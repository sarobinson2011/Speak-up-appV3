<a id="pe-g2-art-pe-g2-source-s47"></a>
# Privacy Engine Runtime Model G2 Candidate V1

Successor source artifact: PE-G2-SOURCE-S47

Successor generation: PE-PROTOCOL-GENERATION-002

Immutable predecessor: docs/PRIVACY_ENGINE_RUNTIME_MODEL_V1.md

Immutable predecessor SHA-256: 15c0ad7a7b87343946ad5d61ba720730791c883f8f4cc1dbd8ad0d4f8a6d2398

Status: candidate; unreviewed; unpublished; non-authoritative.

All inherited V1 identity, review, publication and current-generation statements below are predecessor derivation text concerning G1 only. They do not assert G2 identity, review, publication or authority. G2 candidate meaning is established by the successor semantic-obligation register and exact section bindings.

## Successor Candidate Semantic-Obligation Register

| Source anchor | Engineering trace input | Successor requirement | Exact successor rule |
|---|---|---|---|
| <a id="pe-g2-src-s47-clar-atomic-009-01"></a> pe-g2-src-s47-clar-atomic-009-01 | CLAR-ATOMIC-009 | PE-G2-SURF-019 | Protocol-semantic Determination production MUST remain distinct from representation, serialization, persistence, publication, transport, operational delivery, display, indexing, events, logs, responses and application interpretation. |
| <a id="pe-g2-src-s47-clar-atomic-009-02"></a> pe-g2-src-s47-clar-atomic-009-02 | CLAR-ATOMIC-009 | PE-G2-EXCLUDE-028 | A later mechanism or observation MUST NOT be treated as creating, replacing or identifying the protocol-semantic completion boundary merely because it represents or reports a Determination. |
| <a id="pe-g2-src-s47-clar-atomic-010-01"></a> pe-g2-src-s47-clar-atomic-010-01 | CLAR-ATOMIC-010 | PE-G2-FAIL-019 | Failure of representation, serialization, persistence, publication, transport, operational delivery, display, indexing or application translation after Determination production MUST NOT erase the Determination, reopen or fail the completed Evaluation, alter its acceptance or rejection classification, or become protocol rejection. |
| <a id="pe-g2-src-s47-clar-atomic-011-01"></a> pe-g2-src-s47-clar-atomic-011-01 | CLAR-ATOMIC-011 | PE-G2-STALEAUTH-013 | Retry of a later representation, publication, transport or delivery operation MUST preserve the same already-produced Determination and MUST NOT produce another Determination or another Evaluation occurrence. |
| <a id="pe-g2-src-s47-clar-atomic-013-01"></a> pe-g2-src-s47-clar-atomic-013-01 | CLAR-ATOMIC-013 | PE-G2-EXCLUDE-029 | Protocol-semantic atomicity MUST NOT be inferred from or defined by implementation transaction atomicity, storage atomicity, event emission, response production, logging, persistence, consensus, rollback or any other implementation mechanism. |
| <a id="pe-g2-src-s47-clar-atomic-014-01"></a> pe-g2-src-s47-clar-atomic-014-01 | CLAR-ATOMIC-014 | PE-G2-FAIL-020 | Operational success or failure MUST remain distinct from Determination production and from formal Evaluation success or failure. |
| <a id="pe-g2-src-s47-clar-atomic-014-02"></a> pe-g2-src-s47-clar-atomic-014-02 | CLAR-ATOMIC-014 | PE-G2-RUNTIME-017 | Operational failure after a Determination exists MUST be classified at the actual later lifecycle layer. |
| <a id="pe-g2-src-s47-clar-atomic-015-01"></a> pe-g2-src-s47-clar-atomic-015-01 | CLAR-ATOMIC-015 | PE-G2-SEMPRES-027 | Every Evaluation, Determination, failure, retry, representation, publication, transport, delivery, diagnostic and observability surface MUST preserve Private Actor non-disclosure, neutral naming, action-bounded public identity and the prohibition on reusable participant identity, actor provenance and cross-action linkage. |

STATE.md remains canonical.
This document is supporting documentation only.

<a id="pe-g2-src-s47-sec-001-000"></a>
# 1. Purpose of the Runtime

The Privacy Engine runtime is the architectural authority responsible for executing the published Privacy Engine protocol.

Its purpose is to preserve protocol semantics during execution.

It does not:

- define protocol truth
- define application behavior
- define business meaning
- redefine published protocol semantics
- redesign protocol architecture

<a id="pe-g2-src-s47-sec-002-000"></a>
# 2. Definition of the Privacy Engine Runtime

The Privacy Engine runtime is the bounded architectural authority responsible for executing and preserving the published anonymous participation semantics of the Privacy Engine protocol.

The runtime executes protocol behavior.

It does not determine application behavior.

<a id="pe-g2-src-s47-sec-003-000"></a>
# 3. Runtime Authority
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s47-clar-atomic-009-01,pe-g2-src-s47-clar-atomic-009-02,pe-g2-src-s47-clar-atomic-010-01,pe-g2-src-s47-clar-atomic-013-01,pe-g2-src-s47-clar-atomic-014-01,pe-g2-src-s47-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The runtime exclusively owns authority for:

- execution of published protocol semantics
- preservation of protocol invariants
- anonymous participation verification
- protocol-defined state transitions
- protocol interface execution

