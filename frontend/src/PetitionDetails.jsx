// frontend/src/PetitionDetails.jsx (M2-only)
import { useEffect, useMemo, useState } from 'react';
import { ethers } from 'ethers';
import { poseidon1, poseidon3 } from 'poseidon-lite';
import { PetitionDisplaySection } from './components/PetitionDisplaySection';
import { REGISTRY_ADDRESS, REGISTRY_ABI, RPC_URL, BACKEND_URL } from './config';
import './PetitionDetails.css';
import {
  loadMemberSecret,
  createMemberSecret,
  importMemberSecret,
  exportMemberSecret
} from './m2Identity';
import { M2StatusSection } from './components/M2StatusSection';

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
const ADMISSION_COMMITMENT_PREFIX = 'su_admissionCommitment_v1:leaf:';

function pendingAdmissionKey(wallet) {
  return `${PENDING_ADMISSION_PREFIX}${String(wallet || '').toLowerCase()}`;
}

function admissionCommitmentKey(leaf) {
  return `${ADMISSION_COMMITMENT_PREFIX}${String(leaf || '').toLowerCase()}`;
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

  const [membershipExists, setMembershipExists] = useState(null);

  // Local membership path state — source of truth inside this page
  const [membershipPath, setMembershipPath] = useState(null);
  const [membershipPathLoading, setMembershipPathLoading] = useState(false);

  // Identity / operator actions
  const [identityVersion, setIdentityVersion] = useState(0);
  const [secretActionError, setSecretActionError] = useState('');
  const [secretImportText, setSecretImportText] = useState('');
  const [secretExportText, setSecretExportText] = useState('');

  // Admission bond safety
  const [admissionBondWei, setAdmissionBondWei] = useState(null);
  const [admissionBondEth, setAdmissionBondEth] = useState('');
  const [bondSafetyError, setBondSafetyError] = useState('');

  // Identity: localStorage-only, wallet-agnostic
  const memberSecretBI = useMemo(() => loadMemberSecret(), [identityVersion, account]);
  const secretPresent = Boolean(memberSecretBI);

  const currentPendingAdmissionKey = useMemo(() => pendingAdmissionKey(account), [account]);

  const uiLeafHex = useMemo(() => {
    if (!memberSecretBI) return null;
    try {
      const leaf = poseidon1([memberSecretBI]);
      return bigIntToHex32(leaf);
    } catch {
      return null;
    }
  }, [memberSecretBI]);

  const currentAdmissionCommitmentKey = useMemo(
    () => admissionCommitmentKey(uiLeafHex),
    [uiLeafHex]
  );

  const currentAdmissionCommitment = useMemo(() => {
    const storedCommitment = safeGetLocalStorage(currentAdmissionCommitmentKey);
    return isHex32(storedCommitment) ? storedCommitment : null;
  }, [currentAdmissionCommitmentKey, identityVersion]);

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

  function refreshIdentity() {
    setIdentityVersion((v) => v + 1);
  }

  function handleCreateSecret() {
    setSecretActionError('');
    setSecretExportText('');

    try {
      if (secretPresent) {
        const confirmed = window.confirm(
          'Create a new secret and replace the current anonymous identity on this device? This will switch you away from the current identity until you restore the original secret.'
        );

        if (!confirmed) return;

        createMemberSecret({ replaceExisting: true });
      } else {
        createMemberSecret();
      }

      setMembershipPath(null);
      refreshIdentity();
    } catch (e) {
      setSecretActionError(e?.message || String(e));
    }
  }

  function handleImportSecret() {
    setSecretActionError('');
    setSecretExportText('');

    try {
      importMemberSecret(secretImportText);
      setSecretImportText('');
      setMembershipPath(null);
      refreshIdentity();
    } catch (e) {
      setSecretActionError(e?.message || String(e));
    }
  }

  function handleExportSecret() {
    setSecretActionError('');

    try {
      const exported = exportMemberSecret();
      if (!exported) throw new Error('No active secret to export.');
      setSecretExportText(exported);
    } catch (e) {
      setSecretActionError(e?.message || String(e));
    }
  }

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
        leafMatches,
        admissionBondWei: admissionBondWei ? admissionBondWei.toString() : null,
        admissionBondEth,
        bondSafetyError
      });
    } catch (e) {
      console.warn('[M2_PREFLIGHT] failed to log', e);
    }
  }

  async function fetchMembershipStatus(leafHex) {
    try {
      if (!leafHex) {
        setMembershipExists(null);
        return;
      }

      const url = `${BACKEND_URL}/api/membership/leaf-status?leaf=${leafHex}`;
      const res = await fetch(url);

      if (!res.ok) {
        setMembershipExists(null);
        return;
      }

      const data = await res.json();
      setMembershipExists(Boolean(data.exists));
    } catch {
      setMembershipExists(null);
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

  useEffect(() => {
    let cancelled = false;

    async function loadAdmissionBond() {
      try {
        const provider = new ethers.JsonRpcProvider(RPC_URL);
        const admission = new ethers.Contract(
          ADMISSION_REGISTRY_ADDRESS,
          ADMISSION_REGISTRY_ABI,
          provider
        );
        const bond = await admission.admissionBond();

        if (cancelled) return;

        setAdmissionBondWei(bond);
        setAdmissionBondEth(ethers.formatEther(bond));

        const maxExpectedWei = ethers.parseEther('0.02');
        if (bond > maxExpectedWei) {
          setBondSafetyError(
            `Enrollment blocked: live on-chain bond is ${ethers.formatEther(
              bond
            )} ETH, which exceeds the current safe frontend threshold.`
          );
        } else {
          setBondSafetyError('');
        }
      } catch (e) {
        if (cancelled) return;
        setBondSafetyError(`Failed to load live admission bond: ${e?.message || String(e)}`);
      }
    }

    loadAdmissionBond();

    return () => {
      cancelled = true;
    };
  }, []);

  // Fetch membership path locally by current leaf
  useEffect(() => {
    if (!uiLeafHex) {
      setMembershipPath(null);
      setMembershipExists(null);
      return;
    }

    setMembershipPath(null);
    fetchMembershipStatus(uiLeafHex);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [uiLeafHex]);

  useEffect(() => {
    if (!uiLeafHex || membershipExists !== true) {
      setMembershipPath(null);
      return;
    }

    fetchMembershipPathByLeaf(uiLeafHex);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [uiLeafHex, membershipExists]);

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
  }, [
    petitionId,
    membershipPath,
    memberSecretBI,
    leafMatches,
    admissionBondWei,
    admissionBondEth,
    bondSafetyError
  ]);

  async function loadPetitionDetails(isCancelled) {
    try {
      const provider = new ethers.JsonRpcProvider(RPC_URL);
      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);

      await refreshM2SignedState(registry, petitionId, isCancelled);

      const petitionRes = await fetch(`${BACKEND_URL}/api/petitions/${petitionId}`);
      if (!petitionRes.ok) {
        throw new Error(`Failed to load petition detail: ${petitionRes.status}`);
      }

      const petitionJson = await petitionRes.json();
      const backendPetition = petitionJson?.petition;

      if (!backendPetition) {
        throw new Error('Invalid petition detail response');
      }

      if (isCancelled()) return;

      setPetition({
        petitionId: backendPetition.petitionId,
        creator: backendPetition.creator,
        metadataURI: backendPetition.metadataURI,
        createdAt: backendPetition.createdAt,
        signatureCount: backendPetition.signatureCount
      });

      const createdAtISO = backendPetition?.createdAt
        ? new Date(Number(backendPetition.createdAt) * 1000).toISOString()
        : new Date().toISOString();

      setMetadata({
        petitionId: backendPetition.petitionId,
        title: backendPetition.metadata?.title || `Petition #${petitionId}`,
        description:
          backendPetition.metadata?.description || 'No description available.',
        category: 'Unknown',
        target: 'Public',
        goalSignatures: 100,
        createdAt: createdAtISO
      });

      setSignatureCount(Number(backendPetition.signatureCount || 0));

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
      if (!memberSecretBI) throw new Error('No active secret on this device/browser');
      if (!uiLeafHex) throw new Error('Failed to derive membership leaf from the active secret');

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

      const admissionCommitment = bigIntToHex32(poseidon1([BigInt(admissionSecret)]));

      const status = Number(await admission.getStatus(admissionCommitment));

      // Status enum:
      // 0 = None
      // 1 = Funded
      // 2 = Consumed
      // 3 = Refunded

      if (status === 0) {
        const bond = await admission.admissionBond();

        const maxExpectedWei = ethers.parseEther('0.02');
        if (bond > maxExpectedWei) {
          throw new Error(
            `Enrollment blocked for safety: live on-chain bond is ${ethers.formatEther(
              bond
            )} ETH, above allowed frontend threshold.`
          );
        }

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

      safeSetLocalStorage(currentAdmissionCommitmentKey, admissionCommitment);
      safeRemoveLocalStorage(currentPendingAdmissionKey);
      setIdentityVersion((v) => v + 1);
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

  const hasM2Inputs = Boolean(secretPresent && membershipPath && leafMatches);
  const resolvedHasSignedM2 = Boolean(hasSignedM2);
  const canM2Sign = Boolean(hasM2Inputs && !m2CheckLoading && !resolvedHasSignedM2);

  return (
    <div>
      <button onClick={onBack} className="back-button">
        ← Back to All Petitions
      </button>

      <PetitionDisplaySection
        metadata={metadata}
        petition={petition}
        signatureCount={signatureCount}
        resolvedHasSignedM2={resolvedHasSignedM2}
      />

      <M2StatusSection
        petitionId={petitionId}
        membershipPath={membershipPath}
        memberSecretBI={memberSecretBI}
        currentAdmissionCommitment={currentAdmissionCommitment}
        resolvedHasSignedM2={resolvedHasSignedM2}
        m2CheckLoading={m2CheckLoading}
        membershipPathLoading={membershipPathLoading}
        secretPresent={secretPresent}
        leafMatches={leafMatches}
        admissionBondEth={admissionBondEth}
        bondSafetyError={bondSafetyError}
        enrolling={enrolling}
        enrollError={enrollError}
        secretImportText={secretImportText}
        setSecretImportText={setSecretImportText}
        handleCreateSecret={handleCreateSecret}
        handleImportSecret={handleImportSecret}
        handleExportSecret={handleExportSecret}
        secretExportText={secretExportText}
        secretActionError={secretActionError}
        enrollMembershipOnce={enrollMembershipOnce}
        logM2Preflight={logM2Preflight}
        refreshM2SignedState={refreshM2SignedState}
        fetchMembershipPathByLeaf={fetchMembershipPathByLeaf}
        uiLeafHex={uiLeafHex}
        setSignatureCount={setSignatureCount}
        onSigned={onSigned}
        m2Nullifier={m2Nullifier}
        membershipExists={membershipExists}
      />

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