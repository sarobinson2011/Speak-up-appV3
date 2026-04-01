# STATE.md — Speak-up-appV3

Last updated: 2026-03-31 (Europe/London)

This file is the canonical source of truth for:

- Architecture decisions
- Invariants
- Deployed addresses
- ZK stack configuration
- Development governance model

When in doubt, STATE.md wins.  
Changes must be recorded here before implementation.

---

## Documentation rules

`STATE.md` is the canonical source of truth for the current architecture, invariants, deployed addresses, development governance, and the next concrete implementation steps.

All other project markdown documentation lives under the `/docs` directory and is considered **supporting documentation only**.

Rules:

- If any document in `/docs` conflicts with `STATE.md`, **`STATE.md` wins**.
- Documents in `/docs` may expand on a single bounded topic (for example: ZK circuit specification, artifact provenance, relayer implementation, privacy threat model, operational commands), but must not redefine project-wide architecture.
- New project documentation should be placed under `/docs` unless there is a strong reason for it to live elsewhere.
- To avoid documentation drift, `/docs` files should reference `STATE.md` for global architecture rather than duplicating it.

Purpose of `/docs`:

- `/docs/ZK_*` → ZK system specification and artifact integrity
- `/docs/RELAYER_*` → relayer architecture and evolution
- `/docs/PRIVACY_*` → threat model and anonymity roadmap
- `/docs/dev/` → developer operational notes and commands
- `/docs/tempest/` → TEMPEST multi-relayer execution-layer design
- `/docs/reflect/` → REFLECT distributed mirror path-layer design

---

# 0) Development Governance Model (Locked)

Baseline anchor (ground truth):

- Tag: `baseline-v0`
- Commit: `e02aacdc0f10e6919d8a759d8829758b58e0367e`

Current main includes baseline via merge commit:

- `0ecd367` on `origin/main`

Two-track development model:

## Human Track (main)

- Only Steve (human) develops on `main`
- Assisted by GPT in Engineering[n] chats
- Slow, deterministic, minimal diffs
- No speculative expansion
- Cryptographic correctness is paramount
- STATE.md must be updated before architectural changes

Engineering chat convention:

Development discussions with GPT occur in sequential chats named:

- Engineering[0]
- Engineering[1]
- Engineering[2]
- …

When a chat becomes too long or unwieldy, development continues in the next chat:

- Engineering[n+1]

The current engineering chat number therefore increases over time.  
`STATE.md` references use the generic form Engineering[n].

Engineering work proceeds through a rolling `Engineering[n]` chat series.

This is an operational continuity model, not a project reset model.

Meaning:

- `Engineering[n]` and `Engineering[n+1]` are treated as consecutive segments of the same development thread
- continuity is preserved by carrying forward:
  - the current `STATE.md`
  - a handover prompt prepared in `Engineering[n]` for `Engineering[n+1]`
- `STATE.md` remains the canonical source of truth across all chat transitions
- if any conflict exists between conversational memory, handover prompts, or older discussion, `STATE.md` wins

Purpose of the rolling-chat model:

- allow long-running deterministic development to continue across multiple chat sessions
- preserve architectural continuity without drift
- keep implementation aligned to one canonical state record
- avoid treating chat rollover as an opportunity for silent redesign

This rolling continuity model will always be used unless I (Steve) explicitly state otherwise.

## Agent Track (separate machine)

- Agent NEVER checks out or commits to `main`
- One branch per iteration
- Branches created fresh from `baseline-v0` (preferred)
- Naming convention:
  - `agent/iter-0001-<desc>`
  - `agent/iter-0002-<desc>`
- Human reviews before merge
- No automatic merges
- No silent merges

This separation is non-negotiable.

---

# 1) Project Goal (M2-only MVP)

Build a privacy-preserving petition platform where users can:

- Create petitions (wallet-authenticated; not private in MVP)
- Sign petitions with Strong Privacy (M2):
  - proof generated client-side
  - on-chain verification authoritative
  - uniqueness enforced via nullifier (not wallet address)

Comments are disabled in MVP.

---

# 2) Core Principles

## 2.1 Separation of concerns

The system is divided into independent layers:

- Enrollment Layer → economic admission / eligibility
- Anonymous Membership Layer → identity abstraction
- REFLECT → path / witness-data layer
- TEMPEST → execution / submission layer
- Backend → non-authoritative path distribution

