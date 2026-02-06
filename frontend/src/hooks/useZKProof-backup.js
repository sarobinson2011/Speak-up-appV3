// frontend/src/hooks/useZKProof.js
import { useState } from 'react';
import * as snarkjs from 'snarkjs';
import { poseidon3 } from 'poseidon-lite';

/**
 * Hook for generating ZK proofs for M2 Strong Privacy
 */
export function useZKProof() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Generate ZK proof for signing a petition
   * @param {object} merkleProof - From backend /api/m2/merkle-proof
   * @param {number} petitionId - Petition ID
   * @returns {object} { proof, publicSignals, nullifier }
   */
  async function generateProof(merkleProof, petitionId) {
    setLoading(true);
    setError(null);

    try {
      console.log('🔐 Generating ZK proof...');

      // 1. Compute nullifier locally
      const SIGN_DOMAIN = BigInt('0x5349474e'); // "SIGN"
      const memberSecret = BigInt(merkleProof.memberSecret);
      const nullifier = poseidon3([memberSecret, BigInt(petitionId), SIGN_DOMAIN]);

      console.log('Nullifier computed:', nullifier.toString());

      // 2. Prepare circuit inputs
      const input = {
        memberSecret: merkleProof.memberSecret,
        membershipPath: merkleProof.membershipPath,
        membershipIndices: merkleProof.membershipIndices,
        petitionId: petitionId.toString(),
        membershipRoot: merkleProof.membershipRoot
      };

      console.log('Circuit inputs prepared');

      // 3. Load WASM and proving key
      const wasmPath = '/zk/sign_petition.wasm';
      const zkeyPath = '/zk/sign_petition_final.zkey';

      console.log('Loading circuit files...');

      // 4. Generate proof
      const { proof, publicSignals } = await snarkjs.groth16.fullProve(
        input,
        wasmPath,
        zkeyPath
      );

      console.log('✅ Proof generated successfully!');
      console.log('Public signals:', publicSignals);

      // 5. Verify locally (optional but recommended)
      const vkeyResponse = await fetch('/zk/verification_key.json');
      const vkey = await vkeyResponse.json();

      const verified = await snarkjs.groth16.verify(vkey, publicSignals, proof);

      if (!verified) {
        throw new Error('Local proof verification failed');
      }

      console.log('✅ Local verification passed');

      // 6. Export Solidity calldata
      const calldataStr = await snarkjs.groth16.exportSolidityCallData(
        proof,
        publicSignals
      );

      const calldata = JSON.parse('[' + calldataStr + ']');

      setLoading(false);

      return {
        proof: {
          pA: calldata[0],
          pB: calldata[1],
          pC: calldata[2],
          publicSignals: calldata[3]
        },
        nullifier: '0x' + nullifier.toString(16).padStart(64, '0'),
        publicSignals: publicSignals
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
