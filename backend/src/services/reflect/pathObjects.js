import { getMembershipLeafByLeaf } from "../../db/repositories/membership.js";

function normalizeLeafInput(rawLeaf) {
  const leaf = String(rawLeaf || "").trim().toLowerCase();

  if (!leaf) {
    return { ok: false, status: 400, body: { error: "leaf required" } };
  }

  if (!leaf.startsWith("0x") || !/^0x[0-9a-fA-F]+$/.test(leaf) || leaf.length > 66) {
    return { ok: false, status: 400, body: { error: "bad leaf" } };
  }

  return { ok: true, leaf };
}

async function ensureCurrent(indexer) {
  if (!indexer.synced) await indexer.sync(0);
}

async function resyncOnce(indexer) {
  await indexer.sync(0);
}

export async function getPathObjectStatus({ indexer, leaf: rawLeaf }) {
  const normalized = normalizeLeafInput(rawLeaf);
  if (!normalized.ok) return normalized;

  const { leaf } = normalized;

  await ensureCurrent(indexer);

  let row = getMembershipLeafByLeaf(leaf);

  if (!row) {
    await resyncOnce(indexer);
    row = getMembershipLeafByLeaf(leaf);
  }

  return {
    ok: true,
    status: 200,
    body: {
      ok: true,
      exists: Boolean(row),
    },
  };
}

export async function getPathObjectByLeaf({ indexer, leaf: rawLeaf }) {
  const normalized = normalizeLeafInput(rawLeaf);
  if (!normalized.ok) return normalized;

  const { leaf } = normalized;

  await ensureCurrent(indexer);

  let pathObject = await indexer.getPathByLeaf(leaf);

  if (!pathObject) {
    await resyncOnce(indexer);
    pathObject = await indexer.getPathByLeaf(leaf);
  }

  if (!pathObject) {
    return {
      ok: false,
      status: 404,
      body: {
        error: "not_found",
        details: "leaf not found",
      },
    };
  }

  return {
    ok: true,
    status: 200,
    body: pathObject,
  };
}

export async function getPathObjectByIndex({ indexer, index }) {
  if (index === undefined) {
    return { ok: false, status: 400, body: { error: "index required" } };
  }

  await ensureCurrent(indexer);

  const idx = Number(index);

  let pathObject = await indexer.getPathByIndex(idx);

  if (!pathObject) {
    await resyncOnce(indexer);
    pathObject = await indexer.getPathByIndex(idx);
  }

  if (!pathObject) {
    return {
      ok: false,
      status: 404,
      body: {
        error: "not_found",
        details: "leaf not found",
      },
    };
  }

  return {
    ok: true,
    status: 200,
    body: pathObject,
  };
}
