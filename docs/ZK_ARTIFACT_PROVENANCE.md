# ZK Artifact Provenance Specification
Speak-up-appV3 (M2-only baseline)
Status: LIVE (Engineering[5])
Last updated: 2026-02-27 (Europe/London)

---

## 1. Purpose

This document defines how we pin, verify, and enforce the integrity of all
Zero-Knowledge artifacts in Speak-up-appV3.

The goal is to make the zk-contracts loop:

- Reproducible
- Tamper-evident
- Auditable
- Portable as standalone IP

Any third party should be able to independently verify they are using
the exact circuit, keys, verifier, and frontend encoding expected by
the deployed contracts.

No circuit or verifier change may occur without updating this document
and the manifest defined below.

---

## 2. Threat Model

We defend against:

- Silent drift in circuit source or dependencies
- Accidental mismatch between:
  - circuit public input order
  - verification key
  - Solidity verifier
  - frontend signal encoding
- Artifact tampering (.wasm, .zkey, verifier.sol)
- “Works on my machine” discrepancies
- Untracked toolchain version drift

We are NOT addressing trusted setup ceremony decentralization in this
document (that is future work). We are addressing integrity and reproducibility.

---

## 3. Locked Cryptographic Interface (MVP)

From ZK_CIRCUIT_SPEC.md:

Public input order (MUST remain identical across layers):

1. petitionId
2. nullifier
3. membershipRoot

This order is locked.

Any change requires:
- Circuit regeneration
- Verifier regeneration
- Frontend encoder update
- Manifest update
- Explicit commit

---

## 4. Required Pinned Artifacts

The following MUST be hashed and pinned.

### Circuit Layer
- sign_petition.circom
- any imported .circom dependencies
- generated .r1cs
- generated witness .wasm
- proving key (.zkey)
- verification_key.json

### Solidity Layer
- Groth16Verifier.sol
- Petition registry contract containing verify call
- Any Poseidon contracts used on-chain

### Frontend Layer
- Proof generation component (e.g. M2SignButton)
- Public signal encoding helper
- poseidon-lite version (package-lock.json)
- snarkjs version
- any ABI used for proof submission

---

## 5. ZK_ARTIFACTS_MANIFEST.json

A single canonical manifest must exist at repo root:

ZK_ARTIFACTS_MANIFEST.json

It must include:

- baseline_anchor_commit
- hash_algorithm (SHA-256)
- circuit file hashes
- key file hashes
- verifier file hashes
- frontend file hashes
- toolchain versions:
  - circom version
  - snarkjs version
  - node version
  - solidity compiler version
  - foundry version (if applicable)
- canonical public input declaration

All hashes are SHA-256 of raw file bytes.

No line-ending normalization.
No formatting normalization.
Hash exactly what is committed.

---

## 6. Deterministic Build Requirements

We must provide scripts:

scripts/zk/build_artifacts.sh
scripts/zk/hash_manifest.sh
scripts/zk/verify_manifest.sh

### verify_manifest.sh must:
- Recompute SHA-256 for all pinned files
- Compare against manifest
- Exit non-zero on mismatch

CI must fail on mismatch.

---

## 7. Golden Proof Test (Mandatory)

Before any deploy:

- Fixed memberSecret
- Fixed test tree
- Fixed petitionId
- Witness builds
- Proof verifies locally
- Public signals match expected order and values

This test must remain green.

---

## 8. On-Chain Circuit Identity (Optional Enhancement)

Future enhancement:

Embed a bytes32 CIRCUIT_ID constant derived from:
- verification_key.json hash OR
- verifier bytecode hash

Emit event on deploy.

This allows on-chain pinning of the circuit identity.

---

## 9. Change Procedure

If ANY of the following change:
- circuit logic
- input order
- zkey
- verifier
- encoding logic

You MUST:

1. Regenerate artifacts
2. Update manifest
3. Update this document if interface changed
4. Commit explicitly referencing change
5. Ensure golden proof test passes

No silent regeneration allowed.

---

## 10. Acceptance Criteria

- Manifest exists and is enforced
- CI blocks drift
- Developers can reproduce artifacts
- Public input order is declared and tested
- Frontend and verifier cannot silently diverge

This document remains LIVE until v1 cryptographic freeze.