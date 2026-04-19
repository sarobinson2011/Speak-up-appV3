import { JsonRpcProvider, id } from "ethers";
import { getSyncCursor, updateSyncCursor, } from "../../db/repositories/syncState.js";
import { processPetitionLogs } from "./processor.js";

const RPC_URL = process.env.RPC_URL;
const PETITION_REGISTRY_ADDRESS = process.env.PETITION_REGISTRY_ADDRESS;

const rawStartBlock = process.env.PETITION_REGISTRY_START_BLOCK;
const PETITION_REGISTRY_START_BLOCK =
  rawStartBlock === undefined ? 0 : Number(rawStartBlock);

const rawBatchSize = process.env.INDEXER_BLOCK_BATCH_SIZE;
const BLOCK_BATCH_SIZE =
  rawBatchSize === undefined ? 1000 : Number(rawBatchSize);

const PETITION_CREATED_TOPIC = id(
  "PetitionCreated(uint256,address,string)"
);

const PETITION_SIGNED_TOPIC = id(
  "PetitionSigned(uint256,bytes32,bytes32)"
);

if (
  !Number.isInteger(PETITION_REGISTRY_START_BLOCK) ||
  PETITION_REGISTRY_START_BLOCK < 0
) {
  throw new Error(
    `Invalid PETITION_REGISTRY_START_BLOCK: ${rawStartBlock}`
  );
}

if (!Number.isInteger(BLOCK_BATCH_SIZE) || BLOCK_BATCH_SIZE <= 0) {
  throw new Error(
    `Invalid INDEXER_BLOCK_BATCH_SIZE: ${rawBatchSize}`
  );
}

export async function syncPetitionRegistry() {
  if (!RPC_URL) {
    throw new Error("Missing RPC_URL");
  }

  if (!PETITION_REGISTRY_ADDRESS) {
    throw new Error("Missing PETITION_REGISTRY_ADDRESS");
  }

  const provider = new JsonRpcProvider(RPC_URL);

  const cursor = getSyncCursor("PetitionRegistry");
  const latestBlock = await provider.getBlockNumber();

  let fromBlock =
    cursor && cursor.last_processed_block > 0
      ? cursor.last_processed_block
      : PETITION_REGISTRY_START_BLOCK;

  console.log("[PetitionRegistry] RPC_URL:", RPC_URL);
  console.log("[PetitionRegistry] address:", PETITION_REGISTRY_ADDRESS);
  console.log("[PetitionRegistry] start block:", PETITION_REGISTRY_START_BLOCK);
  console.log("[PetitionRegistry] cursor:", cursor);
  console.log("[PetitionRegistry] latest block:", latestBlock);

  while (fromBlock <= latestBlock) {
    const toBlock = Math.min(fromBlock + BLOCK_BATCH_SIZE - 1, latestBlock);

    console.log(
      `[PetitionRegistry] syncing blocks ${fromBlock} -> ${toBlock}`
    );

    const logs = await provider.getLogs({
      address: PETITION_REGISTRY_ADDRESS,
      fromBlock,
      toBlock,
      topics: [[PETITION_CREATED_TOPIC, PETITION_SIGNED_TOPIC]],
    });

    console.log(
      `[PetitionRegistry] fetched ${logs.length} raw logs in range ${fromBlock} -> ${toBlock}`
    );

    logs.sort((a, b) => {
      if (a.blockNumber !== b.blockNumber) {
        return a.blockNumber - b.blockNumber;
      }
      if (a.transactionIndex !== b.transactionIndex) {
        return a.transactionIndex - b.transactionIndex;
      }
      return a.logIndex - b.logIndex;
    });

    await processPetitionLogs(logs, provider);

    updateSyncCursor(
      "PetitionRegistry",
      toBlock,
      null,
      null,
      Math.floor(Date.now() / 1000)
    );

    fromBlock = toBlock + 1;
  }

  console.log("[PetitionRegistry] sync complete");
}