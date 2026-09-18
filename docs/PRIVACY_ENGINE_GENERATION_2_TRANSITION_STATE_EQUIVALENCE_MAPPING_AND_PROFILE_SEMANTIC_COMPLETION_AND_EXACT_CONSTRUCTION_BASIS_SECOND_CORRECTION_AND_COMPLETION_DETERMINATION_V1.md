# Privacy Engine Generation 2 Transition-State Equivalence Mapping and Profile Semantic Completion and Exact Construction-Basis Second Correction and Completion Determination V1

Identifier:
PE-TRANSITION-STATE-EQUIVALENCE-MAPPING-AND-PROFILE-SEMANTIC-COMPLETION-AND-EXACT-CONSTRUCTION-BASIS-SECOND-CORRECTION-AND-COMPLETION-DETERMINATION-V1

Document version:
V1

Result:
transition-state-equivalence-mapping-and-profile-semantic-completion-and-exact-construction-basis-second-correction-and-completion-resolved

Authority classification:
development-authority-determination-non-protocol-non-publication

## 1. Status, scope and immutable inputs

This determination corrects and completes the Engineering[248] basis in response to the complete Engineering[249] read-only independent review. It does not amend, reopen or reinterpret published Generation 2. It defines development authority for construction of a distinct future successor only.

The immutable correction inputs are:

| Input | SHA-256 | Bytes | LF |
|---|---|---:|---:|
| Engineering[248] determination | `1f5b59b0ff4720ee142a42017f13e543e1a3973fd81113ca86ca2ead43834a73` | 93575 | 721 |
| Engineering[247] report | `35f2ce9bb84aaec7e3d5dfecb341d3d04cadb65060d89028a4e70a08e731bcc5` | 21318 | 228 |
| Engineering[249] report | `636899f5426b8a70065b7f7193bba8ef1d0542e10c2ecc014a90cea39990bb37` | 19543 | 331 |
| Published G2 specification | `ffeaed785a34e8535d489ad6946dbdae3a55b441a0c94c8c05791eb33fd423e1` | 359620 | 4131 |

Engineering[248] remains an input but its sections 3 through 19 are replaced wherever this determination supplies a rule with the same subject. In a conflict, this determination governs successor construction. Unchanged Engineering[248] registers, paths and predecessor bindings remain inputs only where this determination explicitly imports them.

The permitted later-authorized parameters remain exactly:

1. `SUCCESSOR-GENERATION-ID`;
2. `SUCCESSOR-GENERATION-LABEL`;
3. `SUCCESSOR-NAMESPACE`;
4. `SUCCESSOR-VERSION`.

No other constructor-selected semantic value exists. `M = 0`. A mapping or profile MUST NOT be inferred from I164, Speak Up, another implementation, runtime evidence or observed behaviour.

## 2. Canonical data model and lexical grammar

All construction text is UTF-8 without BOM, Unicode NFC, LF-only, has no trailing horizontal whitespace and ends in exactly one LF. ASCII terminals below are case-sensitive. `DIGIT`, `HEXDIG`, `ALPHA` and `LF` have their RFC 5234 meanings. `SP` is one U+0020.

The expression language identifier is `PE-TSE-EXPR-V1`.

```abnf
ord2        = 2DIGIT
ord3        = 3DIGIT
ord4        = 4DIGIT
ord6        = 6DIGIT
uint        = "0" / (%x31-39 *DIGIT)
hex-octet   = 2HEXDIG
hex-bytes   = hex-octet *(hex-octet)
sha256      = 64(%x30-39 / %x61-66)
id-first    = %x41-5A
id-rest     = %x41-5A / DIGIT / "-"
identifier  = id-first *id-rest
type-id     = identifier
def-id      = identifier
component-id = identifier
side        = "BASE" / "CURRENT"
bool3       = "TRUE" / "FALSE" / "UNRESOLVED"
expr        = literal / reference / equal / unequal / conjunction / disjunction / negation / membership / application / condition
literal     = "literal(" type-id "," hex-bytes ")"
reference   = "ref(" component-id "," side ")"
equal       = "eq(" expr "," expr ")"
unequal     = "ne(" expr "," expr ")"
conjunction = "and(" expr "," expr ")"
disjunction = "or(" expr "," expr ")"
negation    = "not(" expr ")"
membership  = "member(" expr "," def-id ")"
application = "apply(" def-id ["," expr *("," expr)] ")"
condition   = "condition(" def-id ["," expr *("," expr)] ")"
```

Canonical expressions contain no whitespace. Hexadecimal is lowercase, non-empty and even-length. Identifiers MUST satisfy the grammar and MUST NOT contain consecutive hyphens or end in a hyphen.

The primitive type roots are exactly:

| Type | Canonical value |
|---|---|
| `PE-TSE-BOOL3` | one of the three ASCII tokens in `bool3` |
| `PE-TSE-BYTES` | a finite octet string |
| `PE-TSE-ID` | an `identifier` encoded as ASCII |
| `PE-TSE-UINT` | a `uint` encoded as ASCII |

Derived type records use this exact TSV schema:

```text
type_order\ttype_id\tkind\telement_type_id\tfield_type_ids
```

`kind` is `PRIMITIVE`, `SET` or `TUPLE`. The four roots are `PRIMITIVE` and use `NOT-APPLICABLE` in the final two cells. `SET` has one earlier `element_type_id` and `NOT-APPLICABLE` in `field_type_ids`. `TUPLE` has `NOT-APPLICABLE` in `element_type_id` and a non-empty comma-separated list of earlier type IDs in field order. Type order begins at `0001`, is contiguous and is the only permitted dependency order. Forward references and cycles are invalid.

