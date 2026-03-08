// frontend/src/components/M2SignButton.jsx (M2-only)
import { useMemo, useState } from 'react';
import { ethers } from 'ethers';
import { useZKProof } from '../hooks/useZKProof';
import { REGISTRY_ADDRESS } from '../config';

// Verifier MUST be provided via env (prevents accidental fallback to an old address)
const VERIFIER_ADDRESS = import.meta.env.VITE_VERIFIER_ADDRESS;

// Preflight is ON by default; disable only if explicitly set to "true"
const DISABLE_PREFLIGHT =
  (import.meta.env.VITE_DISABLE_PREFLIGHT || '').toString().toLowerCase() === 'true';

// Debug logs OFF by default; enable with VITE_DEBUG=true
const DEBUG = (import.meta.env.VITE_DEBUG || '').toString().toLowerCase() === 'true';

const REQUIRED_CHAIN_ID = (import.meta.env.VITE_REQUIRED_CHAIN_ID || '').toString().trim(); // e.g. "1313161555"

function dlog(...args) {
  if (DEBUG) console.log(...args);
}
function dwarn(...args) {
  if (DEBUG) console.warn(...args);
}

const VERIFIER_ABI = [
  'function verifyProof(uint256[2],uint256[2][2],uint256[2],uint256[3]) external view returns (bool)'
];

const REGISTRY_SIGN_ABI = [
  'function signPetitionWithZKProof(uint256 petitionId, bytes32 nullifier, uint256[2] pA, uint256[2][2] pB, uint256[2] pC, uint256[3] pubSignals) external'
];

