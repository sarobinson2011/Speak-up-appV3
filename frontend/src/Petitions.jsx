// frontend/src/Petitions.jsx (M2-only)

import { useEffect, useMemo, useState } from 'react';
import { ethers } from 'ethers';
import { poseidon1 } from 'poseidon-lite';
import { REGISTRY_ADDRESS, BACKEND_URL } from './config';
import PetitionDetails from './PetitionDetails';
import './Petitions.css';

const SECRET_PREFIX = 'su_memberSecret_v1:wallet:'; // per-wallet key

// Petition registry ABI (create only)
const REGISTRY_PETITION_ABI = [
  'function createPetition(string metadataURI) external returns (uint256 petitionId)'
];

// --- Env knobs (dev-safe defaults) ---
const REQUIRED_CHAIN_ID = BigInt(import.meta.env.VITE_REQUIRED_CHAIN_ID || '1313161555');
const ADMIN_WALLET = (import.meta.env.VITE_ADMIN_WALLET || '').toLowerCase();
const DEBUG = (import.meta.env.VITE_DEBUG || '').toString().toLowerCase() === 'true';

function dlog(...args) {
  if (DEBUG) console.log(...args);
}
function dwarn(...args) {
  if (DEBUG) console.warn(...args);
}

// --- Safe base64 for UTF-8 (NO deprecated unescape) ---
function utf8ToBase64(str) {
  // TextEncoder is standard in modern browsers
  const bytes = new TextEncoder().encode(str);
  let binary = '';
  for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
  return btoa(binary);
}

function buildMetadataDataUri({ title, description }) {
  const obj = {
    title: (title || '').trim(),
    description: (description || '').trim(),
    createdAt: new Date().toISOString(),
    schema: 'speakup.petition.v1'
  };
  const json = JSON.stringify(obj);
  return `data:application/json;base64,${utf8ToBase64(json)}`;
}

function walletSecretKey(wallet) {
  return `${SECRET_PREFIX}${String(wallet || '').toLowerCase()}`;
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
    return true;
  } catch {
    return false;
  }
}

function isHex32(x) {
  return typeof x === 'string' && /^0x[0-9a-fA-F]{64}$/.test(x);
}

function hex32ToBigInt(hex32) {
  return BigInt(hex32);
}

function bigIntToHex32(v) {
  const hex = v.toString(16);
  return '0x' + hex.padStart(64, '0');
}

