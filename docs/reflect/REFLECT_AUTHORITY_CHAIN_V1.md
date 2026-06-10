# REFLECT_AUTHORITY_CHAIN_V1

## Purpose

This document records the REFLECT authority chain established through Engineering[41]–Engineering[49].

It serves as a consolidation and navigation document.

It does not replace individual authority-contract documents.

If any conflict exists, STATE.md remains authoritative.

---

## Core Principle

REFLECT preserves truth by separating authority into distinct layers.

Each layer owns a bounded responsibility.

No layer may silently absorb the authority of another layer.

---

## Authority Chain

The current REFLECT authority chain is:

    selection
        ->
    target
        ->
    acquisition
        ->
    retrieved material
        ->
    reconstruction
        ->
    validation

Truth preservation emerges from the separation of these responsibilities.

---

## Selection

Selection chooses truth.

Selection determines:

- selected publication state
- selected publication-state identity

Selection occurs before acquisition begins.

Selection authority must not migrate downstream.

---

## Target

Target preserves truth identity.

Target answers:

    What object is being acquired?

Target does not answer:

    How is the object obtained?

Target authority is documented in:

- REFLECT_MINIMUM_ACQUISITION_TARGET_CONTRACT_V1.md

---

## Acquisition

Acquisition preserves selected truth during execution.

Acquisition owns:

- target preservation
- traversal preservation
- continuation
- fallback
- surface substitution
- lifecycle result construction

Acquisition does not own:

- truth selection
- target mutation
- reconstruction
- truth repair

Acquisition authority is documented in:

- REFLECT_MINIMUM_ACQUISITION_CONTRACT_V1.md

---

## Retrieved Material

Retrieved material is acquisition output.

Retrieved material preserves:

- descriptor identity
- connector identity
- chunk identity
- digest identity

Retrieved material is not reconstructed truth.

Retrieved-material authority is documented in:

- REFLECT_RETRIEVED_MATERIAL_CONTRACT_V1.md

---

## Reconstruction

Reconstruction interprets preserved material.

Reconstruction may:

- verify object consistency
- assemble chunks
- derive path material

Reconstruction must not:

- select truth
- repair truth
- replace truth
- synthesize truth

Reconstruction authority is documented in:

- REFLECT_RECONSTRUCTION_BOUNDARY_V1.md

---

## Validation

Validation confirms preservation.

Validation determines whether reconstructed material matches expected truth.

Validation may:

- confirm preservation
- reject preservation failure

Validation must not:

- rewrite truth
- repair truth
- substitute truth

---

## Preservation Rule

Each layer may preserve truth.

No layer may silently redefine truth.

A valid authority boundary satisfies:

    upstream truth selected
        ->
    downstream truth preserved

not:

    upstream truth selected
        ->
    downstream truth replaced

---

## Engineering[49] Consolidation

Engineering[49] established:

- acquisition authority contract
- retrieved-material contract
- reconstruction boundary

The resulting authority chain is:

    selection
        ->
    target
        ->
    acquisition
        ->
    retrieved material
        ->
    reconstruction
        ->
    validation

This chain is the current REFLECT authority model.

---

## Conclusion

REFLECT preserves truth through authority separation.

Selection chooses truth.

Target preserves truth identity.

Acquisition preserves truth during acquisition.

Retrieved material preserves acquired identity.

Reconstruction interprets preserved material.

Validation confirms preservation.

No layer may absorb the authority of another layer.
