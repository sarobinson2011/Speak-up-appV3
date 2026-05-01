#!/usr/bin/env bash
set -euo pipefail

: "${RPC_URL:=https://testnet.aurora.dev}"
: "${PETITION_REGISTRY_ADDRESS:=0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD}"
: "${ADMISSION_PROXY_ADDRESS:=0x36c22227098B24E5aCE48dEa3988327256481F0e}"

echo "PetitionRegistry gate"
echo "RPC_URL=$RPC_URL"
echo "PETITION_REGISTRY_ADDRESS=$PETITION_REGISTRY_ADDRESS"
echo "ADMISSION_PROXY_ADDRESS=$ADMISSION_PROXY_ADDRESS"

echo
echo "== Core state =="

petition_count="$(cast call "$PETITION_REGISTRY_ADDRESS" "petitionCount()(uint256)" --rpc-url "$RPC_URL" | awk '{print $1}')"
admission_registry="$(cast call "$PETITION_REGISTRY_ADDRESS" "admissionRegistry()(address)" --rpc-url "$RPC_URL")"
has_signed_11="$(cast call "$PETITION_REGISTRY_ADDRESS" "hasSignedPetition(uint256,bytes32)(bool)" 11 0x00 --rpc-url "$RPC_URL" 2>/dev/null || true)"

echo "petitionCount=$petition_count"
echo "admissionRegistry=$admission_registry"

if [[ "$admission_registry" != "$ADMISSION_PROXY_ADDRESS" ]]; then
  echo "ERROR: admissionRegistry mismatch"
  exit 1
fi

echo
echo "== Known Engineering[17] petition existence =="

# Petition 11 should exist from the validated Engineering[17] flow.
petition_11="$(cast call "$PETITION_REGISTRY_ADDRESS" "petitions(uint256)(address,uint256,string,bool)" 11 --rpc-url "$RPC_URL")"
echo "$petition_11"

if ! echo "$petition_11" | grep -q "true"; then
  echo "ERROR: petition 11 does not appear to exist"
  exit 1
fi

echo
echo "PetitionRegistry gate passed"
