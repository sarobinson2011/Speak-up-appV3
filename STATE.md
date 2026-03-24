# STATE.md — Speak-up-appV3

Last updated: 2026-03-11 (Europe/London)

This file is the canonical source of truth for:

* Architecture decisions
* Invariants
* Deployed addresses
* ZK stack configuration
* Development governance model

When in doubt, STATE.md wins.
Changes must be recorded here before implementation.

---

## Documentation rules

`STATE.md` is the canonical source of truth for the current architecture, invariants, deployed addresses, development governance, and the next concrete implementation steps.

All other project markdown documentation lives under the `/docs` directory and is considered **supporting documentation only**.

Rules:

* If any document in `/docs` conflicts with `STATE.md`, **`STATE.md` wins**.
* Documents in `/docs` may expand on a single bounded topic (for example: ZK circuit specification, artifact provenance, relayer implementation, privacy threat model, operational commands), but must not redefine project-wide architecture.
* New project documentation should be placed under `/docs` unless there is a strong reason for it to live elsewhere.
* To avoid documentation drift, `/docs` files should reference `STATE.md` for global architecture rather than duplicating it.

Purpose of `/docs`:

* `/docs/ZK_*` → ZK system specification and artifact integrity
* `/docs/RELAYER_*` → relayer architecture and evolution
* `/docs/PRIVACY_*` → threat model and anonymity roadmap
* `/docs/dev/` → developer operational notes and commands

---

# 0) Development Governance Model (Locked)

Baseline anchor (ground truth):

* Tag: baseline-v0
* Commit: e02aacdc0f10e6919d8a759d8829758b58e0367e

Current main includes baseline via merge commit:

* 0ecd367 on origin/main

Two-track development model:

## Human Track (main)

* Only Steve (human) develops on main
* Assisted by GPT in Engineering[n] chats
* Slow, deterministic, minimal diffs
* No speculative expansion
* Cryptographic correctness is paramount
* STATE.md must be updated before architectural changes

Engineering chat convention:

Development discussions with GPT occur in sequential chats named:

Engineering[0], Engineering[1], Engineering[2], …

When a chat becomes too long or unwieldy, development continues in the next chat:

Engineering[n+1]

The current engineering chat number therefore increases over time.
STATE.md references use the generic form Engineering[n].

## Agent Track (separate machine)

* Agent NEVER checks out or commits to main
* One branch per iteration
* Branches created fresh from baseline-v0 (preferred)
* Naming convention:

  * agent/iter-0001-<desc>
  * agent/iter-0002-<desc>
* Human reviews before merge
* No automatic merges
* No silent merges

This separation is non-negotiable.

---

# 1) Project Goal (M2-only MVP)

Build a privacy-preserving petition platform where users can:

* Create petitions (wallet-authenticated; not private in MVP)
* Sign petitions with Strong Privacy (M2):

  * proof generated client-side
  * on-chain verification authoritative
  * uniqueness enforced via nullifier (not wallet address)

Comments are disabled in MVP.

---

# 2) Core Product Invariants (Locked)

1. Uniqueness:

* Max 1 signature per (petitionId, member)
* Enforced via nullifier
* Not wallet-based

2. Privacy:

* Signer proves membership without revealing identity

3. On-chain authority:

* Chain verifies proof validity
* Chain validates root validity
* Chain enforces nullifier uniqueness

4. No trusted gatekeeper:

* Membership is permissionless on-chain
* Backend is non-authoritative convenience only

5. M2-only mode:

* No email verification
* No JWT
* No attestations
* No M1 routes/UI

---

# 3) ZK Stack (Current, Locked)

Circuit framework: Circom
Prover/verifier: Groth16 (BN254)
Tooling: snarkjs

Hashing: Poseidon

* leaf: Poseidon1
* merkle node: Poseidon2
* nullifier: Poseidon3

SIGN_DOMAIN:

0x5349474e  // ASCII "SIGN"

Tree depth:

DEPTH = 16

Root history window:

N = 16

Full implementation spec:
See docs/ZK_CIRCUIT_SPEC.md

---

# 4) ZK Artifact Integrity (Engineering[n])

Artifact reproducibility and tamper detection are mandatory.

Specification:
docs/ZK_ARTIFACT_PROVENANCE.md

This document defines:

* ZK_ARTIFACTS_MANIFEST.json
* Required pinned artifacts
* SHA-256 hashing rules
* Golden proof requirement
* CI enforcement rules
* Public input order lock

Public input order (locked):

1. nullifier
2. petitionId
3. membershipRoot

No circuit, key, verifier, or encoding change is allowed without:

* Regeneration
* Manifest update
* Explicit commit
* Golden proof passing

