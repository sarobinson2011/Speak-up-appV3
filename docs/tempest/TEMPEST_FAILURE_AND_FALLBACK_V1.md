# TEMPEST Failure and Fallback V1

## Core Rule

Fallback is for relay failure, not logical invalidity.

---

## Flow

1. try relay in deterministic order
2. if success → stop
3. if temporary failure → next relay
4. if terminal invalid → stop
5. if all fail → return failure

---

## Unknown State Handling

If uncertain:

1. check nullifier on-chain
2. if used → treat as success
3. else → continue fallback

---

## Retry Rules

- max 1–2 attempts per relay
- no infinite retry loops

---

## Concurrency

- single active relay attempt per action
- no parallel broadcast

---

## Hard Stops

Do not fallback if:

- nullifier already used
- proof invalid
- contract will revert

---

## Rationale

Prevents:

- duplicate submissions
- relay amplification
- correlation leakage