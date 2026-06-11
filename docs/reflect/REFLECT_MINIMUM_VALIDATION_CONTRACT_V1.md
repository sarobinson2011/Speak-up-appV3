# REFLECT_MINIMUM_VALIDATION_CONTRACT_V1

## Purpose

This document defines the minimum stable contract of REFLECT validation.

The objective is to isolate what validation owns, what validation may safely conclude, and what authority must never migrate into validation as REFLECT evolves.

If any conflict exists, STATE.md remains authoritative.

---

## Core Principle

Validation owns confirmation.

Validation does not own determination.

Validation may confirm that preservation has been demonstrated.

Validation must not decide what truth should be preserved.

---

## Authority Boundary

Truth selection occurs upstream.

Target construction occurs upstream.

Acquisition occurs upstream.

Retrieved material preservation occurs upstream.

Reconstruction occurs upstream.

Validation consumes already-reconstructed material and confirms whether it matches the expected preserved truth.

Validation must not mutate any upstream authority boundary.

---

## Validation Responsibility

Validation exists to answer one narrow question:

    Was preservation demonstrated?

It does not answer:

    What truth should be selected?

    What alternate truth should replace this truth?

    What material should be repaired?

    Which source is more truthful?

    Which available object should win?

---

## Validation-Owned Authority

### Preservation Confirmation

Validation may confirm that reconstructed material preserves the expected truth.

Examples:

- reconstructed leaf matches expected leaf
- reconstructed index matches expected index
- reconstructed root matches expected root
- reconstructed depth matches expected depth
- reconstructed siblings match expected siblings
- reconstructed path bits match expected path bits

---

### Identity Confirmation

Validation may confirm that identity anchors remain stable.

Examples:

- selected contentDigest is present
- descriptor contentDigest matches expected contentDigest
- publication-state digest matches expected digest

Validation confirms identity preservation.

Validation does not create identity.

---

### Coherence Confirmation

Validation may confirm that related objects agree with each other.

Examples:

- descriptor agrees with connector
- connector agrees with chunks
- chunk digests match connector entries
- offsets and sizes match expected entries
- recomputed digest matches declared digest

Coherence confirmation is not truth selection.

It only confirms that preserved objects remain internally consistent.

---

### Reconstruction Confirmation

Validation may confirm that reconstructed material exactly matches expected prepared-path material.

Validation must require equality.

Validation must not accept partial truth as complete truth.

Validation must not fill missing material.

Validation must not reinterpret malformed material as valid truth.

---

### Failure Classification

Validation may classify failure.

Examples:

- invalid shape
- digest mismatch
- coherence mismatch
- reconstruction mismatch
- preservation not confirmed

Failure classification must remain descriptive and bounded.

It must not become truth selection, ranking, repair, or reconciliation.

---

## Failure Semantics

Validation success means:

    preservation confirmed

Validation failure means:

    preservation could not be confirmed

Validation failure does not mean:

    falsehood proven

    global absence proven

    alternate truth selected

    repair authorized

    fallback authorized by validation

    newer material should be preferred

    available material is more truthful

Failure is safe only when it remains explicit and bounded.

If preservation cannot be confirmed, validation must fail.

---

## Forbidden Authority Migration

The following authority classes must never migrate into validation.

### Truth-Selection Authority

Examples:

- selecting publication state
- reselecting publication state
- choosing an alternate target
- choosing a different digest
- deciding which truth should be used

Validation confirms selected truth preservation.

Validation does not select truth.

---

### Truth-Repair Authority

Examples:

- repairing chunks
- repairing descriptors
- filling missing siblings
- filling missing path bits
- correcting malformed material
- accepting repaired material as preserved truth

Validation must fail rather than repair.

---

### Truth-Replacement Authority

Examples:

- substituting a new root
- substituting a new leaf
- substituting alternate siblings
- replacing path bits
- replacing connector or chunk identity

Validation must not replace truth.

---

### Reconciliation Authority

Examples:

- merging materials from conflicting publications
- resolving disagreement across sources
- accepting partial overlap as sufficient truth
- constructing a consensus view from inconsistent objects

Validation confirms preservation of one expected truth.

Validation does not reconcile competing truths.

---

### Ranking Authority

Examples:

- ranking sources
- ranking providers
- ranking mirrors
- ranking publication states
- preferring newer, more available, or more complete material

Ranking is not validation.

---

### Availability Authority

Examples:

- treating availability as validity
- treating unavailability as falsehood
- treating repeated retrieval success as truth
- treating failed retrieval as proof of absence

Availability may affect acquisition outcomes.

Availability must not become validation truth.

---

### Adaptive Authority

Examples:

- adaptive reselection after validation failure
- topology-aware truth substitution
- dynamic policy mutation
- validation-driven fallback selection

Validation failure may be observed by upstream or calling code.

Validation itself must not become adaptive truth selection.

---

## Design Test

A validation extension is valid only if the following remains true:

Given already-selected expected truth and reconstructed material, validation may confirm equality or fail.

It must not select, repair, replace, rank, reconcile, or synthesize truth.

If validation begins deciding what truth should be used, validation has crossed the boundary.

---

## Minimum Stable Validation Contract

Required properties:

- validation consumes expected truth and reconstructed material
- validation confirms preservation by equality or coherence checks
- validation failure is explicit
- validation failure means preservation was not confirmed
- validation does not mutate upstream truth
- validation does not trigger truth replacement

Forbidden properties:

- validation-owned truth selection
- validation-owned truth repair
- validation-owned truth replacement
- validation-owned source ranking
- validation-owned reconciliation
- validation-owned availability-derived truth
- validation-owned adaptive reselection

---

## Conclusion

Validation is confirmation authority, not determination authority.

Selection chooses truth.

Target preserves truth identity.

Acquisition preserves selected truth during acquisition.

Retrieved material preserves acquired identity.

Reconstruction interprets preserved material.

Validation confirms preservation.

If preservation cannot be confirmed, validation fails.

Validation must never redefine truth.
