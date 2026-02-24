// backend/src/routes/membership.js
import express from "express";

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
  // Wallet -> Merkle path
  // ---------------------------
  router.get("/path", async (req, res) => {
    try {
      const wallet = String(req.query.wallet || "").trim();
      if (!wallet || !wallet.startsWith("0x") || wallet.length < 10) {
        return res.status(400).json({ error: "bad wallet" });
      }

      // initial sync if we haven't synced yet
      if (!indexer.synced) await indexer.sync(0);

      const walletLower = wallet.toLowerCase();

      // try from current index
      let path = await indexer.getPath(walletLower);

      // minimal patch: if missing, resync once and try again
      if (!path) {
        await indexer.sync(0);
        path = await indexer.getPath(walletLower);
      }

      if (!path) {
        return res.status(404).json({
          error: "not_found",
          details: "wallet not found in membership index"
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

  // ---------------------------
  // Manual enrollment (DEV / MVP ONLY)
  // ---------------------------
  router.post("/enroll", async (req, res) => {
    try {
      const { wallet, leaf } = req.body || {};

      if (!wallet || !leaf) {
        return res.status(400).json({ error: "wallet and leaf required" });
      }

      if (!wallet.startsWith("0x") || wallet.length < 10) {
        return res.status(400).json({ error: "invalid wallet" });
      }

      if (!leaf.startsWith("0x") || leaf.length !== 66) {
        return res.status(400).json({ error: "invalid leaf (must be 32-byte hex)" });
      }

      const walletLower = wallet.toLowerCase();

      await indexer.addManualMember(walletLower, leaf);

      return res.json({
        success: true,
        wallet: walletLower,
        leaf,
        root: indexer.root
      });
    } catch (e) {
      console.error("Enroll error:", e);
      return res.status(500).json({
        error: "internal",
        details: e?.message || String(e)
      });
    }
  });

  return router;
}