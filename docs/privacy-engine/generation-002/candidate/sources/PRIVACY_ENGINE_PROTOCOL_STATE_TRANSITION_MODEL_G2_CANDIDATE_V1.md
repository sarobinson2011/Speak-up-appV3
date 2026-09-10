<a id="pe-g2-art-pe-g2-source-s27"></a>
# Privacy Engine Protocol State Transition Model G2 Candidate V1

Successor source artifact: PE-G2-SOURCE-S27

Successor generation: PE-PROTOCOL-GENERATION-002

Immutable predecessor: docs/PRIVACY_ENGINE_PROTOCOL_STATE_TRANSITION_MODEL_V1.md

Immutable predecessor SHA-256: 0eb986ffa0094434b93ee5b3c371ad321be8af0f2d9992997daeeec642b92be9

Status: candidate; unreviewed; unpublished; non-authoritative.

All inherited V1 identity, review, publication and current-generation statements below are predecessor derivation text concerning G1 only. They do not assert G2 identity, review, publication or authority. G2 candidate meaning is established by the successor semantic-obligation register and exact section bindings.

## Successor Candidate Semantic-Obligation Register

| Source anchor | Engineering trace input | Successor requirement | Exact successor rule |
|---|---|---|---|
| <a id="pe-g2-src-s27-clar-atomic-010-01"></a> pe-g2-src-s27-clar-atomic-010-01 | CLAR-ATOMIC-010 | PE-G2-FAIL-019 | Failure of representation, serialization, persistence, publication, transport, operational delivery, display, indexing or application translation after Determination production MUST NOT erase the Determination, reopen or fail the completed Evaluation, alter its acceptance or rejection classification, or become protocol rejection. |
| <a id="pe-g2-src-s27-clar-atomic-011-01"></a> pe-g2-src-s27-clar-atomic-011-01 | CLAR-ATOMIC-011 | PE-G2-STALEAUTH-013 | Retry of a later representation, publication, transport or delivery operation MUST preserve the same already-produced Determination and MUST NOT produce another Determination or another Evaluation occurrence. |
| <a id="pe-g2-src-s27-clar-atomic-012-01"></a> pe-g2-src-s27-clar-atomic-012-01 | CLAR-ATOMIC-012 | PE-G2-STALEAUTH-014 | A terminally failed Evaluation MUST NOT later become complete. |
| <a id="pe-g2-src-s27-clar-atomic-012-02"></a> pe-g2-src-s27-clar-atomic-012-02 | CLAR-ATOMIC-012 | PE-G2-STALEAUTH-015 | Any later authoritative re-evaluation MUST instantiate a new Evaluation occurrence and MUST preserve the failed occurrence without mutation, repair or reinterpretation. |
| <a id="pe-g2-src-s27-clar-atomic-015-01"></a> pe-g2-src-s27-clar-atomic-015-01 | CLAR-ATOMIC-015 | PE-G2-SEMPRES-027 | Every Evaluation, Determination, failure, retry, representation, publication, transport, delivery, diagnostic and observability surface MUST preserve Private Actor non-disclosure, neutral naming, action-bounded public identity and the prohibition on reusable participant identity, actor provenance and cross-action linkage. |

STATE.md remains canonical.

<a id="pe-g2-src-s27-sec-001-000"></a>
# 1. Purpose

This document defines the architectural model of a Privacy Engine Protocol State
Transition.

A Protocol State Transition is the bounded public protocol-state consequence
that may follow an accepted Protocol Action Determination.

This document determines:

- whether Protocol State Transition is a distinct first-class architectural
  subject;
- how one transition is identified;
- how transition authorization derives from an accepted Determination;
- how authorization differs from execution;
- how execution differs from commitment;
- how commitment changes protocol state;
- how transition failure is classified;
- how stale authorization and conflicting state are handled;
- how transition correctness and atomicity are preserved;
- how committed transitions enter protocol-state history;
- how public state consequences preserve private-actor privacy.

This document does not redefine Protocol Actions, Protocol Action Evaluations,
Protocol Action Determinations, implementations, applications, or protocol
authority.

<a id="pe-g2-src-s27-sec-002-000"></a>
# 2. Scope

This model is limited to the architecture of one Protocol State Transition and
its immediate relationships to:

- one published Privacy Engine protocol generation;
- one authorizing Protocol Action Determination;
- one bounded pre-transition protocol state;
- one bounded post-transition protocol state;
- one protocol-defined state-change relation;
- transition authorization;
- transition execution;
- transition commitment;
- transition failure;
- transition correctness;
- implementation realization;
- protocol-state history;
- observable public protocol consequence.

Let:

- `P` be one published Privacy Engine protocol generation;
- `I` be one implementation;
- `A` be one Protocol Action;
- `E` be one Protocol Action Evaluation;
- `D` be one Protocol Action Determination;
- `Q0` be one bounded pre-transition protocol state;
- `Q1` be one bounded post-transition protocol state;
- `Qx` be one materially different current protocol state;
- `U` be one Protocol State Transition;
- `R` be one protocol-defined state-change relation;
- `H` be one protocol-state history.

