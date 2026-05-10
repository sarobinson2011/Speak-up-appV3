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

assert(publication.connector);
assert(Array.isArray(publication.chunks));

assert.strictEqual(publication.chunks.length, 3);

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
