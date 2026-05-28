# REFLECT_STATE_VALIDITY_V1

## Purpose

This document defines how a REFLECT publication state becomes acceptable for witness construction.

A publication state is not valid because a mirror exposes it.

A publication state is valid only when the client can verify that the selected connector/chunk object set is coherent, integrity-valid, root-compatible, and within the bounded publication window.

Mirrors are replaceable publication surfaces.

They are not state authorities.

---

## Publication State

A publication state is a coherent set of REFLECT publication objects that share the same:

- publication state ID
- root
- protocol interpretation
- connector/chunk relationship
- publication-window membership

A publication state is treated as a single lifecycle boundary.

Objects from different publication states must not be combined.

---

## Validity Requirements

A publication state is valid only if it is:

- Coherent
- Compatible
- Retrievable through bounded deterministic acquisition semantics
- Integrity-verified
- Within publication window
- Root-valid
- Structurally separable
- Connector/chunk consistent
- Client-verifiable

---

## Client-Derived Validity

Validity is derived by the client.

Validity is not derived from:

- mirror assertion
- mirror freshness claims
- mirror preference
- mirror availability or responsiveness alone
- topology position
- adaptive routing outcome
- federation consensus

A mirror may expose objects.

Only the client accepts or rejects a publication state.

---

## Coherence Rule

Connector and chunk objects must belong to the same publication state.

The connector must describe the chunk set being used.

The chunk set must satisfy the connector, manifest, root metadata, and publication-state identity requirements.

A state is invalid if reconstruction would require mixing:

- different state IDs
- different roots
- different protocol interpretations
- connector material from one state with chunks from another state
- descriptor/group digests with publication-state digests

---

## Highest Recent Valid State

The selected state is the highest recent publication state that satisfies all validity requirements within the bounded publication window.

“Highest recent valid state” means:

- highest according to the deterministic publication-window ordering
- recent according to the bounded window policy
- valid according to client-derived verification
- coherent as one publication-state lifecycle boundary

It does not mean:

- latest object reported by a mirror
- most available or fastest mirror response
- mirror-preferred state
- adaptively selected state
- cross-state reconstruction candidate

---

## Fallback Constraint

Fallback may replace the mirror used to retrieve an object.

Fallback must not replace the selected publication state.

Fallback must not mutate:

- publication state ID
- root
- connector/chunk relationship
- selected object identity
- deterministic state target

Fallback is bounded deterministic object-retrieval substitution only.

It is not adaptive routing.

It is not state reselection.

It is not cross-state recovery.

---

## Hard Rule

If any condition fails, the state is invalid.

No partial acceptance.

No cross-state mixing.

No mirror authority.

No adaptive state repair.
