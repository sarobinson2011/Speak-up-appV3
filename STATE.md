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

Status: **historical / deprecated unless explicitly reintroduced**

The earlier separate-machine autonomous-agent workflow is not the active development authority.

Current active app development authority is:

- Steve working on `main`
- GPT-assisted `Engineering[n]` process
- bounded human-reviewed changes
- clean commit/tag checkpoints

Historical `agent/iter-*` branch conventions are retained below as historical process context only.

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
- Anonymous actions must not be linkable across petitions by any reusable public identifier
- Admission-layer identifiers must not be carried, stored, logged, or emitted as action-layer correlation tags

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

NOTE: Current implementation addresses may evolve via upgrade.
Always refer to the latest Engineering[n] section for current live implementations.

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
- Consumed rights are not refundable
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

## 7.7 Incentive Settlement — Invariants (V1)

This section defines the invariant rules governing the incentive settlement layer.
These rules constrain all implementations and must hold across all contract and
off-chain policy designs.

#### Lifecycle invariants

1. **Single terminal path per right**  
   A funded admission right may resolve through exactly one terminal economic path:
   - unused-right refund, or
   - consumed-right incentive refund

   A right must never complete both paths.

2. **Consumed-only eligibility**  
   Only rights in the `Consumed` state are eligible for incentive settlement.

   Incentive outcomes are earned by the anonymous action that consumes the right,
   not by funding or readiness state.

3. **Single band assignment**  
   Each consumed right may receive at most one refund band assignment.

   Band assignments are immutable once recorded.

4. **Single settlement**  
   Each assigned band may be claimed at most once.

   No re-entrancy or replay may result in multiple payouts for the same right.

5. **Accounting-only consumption**  
   The `Consumed` state remains accounting-only and must not become a participant,
   cohort, or readiness signal.

#### Economic invariants

6. **Bounded payout**  
   The total refund paid for a consumed right must not exceed the allowed bound
   implied by the bond and configured band schedule.

7. **No value creation**  
   Incentive settlement must not create net new value. Total payouts across all
   terminal paths for a right must not exceed the value committed for that right.

8. **Finite coarse band set**  
   Refund outcomes are restricted to exactly three coarse bands:
   - reduced
   - standard
   - enhanced

   No additional implicit or derived bands may exist.

9. **Anti-farming constraint**  
   The enhanced refund band must remain economically conservative such that:

   > the additional refund available from enhanced outcomes is strictly less than
   > the economic cost required to manufacture the conditions that would trigger
   > those outcomes.

   This ensures that shared anonymity cannot be profitably fabricated.

#### Authority invariants

10. **Authorized band assignment only**  
    Refund bands may only be assigned by the designated policy authority
    (V1: single replaceable signer).

11. **Consequence without explanation**  
    The policy authority assigns only a coarse consequence.

    No explanation, score, threshold, window metadata, or reason codes may be
    required or persisted on-chain.

12. **Replaceable authority**  
    The policy authority must be replaceable without altering admission semantics
    or historical right states.

#### Separation-of-concerns invariants

13. **AdmissionRegistry scope**  
    The AdmissionRegistry owns:
    - bond custody
    - admission-right lifecycle
    - unused-right refund path
    - authorized payout execution

    It must not:
    - compute incentive outcomes
    - store refund bands
    - store or infer anonymity-related metrics

14. **IncentiveSettlement scope**  
    The IncentiveSettlement module owns:
    - coarse refund band assignment
    - policy signature verification
    - refund amount derivation from band
    - triggering authorized payout

    It must not:
    - hold primary bond custody
    - store cross-layer traces
    - act as a provenance or identity oracle

15. **No cross-layer trace persistence**  
    No backend, relay, mirror, or preparation-path data may be persisted on-chain
    as part of incentive evaluation or settlement.

#### Event surface invariants

16. **Accounting-only events**  
    Public events must remain limited to:
    - band assignment (coarse only)
    - refund claim / payout

    Events must not expose:
    - privacy scores
    - execution window data
    - density or sparsity metrics
    - threshold conditions
    - participant or cohort labels

#### Core design rule

> On-chain state records and settles only the coarse economic consequence.  
> It must never expose or reconstruct the hidden evaluation function.

Supporting design docs:

- `docs/ADMISSION_RIGHT_MODEL_V0.md`
- `docs/UNLINKABLE_ENROLLMENT_DESIGN_V0.md`
- `docs/ADMISSION_DEPLOYMENT_FLOW_V0.md`
- `docs/PRIVACY_ENGINE_DEFINITION.md`

These documents remain supporting material only.  
If any conflict exists, STATE.md wins.

## 7.8 Engineering[11] fallout / active-source leakage pass

After the AdmissionRegistry semantic hardening milestone:

- `Status.Activated` -> `Status.Consumed`
- `AdmissionRightActivated(...)` -> `AdmissionRightConsumed(...)`
- public right -> leaf bridge removed from the AdmissionRegistry event surface

Engineering[11] performed a bounded fallout / alignment pass across active source (`contracts`, `frontend/src`, `backend`) to confirm that no active runtime surface or source-language artifact still depended on the old participant-oriented admission semantics.

Result:

- no active runtime dependency on `AdmissionRightActivated`
- no active runtime dependency on `Status.Activated`
- no active frontend/backend event consumer relying on the old activation event
- no active source-language artifact remained that reintroduced the forbidden public activation bridge
- one stale frontend enum comment was corrected from `Activated` to `Consumed`

Deferred:

- stale references remain in supporting V0 admission docs only
- these are documentation-hygiene items and do not alter the canonical architecture
- if any conflict exists, `STATE.md` remains authoritative

Locked interpretation:

- right `Consumed` state is accounting-only
- it must not be interpreted as participant creation, participant readiness, or a public right -> participant mapping


## 7.9 Incentive Settlement implementation checkpoint

The V1 incentive settlement contract shape is now implemented and test-covered as a modular block separate from `AdmissionRegistry`.

Locked implementation shape:

- `AdmissionRegistry` remains the economic rights ledger and bond custodian
- `IncentiveSettlement` is a separate module
- coarse refund consequences are restricted to exactly three bands:
  - `Reduced`
  - `Standard`
  - `Enhanced`
- band assignment is signer-authorized (V1: single replaceable signer)
- the hidden evaluation function is not computed on-chain
- on-chain state records and settles only the coarse economic consequence
- consumed-right refunds are paid through a narrow authorized payout hook in `AdmissionRegistry`

Implemented contract responsibilities:

### AdmissionRegistry

Owns:
- bond custody
- admission-right lifecycle
- unused-right refund path
- authorized payout execution for consumed-right incentive refunds

Does not own:
- refund-band assignment
- signer verification
- incentive interpretation

### IncentiveSettlement

Owns:
- policy signer
- linked `AdmissionRegistry`
- refund schedule for the three coarse bands
- signer-authorized band assignment
- consumed-right refund claim flow

Does not own:
- primary bond custody
- hidden-function computation on-chain
- cross-layer trace persistence

Test-covered properties:

- unauthorized payout rejected
- consumed-only payout path enforced
- consumed-right payout is one-shot
- refund schedule admin/config guards enforced
- band assignment is consumed-only and one-shot
- invalid signatures rejected
- signer rotation enforced correctly
- refund claim is one-shot
- unused-right refund path and consumed-right refund path remain mutually exclusive
- total terminal payout for one right does not exceed committed value

---

## 7.10 Settlement Routing via Anonymous Public Action (V1) — SUPERSEDED

> Engineering[18] correction:
> This section is retained as historical design context only.
> It has been superseded for the active M2 petition-signing path.
>
> Active rule:
> - petition signing must not mutate AdmissionRegistry state
> - petition signing must not call `recordActionLink`
> - `admissionCommitment` must not be emitted as a reusable public cross-petition tag
> - nullifier uniqueness remains the only action-layer uniqueness rule
>
> Reason:
> the original one-right-to-one-action linkage model conflicted with reusable anonymous membership
> and introduced a public correlation surface across petition actions.

## 7.10 Historical Superseded Design — Settlement Routing via Anonymous Public Action (V1)

### Purpose

This section defines the minimal routing mechanism that connects an accepted anonymous public action to the consumed admission right that may later receive incentive settlement.

This is a **routing-only extension** of the V1 incentive system. It does not alter:

- anonymous membership semantics
- ZK proof/nullifier model
- epoch classification or hidden-function policy
- band assignment or payout logic

The action earns consequence. The right only receives settlement.

---

### Core Principle

An accepted anonymous public action may carry a **routing-only settlement reference**:

- `admissionCommitment`

This reference:

- identifies the consumed right that will receive settlement **if** later authorized
- is **not** used in anonymity evaluation
- is **not** part of the ZK proof model
- does **not** imply participant identity, origin, or readiness
- does **not** imply settlement outcome at action time

It is a **routing association only**, not a provenance bridge.

---

### Action-Level Integration

The petition-sign action path is extended to include:

- `admissionCommitment` as a routing-only field

Action acceptance follows a strict atomic sequence:

1. validate anonymous public action (proof, root, nullifier)
2. validate-and-record right-side linkage integrity via AdmissionRegistry
3. record accepted action
4. emit accepted-action event including `admissionCommitment`

If any step fails:
- the entire transaction reverts
- no partial action or linkage state is recorded

There are no intermediate states.

---

### Event Surface Policy

The accepted anonymous public action event is extended:

- add exactly one new field:
  - `admissionCommitment`

Constraints:

- no new standalone linkage event family
- no epoch, band, or settlement metadata
- no explanatory or provenance fields
- no language implying:
  - participant origin
  - right realization
  - reward qualification

The event remains **action-centered**.

---

### Storage Policy

#### PetitionRegistry

Stores:

- accepted anonymous public action records
- embedded routing-only `admissionCommitment` (if required)

Does not store:

- standalone right-link registries
- epoch or settlement metadata
- provenance or explanatory linkage structures

Remains **action-centered**.

---

#### AdmissionRegistry

Stores:

- one minimal integrity marker per right indicating:
  - the consumed right has already been action-linked once

This marker:

- enforces one-to-one routing integrity
- does not imply settlement outcome
- does not encode action history

Does not store:

- action metadata
- petition/nullifier linkage history
- epoch/band/context data
- provenance semantics

Remains **right-centered**.

---

### Authority Split

- **PetitionRegistry**
  - validates anonymous action
  - initiates routing association
  - emits accepted-action event

- **AdmissionRegistry**
  - validates right existence and lifecycle compatibility
  - enforces one-time action linkage integrity
  - records minimal linkage marker

- **IncentiveSettlement**
  - unchanged
  - performs band assignment and payout downstream

No circular dependencies.

---

### Interface Constraint

AdmissionRegistry exposes a single narrow procedural interface:

- accepts only `admissionCommitment`
- validates and records one-time linkage atomically
- callable only by PetitionRegistry
- does not expose descriptive right-state getters

No multi-call inspection or query-style interface is introduced.

---

### Observability Policy

New linkage-integrity state is **not exposed via public getters**.

Allowed observability:

- accepted-action event including `admissionCommitment`
- existing settlement-layer outputs

Not allowed:

- linkage convenience getters
- right introspection APIs for linkage state
- action-to-right query helpers
- descriptive revert or diagnostic surfaces

Minimal storage must not become a queryable bridge.

---

### Naming & Documentation Constraint

All implementation surfaces must treat language as part of the privacy boundary.

Allowed framing:

- "routing-only settlement reference"
- "consumed-right settlement target"
- "linkage integrity"

Forbidden framing:

- participant origin / identity
- actor/source right
- reward qualification / eligibility
- "right used by signer"
- any narrative reconstructing actor from right

Applies to:

- code
- comments
- tests
- docs
- logs

---

### Non-Goals (Explicit)

This routing layer does not:

- create a participant identity bridge
- expose action-to-identity mapping
- evaluate anonymity quality
- determine settlement outcome at action time
- introduce new lifecycle states for rights
- modify ZK or nullifier semantics

---

### Invariant Summary

- one anonymous action → one consumed right (routing-only)
- one consumed right → at most one action linkage
- action acceptance and linkage are atomic
- no partial or deferred linkage states
- no explanatory metadata stored or exposed
- settlement outcome remains downstream and coarse

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

### Deployment Record Interpretation

Deployment sections record historical deployment milestones.

For current live implementation addresses, linkage state, and post-upgrade operational truth, the latest completed Engineering[n] checkpoint governs.

Proxy addresses are stable canonical entrypoints unless explicitly superseded.

Implementation addresses are mutable through upgrades and must be read from the latest Engineering[n] checkpoint or directly from the proxy implementation slot.

This milestone records the first successful deployment, verification, and live functional validation of the admission-backed anonymous membership stack on Aurora testnet.

Canonical validated Aurora testnet deployment:

- `POSEIDON1_ADDRESS = 0x358730D22814c9f5c02A282671b9892E28AC88A2`
- `POSEIDON2_ADDRESS = 0x24120c6ffe7A19a675B5C63d8A2a4b135D641A5d`
- `ANON_MEMBERSHIP_LOGIC_ADDRESS = 0x32A0f3db8ed95C693C802Eb0A037b7c8e19c8c39`
- `ANON_MEMBERSHIP_PROXY_ADDRESS = 0xe3A5cAab30DfF154e6Dff35cB35Ba41326C76821`
- `ADMISSION_LOGIC_ADDRESS (initial deployment) = 0xff6f693Ce5975F996AF27b002e017f34d599Aac5`
- 'Current implementation: see Engineering[17] “Current Deployed State”'
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

# 21) Position A — Anti-Abuse Objective & Secret Continuity Discipline (Locked)

This section defines the bounded anti-abuse model and secret continuity rules for the M2 privacy system.

It does not modify:

- ZK circuit
- nullifier model
- leaf derivation
- contract interfaces
- backend role

It clarifies **what the system guarantees**, **what it does not guarantee**, and **how identity continuity is handled operationally**.

---

## 21.1 Anti-Abuse Objective (Position A)

The system guarantees:

> one sign per anonymous member per petition via nullifier enforcement

This guarantee is:

- enforced on-chain
- independent of frontend or client
- derived from the nullifier model:
  - `nullifier = Poseidon3(memberSecret, petitionId, SIGN_DOMAIN)`

---

### Explicit non-goals

The system does **not** guarantee:

- one identity per wallet
- one identity per human
- prevention of all Sybil behavior
- recovery of anonymous identity without the original secret
- wallet-level uniqueness hidden behind anonymity

---

### Abuse resistance model

Resistance to repeated participation is provided by:

1. **Economic admission friction**
   - funded admission rights
   - one-time activation → one membership leaf
   - cost / lock / refund structure

2. **Secret continuity discipline**
   - preventing accidental identity replacement
   - preventing silent re-enrollment after secret loss

The system must not rely on:

- wallet binding
- backend memory
- heuristic identity reconstruction

---

## 21.2 Identity Model Clarification

Anonymous identity is defined strictly as:

> possession of `memberSecret` → derivation of `leaf` → membership inclusion

Canonical:

- `leaf = Poseidon1(memberSecret)`

The leaf is the sole anonymous identity primitive.

---

### Continuity rule

