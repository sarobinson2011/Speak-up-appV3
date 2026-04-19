import db from "../../db/connection.js";
import {
  insertAdmissionRightFunded,
  getAdmissionRight,
  markAdmissionRightConsumed,
  markAdmissionRightRefunded,
} from "../../db/repositories/admission.js";
import { updateSyncCursor } from "../../db/repositories/syncState.js";

function assertPresent(value, fieldName) {
  if (value === undefined || value === null) {
    throw new Error(`Missing required field: ${fieldName}`);
  }
}

export const handleAdmissionRightFunded = db.transaction((event) => {
  const {
    admissionCommitment,
    amount,
    unlockAt,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    timestamp,
  } = event;

  assertPresent(admissionCommitment, "admissionCommitment");
  assertPresent(amount, "amount");
  assertPresent(unlockAt, "unlockAt");
  assertPresent(blockNumber, "blockNumber");
  assertPresent(transactionIndex, "transactionIndex");
  assertPresent(logIndex, "logIndex");
  assertPresent(txHash, "txHash");
  assertPresent(timestamp, "timestamp");

  const result = insertAdmissionRightFunded({
    admissionCommitment,
    amount,
    unlockAt,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    fundedAt: timestamp,
  });

  updateSyncCursor(
    "AdmissionRegistry",
    blockNumber,
    transactionIndex,
    logIndex,
    Math.floor(Date.now() / 1000)
  );

  return {
    status: result.inserted ? "processed" : "already_applied",
    eventName: "AdmissionRightFunded",
    admissionCommitment,
  };
});

export const handleAdmissionRightConsumed = db.transaction((event) => {
  const {
    admissionCommitment,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    timestamp,
  } = event;

  assertPresent(admissionCommitment, "admissionCommitment");
  assertPresent(blockNumber, "blockNumber");
  assertPresent(transactionIndex, "transactionIndex");
  assertPresent(logIndex, "logIndex");
  assertPresent(txHash, "txHash");
  assertPresent(timestamp, "timestamp");

  const existing = getAdmissionRight(admissionCommitment);
  if (!existing) {
    throw new Error(
      `AdmissionRightConsumed with no funded row: ${admissionCommitment}`
    );
  }

  if (existing.state === "consumed") {
    updateSyncCursor(
      "AdmissionRegistry",
      blockNumber,
      transactionIndex,
      logIndex,
      Math.floor(Date.now() / 1000)
    );

    return {
      status: "already_applied",
      eventName: "AdmissionRightConsumed",
      admissionCommitment,
    };
  }

  if (existing.state !== "funded") {
    throw new Error(
      `Invalid lifecycle transition to consumed from state=${existing.state} for ${admissionCommitment}`
    );
  }

  const result = markAdmissionRightConsumed({
    admissionCommitment,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    consumedAt: timestamp,
  });

  if (!result.updated) {
    throw new Error(
      `Failed to mark admission right consumed: ${admissionCommitment}`
    );
  }

  updateSyncCursor(
    "AdmissionRegistry",
    blockNumber,
    transactionIndex,
    logIndex,
    Math.floor(Date.now() / 1000)
  );

  return {
    status: "processed",
    eventName: "AdmissionRightConsumed",
    admissionCommitment,
  };
});

export const handleAdmissionRightRefunded = db.transaction((event) => {
  const {
    admissionCommitment,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    timestamp,
  } = event;

  assertPresent(admissionCommitment, "admissionCommitment");
  assertPresent(blockNumber, "blockNumber");
  assertPresent(transactionIndex, "transactionIndex");
  assertPresent(logIndex, "logIndex");
  assertPresent(txHash, "txHash");
  assertPresent(timestamp, "timestamp");

  const existing = getAdmissionRight(admissionCommitment);
  if (!existing) {
    throw new Error(
      `AdmissionRightRefunded with no funded row: ${admissionCommitment}`
    );
  }

  if (existing.state === "refunded") {
    updateSyncCursor(
      "AdmissionRegistry",
      blockNumber,
      transactionIndex,
      logIndex,
      Math.floor(Date.now() / 1000)
    );

    return {
      status: "already_applied",
      eventName: "AdmissionRightRefunded",
      admissionCommitment,
    };
  }

  if (existing.state !== "funded") {
    throw new Error(
      `Invalid lifecycle transition to refunded from state=${existing.state} for ${admissionCommitment}`
    );
  }

  const result = markAdmissionRightRefunded({
    admissionCommitment,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    refundedAt: timestamp,
  });

  if (!result.updated) {
    throw new Error(
      `Failed to mark admission right refunded: ${admissionCommitment}`
    );
  }

  updateSyncCursor(
    "AdmissionRegistry",
    blockNumber,
    transactionIndex,
    logIndex,
    Math.floor(Date.now() / 1000)
  );

  return {
    status: "processed",
    eventName: "AdmissionRightRefunded",
    admissionCommitment,
  };
});