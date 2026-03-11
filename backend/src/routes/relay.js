// backend/src/routes/relay.js
import express from "express";

export function makeRelayRouter({ rpcUrl, registryAddress, chainId }) {
  if (!rpcUrl) throw new Error("makeRelayRouter requires rpcUrl");
  if (!registryAddress) throw new Error("makeRelayRouter requires registryAddress");

  const router = express.Router();

  router.get("/status", async (req, res) => {
    try {
      return res.json({
        ok: true,
        mode: "relay-v0-skeleton",
        rpcUrl,
        registryAddress,
        chainId
      });
    } catch (e) {
      return res.status(500).json({
        ok: false,
        error: "internal",
        details: e?.message || String(e)
      });
    }
  });

  return router;
}