> continuity of identity = possession of the same `memberSecret`

Anything else is a different identity.

---

## 21.3 Secret Continuity Invariants

The following invariants are locked:

### (1) Secret-possession continuity

Possession of the original `memberSecret` is the only valid basis for identity continuity.

---

### (2) Restoration-only-by-secret

Identity restoration is possible only by reintroducing the original secret.

No wallet, backend, or heuristic recovery is allowed.

---

### (3) New-secret-new-identity

Any different `memberSecret` defines a different anonymous identity.

---

### (4) Enrollment-attaches-to-present-secret

Enrollment always applies only to the currently active secret.

It must never imply restoration.

---

### (5) Observable-state-only behavior

System behavior must depend only on:

- secret present / absent
- derived leaf in tree or not
- nullifier usage

No lifecycle inference is allowed.

---

### (6) No silent identity replacement

The system must not silently convert:

lost identity → new identity

without explicit operator action.

---

## 21.4 Minimal Secret Continuity Toolkit

The system supports exactly four identity-management operations:

### 1. Export

- copies `memberSecret` to operator custody
- preserves identity continuity
- does not modify identity

---

### 2. Import

- sets the active secret to supplied material
- may restore identity **only if** the original secret is provided
- never proves continuity beyond present possession

---

### 3. Create

- generates new `memberSecret`
- establishes new candidate identity
- never implies recovery or continuation

---

### 4. Enroll

- converts current secret-derived leaf into an enrolled identity
- valid only when leaf is not already in tree
- always creates an identity for the present secret
- never restores prior identity

---

## 21.5 Operator Flow Rules

The system exposes only the following flows:

- export
- import
- create
- enroll
- sign

---

### State-based rules

#### O0 — no secret present

Allowed:
- import
- create

Blocked:
- export
- enroll
- sign

---

#### O1 — secret present, leaf not in tree

Allowed:
- export
- import (replaces active secret)
- create (replaces active secret)
- enroll

Blocked:
- sign

---

#### O2 — secret present, leaf in tree

Allowed:
- export
- import/create (explicit replacement only)
- sign (if nullifier unused)

Blocked:
- enroll

---

### Signing constraint

Signing is allowed only when:

- secret present
- leaf in tree
- nullifier unused for petition

---

## 21.6 Hard Constraints

The following are strictly forbidden:

### (1) No implicit secret creation
Secrets must never be generated as a side-effect of normal actions.

---

### (2) No implicit enrollment
Enrollment must always be an explicit operator action.

---

### (3) No hidden secret replacement
Active secret material must not change invisibly.

---

### (4) No recovery-by-enrollment
Enrollment must never be framed or treated as identity recovery.

---

### (5) No wallet-based continuity
Wallet identity must not be used to infer or reconstruct anonymous identity.

---

## 21.7 Identity Boundary Principle

The system supports exactly two identity outcomes:

1. **Continue existing identity**
   - only by possessing the same secret

2. **Create new identity**
   - by using a different secret and enrolling it

The system must never blur these outcomes.

---

## 21.8 Privacy Preservation Constraint

All hardening measures must:

- avoid creating new linkage surfaces
- avoid cross-layer join keys
- avoid backend identity inference
- avoid persistent operator provenance

---

## 21.9 Summary

- One sign per anonymous member is enforced cryptographically.  
- Repeated participation is constrained economically and operationally.  
- Identity continuity is defined solely by secret possession.  
- The system must not infer, reconstruct, or simulate identity continuity.

---

## Engineering[14] — Identity Lifecycle & Admission Hardening (COMPLETED)

### Summary

Engineering[14] completed a bounded hardening and operator-surface alignment pass.  
No architectural, cryptographic, or identity-model changes were introduced.

The goal was to ensure that the implemented system matches the locked M2 identity semantics and is safe against operator/configuration errors.

---

### Identity lifecycle (Position A) — CONFIRMED

The system now behaves as:

- Identity is defined solely by `memberSecret`
- `memberSecret -> leaf -> nullifier` remains the only identity path
- Identity is NOT wallet-bound
- Identity continuity is NOT inferred

#### Manual validation completed:

- O2 → Export secret
- O2 → Create new secret → transition to O1
- O1 → Import original secret → restore O2
- New secret produces new leaf and fails membership lookup (404)
- Restoration via original secret re-establishes identity and signing ability

#### Operator model now explicit:

- Create → creates or replaces active identity (with confirmation)
- Import → restores identity via secret
- Export → allows persistence outside browser
- Enroll → binds current secret to membership tree
- Sign → requires valid secret + membership + unused nullifier

---

### UI / operator surface alignment — COMPLETED

`PetitionDetails.jsx` now correctly reflects observable state:

| State | Meaning |
|------|--------|
| O0 | No identity present |
| O1 | Identity present, not enrolled |
| O2 | Identity enrolled and usable |

#### Changes:

- Identity controls (create/import/export) are always reachable in valid states
- Explicit replacement flow added (no silent overwrite)
- Disabled-action messaging added:
  - signing unavailable when not enrolled
  - recovery guidance for mismatch state
- Status panel is always rendered (no hidden identity state)

---

### AdmissionRegistry hardening — COMPLETED

#### Setter validation added:

- `setAdmissionBond` rejects invalid values
- `setLockPeriod` rejects invalid values

#### Verified properties:

- Existing rights store `amount` and `unlockAt`
- Changing config affects only future rights
- Refunds use stored `amount`, not global bond
- No retroactive economic effects

#### Tests added and passing:

- setter validation (owner / non-owner / invalid input)
- non-retroactivity of:
  - bond → `amount`
  - lockPeriod → `unlockAt`

---

### Invariants preserved

No changes to:

- ZK circuit
- Poseidon usage
- leaf derivation
- nullifier model
- membership tree semantics
- relayer flow

---

### Resulting system state

The system is now:

- cryptographically unchanged
- economically safer (config hardening)
- operationally explicit (identity lifecycle)
- deterministic under manual testing

This closes the identity/operator-surface gap between design and implementation.

---

### Engineering[14] status

**CLOSED — checkpoint complete**

Further work must treat:

- identity lifecycle semantics as locked
- admission config behavior as stable

No reopening of Position A or secret semantics without explicit STATE.md change.

---

---

## Engineering[16] — Petition Indexer + Read Layer Stabilization (COMPLETED)

### Summary

Engineering[16] established a canonical backend indexer and read-layer for petition data, aligned frontend consumption to that layer, and removed implicit coupling between frontend state and chain-derived data.

No architectural changes were introduced. This is a read-path stabilization milestone.

---

### Petition Indexer V0 — IMPLEMENTED

A ground-truth indexer for `PetitionRegistry` is now implemented.

#### Indexed events

- `PetitionCreated`
- `PetitionSigned`

#### Data persistence: SQLite

- `petitions`
- `petition_signatures`
- `petition_signature_counts`
- `indexer_sync_state`

#### Properties

- deterministic block-range sync
- stable ordering: `(blockNumber, transactionIndex, logIndex)`
- resumable via `indexer_sync_state`
- canonical source of truth for petition data

---

### Canonical Petition Read Surface — LOCKED

Backend endpoint:

`GET /api/petitions`

Now returns:

- `petitionId`
- `creator`
- `metadataURI`
- decoded `metadata` when possible
- `createdAt` as chain timestamp
- `signatureCount` aggregated from indexed events

#### Invariant

The frontend must treat `/api/petitions` as the canonical petition state.

Frontend must not derive:

- signature counts from chain queries
- petition ordering from local state

Read-model exposure rule:

- indexed `PetitionCreated` events create candidate petition rows
- backend API exposure requires current live contract existence
- petitions with `exists == false` in `PetitionRegistry.petitions(id)` must not be exposed through product read APIs
- historical rows may remain in SQLite for audit/reconciliation, but inactive rows are hidden from frontend consumption

---

### Metadata Decode Layer — IMPLEMENTED

Backend now decodes:

`data:application/json;base64,...`

into:

`metadata: { title, description }`

#### Result

- frontend no longer decodes base64 metadata
- metadata presentation is consistent and centralized

---

### Deployment Reality Alignment — CONFIRMED

Observed state:

- PetitionRegistry at canonical address contains `PetitionCreated` events
- PetitionRegistry at canonical address contains no `PetitionSigned` events

Result:

- `signatureCount = 0` for all current petitions is correct
- no indexer bug exists
- no aggregation bug exists

#### Locked interpretation

Signature counts reflect current contract history, not historical testing memory.

---

### Membership Path Behavior — CLARIFIED

Endpoint:

`GET /api/membership/path?leaf=...`

Returns:

- `200` when a path exists
- `404` when the leaf is not found / not enrolled

#### Locked interpretation

`404` is a valid state for an unenrolled leaf, not a protocol error.

Frontend behavior updated:

- no longer treats unenrolled-leaf path absence as exceptional
- reflects correct O0 / O1 / O2 identity states

---

### Membership Leaf Status Endpoint — IMPLEMENTED

Endpoint:

`GET /api/membership/leaf-status?leaf=...`

Returns:

`{ "exists": true | false }`

#### Purpose

- lightweight leaf existence check
- avoids path-fetch misuse for state probing
- avoids unnecessary `/path` requests for known unenrolled leaves

---

### Frontend Structural Refactor — IMPLEMENTED

#### Extracted components

1. `PetitionDisplaySection`
   - petition metadata
   - creator
   - description
   - signature count
   - progress bar

2. `M2IdentityControls`
   - create secret
   - import secret
   - export secret
   - reused across identity states

3. `M2StatusSection`
   - M2 status rendering
   - identity-state UI branching
   - signing availability messaging
   - M2 sign button placement

#### Results

- duplicated JSX removed
- `PetitionDetails.jsx` reduced substantially
- display concerns separated from M2 state rendering
- identity controls reused consistently across states
- frontend structure is easier to reason about before future work

---

### Identity UI Alignment — PRESERVED

All changes preserve Position A invariants:

- no implicit identity creation
- no implicit enrollment
- no silent identity replacement
- no wallet-based continuity inference

UI continues to correctly reflect:

- O0: no secret present
- O1: secret present, leaf not enrolled
- O2: secret present, leaf enrolled and usable

---

### Backend Role — UNCHANGED

Backend remains:

- non-authoritative
- event-indexing
- path-distribution
- relayer-supporting

Backend does not:

- gate identity
- infer identity
- store secrets
- become an enrollment provenance oracle

---

### Invariants preserved

No changes to:

- ZK circuit
- nullifier model
- leaf derivation
- contract interfaces
- admission semantics
- relayer flow

---

### Resulting system state

The system now has:

- deterministic petition state reconstruction
- canonical petition read surface
- decoded petition metadata presentation
- correct handling of empty signature sets
- explicit membership leaf existence signal
- stable identity UI aligned with backend truth
- reduced frontend structural complexity

---

### Engineering[16] status

**CLOSED — checkpoint complete**

Next work should build on:

- stable indexer substrate
- canonical read layer
- clean frontend component structure

No redesign required.

---

## Engineering[17] — End-to-End Petition Signing Validation (M2)

### Outcome

Engineering[17] successfully achieved a full end-to-end validation of the M2 Strong Privacy signing path:

- ZK proof generation (client): ✅
- Membership enrollment (Admission → AnonymousMembershipRegistry): ✅
- Relayed signing transaction: ✅
- On-chain `PetitionSigned` event: ✅
- Indexer ingestion → DB persistence: ✅
- API surface → frontend reflection: ✅
- UI duplicate prevention via nullifier: ✅

Concrete validation:

- Petition ID: 11
- Signature count: 1
- Transaction hash:
  `0x38a2ac41112c6959be823137ea015a72c06b16213ee99eb48370affa8208ecd1`

System is now functionally correct across the full pipeline.

---

### Critical Incident — Upgrade Safety Failure (Resolved)

During Engineering[17], a critical upgrade-safety failure was encountered and resolved.

#### Root Cause

The AdmissionRegistry was upgraded using a **newer source layout** instead of the **actual deployed baseline layout**.

Deployed baseline (on-chain implementation):
- Corresponds to commit: `b6997d5`

This baseline has storage:

slot 0 → admissionBond  
slot 1 → lockPeriod  
slot 2 → anonymousMembershipRegistry  
slot 3 → admissionHasher  
slot 4 → rights (mapping)

Later versions introduced new fields:

- incentiveSettlement
- consumedRefundPaid
- petitionRegistry
- _actionLinked

These were incorrectly assumed in upgrade planning and **inserted before the existing mapping**, causing:

- storage slot shift  
- `rights` mapping read from wrong slot  
- `getStatus()` returning `0` (None) for valid commitments  
- complete logical failure of admission validation  

#### Resolution

The correct fix was:

1. Identify deployed baseline (`b6997d5`)  
2. Reconstruct true storage layout from that baseline  
3. Rebuild AdmissionRegistry storage as **strict append-only from baseline**  
4. Verify via `forge inspect storage-layout`  
5. Re-upgrade implementation  
6. Validate live state invariants (existing commitment returns status `2`)  
7. Re-link PetitionRegistry ↔ AdmissionRegistry  
8. Resume signing flow  

Final correct storage layout:

slot 0 → admissionBond  
slot 1 → lockPeriod  
slot 2 → anonymousMembershipRegistry  
slot 3 → admissionHasher  
slot 4 → rights  

slot 5 → incentiveSettlement  
slot 6 → consumedRefundPaid  
slot 7 → petitionRegistry  
slot 8 → _actionLinked  
slot 9+ → __gap  

---

### Upgrade Safety Invariant (MANDATORY)

All future upgrades MUST follow this process:

1. **Canonical baseline = deployed implementation on-chain**  
   - NOT latest local code  
   - Extract via proxy implementation slot  

2. **Storage must be append-only**  
   - No insertion before existing variables  
   - No reordering  
   - No struct layout changes  
   - No inherited storage changes  

3. **Pre-upgrade validation**  
   - Identify baseline commit or reconstruct layout  
   - `forge inspect storage-layout` (old vs new)  
   - Confirm slot alignment  

4. **Post-upgrade gate (hard requirement)**  
   - Read known live state (e.g. admissionCommitment)  
   - Must match pre-upgrade values exactly  

5. **If any mismatch**  
   - STOP  
   - rollback immediately  
   - do not proceed  

---

### System Version Alignment Rule

The system is **version-coupled**:

PetitionRegistry ↔ AdmissionRegistry  

Therefore:

- Contracts must be treated as a **coordinated version set**  
- Upgrades must preserve **cross-contract compatibility**  
- Do not upgrade one contract assuming the other remains valid  

---

### Current Deployed State

PetitionRegistry:
- Proxy: `0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD`
- Implementation: `0xd7CAB0205889d0e308f4809e80a3Fc3C7e21F820`

AdmissionRegistry:
- Proxy: `0x36c22227098B24E5aCE48dEa3988327256481F0e`
- Implementation: `0xF2996875492829a2Dd263EdEbcb49C501E75C504`

Linkage:

- `PetitionRegistry.admissionRegistry` → AdmissionRegistry proxy ✅  
- `AdmissionRegistry.petitionRegistry` → PetitionRegistry proxy ✅  

---

### Known Follow-Up

