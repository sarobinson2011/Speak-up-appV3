# Draft anonymous-participation action, rule and context source

Local documentary owner: E284-DRAFT-ACTION-SOURCE. These are proposed capability clauses, not amendments to published G3. Clause names are document coordinates, not allocated protocol identifiers. The draft type description below fixes meaning without allocating a successor/action-type namespace. Published G3 and M=0 remain unchanged. This draft incorporates the already authorized root-policy, protocol-effect and occurrence selections.

<a id="action-type"></a>
## AC01 — bounded type meaning

The drafted action type is anonymous membership participation for one application-supplied action context a. Its proof establishes the retained membership and action-scoped nullifier relation, with declared public inputs exactly (n,a,r). Membership remains secret-derived; the root is membership-state evidence, the application supplies a unchanged, and n supplies action-local uniqueness. The applicable root policy is the selected latest 16 valid authoritative root introductions, counted as introductions. An accepting D requires the selected single scoped atomic unused-to-used effect through the separately governed authorization/U path. Product objects, product eligibility, petition existence, counters and application records remain outside protocol validity and outside the owned effect.

No new public input, universal technical action ID, actor account, separate acceptance/failure subject or mandatory storage class is introduced. This is the type's semantic description; its eventual published type/generation/specification/profile references require separately governed source closure. The type must never be asserted present in G3's empty mapping registry.

Basis: S19 sections 3–4; S22 sections 5–7/10; S24 sections 4–11; S43 sections 3–9; exact retained ACTION/PROOF/UNIQ/RULE requirements; the three authorized selections.

<a id="occurrence"></a>
## AC02 — selected authoritative occurrence rule

Each presentation newly admitted for authoritative evaluation begins a distinct bounded Protocol Action occurrence, even when its proof or declared public inputs equal those of an earlier presentation. Retrying delivery or retrieving an already completed result does not itself constitute a presentation newly admitted for authoritative evaluation. Each occurrence has its own bounded identity and, if its Evaluation completes, its own Determination. The occurrence identity is not derived from actor identity, proof equality, actionId alone or nullifier equality. The scoped uniqueness state still permits only the selected unused-to-used effect for the same (actionId,nullifier).

The admission boundary is authoritative admission for evaluation, not positive acceptance by D and not merely arrival at an endpoint. The receiver may not use transport arrival, network retry count or implementation scheduling alone as evidence that this boundary has been crossed. The fact of a new authoritative admission and its bounded identity must be established under the source-owned boundary contract. Equal content never merges two separately established admissions. A retained reference used only to deliver/retrieve an existing result does not itself authorize fresh evaluation.

Basis: S24 sections 5–8; ACTION-002/003/006–009/012/014; RULE-011; Steve's selected B.

### Incorporated proposal: occurrence-new

Each new authoritative admission for evaluation MUST instantiate a distinct bounded A even when proof bytes or PI equal an earlier admission. Transport, retransmission, delivery or retrieval alone MUST NOT establish a new authoritative admission or create A/E/D. Admission identity MUST NOT be inferred from proof equality, nullifier equality, actor identity or endpoint arrival.

<a id="admission"></a>
## AC03 — A/R/C before E

Before authoritative E begins, establish A, its type, declared PI, the complete applicable R, and one bounded C as distinct coherent inputs. Type/profile/state/context applicability is source-derived and fixed before E, not chosen by a runtime while evaluating. If complete R or C cannot be established, authoritative E does not begin and no D, acceptance or rejection follows. A network retry is not itself such establishment.

During E preserve that exact A/R/C. Do not repair or replace a failed input, silently widen C, substitute a newer root, drop a rule or add a product rule. New authoritative admission creates a new A under AC02 even if its PI equals an earlier A. S24's distinct A/E/D identities and S25's fixed input boundaries remain intact.

Basis: RULE-001–008/011–013; EVAL-001–007; S25 sections 8–10.

<a id="rules"></a>
## AC04 — assigned validity checks

The concrete assignments in action-rule-context-assignments.tsv bind action/public-input shape and scalar domain; proof/public-input/relation/artifact coherence; bounded complete proof verification; the retained membership/nullifier domain relation; root acceptedness; and scoped unused status. Every additionally applicable source-defined rule must have its exact antecedent, input and assigned check resolved before E. The “other rules” row is a closure obligation, never a TRUE default or a hidden catch-all Boolean.

