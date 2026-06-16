# REFLECT_CONTINUITY_BOUNDARY_V1

## Status

Engineering[54] continuity-boundary review.

STATE.md remains canonical.

No runtime changes were introduced.

---

## Core Principle

Continuity is not a state class.

Continuity is not an authority.

Continuity is not an infrastructure property.

Continuity is the preservation relationship between Selection and Validation.

Selection chooses truth.

Preservation-state defines truth.

Continuity preserves truth.

Validation confirms truth remained preserved.

    Selection chooses T.

    Preservation-state defines T.

    Continuity preserves T.

    Validation confirms T remained T.

---

## Continuity Definition

REFLECT continuity exists when preservation-state remains identical across the authority chain.

The continuity question is:

    Did T remain T?

not:

    Was T available?

not:

    Was T easy to acquire?

not:

    Was T reconstructed successfully?

not:

    Was T validated successfully?

Continuity concerns truth preservation.

It does not concern operational success.

---

## Authority Relationship

Continuity is not a new authority layer.

The authority chain remains:

    selection
        ->
    target
        ->
    acquisition
        ->
    retrieved material
        ->
    reconstruction
        ->
    validation

Continuity spans this chain.

Continuity does not replace this chain.

No layer owns continuity as an independent authority.

Each layer participates in continuity by preserving already-selected truth.

---

## Continuity vs Availability

Availability and continuity are distinct properties.

Availability asks:

    Can T currently be obtained?

Continuity asks:

    Did T remain T?

Examples:

    T unavailable
        ->
    continuity unknown
        ->
    fail

    T available
        ->
    T changed
        ->
    continuity failed

Availability may assist continuity demonstration.

Availability does not define continuity.

Availability must not become truth authority.

---

## Continuity vs Environment Stability

Environment-state may evolve.

Examples:

- providers
- mirrors
- surfaces
- routes
- topology
- transport
- endpoints

Environment continuity is not truth continuity.

The following remains valid:

    T via environment A fails

    T via environment B succeeds

provided:

    T remains T

Environment substitution preserves continuity when preservation-state remains unchanged.

Environment stability is therefore continuity-neutral.

---

## Preservation-State Continuity

Preservation-state is the continuity anchor.

Preservation-state defines T.

If preservation-state changes:

    T changes

Examples:

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

Continuity exists only while preservation-state remains identical.

---

## Carrier Continuity

Carrier-state transports preservation-state.

Examples:

- descriptor
- connector
- chunk
- digest references

Carrier continuity is not truth continuity.

Carrier continuity matters only because carrier-state transports preservation-state.

Carrier-state must not become truth authority.

Carrier failure is acceptable only when acquisition-owned continuation or fallback can preserve the same selected truth.

Carrier replacement must not alter preservation-state.

---

## Reconstruction Continuity

Reconstruction interprets preserved carrier-state.

Reconstruction may:

- verify consistency
- assemble material
- derive reconstructed outputs

Reconstruction must not:

- select truth
- repair truth
- replace truth
- synthesize truth

Reconstruction continuity is not truth continuity.

Reconstruction participates in continuity by preserving preservation-state through interpretation.

If interpretation cannot preserve preservation-state:

    fail

not:

    repair

not:

    infer

not:

    replace

---

## Validation Continuity

Validation confirms continuity.

Validation does not create continuity.

Validation asks:

    Was preservation demonstrated?

Validation does not ask:

    What truth should exist?

Validation may:

- confirm preservation
- reject preservation

Validation must not:

- rewrite truth
- repair truth
- replace truth
- reconcile truth

Validation confirms continuity.

It does not determine continuity.

---

## Demonstrability Boundary

Continuity and continuity demonstration are distinct.

Continuity may exist independently of successful validation.

REFLECT intentionally adopts the rule:

    undemonstrable continuity
        ->
    fail

The system never infers preservation.

The system never assumes preservation.

The system requires preservation to be demonstrated.

Therefore:

    preservation confirmed
        ->
    success

    preservation not confirmed
        ->
    fail

This preserves explicit failure semantics.

---

## Continuity Migration Hazards

The following migrations are forbidden.

### Environment Continuity -> Truth Continuity

Examples:

- provider availability becomes truth
- mirror availability becomes truth
- route success becomes truth
- topology outcome becomes truth

### Carrier Continuity -> Truth Continuity

Examples:

- descriptor existence becomes truth
- connector existence becomes truth
- chunk availability becomes truth

### Derived Continuity -> Truth Continuity

Examples:

- reconstructed output replaces expected truth
- inferred output replaces expected truth
- repaired output replaces expected truth

### Validation Continuity -> Truth Continuity

Examples:

- successful validation creates truth
- validation failure determines alternate truth
- validation selects replacement truth

No downstream continuity class may become truth authority.

---

## Future Evolution Safety

Future REFLECT evolution may safely introduce:

- new providers
- new acquisition surfaces
- new topology shapes
- new publication formats
- new transport mechanisms

provided these changes do not alter preservation-state requirements.

Future evolution may modify environment-state and carrier-state.

Future evolution must not silently modify truth continuity requirements.

Any expansion of preservation-state requirements requires explicit STATE.md update first.

---

## Final Invariant

Selection chooses T.

Preservation-state defines T.

Continuity preserves T.

Validation confirms T remained T.

Success:

    T
        ->
    preserved(T)
        ->
    demonstrated(T)

Failure:

    T
        ->
    fail

Forbidden:

    T
        ->
    T'

Continuity is the preservation relationship between Selection and Validation.

Environment may change.

Truth may not.