Admission bond value is currently:

1.0 ETH  

This is incorrect for intended UX/economic model.

Fix required in future iteration:
- reduce bond magnitude  
- redeploy or upgrade safely (following invariant above)  
- ensure frontend safety threshold aligns with contract value  

---

## Engineering[18] — Admission Bond Correction

Live admission bond corrected without upgrade.

- Previous live bond: `1.0 ETH`
- New live bond: `0.01 ETH`
- Method: `AdmissionRegistry.setAdmissionBond(10000000000000000)`
- No proxy upgrade performed

Validation:

- Existing right non-retroactivity validated:
  - commitment: `0x0c61c6c3b7ba331900a3fe814bfa8494e51b53fb8e531c140664b38179b16c66`
  - stored amount remained `1000000000000000000`
  - status remained `2`

- New right funding validated:
  - commitment: `0x1b0e294500b3af4a904812280e777796062dcd9ea960e980122c5980322607b3`
  - stored amount: `10000000000000000`
  - status: `1`

Frontend:

- Temporary `1.01 ETH` safety ceiling replaced with `0.02 ETH`
- Frontend production build passes

No changes to:

- ZK
- PetitionRegistry
- relay
- membership semantics
- nullifier model

Engineering[18] status:

**CLOSED — admission bond correction complete**

---

## Engineering[18] — Action-Linking Architecture Bug Identified

During post-bond-correction smoke testing, signing a second petition with the same enrolled M2 identity failed.

Observed revert:

`RightAlreadyActionLinked()`

Root cause:

- `PetitionRegistry.signPetitionWithZKProof(...)` calls `AdmissionRegistry.recordActionLink(admissionCommitment)`
- `AdmissionRegistry.recordActionLink(...)` enforces one global action link per `admissionCommitment`
- this makes one consumed admission right usable for only one petition action total

This conflicts with the core petition product invariant:

- one anonymous member may sign many different petitions
- uniqueness is per `(petitionId, member)`
- uniqueness is enforced by the nullifier

Correct interpretation:

- reusable anonymous membership is canonical
- `memberSecret -> leaf -> nullifier` remains the identity path
- `nullifier = Poseidon3(memberSecret, petitionId, SIGN_DOMAIN)` enforces one signature per petition
- an admission right creates membership; it must not limit the member to one petition action total

Privacy correction:

- `admissionCommitment` must not become a reusable public cross-petition correlation tag
- emitting or requiring the same `admissionCommitment` on every petition signature is unsafe because it links actions across petitions
- settlement routing through public `admissionCommitment` is deferred until redesigned

Immediate implementation direction:

- remove the global action-link requirement from the petition signing path
- preserve nullifier-based duplicate prevention
- do not alter ZK circuit, leaf model, membership tree, or nullifier model
- perform upgrade only after storage-layout review and pre/post live-state gate

---

## Engineering[18] — PetitionRegistry Action-Linking Fix Deployed

PetitionRegistry was upgraded to remove action-linking from the M2 signing path.

Deployment:

- PetitionRegistry proxy: `0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD`
- New PetitionRegistry implementation: `0x6479Bea64CA55f2E5745b73A41d22089cBA1a3Db`

Reason:

- M2 signing previously called `AdmissionRegistry.recordActionLink(admissionCommitment)`
- this incorrectly limited one consumed admission right to one petition action total
- it also risked turning `admissionCommitment` into a public cross-petition correlation tag

Active rule:

- M2 petition signing does not mutate AdmissionRegistry state
- `admissionCommitment` is ignored in the signing path and emitted as `bytes32(0)`
- nullifier remains the only action-layer duplicate-prevention mechanism

Validation:

- pre-upgrade PetitionRegistry gate passed
- `forge test` passed: 93 tests
- UUPS upgrade completed successfully
- post-upgrade PetitionRegistry gate passed
- post-upgrade `forge test` passed: 93 tests

No changes to:

- ZK circuit
- membership tree
- nullifier derivation
- AdmissionRegistry storage
- relay API shape

---

STATE.md remains canonical.

If any conflict arises between code and documentation:  
STATE.md governs.
---

## 12. TEMPEST — Execution Layer (Phase A Scaffold)

Status: **IMPLEMENTED (Engineering[20]) — single-relay mode only**

### 12.1 Purpose

TEMPEST introduces a deterministic execution-layer abstraction to remove correlation and observability from the submission path, without modifying action semantics, identity model, or read model.

Phase A establishes the structural scaffold only. No real dispersion is active yet.

### 12.2 Core Properties (Phase A)

The execution path is now:

client  
→ validated relay route  
→ canonical submission (frozen)  
→ deterministic seed (internal only)  
→ deterministic permutation (7 slots)  
→ sequential attempt over slots  
→ executor (currently identical)  
→ chain

The system remains behaviorally identical to pre-TEMPEST.

### 12.3 Canonical Submission Payload

All execution is now driven by a canonical, immutable payload:

- petitionId
- nullifier
- proof (pA, pB, pC)
- pubSignals (ordered)
- admissionCommitment (fixed zero)

This payload:

- is frozen at execution boundary
- contains no identity-layer material
- contains no request metadata
- contains no correlation surface beyond nullifier semantics

### 12.4 Execution Boundary

A strict boundary is enforced:

`executeRelaySubmission({ registry, submission })`

Properties:

- no access to HTTP request/response
- no access to client metadata
- no access to identity/admission state
- no logging inside boundary
- submission is immutable

### 12.5 Deterministic Seed

Seed is derived as:

`keccak256(abi.encode(petitionId, nullifier, admissionCommitment, pA, pB, pC, pubSignals))`

Properties:

- deterministic per action
- derived only from canonical submission
- not logged, stored, or exposed
- not used outside execution layer

### 12.6 Deterministic Permutation

A fixed 7-slot permutation is derived from the seed.

Properties:

- stable per action
- bounded (no unbounded retries)
- not observable externally
- defines execution order

### 12.7 Relay Slots (Abstract)

Seven relay slots exist:

- slots 0–6
- currently all bound to same executor
- executor binding occurs at dispatch time
- no relay identity is exposed or persisted

### 12.8 Sequential Execution (Deterministic Fallback)

Execution attempts follow permutation order:

- sequential only
- no parallel execution
- first success returns
- failure falls through deterministically
- no reshuffle or randomness

### 12.9 Phase A Constraints

Phase A explicitly does NOT include:

- multiple real relayers
- network-level dispersion
- routing over external infrastructure
- relay identity persistence
- correlation caches
- retry amplification
- timing randomization

### 12.10 Invariants Preserved

TEMPEST Phase A does not modify:

- nullifier uniqueness model
- ZK proof structure or verification
- petition contract interface
- read model authority (indexer)
- relay freshness gating
- frontend behavior or semantics
- admission model separation

### 12.11 Next Phase (Not Implemented)

Future phases will introduce:

- real multi-relayer execution
- deterministic mapping of slots → relayer endpoints
- bounded failure handling across independent executors
- path-layer obfuscation (REFLECT)

These must preserve all invariants defined above.


---

## Engineering[20] — TEMPEST Controlled Fallback Validation

A controlled fallback simulation was implemented and validated.

Implementation:

- `TEMPEST_FAIL_EXECUTOR_B=true` enables deterministic failure of execution domain B
- execution domains remained locally orchestrated during this validation phase
- no external relayers were introduced
- no frontend/API response shape changed
- no relay slot, seed, permutation, or executor identity is logged or exposed

Validation:

- backend started successfully with `TEMPEST_FAIL_EXECUTOR_B=true`
- relay status remained healthy
- petition indexer remained healthy
- a fresh M2 identity was enrolled
- ZK signing succeeded through the UI
- frontend reflected the correct signed state after submission
- deterministic fallback did not alter user-visible semantics

Locked interpretation:

TEMPEST Phase A now has validated deterministic fallback behavior in single-relay/local-executor mode.

This does not yet constitute real multi-relayer dispersion.


---

## Engineering[20] — TEMPEST Dual Execution Surface Validation

TEMPEST was extended from abstract execution grouping into distinct execution handles.

Implementation:

- `backend/src/routes/relay.js` now constructs:
  - primary `registry`
  - secondary `secondaryRegistry`
- both point to the same PetitionRegistry address, wallet, and RPC provider
- `backend/src/services/relayExecution.js` accepts both execution handles
- slot-to-executor mapping remains deterministic
- controlled failure mode remains available through `TEMPEST_FAIL_EXECUTOR_B=true`

Validation:

- backend started successfully with controlled executor-B failure enabled
- `/api/relay/status` remained healthy
- `/api/indexer/status` remained healthy
- a fresh M2 signing flow succeeded through the UI
- signature count updated correctly after signing
- no seed, permutation, slot, or executor identity was exposed to frontend or logs

Locked interpretation:

TEMPEST Phase A now supports distinct local execution surfaces and validated deterministic fallback across those surfaces.

This remains single-relayer/local-executor mode.

No external relay endpoints or true network dispersion are active yet.

---

## Engineering[21] — TEMPEST Live Multi-Relayer Execution Validation

TEMPEST Phase A was extended from distinct local execution surfaces into validated multi-relayer execution using separate live relayer wallets on Aurora testnet.

The execution substrate now supports:

- explicit domain configuration
- per-domain provider construction
- per-domain wallet construction
- per-domain contract execution handles
- deterministic slot → domain mapping
- deterministic permutation traversal
- deterministic fallback behavior

The current implementation preserves:

- identical frontend behavior
- identical relay API shape
- identical petition semantics
- identical nullifier semantics
- identical read-model/indexer behavior

No relay topology information is exposed externally.

The frontend remains unaware of:

- selected relay slot
- selected execution domain
- relayer wallet identity
- fallback traversal behavior
- domain-specific infrastructure state

Controlled fallback validation remains available through:

- `TEMPEST_FAIL_EXECUTOR_B=true`

Optional infrastructure divergence is now supported through:

- `TEMPEST_DOMAIN_B_PRIVATE_KEY`
- `TEMPEST_DOMAIN_B_RPC_URL`

while preserving default single-config compatibility.

Engineering[21] validated:

- successful live petition signing through multiple distinct relayer wallets
- successful deterministic fallback behavior
- successful indexer reconciliation after multi-relayer execution
- unchanged frontend and API behavior during relay-domain divergence

This establishes TEMPEST Phase A as a live deterministic multi-relayer execution substrate while remaining within a single backend orchestration process.

No relay federation, distributed coordination, remote relay trust, or inter-relayer communication has been introduced.

---

## Engineering[22] — TEMPEST Operational Hardening Checkpoint

Engineering[22] performed a bounded operational-hardening pass on the live TEMPEST Phase A multi-relayer execution substrate.

No architectural expansion was introduced.

The system remains:

- M2-only
- single-backend orchestrated
- deterministic
- topology-hidden
- frontend/API compatible
- read-model/indexer compatible

No changes were made to:

- ZK proof semantics
- nullifier semantics
- petition semantics
- admission semantics
- indexer/read-model semantics
- frontend behavior

### Hardening completed

Implemented:

- field-specific TEMPEST execution configuration validation
- internal execution readiness classification
- deeper relay submission immutability at the execution boundary
- immutable static relay-slot configuration

### Configuration validation

TEMPEST execution configuration now fails earlier and more explicitly when required internal execution configuration is malformed.

Validated configuration surfaces include:

- execution RPC configuration
- execution registry configuration
- execution ABI configuration
- execution signer configuration

This is startup/operator hardening only.

It does not expose relay topology, selected execution path, fallback traversal, or execution-domain details.

### Internal readiness classification

An internal readiness helper now classifies constructed execution handles by coarse usability.

This helper is internal-only.

It must not become:

- a public topology surface
- a per-domain health API
- a relay reputation system
- a correlation cache
- a petition/nullifier/domain history store

### Execution-boundary immutability

Relay submissions are now frozen more deeply at the execution boundary.

Frozen surfaces include:

- proof arrays
- nested proof arrays
- public signals
- proof object
- submission object
- execution-domain array reference

This hardens the canonical submission boundary without changing submission content or execution semantics.

### Static relay-slot immutability

The static TEMPEST relay-slot configuration is now frozen.

This prevents accidental runtime mutation of the abstract slot set.

It does not alter:

- slot count
- deterministic permutation
- slot-to-domain mapping
- deterministic fallback traversal

### Validation

Checkpoint tag:

`tempest-hardening-v1`

Runtime validation after this checkpoint confirmed:

- backend booted cleanly
- relay status remained healthy
- relay health remained healthy
- petition indexer remained healthy
- working tree was clean before push

### Leakage / observability position

This checkpoint introduced no new external observability.

No new public surface exposes:

- selected relay slot
- permutation order
- execution domain
- relayer wallet identity beyond pre-existing relay health/status behavior
- fallback traversal path
- nullifier-linked relay history
- petition-linked relay topology
- domain health detail

Existing relay status/health surfaces remain coarse and unchanged.

### Explicit non-changes

Engineering[22] did not introduce:

- relay federation
- remote relay APIs
- relay mesh coordination
- distributed consensus
- inter-relayer communication
- public relay participation
- dynamic topology discovery
- adaptive routing
- relay reputation
- retry amplification
- timing randomization
- per-action execution telemetry

Locked interpretation:

TEMPEST Phase A remains a live deterministic multi-relayer execution substrate within a single backend orchestration process.

Engineering[22] strengthened the current substrate without expanding trust boundaries.


### Engineering[22] — Relay Observability Reduction Addendum

Engineering[22] also reduced legacy relay status/health observability.

Public relay status is now coarse only:

- `ok`
- `mode`
- `chainId`

Public relay health is now coarse only:

- `ok`
- `mode`
- `chainId`
- `chainReachable`

Removed from public relay status/health surfaces:

- RPC URL
- registry address
- relayer address
- relayer balance
- latest block

This change did not alter:

- relay execution behavior
- deterministic TEMPEST traversal
- fallback semantics
- frontend behavior
- API consumers
- ZK semantics
- petition semantics
- indexer/read-model semantics

Locked interpretation:

Relay health/status must remain coarse and must not expose relay topology, relayer identity, domain state, fallback path, or infrastructure-specific details.


---

## Engineering[23] — REFLECT Phase A Prepared Path Boundary Checkpoint

Engineering[23] began REFLECT Phase A implementation with a bounded scaffold and boundary-hardening pass.

REFLECT remains the path / witness-data layer.

No architectural expansion was introduced.

No changes were made to:

- M2 identity semantics
- memberSecret / leaf semantics
- nullifier semantics
- petition semantics
- admission semantics
- ZK circuit or proof inputs
- TEMPEST execution semantics
- relay API behavior
- frontend behavior
- SQLite petition read-model authority

### REFLECT path boundary scaffold

A backend REFLECT service boundary was introduced between membership HTTP routes and direct membership path preparation.

The membership route layer now delegates path preparation through:

- `backend/src/services/reflect/preparedPaths.js`

The existing public membership APIs remain unchanged:

- `GET /api/membership/leaf-status?leaf=...`
- `GET /api/membership/path?leaf=...`
- `GET /api/membership/pathByIndex?index=...`

API response semantics were preserved.

Observed behavior remains:

- unenrolled / unknown leaf status returns:
  - `{ "ok": true, "exists": false }`
- missing path returns:
  - `404`
  - `{ "error": "not_found", "details": "leaf not found" }`

### Prepared path boundary hardening

The first REFLECT boundary-hardening slice established a prepared-path layer without introducing distributed behavior.

The prepared-path layer:

- validates path request inputs
- performs bounded indexer sync / retry behavior
- obtains Merkle paths from the existing membership indexer
- normalizes returned path material
- freezes prepared path material before returning it to the route layer

This prevents the HTTP route layer from directly owning path preparation semantics.

### Explicit non-changes

Engineering[23] did not introduce:

- REFLECT mirrors
- chunking
- connector objects
- cover fetches
- mirror fallback
- distributed publication
- adaptive routing
- timing randomization
- request persistence
- path-request history
- path telemetry
- identity tracking
- petition-linked path tracking
- topology discovery

### Validation

Validated during Engineering[23]:

- backend booted cleanly
- `node --check` passed for updated membership route and REFLECT service file
- absent-leaf status endpoint returned expected response
- absent-leaf path endpoint returned expected 404 response
- real ZK signing flow completed successfully through frontend
- signature count incremented correctly
- backend relay submission completed normally

Observed relay success log:

- `[relay] {"event":"submit-ok"}`

### Checkpoint tags

Stable recovery tags:

- `reflect-path-boundary-v1`
- `reflect-prepared-path-boundary-v1`

### Locked interpretation

Engineering[23] established the first REFLECT implementation boundary.

The system now has:

- TEMPEST execution boundary
- REFLECT prepared-path boundary

This creates architectural separation between:

- path / witness-data preparation
- execution / submission

while preserving all locked M2, ZK, petition, admission, read-model, and TEMPEST invariants.

Future REFLECT work must continue from this boundary and must not introduce hidden observability, request tracking, correlation state, or naming surfaces that imply identity, origin, signer, linkage, or provenance.


---

## Engineering[23] — REFLECT Readiness Observability Reduction

Engineering[23] continued with a bounded REFLECT observability-reduction slice.

No architectural expansion was introduced.

No changes were made to:

- M2 identity semantics
- nullifier semantics
- ZK proof semantics
- petition semantics
- admission semantics
- TEMPEST execution semantics
- frontend behavior
- path response shape

### Membership readiness surface reduced

The public membership status endpoint was reduced to a coarse readiness surface.

Current public response shape:

- `ok`
- `ready`
- `depth`

Removed from the public membership status response:

- membership contract address
- RPC URL
- latest synced block
- indexer internals
- root / tree state details

This aligns the membership/path surface with the REFLECT privacy boundary.

### Preserved behavior

Validated behavior remains:

- absent leaf status returns:
  - `{ "ok": true, "exists": false }`
- absent path returns:
  - `404`
  - `{ "error": "not_found", "details": "leaf not found" }`
- real frontend ZK signing flow completed successfully
- signature count updated correctly
- backend relay submission completed normally

Observed relay success log:

- `[relay] {"event":"submit-ok"}`

### Checkpoint tag

Stable recovery tag:

- `reflect-readiness-observability-reduced-v1`

### Locked interpretation

REFLECT path readiness must remain coarse.

Public path-layer surfaces must not expose infrastructure details, tree internals, root freshness details, mirror topology, request history, or any state that can become a correlation aid.


---

## Engineering[23] — REFLECT Internal Envelope Language Checkpoint

Engineering[23] completed the local/internal REFLECT structural phase.

This checkpoint records the transition from a simple prepared-path boundary to a deterministic internal REFLECT object language.

No distributed REFLECT behavior was introduced.

No changes were made to:

- M2 identity semantics
- memberSecret / leaf semantics
- nullifier semantics
- petition semantics
- admission semantics
- ZK circuit or proof inputs
- TEMPEST execution semantics
- relay API behavior
- frontend behavior
- public path response shape
- SQLite petition read-model authority

### Internal prepared-path envelope

REFLECT now wraps prepared path material in an internal envelope before returning the legacy public path body to the membership route layer.

The envelope is internal-only.

It is not exposed to the frontend.

The public membership path endpoint continues to return the same proof-compatible path material expected by the frontend.

### Envelope integrity and coherence metadata

The internal prepared-path envelope now includes deterministic metadata sufficient to support future REFLECT object evolution.

This includes:

- stable internal envelope versioning
- deterministic object typing
- digest algorithm declaration
- deterministic digest material
- coherence metadata for prepared path material

This metadata is used only inside the REFLECT preparation layer.

It does not introduce request tracking, persistence, telemetry, mirrors, chunks, publication, or distributed fetch behavior.

### Internal object language

Engineering[23] established the first internal REFLECT object language primitives:

- envelope version constant
- digest algorithm constant
- internal type registry
- generic internal envelope builder
- prepared-path as the first REFLECT internal object type

This prepares future REFLECT work to add connector/chunk/publication semantics without changing:

- frontend API shape
- proof-generation inputs
- route semantics
- membership indexer authority

### Explicit non-changes

Engineering[23] did not introduce:

- REFLECT mirrors
- distributed publication
- subtree chunking
- connector objects
- cover fetches
- mirror fallback
- adaptive routing
- timing randomization
- request persistence
- path-request history
- path telemetry
- identity tracking
- petition-linked path tracking
- topology discovery

### Validation

Validated during Engineering[23]:

- backend booted cleanly
- `node --check` passed for REFLECT service changes
- forbidden naming / observability searches returned cleanly
- membership readiness endpoint remained coarse
- absent-leaf status endpoint returned expected response
- absent-leaf path endpoint returned expected 404 response
- real frontend ZK signing flow completed successfully after each slice
- signature count updated correctly
- backend relay submission completed normally

Observed relay success logs remained limited to coarse relay success events.

### Checkpoint tags

Stable recovery tags established during Engineering[23]:

- `reflect-path-boundary-v1`
- `reflect-prepared-path-boundary-v1`
- `reflect-readiness-observability-reduced-v1`
- `reflect-prepared-path-envelope-v1`
- `reflect-prepared-path-integrity-v1`
- `reflect-envelope-language-v1`

### Locked interpretation

Engineering[23] completed local/internal REFLECT semantics.

The system now has:

- TEMPEST execution boundary
- REFLECT prepared-path boundary
- REFLECT internal envelope language

This is the natural stopping point before distributed REFLECT semantics.

Future work should treat Engineering[24] as the beginning of distributed REFLECT design/implementation, starting from the internal envelope language established here.


---

## Engineering[24] — REFLECT Local Publication Object Checkpoint

Engineering[24] began the transition from internal REFLECT prepared-path semantics toward publication-ready REFLECT object semantics.

This checkpoint remains local/offline only.

No distributed behavior was introduced.

### Implemented

REFLECT object-language helpers were separated from prepared-path preparation into:

- `backend/src/services/reflect/objectModel.js`

REFLECT object types now include:

- `prepared-path`
- `connector`
- `chunk`

A local publication-object layer was added:

- `backend/src/services/reflect/publicationObjects.js`

This layer supports:

- deterministic chunk envelope construction
- deterministic connector envelope construction
- deterministic local publication object sets
- digest verification across connector/chunk objects
- reconstruction of proof-compatible path material from local publication objects

Canonical prepared-path material normalization was shared through:

- `backend/src/services/reflect/materials.js`

A local validation command was added:

- `npm --prefix backend run reflect:publication:test`

### Checkpoint tags

Stable recovery tags:

- `reflect-object-model-seam-v1`
- `reflect-publication-types-v1`
- `reflect-local-publication-objects-v1`
- `reflect-material-normalization-v1`
- `reflect-publication-validation-script-v1`
- `reflect-publication-verification-test-v1`

### Preserved behavior

No changes were made to:

- M2 identity semantics
- memberSecret / leaf semantics
- nullifier semantics
- petition semantics
- admission semantics
- ZK circuit or proof inputs
- TEMPEST execution semantics
- relay API behavior
- frontend behavior
- SQLite petition read-model authority
- public membership API response shape

The frontend still receives the same proof-compatible prepared-path material.

### Explicit non-changes

Engineering[24] has not introduced:

- REFLECT mirrors
- networking
- distributed fetches
- chunk publication
- connector publication
- cover retrieval
- mirror fallback
- publication persistence
- request persistence
- request telemetry
- topology discovery
- adaptive routing
- timing randomization
- identity tracking
- petition-linked path tracking
- correlation state

### Locked interpretation

This checkpoint defines local publication-ready REFLECT object semantics before distribution exists.

The current progression is:

internal prepared-path envelope
→ generic REFLECT object model
→ local connector/chunk object semantics
→ local integrity verification
→ proof-compatible path reconstruction

Future REFLECT work may integrate these local objects into preparation/publication seams, but must not introduce mirrors, networking, persistence, request tracking, or topology semantics without a separate bounded checkpoint.


---

## Engineering[24] — REFLECT Local Publication Semantics Closeout

Engineering[24] closed with REFLECT local publication-ready object semantics implemented and validated.

This remains a local/internal publication semantics checkpoint.

### Additional completed work

Prepared-path preparation now internally validates through the local REFLECT publication object model:

- prepared path envelope
- local connector/chunk object construction
- connector/chunk integrity verification
- reconstruction into proof-compatible prepared-path material
- unchanged legacy API response

REFLECT serialization boundaries were added:

- `serializeReflectObject(...)`
- `parseReflectObject(...)`

The offline validation script now exercises:

- deterministic local publication object construction
- connector/chunk digest validation
- canonical serialization
- parse boundary
- integrity verification after parse
- reconstruction into proof-compatible material

### Final Engineering[24] checkpoint tags

- `reflect-prepared-path-local-publication-validation-v1`
- `reflect-serialization-boundaries-v1`

### Final locked interpretation

Engineering[24] completed the transition from internal prepared-path envelopes to local publication-ready REFLECT object semantics.

The implemented progression is now:

internal prepared-path envelope
→ generic REFLECT object model
→ local connector/chunk object semantics
→ local integrity verification
→ canonical serialization / parse boundary
→ proof-compatible path reconstruction
→ unchanged public membership API response

No distributed behavior exists yet.

Future Engineering work may begin from this stable local publication boundary, but must introduce mirror-facing, publication, fetch, cover, or topology behavior only as separate bounded checkpoints.


---

## Engineering[25] — REFLECT Local Publication State Checkpoint

Engineering[25] began the publication-facing / mirror-facing seam preparation phase for REFLECT.

This checkpoint remains local-only.

No distributed behavior was introduced.

### Implemented

REFLECT local publication semantics were extended from local connector/chunk object sets into a layered local publication model:

- local publication descriptor
- local publication group
- descriptor-aware local publication verification
- local publication group verification
- local publication state

The resulting local semantic chain is:

prepared path  
→ publication objects  
→ descriptor  
→ publication group  
→ publication group verification  
→ publication state

### Publication descriptor

A local publication descriptor now summarizes a deterministic publication group using:

- envelope version
- root
- depth
- connector digest
- chunk count
- chunk digests
- deterministic content digest

The descriptor is local and integrity-oriented.

It does not expose or imply:

- source
- origin
- ownership
- requester
- topology
- transport route
- persistence location

### Publication group

A local publication group now binds:

- descriptor
- connector
- chunks

as one deterministic local publication unit.

This creates a future insertion seam while preserving current local behavior.

### Publication state

A local publication state now summarizes one or more local publication groups through deterministic entries and a state-level content digest.

This state is:

- local
- deterministic
- non-persistent
- non-networked
- topology-agnostic

It does not introduce mirrors, fetch behavior, routing behavior, publication storage, request history, or observability expansion.

### Verification

Descriptor-aware verification was added so that when a descriptor is present it must match the connector/chunk material.

A local publication group verifier was added as the explicit validation boundary for grouped publication material.

Existing reconstruction semantics remain compatible with connector/chunk verification.

### Invariants preserved

No changes were made to:

- M2 identity semantics
- memberSecret / leaf semantics
- nullifier semantics
- petition semantics
- admission semantics
- ZK circuit or proof inputs
- TEMPEST execution semantics
- relay API behavior
- frontend behavior
- public membership API response shape
- SQLite/read-model authority

### Explicit non-changes

Engineering[25] did not introduce:

- live mirrors
- distributed fetches
- network transport
- adaptive routing
- timing randomization
- peer discovery
- gossip protocols
- reputation systems
- distributed consensus
- persistent request history
- identity-linked telemetry
- petition-linked fetch tracking
- topology exposure
- long-lived correlation state

### Privacy-language discipline

No origin/source/ownership/provenance/requester naming was introduced.

Current neutral REFLECT naming remains centered on:

- material
- object
- descriptor
- connector
- chunk
- group
- state
- coherence
- envelope

Locked interpretation:

Engineering[25] has established local publication-state semantics as the next REFLECT seam after Engineering[24]'s local publication object semantics.

This is a preparation layer only.

Future mirror-facing work must build on this seam without introducing networking, persistence, topology semantics, request telemetry, or correlation state prematurely.


---

## Engineering[25] — REFLECT Local Publication Acceptance Closeout

Engineering[25] completed the local publication-facing seam stack for REFLECT.

This closes the Engineering[25] phase.

### Final Engineering[25] scope

Engineering[25] remained strictly local and deterministic.

It extended REFLECT from Engineering[24]'s local publication object semantics into a complete local publication seam model:

prepared path  
→ publication objects  
→ descriptor  
→ publication group  
→ group verification  
→ publication state  
→ publication state acceptance boundary

### Final implemented seam

A local publication state acceptance boundary was added.

This boundary validates and accepts local publication state shape without introducing runtime distribution.

It is:

- local
- deterministic
- non-persistent
- non-networked
- topology-neutral
- mirror-neutral
- fetch-neutral

### Locked Engineering[25] interpretation

Engineering[25] did not implement mirrors.

Engineering[25] prepared the semantic boundary that future mirror/publication runtime behavior may later use.

The accepted state is a local semantic object only.

It must not be interpreted as:

- published network state
- mirror-held state
- persisted state
- fetchable state
- topology state
- request history
- transport metadata

### Engineering[25] tags

Stable recovery tags added during Engineering[25]:

- reflect-local-publication-descriptor-v1
- reflect-local-publication-group-v1
- reflect-local-publication-group-verification-v1
- reflect-local-publication-state-v1
- reflect-local-publication-state-acceptance-v1
- engineering25-reflect-local-publication-state-checkpoint

### Invariants preserved

No changes were made to:

- M2 identity semantics
- memberSecret / leaf semantics
- nullifier semantics
- petition semantics
- admission semantics
- ZK circuit or proof inputs
- TEMPEST execution semantics
- relay API behavior
- frontend behavior
- public membership API response shape
- SQLite/read-model authority

### Explicit non-changes

Engineering[25] did not introduce:

- live mirrors
- runtime mirror behavior
- distributed fetches
- network transport
- adaptive routing
- timing randomization
- peer discovery
- gossip protocols
- reputation systems
- distributed consensus
- persistent publication state
- persistent request history
- identity-linked telemetry
- petition-linked fetch tracking
- topology exposure
- long-lived correlation state