No layer should leak or infer the responsibility of another.

## 2.2 Determinism over randomness

- Deterministic selection is preferred
- Systems should produce broad equivalence classes
- Avoid rare or unique observable patterns wherever possible

## 2.3 Bounded Systems

- fixed node sets (7 TEMPEST relays, 7 REFLECT mirrors)

## 2.4 Explicit failure semantics

- Fail cleanly
- No silent degradation
- No hidden fallback behavior

## 2.5 No hidden coupling

- No implicit identity linkage across layers
- No silent reintroduction of wallet-shaped or sponsor-shaped lookup dependencies

---

# 3) Core Product Invariants (Locked)

1. Uniqueness

- Max 1 signature per `(petitionId, member)`
- Enforced via nullifier
- Not wallet-based

2. Privacy

- Signer proves membership without revealing identity

3. On-chain authority

- Chain verifies proof validity
- Chain validates root validity
- Chain enforces nullifier uniqueness

4. No trusted gatekeeper

- Membership is permissionless on-chain
- Backend is non-authoritative convenience only

5. M2-only mode

- No email verification
- No JWT
- No attestations
- No M1 routes/UI

---

# 4) ZK Stack (Current, Locked)

Circuit framework: Circom  
Prover/verifier: Groth16 (BN254)  
Tooling: snarkjs

Hashing: Poseidon

- leaf: Poseidon1
- merkle node: Poseidon2
- nullifier: Poseidon3

SIGN_DOMAIN:

`0x5349474e`  // ASCII "SIGN"

Tree depth:

`DEPTH = 16`

Root history window:

`N = 16`

Full implementation spec:  
See `docs/ZK_CIRCUIT_SPEC.md`

---

# 5) ZK Artifact Integrity (Engineering[n])

Artifact reproducibility and tamper detection are mandatory.

Specification:  
`docs/ZK_ARTIFACT_PROVENANCE.md`

This document defines:

- `ZK_ARTIFACTS_MANIFEST.json`
- Required pinned artifacts
- SHA-256 hashing rules
- Golden proof requirement
- CI enforcement rules
- Public input order lock

Public input order (locked):

1. nullifier
2. petitionId
3. membershipRoot

No circuit, key, verifier, or encoding change is allowed without:

- regeneration
- manifest update
- explicit commit
- golden proof passing

---

# 6) Network Endpoints + Deployed Contracts

Chain: Aurora Testnet  
`chainId = 1313161555`  
`RPC_URL = https://testnet.aurora.dev`

Deployed contracts:

- MembershipRegistry (membership tree / LeafRegistered):  
  `0x7C329B70Da1Dc94d5655a0DB907637bc4530991f`

- PetitionRegistry (proof verification entrypoint):  
  `0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD`

- Groth16Verifier (ZK verifier):  
  `0x25C9A59DC47Ba0869229f02f8d80CC22860bFFBa`

- Poseidon2 (hash contract/library):  
  `0xEFbb2780fA51c9D2f0375B226BEB03a897b0D9CF`

---

# 7) Enrollment Layer (V1 — Passive Sponsored Admission Rights)

## Status

Architecture locked in STATE.  
Contract / runtime delta still to be implemented.

## Overview

The enrollment layer is defined as:

**public economic admission + private anonymous activation**

Funded rights are:

**economic objects, not participant identities**

The system explicitly removes the assumption:

**funder = participant**

and replaces it with:

**funder and participant are not reliably linkable**

## Core model

### 7.1 Public bonded admission rights

Admission requires a public funding transaction:

`fundAdmissionRight(admissionCommitment)`

This creates a bonded admission right keyed by `admissionCommitment`.

Admission friction is preserved:

- cost
- lock
- refund semantics

This maintains the economic boundary of the system.

### 7.2 Identity-agnostic rights

- Funded rights are keyed by `admissionCommitment`, not wallet address
- A funded right does not encode or imply participant identity
- A public observer must not treat the funding wallet as the future participant

### 7.3 Structural sponsorship

- Activation of a funded right does **not** require authorization from the original funding wallet
- Any holder of the valid private material (`admissionSecret`) may activate the right
- Multiple funded rights per wallet are allowed

Therefore:

**funder ≠ participant is a first-class system property**

### 7.4 Activation (accounting-real, attribution-weak)

Activation:

`activateMembership(admissionCommitment, admissionSecret, leaf)`

Must satisfy:

- One funded right → exactly one membership leaf
- Activation consumes the right permanently
- Activated rights are not refundable
- Unused rights remain refundable after lock expiry

However:

**activation must not function as a public participant-creation signal**

### 7.5 No public participant-readiness signal

The system must not expose any public artifact that allows observers to infer:

- when a participant became usable
- which funded right produced which participant
- that a specific event corresponds to “participant birth”

Forbidden emergent artifacts include:

- activation receipts acting as identity labels
- claim / entitlement tokens
- sponsor handoff records
- cohort / batch identifiers

### 7.6 Funding time is not a usability oracle

Public funding timestamps must not provide a narrow or reliable prediction of:

**when a participant becomes action-capable**

The mapping between:

`funding time -> usable anonymous participant`

must be non-reliable from an observer perspective.

## Event / state exposure policy

### Allowed (public, required)

- Admission funding transactions
- Refund events and refund eligibility
- Admission-right accounting state

### Allowed but accounting-only

- Right “used / consumed” state

This must not be interpreted as:

**“a new anonymous participant now exists”**

### Forbidden as public signals

The system must not expose any artifact that acts as a participant label:

- activation-as-identity event
- claim / entitlement artifacts
- sponsor-to-participant linkage
- cohort or batch identity markers

## Security objective (enrollment)

The enrollment model must ensure:

**public admission events do not form a reliable participant shortlist**

After this model:

### No longer acceptable as the cheapest attack path

`public funding -> recent entrant shortlist -> anonymous action`

### Remaining dominant risks (accepted for this iteration)

- network-level metadata
- cross-layer timing correlation
- relay / mirror observation
- low-volume anonymity weakness

## Non-goals (this iteration)

This enrollment change does **not** attempt to solve:

- network-layer anonymity
- relay metadata leakage
- mirror access-pattern leakage
- global anonymity set size

These remain later-phase concerns.

Supporting design docs:

- `docs/ADMISSION_RIGHT_MODEL_V0.md`
- `docs/UNLINKABLE_ENROLLMENT_DESIGN_V0.md`
- `docs/ADMISSION_DEPLOYMENT_FLOW_V0.md`
- `docs/PRIVACY_ENGINE_DEFINITION.md`

These documents remain supporting material only.  
If any conflict exists, STATE.md wins.

---

# 8) Anonymous Membership Layer (Current Canonical Model)

## Identity model

Client stores one membership secret per wallet in localStorage.

Storage key:

`su_memberSecret_v1:wallet:<walletLowercase>`

This is a current MVP frontend/runtime behavior and not the canonical architectural identity rule.

Canonical leaf definition:

`leaf = Poseidon1(memberSecret)`

The leaf is the sole anonymous membership identity primitive.

## Core properties

- Membership identity is derived solely from `memberSecret`
- The leaf is the only identifier used for:
  - path lookup
  - proof generation
  - nullifier derivation

## Backend interaction

Backend path lookup remains:

`/api/membership/path?leaf=<hex>`

Backend remains leaf-indexed only and must not regress toward wallet-indexed membership recovery.

## Invariants

- Leaf model unchanged
- Proof system unchanged
- Nullifier model unchanged

---

# 9) Nullifier Model (Locked)

`nullifier = Poseidon3(memberSecret, petitionId, SIGN_DOMAIN)`

On-chain:

- nullifier stored per petition
- duplicates rejected

This enforces one signature per petition per member.

---

# 10) Backend Role (MVP)

Backend is non-authoritative.

Responsibilities:

- Mirror membership events
- Rebuild Merkle tree
- Serve membership paths
- Relay ZK proof signing transactions

Must NOT:

- Gate membership
- Gate signing
- Store secrets
- Become a sponsor registry
- Become an enrollment provenance oracle

### Backend configuration (canonical)

- `ANON_MEMBERSHIP_PROXY_ADDRESS` is the canonical backend env variable for the `AnonymousMembershipRegistry` proxy
- Legacy backend aliases are temporarily supported during transition:
  - `MEMBERSHIP_REGISTRY_ADDRESS`
  - `MEMBERSHIP_ADDRESS`
