import { Interface } from "ethers";
import {
  handlePetitionCreated,
  handlePetitionSigned,
} from "./handlers.js";

const petitionRegistryAbi = [
  "event PetitionCreated(uint256 indexed petitionId, address indexed creator, string metadataURI)",
  "event PetitionSigned(uint256 indexed petitionId, bytes32 indexed nullifier, bytes32 admissionCommitment)",
];

const iface = new Interface(petitionRegistryAbi);

function normalizeEvent(log, parsed, timestamp) {
  const base = {
    blockNumber: log.blockNumber,
    transactionIndex: log.transactionIndex,
    logIndex: log.logIndex ?? log.index,
    txHash: log.transactionHash,
    timestamp,
  };

  if (parsed.name === "PetitionCreated") {
    return {
      ...base,
      eventName: "PetitionCreated",
      petitionId: parsed.args.petitionId.toString(),
      creator: parsed.args.creator,
      metadataUri: parsed.args.metadataURI,
    };
  }

  if (parsed.name === "PetitionSigned") {
    return {
      ...base,
      eventName: "PetitionSigned",
      petitionId: parsed.args.petitionId.toString(),
      nullifier: parsed.args.nullifier,
      admissionCommitment: parsed.args.admissionCommitment,
    };
  }

  return null;
}

function dispatchEvent(normalizedEvent) {
  if (!normalizedEvent) return null;

  if (normalizedEvent.eventName === "PetitionCreated") {
    return handlePetitionCreated(normalizedEvent);
  }

  if (normalizedEvent.eventName === "PetitionSigned") {
    return handlePetitionSigned(normalizedEvent);
  }

  return null;
}

export async function processPetitionLogs(logs, provider) {
  for (const log of logs) {
    const parsed = iface.parseLog(log);

    if (!parsed) {
      console.log(
        `[PetitionRegistry] ignoring non-V0 event topic ${log.topics[0]} at block ${log.blockNumber}`
      );
      continue;
    }

    const block = await provider.getBlock(log.blockNumber);
    const timestamp = block.timestamp;

    const normalized = normalizeEvent(log, parsed, timestamp);
    const result = dispatchEvent(normalized);

    if (result) {
      console.log(
        `[PetitionRegistry] ${result.eventName} -> ${result.status}`
      );
    }
  }
}