Proof verification is a component, not the whole E. A proof-invalid result is a negative component result only when verification actually completed. Inability to complete verification is not proof-invalid. Root proof recomputation alone does not establish current acceptedness. Used status and root observation must refer to the same fixed context/scope declared for the occurrence. Canonical UINT encoding alone does not validate the retained scalar domain; the domain/status source contract remains mandatory.

The requirement-role register separates dynamic validity checks from construction, identity, completion, authorization, privacy and governance obligations. It is not correct to fold every normative sentence into a runtime Boolean, or to drop non-predicate obligations because they are not a proof signal.

Basis: PROOF, VERIFY, VALID, UNIQ, RULE-007, EVAL-009–016 and source-contract SC01–16.

<a id="context"></a>
## AC05 — exact context content and exclusions

C fixes the governing generation/specification/profile/type references, selected root-policy/domain/relation/artifact meanings, the application-supplied a and declared n,r, coherent membership/root and uniqueness facts, and only the source-required scope/cut/ordering/dependency conditions. The context must be sufficient for R. It cannot contain discretionary application eligibility, transport policy, wallet/actor identity, provenance bridges, implementation-specific finality defaults or an unrestricted storage snapshot.

The existing internal tuple (a,n,r) remains only a bounded coordinate. It is not the whole C and it does not reorder public PI (n,a,r). Stable scope, policy and source-cut meanings must be source-owned and authenticated; the occurrence selection does not fill their missing interface or authority. Root history is read evidence and a dependency, not an owned write effect.

Basis: S24 sections 9–11; S25 section 8; RULE-003/008/009/013; source-contract SC04–07/17.

<a id="completion"></a>
## AC06 — completion before classification

All required assigned checks must complete coherently before classification. If a required result is unavailable, unresolved, unauthenticated where authentication is required, or incoherent, E remains incomplete and cannot produce D. A known negative from another component does not turn that incomplete E into rejection. Strong-Kleene AND(FALSE,UNRESOLVED)=FALSE is therefore not by itself a complete-E classifier. The v/b gate table is not substituted for this completeness obligation.

Once every required check has completed coherently, acceptance requires satisfaction of every applicable validity rule; rejection means at least one applicable validity rule is not satisfied. Completion and production of exactly one D occur at the same indivisible protocol-semantic boundary. A begun E unable to establish its one valid D at that boundary terminates as Evaluation failure, with no D/acceptance/rejection. Internal steps may exist while E remains active and incomplete; they confer no completed result.

Basis: EVAL-008/012/017–026; DETERM-001–009/015–016; CLASS-001–010; S25 sections 13–14. No new outcome subject is created.

<a id="determination"></a>
## AC07 — identity and preservation of D

D identifies its producing E, evaluated A, fixed R and bounded C and carries the existing acceptance/rejection classification. It remains distinct from proof verification, delivery/public result, authorization, U and committed state. Losing or retrying delivery after E/D completion preserves that E/D and does not create a new D. An explicitly new authoritative presentation follows AC02 and does not revise the prior A/E/D, even if new E produces the same classification.

Deterministic-classification obligations for equivalent valid inputs are preserved without merging identities. A new occurrence is not permission for arbitrary acceptance/rejection, nor is a repeated proof a participant identifier.

Basis: DETERM-001–016; CLASS-001–012; ACTION-002/008/014/016; SEMPRES/SURF preservation obligations.

### Incorporated proposal: occurrence-delivery

Delivery loss or retry after successful E/D completion MUST preserve the same E/D, MUST NOT erase D or reopen E, and MUST NOT by itself create another D. Equal classifications across distinct admissions MUST NOT merge their occurrence identities.

<a id="effect"></a>
## AC08 — effect requirement and bounded success

For this selected type the accepted no-transition terminal route is not selected. Its accepting D supplies the required positive determination basis for the one scoped unused-to-used effect. D alone creates no authorization or U and commits nothing. Actual authorization must still bind a real admitted mapping/profile, Q0, the selected four-argument successor relation, all required coordinates and the exact U; current G3 M=0 supplies none of them.

