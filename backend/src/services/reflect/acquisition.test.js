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
assert.deepStrictEqual(plan.traversalOrder, ["group-1"]);
assert.strictEqual(
  plan.objects[0].contentDigest.value,
  publication.descriptor.contentDigest.value,
);

const acquired = acquireLocalPublicationGroup({
  plan,
  publication,
});

assert(acquired.ok);
assert.strictEqual(acquired.terminal, true);
assert.strictEqual(acquired.terminalReason, "terminal-success");
assert.strictEqual(acquired.continuationEligible, false);
assert.deepStrictEqual(acquired.continuation, {
  eligible: false,
  reason: null,
  executed: false,
});
assert.deepStrictEqual(
  acquired.completedSteps,
  [
    "plan-accepted",
    "publication-accepted",
    "selected-state-validated",
    "traversal-group-1-completed",
    "publication-acquired",
  ],
);
assert.deepStrictEqual(acquired.attempts, [
  {
    traversalKey: "group-1",
    outcome: "started",
  },
  {
    traversalKey: "group-1",
    outcome: "succeeded",
  },
]);
assert.deepStrictEqual(acquired.publication, publication);

const wrongPublication = buildLocalPublicationObjects({
  material: {
    ...material,
    root: "0xbb",
  },
  chunkSize: 2,
});

const wrongPublicationResult = acquireLocalPublicationGroup({
  plan,
  publication: wrongPublication,
});

assert.strictEqual(
  wrongPublicationResult.reason,
  "content-digest-mismatch",
);
assert.strictEqual(wrongPublicationResult.terminal, false);
assert.strictEqual(wrongPublicationResult.terminalReason, null);
assert.strictEqual(wrongPublicationResult.continuationEligible, true);
assert.deepStrictEqual(wrongPublicationResult.continuation, {
  eligible: true,
  reason: "content-digest-mismatch",
  executed: false,
});

assert.deepStrictEqual(wrongPublicationResult.attempts, [
  {
    traversalKey: "group-1",
    outcome: "started",
  },
  {
    traversalKey: "group-1",
    outcome: "failed",
    reason: "content-digest-mismatch",
  },
]);

assert.strictEqual(buildLocalAcquisitionPlan({ publicationState: null }), null);
const invalidPlanResult = acquireLocalPublicationGroup({ plan: null, publication });

assert.strictEqual(invalidPlanResult.reason, "invalid-plan");
assert.strictEqual(invalidPlanResult.terminal, true);
assert.strictEqual(invalidPlanResult.terminalReason, "terminal-failure");
assert.strictEqual(invalidPlanResult.continuationEligible, false);
assert.deepStrictEqual(invalidPlanResult.continuation, {
  eligible: false,
  reason: null,
  executed: false,
});

assert.strictEqual(
  acquireLocalPublicationGroup({ plan, publication: null }).reason,
  "invalid-publication",
);

assert.deepStrictEqual(
  acquireLocalPublicationGroup({
    plan: null,
    publication,
  }).completedSteps,
  [],
);

assert.strictEqual(
  acquireLocalPublicationGroup({
    plan: {
      ...plan,
      objectCount: 2,
    },
    publication,
  }).reason,
  "object-count-mismatch",
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
  }).reason,
  "invalid-sequence",
);


assert.strictEqual(
  acquireLocalPublicationGroup({
    plan: {
      ...plan,
      traversalOrder: [],
    },
    publication,
  }).reason,
  "traversal-order-mismatch",
);

assert.strictEqual(
  acquireLocalPublicationGroup({
    plan: {
      ...plan,
      traversalOrder: ["wrong-group"],
    },
    publication,
  }).reason,
  "invalid-traversal-order",
);

console.log("reflect acquisition boundary validation ok");
