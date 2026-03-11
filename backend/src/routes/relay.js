// backend/src/routes/relay.js
import express from "express";
import { ethers } from "ethers";

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
    "function signPetitionWithZKProof(uint256,bytes32,uint256[2],uint256[2][2],uint256[2],uint256[3])"
  ];

  const registry = new ethers.Contract(
    registryAddress,
    registryAbi,
    wallet
  );

  const router = express.Router();

  // ---------------------------
  // Status
  // ---------------------------
  router.get("/status", async (req, res) => {
    try {
      return res.json({
        ok: true,
        mode: "relay-v0-skeleton",
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
  // Relay sign
  // ---------------------------
  router.post("/sign", async (req, res) => {
    try {
      const {
        petitionId,
        nullifier,
        pA,
        pB,
        pC,
        pubSignals
      } = req.body || {};

      // ---------------------------
      // Validate petitionId
      // ---------------------------
      if (petitionId === undefined) {
        return res.status(400).json({ error: "missing petitionId" });
      }

      try {
        BigInt(petitionId);
      } catch {
        return res.status(400).json({ error: "invalid petitionId" });
      }

      // ---------------------------
      // Validate nullifier
      // ---------------------------
      if (
        typeof nullifier !== "string" ||
        !/^0x[0-9a-fA-F]{64}$/.test(nullifier)
      ) {
        return res.status(400).json({ error: "invalid nullifier" });
      }

      // ---------------------------
      // Validate proof arrays
      // ---------------------------
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

      // ---------------------------
      // Canonical consistency checks
      // Contract expects:
      // pubSignals = [nullifier, petitionId, membershipRoot]
      // ---------------------------
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

      // ---------------------------
      // Signed-state precheck
      // ---------------------------
      const alreadySigned = await registry.hasSignedPetition(
        BigInt(petitionId),
        nullifier
      );

      if (alreadySigned) {
        return res.json({
          ok: true,
          alreadySigned: true
        });
      }

      // ---------------------------
      // Relay transaction submit
      // ---------------------------
      const tx = await registry.signPetitionWithZKProof(
        BigInt(petitionId),
        nullifier,
        pA,
        pB,
        pC,
        pubSignals
      );

      return res.json({
        ok: true,
        alreadySigned: false,
        txHash: tx.hash
      });
    } catch (e) {
      return res.status(500).json({
        error: "internal",
        details: e?.message || String(e)
      });
    }
  });

  return router;
}