<a id="pe-g2-src-s27-sec-003-000"></a>
# 3. Proposed Subject

The proposed subject is the Privacy Engine Protocol State Transition.

The proposed subject is not assumed to be first-class merely because transition
authorization, execution, commitment, and failure require separate explanation.

The assessment must determine whether the proposed subject:

- possesses independent architectural identity;
- possesses a bounded lifecycle;
- owns a protocol-state relation not owned by an existing subject;
- possesses correctness conditions distinct from Action validity and
  Determination correctness;
- may succeed or fail independently of the correctness of its authorizing
  Determination;
- creates a public protocol-state consequence not created by the Action or
  Determination alone.

The candidate subject is:

> A bounded protocol-governed occurrence capable of completely changing one
> applicable protocol state into another protocol-defined protocol state.

<a id="pe-g2-src-s27-sec-004-000"></a>
# 4. Architectural Subject Assessment

<a id="pe-g2-src-s27-sec-004-001"></a>
## 4.1 Identity test

A Protocol State Transition possesses occurrence identity distinct from the
identity of its authorizing Action, Evaluation, and Determination.

One accepted Determination may authorize no transition.

One accepted Determination may authorize one transition.

One accepted Determination may authorize multiple separately identified
transitions.

Therefore, transition identity cannot be reduced to Determination identity.

> U != A

> U != E

> U != D

> identifiesTransition(id(U), U)

<a id="pe-g2-src-s27-sec-004-002"></a>
## 4.2 Semantic independence test

The Determination records whether the Protocol Action is accepted or rejected.

The transition records whether an authorized protocol-state change is completely
committed.

These meanings are not equivalent.

> accepts(D, A) =/=> committed(U)

> authorizedBy(U, D) =/=> committed(U)

An accepted Action may require no transition.

An authorized transition may fail after the Determination is complete.

A committed transition creates a protocol-state consequence that acceptance
alone does not create.

<a id="pe-g2-src-s27-sec-004-003"></a>
## 4.3 Lifecycle independence test
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-010,CLAR-ATOMIC-011; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-010-01,pe-g2-src-s27-clar-atomic-011-01; successor-requirements=PE-G2-FAIL-019,PE-G2-STALEAUTH-013; status=candidate-unreviewed-unpublished-non-authoritative.


A Determination is complete when its Evaluation produces its authoritative
acceptance or rejection result.

A transition may then possess a bounded lifecycle containing:

- authorization;
- pre-transition state validation;
- execution;
- commitment; or
- failure.

The transition lifecycle may continue after the Determination is complete.

Transition failure does not reopen or rewrite the completed Evaluation.

> transitionFailure(U) =/=> evaluationFailure(E)

> transitionFailure(U) =/=> rejects(D, A)

<a id="pe-g2-src-s27-sec-004-004"></a>
## 4.4 State-relation test

A Protocol State Transition owns the bounded relationship between:

- `Q0`, the applicable pre-transition protocol state;
- `R`, the protocol-defined state-change relation;
- `Q1`, the resulting post-transition protocol state.

Neither the Protocol Action nor its Determination independently establishes that
state change.

> transitions(U, Q0, Q1)

> appliesStateChangeRelation(U, R)

<a id="pe-g2-src-s27-sec-004-005"></a>
## 4.5 Correctness-independence test
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-010,CLAR-ATOMIC-011; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-010-01,pe-g2-src-s27-clar-atomic-011-01; successor-requirements=PE-G2-FAIL-019,PE-G2-STALEAUTH-013; status=candidate-unreviewed-unpublished-non-authoritative.


A correct Determination may authorize a transition that later fails because:

- applicable protocol state has changed;
- required execution cannot begin;
- execution cannot preserve the authorized transition;
- infrastructure cannot complete execution;
- commitment cannot be established.

Such failure does not make the earlier correct Determination incorrect.

Transition correctness therefore possesses requirements distinct from
Determination correctness.

<a id="pe-g2-src-s27-sec-004-006"></a>
## 4.6 Public-consequence test

A committed Protocol State Transition changes public protocol state.

An accepted Determination may exist without such a state change.

The transition therefore possesses a public consequence that is not merely
another name for Action acceptance.

<a id="pe-g2-src-s27-sec-005-000"></a>
# 5. Architectural Subject Conclusion

Protocol State Transition is a distinct first-class architectural subject.

It possesses:

- independent occurrence identity;
- a bounded protocol-state relation;
- a bounded lifecycle;
- distinct correctness conditions;
- independent success and failure semantics;
- a distinct public protocol-state consequence.

The model does not reduce to Protocol Action or Protocol Action Determination
semantics.

Transition authorization, transition execution, transition commitment, and
transition failure are not separate first-class architectural subjects.

They are bounded relationships, stages, predicates, or classifications within
one Protocol State Transition model.

They do not possess independent protocol identity, semantic authority, or
lifecycle outside the transition they describe.

Implementation-level execution attempts may possess operational identifiers.

