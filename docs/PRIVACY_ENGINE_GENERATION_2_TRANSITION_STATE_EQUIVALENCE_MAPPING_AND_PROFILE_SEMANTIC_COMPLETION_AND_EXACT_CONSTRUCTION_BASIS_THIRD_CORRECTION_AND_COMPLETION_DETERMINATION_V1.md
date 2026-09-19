# Privacy Engine Generation 2 Transition-State Equivalence Mapping and Profile Semantic Completion and Exact Construction-Basis Third Correction and Completion Determination V1

Identifier:
PE-TRANSITION-STATE-EQUIVALENCE-MAPPING-AND-PROFILE-SEMANTIC-COMPLETION-AND-EXACT-CONSTRUCTION-BASIS-THIRD-CORRECTION-AND-COMPLETION-DETERMINATION-V1

Document version:
V1

Result:
transition-state-equivalence-mapping-and-profile-semantic-completion-and-exact-construction-basis-third-correction-and-completion-resolved

Payload status:
proposed-exact-payload-awaiting-materialization-authorization

Authority classification:
development-authority-determination-non-protocol-non-publication

## 1. Status, scope, precedence and immutable inputs

This determination is a bounded correction of Engineering[250] in response to the complete Engineering[251] read-only independent review. It neither amends nor reinterprets published Generation 2. It supplies development authority only for a distinct future successor construction.

Read-only intake passed by content identity: formal corpus `f0e8b9e209ce3c90e5557f1ba518b5fa47461a2b4bf6f6fd951a08b08da4835a`, 1,742,255 bytes, 177 regular files and ZIP comment `f4571a8547d9552455b35f3f363840ba5113f0ef`; I164 baseline `7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847`, 3,659,875 bytes and ZIP comment `003e984ea73a2dede092443893dfbc9e74121e14`; provenance `4bcf30fd689c809aae7b6d5dacb318857512745b6239a0ac07c9392d86c8f770`, 97,879 bytes, 66 Engineering records, 19 generic-tag bindings and 104 changed-file identities; pack `7d9b24ea0f34220b74f8f8794c735e49ccf69d8e9d9609938cc9d1dec758fa9a`, 109,932 bytes and internal checksum `a0838725044d3b6c49740f76e2026a6b678266a2`. Both ZIP integrity tests and all 66 supplied raw-commit identity reconstructions passed. This is supplied-archive verification, not a live remote/worktree claim.

The immutable inputs are:

| Input | SHA-256 | Bytes | LF |
|---|---|---:|---:|
| Engineering[248] determination | `1f5b59b0ff4720ee142a42017f13e543e1a3973fd81113ca86ca2ead43834a73` | 93575 | 721 |
| Engineering[247] report | `35f2ce9bb84aaec7e3d5dfecb341d3d04cadb65060d89028a4e70a08e731bcc5` | 21318 | 228 |
| Engineering[249] report | `636899f5426b8a70065b7f7193bba8ef1d0542e10c2ecc014a90cea39990bb37` | 19543 | 331 |
| Engineering[250] determination | `558747f7091ab5e5f597a3f3fba3acb987ea28dfd652e7e691e81371d2b5ccf2` | 43973 | 581 |
| Engineering[251] report | `ae67f309c7d13a656d0e5d66a89ad016eb64910a464897def54116e02cef940b` | 15499 | 282 |
| Published G2 specification | `ffeaed785a34e8535d489ad6946dbdae3a55b441a0c94c8c05791eb33fd423e1` | 359620 | 4131 |

Engineering[248] remains the source of the 66-source register, the four revised and 88 new lexical requirement inputs, and the 40-artifact inventory. Engineering[250] remains the source of the total comparison table and every rule not replaced here. This determination replaces Engineering[250] sections 2, 5 through 14 and their dependent claims. On any conflict this determination governs future-successor construction.

Exactly four later-authorized construction parameters remain:

1. `SUCCESSOR-GENERATION-ID`;
2. `SUCCESSOR-GENERATION-LABEL`;
3. `SUCCESSOR-NAMESPACE`;
4. `SUCCESSOR-VERSION`.

No other semantic value may be constructor-selected. `M = 0`. No mapping, profile, authority, predicate, evidence or recovery choice may be inferred from I164, Speak Up, another implementation, runtime evidence or observed behaviour.

## 2. Complete PE-TSE-EXPR-V1 type and definition system

<!-- BEGIN E252-SEM-TYPES -->
All text governed by this section is UTF-8 without BOM, Unicode NFC, LF-only, without trailing horizontal whitespace and with exactly one terminal LF. ASCII terminals are case-sensitive. Unsigned integers in text are canonical decimal: `0` or a non-zero digit followed by zero or more digits. Lowercase hexadecimal contains an even, non-zero number of characters from `0` through `9` and `a` through `f`.

The primitive type roots are exactly `PE-TSE-BOOL3`, `PE-TSE-BYTES`, `PE-TSE-ID` and `PE-TSE-UINT`. A derived type record has the exact TSV schema:

```text
type_order\ttype_id\tkind\telement_type_id\tfield_type_ids
```

`type_order` begins at `0001` and is contiguous. The four primitive roots occur first in the order shown. `kind` is `PRIMITIVE`, `SET` or `TUPLE`. A primitive row uses `NOT-APPLICABLE` in both final cells. A `SET` row names exactly one earlier type in `element_type_id` and uses `NOT-APPLICABLE` in `field_type_ids`. A `TUPLE` row uses `NOT-APPLICABLE` in `element_type_id` and names two or more earlier type IDs, comma-separated without spaces, in field order. Duplicate type IDs, forward references and cycles are invalid. There is no type whose literal identifier is `SET`.

Every typed value has one canonical octet encoding. `U32(n)` and `U64(n)` mean unsigned big-endian 32-bit and 64-bit encodings; overflow is invalid. `A(s)` means the ASCII bytes of `s`. `L32(x)` means `U32(len(x)) || x`; `L64(x)` means `U64(len(x)) || x`. The complete encoding is:

```text
A("TSEV1") || L32(A(type_id)) || kind_octet || L64(body)
```

The four primitive `kind_octet` values and bodies are:

| Type | Octet | Body |
|---|---|---|
| `PE-TSE-BOOL3` | `00` | `00` for FALSE, `01` for TRUE, `02` for UNRESOLVED |
| `PE-TSE-BYTES` | `01` | the represented octets, including the empty string when the owning component permits it |
| `PE-TSE-ID` | `02` | one nonempty ASCII identifier matching `[A-Za-z0-9][A-Za-z0-9._:#-]*`; its identity class applies its narrower grammar before encoding |
| `PE-TSE-UINT` | `03` | canonical decimal ASCII |

A derived `SET` uses `kind_octet = 10`. Its body is `U32(count)` followed by `L64(value)` for each distinct complete canonical element encoding, sorted by unsigned bytewise ascending order. A duplicate encoding is invalid. A derived `TUPLE` uses `kind_octet = 11`. Its body is `U32(field_count)` followed by `L64(value)` for each field in declared order. Each nested value must name the declared element or field type. These rules supply canonical bytes for every primitive and derived value.

The PE-TSE-EXPR-V1 grammar is the following complete ABNF; no Engineering[250] grammar is imported:

```text
expression = literal / argument / reference / tuple-expression / equal-expression / not-expression / and-expression / or-expression / member-expression / apply-expression / status-expression
literal = "literal(" type-id "," hex-bytes ")"
argument = "arg(" ord4 ")"
reference = "ref(" component-id "," side ")"
tuple-expression = "tuple(" expression "," expression *( "," expression ) ")"
equal-expression = "equal(" expression "," expression ")"
not-expression = "not(" expression ")"
and-expression = "and(" expression *( "," expression ) ")"
or-expression = "or(" expression *( "," expression ) ")"
member-expression = "member(" expression "," definition-id ")"
apply-expression = "apply(" definition-id *( "," expression ) ")"
status-expression = status-op "(" component-id "," side ")"
status-op = "authoritative" / "available" / "valid" / "authenticated"
side = "AUTHORIZED" / "CURRENT"
ord4 = 4DIGIT
hex-bytes = 2HEXDIG *( 2HEXDIG )
```

ASCII space is prohibited inside an expression. `and` and `or` have at least one argument. `tuple` has at least two. `arg(0001)` denotes the first declared input; `0000`, an ordinal above the definition arity, or `arg` in a zero-input definition is invalid. `apply` evaluates argument expressions left-to-right, binds their canonical values to the callee's `arg` ordinals, and evaluates the callee in a new environment. No caller argument is visible except through those bindings.

`PE-TSE-SET` is a reserved built-in definition identifier and is not a definition record. It may occur only as `apply(PE-TSE-SET,<literal>...)` in a `SET` definition. Its arity is the number of literal arguments, including zero. All literals must have the output set type's element type; the result is the canonical set encoding above. `PE-TSE-SET` is forbidden in `definition_id`, source ownership and every other position.

A literal is `literal(type-id,hex-bytes)`. `hex-bytes` decodes to one complete canonical typed-value encoding; its embedded `type_id` must equal the literal's `type-id`. A literal that is not canonical is invalid rather than normalized. `ref(component-id,side)` returns the component's authenticated represented value after its representation decoder, canonicalizer and normalizer have succeeded, as one complete canonical typed-value encoding of the component's `canonical_type_id`.

Definition records have the exact TSV schema:

```text
definition_order\tdefinition_id\tkind\tinput_type_ids\toutput_type_id\texpression\tsource_id\tsource_anchor
```

`definition_order` begins at `0001` and is contiguous. `kind` is `SET`, `CONDITION` or `FUNCTION`. `input_type_ids` is `NONE` or a comma-separated ordered list. A `SET` definition has `NONE` inputs, names an earlier derived type whose kind is `SET`, and has exactly one `apply(PE-TSE-SET,...)` expression. A `CONDITION` returns `PE-TSE-BOOL3`. A `FUNCTION` returns its declared type. Every definition names one owning successor source and anchor. Profile-local, implementation-owned and unresolved definitions are invalid. Admission builds one directed graph whose vertices are every definition plus every component's decoder, canonicalizer and normalizer stages. An edge goes from an expression owner to every definition named by `apply` or `member`; from each stage to its named definition; from decoder to canonicalizer; from canonicalizer to normalizer; and from every expression containing `ref` to the referenced component's normalizer. `PE-TSE-SET` adds no vertex. Kahn's algorithm, choosing the unsigned-UTF-8-lowest available vertex, must consume every vertex. Thus definition-to-component-to-normalizer-to-definition recursion is rejected. Definition-record order must also be a topological order.

Component records have the exact TSV schema:

```text
component_order\tcomponent_id\trepresented_type_id\trepresentation_decoder_definition_id\tcanonical_type_id\tcanonicalization_definition_id\tnormalization_definition_id\tauthority_source_id\tauthority_anchor\tavailability_condition_definition_id\tvalidity_condition_definition_id\tauthentication_definition_id\tprivacy_class\tobservability_class\tbinding_mode
```

`component_order` begins at `0001` and is contiguous. Every type and definition reference must resolve in the profile's closed type/definition tables. `privacy_class` is `PUBLIC`, `ACTION-BOUNDED` or `CONFIDENTIAL`. `observability_class` is `NONE`, `RESULT-ONLY` or `AUTHENTICATED-CONFIDENTIAL-COMPARISON-ONLY`. `binding_mode` is `CANONICAL-VALUE` or `BLINDED-SHA256`. The three condition/authentication definitions must return `PE-TSE-BOOL3`; decoder, canonicalizer and normalizer types must compose exactly from represented type to canonical type. `NONE` is forbidden in every component cell.

`apply` resolves either the reserved built-in above or one definition record, checks exact arity and input types, and evaluates it once in the bound argument environment. `member` requires a `SET` definition and compares complete canonical element encodings. `tuple` constructs the containing definition's declared tuple output and requires exact field count and types. The four status operators return `PE-TSE-BOOL3`. Failure, unavailable authority, failed authentication, invalid representation, noncanonical encoding, type failure or definition failure returns `NO-VALUE` for a non-Boolean result and `UNRESOLVED` for a Boolean result. `not`, `and` and `or` use Kleene strong three-valued truth tables. `equal` returns UNRESOLVED if either operand is NO-VALUE and otherwise compares complete canonical typed encodings. There are no other built-ins, references, substitutions, implicit conversions, collations, clocks, random sources or defaults.
<!-- END E252-SEM-TYPES -->

