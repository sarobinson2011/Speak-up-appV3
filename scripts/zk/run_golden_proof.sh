#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$ROOT" ]; then
  echo "ERROR: not inside git repo"
  exit 1
fi

cd "$ROOT/zk/v3-groth16"

echo "Running golden proof test..."

if ! command -v node >/dev/null 2>&1; then
  echo "ERROR: node not installed"
  exit 1
fi

node test-golden-proof.js

echo ""
echo "Golden proof verification completed successfully."