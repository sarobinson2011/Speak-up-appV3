import assert from "assert";

import { buildLocalPublicationObjects } from "./publicationObjects.js";
import {
  buildLocalPublicationRegistry,
  buildLocalRetrievalProvider,
} from "./retrievalProvider.js";

const material = {
  leaf: "0x01",
  index: 0,
  root: "0xaa",
  siblings: ["0x11", "0x22", "0x33", "0x44"],
  pathBits: [0, 1, 0, 1],
};

const publication = buildLocalPublicationObjects({
  material,
  chunkSize: 2,
});

const registry = buildLocalPublicationRegistry({
  publicationsByAcquisitionKey: {
    "group-1": publication,
  },
});

assert.strictEqual(registry.version, 1);
assert.deepStrictEqual(registry.get("group-1"), publication);
assert.strictEqual(registry.get("missing-group"), null);
assert.strictEqual(registry.get(null), null);

const provider = buildLocalRetrievalProvider({
  publicationRegistry: registry,
});

assert.strictEqual(provider.version, 1);
assert.deepStrictEqual(
  provider.getPublicationGroup({
    target: {
      acquisitionKey: "group-1",
    },
  }),
  publication,
);

assert.strictEqual(
  provider.getPublicationGroup({
    target: {
      acquisitionKey: "missing-group",
    },
  }),
  null,
);

assert.strictEqual(
  provider.getPublicationGroup({
    target: {},
  }),
  null,
);

const compatibilityProvider = buildLocalRetrievalProvider({
  publication,
});

assert.deepStrictEqual(
  compatibilityProvider.getPublicationGroup({
    target: {
      acquisitionKey: "group-1",
    },
  }),
  publication,
);

console.log("reflect retrieval provider registry validation ok");
