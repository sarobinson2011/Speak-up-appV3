import { Interface } from "ethers";
import { handleLeafRegistered } from "./handlers.js";

const abi = [
  "event LeafRegistered(bytes32 indexed leaf, uint256 leafIndex, bytes32 newRoot)",
];

const iface = new Interface(abi);

function normalizeEvent(log, parsed, timestamp) {
  const base = {
    blockNumber: log.blockNumber,
    transactionIndex: log.transactionIndex,
    logIndex: log.logIndex ?? log.index,
    txHash: log.transactionHash,
    timestamp,
  };

  if (parsed.name === "LeafRegistered") {
    return {
      ...base,
      eventName: "LeafRegistered",
      leaf: parsed.args.leaf,
      leafIndex: Number(parsed.args.leafIndex),
    };
  }

  return null;
}

export async function processMembershipLogs(logs, provider) {
  for (const log of logs) {
    const parsed = iface.parseLog(log);

    if (!parsed) continue;

    const block = await provider.getBlock(log.blockNumber);
    const timestamp = block.timestamp;

    const normalized = normalizeEvent(log, parsed, timestamp);

    if (!normalized) continue;

    const result = handleLeafRegistered(normalized);

    if (result) {
      console.log(
        `[Membership] ${result.eventName} -> ${result.status}`
      );
    }
  }
}