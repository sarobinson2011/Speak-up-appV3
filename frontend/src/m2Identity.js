// frontend/src/m2Identity.js
// Active anonymous identity: localStorage only.
//
// Rules:
// - Secret is the identity primitive
// - Wallet-keyed storage is an MVP/browser convenience handle only
// - Legacy active-key storage is supported as compatibility fallback
// - Never derive identity from MetaMask signatures
// - Never auto-create during normal app flow
// - Create/import are explicit operator actions only

const LEGACY_ACTIVE_SECRET_KEY = 'su_memberSecret_v1:active';
const SECRET_PREFIX = 'su_memberSecret_v1:wallet:';

function secretKey(account) {
  if (!account) return null;
  return `${SECRET_PREFIX}${String(account).toLowerCase()}`;
}

function safeGet(key) {
  try {
    return key ? localStorage.getItem(key) : null;
  } catch {
    return null;
  }
}

function safeSet(key, val) {
  try {
    if (!key) return false;
    localStorage.setItem(key, val);
    return true;
  } catch {
    return false;
  }
}

function safeRemove(key) {
  try {
    if (!key) return false;
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

export function loadMemberSecret(account) {
  const key = secretKey(account);
  const walletRaw = safeGet(key);

  if (walletRaw) {
    try {
      return BigInt(walletRaw);
    } catch {
      return null;
    }
  }

  const existingWalletKeys = Object.keys(localStorage).filter((k) =>
    k.startsWith(SECRET_PREFIX)
  );

  if (existingWalletKeys.length > 0) return null;

  const legacyRaw = safeGet(LEGACY_ACTIVE_SECRET_KEY);
  if (!legacyRaw) return null;

  try {
    const legacySecret = BigInt(legacyRaw);

    // Compatibility bridge: preserve existing local identity while bringing the
    // currently connected wallet onto the wallet-keyed runtime shape.
    if (key) {
      safeSet(key, legacySecret.toString(10));
    }

    return legacySecret;
  } catch {
    return null;
  }
}

export function hasMemberSecret(account) {
  return loadMemberSecret(account) !== null;
}

export function createMemberSecret(account, options = {}) {
  const key = secretKey(account);
  if (!key) throw new Error('Wallet account required to create a local secret.');

  const { replaceExisting = false } = options;
  const existing = loadMemberSecret(account);

  if (existing !== null && !replaceExisting) {
    throw new Error('Active secret already exists. Creating a new one would replace the current anonymous identity.');
  }

  const fresh = generateSecretDecimal();
  safeSet(key, fresh);
  safeSet(LEGACY_ACTIVE_SECRET_KEY, fresh);
  return BigInt(fresh);
}

export function importMemberSecret(account, raw) {
  const key = secretKey(account);
  if (!key) throw new Error('Wallet account required to import a local secret.');

  const normalized = normalizeSecret(raw);
  if (!normalized) {
    throw new Error('Invalid secret. Paste the exact decimal or 0x-prefixed hex secret that you previously exported.');
  }

  safeSet(key, normalized);
  safeSet(LEGACY_ACTIVE_SECRET_KEY, normalized);
  return BigInt(normalized);
}

export function exportMemberSecret(account) {
  const existing = loadMemberSecret(account);
  return existing !== null ? existing.toString(10) : null;
}

export function clearMemberSecret(account) {
  safeRemove(secretKey(account));
}