## 3. Exact privacy evidence, authority and validation

<!-- BEGIN E252-SEM-PRIVACY -->
An immutable profile appoints its privacy-validation authority without incorporating occurrence evidence. Its exact appointment record is:

```text
appointment_order\tauthority_id\talgorithm\tpublic_key\tkey_fingerprint_sha256\towner_source_id\towner_anchor
000001\t{authority-id}\tED25519-RFC8032\t{64-lowercase-hex}\t{64-lowercase-hex}\t{source-id}\t{source-anchor}
```

The fingerprint is SHA-256 of the raw 32 public-key octets. The source ID and anchor must be an authoritative successor source appointment. An evidence issuer must match every appointment cell. Possession of a signing key, construction access, runtime activity or successful self-signature never appoints an authority.

The profile also contains `privacy_surface_template.tsv` and `privacy_relation_template.tsv`. Their exact schemas are:

```text
surface_order\tsurface_id\trecord_class\tfield_name\texposure\taction_context_rule\tpermitted_reuse_class\tderived_from_surface_ids\tderivation_class\towner_source_id\towner_anchor
relation_order\tfrom_surface_id\tto_surface_id\trelation_class\tcondition_definition_id\towner_source_id\towner_anchor
```

`exposure` is `PUBLIC`, `CONFIDENTIAL` or `PRIVATE-ACTOR`; reuse is `NONE`, `GENERATION-CONSTANT` or `PROFILE-CONSTANT`; relation/derivation class is `ENCODES`, `DERIVES`, `EQUALS`, `AUTHENTICATES`, `REFERENCES` or `OBSERVABLY-JOINABLE`. `derived_from_surface_ids` is an ordered comma list or `NONE`; derivation class is `NOT-APPLICABLE` exactly with `NONE`. Surface rows are generated, not selected: emit one row for every field in the authorization header, component binding, comparison attempt, comparison result, recovery result and observability-output schemas, in that schema order, and then every component's represented value, canonical value, blind and opening in component order. Each owning schema must declare exactly one exposure, action-context rule, reuse class and derivation tuple for every field; an unlabeled or multiply labeled field invalidates the profile, and any other output schema is prohibited. Relation rows are generated from the declared derivation tuple, every expression-AST reference, equality/authentication operator and explicitly declared observability join, sorted by origin surface order then target surface order then class. The validator independently regenerates both tables and requires byte equality. This equality, rather than an issuer assertion, establishes the finite observable-relation universe. The profile digest covers the templates and appointment, but no evidence digest; evidence may therefore bind the already final profile digest without a cycle.

One evidence object contains `evidence.tsv`, `tokens.tsv`, `links.tsv` and `signature.txt`. `evidence.tsv` has exactly one row under this header:

```text
evidence_id\tevidence_kind\tprofile_id\tprofile_sha256\tscope_id\tcomponent_id\tsurface_template_sha256\trelation_template_sha256\ttokens_sha256\tlinks_sha256\tcorrelation_result\tuniqueness_result\tactor_reconstruction_result\tissued_by\talgorithm
```

`evidence_kind` is `COMPONENT` or `COMPOSITION`; `component_id` is the component ID or `NOT-APPLICABLE`. `tokens.tsv` has header `token_order surface_id action_context_id token_id token_sha256 exposure permitted_reuse_class`. It has exactly one instantiated row for each template surface occurrence in scope. `links.tsv` has header `link_order from_token_id to_token_id relation_order relation_class`. It has exactly one instantiated row for each applicable template relation and every runtime equality of token digests. Rows are sorted by complete row bytes excluding ordinal, then numbered from `000001`. A missing, extra or duplicate row is `INCOMPLETE-EVIDENCE-UNIVERSE`.

The signed payload is ASCII `PE-TSE-PRIVACY-EVIDENCE-V1`, LF, then exact `evidence.tsv`, `tokens.tsv` and `links.tsv` bytes. `signature.txt` is `authority_id`, one ASCII space, 128 lowercase signature hex characters and LF. Verify Ed25519 per RFC 8032 over the payload bytes themselves, not a reserialization or pre-hash variant.

The total uniqueness test returns FAIL iff two PUBLIC token rows in different action contexts have equal `token_sha256` and do not share the same permitted non-`NONE` constant class. The total correlation test constructs an undirected graph using all link rows plus equal-digest edges and returns FAIL iff a path joins PUBLIC tokens in distinct action contexts and at least one edge on every such path is not an allowed equal constant edge. The actor-reconstruction test does not insert any node. It uses the generated graph containing the instantiated `PRIVATE-ACTOR` surfaces and returns FAIL iff any PUBLIC token is connected to any PRIVATE-ACTOR token. With no such path it returns PASS; mere existence of a private-actor surface is not failure.

Component evidence filters the regenerated universe to one component plus all transitively related surfaces; composition evidence uses the entire universe. The component privacy TSV schema is exactly:

```text
component_order\tprofile_id\tcomponent_id\tcanonical_type_id\tauthoritative_source_id\tminimum_necessity_basis\tbinding_mode\tpublic_identifier_class\topening_disclosure_class\tcross_action_linkability\tcorrelation_test_id\tevidence_id\tevidence_sha256\tvalidation_result\tfailure_code
```

`minimum_necessity_basis` is `PREDICATE-INPUT`, `AUTHORIZATION-BINDING`, `ORDERING-COORDINATE` or `DEPENDENCY-COORDINATE`; public identifier is `NONE` or `ACTION-BOUNDED`; opening disclosure is `NONE` or `AUTHENTICATED-CONFIDENTIAL-COMPARISON-ONLY`; linkability is `PROHIBITED`; result is PASS or FAIL. The composition privacy record is one canonical Markdown field record with these fields in this order:

```text
composition_privacy_record_id
profile_id
profile_sha256
authorization_schema_sha256
component_privacy_tsv_sha256
component_count
surface_template_sha256
relation_template_sha256
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

Each line is `field-name`, colon, SP, value, LF. Both records use this one closed first-failure domain:

```text
NONE
UNNECESSARY-COMPONENT
PUBLIC-PRIVATE-VALUE
REUSABLE-IDENTIFIER
OPENING-DISCLOSURE
CORRELATION-FAILURE
UNIQUENESS-FAILURE
ACTOR-RECONSTRUCTION-RISK
MISSING-EVIDENCE
INCOMPLETE-EVIDENCE-UNIVERSE
INVALID-EVIDENCE-DIGEST
INVALID-EVIDENCE-AUTHORITY
INVALID-EVIDENCE-AUTHENTICATION
PROFILE-DIGEST-MISMATCH
COMPONENT-COUNT-MISMATCH
COMPONENT-FAILURE
```

`NONE` is the only PASS code. Validation order is: profile digest; appointment and key fingerprint; signature; template digests; regenerated-universe equality; component count; confidentiality/opening rules; uniqueness; correlation; actor reconstruction. The first failure selects the corresponding code in the closed list. Composition PASS requires every component PASS and all three total tests PASS. Every test has finite generated inputs and a Boolean result; no descriptive completeness claim or implementation-selected relation is accepted.
<!-- END E252-SEM-PRIVACY -->

## 4. Evaluation production and occurrence-specific Dep(D)

<!-- BEGIN E252-SEM-DEPENDENCY -->
An immutable profile contains only an admitted-operation register and identity-group templates. It never contains occurrence nodes, edges or Dep(D). An Evaluation that successfully produces D also produces one immutable execution transcript, identity-group instance table, node table and edge table. The five objects become authoritative atomically at Evaluation completion. A failed Evaluation produces none of them and no D.

The profile's finite read-field register and admitted-operation register have these exact TSV schemas:

```text
field_order\tfield_id\tfield_class\tcanonical_type_id\tsemantic_equality_definition_id\tauthority_source_id\tauthority_anchor
operation_order\toperation_id\toperation_kind\texpression_owner_id\tpermitted_read_field_ids\towner_source_id\towner_anchor
```

`field_class` is `ACTION`, `RULE-SET`, `EVALUATION-CONTEXT`, `AUTHORITATIVE-STATE`, `ORDERING-COORDINATE`, `DEPENDENCY-COORDINATE` or `COMPONENT`; the register contains the four singular fields followed by every coordinate and component/side field in profile order. Every semantic-equality definition is total and Boolean. `operation_kind` is `EVALUATION-ROOT`, `DEFINITION` or `COMPONENT-STAGE`. The root is first; definitions then follow definition order; component decoder, canonicalizer and normalizer stages follow component order. `permitted_read_field_ids` is an ASCII-comma list or `NONE`. It is generated from the expression AST: each `ref` supplies its component/side field; each `apply` supplies its callee operation; each status operator supplies its component/side status field; `arg` supplies no external field. Byte equality with independent register and AST regeneration is required.

The occurrence transcript schema is:

```text
event_order\tevaluation_id\tdetermination_id\tevent_kind\toperation_id\tparent_event_order\tfield_id\tobject_id\tcanonical_type_id\tcanonical_sha256\tauthority_source_id\tauthority_anchor\tauthentication_evidence_id\tresult
```

`event_kind` is `ENTER`, `READ`, `CALL`, `RETURN` or `DETERMINATION`. `event_order` starts `000001` and is contiguous. Root ENTER has parent `000000`. Before an operation retrieves or tests an external value it emits READ; before evaluating a callee it emits CALL and the callee immediately emits ENTER; RETURN closes the most recent unclosed ENTER; the final event is DETERMINATION. A branch not evaluated emits no READ or CALL. Short-circuit order is left-to-right: `and` stops at FALSE, `or` stops at TRUE, and the comparison procedure evaluates only witnesses required by its stated precedence. Every field ID must be in that operation's regenerated permitted-read list. Stack replay must accept the transcript, every READ object must validate its authority, digest, authentication and type, and the transcript result must reproduce D under PE-TSE-EXPR-V1. An extra read, missing read, unlogged call or result mismatch invalidates the Evaluation evidence.

The exact field-to-edge register is:

| Event | Edge from | Edge to | Class |
|---|---|---|---|
| root ENTER | D | root operation instance | DEFINITION |
| READ | current operation instance | read object | VALUE |
| READ authentication evidence | read object | authentication evidence object | AUTHENTICATION |
| READ authority source | read object | authority source endpoint | AUTHORITY |
| CALL | current operation instance | callee operation instance | DEFINITION |
| DETERMINATION | D | transcript object | PRODUCTION |

Rows are emitted in transcript order and, for READ, in class order VALUE, AUTHENTICATION, AUTHORITY, skipping only an authentication evidence field equal to `NOT-APPLICABLE`, which is permitted solely for a profile-declared public constant. No other edge is permitted. This preserves actual-read semantics: an admitted but unevaluated component or definition creates no occurrence edge and is absent from Dep(D).

The identity-group template and instance schemas are:

```text
group_template_order\tgroup_template_id\tmember_field_ids\tidentity_rule_definition_id\towner_source_id\towner_anchor
group_order\tidentity_group_id\tgroup_template_id\tmember_object_ids\tidentity_rule_result
```

Members are comma-separated in template order, groups do not overlap, and a group has at least two members. `identity_rule_result` must be TRUE after evaluating the named total definition over the member canonical values; FALSE or UNRESOLVED invalidates the transcript. An instance ID is `{evaluation_id}-IG-{group_order}`. Grouping records aliases of one semantic object; it does not permit graph cycles or invent dependencies. Node construction collapses group members to the unsigned-UTF-8-lowest object ID and records every alias in the node's `alias_object_ids` cell.

The node schema is `node_order node_id alias_object_ids node_class canonical_type_id canonical_sha256 authority_source_id authority_anchor semantic_equality_definition_id`. Emit D, the transcript object, every executed operation instance, then every distinct READ object and its evidence/source endpoint, in first-event order, collapsing groups as above. The D, transcript, operation and evidence/source nodes use the closed sentinel `BYTE-IDENTITY`; READ nodes copy the field register's definition. `BYTE-IDENTITY` means exact equality of the already validated canonical digest and is not a definition reference. The edge schema is `edge_order from_node_id to_node_id dependency_class transcript_event_order production_field`. Generate it only from the field-to-edge register, substitute collapsed node IDs, remove exact duplicate rows after first occurrence, and renumber from `000001`. Self-edges and any directed cycle are invalid.

Dep(D) is the least transitive closure from D over these occurrence edges. A node is semantically unchanged only when identity, canonical type, authority, validity, authentication and canonical digest match and its declared semantic-equality definition returns TRUE. Unchanged-D sufficiency is TRUE exactly when every closure node is semantically unchanged; FALSE when an authoritative difference or invalidity is proved; otherwise UNRESOLVED. This preserves the prior unchangedness test while limiting the universe to actual reads. Profile registers/templates are immutable generation members. Transcript, groups, nodes, edges and Dep(D) are occurrence evidence owned by E and D and are never profile members.
<!-- END E252-SEM-DEPENDENCY -->

## 5. Corrected total recovery table

<!-- BEGIN E252-SEM-RECOVERY -->
The recovery TSV uses the Engineering[250] section 7 header. It has exactly 21 data rows. There is no `ANY` token in serialized output.

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
| 0012 | PRE-COMMITMENT | material-conflict | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0013 | PRE-COMMITMENT | material-conflict | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0014 | PRE-COMMITMENT | material-conflict | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0015 | PRE-COMMITMENT | indeterminate | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0016 | PRE-COMMITMENT | indeterminate | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0017 | PRE-COMMITMENT | indeterminate | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0018 | PRE-COMMITMENT | revalidation-failure | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0019 | PRE-COMMITMENT | revalidation-failure | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0020 | PRE-COMMITMENT | revalidation-failure | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0021 | COMMITMENT | commitment-success | NOT-APPLICABLE | COMMITTED | CONSUMED | SAME | SAME | NONE | NONE | PROHIBIT | COMPLETE |

The lookup key is the exact triple `(stage,event,unchanged_d_sufficiency)`. For `equivalent` and `commitment-success`, sufficiency must be `NOT-APPLICABLE`; for every other event it must be TRUE, FALSE or UNRESOLVED. Exactly one row therefore matches every admitted event. Unmatched or multiply matched input is invalid and yields no permission. `NEW-ON-SUCCESSFUL-COMPLETION` retains the Engineering[250] meaning. No failed U may be repaired, resumed, reactivated or committed.
<!-- END E252-SEM-RECOVERY -->

## 6. Literal successor-source construction

<!-- BEGIN E252-SEM-SOURCES -->
The 16 revised slots are S18, S25, S26, S27, S30, S32, S33, S34, S35, S36, S37, S38, S39, S42, S43 and S47. The four new slots are S69 through S72. The remaining 50 S03-through-S68 sources are byte-preserved. Predecessor paths, digests, H1 values and successor paths are exactly the Engineering[248] sections 13 and 16 register cells; no filename or title is inferred.

The source template language has only three controls: `{{NAME}}` substitutes the named ASCII parameter; `{{BLOCK:ID}}` substitutes the bytes strictly between `<!-- BEGIN ID --> LF` and `<!-- END ID --> LF` in this determination; `{{ROWS:SOURCE-SLOT}}` emits requirement rows by the exact section 7 rule. Control lines are not emitted. A missing or duplicate marker, parameter or source slot is fatal.

Every revised source is the following literal template:

```text
<a id="{{ROOT-ANCHOR}}"></a>
{{H1}}

