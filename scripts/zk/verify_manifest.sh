#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$ROOT" ]; then
  echo "ERROR: not inside a git repo (can't find repo root)." >&2
  exit 1
fi

MANIFEST="$ROOT/ZK_ARTIFACTS_MANIFEST.json"

if [ ! -f "$MANIFEST" ]; then
  echo "ERROR: manifest not found: $MANIFEST" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required." >&2
  exit 1
fi

MODE="verify"
if [ "${1:-}" = "--write" ]; then
  MODE="write"
fi

python3 - "$ROOT" "$MANIFEST" "$MODE" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
manifest_path = Path(sys.argv[2])
mode = sys.argv[3]

with manifest_path.open("r", encoding="utf-8") as f:
    manifest = json.load(f)

errors = []

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

# Validate artifact paths and compute hashes
for item in manifest.get("artifacts", []):
    rel = item["path"]
    abs_path = root / rel
    if not abs_path.exists():
        errors.append(f"Missing artifact: {rel}")
        continue

    digest = sha256_file(abs_path)

    if mode == "write":
        item["sha256"] = digest
    else:
        recorded = item.get("sha256", "")
        if not recorded:
            errors.append(f"Missing sha256 in manifest for: {rel}")
        elif recorded != digest:
            errors.append(
                f"Hash mismatch for {rel}\n"
                f"  manifest: {recorded}\n"
                f"  actual:   {digest}"
            )

# Validate byte-for-byte consistency pairs
for check in manifest.get("consistency_checks", []):
    left_rel = check["left"]
    right_rel = check["right"]
    left = root / left_rel
    right = root / right_rel

    if not left.exists():
        errors.append(f"Consistency check missing left file: {left_rel}")
        continue
    if not right.exists():
        errors.append(f"Consistency check missing right file: {right_rel}")
        continue

    left_hash = sha256_file(left)
    right_hash = sha256_file(right)

    if left_hash != right_hash:
        errors.append(
            f"Consistency check failed: {check['name']}\n"
            f"  left:  {left_rel}  {left_hash}\n"
            f"  right: {right_rel}  {right_hash}"
        )

if mode == "write":
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print(f"Wrote hashes into {manifest_path}")
    sys.exit(0)

if errors:
    print("ZK artifact manifest verification FAILED:\n", file=sys.stderr)
    for err in errors:
        print(f"- {err}", file=sys.stderr)
    sys.exit(1)

print("ZK artifact manifest verification PASSED.")
PY