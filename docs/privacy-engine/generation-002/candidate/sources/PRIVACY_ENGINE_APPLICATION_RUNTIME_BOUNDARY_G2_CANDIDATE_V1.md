<a id="pe-g2-art-pe-g2-source-s43"></a>
# Privacy Engine Application Runtime Boundary G2 Candidate V1

Successor source artifact: PE-G2-SOURCE-S43

Successor generation: PE-PROTOCOL-GENERATION-002

Immutable predecessor: docs/PRIVACY_ENGINE_APPLICATION_RUNTIME_BOUNDARY_V1.md

Immutable predecessor SHA-256: a0ff330cf1045151948828f69eb06236cc734e19132d0ee70248c46b2e49539c

Status: candidate; unreviewed; unpublished; non-authoritative.

All inherited V1 identity, review, publication and current-generation statements below are predecessor derivation text concerning G1 only. They do not assert G2 identity, review, publication or authority. G2 candidate meaning is established by the successor semantic-obligation register and exact section bindings.

## Successor Candidate Semantic-Obligation Register

| Source anchor | Engineering trace input | Successor requirement | Exact successor rule |
|---|---|---|---|
| <a id="pe-g2-src-s43-clar-atomic-009-01"></a> pe-g2-src-s43-clar-atomic-009-01 | CLAR-ATOMIC-009 | PE-G2-SURF-019 | Protocol-semantic Determination production MUST remain distinct from representation, serialization, persistence, publication, transport, operational delivery, display, indexing, events, logs, responses and application interpretation. |
| <a id="pe-g2-src-s43-clar-atomic-009-02"></a> pe-g2-src-s43-clar-atomic-009-02 | CLAR-ATOMIC-009 | PE-G2-EXCLUDE-028 | A later mechanism or observation MUST NOT be treated as creating, replacing or identifying the protocol-semantic completion boundary merely because it represents or reports a Determination. |
| <a id="pe-g2-src-s43-clar-atomic-010-01"></a> pe-g2-src-s43-clar-atomic-010-01 | CLAR-ATOMIC-010 | PE-G2-FAIL-019 | Failure of representation, serialization, persistence, publication, transport, operational delivery, display, indexing or application translation after Determination production MUST NOT erase the Determination, reopen or fail the completed Evaluation, alter its acceptance or rejection classification, or become protocol rejection. |
| <a id="pe-g2-src-s43-clar-atomic-011-01"></a> pe-g2-src-s43-clar-atomic-011-01 | CLAR-ATOMIC-011 | PE-G2-STALEAUTH-013 | Retry of a later representation, publication, transport or delivery operation MUST preserve the same already-produced Determination and MUST NOT produce another Determination or another Evaluation occurrence. |
| <a id="pe-g2-src-s43-clar-atomic-013-01"></a> pe-g2-src-s43-clar-atomic-013-01 | CLAR-ATOMIC-013 | PE-G2-EXCLUDE-029 | Protocol-semantic atomicity MUST NOT be inferred from or defined by implementation transaction atomicity, storage atomicity, event emission, response production, logging, persistence, consensus, rollback or any other implementation mechanism. |
| <a id="pe-g2-src-s43-clar-atomic-014-01"></a> pe-g2-src-s43-clar-atomic-014-01 | CLAR-ATOMIC-014 | PE-G2-FAIL-020 | Operational success or failure MUST remain distinct from Determination production and from formal Evaluation success or failure. |
| <a id="pe-g2-src-s43-clar-atomic-014-02"></a> pe-g2-src-s43-clar-atomic-014-02 | CLAR-ATOMIC-014 | PE-G2-RUNTIME-017 | Operational failure after a Determination exists MUST be classified at the actual later lifecycle layer. |
| <a id="pe-g2-src-s43-clar-atomic-015-01"></a> pe-g2-src-s43-clar-atomic-015-01 | CLAR-ATOMIC-015 | PE-G2-SEMPRES-027 | Every Evaluation, Determination, failure, retry, representation, publication, transport, delivery, diagnostic and observability surface MUST preserve Private Actor non-disclosure, neutral naming, action-bounded public identity and the prohibition on reusable participant identity, actor provenance and cross-action linkage. |

STATE.md remains canonical.
This document is supporting documentation only.

<a id="pe-g2-src-s43-sec-001-000"></a>
# 1. Purpose

This document defines the implementation responsibility boundary between:

- the application
- the application adapter
- the Privacy Engine runtime

It does not redesign the protocol.

