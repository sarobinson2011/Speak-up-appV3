// backend/src/routes/relay.js
import express from "express";
import { ethers } from "ethers";
import { getPetitionIndexerFreshness } from "../services/indexerFreshness.js";

const ZERO_ADMISSION_COMMITMENT = "0x0000000000000000000000000000000000000000000000000000000000000000";

const RATE_LIMIT_WINDOW_MS = 60_000; // 1 minute
const SIGN_MAX_REQUESTS_PER_WINDOW = 10;
const STATUS_MAX_REQUESTS_PER_WINDOW = 30;
const HEALTH_MAX_REQUESTS_PER_WINDOW = 30;

function getClientIp(req) {
  const xff = req.headers["x-forwarded-for"];
  if (typeof xff === "string" && xff.trim()) {
    return xff.split(",")[0].trim();
  }
  return req.ip || req.socket?.remoteAddress || "unknown";
}

function createInMemoryRateLimiter({ windowMs, maxRequests, label }) {
  const hits = new Map();

  return function rateLimit(req, res, next) {
    const now = Date.now();
    const ip = getClientIp(req);
    const key = `${label}:${ip}`;

    const entry = hits.get(key);

    if (!entry || now >= entry.resetAt) {
      hits.set(key, {
        count: 1,
        resetAt: now + windowMs
      });
      return next();
    }

    if (entry.count >= maxRequests) {
      const retryAfterSec = Math.max(
        1,
        Math.ceil((entry.resetAt - now) / 1000)
      );

      return res.status(429).json({
        error: "rate limit exceeded",
        route: label,
        retryAfterSec
      });
    }

    entry.count += 1;
    return next();
  };
}

function logRelayEvent(event, data) {
  const payload = {
    ts: new Date().toISOString(),
    event,
    ...data
  };
  console.log("[relay]", JSON.stringify(payload));
}

