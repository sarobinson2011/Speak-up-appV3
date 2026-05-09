// backend/src/routes/membership.js
import express from "express";
import {
  getPreparedPathByIndex,
  getPreparedPathByLeaf,
  getPreparedPathReadiness,
  getPreparedPathStatus,
} from "../services/reflect/preparedPaths.js";

export function makeMembershipRouter(indexer) {
  if (!indexer) throw new Error("makeMembershipRouter requires indexer");

  const router = express.Router();

  // ---------------------------
  // Status
  // ---------------------------
  router.get("/status", async (req, res) => {
    try {
      const result = await getPreparedPathReadiness({ indexer });

      return res.status(result.status).json(result.body);
    } catch (e) {
      return res.status(500).json({
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
      const result = await getPreparedPathStatus({
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
      const result = await getPreparedPathByLeaf({
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
      const result = await getPreparedPathByIndex({
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
