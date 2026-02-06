#!/bin/bash

echo "Installing Groth16/Circom dependencies..."

# Install SnarkJS globally
npm install -g snarkjs

# Install Circom compiler
# Check if already installed
if command -v circom &> /dev/null; then
    echo "✅ Circom already installed: $(circom --version)"
else
    echo "Installing Circom..."
    # For Ubuntu/Linux
    curl -L https://github.com/iden3/circom/releases/download/v2.1.6/circom-linux-amd64 -o /tmp/circom
    chmod +x /tmp/circom
    sudo mv /tmp/circom /usr/local/bin/circom
    echo "✅ Circom installed: $(circom --version)"
fi

# Install circomlib (circuit library)
cd /home/oem/Documents/Coding/Speak-up-appV3/circuits-v3
npm init -y
npm install --save circomlib

echo "✅ All dependencies installed!"
echo ""
echo "Verify installations:"
echo "  snarkjs version: $(snarkjs --version)"
echo "  circom version: $(circom --version)"
