import "dotenv/config";
import { syncMembership } from "./membership/sync.js";

async function main() {
  console.log("[Indexer] Starting membership sync...");
  await syncMembership();
  console.log("[Indexer] Membership sync finished");
}

main();