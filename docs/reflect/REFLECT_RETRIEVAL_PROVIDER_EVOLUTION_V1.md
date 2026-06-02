# REFLECT_RETRIEVAL_PROVIDER_EVOLUTION_V1

## Purpose

This document defines how REFLECT retrieval providers may evolve without becoming authority surfaces.

STATE.md remains canonical.

## Core Rule

Retrieval providers are acquisition surfaces only.

They may obtain already-selected publication material.

They must not choose, rank, repair, validate, or reinterpret publication truth.

## Authority Split

- Selection chooses truth.
- Retrieval obtains material.
- Validation accepts or rejects material.

## Current Retrieval Identity Surface

The current retrieval identity surface is:

- acquisition target

The current local provider shape is:

    getPublicationGroup({ target })

No separate retrieval-request object currently exists.

This is intentional.

## Allowed Future Provider Capabilities

A future provider may:

- fetch selected publication material
- fail to return material
- return material for acquisition validation
- use the acquisition target as retrieval identity
- support bounded deterministic retrieval substitution when acquisition owns the substitution rules

## Forbidden Provider Capabilities

A retrieval provider must not:

- select publication state
- rank publication state
- prefer newer or faster state
- repair publication state
- repair publication groups
- mutate traversal order
- mutate continuation semantics
- decide fallback eligibility
- decide semantic validity
- infer validity from availability
- expose topology-aware behavior
- create request telemetry
- maintain petition/nullifier-linked retrieval history
- become a cache/replay authority
- become a mirror reputation system
- become a provider ranking system

## Provider Knowledge Boundary

A provider may know:

- the acquisition target it is asked to retrieve
- the object identity required by that target
- the minimum location/material information needed to perform retrieval in a future runtime

A provider must not know or persist:

- why the object matters
- petition identity
- nullifier identity
- actor identity
- membership secret material
- selected-state priority logic
- validity decision logic
- continuation eligibility logic
- fallback traversal authority
- topology preference history

## Continuation and Fallback Boundary

Continuation and fallback remain acquisition-owned.

A provider may be invoked during continuation.

A provider must not decide whether continuation is allowed.

A provider must not mutate the selected target during continuation.

A provider must not substitute a different publication state.

Fallback replaces acquisition surface, not truth.

## Retrieval Minimality Principle

A retrieval provider should receive only the minimum information required to identify the retrieval target.

A retrieval provider should not receive:

- publication-window state
- alternative selected states
- continuation history
- attempt history
- validity outcomes
- selection rationale

The acquisition layer remains the sole owner of those concerns.

## Retrieval Request Object

Introducing a separate retrieval-request object is not currently justified.

A retrieval-request object may only be introduced if it remains a derived, non-authoritative wrapper around the acquisition target.

It must not add:

- selection logic
- validity logic
- ranking logic
- topology preference
- request telemetry
- petition/nullifier context
- cross-request memory

## Design Test

Any future provider extension must pass this test:

> Could this provider still be replaced by a dumb material fetcher without changing semantic truth?

If no, the provider has become an authority surface and is invalid.

## Summary

A provider may know what to fetch.

A provider must not know why it matters.

A provider must not choose what should count.
