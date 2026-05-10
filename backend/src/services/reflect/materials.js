import { freezePlain } from "./objectModel.js";

function isHexString(value) {
  return typeof value === "string" && /^0x[0-9a-fA-F]+$/.test(value);
}

export function normalizeHexValue(value) {
  if (!isHexString(value)) return null;
  return value.toLowerCase();
}

export function normalizePathBits(pathBits) {
  if (!Array.isArray(pathBits)) return null;

  const normalized = [];

  for (const bit of pathBits) {
    if (bit !== 0 && bit !== 1) return null;
    normalized.push(bit);
  }

  return normalized;
}

export function normalizeSiblingValues(siblings) {
  if (!Array.isArray(siblings)) return null;

  const normalized = [];

  for (const sibling of siblings) {
    const value = normalizeHexValue(sibling);
    if (!value) return null;
    normalized.push(value);
  }

  return normalized;
}

export function normalizePreparedPathMaterial(material) {
  if (!material || typeof material !== "object") return null;

  const leaf = normalizeHexValue(material.leaf);
  const root = normalizeHexValue(material.root);
  const index = Number(material.index);
  const siblings = normalizeSiblingValues(material.siblings);
  const pathBits = normalizePathBits(material.pathBits);

  if (!leaf || !root) return null;
  if (!Number.isInteger(index) || index < 0) return null;
  if (!siblings || !pathBits) return null;
  if (siblings.length !== pathBits.length) return null;

  return freezePlain({
    leaf,
    index,
    root,
    siblings,
    pathBits,
  });
}