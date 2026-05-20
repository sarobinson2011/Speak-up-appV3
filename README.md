# Speak-up-appV3

Privacy-preserving petition system built around the rule:

> Private actors, public actions.

The current project direction is an **M2-only Strong Privacy MVP**.

`STATE.md` is the canonical source of truth for architecture, invariants, deployed addresses, development governance, and current implementation status.

If this README or any supporting document conflicts with `STATE.md`, **STATE.md wins**.

---

## Current Architecture

The active system is organized into separate layers:

- **M2** — identity / proof semantics
- **Enrollment** — economic admission / eligibility semantics
- **Custody** — local `memberSecret` custody and portability semantics
- **TEMPEST** — execution / submission semantics
- **REFLECT** — path / publication semantics
- **Backend** — non-authoritative indexing, path distribution, and relay support

Core identity path:

    memberSecret -> leaf -> nullifier

Continuity rule:

    continuity = possession of the same original memberSecret

Wallets are runtime convenience handles only.  
Wallets are not identity, recovery, or continuity authorities.

---

## Current Privacy Model

The system allows users to sign petitions with Strong Privacy:

- proof generation happens client-side
- on-chain verification is authoritative
- uniqueness is enforced by nullifier
- the user wallet is not the on-chain signing sender
- backend services remain non-authoritative
- comments are disabled in the MVP

Current ZK stack:

- Circom
- Groth16
- BN254
- Poseidon
- public input order locked in `STATE.md` and `docs/ZK_CIRCUIT_SPEC.md`

---

## Quick Start

    # 1. Setup
    cd Speak-up-appV3
    cp .env.example .env
    # Edit .env with your local values

    # 2. Contracts
    cd contracts
    forge build
    forge test

    # 3. Backend
    cd ../backend
    npm install
    npm run dev

    # 4. Frontend
    cd ../frontend
    npm install
    npm run dev

---

## Project Structure

    .
    ├── backend/        # Node/Express backend: indexer, path service, relay support
    ├── contracts/      # Foundry smart contracts
    ├── docs/           # Supporting documentation
    ├── frontend/       # React + Vite frontend
    ├── scripts/        # Project scripts
    ├── zk/             # ZK circuits/artifacts
    ├── STATE.md        # Canonical project truth
    └── ZK_ARTIFACTS_MANIFEST.json

---

## Documentation Map

Canonical authority:

- `STATE.md`

Current supporting docs:

- `docs/CONTINUITY_CUSTODY_MODEL_V1.md`
- `docs/PRIVACY_ENGINE_DEFINITION.md`
- `docs/PRIVACY_THREAT_MODEL.md`
- `docs/ZK_CIRCUIT_SPEC.md`
- `docs/ZK_ARTIFACT_PROVENANCE.md`
- `docs/tempest/*`
- `docs/reflect/*`

Historical/supporting docs may remain in `docs/`.

Historical documents are useful context, but they must not be read as redefining current architecture if they conflict with `STATE.md`.

---

## Development Governance

Active development currently happens through the human Steve + GPT `Engineering[n]` process on `main`.

Development discipline:

- observe before editing
- make bounded changes
- preserve layer boundaries
- update `STATE.md` before architectural changes
- validate deterministically
- commit and tag clean checkpoints

Historical autonomous-agent / second-laptop workflows are not the active development authority unless explicitly reintroduced in `STATE.md`.

---

## Tech Stack

- **Contracts:** Solidity, Foundry, OpenZeppelin upgradeable patterns
- **Backend:** Node.js, Express, ethers.js, SQLite indexing
- **Frontend:** React, Vite, ethers.js
- **ZK:** Circom, Groth16, snarkjs, Poseidon
- **Network:** Aurora Testnet

---

## Security Notes

The project is privacy-sensitive.

Do not introduce wording, code, comments, logs, route names, or documentation that implies:

- wallet-based identity
- account recovery
- backend custody
- relay continuity
- REFLECT continuity
- identity reconstruction
- hidden linkage semantics

When in doubt, check `STATE.md`.