Definition records use this exact TSV schema:

```text
definition_order\tdefinition_id\tkind\tinput_type_ids\toutput_type_id\texpression\tsource_id\tsource_anchor
```

`kind` is exactly `SET`, `CONDITION` or `FUNCTION`. `SET` has no inputs, an output type of `SET`, and an expression that is a canonical sorted list encoded as `apply(PE-TSE-SET,<literal>...)`; duplicate members are invalid. `CONDITION` returns `PE-TSE-BOOL3`. `FUNCTION` returns its declared output type. Input types are comma-separated or `NONE`. Every referenced type and definition MUST have a lower order. Every definition is therefore a finite DAG. `source_id` and `source_anchor` MUST identify the one successor normative source that owns the definition. Profile-local or implementation-owned definitions are invalid.

Operator typing and arity are exact:

| Form | Inputs | Output |
|---|---|---|
| `literal` | declared primitive or derived value | declared type |
| `ref` | zero evaluated arguments; component declaration supplies type | component type |
| `eq`, `ne` | two values of the same type | `PE-TSE-BOOL3` |
| `and`, `or` | two `PE-TSE-BOOL3` values | `PE-TSE-BOOL3` |
| `not` | one `PE-TSE-BOOL3` value | `PE-TSE-BOOL3` |
| `member` | one value matching the set element type | `PE-TSE-BOOL3` |
| `apply` | exactly the definition input arity and types | definition output type |
| `condition` | a `CONDITION` definition with its exact arity and types | `PE-TSE-BOOL3` |

`ref` returns authenticated, represented bytes first, then applies the component's canonicalization and normalization definitions, and returns the resulting canonical typed value. Absence, failed authentication, invalid representation, canonicalization failure, normalization failure, type failure, definition failure or unavailable authority returns `UNRESOLVED` when the required result is Boolean and `NO-VALUE` otherwise. Any operator receiving `NO-VALUE` returns `UNRESOLVED` for a Boolean output or `NO-VALUE` for another output. It MUST NOT coerce failure to `FALSE` or an empty value.

The three-status truth tables are:

| A | B | `and(A,B)` | `or(A,B)` |
|---|---|---|---|
| TRUE | TRUE | TRUE | TRUE |
| TRUE | FALSE | FALSE | TRUE |
| TRUE | UNRESOLVED | UNRESOLVED | TRUE |
| FALSE | TRUE | FALSE | TRUE |
| FALSE | FALSE | FALSE | FALSE |
| FALSE | UNRESOLVED | FALSE | UNRESOLVED |
| UNRESOLVED | TRUE | UNRESOLVED | TRUE |
| UNRESOLVED | FALSE | FALSE | UNRESOLVED |
| UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED |

`not(TRUE)=FALSE`, `not(FALSE)=TRUE` and `not(UNRESOLVED)=UNRESOLVED`. `eq` and `ne` return `UNRESOLVED` if either operand is `NO-VALUE`; otherwise they use canonical typed-byte equality and are complements. `member` returns `UNRESOLVED` on failure, otherwise exact canonical membership.

## 3. Profile ownership and validation

The profile is a successor-source-owned immutable object. Its ordered members are: identity record; type records; definition records; component records; equivalence expression; sufficient-conflict expressions; immaterial-difference records; Dep(D) node records; Dep(D) edge records; recovery rows; component privacy rows; composition privacy record. Each member is digest-bound by the profile manifest. A reference outside this closed member set or the 70-source successor closed set is invalid.

Profile validation is a total function returning `VALID` or `INVALID`. It returns `INVALID` upon the first check failure in this order: lexical grammar; identity uniqueness; type order; definition order; source ownership; component completeness; expression typing; expression totality over declared complete inputs; sufficient-conflict independence; immaterial-difference proof binding; dependency closure; recovery coverage; component privacy; composition privacy; digest closure. An invalid profile authorizes zero transitions.

## 4. Total comparison procedure

Each comparison attempt has the immutable identity:

```text
{U-ID}-TSE-CMP-{ORD6}
```

Ordinals begin at `000001` and are contiguous within U. The exact attempt record fields are: attempt ID; generation ID; mapping ID and digest; profile ID and digest; authorization ID and digest; U ID; D ID; Q0 ID and digest; current-state ID and digest; stage; result; failure code. `stage` is `PRE-EXECUTION` or `PRE-COMMITMENT`. `result` is `equivalent`, `material-conflict` or `indeterminate`. `failure_code` is `NONE` or one code from the closed table below.

Evaluation proceeds in this order:

1. Validate every identity grammar, registered identity relationship and digest.
2. Validate the profile, authorization, opening evidence and authoritative state authentication.
3. Evaluate the equivalence expression `EQ`.
4. Evaluate every sufficient-conflict expression in profile order and set `MC=TRUE` if any is TRUE, `MC=FALSE` if all are FALSE, otherwise `MC=UNRESOLVED`.
5. Apply the following first-match table.

| Condition | Result | Failure code |
|---|---|---|
| phase 1 or 2 failure | indeterminate | exact failing validation code |
| `EQ=TRUE` and `MC=TRUE` | indeterminate | `INCONSISTENT-BOTH-TRUE` |
| `MC=TRUE` | material-conflict | `NONE` |
| `EQ=TRUE` and `MC=FALSE` | equivalent | `NONE` |
| `EQ=FALSE` and `MC=FALSE` | indeterminate | `INCOMPLETE-PROFILE-COVERAGE` |
| otherwise | indeterminate | `UNRESOLVED-REQUIRED-INPUT` |

