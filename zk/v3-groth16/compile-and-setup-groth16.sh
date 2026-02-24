#!/bin/bash
set -euo pipefail

echo "🔨 Compiling Circom Circuit & Setting up Groth16"
echo "================================================"
echo ""

# Always run from this script’s directory (portable; no hardcoded paths)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Tooling: prefer global install, fallback to npx for snarkjs
if command -v snarkjs >/dev/null 2>&1; then
  SNARKJS="snarkjs"
else
  SNARKJS="npx snarkjs"
fi

if ! command -v circom >/dev/null 2>&1; then
  echo "❌ circom not found on PATH."
  echo "Run: bash ./install-groth16-deps.sh"
  exit 1
fi

CIRCUIT_DIR="circuits"
BUILD_DIR="build"
KEYS_DIR="keys"
CONTRACTS_DIR="contracts"

CIRCUIT_FILE="${CIRCUIT_DIR}/sign_petition.circom"
R1CS_FILE="${BUILD_DIR}/sign_petition.r1cs"
WASM_FILE="${BUILD_DIR}/sign_petition_js/sign_petition.wasm"
PTAU_FILE="${KEYS_DIR}/powersOfTau28_hez_final_21.ptau"
ZKEY_0000="${KEYS_DIR}/sign_petition_0000.zkey"
ZKEY_FINAL="${KEYS_DIR}/sign_petition_final.zkey"
VKEY_JSON="${KEYS_DIR}/verification_key.json"
SOL_VERIFIER="${CONTRACTS_DIR}/Groth16Verifier.sol"

mkdir -p "$BUILD_DIR" "$KEYS_DIR" "$CONTRACTS_DIR"

# Step 1: Compile circuit
echo "📝 Compiling sign_petition.circom..."
echo "   (Merkle depth should now be 16)"
circom "$CIRCUIT_FILE" -l node_modules --r1cs --wasm --sym -o "$BUILD_DIR"

echo "✅ Circuit compiled!"
echo "   Files created:"
ls -lh "$R1CS_FILE"
ls -lh "$WASM_FILE"
echo ""

# Step 2: Get circuit info
echo "📊 Circuit statistics:"
$SNARKJS r1cs info "$R1CS_FILE"
echo ""

# Step 3: Ensure Powers of Tau exists (download only if missing)
if [ ! -f "$PTAU_FILE" ]; then
  echo "📥 Powers of Tau not found: $PTAU_FILE"
  echo "   Running download script..."
  bash ./download-powers-of-tau.sh
else
  echo "✅ Powers of Tau already present"
fi
echo ""

# Step 4: Generate Groth16 setup
echo "🔑 Generating Groth16 proving key..."
echo "   (This may take a few minutes)"
$SNARKJS groth16 setup "$R1CS_FILE" "$PTAU_FILE" "$ZKEY_0000"
echo "✅ Initial key generated: $(basename "$ZKEY_0000")"
echo ""

# Step 5: Contribute randomness (phase 2)
echo "🎲 Adding randomness to key..."
# You can replace the entropy string any time; it’s just local dev ceremony.
echo "v3-groth16 local entropy" | $SNARKJS zkey contribute "$ZKEY_0000" "$ZKEY_FINAL" --name="V3 contribution"
rm -f "$ZKEY_0000"
echo "✅ Final proving key: $(basename "$ZKEY_FINAL")"
echo ""

# Step 6: Export verification key
echo "📤 Exporting verification key..."
$SNARKJS zkey export verificationkey "$ZKEY_FINAL" "$VKEY_JSON"
echo "✅ Verification key exported: $(basename "$VKEY_JSON")"
echo ""

# Step 7: Generate Solidity verifier
echo "📜 Generating Solidity verifier contract..."
$SNARKJS zkey export solidityverifier "$ZKEY_FINAL" "$SOL_VERIFIER"
echo "✅ Verifier contract generated: $(basename "$SOL_VERIFIER")"
echo ""

# Step 8: Check sizes
echo "📏 File sizes:"
echo "   Proving key:  $(ls -lh "$ZKEY_FINAL" | awk '{print $5}')"
echo "   Verifier contract: $(ls -lh "$SOL_VERIFIER" | awk '{print $5}')"
echo ""

# Check if verifier is under 24KB
verifier_bytes=$(wc -c < "$SOL_VERIFIER")
# Avoid bc dependency; print simple bytes + KB
verifier_kb=$((verifier_bytes / 1024))
echo "   Verifier size: ${verifier_kb}KB (${verifier_bytes} bytes)"
if [ "$verifier_bytes" -lt 24576 ]; then
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
echo "  ✅ $R1CS_FILE"
echo "  ✅ $WASM_FILE"
echo "  ✅ $ZKEY_FINAL"
echo "  ✅ $VKEY_JSON"
echo "  ✅ $SOL_VERIFIER"
echo ""

# Optional: show exact copy commands to frontend
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
FRONTEND_ZK_DIR="$REPO_ROOT/frontend/public/zk"

echo "Next step (copy artifacts into frontend):"
echo "  mkdir -p \"$FRONTEND_ZK_DIR\""
echo "  cp \"$SCRIPT_DIR/$WASM_FILE\" \"$FRONTEND_ZK_DIR/sign_petition.wasm\""
echo "  cp \"$SCRIPT_DIR/$ZKEY_FINAL\" \"$FRONTEND_ZK_DIR/sign_petition_final.zkey\""
echo "  cp \"$SCRIPT_DIR/$VKEY_JSON\" \"$FRONTEND_ZK_DIR/verification_key.json\""
echo ""