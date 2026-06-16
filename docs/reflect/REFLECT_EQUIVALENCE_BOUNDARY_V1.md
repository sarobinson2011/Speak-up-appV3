# REFLECT Equivalence Boundary V1

## Status

Engineering[55] equivalence-boundary review.

STATE.md remains canonical.

No runtime changes were introduced.

## Core Principle

Equivalence is not similarity.

Equivalence is not availability.

Equivalence is not provider agreement.

Equivalence is not carrier similarity.

Equivalence exists only when two REFLECT outcomes preserve the same selected truth.

    Selection chooses T.
    Preservation-state defines T.
    Continuity preserves T.
    Equivalence compares preservation outcomes.
    Validation demonstrates preservation.

## Equivalence Definition

Two REFLECT outcomes are equivalent only when their preservation-state is identical.

    Equivalent:
        preservation-state(A) == preservation-state(B)

    Not equivalent:
        preservation-state(A) != preservation-state(B)

    Undemonstrable:
        preservation cannot be confirmed

Equivalence answers:

    Are these outcomes preserving the same T?

not:

    Do these outcomes look similar?

not:

    Did they use the same provider, carrier, route, topology, or transport?

## Relationship To Continuity

Continuity asks:

    Did T remain T?

Equivalence asks:

    Do these outcomes preserve the same T?

Continuity is a preservation relationship over time.

Equivalence is a comparison relationship between outcomes.

Neither is an authority.

Neither selects truth.

## Required Equality

The required equality is preservation-state equality.

Current preservation-state examples include:

- selectedStateDigest
- contentDigest
- acquisitionKey
- sequence
- expected root
- expected leaf
- expected siblings
- expected path bits

If these identity-bearing values differ, the outcomes are not equivalent.

## Environment-State Is Not Equivalence

Environment-state may differ without breaking equivalence.

Examples:

- provider
- mirror
- source
- surface
- route
- topology
- transport
- endpoint
- retry behavior

Different environment-state does not imply different truth.

Same environment-state does not imply equivalent truth.

## Carrier-State Is Not Equivalence

Carrier-state transports preservation-state.

Carrier-state may provide evidence for preservation.

Carrier-state must not become equivalence authority.

Same descriptor, connector, or chunk shape is not sufficient.

Different carrier shape may still be acceptable if the same preservation-state is preserved and demonstrated.

## Derived-State Is Not Authority

Derived-state is produced by reconstruction.

Derived-state may demonstrate preservation only by matching expected preservation-state.

Derived-state must not replace preservation-state.

Similarity is insufficient.

Partial overlap is insufficient.

Repaired output is insufficient.

## Validation Relationship

Validation demonstrates equivalence.

Validation does not create equivalence.

Validation may confirm:

    reconstructed(T) == expected(T)

Validation must not infer:

    similar(T') == T

Validation success is evidence that preservation was demonstrated.

Validation must not become the definition of truth.

## False Equivalence Rules

REFLECT must never infer equivalence from:

- availability
- recency
- provider agreement
- mirror agreement
- route similarity
- topology similarity
- carrier similarity
- partial reconstruction
- repaired reconstruction
- successful acquisition alone
- validation convenience

The forbidden migration is:

    similarity -> equivalence

## Failure Rule

If equivalence cannot be demonstrated, the result is failure.

    Valid:
        T -> preserved(T)

    Valid:
        T -> fail

    Forbidden:
        T -> T'

Failure must not authorize repair, reselection, reconciliation, or truth substitution.

## Future Evolution Safety

Future REFLECT evolution may introduce:

- new providers
- new mirrors
- new acquisition surfaces
- new routing mechanisms
- new topology shapes
- new publication formats
- new carrier formats

provided equivalence remains anchored to preservation-state equality.

Evolution may change how T is acquired or carried.

Evolution must not change what makes T equal to T.

## Final Invariant

Equivalence is preservation-state equality.

Environment may differ.

Carrier may differ.

Acquisition path may differ.

Topology may differ.

Truth must not differ.

    Equivalent:
        T == T

    Not equivalent:
        T != T'

    Forbidden:
        similar(T') -> T