The closed validation failure codes are `INVALID-IDENTITY`, `UNREGISTERED-IDENTITY`, `DIGEST-MISMATCH`, `INVALID-PROFILE`, `INVALID-AUTHORIZATION`, `INVALID-OPENING`, `UNAUTHENTICATED-STATE`, `INCONSISTENT-BOTH-TRUE`, `INCOMPLETE-PROFILE-COVERAGE` and `UNRESOLVED-REQUIRED-INPUT`.

`INCONSISTENT-BOTH-TRUE` and `INCOMPLETE-PROFILE-COVERAGE` invalidate the evaluated profile evidence. Other phase failures invalidate the attempt evidence. Every completed attempt still produces exactly one immutable result. Only `equivalent` permits the next gate. An independently sufficient authenticated conflict remains `material-conflict` despite an unrelated unresolved input because the `MC=TRUE` row precedes unresolved handling. Invalid identity, digest, authorization or opening evidence never yields no result and never yields equivalence.

## 5. Exact privacy-validation records

The component privacy TSV schema is:

```text
component_order\tprofile_id\tcomponent_id\tcanonical_type_id\tauthoritative_source_id\tminimum_necessity_basis\tbinding_mode\tpublic_identifier_class\topening_disclosure_class\tcross_action_linkability\tcorrelation_test_id\tevidence_id\tevidence_sha256\tvalidation_result\tfailure_code
```

Closed domains are:

- `minimum_necessity_basis`: `PREDICATE-INPUT`, `AUTHORIZATION-BINDING`, `ORDERING-COORDINATE` or `DEPENDENCY-COORDINATE`;
- `binding_mode`: `CANONICAL-VALUE` or `BLINDED-SHA256`;
- `public_identifier_class`: `NONE` or `ACTION-BOUNDED`;
- `opening_disclosure_class`: `NONE` or `AUTHENTICATED-CONFIDENTIAL-COMPARISON-ONLY`;
- `cross_action_linkability`: `PROHIBITED`;
- `validation_result`: `PASS` or `FAIL`;
- `failure_code`: `NONE`, `UNNECESSARY-COMPONENT`, `PUBLIC-PRIVATE-VALUE`, `REUSABLE-IDENTIFIER`, `OPENING-DISCLOSURE`, `CORRELATION-FAILURE`, `MISSING-EVIDENCE` or `INVALID-EVIDENCE`.

Rows are ordered by component order. PASS is mechanically permitted only when the component occurs in a typed expression or coordinate set, its disclosure classes meet the table, and its evidence object has the declared digest and is issued by the successor profile-validation authority identified in the source. A constructor is not a validation authority merely by constructing the row.

The one composition privacy record uses this exact field order:

```text
composition_privacy_record_id
profile_id
profile_sha256
authorization_schema_sha256
component_privacy_tsv_sha256
component_count
public_output_set
public_identifier_set
commitment_scheme_id
commitment_context_binding
opening_boundary
uniqueness_test_id
cross_action_correlation_test_id
actor_reconstruction_test_id
evidence_authority_id
evidence_id
evidence_sha256
validation_result
failure_code
```

Each line is `field-name: SP value`. `public_output_set` and `public_identifier_set` are comma-separated ASCII-sorted identifiers or `NONE`. `commitment_scheme_id` is `PE-TSE-SHA256-COMMITMENT-V1`; `commitment_context_binding` is `COMPLETE-AUTHORIZATION-HEADER`; `opening_boundary` is `AUTHENTICATED-CONFIDENTIAL-COMPARISON-ONLY`. The three test IDs MUST resolve to successor-source-owned total tests. PASS requires all component rows PASS, exact counts and digests, no reusable public participant identifier, no cross-action link, no actor-reconstruction bridge and valid independent evidence. Otherwise the result is FAIL with the first component-order failure or, after all components, `COMPOSITION-CORRELATION-FAILURE`, `ACTOR-RECONSTRUCTION-RISK`, `MISSING-EVIDENCE` or `INVALID-EVIDENCE` in that order.

## 6. Finite Dep(D) universe

The node TSV schema is:

```text
node_order\tnode_id\tnode_class\towner_source_id\towner_anchor\tcanonical_type_id\tcanonical_digest\tsemantic_equality_definition_id
```

The closed `node_class` domain is `EVALUATION-INPUT`, `RULE-SET`, `EVALUATION-CONTEXT`, `ACTION`, `AUTHORITATIVE-STATE`, `ORDERING-COORDINATE`, `DEPENDENCY-COORDINATE`, `DEFINITION` and `DETERMINATION`. The universe contains exactly every authoritative object read by the completed Evaluation that produced D, every definition transitively called by such a read and D itself. No runtime, database, application, diagnostic or observability object is admitted.

The edge TSV schema is:

```text
edge_order\tfrom_node_id\tto_node_id\tdependency_class\towner_source_id\towner_anchor\tproduction_field
```

The closed `dependency_class` domain is `VALUE`, `VALIDITY`, `AUTHENTICATION`, `ORDERING`, `APPLICABILITY`, `DEFINITION` and `COMPOSITION`. Every edge is extracted from one literal ID-bearing field in an authoritative Evaluation production record; `production_field` is that field's source anchor. The owner is the normative source that defines that field. An edge `A -> B` means B can affect the authoritative value, validity, authentication, ordering, applicability, definition or composition of A.

