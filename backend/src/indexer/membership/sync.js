import { JsonRpcProvider, id } from "ethers";
import {
  getSyncCursor,
  updateSyncCursor,
} from "../../db/repositories/syncState.js";
import { processMembershipLogs } from "./processor.js";

const RPC_URL = process.env.RPC_URL;
const MEMBERSHIP_ADDRESS = process.env.ANON_MEMBERSHIP_PROXY_ADDRESS;

const rawStartBlock = process.env.MEMBERSHIP_START_BLOCK;
const START_BLOCK =
  rawStartBlock === undefined ? 0 : Number(rawStartBlock);

const rawBatchSize = process.env.INDEXER_BLOCK_BATCH_SIZE;
const BATCH_SIZE =
  rawBatchSize === undefined ? 10000 : Number(rawBatchSize);

if (!Number.isInteger(START_BLOCK) || START_BLOCK < 0) {
  throw new Error(`Invalid MEMBERSHIP_START_BLOCK: ${rawStartBlock}`);
}

if (!Number.isInteger(BATCH_SIZE) || BATCH_SIZE <= 0) {
  throw new Error(`Invalid INDEXER_BLOCK_BATCH_SIZE: ${rawBatchSize}`);
}

const LEAF_REGISTERED_TOPIC = id(
  "LeafRegistered(bytes32,uint256,bytes32)"
);

export async function syncMembership() {
  if (!RPC_URL) throw new Error("Missing RPC_URL");
  if (!MEMBERSHIP_ADDRESS) throw new Error("Missing membership address");

  const provider = new JsonRpcProvider(RPC_URL);

  const cursor = getSyncCursor("AnonymousMembershipRegistry");
  const latestBlock = await provider.getBlockNumber();

  let fromBlock =
    cursor && cursor.last_processed_block > 0
      ? cursor.last_processed_block
      : START_BLOCK;

  console.log("[Membership] RPC_URL:", RPC_URL);
  console.log("[Membership] address:", MEMBERSHIP_ADDRESS);
  console.log("[Membership] start block:", START_BLOCK);
  console.log("[Membership] cursor:", cursor);
  console.log("[Membership] latest block:", latestBlock);

  while (fromBlock <= latestBlock) {
    const toBlock = Math.min(fromBlock + BATCH_SIZE - 1, latestBlock);

    console.log(`[Membership] syncing ${fromBlock} -> ${toBlock}`);

    const logs = await provider.getLogs({
      address: MEMBERSHIP_ADDRESS,
      fromBlock,
      toBlock,
      topics: [[LEAF_REGISTERED_TOPIC]],
    });

    console.log(
      `[Membership] fetched ${logs.length} raw logs in range ${fromBlock} -> ${toBlock}`
    );

    logs.sort((a, b) => {
      if (a.blockNumber !== b.blockNumber) return a.blockNumber - b.blockNumber;
      if (a.transactionIndex !== b.transactionIndex) {
        return a.transactionIndex - b.transactionIndex;
      }
      return (a.index ?? 0) - (b.index ?? 0);
    });

    await processMembershipLogs(logs, provider);

    updateSyncCursor(
      "AnonymousMembershipRegistry",
      toBlock,
      null,
      null,
      Math.floor(Date.now() / 1000)
    );

    fromBlock = toBlock + 1;
  }

  console.log("[Membership] sync complete");
}