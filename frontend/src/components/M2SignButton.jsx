// frontend/src/components/M2SignButton.jsx (M2-only)
import { useState } from 'react';
import { ethers } from 'ethers';
import { useZKProof } from '../hooks/useZKProof';
import { REGISTRY_ADDRESS } from '../config';

// Optional: if you want this configurable, set VITE_VERIFIER_ADDRESS in frontend .env
const VERIFIER_ADDRESS =
  import.meta.env.VITE_VERIFIER_ADDRESS || '0xE70E2cFA4a4272B39918A45BA1F067676CCf8c11';

const DISABLE_PREFLIGHT =
  (import.meta.env.VITE_DISABLE_PREFLIGHT || '').toString().toLowerCase() === 'true';

const VERIFIER_ABI = [
  'function verifyProof(uint256[2],uint256[2][2],uint256[2],uint256[3]) external view returns (bool)'
];

const REGISTRY_SIGN_ABI = [
  'function signPetitionWithZKProof(uint256 petitionId, bytes32 nullifier, uint256[2] pA, uint256[2][2] pB, uint256[2] pC, uint256[3] pubSignals) external'
];

// Best-effort: common verifier getter names some registries expose
const REGISTRY_VERIFIER_PROBE_ABI = [
  'function verifier() view returns (address)',
  'function zkVerifier() view returns (address)',
  'function groth16Verifier() view returns (address)',
  'function proofVerifier() view returns (address)'
];

function isHexString(s) {
  return typeof s === 'string' && /^0x[0-9a-fA-F]+$/.test(s);
}
function isDecString(s) {
  return typeof s === 'string' && /^[0-9]+$/.test(s);
}

function normalizePublicSignals(ps) {
  if (!Array.isArray(ps) || ps.length !== 3) return null;
  for (const x of ps) {
    if (typeof x !== 'string') return null;
    if (!isDecString(x) && !isHexString(x)) return null;
  }
  return ps;
}

function permute3(ps) {
  const [a, b, c] = ps;
  return [
    { name: 'as-is [0,1,2]', inputs: [a, b, c] },
    { name: '[0,2,1]', inputs: [a, c, b] },
    { name: '[1,0,2]', inputs: [b, a, c] },
    { name: '[1,2,0]', inputs: [b, c, a] },
    { name: '[2,0,1]', inputs: [c, a, b] },
    { name: '[2,1,0]', inputs: [c, b, a] }
  ];
}

async function probeRegistryVerifier(provider) {
  // Try several common getter names; return first that works.
  const probe = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_VERIFIER_PROBE_ABI, provider);
  const candidates = ['verifier', 'zkVerifier', 'groth16Verifier', 'proofVerifier'];

  for (const fn of candidates) {
    try {
      // eslint-disable-next-line no-await-in-loop
      const addr = await probe[fn]();
      if (addr && typeof addr === 'string' && addr.startsWith('0x') && addr.length === 42) {
        return { fn, addr };
      }
    } catch {
      // ignore
    }
  }
  return null;
}