Construction enumerates nodes in first appearance order in the production record, enumerates each node's edges in dependency-class order followed by target ID byte order, rejects unresolved targets, then computes the least transitive closure from D. Strongly connected components are invalid except a component whose every internal edge has class `COMPOSITION` and whose members share one declared identity group. Such a group is contracted to its ASCII-lowest node ID for closure calculation; all original nodes remain serialized.

Two dependency nodes are semantically unchanged only when identity, canonical type, authenticated authority, validity, canonical digest and the result of the declared total semantic-equality definition all match. Digest equality alone is insufficient. Unchanged-D sufficiency is TRUE only when every node in the validated closure is present, authoritative, valid, authenticated and semantically unchanged. It is FALSE when any is changed or invalid and UNRESOLVED when any required evidence is unavailable.

## 7. Exact recovery function and rows

The recovery TSV schema is:

```text
row_order\tstage\tevent\tunchanged_d_sufficiency\tu_terminal_classification\tauthorization_disposition\trequired_evaluation\trequired_d\trequired_authorization\trequired_u\texecution_permission\tcommitment_permission
```

The exact rows are:

| Order | Stage | Event | D sufficiency | U classification | Authorization | Evaluation | D | Authorization required | U required | Execute | Commit |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0001 | PRE-EXECUTION | equivalent | NOT-APPLICABLE | ACTIVE | PRESERVE | SAME | SAME | SAME | SAME | PERMIT | PROHIBIT |
| 0002 | PRE-EXECUTION | material-conflict | TRUE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0003 | PRE-EXECUTION | material-conflict | FALSE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0004 | PRE-EXECUTION | material-conflict | UNRESOLVED | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0005 | PRE-EXECUTION | indeterminate | TRUE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0006 | PRE-EXECUTION | indeterminate | FALSE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0007 | PRE-EXECUTION | indeterminate | UNRESOLVED | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0008 | EXECUTION | execution-failure | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0009 | EXECUTION | execution-failure | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0010 | EXECUTION | execution-failure | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0011 | PRE-COMMITMENT | equivalent | NOT-APPLICABLE | ACTIVE | PRESERVE | SAME | SAME | SAME | SAME | PROHIBIT | PERMIT |
| 0012 | PRE-COMMITMENT | material-conflict | ANY | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0013 | PRE-COMMITMENT | indeterminate | ANY | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0014 | PRE-COMMITMENT | revalidation-failure | ANY | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0015 | COMMITMENT | commitment-success | NOT-APPLICABLE | COMMITTED | CONSUMED | SAME | SAME | NONE | NONE | PROHIBIT | COMPLETE |

`ANY` expands during TSV serialization to three rows in order TRUE, FALSE, UNRESOLVED. The serialized table therefore has 19 data rows. `NEW-ON-SUCCESSFUL-COMPLETION` means a new Evaluation has a new identity and produces a new D only if it reaches the accepted Evaluation-completion boundary. Failure produces no new D, acceptance, authorization or U. No failed U can be repaired, resumed, reactivated or committed.

## 8. Exact successor-source construction

The 16 revised source slots remain exactly R18, R25, R26, R27, R30, R32, R33, R34, R35, R36, R37, R38, R39, R42, R43 and R47 from Engineering[248] section 13. The four new sources remain S69 through S72. The other 50 sources remain byte-preserved predecessor-derived sources.

The literal semantic blocks owned by successor sources are:

| Block | Exact content source | Owning sources |
|---|---|---|
| `SEM-LEXICAL` | this determination section 2 from the first ABNF fence through the final truth-table paragraph | S70 |
| `SEM-PROFILE` | section 3 excluding its heading | S70 |
| `SEM-COMPARISON` | section 4 excluding its heading | S18, S27, S33, S34, S36, S37, S72 |
| `SEM-PRIVACY` | section 5 excluding its heading | S30, S32, S42, S43, S47, S70, S71 |
| `SEM-DEPENDENCY` | section 6 excluding its heading | S25, S35, S38, S39, S70 |
| `SEM-RECOVERY` | section 7 excluding its heading | S18, S25, S26, S27, S34, S36, S47, S72 |
| `SEM-AUTHORITY` | section 1 paragraphs 1, 5 and 6 | S69, S70, S71, S72 |

Block extraction is byte-exact: omit the named Markdown heading line and its following blank line where stated; retain every subsequent byte through the LF immediately before the next same-or-higher-level heading. No paraphrase is permitted.

Each revised source is serialized by `REVISED-SOURCE-V2`:

1. Read the predecessor bytes bound by Engineering[248] section 13.
2. Verify the predecessor SHA-256 from that register.
3. Emit the Engineering[248] inventory H1 and its five fixed metadata fields.
4. Emit `## Successor Transition-State Equivalence Definitions`.
5. For each semantic block assigned to the slot above, in block-table order, emit the anchor `pe-{namespace-lower}-src-{slot-lower}-{block-lower}`, LF, the exact block bytes and one LF.
6. Emit `## Successor Atomic Requirements` and the mechanically assigned atomic requirement table from section 9.
7. Emit `## Predecessor-Derived Body` and then the predecessor body without its H1, inserting deterministic heading anchors immediately before every ATX heading.
8. Emit `Candidate status: unreviewed-unpublished-non-authoritative` and `End of source: {SOURCE-ID}` on separate final lines.

Heading anchors are `pe-{namespace-lower}-src-{slot-lower}-h-{heading-ordinal-ORD4}`. Requirement anchors are the lowercase atomic requirement ID. No predecessor prose is deleted or replaced; semantic supersession is explicit in the inserted successor blocks. Exactly one blank line separates blocks.

