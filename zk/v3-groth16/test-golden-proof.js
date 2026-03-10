#!/usr/bin/env node
// Phase 1: Generate "golden proof" in Node.js CLI
// This MUST pass before touching blockchain

import * as snarkjs from "snarkjs";
import fs from "node:fs";
import { poseidon1, poseidon2, poseidon3 } from "poseidon-lite";

const DEPTH = 16;
const SIGN_DOMAIN = BigInt("0x5349474e"); // "SIGN"

async function main() {
    console.log("🧪 Phase 1: Golden Proof Test");
    console.log("=============================\n");

    // ===== 1. BUILD TEST INPUTS =====
    console.log("📝 Step 1: Building test inputs...");

    const memberSecret = BigInt("12345678901234567890");
    const memberLeaf = poseidon1([memberSecret]);

    console.log(`   Member secret: ${memberSecret}`);
    console.log(`   Member leaf:   ${memberLeaf}`);

    // ---- Build small subtree ----
    const leaf0 = poseidon1([BigInt("11111111111111111111")]);
    const leaf1 = poseidon1([BigInt("22222222222222222222")]);
    const leaf2 = memberLeaf;
    const leaf3 = BigInt(0);

    const hash01 = poseidon2([leaf0, leaf1]);
    const hash23 = poseidon2([leaf2, leaf3]);
    let currentHash = poseidon2([hash01, hash23]);

    // ---- Merkle path ----
    const membershipPath = [];
    const membershipPathBits = [];

    // level 0
    membershipPath.push(leaf3);
    membershipPathBits.push(0);

    // level 1
    membershipPath.push(hash01);
    membershipPathBits.push(1);

    // levels 2..15
    for (let i = 2; i < DEPTH; i++) {
        membershipPath.push(BigInt(0));
        membershipPathBits.push(0);
        currentHash = poseidon2([currentHash, BigInt(0)]);
    }

    const membershipRoot = currentHash;

    console.log(`   Membership root: ${membershipRoot}`);

    const petitionId = BigInt(1);

    const nullifier = poseidon3([
        memberSecret,
        petitionId,
        SIGN_DOMAIN
    ]);

    console.log(`   Petition ID:     ${petitionId}`);
    console.log(`   Nullifier:       ${nullifier}\n`);

    // ===== 2. GENERATE PROOF =====
    console.log("🔐 Step 2: Generating Groth16 proof...");

    const input = {
        memberSecret: memberSecret.toString(),
        membershipPath: membershipPath.map(v => v.toString()),
        membershipIndices: membershipPathBits,
        petitionId: petitionId.toString(),
        membershipRoot: membershipRoot.toString()
    };

    const wasmPath = "build/sign_petition_js/sign_petition.wasm";
    const zkeyPath = "keys/sign_petition_final.zkey";

    const { proof, publicSignals } =
        await snarkjs.groth16.fullProve(input, wasmPath, zkeyPath);

    console.log("   ✅ Proof generated!\n");

    // ===== 3. VERIFY LOCALLY =====
    console.log("✓  Step 3: Verifying proof locally...");

    const vkey = JSON.parse(
        fs.readFileSync("keys/verification_key.json", "utf8")
    );

    const verified =
        await snarkjs.groth16.verify(vkey, publicSignals, proof);

    if (!verified) {
        console.error("   ❌ LOCAL VERIFICATION FAILED!");
        process.exit(1);
    }

    console.log("   ✅ Local verification PASSED!\n");

    // ===== 4. SHOW PUBLIC SIGNALS =====
    console.log("📊 Step 4: Public signals (circuit output order):");

    if (publicSignals.length !== 3) {
        throw new Error(
            `Expected 3 public signals, got ${publicSignals.length}`
        );
    }

    publicSignals.forEach((s, idx) => {
        console.log(`   publicSignals[${idx}]: ${s}`);
    });

    console.log(`\n   Expected petition ID:     ${petitionId}`);
    console.log(`   Expected membership root: ${membershipRoot}`);
    console.log(`   Expected nullifier:       ${nullifier}\n`);

    // ===== 5. EXPORT SOLIDITY CALLDATA =====
    console.log("📤 Step 5: Exporting Solidity calldata...");

    const calldataStr =
        await snarkjs.groth16.exportSolidityCallData(proof, publicSignals);

    const calldata = JSON.parse("[" + calldataStr + "]");

    console.log("   Calldata format:");
    console.log("   _pA:         ", calldata[0]);
    console.log("   _pB:         ", calldata[1]);
    console.log("   _pC:         ", calldata[2]);
    console.log("   _pubSignals: ", calldata[3]);
    console.log("");

    fs.writeFileSync(
        "golden-proof.json",
        JSON.stringify(
            {
                proof,
                publicSignals,
                calldata,
                inputs: input
            },
            null,
            2
        )
    );

    console.log("✅ Golden proof saved to: golden-proof.json");
    console.log("");
    console.log("🎉 PHASE 1 COMPLETE!");
}

main()
    .then(() => process.exit(0))
    .catch((err) => {
        console.error(err);
        process.exit(1);
    });