The successful state change remains exactly (a,n,FALSE)->(a,n,TRUE), framed to leave all other keys, membership/history and product state unchanged. New A/E/D identities do not reset (a,n), fork its used state, authorize a second effect, or promote product work into protocol state. This selection fixes one required successful scoped effect; failed attempts and recovery still follow the original exact table. An accepting D is not a liveness promise that every attempted U will commit.

Basis: selected E283 effect; NOTRANS-001/005–008; TRANSAUTH-001–010/014–015; E283 successor relation and S70 COMPARISON/RECOVERY. RF-25 conditional rules remain preserved for their actual antecedents; they are not globally removed.

<a id="recovery"></a>
## AC09 — recovery joins under B

For each governing recovery row with evaluation_required=SAME and determination_required=SAME, preserve the existing A/E/D. Where that row requires a new authorization/new U, create only those separately authorized occurrences; their failure predecessors stay terminal. This is not a new authoritative action presentation merely because a new U is required.

For each row requiring NEW E and NEW-ON-SUCCESSFUL-COMPLETION D, a new authoritative presentation under AC02 establishes a new A and fresh bounded A/R/C inputs before the new E. Preserve all prior A/E/D. If new E fails, it produces no new D, acceptance, authorization or U. If it succeeds, its one D is distinct even where its classification equals an earlier D. Re-evaluation cannot revive the failed U. recovery-occurrence-joins.tsv overlays these consequences on all 21 unchanged rows; it is not a replacement recovery function.

Basis: exact S70 recovery; TSEREEVAL-001-A01/A02/002/003; ACTION-009 plus selected B; EVAL-005/021/026. No recovery event is selected here.

### Incorporated proposal: occurrence-recovery

For every unchanged recovery row requiring SAME E and SAME D, the existing A/E/D MUST be preserved. Where a row requires NEW E, a new authoritative admission MUST establish a new A before that E and a new D MUST arise only on successful completion. Failed U MUST remain terminal. No recovery overlay MUST change the 21-row function or authorize a second consumption of a used key.

<a id="concurrency"></a>
## AC10 — equal submissions and competing determinations

Distinct A1/A2 with equal (n,a,r) may each have an accepting D if each complete E observes a valid unused context before a commitment. The occurrence rule does not serialize those Evaluations or manufacture a winner. Each U still requires independently authenticated current gate evidence. At most one successful atomic unused-to-used effect can consume the same key under the selected source relation; a later coherent used=TRUE establishes material conflict. The comparison/commitment boundary remains indivisible. No actor identity or database/chain transaction mechanism is inferred.

Basis: AC02/06/08, E283 effect/source relation, source-contract SC14–16 and S70 COMPARISON. This is a protocol-semantic consequence, not tested I164 concurrency behavior.

<a id="privacy"></a>
## AC11 — privacy of the occurrence boundary

An action occurrence coordinate distinguishes public protocol occurrences and cannot encode or become a reusable identifier for the Private Actor. Equality of proof/PI/n does not infer actor identity or merge occurrences. Any boundary or retrieval reference must remain within its governing disclosure/custody contract; selection B does not authorize publishing a new A-to-D-to-U trace, request path, source-cut history or acquisition topology. Preserve the full privacy component/composition and actor-graph obligations and the existing bounded TSE output surface.

Basis: ACTION-013/014/016; EVAL-020; DETERM-011; CLASS-012; RF-09–11; S70 PRIVACY. No concrete disclosure universe or independent privacy appointment is asserted.

<a id="closure"></a>
## AC12 — scope of completion

The root-policy, effect and repeated-authoritative-presentation choices are now selected. This completes the documentary occurrence rule and its type/R/C, E/D, no-transition, recovery and concurrency consequences. No additional user policy choice has been identified by these consequences. The exact source authority, canonical external decoder/status/cut/source interface, complete capability applicability, full E acquisition/dependency program, full-profile minimality/privacy and final admission remain distinct unfinished obligations. Their absence is not cured by the occurrence choice or by a local hash. A complete S55 target remains unclaimed.
