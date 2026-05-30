import { freezePlain } from "./objectModel.js";

export function buildLocalRetrievalProvider({ publication }) {
  return freezePlain({
    version: 1,

    getPublicationGroup({ target }) {
      if (!target?.acquisitionKey) return null;
      if (!publication || typeof publication !== "object") return null;

      return publication;
    },
  });
}
