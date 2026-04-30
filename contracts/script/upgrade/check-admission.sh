#!/usr/bin/env bash
set -e

RPC="https://testnet.aurora.dev"
PROXY="0x36c22227098B24E5aCE48dEa3988327256481F0e"

COMMITMENT="0x0c61c6c3b7ba331900a3fe814bfa8494e51b53fb8e531c140664b38179b16c66"

echo "== Pre-upgrade gate =="
PRE=$(cast call $PROXY "getStatus(bytes32)(uint8)" $COMMITMENT --rpc-url $RPC)
echo "status before: $PRE"

echo ""
echo "== After you run upgrade, press enter =="
read

echo "== Post-upgrade gate =="
POST=$(cast call $PROXY "getStatus(bytes32)(uint8)" $COMMITMENT --rpc-url $RPC)
echo "status after: $POST"

if [ "$PRE" != "$POST" ]; then
  echo "❌ STORAGE CORRUPTION DETECTED"
  exit 1
else
  echo "✅ Upgrade safe"
fi