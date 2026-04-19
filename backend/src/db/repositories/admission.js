import db from "../connection.js";

export function insertAdmissionRightFunded({
  admissionCommitment,
  amount,
  unlockAt,
  blockNumber,
  transactionIndex,
  logIndex,
  txHash,
  fundedAt,
}) {
  const stmt = db.prepare(`
    INSERT OR IGNORE INTO admission_rights (
      admission_commitment,
      state,
      amount,
      unlock_at,
      funded_block_number,
      funded_transaction_index,
      funded_log_index,
      funded_tx_hash,
      funded_at
    ) VALUES (?, 'funded', ?, ?, ?, ?, ?, ?, ?)
  `);

  const result = stmt.run(
    admissionCommitment,
    String(amount),
    unlockAt,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    fundedAt
  );

  return {
    inserted: result.changes > 0,
  };
}

export function getAdmissionRight(admissionCommitment) {
  const stmt = db.prepare(`
    SELECT *
    FROM admission_rights
    WHERE admission_commitment = ?
  `);

  return stmt.get(admissionCommitment) ?? null;
}

export function markAdmissionRightConsumed({
  admissionCommitment,
  blockNumber,
  transactionIndex,
  logIndex,
  txHash,
  consumedAt,
}) {
  const stmt = db.prepare(`
    UPDATE admission_rights
    SET
      state = 'consumed',
      consumed_block_number = ?,
      consumed_transaction_index = ?,
      consumed_log_index = ?,
      consumed_tx_hash = ?,
      consumed_at = ?
    WHERE admission_commitment = ?
      AND state = 'funded'
  `);

  const result = stmt.run(
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    consumedAt,
    admissionCommitment
  );

  return {
    updated: result.changes > 0,
  };
}

export function markAdmissionRightRefunded({
  admissionCommitment,
  blockNumber,
  transactionIndex,
  logIndex,
  txHash,
  refundedAt,
}) {
  const stmt = db.prepare(`
    UPDATE admission_rights
    SET
      state = 'refunded',
      refunded_block_number = ?,
      refunded_transaction_index = ?,
      refunded_log_index = ?,
      refunded_tx_hash = ?,
      refunded_at = ?
    WHERE admission_commitment = ?
      AND state = 'funded'
  `);

  const result = stmt.run(
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    refundedAt,
    admissionCommitment
  );

  return {
    updated: result.changes > 0,
  };
}