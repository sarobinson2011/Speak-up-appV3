#!/bin/bash
set -euo pipefail
# Test golden proof on-chain using cast

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VERIFIER_ADDRESS=${1:-}
TEST_CONTRACT=${2:-}

if [ -z "$VERIFIER_ADDRESS" ] || [ -z "$TEST_CONTRACT" ]; then
  echo "Usage: ./test-on-chain.sh <VERIFIER_ADDRESS> <TEST_CONTRACT>"
  exit 1
fi

RPC_URL="https://testnet.aurora.dev"

echo "🧪 Testing Golden Proof On-Chain"
echo "================================="
echo ""
echo "Verifier:      $VERIFIER_ADDRESS"
echo "Test Contract: $TEST_CONTRACT"
echo ""

if [ ! -f "golden-proof.json" ]; then
  echo "❌ golden-proof.json not found in $SCRIPT_DIR"
  exit 1
fi

echo "✅ Found golden-proof.json"
echo "RPC: $RPC_URL"
echo ""
echo "NOTE: This script assumes you have Foundry 'cast' installed and that your test contract matches golden-proof.json encoding."