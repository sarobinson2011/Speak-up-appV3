#!/bin/bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$ROOT" ]; then
  echo "ERROR: not inside a git repo (can't find repo root)."
  exit 1
fi

ENV_FILE="$ROOT/.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "ERROR: $ENV_FILE not found."
  echo "Create it (or copy from .env.example) at repo root: $ROOT"
  exit 1
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

# ---- required env ----
: "${AURORA_TESTNET_RPC:=https://testnet.aurora.dev}"
: "${MEMBERSHIP_REGISTER_BOND_WEI:?Missing MEMBERSHIP_REGISTER_BOND_WEI in .env}"
: "${MEMBERSHIP_BOND_LOCK_SECONDS:?Missing MEMBERSHIP_BOND_LOCK_SECONDS in .env}"

# ---- args ----
POSEIDON2_ADDR="${1:-}"
MEMBERSHIP_ADDR="${2:-}"

if [ -z "$POSEIDON2_ADDR" ] || [ -z "$MEMBERSHIP_ADDR" ]; then
  echo "Usage:"
  echo "  ./verify-membership.sh <POSEIDON2_ADDR> <MEMBERSHIP_REGISTRY_ADDR>"
  echo ""
  echo "Example:"
  echo "  ./verify-membership.sh 0xEFbb... 0x7C32..."
  exit 1
fi

CHAIN_ID=1313161555
BLOCKSCOUT_URL="https://explorer.testnet.aurora.dev/api/v1/"

echo "=== Verify Membership on Aurora Testnet ==="
echo "RPC:        $AURORA_TESTNET_RPC"
echo "ChainId:    $CHAIN_ID"
echo "Poseidon2:  $POSEIDON2_ADDR"
echo "Registry:   $MEMBERSHIP_ADDR"
echo "BondWei:    $MEMBERSHIP_REGISTER_BOND_WEI"
echo "LockSeconds:${MEMBERSHIP_BOND_LOCK_SECONDS}"
echo ""

cd "$ROOT/contracts"

echo "-> Verifying Poseidon2..."
forge verify-contract \
  "$POSEIDON2_ADDR" \
  "src/poseidon/Poseidon2.sol:Poseidon2" \
  --chain-id "$CHAIN_ID" \
  --verifier blockscout \
  --verifier-url "$BLOCKSCOUT_URL"

echo ""
echo "-> Verifying MembershipRegistry (constructor args: hasher,bondWei,lockSeconds)..."

# ABI-encode constructor args exactly as deployed:
# constructor(address _hasher, uint256 _registerBondWei, uint64 _bondLockSeconds)
CTOR_ARGS="$(cast abi-encode "constructor(address,uint256,uint64)" \
  "$POSEIDON2_ADDR" \
  "$MEMBERSHIP_REGISTER_BOND_WEI" \
  "$MEMBERSHIP_BOND_LOCK_SECONDS")"

forge verify-contract \
  "$MEMBERSHIP_ADDR" \
  "src/MembershipRegistry.sol:MembershipRegistry" \
  --chain-id "$CHAIN_ID" \
  --verifier blockscout \
  --verifier-url "$BLOCKSCOUT_URL" \
  --constructor-args "$CTOR_ARGS"

echo ""
echo "✅ Done. Check the Blockscout UI pages for both addresses."
