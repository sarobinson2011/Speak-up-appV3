import { createHash } from "crypto";

import { getMembershipLeafByLeaf } from "../../db/repositories/membership.js";

const REFLECT_ENVELOPE_VERSION = 1;
const REFLECT_DIGEST_ALGORITHM = "sha256";

const REFLECT_TYPES = freezePlain({
  PREPARED_PATH: "prepared-path",
});

function normalizeLeafInput(rawLeaf) {
  const leaf = String(rawLeaf || "").trim().toLowerCase();

  if (!leaf) {
    return { ok: false, status: 400, body: { error: "leaf required" } };
  }

  if (!leaf.startsWith("0x") || !/^0x[0-9a-fA-F]+$/.test(leaf) || leaf.length > 66) {
    return { ok: false, status: 400, body: { error: "bad leaf" } };
  }

  return { ok: true, leaf };
}

function normalizeIndexInput(rawIndex) {
  if (rawIndex === undefined) {
    return { ok: false, status: 400, body: { error: "index required" } };
  }

  const index = Number(rawIndex);

  if (!Number.isInteger(index) || index < 0) {
    return { ok: false, status: 400, body: { error: "bad index" } };
  }

  return { ok: true, index };
}

async function ensureCurrent(indexer) {
  if (!indexer.synced) await indexer.sync(0);
}

async function refreshOnce(indexer) {
  await indexer.sync(0);
}

function freezePlain(value) {
  if (Array.isArray(value)) {
    for (const item of value) freezePlain(item);
    return Object.freeze(value);
  }

  if (value && typeof value === "object") {
    for (const item of Object.values(value)) freezePlain(item);
    return Object.freeze(value);
  }

  return value;
}

function isHexString(value) {
  return typeof value === "string" && /^0x[0-9a-fA-F]+$/.test(value);
}

function normalizeHexValue(value) {
  if (!isHexString(value)) return null;
  return value.toLowerCase();
}

function normalizePathBits(pathBits) {
  if (!Array.isArray(pathBits)) return null;

  const normalized = [];

  for (const bit of pathBits) {
    if (bit !== 0 && bit !== 1) return null;
    normalized.push(bit);
  }

  return normalized;
}

function normalizeSiblingValues(siblings) {
  if (!Array.isArray(siblings)) return null;

  const normalized = [];

  for (const sibling of siblings) {
    const value = normalizeHexValue(sibling);
    if (!value) return null;
    normalized.push(value);
  }

  return normalized;
}

function normalizePreparedPathMaterial(path) {
  if (!path || typeof path !== "object") return null;

  const leaf = normalizeHexValue(path.leaf);
  const root = normalizeHexValue(path.root);
  const index = Number(path.index);
  const siblings = normalizeSiblingValues(path.siblings);
  const pathBits = normalizePathBits(path.pathBits);

  if (!leaf || !root) return null;
  if (!Number.isInteger(index) || index < 0) return null;
  if (!siblings || !pathBits) return null;
  if (siblings.length !== pathBits.length) return null;

  return freezePlain({
    leaf,
    index,
    root,
    siblings,
    pathBits,
  });
}

function canonicalValue(value) {
  if (Array.isArray(value)) {
    return value.map(canonicalValue);
  }

  if (value && typeof value === "object") {
    const out = {};
    for (const key of Object.keys(value).sort()) {
      out[key] = canonicalValue(value[key]);
    }
    return out;
  }

  return value;
}

function canonicalString(value) {
  return JSON.stringify(canonicalValue(value));
}

function digestPreparedMaterial(material) {
  return createHash(REFLECT_DIGEST_ALGORITHM)
    .update(canonicalString(material))
    .digest("hex");
}

function describePreparedMaterial(material) {
  return freezePlain({
    depth: material.siblings.length,
    siblingCount: material.siblings.length,
    bitCount: material.pathBits.length,
  });
}

function buildReflectEnvelope({ type, material, coherence }) {
  if (!type || !material || !coherence) return null;

  return freezePlain({
    type,
    version: REFLECT_ENVELOPE_VERSION,
    digest: {
      algorithm: REFLECT_DIGEST_ALGORITHM,
      value: digestPreparedMaterial(material),
    },
    coherence,
    material,
  });
}

function preparePathEnvelope(path) {
  const material = normalizePreparedPathMaterial(path);
  if (!material) return null;

  return buildReflectEnvelope({
    type: REFLECT_TYPES.PREPARED_PATH,
    material,
    coherence: describePreparedMaterial(material),
  });
}

function preparedPathBody(envelope) {
  if (!envelope || envelope.type !== REFLECT_TYPES.PREPARED_PATH) return null;
  if (envelope.version !== REFLECT_ENVELOPE_VERSION) return null;

  return envelope.material;
}

function ok(body) {
  return freezePlain({
    ok: true,
    status: 200,
    body,
  });
}

function notFound(details) {
  return freezePlain({
    ok: false,
    status: 404,
    body: {
      error: "not_found",
      details,
    },
  });
}

export async function getPreparedPathReadiness({ indexer }) {
  if (!indexer.synced) {
    await indexer.sync(0);
  }

  return ok({
    ok: true,
    ready: Boolean(indexer.synced),
    depth: indexer.depth,
  });
}

export async function getPreparedPathStatus({ indexer, leaf: rawLeaf }) {
  const normalized = normalizeLeafInput(rawLeaf);
  if (!normalized.ok) return freezePlain(normalized);

  const { leaf } = normalized;

  await ensureCurrent(indexer);

  let row = getMembershipLeafByLeaf(leaf);

  if (!row) {
    await refreshOnce(indexer);
    row = getMembershipLeafByLeaf(leaf);
  }

  return ok({
    ok: true,
    exists: Boolean(row),
  });
}

export async function getPreparedPathByLeaf({ indexer, leaf: rawLeaf }) {
  const normalized = normalizeLeafInput(rawLeaf);
  if (!normalized.ok) return freezePlain(normalized);

  const { leaf } = normalized;

  await ensureCurrent(indexer);

  let path = await indexer.getPathByLeaf(leaf);

  if (!path) {
    await refreshOnce(indexer);
    path = await indexer.getPathByLeaf(leaf);
  }

  const body = preparedPathBody(preparePathEnvelope(path));

  if (!body) {
    return notFound("leaf not found");
  }

  return ok(body);
}

export async function getPreparedPathByIndex({ indexer, index: rawIndex }) {
  const normalized = normalizeIndexInput(rawIndex);
  if (!normalized.ok) return freezePlain(normalized);

  const { index } = normalized;

  await ensureCurrent(indexer);

  let path = await indexer.getPathByIndex(index);

  if (!path) {
    await refreshOnce(indexer);
    path = await indexer.getPathByIndex(index);
  }

  const body = preparedPathBody(preparePathEnvelope(path));

  if (!body) {
    return notFound("index out of range or leaf missing");
  }

  return ok(body);
}