Identifier:
{{SUCCESSOR-NAMESPACE}}-SOURCE-{{SOURCE-SLOT}}

Document version:
V1

Successor generation:
{{SUCCESSOR-GENERATION-ID}}

Predecessor source identifier:
PE-G2-SOURCE-{{SOURCE-SLOT}}

Predecessor source SHA-256:
{{PREDECESSOR-SHA256}}

Status:
unreviewed-unpublished-non-authoritative

## Successor Transition-State Equivalence Definitions

{{SOURCE-BLOCK-SEQUENCE}}
## Successor Atomic Requirements

| Requirement | Strength | Applicability | Condition | Normative text | RF | SF |
|---|---|---|---|---|---|---|
{{ROWS:SOURCE-SLOT}}

## Predecessor-Derived Body

{{CANONICAL-PREDECESSOR-BODY}}

Candidate status: unreviewed-unpublished-non-authoritative
End of source: {{SUCCESSOR-NAMESPACE}}-SOURCE-{{SOURCE-SLOT}}
```

`ROOT-ANCHOR` is the lowercase ASCII artifact identifier. `SOURCE-BLOCK-SEQUENCE` is the concatenation, in the table order below, of `### {block-id}` LF LF, the exact marked block bytes, and one LF. `PREDECESSOR-BODY` is every predecessor byte after its first ATX-H1 physical line. `CANONICAL-PREDECESSOR-BODY` is produced by this byte-determined transform: decode strict UTF-8; require NFC; split CRLF, CR or LF as line endings; delete only trailing ASCII SP and TAB from each line; remove leading empty lines; join with LF; remove terminal empty lines; append exactly one LF. Before and after transformation, tokenize each line into maximal Unicode non-whitespace runs after discarding line-ending bytes and trailing SP/TAB; the two token sequences must be identical or construction fails. No anchors or semantic text are inserted into the predecessor body. A revised source is therefore canonical predecessor-derived text, not a claim of byte identity. Endpoint IDs for its headings come only from section 9 and do not alter bytes.

The exact revised-source block sequences are:

| Slot | Blocks, in order |
|---|---|
| S18 | `E252-SEM-COMPARISON`, `E252-SEM-RECOVERY` |
| S25 | `E252-SEM-DEPENDENCY`, `E252-SEM-RECOVERY` |
| S26 | `E252-SEM-DEPENDENCY`, `E252-SEM-RECOVERY` |
| S27 | `E252-SEM-COMPARISON`, `E252-SEM-RECOVERY` |
| S30 | `E252-SEM-PRIVACY` |
| S32 | `E252-SEM-PRIVACY` |
| S33 | `E252-SEM-COMPARISON` |
| S34 | `E252-SEM-COMPARISON`, `E252-SEM-RECOVERY` |
| S35 | `E252-SEM-DEPENDENCY` |
| S36 | `E252-SEM-COMPARISON`, `E252-SEM-RECOVERY` |
| S37 | `E252-SEM-COMPARISON` |
| S38 | `E252-SEM-DEPENDENCY` |
| S39 | `E252-SEM-DEPENDENCY` |
| S42 | `E252-SEM-PRIVACY` |
| S43 | `E252-SEM-PRIVACY` |
| S47 | `E252-SEM-PRIVACY`, `E252-SEM-RECOVERY` |

`E252-SEM-COMPARISON` means only the bytes between this determination's unique markers `BEGIN E252-SEM-COMPARISON` and `END E252-SEM-COMPARISON`, excluding the marker lines. No Engineering[250] section plus supplemental paragraph is an alternative representation.

Every new source uses this distinct literal prefix and suffix; it has no predecessor fields:

```text
<a id="{{ROOT-ANCHOR}}"></a>
{{H1}}

Identifier:
{{SUCCESSOR-NAMESPACE}}-SOURCE-{{SOURCE-SLOT}}

Document version:
V1

Successor generation:
{{SUCCESSOR-GENERATION-ID}}

Status:
unreviewed-unpublished-non-authoritative

{{NEW-SOURCE-SEQUENCE}}
Candidate status: unreviewed-unpublished-non-authoritative
End of source: {{SUCCESSOR-NAMESPACE}}-SOURCE-{{SOURCE-SLOT}}
```

`NEW-SOURCE-SEQUENCE` is the exact literal sequence below. Each sequence item emits `## {heading}` LF LF, its named block bytes, and one LF.

For an `Atomic Requirements` item, the named block bytes are exactly:

```text
| Requirement | Strength | Applicability | Condition | Normative text | RF | SF |
|---|---|---|---|---|---|---|
{{ROWS:SOURCE-SLOT}}
```

The substitution emits its final data-row LF; when there are no rows it emits zero bytes after the delimiter-row LF.

| Slot | H1 | Exact ordered heading and content sequence |
|---|---|---|
| S69 | `# Privacy Engine Transition Mapping Registry Model {SUCCESSOR-NAMESPACE} Candidate V1` | `Authority Boundary` = `E252-SEM-AUTHORITY`; `Registry Schema` = Engineering[248] section 5 from its registry TSV fence through its empty-registry paragraph; `Atomic Requirements` = generated S69 table; `Conclusion` = `E252-CONCLUSION-S69` |
| S70 | `# Privacy Engine Transition-State Equivalence Profile Model {SUCCESSOR-NAMESPACE} Candidate V1` | `Type and Definition System` = `E252-SEM-TYPES`; `Privacy Validation` = `E252-SEM-PRIVACY`; `Evaluation Dependencies` = `E252-SEM-DEPENDENCY`; `Recovery Function` = `E252-SEM-RECOVERY`; `Atomic Requirements` = generated S70 table; `Conclusion` = `E252-CONCLUSION-S70` |
| S71 | `# Privacy Engine Transition Authorization Binding Model {SUCCESSOR-NAMESPACE} Candidate V1` | `Authorization Binding` = Engineering[248] section 8 excluding heading; `Commitment Construction` = Engineering[248] section 9 excluding heading; `Privacy Validation` = `E252-SEM-PRIVACY`; `Atomic Requirements` = generated S71 table; `Conclusion` = `E252-CONCLUSION-S71` |
| S72 | `# Privacy Engine Transition-State Comparison, Recovery and Semantic Atomicity Model {SUCCESSOR-NAMESPACE} Candidate V1` | `Comparison Procedure` = `E252-SEM-COMPARISON`; `Recovery Function` = `E252-SEM-RECOVERY`; `Authority Boundary` = `E252-SEM-AUTHORITY`; `Atomic Requirements` = generated S72 table; `Conclusion` = `E252-CONCLUSION-S72` |

For the three Engineering[248] imports, the endpoint is exact: section 8 and section 9 begin with the first byte after the named H2 line's LF and end immediately before the next H2 line, retaining the LF before that next H2. The section 5 registry import begins with the line `Registry identifier: {SUCCESSOR-NAMESPACE}-TRANSITION-MAPPING-REGISTRY-001.` and ends with the terminal LF of the paragraph ending `That empty registry authorizes zero transitions.` Absence or multiplicity of either delimiter is fatal.

<!-- BEGIN E252-SEM-AUTHORITY -->
Published Generation 2 remains complete, immutable and unchanged. Correction can occur only through a distinct future successor. Privacy Engine is the implementation-independent authority. I164 is one bounded Speak-up-appV3 implementation; Speak Up is one application adapter and use case. Neither may define, narrow, repair, replace or become the protocol. M remains zero until separately authorized protocol-owned mappings and profiles exist.
<!-- END E252-SEM-AUTHORITY -->

<!-- BEGIN E252-CONCLUSION-S69 -->
The validated empty registry authorizes zero transitions. No absent mapping, profile or authority may be inferred.
<!-- END E252-CONCLUSION-S69 -->

<!-- BEGIN E252-CONCLUSION-S70 -->
An invalid or incomplete profile authorizes zero transitions. Profile validity supplies no authority outside its registered mapping.
<!-- END E252-CONCLUSION-S70 -->

<!-- BEGIN E252-CONCLUSION-S71 -->
A digest establishes only the bounded computational claim defined by its encoded preimage and algorithm. It proves no unencoded identity or semantic claim.
<!-- END E252-CONCLUSION-S71 -->

<!-- BEGIN E252-CONCLUSION-S72 -->
Every occurrence and result remains immutable. Protocol-semantic atomicity neither requires nor derives authority from an implementation transaction mechanism.
<!-- END E252-CONCLUSION-S72 -->

