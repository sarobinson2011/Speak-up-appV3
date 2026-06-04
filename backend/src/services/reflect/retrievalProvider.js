import { freezePlain } from "./objectModel.js";

export function buildLocalPublicationRegistry({ publicationsByAcquisitionKey }) {
  const entries =
    publicationsByAcquisitionKey && typeof publicationsByAcquisitionKey === "object"
      ? publicationsByAcquisitionKey
      : {};

  return freezePlain({
    version: 1,

    get(acquisitionKey) {
      if (!acquisitionKey) return null;

      const publication = entries[acquisitionKey];

      if (!publication || typeof publication !== "object") return null;

      return publication;
    },
  });
}

export function buildLocalRetrievalProvider({
  publication,
  publicationRegistry = buildLocalPublicationRegistry({
    publicationsByAcquisitionKey: publication
      ? {
          "group-1": publication,
        }
      : {},
  }),
}) {
  return freezePlain({
    version: 1,

    getPublicationGroup({ target }) {
      if (!target?.acquisitionKey) return null;
      if (!publicationRegistry || typeof publicationRegistry.get !== "function") return null;

      return publicationRegistry.get(target.acquisitionKey);
    },
  });
}
