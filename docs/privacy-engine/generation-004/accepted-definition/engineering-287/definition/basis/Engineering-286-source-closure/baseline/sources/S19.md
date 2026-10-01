# PRIVACY_ENGINE_DEFINITION.md

Supporting document only.  
If this document conflicts with `STATE.md`, **STATE.md wins**.

---

# Speak-Up Privacy Engine Definition

This document defines the **core privacy primitive** that Speak-Up provides.

Speak-Up should be understood as a **privacy participation engine**, not a petition application.

Applications such as petitions, coordination signals, or funding systems are **built on top of this engine**.

Architecture rules remain defined in `STATE.md`.  
Threat analysis remains defined in `PRIVACY_THREAT_MODEL.md`.

This document defines **what the privacy engine does**.

---

## Terminology and Layer Boundary

In this document, terms such as "member", "participant", and "actor" refer to anonymous membership/proof semantics.

They must not be interpreted as:

- human identity
- account identity
- wallet identity
- profile identity
- recovery authority
- continuity authority

Current layer ownership:

- M2 owns identity / proof semantics
- Enrollment owns economic admission / eligibility semantics
- Custody owns local secret custody and portability semantics
- TEMPEST owns execution / submission semantics
- REFLECT owns path / publication semantics

The current identity primitive remains:

- `memberSecret -> leaf -> nullifier`

Continuity is defined only by possession of the same original `memberSecret`.

---

# 1. Core Principle

Speak-Up follows the rule:

**Private actors, public actions.**

Observers must be able to verify:

> “A valid member performed a valid action.”

without being able to determine:

> “Which member performed that action.”

The system therefore separates two concerns:

**Cryptography proves validity.**  
**Architecture preserves ambiguity.**

---

# 2. Privacy Goal

The privacy engine aims to guarantee **non-linkability of participation**.

A successful system allows observers to confirm that:

- an action occurred
- the action was valid
- the actor belonged to the valid participant set

while preventing observers from reliably determining:

- which participant performed the action
- which wallet funded participation
- which network request corresponds to which participant

The objective is not invisibility, but **high ambiguity**.

---

# 3. The Privacy Primitive

The Speak-Up engine exposes four capabilities.

### 1. Join an anonymity set

Participants join a set represented by a Merkle tree commitment.

### 2. Perform an anonymous action

A member generates a zero-knowledge proof locally.

### 3. Enforce one-action-per-member

A nullifier prevents the same member from performing the same action twice.

### 4. Publish verifiable public results

The blockchain records that a valid action occurred.

No participant identity is revealed.

This primitive can support many types of anonymous actions.

---

# 4. Engine Components

The engine consists of four functional layers.

---

## 4.1 Membership Set

The anonymity set is represented by an incremental Merkle tree.

Each member corresponds to:

leaf = Poseidon1(memberSecret)

The Merkle root represents the current valid participant set.

---

## 4.2 Proof Generation

The participant generates a proof locally demonstrating:

- knowledge of a valid membership leaf
- knowledge of the secret corresponding to that leaf
- correctness of the nullifier for the action

The proof reveals **no identity information**.

---

## 4.3 Nullifier Enforcement

Each action generates a nullifier:

nullifier = Poseidon3(memberSecret, actionId, SIGN_DOMAIN)

The smart contract rejects duplicate nullifiers.

This guarantees **one action per member per actionId**.

---

## 4.4 Public Verification

The verifier contract checks:

- proof validity
- Merkle root validity
- nullifier uniqueness

If valid, the contract records the action.

The blockchain therefore proves:

“A valid member performed a valid action.”

without revealing the member.

---

# 5. Relay Layer

To prevent wallet exposure, actions are submitted through relayers.

The relayer acts as a **sealed courier**.

Responsibilities:

- validate payload structure
- submit transactions
- avoid interpreting user intent

The relay must not introduce identifying signals.

---

# 6. Privacy Design Rule

The system must minimise **linkability**, not merely hide content.

Privacy failures can arise through:

- wallet exposure
- relay metadata
- request payload fingerprinting
- timing correlation
- backend logs
- network identifiers

Engineering decisions must therefore minimise **distinguishability between actions**.

Two valid actions should appear as similar as possible to external observers.

---

# 7. Application Layer

Applications use the privacy engine by defining an **action identifier**.

Example uses include:

- petition signatures
- anonymous voting
- anonymous attestations
- coordination signals
- participation proofs

Applications provide:

actionId

which becomes the domain for the nullifier.

Applications must **not modify the core privacy primitive**.

---

# 8. Design Objective

Engineering success for the privacy engine means:

- proofs are reproducible and deterministic
- nullifier enforcement is correct
- relay submission does not leak identity
- public artifacts prove validity without revealing origin

The engine therefore guarantees:

valid participation is provable  
participant identity remains ambiguous

Higher-level systems may safely build on top of this primitive.

The privacy layer itself must remain **minimal, robust, and generic**.