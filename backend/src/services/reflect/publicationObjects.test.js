import assert from "assert";

import {
  parseReflectObject,
  serializeReflectObject,
} from "./objectModel.js";

import {
  acceptLocalPublicationState,
  buildLocalPublicationObjects,
  buildLocalPublicationState,
  reconstructPreparedPathMaterial,
  verifyLocalPublicationObjects,
  verifyLocalPublicationGroup,
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

const publicationState = buildLocalPublicationState({
  groups: [publication],
});

assert(publicationState);
assert.strictEqual(publicationState.version, 1);
assert.strictEqual(publicationState.groupCount, 1);
assert.strictEqual(publicationState.entries.length, 1);
assert.deepStrictEqual(
  publicationState.entries[0].descriptor,
  publication.descriptor,
);
assert.deepStrictEqual(
  publicationState.entries[0].contentDigest,
  publication.descriptor.contentDigest,
);
assert(publicationState.contentDigest);
assert(publicationState.contentDigest.value);

const acceptedPublicationState =
  acceptLocalPublicationState(publicationState);

assert(acceptedPublicationState);
assert.deepStrictEqual(
  acceptedPublicationState,
  publicationState,
);

assert.strictEqual(
  acceptLocalPublicationState({
    ...publicationState,
    groupCount: 2,
  }),
  null,
);

assert.strictEqual(
  verifyLocalPublicationObjects(publication),
  true,
);

assert.strictEqual(
  verifyLocalPublicationGroup(publication),
  true,
);

const materialB = {
  ...material,
  root:
    "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  index: 10,
};

const publicationB = buildLocalPublicationObjects({
  material: materialB,
  chunkSize: 2,
});

assert(publicationB);

assert.notStrictEqual(
  publication.descriptor.contentDigest.value,
  publicationB.descriptor.contentDigest.value,
);

assert.strictEqual(
  verifyLocalPublicationObjects({
    descriptor: publication.descriptor,
    connector: publication.connector,
    chunks: publicationB.chunks,
  }),
  false,
);

assert.strictEqual(
  reconstructPreparedPathMaterial({
    connector: publication.connector,
    chunks: publicationB.chunks,
  }),
  null,
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


assert.deepStrictEqual(
  acceptLocalPublicationState({
    ...publicationState,
    contentDigest: {
      ...publicationState.contentDigest,
      value: "tampered-publication-state-digest",
    },
  }),
  null,
);

console.log("reflect publication object validation ok");
