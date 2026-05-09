// backend/src/routes/membership.js
import express from "express";
import {
  getPathObjectByIndex,
  getPathObjectByLeaf,
  getPathObjectStatus,
} from "../services/reflect/pathObjects.js";

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
  // Coarse membership existence
  // ---------------------------
  router.get("/leaf-status", async (req, res) => {
    try {
      const result = await getPathObjectStatus({
        indexer,
        leaf: req.query.leaf,
      });

      return res.status(result.status).json(result.body);
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
      const result = await getPathObjectByLeaf({
        indexer,
        leaf: req.query.leaf,
      });

      return res.status(result.status).json(result.body);
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
      const result = await getPathObjectByIndex({
        indexer,
        index: req.query.index,
      });

      return res.status(result.status).json(result.body);
    } catch (e) {
      return res.status(500).json({
        error: "internal",
        details: e?.message || String(e)
      });
    }
  });

  return router;
}