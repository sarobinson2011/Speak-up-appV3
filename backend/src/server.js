// backend/src/server.js (M2-only)
import "dotenv/config";

import express from "express";
import cors from "cors";

import { MembershipIndexer } from "./membership/indexer.js";
import { makeMembershipRouter } from "./routes/membership.js";
import { makeRelayRouter } from "./routes/relay.js";
import { makePetitionsRouter } from "./routes/petitions.js";
import { makeAdmissionRouter } from "./routes/admission.js";
import { makeIndexerRouter } from "./routes/indexer.js";

const app = express();
app.use(cors());
app.use(express.json({ limit: "16kb" }));
app.use("/api/admission", makeAdmissionRouter());

// ===== Config (M2-only) =====
const PORT = Number(process.env.PORT || 3001);
const CHAIN_ID = Number(process.env.CHAIN_ID || 1313161555);

// Prefer RPC_URL (your .env), fall back to old var if present
const RPC_URL =
  process.env.RPC_URL ||
  process.env.AURORA_TESTNET_RPC ||
  "https://testnet.aurora.dev";

// Canonical env name first, legacy aliases only as temporary fallback.
const anonMembershipRegistryAddress =
  process.env.ANON_MEMBERSHIP_PROXY_ADDRESS ||
  process.env.MEMBERSHIP_REGISTRY_ADDRESS ||
  process.env.MEMBERSHIP_ADDRESS;

const usingLegacyMembershipEnv =
  !process.env.ANON_MEMBERSHIP_PROXY_ADDRESS &&
  (process.env.MEMBERSHIP_REGISTRY_ADDRESS || process.env.MEMBERSHIP_ADDRESS);

const PETITION_REGISTRY_ADDRESS = process.env.PETITION_REGISTRY_ADDRESS;

if (!PETITION_REGISTRY_ADDRESS) {
  throw new Error("PETITION_REGISTRY_ADDRESS missing");
}

const MEMBERSHIP_DEPTH = process.env.MEMBERSHIP_DEPTH
  ? Number(process.env.MEMBERSHIP_DEPTH)
  : 16;

if (!RPC_URL) throw new Error("RPC_URL missing");
if (!anonMembershipRegistryAddress) {
  throw new Error(
    "ANON_MEMBERSHIP_PROXY_ADDRESS missing (legacy aliases: MEMBERSHIP_REGISTRY_ADDRESS, MEMBERSHIP_ADDRESS)"
  );
}

if (usingLegacyMembershipEnv) {
  console.warn(
    "[deprecated] Using legacy membership env var. Please migrate to ANON_MEMBERSHIP_PROXY_ADDRESS."
  );
}

// ===== Indexer boot =====
const indexer = new MembershipIndexer({
  depth: MEMBERSHIP_DEPTH,
});

// Kick off sync once at boot (non-fatal)
indexer
  .sync()
  .then((r) => console.log("membership sync:", r))
  .catch((e) => console.warn("membership sync failed:", e?.message || e));

// ===== Routes =====
app.get("/health", (req, res) => {
  res.json({
    ok: true,
    mode: "M2_ONLY",
    chainId: CHAIN_ID,
    rpcUrl: RPC_URL,
    membershipAddress: anonMembershipRegistryAddress,
    ts: new Date().toISOString(),
  });
});

app.use("/api/membership", makeMembershipRouter(indexer));

app.use("/api/petitions", makePetitionsRouter());

app.use(
  "/api/indexer",
  makeIndexerRouter({
    rpcUrl: RPC_URL,
  })
);

app.use(
  "/api/relay",
  makeRelayRouter({
    rpcUrl: RPC_URL,
    registryAddress: PETITION_REGISTRY_ADDRESS,
    chainId: CHAIN_ID,
  })
);

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
  console.log(`AnonymousMembershipRegistry: ${anonMembershipRegistryAddress}`);
});