Those identifiers do not become Privacy Engine architectural identities.

<a id="pe-g2-src-s27-sec-006-000"></a>
# 6. Primary Definition

A Privacy Engine Protocol State Transition is one identified, bounded,
protocol-governed state-change occurrence whose successful commitment completely
changes one applicable pre-transition protocol state into one protocol-defined
post-transition protocol state.

> transitions(U, Q0, Q1)

> governedBy(U, P)

> appliesStateChangeRelation(U, R)

> executedThrough(U, I)

The identity of `U` remains fixed throughout authorization, execution, and
commitment.

Authorization does not itself change protocol state.

Execution does not itself establish a committed protocol-state change.

Only complete commitment establishes the transition from `Q0` to `Q1`.

<a id="pe-g2-src-s27-sec-007-000"></a>
# 7. Transition Identity

Every Protocol State Transition possesses its own transition-occurrence
identity.

Transition identity identifies exactly one bounded transition occurrence.

It may identify relationships to:

- one authorizing Determination;
- one applicable pre-transition protocol state;
- one protocol-defined state-change relation;
- one post-transition protocol state;
- one implementation through which execution occurs.

Transition identity is not:

- Protocol Action identity;
- Evaluation identity;
- Determination identity;
- implementation identity;
- application identity;
- actor identity.

> identifiesTransition(id(U), U)

> identifiesTransition(id(U), U) =/=> identifiesAction(id(U), A)

> identifiesTransition(id(U), U) =/=> identifiesDetermination(id(U), D)

> identifiesTransition(id(U), U) =/=> identifiesImplementation(id(U), I)

> identifiesTransition(id(U), U) =/=> identifiesActor(id(U), X)

Transition identity must not contain or reconstruct private-actor identity.

<a id="pe-g2-src-s27-sec-008-000"></a>
# 8. Transition Scope and Boundedness

Every Protocol State Transition is bounded by:

- one transition identity;
- one published protocol generation;
- one authorizing Determination;
- one applicable pre-transition protocol state;
- one protocol-defined state-change relation;
- one defined post-transition protocol state;
- one semantic commitment boundary.

A transition may contain several protocol-required state effects when those
effects together form one indivisible protocol-defined state change.

Those effects remain parts of one transition.

They do not become independently committable merely because an implementation
performs them through several instructions, calls, writes, or internal steps.

If several state changes may commit independently, they are separately
identified Protocol State Transitions.

If the protocol requires several effects to succeed or fail together, they form
one composite but semantically atomic Protocol State Transition.

Implementation structure does not determine transition scope.

The published protocol rules determine transition scope.

<a id="pe-g2-src-s27-sec-009-000"></a>
# 9. Transition Lifecycle
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-010,CLAR-ATOMIC-011; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-010-01,pe-g2-src-s27-clar-atomic-011-01; successor-requirements=PE-G2-FAIL-019,PE-G2-STALEAUTH-013; status=candidate-unreviewed-unpublished-non-authoritative.


The bounded transition lifecycle may include:

> authorized(U)

> executable(U)

> executing(U)

> committed(U)

or:

> transitionFailure(U)

Authorization, execution, commitment, and failure describe the state of the same
identified `U`.

They do not create separate architectural objects.

A transition must not simultaneously possess successful and failed terminal
classifications.

> committed(U) xor transitionFailure(U)

This exclusivity applies once the transition has reached a terminal
classification.

An authorized transition that has not completed is neither committed nor
necessarily failed.

> authorized(U) =/=> committed(U)

> not committed(U) =/=> transitionFailure(U)

<a id="pe-g2-src-s27-sec-010-000"></a>
# 10. Pre-Transition Protocol State

The pre-transition protocol state is the bounded protocol state against which
the transition is authorized.

> authorizedAgainst(U, Q0)

`Q0` contains only the protocol-relevant state required to define and validate
the transition.

It does not require disclosure or reconstruction of private-actor identity.

The pre-transition state must be sufficiently defined to determine:

- whether the transition remains applicable;
- whether the authorized state-change relation can be preserved;
- whether execution may begin;
- whether commitment may occur.

The implementation must not select or reconstruct a preferred pre-transition
state after authorization.

> authorizedAgainst(U, Q0)

> not equivalentTransitionState(Qx, Q0)

> -> not maySubstitutePreState(U, Qx)

<a id="pe-g2-src-s27-sec-011-000"></a>
# 11. Post-Transition Protocol State

The post-transition protocol state is the complete protocol-defined result of
successfully applying the authorized state-change relation to the applicable
pre-transition state.

> definesPostState(U, Q1)

> transitions(U, Q0, Q1)

`Q1` must preserve every protocol-relevant result required by `U`.

The implementation must not:

- omit required state effects;
- add unauthorized state effects;
- replace `Q1` with a preferred state;
- infer additional application meaning;
- introduce private-actor identity;
- report a partially produced state as the complete `Q1`.

A post-transition state becomes authoritative for this transition only through
commitment.

> definesPostState(U, Q1) =/=> committed(U)

