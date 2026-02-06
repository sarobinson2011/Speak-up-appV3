#!/bin/bash
# Test golden proof on-chain using cast

VERIFIER_ADDRESS=$1
TEST_CONTRACT=$2

if [ -z "$VERIFIER_ADDRESS" ] || [ -z "$TEST_CONTRACT" ]; then
    echo "Usage: ./test-on-chain.sh <VERIFIER_ADDRESS> <TEST_CONTRACT>"
    exit 1
fi

# Use actual RPC URL
RPC_URL="https://testnet.aurora.dev"

echo "🧪 Testing Golden Proof On-Chain"
echo "================================="
echo ""
echo "Verifier:      $VERIFIER_ADDRESS"
echo "Test Contract: $TEST_CONTRACT"
echo ""

# Check golden-proof.json exists
if [ ! -f "golden-proof.json" ]; then
    echo "❌ golden-proof.json not found!"
    echo "Run: node test-golden-proof.js first"
    exit 1
fi

# Extract calldata from JSON
PA_0=$(jq -r '.calldata[0][0]' golden-proof.json)
PA_1=$(jq -r '.calldata[0][1]' golden-proof.json)

PB_00=$(jq -r '.calldata[1][0][0]' golden-proof.json)
PB_01=$(jq -r '.calldata[1][0][1]' golden-proof.json)
PB_10=$(jq -r '.calldata[1][1][0]' golden-proof.json)
PB_11=$(jq -r '.calldata[1][1][1]' golden-proof.json)

PC_0=$(jq -r '.calldata[2][0]' golden-proof.json)
PC_1=$(jq -r '.calldata[2][1]' golden-proof.json)

PUB_0=$(jq -r '.calldata[3][0]' golden-proof.json)
PUB_1=$(jq -r '.calldata[3][1]' golden-proof.json)
PUB_2=$(jq -r '.calldata[3][2]' golden-proof.json)

echo "📊 Public Signals:"
echo "   [0] nullifier:       $PUB_0"
echo "   [1] petitionId:      $PUB_1"
echo "   [2] membershipRoot:  $PUB_2"
echo ""

# Test 1: View function (read-only, no gas)
echo "🔍 Test 1: Read-only verification (view function)..."
RESULT=$(cast call $TEST_CONTRACT \
    "verifyProof(uint256[2],uint256[2][2],uint256[2],uint256[3])" \
    "[$PA_0,$PA_1]" \
    "[[$PB_00,$PB_01],[$PB_10,$PB_11]]" \
    "[$PC_0,$PC_1]" \
    "[$PUB_0,$PUB_1,$PUB_2]" \
    --rpc-url $RPC_URL)

if [ "$RESULT" = "0x0000000000000000000000000000000000000000000000000000000000000001" ]; then
    echo "   ✅ Read-only verification PASSED!"
else
    echo "   ❌ Read-only verification FAILED!"
    echo "   Result: $RESULT"
    exit 1
fi
echo ""

# Test 2: State-changing transaction (requires gas)
echo "💰 Test 2: On-chain transaction (testGoldenProof)..."
echo "   This will cost gas and emit an event..."

cast send $TEST_CONTRACT \
    "testGoldenProof(uint256[2],uint256[2][2],uint256[2],uint256[3])" \
    "[$PA_0,$PA_1]" \
    "[[$PB_00,$PB_01],[$PB_10,$PB_11]]" \
    "[$PC_0,$PC_1]" \
    "[$PUB_0,$PUB_1,$PUB_2]" \
    --rpc-url $RPC_URL \
    --private-key $PRIVATE_KEY

if [ $? -eq 0 ]; then
    echo ""
    echo "   ✅ Transaction SUCCEEDED!"
    echo ""
    
    # Check counter
    COUNT=$(cast call $TEST_CONTRACT "successfulVerifications()" --rpc-url $RPC_URL)
    echo "📈 Successful verifications: $COUNT"
else
    echo ""
    echo "   ❌ Transaction FAILED!"
    exit 1
fi

echo ""
echo "🎉 PHASE 2 COMPLETE!"
echo "==================="
echo "On-chain verification works!"
echo ""
echo "Next: Phase 3 - Browser proof generation"
