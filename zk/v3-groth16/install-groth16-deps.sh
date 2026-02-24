#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing Groth16/Circom dependencies..."

# Install SnarkJS globally (optional). If you prefer local, comment this out.
npm install -g snarkjs

# Install Circom compiler
if command -v circom >/dev/null 2>&1; then
  echo "✅ Circom already installed: $(circom --version)"
else
  echo "Installing Circom..."
  curl -L https://github.com/iden3/circom/releases/download/v2.1.6/circom-linux-amd64 -o /tmp/circom
  chmod +x /tmp/circom
  sudo mv /tmp/circom /usr/local/bin/circom
  echo "✅ Circom installed: $(circom --version)"
fi

# Install node deps for this zk package (circomlib, etc.)
if [ -f package.json ]; then
  npm install
else
  echo "⚠️ package.json not found in $SCRIPT_DIR. Skipping npm install."
fi

echo ""
echo "✅ Dependencies installed!"
echo "Verify:"
echo "  snarkjs: $(command -v snarkjs >/dev/null 2>&1 && snarkjs --version || echo 'use: npx snarkjs')"
echo "  circom:  $(circom --version)"