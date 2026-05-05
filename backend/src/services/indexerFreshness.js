import { JsonRpcProvider } from "ethers";
import { getSyncCursor } from "../db/repositories/syncState.js";

export const DEFAULT_MAX_INDEXER_LAG_BLOCKS = 25;

export function getMaxIndexerLagBlocks() {
  const raw = process.env.MAX_INDEXER_LAG_BLOCKS;
  if (raw === undefined || raw === "") return DEFAULT_MAX_INDEXER_LAG_BLOCKS;

  const parsed = Number(raw);
  if (!Number.isInteger(parsed) || parsed < 0) {
    throw new Error(`Invalid MAX_INDEXER_LAG_BLOCKS: ${raw}`);
  }

  return parsed;
}

export async function getPetitionIndexerFreshness({ rpcUrl }) {
  if (!rpcUrl) throw new Error("getPetitionIndexerFreshness requires rpcUrl");

  const provider = new JsonRpcProvider(rpcUrl);

  const [latestBlock, petitionCursor] = await Promise.all([
    provider.getBlockNumber(),
    Promise.resolve(getSyncCursor("PetitionRegistry")),
  ]);

  const lastProcessedBlock = petitionCursor?.last_processed_block ?? null;

  const lagBlocks =
    lastProcessedBlock == null
      ? null
      : Math.max(0, latestBlock - Number(lastProcessedBlock));

  const maxAllowedLagBlocks = getMaxIndexerLagBlocks();

  const status =
    lagBlocks == null
      ? "unknown"
      : lagBlocks > maxAllowedLagBlocks
        ? "degraded"
        : "healthy";

  return {
    status,
    lastProcessedBlock,
    latestBlock,
    lagBlocks,
    maxAllowedLagBlocks,
    updatedAt: petitionCursor?.updated_at ?? null,
  };
}
