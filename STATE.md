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

