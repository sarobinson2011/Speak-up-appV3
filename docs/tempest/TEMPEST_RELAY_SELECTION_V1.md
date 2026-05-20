# TEMPEST Relay Selection V1

## Policy

Relay selection uses:

**Deterministic shuffle per action**

---

## Inputs

Seed is derived from:

- petitionId
- nullifier
- protocol tag (e.g. TEMPEST_V1)

---

## Behavior

For each action:

1. compute deterministic permutation of 7 relays
2. attempt relays in that order
3. stop on success or terminal failure

---

## Properties

- same input → same order
- different input → different order
- no fixed primary relay
- built-in fallback

---

## Constraints

- relay health does NOT affect ordering
- no runtime reshuffling
- deterministic for canonical execution orchestration

---

Current orchestration semantics are governed by `STATE.md`.

Clients/frontends must not infer, expose, or depend upon relay ordering or topology visibility.

---

## Rationale

Prevents:

- relay stickiness
- single-relay dominance
- predictable routing patterns