### Naming / privacy-language discipline

Engineering[25] preserved neutral REFLECT naming.

No origin/source/ownership/provenance/requester terminology was introduced.

Future work must continue treating naming as part of the privacy boundary.

Forbidden naming surfaces include language implying:

- identity
- origin
- source attribution
- ownership
- provenance
- requester identity
- tracking
- linkage
- user affinity

This applies to:

- variables
- helper names
- comments
- tests
- docs
- logs
- serialization fields
- route names

### Engineering[26] boundary

Engineering[26] should begin only after this local semantic seam.

The next category of work is no longer local object semantics.

The next category is likely:

- bounded runtime publication simulation
- local publication-window semantics
- deterministic state selection
- stale-state rejection
- coherence targeting

But Engineering[26] must still begin with observation only.

Engineering[26] must not immediately introduce real mirrors, networking, persistence, topology, request telemetry, or distributed fetch behavior.

Locked interpretation:

Engineering[25] closed the local REFLECT publication seam phase.

Engineering[26] begins only if moving from local publication-state semantics toward bounded runtime publication/window simulation.



---

## Engineering[26] — REFLECT Local Publication Window Semantics

Engineering[26] extended the local REFLECT publication seam with bounded runtime/window semantics.

This checkpoint remains local-only and deterministic.

No architectural expansion was introduced.

No changes were made to:

- M2 identity semantics
- memberSecret / leaf semantics
- nullifier semantics
- petition semantics
- admission semantics
- ZK circuit or proof inputs
- TEMPEST execution semantics
- relay API behavior
- frontend behavior
- public membership API response shape
- SQLite/indexer authority

### Implemented REFLECT local window semantics

Engineering[26] added:

- local publication window construction
- bounded window limit validation
- local publication state acceptance inside the window boundary
- deterministic selected-state semantics
- coherent-state targeting by content digest
- explicit deterministic sequence validation
- prepared-path internal routing through the local publication window
- reconstruction validation after selected-state coherence checks

Current internal REFLECT flow:

prepared path  
→ publication objects  
→ descriptor  
→ publication group  
→ publication state  
→ local publication window  
→ deterministic selected state  
→ coherent-state targeting  
→ sequence validation  
→ reconstruction validation  
→ legacy proof-compatible prepared-path response

### Public/runtime behavior preserved

The frontend still receives the same legacy proof-compatible prepared-path object.

There is still:

- no public connector exposure
- no public chunk exposure
- no public descriptor exposure
- no public group exposure
- no public state exposure
- no public window exposure
- no mirror behavior
- no distributed fetches
- no publication persistence
- no topology semantics
- no request telemetry expansion

### Explicit non-changes

Engineering[26] did not introduce:

- live mirrors
- real distributed fetches
- external network transport
- adaptive routing
- timing randomization
- peer discovery
- gossip protocols
- reputation systems
- distributed consensus
- persistent request history
- identity-linked telemetry
- petition-linked fetch tracking
- topology exposure
- long-lived correlation state

### Checkpoint tags

Stable recovery tags:

- `reflect-local-publication-window-v1`
- `reflect-prepared-path-publication-window-v1`
- `reflect-coherent-publication-selection-v1`
- `reflect-publication-window-sequence-v1`

### Locked interpretation

Engineering[26] defines local runtime/window semantics before any distributed REFLECT infrastructure exists.

The system now has a deterministic, bounded, local publication-window boundary that can reject malformed, incoherent, or sequence-invalid local states without exposing new public surfaces.

Future REFLECT work must continue to preserve:

- local/public API separation
- neutral naming discipline
- no identity/source/provenance/requester language
- no hidden telemetry
- no persistence before explicit design
- no mirrors or network fetches before a separate bounded checkpoint

Engineering[26] status:

**CLOSED — local publication window semantics checkpoint complete**


### Engineering[26] — REFLECT Window Selection Test Coverage Addendum

After the Engineering[26] local publication-window checkpoint, a bounded test-hardening pass was completed.

Additional validation now covers:

- deterministic sequence assignment inside local publication windows
- coherent selected-state success by content digest
- coherent selected-state mismatch rejection
- invalid sequence rejection during local state selection

No runtime semantics changed.

No changes were made to:

- public API behavior
- frontend behavior
- persistence
- networking
- mirror semantics
- topology semantics
- request telemetry

Checkpoint tag:

- `reflect-publication-window-selection-tests-v1`

Locked interpretation:

The local REFLECT window boundary is now both implemented and test-covered for deterministic sequence validation and coherent selected-state targeting.

---

### Engineering[26] — REFLECT Multi-State Local Window Selection Addendum

Engineering[26] added bounded local multi-state publication-window selection semantics.

This is still local-only simulation.

Additional semantics now implemented:

- local publication windows may contain multiple valid accepted states
- generic local selection returns the latest valid window state
- coherent local selection searches backward through the window
- coherent local selection returns the latest state matching the requested content digest
- unmatched coherent targets are rejected
- sequence validation remains enforced before selection

This creates deterministic local state-contention behavior before any distributed REFLECT runtime exists.

No changes were made to:

- public API behavior
- frontend behavior
- membership path response shape
- persistence
- networking
- mirror behavior
- topology semantics
- request telemetry

Checkpoint tag:

- `reflect-coherent-window-selection-v1`

Locked interpretation:

REFLECT now has local multi-state window simulation semantics, but this must not be interpreted as distributed publication, mirror discovery, network ordering, source attribution, or persistence.

Future work must continue to avoid names and structures implying origin, publisher, provider, requester, ownership, provenance, topology, or telemetry.


### Engineering[26] — REFLECT Prepared-Path Reconstruction Fix Addendum

During live end-to-end validation after local publication-window work, a regression was found in the membership path flow.

Observed failure:

- `GET /api/membership/leaf-status?leaf=...` returned `exists: true`
- `GET /api/membership/path?leaf=...` returned `404`
- frontend therefore treated an enrolled identity as not signable

Root cause:

- coherent window selection compared the requested target against the wrong digest layer
- the code used publication descriptor / group content digest where publication-state content digest was required

Correction:

- coherent local state selection now targets the publication-state content digest
- prepared-path reconstruction preserves the legacy proof-compatible fields:
  - `leaf`
  - `index`
  - `root`
  - `siblings`
  - `pathBits`

Validation:

- membership path lookup returned the expected legacy-compatible response keys:
  - `index`
  - `leaf`
  - `pathBits`
  - `root`
  - `siblings`
- full live signing flow was revalidated with both enrolled test wallets
- signature count updated correctly after both signatures
- existing public API behavior remained unchanged

Checkpoint tag:

- `reflect-prepared-path-reconstruction-fix-v1`

Locked lesson:

REFLECT digest comparisons must explicitly respect layer boundaries.

Do not compare across:

- descriptor / group digest
- publication-state digest
- window-entry digest

unless there is an explicit derivation rule and a test covering that comparison.

This class of bug is now treated as a known REFLECT risk: semantic-layer digest confusion.


### Engineering[26] — REFLECT Digest-Layer Regression Coverage Addendum

After the prepared-path reconstruction regression fix, Engineering[26] added explicit regression coverage for semantic-layer digest confusion.

Additional validation now asserts:

- publication group descriptor digest is not equivalent to publication-state digest
- coherent local publication-state selection must target publication-state digest
- descriptor/group digest must not satisfy publication-state coherent selection

This specifically covers the regression class where:

- membership leaf existence remained valid
- but prepared-path reconstruction failed due to incorrect digest-layer targeting

Validation remains local-only and deterministic.

No changes were made to:

- public API behavior
- frontend behavior
- membership path response shape
- persistence
- networking
- mirrors
- topology semantics
- request telemetry

Checkpoint tag:

- `reflect-digest-layer-selection-regression-test-v1`

Locked interpretation:

Digest-layer boundaries are now treated as explicit REFLECT runtime invariants.

Future REFLECT work must avoid implicit equivalence assumptions between:

- descriptor/group digests
- publication-state digests
- window-entry digests

unless an explicit derivation rule and regression coverage exist.


---

## Engineering[27] — TEMPEST Operational Determinism Hardening Checkpoint

Engineering[27] returned to TEMPEST after the Engineering[26] REFLECT local runtime semantic checkpoint.

This was an intentional bounded multiplexing step:

- REFLECT remains the path / witness-data layer
- TEMPEST remains the execution / submission layer
- no simultaneous distributed expansion was introduced

No architectural expansion was introduced.

No changes were made to:

- M2 identity semantics
- ZK proof semantics
- nullifier semantics
- admission semantics
- petition semantics
- frontend behavior
- public relay API shape
- indexer/read-model semantics
- REFLECT semantics

### Hardening completed

Implemented bounded TEMPEST operational-determinism hardening:

- startup validation that every deterministic execution slot resolves to a usable execution domain
- startup validation that configured execution domains target the same registry address
- immutable execution-domain lifecycle objects
- immutable execution-domain array returned from construction
- internal normalized execution-failure classification seam
- regression coverage for deterministic fallback continuation
- regression coverage for invalid execution topology rejection
- regression coverage for immutable execution-domain lifecycle objects

### Naming / observability discipline

This checkpoint preserved strict privacy-language discipline.

No new public surface exposes:

- selected relay slot
- permutation order
- execution domain
- relayer wallet identity
- fallback traversal path
- topology details
- per-action execution history
- domain-specific health
- request-linked execution metadata

Implementation language remains coarse and operational.

No actor, provenance, linkage, signer-origin, or correlation terminology was introduced.

### Validation

Validated during Engineering[27]:

- backend source checks passed
- TEMPEST regression script passed
- backend booted cleanly
- relay status remained coarse:
  - ok
  - mode
  - chainId
- relay health remained coarse:
  - ok
  - mode
  - chainId
  - chainReachable
- petition indexer remained healthy
- live UI signing flow succeeded
- backend relay log remained coarse:
  - submit-ok
- no topology, slot, domain, relayer, fallback, permutation, or traversal detail appeared in public API output or relay logs

### Locked interpretation

TEMPEST Phase A remains:

- deterministic
- topology-hidden
- single-backend orchestrated
- live multi-relayer capable
- operationally hardened
- frontend/API compatible

This checkpoint strengthens deterministic execution semantics before any future distributed operational expansion.

It does not introduce:

- relay federation
- remote relay APIs
- relay mesh coordination
- inter-relayer communication
- dynamic topology discovery
- adaptive routing
- relay reputation
- timing randomization
- public relay topology
- per-action execution telemetry

Engineering[27] status:

**TEMPEST operational-determinism hardening checkpoint complete**

---

## Engineering[27] — TEMPEST Failure/Fallback Semantics Alignment

Engineering[27] continued with a bounded TEMPEST failure/fallback semantics alignment pass.

No architectural expansion was introduced.

No changes were made to:

- M2 identity semantics
- ZK proof semantics
- nullifier semantics
- admission semantics
- petition semantics
- frontend behavior
- public relay API shape
- indexer/read-model semantics
- REFLECT semantics

### Issue corrected

The implementation previously classified execution failures but still continued fallback traversal for all thrown errors.

This was too permissive relative to the TEMPEST failure/fallback design.

Design rule restored:

- fallback is for operational execution failure
- fallback is not for semantic invalidity

### Runtime behavior aligned

Fallback now continues only for:

- controlled operational failure
- transport failure

Fallback now hard-stops for:

- contract revert
- semantic invalidity
- unclassified execution failure

### Regression coverage added

TEMPEST execution regression coverage now verifies:

- transport failure continues traversal
- controlled operational failure continues traversal
- contract revert stops traversal
- unclassified execution failure stops traversal
- invalid execution topology is rejected
- execution-domain lifecycle objects remain immutable

### Observability preserved

No new public or persistent observability was introduced.

No public output or relay log exposes:

- selected relay slot
- permutation order
- execution domain
- relayer wallet identity
- fallback traversal path
- topology details
- per-action execution history
- domain-specific health
- request-linked execution metadata

Live validation confirmed:

- sign loop still works
- relay log remained coarse:
  - submit-ok

### Locked interpretation

TEMPEST fallback semantics are now aligned across:

- design documentation
- runtime behavior
- regression coverage
- public observability policy

This checkpoint preserves TEMPEST as a deterministic operational execution layer and avoids treating semantic invalidity as relay failure.

Engineering[27] status:

**TEMPEST failure/fallback semantics alignment complete**

---

## Engineering[27] — TEMPEST Unknown-State Reconciliation Checkpoint

Engineering[27] continued with a bounded TEMPEST unknown-state handling pass.

No architectural expansion was introduced.

No changes were made to:

- M2 identity semantics
- ZK proof semantics
- nullifier semantics
- admission semantics
- petition semantics
- frontend behavior
- public relay API shape
- indexer/read-model semantics
- REFLECT semantics

### Issue addressed

The TEMPEST failure/fallback design requires uncertain execution state to be reconciled before continuing fallback.

Design rule:

- if execution outcome is uncertain, check action state
- if the nullifier is already recorded, treat the action as accepted
- otherwise continue deterministic fallback

### Runtime behavior implemented

After retryable execution failure only:

- TEMPEST checks `hasSignedPetition(petitionId, nullifier)` through the current execution handle
- if already recorded, execution returns a success-shaped result with `txHash: null`
- if not recorded, deterministic fallback traversal continues
- terminal failures still hard-stop

Fallback remains allowed only for:

- controlled operational failure
- transport failure

Fallback remains disallowed for:

- contract revert
- semantic invalidity
- unclassified execution failure

### Regression coverage added

TEMPEST regression coverage now verifies:

- retryable failure plus recorded action returns success-shaped result
- retryable failure plus unrecorded action continues traversal
- terminal failure behavior remains unchanged

### Observability preserved

No new public or persistent observability was introduced.

No public output or relay log exposes:

- selected relay slot
- permutation order
- execution domain
- relayer wallet identity
- fallback traversal path
- topology details
- per-action execution history
- domain-specific health
- request-linked execution metadata

Validation confirmed:

- TEMPEST regression script passed
- relay status remained coarse
- relay health remained coarse
- petition indexer remained healthy
- frontend correctly remained governed by M2 identity state

### Locked interpretation

TEMPEST now handles uncertain execution state by reconciling action state, not by exposing or persisting execution-path state.

This preserves deterministic fallback semantics while avoiding duplicate submission amplification.

Engineering[27] status:

**TEMPEST unknown-state reconciliation checkpoint complete**

---

## Engineering[27] — TEMPEST Response Surface Normalization

Engineering[27] performed a bounded TEMPEST response-surface normalization pass.

No architectural expansion was introduced.

No changes were made to:

- M2 identity semantics
- ZK proof semantics
- nullifier semantics
- admission semantics
- petition semantics
- frontend behavior
- public relay status/health shape
- indexer/read-model semantics
- REFLECT semantics

### Issue addressed

Unknown-state reconciliation can internally return a success-shaped execution result without a transaction hash.

The public relay response must not expose this as a distinct execution-path category.

### Runtime behavior

The relay sign route now returns:

- `ok`
- `alreadySigned`

and includes:

- `txHash`

only when a transaction hash is present.

No new public flag or status was introduced.

Specifically, the route does not expose:

- reconciled state
- selected relay slot
- permutation order
- execution domain
- relayer wallet identity
- fallback traversal path
- topology details
- per-action execution history
- domain-specific health
- request-linked execution metadata

### Validation

Validated during Engineering[27]:

- relay route syntax check passed
- TEMPEST regression script passed
- relay status remained coarse
- relay health remained coarse
- petition indexer remained healthy

### Locked interpretation

Internal execution uncertainty handling must not become a public semantic category.

Public relay success remains protocol-level success, independent of internal execution-path detail.

Engineering[27] status:

**TEMPEST response surface normalization complete**

---

## Engineering[28] — Secret Continuity UX Checkpoint

Engineering[28] performed a bounded secret-continuity UX pass.

No architectural, cryptographic, backend, relay, REFLECT, TEMPEST, storage-key, or recovery-semantics changes were introduced.

### Continuity copy hardening

Updated frontend M2 copy to distinguish:

- local secret presence
- enrolled membership state
- browser-local continuity state

from identity existence or account recovery.

The UI now avoids language implying:

- wallet-based identity
- backend recovery
- account recovery
- centralized continuity authority
- identity loss when browser storage is missing

Locked interpretation preserved:

- continuity = possession of the same `memberSecret`
- browser storage loss is local continuity loss only
- importing the original secret restores continuity
- creating a new secret creates a different identity

Checkpoint tag:

- `secret-continuity-copy-v1`

### M2 panel readability cleanup

The M2 status / continuity panel styling was updated for readability:

- improved contrast
- larger text
- cleaner spacing
- theme-aligned panel styling
- less warning-like yellow/orange presentation

No copy semantics or runtime behavior changed.

Checkpoint tag:

- `secret-continuity-panel-readability-v1`

### Invariants preserved

No changes to:

- Position A identity model
- `memberSecret -> leaf -> nullifier`
- O0 / O1 / O2 state semantics
- localStorage key structure
- import / export / create semantics
- enrollment flow
- signing flow
- ZK circuit
- backend path lookup
- TEMPEST execution
- REFLECT path boundary

Engineering[28] status:

**PARTIAL CHECKPOINT — secret continuity UX clarified; no recovery semantics introduced**


### Engineering[28] — Secret Import / Export Ergonomics Addendum

Engineering[28] completed a final bounded import/export ergonomics pass.

Changes:

- added clearer import/export labels
- improved secret textarea readability
- added explicit offline custody reminder after export
- clarified invalid import error wording

No changes were made to:

- secret format
- storage keys
- import/export semantics
- identity model
- enrollment flow
- signing flow
- backend behavior
- recovery semantics

Checkpoint tag:

- `secret-continuity-import-export-ergonomics-v1`

Locked interpretation:

This is an operator UX improvement only.  
It does not introduce encrypted bundles, account recovery, wallet-based recovery, backend custody, or centralized continuity.

Engineering[28] status:

**CLOSED — secret continuity UX pass complete**


---

## Engineering[29] — Encrypted Continuity Bundle Design

Engineering[29] begins a design-only phase for encrypted portable continuity custody.

No runtime implementation is introduced by this checkpoint.

### Objective

Introduce a future encrypted export/import format for operator-controlled custody of the M2 `memberSecret`, while preserving the locked Position A identity model:

- continuity = possession of the same `memberSecret`
- wallet ≠ identity
- backend ≠ custodian
- relay ≠ memory
- encrypted custody ≠ account recovery

### Bundle semantics

An encrypted continuity bundle is only:

- portable encrypted custody material
- manually exported/imported by the operator
- decrypted locally in the browser
- useful only if the operator knows the bundle password

It is not:

- an account
- a wallet backup
- a recovery phrase
- a cloud sync object
- a backend-restorable identity
- a continuity authority

### Bundle contents

The encrypted payload may contain:

- `memberSecret`

The plaintext envelope may contain only decryption-required fields:

- format marker
- format version
- encryption algorithm
- KDF algorithm/settings
- salt
- nonce/iv
- ciphertext

### Explicit non-contents

The bundle must not contain:

- wallet address
- leaf
- nullifier
- petition IDs
- petition history
- enrollment status
- admission commitment
- admission secret
- relay metadata
- TEMPEST metadata
- REFLECT metadata
- timestamps unless strictly required
- browser/device identifiers
- request history
- topology information

### Metadata policy

Default rule:

- minimize plaintext metadata
- include only fields required for deterministic local decryption
- do not include operator, wallet, identity, device, petition, relay, mirror, or enrollment context

### Cryptographic direction

Future implementation should use browser-local Web Crypto only.

Preferred initial shape:

- password-derived key
- random salt
- random nonce/iv
- authenticated encryption
- encrypted JSON payload containing only `memberSecret`

Exact KDF and parameter selection must be finalized before implementation.

### Naming discipline

Allowed framing:

- encrypted continuity bundle
- encrypted local custody
- import encrypted bundle
- export encrypted bundle
- password-protected bundle

Forbidden framing:

- account recovery
- wallet recovery
- restore account
- recovery phrase
- seed phrase
- cloud backup
- identity provider
- backend recovery
- server custody

### Implementation boundary

Implementation is deferred until after this design checkpoint is reviewed.

Future implementation must remain frontend-only unless STATE.md is explicitly updated.

No backend route, relay behavior, contract behavior, ZK circuit, nullifier model, membership path model, TEMPEST behavior, or REFLECT behavior is changed by this design.


---

## Engineering[29] — Encrypted Continuity Bundle Cryptographic Profile

Engineering[29] selected the initial cryptographic profile for future encrypted continuity bundles.

This is still design-only. No runtime implementation is introduced by this checkpoint.

### Threat model

The encrypted continuity bundle defends against:

- accidental exposure of exported custody material
- theft or copying of an exported bundle file
- offline password guessing attempts against that bundle

It does not defend against:

- compromised browser/runtime
- malware/keyloggers
- weak operator password choice
- operator sharing the password
- backend custody failure, because no backend custody exists
- wallet compromise, because wallet is not the identity primitive

### Initial cryptographic profile

Future implementation should use:

- KDF: PBKDF2-HMAC-SHA256
- derived key size: 256 bits
- encryption: AES-GCM-256
- salt: random 16 bytes minimum
- nonce/IV: random 12 bytes
- initial PBKDF2 iteration target: fixed profile in the low-to-mid hundreds of thousands
- preferred starting value for implementation review: `400000`

### Iteration policy

The PBKDF2 iteration count must be stored in the plaintext bundle envelope.

The iteration count is not secret.

The system must not rely on hiding KDF parameters.

The implementation must not auto-tune iteration count per device or browser.

Reason:

- deterministic import/export behavior is preferred
- bundle compatibility must remain stable
- device-specific tuning risks inconsistent UX and fingerprint-like behavior
- future parameter upgrades should be handled by explicit version/profile changes

### Password policy

Bundle security depends materially on operator password quality.

The bundle format must not imply that encryption compensates for a weak password.

UX copy should say password-protected custody, not recovery.

### Envelope compatibility

The plaintext envelope must include enough cryptographic metadata for deterministic local decryption:

- format marker
- version
- KDF name
- KDF hash
- KDF iterations
- salt
- cipher name
- IV/nonce
- ciphertext

Future changes to KDF, cipher, parameters, or payload encoding must be represented by explicit version/profile changes.

### Implementation boundary

Implementation remains deferred.

The next safe implementation slice, when chosen, should be a small frontend-only crypto helper with tests or browser-console validation before UI integration.


---

## Engineering[29] — Encrypted Continuity Helper Validation Checkpoint

Engineering[29] implemented and manually validated an isolated frontend-only encrypted continuity bundle helper.

Implementation file:

- `frontend/src/continuityBundle.js`

The helper provides:

- `encryptContinuityBundle(memberSecret, password)`
- `decryptContinuityBundle(bundleText, password)`

Implementation properties:

- frontend/browser only
- WebCrypto only
- PBKDF2-HMAC-SHA256
- AES-GCM-256
- fixed initial PBKDF2 iteration count: `400000`
- random 16-byte salt
- random 12-byte IV
- JSON envelope
- encrypted payload contains only normalized `memberSecret`
- no localStorage mutation
- no UI integration
- no backend interaction
- no wallet semantics

Manual validation completed:

- decimal secret encrypt/decrypt roundtrip succeeded
- `0x` hex secret input normalized to decimal on decrypt
- wrong password failed with bounded helper error
- malformed JSON failed with bounded helper error
- generated bundle envelope contained no wallet address, leaf, nullifier, petition history, enrollment status, relay metadata, TEMPEST metadata, REFLECT metadata, device identifier, or browser identifier

Build validation:

- `node --check frontend/src/continuityBundle.js` passed
- `npm --prefix frontend run build` passed

No changes were made to:

- existing plaintext import/export UI
- `m2Identity.js` localStorage behavior
- backend routes
- relay behavior
- contract behavior
- ZK circuit
- nullifier model
- membership path model
- TEMPEST behavior
- REFLECT behavior

Locked interpretation:

This checkpoint introduces an isolated crypto primitive only.

Encrypted bundle UI wiring remains a separate future slice.


---

## Engineering[30] — Encrypted Continuity UI Integration

Engineering[30] integrated encrypted continuity bundles into the existing M2 identity/operator UI.

No architectural expansion was introduced.

Implemented:

- encrypted continuity bundle export UI
- encrypted continuity bundle import UI
- plaintext secret import/export preserved
- existing O0/O1/O2 state semantics preserved
- existing `m2Identity.js` storage semantics preserved
- encrypted import decrypts first, then calls the existing `importMemberSecret(...)` path
- encrypted export uses the existing `exportMemberSecret(...)` path before encryption

Checkpoint tags:

- `encrypted-continuity-export-ui-v1`
- `encrypted-continuity-import-ui-v1`

Validation:

- frontend production build passed
- manual encrypted export/import roundtrip completed
- wrong-password import failure handled cleanly
- working tree clean after commit/tag/push

Locked interpretation:

Encrypted continuity bundles are a password-protected custody format for the current `memberSecret`.

They are not:

- an account
- a wallet backup
- a recovery phrase
- a cloud backup
- a backend continuity service
- an identity authority

Continuity remains defined only as possession of the same original `memberSecret`.

No changes were made to:

- ZK circuits
- proof semantics
- nullifier semantics
- membership semantics
- enrollment semantics
- backend routes
- contracts
- TEMPEST
- REFLECT

Engineering[30] status:

**CLOSED — encrypted continuity UI integration complete**

---

## Engineering[31] — Continuity Custody Semantic Hardening

Engineering[31] hardened M2 continuity and custody semantics without changing protocol behavior or runtime identity rules.

This phase focused on:

- continuity-language tightening
- operator expectation hardening
- anti-recovery semantic discipline
- encrypted continuity bundle interpretation stability
- prevention of accidental account-style framing

Implemented:

- tightened UI copy around local secret replacement semantics
- removed “restore/recovery/restoration” continuity phrasing from active UX surfaces
- clarified that continuity exists only with the same original `memberSecret`
- clarified encrypted bundle semantics as encrypted local custody only
- clarified that bundle import only sets the active local secret using existing import semantics
- clarified replacement semantics around switching away from an active anonymous membership
- tightened developer-facing mismatch diagnostics to avoid recovery framing
- removed “recoverable” wording from pending admission flow comments
- added `docs/CONTINUITY_CUSTODY_MODEL_V1.md` as the bounded continuity/custody supporting specification

No changes were made to:

- M2 cryptographic semantics
- nullifier derivation
- enrollment semantics
- contract behavior
- TEMPEST
- REFLECT
- relay behavior
- backend authority model
- wallet semantics

Locked continuity interpretation remains:

continuity = possession of the same original `memberSecret`

The encrypted continuity bundle remains:

portable encrypted custody

NOT:

- an account
- a recovery phrase
- a cloud backup
- a synced identity
- a backend authority
- a continuity authority
- a wallet recovery mechanism

This phase further established wording and operator expectations as part of the privacy boundary.

Checkpoint artifacts:

- `docs/CONTINUITY_CUSTODY_MODEL_V1.md`

Suggested checkpoint tag:

- `continuity-custody-semantics-v1`


---

## Engineering[31] — M2 Local Secret Naming Tightening

Engineering[31] performed a second bounded semantic-tightening pass on `frontend/src/m2Identity.js`.

No runtime logic changed.

The pass tightened source-level wording around the local M2 secret surface:

- “active anonymous identity” was replaced with “active local M2 secret”
- “secret is the identity primitive” was tightened to “memberSecret is the M2 membership primitive”
- legacy compatibility comments now preserve “local secret continuity” rather than “local identity”
- the duplicate-create error now says creating a new secret replaces the active local secret and switches away from the current anonymous membership

This preserves the locked Position A interpretation:

continuity = possession of the same original `memberSecret`

No changes were made to:

- localStorage key structure
- import/export behavior
- encrypted continuity bundles
- O0/O1/O2 semantics
- proof generation
- nullifier semantics
- backend behavior
- TEMPEST
- REFLECT


---

## Engineering[31] — Legacy Petition List Copy Alignment

Engineering[31] performed a final bounded copy/comment alignment pass on `frontend/src/Petitions.jsx`.

No runtime logic changed.

The pass corrected stale wording around the older petition-list M2 surface:

- local secret storage is described as wallet-keyed MVP browser handling, not wallet-derived identity
- membership path loading is described as derived-leaf based, not wallet based
- membership-path unavailable copy now refers to the active local secret being enrolled, not enrollment “for this wallet”

This preserves the locked M2 rule:

`memberSecret -> leaf -> nullifier`

and avoids reintroducing wallet-continuity semantics through legacy comments or fallback UI copy.

---

## Engineering[33] — REFLECT Publication-State Semantic Hardening

Engineering[33] performed a bounded REFLECT documentation hardening pass focused on publication-state lifecycle semantics.

No runtime behavior changed.

No code changed.

No REFLECT infrastructure expansion was introduced.

No distributed mirror deployment semantics were introduced.

### Hardened semantics

The REFLECT docs now clarify that:

- mirrors are replaceable publication surfaces, not authorities
- publication-state validity is client-derived
- a publication state is a coherent lifecycle boundary
- connector/chunk coherence is required for object acceptance
- fallback replaces mirror, not publication state
- fallback must not trigger adaptive reselection
- cross-state reconstruction remains forbidden
- digest-layer boundaries remain explicit
- topology-aware client behavior remains forbidden

### Clarified authority boundary

REFLECT validity now resolves through:

`client-derived coherent publication-state verification`

not:

`mirror exposure, mirror freshness, mirror preference, routing authority, topology authority, or federation consensus`

### Files updated

- `docs/reflect/REFLECT_OVERVIEW_V1.md`
- `docs/reflect/REFLECT_STATE_VALIDITY_V1.md`
- `docs/reflect/REFLECT_SELECTION_POLICY_V1.md`
- `docs/reflect/REFLECT_FAILURE_AND_FALLBACK_V1.md`
- `docs/reflect/REFLECT_OBJECT_MODEL_V1.md`
- `docs/reflect/REFLECT_PUBLICATION_WINDOW_V1.md`

### Invariants preserved

