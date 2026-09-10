<a id="pe-g2-art-pe-g2-source-s25"></a>
# Privacy Engine Protocol Action Evaluation Model G2 Candidate V1

Successor source artifact: PE-G2-SOURCE-S25

Successor generation: PE-PROTOCOL-GENERATION-002

Immutable predecessor: docs/PRIVACY_ENGINE_PROTOCOL_ACTION_EVALUATION_MODEL_V1.md

Immutable predecessor SHA-256: ce87a40a508d8e2a5d1ef36635748f4a99e4b26bf794b2f642380ae11fe33790

Status: candidate; unreviewed; unpublished; non-authoritative.

All inherited V1 identity, review, publication and current-generation statements below are predecessor derivation text concerning G1 only. They do not assert G2 identity, review, publication or authority. G2 candidate meaning is established by the successor semantic-obligation register and exact section bindings.

## Successor Candidate Semantic-Obligation Register

| Source anchor | Engineering trace input | Successor requirement | Exact successor rule |
|---|---|---|---|
| <a id="pe-g2-src-s25-clar-atomic-001-01"></a> pe-g2-src-s25-clar-atomic-001-01 | CLAR-ATOMIC-001 | PE-G2-EVAL-021 | Every completed Protocol Action Evaluation MUST produce exactly one Protocol Action Determination as part of the same protocol-semantic completion transition. |
| <a id="pe-g2-src-s25-clar-atomic-001-02"></a> pe-g2-src-s25-clar-atomic-001-02 | CLAR-ATOMIC-001 | PE-G2-EVAL-022 | An implementation MUST NOT represent Evaluation completion and required Determination production as two protocol-semantic transitions separated by a valid completed-Evaluation state. |
| <a id="pe-g2-src-s25-clar-atomic-002-01"></a> pe-g2-src-s25-clar-atomic-002-01 | CLAR-ATOMIC-002 | PE-G2-EVAL-023 | A Protocol Action Evaluation MUST be in a valid completed state exactly when every applicable completion requirement is satisfied and exactly one corresponding Protocol Action Determination has been produced. |
| <a id="pe-g2-src-s25-clar-atomic-003-01"></a> pe-g2-src-s25-clar-atomic-003-01 | CLAR-ATOMIC-003 | PE-G2-DETERM-015 | A protocol state MUST NOT contain a completed Protocol Action Evaluation without exactly one corresponding Protocol Action Determination. |
| <a id="pe-g2-src-s25-clar-atomic-004-01"></a> pe-g2-src-s25-clar-atomic-004-01 | CLAR-ATOMIC-004 | PE-G2-DETERM-016 | Atomic establishment of Evaluation completion and Determination production MUST preserve the distinct identities and meanings of the Evaluation process and Determination result. |
| <a id="pe-g2-src-s25-clar-atomic-005-01"></a> pe-g2-src-s25-clar-atomic-005-01 | CLAR-ATOMIC-005 | PE-G2-EVAL-024 | An active Protocol Action Evaluation MAY contain bounded internal steps, completed components and intermediate component state while remaining incomplete. |
| <a id="pe-g2-src-s25-clar-atomic-005-02"></a> pe-g2-src-s25-clar-atomic-005-02 | CLAR-ATOMIC-005 | PE-G2-EVAL-025 | An internal step, component result, combined intermediate state or completion-readiness condition MUST NOT be represented as completed Evaluation or as a Protocol Action Determination. |
| <a id="pe-g2-src-s25-clar-atomic-006-01"></a> pe-g2-src-s25-clar-atomic-006-01 | CLAR-ATOMIC-006 | PE-G2-EVAL-026 | If an Evaluation that has begun cannot establish exactly one valid Determination at the same protocol-semantic boundary as Evaluation completion, the Evaluation MUST terminate as Evaluation failure, MUST remain incomplete, and MUST produce no Determination, acceptance or rejection. |
| <a id="pe-g2-src-s25-clar-atomic-007-01"></a> pe-g2-src-s25-clar-atomic-007-01 | CLAR-ATOMIC-007 | PE-G2-FAIL-018 | Failure before authoritative Evaluation begins MUST create no authoritative Evaluation, Determination, acceptance or rejection. |
| <a id="pe-g2-src-s25-clar-atomic-008-01"></a> pe-g2-src-s25-clar-atomic-008-01 | CLAR-ATOMIC-008 | PE-G2-EXCLUDE-027 | Partial Evaluation completion MUST NOT be represented as a valid terminal protocol state. |
| <a id="pe-g2-src-s25-clar-atomic-009-01"></a> pe-g2-src-s25-clar-atomic-009-01 | CLAR-ATOMIC-009 | PE-G2-SURF-019 | Protocol-semantic Determination production MUST remain distinct from representation, serialization, persistence, publication, transport, operational delivery, display, indexing, events, logs, responses and application interpretation. |
| <a id="pe-g2-src-s25-clar-atomic-009-02"></a> pe-g2-src-s25-clar-atomic-009-02 | CLAR-ATOMIC-009 | PE-G2-EXCLUDE-028 | A later mechanism or observation MUST NOT be treated as creating, replacing or identifying the protocol-semantic completion boundary merely because it represents or reports a Determination. |
| <a id="pe-g2-src-s25-clar-atomic-010-01"></a> pe-g2-src-s25-clar-atomic-010-01 | CLAR-ATOMIC-010 | PE-G2-FAIL-019 | Failure of representation, serialization, persistence, publication, transport, operational delivery, display, indexing or application translation after Determination production MUST NOT erase the Determination, reopen or fail the completed Evaluation, alter its acceptance or rejection classification, or become protocol rejection. |
| <a id="pe-g2-src-s25-clar-atomic-011-01"></a> pe-g2-src-s25-clar-atomic-011-01 | CLAR-ATOMIC-011 | PE-G2-STALEAUTH-013 | Retry of a later representation, publication, transport or delivery operation MUST preserve the same already-produced Determination and MUST NOT produce another Determination or another Evaluation occurrence. |
| <a id="pe-g2-src-s25-clar-atomic-012-01"></a> pe-g2-src-s25-clar-atomic-012-01 | CLAR-ATOMIC-012 | PE-G2-STALEAUTH-014 | A terminally failed Evaluation MUST NOT later become complete. |
| <a id="pe-g2-src-s25-clar-atomic-012-02"></a> pe-g2-src-s25-clar-atomic-012-02 | CLAR-ATOMIC-012 | PE-G2-STALEAUTH-015 | Any later authoritative re-evaluation MUST instantiate a new Evaluation occurrence and MUST preserve the failed occurrence without mutation, repair or reinterpretation. |
| <a id="pe-g2-src-s25-clar-atomic-013-01"></a> pe-g2-src-s25-clar-atomic-013-01 | CLAR-ATOMIC-013 | PE-G2-EXCLUDE-029 | Protocol-semantic atomicity MUST NOT be inferred from or defined by implementation transaction atomicity, storage atomicity, event emission, response production, logging, persistence, consensus, rollback or any other implementation mechanism. |
| <a id="pe-g2-src-s25-clar-atomic-014-01"></a> pe-g2-src-s25-clar-atomic-014-01 | CLAR-ATOMIC-014 | PE-G2-FAIL-020 | Operational success or failure MUST remain distinct from Determination production and from formal Evaluation success or failure. |
| <a id="pe-g2-src-s25-clar-atomic-014-02"></a> pe-g2-src-s25-clar-atomic-014-02 | CLAR-ATOMIC-014 | PE-G2-RUNTIME-017 | Operational failure after a Determination exists MUST be classified at the actual later lifecycle layer. |
| <a id="pe-g2-src-s25-clar-atomic-015-01"></a> pe-g2-src-s25-clar-atomic-015-01 | CLAR-ATOMIC-015 | PE-G2-SEMPRES-027 | Every Evaluation, Determination, failure, retry, representation, publication, transport, delivery, diagnostic and observability surface MUST preserve Private Actor non-disclosure, neutral naming, action-bounded public identity and the prohibition on reusable participant identity, actor provenance and cross-action linkage. |

