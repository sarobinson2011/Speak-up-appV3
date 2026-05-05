import express from "express";
import { getPetitionIndexerFreshness } from "../services/indexerFreshness.js";

export function makeIndexerRouter({ rpcUrl }) {
  if (!rpcUrl) throw new Error("makeIndexerRouter requires rpcUrl");

  const router = express.Router();

  router.get("/status", async (req, res) => {
    try {
      const petitionIndexer = await getPetitionIndexerFreshness({ rpcUrl });

      return res.json({
        ok: true,
        petitionIndexer,
      });
    } catch (e) {
      return res.status(500).json({
        ok: false,
        error: "internal",
        details: e?.message || String(e),
      });
    }
  });

  return router;
}
