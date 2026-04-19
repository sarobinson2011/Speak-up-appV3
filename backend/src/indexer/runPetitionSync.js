import "dotenv/config";
import { syncPetitionRegistry } from "./petitions/sync.js";

async function main() {
  try {
    console.log("[Indexer] Starting PetitionRegistry sync...");

    await syncPetitionRegistry();

    console.log("[Indexer] PetitionRegistry sync finished");
    process.exit(0);
  } catch (err) {
    console.error("[Indexer] Sync failed:", err);
    process.exit(1);
  }
}

main();