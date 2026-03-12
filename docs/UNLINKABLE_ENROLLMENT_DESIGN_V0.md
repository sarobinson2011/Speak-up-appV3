# UNLINKABLE_ENROLLMENT_DESIGN_V0.md

Supporting document only.  
If this document conflicts with `STATE.md`, **STATE.md wins**.

---

# Speak-up-appV3 — Unlinkable Enrollment Design (V0)

This document explores how users can **enter the membership set without linking their identity or wallet to later petition signatures**.

The goal is to evolve the current membership model toward **Tornado-grade anonymity**, while preserving:

- Sybil resistance
- economic friction
- architectural simplicity
- compatibility with the existing ZK proof system

Architecture details remain in `STATE.md`.

---

# 1. Problem Statement

The current system enrolls members through a **wallet transaction**.

This creates a public link between:

- wallet address
- membership leaf creation
- enrollment time

Later, when the member signs a petition anonymously, observers can narrow possible identities by correlating:

- wallet enrollment events
- membership tree size
- timing
- known participants

Even though the ZK proof hides the identity of the signer, **membership entry itself remains publicly attributable**.

This weakens the anonymity set.

---

# 2. Design Goal

Allow users to **join the membership tree without a reliable public link between their wallet and their future petition signatures**.

Target properties:

- admission into the anonymity set is **not publicly attributable**
- the ZK proof system remains unchanged
- each member still has **one leaf**
- signing remains **one per petition via nullifier**
- Sybil resistance remains meaningful

---

# 3. Non-Goals

This design does **not** attempt to:

- hide petition creation (petition authors remain public)
- hide blockchain activity completely
- remove economic friction for membership
- eliminate all network metadata leaks

The goal is **unlinkable membership entry**, not total anonymity.

---

# 4. Hard Constraints

The following constraints must be preserved unless explicitly changed in `STATE.md`.

### 4.1 On-chain verification remains authoritative

The smart contract must enforce:

- proof validity
- root validity
- nullifier uniqueness

### 4.2 Membership identity derives from a secret

Current model:

leaf = Poseidon1(memberSecret)

### 4.3 Signing proof format remains unchanged

Public inputs:

- nullifier
- petitionId
- membershipRoot

### 4.4 Each member corresponds to one leaf

One member → one secret → one leaf.

### 4.5 Sybil resistance must exist

Membership admission must require **some scarce resource**.

---

# 5. Current Enrollment Model

Current flow:

wallet → registerBond() → MembershipRegistry

Result:

- wallet publicly appears in enrollment transaction
- leaf is registered on-chain
- membership tree grows

Privacy issue:

wallet → leaf → later proof use

Even though the proof is anonymous, the **enrollment event remains public**.

---

# 6. Candidate Enrollment Models

This section evaluates several possible designs.

---

## Model A — Direct Commitment Enrollment

User generates locally:

- memberSecret
- commitment = Poseidon1(memberSecret)

User submits commitment directly to the contract.

Pros:

- simple
- no backend involvement

Cons:

- wallet address still visible
- same leak as current system

Conclusion:

Does **not solve the core privacy problem**.

---

## Model B — Relayed Commitment Enrollment (Leading Candidate)

User generates locally:

- memberSecret
- commitment = Poseidon1(memberSecret)

Instead of submitting directly, the user sends the commitment to a **relayer**.

The relayer submits the on-chain transaction.

Flow:

user → relayer → MembershipRegistry

Result:

- blockchain sender = relayer
- user wallet not publicly linked to enrollment

Pros:

- consistent with existing relay signing model
- minimal contract changes
- removes direct wallet → leaf link
- preserves current ZK circuit design

Cons:

- relayer observes enrollment requests
- Sybil resistance must be enforced elsewhere

Conclusion:

Strong candidate.

---

## Model C — Credential-Based Admission

Users receive anonymous credentials that allow them to enroll.

Example sources:

- institutional issuer
- invite system
- identity attestations

Pros:

- strong Sybil resistance possible

Cons:

- introduces trust assumptions
- complicates architecture
- risks identity linkage

Conclusion:

Too complex for MVP evolution.

---

## Model D — Mixer-Style Admission Notes

Users deposit funds and receive an **admission note** similar to Tornado.

Later they use the note to enter the membership tree anonymously.

Pros:

- strongest theoretical unlinkability

Cons:

- introduces an entire mixer-style lifecycle
- significantly more complexity
- may require circuit redesign

Conclusion:

Too heavy for the current architecture stage.

---

# 7. Leading Candidate

The leading direction is:

## Relayed Commitment Enrollment with Bonded Admission

High-level flow:

1. User generates locally:

   - memberSecret
   - commitment = Poseidon1(memberSecret)

2. User submits enrollment request to relayer.

3. Relayer submits:

   registerCommitment(commitment)

4. Contract inserts commitment as a membership leaf.

5. User later signs petitions anonymously using `memberSecret`.

---

# 8. Sybil Resistance

Privacy cannot eliminate admission friction.

Membership entry must require a **scarce resource**.

Candidate mechanisms:

- refundable ETH bond
- admission fee
- rate-limited relayer admission
- invite tokens

The most natural continuation of the current system is:

**refundable bond-based admission.**

This maintains economic friction while enabling private membership entry.

---

# 9. Relayer Implications

If enrollment is relayed, the relayer becomes more important.

Responsibilities may include:

- submitting enrollment transactions
- enforcing rate limits
- rejecting malformed commitments

However the relayer must remain **non-authoritative**.

The contract must remain the final arbiter of membership.

---

# 10. Remaining Privacy Limitations

Even with relayed enrollment:

- relayer can observe submission timing
- IP metadata may leak
- anonymity set size may remain limited

Further privacy improvements may include:

- multiple relayers
- batching of enrollment transactions
- delayed admission

These are future improvements.

---

# 11. Decision Gate

Before implementing unlinkable enrollment, the following must be decided:

1. Should enrollment require a **refundable bond** or a **fee**?

2. Should **one relayer** or **multiple relayers** handle enrollment?

3. Should enrollment transactions be **batched** to reduce correlation?

4. Does enrollment require **rate limiting**?

Once these decisions are made, implementation can begin.

---

# 12. Summary

Current system:

wallet → enrollment → leaf

Proposed evolution:

user → relayer → commitment → leaf

This removes the public wallet → membership link while preserving:

- ZK proof design
- nullifier uniqueness
- economic admission friction

The system moves closer to **Tornado-grade anonymity** while remaining simpler than a full mixer architecture.