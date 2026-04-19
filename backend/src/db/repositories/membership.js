import db from "../connection.js";

export function insertMembershipLeaf({
  leaf,
  leafIndex,
  blockNumber,
  transactionIndex,
  logIndex,
  txHash,
  registeredAt,
}) {
  const stmt = db.prepare(`
    INSERT OR IGNORE INTO membership_leaves (
      leaf,
      leaf_index,
      block_number,
      transaction_index,
      log_index,
      tx_hash,
      registered_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
  `);

  const result = stmt.run(
    leaf,
    leafIndex,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    registeredAt
  );

  return {
    inserted: result.changes > 0,
  };
}

export function getAllMembershipLeavesOrdered() {
  const stmt = db.prepare(`
    SELECT leaf, leaf_index
    FROM membership_leaves
    ORDER BY leaf_index ASC
  `);

  return stmt.all();
}