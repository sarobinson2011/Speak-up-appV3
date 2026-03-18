# ADMISSION_RIGHT_MODEL_V0.md

Status: Draft V0 design candidate  
Scope: Design only; no implementation in this document

## Purpose
Define the V0 admission-right lifecycle for unlinkable membership enrollment in the Speak-up privacy participation engine.

This mechanism separates **public admission funding** from **anonymous membership activation**, allowing users to join the anonymous membership set without linking their wallet identity to their participation identity.

---

# Design goals

- Separate public funding identity from anonymous membership identity
- Preserve the current ZK signing model
- Minimise public linkage
- Minimise relay knowledge
- Maintain economic admission friction (anti-Sybil)
- Keep V0 simple, deterministic, and auditable
- Avoid modifying the existing ZK signing circuit if possible

---

# Locked decisions

The following design decisions are considered locked for V0 unless a critical flaw is discovered.

- Two-secret model: `admissionSecret` and `memberSecret` must be distinct
- Public bonded admission right + relayed private commitment activation
- One funded admission right activates exactly one membership leaf
- Activation consumes the right permanently
- Activated rights are not refundable
- Refunds apply only to unactivated rights after lock expiry
- Activation does **not** require authorization from the original funding wallet
- Multiple funded rights per wallet are allowed
- No expiry model in V0 beyond lock-then-refundable semantics
- AdmissionRegistry and MembershipRegistry are conceptually separate
- V0 assumes direct `AdmissionRegistry -> MembershipRegistry` interaction
- Refund calls may specify an explicit recipient
- The existing signing proof system should remain unchanged if possible

---

# Core objects

### admissionSecret

A private secret generated locally by the user.

Used only to control the funded admission right.

### admissionCommitment

```
admissionCommitment = Poseidon1(admissionSecret)
```

Public commitment representing a funded admission right.

This value appears on-chain when the right is funded.

### memberSecret

A separate private secret used for anonymous membership identity.

### leaf

```
leaf = Poseidon1(memberSecret)
```

This value becomes the membership leaf inserted into the Merkle tree.

---

# Core rule

`admissionSecret` and `memberSecret` must be distinct.

Reusing them would collapse the separation between funding identity and membership identity.

---

# Contract roles

## AdmissionRegistry

Responsible for the economic admission mechanism.

Responsibilities:

- fund admission rights
- enforce bond and lock period
- refund unused rights
- consume rights during activation

## MembershipRegistry

Responsible for anonymous membership state.

Responsibilities:

- register membership leaves
- maintain Merkle tree and root history
- support membership path lookup
- maintain compatibility with the existing signing flow

---

# AdmissionRight state

Each admission right is keyed by its commitment.

```
mapping(bytes32 => AdmissionRight) rights
```

### Fields

- `amount`
- `fundedAt`
- `unlockAt`
- `status`

### Status enum

```
None
Funded
Activated
Refunded
```

### Primary key

```
rights[admissionCommitment]
```

Wallet addresses are **not** used as the primary state key.

---

# Lifecycle

## 1. Fund

User locally generates:

```
admissionSecret
admissionCommitment = Poseidon1(admissionSecret)
```

Wallet funds one admission right.

Contract action:

```
fundAdmissionRight(admissionCommitment)
```

### Contract checks

- exact bond amount
- commitment unused
- status must be `None`

### Effects

- create right
- set `fundedAt`
- set `unlockAt`
- status = `Funded`

### Meaning

A right now exists.

The wallet **is not yet a member**.

---

## 2. Optional delay

No on-chain state change.

This delay intentionally separates:

- public funding event
- anonymous activation event

Increasing ambiguity improves privacy.

---

## 3. Activate

User generates a **separate** identity secret.

```
memberSecret
leaf = Poseidon1(memberSecret)
```

User sends to relayer:

```
admissionSecret
leaf
```

Relayer submits activation.

Contract verifies that the revealed secret opens a funded commitment.

### Contract checks

- right exists
- status is `Funded`
- right not refunded
- leaf not already registered
- revealed secret matches commitment

### Effects

- mark right as `Activated`
- insert `leaf` into membership tree
- emit activation event

### Meaning

One funded admission right has been privately consumed to create one anonymous member.

---

## 4. Sign

The existing signing model remains unchanged.

User signs using:

- `memberSecret`
- membership Merkle path
- existing nullifier logic
- existing public input ordering

The admission layer must not leak into the signing circuit.

---

## 5. Refund

Refund applies only to **unused rights**.

Conditions:

- status = `Funded`
- current time ≥ `unlockAt`
- caller proves possession of `admissionSecret`

Example call shape:

```
refundAdmissionRight(admissionSecret, recipient)
```

### Effects

- mark right as `Refunded`
- transfer bond

### Meaning

Unused admission right reclaimed.

No membership was created.

Activated rights are **not refundable**.

---

# Event set

## Admission layer

```
event AdmissionRightFunded(
    bytes32 indexed admissionCommitment,
    uint256 amount,
    uint256 unlockAt
);
```

```
event AdmissionRightActivated(
    bytes32 indexed admissionCommitment,
    bytes32 indexed leaf
);
```

```
event AdmissionRightRefunded(
    bytes32 indexed admissionCommitment,
    address indexed recipient,
    uint256 amount
);
```

## Membership layer

```
event LeafRegistered(
    bytes32 indexed leaf,
    uint256 leafIndex,
    bytes32 newRoot
);
```

---

# Privacy notes

- Funding wallet is linked only to `admissionCommitment`
- Anonymous membership identity is linked only to `leaf`
- Activation should be performed through the relayer
- Optional delay increases ambiguity between funding and activation
- Signing remains detached from public funding identity

---

# Non-goals for V0

The following are intentionally **out of scope** for this version.

- Post-activation refund mechanisms
- Wallet-authorized activation
- Changes to the ZK signing circuit
- Governance or treasury integrations
- Advanced batching or pooled activation
- Expiry models beyond lock-then-refundable semantics
- Tokenized admission-right representations

---

# Remaining implementation detail

The following items remain to be finalized before Solidity implementation:

- Minimal Solidity surface for `AdmissionRegistry`
- Minimal Solidity surface for `MembershipRegistry`
- Exact activation call shape between the two contracts
- Final storage layout and event field ordering