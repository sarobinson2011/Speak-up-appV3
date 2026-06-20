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

const continuationResult = acquireLocalPublicationGroup({
  plan,
  publication: wrongPublication,
  continuationPublication: publication,
});

assert(continuationResult.ok);
assert.strictEqual(continuationResult.terminal, true);
assert.strictEqual(continuationResult.terminalReason, "terminal-success");
assert.strictEqual(continuationResult.continuationEligible, false);
assert.deepStrictEqual(continuationResult.continuation, {
  eligible: true,
  reason: "content-digest-mismatch",
  executed: true,
});
assert.deepStrictEqual(
  continuationResult.completedSteps,
  [
    "plan-accepted",
    "publication-accepted",
    "selected-state-validated",
    "continuation-executed",
    "traversal-group-1-completed",
    "publication-acquired",
  ],
);
assert.deepStrictEqual(continuationResult.attempts, [
  {
    traversalKey: "group-1",
    outcome: "started",
  },
  {
    traversalKey: "group-1",
    outcome: "failed",
    reason: "content-digest-mismatch",
  },
  {
    traversalKey: "group-1",
    outcome: "started",
  },
  {
    traversalKey: "group-1",
    outcome: "succeeded",
  },
]);

const failedContinuationResult = acquireLocalPublicationGroup({
  plan,
  publication: wrongPublication,
  continuationPublication: wrongPublication,
});

assert.strictEqual(failedContinuationResult.ok, false);
assert.strictEqual(
  failedContinuationResult.reason,
  "content-digest-mismatch",
);
assert.deepStrictEqual(plan.selectedStateDigest, publicationState.contentDigest);
assert.deepStrictEqual(
  plan.objects[0].contentDigest,
  publication.descriptor.contentDigest,
);
assert.deepStrictEqual(
  failedContinuationResult.attempts,
  [
    {
      traversalKey: "group-1",
      outcome: "started",
    },
    {
      traversalKey: "group-1",
      outcome: "failed",
      reason: "content-digest-mismatch",
    },
    {
      traversalKey: "group-1",
      outcome: "started",
    },
    {
      traversalKey: "group-1",
      outcome: "failed",
      reason: "content-digest-mismatch",
    },
  ],
);

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


const missingProviderResult = acquireLocalPublicationGroup({
  plan,
  publication,
  retrievalProvider: {
    version: 1,
    getPublicationGroup() {
      return null;
    },
  },
});

assert.strictEqual(missingProviderResult.ok, false);
assert.strictEqual(missingProviderResult.reason, "publication-not-retrieved");

console.log("reflect acquisition boundary validation ok");

const unavailableSurface = {
  surfaceKey: "surface-a",
  acquirePublicationGroup() {
    return null;
  },
};

const availableSurface = {
  surfaceKey: "surface-b",
  acquirePublicationGroup({ target }) {
    assert.deepStrictEqual(target, plan.objects[0]);
    return publication;
  },
};

const selectedTargetBeforeSurfaceSubstitution = plan.objects[0];
const selectedStateDigestBeforeSurfaceSubstitution = plan.selectedStateDigest;

const substitutedSurfaceResult = acquireLocalPublicationGroup({
  plan,
  publication,
  acquisitionSurfaces: [unavailableSurface, availableSurface],
});

assert(substitutedSurfaceResult.ok);
assert.strictEqual(substitutedSurfaceResult.terminal, true);
assert.strictEqual(substitutedSurfaceResult.terminalReason, "terminal-success");
assert.deepStrictEqual(
  substitutedSurfaceResult.publication.descriptor.contentDigest,
  publication.descriptor.contentDigest,
);
assert.deepStrictEqual(
  plan.selectedStateDigest,
  selectedStateDigestBeforeSurfaceSubstitution,
);
assert.deepStrictEqual(
  plan.objects[0],
  selectedTargetBeforeSurfaceSubstitution,
);
assert.deepStrictEqual(plan.selectedStateDigest, publicationState.contentDigest);
assert.deepStrictEqual(
  substitutedSurfaceResult.completedSteps,
  [
    "plan-accepted",
    "publication-accepted",
    "selected-state-validated",
    "traversal-group-1-completed",
    "publication-acquired",
  ],
);
assert.deepStrictEqual(substitutedSurfaceResult.attempts, [
  {
    traversalKey: "group-1",
    surfaceKey: "surface-a",
    outcome: "surface-started",
  },
  {
    traversalKey: "group-1",
    surfaceKey: "surface-a",
    outcome: "surface-failed",
    reason: "publication-not-retrieved",
  },
  {
    traversalKey: "group-1",
    surfaceKey: "surface-b",
    outcome: "surface-started",
  },
  {
    traversalKey: "group-1",
    surfaceKey: "surface-b",
    outcome: "surface-succeeded",
  },
  {
    traversalKey: "group-1",
    outcome: "started",
  },
  {
    traversalKey: "group-1",
    outcome: "succeeded",
  },
]);

console.log("reflect acquisition surface substitution validation ok");