export default function Petitions({ signer, account }) {
  const [petitions, setPetitions] = useState([]);
  const [loadingPetitions, setLoadingPetitions] = useState(true);
  const [indexerLagBlocks, setIndexerLagBlocks] = useState(null);

  // M2-only local secret, stored under the connected wallet as an MVP browser handle
  const [memberSecret, setMemberSecret] = useState('');

  // Merkle path fetched from backend by derived leaf
  const [membershipPath, setMembershipPath] = useState(null);

  const [viewingPetitionId, setViewingPetitionId] = useState(null);
  const [expandedPetition, setExpandedPetition] = useState(null);

  // Create petition UI state
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState('');

  const currentWalletKey = useMemo(() => walletSecretKey(account), [account]);
  const isAdminWallet = useMemo(() => {
    if (!ADMIN_WALLET) return false;
    return String(account || '').toLowerCase() === ADMIN_WALLET;
  }, [account]);

  // -----------------------------
  // SECRET + ENROLL (M2)
  // -----------------------------
  const memberLeafHex = useMemo(() => {
    if (!isHex32(memberSecret)) return null;
    const secretBI = hex32ToBigInt(memberSecret);
    const leafBI = poseidon1([secretBI]);
    return bigIntToHex32(leafBI);
  }, [memberSecret]);

  // Load the locally stored member secret for the currently connected wallet handle.
  // Never auto-generate here; secret creation remains an explicit user action.
  useEffect(() => {
    setMembershipPath(null);

    if (!account) {
      setMemberSecret('');
      return;
    }

    const stored = safeGetLocalStorage(currentWalletKey);
    setMemberSecret(stored || '');
  }, [account, currentWalletKey]);

  useEffect(() => {
    if (viewingPetitionId) return;

    let cancelled = false;

    async function refreshList() {
      if (cancelled) return;
      await loadPetitions();

      try {
        const indexerRes = await fetch(`${BACKEND_URL}/api/indexer/status`);
        if (!indexerRes.ok || cancelled) return;

        const indexerJson = await indexerRes.json();
        setIndexerLagBlocks(indexerJson?.petitionIndexer?.lagBlocks ?? null);
      } catch {
        if (!cancelled) setIndexerLagBlocks(null);
      }
    }

    refreshList();

    const interval = setInterval(refreshList, 5000);

    return () => {
      cancelled = true;
      clearInterval(interval);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [viewingPetitionId]);

  useEffect(() => {
    if (!account || !memberLeafHex) return;
    fetchMembershipPath(memberLeafHex);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [account, memberLeafHex]);

  async function fetchMembershipPath(leafHex) {
    try {
      if (!leafHex) {
        setMembershipPath(null);
        return;
      }
      const url = `${BACKEND_URL}/api/membership/path?leaf=${leafHex}`;

      const res = await fetch(url);
      
      if (!res.ok) {
        setMembershipPath(null);
        return;
      }
      const data = await res.json();
      setMembershipPath(data);
    } catch {
      setMembershipPath(null);
    }
  }

  async function handleGenerateSecret() {
    if (!account) return;
    const secret = ethers.hexlify(ethers.randomBytes(32)); // 0x + 64 hex chars
    safeSetLocalStorage(currentWalletKey, secret);
    setMemberSecret(secret);
  }

  // -----------------------------
  // CREATE PETITION (wallet-only, no JWT, no Pinata)
  // metadataURI is a data:application/json;base64,... URI
  // -----------------------------
  async function handleCreatePetition() {
    try {
      setCreateError('');
      if (!account) throw new Error('Connect a wallet first.');
      if (!window.ethereum) throw new Error('MetaMask not found.');

      const title = newTitle.trim();
      const description = newDesc.trim();
      if (!title) throw new Error('Title is required.');
      if (!description) throw new Error('Description is required.');

      setCreating(true);

      const provider = new ethers.BrowserProvider(window.ethereum);
      const net = await provider.getNetwork();

      if (REQUIRED_CHAIN_ID && BigInt(net.chainId) !== REQUIRED_CHAIN_ID) {
        throw new Error(`Wrong network. Expected chainId ${REQUIRED_CHAIN_ID.toString()}`);
      }

      const mmSigner = await provider.getSigner();
      const wallet = (await mmSigner.getAddress()).toLowerCase();

      if (wallet !== String(account).toLowerCase()) {
        throw new Error(`Wallet mismatch: UI=${account} MetaMask=${wallet}`);
      }

      const metadataURI = buildMetadataDataUri({ title, description });

      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_PETITION_ABI, mmSigner);

      const tx = await registry.createPetition(metadataURI, { gasLimit: 500000 });
      dlog('[CREATE] tx sent', tx.hash);

      await tx.wait();
      dlog('[CREATE] tx confirmed');

      setNewTitle('');
      setNewDesc('');
      await loadPetitions();
    } catch (e) {
      console.error('[CREATE] error', e);
      setCreateError(e?.message || String(e));
    } finally {
      setCreating(false);
    }
  }

  // -----------------------------
  // PETITIONS LIST
  // -----------------------------
  async function loadPetitions() {
    setLoadingPetitions(true);

    try {
      const res = await fetch(`${BACKEND_URL}/api/petitions`);

      if (!res.ok) {
        throw new Error(`Failed to load petitions: ${res.status}`);
      }

      const data = await res.json();

      if (!data?.ok || !Array.isArray(data.petitions)) {
        throw new Error('Invalid petitions response');
      }

      const list = data.petitions.map((petition) => ({
        petitionId: petition.petitionId,
        creator: petition.creator,
        metadataURI: petition.metadataURI,
        metadata: petition.metadata || null,
        createdAt: petition.createdAt,
        signatureCount: petition.signatureCount
      }));

      setPetitions(list);
    } catch (e) {
      console.error('Error loading petitions:', e);
      setPetitions([]);
    } finally {
      setLoadingPetitions(false);
    }
  }

  // -----------------------------
  // RENDER
  // -----------------------------
  const secretPreview =
    isHex32(memberSecret) ? `${memberSecret.slice(0, 10)}…${memberSecret.slice(-10)}` : '(none)';

  return (
    <div>
      {viewingPetitionId ? (
        <PetitionDetails
          petitionId={viewingPetitionId}
          signer={signer}
          account={account}
          memberSecret={memberSecret}
          membershipPath={membershipPath}
          onBack={() => setViewingPetitionId(null)}
          onSigned={async () => {
            await loadPetitions(); // refresh petition list counts after signing
          }}
        />
      ) : (
        <>
          <h2>Petitions</h2>

          {/* --- Create Petition (wallet-only, metadataURI as data: URI) --- */}
          <div style={{ margin: '16px 0', padding: 12, border: '1px solid #e5e7eb', borderRadius: 8 }}>
            <div style={{ fontSize: 14, marginBottom: 8 }}>
              <strong>Create petition</strong>
              <div style={{ opacity: 0.8, marginTop: 4 }}>
                Stored as <code>data:application/json;base64,...</code> in <code>metadataURI</code> (no JWT/Pinata).
              </div>
            </div>

            <input
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="Title"
              style={{ width: '100%', padding: 10, marginBottom: 8, borderRadius: 6, border: '1px solid #ddd' }}
            />

            <textarea
              value={newDesc}
              onChange={(e) => setNewDesc(e.target.value)}
              placeholder="Description"
              rows={4}
              style={{ width: '100%', padding: 10, marginBottom: 8, borderRadius: 6, border: '1px solid #ddd' }}
            />

            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
              <button className="btn-outline" onClick={handleCreatePetition} disabled={!account || creating}>
                {creating ? 'Creating…' : 'Create petition'}
              </button>
              <button className="btn-outline" onClick={loadPetitions} disabled={loadingPetitions}>
                Refresh list
              </button>
            </div>

            {createError ? (
              <div style={{ marginTop: 10, fontSize: 13, color: '#b91c1c' }}>{createError}</div>
            ) : null}
          </div>

          

          <div>
            <h3>All Petitions ({petitions.length})</h3>
            {indexerLagBlocks > 0 && (
              <div style={{ color: '#999', fontSize: '0.9rem', marginBottom: '1rem' }}>
                Updating read model… {indexerLagBlocks} block{indexerLagBlocks === 1 ? '' : 's'} behind
              </div>
            )}

            {loadingPetitions ? (
              <div style={{ textAlign: 'center', padding: '3rem', color: '#667eea', fontSize: '1.2rem' }}>
                <div>Loading petitions...</div>
                <div style={{ fontSize: '0.9rem', color: '#999', marginTop: '0.5rem' }}>Fetching data from blockchain</div>
              </div>
            ) : petitions.length === 0 ? (
              <p style={{ textAlign: 'center', color: '#999', padding: '2rem' }}>No petitions yet.</p>
            ) : (
              petitions.map((petition) => {
                const isExpanded = expandedPetition === petition.petitionId;

                return (
                  <div key={petition.petitionId} className={`petition-card ${isExpanded ? 'expanded' : ''}`}>
                    <div
                      className="petition-preview"
                      onClick={() => setExpandedPetition(isExpanded ? null : petition.petitionId)}
                    >
                      <div className="petition-preview-left">
                        <h4 className="petition-compact-title">
                          {petition.metadata?.title || `Petition #${petition.petitionId}`}
                        </h4>
                        <div className="petition-compact-meta">
                          Created {new Date(Number(petition.createdAt) * 1000).toLocaleDateString()} · {petition.creator.slice(0, 10)}...
                        </div>
                      </div>

                      <div className="petition-preview-right">
                        <div className="petition-compact-signatures">{petition.signatureCount} 📝</div>
                        <div className="expand-icon">{isExpanded ? '▲' : '▼'}</div>
                      </div>
                    </div>

                    {isExpanded && (
                      <div className="petition-expanded-content">
                        {petition.metadata?.description ? (
                          <p className="petition-meta">
                            <strong>Description:</strong> {petition.metadata.description}
                          </p>
                        ) : null}

                        <p className="petition-meta">
                          <strong>Creator:</strong> {petition.creator}
                        </p>

                        {petition.metadataURI ? (
                          <p className="petition-meta">
                            <strong>Metadata URI:</strong> {petition.metadataURI}
                          </p>
                        ) : null}

                        <div className="petition-actions">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              setViewingPetitionId(petition.petitionId);
                            }}
                            className="btn-outline"
                          >
                            View Full Details
                          </button>
                        </div>

                        {!membershipPath && (
                          <div
                            style={{
                              marginTop: 12,
                              fontSize: 13,
                              color: '#a16207',
                              background: '#fffbeb',
                              padding: 10,
                              borderRadius: 6
                            }}
                          >
                            Membership path not loaded yet. Ensure backend is running and the active local secret is enrolled.
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </>
      )}
    </div>
  );
}