Markdown table cells escape each `\` as `\\` and then each `|` as `\|`; TAB and LF are forbidden. Requirement rows are sorted by final successor inventory order and include a row exactly when `normative_source_ids` contains that source's ID. Supporting references never cause source-local emission. Thus all 16 revised and four new sources have one byte-determined construction with no prose, heading, endpoint or anchor choice.
<!-- END E252-SEM-SOURCES -->

## 7. Exact atomic requirement construction and recomputed counts

<!-- BEGIN E252-SEM-REQUIREMENTS -->
The 92 input rows are exactly the four revised and 88 new rows in Engineering[248] section 14. A row is parsed only when it has exactly four Markdown cells and its first cell begins `{SUCCESSOR-NAMESPACE}-`. The input SHA-256 is inherited from the bound Engineering[248] artifact; no retyping is an authority input.

Modal tokens are `MUST NOT`, `MUST` and `MAY`, matched longest first as complete ASCII words outside code spans. A one-modal input emits one atom byte-for-byte and retains its ID. A multi-modal input is never heuristically split: its ID must occur exactly once in the following closed expansion register, and the listed atom texts are emitted in order as `-A01` onward. The register is construction authority and removes separator, subject and condition judgment.

| Input ID | Exact atoms in order |
|---|---|
| STALEAUTH-003 | `When comparison returns equivalent, the equivalence determination MUST remain bounded to U and its governing profile.` / `When comparison returns equivalent, the equivalence determination MUST preserve D and the authorization unchanged.` / `When comparison returns equivalent, the equivalence determination MUST authorize only the next gate for that U.` |
| STALEAUTH-004 | `When pre-execution comparison returns material-conflict, U MUST terminate with pre-transition failure.` / `When pre-execution comparison returns material-conflict, U's authorization MUST become terminally stale for U.` / `When pre-execution comparison returns material-conflict, execution and commitment MUST be prohibited.` / `When pre-execution comparison returns material-conflict, recovery MUST require a new U under the total disposition function.` |
| TSEID-001 | `Every registry, mapping, profile, authorization, U, comparison attempt, definition and recovery table MUST have one identity satisfying its declared grammar.` / `Every registry, mapping, profile, authorization, U, comparison attempt, definition and recovery table MUST remain distinct from every other identity class.` |
| TSEPRIV-003 | `A blinded component opening MUST remain confidential.` / `A blinded component opening MUST be disclosed only inside an authorized comparison or independent privacy-validation boundary.` |
| TSEPRIV-005 | `Failure, recovery, retry and observability surfaces MUST preserve Private actors, public actions.` / `Failure, recovery, retry and observability surfaces MUST NOT expand disclosure.` |
| TSERESULT-003 | `A commitment digest MUST establish only computational binding of its encoded preimage under the identified algorithm.` / `A commitment digest MUST NOT prove any unencoded semantic or identity claim.` |
| TSEREEVAL-001 | `A new Evaluation MUST create a new E identity.` / `A new Evaluation MUST preserve every earlier E and D without mutation.` |
| TMREG-003 | `Mapping-to-profile cardinality MUST be exactly 1:1.` / `Mapping and profile ordinals MUST match.` |
| TMREG-005 | `An empty validated registry MUST authorize zero transitions.` / `An empty validated registry MUST NOT imply missing or inferred mappings.` |
| TSEPROF-006 | `Every profile MUST define which differences are immaterial.` / `Every profile MUST prove that each immaterial difference is outside the mapping's materiality boundary.` |
| TSEPROF-008 | `An incomplete, ambiguous, cyclic, non-total or privacy-invalid profile MUST be inadmissible.` / `An incomplete, ambiguous, cyclic, non-total or privacy-invalid profile MUST authorize no transition.` |
| TSECMPID-003 | `Each attempt and result MUST remain immutable history of U.` / `Each attempt and result MUST have no lifecycle independent of U.` |
| TSEAUTH-004 | `Each component binding mode MUST be fixed by the published profile.` / `Each component binding mode MUST NOT be chosen per execution.` |
| TSEEXEC-003 | `Execution failure MUST terminally fail U.` / `Execution failure MUST prohibit partial commitment, repair, resumption or alternate successor-state substitution.` |
| TSEFAIL-002 | `An authoritatively evaluated false condition MUST remain FALSE.` / `An authoritatively evaluated false condition MUST be processed by the profile's materiality definition.` |
| TSERECOV-001 | `Dep(D) MUST be the validated least transitive closure defined by S70.` / `Dep(D) MUST include every input capable of affecting D.` |
| TSEAPP-001 | `An application response MAY translate the authoritative bounded result.` / `An application response MUST NOT create, change or reinterpret the authoritative bounded result.` |
| TSERUNTIME-001 | `A runtime MUST implement the published profile and gate exactly.` / `A runtime MUST NOT choose predicates, defaults, materiality or recovery.` |
| TSERUNTIME-003 | `Operational failure MUST be classified at its actual lifecycle layer.` / `Operational failure MUST NOT become protocol rejection, material conflict or equivalence.` |
| TSERUNTIME-004 | `Runtime retry MUST preserve immutable history.` / `Runtime retry MUST instantiate new occurrences exactly where the disposition function requires them.` |
| TSEPRES-002 | `Predecessor and successor generations MUST coexist.` / `Any future succession MUST remain directional and non-retroactive.` |

Validation requires: 71 input IDs absent from this register and containing one modal; 21 IDs present and containing respectively 19 times two, once three and once four modals; every emitted atom contains exactly one modal; no multi-modal input is emitted unsuffixed; and concatenated atom count is 116. The strength is its sole modal.

Condition parsing is exact. If an emitted atom begins `When ` or `For `, `condition_text` is the bytes after that word through the byte before the first comma that precedes the modal, prefixed again by the word; applicability is `conditional`. Otherwise condition is `ALWAYS` and applicability is `applicable`. The condition remains in normative text. The register deliberately repeats the conditions for every STALEAUTH atom; the singleton TSERECOV-006 retains its condition. The exact condition values are `When comparison returns equivalent`, `When pre-execution comparison returns material-conflict` and `When unchanged D is insufficient or cannot be established`.

Source/reference conversion is closed and keeps authority classes separate:

| Input token | Output field | Output token |
|---|---|---|
| `S01` | `supporting_reference_ids` | `STATE` |
| `S02` | `supporting_reference_ids` | `{SUCCESSOR-NAMESPACE}-COMPOSITION-MAP-001` |
| `S03` through `S72` | `normative_source_ids` | `{SUCCESSOR-NAMESPACE}-SOURCE-{input-token}` |
| `PE-G2-SEMANTIC-DIFFERENCE-001` | `supporting_reference_ids` | `{SUCCESSOR-NAMESPACE}-TSE-SEMANTIC-DIFFERENCE-001` |

For a retained G2 row, split its `sources` cell only on comma-space; every resulting complete token must match the table. For an Engineering[248] row, split `Source anchor` only on semicolon-space; each segment must be `SNN`, one space, then a nonempty anchor label. The SNN token is converted by the table and the label is retained in the separate atom-audit source-anchor expression; it is not treated as an identifier. No other token or delimiter is valid. Each output field preserves input order, removes duplicates after first occurrence and joins by comma-space; an empty field is `NONE`. Supporting references never become normative source authority and generate no source-ownership composition edge.

The RF-to-SF register is complete:

```text
RF-01 SF-01
RF-02 SF-01
RF-03 SF-02
RF-04 SF-02
RF-05 SF-01
RF-06 SF-03
RF-07 SF-03
RF-08 SF-03
RF-09 SF-04
RF-10 SF-04
RF-11 SF-04
RF-12 SF-05
RF-13 SF-05
RF-14 SF-12
RF-15 SF-04
RF-16 SF-06
RF-17 SF-06
RF-18 SF-06
RF-19 SF-04
RF-20 SF-07
RF-21 SF-07
RF-22 SF-08
RF-23 SF-08
RF-24 SF-08
RF-25 SF-08
RF-26 SF-09
RF-27 SF-09
RF-28 SF-09
RF-29 SF-10
RF-30 SF-10
RF-31 SF-10
RF-32 SF-11
RF-33 SF-11
RF-34 SF-11
RF-35 SF-11
RF-36 SF-12
RF-37 SF-12
RF-38 SF-13
RF-39 SF-13
RF-40 SF-13
RF-41 SF-13
RF-42 SF-14
RF-43 SF-14
RF-44 SF-15
RF-45 SF-15
RF-46 SF-15
RF-47 SF-15
RF-48 SF-15
RF-49 SF-16
RF-50 SF-16
```

The 745 unchanged G2 rows are all rows except `PE-G2-COMMIT-004` and `PE-G2-STALEAUTH-002` through `004`. Their successor IDs replace the first literal `PE-G2-` with `{SUCCESSOR-NAMESPACE}-`; their anchors are the lowercase successor IDs; source tokens use the conversion table; normative text, strength, applicability text, RF, SF and predecessor relationship are otherwise copied. Each atomized revised row replaces its predecessor at that predecessor's first inventory position. Atomized additions follow, in Engineering[248] row order. Orders begin `0001` and are contiguous.

Every emitted atom must pass all of these tests: exactly one modal equal to `strength`; RF exists once in the register; SF equals the register output; every reference token converts into exactly one authority class; every normative source exists; ID and anchor are unique; predecessor is one of the four replaced IDs for revisions and `NONE` for additions; and no TAB, CR or LF occurs in a cell. Failure rejects the complete inventory.

Per-atom family validation is exact rather than statistical. The audit row is `atom_id input_id rf sf conservation_class audit_result`. For a singleton, `conservation_class` is `IDENTICAL-LEXICAL-OBLIGATION`; for a registered expansion it is `EXPLICIT-CONJUNCT-OF-INPUT`. `rf` is copied from the sole input row and `sf` is the closed RF lookup. `audit_result` is PASS only if the atom occurs byte-for-byte in the closed expansion register or equals the singleton input, its sole modal is preserved, its condition is preserved, and it retains the input RF. This determination authoritatively classifies each explicit conjunct in the register as within its input RF; a constructor performs no semantic classification. There are 116 audit rows and all must PASS. Family sufficiency is then tested independently on the complete inventory: every one of RF-01 through RF-50 and SF-01 through SF-16 must have at least one row, every RF must have its registered SF, and no unregistered family may appear.

Independent recomputation gives:

| Quantity | Exact result |
|---|---:|
| G2 input rows | 749 |
| Replaced G2 rows | 4 |
| Byte-preserved predecessor-derived rows | 745 |
| Revised/new lexical rows | 92 |
| One-modal lexical rows | 71 |
| Two-modal lexical rows | 19 |
| Three-modal lexical rows | 1 |
| Four-modal lexical rows | 1 |
| Revised/new atoms | `71 + 19*2 + 1*3 + 1*4 = 116` |
| Successor requirement rows | `745 + 116 = 861` |
| Successor `MUST` rows | 565 |
| Successor `MUST NOT` rows | 278 |
| Successor `MAY` rows | 18 |
| RF families represented | 50 |
| SF families represented | 16 |

The revised/new atom counts by affected RF are: RF-08 3; RF-10 7; RF-11 5; RF-12 3; RF-13 4; RF-22 4; RF-26 20; RF-27 4; RF-28 9; RF-29 5; RF-30 6; RF-31 4; RF-34 6; RF-35 16; RF-36 3; RF-37 7; RF-40 2; RF-49 4; RF-50 4. Every one resolves through the closed register. Because the 745 retained rows already collectively represent RF-01 through RF-50 and SF-01 through SF-16, and every new atom maps to an existing RF and its single registered SF, the mechanically retained family totals are 50 RF and 16 SF; these counts are not assumptions.

`PE-TSE-REQDATA-V3` is the immutable lexical construction dataset shared by source and inventory constructors. Its bytes are ASCII `PE-TSE-REQDATA-V3` LF; an input TSV with header `input_order input_id normative_text source_anchor_expression rf modal_count`; its 92 Engineering[248] rows in input order; an atom TSV with header `atom_order atom_id input_id strength normative_text source_anchor_expression rf sf conservation_class`; and its 116 emitted atoms in order. Spaces between field names in this description are emitted TAB. Ordinals are ORD4. `conservation_class` is the audit value above. Every row ends LF. Its independently executed construction has SHA-256 `ff0ed6cf287cca253b50953b28e22d5f27dae5326c5213a65f61d84ddd3825da`, 45,095 bytes and 211 LF. Both source `ROWS` emission and artifact 0034 consume these immutable bytes; neither consumes the other's output. A mismatch rejects construction.
<!-- END E252-SEM-REQUIREMENTS -->

