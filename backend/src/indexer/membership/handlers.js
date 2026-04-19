import db from "../../db/connection.js";
import { insertMembershipLeaf } from "../../db/repositories/membership.js";
import { updateSyncCursor } from "../../db/repositories/syncState.js";

function assertPresent(value, fieldName) {
  if (value === undefined || value === null) {
    throw new Error(`Missing required field: ${fieldName}`);
  }
}

export const handleLeafRegistered = db.transaction((event) => {
  const {
    leaf,
    leafIndex,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    timestamp,
  } = event;

  assertPresent(leaf, "leaf");
  assertPresent(leafIndex, "leafIndex");
  assertPresent(blockNumber, "blockNumber");
  assertPresent(transactionIndex, "transactionIndex");
  assertPresent(logIndex, "logIndex");
  assertPresent(txHash, "txHash");
  assertPresent(timestamp, "timestamp");

  const result = insertMembershipLeaf({
    leaf,
    leafIndex,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    registeredAt: timestamp,
  });

  updateSyncCursor(
    "AnonymousMembershipRegistry",
    blockNumber,
    transactionIndex,
    logIndex,
    Math.floor(Date.now() / 1000)
  );

  return {
    status: result.inserted ? "processed" : "already_applied",
    eventName: "LeafRegistered",
    leaf,
  };
});