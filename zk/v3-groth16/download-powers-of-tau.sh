#!/bin/bash
set -e

cd /home/oem/Documents/Coding/Speak-up-appV3/zk/v3-groth16/keys

echo "📥 Downloading Powers of Tau ceremony file..."
echo "   Trying alternative sources..."

# Try Perpetual Powers of Tau (more reliable)
if wget -q --show-progress https://storage.googleapis.com/zkevm/ptau/powersOfTau28_hez_final_21.ptau; then
    echo "✅ Downloaded from Google Cloud Storage"
elif wget -q --show-progress https://github.com/iden3/snarkjs/raw/master/powersoftau/powersOfTau28_hez_final_21.ptau; then
    echo "✅ Downloaded from GitHub"
else
    echo "❌ All sources failed. Generating smaller Powers of Tau locally..."
    echo "   (This will take ~5 minutes but works offline)"
    snarkjs powersoftau new bn128 12 pot12_0000.ptau -v
    snarkjs powersoftau contribute pot12_0000.ptau pot12_0001.ptau --name="First contribution" -v -e="random text"
    snarkjs powersoftau prepare phase2 pot12_0001.ptau powersOfTau28_hez_final_21.ptau -v
    rm pot12_0000.ptau pot12_0001.ptau
    echo "✅ Generated local Powers of Tau (supports up to 2^12 = 4096 constraints)"
fi

echo ""
echo "Powers of Tau ready: $(ls -lh powersOfTau28_hez_final_21.ptau | awk '{print $5}')"
