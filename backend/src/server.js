// backend/src/server.js (M2-only)
import "dotenv/config";

import express from "express";
import cors from "cors";

import { MembershipIndexer } from "./membership/indexer.js";
import { makeMembershipRouter } from "./routes/membership.js";

const app = express();
app.use(cors());
app.use(express.json());

// ===== Config (M2-only) =====
const PORT = Number(process.env.PORT || 3001);
const CHAIN_ID = Number(process.env.CHAIN_ID || 1313161555);

// Prefer RPC_URL (your .env), fall back to old var if present
const RPC_URL =
  process.env.RPC_URL ||
  process.env.AURORA_TESTNET_RPC ||
  "https://testnet.aurora.dev";

// Accept either MEMBERSHIP_ADDRESS or MEMBERSHIP_REGISTRY_ADDRESS
const MEMBERSHIP_ADDRESS =
  process.env.MEMBERSHIP_ADDRESS || process.env.MEMBERSHIP_REGISTRY_ADDRESS;

const MEMBERSHIP_DEPTH = process.env.MEMBERSHIP_DEPTH
  ? Number(process.env.MEMBERSHIP_DEPTH)
  : 16;

if (!RPC_URL) throw new Error("RPC_URL missing");
if (!MEMBERSHIP_ADDRESS) {
  throw new Error("MEMBERSHIP_ADDRESS (or MEMBERSHIP_REGISTRY_ADDRESS) missing");
}

// ===== Indexer boot =====
const indexer = new MembershipIndexer({
  rpcUrl: RPC_URL,
  membershipAddress: MEMBERSHIP_ADDRESS,
  depth: MEMBERSHIP_DEPTH,
});

// Kick off sync once at boot (non-fatal)
indexer
  .sync(0)
  .then((r) => console.log("membership sync:", r))
  .catch((e) => console.warn("membership sync failed:", e?.message || e));

// ===== Routes =====
app.get("/health", (req, res) => {
  res.json({
    ok: true,
    mode: "M2_ONLY",
    chainId: CHAIN_ID,
    rpcUrl: RPC_URL,
    membershipAddress: MEMBERSHIP_ADDRESS,
    ts: new Date().toISOString(),
  });
});

app.use("/api/membership", makeMembershipRouter(indexer));

// Explicitly disable legacy M1 routes (clear failures, no surprises)
app.use("/api/auth", (req, res) => {
  res.status(410).json({ error: "M1 disabled. M2-only backend." });
});
app.use("/api/petition", (req, res) => {
  res.status(410).json({ error: "M1 disabled. M2-only backend." });
});
app.use("/api/m2/member-secret", (req, res) => {
  res.status(410).json({ error: "M2-only: no server-issued member secret." });
});

app.listen(PORT, () => {
  console.log(`Speak Up Backend running on port ${PORT}`);
  console.log(`Health: http://localhost:${PORT}/health`);
  console.log(`Chain ID: ${CHAIN_ID}`);
  console.log(`Mode: M2_ONLY`);
  console.log(`MembershipRegistry: ${MEMBERSHIP_ADDRESS}`);
});