## 8. Closed comparison block

<!-- BEGIN E252-SEM-COMPARISON -->
Each comparison attempt identity is `{U-ID}-TSE-CMP-{ORD6}`. Ordinals begin `000001` and are contiguous within U. The exact attempt fields, in order, are attempt ID; generation ID; mapping ID and digest; profile ID and digest; authorization ID and digest; U ID; D ID; Q0 ID and digest; current-state ID and digest; stage; result; failure code. Stage is `PRE-EXECUTION` or `PRE-COMMITMENT`. Result is `equivalent`, `material-conflict` or `indeterminate`.

Evaluation executes in this order: validate identity grammar, registered relationships and digests; validate profile, authorization, opening evidence and state authentication; evaluate equivalence expression `EQ`; evaluate sufficient-conflict expressions in profile order, producing `MC=TRUE` if any is TRUE, `MC=FALSE` if all are FALSE and `MC=UNRESOLVED` otherwise; then select the first matching row:

| Condition | Result | Failure code |
|---|---|---|
| identity, relationship, digest, profile, authorization, opening or authentication failure | indeterminate | the exact validation failure |
| `EQ=TRUE` and `MC=TRUE` | indeterminate | `INCONSISTENT-BOTH-TRUE` |
| `MC=TRUE` | material-conflict | `NONE` |
| `EQ=TRUE` and `MC=FALSE` | equivalent | `NONE` |
| `EQ=FALSE` and `MC=FALSE` | indeterminate | `INCOMPLETE-PROFILE-COVERAGE` |
| otherwise | indeterminate | `UNRESOLVED-REQUIRED-INPUT` |

The closed comparison failure codes, in order, are `NONE`, `INVALID-IDENTITY`, `UNREGISTERED-IDENTITY`, `DIGEST-MISMATCH`, `INVALID-PROFILE`, `INVALID-AUTHORIZATION`, `INVALID-OPENING`, `UNAUTHENTICATED-STATE`, `INCONSISTENT-BOTH-TRUE`, `INCOMPLETE-PROFILE-COVERAGE` and `UNRESOLVED-REQUIRED-INPUT`. Every attempt produces one immutable result and one code. Only equivalent permits the next gate. An independently sufficient authenticated conflict remains material-conflict despite unrelated unresolved input. No validation failure yields equivalence or absence of a result.
<!-- END E252-SEM-COMPARISON -->

## 9. Byte-level canonical Markdown lexer and parser

`CANONICAL-MARKDOWN-ENDPOINTS-V3` accepts strict UTF-8, NFC and LF-only bytes. BOM, CR and non-NFC text are invalid. A terminal LF is not required: scan byte zero through each LF into physical lines whose span includes that LF, then, if bytes remain, emit one final line with `has_lf=FALSE`. Empty input has zero lines. Concatenating every line span must reproduce the exact input. Recognition is stateful and uses this precedence:

1. If inside a fenced block, consume through the first closing fence. An opening line, after removing its optional LF, is zero through three spaces followed by `n >= 3` backticks or tildes and then only bytes other than that fence character. A closing line is zero through three spaces, at least `n` copies of the same fence character and optional spaces, with no suffix. All lines form one `FENCE`; EOF before closing is invalid. Fenced bytes are never reparsed.
2. After removing optional LF, a display-formula delimiter is zero through three spaces, exactly `$$` and optional spaces. It ends at the next delimiter line. A one-line formula is zero through three spaces, `$$`, nonempty content, `$$`, optional spaces. The delimiter form is tested first; EOF before its close is invalid.
3. After removing optional LF, an ATX heading is zero through three spaces, one through six `#`, one space, nonempty content, optional space plus terminal `#` characters and optional spaces. It is one `HEAD`.
4. After removing optional LF, a thematic break is zero through three spaces and at least three identical `*`, `-` or `_` separated only by spaces. It is one `BREAK`.
5. A table is recognized only when the current nonblank line and immediately following line have the same positive cell count and the following line's every cell matches `:?-{3,}:?` after trimming ASCII spaces. The current line is one `THEAD`, the following line one `TDELIM`, and each subsequent nonblank line having that same cell count is one `TROW`; the table ends before the first other line.
6. A list item begins with zero through three spaces followed by `- `, `* `, `+ ` or one through nine decimal digits plus `. `. It consumes a later nonblank line only when that line has at least marker-start-column plus two leading spaces. It consumes intervening blank lines only when followed by such a continuation. It is one `LIST` endpoint.
7. A line with four or more leading spaces is immediately one `LINE`; this rule is tested before paragraph collection.
8. A paragraph begins at any remaining nonblank line. It consumes following nonblank lines only while each line fails rules 1 through 7 when tested independently. It is one `PARA` endpoint.

Blank lines delimit endpoints and are not endpoints. They remain addressable as exact gap bytes so concatenating endpoint bytes and gap bytes reproduces the input exactly.

Table cell parsing scans a row after removing only its optional LF. First pre-scan backtick runs left-to-right: a run begins a code span only if a later unescaped run of exactly the same length exists; otherwise every byte of the unmatched run is ordinary literal data. A backslash escapes exactly the next byte, including a backslash or pipe; a terminal backslash is literal. Pipe bytes inside recognized code spans or immediately preceded by an escaping backslash are not separators. Other pipes are separators. Remove at most one leading and at most one trailing presentation pipe before division; trim ASCII SP around each cell but retain escapes and all other bytes. Cell endpoints are `{ROW-ID}-CELL-{ORD3}`.

Block endpoints are `{ROOT-ID}-{KIND}-{ORD6}`, with one global contiguous ordinal in byte order and `KIND` one of `HEAD`, `PARA`, `LIST`, `THEAD`, `TDELIM`, `TROW`, `FENCE`, `FORMULA`, `BREAK` or `LINE`. The endpoint digest is SHA-256 of its exact bytes. No sentence splitting or normative keyword filtering occurs.

The following test vectors are mandatory. `\n` denotes LF only in this display.

| Vector bytes | Expected kinds | Additional assertion |
|---|---|---|
| `` ```abnf\na = b\n```\nAfter.\n `` | `FENCE,PARA` | `abnf` is suffix text; content is not reparsed |
| `| A | B |\n| --- | --- |\n| x\\|y | \`p|q\` |\n` | `THEAD,TDELIM,TROW` | data row has exactly two cells |
| `- item\n  continuation\n\nParagraph.\n` | `LIST,PARA` | continuation belongs to LIST; blank line is a gap |
| `$$\nx+y\n$$\n---\n    indented\n` | `FORMULA,BREAK,LINE` | no paragraph absorbs formula, break or indented line |
| `# Final` | `HEAD` | unterminated final line is accepted and endpoint bytes have no LF |
| ``| A | B |\n| --- | --- |\n| `x | y |\n`` | `INVALID-TABLE-CELL-COUNT` | unmatched backtick is literal, so its pipes are separators |

Mandatory conformance hashes the reconstructed bytes and requires equality with the original for every accepted vector. The exact D247 input (SHA-256 `35f2ce9bb84aaec7e3d5dfecb341d3d04cadb65060d89028a4e70a08e731bcc5`) is mandatory: it has 228 LF, one final unterminated physical line, round-trips byte-for-byte and must parse without terminal-LF normalization.

## 10. Syntactic bidirectional trace generation

The immutable root set is E243, E244, B245-CANONICAL-V1, E246, D247, E248, D249, E250, D251 and E252. Its digest register is:

| Root | SHA-256 |
|---|---|
| E243 | `97f5201adbed45395a1cbc0d3db2fd6a8419d36d687a1bfe25c901e99c9c59d3` |
| E244 | `d57807fc9da70a5a0cfa4a37897256b336fc18dba2aa987d97ad5d5146e99f30` |
| B245-CANONICAL-V1 | `cbcab0d6899e9f82aa2fc9a26ad3c3d034c79d976a448626396d2df85062b32d` |
| E246 | `a191d11525b254374731562f40fd2be142fa00d8c89c03441bc0b694c66cb493` |
| D247 | `35f2ce9bb84aaec7e3d5dfecb341d3d04cadb65060d89028a4e70a08e731bcc5` |
| E248 | `1f5b59b0ff4720ee142a42017f13e543e1a3973fd81113ca86ca2ead43834a73` |
| D249 | `636899f5426b8a70065b7f7193bba8ef1d0542e10c2ecc014a90cea39990bb37` |
| E250 | `558747f7091ab5e5f597a3f3fba3acb987ea28dfd652e7e691e81371d2b5ccf2` |
| D251 | `ae67f309c7d13a656d0e5d66a89ad016eb64910a464897def54116e02cef940b` |
| E252 | exact authorized materialized payload SHA-256 |

B245-CANONICAL-V1 is the exact 1,205-byte, 10-LF TSV serialization required by Engineering[250] section 10. E252's digest is derived from its later authorized materialized bytes and is not a constructor-selected parameter.

Destination endpoints are rows in this closed register; each row's locator must resolve exactly once in this determination:

```text
E252-ROOT-IMPORT-E243 heading:## 1. Status, scope, precedence and immutable inputs
E252-ROOT-IMPORT-E244 heading:## 1. Status, scope, precedence and immutable inputs
E252-ROOT-IMPORT-B245-CANONICAL-V1 heading:## 1. Status, scope, precedence and immutable inputs
E252-ROOT-IMPORT-E246 heading:## 1. Status, scope, precedence and immutable inputs
E252-ROOT-IMPORT-D247 heading:## 1. Status, scope, precedence and immutable inputs
E252-ROOT-IMPORT-E248 heading:## 1. Status, scope, precedence and immutable inputs
E252-ROOT-IMPORT-D249 heading:## 1. Status, scope, precedence and immutable inputs
E252-ROOT-IMPORT-E250 heading:## 1. Status, scope, precedence and immutable inputs
E252-ROOT-IMPORT-D251 heading:## 1. Status, scope, precedence and immutable inputs
E252-ROOT-IMPORT-E252 heading:## 1. Status, scope, precedence and immutable inputs
E252-CORRECTION-2 heading:## 2. Complete PE-TSE-EXPR-V1 type and definition system
E252-CORRECTION-5 heading:## 3. Exact privacy evidence, authority and validation
E252-CORRECTION-6 heading:## 4. Evaluation production and occurrence-specific Dep(D)
E252-CORRECTION-7 heading:## 5. Corrected total recovery table
E252-CORRECTION-8 heading:## 6. Literal successor-source construction
E252-CORRECTION-9 heading:## 7. Exact atomic requirement construction and recomputed counts
E252-CORRECTION-10 heading:## 10. Syntactic bidirectional trace generation
E252-CORRECTION-11 heading:## 9. Byte-level canonical Markdown lexer and parser
E252-CORRECTION-12 heading:## 11. Literal Markdown, TSV and manifest serializers
E252-CORRECTION-13 heading:## 12. Complete artifact adjacency graph and topological order
E252-CORRECTION-14 heading:## 13. Append-only authenticated installation and recovery
E252-DEFECT-01 section-14:defect-01
E252-DEFECT-02 section-14:defect-02
E252-DEFECT-03 section-14:defect-03
E252-DEFECT-04 section-14:defect-04
E252-DEFECT-05 section-14:defect-05
E252-DEFECT-06 section-14:defect-06
E252-DEFECT-07 section-14:defect-07
E252-DEFECT-08 section-14:defect-08
E252-DEFECT-09 section-14:defect-09
E252-DEFECT-10 section-14:defect-10
E252-DEFECT-11 section-14:defect-11
```

The `section-14:defect-NN` locator is the unique first Engineering[251] table row in section 14 whose first cell is canonical decimal N without a leading zero; the destination identifier retains two-digit NN. These destination-register rows are canonical endpoints and are included in endpoint-existence validation.

Every root is parsed by V3. Assignment requires no semantic choice:

1. Every endpoint from E243, E244, B245-CANONICAL-V1, E246, D247, E248 or D249 maps by `preserved-by` to `E252-ROOT-IMPORT-{ROOT-ID}`. This is an explicit preservation disposition, not a semantic import into a successor source.
2. E250 section membership begins at an ATX H2 whose content starts with canonical decimal section number, full stop and space, and ends before the next H2 or EOF. Endpoints in sections 2 or 5 through 14 map by `corrected-by` to `E252-CORRECTION-{number}`; every other E250 endpoint, including bytes before its first H2, maps by `preserved-by` to `E252-ROOT-IMPORT-E250`.
3. For D251, a defect range begins at an ATX H3 whose content is `{N}.` followed by a space, for N 1 through 11, and ends before the next H3 or any H2. Every endpoint in that range maps by `resolved-by` to `E252-DEFECT-{N:02d}`. Every other D251 endpoint—including intake, verdict, improvements, authority/lifecycle and next-gate sections and bytes before the first defect H3—maps by `preserved-by` to `E252-ROOT-IMPORT-D251`.
4. Every E252 marked semantic-block endpoint maps by `defined-by` to every source slot listed for that block in section 6. All other E252 endpoints map by `preserved-by` to `E252-ROOT-IMPORT-E252`.
5. Every requirement maps by `assigned-to` to its source IDs, RF and SF in emitted cell order.
6. Every source and requirement maps by `composed-into` to its exact specification anchor generated in section 11.
7. Emit the inverse immediately after every forward row. Forward and inverse rows name each other's final ordinal.

Forward rows sort by root order above, from-endpoint byte order, relation order `preserved-by`, `corrected-by`, `resolved-by`, `defined-by`, `assigned-to`, `composed-into`, then destination byte order. Each parsed source endpoint receives exactly one disposition under rules 1 through 4; rules 5 and 6 add constructed-object relations and do not replace that disposition. Validation requires disposition-domain cardinality to equal total parsed endpoint cardinality and every source endpoint to occur exactly once. This is a closed endpoint-to-endpoint generation rule. No subject interpretation, keyword selection or constructor assignment exists.

The trace TSV schema is:

```text
trace_order\tfrom_endpoint\tto_endpoint\trelation\tinverse_trace_order\troot_id\troot_sha256\tcoverage_status
```

`coverage_status` is literal `complete`. Validation rejects an endpoint without its required row, a duplicate disposition, a missing inverse, a dangling endpoint or a relation outside the closed set and their exact inverses.

## 11. Literal Markdown, TSV and manifest serializers

The only serializer controls are `{{NAME}}`, `{{BLOCK:ID}}`, `{{ROWS:SOURCE-SLOT}}`, `{{FOREACH:REGISTER}}...{{END}}` and `{{EXACT-BYTES:ARTIFACT-RANGE}}`. `NAME` performs one bound ASCII substitution; BLOCK and ROWS have the section 6 meanings; a loop iterates the named closed register in its stated order; EXACT-BYTES copies the uniquely named byte range. Controls are not emitted. There are no conditional controls except explicitly named two-variant templates. Every emitted Markdown file uses this common prefix:

```text
<a id="{{ROOT-ANCHOR}}"></a>
{{H1}}

