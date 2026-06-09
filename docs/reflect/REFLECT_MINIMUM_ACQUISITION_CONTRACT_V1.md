# REFLECT_MINIMUM_ACQUISITION_CONTRACT_V1

## Purpose

This document defines the minimum stable contract of REFLECT acquisition.

The objective is to preserve acquisition truth while allowing acquisition surfaces, providers, topology, routing mechanisms, and retrieval infrastructure to evolve independently.

If any conflict exists, STATE.md remains authoritative.

---

## Core Principle

Acquisition owns truth-preserving acquisition behavior.

Acquisition does not own truth selection.

Acquisition may substitute acquisition surfaces.

Acquisition must not substitute acquisition truth.

---

## Authority Boundary

Truth selection occurs before acquisition begins.

Publication-state selection occurs before acquisition begins.

Target construction occurs before acquisition begins.

Acquisition consumes already-selected truth.

Acquisition must preserve that truth throughout execution.

---

## Acquisition Responsibility

Acquisition exists to obtain already-selected material while preserving:

- selected publication-state identity
- target identity
- traversal identity
- validation identity

Acquisition is not permitted to reinterpret any of these identities.

---

## Acquisition-Owned Authority

### Selected-State Preservation

Examples:

- selectedStateDigest

Purpose:

- preserves selected publication-state identity throughout acquisition

---

### Target Preservation

Examples:

- acquisitionKey
- target identity

Purpose:

- preserves the selected acquisition objective

---

### Traversal Preservation

Examples:

- traversalOrder
- sequence

Purpose:

- preserves acquisition ordering semantics

---

### Validation Preservation

Examples:

- contentDigest

Purpose:

- preserves object identity independent of acquisition surface

Acquisition validates preservation.

Acquisition does not redefine validity.

---

### Continuation Authority

Examples:

- continuation eligibility
- continuation execution

Purpose:

- determines whether acquisition may continue attempting to obtain an already-selected target

Continuation remains acquisition-owned.

---

### Fallback Authority

Examples:

- acquisition-surface substitution
- surface traversal order

Purpose:

- allows acquisition to replace acquisition surfaces without replacing acquisition truth

Fallback remains acquisition-owned.

---

### Lifecycle Authority

Examples:

- failure classification
- terminal classification
- result construction

Purpose:

- produces acquisition outcomes without mutating acquisition truth

---

## Forbidden Authority Migration

The following authority classes must never migrate into acquisition.

### Truth-Selection Authority

Examples:

- publication-state selection
- publication-state reselection
- truth ranking
- truth replacement

Truth selection occurs before acquisition.

---

### Target-Mutation Authority

Examples:

- target reinterpretation
- acquisitionKey replacement
- target substitution

Acquisition preserves targets.

Acquisition does not redefine targets.

---

### Validation-Mutation Authority

Examples:

- digest replacement
- validity redefinition
- validation-policy mutation

Acquisition preserves validation identity.

Acquisition does not redefine validation identity.

---

### Provider Authority

Examples:

- provider ranking
- provider preference
- provider reputation

Provider behavior must not affect acquisition truth.

---

### Availability Authority

Examples:

- availability-derived validity
- availability-derived truth
- availability-derived preference

Material availability does not determine truth.

---

### Topology Authority

Examples:

- topology preference
- topology ranking
- mirror-set interpretation
- provider-graph interpretation

Topology is environmental knowledge.

It is not acquisition truth.

---

### Adaptive-Routing Authority

Examples:

- dynamic provider ranking
- adaptive reselection
- topology-driven truth mutation

Adaptive behavior must not alter selected truth.

---

## Preservation Rule

Acquisition may change:

- acquisition surface
- provider
- routing mechanism
- retrieval implementation

Acquisition must not change:

- selected publication state
- selected target
- traversal identity
- validation identity
- acquisition truth

---

## Design Test

A proposed acquisition extension is valid only if the following remains true:

If acquisition surfaces changed completely, would the same selected target still be acquired and validated as the same object?

If yes:

- acquisition truth is preserved

If no:

- acquisition has absorbed forbidden authority

---

## Minimum Stable Acquisition Contract

Required authority classes:

- selected-state preservation
- target preservation
- traversal preservation
- validation preservation
- continuation authority
- fallback authority
- lifecycle authority

Forbidden authority classes:

- truth-selection authority
- target-mutation authority
- validation-mutation authority
- provider authority
- availability authority
- topology authority
- adaptive-routing authority

---

## Conclusion

Acquisition owns truth-preserving acquisition behavior.

Acquisition does not own truth selection.

Acquisition may substitute acquisition surfaces.

Acquisition must not substitute acquisition truth.

The minimum stable acquisition contract is the authority required to preserve selected truth throughout acquisition evolution.