Each new source is serialized by `NEW-SOURCE-V2` using the common metadata template in section 12, then these exact block sequences:

| Source | Ordered blocks |
|---|---|
| S69 | `SEM-AUTHORITY`; mapping registry rows imported from Engineering[248] section 5; assigned atomic requirements; immutable empty-registry conclusion |
| S70 | `SEM-LEXICAL`; `SEM-PROFILE`; `SEM-PRIVACY`; `SEM-DEPENDENCY`; assigned atomic requirements; profile-validation conclusion |
| S71 | canonical authorization and commitment clauses imported from Engineering[248] sections 8 and 9; `SEM-PRIVACY`; assigned atomic requirements; evidence-limit conclusion |
| S72 | `SEM-COMPARISON`; `SEM-RECOVERY`; `SEM-AUTHORITY`; assigned atomic requirements; immutable-history and implementation-non-authority conclusion |

The four literal conclusions are respectively:

```text
The validated empty registry authorizes zero transitions. No missing mapping or profile may be inferred.
```

```text
An invalid or incomplete profile authorizes zero transitions. Profile validity supplies no authority outside its registered mapping.
```

```text
A digest establishes only the bounded computational claim defined by its encoded preimage and algorithm. It proves no unencoded identity or semantic claim.
```

```text
Every occurrence and result remains immutable. Protocol-semantic atomicity neither requires nor derives authority from an implementation transaction mechanism.
```

These algorithms reproduce complete normative sources because every non-requirement semantic definition is emitted from a byte-exact block, and every requirement is emitted separately.

## 9. Atomic requirement reconstruction

The Engineering[248] section 14 table is the immutable lexical input. Its four revised rows and 88 proposed new rows are not successor rows directly. `MODAL-ATOM-V2` transforms them mechanically.

The modal tokens are `MUST NOT`, `MUST` and `MAY`, matched longest-first as complete ASCII words outside code spans. For each input row:

1. Parse the normative cell as one sentence.
2. Locate modal tokens from left to right.
3. `first-subject` is the bytes from sentence start through the U+0020 immediately before the first modal, with leading and trailing spaces removed.
4. For modal `i>1`, its clause separator is the rightmost complete ASCII separator `, ` or ` and ` after modal `i-1` and before modal `i`. Absence of such a separator is invalid. The separator belongs to neither clause. The clause for modal `i` begins immediately after that separator. The preceding clause ends immediately before it. The first clause begins at sentence byte zero and the final clause ends before the terminal full stop.
5. If a non-first clause begins with a modal token, prepend `first-subject` and one U+0020. Otherwise its own bytes before its modal are its explicit subject. Remove one leading `and ` if present. Normalize each atom to one terminal full stop.
6. Coordinated objects following one modal remain one obligation because the single modal governs the complete closed object set.
7. One-modal rows retain the proposed ID. Multi-modal rows emit IDs `{PROPOSED-ID}-A01` through `{PROPOSED-ID}-A{NN}` in modal order; the unsuffixed proposed ID is not emitted.
8. Strength is exactly the matched modal. Applicability is `applicable`. A leading `When` or `For` clause is copied to `condition_text`; otherwise `condition_text` is `ALWAYS`. The condition remains part of the normative text.
9. Every atom inherits the source anchors and RF destination of its input row. Revised atoms inherit the predecessor requirement ID. New atoms use `NONE` as predecessor requirement ID.

The extended requirement-ID grammar is the Engineering[248] successor requirement grammar optionally followed by `-A` and `ord2`. Atom ordinals are contiguous from 01.

Mechanical counts are:

| Class | Input rows | Atomic rows |
|---|---:|---:|
| Revised predecessor requirements | 4 | 9 |
| Proposed new requirements | 88 | 107 |
| Unchanged G2 requirements | 745 | 745 |
| Successor total | 837 proposed basis rows | 861 exact atomic rows |

Across the 116 revised/new atoms, strengths are 93 `MUST`, 21 `MUST NOT` and 2 `MAY`. The successor inventory has 861 rows. It MUST NOT be forced to 837.

The complete multi-modal cardinality register is:

```text
{SUCCESSOR-NAMESPACE}-STALEAUTH-003 3
{SUCCESSOR-NAMESPACE}-STALEAUTH-004 4
{SUCCESSOR-NAMESPACE}-TSEID-001 2
{SUCCESSOR-NAMESPACE}-TSEPRIV-003 2
{SUCCESSOR-NAMESPACE}-TSEPRIV-005 2
{SUCCESSOR-NAMESPACE}-TSERESULT-003 2
{SUCCESSOR-NAMESPACE}-TSEREEVAL-001 2
{SUCCESSOR-NAMESPACE}-TMREG-003 2
{SUCCESSOR-NAMESPACE}-TMREG-005 2
{SUCCESSOR-NAMESPACE}-TSEPROF-006 2
{SUCCESSOR-NAMESPACE}-TSEPROF-008 2
{SUCCESSOR-NAMESPACE}-TSECMPID-003 2
{SUCCESSOR-NAMESPACE}-TSEAUTH-004 2
{SUCCESSOR-NAMESPACE}-TSEEXEC-003 2
{SUCCESSOR-NAMESPACE}-TSEFAIL-002 2
{SUCCESSOR-NAMESPACE}-TSERECOV-001 2
{SUCCESSOR-NAMESPACE}-TSEAPP-001 2
{SUCCESSOR-NAMESPACE}-TSERUNTIME-001 2
{SUCCESSOR-NAMESPACE}-TSERUNTIME-003 2
{SUCCESSOR-NAMESPACE}-TSERUNTIME-004 2
{SUCCESSOR-NAMESPACE}-TSEPRES-002 2
```

