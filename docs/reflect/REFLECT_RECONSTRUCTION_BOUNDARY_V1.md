# REFLECT_RECONSTRUCTION_BOUNDARY_V1

## Purpose

This document defines the REFLECT boundary between retrieved material, reconstruction, and final prepared-path validation.

The objective is to preserve the separation between acquisition authority and reconstruction authority as REFLECT acquisition surfaces evolve.

If any conflict exists, STATE.md remains authoritative.

---

## Core Principle

Acquisition acquires and preserves material.

Reconstruction interprets preserved material.

Validation confirms interpreted material matches selected truth.

Reconstruction does not select truth.

Reconstruction does not repair truth.

---

## Authority Chain

The REFLECT authority chain is:

    selection
        -> target
        -> acquisition
        -> retrieved material
        -> reconstruction
        -> prepared-path validation

Each stage has a distinct authority boundary.

No later stage may silently absorb the authority of an earlier stage.

---

## Acquisition Boundary

Acquisition owns:

- material acquisition
- selected target preservation
- traversal preservation
- digest identity preservation
- continuation and fallback behavior
- acquisition failure classification

Acquisition does not own:

- material interpretation
- path reconstruction
- chunk semantic assembly
- final prepared-path truth validation

Acquisition may hand retrieved material downstream.

It must not reconstruct that material.

---

## Retrieved Material Boundary

Retrieved material is acquisition output.

Retrieved material must preserve:

- descriptor identity
- connector identity
- chunk identity
- digest identity

Retrieved material is not yet reconstructed path truth.

It is structured publication material awaiting reconstruction.

---

## Reconstruction Authority

Reconstruction owns interpretation of preserved publication material.

It may:

- verify publication object consistency
- sort chunks by offset
- assemble siblings
- assemble path bits
- derive reconstructed leaf
- derive reconstructed index
- derive reconstructed root
- derive reconstructed depth
- produce reconstructed path material

Reconstruction must operate only on preserved retrieved material.

---

## Reconstruction Constraints

Reconstruction must fail rather than repair.

Reconstruction must not:

- select publication state
- reselect target identity
- replace acquisition truth
- repair missing chunks
- synthesize path material
- merge inconsistent materials
- accept digest mismatches
- reinterpret malformed descriptors as valid truth
- mutate connector identity
- mutate chunk identity
- mutate content digest identity

---

## Validation Boundary

Prepared-path validation occurs after reconstruction.

Validation confirms that reconstructed material matches the expected prepared-path material.

Examples of required confirmations include:

- reconstructed leaf matches expected leaf
- reconstructed index matches expected index
- reconstructed root matches expected root
- reconstructed depth matches expected depth
- reconstructed siblings match expected siblings
- reconstructed path bits match expected path bits

Validation confirms truth preservation.

Validation does not authorize reconstruction to repair truth.

---

## Failure Rule

Failure is safe.

If reconstruction or validation cannot prove preservation, the result must fail.

Acceptable outcomes are:

- reconstructed material matches expected truth
- reconstruction fails
- validation fails

Unacceptable outcomes are:

- reconstruction repairs truth
- validation rewrites truth
- acquisition substitutes truth
- downstream code accepts partial truth as complete truth

---

## Forbidden Authority Migration

The following authority classes must never migrate into reconstruction.

### Selection Authority

Examples:

- choosing publication state
- choosing alternate target
- choosing alternate digest
- selecting newer or more available material

### Acquisition Authority

Examples:

- invoking fallback
- changing acquisition surface
- continuing traversal
- replacing retrieved material

### Repair Authority

Examples:

- filling missing chunks
- correcting malformed chunks
- substituting connector data
- manufacturing siblings or path bits

### Reconciliation Authority

Examples:

- merging chunks from conflicting publications
- resolving disagreement across sources
- choosing the most plausible material
- accepting partial overlap as sufficient truth

### Digest-Mutation Authority

Examples:

- recomputing a digest to fit reconstructed material
- accepting alternate content identity
- modifying descriptor identity after acquisition

---

## Design Test

A reconstruction extension is valid only if the following remains true:

Given the same preserved retrieved material, reconstruction may interpret it or fail.

It must not select, repair, replace, or synthesize truth.

If reconstruction begins changing what counts as selected truth, it has crossed the boundary.

---

## Minimum Stable Reconstruction Boundary

Required properties:

- reconstruction consumes preserved retrieved material
- reconstruction verifies publication-object consistency before interpretation
- reconstruction interprets connector and chunk material into path material
- prepared-path validation confirms reconstructed material against expected truth
- failure remains explicit and safe

Forbidden properties:

- reconstruction-side truth selection
- reconstruction-side acquisition fallback
- reconstruction-side material repair
- reconstruction-side cross-source reconciliation
- reconstruction-side digest mutation
- validation-side truth rewriting

---

## Conclusion

Reconstruction is interpretation authority, not truth-selection authority.

Acquisition preserves material identity.

Reconstruction interprets preserved material.

Prepared-path validation confirms interpreted material matches selected truth.

The stable boundary is:

    acquire / preserve / reject
        ->
    interpret / assemble / derive
        ->
    confirm / fail
