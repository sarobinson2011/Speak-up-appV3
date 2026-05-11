import assert from "assert";

import {
  parseReflectObject,
  serializeReflectObject,
} from "./objectModel.js";

import {
  buildLocalPublicationObjects,
  reconstructPreparedPathMaterial,
  verifyLocalPublicationObjects,
} from "./publicationObjects.js";

const material = {
  leaf:
    "0x1111111111111111111111111111111111111111111111111111111111111111",

  root:
    "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",

  index: 9,

  siblings: [
    "0x0000000000000000000000000000000000000000000000000000000000000001",
    "0x0000000000000000000000000000000000000000000000000000000000000002",
    "0x0000000000000000000000000000000000000000000000000000000000000003",
    "0x0000000000000000000000000000000000000000000000000000000000000004",
    "0x0000000000000000000000000000000000000000000000000000000000000005",
    "0x0000000000000000000000000000000000000000000000000000000000000006",
  ],

  pathBits: [0, 1, 0, 1, 1, 0],
};

const publication = buildLocalPublicationObjects({
  material,
  chunkSize: 2,
});

assert(publication);

assert(publication.descriptor);
assert(publication.connector);
assert(Array.isArray(publication.chunks));

assert.strictEqual(publication.chunks.length, 3);

assert.strictEqual(publication.descriptor.version, publication.connector.version);
assert.strictEqual(publication.descriptor.root, publication.connector.material.root);
assert.strictEqual(publication.descriptor.depth, publication.connector.material.depth);
assert.strictEqual(publication.descriptor.chunkCount, publication.chunks.length);
assert.strictEqual(
  publication.descriptor.connectorDigest.value,
  publication.connector.digest.value,
);
assert.strictEqual(
  publication.descriptor.chunkDigests.length,
  publication.chunks.length,
);
assert(publication.descriptor.contentDigest);
assert(publication.descriptor.contentDigest.value);

for (const chunk of publication.chunks) {
  assert.strictEqual(chunk.type, "chunk");
  assert(chunk.digest);
  assert(chunk.material);
  assert(chunk.coherence);
}

assert.strictEqual(
  publication.connector.type,
  "connector",
);

assert.strictEqual(
  publication.connector.material.chunkSize,
  2,
);

assert.strictEqual(
  publication.connector.material.chunks.length,
  3,
);

for (let i = 0; i < publication.chunks.length; i++) {
  const chunk = publication.chunks[i];
  const connectorChunk =
    publication.connector.material.chunks[i];

  assert.strictEqual(
    chunk.digest.value,
    connectorChunk.digest.value,
  );
}

const publicationAgain = buildLocalPublicationObjects({
  material,
  chunkSize: 2,
});

assert.deepStrictEqual(
  publication,
  publicationAgain,
);

assert.deepStrictEqual(
  publication.descriptor,
  publicationAgain.descriptor,
);

assert.strictEqual(
  verifyLocalPublicationObjects(publication),
  true,
);

const serializedConnector = serializeReflectObject(publication.connector);
const serializedChunks = publication.chunks.map(serializeReflectObject);

assert(serializedConnector);
assert(serializedChunks.every(Boolean));

const parsedPublication = {
  connector: parseReflectObject(serializedConnector),
  chunks: serializedChunks.map(parseReflectObject),
};

assert.strictEqual(
  verifyLocalPublicationObjects(parsedPublication),
  true,
);

const reconstructed = reconstructPreparedPathMaterial(parsedPublication);

assert(reconstructed);
assert.strictEqual(reconstructed.root, material.root);
assert.strictEqual(reconstructed.depth, material.siblings.length);
assert.deepStrictEqual(reconstructed.siblings, material.siblings);
assert.deepStrictEqual(reconstructed.pathBits, material.pathBits);

console.log("reflect publication object validation ok");