- New setup should use `ANON_MEMBERSHIP_PROXY_ADDRESS`

---

# 11) Path Privacy Hardening (Implemented)

Goal:

Remove wallet address from membership path requests.

Original API:

`GET /api/membership/path?wallet=<address>`

New API (current):

`GET /api/membership/path?leaf=<hex>`

Leaf is defined as:

`leaf = Poseidon1(memberSecret)`

The frontend computes the leaf locally and requests the membership path by leaf.

This removes direct wallet identifiers from path distribution requests and reduces backend-level deanonymization risk.

Implementation notes:

- Backend supports both wallet and leaf lookup during transition
- Frontend now uses leaf-based lookup exclusively
- Verified operational in milestone tag: `m2-leaf-path-stable`

No circuit or contract changes required.

---

# 12) Relayer Signing (Implemented)

Goal:

Decouple proof submission from the wallet that sends the on-chain transaction.

Previous flow (prototype):

`frontend -> wallet -> contract`

The user's wallet directly submitted the transaction calling:

`signPetitionWithZKProof(...)`

This exposed the wallet address as the transaction sender and created a metadata link between the wallet and the petition signing event.

Current flow (implemented):

`frontend -> backend relayer -> contract`

Frontend sends the ZK proof payload to:

`POST /api/relay/sign`

Backend:

1. Validates payload structure
2. Checks nullifier status
3. Submits transaction via relayer wallet

Contract interface remains unchanged:

`signPetitionWithZKProof(
  petitionId,
  nullifier,
  pA,
  pB,
  pC,
  pubSignals
)`

Privacy result:

- On-chain sender is now the **relayer wallet**
- User wallet is not exposed during signing
- Identity remains protected by the ZK proof and nullifier

Design docs:

- `docs/RELAYER_IMPLEMENTATION_PLAN.md`
- `docs/RELAYER_PROTOCOL_DESIGN.md`

---

# 13) Known MVP Limitations

Current accepted limitations include:

- Backend relayer can observe submissions
- Network metadata (IP / timing) may leak correlations
- Backend required for membership path distribution
- Secret loss breaks signing on that device
- Network-layer anonymity is not solved
- Low-volume anonymity sets remain weak

Historical limitation “enrollment publicly tied to wallet” is the attack path targeted by Enrollment Layer V1 and must be removed by faithful implementation of that model.

Full privacy analysis:

`docs/PRIVACY_THREAT_MODEL.md`

---

# 14) Verified Operational Baseline (Milestone)

Milestone tag:

`m2-leaf-path-stable`

This milestone represents a fully working M2-only baseline with:

Verified flows:

- Existing enrolled wallet signing
- Fresh wallet enrollment → signing
- Petition creation
- Petition create + sign
- Signature persistence across refresh
- Petition list signature counts updating correctly
- Leaf-based membership path lookup operational
- Relayed ZK signing operational

Frontend / backend loop is considered stable at this milestone.

This serves as the recovery point before further protocol evolution.

---

# 15) Aurora Admission Stack Deployment + Validation (Milestone)

This milestone records the first successful deployment, verification, and live functional validation of the admission-backed anonymous membership stack on Aurora testnet.

Canonical validated Aurora testnet deployment:

- `POSEIDON1_ADDRESS = 0x358730D22814c9f5c02A282671b9892E28AC88A2`
- `POSEIDON2_ADDRESS = 0x24120c6ffe7A19a675B5C63d8A2a4b135D641A5d`
- `ANON_MEMBERSHIP_LOGIC_ADDRESS = 0x32A0f3db8ed95C693C802Eb0A037b7c8e19c8c39`
- `ANON_MEMBERSHIP_PROXY_ADDRESS = 0xe3A5cAab30DfF154e6Dff35cB35Ba41326C76821`
- `ADMISSION_LOGIC_ADDRESS = 0xff6f693Ce5975F996AF27b002e017f34d599Aac5`
- `ADMISSION_PROXY_ADDRESS = 0x36c22227098B24E5aCE48dEa3988327256481F0e`

Deployment discipline locked:

- repo-root `.env` is the single source of truth
- Solidity `.s.sol` files are deployment primitives
- shell `.sh` wrappers are the canonical operator entrypoints
- direct `forge script` runs must reload repo-root env into the active shell before execution:
  - `set -a`
  - `source ../.env`
  - `set +a`

