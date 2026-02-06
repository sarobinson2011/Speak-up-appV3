// frontend/src/components/M2SignButton.jsx
import { useState } from 'react';
import { ethers } from 'ethers';
import { useZKProof } from '../hooks/useZKProof';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';
const REGISTRY_ADDRESS = '0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD';

export function M2SignButton({ petitionId, onSuccess, onError }) {
  const [status, setStatus] = useState('idle');
  const { generateProof } = useZKProof();

  async function handleM2Sign() {
    try {
      setStatus('fetching-proof');

      const token = localStorage.getItem('authToken');
      if (!token) {
        throw new Error('Please log in first');
      }

      // Fetch Merkle proof
      console.log('📡 Fetching Merkle proof...');
      const proofResponse = await fetch(`${API_URL}/api/m2/merkle-proof`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!proofResponse.ok) {
        const error = await proofResponse.json();
        throw new Error(error.error || 'Failed to fetch Merkle proof');
      }

      const { proof: merkleProof } = await proofResponse.json();
      console.log('✅ Merkle proof received');

      // Generate ZK proof
      setStatus('generating-zk');
      console.log('🔐 Generating ZK proof...');

      const zkProof = await generateProof(merkleProof, petitionId);
      console.log('✅ ZK proof generated');

      // Check nullifier
      const nullifierCheck = await fetch(`${API_URL}/api/m2/check-nullifier`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          petitionId,
          nullifier: zkProof.nullifier
        })
      });

      const { used } = await nullifierCheck.json();
      if (used) {
        throw new Error('Already signed with Strong Privacy');
      }

      // Submit to blockchain
      setStatus('submitting');
      console.log('📤 Submitting...');

      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();

      // === PREFLIGHT TEST ===
      const VERIFIER_ADDRESS = '0xE70E2cFA4a4272B39918A45BA1F067676CCf8c11';
      const VERIFIER_ABI = ['function verifyProof(uint256[2],uint256[2][2],uint256[2],uint256[3]) external view returns (bool)'];
      const verifier = new ethers.Contract(VERIFIER_ADDRESS, VERIFIER_ABI, provider);

      const preflightOk = await verifier.verifyProof(
        zkProof.proof.pA,
        zkProof.proof.pB,
        zkProof.proof.pC,
        zkProof.proof.publicSignals
      );

      console.log('🔍 PREFLIGHT VERIFIER:', preflightOk);
      console.log('Proof data:', { pA: zkProof.proof.pA, pB: zkProof.proof.pB, pC: zkProof.proof.pC, pubSignals: zkProof.proof.publicSignals });

      if (!preflightOk) {
        throw new Error('PREFLIGHT FAILED: Proof invalid on-chain!');
      }

      console.log('✅ Preflight passed!');
      // === END PREFLIGHT ===

      // Use ACTUAL PetitionRegistry contract
      const REGISTRY_ABI = [
        'function signPetitionWithZKProof(uint256 petitionId, bytes32 nullifier, uint256[2] calldata pA, uint256[2][2] calldata pB, uint256[2] calldata pC, uint256[3] calldata pubSignals) external'
      ];

      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, signer);

      const tx = await registry.signPetitionWithZKProof(
        petitionId,
        zkProof.nullifier,
        zkProof.proof.pA,
        zkProof.proof.pB,
        zkProof.proof.pC,
        zkProof.proof.publicSignals,
        { gasLimit: 500000 }
      );

      console.log('Transaction sent:', tx.hash);
      await tx.wait();
      console.log('✅ Confirmed!');

      // Record nullifier
      await fetch(`${API_URL}/api/m2/record-signature`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          petitionId,
          nullifier: zkProof.nullifier,
          txHash: tx.hash
        })
      });

      setStatus('success');
      onSuccess?.({ txHash: tx.hash, nullifier: zkProof.nullifier });

    } catch (error) {
      console.error('M2 error:', error);
      setStatus('idle');
      onError?.(error);
    }
  }

  const buttonText = {
    idle: '🔐 Sign with Strong Privacy (ZK)',
    'fetching-proof': 'Fetching proof...',
    'generating-zk': 'Generating ZK proof (5-10s)...',
    submitting: 'Submitting...',
    success: '✅ Signed Anonymously!'
  }[status];

  const isLoading = status !== 'idle' && status !== 'success';

  return (
    <button
      onClick={handleM2Sign}
      disabled={isLoading || status === 'success'}
      style={{
        padding: '12px 24px',
        backgroundColor: status === 'success' ? '#10b981' : '#8b5cf6',
        color: 'white',
        border: 'none',
        borderRadius: '8px',
        fontSize: '16px',
        fontWeight: '600',
        cursor: isLoading ? 'wait' : 'pointer',
        opacity: isLoading || status === 'success' ? 0.7 : 1
      }}
    >
      {buttonText}
    </button>
  );
}