STATE.md remains canonical.

<a id="pe-g2-src-s25-sec-001-000"></a>
# 1. Purpose

This document defines the bounded architectural model through which one Privacy
Engine Protocol Action is evaluated and receives an authoritative acceptance or
rejection determination.

It establishes the relationships among:

- the evaluated Protocol Action;
- the Protocol Action Evaluation;
- the evaluation context;
- the applicable protocol-rule set;
- proof verification;
- non-proof validity conditions;
- evaluation completeness;
- evaluation failure;
- the Protocol Action Determination;
- acceptance;
- rejection;
- implementation error;
- possible public state transition.

The model preserves the distinction:

> action != evaluation != proof verification != determination != outcome classification != public state transition

It does not redefine Protocol Actions, proofs, public inputs, proof verification,
implementations, application meaning, or protocol authority.

<a id="pe-g2-src-s25-sec-002-000"></a>
# 2. Scope

This document applies to the architectural evaluation of a Protocol Action under
one published Privacy Engine protocol generation.

Let:

- `P` be one published Privacy Engine protocol generation;
- `S` be one Privacy Engine Protocol Specification;
- `F` be one implementation profile;
- `I` be one implementation;
- `A` be one Protocol Action;
- `R` be the complete applicable protocol-rule set;
- `C` be one bounded evaluation context;
- `E` be one Protocol Action Evaluation;
- `Z` be one proof;
- `PI` be one declared public-input set;
- `V` be one proof-verification determination;
- `D` be one Protocol Action Determination;
- `U` be one public state transition.

This document defines only the evaluation of `A`, the resulting determination
`D`, and their immediate architectural boundaries.

It does not define application-specific actions, application-specific
acceptance rules, transport behavior, transaction formats, execution topology,
or implementation internals.

<a id="pe-g2-src-s25-sec-003-000"></a>
# 3. Primary Definition
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-004; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-004-01; successor-requirements=PE-G2-DETERM-016; status=candidate-unreviewed-unpublished-non-authoritative.


A Privacy Engine Protocol Action Evaluation is one identified, bounded, and
authoritative evaluation occurrence that evaluates one identified Protocol
Action against the complete applicable protocol-rule set within one bounded
evaluation context.

> evaluates(E, A)

> evaluatedIn(E, C)

> applies(E, R)

A Privacy Engine Protocol Action Determination is the identified and bounded
authoritative result produced by one completed Protocol Action Evaluation.

> complete(E) -> produces(E, D)

> determinationOf(D, E)

> determines(D, A)

The determination records exactly one of two mutually exclusive classifications:

> accepts(D, A) xor rejects(D, A)

Acceptance and rejection are predicates of the Protocol Action Determination.

They are not separate first-class architectural subjects.

<a id="pe-g2-src-s25-sec-004-000"></a>
# 4. Architectural Subject Assessment

Protocol Action Evaluation and Protocol Action Determination possess distinct
architectural roles:

- Evaluation is the bounded authoritative process.
- Determination is the bounded authoritative result of that process.

They are not identical:

> E != D

The Evaluation has occurrence identity, bounded scope, applicable rules,
evaluation context, components, completeness conditions, and failure semantics.

The Determination has result identity, an evaluated action, a producing
Evaluation, and exactly one acceptance or rejection classification.

The Determination is nevertheless relationally dependent upon the completed
Evaluation that produced it:

> exists(D) -> exists(E)

> determinationOf(D, E) -> complete(E)

> determinationOf(D, E) -> produces(E, D)

The Determination does not possess an independent protocol role outside the
Evaluation relationship.

Accordingly:

> boundedProcess(E)

> boundedResult(D)

> aspectOfModel(E, evaluationProcess)

> aspectOfModel(D, evaluationResult)

Protocol Action Evaluation and Protocol Action Determination are two bounded
aspects of one architectural model.

They do not require two separate ontology documents.

Acceptance and rejection are not independent outcome objects.

They are mutually exclusive predicates of the determination:

> accepts(D, A) xor rejects(D, A)

The term `outcome` may describe the classification of `D`, but it does not
introduce an independently identified object.

No additional ontology is introduced for editorial convenience.

<a id="pe-g2-src-s25-sec-005-000"></a>
# 5. Evaluation Identity

Every Protocol Action Evaluation possesses its own occurrence identity.

An Evaluation identifies exactly:

- one evaluation occurrence;
- one evaluated Protocol Action;
- one complete applicable protocol-rule set;
- one bounded evaluation context.

Formally:

> identifiesEvaluation(id(E), E)

> evaluates(E, A)

> applies(E, R)

> evaluatedIn(E, C)

Evaluation identity is not:

- Protocol Action identity;
- action-type identity;
- proof identity;
- public-input identity;
- proof-verification identity;
- implementation identity;
- actor identity;
- determination identity;
- public-state-transition identity.

Multiple evaluation occurrences may evaluate the same Protocol Action.

> E1 != E2

does not necessarily imply:

> A1 != A2

Evaluation identity records the bounded evaluation occurrence. It does not
create reusable identity for the private actor.

<a id="pe-g2-src-s25-sec-006-000"></a>
# 6. Evaluation Scope and Boundedness
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-007; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-007-01; successor-requirements=PE-G2-FAIL-018; status=candidate-unreviewed-unpublished-non-authoritative.


One Protocol Action Evaluation is bounded to:

- one identified Protocol Action;
- one selected complete applicable protocol-rule set;
- one evaluation context;
- every evaluation component required by that rule set;
- one completeness result;
- at most one Protocol Action Determination.

An Evaluation must not silently widen its scope after evaluation begins.

> begins(E, A, R, C) -> fixedScope(E, A, R, C)

An Evaluation must not substitute a different action, rule set, or context:

> begins(E, A, R, C) =/=> mayEvaluate(E, A2, R2, C2)

where any substituted value changes the authoritative evaluation subject.

Evaluation scope does not include:

- application truth;
- legal truth;
- factual truth;
- actor identity;
- transport success;
- infrastructure preference;
- implementation convenience;
- application-specific policy not derived from the applicable protocol rules.

<a id="pe-g2-src-s25-sec-007-000"></a>
# 7. Evaluated Protocol Action

The Protocol Action is the subject evaluated by the Protocol Action Evaluation.

> evaluates(E, A)

The action is not the Evaluation:

> A != E

The action carries its declared public inputs:

> carries(A, PI)

A proof may support the action:

> supports(Z, A)

Neither the proof nor its public inputs replace the Protocol Action as the
evaluated subject:

> Z != A

> PI != A

> verifies(V, Z, PI) =/=> evaluates(V, A)

The Evaluation assesses whether the Protocol Action satisfies every applicable
protocol rule within the bounded evaluation context.

It does not reinterpret the action as an application claim.

<a id="pe-g2-src-s25-sec-008-000"></a>
# 8. Evaluation Context

An evaluation context is the bounded set of protocol-relevant conditions under
which one Protocol Action is evaluated.

> evaluatedIn(E, C)

The context may contain only information required by the applicable protocol
rules, including where applicable:

- the relevant published protocol generation;
- the applicable Protocol Specification;
- the applicable implementation profile;
- the protocol-relevant state;
- the valid-root state;
- the uniqueness state;
- the applicable domain;
- the protocol-relevant temporal position;
- other explicitly required protocol conditions.

The context must be sufficient to evaluate `R` without becoming an unrestricted
container for implementation policy.

> contains(C, x) -> protocolRelevant(x, R)

The context must not acquire authority to introduce:

- application-specific validity rules;
- implementation preferences;
- transport policy;
- discretionary repair rules;
- actor-identifying material;
- reusable participant identity;
- external truth claims.

Equivalent contexts need not use identical internal representations.

They must preserve the same protocol-relevant facts required for evaluation.

<a id="pe-g2-src-s25-sec-009-000"></a>
# 9. Applicable Protocol Rules

