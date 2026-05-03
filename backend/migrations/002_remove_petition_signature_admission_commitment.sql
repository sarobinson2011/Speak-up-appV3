DROP INDEX IF EXISTS idx_petition_signatures_admission_commitment;

CREATE TABLE IF NOT EXISTS petition_signatures_new (
    petition_id INTEGER NOT NULL,
    nullifier TEXT NOT NULL,

    block_number INTEGER NOT NULL,
    transaction_index INTEGER NOT NULL,
    log_index INTEGER NOT NULL,
    tx_hash TEXT NOT NULL,
    signed_at INTEGER NOT NULL,

    PRIMARY KEY (tx_hash, log_index),

    CONSTRAINT uq_petition_signatures_petition_nullifier
        UNIQUE (petition_id, nullifier),

    CONSTRAINT fk_petition_signatures_petition
        FOREIGN KEY (petition_id)
        REFERENCES petitions (petition_id)
        ON DELETE CASCADE
);

INSERT OR IGNORE INTO petition_signatures_new (
    petition_id,
    nullifier,
    block_number,
    transaction_index,
    log_index,
    tx_hash,
    signed_at
)
SELECT
    petition_id,
    nullifier,
    block_number,
    transaction_index,
    log_index,
    tx_hash,
    signed_at
FROM petition_signatures;

DROP TABLE petition_signatures;

ALTER TABLE petition_signatures_new RENAME TO petition_signatures;

CREATE INDEX IF NOT EXISTS idx_petition_signatures_petition_id
    ON petition_signatures (petition_id);

CREATE INDEX IF NOT EXISTS idx_petition_signatures_order
    ON petition_signatures (block_number, transaction_index, log_index);

CREATE INDEX IF NOT EXISTS idx_petition_signatures_nullifier
    ON petition_signatures (nullifier);
