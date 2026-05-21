import assert from "assert";

import {
  buildLocalPublicationObjects,
  buildLocalPublicationState,
} from "./publicationObjects.js";

import {
  buildLocalPublicationWindow,
  selectCoherentLocalPublicationState,
  selectLocalPublicationState,
} from "./publicationWindows.js";

const materialA = {
  leaf: "0x1111111111111111111111111111111111111111111111111111111111111111",
  root: "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  index: 1,
  siblings: [
    "0x0000000000000000000000000000000000000000000000000000000000000001",
    "0x0000000000000000000000000000000000000000000000000000000000000002",
  ],
  pathBits: [0, 1],
};

const materialB = {
  ...materialA,
  root: "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  index: 2,
};

const groupA = buildLocalPublicationObjects({ material: materialA, chunkSize: 1 });
const groupB = buildLocalPublicationObjects({ material: materialB, chunkSize: 1 });

const stateA = buildLocalPublicationState({ groups: [groupA] });
const stateB = buildLocalPublicationState({ groups: [groupB] });

const window = buildLocalPublicationWindow({
  states: [stateA, stateB],
  limit: 4,
});

assert(window);
assert.strictEqual(window.version, 1);
assert.strictEqual(window.limit, 4);
assert.strictEqual(window.entryCount, 2);
assert.strictEqual(window.entries.length, 2);
assert.deepStrictEqual(selectLocalPublicationState(window), stateB);
assert.strictEqual(window.entries[0].sequence, 1);
assert.strictEqual(window.entries[1].sequence, 2);

assert.notStrictEqual(
  groupB.descriptor.contentDigest.value,
  stateB.contentDigest.value,
);

assert.deepStrictEqual(
  selectCoherentLocalPublicationState({
    window,
    contentDigest: stateB.contentDigest,
  }),
  stateB,
);

assert.strictEqual(
  selectCoherentLocalPublicationState({
    window,
    contentDigest: groupB.descriptor.contentDigest,
  }),
  null,
);

assert.deepStrictEqual(
  selectCoherentLocalPublicationState({
    window,
    contentDigest: stateA.contentDigest,
  }),
  stateA,
);

assert.strictEqual(
  selectCoherentLocalPublicationState({
    window,
    contentDigest: {
      algorithm: stateA.contentDigest.algorithm,
      value: "not-a-window-digest",
    },
  }),
  null,
);

assert.strictEqual(
  selectLocalPublicationState({
    ...window,
    entries: [
      window.entries[0],
      {
        ...window.entries[1],
        sequence: 1,
      },
    ],
  }),
  null,
);


const reversedWindow = {
  ...window,
  entries: [...window.entries].reverse(),
};

assert.strictEqual(
  selectLocalPublicationState(reversedWindow),
  null,
);

assert.strictEqual(
  buildLocalPublicationWindow({ states: [], limit: 4 }),
  null,
);

assert.strictEqual(
  buildLocalPublicationWindow({ states: [stateA, stateB], limit: 1 }),
  null,
);

assert.strictEqual(
  buildLocalPublicationWindow({ states: [stateA, null], limit: 4 }),
  null,
);

assert.strictEqual(selectLocalPublicationState(null), null);

console.log("reflect publication window validation ok");
