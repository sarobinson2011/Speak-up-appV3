// frontend/src/hooks/useZKProof.js
import { useState } from 'react';
import * as snarkjs from 'snarkjs';
import { poseidon3 } from 'poseidon-lite';

const FIELD = 21888242871839275222246405745257275088548364400416034343698204186575808495617n;

function assertField(x, label) {
  const v = BigInt(x);
  if (v < 0n || v >= FIELD) {
    throw new Error(`${label} out of field: ${x}`);
  }
}

export function useZKProof() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function generateProof(merkleProof, petitionId) {
    setLoading(true);
    setError(null);

    try {
      console.log('🔐 Generating ZK proof...');

      // Compute nullifier
      const SIGN_DOMAIN = BigInt('0x5349474e');
      const memberSecret = BigInt(merkleProof.memberSecret);
      const nullifier = poseidon3([memberSecret, BigInt(petitionId), SIGN_DOMAIN]);

      console.log('Nullifier computed:', nullifier.toString());

      // Prepare circuit inputs
      const input = {
        memberSecret: merkleProof.memberSecret,
        membershipPath: merkleProof.membershipPath,
        membershipIndices: merkleProof.membershipIndices,
        petitionId: petitionId.toString(),
        membershipRoot: merkleProof.membershipRoot
      };

      console.log('Circuit inputs prepared');

      // Load WASM and proving key
      const wasmPath = '/zk/sign_petition.wasm';
      const zkeyPath = '/zk/sign_petition_final.zkey';

      console.log('Loading circuit files...');

      // Generate proof
      const { proof, publicSignals } = await snarkjs.groth16.fullProve(
        input,
        wasmPath,
        zkeyPath
      );

      console.log('✅ Proof generated successfully!');
      console.log('Public signals:', publicSignals);

      // Verify locally
      const vkeyResponse = await fetch('/zk/verification_key.json');
      const vkey = await vkeyResponse.json();

      const verified = await snarkjs.groth16.verify(vkey, publicSignals, proof);

      if (!verified) {
        throw new Error('Local proof verification failed');
      }

      console.log('✅ Local verification passed');

      // Export Solidity calldata
      const calldataStr = await snarkjs.groth16.exportSolidityCallData(
        proof,
        publicSignals
      );

      console.log('RAW CALLDATA:', calldataStr);

      // FIXED: Safe parsing without Number corruption
      const argv = JSON.parse('[' + calldataStr.replace(/\b(\d+)\b/g, '"$1"') + ']');
      const [pA, pB, pC, pubSigs] = argv;

      // Field bound checks
      [...pA, ...pB[0], ...pB[1], ...pC, ...pubSigs].forEach((x, idx) =>
        assertField(x, `arg[${idx}]`)
      );

      console.log('✅ Field bounds validated');

      setLoading(false);

      return {
        proof: {
          pA,
          pB,
          pC,
          publicSignals: pubSigs
        },
        nullifier: '0x' + BigInt(pubSigs[0]).toString(16).padStart(64, '0'),
        publicSignals: pubSigs
      };

    } catch (err) {
      console.error('ZK proof generation error:', err);
      setError(err.message);
      setLoading(false);
      throw err;
    }
  }

  return {
    generateProof,
    loading,
    error
  };
}
