# PE-G4-SOURCE-S73 — unpublished G4 source candidate

Status: candidate construction, not appointed or published. The following inherited authoring narrative is preserved with explicit identifier substitution. Its references to unallocated identities and earlier chat status are historical; identity.json and sources/PE-G4-SOURCE-S82.md govern this candidate. No compatible semantic duty is waived.

# Engineering[284] — source contract for the bounded comparison draft

Documentary owner: PE-G4-SOURCE-S73. All anchors below are local draft coordinates, not appointed or published sources. The existing PE-G4-SOURCE-S74 and PE-G4-SOURCE-S75 definitions retain their exact meanings and bytes. This text supplies a candidate interface using existing S70 types; it allocates no successor, mapping, profile, action-type identity or live source. The two selected rules are not reopened.

<a id="domain"></a>
## Domain and representation

SC01. Each a, n and r, and each occupied root slot, denotes one scalar x with 0 <= x < 21888242871839275222246405745257275088548364400416034343698204186575808495617. The modulus is the scalar modulus retained by E283, not BN254's base-field modulus. PE-TSE-UINT only establishes a canonical nonnegative integer. Source validation must additionally establish the strict upper bound. No implicit field reduction, truncation, signed conversion or interpretation of a hash as a scalar is allowed. The order of public proof inputs remains n,a,r. None of the observation arguments becomes a new public proof input.

SC02. At the declared expression boundary values already use the complete canonical S70 TSEV1 typed encoding. The identity decoder/canonicalizer/normalizer is consequently valid for BOOL3 components: each maps BOOL3 to itself. It does not decode an RPC object, JSON integer, Solidity word, Merkle event or arbitrary bytes. Such a representation needs its own adequate source-owned decoder and authenticated correspondence before it can cross this boundary. No external wire format is selected.

SC03. An authoritative used state contains only FALSE or TRUE. The tuple (a,n,used) has exactly that order. UNRESOLVED is an evaluation/evidence status, never a third state or an unused default. Missing storage is not FALSE unless a separately adequate state source establishes the complete scoped unused fact. The nullifier's correct private derivation is established by the retained proof relation; no secret is an observation input.

<a id="history"></a>
## Valid introductions and exact observation

SC04. H is the complete finite authoritative sequence of valid membership-root introductions for one membership-state scope through the relevant cut. An introduction is one authoritative state-introduction occurrence accepted under the governing membership-state validity rules. A duplicate observation/retransmission of that occurrence adds nothing. A distinct valid introduction with the same root adds one. Initial state adds one only if actually introduced. This clause does not define a new membership mutation, appoint a log, or deem every scalar a valid membership root.

SC05. K=min(16,|H|). Slots 1..K are the last K introductions, newest first; all their occupancy flags are TRUE. Slots K+1..16 have value zero and flag FALSE. An occupied zero is not a sentinel and is permitted only when its membership-state introduction is valid. All flags must be complete Boolean values and form a TRUE prefix. The root-acceptance expression is unchanged. Reordering, omission, fabricated occupancy, counting retransmissions or padding privilege invalidates the observation, rather than establishing root conflict.

SC06. An adequate source assertion must bind membership scope, introduction identities, their authoritative order, complete suffix and evidence of its cut, policy/version/owner, canonical scalar meanings, and the fixed r. The cut is the context selected for E or the independently current PRE-EXECUTION/PRE-COMMITMENT boundary. A timestamp, block height, RPC label, signature or list alone is insufficient. A full earlier history need not be copied into the projection, but evidence must establish that the supplied suffix is complete and newest at that cut. No universal finality rule, concrete provider or chain is selected.

SC07. Two observations can project the same acceptedness while differing in their actual read values/evidence. Such a change may be immaterial to this gate and still fail unchanged-D sufficiency. Keep every actual dependency and its independently authenticated source metadata. Changing history is not automatically a write effect or a root conflict.

<a id="status"></a>
## Status stage meaning and exact signatures

SC08. The available, valid and authenticated stage functions each have ordered signature (PE-TSE-BOOL3)->PE-TSE-BOOL3 and expression arg(0001). They propagate a separately authenticated fact; they do not establish one. AUTHORITATIVE is the existing S70 status read, not an invented fourth configurable function. The projection authority predicate also propagates a validated authority fact. No status function is the constant TRUE.