Identifier:
{{ARTIFACT-ID}}

Document version:
V1

Successor generation:
{{SUCCESSOR-GENERATION-ID}}

Status:
unreviewed-unpublished-non-authoritative

```

The seven previously descriptive Markdown bodies are replaced as follows.

`MD-STATUS-V3` body:

```text
## Candidate State

This candidate contains exactly 40 artifacts: 36 normative and four evidence-only.

## Exact Inventory

The normative closed set contains 70 sources, 861 requirements, zero mappings and zero profiles.

## Validation State

Every artifact must pass its canonical serializer, digest graph and closed-set validation before independent review.

## Review State

Candidate review has not been performed.

## Publication State

The candidate is unpublished and non-authoritative.

## Authority

Published Generation 2 remains complete, immutable and unchanged. This candidate has no authority before the separately required lifecycle acts.

## Conclusion

Candidate status is unreviewed-unpublished-non-authoritative.
```

`MD-DECLARATION-V3` has two exact bodies. Artifact 0002 uses:

```text
## Immutable Predecessor

Generation: PE-PROTOCOL-GENERATION-002
Published identity: PE-PUBLISHED-PROTOCOL-G2-001
Specification: PE-PROTOCOL-SPECIFICATION-G2
Specification version: 2.0.0
Specification SHA-256: ffeaed785a34e8535d489ad6946dbdae3a55b441a0c94c8c05791eb33fd423e1

## Boundary

Generation 2 remains complete, immutable and unchanged. This successor candidate does not modify, reopen, reinterpret or retroactively govern Generation 2.
```

Artifact 0004 uses:

```text
## Coexistence

The predecessor and successor generations coexist as distinct immutable generations.

## Non-Retroactivity

No successor requirement, source, mapping, profile, comparison, recovery or publication act changes a predecessor occurrence, result or authority.

## Succession Boundary

Any future succession is directional, separately authorized and non-retroactive.
```

`MD-DIFFERENCE-V3` body is the literal line `## Complete Corrected Semantics`, LF LF, followed by marked blocks `E252-SEM-TYPES`, `E252-SEM-PRIVACY`, `E252-SEM-DEPENDENCY`, `E252-SEM-RECOVERY`, `E252-SEM-SOURCES`, `E252-SEM-REQUIREMENTS`, `E252-SEM-COMPARISON` in that order, each preceded by `### {BLOCK-ID}` LF LF and followed by one LF.

`MD-IDENTITY-V3` body:

```text
## Identity

Generation identifier: {{SUCCESSOR-GENERATION-ID}}
Generation label: {{SUCCESSOR-GENERATION-LABEL}}
Namespace: {{SUCCESSOR-NAMESPACE}}
Version: {{SUCCESSOR-VERSION}}

## Grammar

The generation identifier, label, namespace and version must satisfy their separately authorized construction grammar. No other identity parameter is permitted.

## Predecessor

Immediate predecessor: PE-PROTOCOL-GENERATION-002

## Status

This identity is candidate-only, unreviewed, unpublished and non-authoritative.
```

`MD-PREREQUISITES-V3` has two bodies. Artifact 0006 uses:

```text
## Required Review

Independent candidate review must verify all 40 artifacts, 70 sources, 861 requirements, zero mappings, zero profiles, every digest edge and complete bidirectional traceability.

## Failure Rule

A missing, invalid, ambiguous or non-reproducible member blocks candidate acceptance.

## Separation

Candidate review neither performs specification acceptance nor any publication, succession or implementation-adoption act.
```

Artifact 0007 uses:

```text
## Required Acceptance

Independent candidate acceptance and independent specification acceptance must complete before publication readiness may be assessed.

## Required Lifecycle Separation

Protocol Publication, succession and Protocol Specification Publication are separate authorized acts with separate records.

## Failure Rule

Missing authority, digest mismatch or incomplete lifecycle evidence blocks publication.

## Implementation Boundary

Publication does not adopt the successor into I164.
```

`MD-CLOSED-SET-V3` body:

```text
## Closed Counts

Sources: 70
Mappings: 0
Profiles: 0
Requirements: 861
Artifacts: 40
Normative artifacts: 36
Evidence-only artifacts: 4

## Closure

No unlisted source, mapping, profile, requirement or artifact is a candidate member.
```

`MD-SPEC-IDENTITY-V3` body:

```text
## Specification Identity

Specification identifier: PE-PROTOCOL-SPECIFICATION-{{SUCCESSOR-GENERATION-LABEL}}
Specification version: {{SUCCESSOR-VERSION}}
Governing generation: {{SUCCESSOR-GENERATION-ID}}
Candidate digest state: DIGEST-COMPUTED-AFTER-NORMATIVE-COMPOSITION-BEFORE-SEMANTIC-MANIFEST
Source count: 70
Requirement count: 861
```

`MD-SPECIFICATION-V3` body is generated only by this literal loop template:

```text
## Specification Identity

Specification identity artifact: {{SUCCESSOR-NAMESPACE}}-PROTOCOL-SPECIFICATION-IDENTITY-001
Specification identity SHA-256: {{ARTIFACT-0037-SHA256}}
Specification identifier: PE-PROTOCOL-SPECIFICATION-{{SUCCESSOR-GENERATION-LABEL}}
Specification version: {{SUCCESSOR-VERSION}}
Governing generation: {{SUCCESSOR-GENERATION-ID}}

{{FOREACH:SF-REGISTER}}<a id="{{sf_anchor}}"></a>
## {{sf_id}} — {{sf_title}}

{{FOREACH:RF-IN-SF}}<a id="{{rf_anchor}}"></a>
### {{rf_id}} — {{rf_title}}

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
{{FOREACH:REQUIREMENT-IN-RF}}| <a id="{{requirement_anchor}}"></a> {{requirement_id}} | {{strength}} | {{applicability}} | {{condition_text}} | {{escaped_normative_text}} | {{escaped_normative_source_ids}} | {{escaped_supporting_reference_ids}} |
{{END}}
{{END}}
{{END}}
```

SF and RF titles and order are copied from the G2 section/family inventory after digest verification; only IDs and anchors replace literal `G2` with the authorized successor label or namespace where present. Every RF belongs to exactly one SF by section 7. Requirement iteration is final inventory order filtered by RF. `ARTIFACT-0037-SHA256` is computed only after artifact 0037 is final. These are byte operations, not prose selections.

Revised and new sources use section 6 templates. No other Markdown serializer exists.

All TSVs use TAB separators, LF records, no quoting, no TAB or LF in cells, one header, contiguous zero-padded ordinals and exactly one terminal LF. In the following serializer table, spaces between header field names denote one emitted TAB; spaces within a cell value are shown only inside backticks as part of that value. The artifacts are:

| Artifact | Exact header | Exact data-row generation |
|---|---|---|
| 0028 Registry | `registry_order mapping_id mapping_path mapping_sha256 profile_id profile_path profile_sha256 applicability_definition_id recovery_definition_id status` | zero rows because M=0 |
| 0029 Source closed set | `source_order source_slot source_identifier successor_path treatment identity_method successor_sha256 predecessor_path predecessor_sha256 predecessor_relationship` | S03 through S72; S03-S68 copy predecessor register cells, use `PRESERVED` or `REVISED`; S69-S72 use `NEW`, `NOT-APPLICABLE` predecessor cells; all successor IDs are `{SUCCESSOR-NAMESPACE}-SOURCE-Sxx`; revised and new paths and digests come from constructed source artifacts |
| 0032 Composition | `composition_order relation from_id to_id from_anchor to_anchor normative_status` | the closed rules below |
| 0034 Requirements | `requirement_order requirement_id requirement_anchor rf_family sf_family strength applicability condition_text normative_text normative_source_ids supporting_reference_ids treatment predecessor_requirement_id mapping_id profile_id` | section 7, exactly 861 rows |
| 0035 Classification | `classification_order successor_requirement_id predecessor_requirement_id classification reason` | one row per requirement; `unchanged` and `BYTE-PRESERVED`, `revised` and `MODAL-ATOMIZED-REVISION`, or `new` and `MODAL-ATOMIZED-ADDITION` |
| 0036 Sections | `record_order record_class identifier title parent_identifier first_requirement last_requirement requirement_count` | one ROOT row, then SF-01 through SF-16, then RF-01 through RF-50; first, last and count are derived by filtering 0034 and use `NONE`, `NONE`, `0` only for an empty group, which validation forbids for RF or SF in this candidate |
| 0039 Trace | section 10 header | section 10 algorithm |

For 0029, `source_order` is `source_slot - 2`, formatted ORD4. `successor_path` is the exact successor path in Engineering[248] section 16 for revised/new artifacts and the exact predecessor path for preserved sources. The remaining cells are fixed by treatment:

| Treatment | treatment | identity_method | successor_sha256 | predecessor cells | predecessor_relationship |
|---|---|---|---|---|---|
| Preserved S03-S68 | `unchanged-immutable-source-input` | `sha256-fixed-predecessor-bytes` | exact predecessor SHA-256 | exact predecessor path and SHA-256 | `identical-to-immutable-source-by-reference` |
| Revised S03-S68 | `successor-revised-source` | `sha256-constructed-canonical-bytes` | constructed source SHA-256 | exact predecessor path and SHA-256 | `successor-revision-of` |
| New S69-S72 | `successor-new-source` | `sha256-constructed-canonical-bytes` | constructed source SHA-256 | both `NOT-APPLICABLE` | `new-successor-source` |