The applicable protocol-rule set is the complete set of protocol requirements
that governs the identified Protocol Action in the identified evaluation
context.

> applicableRules(A, C, R)

> applies(E, R)

The applicable rules derive from the published protocol generation through the
Protocol Specification and applicable implementation profile.

> derives(S, P)

> derives(F, S)

> applicableRules(A, C, R)

Rule selection must be complete and fixed before authoritative component
evaluation proceeds.

Selection chooses `R`.

Every evaluation component preserves `R`.

No component may:

- omit a required rule;
- add an unauthorized rule;
- weaken a required rule;
- repair a failed rule;
- infer a replacement rule;
- substitute implementation policy for a protocol rule.

If the complete applicable rule set cannot be established, authoritative
evaluation must not proceed.

> not establishesCompleteRules(A, C, R)
> -> preEvaluationFailure(A, C)

<a id="pe-g2-src-s25-sec-010-000"></a>
# 10. Evaluation Components
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-005; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-005-01,pe-g2-src-s25-clar-atomic-005-02; successor-requirements=PE-G2-EVAL-024,PE-G2-EVAL-025; status=candidate-unreviewed-unpublished-non-authoritative.


A Protocol Action Evaluation may contain multiple bounded evaluation
components.

Components may evaluate, where applicable:

- action-type validity;
- declared public-input validity;
- proof-verification requirements;
- proof-to-public-input consistency;
- protocol-state requirements;
- root-validity requirements;
- uniqueness requirements;
- domain-separation requirements;
- temporal requirements;
- every other applicable protocol rule.

Each component evaluates only the protocol requirement assigned to it.

> componentOf(K, E)

> evaluatesRequirement(K, r)

> memberOf(r, R)

No component independently determines complete Protocol Action validity unless
its assigned requirement set is the complete applicable rule set.

> evaluatesSubset(K, R) =/=> completeEvaluation(K, E)

Component results contribute to the complete Evaluation.

They do not independently accept the Protocol Action.

<a id="pe-g2-src-s25-sec-011-000"></a>
# 11. Relationship to Proof Verification

Proof verification evaluates bounded cryptographic evidence.

> supports(Z, A)

> carries(A, PI)

> verifies(V, Z, PI)

> contributesTo(V, E)

A valid proof-verification determination establishes only the protocol meaning
assigned to that proof and public-input relationship.

It does not automatically establish complete Protocol Action validity:

> verifiesValid(V, Z, PI) =/=> protocolValid(A, C)

It does not automatically produce acceptance:

> verifiesValid(V, Z, PI) =/=> accepts(D, A)

The implication may hold only where proof verification constitutes the complete
applicable protocol-rule set for the action:

> proofRules(Z, PI) = R
> and verifiesValid(V, Z, PI)
> -> satisfiesAll(A, R, C)

Proof verification must not extend the proof's protocol meaning into:

- actor identification;
- application truth;
- legal truth;
- factual truth;
- enrollment provenance;
- admission provenance;
- cross-action identity;
- reusable participant identity.

<a id="pe-g2-src-s25-sec-012-000"></a>
# 12. Non-Proof Validity Conditions

Protocol Action validity may depend upon requirements not established by proof
verification.

Non-proof validity conditions may include:

- action-type requirements;
- public-input shape and domain requirements;
- current protocol-state requirements;
- accepted-root requirements;
- uniqueness requirements;
- replay-prevention requirements;
- temporal requirements;
- protocol-authorized state-transition preconditions.

These conditions remain protocol rules only when derived from the published
protocol generation and applicable to the action.

> nonProofRule(r)

> memberOf(r, R)

> evaluatesRequirement(E, r)

Implementation convenience does not create a non-proof protocol rule.

Application policy does not become a protocol rule merely because an
implementation evaluates it.

<a id="pe-g2-src-s25-sec-013-000"></a>
# 13. Evaluation Completeness
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-001,CLAR-ATOMIC-002,CLAR-ATOMIC-003,CLAR-ATOMIC-005,CLAR-ATOMIC-006,CLAR-ATOMIC-008; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-001-01,pe-g2-src-s25-clar-atomic-001-02,pe-g2-src-s25-clar-atomic-002-01,pe-g2-src-s25-clar-atomic-003-01,pe-g2-src-s25-clar-atomic-005-01,pe-g2-src-s25-clar-atomic-005-02,pe-g2-src-s25-clar-atomic-006-01,pe-g2-src-s25-clar-atomic-008-01; successor-requirements=PE-G2-DETERM-015,PE-G2-EVAL-021,PE-G2-EVAL-022,PE-G2-EVAL-023,PE-G2-EVAL-024,PE-G2-EVAL-025,PE-G2-EVAL-026,PE-G2-EXCLUDE-027; status=candidate-unreviewed-unpublished-non-authoritative.


A Protocol Action Evaluation is complete exactly when it evaluates every
applicable protocol rule for the identified Protocol Action in the identified
evaluation context.

> complete(E) iff evaluatesAll(E, R, A, C)

Completeness requires:

- the complete applicable rule set was established;
- every required evaluation component was performed;
- every component evaluated its assigned requirement;
- all component results were available;
- component results were coherently combined;
- no required rule was omitted, substituted, weakened, repaired, or inferred.

Only a complete Evaluation may produce a Protocol Action Determination:

> produces(E, D) -> complete(E)

