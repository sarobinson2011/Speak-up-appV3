#!/usr/bin/env node
// Phase 1: Generate "golden proof" in Node.js CLI
// This MUST pass before touching blockchain

import * as snarkjs from "snarkjs";
import fs from "node:fs";
import { poseidon1, poseidon2, poseidon3 } from "poseidon-lite";

async function main() {
    console.log("🧪 Phase 1: Golden Proof Test");
    console.log("=============================\n");

    // ===== 1. BUILD TEST INPUTS =====
    console.log("📝 Step 1: Building test inputs...");

    // Test member secret (random BigInt)
    const memberSecret = BigInt("12345678901234567890");

    // Compute member leaf: hash(memberSecret)
    const memberLeaf = poseidon1([memberSecret]);
    console.log(`   Member secret: ${memberSecret}`);
    console.log(`   Member leaf:   ${memberLeaf}`);

    // Build simple 4-leaf subtree (depth-10 tree)
    const leaf0 = poseidon1([BigInt("11111111111111111111")]);
    const leaf1 = poseidon1([BigInt("22222222222222222222")]);
    const leaf2 = memberLeaf; // Our member is leaf2 (index 2)
    const leaf3 = BigInt(0);  // Empty

    const hash01 = poseidon2([leaf0, leaf1]);
    const hash23 = poseidon2([leaf2, leaf3]);
    const hash0123 = poseidon2([hash01, hash23]);

    // Continue to depth 10 (all remaining siblings are 0)
    let currentHash = hash0123;

    // Siblings for leaf2 at each level:
    // level0: sibling = leaf3 (pair is [leaf2, leaf3])
    // level1: sibling = hash01 (pair is [hash01, hash23])
    // levels 2-9: sibling = 0 (pair is [currentHash, 0])
    const siblings = [leaf3, hash01];
    for (let i = 2; i < 10; i++) {
        siblings.push(BigInt(0));
        currentHash = poseidon2([currentHash, BigInt(0)]);
    }

    const membershipRoot = currentHash;
    console.log(`   Membership root: ${membershipRoot}`);

    // Path indices for leaf index 2 (binary 0010), from leaf to root:
    // Convention: 0 = current is left child, 1 = current is right child
    // level0: leaf2 is LEFT (sibling on right) → 0
    // level1: hash23 is RIGHT (sibling on left) → 1
    // levels 2-9: current is LEFT (sibling on right) → 0
    const pathIndices = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0];

    // Petition ID
    const petitionId = BigInt(1);

    // Compute nullifier: hash(memberSecret, petitionId, SIGN_DOMAIN)
    const SIGN_DOMAIN = BigInt("0x5349474e"); // "SIGN"
    const nullifier = poseidon3([memberSecret, petitionId, SIGN_DOMAIN]);

    console.log(`   Petition ID:     ${petitionId}`);
    console.log(`   Nullifier:       ${nullifier}\n`);

    // ===== 2. GENERATE PROOF =====
    console.log("🔐 Step 2: Generating Groth16 proof...");

    const input = {
        memberSecret: memberSecret.toString(),
        membershipPath: siblings.map((s) => s.toString()),
        membershipIndices: pathIndices.map((i) => i.toString()),
        petitionId: petitionId.toString(),
        membershipRoot: membershipRoot.toString(),
    };

    const wasmPath = "build/sign_petition_js/sign_petition.wasm";
    const zkeyPath = "keys/sign_petition_final.zkey";

    const { proof, publicSignals } = await snarkjs.groth16.fullProve(
        input,
        wasmPath,
        zkeyPath
    );

    console.log("   ✅ Proof generated!\n");

    // ===== 3. VERIFY LOCALLY =====
    console.log("✓  Step 3: Verifying proof locally...");

    const vkey = JSON.parse(fs.readFileSync("keys/verification_key.json", "utf8"));
    const verified = await snarkjs.groth16.verify(vkey, publicSignals, proof);

    if (!verified) {
        console.error("   ❌ LOCAL VERIFICATION FAILED!");
        console.error("   Circuit/inputs are broken. Fix before deploying.");
        process.exit(1);
    }

    console.log("   ✅ Local verification PASSED!\n");

    // ===== 4. SHOW PUBLIC SIGNALS =====
    console.log("📊 Step 4: Public signals (circuit output order):");

    // Verify we have exactly 3 public signals
    if (publicSignals.length !== 3) {
        throw new Error(`Expected 3 public signals, got ${publicSignals.length}`);
    }

    publicSignals.forEach((s, idx) => {
        console.log(`   publicSignals[${idx}]: ${s}`);
    });

    console.log(`\n   Expected petition ID:     ${petitionId}`);
    console.log(`   Expected membership root: ${membershipRoot}`);
    console.log(`   Expected nullifier:       ${nullifier}\n`);

    // ===== 5. EXPORT SOLIDITY CALLDATA =====
    console.log("📤 Step 5: Exporting Solidity calldata...");

    const calldataStr = await snarkjs.groth16.exportSolidityCallData(
        proof,
        publicSignals
    );

    // Parse: "[a0,a1],[[b00,b01],[b10,b11]],[c0,c1],[pub0,pub1,pub2]"
    const calldata = JSON.parse("[" + calldataStr + "]");

    console.log("   Calldata format:");
    console.log("   _pA:         ", calldata[0]);
    console.log("   _pB:         ", calldata[1]);
    console.log("   _pC:         ", calldata[2]);
    console.log("   _pubSignals: ", calldata[3]);
    console.log("");

    // Save for on-chain testing
    fs.writeFileSync(
        "golden-proof.json",
        JSON.stringify(
            {
                proof,
                publicSignals,
                calldata,
                inputs: input,
            },
            null,
            2
        )
    );

    console.log("✅ Golden proof saved to: golden-proof.json");
    console.log("");
    console.log("🎉 PHASE 1 COMPLETE!");
    console.log("===================");
    console.log("Next: Deploy Groth16Verifier.sol and test with this calldata");
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});