> committed(U) -> establishesPostState(U, Q1)

<a id="pe-g2-src-s27-sec-012-000"></a>
# 12. Protocol-Defined State Change

Every Protocol State Transition applies one protocol-defined state-change
relation.

> appliesStateChangeRelation(U, R)

> stateChangeRelationOf(R, P)

> applies(U, R, Q0) -> producesState(R, Q0, Q1)

The state-change relation determines the protocol-relevant relationship between
`Q0` and `Q1`.

The implementation realizes that relation.

The implementation does not define, widen, narrow, repair, or replace it.

> implementationRealizes(I, R)

> implementationRealizes(I, R) =/=> implementationDefines(I, R)

Application interpretation does not alter the protocol-defined state-change
relation.

<a id="pe-g2-src-s27-sec-013-000"></a>
# 13. Transition Authorization

Transition authorization is the bounded relationship that permits one
identified transition to proceed from one accepted Determination.

> accepts(D, A)

> authorizes(D, U)

> authorizedBy(U, D)

> authorizedAgainst(U, Q0)

Authorization selects `U`.

It does not merely select a class of preferred outcomes from which an
implementation may later choose.

The authorized transition must already be sufficiently bounded to preserve:

- its transition identity;
- its applicable pre-transition state;
- its protocol-defined state-change relation;
- its required post-transition state;
- its semantic atomicity.

Authorization is not commitment.

> authorizes(D, U) =/=> committed(U)

Authorization is not execution.

> authorizes(D, U) =/=> executing(U)

Authorization does not itself change protocol state.

> authorizes(D, U) =/=> transitionsCommittedState(Q0, Q1)

<a id="pe-g2-src-s27-sec-014-000"></a>
# 14. Relationship to Accepted Determinations
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-010,CLAR-ATOMIC-011; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-010-01,pe-g2-src-s27-clar-atomic-011-01; successor-requirements=PE-G2-FAIL-019,PE-G2-STALEAUTH-013; status=candidate-unreviewed-unpublished-non-authoritative.


Only an accepted Protocol Action Determination may authorize a transition
arising from that Protocol Action.

> authorizedBy(U, D) -> accepts(D, A)

A rejected Determination must not authorize an accepted transition.

> rejects(D, A)

> -> not authorizesAcceptedTransition(D, U)

Acceptance does not require a transition.

> accepts(D, A) =/=> exists(U)

Acceptance does not establish commitment.

> accepts(D, A) =/=> committed(U)

The complete applicable protocol rules determine whether one accepted
Determination authorizes:

- zero transitions;
- exactly one transition;
- multiple separately identified transitions.

The implementation must not choose transition cardinality for convenience.

Where:

> authorizedBy(U1, D)

> authorizedBy(U2, D)

> U1 != U2

`U1` and `U2` are separately identified and separately atomic transitions.

Protocol-defined dependencies or ordering between them must be preserved.

If the protocol requires all represented state effects to succeed or fail
together, those effects must instead be represented by one composite atomic
transition.

No separate first-class transition-set object is introduced.

<a id="pe-g2-src-s27-sec-015-000"></a>
# 15. Transition Execution

Transition execution is the bounded implementation activity that attempts to
realize the already-authorized transition.

> executedThrough(U, I)

> executes(I, U)

Execution must preserve:

- `id(U)`;
- the authorizing Determination;
- the authorized pre-transition state;
- the protocol-defined state-change relation;
- the required post-transition state;
- transition atomicity.

Execution does not possess independent protocol authority.

Execution may realize `U`.

It may not redefine `U`.

> executes(I, U) =/=> defines(I, U)

Implementation instructions, transaction formats, internal calls, database
operations, storage writes, or retry attempts do not create additional
architectural transition identities.

Execution remains subordinate to the authorized transition.

<a id="pe-g2-src-s27-sec-016-000"></a>
# 16. Transition Commitment

Transition commitment is the successful terminal predicate of one Protocol
State Transition.

Commitment establishes that the complete authorized state change from `Q0` to
`Q1` has occurred.

> committed(U) -> authorizedBy(U, D)

> committed(U) -> executedThrough(U, I)

> committed(U) -> transitions(U, Q0, Q1)

> committed(U) -> completeStateChange(U, Q0, Q1)

> committed(U) -> establishesPostState(U, Q1)

Commitment does not require a separate first-class result object.

It has no architectural identity, authority, or lifecycle independent of `U`.

An implementation report does not itself establish commitment.

> reportsCommitted(I, U) =/=> committed(U)

Commitment is correct only when the protocol-defined transition has been
completely and correctly realized.

<a id="pe-g2-src-s27-sec-017-000"></a>
# 17. Transition Completeness and Atomicity

Every committed Protocol State Transition is semantically complete and atomic.

Atomicity means that one transition either establishes its complete
protocol-defined state change or establishes no committed state change.

> committed(U) iff completeStateChange(U, Q0, Q1)

Within this equivalence, `completeStateChange(U, Q0, Q1)` requires:

- valid authorization;
- preservation of transition identity;
- applicability of the authorized pre-transition state;
- execution of the complete protocol-defined state-change relation;
- establishment of the required post-transition state;
- absence of unauthorized state effects;
- satisfaction of transition atomicity.

A partial state change is not a committed transition.

> partialStateChange(U) =/=> committed(U)

> partialExecution(U) =/=> committed(U)

> committed(U) -> not partiallyCommitted(U)

Semantic atomicity does not prescribe:

- blockchain transaction mechanics;
- database transaction mechanics;
- consensus mechanisms;
- locking algorithms;
- rollback algorithms;
- storage layouts;
- instruction order;
- infrastructure topology.

Implementations may realize atomicity differently while preserving equivalent
protocol semantics.

<a id="pe-g2-src-s27-sec-018-000"></a>
# 18. Transition Preservation and Prohibited Substitution

Authorization chooses `U`.

Every later transition stage preserves `U`.

If execution cannot preserve `U`, it must fail cleanly.

It must not replace `U` with `U'`.

Success path:

> accepts(D, A)

> and authorizedBy(U, D)

> and executes(I, U)

> and completeStateChange(U, Q0, Q1)

> -> committed(U)

No-transition path:

> accepts(D, A)

> and noTransitionRequired(D)

> -> not existsAuthorizedTransition(U, D)

Failure path:

> authorizedBy(U, D)

> and not canPreserveExecution(I, U)

> -> transitionFailure(U)

Forbidden substitution path:

> authorizedBy(U, D)

