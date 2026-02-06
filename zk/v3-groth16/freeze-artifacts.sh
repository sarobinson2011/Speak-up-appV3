#!/bin/bash
# Phase 0: Freeze V3 artifacts before testing

cd /home/oem/Documents/Coding/Speak-up-appV3/zk/v3-groth16

echo "📦 V3 Groth16 Artifact Freeze"
echo "=============================="
echo ""
echo "Circuit compiled: $(date)"
echo ""

# Hash all critical files
echo "File hashes (SHA256):"
echo "---------------------"
sha256sum build/sign_petition.r1cs
sha256sum keys/sign_petition_final.zkey
sha256sum keys/verification_key.json
sha256sum contracts/Groth16Verifier.sol
echo ""

# Save metadata
cat > ARTIFACTS.md << 'EOFMD'
# V3 Groth16 Artifacts (FROZEN)

**Date:** $(date)
**Circuit:** sign_petition.circom (depth 10)

## File Hashes (SHA256)
```
$(sha256sum build/sign_petition.r1cs)
$(sha256sum keys/sign_petition_final.zkey)
$(sha256sum keys/verification_key.json)
$(sha256sum contracts/Groth16Verifier.sol)
```

## Circuit Statistics
- Constraints: 6,220
- Private Inputs: 21
- Public Inputs: 2 (petitionId, membershipRoot)
- Outputs: 1 (nullifier)

## Public Input Order (CRITICAL)
1. `petitionId` (Field)
2. `membershipRoot` (Field)

Output:
- `nullifier` (Field)

## DO NOT MODIFY
If any hash changes, regenerate ALL artifacts:
1. Recompile circuit
2. Regenerate zkey
3. Regenerate verifier
4. Re-test everything
EOFMD

echo "✅ Artifacts frozen!"
echo "   See ARTIFACTS.md for reference"
echo ""

# Get verifier function signature
echo "Verifier function signature:"
echo "----------------------------"
grep -A 5 "function verifyProof" contracts/Groth16Verifier.sol | head -6
