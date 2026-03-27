# TEMPEST Overview V1

## Purpose

TEMPEST defines the execution-layer relay network for the Speak-Up privacy engine.

It replaces the single relayer model with a fixed multi-relayer system to improve:

- privacy
- liveness
- censorship resistance
- operational robustness

TEMPEST is not specific to petitions.

It is a reusable execution layer for private, ZK-authenticated actions.

---

## Layer Position

TEMPEST operates in:

4. Execution / Submission layer

It does NOT handle:

- enrollment (funding/admission)
- membership construction
- Merkle path distribution

---

## TEMPEST Topology

TEMPEST consists of exactly **7 relayers**:

T E M P E S T

This fixed set provides:

- deterministic behavior
- bounded complexity
- sufficient decentralization for Phase A

---

## Core Properties

- deterministic relay selection per action
- no single relay dependency
- treasury-backed gas continuity
- relayers are privacy-stateless

---

## Design Principles

1. Preserve existing ZK system
2. Relayers are transport, not authority
3. No identity or correlation retention
4. Treasury funds continuity, not participation
5. Deterministic behavior over probabilistic behavior

---

## Phase A Scope

TEMPEST V1 addresses:

- execution-layer decentralization
- relay observability reduction
- relay liveness

It does NOT yet solve:

- wallet-funded enrollment linkage
- path-server centralization
- network metadata leakage