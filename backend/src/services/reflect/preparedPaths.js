import {
  REFLECT_ENVELOPE_VERSION,
  REFLECT_TYPES,
  buildReflectEnvelope,
  freezePlain,
} from "./objectModel.js";
import {
  normalizePreparedPathMaterial,
} from "./materials.js";

import { getMembershipLeafByLeaf } from "../../db/repositories/membership.js";

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

function describePreparedMaterial(material) {
  return freezePlain({
    depth: material.siblings.length,
    siblingCount: material.siblings.length,
    bitCount: material.pathBits.length,
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
