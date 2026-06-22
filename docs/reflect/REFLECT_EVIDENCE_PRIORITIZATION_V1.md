# REFLECT Evidence Prioritization V1

Engineering[65]

STATE.md remains canonical. If this document conflicts with STATE.md, STATE.md wins.

## Scope

This document prioritizes the remaining REFLECT evidence gaps identified after Engineering[64].

It does not introduce new REFLECT semantics.

It does not modify runtime behavior.

It does not add tests.

It does not reopen Engineering[49] through Engineering[64].

The question answered here is not:

    what does REFLECT mean?

The question answered here is:

    which remaining evidence gaps justify future effort?

## Decision Rule

An evidence gap deserves future effort only when additional evidence would materially reduce risk.

Priority is based on:

- impact if violated
- likelihood of future drift
- detectability of violation
- existing evidence strength
- future value of additional evidence

Important invariant does not automatically mean high priority.

The relevant distinction is:

    important and already well evidenced
        -> low or no priority

    important and weakly evidenced
        -> medium or high priority

## Prioritization Summary

| Gap | Priority | Recommended Outcome |
|---|---:|---|
| Selected-state preservation during acquisition | High | Future regression coverage |
| Cross-state mixing prevention | High | Future regression coverage |
| Fallback eligibility preservation | Medium | Future regression coverage |
| Digest and coherence enforcement | Medium | Future runtime review |
| Provider authority containment | Medium | Documentation clarification |
| Evidence localization across REFLECT docs | Low | Documentation clarification |
| Semantic closure evidence | None | Defer indefinitely |
| Mirror topology semantics | None | Defer indefinitely |
| Trust / acceptance / authority model evidence | None | Defer indefinitely |

## 1. Selected-State Preservation During Acquisition

### Invariant

Once REFLECT selects publication-state truth, later acquisition must preserve that selected state.

Acquisition may retrieve material.

Acquisition may fail.

Acquisition may use substitute acquisition surfaces.

Acquisition must not silently select a different publication state.

### Existing Evidence

Existing REFLECT work repeatedly distinguishes:

- selection chooses truth
- acquisition retrieves already-selected targets
- validation accepts or rejects retrieved material
- acquisition surfaces are replaceable machinery

Engineering[42] and later reviews support this model.

### Consequence If Violated

High.

A violation would let a downstream layer silently replace T with T'.

That would break the central REFLECT preservation model.

### Likelihood Of Drift

medium

This is a natural future drift risk because implementation convenience may tempt acquisition code to recover from failure by selecting a nearby or newer state.

### Detectability

difficult

A wrong-state substitution could still return structurally valid material unless explicitly checked.

### Additional Evidence Value

high

Regression evidence would materially reduce risk.

### Priority

high

### Recommended Outcome

future regression coverage

### Rationale

This is one of the few remaining gaps where a violation could be both serious and subtle.

Future coverage should prove:

    selected(T) -> acquired(T)