SC09. For ROOT-ELIGIBLE, AUTHORITATIVE means an independently established competent policy/membership observation source; AVAILABLE means the required observation is present at the required boundary; VALID means SC01 and SC04–06, fixed-context joins and exact derivation all hold; AUTHENTICATED means the exact value/status/cut/scope assertion has been independently authenticated through that source's governed authority chain. For SCOPED-USED the corresponding assertions concern exactly (a,n), its complete valid current state and coherent boundary, not an unscoped nullifier set. An authenticated false status and absence of source authentication are different cases; both prevent use of the component as a trusted projected fact.

SC10. ReadObject authority/validity/authentication flags are assertions already checked independently under S70, not unchecked caller inputs. A BOOL3 status value may carry UNRESOLVED where the governed procedure allows it; it cannot fabricate a valid source value. Component PROJECT requires its statuses before normalization and matching authenticated VALUE. A malformed or unauthenticated state is an earlier validation failure. An unrelated unresolved predicate input is not automatically that failure; preserve independently sufficient authenticated MC under the existing comparison procedure.

<a id="components"></a>
## Candidate projection and local minimality

SC11. Candidate component 000001 ROOT-ELIGIBLE is BOOL3 v, the authenticated latest-16 acceptance of fixed r. Candidate component 000002 SCOPED-USED is BOOL3 b, the authenticated used status of fixed (a,n). Both are CONFIDENTIAL, AUTHENTICATED-CONFIDENTIAL-COMPARISON-ONLY, CANONICAL-VALUE in this drafting candidate. This uses an already admitted binding mode and introduces no blind, key or new disclosure. It does not select a real profile or claim canonical-value is compulsory for future profiles. Public proof inputs retain their own existing disclosure rules.

SC12. Within the validated selected-effect domain, both components are necessary: with b=FALSE, v=TRUE permits the gate and v=FALSE conflicts; with v=TRUE, b=FALSE permits and b=TRUE conflicts. Thus neither may be removed while preserving those decisions. Slots/order/occupancy are needed to derive v but their unchanged values are not necessary for gate equivalence. The scoped key and r are validation/context coordinates, not independent mutable eligibility bits. Membership tree, all other keys, product records, actor/provenance, wallet, secret, leaf and path are excluded from this bounded projection. Necessary source evidence and actual reads are not thereby excluded from Dep(D).

SC13. This proves necessity and sufficiency only after all conditions in material-conditions.tsv have been established. It is not global minimality, applicability or complete comparison coverage for an unfinished capability. A newly applicable material rule must be resolved and, if necessary, change this candidate before admission. No whole-state snapshot is authorized. The successful write remains only (a,n,FALSE)->(a,n,TRUE); all other keys, membership/history and product state have the selected frame condition.

<a id="predicates"></a>
## Exact predicate and validation binding

SC14. The E283 v/b functions are unchanged. New zero-input reference wrappers specialize those exact functions to CURRENT component references. ROOT-CONFLICT reads only v and USED-CONFLICT reads only b, so neither wrapper eagerly reads an unused argument. EQ and aggregate MC preserve the original logical form and short-circuit semantics. The ordered sufficient MC list is ROOT-CONFLICT, then USED-CONFLICT; aggregate is their OR. Authorized ROOT-ELIGIBLE must be TRUE and SCOPED-USED FALSE, source q0 must equal SOURCE-STATE(a,n), D must be an accepting completed D, and the fixed a,n,r/policy/context must agree before gate predicates run. A mismatched action, nullifier, root, policy or source is validation failure, not a sufficient state conflict.

SC15. CORE-COHERENCE has ordered inputs (r,s1..s16,o1..o16,a,n,q). It compares computed root acceptance with projected current v, and q with tuple(a,n,current b), and confirms authorized v=TRUE/b=FALSE. It is a bounded coherence check, not E, D, source authentication, full applicability, or a comparison result. It must not be used to turn incoherent source evidence into ordinary MC. A FALSE or unresolved coherence check prevents treating these as complete valid inputs; independently supported conflict handling still follows the governing validation distinction.

SC16. EQ remains v AND NOT b. ROOT-CONFLICT=NOT v; USED-CONFLICT=b. On complete Boolean pairs they are disjoint and exhaustive. Their wrappers do not delete the validation-first, both-true, incomplete-coverage or unresolved-input rows. On authenticated v=FALSE with unrelated b unresolved, or authenticated b=TRUE with unrelated v unresolved, sufficient conflict remains decisive unless a prior validation failure applies. Root expiry cannot retroactively alter D. Gate acceptedness says nothing about recovery's unchanged-D test.

