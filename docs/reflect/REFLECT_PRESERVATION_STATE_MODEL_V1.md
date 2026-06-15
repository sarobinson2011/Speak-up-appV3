# REFLECT Preservation-State Model V1

## Status

Engineering[53] preservation-state review.

STATE.md remains canonical.

No runtime changes were introduced.

## Core Principle

Preservation-state is the minimum identity-bearing state required to demonstrate that selected truth remains the same truth.

Selection creates preservation-state.

Every later layer either carries, preserves, interprets, confirms, or rejects that preservation-state.

No layer after Selection may create new preservation-state.

    Selection chooses T.

    Every later layer preserves T.

    Success:

        T -> preserved(T)

    Failure:

        T -> fail

    Forbidden:

        T -> T'

## State Classes

REFLECT state separates into four classes:

1. preservation-state
2. environment-state
3. carrier-state
4. derived-state

These classes must not silently migrate into one another.

## Preservation-State

Preservation-state defines T.

If preservation-state changes, T changes.

Current examples include:

- selectedStateDigest
- contentDigest
- acquisitionKey
- sequence
- expected root
- expected leaf
- expected siblings
- expected path bits

Preservation-state must remain stable across:

- acquisition
- continuation
- fallback
- retrieved material handling
- reconstruction
- validation

## Environment-State

Environment-state is machinery used to acquire, transport, route, or access preservation-state.

Current examples include:

- provider
- mirror
- source
- surface
- route
- topology
- transport
- endpoint
- retry behavior

Environment-state may evolve.

Environment-state may be substituted.

Environment-state may fail.

Environment-state must not redefine T.

## Carrier-State

Carrier-state transports preservation-state.

Current examples include:

- descriptor
- connector
- chunk
- descriptor contentDigest
- connector digest
- chunk digests

Carrier-state may carry truth identity.

Carrier-state must not become truth authority.

Carrier failure is preservation failure unless the same selected T can be acquired through an already-authorized acquisition path.

Carrier failure must not mutate preservation-state.

## Derived-State

Derived-state is produced by interpreting preserved carrier-state.

Current examples include:

- reconstructed leaf
- reconstructed root
- reconstructed siblings
- reconstructed path bits
- reconstructed depth
- reconstructed index

Derived-state is not authority.

Derived-state must match expected preservation-state.

If derived-state differs from expected preservation-state, the result is failure.

Derived-state must not replace preservation-state.

## Layer Model

### Selection

Selection chooses T and creates preservation-state.

Selection is the only truth-creating authority.

### Target

Target packages preservation-state into a stable acquisition identity object.

Target must not contain environment-state.

### Acquisition

Acquisition preserves preservation-state while operating over replaceable environment-state.

Acquisition may change surfaces.

Acquisition may not change T.

### Retrieved Material

Retrieved material carries preserved identity.

Retrieved material is not reconstructed truth.

### Reconstruction

Reconstruction interprets preserved carrier-state into derived-state.

Reconstruction must fail rather than repair, synthesize, or replace truth.

### Validation

Validation confirms equality between expected preservation-state and derived-state.

Validation confirms preservation.

Validation does not determine truth.

## Migration Hazards

The following migrations are forbidden:

### Environment-State -> Preservation-State

Examples:

- provider availability becomes truth
- newest mirror becomes truth
- routing outcome becomes truth
- fallback result becomes truth

### Carrier-State -> Preservation-State

Examples:

- descriptor claims become truth without validation
- connector material becomes authority
- chunk availability becomes correctness

### Derived-State -> Preservation-State

Examples:

- reconstructed output replaces expected truth
- partial reconstruction becomes sufficient truth
- validation accepts repaired or inferred material

## Future Evolution Safety

Future REFLECT evolution may introduce:

- new providers
- new acquisition surfaces
- new topology shapes
- new publication formats
- new transport mechanisms

provided these changes affect environment-state or carrier-state only.

Future evolution must not increase preservation-state requirements unless STATE.md is explicitly updated first.

## Final Invariant

Preservation-state is small and stable.

Environment-state may evolve.

Carrier-state may transport.

Derived-state may interpret.

Validation may confirm.

No downstream layer may silently turn:

    T -> T'