The success path is:

> A + R + C
> -> completeEvaluation(E)
> -> produces(E, D)

The acceptance path is:

> complete(E)
> and satisfiesAll(A, R, C)
> -> produces(E, D)
> and accepts(D, A)

The rejection path is:

> complete(E)
> and not satisfiesAll(A, R, C)
> -> produces(E, D)
> and rejects(D, A)

The forbidden path is:

> partial(E)
> -> accepts(D, A)

Therefore:

> partial(E) =/=> accepts(D, A)

> incomplete(E) =/=> producesAcceptedDetermination(E, D)

Incomplete evaluation must never silently become acceptance.

<a id="pe-g2-src-s25-sec-014-000"></a>
# 14. Evaluation Failure
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-003,CLAR-ATOMIC-006,CLAR-ATOMIC-007,CLAR-ATOMIC-008,CLAR-ATOMIC-010,CLAR-ATOMIC-012; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-003-01,pe-g2-src-s25-clar-atomic-006-01,pe-g2-src-s25-clar-atomic-007-01,pe-g2-src-s25-clar-atomic-008-01,pe-g2-src-s25-clar-atomic-010-01,pe-g2-src-s25-clar-atomic-012-01,pe-g2-src-s25-clar-atomic-012-02; successor-requirements=PE-G2-DETERM-015,PE-G2-EVAL-026,PE-G2-EXCLUDE-027,PE-G2-FAIL-018,PE-G2-FAIL-019,PE-G2-STALEAUTH-014,PE-G2-STALEAUTH-015; status=candidate-unreviewed-unpublished-non-authoritative.


Evaluation failure occurs when an authoritative Evaluation begins but cannot
complete the evaluation of the identified action against the complete
applicable rule set in the bounded context.

> begins(E, A, R, C)

> not complete(E)

> evaluationFailure(E)

Evaluation failure may result from:

- an unavailable required component result;
- an inability to evaluate a required rule;
- incoherent required evaluation material;
- loss of required protocol-state access;
- internal evaluation interruption;
- implementation or infrastructure failure preventing completion.

Evaluation failure produces no Protocol Action Determination:

> evaluationFailure(E)
> -> not existsProtocolActionDetermination(D, E)

It therefore produces neither acceptance nor protocol rejection:

> evaluationFailure(E) =/=> accepts(D, A)

> evaluationFailure(E) =/=> rejects(D, A)

A rejected action differs from a failed Evaluation.

Rejection means complete authoritative evaluation established that one or more
applicable rules were not satisfied:

> rejects(D, A)
> -> complete(E)
> and determinationOf(D, E)
> and not satisfiesAll(A, R, C)

Evaluation failure means no complete authoritative validity conclusion was
established:

> evaluationFailure(E)
> -> unknownByEvaluation(E, protocolValid(A, C))

Infrastructure failure must not automatically become protocol rejection:

> infrastructureFailure(E) =/=> rejects(D, A)

Pre-evaluation failure occurs when the candidate action does not enter the
authoritative evaluation boundary.

> preEvaluationFailure(A, C)
> -> not beginsAuthoritativeEvaluation(E, A, C)

Pre-evaluation failure produces no authoritative Evaluation and no Protocol
Action Determination.

<a id="pe-g2-src-s25-sec-015-000"></a>
# 15. Protocol Action Determination
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-001,CLAR-ATOMIC-002,CLAR-ATOMIC-003,CLAR-ATOMIC-004,CLAR-ATOMIC-006,CLAR-ATOMIC-009; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-001-01,pe-g2-src-s25-clar-atomic-001-02,pe-g2-src-s25-clar-atomic-002-01,pe-g2-src-s25-clar-atomic-003-01,pe-g2-src-s25-clar-atomic-004-01,pe-g2-src-s25-clar-atomic-006-01,pe-g2-src-s25-clar-atomic-009-01,pe-g2-src-s25-clar-atomic-009-02; successor-requirements=PE-G2-DETERM-015,PE-G2-DETERM-016,PE-G2-EVAL-021,PE-G2-EVAL-022,PE-G2-EVAL-023,PE-G2-EVAL-026,PE-G2-EXCLUDE-028,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


A Protocol Action Determination is the bounded authoritative result of one
completed Protocol Action Evaluation.

> complete(E) -> produces(E, D)

> produces(E, D) -> complete(E)

> determinationOf(D, E)

> determines(D, A)

A valid determination records exactly one authoritative classification:

> accepts(D, A) xor rejects(D, A)

The Determination records the Evaluation result.

It does not:

- perform the Protocol Action;
- replace the Protocol Action;
- perform proof verification;
- redefine the applicable rules;
- redefine protocol validity;
- create application truth;
- create actor identity;
- itself constitute a public state transition.

A determination must not exist without a completed Evaluation.

> exists(D) -> existsCompletedEvaluation(E)

<a id="pe-g2-src-s25-sec-016-000"></a>
# 16. Determination Identity

Every Protocol Action Determination possesses its own result identity.

A determination identifies exactly:

- one determination;
- one producing completed Evaluation;
- one evaluated Protocol Action;
- one bounded evaluation context;
- one applicable protocol-rule set;
- one acceptance or rejection classification.

Formally:

> identifiesDetermination(id(D), D)

> determinationOf(D, E)

> determines(D, A)

> determinedIn(D, C)