> and executes(I, U')

> and U' != U

> -> incorrectExecution(I, U')

Forbidden commitment path:

> authorizedBy(U, D)

> and executes(I, U')

> and U' != U

> -> not mayReportCommitted(I, U)

Forbidden partial path:

> authorizedBy(U, D)

> and partiallyApplies(I, U)

> -> not committed(U)

An implementation must not:

- repair `U`;
- widen `U`;
- narrow `U`;
- substitute `U`;
- merge `U` with another transition;
- infer a preferred `U'`;
- partially commit `U`;
- report `U'` as committed `U`.

<a id="pe-g2-src-s27-sec-019-000"></a>
# 19. Transition Failure
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-012; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-010-01,pe-g2-src-s27-clar-atomic-011-01,pe-g2-src-s27-clar-atomic-012-01,pe-g2-src-s27-clar-atomic-012-02; successor-requirements=PE-G2-FAIL-019,PE-G2-STALEAUTH-013,PE-G2-STALEAUTH-014,PE-G2-STALEAUTH-015; status=candidate-unreviewed-unpublished-non-authoritative.


Transition failure is the explicit terminal classification of an authorized
transition execution that does not establish complete commitment.

> transitionFailure(U) -> not committed(U)

Failure is not equivalent to absence of commitment.

> not committed(U) =/=> transitionFailure(U)

A transition may be authorized, pending, not yet executed, or unable to begin
without yet possessing a terminal transition-failure classification.

Transition failure does not retroactively redefine the Protocol Action
Determination.

> transitionFailure(U) =/=> rejects(D, A)

> transitionFailure(U) =/=> incorrect(D)

> transitionFailure(U) =/=> evaluationFailure(E)

Transition failure may arise from:

- stale authorization;
- conflicting protocol state;
- inability to preserve `U`;
- infrastructure failure;
- inability to establish complete atomic commitment;
- another protocol-defined execution failure.

A correct implementation may report transition failure.

Therefore:

> transitionFailure(U) =/=> incorrectExecution(I, U)

Failure must be explicit.

It must not silently become:

- commitment;
- partial commitment;
- Protocol Action rejection;
- evaluation failure;
- application truth;
- an alternative transition.

<a id="pe-g2-src-s27-sec-020-000"></a>
# 20. Pre-Transition Failure
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-012; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-010-01,pe-g2-src-s27-clar-atomic-011-01,pe-g2-src-s27-clar-atomic-012-01,pe-g2-src-s27-clar-atomic-012-02; successor-requirements=PE-G2-FAIL-019,PE-G2-STALEAUTH-013,PE-G2-STALEAUTH-014,PE-G2-STALEAUTH-015; status=candidate-unreviewed-unpublished-non-authoritative.


Pre-transition failure occurs when the post-determination transition boundary
cannot validly proceed into bounded transition execution.

Where `U` has already been authorized:

> preTransitionFailure(U) -> not executing(U)

> preTransitionFailure(U) -> not committed(U)

> preTransitionFailure(U) =/=> rejects(D, A)

Pre-transition failure may arise when an implementation cannot:

- establish the applicable current protocol state;
- confirm that authorization remains applicable;
- begin execution while preserving `U`;
- obtain required execution capability;
- enter the transition lifecycle without violating protocol rules.

Where no transition has yet been identified or authorized, a
post-determination failure must not fabricate `U` merely to attach a transition
failure record.

Pre-transition failure is not Protocol Action Evaluation failure.

The Evaluation has already completed and produced `D`.

<a id="pe-g2-src-s27-sec-021-000"></a>
# 21. Stale Authorization and Conflicting Protocol State
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-012; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-010-01,pe-g2-src-s27-clar-atomic-011-01,pe-g2-src-s27-clar-atomic-012-01,pe-g2-src-s27-clar-atomic-012-02; successor-requirements=PE-G2-FAIL-019,PE-G2-STALEAUTH-013,PE-G2-STALEAUTH-014,PE-G2-STALEAUTH-015; status=candidate-unreviewed-unpublished-non-authoritative.


Transition authorization may be bounded to `Q0`.

> authorizedAgainst(U, Q0)

Before execution and commitment, the implementation must establish whether the
applicable current state is equivalent to `Q0` for the protocol-relevant purpose
of `U`.

> equivalentTransitionState(Qx, Q0)

> -> mayExecuteAgainst(U, Qx)

Where the current state is materially different:

> not equivalentTransitionState(Qx, Q0)

> -> staleAuthorization(U)

Stale authorization prohibits commitment against the conflicting state.

> staleAuthorization(U) -> not committed(U)

> staleAuthorization(U) -> not mayCommitAgainst(U, Qx)

An implementation must not select whichever state context produces a preferred
result.

> staleAuthorization(U)

> -> not mayChoosePreferredState(I, Q0, Qx)

Changed state does not retroactively rewrite a correct Determination made in its
original evaluation context.

> staleAuthorization(U) =/=> incorrect(D)

> staleAuthorization(U) =/=> rejects(D, A)

> staleAuthorization(U) =/=> evaluationFailure(E)

The applicable protocol rules may require a new Protocol Action Evaluation.

Where re-evaluation is required, it produces a new Evaluation and a new
Determination.

It does not mutate, repair, refresh, or reinterpret the earlier `E` or `D`.

> requiresReevaluation(U)

> -> requiresNewEvaluation(E2)

A state conflict therefore produces one of the bounded results permitted by the
protocol rules:

- transition failure;
- pre-transition failure;
- required re-evaluation;
- another explicitly defined non-committing result.

The implementation may not invent or select among those results
discretionarily.

<a id="pe-g2-src-s27-sec-022-000"></a>
# 22. Transition Correctness

A committed Protocol State Transition is correct only when it preserves:

- valid authorization;
- transition identity;
- the applicable pre-transition state;
- the protocol-defined state-change relation;
- the complete required post-transition state;
- semantic atomicity;
- all applicable protocol rules.

> correctTransition(U)

> iff

> authorizedBy(U, D)

> and accepts(D, A)

> and authorizedAgainst(U, Q0)

> and appliesStateChangeRelation(U, R)

> and executedThrough(U, I)

> and completeStateChange(U, Q0, Q1)

> and committed(U)

A failed transition is not necessarily an incorrect transition execution.

A correct implementation may refuse commitment where commitment would violate
authorization, state applicability, transition preservation, or atomicity.

Correct failure preserves protocol semantics by preventing an invalid
commitment.

<a id="pe-g2-src-s27-sec-023-000"></a>
# 23. Implementation Error
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-010,CLAR-ATOMIC-011; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-010-01,pe-g2-src-s27-clar-atomic-011-01; successor-requirements=PE-G2-FAIL-019,PE-G2-STALEAUTH-013; status=candidate-unreviewed-unpublished-non-authoritative.


Implementation error occurs when an implementation incorrectly realizes,
classifies, or reports a Protocol State Transition.

Implementation error includes:

- committing an unauthorized transition;
- executing `U'` instead of authorized `U`;
- committing against materially conflicting state;
- applying the wrong state-change relation;
- establishing an incorrect post-transition state;
- adding unauthorized state effects;
- omitting required state effects;
- partially committing a transition;
- reporting failure as commitment;
- reporting commitment without complete state change;
- treating transition failure as Protocol Action rejection;
- rewriting a completed Determination because execution failed.

An implementation assertion does not redefine protocol truth.

> reportsCommitted(I, U) =/=> committed(U)

> reportsFailure(I, U) =/=> transitionFailure(U)

> incorrectCommitment(I, U) =/=> correctTransition(U)

Implementation error does not change protocol semantics.

> incorrectTransition(U) =/=> changesSemantics(P)

> incorrectExecution(I, U) =/=> changesSemantics(P)

Protocol correctness remains defined by the published protocol generation.

<a id="pe-g2-src-s27-sec-024-000"></a>
# 24. Determinism and Equivalent Transitions
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-012; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-010-01,pe-g2-src-s27-clar-atomic-011-01,pe-g2-src-s27-clar-atomic-012-01,pe-g2-src-s27-clar-atomic-012-02; successor-requirements=PE-G2-FAIL-019,PE-G2-STALEAUTH-013,PE-G2-STALEAUTH-014,PE-G2-STALEAUTH-015; status=candidate-unreviewed-unpublished-non-authoritative.


Correct implementations must preserve deterministic protocol-relevant
transition semantics.

Where two correctly executed transitions are equivalent in authorization,
pre-transition state, and protocol-defined state-change relation, their
successful protocol-relevant results must be equivalent.

> equivalentAuthorizedTransition(U1, U2)

> and equivalentPreState(Q0a, Q0b)

> and equivalentStateChangeRelation(R1, R2)

> and successfulCorrectExecution(I1, U1)

> and successfulCorrectExecution(I2, U2)

> -> equivalentPostState(Q1a, Q1b)

Equivalent transition results do not require:

- identical implementation internals;
- identical instruction order;
- identical storage representation;
- identical infrastructure;
- identical transaction formats;
- identical diagnostics;
- identical operational identifiers.

Operational availability may differ between implementations.

The equivalence requirement governs successful correct protocol execution.

Infrastructure failure does not authorize semantic substitution.

<a id="pe-g2-src-s27-sec-025-000"></a>
# 25. Relationship to Protocol Actions and Determinations
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-012; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-010-01,pe-g2-src-s27-clar-atomic-011-01,pe-g2-src-s27-clar-atomic-012-01,pe-g2-src-s27-clar-atomic-012-02; successor-requirements=PE-G2-FAIL-019,PE-G2-STALEAUTH-013,PE-G2-STALEAUTH-014,PE-G2-STALEAUTH-015; status=candidate-unreviewed-unpublished-non-authoritative.


The complete protocol-use relationship is:

> performs(X, A)

> evaluates(E, A)

> produces(E, D)

> determines(D, A)

> accepts(D, A) xor rejects(D, A)

An accepted Determination may then authorize a transition:

> accepts(D, A) -> mayAuthorize(D, U)

The transition remains distinct from every earlier subject:

> A != E

> E != D

> D != U

The Action is the evaluated public occurrence.

The Evaluation applies the complete applicable protocol-rule set.

The Determination records acceptance or rejection.

Authorization permits a bounded transition.

Execution attempts to realize that transition.

Commitment establishes the complete protocol-state change.

Application interpretation remains outside this chain.

<a id="pe-g2-src-s27-sec-026-000"></a>
# 26. Relationship to Implementations

A Protocol State Transition occurs through an implementation.

> executedThrough(U, I)

The implementation is responsible for correctly realizing:

- authorization checks;
- applicable-state checks;
- the protocol-defined state-change relation;
- transition preservation;
- complete commitment;
- semantic atomicity;
- explicit failure.

The implementation does not own:

- transition semantics;
- protocol-state authority;
- protocol validity;
- the applicable state-change relation;
- transition cardinality;
- protocol authority.

Different implementations may use different execution mechanisms while
remaining semantically equivalent.

Implementation convenience must not redefine transition boundaries.

<a id="pe-g2-src-s27-sec-027-000"></a>
# 27. Relationship to Protocol-State History

A committed Protocol State Transition may enter authoritative protocol-state
history.

> committed(U) -> includedInProtocolStateHistory(U, H)

Protocol-state history records committed public protocol-state consequences.

A failed transition does not enter history as a committed state transition.

> transitionFailure(U)

> =/=> includedAsCommittedTransition(U, H)

A pre-transition failure does not create a committed transition-history entry.

Operational records of attempts or failures may exist.

Such records are not committed protocol state and do not acquire protocol
authority.

This model does not require:

- one particular history representation;
- one linear storage structure;
- one blockchain;
- one consensus mechanism;
- one database;
- one event format;
- one transaction format.

Any protocol-state history representation must preserve the same committed
transition semantics.

<a id="pe-g2-src-s27-sec-028-000"></a>
# 28. Observable Public Consequence

A committed Protocol State Transition establishes an observable public
protocol-state consequence.

> committed(U) -> publicProtocolConsequence(U, Q1)

The observable consequence is bounded to the protocol meaning of the committed
state change.

It does not establish:

- application truth;
- legal truth;
- factual truth;
- private-actor identity;
- reusable participant identity;
- hidden intent;
- off-protocol meaning.

An accepted Determination may be publicly observable without producing a
Protocol State Transition.

A transition may fail without altering the correctness of the accepted
Determination.

Only commitment establishes the transition's public protocol-state consequence.

<a id="pe-g2-src-s27-sec-029-000"></a>
# 29. Preservation of Privacy Semantics
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-015; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-015-01; successor-requirements=PE-G2-SEMPRES-027; status=candidate-unreviewed-unpublished-non-authoritative.


The Privacy Engine preserves:

> Private actors, public actions.

The completed public protocol-use chain may be represented as:

> Private Actor

> -> Public Protocol Action

> -> Public Protocol Action Determination

> -> Possible Public Protocol State Transition

Public consequences must not reconstruct private actors.

Transition identity must not introduce:

- wallet identity;
- membership-secret material;
- enrollment provenance;
- admission provenance;
- reusable participant identity;
- cross-action identity beyond required public protocol-state relations;
- identity-bearing diagnostic information;
- unnecessary correlation identifiers.

> identifiesTransition(id(U), U)

> =/=> identifiesActor(id(U), X)

Where a committed transition records uniqueness, authorization, membership,
eligibility, possession, or another protocol property, the recorded meaning
remains bounded to that public protocol property.

It must not be extended into actor identification.

<a id="pe-g2-src-s27-sec-030-000"></a>
# 30. Preservation of Protocol Semantics

A Protocol State Transition realizes protocol-defined state-change semantics.

It does not define or redefine them.

> semantics(U) subsetOf semantics(P)

> committed(U) =/=> definesProtocolSemantics(U)

Authorization does not create new protocol rules.

Execution does not create new protocol rules.

Commitment does not create new protocol rules.

Failure does not create new protocol rules.

Implementation behavior does not become protocol authority.

Incorrect execution, incorrect commitment, or incorrect reporting does not
change the meaning of the published protocol generation.

<a id="pe-g2-src-s27-sec-031-000"></a>
# 31. Protocol Authority

Protocol authority always remains with the published Privacy Engine protocol generation.

The Protocol State Transition derives its meaning, authorization conditions,
state-change relation, correctness requirements, commitment requirements, and
failure semantics from that generation.

No transition, authorization, execution, commitment, failure, implementation,
application, actor, state record, or operational report may redefine:

- protocol semantics;
- privacy semantics;
- Protocol Action semantics;
- Evaluation semantics;
- Determination semantics;
- acceptance or rejection;
- transition validity;
- transition atomicity;
- protocol-state meaning;
- protocol-state history;
- conformance;
- certification;
- protocol authority.

<a id="pe-g2-src-s27-sec-032-000"></a>
# 32. Explicit Exclusions

This model does not:

- redefine Protocol Actions;
- redefine Protocol Action identity;
- redefine Protocol Action Evaluation;
- redefine Protocol Action Determination;
- redefine acceptance or rejection;
- make acceptance identical to transition commitment;
- require every accepted Action to produce a transition;
- treat transition failure as Protocol Action rejection;
- treat transition failure as Evaluation failure;
- create a separate first-class authorization object;
- create a separate first-class execution object;
- create a separate first-class commitment object;
- create a separate first-class failure object;
- create a separate first-class transition-set object;
- reintroduce Protocol Claims;
- define application-specific state;
- define application transactions;
- define petition state;
- define voting state;
- define credential state;
- define blockchain consensus;
- define transaction formats;
- define transport protocols;
- define relay behavior;
- define execution topology;
- define database mechanics;
- define storage layouts;
- define implementation-specific execution flows;
- prescribe locking or rollback algorithms;
- introduce discretionary implementation authority;
- define application truth;
- define legal truth;
- define factual truth;
- introduce actor identity;
- introduce reusable participant identifiers;
- introduce cross-action linkage;
- introduce identity-bearing diagnostic information;
- redefine implementations;
- redefine implementation profiles;
- redefine conformance;
- redefine certification;
- redefine protocol semantics;
- redefine protocol authority.

<a id="pe-g2-src-s27-sec-033-000"></a>
# 33. Conclusion
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-012; semantic-obligation-anchors=pe-g2-src-s27-clar-atomic-010-01,pe-g2-src-s27-clar-atomic-011-01,pe-g2-src-s27-clar-atomic-012-01,pe-g2-src-s27-clar-atomic-012-02; successor-requirements=PE-G2-FAIL-019,PE-G2-STALEAUTH-013,PE-G2-STALEAUTH-014,PE-G2-STALEAUTH-015; status=candidate-unreviewed-unpublished-non-authoritative.


A Privacy Engine Protocol State Transition is one identified, bounded,
protocol-governed state-change occurrence whose successful commitment completely
changes one applicable pre-transition protocol state into one protocol-defined
post-transition protocol state.

Protocol State Transition is a distinct first-class architectural subject.

Transition authorization, execution, commitment, and failure are bounded
aspects of the transition model rather than separate first-class subjects.

An accepted Protocol Action Determination may authorize zero, one, or multiple
separately identified transitions, as determined exclusively by the applicable
protocol rules.

Authorization selects `U`.

Every later transition stage must preserve `U`.

If execution cannot preserve `U`, it must fail rather than repair, widen,
substitute, merge, infer, partially commit, or replace `U` with `U'`.

Commitment is the successful terminal predicate of `U`.

Only complete and semantically atomic commitment changes protocol state.

Partial execution is not commitment.

Transition failure does not retroactively become Protocol Action rejection,
Evaluation failure, or an incorrect Determination.

Stale authorization prohibits commitment against materially conflicting state.

Where the protocol requires re-evaluation, a new Evaluation and Determination
must be produced rather than rewriting the earlier result.

Only committed transitions enter authoritative protocol-state history as
committed public state changes.

Transition identity and public protocol-state consequences must not reconstruct
private actors.

Private actors remain private.

Protocol Actions remain public.

Protocol State Transitions record bounded public protocol consequences.

Protocol authority always remains with the published Privacy Engine protocol generation.

Candidate status: candidate; unreviewed; unpublished; non-authoritative.
End of PE-G2-SOURCE-S27.