Application meaning remains outside runtime authority.

<a id="pe-g2-src-s47-sec-004-000"></a>
# 4. Runtime Responsibilities
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s47-clar-atomic-009-01,pe-g2-src-s47-clar-atomic-009-02,pe-g2-src-s47-clar-atomic-010-01,pe-g2-src-s47-clar-atomic-011-01,pe-g2-src-s47-clar-atomic-013-01,pe-g2-src-s47-clar-atomic-014-01,pe-g2-src-s47-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The runtime is responsible for:

- verifying anonymous participation
- preserving protocol invariants
- executing protocol-defined interfaces
- coordinating protocol-layer execution
- rejecting invalid protocol execution

The runtime preserves published protocol semantics.

It does not redefine them.

<a id="pe-g2-src-s47-sec-005-000"></a>
# 5. Runtime-Owned Interfaces
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s47-clar-atomic-009-01,pe-g2-src-s47-clar-atomic-009-02,pe-g2-src-s47-clar-atomic-010-01,pe-g2-src-s47-clar-atomic-013-01,pe-g2-src-s47-clar-atomic-014-01,pe-g2-src-s47-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The runtime owns the interfaces required to execute the published Privacy Engine protocol.

These interfaces expose protocol behavior.

They do not expose application meaning.

Application-specific interfaces remain outside the runtime.

<a id="pe-g2-src-s47-sec-006-000"></a>
# 6. Runtime Relationships
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s47-clar-atomic-009-01,pe-g2-src-s47-clar-atomic-009-02,pe-g2-src-s47-clar-atomic-010-01,pe-g2-src-s47-clar-atomic-011-01,pe-g2-src-s47-clar-atomic-013-01,pe-g2-src-s47-clar-atomic-014-01,pe-g2-src-s47-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


## Application

The application owns:

- action meaning
- business rules
- application state

The runtime does not interpret application meaning.

## Application Adapter

The application adapter conveys application context to the runtime.

It does not modify protocol semantics.

## M2

M2 provides anonymous identity and proof material.

The runtime verifies anonymous participation using the published M2 protocol.

## TEMPEST

TEMPEST provides the execution and submission layer.

The runtime preserves protocol semantics regardless of execution routing.

## REFLECT

REFLECT provides witness and path material.

The runtime preserves protocol semantics regardless of witness distribution.

<a id="pe-g2-src-s47-sec-007-000"></a>
# 7. Runtime Invariants
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014,CLAR-ATOMIC-015; semantic-obligation-anchors=pe-g2-src-s47-clar-atomic-009-01,pe-g2-src-s47-clar-atomic-009-02,pe-g2-src-s47-clar-atomic-010-01,pe-g2-src-s47-clar-atomic-011-01,pe-g2-src-s47-clar-atomic-013-01,pe-g2-src-s47-clar-atomic-014-01,pe-g2-src-s47-clar-atomic-014-02,pe-g2-src-s47-clar-atomic-015-01; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-SEMPRES-027,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The runtime preserves:

- protocol identity
- published protocol semantics
- anonymous participation semantics
- layer responsibility boundaries
- published protocol interfaces
- protocol-defined invariants

The runtime preserves these invariants during execution.

It does not redefine them.

<a id="pe-g2-src-s47-sec-008-000"></a>
# 8. What the Runtime Is Not
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s47-clar-atomic-009-01,pe-g2-src-s47-clar-atomic-009-02,pe-g2-src-s47-clar-atomic-010-01,pe-g2-src-s47-clar-atomic-011-01,pe-g2-src-s47-clar-atomic-013-01,pe-g2-src-s47-clar-atomic-014-01,pe-g2-src-s47-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The runtime is not:

- an application
- an application adapter
- a business-logic engine
- an identity authority
- a policy engine
- a protocol redesign mechanism
- an implementation-planning layer

Its authority is limited to execution of the published protocol.

<a id="pe-g2-src-s47-sec-009-000"></a>
# 9. Conclusion
G2 candidate section binding: clarification-inputs=CLAR-ATOMIC-009,CLAR-ATOMIC-010,CLAR-ATOMIC-011,CLAR-ATOMIC-013,CLAR-ATOMIC-014; semantic-obligation-anchors=pe-g2-src-s47-clar-atomic-009-01,pe-g2-src-s47-clar-atomic-009-02,pe-g2-src-s47-clar-atomic-010-01,pe-g2-src-s47-clar-atomic-011-01,pe-g2-src-s47-clar-atomic-013-01,pe-g2-src-s47-clar-atomic-014-01,pe-g2-src-s47-clar-atomic-014-02; successor-requirements=PE-G2-EXCLUDE-028,PE-G2-EXCLUDE-029,PE-G2-FAIL-019,PE-G2-FAIL-020,PE-G2-RUNTIME-017,PE-G2-STALEAUTH-013,PE-G2-SURF-019; status=candidate-unreviewed-unpublished-non-authoritative.


The Privacy Engine runtime is the minimal architectural authority responsible for preserving and executing the published anonymous participation semantics of the Privacy Engine protocol.

It executes protocol behavior, preserves protocol invariants, and exposes protocol-defined interfaces without assuming application meaning or altering published protocol semantics.

Candidate status: candidate; unreviewed; unpublished; non-authoritative.
End of PE-G2-SOURCE-S47.
