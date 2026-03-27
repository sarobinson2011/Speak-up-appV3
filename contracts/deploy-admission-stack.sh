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

echo "Using env file: $ENV_FILE"

# shellcheck disable=SC1090
set -a
source "$ENV_FILE"
set +a

: "${AURORA_TESTNET_RPC:=https://testnet.aurora.dev}"
: "${OWNER_ADDRESS:?Missing OWNER_ADDRESS in .env}"
: "${ADMISSION_BOND_WEI:?Missing ADMISSION_BOND_WEI in .env}"
: "${ADMISSION_LOCK_SECONDS:?Missing ADMISSION_LOCK_SECONDS in .env}"

cd "$ROOT/contracts"

echo "=== Deploying Admission Stack to Aurora Testnet ==="
echo "RPC:         $AURORA_TESTNET_RPC"
echo "ChainId:     1313161555"
echo "Owner:       $OWNER_ADDRESS"
echo "Deployer:    $(cast wallet address --account dev)"
echo "BondWei:     $ADMISSION_BOND_WEI"
echo "LockSeconds: $ADMISSION_LOCK_SECONDS"
echo ""

echo "-> Step 1: Deploy Poseidon hashes..."
forge script script/DeployPoseidonHashes.s.sol:DeployPoseidonHashes \
  --rpc-url "$AURORA_TESTNET_RPC" \
  --account dev \
  --broadcast \
  --legacy \
  --with-gas-price 1000000000 \
  -vvv

echo ""
echo "Set these in repo-root .env, then press Enter:"
echo "POSEIDON1_ADDRESS=0x..."
echo "POSEIDON2_ADDRESS=0x..."
read -r

# shellcheck disable=SC1090
set -a
source "$ENV_FILE"
set +a

: "${POSEIDON1_ADDRESS:?Missing POSEIDON1_ADDRESS in .env}"
: "${POSEIDON2_ADDRESS:?Missing POSEIDON2_ADDRESS in .env}"

echo ""
echo "-> Step 2: Deploy AnonymousMembershipRegistry..."
forge script script/DeployAnonymousMembershipRegistry.s.sol:DeployAnonymousMembershipRegistry \
  --rpc-url "$AURORA_TESTNET_RPC" \
  --account dev \
  --broadcast \
  --legacy \
  --with-gas-price 1000000000 \
  -vvv

echo ""
echo "Set these in repo-root .env, then press Enter:"
echo "ANON_MEMBERSHIP_LOGIC_ADDRESS=0x..."
echo "ANON_MEMBERSHIP_PROXY_ADDRESS=0x..."
read -r

# shellcheck disable=SC1090
set -a
source "$ENV_FILE"
set +a

: "${ANON_MEMBERSHIP_LOGIC_ADDRESS:?Missing ANON_MEMBERSHIP_LOGIC_ADDRESS in .env}"
: "${ANON_MEMBERSHIP_PROXY_ADDRESS:?Missing ANON_MEMBERSHIP_PROXY_ADDRESS in .env}"

echo ""
echo "-> Step 3: Deploy AdmissionRegistry..."
forge script script/DeployAdmissionRegistry.s.sol:DeployAdmissionRegistry \
  --rpc-url "$AURORA_TESTNET_RPC" \
  --account dev \
  --broadcast \
  --legacy \
  --with-gas-price 1000000000 \
  -vvv

echo ""
echo "Set these in repo-root .env, then press Enter:"
echo "ADMISSION_LOGIC_ADDRESS=0x..."
echo "ADMISSION_PROXY_ADDRESS=0x..."
read -r

# shellcheck disable=SC1090
set -a
source "$ENV_FILE"
set +a

: "${ADMISSION_LOGIC_ADDRESS:?Missing ADMISSION_LOGIC_ADDRESS in .env}"
: "${ADMISSION_PROXY_ADDRESS:?Missing ADMISSION_PROXY_ADDRESS in .env}"

echo ""
echo "-> Step 4: Link AdmissionRegistry into AnonymousMembershipRegistry..."
forge script script/LinkAdmissionRegistry.s.sol:LinkAdmissionRegistry \
  --rpc-url "$AURORA_TESTNET_RPC" \
  --account dev \
  --broadcast \
  --legacy \
  --with-gas-price 1000000000 \
  -vvv

echo ""
echo "✅ Admission stack deployment flow complete."
echo ""
echo "Next recommended manual checks:"
echo "  cast call $ANON_MEMBERSHIP_PROXY_ADDRESS \"owner()(address)\" --rpc-url $AURORA_TESTNET_RPC"
echo "  cast call $ANON_MEMBERSHIP_PROXY_ADDRESS \"hasher()(address)\" --rpc-url $AURORA_TESTNET_RPC"
echo "  cast call $ANON_MEMBERSHIP_PROXY_ADDRESS \"admissionRegistry()(address)\" --rpc-url $AURORA_TESTNET_RPC"
echo "  cast call $ADMISSION_PROXY_ADDRESS \"owner()(address)\" --rpc-url $AURORA_TESTNET_RPC"
echo "  cast call $ADMISSION_PROXY_ADDRESS \"anonymousMembershipRegistry()(address)\" --rpc-url $AURORA_TESTNET_RPC"
echo "  cast call $ADMISSION_PROXY_ADDRESS \"admissionHasher()(address)\" --rpc-url $AURORA_TESTNET_RPC"
echo "  cast call $ADMISSION_PROXY_ADDRESS \"admissionBond()(uint256)\" --rpc-url $AURORA_TESTNET_RPC"
echo "  cast call $ADMISSION_PROXY_ADDRESS \"lockPeriod()(uint256)\" --rpc-url $AURORA_TESTNET_RPC"