const REGISTRY_VIEW_ABI = [
  'function hasSignedPetition(uint256 petitionId, bytes32 nullifier) external view returns (bool)'
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
function isHex32(s) {
  return typeof s === 'string' && /^0x[0-9a-fA-F]{64}$/.test(s);
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

function chainIdMatches(required, actualChainId) {
  if (!required) return true; // not enforced
  try {
    const req = BigInt(required);
    const act = BigInt(actualChainId);
    return req === act;
  } catch {
    return true; // if parsing fails, don't hard-fail; just skip enforcement
  }
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
  const [alreadySigned, setAlreadySigned] = useState(false);

  const { generateProof } = useZKProof();

  const isLoading = status !== 'idle' && status !== 'success' && status !== 'already-signed';

  const buttonText = useMemo(() => {
    if (alreadySigned) return 'Already signed (Strong Privacy)';
    if (disabled) return 'Sign with Strong Privacy (ZK)';
    return (
      {
        idle: 'Sign with Strong Privacy (ZK)',
        'generating-zk': 'Generating ZK proof…',
        checking: 'Checking…',
        submitting: 'Submitting…',
        success: 'Signed anonymously',
        'already-signed': 'Already signed (Strong Privacy)'
      }[status] || 'Sign with Strong Privacy (ZK)'
    );
  }, [disabled, alreadySigned, status]);

  async function handleM2Sign() {
    try {
      if (!VERIFIER_ADDRESS || typeof VERIFIER_ADDRESS !== 'string' || VERIFIER_ADDRESS.length !== 42) {
        throw new Error('Missing VITE_VERIFIER_ADDRESS in .env/.env.local');
      }

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

      setAlreadySigned(false);
      setStatus('generating-zk');

      const zkProof = await generateProof(membershipPath, pidBI.toString(), memberSecret);
      if (!zkProof?.nullifier || !zkProof?.proof) {
        throw new Error('ZK proof generation returned unexpected shape');
      }

      // Nullifier must be bytes32 for contract call
      const nullifierBytes32 = (() => {
        const n = zkProof.nullifier;
        if (isHex32(n)) return n;
        // sometimes it’s decimal; convert safely
        if (typeof n === 'string' && isDecString(n)) return ethers.toBeHex(BigInt(n), 32);
        // sometimes it’s BigInt
        if (typeof n === 'bigint') return ethers.toBeHex(n, 32);
        throw new Error('Unexpected nullifier format from ZK proof (expected bytes32 hex or decimal string)');
      })();

      const { pA, pB, pC, publicSignals } = zkProof.proof;
      if (!pA || !pB || !pC || !publicSignals) {
        throw new Error('ZK proof missing fields (pA/pB/pC/publicSignals)');
      }

      const psNorm = normalizePublicSignals(publicSignals);
      if (!psNorm) {
        throw new Error('publicSignals invalid (expected array of 3 uint256 strings)');
      }

      const provider = new ethers.BrowserProvider(window.ethereum);
      const net = await provider.getNetwork();

      dlog('[M2] chainId', net.chainId?.toString?.() || String(net.chainId));

      if (!chainIdMatches(REQUIRED_CHAIN_ID, net.chainId)) {
        throw new Error(
          `Wrong network. Required chainId=${REQUIRED_CHAIN_ID}, got ${net.chainId?.toString?.() || String(net.chainId)}`
        );
      }

      // --- IMPORTANT: authoritative per-(petitionId,nullifier) check ---
      setStatus('checking');
      const registryView = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_VIEW_ABI, provider);
      const has = await registryView.hasSignedPetition(pidBI, nullifierBytes32);
      dlog('[M2] hasSignedPetition', { petitionId: pidBI.toString(), nullifierBytes32, has });

      if (has) {
        setAlreadySigned(true);
        setStatus('already-signed');
        onSuccess?.({ alreadySigned: true, nullifier: nullifierBytes32 });
        return;
      }

      // --- Low-risk debug checks (only when DEBUG) ---
      if (DEBUG) {
        const [verifierCode, registryCode] = await Promise.all([
          provider.getCode(VERIFIER_ADDRESS),
          provider.getCode(REGISTRY_ADDRESS)
        ]);
        dlog('[M2] verifier code empty?', verifierCode === '0x', VERIFIER_ADDRESS);
        dlog('[M2] registry  code empty?', registryCode === '0x', REGISTRY_ADDRESS);

        const probe = await probeRegistryVerifier(provider);
        if (probe) {
          dlog('[M2] registry exposes verifier via', probe.fn, '=>', probe.addr);
          if (probe.addr.toLowerCase() !== VERIFIER_ADDRESS.toLowerCase()) {
            dwarn('[M2] WARNING: VERIFIER_ADDRESS differs from registry verifier', {
              envVerifier: VERIFIER_ADDRESS,
              registryVerifier: probe.addr
            });
          }
        }
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
            dlog('[M2_PREFLIGHT] verifyProof order:', c.name, '=>', ok);
            if (ok) {
              accepted = c;
              break;
            }
          } catch (e) {
            dlog(
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

        dlog('[M2_PREFLIGHT] accepted publicSignals order:', accepted.name);
        pubSignalsForChain = accepted.inputs;
      }

      // --- Submit tx ---
      setStatus('submitting');
      const signer = await provider.getSigner();
      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_SIGN_ABI, signer);

      // Try estimateGas first; fallback to a safe cap
      let gasLimit = 500000n;
      try {
        const est = await registry.signPetitionWithZKProof.estimateGas(
          pidBI,
          nullifierBytes32,
          pA,
          pB,
          pC,
          pubSignalsForChain
        );
        gasLimit = (est * 12n) / 10n; // +20%
      } catch {
        // keep fallback
      }

      const tx = await registry.signPetitionWithZKProof(
        pidBI,
        nullifierBytes32,
        pA,
        pB,
        pC,
        pubSignalsForChain,
        { gasLimit }
      );

      await tx.wait();

      setStatus('success');
      setAlreadySigned(true); // now true for this petition+nullifier
      onSuccess?.({ txHash: tx.hash, nullifier: nullifierBytes32 });
    } catch (error) {
      console.error('M2SignButton error:', error);
      setStatus('idle');
      onError?.(error);
    }
  }

  return (
    <button
      onClick={handleM2Sign}
      disabled={disabled || alreadySigned || isLoading || status === 'success' || status === 'already-signed'}
      style={{
        padding: '12px 24px',
        backgroundColor: status === 'success' ? '#10b981' : '#8b5cf6',
        color: 'white',
        border: 'none',
        borderRadius: '8px',
        fontSize: '16px',
        fontWeight: '600',
        cursor: disabled || alreadySigned || status === 'success' || status === 'already-signed'
          ? 'not-allowed'
          : isLoading
          ? 'wait'
          : 'pointer',
        opacity: disabled || alreadySigned || isLoading || status === 'success' || status === 'already-signed' ? 0.7 : 1
      }}
    >
      {buttonText}
    </button>
  );
}