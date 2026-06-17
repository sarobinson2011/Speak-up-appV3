# REFLECT Decision Boundary V1

Engineering[56] decision-authority review.

STATE.md is canonical.

## Core conclusion

Selection decides truth.

No later REFLECT layer decides truth.

Later layers may make bounded control or confirmation decisions only when those decisions preserve the already-selected truth.

Text model:

    Selection chooses T.

    No downstream layer may choose T'.

    Success:
        T -> preserved(T)

    Failure:
        T -> fail

    Forbidden:
        T -> decision -> T'

## Decision inventory

### Truth decision

Owner:

    Selection

Decision:

    choose T

Selection is the only truth-authority layer.

No downstream layer may:

- reselect truth
- repair truth
- rank truth
- reconcile truth
- substitute truth
- synthesize truth

### Control-flow decisions

Owner:

    Acquisition

Permitted decisions:

    continue
    retry
    fallback
    stop

These are control decisions, not truth decisions.

Acquisition may choose how to continue preservation of the same selected truth.

Acquisition must not choose a different truth.

Valid:

    T -> acquisition-control -> preserved(T)

Forbidden:

    T -> acquisition-control -> T'

### Confirmation decisions

Owner:

    Validation

Permitted decisions:

    confirm
    reject

Validation confirms whether preservation has been demonstrated.

Validation does not decide what truth should be preserved.

Valid:

    expected(T), derived(T) -> confirm

Valid:

    expected(T), derived(!T) -> reject

Forbidden:

    expected(T), derived(!T) -> accept(T')

## Failure boundary

Failure creates no new authority.

Failure may expose that preservation cannot continue.

Failure may trigger only decisions already authorized elsewhere.

Valid:

    failure -> stop

Valid only when acquisition already owns bounded continuation for the same selected truth:

    failure -> retry/fallback -> preserve(T)

Forbidden:

    failure -> emergency authority -> T'

## Continuity boundary

Continuity is descriptive.

Continuity answers:

    Did T remain T over time?

Continuity does not decide truth.

Continuity does not authorize fallback.

Continuity does not authorize replacement.

## Equivalence boundary

Equivalence is descriptive.

Equivalence answers:

    Do two outcomes preserve the same T?

Equivalent:

    preservation-state(A) == preservation-state(B)

Not equivalent:

    preservation-state(A) != preservation-state(B)

Equivalence does not authorize continuation, replacement, repair, or truth selection.

## Decision vs control

Control-flow authority is not truth authority.

A layer may control execution without controlling truth.

Example:

    fallback changes execution path

while:

    truth remains T

The valid distinction is:

    control(preserve(T))

not:

    control(choose(T'))

## Forbidden authority migrations

The following migrations are forbidden:

    validation -> truth selection
    equivalence -> continuation authorization
    continuity -> truth authority
    failure -> emergency authority
    availability -> truth authority
    provider agreement -> truth authority
    topology agreement -> truth authority
    fallback success -> replacement truth

## Future evolution rule

Future REFLECT evolution may introduce:

- new providers
- new acquisition surfaces
- new topology shapes
- new publication formats

only if the decision boundary remains unchanged.

New infrastructure may change how preservation is attempted.

It must not change who decides truth.

## Summary

    Truth authority:
        Selection

    Control authority:
        Acquisition

    Confirmation authority:
        Validation

    Failure:
        no independent authority

    Continuity:
        descriptive only

    Equivalence:
        descriptive only

    Success:
        T -> preserved(T)

    Failure:
        T -> fail

    Forbidden:
        T -> decision -> T'
