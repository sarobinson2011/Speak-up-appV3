import { freezePlain } from "./objectModel.js";

export function buildLocalAcquisitionPlan({ publicationState }) {
  if (!publicationState || typeof publicationState !== "object") return null;
  if (!Array.isArray(publicationState.entries)) return null;
  if (publicationState.entries.length !== publicationState.groupCount) return null;
  if (!publicationState.contentDigest?.value) return null;

  const objects = publicationState.entries.map((entry, index) => {
    if (entry.sequence !== undefined) return null;
    if (!entry?.descriptor?.contentDigest?.value) return null;
    if (entry.contentDigest?.value !== entry.descriptor.contentDigest.value) return null;

    return freezePlain({
      sequence: index + 1,
      acquisitionKey: `group-${index + 1}`,
      contentDigest: entry.contentDigest,
      descriptor: entry.descriptor,
    });
  });

  if (objects.some((object) => !object)) return null;

  return freezePlain({
    version: 1,
    selectedStateDigest: publicationState.contentDigest,
    objectCount: objects.length,
    traversalOrder: objects.map((object) => object.acquisitionKey),
    objects,
  });
}

function acquisitionOk({ publication, completedSteps }) {
  return freezePlain({
    ok: true,
    completedSteps,
    publication,
  });
}

function acquisitionFailed({ reason, completedSteps }) {
  return freezePlain({
    ok: false,
    completedSteps,
    reason,
  });
}

export function acquireLocalPublicationGroup({ plan, publication }) {
  const completedSteps = [];

  if (!plan || typeof plan !== "object") {
    return acquisitionFailed({
      reason: "invalid-plan",
      completedSteps,
    });
  }

  completedSteps.push("plan-accepted");

  if (!publication || typeof publication !== "object") {
    return acquisitionFailed({
      reason: "invalid-publication",
      completedSteps,
    });
  }

  completedSteps.push("publication-accepted");

  if (!plan.selectedStateDigest?.value) {
    return acquisitionFailed({
      reason: "invalid-selected-state",
      completedSteps,
    });
  }

  completedSteps.push("selected-state-validated");
  if (!Array.isArray(plan.objects)) return acquisitionFailed({
      reason: "invalid-objects",
      completedSteps,
    });
  if (!Array.isArray(plan.traversalOrder)) return acquisitionFailed({
      reason: "invalid-traversal-order",
      completedSteps,
    });
  if (plan.objects.length !== plan.objectCount) return acquisitionFailed({
      reason: "object-count-mismatch",
      completedSteps,
    });
  if (plan.traversalOrder.length !== plan.objectCount) {
    return acquisitionFailed({
      reason: "traversal-order-mismatch",
      completedSteps,
    });
  }
  if (plan.objectCount !== 1) return acquisitionFailed({
      reason: "unsupported-object-count",
      completedSteps,
    });

  const target = plan.objects?.[0];

  if (target?.sequence !== 1) return acquisitionFailed({
      reason: "invalid-sequence",
      completedSteps,
    });
  if (target?.acquisitionKey !== "group-1") {
    return acquisitionFailed({
      reason: "invalid-acquisition-key",
      completedSteps,
    });
  }

  if (plan.traversalOrder[0] !== target.acquisitionKey) {
    return acquisitionFailed({
      reason: "invalid-traversal-order",
      completedSteps,
    });
  }

  if (!target?.contentDigest?.value) return acquisitionFailed({
      reason: "invalid-target",
      completedSteps,
    });
  if (publication.descriptor?.contentDigest?.value !== target.contentDigest.value) {
    return acquisitionFailed({
      reason: "content-digest-mismatch",
      completedSteps,
    });
  }

  completedSteps.push("publication-acquired");

  return acquisitionOk({
    publication,
    completedSteps,
  });
}
