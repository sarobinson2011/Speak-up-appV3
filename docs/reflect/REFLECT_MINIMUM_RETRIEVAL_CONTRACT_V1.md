# REFLECT_MINIMUM_RETRIEVAL_CONTRACT_V1

## Purpose

This document defines the minimum retrieval-provider contract surface for future REFLECT distributed acquisition.

STATE.md remains canonical.

## Core Finding

The current retrieval-provider contract is already the minimum distributed-capable contract:

    getPublicationGroup({ target })

No broader provider contract is currently justified.

## Contract Boundary

A retrieval provider receives:

- the acquisition target

A retrieval provider returns:

- publication group material, or
- no material

A retrieval provider must not receive:

- publication-window state
- alternative selected states
- continuation history
- attempt history
- validity outcomes
- selection rationale
- petition identity
- nullifier identity
- actor identity
- topology preference history

## Authority Split

Selection chooses truth.

Retrieval obtains material.

Validation accepts or rejects material.

The provider may know what to fetch.

The provider must not know why it matters.

The provider must not choose what should count.

## Target as Retrieval Identity Surface

The acquisition target remains the sole retrieval identity surface.

If future distributed retrieval requires additional retrieval coordinates, those coordinates should be added to the acquisition target only when they remain:

- derived
- non-authoritative
- minimal
- object-identifying only

The provider contract should remain:

    getPublicationGroup({ target })

## Retrieval Request Object

A separate retrieval-request object is not currently justified.

A retrieval-request object may only be introduced if the target surface becomes insufficient and the request remains a dumb, derived, non-authoritative wrapper around the acquisition target.

It must not add:

- selection logic
- validity logic
- fallback authority
- continuation authority
- ranking logic
- topology preference
- request telemetry
- cross-request memory

## Continuation Boundary

Continuation remains acquisition-owned.

A provider may be invoked during continuation, but must not know:

- why continuation occurred
- whether continuation was eligible
- what previously failed
- whether returned material later validated

The continuation invocation should continue to use the same selected target.

## Fallback Boundary

Fallback remains acquisition-owned.

Fallback may replace the acquisition surface used to retrieve an already-selected target.

Fallback must not allow the provider to substitute:

- publication state
- object identity
- traversal order
- deterministic state target
- connector/chunk relationship

## Distributed-Capable Minimal Shape

The minimum future distributed-capable shape is:

    getPublicationGroup({ target })

A future provider may internally map the target to a distributed acquisition surface.

That internal mapping must remain implementation detail only.

It must not leak into:

- public API
- frontend behavior
- validation semantics
- selection semantics
- continuation semantics
- fallback semantics

## Design Test

A provider extension is valid only if this remains true:

> The provider could be replaced by a dumb material fetcher without changing semantic truth.

If replacing the provider changes selected truth, validity, continuation eligibility, or fallback semantics, the provider has become an authority surface and is invalid.

## Summary

The minimum retrieval-provider contract is the current contract.

Future distributed acquisition should evolve the material-acquisition implementation behind the provider boundary, not expand the provider into a request, topology, ranking, fallback, validation, or telemetry authority.
