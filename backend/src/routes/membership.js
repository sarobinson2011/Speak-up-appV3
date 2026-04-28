// backend/src/routes/membership.js
import express from "express";
import { getMembershipLeafByLeaf } from "../db/repositories/membership.js";

export function makeMembershipRouter(indexer) {
  if (!indexer) throw new Error("makeMembershipRouter requires indexer");

  const router = express.Router();

  // ---------------------------
  // Status
  // ---------------------------
  router.get("/status", async (req, res) => {
    try {
      const s = await indexer.getStatus();
      res.json({
        ok: true,
        membershipAddress: indexer.membershipAddress,
        rpcUrl: indexer.rpcUrl,
        depth: indexer.depth,
        lastSyncedBlock: indexer.lastBlock || null,
        synced: Boolean(indexer.synced),
        ...s
      });
    } catch (e) {
      res.status(500).json({
        ok: false,
        error: "internal",
        details: e?.message || String(e)
      });
    }
  });
  

  // ---------------------------
  // Leaf -> coarse membership existence
  // ---------------------------
  router.get("/leaf-status", async (req, res) => {
    try {
      const leaf = String(req.query.leaf || "").trim().toLowerCase();

      if (!leaf) {
        return res.status(400).json({ error: "leaf required" });
      }

      if (!leaf.startsWith("0x") || !/^0x[0-9a-fA-F]+$/.test(leaf) || leaf.length > 66) {
        return res.status(400).json({ error: "bad leaf" });
      }

      // initial sync if we haven't synced yet
      if (!indexer.synced) await indexer.sync(0);

      let row = getMembershipLeafByLeaf(leaf);

      // minimal consistency patch: if missing, resync once and try again
      if (!row) {
        await indexer.sync(0);
        row = getMembershipLeafByLeaf(leaf);
      }

      return res.json({
        ok: true,
        exists: Boolean(row),
      });
    } catch (e) {
      return res.status(500).json({
        ok: false,
        error: "internal",
        details: e?.message || String(e),
      });
    }
  });  


  // ---------------------------
  // Leaf -> Merkle path
  // ---------------------------
  router.get("/path", async (req, res) => {
    try {
      const leaf = String(req.query.leaf || "").trim().toLowerCase();

      if (!leaf) {
        return res.status(400).json({ error: "leaf required" });
      }

      if (!leaf.startsWith("0x") || !/^0x[0-9a-fA-F]+$/.test(leaf) || leaf.length > 66) {
        return res.status(400).json({ error: "bad leaf" });
      }

      // initial sync if we haven't synced yet
      if (!indexer.synced) await indexer.sync(0);

      // try from current index
      let path = await indexer.getPathByLeaf(leaf);

      // minimal patch: if missing, resync once and try again
      if (!path) {
        await indexer.sync(0);
        path = await indexer.getPathByLeaf(leaf);
      }

      if (!path) {
        return res.status(404).json({
          error: "not_found",
          details: "leaf not found in membership index"
        });
      }

      return res.json(path);
    } catch (e) {
      return res.status(500).json({
        error: "internal",
        details: e?.message || String(e)
      });
    }
  });

  // ---------------------------
  // Index -> Merkle path
  // ---------------------------
  router.get("/pathByIndex", async (req, res) => {
    try {
      const index = req.query.index;
      if (index === undefined) {
        return res.status(400).json({ error: "index required" });
      }

      // initial sync if we haven't synced yet
      if (!indexer.synced) await indexer.sync(0);

      const idx = Number(index);

      // try from current index
      let path = await indexer.getPathByIndex(idx);

      // optional but consistent: if missing, resync once and try again
      if (!path) {
        await indexer.sync(0);
        path = await indexer.getPathByIndex(idx);
      }

      if (!path) {
        return res.status(404).json({
          error: "not_found",
          details: "index out of range or leaf missing"
        });
      }

      return res.json(path);
    } catch (e) {
      return res.status(500).json({
        error: "internal",
        details: e?.message || String(e)
      });
    }
  });

  return router;
}