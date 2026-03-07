#!/usr/bin/env python3
import datetime
import json
import os
import pathlib
import subprocess
import sys
import textwrap
from typing import Any, Dict, List, Set

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
LOG_DIR = pathlib.Path.home() / "ws" / "notes" / "agent" / "logs" / "autopatch"
LOG_DIR.mkdir(parents=True, exist_ok=True)

MODEL = os.environ.get("AGENT_MODEL", "gpt-5.2-codex")
REASONING_EFFORT = os.environ.get("AGENT_REASONING", "medium")


def sh(
    cmd: List[str],
    check: bool = True,
    capture: bool = True,
    cwd: pathlib.Path = REPO_ROOT,
) -> str:
    p = subprocess.run(
        cmd,
        cwd=str(cwd),
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )
    return p.stdout or ""


def now_utc_compact() -> str:
    # e.g. 20260305T105817Z0000
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    return ts.replace("-", "").replace(":", "").replace("+", "Z")


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def read_file(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def git_branch() -> str:
    return sh(["git", "branch", "--show-current"]).strip()


def assert_not_main(branch: str) -> None:
    if branch in ("main", "master", ""):
        die(f"Refusing to run on branch '{branch or '<detached>'}'")


def assert_clean_worktree() -> None:
    s = sh(["git", "status", "--porcelain"]).strip()
    if s:
        die("Working tree not clean. Commit/stash/discard first.")


def parse_allowed_files() -> Set[str]:
    raw = os.environ.get("AGENT_ALLOWED_FILES", "").strip()
    if not raw:
        return set()
    return {p.strip() for p in raw.split(",") if p.strip()}


def gather_context(allowed_files: Set[str]) -> Dict[str, Any]:
    base_files = [
        # keep these always
        "AGENT_POLICY.md",
        "AGENT_TASK.md",
        "docs/iter-0001-path-privacy-v1.md",
    ]
    files = base_files + sorted(list(allowed_files))

    ctx: Dict[str, Any] = {"files": {}, "git": {}}
    for f in files:
        p = REPO_ROOT / f
        if p.exists():
            ctx["files"][f] = read_file(p)

    ctx["git"]["branch"] = git_branch()
    ctx["git"]["head"] = sh(["git", "rev-parse", "HEAD"]).strip()
    ctx["git"]["status_sb"] = sh(["git", "status", "-sb"])
    return ctx


def call_model(messages: List[Dict[str, Any]]) -> str:
    from openai import OpenAI

    timeout_s = float(os.environ.get("AGENT_TIMEOUT_S", "90"))
    max_retries = int(os.environ.get("AGENT_MAX_RETRIES", "0"))

    # hard limits so the agent never hangs indefinitely
    client = OpenAI(timeout=timeout_s, max_retries=max_retries)

    resp = client.responses.create(
        model=MODEL,
        reasoning={"effort": REASONING_EFFORT},
        input=messages,
    )

    out: List[str] = []
    for item in resp.output:
        if item.type == "message":
            for c in item.content:
                if c.type == "output_text":
                    out.append(c.text)
    return "\n".join(out).strip()


def main() -> None:
    branch = git_branch()
    assert_not_main(branch)
    assert_clean_worktree()

    if not os.environ.get("OPENAI_API_KEY"):
        die("OPENAI_API_KEY not set in environment.")

    allowed_files = parse_allowed_files()
    if not allowed_files:
        die(
            "AGENT_ALLOWED_FILES is required (comma-separated paths). Example: frontend/src/Petitions.jsx"
        )

    # Basic existence check: fail fast if user points to nonsense paths
    for p in sorted(allowed_files):
        if not (REPO_ROOT / p).exists():
            die(f"Allowed file does not exist: {p}")

    ctx = gather_context(allowed_files)

    run_id = f"{now_utc_compact()}0000-{branch.replace('/', '_')}"
    run_dir = LOG_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "context.json").write_text(json.dumps(ctx, indent=2), encoding="utf-8")

    allowed_list = "\n".join(f"- {p}" for p in sorted(allowed_files))

    system = {
        "role": "system",
        "content": textwrap.dedent(
            f"""
            You are a patch-generating engineering agent operating inside a git repo.

            OUTPUT FORMAT (strict):
            Return ONLY valid JSON with this shape:
              {{
                "files": {{
                  "<path>": "<entire updated file contents as a single string>"
                }}
              }}

            HARD RULES:
            - Do NOT output unified diffs.
            - Do NOT include prose, markdown, code fences, or extra keys.
            - You may ONLY modify/output these files:
            {allowed_list}
            - The JSON "files" object MUST NOT contain any other paths.
            - Keep changes minimal and consistent with AGENT_TASK + work package.
            - If you cannot comply, return: {{"files": {{}}}}
            """
        ).strip(),
    }

    user = {
        "role": "user",
        "content": json.dumps(
            {
                "task": "Apply the current work package using JSON edit mode and only the allowed files.",
                "work_package": ctx["files"].get(
                    "docs/iter-0001-path-privacy-v1.md", ""
                ),
                "policy": ctx["files"].get("AGENT_POLICY.md", ""),
                "agent_task": ctx["files"].get("AGENT_TASK.md", ""),
                "allowed_files": sorted(list(allowed_files)),
                "current_files": {
                    p: ctx["files"].get(p, "") for p in sorted(list(allowed_files))
                },
            },
            indent=2,
        ),
    }

    last_err = ""
    hard_tries = int(os.environ.get("AGENT_HARD_TRIES", "3"))

    for attempt in range(1, hard_tries + 1):
        extra = ""
        if attempt > 1:
            extra = f"\n\nPrevious error: {last_err}\nReturn STRICT JSON only, with only allowed files."

        sys_msg = {"role": "system", "content": system["content"] + extra}

        try:
            raw = call_model([sys_msg, user])
            (run_dir / f"model_output.attempt{attempt}.json").write_text(
                raw + "\n", encoding="utf-8"
            )

            data = json.loads(raw)
            files_obj = data.get("files", {})
            if not isinstance(files_obj, dict):
                raise RuntimeError("bad_json_shape_files_not_object")

            out_files = set(files_obj.keys())
            bad = sorted(out_files - allowed_files)
            if bad:
                raise RuntimeError(
                    "output_contains_disallowed_files: " + ", ".join(bad)
                )

            # Empty output means model refused / couldn't comply
            if not files_obj:
                raise RuntimeError("model_returned_empty_files")

            for rel_path, new_text in files_obj.items():
                if not isinstance(new_text, str) or not new_text.strip():
                    raise RuntimeError(f"empty_or_nonstring_content_for: {rel_path}")
                (REPO_ROOT / rel_path).write_text(new_text, encoding="utf-8")

            # Apply succeeded: break out
            break

        except Exception as e:
            last_err = str(e)
            if attempt == hard_tries:
                die("JSON edit mode failed after retries. See logs in: " + str(run_dir))

    # Stage + check
    sh(["git", "add", "-A"], capture=True)

    check_out = sh(["./agent/check"], check=False, capture=True)
    (run_dir / "check.log").write_text(check_out, encoding="utf-8")
    if "[check] Running repo checks..." not in check_out:
        die("agent/check failed. See: " + str(run_dir))

    staged = sh(["git", "diff", "--cached"], capture=True)
    (run_dir / "staged.diff").write_text(staged, encoding="utf-8")

    print(f"OK: patch applied + staged on {branch}")
    print("Review: git diff --cached")
    print(f"Logs: {run_dir}")


if __name__ == "__main__":
    main()