<a id="coordinates"></a>
## Context, coordinates and custody

SC17. The local context type is tuple(a,n,r), distinct from the public PI order (n,a,r). Context construction is an internal typed coordinate, not a reordered proof interface. Scope/policy/source/cut and authorization identities remain mandatory authenticated joins. The three scalar values alone do not identify the membership scope or source cut. The final ordering/dependency-coordinate definition set cannot be declared empty or complete until the exact authority-owned cut/scope interface is supplied. Do not insert a made-up chain height or source digest as a substitute.

SC18. Candidate component values and representation/status evidence are confined to the authorized comparison and independent validation boundary. Header, coordinate digests, component binding and current-state evidence retain the full S70 owning and context joins. CANONICAL-VALUE is not permission for public disclosure. There are no blinds/openings in this candidate; their owning fields are NOT-APPLICABLE as S70 requires. A later choice of blinded mode must satisfy all original per-component/per-authorization entropy, confidentiality and no-reuse requirements, without actor-derived randomness.

<a id="dependency"></a>
## Determination dependencies

SC19. The candidate component membership function uses an owned literal SET containing ROOT-ELIGIBLE and SCOPED-USED. It classifies these two projection rows as INCLUDED; it is not the complete actual Dep(D) algorithm. Full Dep(D) is the least actual dependency closure rooted in the completed D, with all executed operation/READ/status/argument/authority/authentication/control/value/group edges generated by the existing constructor and exact replay. Input acquisition performed outside an expression is not free of dependencies. The separate source-acquisition and complete-E interface remains a closure boundary until its actual dependencies can be represented, authenticated and replayed.

SC20. Pure equality is complete canonical typed equality for BOOL3, UINT, the complete scoped state and the complete internal context; each field also needs matching identity/type/authority and validated evidence under unchanged. Typed scalar equality alone does not compare two observations, cuts or metadata envelopes semantically. No identity groups are declared: repeated equal root values from different introductions are not merged. Actual repeated READ occurrences stay distinct. Adding a group later requires identical canonical value, type and authority, pure binary equality, at least two actual members, and the governing lowest-occurrence representative.

SC21. Fresh recovery must cover every member of the actual Dep(D), not just v,b or a declared field inventory. A proved difference/invalidity yields FALSE; otherwise any unavailable validation/equality yields UNRESOLVED; TRUE requires the complete governing conjunction. The exact 21-row recovery table is preserved byte-for-byte as data in this package. Failed U remains terminal. TRUE sufficiency can justify only separately authorized new U where that row permits it; FALSE/UNRESOLVED require new E and new D only on successful completion.

<a id="privacy"></a>
## Privacy definitions and scope

SC22. Privacy/observability predicates in the local table propagate externally established complete evidence results with (BOOL3)->BOOL3 signatures. They are neither substitute proofs nor a way to let an issuer choose evidence scope. Both components plus full composition require independent static evidence over two distinct symbolic contexts, all fixed owning schemas, conservative expression relations, all possible nonconstant equality joins and the complete actor graph. The constant-edge exception applies only to correlation reachability as governed, never to pruning the actor graph.

SC23. Source ownership, complete materiality/minimality/coverage/disjointness, actual privacy appointment, adequate observation/status/cut definitions and exact source closure are admission obligations. No actual U/D/history/opening is required to draft them. Actual occurrence records, complete observer universe, source-authenticated history and complete fresh validation maps belong at use. Neither absence of an occurrence nor absent live source access is a policy choice for Steve.

<a id="applicability"></a>
## Exact candidate applicability definition

PE-G4-CAP-APPLICABILITY has ordered inputs (type source reference, rule-set source reference, a, n, Q0). Its expression tests exact byte-bound references to S76 action-type and rules and Q0=(a,n,FALSE). It is a mapping applicability predicate within the independently validated domain, not a proof of complete R, source competence, scalar bounds, privacy, an accepting D or authorization. Those antecedents remain mandatory admission/context checks. No caller chooses the expected references: the literals bind the actual S76 bytes in this candidate.

A TRUE result alone never permits E, authorization, execution or commitment. The rule source explicitly requires every additionally applicable rule resolved before E. That obligation is preserved, rather than replaced with a TRUE default. The mapping candidate remains blocked wherever its material/source conditions are unclosed.

## Exact source-owned definition declarations

