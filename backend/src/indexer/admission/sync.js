import { JsonRpcProvider, id } from "ethers";
import {
  getSyncCursor,
  updateSyncCursor,
} from "../../db/repositories/syncState.js";
import { processAdmissionLogs } from "./processor.js";

const RPC_URL = process.env.RPC_URL;
const ADMISSION_ADDRESS = process.env.ADMISSION_REGISTRY_ADDRESS;

const rawStartBlock = process.env.ADMISSION_START_BLOCK;
const START_BLOCK =
  rawStartBlock === undefined ? 0 : Number(rawStartBlock);

const rawBatchSize = process.env.INDEXER_BLOCK_BATCH_SIZE;
const BATCH_SIZE =
  rawBatchSize === undefined ? 10000 : Number(rawBatchSize);

if (!Number.isInteger(START_BLOCK) || START_BLOCK < 0) {
  throw new Error(`Invalid ADMISSION_START_BLOCK: ${rawStartBlock}`);
}

if (!Number.isInteger(BATCH_SIZE) || BATCH_SIZE <= 0) {
  throw new Error(`Invalid INDEXER_BLOCK_BATCH_SIZE: ${rawBatchSize}`);
}

const FUNDED_TOPIC = id(
  "AdmissionRightFunded(bytes32,uint256,uint256)"
);
const CONSUMED_TOPIC = id("AdmissionRightConsumed(bytes32)");
const REFUNDED_TOPIC = id(
  "AdmissionRightRefunded(bytes32,address,uint256)"
);

export async function syncAdmission() {
  if (!RPC_URL) throw new Error("Missing RPC_URL");
  if (!ADMISSION_ADDRESS) throw new Error("Missing ADMISSION_REGISTRY_ADDRESS");

  const provider = new JsonRpcProvider(RPC_URL);

  const cursor = getSyncCursor("AdmissionRegistry");
  const latestBlock = await provider.getBlockNumber();

  let fromBlock =
    cursor && cursor.last_processed_block > 0
      ? cursor.last_processed_block
      : START_BLOCK;

  console.log("[Admission] RPC_URL:", RPC_URL);
  console.log("[Admission] address:", ADMISSION_ADDRESS);
  console.log("[Admission] start block:", START_BLOCK);
  console.log("[Admission] cursor:", cursor);
  console.log("[Admission] latest block:", latestBlock);

  while (fromBlock <= latestBlock) {
    const toBlock = Math.min(fromBlock + BATCH_SIZE - 1, latestBlock);

    console.log(`[Admission] syncing ${fromBlock} -> ${toBlock}`);

    const logs = await provider.getLogs({
      address: ADMISSION_ADDRESS,
      fromBlock,
      toBlock,
      topics: [[FUNDED_TOPIC, CONSUMED_TOPIC, REFUNDED_TOPIC]],
    });

    console.log(
      `[Admission] fetched ${logs.length} raw logs in range ${fromBlock} -> ${toBlock}`
    );

    logs.sort((a, b) => {
      if (a.blockNumber !== b.blockNumber) return a.blockNumber - b.blockNumber;
      if (a.transactionIndex !== b.transactionIndex) {
        return a.transactionIndex - b.transactionIndex;
      }
      return (a.index ?? 0) - (b.index ?? 0);
    });

    await processAdmissionLogs(logs, provider);

    updateSyncCursor(
      "AdmissionRegistry",
      toBlock,
      null,
      null,
      Math.floor(Date.now() / 1000)
    );

    fromBlock = toBlock + 1;
  }

  console.log("[Admission] sync complete");
}