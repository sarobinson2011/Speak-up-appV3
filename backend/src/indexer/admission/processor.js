import { Interface } from "ethers";
import {
  handleAdmissionRightFunded,
  handleAdmissionRightConsumed,
  handleAdmissionRightRefunded,
} from "./handlers.js";

const abi = [
  "event AdmissionRightFunded(bytes32 indexed admissionCommitment, uint256 amount, uint256 unlockAt)",
  "event AdmissionRightConsumed(bytes32 indexed admissionCommitment)",
  "event AdmissionRightRefunded(bytes32 indexed admissionCommitment, address indexed recipient, uint256 amount)",
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

  if (parsed.name === "AdmissionRightFunded") {
    return {
      ...base,
      eventName: "AdmissionRightFunded",
      admissionCommitment: parsed.args.admissionCommitment,
      amount: parsed.args.amount.toString(),
      unlockAt: Number(parsed.args.unlockAt),
    };
  }

  if (parsed.name === "AdmissionRightConsumed") {
    return {
      ...base,
      eventName: "AdmissionRightConsumed",
      admissionCommitment: parsed.args.admissionCommitment,
    };
  }

  if (parsed.name === "AdmissionRightRefunded") {
    return {
      ...base,
      eventName: "AdmissionRightRefunded",
      admissionCommitment: parsed.args.admissionCommitment,
    };
  }

  return null;
}

export async function processAdmissionLogs(logs, provider) {
  for (const log of logs) {
    const parsed = iface.parseLog(log);
    if (!parsed) continue;

    const block = await provider.getBlock(log.blockNumber);
    const timestamp = block.timestamp;

    const normalized = normalizeEvent(log, parsed, timestamp);
    if (!normalized) continue;

    let result = null;

    if (normalized.eventName === "AdmissionRightFunded") {
      result = handleAdmissionRightFunded(normalized);
    } else if (normalized.eventName === "AdmissionRightConsumed") {
      result = handleAdmissionRightConsumed(normalized);
    } else if (normalized.eventName === "AdmissionRightRefunded") {
      result = handleAdmissionRightRefunded(normalized);
    }

    if (result) {
      console.log(`[Admission] ${result.eventName} -> ${result.status}`);
    }
  }
}