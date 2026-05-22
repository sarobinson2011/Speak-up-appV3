import assert from "assert";

import {
  buildLocalPublicationObjects,
  buildLocalPublicationState,
} from "./publicationObjects.js";
import {
  acquireLocalPublicationGroup,
  buildLocalAcquisitionPlan,
} from "./acquisition.js";

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

const publicationState = buildLocalPublicationState({
  groups: [publication],
});

const plan = buildLocalAcquisitionPlan({
  publicationState,
});

assert(plan);
assert.strictEqual(plan.version, 1);
assert.deepStrictEqual(plan.selectedStateDigest, publicationState.contentDigest);
assert.strictEqual(plan.objectCount, 1);
assert.strictEqual(
  plan.objects[0].contentDigest.value,
  publication.descriptor.contentDigest.value,
);

const acquired = acquireLocalPublicationGroup({
  plan,
  publication,
});

assert(acquired);
assert.deepStrictEqual(acquired, publication);

const wrongPublication = buildLocalPublicationObjects({
  material: {
    ...material,
    root: "0xbb",
  },
  chunkSize: 2,
});

assert.strictEqual(
  acquireLocalPublicationGroup({
    plan,
    publication: wrongPublication,
  }),
  null,
);

assert.strictEqual(buildLocalAcquisitionPlan({ publicationState: null }), null);
assert.strictEqual(acquireLocalPublicationGroup({ plan: null, publication }), null);


assert.strictEqual(
  acquireLocalPublicationGroup({
    plan: {
      ...plan,
      objectCount: 2,
    },
    publication,
  }),
  null,
);

assert.strictEqual(
  acquireLocalPublicationGroup({
    plan: {
      ...plan,
      objects: [
        {
          ...plan.objects[0],
          sequence: 2,
        },
      ],
    },
    publication,
  }),
  null,
);

console.log("reflect acquisition boundary validation ok");
