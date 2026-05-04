import express from "express";
import { JsonRpcProvider } from "ethers";
import { getSyncCursor } from "../db/repositories/syncState.js";

export function makeIndexerRouter({ rpcUrl }) {
  if (!rpcUrl) throw new Error("makeIndexerRouter requires rpcUrl");

  const router = express.Router();
  const provider = new JsonRpcProvider(rpcUrl);

  router.get("/status", async (req, res) => {
    try {
      const [latestBlock, petitionCursor] = await Promise.all([
        provider.getBlockNumber(),
        Promise.resolve(getSyncCursor("PetitionRegistry")),
      ]);

      const lastProcessedBlock =
        petitionCursor?.last_processed_block ?? null;

      const lagBlocks =
        lastProcessedBlock == null
          ? null
          : Math.max(0, latestBlock - Number(lastProcessedBlock));

      return res.json({
        ok: true,
        petitionIndexer: {
          lastProcessedBlock,
          latestBlock,
          lagBlocks,
          updatedAt: petitionCursor?.updated_at ?? null,
        },
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