The composition relation domain and generation are closed:

1. For each source S03-S72 emit `SOURCE-DEFINES-SPECIFICATION` from source ID and root anchor to the specification root anchor.
2. For each requirement and each `normative_source_ids` token, emit `REQUIREMENT-OWNED-BY-SOURCE` from requirement ID and anchor to source ID and root anchor. Supporting references emit no ownership edge.
3. For each requirement emit `REQUIREMENT-COMPOSED-INTO-SPECIFICATION` from requirement ID and anchor to its specification requirement anchor.

Sort by that relation order, then `from_id`, `to_id`, `from_anchor`, `to_anchor` as unsigned UTF-8 bytes; number from `000001`; `normative_status` is literal `normative`. There are no other composition rows.

The exact cardinality is 3,267: 70 source-to-specification rows, 2,336 requirement-to-S03-through-S72 source rows and 861 requirement-to-specification rows. The 2,336 middle rows independently decompose into 2,170 rows from the 745 unchanged requirements and 166 rows from the 116 revised/new atoms.

The source manifest is TAB-separated with header `manifest_order source_slot source_id path sha256 bytes lf_count treatment`. It has 70 source rows in S03-S72 order. Row `0071` is exactly `0071`, `END`, `{SUCCESSOR-NAMESPACE}-SOURCE-COMPOSITION-MANIFEST-001`, `NOT-APPLICABLE`, `NOT-APPLICABLE`, `70`, `NOT-APPLICABLE`, `COUNT`.

The semantic manifest has header `manifest_order semantic_class semantic_id path sha256 row_count status` and the following exact rows before digest substitution. `sha256` is the computed digest of the identified artifact and status is `closed-validated-normative-member` in every row.

| Order | semantic_class | semantic_id | path | row_count |
|---|---|---|---|---|
| 0001 | REGISTRY | `{SUCCESSOR-NAMESPACE}-TRANSITION-MAPPING-REGISTRY-001` | `mappings/TRANSITION_MAPPING_REGISTRY_V1.tsv` | 0 |
| 0002 | REQUIREMENTS | `{SUCCESSOR-NAMESPACE}-REQUIREMENT-INVENTORY-001` | `specification/COMPLETE_NORMATIVE_REQUIREMENT_INVENTORY_V1.tsv` | 861 |
| 0003 | SECTIONS | `{SUCCESSOR-NAMESPACE}-SECTION-FAMILY-INVENTORY-001` | `specification/SUCCESSOR_SECTION_AND_FAMILY_INVENTORY_V1.tsv` | 67 |
| 0004 | COMPOSITION | `{SUCCESSOR-NAMESPACE}-COMPOSITION-MAP-001` | `composition/SUCCESSOR_COMPOSITION_MAP_V1.tsv` | 3267 |
| 0005 | SPECIFICATION-IDENTITY | `{SUCCESSOR-NAMESPACE}-PROTOCOL-SPECIFICATION-IDENTITY-001` | `specification/SUCCESSOR_PROTOCOL_SPECIFICATION_IDENTITY_V1.md` | NOT-APPLICABLE |
| 0006 | SPECIFICATION | `PE-PROTOCOL-SPECIFICATION-{SUCCESSOR-GENERATION-LABEL}` | `specification/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_{SUCCESSOR-GENERATION-LABEL}_CANDIDATE_V1.md` | 861 |

The manifest is constructed after 0038.

The package manifest has header `artifact_order artifact_id classification path sha256 bytes lf_count dependency_ids`. It has exactly 40 rows in Engineering[248] section 16 order. `classification` is `NORMATIVE` for N and `EVIDENCE-ONLY` for E. ID and path are copied from that register after parameter substitution. Digests, bytes and LF counts are computed from final artifact bytes. `dependency_ids` is the comma-separated artifact-ID list corresponding to the direct adjacency in section 12, in ascending artifact order, or `NONE`. Row 0040 uses literal `SELF` in sha256, bytes and lf_count; those are the only `SELF` cells and have no digest meaning. No terminal count row exists.

TSV terminal rows are prohibited except the explicitly defined source-manifest row. Thus no ordinal grammar exception remains unstated.

## 12. Complete artifact adjacency graph and topological order

An edge `A -> B` means artifact A consumes B's bytes, digest, identifier, anchor, row set or count and B must be complete first. Numeric range `NNNN-MMMM` expands to every four-digit order in inclusive ascending order. The closed direct adjacency is:

The verified Engineering[252] payload, its bound authorities, the 66 predecessor source records and `PE-TSE-REQDATA-V3` are external immutable construction inputs, not candidate artifacts and not vertices. In particular, artifacts 0008 through 0027 and 0034 independently consume REQDATA; they do not consume one another. Every candidate-to-candidate dependency is listed below.

| Artifact | Direct prerequisites |
|---:|---|
| 0001 | 0031, 0033, 0039 |
| 0002 | NONE |
| 0003 | NONE |
| 0004 | NONE |
| 0005 | NONE |
| 0006 | NONE |
| 0007 | NONE |
| 0008 | NONE |
| 0009 | NONE |
| 0010 | NONE |
| 0011 | NONE |
| 0012 | NONE |
| 0013 | NONE |
| 0014 | NONE |
| 0015 | NONE |
| 0016 | NONE |
| 0017 | NONE |
| 0018 | NONE |
| 0019 | NONE |
| 0020 | NONE |
| 0021 | NONE |
| 0022 | NONE |
| 0023 | NONE |
| 0024 | NONE |
| 0025 | NONE |
| 0026 | NONE |
| 0027 | NONE |
| 0028 | NONE |
| 0029 | 0008-0027 |
| 0030 | 0029 |
| 0031 | 0028, 0032, 0034, 0036, 0037, 0038 |
| 0032 | 0008-0027, 0034, 0036, 0037 |
| 0033 | 0028, 0029, 0034, 0038 |
| 0034 | NONE |
| 0035 | 0034 |
| 0036 | 0034 |
| 0037 | 0005 |
| 0038 | 0008-0027, 0029, 0030, 0032, 0034, 0036, 0037 |
| 0039 | 0003, 0008-0027, 0032, 0034, 0036, 0038 |
| 0040 | 0001-0039 |

Every prerequisite list expands ranges, removes no entry, rejects duplicates, then sorts ascending. The package manifest converts each order to its exact artifact ID. A consumer embedding a prerequisite digest must use the digest computed from the already final bytes. A consumer using only identifiers, anchors, rows or counts still retains the edge so construction order captures every byte dependency, not merely digest fields.

The one valid topological order is fixed for construction as:

```text
0002,0003,0004,0005,0006,0007,
0008,0009,0010,0011,0012,0013,0014,0015,0016,0017,0018,0019,0020,0021,0022,0023,0024,0025,0026,0027,0028,
0034,0035,0036,0029,0030,0037,0032,0038,0031,0033,0039,0001,0040
```

This order places specification identity 0037 before candidate 0038 and semantic manifest 0031 after candidate 0038. It has 40 unique members and satisfies every direct edge. Artifact 0040's `SELF` cells are not graph edges. Any additional embedded digest or byte dependency is an undeclared edge and invalidates construction.

## 13. Append-only authenticated installation and recovery

Candidate construction and destination installation are separate. Installation begins only with two objects: an authorization record and a pre-existing trusted authority binding supplied by the separately authorized installation gate. The trusted binding is exactly `authority_id TAB ED25519-RFC8032 TAB key_fingerprint_sha256 TAB authorization_sha256 LF`, where the fingerprint is SHA-256 of the raw public-key octets. It is stored outside the candidate and attempt and cannot be created or changed by installation. The authorization has exact fields `authorization_id`, `candidate_package_sha256`, `destination_root_sha256`, `authority_id`, `algorithm`, `public_key`, `permitted_operation`, `authorization_sha256`, `signature`. All nine are serialized as `field: SP value LF` in that order. Algorithm is `ED25519-RFC8032`; public key is 64 lowercase hexadecimal characters; permitted operation is `INSTALL-ABSENT-AND-RECOVER` or `REPLACE-COMPLETE-AND-RECOVER`. `destination_root_sha256` hashes the UTF-8/NFC absolute destination path with no terminal slash followed by LF. The authorization digest is SHA-256 over the first seven serialized lines. `authorization_sha256` is that lowercase digest. `signature` is Ed25519 over the raw 32 digest octets. Admission requires exact equality of authority ID, algorithm, computed key fingerprint and authorization digest with the trusted binding before signature verification. A self-supplied key without that equality has no authority. A different package, destination or operation requires a different authorization and trusted binding.

An attempt consists of an outside-destination directory containing `attempt.tsv`, `prior/` and `authorization.txt`. `authorization.txt` contains the exact authorization record and its Ed25519 signature. `prior/` contains immutable prior bytes named by six-digit target order plus `.bin`; absence is represented by no file and digest `ABSENT`. For DIFFERENT-COMPLETE, `prior/manifest.tsv` has header `path_order relative_path prior_sha256 bytes` with exactly 40 artifact-order rows and one terminal LF. Its digest is recorded in BEGIN's `prior_sha256`; every blob digest and byte count must match before mutation. For ABSENT, BEGIN's `prior_sha256` is `ABSENT` and `prior/manifest.tsv` is absent.

`attempt.tsv` has this exact header:

```text
entry_order\tentry_type\tattempt_id\tpath_order\trelative_path\tprior_state\tprior_sha256\tcandidate_sha256\tresult_state\tprevious_entry_sha256\tentry_sha256\tauthority_id\tsignature
```

`attempt_id` is `{authorization_id}-ATTEMPT-{ORD6}`; the ordinal begins `000001` and is contiguous for that authorization. Entry order begins `000001` and is contiguous. `entry_type` is `BEGIN`, `PREPARE-CREATE`, `APPLY-CREATE`, `PREPARE-REPLACE`, `APPLY-REPLACE`, `CHECKPOINT`, `PREPARE-ROLLBACK-REMOVE`, `APPLY-ROLLBACK-REMOVE`, `PREPARE-ROLLBACK-RESTORE`, `APPLY-ROLLBACK-RESTORE` or `TERMINAL`. `path_order` is `000000` for BEGIN, CHECKPOINT and TERMINAL and otherwise the candidate's four-digit artifact order zero-extended to six digits. `relative_path` is `NOT-APPLICABLE` for path order zero. The closed state-cell domain is `ABSENT`, `IDENTICAL-COMPLETE`, `DIFFERENT-COMPLETE`, `PARTIAL-INVALID`, `INTENT-RECORDED`, `PRESENT`, `RESTORED`, `REMOVED`, `COMPLETE`, `ROLLED-BACK`, `BLOCKED`, `PARTIAL-UNRECOVERABLE` and `NOT-APPLICABLE`. Digests are lowercase SHA-256, `ABSENT` or `NOT-APPLICABLE` where the entry matrix permits it.

| Entry type | path fields | prior_state / prior_sha256 | candidate_sha256 | result_state |
|---|---|---|---|---|
| BEGIN | zero / NOT-APPLICABLE | classified destination state / ABSENT or prior-manifest digest | package digest | PRESENT or BLOCKED |
| PREPARE-CREATE | artifact / path | ABSENT / ABSENT | artifact digest | INTENT-RECORDED |
| APPLY-CREATE | artifact / path | ABSENT / ABSENT | artifact digest | PRESENT |
| PREPARE-REPLACE | artifact / path | PRESENT / prior artifact digest | artifact digest | INTENT-RECORDED |
| APPLY-REPLACE | artifact / path | PRESENT / prior artifact digest | artifact digest | PRESENT |
| CHECKPOINT | zero / NOT-APPLICABLE | NOT-APPLICABLE / NOT-APPLICABLE | checkpoint digest | PRESENT |
| PREPARE-ROLLBACK-REMOVE | artifact / path | PRESENT / candidate artifact digest | ABSENT | INTENT-RECORDED |
| APPLY-ROLLBACK-REMOVE | artifact / path | PRESENT / candidate artifact digest | ABSENT | REMOVED |
| PREPARE-ROLLBACK-RESTORE | artifact / path | PRESENT / candidate artifact digest | prior artifact digest | INTENT-RECORDED |
| APPLY-ROLLBACK-RESTORE | artifact / path | PRESENT / candidate artifact digest | prior artifact digest | RESTORED |
| TERMINAL | zero / NOT-APPLICABLE | NOT-APPLICABLE / NOT-APPLICABLE | package digest | COMPLETE, ROLLED-BACK, BLOCKED or PARTIAL-UNRECOVERABLE |

