# REFLECT_RETRIEVED_MATERIAL_CONTRACT_V1

## Purpose

This document defines the minimum stable contract for retrieved material in REFLECT acquisition.

The objective is to define what acquisition may hand downstream after material has been obtained, while preserving the boundary between acquisition and reconstruction.

If any conflict exists, STATE.md remains authoritative.

---

## Core Principle

Acquisition owns material acquisition.

Acquisition does not own material interpretation.

Acquisition may preserve material identity.

Acquisition must not construct material truth.

---

## Authority Boundary

Truth selection occurs before acquisition.

Target construction occurs before acquisition.

Acquisition obtains already-selected material.

Retrieved material is handed downstream for later reconstruction and validation.

Acquisition must not interpret retrieved material as reconstructed path truth.

---

## Retrieved Material Identity

Retrieved material identity is preserved through descriptor and digest identity.

Current identity anchors include:

- descriptor
- descriptor.contentDigest
- target.contentDigest

The content digest preserves material identity independently of:

- provider
- acquisition surface
- source
- routing mechanism
- topology
- transport

---

## Acquisition Responsibility Toward Retrieved Material

Acquisition may:

- obtain material
- reject missing material
- reject malformed material
- compare retrieved material identity against target identity
- preserve retrieved material unchanged
- classify acquisition failure
- continue or fallback according to acquisition-owned rules

Acquisition must not:

- reconstruct material
- synthesize material
- repair material
- normalize material into truth
- merge material across sources
- reconcile conflicting material
- reinterpret descriptors
- replace digests
- mutate material identity

---

## Accept / Reject / Preserve Rule

Acquisition has exactly three safe responses to retrieved material:

1. accept material whose identity matches the selected target
2. reject material whose identity does not match the selected target
3. preserve accepted material unchanged for downstream reconstruction

Acquisition must not introduce a fourth behavior:

- repair
- reinterpret
- enrich
- rewrite
- substitute truth

---

## Reconstruction Boundary

Reconstruction is downstream of acquisition.

Acquisition may return retrieved publication material.

Acquisition must not convert retrieved publication material into reconstructed path truth.

The reconstruction layer owns interpretation of retrieved material structure.

Acquisition owns only the preservation of selected material identity before that boundary.

---

## Continuation and Fallback

Continuation and fallback may attempt to obtain material again for the same selected target.

They must not change:

- selected publication state
- selected target
- traversal identity
- validation identity
- material identity
- reconstruction semantics

Continuation and fallback are acquisition behaviors.

They are not material-repair behaviors.

---

## Forbidden Authority Migration

The following authority classes must never migrate into acquisition through retrieved material handling.

### Material-Interpretation Authority

Examples:

- reconstructing path bodies
- interpreting chunk semantics
- deriving witness material
- deciding reconstructed path truth

### Material-Repair Authority

Examples:

- patching missing chunks
- filling gaps
- correcting malformed descriptors
- rewriting connector material

### Material-Synthesis Authority

Examples:

- constructing replacement publication material
- generating equivalent material
- manufacturing path material from partial inputs

### Cross-Source Reconciliation Authority

Examples:

- merging chunks from multiple selected states
- choosing between conflicting retrieved materials
- resolving source disagreement as truth

### Digest-Mutation Authority

Examples:

- replacing contentDigest
- accepting alternate digests
- recomputing identity to fit retrieved material

---

## Contamination Test

A proposed acquisition extension is valid only if the following remains true:

If the retrieved material is incorrect, incomplete, or inconsistent, acquisition rejects or retries.

It does not repair, reinterpret, or synthesize truth.

If acquisition begins producing material that was not retrieved as the selected object, acquisition has crossed into forbidden authority.

---

## Minimum Stable Retrieved-Material Contract

Required properties:

- retrieved material is tied to selected target identity
- descriptor/contentDigest identity is preserved
- accepted material is handed downstream unchanged
- failed material is rejected or retried
- reconstruction remains downstream

Forbidden properties:

- acquisition-side reconstruction
- acquisition-side material repair
- acquisition-side material synthesis
- acquisition-side cross-source truth reconciliation
- acquisition-side digest mutation
- acquisition-side interpretation of reconstructed path truth

---

## Conclusion

Retrieved material is acquisition output, not acquisition truth.

Acquisition may obtain, check, reject, retry, and preserve material.

Acquisition must not reconstruct, repair, synthesize, reinterpret, or mutate material truth.

The minimum retrieved-material contract preserves the boundary between acquisition and reconstruction while allowing acquisition surfaces to evolve independently.
