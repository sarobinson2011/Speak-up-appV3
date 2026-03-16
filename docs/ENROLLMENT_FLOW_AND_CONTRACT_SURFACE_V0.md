# ENROLLMENT_FLOW_AND_CONTRACT_SURFACE_V0.md

Supporting document only.  
If this document conflicts with `STATE.md`, **STATE.md wins**.

---

# Speak-up-appV3 — Enrollment Flow and Contract Surface (V0)

This document refines the leading direction established in:

- `docs/UNLINKABLE_ENROLLMENT_DESIGN_V0.md`

It focuses on the **actual flow** and **contract surface shape** for moving from the current wallet-linked enrollment model toward **unlinkable membership admission**.

This is still a design document.  
It does **not** authorize implementation yet.

Architecture truth remains in `STATE.md`.

---

# 1. Scope

This document defines the leading V0 direction for:

- unlinkable membership admission
- bond-based anti-Sybil friction
- relayed commitment activation
- separation of public funding from private membership identity

It assumes the following choices for now:

- **two secrets**
- **optional delay**
- **relayed commitment activation**
- **refundable bond friction remains the primary Sybil control**

---

# 2. Problem with the Current Contract

Current `MembershipRegistry` baseline:

- accepts `registerLeaf(uint256 leaf)` directly from `msg.sender`
- requires exact ETH bond in the same transaction
- stores:
  - `isRegistered[msg.sender]`
  - `leafOf[msg.sender]`
  - `bonded[msg.sender]`
  - `unlockAt[msg.sender]`
- emits:
  - `LeafRegistered(address indexed wallet, uint256 leaf, uint32 index, bytes32 newRoot)`

This creates a direct public link:

wallet → bond payment → leaf registration → later anonymous use

Even if later petition signing is relayed, the **membership entry event remains wallet-linked**.

That is the structural privacy limit we are trying to remove.

---

# 3. Design Objective

Replace:

wallet-bound membership registration

with:

public bond funding + private relayed commitment activation

The target effect is:

- a user may still need to provide ETH friction
- but the public wallet that provided ETH should not be trivially linked to the final membership leaf used for anonymous petition signing

---

# 4. Selected High-Level Direction

## Chosen V0 direction

**Two-stage bonded admission with two secrets**

### Public stage
A wallet funds an **admission right**.

### Private stage
A relayer later activates a **membership commitment** that consumes one admission right.

This separates:

- economic admission friction
- anonymous set entry

That is the key architectural move.

---

# 5. Secret Model

The design uses **two secrets**.

## 5.1 admissionSecret

Purpose:

- controls the right to consume a funded admission slot

This secret is associated with the public funding stage.

## 5.2 memberSecret

Purpose:

- defines the actual membership identity used later for petition signing

Current baseline leaf model remains:

leaf = Poseidon1(memberSecret)

This keeps membership identity separate from the funding entitlement.

---

# 6. Why Two Secrets

Using one secret would couple:

- payment entitlement
- membership identity

too tightly.

Using two secrets creates a cleaner split:

- `admissionSecret` controls the right to activate
- `memberSecret` defines the anonymous membership leaf

Benefits:

- cleaner privacy separation
- easier reasoning about funding vs use
- easier future extension if activation is delayed or batched

Cost:

- slightly more conceptual complexity

Conclusion:

The privacy benefit is worth the added structure.

---

# 7. Proposed V0 Flow

## Stage A — public bond funding

The user generates locally:

- `admissionSecret`
- `admissionCommitment`

The funding wallet then submits a public transaction that creates **one funded admission right**.

This stage is public and may remain wallet-linked.

That is acceptable because the goal is not to hide all funding activity.  
The goal is to prevent a clean public link from that funding wallet to the eventual membership leaf.

## Stage B — optional delay

There may be an optional time gap between:

- public funding
- private activation

This delay is not mandatory for V0, but the architecture should allow it.

Reason:

- reduces timing correlation
- keeps room for future batching
- improves practical anonymity

## Stage C — private relayed activation

Later, the user generates locally:

- `memberSecret`
- `leaf = Poseidon1(memberSecret)`

The user then submits to the relayer:

- proof or evidence that one funded admission right may be consumed
- the membership `leaf`

The relayer submits the activation transaction on-chain.

The chain sees:

- relayer as sender
- membership leaf inserted into the tree

The funding wallet is not the sender of this activation transaction.

## Stage D — later petition signing

No change to current signing model.

The user later signs petitions using:

- `memberSecret`
- the current root
- the current nullifier formula

This preserves compatibility with the current ZK signing flow.

---

# 8. Public vs Private Artifacts

## 8.1 Public artifacts

The system may publicly reveal:

- a funded admission right exists
- bond amount
- timing of funding
- timing of activation
- tree growth
- relayer-submitted activation tx

This is acceptable.

## 8.2 Private artifacts

The system should protect:

- the link between funding wallet and final membership leaf
- the link between admission right and future petition signing
- `memberSecret`
- the relation between `admissionSecret` and `memberSecret`

---

# 9. Contract Surface — Conceptual Refactor

The current contract merges three ideas into one action:

- bond payment
- wallet registration
- leaf insertion

The new design should separate them.

## 9.1 Current baseline function

Current shape:

`registerLeaf(uint256 leaf) payable`

This is too coupled for unlinkable admission.

## 9.2 Desired conceptual split

The new model should conceptually split into:

### A. fund admission right
Creates a public, bond-backed right to activate one future member leaf.

### B. activate membership commitment
Consumes one funded right and inserts one leaf into the Merkle tree.

This is the essential contract-surface change.

---

# 10. Candidate Function Shapes

