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
      contentDigest: entry.contentDigest,
      descriptor: entry.descriptor,
    });
  });

  if (objects.some((object) => !object)) return null;

  return freezePlain({
    version: 1,
    selectedStateDigest: publicationState.contentDigest,
    objectCount: objects.length,
    objects,
  });
}

function acquisitionOk(publication) {
  return freezePlain({
    ok: true,
    publication,
  });
}

function acquisitionFailed(reason) {
  return freezePlain({
    ok: false,
    reason,
  });
}

export function acquireLocalPublicationGroup({ plan, publication }) {
  if (!plan || typeof plan !== "object") return acquisitionFailed("invalid-plan");
  if (!publication || typeof publication !== "object") return acquisitionFailed("invalid-publication");

  if (!plan.selectedStateDigest?.value) return acquisitionFailed("invalid-selected-state");
  if (!Array.isArray(plan.objects)) return acquisitionFailed("invalid-objects");
  if (plan.objects.length !== plan.objectCount) return acquisitionFailed("object-count-mismatch");
  if (plan.objectCount !== 1) return acquisitionFailed("unsupported-object-count");

  const target = plan.objects?.[0];

  if (target?.sequence !== 1) return acquisitionFailed("invalid-sequence");

  if (!target?.contentDigest?.value) return acquisitionFailed("invalid-target");
  if (publication.descriptor?.contentDigest?.value !== target.contentDigest.value) {
    return acquisitionFailed("content-digest-mismatch");
  }

  return acquisitionOk(publication);
}
