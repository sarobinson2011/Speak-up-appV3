# PE-G4-SOURCE-S74 — unpublished G4 source candidate

Status: candidate construction, not appointed or published. The following inherited authoring narrative is preserved with explicit identifier substitution. Its references to unallocated identities and earlier chat status are historical; identity.json and sources/PE-G4-SOURCE-S82.md govern this candidate. No compatible semantic duty is waived.

# Draft root-policy source — exact selected semantics

Draft owner label: PE-G4-SOURCE-S74. This is a documentary source draft, not an authenticated successor SOURCE-SNN or admitted profile owner. The local label does not allocate a generation/source-member identity. Steve has authorized the root-policy semantics and Route B. Publication/admission authority remains separate.

<a id="root-domain"></a>
## Root domain and history

For the retained Groth16-over-BN254 anonymous-action relation, roots and public scalar inputs denote canonical scalar-field values. The scalar modulus is 21888242871839275222246405745257275088548364400416034343698204186575808495617; it is distinct from the BN254 base-field modulus. The archived verifier declares the scalar constant at line 25; PROOF-009 requires the retained proof semantics. No modular reduction of an out-of-domain public input is silently permitted by this draft. A complete decoder/domain/status definition must establish the canonical value before the expression consumes it. The TSV type UINT alone does not validate that domain.

History H is the finite authoritative sequence of valid membership-root introductions for the governing membership-state scope at the applicable observation cut. Initial introduction counts; absent entries do not. Retransmission or another observation of the same introduction does not count again. A genuinely distinct introduction of an equal root does count. Validity of the introduced membership state and authentic complete history must be established from the governing membership/source rules; this policy does not authorize their mutation or derive authority from an event log.

Define K=min(16,length(H)). Define slots s1…s16 newest first: for i<=K, si is the root value at introduction length(H)-i+1 and oi=TRUE; for i>K, si=0 and oi=FALSE. Occupancy flags must be a TRUE prefix followed by FALSE, and absent slots have canonical zero payloads. Repeated root values are not collapsed before this projection. A zero-valued occupied slot is not discarded if its root is valid under the membership source; zero padding is distinguished by occupancy. The logical prefix/subscript notation specifies source meaning; it is not an added PE-TSE expression operator.

### Incorporated proposal: root-window

For the selected capability, H MUST be the finite authoritative sequence of valid membership-root introductions in its governing membership scope at the applicable cut. Root eligibility MUST use exactly its latest min(16,|H|) introduction occurrences, newest first. A distinct valid introduction of an equal value MUST count separately; a retransmission or repeated observation of one introduction MUST NOT count again. An initial root MUST count only if authoritatively introduced.

<a id="root-acceptance"></a>
## Exact expression and ordered signature

The ROOT-ACCEPTED definition in definitions.tsv has 33 inputs:

| Ordinals | Meaning | Type |
|---|---|---|
| 0001 | Declared root r, fixed by the proof/public-input context | PE-TSE-UINT within the declared root domain |
| 0002–0017 | s1…s16, newest first | PE-TSE-UINT; occupied roots valid, absent payload zero |
| 0018–0033 | o1…o16 corresponding one-to-one to those slots | PE-TSE-BOOL3; complete valid observations use TRUE/FALSE only |

For complete valid authenticated inputs, ROOT-ACCEPTED is TRUE exactly when some occupied slot equals r. It is FALSE otherwise. An empty history therefore yields FALSE. Validity and authentication of the complete suffix, its cut, ordering, scope, canonical domain and binding to r are prior obligations; this expression cannot authenticate them. Unknown slot/history material is not a trusted empty slot.

The expanded expression uses only or, and, equal and arg. It does not use a dynamic SET, an unimplemented membership primitive, indexing or a new expression-language operation. Existing `member` accepts an owned literal SET definition, so it is not used to disguise a mutable history as a static set. The 33-input form is a finite explicit realization of the selected latest-16 rule, not a new semantic policy or an allocated final interface.

### Incorporated proposal: root-padding

The declared root r MUST be eligible exactly when it equals the root of at least one occupied introduction in that suffix. An empty history MUST yield ineligibility. An unoccupied slot MUST NOT confer eligibility, including for zero; an occupied zero MUST receive no privilege or exclusion beyond the governing membership-state validity rules.

<a id="observation"></a>
## Observation and gate contract

E evaluates the fixed declared r in its bounded coherent C. The same r must be accepted at PRE-EXECUTION and semantic PRE-COMMITMENT against independently authenticated current facts. Newer roots alone are immaterial if r remains accepted and every other required condition remains satisfied. Expiry is material; it does not retroactively alter D. Comparison and commitment remain one indivisible protocol-semantic boundary, with no mandated transaction or consensus mechanism.

Complete and authentic observations require evidence of the authoritative applicable state, not merely possession of these 33 values. No provider, chain address, finality threshold or key is appointed. Exact source/cut/coordinate authority and evidence-sufficiency definitions remain external/source-closure obligations. The slot representation itself grants no permission to disclose histories or acquisition topology.

### Incorporated proposal: root-stages

The same fixed declared r MUST satisfy the selected root policy at E and independently at both PRE-EXECUTION and PRE-COMMITMENT. Later root expiry MUST NOT alter an existing D. A change to history that preserves eligibility MUST NOT alone establish material conflict; actual changed dependencies MUST remain subject to full unchanged-D assessment.

<a id="preservation"></a>
## Source support and limits

Preserved: S19 §4.4; S22 §§6/8/12; S24 §§9–11; S25 §§8–14/22; S70 TYPES/DEPENDENCY/COMPARISON/PRIVACY; S71 AUTHORIZATION/COMMITMENT. Selected new policy details are recorded in Engineering-283-policy-effect-selection.md. STATE §4 and I164 ZK_CIRCUIT_SPEC §§3.3/6 provide the last-16 baseline prescription, not universal protocol authority or optimality evidence.

The source definition and its expression are now concrete. Complete membership-introduction/domain/status/authentication reference closure is not claimed. I164 repeated-root/zero-sentinel correspondence questions from B13 remain, without asserting reachable live behavior. No implementation is authorized by these draft bytes.

## Exact source-owned definition declarations

The following declarations specialize the retained PE-TSE-EXPR-V2 grammar. The source_anchor column identifies the semantic clause above. They are construction candidates, not independently admitted declarations.

```tsv
definition_order	definition_id	kind	input_type_ids	output_type_id	expression	source_id	source_anchor
0001	PE-G4-CAP-ROOT-ACCEPTED	CONDITION	PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3	PE-TSE-BOOL3	or(and(arg(0018),equal(arg(0001),arg(0002))),and(arg(0019),equal(arg(0001),arg(0003))),and(arg(0020),equal(arg(0001),arg(0004))),and(arg(0021),equal(arg(0001),arg(0005))),and(arg(0022),equal(arg(0001),arg(0006))),and(arg(0023),equal(arg(0001),arg(0007))),and(arg(0024),equal(arg(0001),arg(0008))),and(arg(0025),equal(arg(0001),arg(0009))),and(arg(0026),equal(arg(0001),arg(0010))),and(arg(0027),equal(arg(0001),arg(0011))),and(arg(0028),equal(arg(0001),arg(0012))),and(arg(0029),equal(arg(0001),arg(0013))),and(arg(0030),equal(arg(0001),arg(0014))),and(arg(0031),equal(arg(0001),arg(0015))),and(arg(0032),equal(arg(0001),arg(0016))),and(arg(0033),equal(arg(0001),arg(0017))))	PE-G4-SOURCE-S74	root-acceptance
```
