#!/usr/bin/env python3
import json, os, subprocess, sys, textwrap, pathlib, datetime
from typing import List, Dict, Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
LOG_DIR = pathlib.Path.home() / "ws" / "notes" / "agent" / "logs" / "autopatch"
LOG_DIR.mkdir(parents=True, exist_ok=True)

MODEL = os.environ.get("AGENT_MODEL", "gpt-5.2-codex")
REASONING_EFFORT = os.environ.get("AGENT_REASONING", "high")

def sh(cmd: List[str], check=True, capture=True, cwd=REPO_ROOT) -> str:
    p = subprocess.run(
        cmd,
        cwd=str(cwd),
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )
    return p.stdout or ""

def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

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

def gather_context() -> Dict[str, Any]:
    files = [
        "docs/iter-0001-path-privacy-v1.md",
        "AGENT_POLICY.md",
        "AGENT_TASK.md",
        "backend/src/routes/membership.js",
        "backend/src/membership/indexer.js",
    ]
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
    client = OpenAI()
    resp = client.responses.create(
        model=MODEL,
        reasoning={"effort": REASONING_EFFORT},
        input=messages,
    )
    out = []
    for item in resp.output:
        if item.type == "message":
            for c in item.content:
                if c.type == "output_text":
                    out.append(c.text)
    return "\n".join(out).strip()

def main():
    branch = git_branch()
    assert_not_main(branch)
    assert_clean_worktree()

    if not os.environ.get("OPENAI_API_KEY"):
        die("OPENAI_API_KEY not set in environment.")

    wp = REPO_ROOT / "docs/iter-0001-path-privacy-v1.md"
    if not wp.exists():
        die("Missing work package doc: docs/iter-0001-path-privacy-v1.md")

    ctx = gather_context()

    run_id = f"{now().replace(':','').replace('+','Z').replace('-','')}-{branch.replace('/','_')}"
    run_dir = LOG_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "context.json").write_text(json.dumps(ctx, indent=2), encoding="utf-8")

    system = {
        "role": "system",
        "content": textwrap.dedent("""
        You are a patch-generating engineering agent operating inside a git repo.
        Output ONLY a unified diff (git-style) that applies cleanly with `git apply`.
        Do not include explanations, markdown, or code fences.

        Constraints for this iteration:
        - Backend change only.
        - No circuit changes.
        - No contract changes.
        - Keep old wallet query temporarily, but prefer leaf.
        - 400 if neither wallet nor leaf provided.
        - Return payload unchanged except wallet should be optional/null for leaf-based requests.
        """).strip()
    }

    user = {
        "role": "user",
        "content": json.dumps({
            "task": "iter-0001 backend: add leaf query support to /api/membership/path (prefer leaf over wallet) with minimal reversible changes.",
            "work_package": ctx["files"].get("docs/iter-0001-path-privacy-v1.md", ""),
            "current_membership_route": ctx["files"].get("backend/src/routes/membership.js", ""),
            "current_indexer": ctx["files"].get("backend/src/membership/indexer.js", ""),
        })
    }

    diff_text = call_model([system, user])
    (run_dir / "patch.diff").write_text(diff_text + "\n", encoding="utf-8")

    chk = sh(["git", "apply", "--check", str(run_dir / "patch.diff")], capture=True, check=False)
    (run_dir / "apply_check.log").write_text(chk or "", encoding="utf-8")
    if chk.strip():
        die("Patch does not apply cleanly. See logs in: " + str(run_dir))

    sh(["git", "apply", "--whitespace=fix", str(run_dir / "patch.diff")], capture=True, check=False)
    sh(["git", "add", "-A"], capture=True)

    check_out = sh(["./agent/check"], capture=True, check=False)
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