Atomicity distinction locked:

- full-stack deployment is not globally atomic
- each proxy deployment + initialization is atomic because initializer calldata is passed into the proxy constructor
- the only intentional inter-stage gap is final linkage:
  - `AnonymousMembershipRegistry.setAdmissionRegistry(admissionProxy)`
- this intermediate state is acceptable because membership registration remains gated until linkage

Verification status:

- wrapper-based Aurora deployment completed successfully
- `verify-admission-stack.sh` completed successfully against the canonical deployment
- live admission → membership validation completed successfully on Aurora against the canonical deployment

Live validation result:

- `admissionCommitment = Poseidon1(admissionSecret)`
- `leaf = Poseidon1(memberSecret)`

Observed canonical live validation state transition:

- pre-state:
  - `leafCount = 0`
  - `isKnownLeaf(leaf) = false`
  - `status = 0`
- post-state:
  - `leafCount = 1`
  - `isKnownLeaf(leaf) = true`
  - `status = 2`

Operational conclusion (locked):

The admission-backed anonymous membership path is now live and validated on Aurora testnet.  
This checkpoint establishes the deployment and verification discipline for future iterations and provides the recovery point for subsequent integration into the M2 privacy flow.

Refund-path validation remains a separate time-based check because it depends on lock expiry.

A separate short-lock Aurora test deployment was executed with:

- `ADMISSION_LOCK_SECONDS = 120`

This was used only to validate refund logic without waiting for the canonical 7-day lock.

Observed refund-path state transition:

- pre-refund:
  - `status = 1`
  - `amount = 1000000000000000000`
- post-refund:
  - `status = 3`
  - `amount = 0`

Conclusion:

- `refundAdmissionRight(admissionSecret, recipient)` behaves correctly after lock expiry
- refund logic is validated on Aurora
- the canonical 7-day refund test remains a passive long-lock confirmation, but is no longer a blocker for correctness

---

# 16) Admission-backed M2 Integration Status

Frontend and backend integration has been validated against the canonical Aurora deployment.

Integrated flow now proven:

- explicit enrollment is owned by `PetitionDetails.jsx`
- enrollment no longer executes from `Petitions.jsx`
- frontend enrollment uses:
  - `fundAdmissionRight(admissionCommitment)`
  - `activateMembership(admissionCommitment, admissionSecret, leaf)`
- `leaf = Poseidon1(memberSecret)` remains unchanged
- backend membership indexing is aligned to `AnonymousMembershipRegistry`
- backend path lookup remains leaf-based:
  - `/api/membership/path?leaf=...`

End-to-end result validated on Aurora:

- non-enrolled wallet completed explicit admission-backed enrollment
- backend returned a valid Merkle path for the newly inserted leaf
- M2 proof generation succeeded unchanged
- relayed petition signing succeeded unchanged
- signed-state UI updated correctly after signing

Operational conclusion:

The admission-backed enrollment model is integrated into the existing M2 privacy flow without modification to the ZK proof system.

---

# 17) TEMPEST Phase A (execution-layer design locked)

The Phase A multi-relayer execution layer is now locked under the name **TEMPEST**.

TEMPEST is the execution/submission layer of the privacy engine.  
It is not the enrollment layer and not the path-distribution layer.

Phase A TEMPEST baseline:

- fixed 7-relay set (`T E M P E S T`)
- deterministic shuffle per action
- relayers are operationally stateful but privacy-stateless
- relayers must not retain identity or correlation state — whether by design, accident, misconfiguration, or emergent behavior
- treasury-backed relay continuity
- standardized relay interface
- deterministic failure and fallback behavior

TEMPEST Phase A is intended to improve:

- execution-layer privacy
- liveness
- censorship resistance
- operational robustness

It does **not** by itself solve:

- wallet-funded enrollment linkage
- path-server centralization
- network metadata leakage
- anonymity-set weakness at low volume

Detailed Phase A design is defined in:

- `docs/tempest/TEMPEST_OVERVIEW_V1.md`
- `docs/tempest/TEMPEST_RELAY_SELECTION_V1.md`
- `docs/tempest/TEMPEST_OBSERVABILITY_POLICY_V1.md`
- `docs/tempest/TEMPEST_TREASURY_CONTINUITY_V1.md`
- `docs/tempest/TEMPEST_RELAY_INTERFACE_V1.md`
- `docs/tempest/TEMPEST_FAILURE_AND_FALLBACK_V1.md`

