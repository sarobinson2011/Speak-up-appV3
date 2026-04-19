import db from "../connection.js";

export function getSyncCursor(contractName) {
  const stmt = db.prepare(`
    SELECT
      contract_name,
      last_processed_block,
      last_processed_transaction_index,
      last_processed_log_index,
      updated_at
    FROM indexer_sync_state
    WHERE contract_name = ?
  `);

  return stmt.get(contractName) ?? null;
}

export function updateSyncCursor(
  contractName,
  lastProcessedBlock,
  lastProcessedTransactionIndex,
  lastProcessedLogIndex,
  updatedAt
) {
  const stmt = db.prepare(`
    UPDATE indexer_sync_state
    SET
      last_processed_block = ?,
      last_processed_transaction_index = ?,
      last_processed_log_index = ?,
      updated_at = ?
    WHERE contract_name = ?
  `);

  return stmt.run(
    lastProcessedBlock,
    lastProcessedTransactionIndex,
    lastProcessedLogIndex,
    updatedAt,
    contractName
  );
}