For each entry, serialize the first ten cells through `previous_entry_sha256` with TAB separators and LF. `entry_sha256` is SHA-256 of literal `PE-TSE-INSTALL-ENTRY-V1`, LF, those bytes. `signature` is Ed25519 over the raw 32 digest octets. `authority_id` and key must match the trusted authorization. Entry 000001 uses 64 zeroes as previous digest; every later entry uses the immediately preceding `entry_sha256`. Each complete row append must be atomic at row granularity and durably flushed before the next permitted step; an environment unable to guarantee that property must block before BEGIN. Appending never changes earlier bytes. The log is append-only and every row immutable. A missing ordinal, invalid signature, broken link or trailing partial row invalidates the log and permits no mutation.

The admitted destination classifications are exact:

| State | Byte predicate |
|---|---|
| ABSENT | none of the 40 target paths exists |
| IDENTICAL-COMPLETE | all 40 exist and match candidate digests |
| DIFFERENT-COMPLETE | all 40 exist, match one separately authenticated prior complete-set manifest, and at least one differs from candidate |
| PARTIAL-INVALID | every other byte state |

Before mutation, BEGIN records the state in `prior_state`, package digest in `candidate_sha256`, and `BLOCKED` or `PRESENT` in `result_state`. For ABSENT installation, prior digest is `ABSENT`. For each candidate path in artifact order the exact sequence is: verify the current prior predicate; append and durably flush PREPARE-CREATE or PREPARE-REPLACE; perform one atomic path mutation; verify resulting candidate digest; append and durably flush the matching APPLY entry; append and durably flush CHECKPOINT. The checkpoint digest is SHA-256 of ASCII `PE-TSE-INSTALL-CHECKPOINT-V1`, LF, then, for every path with an APPLY entry, `path_order`, TAB, candidate SHA-256, LF. After all 40, reclassify bytes and append TERMINAL `COMPLETE` only for IDENTICAL-COMPLETE. No mutation is permitted without its immediately preceding valid flushed PREPARE.

Recovery first reconciles a terminal PREPARE lacking its matching APPLY. For PREPARE-CREATE: absent means the mutation did not occur and no APPLY is added; exact candidate bytes mean it occurred and APPLY-CREATE is appended; any other bytes block. For PREPARE-REPLACE: exact prior bytes mean it did not occur; exact candidate bytes mean it occurred and APPLY-REPLACE is appended; any other bytes block. Reconciliation is repeated until the log has no unmatched installation PREPARE.

For an ABSENT prior state, recovery processes applied creates in reverse order. For each, verify candidate bytes; append and flush PREPARE-ROLLBACK-REMOVE; atomically remove the path; verify absence; append and flush APPLY-ROLLBACK-REMOVE. If interrupted after rollback PREPARE, candidate bytes mean removal did not occur, absence means it occurred and the APPLY row is appended, and every other state blocks. After all removals, require ABSENT and append TERMINAL `ROLLED-BACK`.

For a separately authorized REPLACE-COMPLETE-AND-RECOVER attempt whose BEGIN proves DIFFERENT-COMPLETE, every prior target's bytes must be copied to `prior/{order}.bin` and verified before the first PREPARE. Installation uses PREPARE-REPLACE and APPLY-REPLACE as above. Recovery processes applied replacements in reverse order: verify candidate and stored prior digests; append and flush PREPARE-ROLLBACK-RESTORE; atomically restore prior bytes; verify; append and flush APPLY-ROLLBACK-RESTORE. An unmatched rollback-restore PREPARE reconciles candidate bytes as not yet restored and exact prior bytes as restored, appending APPLY only in the latter case; other bytes block. Finally verify the authenticated prior complete-set manifest and append TERMINAL `ROLLED-BACK`. This determination supplies no installation authorization.

A pre-existing PARTIAL-INVALID destination without one valid authenticated attempt and matching authorization is terminal `PARTIAL-UNRECOVERABLE`. No removal, overwrite, selective repair, inference or retry is permitted. The only permissible action is to preserve the bytes and obtain a separate explicit forensic recovery authorization outside this construction basis. An invalid log, missing prior blob, digest mismatch or authority failure transitions the attempt to `BLOCKED`; if a valid TERMINAL entry can still be appended it is appended, otherwise the byte state itself is treated as blocked. Retry is permitted only after verified ABSENT or IDENTICAL-COMPLETE classification. DIFFERENT-COMPLETE and PARTIAL-UNRECOVERABLE never silently become retryable.

The state transitions are closed:

| From | Evidence/event | To |
|---|---|---|
| ABSENT | valid INSTALL-ABSENT-AND-RECOVER BEGIN | INSTALLING |
| DIFFERENT-COMPLETE | valid REPLACE-COMPLETE-AND-RECOVER BEGIN and verified prior manifest | INSTALLING |
| INSTALLING | valid PREPARE-CREATE, mutation, APPLY-CREATE and CHECKPOINT | INSTALLING |
| INSTALLING | valid PREPARE-REPLACE, mutation, APPLY-REPLACE and CHECKPOINT | INSTALLING |
| INSTALLING | all 40 and byte verification | IDENTICAL-COMPLETE |
| INSTALLING | interruption with valid log | RECOVERING |
| RECOVERING | complete verified ABSENT rollback | ABSENT |
| RECOVERING | complete verified prior-set rollback | DIFFERENT-COMPLETE |
| any mutable attempt state | mismatch or invalid recovery evidence | BLOCKED |
| PARTIAL-INVALID without valid recovery evidence | classification | PARTIAL-UNRECOVERABLE |

No other transition exists. These controls govern artifact installation only and do not define protocol transaction semantics.

## 14. Engineering[251] defect closure and additional-defect disposition

| Engineering[251] defect | Exact treatment |
|---:|---|
| 1 | Section 2 removes literal SET as a type, defines `PE-TSE-SET`, `arg(ORD4)` environments, complete grammar, derived encodings, component schema and combined definition/component cycle rejection. |
| 2 | Section 3 defines every evidence file and privacy record, externally appointed profile authority, direct Ed25519 authentication, regenerated finite relation universes, total tests and one failure domain. |
| 3 | Section 4 defines finite field and operation registers, an actual-read execution transcript, exact edge generation, identity groups, occurrence ownership and atomic creation with D. |
| 4 | Section 5 serializes the correct 21-row total function. |
| 5 | Section 6 supplies literal parameterized templates, exact import delimiters and closed block sequences for all 16 revised and four new sources; predecessor transformation is token-conserving and inserts no anchors. |
| 6 | Section 7 replaces splitting heuristics with the complete 21-row multi-modal expansion register, exact singleton rule, condition handling, separate authority/reference conversion, RF-to-SF register and 116-row audit rule. |
| 7 | Section 9 defines physical-line preservation, recognition precedence, fences, formulas, tables, escapes, matched/unmatched code spans, lists, indented lines, paragraphs and test vectors, including exact D247. |
| 8 | Section 10 gives total syntactic disposition rules for every root endpoint, including all non-defect D251 sections, and exact downstream/inverse relations. |
| 9 | Section 11 supplies literal Markdown bodies and loops and exact TSV/manifest schemas, rows, cells and the one terminal-row exception. |
| 10 | Section 12 separates immutable REQDATA from its two consumers, lists every candidate-artifact edge and gives a verified topological order with 0037 before 0038 and 0031 after 0038. |
| 11 | Section 13 binds authority to a pre-existing trusted fingerprint and authorization digest, uses signed write-ahead PREPARE/APPLY pairs for forward and rollback mutations, and defines exact reconciliation and terminal partial states. |

The additional defects recorded in the verified Engineering[252] draft-failure report are also closed:

| Additional defect | Disposition |
|---|---|
| N01 `but` defeats splitter | No splitter exists; TSEAPP-001 has two literal registered atoms. |
| N02 subject and condition loss | STALEAUTH-004 has four literal atoms; each repeats the complete condition and preserves the coordinated execution-and-commitment subject. Its `section 12` reference is explicitly normalized to `total disposition function` because candidate section numbering is serializer-owned. |
| N03 D247 lacks terminal LF | V3 represents the final unterminated line and exact D247 round-trips. |
| N04 actor test always fails | The test inserts no node and fails only on a generated graph path from PUBLIC to PRIVATE-ACTOR. |
| N05 self-signed installation authority | Admission requires a pre-existing out-of-attempt trusted authority binding before signature verification. |
| N06 unlogged mutation windows | Every mutation and rollback has a durable signed PREPARE before mutation and deterministic reconciliation before APPLY. |
| N07 Dep(D) over-inclusion | Only actual READ/CALL events create occurrence edges; an unevaluated admitted field creates none, while the prior semantic-unchangedness test is retained. |
| N08 hidden source/requirement cycle | Both consume immutable `PE-TSE-REQDATA-V3`; neither consumes the other's artifact. |
| N09 unsupported review/closure claims | No independent review is claimed. Closure here is this development-authority determination supported by the tests below. |
| N10 referential family coverage only | Every atom has an explicit conservation class and inherited RF determination; the full inventory independently requires all and only 50 RF and 16 SF families. |

The executable validation suite passed the following behavior checks against the immutable inputs and this payload: explicit atom emission; strength and family totals; complete 861-row arithmetic; 3,267 composition-row construction; exact D247 physical-line round trip; Markdown precedence vectors; argument substitution; combined-cycle rejection; actual-read short-circuiting; privacy reachability and uniqueness; recovery-table keys and unchanged-D dispositions; write-ahead reconciliation; source digest and token-conservation checks; marker/template coverage; and all 40 artifact graph edges against the stated topological order. `PE-TSE-REQDATA-V3` independently reproduced SHA-256 `ff0ed6cf287cca253b50953b28e22d5f27dae5326c5213a65f61d84ddd3825da`, 45,095 bytes and 211 LF. These are construction tests, not an assertion that an independent review occurred.

## 15. Preserved authority and lifecycle boundary

Published Generation 2 remains complete, immutable and unchanged:

- generation: `PE-PROTOCOL-GENERATION-002`;
- published identity: `PE-PUBLISHED-PROTOCOL-G2-001`;
- specification: `PE-PROTOCOL-SPECIFICATION-G2` version `2.0.0`;
- specification SHA-256: `ffeaed785a34e8535d489ad6946dbdae3a55b441a0c94c8c05791eb33fd423e1`.

Completed lifecycle identities remain unchanged. Correction may occur only through a distinct future successor. I164 adoption remains `not-performed`. Implementation readiness remains `blocked-pending-published-successor-correction`. M remains zero.

Privacy Engine remains the implementation-independent authority. I164 remains one bounded Speak-up-appV3 implementation. Speak Up remains one application adapter and use case. I164 does not define, own, narrow, repair, replace or become the protocol.

This determination selects no successor identity, constructs no candidate or specification, performs no lifecycle act and adopts nothing into I164.

## 16. Materialization and Git boundary

Construction of these exact bytes outside the repository does not authorize repository materialization. Repository materialization requires Steve's separate exact-payload authorization binding the proposed path, SHA-256 and byte count. Materialization does not authorize staging, commit, tags, push or package regeneration. Each requires a later explicit authorization.

## 17. Terminal determination

The selected result is:

```text
transition-state-equivalence-mapping-and-profile-semantic-completion-and-exact-construction-basis-third-correction-and-completion-resolved
```

All eleven Engineering[251] defects and N01 through N10 from the verified Engineering[252] draft-failure report have bounded dispositions above. Generation 2 remains complete and unchanged. M remains zero. This proposed determination selects no successor identity and constructs no successor candidate or specification. No materialization, Git operation, package regeneration, publication, succession, lifecycle act or I164 adoption has occurred.
