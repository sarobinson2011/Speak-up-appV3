<a id="pe-g2-art-pe-g2-semantic-difference-001"></a>
# Privacy Engine Generation 2 Evaluation Determination Atomicity Semantic Difference V1

Artifact identifier: PE-G2-SEMANTIC-DIFFERENCE-001
Engineering inputs: CLAR-ATOMIC-001 through CLAR-ATOMIC-015
<a id="pe-g2-delta-atomic-001"></a>
Success boundary: active(E) and incomplete(E) and readyToComplete(E) -> complete(E) and producesExactlyOne(E, D) and exactlyOneClassification(D)
<a id="pe-g2-delta-atomic-002"></a>
Classification: exactlyOneClassification(D) = accepts(D, A) xor rejects(D, A)
<a id="pe-g2-delta-atomic-003"></a>
Forbidden state: complete(E) and not producesExactlyOne(E, D)
<a id="pe-g2-delta-atomic-004"></a>
Terminal Evaluation failure: terminalEvaluationFailure(E) and incomplete(E) and not active(E) and no D and no acceptance or rejection
<a id="pe-g2-delta-atomic-005"></a>
Later-realization retry: produced(D) and laterRealizationFailure(D) -> retrySameRealization(D)
<a id="pe-g2-delta-atomic-006"></a>
Re-evaluation: terminalEvaluationFailure(E1) and later authoritative evaluation -> new Evaluation occurrence E2, with E1 != E2
<a id="pe-g2-delta-atomic-007"></a>
Non-retroactivity: a terminally failed Evaluation occurrence cannot later become complete; a successor generation cannot alter a predecessor-governed Evaluation occurrence.
<a id="pe-g2-delta-atomic-008"></a>
Implementation independence: protocol-semantic atomicity is not implementation transaction, storage, event, response, logging, persistence, consensus, rollback, transport or delivery atomicity.
<a id="pe-g2-delta-atomic-009"></a>
Privacy: Private actors, public actions; no reusable participant identity, actor provenance or cross-action linkage.
<a id="pe-g2-delta-atomic-010"></a>
Authority: the published predecessor remains authoritative for predecessor-governed semantics.

Candidate status: candidate; unreviewed; unpublished; non-authoritative.
End of PE-G2-SEMANTIC-DIFFERENCE-001.