The following declarations specialize the retained PE-TSE-EXPR-V2 grammar. The source_anchor column identifies the semantic clause above. They are construction candidates, not independently admitted declarations.

```tsv
definition_order	definition_id	kind	input_type_ids	output_type_id	expression	source_id	source_anchor
0011	PE-G4-CAP-BOOL-IDENTITY	FUNCTION	PE-TSE-BOOL3	PE-TSE-BOOL3	arg(0001)	PE-G4-SOURCE-S73	domain
0012	PE-G4-CAP-AUTHORITY-STATUS	CONDITION	PE-TSE-BOOL3	PE-TSE-BOOL3	arg(0001)	PE-G4-SOURCE-S73	status
0013	PE-G4-CAP-AVAILABILITY-STATUS	CONDITION	PE-TSE-BOOL3	PE-TSE-BOOL3	arg(0001)	PE-G4-SOURCE-S73	status
0014	PE-G4-CAP-VALIDITY-STATUS	CONDITION	PE-TSE-BOOL3	PE-TSE-BOOL3	arg(0001)	PE-G4-SOURCE-S73	status
0015	PE-G4-CAP-AUTHENTICATION-STATUS	CONDITION	PE-TSE-BOOL3	PE-TSE-BOOL3	arg(0001)	PE-G4-SOURCE-S73	status
0016	PE-G4-CAP-EQUAL-BOOL	CONDITION	PE-TSE-BOOL3,PE-TSE-BOOL3	PE-TSE-BOOL3	equal(arg(0001),arg(0002))	PE-G4-SOURCE-S73	dependency
0017	PE-G4-CAP-EQUAL-UINT	CONDITION	PE-TSE-UINT,PE-TSE-UINT	PE-TSE-BOOL3	equal(arg(0001),arg(0002))	PE-G4-SOURCE-S73	dependency
0018	PE-G4-CAP-EQUAL-STATE	CONDITION	PE-G4-CAP-SCOPED-STATE,PE-G4-CAP-SCOPED-STATE	PE-TSE-BOOL3	equal(arg(0001),arg(0002))	PE-G4-SOURCE-S73	dependency
0019	PE-G4-CAP-EQUAL-CONTEXT	CONDITION	PE-G4-CAP-CONTEXT,PE-G4-CAP-CONTEXT	PE-TSE-BOOL3	equal(arg(0001),arg(0002))	PE-G4-SOURCE-S73	dependency
0020	PE-G4-CAP-CONTEXT	FUNCTION	PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT	PE-G4-CAP-CONTEXT	tuple(PE-G4-CAP-CONTEXT,arg(0001),arg(0002),arg(0003))	PE-G4-SOURCE-S73	coordinates
0021	PE-G4-CAP-COMPONENTS	SET	NONE	PE-G4-CAP-COMPONENT-SET	apply(PE-TSE-SET,literal(PE-TSE-ID,54534556310000000950452d5453452d494402000000000000000d524f4f542d454c494749424c45),literal(PE-TSE-ID,54534556310000000950452d5453452d494402000000000000000b53434f5045442d55534544))	PE-G4-SOURCE-S73	dependency
0022	PE-G4-CAP-COMPONENT-DEPENDENCY	CONDITION	PE-TSE-ID	PE-TSE-BOOL3	member(arg(0001),PE-G4-CAP-COMPONENTS)	PE-G4-SOURCE-S73	dependency
0023	PE-G4-CAP-PRIVACY-SUPPORT	CONDITION	PE-TSE-BOOL3	PE-TSE-BOOL3	arg(0001)	PE-G4-SOURCE-S73	privacy
0024	PE-G4-CAP-OBSERVABILITY-SUPPORT	CONDITION	PE-TSE-BOOL3	PE-TSE-BOOL3	arg(0001)	PE-G4-SOURCE-S73	privacy
0025	PE-G4-CAP-EQ	CONDITION	NONE	PE-TSE-BOOL3	and(ref(ROOT-ELIGIBLE,CURRENT),not(ref(SCOPED-USED,CURRENT)))	PE-G4-SOURCE-S73	predicates
0026	PE-G4-CAP-MC-ROOT	CONDITION	NONE	PE-TSE-BOOL3	not(ref(ROOT-ELIGIBLE,CURRENT))	PE-G4-SOURCE-S73	predicates
0027	PE-G4-CAP-MC-USED	CONDITION	NONE	PE-TSE-BOOL3	ref(SCOPED-USED,CURRENT)	PE-G4-SOURCE-S73	predicates
0028	PE-G4-CAP-MC	CONDITION	NONE	PE-TSE-BOOL3	or(not(ref(ROOT-ELIGIBLE,CURRENT)),ref(SCOPED-USED,CURRENT))	PE-G4-SOURCE-S73	predicates
0029	PE-G4-CAP-IMMATERIAL-ROOT-ELIGIBLE	CONDITION	PE-TSE-BOOL3,PE-TSE-BOOL3	PE-TSE-BOOL3	equal(arg(0001),arg(0002))	PE-G4-SOURCE-S73	components
0030	PE-G4-CAP-IMMATERIAL-SCOPED-USED	CONDITION	PE-TSE-BOOL3,PE-TSE-BOOL3	PE-TSE-BOOL3	equal(arg(0001),arg(0002))	PE-G4-SOURCE-S73	components
0031	PE-G4-CAP-PRECONDITION-ROOT-ELIGIBLE	CONDITION	PE-TSE-BOOL3	PE-TSE-BOOL3	arg(0001)	PE-G4-SOURCE-S73	predicates
0032	PE-G4-CAP-PRECONDITION-SCOPED-USED	CONDITION	PE-TSE-BOOL3	PE-TSE-BOOL3	not(arg(0001))	PE-G4-SOURCE-S73	predicates
0033	PE-G4-CAP-FRAME-SUPPORT	CONDITION	PE-TSE-BOOL3	PE-TSE-BOOL3	arg(0001)	PE-G4-SOURCE-S73	components
0034	PE-G4-CAP-CORE-COHERENCE	CONDITION	PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-UINT,PE-TSE-UINT,PE-G4-CAP-SCOPED-STATE	PE-TSE-BOOL3	and(equal(ref(ROOT-ELIGIBLE,CURRENT),apply(PE-G4-CAP-ROOT-ACCEPTED,arg(0001),arg(0002),arg(0003),arg(0004),arg(0005),arg(0006),arg(0007),arg(0008),arg(0009),arg(0010),arg(0011),arg(0012),arg(0013),arg(0014),arg(0015),arg(0016),arg(0017),arg(0018),arg(0019),arg(0020),arg(0021),arg(0022),arg(0023),arg(0024),arg(0025),arg(0026),arg(0027),arg(0028),arg(0029),arg(0030),arg(0031),arg(0032),arg(0033))),equal(arg(0036),tuple(PE-G4-CAP-SCOPED-STATE,arg(0034),arg(0035),ref(SCOPED-USED,CURRENT))),equal(ref(ROOT-ELIGIBLE,AUTHORIZED),literal(PE-TSE-BOOL3,54534556310000000c50452d5453452d424f4f4c3300000000000000000101)),equal(ref(SCOPED-USED,AUTHORIZED),literal(PE-TSE-BOOL3,54534556310000000c50452d5453452d424f4f4c3300000000000000000100)))	PE-G4-SOURCE-S73	predicates
0054	PE-G4-CAP-APPLICABILITY	CONDITION	PE-G4-CAP-SOURCE-REFERENCE,PE-G4-CAP-SOURCE-REFERENCE,PE-TSE-UINT,PE-TSE-UINT,PE-G4-CAP-SCOPED-STATE	PE-TSE-BOOL3	and(equal(arg(0001),literal(PE-G4-CAP-SOURCE-REFERENCE,54534556310000001a50452d47342d4341502d534f555243452d5245464552454e43451100000000000000ab00000003000000000000002b54534556310000000950452d5453452d494402000000000000001050452d47342d534f555243452d533736000000000000003e54534556310000000c50452d5453452d4259544553010000000000000020d5cef2cb095ebc81332b226060c23a95656cc3c991fd5006b1bf221b9d91e206000000000000002654534556310000000950452d5453452d494402000000000000000b616374696f6e2d74797065)),equal(arg(0002),literal(PE-G4-CAP-SOURCE-REFERENCE,54534556310000001a50452d47342d4341502d534f555243452d5245464552454e43451100000000000000a500000003000000000000002b54534556310000000950452d5453452d494402000000000000001050452d47342d534f555243452d533736000000000000003e54534556310000000c50452d5453452d4259544553010000000000000020d5cef2cb095ebc81332b226060c23a95656cc3c991fd5006b1bf221b9d91e206000000000000002054534556310000000950452d5453452d494402000000000000000572756c6573)),apply(PE-G4-CAP-IS-SOURCE,arg(0003),arg(0004),arg(0005)))	PE-G4-SOURCE-S73	applicability
```