It does not define implementation structure, migration, deployment, or contract extraction.

<a id="pe-g2-src-s43-sec-002-000"></a>
# 2. Boundary Principle
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s43-clar-atomic-009-01,pe-g2-src-s43-clar-atomic-009-02,pe-g2-src-s43-clar-atomic-010-01,pe-g2-src-s43-clar-atomic-013-01,pe-g2-src-s43-clar-atomic-014-01,pe-g2-src-s43-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The application chooses the action context.

The Privacy Engine verifies anonymous participation within that context.

The Privacy Engine does not understand application meaning.

<a id="pe-g2-src-s43-sec-003-000"></a>
# 3. Application Responsibility

The application owns:

- application objects
- application metadata
- application lifecycle
- application policy
- application-specific eligibility
- the meaning of an accepted action
- the consequence of an accepted action
- application-specific records and events

For the petition application, this includes:

- petition creation
- petition existence
- petition metadata
- petition lifecycle
- the meaning of a petition signature
- petition-specific signature records
- petition-specific read models

These responsibilities remain outside the Privacy Engine runtime.

<a id="pe-g2-src-s43-sec-004-000"></a>
# 4. Privacy Engine Runtime Responsibility
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s43-clar-atomic-009-01,pe-g2-src-s43-clar-atomic-009-02,pe-g2-src-s43-clar-atomic-010-01,pe-g2-src-s43-clar-atomic-011-01,pe-g2-src-s43-clar-atomic-013-01,pe-g2-src-s43-clar-atomic-014-01,pe-g2-src-s43-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The Privacy Engine runtime owns authoritative anonymous-action verification for an application-supplied action context.

It owns:

- proof verification
- public-signal validation
- membership-root validation
- nullifier enforcement
- anonymous-action acceptance or rejection
- protocol-level duplicate prevention
- preservation of protocol invariants
- publication of the protocol-valid action result

The runtime determines only:

> whether a valid anonymous member performed one valid action within the supplied action context.

It does not determine what that action means.

<a id="pe-g2-src-s43-sec-005-000"></a>
# 5. Application Adapter Responsibility
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s43-clar-atomic-009-01,pe-g2-src-s43-clar-atomic-009-02,pe-g2-src-s43-clar-atomic-010-01,pe-g2-src-s43-clar-atomic-011-01,pe-g2-src-s43-clar-atomic-013-01,pe-g2-src-s43-clar-atomic-014-01,pe-g2-src-s43-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The application adapter is the boundary between application meaning and protocol verification.

It owns:

- receiving the application-selected action context
- preserving that context
- presenting the context to the Privacy Engine runtime
- receiving the runtime result
- returning that result to the application
- applying no independent interpretation of protocol validity

The adapter must not:

- choose a different action context
- redefine protocol acceptance
- duplicate proof verification
- duplicate membership-root validation
- duplicate nullifier enforcement
- modify protocol outputs
- expose application meaning to the runtime

<a id="pe-g2-src-s43-sec-006-000"></a>
# 6. Action Context

The action context is selected by the application.

It identifies the application action for which anonymous participation is being verified.

For the current petition implementation:

`petitionId` is the action context.

At the protocol boundary:

`petitionId` functions as `actionId`.

The runtime requires only the stable action context value.

It does not require knowledge that the value represents a petition.

<a id="pe-g2-src-s43-sec-007-000"></a>
# 7. Anonymous-Action Acceptance
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s43-clar-atomic-009-01,pe-g2-src-s43-clar-atomic-009-02,pe-g2-src-s43-clar-atomic-010-01,pe-g2-src-s43-clar-atomic-014-01,pe-g2-src-s43-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


Anonymous-action acceptance requires:

- a valid proof
- the locked public signal structure
- a valid membership root
- a nullifier derived for the supplied action context
- an unused nullifier within that context

Acceptance means only:

> anonymous participation is protocol-valid for the supplied action context.

Acceptance does not mean:

- the application object exists
- the application permits the action
- the action has application meaning
- application state has been updated
- application policy has been satisfied

Those remain application responsibilities.

<a id="pe-g2-src-s43-sec-008-000"></a>
# 8. Responsibility Sequence
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s43-clar-atomic-009-01,pe-g2-src-s43-clar-atomic-009-02,pe-g2-src-s43-clar-atomic-010-01,pe-g2-src-s43-clar-atomic-011-01,pe-g2-src-s43-clar-atomic-013-01,pe-g2-src-s43-clar-atomic-014-01,pe-g2-src-s43-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The responsibility sequence is:

Application chooses action context.

Application Adapter preserves action context.

Privacy Engine Runtime verifies anonymous participation.

Application Adapter returns the verification result.

Application applies the application-specific consequence.

Formally:

A = application-selected action context

Application:
    choose A

Adapter:
    preserve A

Runtime:
    verify anonymous participation within A

Adapter:
    return accepted(A) or rejected(A)

Application:
    apply application consequence only after accepted(A)

Forbidden paths:

Runtime chooses A

Runtime interprets A

Runtime changes A -> A'

Adapter repairs or replaces A

Application redefines runtime acceptance

<a id="pe-g2-src-s43-sec-009-000"></a>
# 9. PetitionRegistry Responsibility Split

The current PetitionRegistry contains both petition-application and Privacy Engine runtime responsibilities.

Protocol responsibilities currently present within it include:

- proof verification
- membership-root validation
- public-signal validation
- nullifier uniqueness enforcement
- anonymous-action acceptance

Petition-application responsibilities currently present within it include:

- petition creation
- petition existence
- petition metadata association
- petition-specific action records
- petition-specific events
- petition signature consequences

The current co-location does not change responsibility ownership.

Protocol enforcement remains Privacy Engine responsibility.

Petition meaning remains application responsibility.

<a id="pe-g2-src-s43-sec-010-000"></a>
# 10. Invariant Preservation
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014,CLAR-ATOMIC-015; semantic-obligation-anchors=pe-g2-src-s43-clar-atomic-009-01,pe-g2-src-s43-clar-atomic-009-02,pe-g2-src-s43-clar-atomic-010-01,pe-g2-src-s43-clar-atomic-011-01,pe-g2-src-s43-clar-atomic-013-01,pe-g2-src-s43-clar-atomic-014-01,pe-g2-src-s43-clar-atomic-014-02,pe-g2-src-s43-clar-atomic-015-01; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-SEMPRES-027,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


This boundary preserves:

- the existing ZK circuit
- public signal ordering
- leaf = Poseidon1(memberSecret)
- nullifier derivation
- membership-root semantics
- one action per anonymous member per action context
- TEMPEST execution semantics
- REFLECT path semantics
- frontend secret-custody semantics
- frontend privacy semantics
- externally visible petition behaviour

No cryptographic or protocol semantic change is required.

<a id="pe-g2-src-s43-sec-011-000"></a>
# 11. Application Independence

The Privacy Engine runtime is application-independent when:

- the application supplies an action context
- the runtime verifies anonymous participation against that context
- the runtime does not know the application object type
- the runtime does not know the application policy
- the runtime does not determine the application consequence
- application semantics can change without changing protocol verification

Application independence does not require hypothetical application support.

It requires only the absence of petition meaning from runtime responsibility.

<a id="pe-g2-src-s43-sec-012-000"></a>
# 12. Minimum Runtime Boundary
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s43-clar-atomic-009-01,pe-g2-src-s43-clar-atomic-009-02,pe-g2-src-s43-clar-atomic-010-01,pe-g2-src-s43-clar-atomic-011-01,pe-g2-src-s43-clar-atomic-013-01,pe-g2-src-s43-clar-atomic-014-01,pe-g2-src-s43-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The minimum application-independent runtime is the authority that:

1. accepts an application-supplied action context
2. verifies the anonymous-action proof
3. validates the membership root
4. enforces nullifier uniqueness
5. returns authoritative acceptance or rejection

Nothing else is required by this boundary.

<a id="pe-g2-src-s43-sec-013-000"></a>
# 13. Conclusion
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s43-clar-atomic-009-01,pe-g2-src-s43-clar-atomic-009-02,pe-g2-src-s43-clar-atomic-010-01,pe-g2-src-s43-clar-atomic-011-01,pe-g2-src-s43-clar-atomic-013-01,pe-g2-src-s43-clar-atomic-014-01,pe-g2-src-s43-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The application owns action meaning.

The application chooses the action context.

The application adapter preserves and conveys that context.

The Privacy Engine runtime authoritatively verifies anonymous participation within that context.

The runtime does not understand, select, modify, or apply application meaning.

The current implementation already contains this runtime responsibility.

The remaining alignment requirement is to preserve this responsibility boundary explicitly at the implementation level.

Candidate status: candidate; unreviewed; unpublished; non-authoritative.
End of PE-G2-SOURCE-S43.
