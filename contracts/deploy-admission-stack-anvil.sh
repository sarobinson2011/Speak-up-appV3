#!/bin/bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$ROOT" ]; then
  echo "ERROR: not inside a git repo."
  exit 1
fi

ENV_FILE="$ROOT/.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "ERROR: $ENV_FILE not found."
  exit 1
fi

# shellcheck disable=SC1090
set -a
source "$ENV_FILE"
set +a

: "${ANVIL_RPC:=http://127.0.0.1:8545}"
: "${OWNER_ADDRESS:?Missing OWNER_ADDRESS in .env}"
: "${ADMISSION_BOND_WEI:?Missing ADMISSION_BOND_WEI in .env}"
: "${ADMISSION_LOCK_SECONDS:?Missing ADMISSION_LOCK_SECONDS in .env}"

cd "$ROOT/contracts"

echo "=== Deploying Admission Stack to Anvil ==="
echo "RPC:         $ANVIL_RPC"
echo "Owner:       $OWNER_ADDRESS"
echo "BondWei:     $ADMISSION_BOND_WEI"
echo "LockSeconds: $ADMISSION_LOCK_SECONDS"
echo ""

echo "-> Step 1: Deploy Poseidon hashes..."
forge script script/DeployPoseidonHashes.s.sol:DeployPoseidonHashes \
  --rpc-url "$ANVIL_RPC" \
  --account dev \
  --broadcast \
  -vv

echo ""
echo "Set these in .env, then press Enter:"
echo "POSEIDON1_ADDRESS=0x..."
echo "POSEIDON2_ADDRESS=0x..."
read -r

# shellcheck disable=SC1090
source "$ENV_FILE"

: "${POSEIDON1_ADDRESS:?Missing POSEIDON1_ADDRESS in .env}"
: "${POSEIDON2_ADDRESS:?Missing POSEIDON2_ADDRESS in .env}"

echo ""
echo "-> Step 2: Deploy AnonymousMembershipRegistry..."
forge script script/DeployAnonymousMembershipRegistry.s.sol:DeployAnonymousMembershipRegistry \
  --rpc-url "$ANVIL_RPC" \
  --account dev \
  --broadcast \
  -vv

echo ""
echo "Set these in .env, then press Enter:"
echo "ANON_MEMBERSHIP_LOGIC_ADDRESS=0x..."
echo "ANON_MEMBERSHIP_PROXY_ADDRESS=0x..."
read -r

# shellcheck disable=SC1090
source "$ENV_FILE"

: "${ANON_MEMBERSHIP_PROXY_ADDRESS:?Missing ANON_MEMBERSHIP_PROXY_ADDRESS in .env}"

echo ""
echo "-> Step 3: Deploy AdmissionRegistry..."
forge script script/DeployAdmissionRegistry.s.sol:DeployAdmissionRegistry \
  --rpc-url "$ANVIL_RPC" \
  --account dev \
  --broadcast \
  -vv

echo ""
echo "Set these in .env, then press Enter:"
echo "ADMISSION_LOGIC_ADDRESS=0x..."
echo "ADMISSION_PROXY_ADDRESS=0x..."
read -r

# shellcheck disable=SC1090
source "$ENV_FILE"

: "${ADMISSION_PROXY_ADDRESS:?Missing ADMISSION_PROXY_ADDRESS in .env}"

echo ""
echo "-> Step 4: Link AdmissionRegistry into AnonymousMembershipRegistry..."
forge script script/LinkAdmissionRegistry.s.sol:LinkAdmissionRegistry \
  --rpc-url "$ANVIL_RPC" \
  --account dev \
  --broadcast \
  -vv

echo ""
echo "✅ Local Anvil admission stack deployment complete."