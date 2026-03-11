#!/bin/bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$ROOT" ]; then
  echo "ERROR: not inside a git repo (can't find repo root)."
  exit 1
fi

VERIFIER_ADDR="${1:-}"

if [ -z "$VERIFIER_ADDR" ]; then
  echo "Usage:"
  echo "  ./verify-groth16-verifier.sh <GROTH16_VERIFIER_ADDR>"
  echo ""
  echo "Example:"
  echo "  ./verify-groth16-verifier.sh 0x25C9A59DC47Ba0869229f02f8d80CC22860bFFBa"
  exit 1
fi

CHAIN_ID=1313161555
BLOCKSCOUT_URL="https://explorer.testnet.aurora.dev/api/v1/"

echo "=== Verify Groth16Verifier on Aurora Testnet ==="
echo "ChainId:  $CHAIN_ID"
echo "Verifier: $VERIFIER_ADDR"
echo ""

cd "$ROOT/contracts"

forge verify-contract \
  "$VERIFIER_ADDR" \
  "src/v3/Groth16Verifier.sol:Groth16Verifier" \
  --chain-id "$CHAIN_ID" \
  --verifier blockscout \
  --verifier-url "$BLOCKSCOUT_URL"

echo ""
echo "✅ Done. Check the Blockscout UI page for the verifier address."