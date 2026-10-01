# Observation boundary and currentness — proposed source contract

Local documentary owner E284-DRAFT-OBSERVATION-SOURCE. These clauses complete abstract observation semantics for the selected capability. They are proposed source text, not a published amendment, appointed source, actual state assertion, new first-class subject, or selected deployment. No clock, consensus rule, source provider or operational ordering becomes protocol law. Existing S70 source validation and failure precedence remain governing.

<a id="scope"></a>
## OC01 — stable meaning and scope

A membership observation belongs to exactly the membership-state scope required by the fixed action type, proof relation and declared root policy. A uniqueness observation belongs to exactly the protocol-owned action uniqueness scope for the same fixed a,n. Source references bind exact owning source bytes, digest and adequate anchor. The membership scope and uniqueness scope need not have the same identifier or owner. Their joint use requires the governing context to associate those exact scopes with the same selected capability and fixed PI=(n,a,r). No application account, wallet, petition record or provider label supplies that association.

The fixed semantic basis consists of the identified type, governing source/rule/policy meanings, membership and uniqueness scopes, proof relation/artifact meanings, and n,a,r. An observation may not change this basis to obtain an eligible result. An unestablished scope association fails validation before classification. This is source/context validation, not an additional actor or application validity predicate.

### Incorporated proposal: observation-scope

Each root and uniqueness observation MUST identify its exact owning source meaning and scope. Their association to the same selected capability, fixed PI, type and context MUST be validated. Their scope identifiers need not be equal. A provider label, wallet, product record or equal tuple alone MUST NOT establish that association.

<a id="cut"></a>
## OC02 — meaning of a cut

A cut denotes the bounded authoritative observation boundary at which the owning source's stated facts hold. Its identity is a coordinate of that source's boundary, not evidence that the boundary is authentic, complete, current or final. A valid root cut establishes the complete introduction count and newest valid-introduction suffix at that boundary. A valid uniqueness cut establishes the complete exact (a,n) state there. Cut IDs have no inferred lexical, numeric, temporal or cross-source ordering.

The source must establish the meaning of its own cut and its applicability to the requested semantic phase. Two equal cut strings from different sources do not establish the same boundary. Different cut strings can describe jointly applicable observations. A hash authenticates no cut by itself. The abstract interface requires this evidence; a concrete realization supplies its mechanism without changing these meanings.

### Incorporated proposal: observation-cut

A cut MUST denote the bounded source-authoritative observation boundary at which the asserted facts hold. Its identifier MUST NOT itself establish authenticity, completeness, currentness, finality or cross-source ordering. Root evidence MUST establish the complete count and newest valid suffix; state evidence MUST establish the complete exact scoped-key state at the applicable boundary.

<a id="joint"></a>
## OC03 — jointly applicable observations

For fixed context C, a pair of observations is jointly applicable exactly when each observation has been independently validated for its declared scope and cut, and the owning source evidence establishes that their asserted facts can be used together under C at the requested phase without mixing incompatible authoritative states or omitting a relevant change. Both must preserve OC01's fixed basis. Independent plausibility, individual signatures and tuple equality alone do not establish this relation.

This clause does not require one global history, identical source IDs, identical cuts, a shared transaction or simultaneous network retrieval. It does require evidence of the stated joint applicability. If one observation is valid alone but joint applicability is unavailable, no coherent combined input has been established. The source must not select whichever pair yields a preferred classification. A concrete mechanism's finality/reorganization rules require their own adequate governing basis; none is inferred here.

### Incorporated proposal: observation-joint

The owning source evidence MUST establish that individually validated root/state observations can be used together under the fixed context at the requested phase without incompatible authoritative states or omission of a relevant change. Joint applicability MUST NOT be inferred from individual signatures, equal cuts or plausible values alone. It MUST NOT require identical cuts, simultaneous retrieval or one global history absent a governing source rule.

<a id="evaluation"></a>
## OC04 — Evaluation boundary

Before E begins, establish the admitted A, complete R and bounded C as distinct fixed inputs under the selected domain-first and occurrence rules. The E observation assessment binds exactly (E,C,membership-scope,root-cut,uniqueness-scope,state-cut), in that order, using the existing E284-DRAFT-CONTEXT-CUT-BINDING type. Root and state binding tuples retain the existing exact ordered signatures. All facts must be applicable to that E/C and fixed n,a,r.

Currentness at E means applicability to that fixed E/C, not a promise that state remains unchanged forever. Once E begins, do not refresh C, swap an input, silently replace a cut or discard a required rule to make E complete. If the required coherent input/completion basis cannot be established, E cannot produce D; a later attempt must follow the governing new-occurrence rules. A completed D remains historically valid for its own context even if later observations differ.

<a id="gates"></a>
## OC05 — gate boundaries

At PRE-EXECUTION and PRE-COMMITMENT independently, obtain and validate the observations applicable to that gate of the same authorized U. Bind them to the exact authorization, D, Q0, mapping/profile and their digests, immutable fixed semantic basis, gate phase and occurrence-local comparison attempt. Use the existing canonical authorization and comparison-attempt fields; do not add a new public gate subject or silently change their schemas.

Root and state cuts at a gate may differ from E's cuts and from the other gate's cuts. Such differences do not alone establish material conflict. The same fixed r must be accepted under the selected policy and the same (a,n) must be unused. Wrong scope, wrong fixed basis, unestablished currentness or incompatible observations fail validation rather than becoming negative root/unused facts.

An old valid observation is insufficient for a new gate unless the competent source establishes that its asserted facts remain applicable at that gate. Equality of old/new payloads is not currentness evidence. Root expiry after E does not retroactively alter D. It can establish a gate conflict only through a valid, authenticated current observation and the existing predicate.

