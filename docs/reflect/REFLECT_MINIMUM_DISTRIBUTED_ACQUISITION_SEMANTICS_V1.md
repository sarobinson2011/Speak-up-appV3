# REFLECT_MINIMUM_DISTRIBUTED_ACQUISITION_SEMANTICS_V1

## Purpose

This document defines the minimum acquisition-owned distributed retrieval semantics for future REFLECT evolution.

STATE.md remains canonical.

## Core Rule

Distributed acquisition may substitute acquisition surfaces.

Distributed acquisition must not substitute semantic truth.

## Authority Split

Selection chooses truth.

Retrieval obtains material.

Validation accepts or rejects material.

Acquisition orchestrates bounded retrieval of already-selected targets.

Acquisition must not become hidden topology authority.

## Minimum Distributed Acquisition Model

The minimum future distributed acquisition model is:

    selected publication state
    -> acquisition plan
    -> deterministic acquisition-surface order
    -> retrieval provider
    -> publication group
    -> traversal validation
    -> reconstruction

The selected publication-state identity remains fixed before distributed acquisition begins.

## Acquisition-Owned Responsibilities

Acquisition owns:

- selected target preservation
- traversal ordering
- bounded continuation eligibility
- bounded fallback eligibility
- deterministic acquisition-surface substitution
- runtime failure classification
- lifecycle result construction

Acquisition must not delegate these to retrieval providers.

## Forbidden Acquisition Behaviors

Acquisition must not:

- select publication state from retrieval results
- prefer faster surfaces
- prefer newer surfaces
- rank providers dynamically
- infer validity from availability
- mutate selected targets
- mutate traversal order
- perform adaptive reselection
- expose topology behavior
- create request telemetry
- persist cross-request acquisition history

## Provider Boundary Preservation

The retrieval-provider contract remains:

    getPublicationGroup({ target })

A distributed provider may internally map a target to acquisition material.

That mapping must remain an implementation detail.

The provider must remain replaceable by a dumb material fetcher without changing semantic truth.

## Continuation Boundary

Continuation remains acquisition-owned.

Continuation may invoke retrieval again for the same selected target.

Continuation must not disclose to the provider:

- prior failure history
- eligibility reason
- validation result
- attempt history
- selected-state rationale

## Fallback Boundary

Fallback remains acquisition-owned.

Fallback may replace the acquisition surface for an already-selected target.

Fallback must not replace:

- publication state
- object identity
- traversal order
- deterministic state target
- connector/chunk relationship

## Topology Neutrality

Distributed acquisition must be topology-neutral.

Infrastructure behavior may affect whether material is obtained.

Infrastructure behavior must not affect what counts as valid, selected, preferred, recent, or true.

## Local Acquisition Surface Runtime Realization

The local retrieval runtime now includes an explicit local acquisition surface.

Current runtime shape:

    acquisition target
        ->
    retrieval provider
        ->
    local acquisition surface
        ->
    publication registry
        ->
    publication material

The local acquisition surface is an internal acquisition surface only.

It remains:

- local
- deterministic
- topology-neutral
- non-authoritative

It does not select publication state, validate material, rank surfaces, own continuation, own fallback, or infer truth from availability.

Selection, validation, continuation, fallback, and lifecycle result construction remain acquisition-owned.

## Summary

The smallest safe distributed acquisition model is deterministic acquisition-surface substitution for already-selected targets.

Distributed acquisition may improve material availability.

It must not become selection, validity, ranking, telemetry, topology, continuation, or fallback authority.