> determinedUnder(D, R)

Determination identity is not:

- action identity;
- proof identity;
- proof-verification identity;
- actor identity;
- implementation identity;
- public-state-transition identity.

Determination identity does not independently identify the private actor:

> identifiesDetermination(id(D), D)
> =/=> identifiesActor(id(D), X)

The determination is identifiable but relationally dependent upon the
Evaluation that produced it.

This dependency prevents the Determination from becoming an independent source
of protocol semantics or authority.

<a id="pe-g2-src-s25-sec-017-000"></a>
# 17. Acceptance Outcome

Acceptance is the authoritative determination predicate stating that a
completed Protocol Action Evaluation established that the Protocol Action
satisfied every applicable protocol rule in the bounded evaluation context.

> accepts(D, A)

A correct acceptance requires:

> determinationOf(D, E)

> complete(E)

> satisfiesAll(A, R, C)

Acceptance is not a separate architectural object.

It is a classification of `D`.

Acceptance does not imply:

- actor identification;
- application truth;
- legal truth;
- factual truth;
- permanent validity in every future context;
- automatic public state transition;
- implementation authority to redefine protocol semantics.

Acceptance may authorize a protocol-defined consequence:

> accepts(D, A) -> mayAuthorize(D, U)

Authorization does not require that a public state transition always occurs.

<a id="pe-g2-src-s25-sec-018-000"></a>
# 18. Rejection Outcome

Rejection is the authoritative determination predicate stating that a complete
Protocol Action Evaluation established that the Protocol Action failed one or
more applicable protocol rules in the bounded evaluation context.

> rejects(D, A)

A correct rejection requires:

> determinationOf(D, E)

> complete(E)

> not satisfiesAll(A, R, C)

Rejection is not a separate architectural object.

It is a classification of `D`.

Rejection is not:

- evaluation failure;
- pre-evaluation failure;
- infrastructure failure;
- transport failure;
- application disagreement;
- legal or factual falsity;
- actor identification.

A rejected action receives no authorization for an accepted public transition:

> rejects(D, A)
> -> not authorizesAcceptedTransition(D, U)

Rejection remains bounded to the evaluated action, applicable rules, and
evaluation context.

<a id="pe-g2-src-s25-sec-019-000"></a>
# 19. Determination Correctness

A Protocol Action is protocol-valid in an evaluation context exactly when it
satisfies every applicable protocol rule in that context.

> protocolValid(A, C) iff satisfiesAll(A, R, C)

A correct determination preserves this validity relation.

Correct acceptance:

> correct(D, A, C)
> ->
> (accepts(D, A) iff protocolValid(A, C))

Correct rejection:

> correct(D, A, C)
> ->
> (rejects(D, A) iff not protocolValid(A, C))

Because acceptance and rejection are mutually exclusive:

> correct(D, A, C)
> ->
> (accepts(D, A) xor rejects(D, A))

Determination correctness depends upon:

- correct applicable-rule selection;
- complete evaluation;
- correct evaluation of every applicable rule;
- coherent combination of component results;
- correct classification of the complete result.

A determination does not become correct merely because an implementation emits
or records it.

<a id="pe-g2-src-s25-sec-020-000"></a>
# 20. Implementation Error
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-006,CLAR-ATOMIC-010,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-006-01,pe-g2-src-s25-clar-atomic-010-01,pe-g2-src-s25-clar-atomic-014-01,pe-g2-src-s25-clar-atomic-014-02; successor-requirements=PE-G2-EVAL-026,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017; status=candidate-unreviewed-unpublished-non-authoritative.


An implementation error occurs where implementation behavior fails to preserve
the protocol-defined evaluation relation.

Examples include:

- evaluating an incomplete rule set;
- omitting a required evaluation component;
- accepting after partial evaluation;
- treating proof verification as complete evaluation when other rules apply;
- treating infrastructure failure as protocol rejection;
- accepting an invalid action;
- rejecting a valid action;
- evaluating under an incorrect context;
- introducing application policy into protocol validity;
- extending evidence into actor identification.

An erroneous acceptance does not make an invalid action protocol-valid:

> incorrectAcceptance(D, A)
> =/=> protocolValid(A, C)

An erroneous rejection does not make a valid action protocol-invalid:

> incorrectRejection(D, A)
> =/=> not protocolValid(A, C)

An incorrect determination does not alter protocol semantics:

> incorrect(D) =/=> changesSemantics(P)

Implementation behavior remains subordinate to the published protocol
generation.

<a id="pe-g2-src-s25-sec-021-000"></a>
# 21. Determinism and Equivalent Evaluation
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-011,CLAR-ATOMIC-012; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-011-01,pe-g2-src-s25-clar-atomic-012-01,pe-g2-src-s25-clar-atomic-012-02; successor-requirements=PE-G2-STALEAUTH-013,PE-G2-STALEAUTH-014,PE-G2-STALEAUTH-015; status=candidate-unreviewed-unpublished-non-authoritative.


Correct implementations evaluating the same Protocol Action under the same
applicable rules and equivalent protocol-relevant contexts must produce
equivalent determinations.

Let:

- `E1` and `E2` be two correct Evaluations;
- `C1` and `C2` be equivalent evaluation contexts;
- `D1` and `D2` be their determinations.

Then:

> sameAction(A)
> and sameRules(R)
> and equivalentContext(C1, C2)
> and correct(E1)
> and correct(E2)
> and produces(E1, D1)
> and produces(E2, D2)
> ->
> equivalentDetermination(D1, D2)

Equivalent determination means equivalent acceptance or rejection
classification for the same action under equivalent protocol-relevant
conditions.

It does not require:

- identical implementation internals;
- identical execution order;
- identical component organization;
- identical storage representation;
- identical infrastructure;
- identical diagnostic output.

Determinism governs protocol-relevant results.

It does not standardize every implementation mechanism.

<a id="pe-g2-src-s25-sec-022-000"></a>
# 22. Temporal and State-Dependent Evaluation

Protocol Action validity may depend upon the protocol-relevant state present in
the bounded evaluation context.

Therefore:

> protocolValid(A, C1)
> =/=>
> protocolValid(A, C2)

where:

> not equivalentProtocolState(C1, C2)

A root may cease to be accepted.

A uniqueness condition may change.

A temporal boundary may pass.

A protocol-relevant state precondition may cease to hold.

The determination remains bound to the context under which it was produced:

> determinationOf(D, E)

> evaluatedIn(E, C)

> determinedIn(D, C)

A determination must not be silently reused as though it evaluated the action
under a materially different context.

Temporal and state-dependent evaluation does not grant implementations
discretion to choose whichever context produces a preferred result.

The applicable context is governed by protocol rules.

<a id="pe-g2-src-s25-sec-023-000"></a>
# 23. Relationship to Implementations
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-009-01,pe-g2-src-s25-clar-atomic-009-02,pe-g2-src-s25-clar-atomic-010-01,pe-g2-src-s25-clar-atomic-011-01,pe-g2-src-s25-clar-atomic-013-01,pe-g2-src-s25-clar-atomic-014-01,pe-g2-src-s25-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


Protocol Actions are evaluated through implementations.

> performedThrough(A, I)

> executesEvaluation(I, E)

An implementation realizes the applicable implementation profile and performs
the evaluation mechanisms required by that profile.

The implementation does not own protocol semantics.

It must preserve:

- the evaluated action;
- the complete applicable rule set;
- the bounded evaluation context;
- component result meaning;
- completeness requirements;
- evaluation-failure semantics;
- determination correctness;
- privacy semantics.

Different implementations may use different internal mechanisms while
producing equivalent correct determinations.

Implementation-defined behavior is permitted only where the Protocol
Specification or applicable implementation profile explicitly permits it.

Implementation convenience must not become protocol authority.

<a id="pe-g2-src-s25-sec-024-000"></a>
# 24. Relationship to Public State Transitions
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-014-01,pe-g2-src-s25-clar-atomic-014-02; successor-requirements=PE-G2-FAIL-020,PE-G2-RUNTIME-017; status=candidate-unreviewed-unpublished-non-authoritative.


A public state transition is a possible consequence of an accepted Protocol
Action Determination.

> accepts(D, A) -> mayAuthorize(D, U)

The public state transition is not:

- the Protocol Action;
- the Protocol Action Evaluation;
- the Protocol Action Determination;
- the acceptance predicate.

Formally:

> U != A

> U != E

> U != D

Acceptance may authorize a transition without guaranteeing its occurrence.

A transition may fail to occur because of later bounded execution failure
without changing the correctness of the earlier determination.

Rejection does not authorize an accepted transition:

> rejects(D, A)
> -> not authorizesAcceptedTransition(D, U)

Evaluation failure also cannot authorize an accepted transition:

> evaluationFailure(E)
> -> not authorizesAcceptedTransition(E, U)

A public state transition must remain governed by protocol rules and must not
redefine the evaluation that authorized it.

<a id="pe-g2-src-s25-sec-025-000"></a>
# 25. Preservation of Privacy Semantics
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-015; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-015-01; successor-requirements=PE-G2-SEMPRES-027; status=candidate-unreviewed-unpublished-non-authoritative.


The Privacy Engine preserves:

> Private actors, public actions.

Protocol Action Evaluation determines action validity.

It does not determine actor identity.

Evaluation, determination, acceptance, rejection, failure handling, and public
consequence must not require, infer, retain, emit, or expose:

- wallet identity;
- membership-secret material;
- enrollment provenance;
- admission provenance;
- reusable participant identity;
- cross-action identity;
- additional correlation identifiers;
- identity-bearing diagnostic information.

Where a proof or public input establishes authorization, membership,
eligibility, uniqueness, possession, or another bounded protocol property, the
Evaluation must remain bounded to that protocol meaning.

> establishesEvidence(Z, property)
> =/=> identifiesActor(Z, X)

> authorized(A) =/=> identified(X)

> identifiesAction(id(A), A)
> =/=> identifiesActor(id(A), X)

Evaluation identity and determination identity must not become reusable actor
identity.

No Evaluation component may extend public evidence into private-actor
identification.

<a id="pe-g2-src-s25-sec-026-000"></a>
# 26. Preservation of Protocol Semantics
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-001,CLAR-ATOMIC-004,CLAR-ATOMIC-008,CLAR-ATOMIC-009,CLAR-ATOMIC-013; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-001-01,pe-g2-src-s25-clar-atomic-001-02,pe-g2-src-s25-clar-atomic-004-01,pe-g2-src-s25-clar-atomic-008-01,pe-g2-src-s25-clar-atomic-009-01,pe-g2-src-s25-clar-atomic-009-02,pe-g2-src-s25-clar-atomic-013-01; successor-requirements=PE-G2-DETERM-016,PE-G2-EVAL-021,PE-G2-EVAL-022,PE-G2-EXCLUDE-027,PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


