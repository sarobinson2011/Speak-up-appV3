import db from "../connection.js";

export function insertPetition({
  petitionId,
  creator,
  metadataUri,
  createdBlockNumber,
  createdTransactionIndex,
  createdLogIndex,
  createdTxHash,
  createdAt,
}) {
  const stmt = db.prepare(`
    INSERT OR IGNORE INTO petitions (
      petition_id,
      creator,
      metadata_uri,
      created_block_number,
      created_transaction_index,
      created_log_index,
      created_tx_hash,
      created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `);

  const result = stmt.run(
    petitionId,
    creator,
    metadataUri,
    createdBlockNumber,
    createdTransactionIndex,
    createdLogIndex,
    createdTxHash,
    createdAt
  );

  return {
    inserted: result.changes > 0,
  };
}

export function ensurePetitionSignatureCountRow(petitionId) {
  const stmt = db.prepare(`
    INSERT OR IGNORE INTO petition_signature_counts (
      petition_id,
      signature_count
    ) VALUES (?, 0)
  `);

  const result = stmt.run(petitionId);

  return {
    inserted: result.changes > 0,
  };
}

export function insertPetitionSignature({
  petitionId,
  nullifier,
  blockNumber,
  transactionIndex,
  logIndex,
  txHash,
  signedAt,
}) {
  const stmt = db.prepare(`
    INSERT OR IGNORE INTO petition_signatures (
      petition_id,
      nullifier,
      block_number,
      transaction_index,
      log_index,
      tx_hash,
      signed_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
  `);

  const result = stmt.run(
    petitionId,
    nullifier,
    blockNumber,
    transactionIndex,
    logIndex,
    txHash,
    signedAt
  );

  return {
    inserted: result.changes > 0,
  };
}

export function incrementPetitionSignatureCount(petitionId) {
  const stmt = db.prepare(`
    UPDATE petition_signature_counts
    SET signature_count = signature_count + 1
    WHERE petition_id = ?
  `);

  return stmt.run(petitionId);
}

export function rebuildPetitionSignatureCounts() {
  const deleteStmt = db.prepare(`DELETE FROM petition_signature_counts`);
  const rebuildStmt = db.prepare(`
    INSERT INTO petition_signature_counts (petition_id, signature_count)
    SELECT petition_id, COUNT(*)
    FROM petition_signatures
    GROUP BY petition_id
  `);

  const tx = db.transaction(() => {
    deleteStmt.run();

    const petitionIdsStmt = db.prepare(`
      INSERT OR IGNORE INTO petition_signature_counts (petition_id, signature_count)
      SELECT petition_id, 0 FROM petitions
    `);

    petitionIdsStmt.run();
    rebuildStmt.run();
  });

  tx();
}

export function getPetitionsWithCounts() {
  const stmt = db.prepare(`
    SELECT
      p.petition_id,
      p.creator,
      p.metadata_uri,
      p.created_at,
      COALESCE(psc.signature_count, 0) AS signature_count
    FROM petitions p
    LEFT JOIN petition_signature_counts psc
      ON p.petition_id = psc.petition_id
    WHERE p.is_active = 1
    ORDER BY
      p.created_block_number DESC,
      p.created_transaction_index DESC,
      p.created_log_index DESC
  `);

  return stmt.all();
}

export function getPetitionByIdWithCount(petitionId) {
  const stmt = db.prepare(`
    SELECT
      p.petition_id,
      p.creator,
      p.metadata_uri,
      p.created_at,
      COALESCE(psc.signature_count, 0) AS signature_count
    FROM petitions p
    LEFT JOIN petition_signature_counts psc
      ON p.petition_id = psc.petition_id
    WHERE p.petition_id = ?
      AND p.is_active = 1
  `);

  return stmt.get(petitionId) ?? null;
}

export function getPetitionSignatureCount(petitionId) {
  const stmt = db.prepare(`
    SELECT
      p.petition_id,
      COALESCE(psc.signature_count, 0) AS signature_count
    FROM petitions p
    LEFT JOIN petition_signature_counts psc
      ON p.petition_id = psc.petition_id
    WHERE p.petition_id = ?
      AND p.is_active = 1
  `);

  return stmt.get(petitionId) ?? null;
}

export function getAllPetitionIds() {
  const stmt = db.prepare(`
    SELECT petition_id
    FROM petitions
    ORDER BY petition_id
  `);

  return stmt.all();
}

export function setPetitionActive(petitionId, isActive) {
  const stmt = db.prepare(`
    UPDATE petitions
    SET is_active = ?
    WHERE petition_id = ?
  `);

  return stmt.run(isActive ? 1 : 0, petitionId);
}

