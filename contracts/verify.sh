#!/bin/bash
# Auto-load env and verify contract

source ../.env

forge verify-contract \
  "$1" \
  "$2" \
  --chain-id 1313161555 \
  --verifier blockscout \
  --verifier-url https://explorer.testnet.aurora.dev/api/v1/

  # to use
  #
  # ./verify.sh 0xADDRESS src/Contract.sol:ContractName
  #
  # $1 - address of contract to be verified
  # $2 - source contract code deployed at the address

