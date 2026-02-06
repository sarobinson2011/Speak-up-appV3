#!/bin/bash
set -e

echo "🔨 Compiling Circom Circuit & Setting up Groth16"
echo "================================================"
echo ""

cd /home/oem/Documents/Coding/Speak-up-appV3/zk/v3-groth16

# Step 1: Compile circuit
echo "📝 Compiling sign_petition.circom..."
echo "   (This may take 2-5 minutes for depth-20 Merkle tree)"
cd circuits
circom sign_petition.circom --r1cs --wasm --sym -o ../build
cd ..

echo "✅ Circuit compiled!"
echo "   Files created:"
ls -lh build/sign_petition.r1cs
ls -lh build/sign_petition_js/sign_petition.wasm
echo ""

# Step 2: Get circuit info
echo "📊 Circuit statistics:"
snarkjs r1cs info build/sign_petition.r1cs
echo ""

# Step 3: Download Powers of Tau (if not exists)
cd keys
if [ ! -f "powersOfTau28_hez_final_21.ptau" ]; then
    echo "📥 Downloading Powers of Tau ceremony file..."
    echo "   (Hermez/Polygon ceremony - 650MB download)"
    wget --show-progress https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_21.ptau
    echo "✅ Powers of Tau downloaded"
else
    echo "✅ Powers of Tau already present"
fi
echo ""

# Step 4: Generate Groth16 setup
echo "🔑 Generating Groth16 proving key..."
echo "   (This may take 3-7 minutes)"
snarkjs groth16 setup ../build/sign_petition.r1cs powersOfTau28_hez_final_21.ptau sign_petition_0000.zkey
echo "✅ Initial key generated"
echo ""

# Step 5: Contribute randomness (phase 2)
echo "🎲 Adding randomness to key..."
echo "my random entropy for V3" | snarkjs zkey contribute sign_petition_0000.zkey sign_petition_final.zkey --name="V3 contribution"
rm sign_petition_0000.zkey  # Clean up intermediate file
echo "✅ Final proving key: sign_petition_final.zkey"
echo ""

# Step 6: Export verification key
echo "📤 Exporting verification key..."
snarkjs zkey export verificationkey sign_petition_final.zkey verification_key.json
echo "✅ Verification key exported"
echo ""

# Step 7: Generate Solidity verifier
echo "📜 Generating Solidity verifier contract..."
snarkjs zkey export solidityverifier sign_petition_final.zkey ../contracts/Groth16Verifier.sol
echo "✅ Verifier contract generated"
echo ""

# Step 8: Check sizes
echo "📏 File sizes:"
echo "   Proving key:  $(ls -lh sign_petition_final.zkey | awk '{print $5}')"
echo "   Verifier contract: $(ls -lh ../contracts/Groth16Verifier.sol | awk '{print $5}')"
echo ""

# Check if verifier is under 24KB
verifier_bytes=$(wc -c < ../contracts/Groth16Verifier.sol)
verifier_kb=$(echo "scale=1; $verifier_bytes/1024" | bc)
echo "   Verifier size: ${verifier_kb}KB"
if [ $verifier_bytes -lt 24576 ]; then
    echo "   ✅ UNDER 24KB LIMIT - Will deploy!"
else
    echo "   ⚠️  OVER 24KB LIMIT - May need optimization"
fi
echo ""

# Summary
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Generated files:"
echo "  ✅ build/sign_petition.r1cs"
echo "  ✅ build/sign_petition_js/sign_petition.wasm"
echo "  ✅ keys/sign_petition_final.zkey"
echo "  ✅ keys/verification_key.json"
echo "  ✅ contracts/Groth16Verifier.sol"
echo ""
echo "Next steps:"
echo "  1. Test proof generation (we'll create test script)"
echo "  2. Deploy Groth16Verifier.sol to Aurora testnet"
echo "  3. Integrate frontend proving"