export function M2SignButton({
  petitionId,
  membershipPath,
  memberSecret,
  disabled = false,
  onSuccess,
  onError,
  onPreflight
}) {
  const [status, setStatus] = useState('idle');
  const { generateProof } = useZKProof();

  async function handleM2Sign() {
    try {
      let pidBI;
      try {
        pidBI = BigInt(petitionId);
      } catch {
        throw new Error(`Invalid petitionId: ${petitionId}`);
      }
      if (pidBI <= 0n) throw new Error(`Invalid petitionId: ${petitionId}`);

      if (!window.ethereum) throw new Error('MetaMask not found');
      if (!membershipPath) throw new Error('Membership path not loaded yet');

      if (
        !memberSecret ||
        typeof memberSecret !== 'string' ||
        (!isHexString(memberSecret) && !isDecString(memberSecret))
      ) {
        throw new Error('memberSecret missing/invalid (expected hex 0x… or decimal string)');
      }

      setStatus('generating-zk');

      const zkProof = await generateProof(membershipPath, pidBI.toString(), memberSecret);
      if (!zkProof?.nullifier || !zkProof?.proof) {
        throw new Error('ZK proof generation returned unexpected shape');
      }

      const { pA, pB, pC, publicSignals } = zkProof.proof;
      if (!pA || !pB || !pC || !publicSignals) {
        throw new Error('ZK proof missing fields (pA/pB/pC/publicSignals)');
      }

      const psNorm = normalizePublicSignals(publicSignals);
      if (!psNorm) {
        throw new Error('publicSignals invalid (expected array of 3 uint256 strings)');
      }

      setStatus('submitting');

      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();

      // --- Debug: confirm chain + code presence (super low risk) ---
      const net = await provider.getNetwork();
      console.log('[M2] chainId', net.chainId?.toString?.() || String(net.chainId));

      const [verifierCode, registryCode] = await Promise.all([
        provider.getCode(VERIFIER_ADDRESS),
        provider.getCode(REGISTRY_ADDRESS)
      ]);
      console.log('[M2] verifier code empty?', verifierCode === '0x', VERIFIER_ADDRESS);
      console.log('[M2] registry  code empty?', registryCode === '0x', REGISTRY_ADDRESS);

      const probe = await probeRegistryVerifier(provider);
      if (probe) {
        console.log('[M2] registry exposes verifier via', probe.fn, '=>', probe.addr);
        if (probe.addr.toLowerCase() !== VERIFIER_ADDRESS.toLowerCase()) {
          console.warn(
            '[M2] WARNING: VERIFIER_ADDRESS differs from registry verifier',
            { envVerifier: VERIFIER_ADDRESS, registryVerifier: probe.addr }
          );
        }
      } else {
        console.log('[M2] registry verifier address not discoverable via common getters (ok)');
      }

      try {
        onPreflight?.();
      } catch {
        // ignore
      }

      // --- Preflight against VERIFIER_ADDRESS (view call) ---
      let pubSignalsForChain = psNorm;

      if (!DISABLE_PREFLIGHT && VERIFIER_ADDRESS) {
        const verifier = new ethers.Contract(VERIFIER_ADDRESS, VERIFIER_ABI, provider);

        const candidates = permute3(psNorm);
        let accepted = null;

        for (const c of candidates) {
          try {
            // eslint-disable-next-line no-await-in-loop
            const ok = await verifier.verifyProof(pA, pB, pC, c.inputs);
            console.log('[M2_PREFLIGHT] verifyProof order:', c.name, '=>', ok);
            if (ok) {
              accepted = c;
              break;
            }
          } catch (e) {
            console.log(
              '[M2_PREFLIGHT] verifyProof order reverted:',
              c.name,
              e?.reason || e?.message || String(e)
            );
          }
        }

        if (!accepted) {
          throw new Error(
            'Preflight failed: proof invalid on-chain (all publicSignals orders failed). ' +
            'Likely wrong verifier address or wrong verifier/circuit key.'
          );
        }

        console.log('[M2_PREFLIGHT] accepted publicSignals order:', accepted.name);
        pubSignalsForChain = accepted.inputs;
      }

      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_SIGN_ABI, signer);

      const tx = await registry.signPetitionWithZKProof(
        pidBI,
        zkProof.nullifier,
        pA,
        pB,
        pC,
        pubSignalsForChain,
        { gasLimit: 500000 }
      );

      await tx.wait();

      setStatus('success');
      onSuccess?.({ txHash: tx.hash, nullifier: zkProof.nullifier });
    } catch (error) {
      console.error('M2SignButton error:', error);
      setStatus('idle');
      onError?.(error);
    }
  }

  const buttonText = disabled
    ? 'Already signed (Strong Privacy)'
    : ({
        idle: 'Sign with Strong Privacy (ZK)',
        'generating-zk': 'Generating ZK proof...',
        submitting: 'Submitting...',
        success: 'Signed anonymously'
      }[status] || 'Sign with Strong Privacy (ZK)');

  const isLoading = status !== 'idle' && status !== 'success';

  return (
    <button
      onClick={handleM2Sign}
      disabled={disabled || isLoading || status === 'success'}
      style={{
        padding: '12px 24px',
        backgroundColor: status === 'success' ? '#10b981' : '#8b5cf6',
        color: 'white',
        border: 'none',
        borderRadius: '8px',
        fontSize: '16px',
        fontWeight: '600',
        cursor: disabled || status === 'success' ? 'not-allowed' : isLoading ? 'wait' : 'pointer',
        opacity: disabled || isLoading || status === 'success' ? 0.7 : 1
      }}
    >
      {buttonText}
    </button>
  );
}