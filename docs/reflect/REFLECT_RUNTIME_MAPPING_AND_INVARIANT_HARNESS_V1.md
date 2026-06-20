# REFLECT Runtime Mapping & Invariant Harness V1

Engineering[60] runtime mapping review.

STATE.md remains canonical.

## Purpose

This document maps already-locked REFLECT invariants to their current runtime owners and test status.

It does not introduce new REFLECT semantics.

## Conclusion

REFLECT semantic closure remains intact.

Every major locked REFLECT invariant reviewed during Engineering[60] has an identifiable runtime owner.

The remaining frontier is regression coverage and invariant harness strengthening, not further semantic decomposition.

## Runtime Component Inventory

| Runtime component | Role |
|---|---|
| `preparedPaths.js` | Prepared-path boundary and final reconstructed-path equality validation |
| `publicationObjects.js` | Publication object construction, digest integrity, coherence checks, publication-state acceptance, reconstruction |
| `publicationWindows.js` | Bounded publication-window handling and deterministic coherent-state selection |
| `acquisition.js` | Acquisition planning, selected-state preservation, traversal, continuation, fallback/surface substitution |
| `retrievalProvider.js` | Retrieval-provider boundary; resolves selected acquisition targets into publication material only |
| `objectModel.js` | Envelope construction, object typing, digesting, serialization primitives |
| `materials.js` | Prepared-path material normalization |

## Invariant Mapping

| Invariant | Runtime owner | Current status |
|---|---|---|
| Prepared-path boundary | `preparedPaths.js`, `publicationObjects.js` | Implemented |
| Deterministic state targeting | `publicationWindows.js` | Implemented |
| Integrity verification | `publicationObjects.js` | Implemented |
| Coherence verification | `publicationObjects.js` | Implemented |
| No cross-state mixing | `publicationObjects.js`, `publicationWindows.js`, `acquisition.js` | Enforced by digest/coherence/target checks; dedicated regression harness still desirable |
| Reconstruction preservation | `publicationObjects.js`, `preparedPaths.js` | Implemented |
| Fallback preserves selected state | `acquisition.js` | Implemented and partially test-covered |
| Provider non-authority | `retrievalProvider.js` | Implemented and test-covered |
| Acquisition preservation | `acquisition.js` | Implemented |
| Publication-state consistency | `publicationObjects.js`, `publicationWindows.js` | Implemented |

## Runtime Enforcement Notes

### Selected-state preservation

`acquisition.js` builds an acquisition plan from an already-selected publication state.

The plan carries selected state digest, object targets, and traversal order.

The selected target is fixed before retrieval or fallback.

Acquisition validates retrieved publication material against the target content digest.

If material does not match the selected target, acquisition fails with a content-digest mismatch rather than accepting replacement truth.

### Fallback and surface substitution

Fallback or continuation may substitute the acquisition surface or retrieved publication attempt.

Fallback must not substitute the selected state.

Current tests already verify that surface substitution preserves selected state digest and selected target.

This matches the locked REFLECT rule:

    fallback replaces surface
    not state

### Integrity and coherence

`publicationObjects.js` recomputes publication-state digests and rejects digest mismatch.

It also verifies connector/chunk agreement through connector digest, chunk digests, chunk offset, chunk size, and descriptor agreement.

This enforces publication-object integrity and internal coherence before reconstruction.

### Reconstruction preservation

`reconstructPreparedPathMaterial(...)` reconstructs path material only after publication objects verify.

The prepared-path layer then checks reconstructed material against expected material by exact equality over leaf, index, root, depth, siblings, and pathBits.

Reconstruction may interpret preserved material or fail.

It must not repair, synthesize, or replace truth.

## Test Coverage Inventory

| Invariant | Coverage status |
|---|---|
| Prepared-path boundary | Present |
| Deterministic state targeting | Present |
| Integrity verification | Strong |
| Coherence verification | Strong |
| Reconstruction preservation | Present |
| Provider non-authority | Present |
| Acquisition preservation | Present |
| Fallback preserves selected state | Present / partial |
| No cross-state mixing | Enforced indirectly; dedicated regression harness recommended |

## Gap Classification

No semantic gaps were found.

No major invariant was found without a runtime owner.

Identified implementation backlog is test-focused:

| Gap | Classification |
|---|---|
| Dedicated cross-state mixing regression tests | Test missing |
| Dedicated fallback-preserves-selected-state regression harness | Test hardening |
| Explicit invariant mapping comments/test names | Documentation/test clarity |
| Broader multi-state fixture coverage | Test hardening |

## Minimum Invariant Harness

The smallest useful next harness should test:

    connector(state A) + chunks(state B) -> reject
    publication(state A) + selected target(state B) -> reject
    fallback retrieval of wrong state -> reject
    surface substitution preserving selected target -> accept only if target digest matches
    tampered publication-state digest -> reject
    tampered connector/chunk digest -> reject

Highest-leverage first test group:

    No Cross-State Mixing Regression Harness

Reason:

It exercises the most important REFLECT invariants together:

    selected-state preservation
    integrity verification
    coherence verification
    reconstruction preservation
    fallback non-reselection

## Engineering[60] Result

Engineering[60] confirms:

    documented invariant
        -> runtime owner

    runtime owner
        -> enforcement path

    enforcement path
        -> test status

    test status
        -> implementation backlog

The dominant next frontier is not new REFLECT semantics.

The dominant next frontier is invariant regression coverage.
