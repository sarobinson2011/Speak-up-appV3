# REFLECT Failure-Authority Model V1

## Status

Engineering[52] failure-authority review.

STATE.md remains canonical.

No runtime changes were introduced.

## Core Principle

Failure never creates new authority.

Selection chooses truth.

Every later layer is a preservation function over that selected truth.

If any layer cannot preserve selected truth, it must fail rather than acquire new authority.

    Selection chooses T.

    Every later layer preserves T.

    If preservation succeeds:

        T -> preserved(T)

    If preservation fails:

        T -> fail

    Forbidden:

        T -> T'

Failure may stop processing.

Failure may trigger bounded continuation where already authorized.

Failure must not reassign truth.

## Authority Rule

A layer may fail only within the responsibility it already owns.

A layer may classify only the failure it is permitted to observe.

No layer gains authority during failure that it does not possess during success.

## Failure-Origin Model

Failure may originate locally at any stage:

- acquisition failure
- retrieval/material failure
- reconstruction failure
- validation failure

The originating layer owns the local failure condition.

Failure origin does not imply truth authority.

## Detection Authority

Detection is local to the relevant boundary.

Acquisition may detect acquisition/material failure.

Reconstruction may detect reconstruction failure.

Validation may detect preservation-confirmation failure.

Detection does not authorize repair, reselection, substitution, or reinterpretation.

## Classification Authority

Failure classification is descriptive and bounded.

A layer may classify only what it is responsible for.

Examples:

- unavailable
- incomplete
- malformed
- incoherent
- invalid
- non-reconstructable
- preservation not confirmed

Classification must not become ranking.

Classification must not become truth selection.

Classification must not become repair authority.

Classification must not become routing authority.

A layer may describe why preservation failed.

It may not decide what new truth, source, topology, or route should replace the failed path.

## Rejection Authority

Validation owns preservation rejection.

Validation may conclude:

    preservation could not be confirmed

Validation must not conclude:

    alternate truth should be selected

    truth should be repaired

    fallback is authorized by validation

    newer or more available material should replace selected truth

Validation confirms or rejects preservation.

It does not determine truth.

## Acquisition Failure Authority

Acquisition owns bounded continuation and fallback.

Acquisition may continue or fallback only for the same selected target.

Fallback replaces acquisition surface.

Fallback must not replace truth.

    Valid fallback:

        T via surface A fails
        T via surface B succeeds

    Forbidden fallback:

        T via surface A fails
        T' via surface B succeeds

Acquisition may retry preservation.

Acquisition may not perform reselection.

## Reconstruction Failure Authority

Reconstruction owns interpretation of preserved material.

If preserved material cannot be reconstructed, reconstruction fails.

Reconstruction must not repair.

Reconstruction must not synthesize.

Reconstruction must not merge conflicting material.

Reconstruction must not reinterpret malformed material as valid truth.

    Valid reconstruction result:

        preserved(T) -> interpreted(T)

    Valid failure result:

        preserved(T) -> fail

    Forbidden result:

        partial(T) -> repaired(T)

## Validation Failure Authority

Validation owns final preservation confirmation.

If validation cannot confirm preservation, validation fails.

Validation failure is terminal unless an upstream authority already owns bounded continuation for the same selected target.

Validation failure must not become reselection.

Validation failure must not become repair authorization.

Validation failure must not become truth substitution.

## Fallback Boundary

Fallback is acquisition continuity authority only.

Fallback may preserve liveness.

Fallback may not alter selected truth.

Fallback may not mutate:

- selected publication state
- selected target
- selected object identity
- digest identity
- reconstruction semantics
- validation semantics

Fallback is valid only when it preserves the original selected truth.

## Chain Consistency

The success authority chain remains:

    Selection
        chooses truth

    Target
        preserves truth identity

    Acquisition
        preserves selected truth during acquisition

    Retrieved Material
        preserves acquired identity

    Reconstruction
        interprets preserved material

    Validation
        confirms preservation

The failure-authority chain must not contradict this.

During failure:

    Selection
        remains sole truth authority

    Target
        remains fixed identity

    Acquisition
        may continue/fallback for the same target

    Retrieved Material
        may be accepted, rejected, or absent

    Reconstruction
        may interpret or fail

    Validation
        may confirm or reject preservation

No layer after Selection may determine truth.

No layer may gain emergency authority.

## Forbidden Failure Behaviors

The following are forbidden:

- validation becoming selection
- fallback becoming reselection
- acquisition becoming repair
- reconstruction becoming synthesis
- retrieved material becoming reconciliation
- provider availability becoming validity
- topology becoming truth authority
- classification becoming ranking
- failure becoming adaptive routing authority
- termination becoming silent degradation

## Future Evolution Safety

Future REFLECT evolution may introduce:

- new acquisition surfaces
- new providers
- new publication formats
- new topology shapes
- new retrieval mechanisms

provided the following invariant remains true:

    Success path:

        T -> preserved(T)

    Failure path:

        T -> fail

    Forbidden path:

        T -> T'

New infrastructure may improve acquisition.

It must not change failure authority.

## Final Invariant

Failure is not a license to improvise truth.

Failure is only permission to:

- classify locally
- reject explicitly
- continue where already authorized
- fallback for the same selected target
- terminate safely

The simplest safe model is:

    preserve selected truth or fail.

Not:

    replace selected truth.
