// frontend/src/PetitionDetails.jsx (M2-only)
import { useEffect, useMemo, useState } from 'react';
import { ethers } from 'ethers';
import { poseidon1, poseidon3 } from 'poseidon-lite';

import { REGISTRY_ADDRESS, REGISTRY_ABI, RPC_URL, BACKEND_URL } from './config';
import { M2SignButton } from './components/M2SignButton';
import './PetitionDetails.css';
import { loadMemberSecret } from './m2Identity';

const SIGN_DOMAIN = 0x5349474en; // BigInt("SIGN") — must match circuit

// AdmissionRegistry (canonical Aurora testnet deployment)
const ADMISSION_REGISTRY_ADDRESS =
  import.meta.env.VITE_ADMISSION_PROXY_ADDRESS || '0x36c22227098B24E5aCE48dEa3988327256481F0e';

const ADMISSION_REGISTRY_ABI = [
  'function admissionBond() view returns (uint256)',
  'function fundAdmissionRight(bytes32 admissionCommitment) payable',
  'function activateMembership(bytes32 admissionCommitment, bytes32 admissionSecret, bytes32 leaf)',
  'function getStatus(bytes32 admissionCommitment) view returns (uint8)'
];

const PENDING_ADMISSION_PREFIX = 'su_pendingAdmissionSecret_v1:wallet:';

function pendingAdmissionKey(wallet) {
  return `${PENDING_ADMISSION_PREFIX}${String(wallet || '').toLowerCase()}`;
}