export function makeRelayRouter({ rpcUrl, registryAddress, chainId }) {
  if (!rpcUrl) throw new Error("makeRelayRouter requires rpcUrl");
  if (!registryAddress) throw new Error("makeRelayRouter requires registryAddress");

  const RELAYER_PRIVATE_KEY = process.env.RELAYER_PRIVATE_KEY;

  if (!RELAYER_PRIVATE_KEY) {
    throw new Error("RELAYER_PRIVATE_KEY missing");
  }

  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const wallet = new ethers.Wallet(RELAYER_PRIVATE_KEY, provider);

  const registryAbi = [
    "function hasSignedPetition(uint256,bytes32) view returns (bool)",
    "function signPetitionWithZKProof(uint256,bytes32,bytes32,uint256[2],uint256[2][2],uint256[2],uint256[3])"
  ];

  const registry = new ethers.Contract(
    registryAddress,
    registryAbi,
    wallet
  );

  const statusRateLimit = createInMemoryRateLimiter({
    windowMs: RATE_LIMIT_WINDOW_MS,
    maxRequests: STATUS_MAX_REQUESTS_PER_WINDOW,
    label: "relay-status"
  });

  const healthRateLimit = createInMemoryRateLimiter({
    windowMs: RATE_LIMIT_WINDOW_MS,
    maxRequests: HEALTH_MAX_REQUESTS_PER_WINDOW,
    label: "relay-health"
  });

  const signRateLimit = createInMemoryRateLimiter({
    windowMs: RATE_LIMIT_WINDOW_MS,
    maxRequests: SIGN_MAX_REQUESTS_PER_WINDOW,
    label: "relay-sign"
  });

  const router = express.Router();

  // ---------------------------
  // Status
  // ---------------------------
  router.get("/status", statusRateLimit, async (req, res) => {
    try {
      return res.json({
        ok: true,
        mode: "relay-v1-live",
        rpcUrl,
        registryAddress,
        chainId,
        relayerAddress: wallet.address
      });
    } catch (e) {
      return res.status(500).json({
        ok: false,
        error: "internal",
        details: e?.message || String(e)
      });
    }
  });

  // ---------------------------
  // Health
  // ---------------------------
  router.get("/health", healthRateLimit, async (req, res) => {
    try {
      const [latestBlock, balanceWei] = await Promise.all([
        provider.getBlockNumber(),
        provider.getBalance(wallet.address)
      ]);

      return res.json({
        ok: true,
        mode: "relay-v1-live",
        rpcUrl,
        registryAddress,
        chainId,
        relayerAddress: wallet.address,
        relayerBalanceWei: balanceWei.toString(),
        latestBlock
      });
    } catch (e) {
      return res.status(500).json({
        ok: false,
        error: "internal",
        details: e?.message || String(e)
      });
    }
  });

  // ---------------------------
  // Relay sign
  // ---------------------------
  router.post("/sign", signRateLimit, async (req, res) => {
    let petitionIdForLog = null;
    let nullifierForLog = null;

    try {
      const {
        petitionId,
        nullifier,
        pA,
        pB,
        pC,
        pubSignals
      } = req.body || {};

      petitionIdForLog = petitionId ?? null;
      nullifierForLog = nullifier ?? null;

      if (petitionId === undefined) {
        return res.status(400).json({ error: "missing petitionId" });
      }

      try {
        BigInt(petitionId);
      } catch {
        return res.status(400).json({ error: "invalid petitionId" });
      }

      if (
        typeof nullifier !== "string" ||
        !/^0x[0-9a-fA-F]{64}$/.test(nullifier)
      ) {
        return res.status(400).json({ error: "invalid nullifier" });
      }

      const isHex = (v) => typeof v === "string" && /^0x[0-9a-fA-F]+$/.test(v);

      if (!Array.isArray(pA) || pA.length !== 2 || !pA.every(isHex)) {
        return res.status(400).json({ error: "invalid pA" });
      }

      if (
        !Array.isArray(pB) ||
        pB.length !== 2 ||
        !Array.isArray(pB[0]) ||
        !Array.isArray(pB[1]) ||
        pB[0].length !== 2 ||
        pB[1].length !== 2 ||
        !pB.flat().every(isHex)
      ) {
        return res.status(400).json({ error: "invalid pB" });
      }

      if (!Array.isArray(pC) || pC.length !== 2 || !pC.every(isHex)) {
        return res.status(400).json({ error: "invalid pC" });
      }

      if (
        !Array.isArray(pubSignals) ||
        pubSignals.length !== 3 ||
        !pubSignals.every(isHex)
      ) {
        return res.status(400).json({ error: "invalid pubSignals" });
      }

      if (
        String(pubSignals[0]).toLowerCase() !== String(nullifier).toLowerCase()
      ) {
        return res.status(400).json({
          error: "nullifier mismatch with pubSignals[0]"
        });
      }

      if (BigInt(petitionId) !== BigInt(pubSignals[1])) {
        return res.status(400).json({
          error: "petitionId mismatch with pubSignals[1]"
        });
      }

      const freshness = await getPetitionIndexerFreshness({ rpcUrl });

      if (freshness.status !== "healthy") {
        logRelayEvent("indexer-not-healthy", {
          petitionId: String(petitionId),
          nullifier,
          indexerStatus: freshness.status,
          lagBlocks: freshness.lagBlocks,
          maxAllowedLagBlocks: freshness.maxAllowedLagBlocks
        });

        return res.status(503).json({
          error: "indexer not healthy",
          indexer: freshness
        });
      }

      const alreadySigned = await registry.hasSignedPetition(
        BigInt(petitionId),
        nullifier
      );

      if (alreadySigned) {
        logRelayEvent("already-signed", {
          petitionId: String(petitionId),
          nullifier
        });

        return res.json({
          ok: true,
          alreadySigned: true
        });
      }

      const tx = await registry.signPetitionWithZKProof(
        BigInt(petitionId),
        nullifier,
        ZERO_ADMISSION_COMMITMENT,
        pA,
        pB,
        pC,
        pubSignals
      );

      logRelayEvent("submit-ok", {
        petitionId: String(petitionId),
        nullifier,
        txHash: tx.hash
      });

      return res.json({
        ok: true,
        alreadySigned: false,
        txHash: tx.hash
      });
    } catch (e) {
      logRelayEvent("submit-error", {
        petitionId: petitionIdForLog != null ? String(petitionIdForLog) : null,
        nullifier: nullifierForLog,
        error: e?.message || String(e)
      });

      return res.status(500).json({
        error: "internal",
        details: e?.message || String(e)
      });
    }
  });

  return router;
}
