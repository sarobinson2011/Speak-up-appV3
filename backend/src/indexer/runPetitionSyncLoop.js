import "dotenv/config";
import { syncPetitionRegistry } from "./petitions/sync.js";

const POLL_MS = Number(process.env.PETITION_INDEXER_POLL_MS || 5000);

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function main() {
  console.log("[PetitionRegistry loop] starting");
  console.log("[PetitionRegistry loop] poll ms:", POLL_MS);

  while (true) {
    try {
      await syncPetitionRegistry();
    } catch (err) {
      console.error("[PetitionRegistry loop] sync failed:", err);
    }

    await sleep(POLL_MS);
  }
}

main();