function safeGetLocalStorage(key) {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

function safeSetLocalStorage(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch {
    // ignore
  }
}

function safeRemoveLocalStorage(key) {
  try {
    localStorage.removeItem(key);
  } catch {
    // ignore
  }
}

function isHex32(value) {
  return /^0x[0-9a-fA-F]{64}$/.test(String(value || ''));
}

function bigIntToHex32(v) {
  const hex = v.toString(16);
  return '0x' + hex.padStart(64, '0');
}

export default function PetitionDetails({
  petitionId,
  signer, // kept for consistency; M2SignButton uses window.ethereum
  account,
  memberSecret: _memberSecretProp, // deprecated: ignore prop, derive locally
  membershipPath: _membershipPathProp, // deprecated: fetch locally here
  onBack,
  onSigned
}) {
  const [petition, setPetition] = useState(null);
  const [metadata, setMetadata] = useState(null);

  const [signatureCount, setSignatureCount] = useState(0);

  const [comments, setComments] = useState([]);
  const [commentsAvailable, setCommentsAvailable] = useState(false);

  const [hasSignedM2, setHasSignedM2] = useState(false);
  const [m2Nullifier, setM2Nullifier] = useState(null);
  const [m2CheckLoading, setM2CheckLoading] = useState(false);

  const [enrolling, setEnrolling] = useState(false);
  const [enrollError, setEnrollError] = useState('');

  // Local membership path state — source of truth inside this page
  const [membershipPath, setMembershipPath] = useState(null);
  const [membershipPathLoading, setMembershipPathLoading] = useState(false);

  // Identity: localStorage-only
  const memberSecretBI = useMemo(() => loadMemberSecret(account), [account]);
  const secretPresent = Boolean(memberSecretBI);

  const currentPendingAdmissionKey = useMemo(
    () => pendingAdmissionKey(account),
    [account]
  );

  const uiLeafHex = useMemo(() => {
    if (!memberSecretBI) return null;
    try {
      const leaf = poseidon1([memberSecretBI]);
      return bigIntToHex32(leaf);
    } catch {
      return null;
    }
  }, [memberSecretBI]);

  const leafMatches = useMemo(() => {
    if (!membershipPath || !memberSecretBI) return false;
    try {
      const computed = poseidon1([memberSecretBI]);
      const pathLeaf = BigInt(membershipPath.leaf);
      return computed === pathLeaf;
    } catch {
      return false;
    }
  }, [membershipPath, memberSecretBI]);

  function logM2Preflight(tag = 'M2_PREFLIGHT') {
    try {
      console.log(`[${tag}]`, {
        petitionId,
        secretPresent,
        memberSecretPresent: Boolean(memberSecretBI),
        memberSecretPreview: memberSecretBI ? `${memberSecretBI.toString().slice(0, 8)}…` : '(none)',
        uiLeafHex,
        pathWallet: membershipPath?.wallet,
        pathLeaf: membershipPath?.leaf,
        root: membershipPath?.root,
        index: membershipPath?.index,
        siblingsLen: membershipPath?.siblings?.length,
        pathBitsLen: membershipPath?.pathBits?.length,
        leafMatches
      });
    } catch (e) {
      console.warn('[M2_PREFLIGHT] failed to log', e);
    }
  }

  async function fetchMembershipPathByLeaf(leafHex) {
    try {
      if (!leafHex) {
        setMembershipPath(null);
        return;
      }

      setMembershipPathLoading(true);

      const url = `${BACKEND_URL}/api/membership/path?leaf=${leafHex}`;
      const res = await fetch(url);

      if (!res.ok) {
        setMembershipPath(null);
        return;
      }

      const data = await res.json();
      setMembershipPath(data);
    } catch (e) {
      console.warn('Failed to fetch membership path by leaf:', e);
      setMembershipPath(null);
    } finally {
      setMembershipPathLoading(false);
    }
  }

  // Fetch membership path locally by current leaf
  useEffect(() => {
    if (!account || !uiLeafHex) {
      setMembershipPath(null);
      return;
    }

    fetchMembershipPathByLeaf(uiLeafHex);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [account, uiLeafHex]);

  // Load petition + signed state whenever core inputs change
  useEffect(() => {
    let cancelled = false;
    const isCancelled = () => cancelled;

    (async () => {
      await loadPetitionDetails(isCancelled);
    })();

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [petitionId, membershipPath, memberSecretBI]);

  // Log whenever critical M2 inputs change
  useEffect(() => {
    logM2Preflight('M2_PREFLIGHT');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [petitionId, membershipPath, memberSecretBI, leafMatches]);

  async function loadPetitionDetails(isCancelled) {
    try {
      const provider = new ethers.JsonRpcProvider(RPC_URL);
      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);

      await refreshM2SignedState(registry, petitionId, isCancelled);

      const petitionData = await registry.getPetition(petitionId);
      if (isCancelled()) return;
      setPetition(petitionData);

      const createdAtISO = petitionData?.createdAt
        ? new Date(Number(petitionData.createdAt) * 1000).toISOString()
        : new Date().toISOString();

      const metadataURI =
        (petitionData && typeof petitionData.metadataURI === 'string' && petitionData.metadataURI) || '';

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

      const filter = registry.filters.PetitionSigned(petitionId);
      const events = await registry.queryFilter(filter);
      if (!isCancelled()) setSignatureCount(events.length);

      setCommentsAvailable(false);
      setComments([]);
    } catch (error) {
      console.error('Error loading petition details:', error);
    }
  }

  async function refreshM2SignedState(registry, pid, isCancelled = () => false) {
    setM2CheckLoading(true);

    if (!isCancelled()) {
      setHasSignedM2(false);
      setM2Nullifier(null);
    }

    try {
      if (!memberSecretBI) return;

      const petitionIdBI = BigInt(pid);
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

  async function enrollMembershipOnce() {
    setEnrollError('');
    setEnrolling(true);

    try {
      if (!window.ethereum) throw new Error('MetaMask not found');
      if (!account) throw new Error('Wallet not connected');
      if (!memberSecretBI) throw new Error('Secret missing for this wallet');
      if (!uiLeafHex) throw new Error('Failed to derive membership leaf for this wallet');

      const provider = new ethers.BrowserProvider(window.ethereum);
      const s = await provider.getSigner();
      const wallet = (await s.getAddress()).toLowerCase();

      if (wallet !== String(account).toLowerCase()) {
        throw new Error(`Wallet mismatch: UI=${account} MetaMask=${wallet}`);
      }

      const admission = new ethers.Contract(
        ADMISSION_REGISTRY_ADDRESS,
        ADMISSION_REGISTRY_ABI,
        s
      );

      // Reuse a pending admission secret if one already exists for this wallet.
      // This makes the flow recoverable if funding succeeded but activation did not.
      let admissionSecret = safeGetLocalStorage(currentPendingAdmissionKey);

      if (!isHex32(admissionSecret)) {
        admissionSecret = ethers.hexlify(ethers.randomBytes(32));
        safeSetLocalStorage(currentPendingAdmissionKey, admissionSecret);
      }

      const admissionCommitment = bigIntToHex32(
        poseidon1([BigInt(admissionSecret)])
      );

      const status = Number(await admission.getStatus(admissionCommitment));

      // Status enum:
      // 0 = None
      // 1 = Funded
      // 2 = Consumed
      // 3 = Refunded

      if (status === 0) {
        const bond = await admission.admissionBond();
        const fundTx = await admission.fundAdmissionRight(admissionCommitment, {
          value: bond
        });
        await fundTx.wait();
      }

      if (status === 2) {
        safeRemoveLocalStorage(currentPendingAdmissionKey);
        await fetchMembershipPathByLeaf(uiLeafHex);
        return;
      }

      if (status === 3) {
        throw new Error(
          'Pending admission right was already refunded. Please click Enroll again to start a fresh admission.'
        );
      }

      const activateTx = await admission.activateMembership(
        admissionCommitment,
        admissionSecret,
        uiLeafHex
      );
      await activateTx.wait();

      safeRemoveLocalStorage(currentPendingAdmissionKey);
      await fetchMembershipPathByLeaf(uiLeafHex);
    } catch (e) {
      setEnrollError(e?.message || String(e));
    } finally {
      setEnrolling(false);
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
    metadata.goalSignatures > 0 ? Math.min((signatureCount / metadata.goalSignatures) * 100, 100) : 0;

  const hasM2Inputs = Boolean(secretPresent && membershipPath && leafMatches);
  const resolvedHasSignedM2 = Boolean(hasSignedM2);
  const canM2Sign = Boolean(hasM2Inputs && !m2CheckLoading && !resolvedHasSignedM2);

  return (
    <div>
      <button onClick={onBack} className="back-button">
        ← Back to All Petitions
      </button>

      <div className="petition-detail-header">
        <div className="detail-title-row">
          <h2 className="detail-title">{metadata.title}</h2>
          {resolvedHasSignedM2 && (
            <span className="signed-badge">✓ You signed this (strong privacy)</span>
          )}
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

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '24px' }}>
          {(!canM2Sign || (!membershipPath && secretPresent && !resolvedHasSignedM2)) && (
            <div
              style={{
                fontSize: 13,
                color: '#a16207',
                background: '#fffbeb',
                padding: 10,
                borderRadius: 6,
                border: '1px solid #fde68a'
              }}
            >
              <strong>Strong Privacy (M2) status:</strong>
              <div style={{ marginTop: 6, opacity: 0.9 }}>
                {resolvedHasSignedM2 ? (
                  <div>Already signed.</div>
                ) : m2CheckLoading ? (
                  <div>Checking signed state…</div>
                ) : membershipPathLoading ? (
                  <div>Loading membership path…</div>
                ) : !secretPresent ? (
                  <div>Secret missing for this wallet (cannot sign from this device).</div>
                ) : !membershipPath ? (
                  <>
                    <div>Not enrolled for this wallet.</div>
                    <div style={{ marginTop: 6 }}>
                      Enrollment is one-time and requires a refundable bond (0.001 ETH on Aurora testnet).
                    </div>

                    <div style={{ marginTop: 10, display: 'flex', flexDirection: 'column', gap: 8 }}>
                      <button
                        onClick={enrollMembershipOnce}
                        disabled={enrolling || !secretPresent || resolvedHasSignedM2}
                        style={{
                          padding: '10px 12px',
                          borderRadius: 8,
                          border: '1px solid #e5e7eb',
                          background: enrolling ? '#f3f4f6' : '#111827',
                          color: enrolling ? '#6b7280' : '#ffffff',
                          cursor: enrolling ? 'not-allowed' : 'pointer',
                          fontWeight: 600
                        }}
                      >
                        {enrolling ? 'Enrolling…' : 'Enroll (one-time)'}
                      </button>

                      {enrollError ? (
                        <div style={{ color: '#b91c1c' }}>Enroll failed: {enrollError}</div>
                      ) : null}
                    </div>
                  </>
                ) : !leafMatches ? (
                  <div>Secret mismatch (wallet enrolled with different secret). Use original device/restore secret.</div>
                ) : (
                  <div>Ready.</div>
                )}
              </div>
            </div>
          )}

          <M2SignButton
            petitionId={petitionId}
            membershipPath={membershipPath}
            memberSecret={memberSecretBI ? memberSecretBI.toString() : ''}
            alreadySigned={resolvedHasSignedM2}
            disabled={
              resolvedHasSignedM2 ||
              m2CheckLoading ||
              membershipPathLoading ||
              !secretPresent ||
              !membershipPath ||
              !leafMatches ||
              enrolling
            }
            onPreflight={() => logM2Preflight('M2_CLICK_PREFLIGHT')}
            onSuccess={async ({ txHash }) => {
              console.log('M2 signature successful:', { txHash });
              alert(`Signed anonymously with ZK proof!\nTransaction: ${txHash.slice(0, 10)}...`);

              try {
                const provider = new ethers.JsonRpcProvider(RPC_URL);
                const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);

                await refreshM2SignedState(registry, petitionId);
                await fetchMembershipPathByLeaf(uiLeafHex);

                const filter = registry.filters.PetitionSigned(petitionId);
                const events = await registry.queryFilter(filter);
                const newCount = events.length;

                setSignatureCount(newCount);
                onSigned?.(petitionId, newCount);
              } catch (e) {
                console.warn('Failed to refresh M2 state:', e);
              }
            }}
            onError={(error) => {
              alert('M2 signing failed: ' + (error?.message || String(error)));
            }}
          />

          {m2Nullifier ? (
            <div
              style={{
                fontSize: '12px',
                color: '#666',
                marginTop: '8px',
                padding: '10px',
                background: '#f3f4f6',
                borderRadius: '6px',
                fontFamily: 'monospace'
              }}
            >
              nullifier: {m2Nullifier.slice(0, 10)}...{m2Nullifier.slice(-8)}
            </div>
          ) : null}
        </div>
      </div>

      <div className="comments-card">
        <h3 className="comments-title">Comments ({comments.length})</h3>

        {commentsAvailable ? (
          comments.length > 0 ? (
            comments.map((c, i) => (
              <div key={i} className="comment-item">
                <div className="comment-header">
                  <span className="comment-author">{c.author || 'Anonymous'}</span>
                  <span className="comment-date">{c.date || ''}</span>
                </div>
                <div className="comment-text">{c.text}</div>
              </div>
            ))
          ) : (
            <div className="comments-placeholder">No comments yet.</div>
          )
        ) : (
          <div className="comments-placeholder">
            Comments are disabled in the M2-only MVP baseline.
          </div>
        )}
      </div>
    </div>
  );
}