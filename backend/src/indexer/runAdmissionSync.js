import "dotenv/config";
import { syncAdmission } from "./admission/sync.js";

async function main() {
  console.log("[Indexer] Starting admission sync...");
  await syncAdmission();
  console.log("[Indexer] Admission sync finished");
}

main();