Every other input row has cardinality one. The register sums to 45 atoms from 21 rows; the remaining 71 rows contribute 71 atoms, yielding 116.

The successor inventory schema is:

```text
requirement_order\trequirement_id\trequirement_anchor\trf_family\tsf_family\tstrength\tapplicability\tcondition_text\tnormative_text\tsource_ids\ttreatment\tpredecessor_requirement_id\tmapping_id\tprofile_id
```

The 745 unchanged rows are copied in G2 order with successor source IDs and `unchanged-predecessor-derived`. The nine revised atoms replace their four predecessor rows at the first predecessor position, ordered by proposed-row order then atom order. The 107 new atoms follow in Engineering[248] table order then atom order. `mapping_id` and `profile_id` are `NOT-APPLICABLE` because M=0. Existing 16 SF and 50 RF assignments are inherited from each row's RF family; no new family is introduced.

## 10. Canonical B245 blocker register

No Engineering[245] digest is asserted. `B245-CANONICAL-V1` is derived only from verified available authority: Engineering[246] section 18 and Engineering[247] findings across nine review areas. It has these exact records:

| ID | Subject | Required closure |
|---|---|---|
| B01 | Mapping closure | Distinguish requirements, mappings, relations and occurrences; bind the closed registry and admission rules without inventing M. |
| B02 | Profile architecture | Define immutable separate profiles, complete fields, reference resolution and mapping-to-profile binding. |
| B03 | Comparison and authorization | Define total comparison, authorization binding, commitment opening and current-state verification. |
| B04 | Recovery, atomicity and failure | Define dependency closure, total recovery, terminality and semantic atomicity. |
| B05 | Source closure | Define exact 66-source treatment, revisions, additions, preservation and authority boundaries. |
| B06 | Requirements and traceability | Define exact requirements, families, sources, destinations and bidirectional trace closure. |
| B07 | Construction determinism | Define exact inventory, paths, identities, templates, serializers, manifests and parameter boundary. |
| B08 | Privacy and authority | Define blinding assumptions, evidence limits, component and composition privacy validation and non-correlation. |
| B09 | Lifecycle separation | Preserve G2 immutability, successor-only correction, separate review/publication acts and I164 non-adoption. |

The register serializer is the table above encoded as TSV with columns `blocker_id`, `subject`, `required_closure`, in B01 through B09 order. Its roots are the bound Engineering[246] artifact identified by Engineering[247] and the bound Engineering[247] report in section 1. Absence of Engineering[245] bytes cannot alter these records.

## 11. Canonical Markdown endpoint extraction and trace generation

`CANONICAL-MARKDOWN-ENDPOINTS-V2` consumes canonical Markdown bytes without semantic keyword filtering. It tokenizes from start to end into these block kinds: ATX heading; paragraph; list item including its indented continuation; table header; table delimiter; table data row; fenced block including opening and closing fence; displayed formula block; thematic break; remaining nonblank line. Blank lines delimit but do not create endpoints.

Endpoint IDs are `{ROOT-ID}-{KIND}-{ORD6}` where `KIND` is `HEAD`, `PARA`, `LIST`, `THEAD`, `TDELIM`, `TROW`, `FENCE`, `FORMULA`, `BREAK` or `LINE`; ordinals are contiguous globally in byte order. The endpoint digest is SHA-256 of the exact block bytes including its terminal LF. Table rows are also parsed into cell endpoints `{ROW-ID}-CELL-{ORD3}` using unescaped pipe boundaries; leading and trailing presentation pipes do not create empty cells. Fenced content is never reparsed. No sentence splitting, capitalization test, abbreviation rule or normative keyword test exists. Therefore punctuation, lowercase starts, formulas, tables, fenced text and non-keyword authority statements cannot be lost or merged.

The trace root set is E243, E244, B245-CANONICAL-V1, E246, D247, E248, D249 and this determination E250. D247 uses only the corrected digest in section 1. D249 uses the Engineering[249] digest in section 1.

Trace rows use:

```text
trace_order\tfrom_endpoint\tto_endpoint\trelation\tinverse_trace_order\troot_id\troot_sha256\tcoverage_status
```

Closed relations are `preserved-by`, `corrected-by`, `defined-by`, `serialized-by`, `assigned-to`, `composed-into`, `excluded-by` and their exact inverses. Generation is mechanical:

1. Every extracted root endpoint receives one `preserved-by` row to the E250 section endpoint that imports it, or one `corrected-by` row to the E250 section that replaces it. The root-to-section assignment is the thirteen-row defect table in section 15; E243/E244/E246/B245 endpoints are assigned by B01 through B09 subject, and unmatched lifecycle/authority endpoints are assigned to section 16.
2. Every E250 semantic block receives `defined-by` rows to each owning source in section 8.
3. Every atomic requirement receives `assigned-to` rows to each source ID and its RF/SF destination from section 9.
4. Every source, registry row and requirement receives `composed-into` rows to the exact specification anchor produced by the section 12 composition algorithm.
5. Every prohibited authority or implementation-derived input receives `excluded-by` to section 1 or 16.
6. Emit the inverse of every row immediately after the forward row. The two rows cross-reference each other's final ORD8 trace order.
7. Sort forward relationships by root-set order, source endpoint byte order, relation order above and destination byte order before interleaving inverses.