These names are illustrative only.

## Option 1 — explicit two-step naming

- `fundAdmissionRight(bytes32 admissionCommitment) payable`
- `activateMembershipLeaf(...)`

Pros:

- very clear semantics
- easy to reason about

Cons:

- names may feel verbose

## Option 2 — slot language

- `reserveMembershipSlot(bytes32 admissionCommitment) payable`
- `consumeReservedSlot(...)`

Pros:

- communicates “bond buys one right”
- good mental model

Cons:

- less direct than “admission”

## Option 3 — note language

- `depositAdmissionNote(...) payable`
- `activateFromAdmissionNote(...)`

Pros:

- most Tornado-like mentally

Cons:

- may overfit mixer language to a non-mixer app

### Current recommendation

Use language closer to:

- **admission right**
- **membership activation**

This matches the actual system purpose better than mixer vocabulary.

---

# 11. Proposed Event Model

The baseline event:

`LeafRegistered(address indexed wallet, uint256 leaf, uint32 index, bytes32 newRoot)`

is no longer compatible with the privacy target because it explicitly logs the wallet.

Future event model should conceptually split into two event types.

## 11.1 Public admission funding event

Something like:

- funded admission right created
- amount locked
- maturity / unlock metadata if needed

This event may remain wallet-linked.

## 11.2 Membership activation event

Something like:

- leaf inserted
- index
- new root

This event should **not** include the originating funding wallet.

That is one of the most important event-level privacy requirements.

---

# 12. Bond Semantics

The current bond is:

- exact amount
- refundable after a lock period
- tied to `msg.sender`

In the new model, the bond should conceptually belong to the **admission right**, not directly to the final membership identity.

Key question:

Who can later recover the bond?

Possible answers:

## A. funding wallet recovers it
Simplest.

Pros:

- preserves current economic intuition
- easy to reason about

Cons:

- public funding identity remains visible at the economic layer

## B. admission right holder recovers it privately
Stronger privacy, but much more complex.

Pros:

- better privacy purity

Cons:

- much harder design
- may require note-style withdrawal logic

### Current recommendation

For V0, keep the refund semantics closer to the **funding wallet**.

Reason:

- simpler
- keeps complexity bounded
- still allows significant improvement if activation is relayed separately

This means V0 improves membership unlinkability without attempting perfect funding unlinkability.

That is an acceptable and honest trade.

---

# 13. Sybil Model

The primary Sybil friction remains:

- refundable ETH bond

This is still the simplest scarce resource compatible with the current architecture.

Additional optional controls:

- relayer rate limiting
- activation delay
- relayer-side spam throttling

These are supplemental only.

The bond remains the core anti-Sybil mechanism.

---

# 14. Relay Responsibilities

If this model is adopted, the relayer gains an additional role.

## 14.1 Enrollment relayer

Responsibilities:

- receive activation payloads
- validate payload structure
- submit activation transactions

## 14.2 Signing relayer

Already exists.

Responsibilities:

- receive proof payloads
- validate payload structure
- submit sign transactions

## 14.3 V0 operational recommendation

Use one backend implementation initially, but preserve conceptual separation between:

- enrollment relay path
- signing relay path

This keeps future multi-relayer evolution open.

---

# 15. Optional Delay

Optional delay between funding and activation is recommended, but not required for V0.

Reason:

- reduces simple timing linkage
- keeps room for later batching
- improves anonymity without forcing operational complexity immediately

Current recommendation:

- architect for optional delay
- do not require batching in V0

---

# 16. Compatibility with Current ZK System

The proposed flow should preserve:

- current petition signing circuit
- current public input order
- current nullifier model
- current petition signing verifier path

That means the first evolution should be concentrated in:

- membership admission flow
- membership registry surface
- relayer responsibilities

not in the petition-signing proof system.

This is a major advantage of the proposed direction.

---

# 17. What This Design Does NOT Solve

Even if implemented, this V0 approach does not fully eliminate:

- network metadata leakage
- relay observability
- timing correlation
- funding-wallet visibility at the economic layer

So this is not “perfect anonymity.”

It is a serious step forward because it breaks the most damaging public link:

funding wallet → direct member leaf registration

That is enough to justify the design.

---

# 18. Open Questions

These questions must be resolved before implementation.

## 18.1 Admission right representation

What exact on-chain object represents one funded admission right?

## 18.2 Activation authorization

How does the relayer prove or verify that one admission right may be consumed?

## 18.3 Refund mechanics

Does the funding wallet retain bond recovery rights in V0?

## 18.4 Event design

What exact events are emitted during:

- funding
- activation
- refund

## 18.5 Delay semantics

Should V0 merely allow delay, or should it encourage it explicitly?

## 18.6 Contract decomposition

Should this remain one registry contract with expanded semantics, or split into:

- admission registry
- membership registry

This is a major architecture choice and should be considered carefully before coding.

---

# 19. Current Recommendation

The current leading V0 direction is:

**Public bonded admission right + relayed private commitment activation**

This preserves:

- economic friction
- the current signing architecture
- current ZK proof design

while improving privacy by separating:

- public funding
- anonymous membership identity

This is the strongest next design candidate consistent with the existing system.

---

# 20. Summary

Current model:

wallet → bond payment → direct leaf registration

Proposed V0 direction:

wallet → public funded admission right  
(optional delay)  
user/relayer → private membership activation  
later → relayed anonymous petition signing

This design is not a full Tornado clone.

It is a more appropriate privacy architecture for a **free-speech anonymous membership system**:

- money provides anti-Sybil friction
- relayers reduce public identity linkage
- membership identity is separated from funding identity
- signing remains anonymous and nullifier-based