// frontend/src/m2Identity.js
// Active anonymous identity: localStorage only, wallet-agnostic.
//
// Rules:
// - Secret is the identity primitive
// - Never derive from MetaMask signatures
// - Never auto-create during normal app flow
// - Create/import are explicit operator actions only

const ACTIVE_SECRET_KEY = 'su_memberSecret_v1:active';

function safeGet(key) {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

function safeSet(key, val) {
  try {
    localStorage.setItem(key, val);
    return true;
  } catch {
    return false;
  }
}

function safeRemove(key) {
  try {
    localStorage.removeItem(key);
    return true;
  } catch {
    return false;
  }
}

function normalizeSecret(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim();
  if (!s) return null;

  try {
    return BigInt(s).toString(10);
  } catch {
    return null;
  }
}

function generateSecretDecimal() {
  // 31 bytes -> comfortably inside BN254 field
  const bytes = new Uint8Array(31);
  crypto.getRandomValues(bytes);

  let hex = '0x';
  for (const b of bytes) hex += b.toString(16).padStart(2, '0');

  return BigInt(hex).toString(10);
}

export function loadMemberSecret() {
  const raw = safeGet(ACTIVE_SECRET_KEY);
  if (!raw) return null;

  try {
    return BigInt(raw);
  } catch {
    return null;
  }
}

export function hasMemberSecret() {
  return loadMemberSecret() !== null;
}

export function createMemberSecret(options = {}) {
  const { replaceExisting = false } = options;
  const existing = loadMemberSecret();

  if (existing !== null && !replaceExisting) {
    throw new Error('Active secret already exists. Creating a new one would replace the current anonymous identity.');
  }

  const fresh = generateSecretDecimal();
  safeSet(ACTIVE_SECRET_KEY, fresh);
  return BigInt(fresh);
}

export function importMemberSecret(raw) {
  const normalized = normalizeSecret(raw);
  if (!normalized) {
    throw new Error('Invalid secret format. Expected decimal string or 0x-prefixed hex.');
  }

  safeSet(ACTIVE_SECRET_KEY, normalized);
  return BigInt(normalized);
}

export function exportMemberSecret() {
  const existing = loadMemberSecret();
  return existing !== null ? existing.toString(10) : null;
}

export function clearMemberSecret() {
  safeRemove(ACTIVE_SECRET_KEY);
}