Because every endpoint receives exactly one step-1 disposition and later rows are generated from closed registries, no semantic relationship is selected during construction. Coverage is complete only when every endpoint, semantic block, source, requirement, composition member and specification destination has the required forward and inverse rows.

## 12. Exact artifact serializers

The Engineering[248] section 16 inventory fixes the 40 paths, artifact identifiers, classifications and H1 values. This determination replaces its serializers with the following exact generators.

`MD-COMMON-V2` emits:

```text
<a id="{root-anchor}"></a>
{H1}

Identifier:
{artifact-id}

Document version:
V1

Successor generation:
{SUCCESSOR-GENERATION-ID}

Status:
unreviewed-unpublished-non-authoritative

{body}
```

`root-anchor` is the lowercase artifact ID. The one terminal LF shown is mandatory. `body` is one of the following exact ordered compositions:

| Serializer | Body composition |
|---|---|
| `MD-STATUS-V2` | H2 sections `Candidate State`, `Exact Inventory`, `Validation State`, `Review State`, `Publication State`, `Authority`, `Conclusion`; literal counts 40, 36 normative, four evidence-only, M=0, 70 sources and 861 requirements. |
| `MD-DECLARATION-V2` | Engineering[248] declaration clauses, with exact G2 identifiers and digests, followed by section 16 boundary clauses. |
| `MD-DIFFERENCE-V2` | Sections 2 through 11 of this determination, byte-exact and in order. |
| `MD-IDENTITY-V2` | the four later-authorized parameters, their grammar checks, G2 predecessor binding and candidate-only status. |
| `MD-PREREQUISITES-V2` | literal required independent candidate review, specification review, lifecycle separation, digest validation and fail-closed clauses from Engineering[248], with 861 substituted for 837. |
| `REVISED-SOURCE-V2` | section 8 algorithm. |
| `NEW-SOURCE-V2` | section 8 algorithm. |
| `MD-CLOSED-SET-V2` | literal counts: 70 sources, zero mappings, zero profiles, 861 requirements, 40 artifacts, 36 normative, four evidence-only. |
| `MD-SPEC-IDENTITY-V2` | identifier `PE-PROTOCOL-SPECIFICATION-{SUCCESSOR-GENERATION-LABEL}`, version parameter, governing generation, literal digest state `DIGEST-COMPUTED-AFTER-NORMATIVE-COMPOSITION-BEFORE-PACKAGE-MANIFEST`, source count 70 and requirement count 861. |
| `MD-SPECIFICATION-V2` | 16 SF sections in G2 order; 50 RF sections in G2 order; requirements in section 9 inventory order; each emits anchor, identifier, strength, applicability, condition, normative text and ordered source bindings. No other prose. |

All H2 labels named in a composition are emitted literally as `## {label}`. Imported clauses are byte-exact endpoints, not paraphrases.

TSV uses UTF-8/NFC, TAB delimiters, LF rows, no quoting, no TAB/LF inside cells, uppercase `NOT-APPLICABLE`, one header and no terminal count row unless specified. Ordinals are zero-padded and contiguous.

The exact TSV artifacts are:

| Artifact | Schema and generator |
|---|---|
| Registry | Engineering[248] section 5 header; zero data rows for M=0. |
| Source closed set | Engineering[248] section 17.2 schema; exactly 70 rows S03-S72 plus terminal `end` row; revised/new digests are computed, preserved digests equal predecessor digests. |
| Requirements | section 9 schema; exactly 861 data rows. |
| Classification | `classification_order`, `successor_requirement_id`, `predecessor_requirement_id`, `classification`, `reason`; 861 rows; reason is exactly `BYTE-PRESERVED`, `MODAL-ATOMIZED-REVISION` or `MODAL-ATOMIZED-ADDITION`. |
| Sections | root, 16 SF and 50 RF rows only; no undefined additional subsection rows; ranges and counts derive from the requirement inventory. |
| Composition | one row per source-to-specification, requirement-to-source and requirement-to-specification relationship; relation domain exactly `SOURCE-DEFINES-SPECIFICATION`, `REQUIREMENT-OWNED-BY-SOURCE`, `REQUIREMENT-COMPOSED-INTO-SPECIFICATION`; sort in that relation order then IDs. |
| Trace | section 11 schema and algorithm. |

The source manifest has header `manifest_order source_slot source_id path sha256 bytes lf_count treatment` separated by TAB, 70 source rows, then `0071`, `END`, the manifest ID, `NOT-APPLICABLE` in path and digest cells, `70` in bytes, `NOT-APPLICABLE` in LF and `COUNT` in treatment.

The semantic manifest has header `manifest_order semantic_class semantic_id path sha256 row_count status` and exactly five rows in this order: registry, requirement inventory, section inventory, composition map, specification. Status is `closed-validated-normative-member`.

The package manifest has header `artifact_order artifact_id classification path sha256 bytes lf_count dependency_ids` and exactly 40 rows in Engineering[248] order. Dependency IDs are sorted by artifact order and comma-separated, or `NONE`. Order 0040 has literal `SELF` in sha256, bytes and lf_count only. `SELF` is forbidden elsewhere and has no digest meaning.

## 13. Digest graph

The graph is generated from literal content references. An edge A -> B means A embeds B's digest and B MUST be complete first. The closed order is:

1. preserved predecessors and immutable review inputs;
2. types, definitions, privacy schemas, dependency schemas, recovery rows and atomic requirements;
3. revised and new sources;
4. source closed set and source manifest;
5. registry, requirement inventory, classification and section inventory;
6. composition map and semantic manifest;
7. specification candidate;
8. specification identity using the fixed candidate-digest-state literal, not its own digest;
9. declarations, prerequisites, difference, closed-set and status artifacts;
10. traceability;
11. package manifest with its sole SELF cells.

Every manifest dependency list is the transitive reduction of this order restricted to direct embedded-digest references, sorted by artifact order. A constructor MUST reject a missing edge, forward digest reference, self-reference outside the package-manifest SELF cells, duplicate edge or digest mismatch.

## 14. Installation and deterministic recovery

The destination evidence record has exact fields: destination path; prior-state class; expected 40-path ordered list; per-path SHA-256 or `ABSENT`; complete-set digest; evidence source; evidence SHA-256; validation result. The admitted states are:

- `ABSENT`: none of the 40 paths exists;
- `IDENTICAL-COMPLETE`: all 40 exist and every digest matches the candidate;
- `DIFFERENT-COMPLETE`: all 40 exist, form a previously validated complete set, and at least one digest differs;
- `PARTIAL-INVALID`: every other state.

`ABSENT` permits one atomic installation attempt. `IDENTICAL-COMPLETE` is idempotent success. `DIFFERENT-COMPLETE` prohibits replacement without a separately authorized successor operation. `PARTIAL-INVALID` prohibits continuation and selective repair.

Before an installation attempt, the constructor writes outside the destination an immutable attempt record containing prior-state evidence, the ordered 40 candidate paths, all candidate digests and prior bytes for every existing target. Each successful path creation is appended to the record. On interruption, recovery verifies the record digest. If the prior state was ABSENT, recovery removes only paths recorded as newly created whose current digest equals the recorded candidate digest. If the prior state was a validated complete set, recovery restores each changed path from its recorded prior bytes after verifying the recorded prior digest. Any mismatch blocks recovery. After recovery, the destination is reclassified from bytes; retry is permitted only from ABSENT or IDENTICAL-COMPLETE.

These are construction controls, not protocol transaction semantics.

## 15. Engineering[249] defect closure

| Defect | Exact closure |
|---:|---|
| 1 | Sections 2 and 3 define the complete typed expression language, primitive roots, sets, conditions, functions, truth tables, failures, stages, arities, termination and ownership. |
| 2 | Section 4 gives one first-match exhaustive comparison table, including both-true and invalid identity/digest cases. |
| 3 | Section 5 gives exact component and composition schemas, evidence authority and deterministic PASS/FAIL. |
| 4 | Section 6 gives the finite node/edge universe, extraction, classes, ownership, cycles, equality and closure. |
| 5 | Section 7 gives exact serialized rows, terminal classifications, unchanged-D sufficiency and new-authorization boundaries. |
| 6 | Section 8 provides mechanically exact complete serializers for all 16 revised and four new sources, including non-requirement definitions. |
| 7 | Section 9 atomizes modal obligations, corrects strengths and applicability and recomputes the exact total as 861. |
| 8 | Sections 1 and 11 bind the actual D247 digest and prohibit the superseded digest. |
| 9 | Section 10 defines B245-CANONICAL-V1 from verified available authority without inventing an Engineering[245] digest. |
| 10 | Section 11 replaces keyword/sentence extraction with lossless canonical-Markdown block endpoints. |
| 11 | Section 11 supplies closed relationship rules, literal assignments and exact inverse generation. |
| 12 | Section 12 supplies literal parameterized Markdown templates and exact TSV/manifest generators. |
| 13 | Sections 13 and 14 close all digest dependencies and all four destination/recovery states. |

No Engineering[249] defect remains. The exact construction basis leaves only the four explicitly later-authorized successor identity parameters unresolved.

## 16. Preserved authority and lifecycle boundary

Published Generation 2 remains complete, immutable and unchanged:

- generation: `PE-PROTOCOL-GENERATION-002`;
- published identity: `PE-PUBLISHED-PROTOCOL-G2-001`;
- specification: `PE-PROTOCOL-SPECIFICATION-G2` version `2.0.0`;
- Protocol Publication: `PE-PROTOCOL-PUBLICATION-G2-001`;
- succession: `PE-PROTOCOL-SUCCESSION-G2-G1-001` with `succession(G2, G1)`;
- Protocol Specification Publication: `PE-PROTOCOL-SPECIFICATION-PUBLICATION-G2-001`.

Privacy Engine remains the implementation-independent protocol. I164 remains one bounded Speak-up-appV3 implementation. Speak Up remains one application adapter and use case. I164 does not define, own, narrow, repair, replace or become the protocol.

I164 adoption remains `not-performed`. Implementation readiness remains `blocked-pending-published-successor-correction`. Candidate acceptance, specification acceptance, Protocol Publication, succession, Protocol Specification Publication and implementation adoption remain separate acts.

## 17. Materialization and Git boundary

This determination selects no successor identity, constructs no candidate or specification, performs no publication or succession and adopts nothing into I164.

Construction of this determination's exact bytes outside the repository does not authorize repository materialization. Repository materialization requires Steve's separate exact-payload authorization binding the path, SHA-256 and byte count. Materialization does not authorize staging, commit, tags, push or package regeneration. Each requires a later explicit gate.

## 18. Terminal determination

The selected result is:

```text
transition-state-equivalence-mapping-and-profile-semantic-completion-and-exact-construction-basis-second-correction-and-completion-resolved
```

Generation 2 remains complete and unchanged. M remains zero. The second correction supplies semantic closure and deterministic exact construction for the later successor-identity gate without performing that gate.
