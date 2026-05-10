import {
  REFLECT_TYPES,
  buildReflectEnvelope,
  digestReflectMaterial,
  freezePlain,
} from "./objectModel.js";

function isNonNegativeInteger(value) {
  return Number.isInteger(value) && value >= 0;
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

function normalizePreparedPathMaterial(material) {
  if (!material || typeof material !== "object") return null;

  const leaf = normalizeHexValue(material.leaf);
  const root = normalizeHexValue(material.root);
  const index = Number(material.index);
  const siblings = normalizeSiblingValues(material.siblings);
  const pathBits = normalizePathBits(material.pathBits);

  if (!leaf || !root) return null;
  if (!isNonNegativeInteger(index)) return null;
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

function normalizeChunkSize(rawSize) {
  const size = Number(rawSize);

  if (!isNonNegativeInteger(size) || size <= 0) return null;

  return size;
}

function buildChunkMaterial({ material, offset, size }) {
  const normalized = normalizePreparedPathMaterial(material);
  const start = Number(offset);
  const length = normalizeChunkSize(size);

  if (!normalized) return null;
  if (!isNonNegativeInteger(start)) return null;
  if (!length) return null;
  if (start >= normalized.siblings.length) return null;

  const end = Math.min(start + length, normalized.siblings.length);

  return freezePlain({
    root: normalized.root,
    depth: normalized.siblings.length,
    index: normalized.index,
    offset: start,
    size: end - start,
    siblings: normalized.siblings.slice(start, end),
    pathBits: normalized.pathBits.slice(start, end),
  });
}

function describeChunkMaterial(material) {
  return freezePlain({
    root: material.root,
    depth: material.depth,
    offset: material.offset,
    size: material.size,
  });
}

export function buildChunkEnvelope({ material, offset, size }) {
  const chunkMaterial = buildChunkMaterial({ material, offset, size });
  if (!chunkMaterial) return null;

  return buildReflectEnvelope({
    type: REFLECT_TYPES.CHUNK,
    material: chunkMaterial,
    coherence: describeChunkMaterial(chunkMaterial),
  });
}

function buildConnectorMaterial({ material, chunkSize }) {
  const normalized = normalizePreparedPathMaterial(material);
  const size = normalizeChunkSize(chunkSize);

  if (!normalized || !size) return null;

  const chunks = [];

  for (let offset = 0; offset < normalized.siblings.length; offset += size) {
    const envelope = buildChunkEnvelope({
      material: normalized,
      offset,
      size,
    });

    if (!envelope) return null;

    chunks.push({
      offset,
      size: envelope.material.size,
      digest: envelope.digest,
    });
  }

  return freezePlain({
    root: normalized.root,
    depth: normalized.siblings.length,
    chunkSize: size,
    chunks,
  });
}

function describeConnectorMaterial(material) {
  return freezePlain({
    root: material.root,
    depth: material.depth,
    chunkSize: material.chunkSize,
    chunkCount: material.chunks.length,
    contentDigest: digestReflectMaterial(material.chunks),
  });
}

export function buildConnectorEnvelope({ material, chunkSize }) {
  const connectorMaterial = buildConnectorMaterial({ material, chunkSize });
  if (!connectorMaterial) return null;

  return buildReflectEnvelope({
    type: REFLECT_TYPES.CONNECTOR,
    material: connectorMaterial,
    coherence: describeConnectorMaterial(connectorMaterial),
  });
}

export function buildLocalPublicationObjects({ material, chunkSize }) {
  const normalized = normalizePreparedPathMaterial(material);
  const size = normalizeChunkSize(chunkSize);

  if (!normalized || !size) return null;

  const chunks = [];

  for (let offset = 0; offset < normalized.siblings.length; offset += size) {
    const envelope = buildChunkEnvelope({
      material: normalized,
      offset,
      size,
    });

    if (!envelope) return null;

    chunks.push(envelope);
  }

  const connector = buildConnectorEnvelope({
    material: normalized,
    chunkSize: size,
  });

  if (!connector) return null;

  return freezePlain({
    connector,
    chunks,
  });
}
