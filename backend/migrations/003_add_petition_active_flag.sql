ALTER TABLE petitions
ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1;

CREATE INDEX IF NOT EXISTS idx_petitions_active_order
    ON petitions (
        is_active,
        created_block_number,
        created_transaction_index,
        created_log_index
    );