No changes to:

- M2 identity semantics
- memberSecret / leaf / nullifier semantics
- ZK circuit
- petition semantics
- admission semantics
- TEMPEST execution semantics
- backend route behavior
- frontend behavior
- REFLECT runtime behavior

Engineering[33] status:

**REFLECT publication-state semantic hardening complete**

---

### Engineering[33] — REFLECT Publication-State Acceptance Runtime Alignment

After the REFLECT publication-state semantic hardening checkpoint, Engineering[33] performed a bounded implementation-surface observation pass.

A small runtime alignment was added to the local REFLECT publication-state acceptance boundary.

Implemented:

- `acceptLocalPublicationState(...)` now verifies that the publication-state content digest matches the digest recomputed from accepted state entries
- state entries must carry descriptor-linked content digests
- entry content digests must match descriptor content digests
- malformed or tampered publication-state digests are rejected

Regression coverage:

- `publicationObjects.test.js` now rejects a tampered publication-state digest

Validation:

- `node --check backend/src/services/reflect/publicationObjects.js`
- `node --check backend/src/services/reflect/publicationObjects.test.js`
- `node backend/src/services/reflect/publicationObjects.test.js`
- `node backend/src/services/reflect/publicationWindows.test.js`

No infrastructure expansion was introduced.

No mirrors, distributed fetches, topology behavior, adaptive routing, request telemetry, or public API changes were introduced.

This aligns the local runtime acceptance boundary with the Engineering[33] rule:

`publication-state validity is client-derived coherent verification, not object exposure`

---

### Engineering[33] — REFLECT Publication-Window Ordering Runtime Alignment

Engineering[33] performed a bounded runtime hardening pass on local REFLECT publication-window selection semantics.

Implemented:

- `selectLocalPublicationState(...)` now selects by explicit highest deterministic sequence entry
- selection no longer relies on implicit array-tail interpretation
- existing sequence validation remains mandatory before selection
- reversed or sequence-invalid windows are rejected before selection

Regression coverage:

- `publicationWindows.test.js` now asserts reversed window entry order is rejected

Validation:

- `node --check backend/src/services/reflect/publicationWindows.js`
- `node --check backend/src/services/reflect/publicationWindows.test.js`
- `node backend/src/services/reflect/publicationWindows.test.js`
- `node backend/src/services/reflect/publicationObjects.test.js`

No public API behavior changed.

No mirrors, distributed fetches, topology behavior, adaptive routing, request telemetry, or infrastructure expansion were introduced.

This aligns local runtime behavior with the Engineering[33] rule:

`highest recent valid publication state = highest valid state by deterministic publication-window ordering`


---

### Engineering[35] — REFLECT Local Acquisition Boundary

Engineering[35] introduced the first bounded REFLECT acquisition-boundary slice.

This is a local/runtime boundary only.

Implemented:

- `backend/src/services/reflect/acquisition.js`
- `backend/src/services/reflect/acquisition.test.js`
- prepared-path flow now routes through:
  - selected publication state
  - local acquisition plan
  - local publication acquisition
  - reconstruction

The implemented flow is now:

`publication-state selection -> acquisition planning -> acquisition validation -> reconstruction`

### Acquisition boundary semantics

The acquisition plan records the selected publication-state digest before acquisition occurs.

This preserves the rule:

`acquisition may retrieve material for a selected state; it may not choose semantic truth`

The acquisition layer now validates:

- selected-state digest presence
- object count consistency
- acquisition object ordering
- descriptor/content-digest coherence
- mismatched publication material rejection

### Explicit non-goals

Engineering[35] did not introduce:

- mirrors
- network fetches
- distributed retrieval
- topology behavior
- adaptive routing
- fallback traversal
- request telemetry
- persistence
- frontend/public API changes

### Preserved invariants

- selected publication-state identity remains fixed during acquisition
- acquisition does not mutate state selection
- acquisition does not trigger adaptive reselection
- acquisition does not treat runtime availability as validity
- reconstruction remains coherent-state-bound
- cross-state reconstruction remains forbidden
- mirrors remain future replaceable publication surfaces, not authorities

### Checkpoint tags

- `reflect-local-acquisition-boundary-v1`
- `reflect-acquisition-plan-validation-v1`

Engineering[35] status:

**REFLECT local acquisition boundary established and acquisition-plan validation hardened**

---

### Engineering[35] — REFLECT Acquisition Lifecycle Result Semantics

Engineering[35] extended the local REFLECT acquisition boundary with explicit acquisition lifecycle result semantics.

Implemented:

- acquisition now returns explicit structured lifecycle results
- acquisition success and acquisition failure are separated explicitly
- acquisition failure reasons are deterministic and bounded
- prepared-path reconstruction now consumes successful acquisition results only

The acquisition lifecycle surface now distinguishes:

`semantic acquisition failure`

from:

`coherent acquired publication material`

### Acquisition result semantics

`acquireLocalPublicationGroup(...)` now returns:

- `{ ok: true, publication }`
- `{ ok: false, reason }`

Current bounded acquisition failure reasons include:

- `invalid-plan`
- `invalid-publication`
- `invalid-selected-state`
- `invalid-objects`
- `object-count-mismatch`
- `unsupported-object-count`
- `invalid-sequence`
- `invalid-target`
- `content-digest-mismatch`

### Architectural effect

This establishes the first explicit REFLECT acquisition lifecycle boundary.

The acquisition layer now has:

- deterministic acquisition result semantics
- bounded acquisition failure classification
- explicit separation between acquisition/runtime failure and semantic reconstruction validity

This prepares future bounded runtime traversal/fallback work without introducing topology authority or adaptive semantics.

### Explicit non-goals

Engineering[35] still did not introduce:

- mirrors
- network retrieval
- distributed fetches
- fallback traversal
- adaptive routing
- topology awareness
- request telemetry
- infrastructure orchestration
- frontend/public API changes

### Preserved invariants

- acquisition does not mutate selected publication-state identity
- acquisition failure does not trigger adaptive reselection
- runtime acquisition availability does not define semantic validity
- reconstruction remains coherent-state-bound
- cross-state reconstruction remains forbidden

### Checkpoint tag

- `reflect-acquisition-result-shape-v1`

Engineering[35] status:

**REFLECT acquisition lifecycle result semantics established**

---

### Engineering[35] — REFLECT Acquisition Traversal Order

Engineering[35] added explicit deterministic traversal ordering to the local REFLECT acquisition plan.

Implemented:

- acquisition objects now carry deterministic acquisition keys
- acquisition plans now expose `traversalOrder`
- traversal order is validated during local acquisition
- malformed or mismatched traversal order is rejected

This establishes a local traversal-order seam before any distributed runtime traversal exists.

### Explicit non-goals

This did not introduce:

- mirrors
- network fetches
- fallback traversal
- distributed acquisition
- topology behavior
- adaptive routing
- public API changes

### Preserved invariant

Traversal order is runtime acquisition structure only.

It does not define publication-state validity, does not mutate selected-state identity, and does not grant acquisition/runtime behavior semantic authority.

### Checkpoint tag

- `reflect-acquisition-traversal-order-v1`

---

### Engineering[35] — REFLECT Acquisition Lifecycle Steps

Engineering[35] added explicit deterministic lifecycle steps to the local REFLECT acquisition result surface.

Implemented:

- successful acquisition now records bounded completed steps
- failed acquisition returns completed steps up to the failure point
- acquisition lifecycle progression is deterministic and local-only

Current successful local acquisition lifecycle:

`plan-accepted -> publication-accepted -> selected-state-validated -> publication-acquired`

This prepares future bounded traversal/fallback work by giving acquisition a deterministic continuation/stopping surface before any distributed runtime exists.

### Explicit non-goals

This did not introduce:

- mirrors
- network fetches
- distributed acquisition
- fallback traversal
- adaptive routing
- topology exposure
- request telemetry
- frontend/public API changes

### Preserved invariant

Lifecycle steps describe runtime acquisition progress only.

They do not define semantic validity, do not mutate selected publication-state identity, and do not grant acquisition/runtime behavior authority over publication-state selection.

### Checkpoint tag

- `reflect-acquisition-lifecycle-steps-v1`

---

### Engineering[35] — REFLECT Acquisition Orchestration Extraction

Engineering[35] extracted local REFLECT acquisition orchestration out of prepared-path handling and into the acquisition layer.

Implemented:

- `acquirePreparedPathPublication(...)`
- prepared-path flow now delegates publication-state selection, acquisition-plan construction, and local publication acquisition to the acquisition boundary
- `preparedPaths.js` now remains focused on envelope preparation and reconstruction validation

This creates a cleaner insertion point for future bounded traversal/fallback work.

### Explicit non-goals

This did not introduce:

- mirrors
- network retrieval
- distributed fetches
- fallback traversal
- adaptive routing
- topology exposure
- request telemetry
- frontend/public API changes

### Preserved invariant

Acquisition orchestration remains local/runtime-only.

It does not define semantic validity, does not mutate selected publication-state identity, and does not grant runtime acquisition behavior authority over publication-state selection.

### Checkpoint tag

- `reflect-acquisition-orchestration-v1`

---

### Engineering[35] — REFLECT Acquisition Traversal Seam

Engineering[35] added the first explicit local traversal execution seam inside the REFLECT acquisition layer.

Implemented:

- `acquireTraversalTarget(...)`
- traversal target validation separated from local publication acquisition
- successful acquisition lifecycle now records:
  - `traversal-group-1-completed`
- acquisition still supports only the current local single-group path

This creates a bounded insertion point for future traversal/fallback work without changing semantic validity rules.

### Explicit non-goals

This did not introduce:

- mirrors
- network retrieval
- distributed fetches
- fallback traversal
- adaptive routing
- topology exposure
- request telemetry
- frontend/public API changes

### Preserved invariant

Traversal execution remains local/runtime-only.

It does not define publication-state validity, does not mutate selected publication-state identity, and does not grant traversal behavior authority over semantic selection.

### Checkpoint tag

- `reflect-acquisition-traversal-seam-v1`

---

### Engineering[36] — REFLECT Traversal Attempt Records

Engineering[36] added explicit deterministic traversal attempt records to the local REFLECT acquisition layer.

Implemented:

- acquisition results now include bounded traversal attempt records
- traversal attempts record deterministic `traversalKey`
- successful local traversal records:
  - `started`
  - `succeeded`
- successful acquisition still remains local and single-target only

This establishes a local attempt-record surface before any fallback continuation or distributed retrieval exists.

### Explicit non-goals

This did not introduce:

- mirrors
- network retrieval
- distributed fetches
- fallback traversal
- adaptive routing
- topology exposure
- request telemetry
- frontend/public API changes

### Preserved invariant

Traversal attempts describe local runtime progress only.

They do not define publication-state validity, do not mutate selected publication-state identity, and do not grant traversal or availability semantics authority over REFLECT selection.

### Checkpoint tag

- `reflect-traversal-attempt-records-v1`

---

### Engineering[36] — REFLECT Failed Traversal Attempt Records

Engineering[36] extended local REFLECT traversal attempt records to include deterministic failed-attempt outcomes.

Implemented:

- traversal attempts now record failed outcomes
- failed attempts include bounded failure reasons
- content-digest mismatch now records:
  - `started`
  - `failed`
- successful traversal attempt semantics remain unchanged

This establishes deterministic local attempt outcome recording before any fallback continuation exists.

### Explicit non-goals

This did not introduce:

- mirrors
- network retrieval
- distributed fetches
- fallback traversal
- adaptive routing
- topology exposure
- request telemetry
- frontend/public API changes

### Preserved invariant

Failed traversal attempts describe runtime acquisition progress only.

They do not define publication-state validity, do not mutate selected publication-state identity, and do not grant traversal/fallback behavior authority over REFLECT selection.

### Checkpoint tag

- `reflect-failed-traversal-attempt-records-v1`

---

### Engineering[36] — REFLECT Bounded Local Continuation Execution

Engineering[36] added the first bounded local continuation execution path inside the REFLECT acquisition layer.

Implemented:

- optional `continuationPublication` input
- continuation execution only after a continuation-eligible local acquisition failure
- continuation eligibility remains limited to:
  - `content-digest-mismatch`
- continuation performs exactly one additional local traversal attempt
- continuation uses:
  - the same acquisition plan
  - the same selected publication-state
  - the same traversal target
  - the same traversal key
- successful continuation records:
  - `continuation-executed`
  - `traversal-group-1-completed`
  - `publication-acquired`
- continuation result records:
  - `eligible: true`
  - original failure `reason`
  - `executed: true`

The continuation path was deliberately implemented by cloning lifecycle arrays before the continuation branch.

This preserves acquisition-result immutability and prevents continuation execution from mutating already-finalized failure state.

### Explicit non-goals

This did not introduce:

- live distributed mirrors
- network retrieval
- distributed fetches
- adaptive fallback
- selected publication-state reselection
- topology-aware runtime behavior
- mirror freshness authority
- public acquisition APIs
- frontend topology awareness
- cache/replay systems
- retry amplification
- probabilistic retrieval

### Preserved invariant

Bounded continuation execution is local runtime behavior only.

It does not define publication-state validity, does not mutate selected publication-state identity, and does not grant traversal/fallback behavior authority over REFLECT selection.

Continuation execution remains:

- deterministic
- single-attempt
- topology-neutral
- selected-state-preserving
- local-only

Future distributed REFLECT work must attach to this boundary without changing these semantics unless STATE.md is explicitly updated first.

### Checkpoint tag

- `reflect-bounded-local-continuation-v1`


---

### Engineering[37] — REFLECT Retrieval Substitution Semantics

Engineering[37] performed a bounded REFLECT mirror-facing semantic hardening pass.

Implemented:

- tightened `availability` wording in REFLECT state-validity semantics
- replaced loose retry language with bounded deterministic retrieval-substitution language
- clarified that fallback remains selected-state-preserving
- clarified that mirror availability or responsiveness does not define semantic validity

No runtime behavior changed.

No distributed REFLECT implementation was introduced.

No mirrors, network retrieval, topology behavior, adaptive routing, request telemetry, cache/replay systems, or frontend/public API changes were introduced.

Preserved invariants:

- publication-state validity remains client-derived
- selected publication-state identity remains fixed during acquisition/fallback
- fallback is bounded deterministic object-retrieval substitution only
- mirror availability does not become semantic authority
- mirror responsiveness does not become state preference
- runtime acquisition behavior does not define semantic validity
- cross-state reconstruction remains forbidden
- mirrors remain replaceable publication surfaces, not authorities

Checkpoint:

- `reflect-retrieval-substitution-semantics-v1`

Engineering[37] status:

**REFLECT retrieval-substitution semantic hardening complete**

---

### Engineering[37] — REFLECT Fetch Policy Runtime Boundary

Engineering[37] performed a bounded REFLECT fetch-policy semantic hardening pass.

Implemented:

- clarified that fetch execution is runtime retrieval structure only
- clarified that fetch behavior remains subordinate to the selected publication state and acquisition plan
- clarified that parallel retrieval does not define validity, priority, freshness, mirror preference, routing authority, topology authority, or adaptive selection authority
- clarified that faster or more responsive mirrors do not become semantic authorities
- clarified that fetch completion may only satisfy retrieval of already-selected objects
- clarified that fetch failure may only trigger bounded deterministic retrieval substitution for the same selected object

