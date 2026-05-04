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
    INSERT INTO indexer_sync_state (
      contract_name,
      last_processed_block,
      last_processed_transaction_index,
      last_processed_log_index,
      updated_at
    ) VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(contract_name) DO UPDATE SET
      last_processed_block = excluded.last_processed_block,
      last_processed_transaction_index = excluded.last_processed_transaction_index,
      last_processed_log_index = excluded.last_processed_log_index,
      updated_at = excluded.updated_at
  `);

  return stmt.run(
    contractName,
    lastProcessedBlock,
    lastProcessedTransactionIndex,
    lastProcessedLogIndex,
    updatedAt
  );
}
