#!/bin/bash
set -euo pipefail

# Always run from this script’s directory (portable)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Tooling: prefer global install, fallback to npx for snarkjs
if command -v snarkjs >/dev/null 2>&1; then
  SNARKJS="snarkjs"
else
  SNARKJS="npx snarkjs"
fi

mkdir -p keys
cd keys

echo "📥 Downloading Powers of Tau ceremony file..."
echo "   Trying alternative sources..."

TARGET="powersOfTau28_hez_final_21.ptau"

if [ -f "$TARGET" ]; then
  echo "✅ Powers of Tau already present: $TARGET"
  exit 0
fi

# Try Perpetual Powers of Tau (more reliable)
if wget -q --show-progress "https://storage.googleapis.com/zkevm/ptau/${TARGET}"; then
  echo "✅ Downloaded from Google Cloud Storage"
elif wget -q --show-progress "https://github.com/iden3/snarkjs/raw/master/powersoftau/${TARGET}"; then
  echo "✅ Downloaded from GitHub"
else
  echo "❌ All sources failed. Generating smaller Powers of Tau locally..."
  echo "   (Offline dev fallback)"

  # 2^14 capacity (16384) — more forgiving than 2^12
  $SNARKJS powersoftau new bn128 14 pot14_0000.ptau -v
  $SNARKJS powersoftau contribute pot14_0000.ptau pot14_0001.ptau --name="First contribution" -v -e="random text"
  $SNARKJS powersoftau prepare phase2 pot14_0001.ptau "$TARGET" -v
  rm -f pot14_0000.ptau pot14_0001.ptau

  echo "✅ Generated local Powers of Tau: $TARGET"
fi

echo ""
echo "Powers of Tau ready: $(ls -lh "$TARGET" | awk '{print $5}')"