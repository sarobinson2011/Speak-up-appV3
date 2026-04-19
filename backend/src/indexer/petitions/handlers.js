import db from "../../db/connection.js";
import {
  insertPetition,
  ensurePetitionSignatureCountRow,
  insertPetitionSignature,
  incrementPetitionSignatureCount,
} from "../../db/repositories/petitions.js";
import { updateSyncCursor } from "../../db/repositories/syncState.js";

function assertPresent(value, fieldName) {
  if (value === undefined || value === null) {
    throw new Error(`Missing required field: ${fieldName}`);
  }
}

export const handlePetitionCreated = db.transaction((event) => {
  const {
    petitionId,
    creator,
    metadataUri,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    timestamp,
  } = event;

  assertPresent(petitionId, "petitionId");
  assertPresent(creator, "creator");
  assertPresent(metadataUri, "metadataUri");
  assertPresent(blockNumber, "blockNumber");
  assertPresent(transactionIndex, "transactionIndex");
  assertPresent(logIndex, "logIndex");
  assertPresent(txHash, "txHash");
  assertPresent(timestamp, "timestamp");

  const petitionResult = insertPetition({
    petitionId,
    creator,
    metadataUri,
    createdBlockNumber: blockNumber,
    createdTransactionIndex: transactionIndex,
    createdLogIndex: logIndex,
    createdTxHash: txHash,
    createdAt: timestamp,
  });

  ensurePetitionSignatureCountRow(petitionId);

  updateSyncCursor(
    "PetitionRegistry",
    blockNumber,
    transactionIndex,
    logIndex,
    Math.floor(Date.now() / 1000)
  );

  return {
    status: petitionResult.inserted ? "processed" : "already_applied",
    eventName: "PetitionCreated",
    petitionId,
  };
});

export const handlePetitionSigned = db.transaction((event) => {
  const {
    petitionId,
    nullifier,
    admissionCommitment,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    timestamp,
  } = event;

  assertPresent(petitionId, "petitionId");
  assertPresent(nullifier, "nullifier");
  assertPresent(admissionCommitment, "admissionCommitment");
  assertPresent(blockNumber, "blockNumber");
  assertPresent(transactionIndex, "transactionIndex");
  assertPresent(logIndex, "logIndex");
  assertPresent(txHash, "txHash");
  assertPresent(timestamp, "timestamp");

  const signatureResult = insertPetitionSignature({
    petitionId,
    nullifier,
    admissionCommitment,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    signedAt: timestamp,
  });

  if (signatureResult.inserted) {
    incrementPetitionSignatureCount(petitionId);
  }

  updateSyncCursor(
    "PetitionRegistry",
    blockNumber,
    transactionIndex,
    logIndex,
    Math.floor(Date.now() / 1000)
  );

  return {
    status: signatureResult.inserted ? "processed" : "already_applied",
    eventName: "PetitionSigned",
    petitionId,
    nullifier,
  };
});