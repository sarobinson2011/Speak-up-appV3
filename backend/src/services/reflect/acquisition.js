import { freezePlain } from "./objectModel.js";
import { buildLocalRetrievalProvider } from "./retrievalProvider.js";
import { selectCoherentLocalPublicationState } from "./publicationWindows.js";

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

function buildContinuation({ eligible, reason, executed = false }) {
  return freezePlain({
    eligible,
    reason: eligible ? reason : null,
    executed,
  });
}

function acquisitionOk({
  publication,
  completedSteps,
  attempts = [],
  continuation = buildContinuation({ eligible: false }),
}) {
  return freezePlain({
    ok: true,
    terminal: true,
    terminalReason: "terminal-success",
    continuationEligible: false,
    continuation,
    completedSteps,
    attempts,
    publication,
  });
}

function isContinuationEligible(reason) {
  return reason === "content-digest-mismatch";
}

function acquisitionFailed({
  reason,
  completedSteps,
  attempts = [],
  allowContinuation = true,
}) {
  const continuationEligible = allowContinuation && isContinuationEligible(reason);

  return freezePlain({
    ok: false,
    terminal: !continuationEligible,
    terminalReason: continuationEligible ? null : "terminal-failure",
    continuationEligible,
    continuation: buildContinuation({
      eligible: continuationEligible,
      reason,
    }),
    completedSteps,
    attempts,
    reason,
  });
}


function recordAttempt({ traversalKey, outcome, reason }) {
  const attempt = {
    traversalKey,
    outcome,
  };

  if (reason) attempt.reason = reason;

  return freezePlain(attempt);
}

function acquireTraversalTarget({
  target,
  traversalKey,
  publication,
  completedSteps,
  attempts,
  allowContinuation = true,
}) {
  attempts.push(recordAttempt({ traversalKey, outcome: "started" }));
  if (target?.acquisitionKey !== traversalKey) {
    attempts.push(
      recordAttempt({
        traversalKey,
        outcome: "failed",
        reason: "invalid-traversal-order",
      }),
    );

    return acquisitionFailed({
      reason: "invalid-traversal-order",
      completedSteps,
      attempts,
      allowContinuation,
    });
  }

  if (!target?.contentDigest?.value) {
    attempts.push(
      recordAttempt({
        traversalKey,
        outcome: "failed",
        reason: "invalid-target",
      }),
    );

    return acquisitionFailed({
      reason: "invalid-target",
      completedSteps,
      attempts,
      allowContinuation,
    });
  }

  if (publication.descriptor?.contentDigest?.value !== target.contentDigest.value) {
    attempts.push(
      recordAttempt({
        traversalKey,
        outcome: "failed",
        reason: "content-digest-mismatch",
      }),
    );

    return acquisitionFailed({
      reason: "content-digest-mismatch",
      completedSteps,
      attempts,
      allowContinuation,
    });
  }

  attempts.push(recordAttempt({ traversalKey, outcome: "succeeded" }));

  return freezePlain({
    ok: true,
    attempts,
    step: `traversal-${traversalKey}-completed`,
    publication,
  });
}



export function acquirePreparedPathPublication({
  publication,
  publicationState,
  publicationWindow,
}) {
  const selectedPublicationState =
    selectCoherentLocalPublicationState({
      window: publicationWindow,
      contentDigest: publicationState.contentDigest,
    });

  if (!selectedPublicationState) {
    return acquisitionFailed({
      reason: "publication-state-not-selected",
      completedSteps: [],
    });
  }

  if (selectedPublicationState.groupCount !== 1) {
    return acquisitionFailed({
      reason: "invalid-group-count",
      completedSteps: [],
    });
  }

  const acquisitionPlan = buildLocalAcquisitionPlan({
    publicationState: selectedPublicationState,
  });

  if (!acquisitionPlan) {
    return acquisitionFailed({
      reason: "invalid-acquisition-plan",
      completedSteps: [],
    });
  }

  return acquireLocalPublicationGroup({
    plan: acquisitionPlan,
    publication,
  });
}

export function acquireLocalPublicationGroup({
  plan,
  publication,
  continuationPublication,
  retrievalProvider = buildLocalRetrievalProvider({ publication }),
  continuationRetrievalProvider = continuationPublication
    ? buildLocalRetrievalProvider({ publication: continuationPublication })
    : null,
}) {
  const completedSteps = [];
  const attempts = [];

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
      attempts,
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

  if (target?.sequence !== 1) {
    return acquisitionFailed({
      reason: "invalid-sequence",
      completedSteps,
    });
  }

  if (target?.acquisitionKey !== "group-1") {
    return acquisitionFailed({
      reason: "invalid-acquisition-key",
      completedSteps,
    });
  }

  if (!retrievalProvider || typeof retrievalProvider.getPublicationGroup !== "function") {
    return acquisitionFailed({
      reason: "invalid-retrieval-provider",
      completedSteps,
      attempts,
    });
  }

  const retrievedPublication = retrievalProvider.getPublicationGroup({ target });

  if (!retrievedPublication || typeof retrievedPublication !== "object") {
    return acquisitionFailed({
      reason: "publication-not-retrieved",
      completedSteps,
      attempts,
    });
  }

  const traversalResult = acquireTraversalTarget({
    target,
    traversalKey: plan.traversalOrder[0],
    publication: retrievedPublication,
    completedSteps,
    attempts,
  });

  if (!traversalResult.ok) {
    if (!traversalResult.continuationEligible || !continuationPublication) {
      return traversalResult;
    }

    if (!continuationPublication || typeof continuationPublication !== "object") {
      return acquisitionFailed({
        reason: "invalid-continuation-publication",
        completedSteps,
        attempts,
        allowContinuation: false,
      });
    }

    const continuationSteps = [...completedSteps];
    const continuationAttempts = [...attempts];

    if (
      !continuationRetrievalProvider ||
      typeof continuationRetrievalProvider.getPublicationGroup !== "function"
    ) {
      return acquisitionFailed({
        reason: "invalid-continuation-retrieval-provider",
        completedSteps,
        attempts,
        allowContinuation: false,
      });
    }

    const retrievedContinuationPublication =
      continuationRetrievalProvider.getPublicationGroup({ target });

    if (
      !retrievedContinuationPublication ||
      typeof retrievedContinuationPublication !== "object"
    ) {
      return acquisitionFailed({
        reason: "continuation-publication-not-retrieved",
        completedSteps,
        attempts,
        allowContinuation: false,
      });
    }

    const continuationResult = acquireTraversalTarget({
      target,
      traversalKey: plan.traversalOrder[0],
      publication: retrievedContinuationPublication,
      completedSteps: continuationSteps,
      attempts: continuationAttempts,
      allowContinuation: false,
    });

    if (!continuationResult.ok) return continuationResult;

    continuationSteps.push("continuation-executed");
    continuationSteps.push(continuationResult.step);
    continuationSteps.push("publication-acquired");

    return acquisitionOk({
      publication: continuationResult.publication,
      completedSteps: continuationSteps,
      attempts: continuationResult.attempts,
      continuation: buildContinuation({
        eligible: true,
        reason: traversalResult.reason,
        executed: true,
      }),
    });
  }

  completedSteps.push(traversalResult.step);
  completedSteps.push("publication-acquired");

  return acquisitionOk({
    publication: traversalResult.publication,
    completedSteps,
    attempts: traversalResult.attempts,
  });
}
