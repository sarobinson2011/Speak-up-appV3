# REFLECT_FAILURE_AND_FALLBACK_V1

## Purpose

This document defines REFLECT failure and fallback semantics.

Fallback exists to preserve bounded object retrieval when a selected mirror fails.

Fallback does not change publication-state selection.

Fallback does not grant mirrors authority over validity, priority, routing, or state acceptance.

---

## Failure Classes

- Success
- Temporary failure
- Integrity failure
- Global invalid state

---

## Core Rule

Fallback replaces mirror, not object.

Fallback may substitute the publication surface used to retrieve an already-selected object.

Fallback must not substitute:

- publication state
- publication state ID
- root
- connector/chunk relationship
- selected object identity
- deterministic state target

---

## State Boundary

Fallback operates inside the selected publication-state lifecycle boundary.

If the selected publication state cannot be verified coherently, the state is invalid.

The client must not repair invalidity by mixing objects from another state.

---

## Constraints

- object identity is fixed per action
- connector separation is enforced
- fallback is bounded and deterministic
- fallback is per-object
- fallback is topology-neutral
- system must not collapse into single-mirror mode

---

## Retry Policy

Each object has:

- 1 primary mirror
- 2 fallback mirrors

Retrieval substitutions are bounded and deterministic.

Fallback mirrors are derived from the same deterministic selection context.

Fallback mirrors do not provide adaptive routing authority.

---

## Invalidity Handling

Integrity failure or coherence failure invalidates the affected state/object path according to the client verification rules.

Fallback may perform bounded deterministic retrieval substitution for the same selected object through an allowed fallback mirror.

Fallback must not be used to:

- select a different publication state
- combine connector/chunk material across states
- prefer a mirror-reported latest state
- heal digest-layer mismatch
- weaken connector separation
- introduce probabilistic routing

---

## Hard Rule

Fallback is bounded deterministic object-retrieval substitution only.

No cross-state recovery.

No adaptive reselection.

No mirror authority.
