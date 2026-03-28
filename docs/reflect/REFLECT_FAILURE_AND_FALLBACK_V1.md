# REFLECT_FAILURE_AND_FALLBACK_V1

## Failure Classes

- Success
- Temporary failure
- Integrity failure
- Global invalid state

---

## Core Rule

Fallback replaces mirror, not object.

---

## Constraints

- object identity is fixed per action
- connector separation is enforced
- system must not collapse into single-mirror mode

---

## Retry Policy

Each object has:

- 1 primary mirror
- 2 fallback mirrors

Retries are bounded and deterministic.