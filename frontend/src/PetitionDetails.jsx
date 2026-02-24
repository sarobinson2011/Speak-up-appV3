// frontend/src/PetitionDetails.jsx (M2-only)
import { useEffect, useMemo, useState } from 'react';
import { ethers } from 'ethers';
import { poseidon1, poseidon3 } from 'poseidon-lite';

import { REGISTRY_ADDRESS, REGISTRY_ABI, RPC_URL } from './config';
import { M2SignButton } from './components/M2SignButton';
import './PetitionDetails.css';

const SIGN_DOMAIN = 0x5349474en; // BigInt("SIGN") — must match circuit

function toBigIntFromHex32(hex) {
  if (!hex || typeof hex !== 'string' || !hex.startsWith('0x')) return null;
  try {
    return BigInt(hex);
  } catch {
    return null;
  }
}

function bigIntToHex32(v) {
  const hex = v.toString(16);
  return '0x' + hex.padStart(64, '0');
}

export default function PetitionDetails({
  petitionId,
  signer, // kept for consistency; M2SignButton uses window.ethereum
  memberSecret, // hex bytes32 stored locally
  membershipPath, // REQUIRED for M2 proof generation (from backend /api/membership/path)
  onBack
}) {
  const [petition, setPetition] = useState(null);
  const [metadata, setMetadata] = useState(null);

  const [signatureCount, setSignatureCount] = useState(0);

  const [comments, setComments] = useState([]);
  const [commentsAvailable, setCommentsAvailable] = useState(false);

  const [hasSignedM2, setHasSignedM2] = useState(false);
  const [m2Nullifier, setM2Nullifier] = useState(null);
  const [m2CheckLoading, setM2CheckLoading] = useState(false);

  const memberSecretBI = useMemo(() => toBigIntFromHex32(memberSecret), [memberSecret]);

  // --- PRE-FLIGHT (M2) ---
  const uiLeafHex = useMemo(() => {
    if (!memberSecretBI) return null;
    try {
      const leaf = poseidon1([memberSecretBI]);
      return bigIntToHex32(leaf);
    } catch {
      return null;
    }
  }, [memberSecretBI]);

  function logM2Preflight(tag = 'M2_PREFLIGHT') {
    try {
      console.log(`[${tag}]`, {
        petitionId,
        memberSecretPresent: Boolean(memberSecretBI),
        memberSecretPreview:
          typeof memberSecret === 'string' && memberSecret.startsWith('0x') && memberSecret.length > 20
            ? `${memberSecret.slice(0, 10)}…${memberSecret.slice(-10)}`
            : '(none)',
        uiLeafHex,
        pathWallet: membershipPath?.wallet,
        pathLeaf: membershipPath?.leaf,
        root: membershipPath?.root,
        index: membershipPath?.index,
        siblingsLen: membershipPath?.siblings?.length,
        pathBitsLen: membershipPath?.pathBits?.length,
        leafMatches: Boolean(uiLeafHex && membershipPath?.leaf && uiLeafHex.toLowerCase() === String(membershipPath.leaf).toLowerCase())
      });
    } catch (e) {
      console.warn('[M2_PREFLIGHT] failed to log', e);
    }
  }

  useEffect(() => {
    let cancelled = false;

    (async () => {
      await loadPetitionDetails(() => cancelled);
    })();

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [petitionId, memberSecret, membershipPath]);

  // Log whenever critical M2 inputs change (helps confirm pipe integrity before clicking Sign)
  useEffect(() => {
    logM2Preflight('M2_PREFLIGHT');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [petitionId, memberSecret, membershipPath]);

  async function loadPetitionDetails(isCancelled) {
    try {
      const provider = new ethers.JsonRpcProvider(RPC_URL);
      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);

      // 1) Signed state (M2)
      await refreshM2SignedState(registry, petitionId, isCancelled);

      // 2) Petition data (on-chain)
      const petitionData = await registry.getPetition(petitionId);
      if (isCancelled()) return;
      setPetition(petitionData);

      // 3) Metadata (M2-only MVP)
      // Backend legacy metadata endpoints are deprecated (410 Gone). Keep UI stable with a safe fallback.
      const createdAtISO = petitionData?.createdAt
        ? new Date(Number(petitionData.createdAt) * 1000).toISOString()
        : new Date().toISOString();

      const metadataURI =
        (petitionData && typeof petitionData.metadataURI === 'string' && petitionData.metadataURI) ||
        '';

      setMetadata({
        petitionId,
        title: `Petition #${petitionId}`,
        description: metadataURI
          ? `Metadata URI: ${metadataURI}`
          : 'No description available (metadata not loaded in M2-only MVP)',
        category: 'Unknown',
        target: 'Public',
        goalSignatures: 100,
        createdAt: createdAtISO
      });

      // 4) Signature count (events)
      const filter = registry.filters.PetitionSigned(petitionId);
      const events = await registry.queryFilter(filter);
      if (!isCancelled()) setSignatureCount(events.length);

      // 5) Comments are disabled in M2-only MVP (read-only UI placeholder)
      setCommentsAvailable(false);
      setComments([]);
    } catch (error) {
      console.error('Error loading petition details:', error);
    }
  }

  async function refreshM2SignedState(registry, pid, isCancelled = () => false) {
    setM2CheckLoading(true);
    try {
      if (!memberSecretBI) {
        setHasSignedM2(false);
        setM2Nullifier(null);
        return;
      }

      const petitionIdBI = BigInt(pid);

      // Must match circuit: Poseidon3([memberSecret, petitionId, SIGN_DOMAIN])
      const n = poseidon3([memberSecretBI, petitionIdBI, SIGN_DOMAIN]);
      const nullifierHex = '0x' + n.toString(16).padStart(64, '0');

      const signed = await registry.hasSignedPetition(petitionIdBI, nullifierHex);
      if (isCancelled()) return;

      setHasSignedM2(Boolean(signed));
      setM2Nullifier(nullifierHex);
    } catch (error) {
      if (!isCancelled()) {
        console.warn('Failed to refresh M2 signed state:', error);
        setHasSignedM2(false);
        setM2Nullifier(null);
      }
    } finally {
      if (!isCancelled()) setM2CheckLoading(false);
    }
  }

  if (!petition || !metadata) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem' }}>
        <div>Loading petition details...</div>
      </div>
    );
  }

  const progress =
    metadata.goalSignatures > 0
      ? Math.min((signatureCount / metadata.goalSignatures) * 100, 100)
      : 0;

  const canM2Sign = Boolean(membershipPath && memberSecret && !m2CheckLoading && !hasSignedM2);

  return (
    <div>
      <button onClick={onBack} className="back-button">
        ← Back to All Petitions
      </button>

      <div className="petition-detail-header">
        <div className="detail-title-row">
          <h2 className="detail-title">{metadata.title}</h2>
          {hasSignedM2 && <span className="signed-badge">✓ You signed this (strong privacy)</span>}
        </div>

        <div className="meta-grid">
          <div className="meta-item">
            <small className="meta-label">Category</small>
            <div className="meta-value">{metadata.category}</div>
          </div>
          <div className="meta-item">
            <small className="meta-label">Target</small>
            <div className="meta-value">{metadata.target || 'Public'}</div>
          </div>
          <div className="meta-item">
            <small className="meta-label">Created</small>
            <div className="meta-value">{new Date(metadata.createdAt).toLocaleDateString()}</div>
          </div>
          <div className="meta-item">
            <small className="meta-label">Creator</small>
            <div className="meta-value" style={{ fontSize: '0.85rem' }}>
              {petition.creator.slice(0, 10)}...
            </div>
          </div>
        </div>

        <div className="description-section">
          <h3>Description</h3>
          <p className="description-text">{metadata.description}</p>
        </div>

        {/* Progress */}
        <div style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <strong style={{ fontSize: '1.3rem', color: '#667eea' }}>
              {signatureCount.toLocaleString()} signatures
            </strong>
            <span style={{ color: '#666' }}>Goal: {metadata.goalSignatures.toLocaleString()}</span>
          </div>

          <div
            style={{
              width: '100%',
              height: '20px',
              background: '#e0e0e0',
              borderRadius: '10px',
              overflow: 'hidden'
            }}
          >
            <div
              style={{
                width: `${progress}%`,
                height: '100%',
                background: progress >= 100 ? '#4CAF50' : '#667eea',
                transition: 'width 0.3s ease'
              }}
            />
          </div>

          <small style={{ color: '#666' }}>{progress.toFixed(1)}% of goal reached</small>
        </div>

        {/* M2-only signing */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '24px' }}>
          <M2SignButton
            petitionId={petitionId}
            membershipPath={membershipPath}
            memberSecret={memberSecret}
            disabled={!canM2Sign}
            // Optional: if M2SignButton calls this on click, you'll get a clean "just before prove" dump.
            onPreflight={() => logM2Preflight('M2_CLICK_PREFLIGHT')}
            onSuccess={async ({ txHash }) => {
              console.log('M2 signature successful:', { txHash });
              alert(`Signed anonymously with ZK proof!\nTransaction: ${txHash.slice(0, 10)}...`);

              try {
                const provider = new ethers.JsonRpcProvider(RPC_URL);
                const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);
                await refreshM2SignedState(registry, petitionId);
              } catch (e) {
                console.warn('Failed to refresh M2 state:', e);
              }
            }}
            onError={(error) => {
              alert('M2 signing failed: ' + (error?.message || String(error)));
            }}
          />

          <div
            style={{
              fontSize: '14px',
              color: '#666',
              marginTop: '8px',
              padding: '12px',
              background: '#f3f4f6',
              borderRadius: '6px'
            }}
          >
            <strong>Strong Privacy (M2):</strong> Signs with a zero-knowledge proof. No email, no
            JWT, no attester.
            {m2Nullifier ? (
              <div style={{ marginTop: 8, fontFamily: 'monospace', fontSize: 12 }}>
                nullifier: {m2Nullifier.slice(0, 10)}...{m2Nullifier.slice(-8)}
              </div>
            ) : null}
          </div>

          {!membershipPath && (
            <div
              style={{
                fontSize: 13,
                color: '#a16207',
                background: '#fffbeb',
                padding: 10,
                borderRadius: 6
              }}
            >
              Membership path not loaded yet. Ensure the backend is running and your wallet is
              registered in the membership registry.
            </div>
          )}
        </div>
      </div>

      {/* Comments: read-only placeholder (disabled in MVP) */}
      <div className="comments-card">
        <h3 className="comments-title">Comments ({comments.length})</h3>

        {!commentsAvailable && (
          <p style={{ color: '#999', fontStyle: 'italic', padding: '1rem 0' }}>
            Comments are disabled in M2-only MVP.
          </p>
        )}

        {commentsAvailable && (
          <div>
            {comments.length > 0 ? (
              comments.map((comment, idx) => (
                <div
                  key={idx}
                  style={{
                    background: '#f9f9f9',
                    padding: '1.5rem',
                    marginBottom: '1rem',
                    borderRadius: '4px',
                    borderLeft: '4px solid #667eea'
                  }}
                >
                  <p style={{ margin: '0 0 0.75rem 0', lineHeight: '1.6' }}>{comment.text}</p>
                  <small style={{ color: '#666' }}>
                    Posted {new Date(comment.timestamp).toLocaleString()}
                  </small>
                </div>
              ))
            ) : (
              <p
                style={{
                  textAlign: 'center',
                  color: '#999',
                  fontStyle: 'italic',
                  padding: '2rem'
                }}
              >
                No comments.
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}