---

# 18) REFLECT Phase A (path-layer design locked)

The Phase A distributed mirror path layer is now locked under the name **REFLECT**.

REFLECT is the path/witness-data layer of the privacy engine.  
It is not the enrollment layer and not the execution/submission layer.

Phase A REFLECT baseline:

- fixed 7-mirror set (**REFLECT**)
- distributed multi-source publication model
- client-verifiable subtree-chunk data model
- fixed subtree chunks
- medium subtree size policy
- single connector object per root
- hybrid discovery
- 3 chunk interests per action:
  - 1 required chunk
  - 2 deterministic cover chunks
- symmetric deterministic cover offsets derived from the action seed
- chunk interests split across mirrors
- mirror roles derived by deterministic per-action permutation
- connector object fetched from a separately selected REFLECT mirror
- connector separation enforced
- 2 fallback mirrors per object
- bounded recent publication window
- deterministic state targeting:
  - highest recent valid publication state
- integrity + coherence verification required across all selected objects
- no cross-state mixing
- no global reshuffle during fallback

REFLECT Phase A is intended to improve:

- path-layer privacy
- robustness under mirror skew or mild staleness
- resistance to centralized path-oracle observation
- future scalability for larger tree depth / anonymity-set growth

REFLECT Phase A does **not** by itself solve:

- wallet-funded enrollment linkage
- network-level metadata leakage
- mirror collusion
- total elimination of chunk access-pattern leakage

Detailed Phase A design is defined in:

- `docs/reflect/REFLECT_OVERVIEW_V1.md`
- `docs/reflect/REFLECT_OBJECT_MODEL_V1.md`
- `docs/reflect/REFLECT_PUBLICATION_WINDOW_V1.md`
- `docs/reflect/REFLECT_STATE_VALIDITY_V1.md`
- `docs/reflect/REFLECT_MIRROR_SELECTION_V1.md`
- `docs/reflect/REFLECT_FETCH_POLICY_V1.md`
- `docs/reflect/REFLECT_FAILURE_AND_FALLBACK_V1.md`
- `docs/reflect/REFLECT_SELECTION_POLICY_V1.md`

---

# 19) Engineering[9] Consolidation Checkpoint

Backend env/config naming has been normalized around:

- `ANON_MEMBERSHIP_PROXY_ADDRESS` (canonical)

Temporary backend aliases remain supported during transition:

- `MEMBERSHIP_REGISTRY_ADDRESS`
- `MEMBERSHIP_ADDRESS`

Runtime behavior is unchanged:

- backend remains leaf-indexed only
- path lookup remains `/api/membership/path?leaf=...`
- ZK proof generation, relay signing, and on-chain verification are unchanged

Engineering[9] also locked:

- the Phase A TEMPEST execution-layer design under `docs/tempest/`
- the Phase A REFLECT path-layer design under `docs/reflect/`

Together these establish the first two bounded infrastructure layers of the privacy engine:

- TEMPEST = execution / submission
- REFLECT = path / witness-data publication

---

# 20) Next Strategic Layer (Post-MVP)

Long-term Tornado-grade privacy requires:

- unlinkable enrollment model
- multi-relayer infrastructure
- strong artifact provenance enforcement
- larger anonymity sets

Speak-Up is evolving toward a **privacy participation engine** that allows valid actions to be publicly verified while preserving ambiguity about which participant performed them.

Core design rule:

**Private actors, public actions.**

The verifier proves validity; the architecture must preserve ambiguity.

Definition of the core privacy primitive:

`docs/PRIVACY_ENGINE_DEFINITION.md`

This document defines the minimal privacy engine that applications (petitions, coordination signals, funding systems, etc.) can build on top of.

The next architectural evolution focused on breaking the public wallet → membership link while preserving economic admission friction and compatibility with the current ZK signing model is now captured in Section 7 of this STATE file as Enrollment Layer V1.

Design must precede implementation.  
All architectural changes must be recorded in `STATE.md` first.

---

STATE.md remains canonical.

If any conflict arises between code and documentation:  
STATE.md governs.