// frontend/src/m2Identity.js
// MVP Identity: single source of truth (localStorage only)
//
// memberSecret stored under:
//   su_memberSecret_v1:wallet:<addrLower>
//
// Rules:
// - Never derive from MetaMask signatures
// - Never overwrite an existing valid secret
// - If missing, caller may choose:
//     - loadMemberSecret(wallet)  => read-only
//     - ensureMemberSecret(wallet)=> create-on-missing

const SECRET_PREFIX = 'su_memberSecret_v1:wallet:';

function walletKey(addr) {
  return `${SECRET_PREFIX}${String(addr || '').toLowerCase()}`;
}

function safeGet(key) {
  try { return localStorage.getItem(key); } catch { return null; }
}

function safeSet(key, val) {
  try { localStorage.setItem(key, val); return true; } catch { return false; }
}

function generateSecretDecimal() {
  // 31 bytes -> < 2^248, comfortably within BN254 field; store as decimal string
  const bytes = new Uint8Array(31);
  crypto.getRandomValues(bytes);

  let hex = '0x';
  for (const b of bytes) hex += b.toString(16).padStart(2, '0');

  return BigInt(hex).toString(10);
}

// Read-only: returns BigInt or null
export function loadMemberSecret(wallet) {
  if (!wallet) return null;
  const raw = safeGet(walletKey(wallet));
  if (!raw) return null;
  try { return BigInt(raw); } catch { return null; }
}

// Create-on-missing: returns BigInt or null
export function ensureMemberSecret(wallet) {
  if (!wallet) return null;

  const key = walletKey(wallet);
  const existing = safeGet(key);

  if (existing) {
    try { return BigInt(existing); } catch { /* corrupted: fallthrough */ }
  }

  const fresh = generateSecretDecimal();
  safeSet(key, fresh);
  return BigInt(fresh);
}
