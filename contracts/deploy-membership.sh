#!/bin/bash
set -euo pipefail

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

source "$ENV_FILE"

echo "=== Deploying Membership (Poseidon2 + MembershipRegistry) to Aurora Testnet ==="
echo "RPC: https://testnet.aurora.dev"
echo "ChainId: 1313161555"
echo "Deployer: $(cast wallet address --account dev-deployer)"
echo "BondWei: ${MEMBERSHIP_REGISTER_BOND_WEI}"
echo "LockSeconds: ${MEMBERSHIP_BOND_LOCK_SECONDS}"
echo ""

forge script script/DeployMembership.s.sol:DeployMembership \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --broadcast \
  --legacy \
  -vv
