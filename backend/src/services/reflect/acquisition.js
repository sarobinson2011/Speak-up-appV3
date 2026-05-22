import { freezePlain } from "./objectModel.js";

export function buildLocalAcquisitionPlan({ publicationState }) {
  if (!publicationState || typeof publicationState !== "object") return null;
  if (!Array.isArray(publicationState.entries)) return null;
  if (publicationState.entries.length !== publicationState.groupCount) return null;
  if (!publicationState.contentDigest?.value) return null;

  const objects = publicationState.entries.map((entry, index) => {
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

export function acquireLocalPublicationGroup({ plan, publication }) {
  if (!plan || typeof plan !== "object") return null;
  if (!publication || typeof publication !== "object") return null;
  if (plan.objectCount !== 1) return null;

  const target = plan.objects?.[0];

  if (!target?.contentDigest?.value) return null;
  if (publication.descriptor?.contentDigest?.value !== target.contentDigest.value) {
    return null;
  }

  return freezePlain(publication);
}
