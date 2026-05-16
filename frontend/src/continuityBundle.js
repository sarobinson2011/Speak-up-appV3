// frontend/src/continuityBundle.js
//
// Encrypted continuity bundle helper.
//
// Design constraints:
// - frontend/browser only
// - WebCrypto only
// - no wallet semantics
// - no backend semantics
// - no localStorage mutation
// - bundle contains encrypted memberSecret only
// - deterministic envelope shape
// - explicit versioning from day one

const BUNDLE_FORMAT = 'su-encrypted-continuity-bundle';
const BUNDLE_VERSION = 1;

const PBKDF2_ITERATIONS = 400000;
const PBKDF2_HASH = 'SHA-256';

const AES_MODE = 'AES-GCM';
const AES_KEY_LENGTH = 256;

const SALT_BYTES = 16;
const IV_BYTES = 12;

function ensureString(value, label) {
  if (typeof value !== 'string') {
    throw new Error(`${label} must be a string`);
  }

  return value;
}

function normalizeSecret(secret) {
  const s = ensureString(secret, 'memberSecret').trim();

  if (!s) {
    throw new Error('memberSecret cannot be empty');
  }

  try {
    return BigInt(s).toString(10);
  } catch {
    throw new Error('memberSecret must be a valid decimal or 0x-prefixed integer');
  }
}

function normalizePassword(password) {
  const p = ensureString(password, 'password');

  if (!p.trim()) {
    throw new Error('password cannot be empty');
  }

  return p;
}

function bytesToBase64(bytes) {
  let binary = '';

  for (const b of bytes) {
    binary += String.fromCharCode(b);
  }

  return btoa(binary);
}

function base64ToBytes(base64, label) {
  try {
    const binary = atob(ensureString(base64, label));
    const bytes = new Uint8Array(binary.length);

    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }

    return bytes;
  } catch {
    throw new Error(`Invalid base64 field: ${label}`);
  }
}

async function deriveKey({ password, salt, iterations }) {
  const enc = new TextEncoder();

  const baseKey = await crypto.subtle.importKey(
    'raw',
    enc.encode(password),
    { name: 'PBKDF2' },
    false,
    ['deriveKey']
  );

  return crypto.subtle.deriveKey(
    {
      name: 'PBKDF2',
      salt,
      iterations,
      hash: PBKDF2_HASH
    },
    baseKey,
    {
      name: AES_MODE,
      length: AES_KEY_LENGTH
    },
    false,
    ['encrypt', 'decrypt']
  );
}

export async function encryptContinuityBundle(memberSecret, password) {
  const normalizedSecret = normalizeSecret(memberSecret);
  const normalizedPassword = normalizePassword(password);

  const enc = new TextEncoder();

  const salt = crypto.getRandomValues(new Uint8Array(SALT_BYTES));
  const iv = crypto.getRandomValues(new Uint8Array(IV_BYTES));

  const key = await deriveKey({
    password: normalizedPassword,
    salt,
    iterations: PBKDF2_ITERATIONS
  });

  const plaintext = JSON.stringify({
    memberSecret: normalizedSecret
  });

  const ciphertext = await crypto.subtle.encrypt(
    {
      name: AES_MODE,
      iv
    },
    key,
    enc.encode(plaintext)
  );

  const envelope = {
    format: BUNDLE_FORMAT,
    version: BUNDLE_VERSION,
    kdf: {
      name: 'PBKDF2',
      hash: PBKDF2_HASH,
      iterations: PBKDF2_ITERATIONS,
      salt: bytesToBase64(salt)
    },
    cipher: {
      name: AES_MODE,
      iv: bytesToBase64(iv)
    },
    ciphertext: bytesToBase64(new Uint8Array(ciphertext))
  };

  return JSON.stringify(envelope, null, 2);
}

export async function decryptContinuityBundle(bundleText, password) {
  const normalizedPassword = normalizePassword(password);

  let envelope;

  try {
    envelope = JSON.parse(ensureString(bundleText, 'bundleText'));
  } catch {
    throw new Error('Invalid continuity bundle JSON');
  }

  if (envelope?.format !== BUNDLE_FORMAT) {
    throw new Error('Unsupported continuity bundle format');
  }

  if (envelope?.version !== BUNDLE_VERSION) {
    throw new Error('Unsupported continuity bundle version');
  }

  const iterations = envelope?.kdf?.iterations;

  if (!Number.isInteger(iterations) || iterations <= 0) {
    throw new Error('Invalid PBKDF2 iteration count');
  }

  const salt = base64ToBytes(envelope.kdf?.salt, 'kdf.salt');
  const iv = base64ToBytes(envelope.cipher?.iv, 'cipher.iv');
  const ciphertext = base64ToBytes(envelope.ciphertext, 'ciphertext');

  const key = await deriveKey({
    password: normalizedPassword,
    salt,
    iterations
  });

  let plaintextBytes;

  try {
    plaintextBytes = await crypto.subtle.decrypt(
      {
        name: AES_MODE,
        iv
      },
      key,
      ciphertext
    );
  } catch {
    throw new Error('Failed to decrypt continuity bundle');
  }

  let payload;

  try {
    const dec = new TextDecoder();

    payload = JSON.parse(dec.decode(plaintextBytes));
  } catch {
    throw new Error('Invalid decrypted continuity payload');
  }

  const normalizedSecret = normalizeSecret(payload?.memberSecret);

  return {
    memberSecret: normalizedSecret
  };
}
