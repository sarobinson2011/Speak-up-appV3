#!/usr/bin/env bash
set -euo pipefail

# --- resolve repo root ---
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${ROOT}" ]]; then
  echo "ERROR: not inside a git repo (can't find repo root)."
  exit 1
fi

CONTRACTS_DIR="${ROOT}/contracts"

# --- load env from root or contracts ---
ENV_ROOT="${ROOT}/.env"
ENV_CONTRACTS="${CONTRACTS_DIR}/.env"

if [[ -f "${ENV_ROOT}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_ROOT}"
elif [[ -f "${ENV_CONTRACTS}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_CONTRACTS}"
else
  echo "ERROR: .env not found at ${ENV_ROOT} or ${ENV_CONTRACTS}"
  exit 1
fi

# --- defaults / sanity ---
: "${AURORA_TESTNET_RPC:=https://testnet.aurora.dev}"
: "${MEMBERSHIP_REGISTER_BOND_WEI:?missing MEMBERSHIP_REGISTER_BOND_WEI}"
: "${MEMBERSHIP_BOND_LOCK_SECONDS:?missing MEMBERSHIP_BOND_LOCK_SECONDS}"

ACCOUNT="${ACCOUNT:-dev-deployer}"
CHAIN_ID="${CHAIN_ID:-1313161555}"
VERIFIER_URL="${VERIFIER_URL:-https://explorer.testnet.aurora.dev/api/v1/}"

cd "${CONTRACTS_DIR}"

cmd="${1:-}"
case "${cmd}" in
  membership:deploy)
    echo "=== Deploying Membership (Poseidon2 + MembershipRegistry) ==="
    echo "RPC: ${AURORA_TESTNET_RPC}"
    echo "ChainId: ${CHAIN_ID}"
    echo "Account: ${ACCOUNT}"
    echo "BondWei: ${MEMBERSHIP_REGISTER_BOND_WEI}"
    echo "LockSeconds: ${MEMBERSHIP_BOND_LOCK_SECONDS}"
    echo

    forge script script/DeployMembership.s.sol:DeployMembership \
      --rpc-url "${AURORA_TESTNET_RPC}" \
      --account "${ACCOUNT}" \
      --broadcast \
      --legacy \
      -vv
    ;;

  membership:verify)
    POSEIDON_ADDR="${2:-}"
    REGISTRY_ADDR="${3:-}"
    if [[ -z "${POSEIDON_ADDR}" || -z "${REGISTRY_ADDR}" ]]; then
      echo "Usage: $0 membership:verify <POSEIDON2_ADDR> <MEMBERSHIP_REGISTRY_ADDR>"
      exit 1
    fi

    echo "=== Verifying Membership contracts ==="
    echo "Poseidon2: ${POSEIDON_ADDR}"
    echo "MembershipRegistry: ${REGISTRY_ADDR}"
    echo

    forge verify-contract \
      "${POSEIDON_ADDR}" \
      "src/poseidon/Poseidon2.sol:Poseidon2" \
      --chain-id "${CHAIN_ID}" \
      --verifier blockscout \
      --verifier-url "${VERIFIER_URL}"

    forge verify-contract \
      "${REGISTRY_ADDR}" \
      "src/MembershipRegistry.sol:MembershipRegistry" \
      --chain-id "${CHAIN_ID}" \
      --verifier blockscout \
      --verifier-url "${VERIFIER_URL}"
    ;;

  membership:deploy-verify)
    echo "Run deploy, then you paste the two addresses into the verify command."
    echo "1) $0 membership:deploy"
    echo "2) $0 membership:verify <POSEIDON2_ADDR> <MEMBERSHIP_REGISTRY_ADDR>"
    ;;

  *)
    echo "Commands:"
    echo "  $0 membership:deploy"
    echo "  $0 membership:verify <POSEIDON2_ADDR> <MEMBERSHIP_REGISTRY_ADDR>"
    echo "  $0 membership:deploy-verify"
    exit 1
    ;;
esac