No runtime behavior changed.

No distributed REFLECT implementation was introduced.

No mirrors, network retrieval, topology behavior, adaptive routing, request telemetry, cache/replay systems, or frontend/public API changes were introduced.

Preserved invariants:

- publication-state validity remains client-derived
- selected publication-state identity remains fixed during fetch/acquisition/fallback
- acquisition plans remain the subordinate runtime boundary for retrieval
- parallel fetch behavior does not define semantic priority
- mirror responsiveness does not become state preference
- runtime retrieval behavior does not define semantic validity
- cross-state reconstruction remains forbidden
- mirrors remain replaceable publication surfaces, not authorities

Checkpoint:

- `reflect-fetch-policy-runtime-boundary-v1`

Engineering[37] status:

**REFLECT fetch-policy runtime-boundary semantic hardening complete**

---

### Engineering[37] — REFLECT Mirror Selection Semantics

Engineering[37] performed a bounded REFLECT mirror-selection semantic hardening pass.

Implemented:

- clarified that mirror assignment is deterministic publication-surface assignment
- clarified that mirror assignment exists to preserve bounded separation and fragmented observability
- clarified that mirror assignment does not define validity, priority, trust, preference, capability ranking, routing authority, topology authority, or adaptive retrieval authority
- clarified that primary mirrors are not semantic authorities
- clarified that fallback mirrors are not lower-priority publication states
- clarified that mirror roles are runtime retrieval surfaces only

No runtime behavior changed.

No distributed REFLECT implementation was introduced.

No mirrors, network retrieval, topology behavior, adaptive routing, request telemetry, cache/replay systems, or frontend/public API changes were introduced.

Preserved invariants:

- publication-state validity remains client-derived
- selected publication-state identity remains fixed
- mirror assignment fragments observability; it does not optimize semantic truth
- mirror roles do not define object validity or state freshness
- mirror selection does not introduce routing authority or topology authority
- runtime retrieval behavior does not define semantic validity
- cross-state reconstruction remains forbidden
- mirrors remain replaceable publication surfaces, not authorities

Checkpoint:

- `reflect-mirror-selection-semantics-v1`

Engineering[37] status:

**REFLECT mirror-selection semantic hardening complete**

---

## Engineering[38] — REFLECT Retrieval Provider Boundary Clarification

Engineering[38] performed a bounded REFLECT distributed-acquisition seam discipline pass.

No distributed retrieval, live mirrors, networking, topology behavior, adaptive routing, cache/replay systems, public API changes, or frontend topology awareness were introduced.

Clarified:

- retrieval providers are future runtime acquisition surfaces only
- retrieval providers may supply already-selected publication material to the acquisition layer
- retrieval providers must not select, rank, repair, or prefer publication state
- retrieval providers must not mutate traversal order or continuation semantics
- retrieval availability must not define semantic validity
- `acquireTraversalTarget(...)` currently validates already-supplied material and does not perform retrieval
- future retrieval providers must attach before traversal validation
- acquisition validation remains subordinate to the selected publication-state identity and acquisition plan

Locked interpretation:

`Retrieval may obtain material. Retrieval may not choose truth.`

Checkpoint tag:

- `reflect-retrieval-provider-boundary-v1`

Engineering[38] status:

**REFLECT retrieval-provider boundary clarification complete**

---

## Engineering[39] — REFLECT Local Retrieval Provider Abstraction

Engineering[39] introduced the first bounded local retrieval-provider abstraction.

No distributed retrieval, live mirrors, networking, topology behavior, adaptive routing, cache/replay systems, public API changes, or frontend changes were introduced.

Implemented:

- local retrieval-provider module
- provider seam inside local acquisition
- explicit provider failure handling before traversal validation
- regression coverage for missing provider material

The provider seam attaches after acquisition-plan construction and before traversal validation.

Current runtime shape:

selected publication state
→ acquisition plan
→ local retrieval provider
→ publication group
→ traversal validation
→ reconstruction

The current local provider returns an already-supplied publication group.

The retrieval unit is the publication group:

- descriptor
- connector
- chunks

Locked responsibilities:

- selection chooses publication-state truth
- retrieval supplies already-selected material
- validation accepts or rejects retrieved material

Retrieval-provider responsibility is limited to supplying selected publication material.

A retrieval provider must not:

- select publication state
- rank publication state
- prefer faster or newer state
- mutate traversal order
- mutate continuation semantics
- validate truth
- repair publication groups
- infer validity from availability
- expose topology-aware behavior

Validation remains owned by acquisition/traversal and publication-object verification.

Provider failure is now explicitly separated from validation failure:

- `publication-not-retrieved`
- `invalid-retrieval-provider`
- `continuation-publication-not-retrieved`
- `invalid-continuation-retrieval-provider`

These are runtime acquisition failures only. They do not imply publication-state invalidity.

Locked rule:

`Retrieval obtains material. Selection chooses truth. Validation accepts or rejects material.`


Current retrieval identity surface:

- acquisition target

The current local retrieval provider consumes acquisition targets directly.

No separate retrieval-request object currently exists.

This is intentional.

The acquisition plan remains the authority for:

- selected publication-state identity
- traversal ordering
- object identity

Retrieval remains subordinate to the acquisition plan.

Future retrieval-provider evolution must preserve this relationship.

Introducing a retrieval-request object is not currently justified and may only occur if it preserves the existing separation between:

- selection authority
- retrieval responsibility
- validation authority

---

## Engineering[40] — REFLECT Retrieval Provider Evolution Constraints

Engineering[40] performed a bounded semantic-hardening pass for future REFLECT retrieval-provider evolution.

No runtime code was changed.

No distributed retrieval, mirrors, networking, topology behavior, adaptive routing, cache/replay systems, request telemetry, public API changes, or frontend changes were introduced.

Documented:

- retrieval providers are acquisition surfaces only
- provider evolution must preserve the authority split between selection, retrieval, and validation
- the current retrieval identity surface remains the acquisition target
- no separate retrieval-request object is currently justified
- retrieval providers should receive only the minimum information required to identify the retrieval target
- providers should not receive publication-window state, alternative selected states, continuation history, attempt history, validity outcomes, or selection rationale
- any future retrieval-request object must remain a derived, non-authoritative wrapper around the acquisition target
- continuation and fallback remain acquisition-owned
- providers must not decide continuation eligibility
- providers must not mutate selected targets
- providers must not substitute publication states
- providers must not become topology, ranking, validity, cache, replay, or telemetry authority

Locked interpretation:

Selection chooses truth.

Retrieval obtains material.

Validation accepts or rejects material.

Provider design test:

A future provider extension is valid only if the provider could still be replaced by a dumb material fetcher without changing semantic truth.

Supporting doc:

- `docs/reflect/REFLECT_RETRIEVAL_PROVIDER_EVOLUTION_V1.md`

Engineering[40] status:

**REFLECT retrieval-provider evolution constraints documented**

---

## Engineering[41] — REFLECT Minimum Retrieval Contract Surface

Engineering[41] performed a bounded design-observation pass on future retrieval-provider evolution.

No runtime code was changed.

No distributed retrieval, mirrors, networking, topology behavior, adaptive routing, cache/replay systems, request telemetry, public API changes, or frontend changes were introduced.

Documented:

- the minimum distributed-capable retrieval-provider contract surface
- retrieval-contract minimality constraints
- continued use of the acquisition target as the retrieval identity surface
- continuation ownership boundaries
- fallback ownership boundaries
- retrieval-request object justification constraints

Observed implementation result:

The current provider contract:

    getPublicationGroup({ target })

already satisfies the minimum distributed-capable retrieval-provider contract.

Current implementation confirms:

- retrieval consumes acquisition targets directly
- continuation reuses the same selected target
- providers do not receive continuation history
- providers do not receive attempt history
- providers do not receive validity outcomes
- providers do not receive selection rationale

Locked interpretation:

The acquisition target remains the sole retrieval identity surface.

Future distributed acquisition should evolve retrieval implementation behind the provider boundary rather than expanding provider authority.

A separate retrieval-request object is not currently justified.

If introduced in the future, it must remain a derived, non-authoritative wrapper around the acquisition target.

Continuation remains acquisition-owned.

Fallback remains acquisition-owned.

Provider design test:

A provider extension is valid only if the provider could still be replaced by a dumb material fetcher without changing semantic truth.

Supporting doc:

- `docs/reflect/REFLECT_MINIMUM_RETRIEVAL_CONTRACT_V1.md`

Engineering[41] status:

**REFLECT minimum retrieval contract surface documented**

---

## Engineering[42] — REFLECT Minimum Distributed Acquisition Semantics

Engineering[42] performed a bounded design-observation pass on future distributed acquisition evolution.

No runtime code was changed.

No distributed retrieval, mirrors, networking, topology behavior, adaptive routing, cache/replay systems, request telemetry, public API changes, or frontend changes were introduced.

Documented:

- minimum acquisition-owned distributed acquisition semantics
- acquisition-owned retrieval-substitution boundaries
- acquisition-owned continuation boundaries
- acquisition-owned fallback boundaries
- topology-neutral acquisition constraints
- acquisition authority minimization rules

Locked interpretation:

Distributed acquisition may substitute acquisition surfaces.

Distributed acquisition must not substitute semantic truth.

Selection chooses truth.

Retrieval obtains material.

Validation accepts or rejects material.

Acquisition orchestrates bounded retrieval of already-selected targets.

Acquisition must not become hidden topology authority.

Observed result:

The minimum future distributed acquisition model is:

    selected publication state
    -> acquisition plan
    -> deterministic acquisition-surface order
    -> retrieval provider
    -> publication group
    -> traversal validation
    -> reconstruction

The selected publication-state identity remains fixed before distributed acquisition begins.

Acquisition remains responsible for:

- selected target preservation
- traversal ordering
- continuation eligibility
- fallback eligibility
- deterministic acquisition-surface substitution
- runtime failure classification
- lifecycle result construction

Distributed acquisition may improve material availability.

It must not become selection, validity, ranking, telemetry, topology, continuation, or fallback authority.

Supporting doc:

- `docs/reflect/REFLECT_MINIMUM_DISTRIBUTED_ACQUISITION_SEMANTICS_V1.md`

Engineering[42] status:

**REFLECT minimum distributed acquisition semantics documented**


---

## Engineering[43] — REFLECT Convergence Assessment

Engineering[43] performed a bounded REFLECT convergence and remaining-risk assessment.

No runtime code was changed.

No distributed retrieval, mirrors, networking, topology behavior, adaptive routing, cache/replay systems, request telemetry, public API changes, or frontend changes were introduced.

Assessment result:

REFLECT semantic design is presently sufficiently constrained.

No major unresolved REFLECT authority ambiguity was identified.

The locked authority model remains:

- selection chooses publication-state truth
- retrieval obtains already-selected material
- validation accepts or rejects retrieved material
- acquisition orchestrates bounded retrieval of already-selected targets
- continuation remains acquisition-owned
- fallback remains acquisition-owned
- mirrors remain replaceable publication surfaces only
- retrieval providers remain non-authoritative acquisition surfaces only

Future REFLECT work should be implementation-driven only.

Further semantic decomposition is not currently justified unless a genuine new unresolved authority risk is discovered.

Remaining risks are implementation-discipline risks, not current design-frontier risks:

- digest-layer regression
- provider input widening
- accidental topology exposure
- adaptive routing creep
- request/history persistence
- convenience code becoming authority

Engineering[43] status:

**REFLECT semantic convergence assessed — no further REFLECT design decomposition currently required**

---

## Engineering[48] — REFLECT Minimum Acquisition Target Contract

Engineering[48] documented the minimum stable REFLECT acquisition target contract.

Document added:

- `docs/reflect/REFLECT_MINIMUM_ACQUISITION_TARGET_CONTRACT_V1.md`

Locked interpretation:

- the acquisition target is an acquisition identity object
- the target describes what must be acquired
- the target does not describe how acquisition occurs
- target owns truth-preservation authority
- acquisition machinery owns truth-acquisition behavior

Required target authority classes:

- acquisition authority
- validation authority
- traversal authority
- state-coherence authority

Forbidden target authority classes:

- provider authority
- surface authority
- routing authority
- fallback authority
- topology authority
- transport authority

Evolution rule:

- target may acquire additional truth-preservation coordinates
- target must not acquire truth-acquisition coordinates
- provider, surface, routing, fallback, topology, transport, or orchestration changes must not require target mutation

No runtime changes were introduced.

Engineering[48] status:

**CLOSED — checkpoint complete**

-------------------------------------------------------------------------------
FORMAL ARCHITECTURE STATUS (Engineering[127])
-------------------------------------------------------------------------------

Engineering[127] completed the first formal consolidation review of the Privacy
Engine architectural ontology.

Result:

- The foundational Privacy Engine formal ontology is considered
  architecturally complete.
- No missing first-class architectural subject was identified.
- No conflicting architectural identity model was identified.
- No conflicting protocol-authority model was identified.
- Remaining work consists of editorial normalization, specification
  composition, and preservation of the established ontology.

Future architectural work should preserve the established ontology.

Expansion of the ontology requires demonstration of a genuine new first-class
architectural subject rather than editorial, structural, or terminology
refinement.

The consolidation review is recorded in:

docs/PRIVACY_ENGINE_FORMAL_ARCHITECTURE_CONSOLIDATION_REVIEW_V1.md

STATE.md remains the canonical architectural authority.



---

## Engineering[287] — Accepted G4 protocol-definition baseline

Checkpoint identity: E287-ACCEPTED-DEFINITION-BASELINE-V1

Steve fully accepted the corrected parameterized G4 protocol definition on
1 October 2026. Definition acceptance is complete at the reviewed scope;
implementation can now be developed against the accepted contract. Concrete
governing parameters and qualified evidence remain required by that contract.

Accepted baseline:
`docs/privacy-engine/generation-004/accepted-definition/engineering-287/README.md`

Frozen definition archive SHA-256:
`6dd7fb4658ff25076ed7c4409bbe7ae74479fea247586da4cc460a3955045505`

Owning S90 SHA-256:
`0bb1e21b33d919aa9e174f374d224803aadef17dd8087e048562ab8d277c35f4`

The 972-requirement accepted definition preserves all S03–S89 source bytes and
the preceding 971 requirement records. CAP-111 records the approved non-vacuity
rule. Acceptance is user acceptance following a same-reviewer semantic assessment;
separately independent technical-review provenance is not asserted.

This Git checkpoint preserves accepted definition and review provenance. G4
remains unpublished; no succession, source/assessor appointment, profile admission
or registry insertion occurs. Published G3 is unchanged, M=0, and I164 adoption
remains not-performed. No runtime implementation, circuit, key, proof artifact,
environment configuration or deployed contract is changed by this checkpoint.

Next substantive work: develop and demonstrate a conforming implementation
against this accepted parameterized definition, preserving the stated scope
and qualification/admission boundaries. Do not reopen a generic definition
review cycle without a concrete demonstrated defect.