Protocol Action Evaluation applies protocol semantics.

It does not create or redefine them.

The applicable rule set derives from the published protocol generation through
the Protocol Specification and applicable implementation profile.

> derives(S, P)

> derives(F, S)

> applicableRules(A, C, R)

> semantics(R) subsetOf semantics(P)

Evaluation must preserve the selected rule set:

> begins(E, A, R, C)
> -> preserves(E, A, R, C)

If an Evaluation cannot preserve the selected action, rule set, or context, it
must fail.

Success path:

> A + R + C
> -> complete evaluation
> -> correct determination

Rejection path:

> A + R + C
> -> complete evaluation
> -> failed applicable requirement
> -> rejection

Evaluation-failure path:

> A + R + C
> -> incomplete evaluation
> -> evaluation failure
> -> no determination

Forbidden path:

> A + R + C
> -> partial evaluation
> -> acceptance

No Evaluation, Determination, implementation, application, proof,
proof-verification result, acceptance, rejection, failure, or public state
transition may redefine protocol semantics.

<a id="pe-g2-src-s25-sec-027-000"></a>
# 27. Protocol Authority

Protocol authority always remains with the published Privacy Engine protocol generation.

The Protocol Specification derives from that generation.

Implementation profiles derive from the Protocol Specification.

Implementations realize implementation profiles.

Protocol Action Evaluations apply rules derived from the published protocol
generation.

Protocol Action Determinations record the results of those Evaluations.

No Evaluation or Determination possesses authority to redefine:

- the protocol generation;
- protocol semantics;
- privacy semantics;
- Protocol Action semantics;
- proof semantics;
- public-input semantics;
- validity requirements;
- evaluation requirements;
- implementation requirements;
- conformance;
- certification.

An incorrect determination remains an implementation error:

> incorrect(D) =/=> changesSemantics(P)

Protocol authority does not transfer to the evaluated action, Evaluation,
Determination, implementation, proof, application, actor, or resulting public
state transition.

<a id="pe-g2-src-s25-sec-028-000"></a>
# 28. Explicit Exclusions
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-008,CLAR-ATOMIC-009,CLAR-ATOMIC-013; semantic-obligation-anchors=pe-g2-src-s25-clar-atomic-008-01,pe-g2-src-s25-clar-atomic-009-01,pe-g2-src-s25-clar-atomic-009-02,pe-g2-src-s25-clar-atomic-013-01; successor-requirements=PE-G2-EXCLUDE-027,PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


This model does not:

- redefine Protocol Actions;
- redefine Protocol Action identity;
- redefine action types;
- define Protocol Claims;
- define application claims;
- redefine proofs;
- redefine proof systems;
- redefine public inputs;
- redefine proof verification;
- treat successful proof verification as automatically complete action evaluation;
- define application-specific acceptance rules;
- define petition signing;
- define voting;
- define credentials;
- define transaction formats;
- define transport protocols;
- define implementation-specific execution flows;
- define execution topology;
- treat infrastructure failure as protocol rejection;
- permit incomplete evaluation to produce acceptance;
- introduce discretionary implementation authority;
- define application truth;
- define legal truth;
- define factual truth;
- introduce actor identity;
- introduce reusable participant identifiers;
- introduce cross-action linkage;
- introduce identity-bearing diagnostic information;
- introduce a separate first-class outcome object;
- create separate ontology documents for Evaluation and Determination;
- redefine implementations;
- redefine implementation profiles;
- redefine conformance;
- redefine certification;
- redefine protocol semantics;
- redefine protocol authority.

<a id="pe-g2-src-s25-sec-029-000"></a>
# 29. Conclusion

A Privacy Engine Protocol Action Evaluation is one identified, bounded, and
authoritative evaluation occurrence that evaluates one identified Protocol
Action against the complete applicable protocol-rule set within one bounded
evaluation context.

A Privacy Engine Protocol Action Determination is the identified and bounded
authoritative result of one completed Evaluation.

Evaluation is the process.

Determination is the result.

Acceptance and rejection are mutually exclusive predicates of the
Determination.

> complete(E) -> produces(E, D)

> accepts(D, A) xor rejects(D, A)

A rejected action has received a complete authoritative evaluation.

An Evaluation failure has not produced a complete authoritative validity
conclusion.

> evaluationFailure(E) =/=> rejects(D, A)

> evaluationFailure(E) =/=> accepts(D, A)

Proof verification contributes bounded evidence.

It does not automatically constitute complete Protocol Action Evaluation.

Incomplete evaluation must never become acceptance.

Infrastructure failure must not silently become protocol rejection.

An accepted determination may authorize a public state transition, but the
transition remains distinct from the action, Evaluation, Determination, and
acceptance predicate.

Protocol Action Evaluation and Protocol Action Determination are two bounded
aspects of one architectural model.

No separate first-class Outcome object is introduced.

Private actors remain private.

Protocol Actions remain public.

Protocol authority always remains with the published Privacy Engine protocol generation.

Candidate status: candidate; unreviewed; unpublished; non-authoritative.
End of PE-G2-SOURCE-S25.