---

# 4.6) Network Endpoints + Deployed Contracts

Chain: Aurora Testnet
chainId: 1313161555
RPC_URL: https://testnet.aurora.dev

Deployed contracts:

* MembershipRegistry (membership tree / LeafRegistered):
  0x7C329B70Da1Dc94d5655a0DB907637bc4530991f

* PetitionRegistry (proof verification entrypoint):
  0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD

* Groth16Verifier (ZK verifier):
  0x25C9A59DC47Ba0869229f02f8d80CC22860bFFBa

* Poseidon2 (hash contract/library):
  0xEFbb2780fA51c9D2f0375B226BEB03a897b0D9CF

---

# 5) Membership Model (Baseline)

Client stores one secret per wallet in localStorage.

Storage key:

su_memberSecret_v1:wallet:<walletLowercase>

Leaf definition:

leaf = Poseidon1(memberSecret)

Enrollment:

* One leaf per wallet
* Refundable bond required

Bond parameters:

registerBondWei() = 1e15 (0.001 ETH)
bondLockSeconds() = 3600

---

# 6) Nullifier Model (Locked)

nullifier = Poseidon3(memberSecret, petitionId, SIGN_DOMAIN)

On-chain:

* nullifier stored per petition
* duplicates rejected

This enforces one signature per petition per member.

---

# 7) Backend Role (MVP)

Backend is non-authoritative.

Responsibilities:

* Mirror membership events
* Rebuild Merkle tree
* Serve membership paths
* Relay ZK proof signing transactions

Must NOT:

* Gate membership
* Gate signing
* Store secrets

---

# 8) Path Privacy Hardening (Implemented)

Goal:

Remove wallet address from membership path requests.

Original API:

GET /api/membership/path?wallet=<address>

New API (current):

GET /api/membership/path?leaf=<hex>

Leaf is defined as:

leaf = Poseidon1(memberSecret)

The frontend computes the leaf locally and requests the membership path by leaf.

This removes direct wallet identifiers from path distribution requests and reduces backend-level deanonymization risk.

Implementation notes:

* Backend supports both wallet and leaf lookup during transition.
* Frontend now uses leaf-based lookup exclusively.
* Verified operational in milestone tag: m2-leaf-path-stable.

No circuit or contract changes required.

---

# 9) Relayer Signing (Implemented)

Goal:

Decouple proof submission from the wallet that sends the on-chain transaction.

Previous flow (prototype):

frontend → wallet → contract

The user's wallet directly submitted the transaction calling:

signPetitionWithZKProof(...)

This exposed the wallet address as the transaction sender and created a metadata link between the wallet and the petition signing event.

Current flow (implemented):

frontend → backend relayer → contract

Frontend sends the ZK proof payload to:

POST /api/relay/sign

Backend:

1. Validates payload structure
2. Checks nullifier status
3. Submits transaction via relayer wallet

Contract interface remains unchanged:

signPetitionWithZKProof(
petitionId,
nullifier,
pA,
pB,
pC,
pubSignals
)

Privacy result:

* On-chain sender is now the **relayer wallet**
* User wallet is not exposed during signing
* Identity remains protected by the ZK proof and nullifier

Design docs:

docs/RELAYER_IMPLEMENTATION_PLAN.md
docs/RELAYER_PROTOCOL_DESIGN.md

---

# 10) Known MVP Limitations

* Enrollment publicly tied to wallet
* Backend relayer can observe submissions
* Network metadata (IP / timing) may leak correlations
* Backend required for membership path distribution
* Secret loss breaks signing on that device

Full privacy analysis:

docs/PRIVACY_THREAT_MODEL.md

---

# 10.5) Verified Operational Baseline (Milestone)

Milestone tag:

m2-leaf-path-stable

This milestone represents a fully working M2-only baseline with:

Verified flows:

* Existing enrolled wallet signing
* Fresh wallet enrollment → signing
* Petition creation
* Petition create + sign
* Signature persistence across refresh
* Petition list signature counts updating correctly
* Leaf-based membership path lookup operational
* Relayed ZK signing operational

Frontend / backend loop is considered stable at this milestone.

This serves as the recovery point before further protocol evolution.

---

# 10.6) Aurora Admission Stack Deployment + Validation (Milestone)

This milestone records the first successful deployment, verification, and live functional validation of the admission-backed anonymous membership stack on Aurora testnet.

Canonical validated Aurora testnet deployment:

* `POSEIDON1_ADDRESS = 0x358730D22814c9f5c02A282671b9892E28AC88A2`
* `POSEIDON2_ADDRESS = 0x24120c6ffe7A19a675B5C63d8A2a4b135D641A5d`
* `ANON_MEMBERSHIP_LOGIC_ADDRESS = 0x32A0f3db8ed95C693C802Eb0A037b7c8e19c8c39`
* `ANON_MEMBERSHIP_PROXY_ADDRESS = 0xe3A5cAab30DfF154e6Dff35cB35Ba41326C76821`
* `ADMISSION_LOGIC_ADDRESS = 0xff6f693Ce5975F996AF27b002e017f34d599Aac5`
* `ADMISSION_PROXY_ADDRESS = 0x36c22227098B24E5aCE48dEa3988327256481F0e`

Deployment discipline locked:

* repo-root `.env` is the single source of truth
* Solidity `.s.sol` files are deployment primitives
* shell `.sh` wrappers are the canonical operator entrypoints
* direct `forge script` runs must reload repo-root env into the active shell before execution:
  * `set -a`
  * `source ../.env`
  * `set +a`

Atomicity distinction locked:

* full-stack deployment is not globally atomic
* each proxy deployment + initialization is atomic because initializer calldata is passed into the proxy constructor
* the only intentional inter-stage gap is final linkage:
  * `AnonymousMembershipRegistry.setAdmissionRegistry(admissionProxy)`
* this intermediate state is acceptable because membership registration remains gated until linkage

Verification status:

* wrapper-based Aurora deployment completed successfully
* `verify-admission-stack.sh` completed successfully against the canonical deployment
* live Aurora admission → membership validation completed successfully on the canonical deployment

Live validation result:

* `admissionCommitment = Poseidon1(admissionSecret)`
* `leaf = Poseidon1(memberSecret)`

Observed canonical live validation state transition:

* pre-state:
  * `leafCount = 0`
  * `isKnownLeaf(leaf) = false`
  * `status = 0`
* post-state:
  * `leafCount = 1`
  * `isKnownLeaf(leaf) = true`
  * `status = 2`

Operational conclusion:

The admission-backed anonymous membership path is now live and validated on Aurora testnet.
This checkpoint establishes the deployment and verification discipline for future iterations and provides the recovery point for subsequent integration into the M2 privacy flow.

Refund-path validation remains a separate time-based check because it depends on lock expiry.

---

# 11) Next Strategic Layer (Post-MVP)

Long-term Tornado-grade privacy requires:

* Unlinkable enrollment model
* Multi-relayer infrastructure
* Strong artifact provenance enforcement
* Larger anonymity sets

Speak-Up is evolving toward a **privacy participation engine** that allows valid actions to be publicly verified while preserving ambiguity about which participant performed them.

Core design rule:

**Private actors, public actions.**

The verifier proves validity; the architecture must preserve ambiguity.

Definition of the core privacy primitive:

docs/PRIVACY_ENGINE_DEFINITION.md

This document defines the minimal privacy engine that applications (petitions, coordination signals, funding systems, etc.) can build on top of.

The next architectural evolution focuses on **breaking the public wallet → membership link** while preserving economic admission friction and compatibility with the current ZK signing model.

Current enrollment design study:

Active V0 enrollment direction:

**Public bonded admission right + relayed private commitment activation**

This uses a two-secret model:

* `admissionSecret -> admissionCommitment` for the public funded admission right
* `memberSecret -> Poseidon1(memberSecret) -> leaf` for anonymous membership used by the existing ZK signing flow

Current V0 design decisions:

* Funded rights are keyed by `admissionCommitment`, not wallet address
* One funded right may activate exactly one membership leaf
* Activation consumes the right permanently
* Activated rights are not refundable
* Unused rights are refundable after lock expiry
* Activation does not require authorization from the original funding wallet
* Multiple funded rights per wallet are allowed
* No expiry model in V0 beyond lock-then-refundable semantics
* AdmissionRegistry and AnonymousMembershipRegistry are conceptually separate
* V0 assumes direct AdmissionRegistry -> AnonymousMembershipRegistry interaction
* Signing flow should remain unchanged if possible

Supporting design doc:

`docs/ADMISSION_RIGHT_MODEL_V0.md`

docs/UNLINKABLE_ENROLLMENT_DESIGN_V0.md

This document explores candidate approaches for unlinkable membership admission and evaluates **relayed commitment enrollment with bonded admission** as the leading direction.

Design must precede implementation.  
All architectural changes must be recorded in `STATE.md` first.

docs/ADMISSION_DEPLOYMENT_FLOW_V0.md

This document defines the V0 deployment and initialization order for Poseidon1, Poseidon2, AnonymousMembershipRegistry, and AdmissionRegistry, including proxy wiring and post-deploy linkage.

---

STATE.md remains canonical.

If any conflict arises between code and documentation:  
STATE.md governs.
