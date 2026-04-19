PRAGMA foreign_keys = ON;

-- ============================================================
-- Ground-Truth Indexer V0
-- Initial schema
-- ============================================================

-- ------------------------------------------------------------
-- petitions
-- Source: PetitionCreated
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS petitions (
    petition_id INTEGER PRIMARY KEY,
    creator TEXT NOT NULL,
    metadata_uri TEXT NOT NULL,

    created_block_number INTEGER NOT NULL,
    created_transaction_index INTEGER NOT NULL,
    created_log_index INTEGER NOT NULL,
    created_tx_hash TEXT NOT NULL,
    created_at INTEGER NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_petitions_created_event
    ON petitions (created_tx_hash, created_log_index);

CREATE INDEX IF NOT EXISTS idx_petitions_created_order
    ON petitions (created_block_number, created_transaction_index, created_log_index);


-- ------------------------------------------------------------
-- petition_signatures
-- Source: PetitionSigned
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS petition_signatures (
    petition_id INTEGER NOT NULL,
    nullifier TEXT NOT NULL,
    admission_commitment TEXT NOT NULL,

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

CREATE INDEX IF NOT EXISTS idx_petition_signatures_petition_id
    ON petition_signatures (petition_id);

CREATE INDEX IF NOT EXISTS idx_petition_signatures_order
    ON petition_signatures (block_number, transaction_index, log_index);

CREATE INDEX IF NOT EXISTS idx_petition_signatures_nullifier
    ON petition_signatures (nullifier);

CREATE INDEX IF NOT EXISTS idx_petition_signatures_admission_commitment
    ON petition_signatures (admission_commitment);


-- ------------------------------------------------------------
-- petition_signature_counts
-- Derived from petition_signatures
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS petition_signature_counts (
    petition_id INTEGER PRIMARY KEY,
    signature_count INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT fk_petition_signature_counts_petition
        FOREIGN KEY (petition_id)
        REFERENCES petitions (petition_id)
        ON DELETE CASCADE,

    CONSTRAINT ck_petition_signature_counts_nonnegative
        CHECK (signature_count >= 0)
);


-- ------------------------------------------------------------
-- membership_leaves
-- Source: LeafRegistered
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS membership_leaves (
    leaf TEXT PRIMARY KEY,
    leaf_index INTEGER NOT NULL,

    block_number INTEGER NOT NULL,
    transaction_index INTEGER NOT NULL,
    log_index INTEGER NOT NULL,
    tx_hash TEXT NOT NULL,
    registered_at INTEGER NOT NULL,

    CONSTRAINT uq_membership_leaves_leaf_index
        UNIQUE (leaf_index),

    CONSTRAINT uq_membership_leaves_event
        UNIQUE (tx_hash, log_index)
);

CREATE INDEX IF NOT EXISTS idx_membership_leaves_leaf_index
    ON membership_leaves (leaf_index);

CREATE INDEX IF NOT EXISTS idx_membership_leaves_order
    ON membership_leaves (block_number, transaction_index, log_index);


-- ------------------------------------------------------------
-- admission_rights
-- Source:
--   AdmissionRightFunded
--   AdmissionRightConsumed
--   AdmissionRightRefunded
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS admission_rights (
    admission_commitment TEXT PRIMARY KEY,
    state TEXT NOT NULL,
    amount TEXT NOT NULL,
    unlock_at INTEGER NOT NULL,

    funded_block_number INTEGER NOT NULL,
    funded_transaction_index INTEGER NOT NULL,
    funded_log_index INTEGER NOT NULL,
    funded_tx_hash TEXT NOT NULL,
    funded_at INTEGER NOT NULL,

    consumed_block_number INTEGER,
    consumed_transaction_index INTEGER,
    consumed_log_index INTEGER,
    consumed_tx_hash TEXT,
    consumed_at INTEGER,

    refunded_block_number INTEGER,
    refunded_transaction_index INTEGER,
    refunded_log_index INTEGER,
    refunded_tx_hash TEXT,
    refunded_at INTEGER,

    CONSTRAINT ck_admission_rights_state
        CHECK (state IN ('funded', 'consumed', 'refunded'))
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_admission_rights_funded_event
    ON admission_rights (funded_tx_hash, funded_log_index);

CREATE INDEX IF NOT EXISTS idx_admission_rights_state
    ON admission_rights (state);

CREATE INDEX IF NOT EXISTS idx_admission_rights_unlock_at
    ON admission_rights (unlock_at);


-- ------------------------------------------------------------
-- indexer_sync_state
-- One row per indexed contract
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS indexer_sync_state (
    contract_name TEXT PRIMARY KEY,
    last_processed_block INTEGER NOT NULL,
    last_processed_transaction_index INTEGER,
    last_processed_log_index INTEGER,
    updated_at INTEGER NOT NULL
);

INSERT OR IGNORE INTO indexer_sync_state (
    contract_name,
    last_processed_block,
    last_processed_transaction_index,
    last_processed_log_index,
    updated_at
) VALUES
    ('PetitionRegistry', 0, NULL, NULL, strftime('%s','now')),
    ('AnonymousMembershipRegistry', 0, NULL, NULL, strftime('%s','now')),
    ('AdmissionRegistry', 0, NULL, NULL, strftime('%s','now'));