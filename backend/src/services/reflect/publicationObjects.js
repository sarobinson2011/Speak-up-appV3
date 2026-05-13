import {
  REFLECT_TYPES,
  buildReflectEnvelope,
  digestReflectMaterial,
  freezePlain,
} from "./objectModel.js";
import {
  normalizePreparedPathMaterial,
} from "./materials.js";

function isNonNegativeInteger(value) {
  return Number.isInteger(value) && value >= 0;
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
    leaf: normalized.leaf,
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

function buildPublicationDescriptor({ connector, chunks }) {
  if (!connector || !Array.isArray(chunks)) return null;
  if (connector.type !== REFLECT_TYPES.CONNECTOR) return null;

  const chunkDigests = chunks.map((chunk) => chunk?.digest);

  if (chunkDigests.some((digest) => !digest?.value)) return null;

  return freezePlain({
    version: connector.version,
    root: connector.material.root,
    depth: connector.material.depth,
    connectorDigest: connector.digest,
    chunkCount: chunks.length,
    chunkDigests,
    contentDigest: {
      algorithm: connector.digest.algorithm,
      value: digestReflectMaterial({
        connector: connector.digest,
        chunks: chunkDigests,
      }),
    },
  });
}

function buildLocalPublicationGroup({
  descriptor,
  connector,
  chunks,
}) {
  if (!descriptor || !connector || !Array.isArray(chunks)) {
    return null;
  }

  return freezePlain({
    descriptor,
    connector,
    chunks,
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

  const descriptor = buildPublicationDescriptor({
    connector,
    chunks,
  });

  if (!descriptor) return null;

  return buildLocalPublicationGroup({
    descriptor,
    connector,
    chunks,
  });
}

function digestMatches(envelope) {
  if (!envelope || !envelope.digest || !envelope.material) return false;

  return envelope.digest.value === digestReflectMaterial(envelope.material);
}

function descriptorMatches({ descriptor, connector, chunks }) {
  if (!descriptor) return true;

  if (descriptor.version !== connector.version) return false;
  if (descriptor.root !== connector.material.root) return false;
  if (descriptor.depth !== connector.material.depth) return false;
  if (descriptor.chunkCount !== chunks.length) return false;
  if (descriptor.connectorDigest?.value !== connector.digest.value) return false;
  if (!Array.isArray(descriptor.chunkDigests)) return false;
  if (descriptor.chunkDigests.length !== chunks.length) return false;

  for (let i = 0; i < chunks.length; i++) {
    if (descriptor.chunkDigests[i]?.value !== chunks[i]?.digest?.value) {
      return false;
    }
  }

  return true;
}

export function verifyLocalPublicationObjects({ descriptor, connector, chunks }) {
  if (!connector || !Array.isArray(chunks)) return false;
  if (connector.type !== REFLECT_TYPES.CONNECTOR) return false;
  if (!digestMatches(connector)) return false;

  const entries = connector.material?.chunks;
  if (!Array.isArray(entries)) return false;
  if (entries.length !== chunks.length) return false;
  if (!descriptorMatches({ descriptor, connector, chunks })) return false;

  for (let i = 0; i < chunks.length; i++) {
    const chunk = chunks[i];
    const entry = entries[i];

    if (!chunk || chunk.type !== REFLECT_TYPES.CHUNK) return false;
    if (!digestMatches(chunk)) return false;
    if (!entry?.digest?.value) return false;
    if (chunk.digest.value !== entry.digest.value) return false;
    if (chunk.material.offset !== entry.offset) return false;
    if (chunk.material.size !== entry.size) return false;
  }

  return true;
}

export function verifyLocalPublicationGroup(publication) {
  if (!publication || typeof publication !== "object") return false;

  return verifyLocalPublicationObjects({
    descriptor: publication.descriptor,
    connector: publication.connector,
    chunks: publication.chunks,
  });
}

export function buildLocalPublicationState({ groups }) {
  if (!Array.isArray(groups) || groups.length === 0) return null;

  const entries = groups.map((group) => {
    if (!verifyLocalPublicationGroup(group)) return null;

    return freezePlain({
      descriptor: group.descriptor,
      contentDigest: group.descriptor.contentDigest,
    });
  });

  if (entries.some((entry) => !entry)) return null;

  return freezePlain({
    version: 1,
    groupCount: entries.length,
    entries,
    contentDigest: {
      algorithm: entries[0].contentDigest.algorithm,
      value: digestReflectMaterial(entries),
    },
  });
}

export function acceptLocalPublicationState(state) {
  if (!state || typeof state !== "object") return null;

  if (!Number.isInteger(state.version) || state.version <= 0) {
    return null;
  }

  if (!Number.isInteger(state.groupCount) || state.groupCount <= 0) {
    return null;
  }

  if (!Array.isArray(state.entries)) {
    return null;
  }

  if (state.entries.length !== state.groupCount) {
    return null;
  }

  if (!state.contentDigest?.value) {
    return null;
  }

  return freezePlain(state);
}

export function reconstructPreparedPathMaterial({ connector, chunks }) {
  if (!verifyLocalPublicationObjects({ connector, chunks })) return null;

  const root = connector.material.root;
  const depth = connector.material.depth;
  const firstChunk = chunks.find((chunk) => chunk?.material?.offset === 0);
  const leaf = firstChunk?.material?.leaf;
  const index = firstChunk?.material?.index;
  const sortedChunks = [...chunks].sort(
    (a, b) => a.material.offset - b.material.offset,
  );

  const siblings = [];
  const pathBits = [];

  for (const chunk of sortedChunks) {
    siblings.push(...chunk.material.siblings);
    pathBits.push(...chunk.material.pathBits);
  }

  if (siblings.length !== depth) return null;
  if (pathBits.length !== depth) return null;
  if (!leaf) return null;
  if (!Number.isInteger(index) || index < 0) return null;

  return freezePlain({
    leaf,
    index,
    root,
    depth,
    siblings,
    pathBits,
  });
}