and forbid:

    selected(T) -> acquired(T')

## 2. Cross-State Mixing Prevention

### Invariant

REFLECT must not construct a usable result by mixing connector, chunk, continuation, or fallback material from incompatible publication states.

### Existing Evidence

Engineering[61] and Engineering[62] directly addressed cross-state mixing and added a regression harness.

STATE.md also locks no cross-state mixing as a REFLECT Phase A property.

### Consequence If Violated

High.

Cross-state mixing could produce incoherent witness data while appearing superficially complete.

### Likelihood Of Drift

low

Existing evidence is strong, but future implementation expansion could reintroduce risk at new boundaries.

### Detectability

difficult

Mixed-state material may not fail obviously without digest/coherence checks.

### Additional Evidence Value

medium

The core invariant is already evidenced, but future changes should preserve coverage.

### Priority

high

### Recommended Outcome

future regression coverage

### Rationale

This invariant is already strongly established, but it is central enough and subtle enough that future implementation work should keep regression coverage attached to it.

## 3. Fallback Eligibility Preservation

### Invariant

Fallback may substitute acquisition surfaces for the same selected object.

Fallback must not become reselection.

Fallback must not perform global reshuffle.

Fallback must not use failure as authority to choose a different truth state.

### Existing Evidence

REFLECT Phase A explicitly locks:

- 2 fallback mirrors per object
- no global reshuffle during fallback
- deterministic state targeting
- no cross-state mixing

Prior REFLECT reviews also keep fallback acquisition-owned rather than authority-owned.

### Consequence If Violated

High.

Fallback is one of the most tempting places for semantic drift because failure-handling code often tries to repair state.

### Likelihood Of Drift

medium

Future distributed acquisition work could accidentally widen fallback behavior.

### Detectability

moderate

Some violations would be visible in tests or logs, but silent replacement remains possible if not specifically asserted.

### Additional Evidence Value

medium

Additional evidence is useful when fallback implementation expands.

### Priority

medium

### Recommended Outcome

future regression coverage

### Rationale

No immediate semantic work is needed.

Future implementation work should include regression cases proving:

    fallback(surface(T)) -> surface'(T)

and forbidding:

    fallback(surface(T)) -> surface(T')

## 4. Digest And Coherence Enforcement

### Invariant

REFLECT must verify integrity and coherence across selected objects before material becomes usable.

### Existing Evidence

STATE.md locks integrity and coherence verification across selected objects.

Prior REFLECT work established digest/coherence as preservation evidence rather than optional metadata.

### Consequence If Violated

High.

Weak digest or coherence enforcement could allow malformed, stale, or mismatched material to be accepted.

### Likelihood Of Drift

low

The semantic model is clear, but implementation-level enforcement can regress through refactor or convenience handling.

### Detectability

moderate

Some failures are easy to detect; partial or boundary-specific weakening may not be.

### Additional Evidence Value

medium

A future runtime review would be valuable once REFLECT implementation expands further.

### Priority

medium

### Recommended Outcome

future runtime review

### Rationale

This is less a semantic gap than an implementation-discipline risk.

Do not reopen the model.

Review actual enforcement when implementation surface grows.

## 5. Provider Authority Containment

### Invariant

Retrieval providers are acquisition surfaces only.

They must not become selection, validation, ranking, telemetry, topology, continuation, or fallback authority.

### Existing Evidence

Engineering[40], Engineering[41], Engineering[42], and Engineering[43] strongly constrain provider evolution.

The current model treats the acquisition target as the retrieval identity surface and keeps providers subordinate to the acquisition plan.

### Consequence If Violated

Medium to high.

Provider authority creep could reintroduce topology or availability as hidden truth authority.

### Likelihood Of Drift

medium

Future provider expansion is a likely pressure point.

### Detectability

moderate

Some provider widening is visible in interfaces; subtle semantic widening through naming, logging, or helper logic may be harder to detect.

### Additional Evidence Value

medium

Additional documentation localization is useful before future provider work.

### Priority

medium

### Recommended Outcome

documentation clarification

### Rationale

The semantic evidence is strong.

The useful future work is not more architecture.

The useful work is keeping the provider rule easy to find before implementation resumes.

## 6. Evidence Localization Across REFLECT Docs

### Invariant

A reviewer should be able to locate the evidence supporting REFLECT preservation invariants without reconstructing the entire Engineering[49]-[64] chain.

### Existing Evidence

The evidence exists across many REFLECT documents and STATE.md checkpoints.

### Consequence If Violated

Low.

Poor localization does not itself weaken runtime semantics.

It may slow review and increase the chance of future misunderstanding.

### Likelihood Of Drift

medium

As docs accumulate, evidence can become harder to find.

### Detectability

easy

Reviewers will notice when evidence is scattered.

### Additional Evidence Value

low

Useful, but not urgent.

### Priority

low

### Recommended Outcome

documentation clarification

### Rationale

This is a documentation-maintenance issue.

It does not justify runtime work or new tests.

## 7. Semantic Closure Evidence

### Invariant

REFLECT semantic closure remains intact unless direct contradictory evidence appears.

### Existing Evidence

Engineering[43] and Engineering[63] already concluded that remaining REFLECT risks are implementation-discipline and evidence-strengthening risks, not unresolved semantic-frontier risks.

### Consequence If Violated

High in theory, but no current unresolved contradiction exists.

### Likelihood Of Drift

very low

### Detectability

easy

A genuine semantic contradiction would be visible during review because it would conflict with STATE.md or existing REFLECT boundary documents.

### Additional Evidence Value

negligible

### Priority

none

### Recommended Outcome

defer indefinitely

### Rationale

More semantic closure documentation would mostly duplicate existing conclusions.

No further work is justified unless a concrete contradiction is discovered.

## 8. Mirror Topology Semantics

### Invariant

Mirrors are replaceable publication surfaces.

Mirror topology must not become authority.

### Existing Evidence

STATE.md locks a fixed 7-mirror REFLECT Phase A set and documents mirror selection, fallback, connector separation, deterministic targeting, and no global reshuffle.

Prior REFLECT documents repeatedly demote mirrors to replaceable surfaces.

### Consequence If Violated

Medium.

Topology authority would be harmful, but the current Phase A model is already tightly bounded.

### Likelihood Of Drift

very low

No active distributed mirror evolution is currently being implemented.

### Detectability

easy

Topology expansion would be visible in docs, config, or runtime interfaces.

### Additional Evidence Value

negligible

### Priority

none

### Recommended Outcome

defer indefinitely

### Rationale

No current work depends on further mirror-topology evidence.

Reopen only if distributed mirror implementation resumes.

## 9. Trust / Acceptance / Authority Model Evidence

### Invariant

Trust, acceptance, validation, acquisition, retrieval, and selection remain separate.

No downstream layer may become selection authority.

### Existing Evidence

Engineering[49] through Engineering[58] decomposed the authority, acceptance, decision, equivalence, continuity, preservation, failure, and trust boundaries.

Engineering[64] confirmed semantic closure remains intact.

### Consequence If Violated

High.

But this is already one of the best-evidenced REFLECT areas.

### Likelihood Of Drift

very low

### Detectability

easy to moderate

Model-level violations are usually visible in terminology, docs, interfaces, or tests.

### Additional Evidence Value

negligible

### Priority

none

### Recommended Outcome

defer indefinitely

### Rationale

This area is architecturally important but already sufficiently evidenced.

Additional work would be low-value repetition.

## Future Work Queue

The only future REFLECT evidence work currently justified is:

1. future regression coverage for selected-state preservation
2. future regression coverage for cross-state mixing preservation during implementation expansion
3. future regression coverage for fallback eligibility preservation
4. future runtime review of digest/coherence enforcement when implementation expands
5. lightweight documentation clarification around provider authority containment

Everything else can be deferred.

## Non-Goals

This document does not authorize:

- new trust model
- new acceptance model
- new fallback model
- new acquisition model
- new mirror model
- adaptive routing
- distributed mirror evolution
- authority redistribution
- runtime modification
- test implementation

## Conclusion

Engineering[65] confirms that remaining REFLECT work is not architecture work.

The only remaining justified work is selective evidence-strengthening.

Most gaps can safely be deferred because semantic closure is already established and existing evidence is sufficient.

Priority should attach only to gaps where future drift could be silent, materially harmful, and difficult to detect.
