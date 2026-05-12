import {
  acceptLocalPublicationState,
} from "./publicationObjects.js";
import {
  freezePlain,
} from "./objectModel.js";

function isPositiveInteger(value) {
  return Number.isInteger(value) && value > 0;
}

function normalizeWindowLimit(rawLimit) {
  const limit = Number(rawLimit);
  if (!isPositiveInteger(limit)) return null;
  return limit;
}

export function buildLocalPublicationWindow({ states, limit }) {
  const maxEntries = normalizeWindowLimit(limit);
  if (!maxEntries) return null;
  if (!Array.isArray(states)) return null;
  if (states.length === 0) return null;
  if (states.length > maxEntries) return null;
  const entries = states.map((state, position) => {
    const accepted = acceptLocalPublicationState(state);
    if (!accepted) return null;
    return freezePlain({
      position,
      sequence: position + 1,
      state: accepted,
      contentDigest: accepted.contentDigest,
    });
  });
  if (entries.some((entry) => !entry)) return null;
  return freezePlain({ version: 1, limit: maxEntries, entryCount: entries.length, entries });
}

export function selectLocalPublicationState(window) {
  if (!window || typeof window !== "object") return null;
  if (!Number.isInteger(window.version) || window.version <= 0) return null;
  if (!isPositiveInteger(window.limit)) return null;
  if (!Array.isArray(window.entries)) return null;
  if (window.entries.length !== window.entryCount) return null;
  if (window.entries.length === 0) return null;
  if (window.entries.length > window.limit) return null;

  for (let i = 0; i < window.entries.length; i++) {
    const entry = window.entries[i];

    if (!isPositiveInteger(entry?.sequence)) return null;
    if (entry.sequence !== i + 1) return null;
  }

  const selected = window.entries[window.entries.length - 1];
  if (!selected?.state) return null;
  return freezePlain(selected.state);
}

export function selectCoherentLocalPublicationState({ window, contentDigest }) {
  const selected = selectLocalPublicationState(window);

  if (!selected) return null;
  if (!contentDigest?.value) return null;
  if (selected.contentDigest?.value !== contentDigest.value) return null;

  return freezePlain(selected);
}
