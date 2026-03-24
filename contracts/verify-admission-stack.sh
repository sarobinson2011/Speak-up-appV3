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
: "${POSEIDON1_ADDRESS:?Missing POSEIDON1_ADDRESS in .env}"
: "${POSEIDON2_ADDRESS:?Missing POSEIDON2_ADDRESS in .env}"
: "${ANON_MEMBERSHIP_LOGIC_ADDRESS:?Missing ANON_MEMBERSHIP_LOGIC_ADDRESS in .env}"
: "${ANON_MEMBERSHIP_PROXY_ADDRESS:?Missing ANON_MEMBERSHIP_PROXY_ADDRESS in .env}"
: "${ADMISSION_LOGIC_ADDRESS:?Missing ADMISSION_LOGIC_ADDRESS in .env}"
: "${ADMISSION_PROXY_ADDRESS:?Missing ADMISSION_PROXY_ADDRESS in .env}"

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; exit 1; }

assert_eq() {
  local actual expected label
  actual="$(echo "$1" | tr '[:upper:]' '[:lower:]')"
  expected="$(echo "$2" | tr '[:upper:]' '[:lower:]')"
  label="$3"

  if [ "$actual" != "$expected" ]; then
    echo "FAIL: $label"
    echo "  expected: $expected"
    echo "  actual:   $actual"
    exit 1
  fi
  echo "PASS: $label -> $1"
}

assert_nonempty_code() {
  local addr label code
  addr="$1"
  label="$2"
  code="$(cast code "$addr" --rpc-url "$AURORA_TESTNET_RPC")"
  if [ -z "$code" ] || [ "$code" = "0x" ]; then
    fail "$label has no deployed bytecode at $addr"
  fi
  pass "$label has bytecode at $addr"
}

echo "=== Verify Admission Stack on Aurora Testnet ==="
echo "RPC:         $AURORA_TESTNET_RPC"
echo "ChainId:     1313161555"
echo "Owner:       $OWNER_ADDRESS"
echo "BondWei:     $ADMISSION_BOND_WEI"
echo "LockSeconds: $ADMISSION_LOCK_SECONDS"
echo ""

echo "-> Check 1: Bytecode present"
assert_nonempty_code "$POSEIDON1_ADDRESS" "Poseidon1"
assert_nonempty_code "$POSEIDON2_ADDRESS" "Poseidon2"
assert_nonempty_code "$ANON_MEMBERSHIP_LOGIC_ADDRESS" "AnonymousMembershipRegistry logic"
assert_nonempty_code "$ANON_MEMBERSHIP_PROXY_ADDRESS" "AnonymousMembershipRegistry proxy"
assert_nonempty_code "$ADMISSION_LOGIC_ADDRESS" "AdmissionRegistry logic"
assert_nonempty_code "$ADMISSION_PROXY_ADDRESS" "AdmissionRegistry proxy"
echo ""

echo "-> Check 2: AnonymousMembershipRegistry proxy state"
membership_owner="$(cast call "$ANON_MEMBERSHIP_PROXY_ADDRESS" "owner()(address)" --rpc-url "$AURORA_TESTNET_RPC")"
membership_hasher="$(cast call "$ANON_MEMBERSHIP_PROXY_ADDRESS" "hasher()(address)" --rpc-url "$AURORA_TESTNET_RPC")"
membership_admission="$(cast call "$ANON_MEMBERSHIP_PROXY_ADDRESS" "admissionRegistry()(address)" --rpc-url "$AURORA_TESTNET_RPC")"

assert_eq "$membership_owner" "$OWNER_ADDRESS" "membership.owner"
assert_eq "$membership_hasher" "$POSEIDON2_ADDRESS" "membership.hasher"
assert_eq "$membership_admission" "$ADMISSION_PROXY_ADDRESS" "membership.admissionRegistry"
echo ""

echo "-> Check 3: AdmissionRegistry proxy state"
admission_owner="$(cast call "$ADMISSION_PROXY_ADDRESS" "owner()(address)" --rpc-url "$AURORA_TESTNET_RPC")"
admission_membership="$(cast call "$ADMISSION_PROXY_ADDRESS" "anonymousMembershipRegistry()(address)" --rpc-url "$AURORA_TESTNET_RPC")"
admission_hasher="$(cast call "$ADMISSION_PROXY_ADDRESS" "admissionHasher()(address)" --rpc-url "$AURORA_TESTNET_RPC")"
admission_bond="$(cast call "$ADMISSION_PROXY_ADDRESS" "admissionBond()(uint256)" --rpc-url "$AURORA_TESTNET_RPC" | awk '{print $1}')"
admission_lock="$(cast call "$ADMISSION_PROXY_ADDRESS" "lockPeriod()(uint256)" --rpc-url "$AURORA_TESTNET_RPC" | awk '{print $1}')"

assert_eq "$admission_owner" "$OWNER_ADDRESS" "admission.owner"
assert_eq "$admission_membership" "$ANON_MEMBERSHIP_PROXY_ADDRESS" "admission.anonymousMembershipRegistry"
assert_eq "$admission_hasher" "$POSEIDON1_ADDRESS" "admission.admissionHasher"
assert_eq "$admission_bond" "$ADMISSION_BOND_WEI" "admission.admissionBond"
assert_eq "$admission_lock" "$ADMISSION_LOCK_SECONDS" "admission.lockPeriod"
echo ""

echo "-> Check 4: Summary"
echo "PASS: Full admission stack verified against repo-root .env"
echo ""
echo "Canonical addresses:"
echo "  POSEIDON1_ADDRESS=$POSEIDON1_ADDRESS"
echo "  POSEIDON2_ADDRESS=$POSEIDON2_ADDRESS"
echo "  ANON_MEMBERSHIP_LOGIC_ADDRESS=$ANON_MEMBERSHIP_LOGIC_ADDRESS"
echo "  ANON_MEMBERSHIP_PROXY_ADDRESS=$ANON_MEMBERSHIP_PROXY_ADDRESS"
echo "  ADMISSION_LOGIC_ADDRESS=$ADMISSION_LOGIC_ADDRESS"
echo "  ADMISSION_PROXY_ADDRESS=$ADMISSION_PROXY_ADDRESS"