## Exact type declarations

```tsv
type_order	type_id	kind	element_type_id	field_type_ids
0001	PE-TSE-BOOL3	PRIMITIVE	NOT-APPLICABLE	NOT-APPLICABLE
0002	PE-TSE-BYTES	PRIMITIVE	NOT-APPLICABLE	NOT-APPLICABLE
0003	PE-TSE-ID	PRIMITIVE	NOT-APPLICABLE	NOT-APPLICABLE
0004	PE-TSE-UINT	PRIMITIVE	NOT-APPLICABLE	NOT-APPLICABLE
0005	PE-G4-CAP-SCOPED-STATE	TUPLE	NOT-APPLICABLE	PE-TSE-UINT,PE-TSE-UINT,PE-TSE-BOOL3
0006	PE-G4-CAP-CONTEXT	TUPLE	NOT-APPLICABLE	PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT
0007	PE-G4-CAP-COMPONENT-SET	SET	PE-TSE-ID	NOT-APPLICABLE
0008	PE-G4-CAP-SOURCE-REFERENCE	TUPLE	NOT-APPLICABLE	PE-TSE-ID,PE-TSE-BYTES,PE-TSE-ID
0009	PE-G4-CAP-SCOPE-REFERENCE	TUPLE	NOT-APPLICABLE	PE-G4-CAP-SOURCE-REFERENCE,PE-TSE-ID
0010	PE-G4-CAP-CUT-REFERENCE	TUPLE	NOT-APPLICABLE	PE-G4-CAP-SCOPE-REFERENCE,PE-TSE-ID
0011	PE-G4-CAP-PUBLIC-INPUTS	TUPLE	NOT-APPLICABLE	PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT
0012	PE-G4-CAP-ACTION-INPUT-BINDING	TUPLE	NOT-APPLICABLE	PE-TSE-ID,PE-TSE-ID,PE-G4-CAP-SOURCE-REFERENCE,PE-G4-CAP-SOURCE-REFERENCE,PE-TSE-ID,PE-G4-CAP-PUBLIC-INPUTS
0013	PE-G4-CAP-ADMITTED-DOMAIN-BINDING	TUPLE	NOT-APPLICABLE	PE-TSE-ID,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT
0014	PE-G4-CAP-ROOT-OBSERVATION-BINDING	TUPLE	NOT-APPLICABLE	PE-G4-CAP-SOURCE-REFERENCE,PE-G4-CAP-SCOPE-REFERENCE,PE-G4-CAP-CUT-REFERENCE,PE-TSE-ID,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BOOL3,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-BYTES,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT
0015	PE-G4-CAP-STATE-OBSERVATION-BINDING	TUPLE	NOT-APPLICABLE	PE-G4-CAP-SCOPE-REFERENCE,PE-G4-CAP-CUT-REFERENCE,PE-TSE-ID,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-BOOL3
0016	PE-G4-CAP-VERIFICATION-INPUT-BINDING	TUPLE	NOT-APPLICABLE	PE-TSE-ID,PE-TSE-ID,PE-TSE-BYTES,PE-TSE-UINT,PE-TSE-UINT,PE-TSE-UINT,PE-G4-CAP-SOURCE-REFERENCE,PE-G4-CAP-SOURCE-REFERENCE,PE-TSE-BYTES,PE-TSE-BOOL3,PE-TSE-ID
0017	PE-G4-CAP-CONTEXT-CUT-BINDING	TUPLE	NOT-APPLICABLE	PE-TSE-ID,PE-TSE-ID,PE-G4-CAP-SCOPE-REFERENCE,PE-G4-CAP-CUT-REFERENCE,PE-G4-CAP-SCOPE-REFERENCE,PE-G4-CAP-CUT-REFERENCE
0018	PE-G4-CAP-RECOVERY-ROW	TUPLE	NOT-APPLICABLE	PE-TSE-ID,PE-TSE-ID,PE-TSE-ID,PE-TSE-ID,PE-TSE-ID,PE-TSE-ID,PE-TSE-ID,PE-TSE-ID,PE-TSE-ID,PE-TSE-ID,PE-TSE-ID
0019	PE-G4-CAP-RECOVERY-ROW-SET	SET	PE-G4-CAP-RECOVERY-ROW	NOT-APPLICABLE
```