### Incorporated proposal: observation-phase

E observations MUST bind fixed E/C; each gate observation MUST independently bind the exact authorization, D, Q0, mapping/profile and digests, fixed semantic basis, gate stage and comparison attempt of that U. Old observations MUST NOT be treated as current merely because payloads match; competent evidence MUST establish their continued applicability. Gate cuts MAY differ from E and each other without that difference alone being conflict.

<a id="commitment"></a>
## OC06 — commitment timing and frame

The final authoritative comparison and semantic commitment are one indivisible decision under the existing rule, with no intervening authoritative protocol-state change. If a realization cannot establish that boundary, it cannot commit. This requirement does not select a lock, database transaction, chain transaction, consensus mechanism or rollback strategy.

The only owned effect remains (a,n,FALSE)->(a,n,TRUE), with other keys, membership/history and product state framed unchanged. Currentness assessment observes state; it does not introduce a membership write, change the root policy, reserve the key, serialize all Evaluations, or commit an effect. Competing accepting determinations still require their own gates; an implementation must preserve the selected one-consumption semantics.

<a id="failure"></a>
## OC07 — phase-correct unavailable and negative results

A missing, malformed, untrusted, incomplete or incoherent observation is not a completed negative validity fact. At E it cannot support completion or D. At a gate it follows the governing earlier validation/indeterminate rules. After validation, a complete root observation with acceptedness FALSE or a complete used=TRUE observation may establish independently sufficient material conflict as the existing comparison procedure allows, despite an unrelated unresolved predicate input. OC03 must not be used to erase that distinction or to turn every unresolved predicate into a validation failure.

A valid joint source basis is distinct from whether every material predicate is evaluable. Complete E requires all assigned rule results; gate comparison retains its independently sufficient MC rule. No new failure subject is created.

### Incorporated proposal: observation-failure

Missing, malformed, untrusted or incoherent source facts MUST NOT become completed negative facts. Validation failures MUST retain precedence over gate predicates. Once preceding validation succeeds, independently sufficient authenticated MC MUST remain decisive despite unrelated unresolved predicate input. Joint applicability MUST NOT turn all unresolved predicates into validation failures or suppress such a conflict.

<a id="coordinates"></a>
## OC08 — fixed bindings, mutable observations and recovery

Maintain three separate joins. First, immutable authorization/context joins fix subjects, meanings, scopes and n,a,r. Second, current gate observations establish the phase-specific root and scoped state facts. Third, full actual Dep(D) and its fresh validation/equality map govern unchanged-D recovery. Equality at one join does not imply equality at another.

Introduction count/positions are ordered history evidence, not automatically an inter-transition authorization ordering coordinate. Cut IDs are source observation coordinates, not automatically canonical ordering coordinates. This contract introduces no inter-U dependency beyond the selected source rules. It does not prove that the final authorization coordinate sets are empty: concrete source definitions must establish whether additional required ordering/dependency coordinates exist. Any such coordinate must be explicit and canonically bound before profile admission.

The typed E binding already reads every supplied cut/scope/raw history/state/proof field. Source and authentication evidence remain actual S70 dependency nodes. A history change may preserve gate eligibility while changing Dep(D). Fresh sufficiency must assess every actual dependency, not only the two projected Boolean values. Exact 21-row recovery and failed-U terminality remain unchanged.

### Incorporated proposal: coordinates

Fixed authorization/context coordinates, mutable current observations and full recovery dependencies MUST remain separate. The complete ordering/dependency-coordinate sets MUST include every coordinate required by the selected source meanings. Cut IDs and introduction positions MUST NOT automatically become inter-U ordering coordinates. A declaration of no additional coordinates MUST have an exact source completeness basis; NONE in the retained bounded projection is not that proof.

<a id="privacy"></a>
## OC09 — custody and composed observations

Additional cut, source, history, proof-completion and context-join records are confined to the authorized source/evaluation/comparison and independent privacy-validation boundaries. Public PI remain on their existing governed surface; confidentiality of a joined internal record does not erase those public values or their equality links. Source metadata and occurrence/cut identifiers can correlate records and must appear in the complete actor/correlation model.

The declared two-context model must include the full 118-field program inventory, relevant source/authentication metadata, operation/argument/control relationships, existing owning schemas, and public PI aliases. No provider trace or currentness witness is automatically authorized for publication. Actual source-specific observer/custody facts and independent appointment/evidence remain unsupplied. A finite local model cannot prove completeness of an absent concrete source adapter.

### Incorporated proposal: privacy-universe

The complete privacy model MUST include all 118 declared fields, exact owning schemas, public PI aliases, source/evidence/operation/argument/control surfaces and every producer-added observer/custody/correlation path in two distinct contexts. Additional joined records MUST NOT become public by implication. Actor reconstruction MUST use the full graph; the governed constant-edge exception MUST apply only to correlation reachability.

<a id="closure"></a>
## OC10 — what is complete and what remains

OC01–09 close the abstract semantic drafting for scope, cut, joint applicability, E/gate currentness, commitment timing, failure, dependency and custody. Missing appointment or occurrence evidence is not an obstacle to writing those clauses. Conversely, these clauses do not appoint their owner, establish any real current facts, supply a concrete decoder/authority mechanism, or prove source-specific coordinate/acquisition closure.

The next concrete source realization must provide adequate exact mappings from its representations and evidence to these meanings, satisfy VI01–04's completed-verification distinction, and expose all additional actual dependencies/observers. That remaining adapter construction cannot be replaced by setting validated flags to TRUE. Current G3 remains immutable with M=0; all proposed new source meanings require their separately governed basis. No [285] handover is justified solely by this abstract contract.
