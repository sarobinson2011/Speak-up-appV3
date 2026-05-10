import { createHash } from "crypto";

export const REFLECT_ENVELOPE_VERSION = 1;
export const REFLECT_DIGEST_ALGORITHM = "sha256";

export const REFLECT_TYPES = freezePlain({
  PREPARED_PATH: "prepared-path",
  CONNECTOR: "connector",
  CHUNK: "chunk",
});

export function freezePlain(value) {
  if (Array.isArray(value)) {
    for (const item of value) freezePlain(item);
    return Object.freeze(value);
  }

  if (value && typeof value === "object") {
    for (const item of Object.values(value)) freezePlain(item);
    return Object.freeze(value);
  }

  return value;
}

export function canonicalValue(value) {
  if (Array.isArray(value)) {
    return value.map(canonicalValue);
  }

  if (value && typeof value === "object") {
    const out = {};
    for (const key of Object.keys(value).sort()) {
      out[key] = canonicalValue(value[key]);
    }
    return out;
  }

  return value;
}

export function canonicalString(value) {
  return JSON.stringify(canonicalValue(value));
}

export function digestReflectMaterial(material) {
  return createHash(REFLECT_DIGEST_ALGORITHM)
    .update(canonicalString(material))
    .digest("hex");
}

export function buildReflectEnvelope({ type, material, coherence }) {
  if (!type || !material || !coherence) return null;

  return freezePlain({
    type,
    version: REFLECT_ENVELOPE_VERSION,
    digest: {
      algorithm: REFLECT_DIGEST_ALGORITHM,
      value: digestReflectMaterial(material),
    },
    coherence,
    material,
  });
}

export function serializeReflectObject(envelope) {
  if (!envelope || typeof envelope !== "object") return null;

  return canonicalString(envelope);
}

export function parseReflectObject(serialized) {
  if (typeof serialized !== "string" || serialized.length === 0) return null;

  try {
    return freezePlain(JSON.parse(serialized));
  } catch {
    return null;
  }
}
