# Concrete source-interface contract draft

Local owner E284-DRAFT-INTERFACE-SOURCE. This is proposed source text, not an appointed source, registered mapping or published extension. Interface field ordinals specify documentary argument order; they introduce no RPC, live endpoint, new PE-TSE operator, universal chain or technical identity mechanism. The exact existing expression program remains unchanged; additional pure definitions are in this directory as a separate construction fragment.

<a id="carriers"></a>
## IF01 — value carriers, meaning and authentication

At the existing S70 read boundary, every supplied value is one complete canonical TSEV1 encoding. A source reference consists of its exact source identifier, exact source bytes/digest and adequate owning anchor; a profile-local label alone is not such authority. An identity used as a scope or cut coordinate must have an independently owned meaning and source validation. Wrapping arbitrary text as PE-TSE-ID or bytes does not establish that meaning. No concrete source/scope/cut identifiers are allocated in these drafts.

A source assertion must identify the exact ordered semantic arguments assessed, the exact returned value or bounded assessment, its required authority scope and evidence, and its applicability to the relevant E or gate cut. For compound assessments, every argument/result join must be exact. Matching hashes alone cannot establish source truth. Existing ReadObject fields (object_id, value, source, anchor, evidence_id, evidence, endpoint, independently validated authoritative/valid/authenticated flags) carry the declared value and validation envelope; the flags are never accepted as unchecked caller declarations. Representation/value/status READ occurrences retain their own identities, source/evidence edges and canonical bytes.

These fields can transport a previously source-authenticated fact. They do not specify a new authority-acquisition or signature-verification primitive. Cryptographic appointment, adequate source ownership and live truth remain independently established. Retained S22 section 6 assigns authoritative proof verification to the on-chain surface; no arbitrary signer, backend preflight or browser result is substituted for that retained authority role. The actual realization and source chain remain to be supplied separately under that role.

<a id="scalar"></a>
## IF02 — exact canonical scalar assessment algorithm

The domain constant p is 21888242871839275222246405745257275088548364400416034343698204186575808495617. Given present bytes x, first parse exactly the S70 TSEV1 primitive UINT encoding: the correct magic, exact type identifier, UINT kind octet, declared body length with no extra/truncated bytes, and canonical ASCII decimal body `0` or `[1-9][0-9]*`. Re-encoding must reproduce all bytes. This step establishes a canonical nonnegative UINT, not a scalar.

For a successfully decoded decimal body d, compare its decimal length to the length of p's canonical decimal body. Fewer digits means in-domain; more means out-of-domain. At equal length, unsigned ASCII lexical order below p means in-domain and equality or greater means out-of-domain. This computes exactly 0 <= x < p without modular reduction or numerical precision loss. A malformed encoding has no canonical scalar result. Missing bytes or inability to carry out a required assessment has no completed assessment and cannot be treated as a valid zero or an out-of-domain proof-invalid result.

The canonical-input procedure is supplied as a documentary byte algorithm and reproducible local checker in scalar-assessment.py. Its dictionary labels are local assessment diagnostics, not new protocol failure codes, a first-class result subject or an added wire schema. It is NOT an admitted PE-TSE definition, implicit decoder, host-call operator or replacement for external-source authentication. The PE-TSE language does not have a general decimal parser/range primitive; this proposed source-boundary computation supplies precise semantics without pretending to extend that language. Its competent ownership remains unestablished. Domain-first selection fixes this assessment before authoritative admission; see ../domain-admission-selection.md.

For candidate n,a,r, malformed representation or completed out-of-domain assessment refuses admission before A/E/D under the selected domain-first rule. Inability likewise admits nothing and is not rejection. The decision in domain-boundary-decision.md is resolved. For source-supplied occupied root slots and scoped-state values, the already declared scalar-state domain remains a required validity condition: invalid source state is not converted into a negative root or unused fact.

### Incorporated proposal: admission-domain

Before authoritative admission for this capability, n,a,r MUST each be available in their declared canonical representation and denote a scalar x with 0 <= x < 21888242871839275222246405745257275088548364400416034343698204186575808495617. Malformed representation, completed out-of-domain assessment, or inability to establish that assessment MUST admit no A, begin no E, produce no D, acceptance or rejection. Modular reduction, truncation or a default value MUST NOT substitute for that assessment.

<a id="root"></a>
## IF03 — root-observation assessment

Ordered semantic arguments: exact root-policy reference; exact membership-state scope reference; required observation-cut reference and phase; fixed declared r; introduction occurrences for the newest suffix, newest first; complete-suffix/order evidence; and competent-source authentication evidence. Each introduction carries its own authoritative occurrence identity, valid membership-root value and source-defined position. The typed expression still receives r,s1..s16,o1..o16, not these evidence records as public proof inputs.

Assessment must establish all of the following before complete valid root facts can be consumed: the source is competent for this scope and policy; the cut is applicable and current for the requested phase; every included introduction is a distinct actual valid introduction in that scope; repeated observations are not counted twice; separately introduced equal values are not collapsed; the prefix is complete/newest and no omitted newer introduction belongs in the suffix; each occupied value is in the scalar domain and is a valid introduced membership root; occupancy matches the authoritative length up to 16; unoccupied payloads are zero; there is no sentinel privilege. Initial roots count only if introduced.

The pure ROOT-COMPLETE-SHAPE definition constructed here checks TRUE/FALSE occupancy, prefix shape and absent zero payloads using the existing expression grammar. It does not prove introduction validity, order, completeness, freshness, source authority or scalar range. On incomplete/malformed source facts a shape check must not be used as a false root-acceptance result. Once the whole assessment is valid, the existing 33-argument ROOT-ACCEPTED function supplies v. Current true-to-true history changes remain gate-immaterial but remain actual read/evidence changes for recovery.

The current cut is a boundary fact, not necessarily a wall clock or a block number. Its source-owned ordering/currentness relation must be supplied exactly before admission. Matching a new cut to an old authorization cut by byte equality is not required for root eligibility; asserting the old cut is current is not permitted either. Do not freeze root history merely to make unchanged-D easy.

### Incorporated proposal: adapter-history

Root production MUST establish valid introduction identities, authoritative order/count, complete newest suffix, scalar domain, occupancy and exact scope/policy/cut/r binding. Occupied positions MUST be h,h-1,...,h-min(16,h)+1 with source-owned nonempty occurrence identities; absent positions/values MUST be zero and absent identity bytes empty. Shape equality MUST NOT establish validity, authority or currentness.

<a id="state"></a>
## IF04 — scoped-state assessment

Ordered semantic arguments: exact uniqueness-state source/scope reference; required coherent cut/phase; fixed a; fixed n; observed used state; complete-state and source-authentication evidence. The state is exactly tuple(a,n,FALSE) or tuple(a,n,TRUE), with a,n in the retained scalar domain. Source/current key bindings must match the fixed occurrence context. A missing entry is not unused unless the competent complete-state rule independently establishes that meaning. Unknown, unreadable or unauthenticated state is neither valid FALSE nor a newly defined third participation state.

The E283 source/successor constructor and relation signatures remain unchanged. Constructors do not create authenticated state. The selected frame still forbids writing membership/history, other keys or product state. Current used=TRUE can be a sufficient gate conflict only when the exact key/current fact is independently authentic and all preceding validation requirements have passed. Missing unrelated predicate information does not remove a sufficient authentic conflict; failed authentication is still earlier indeterminate.

### Incorporated proposal: adapter-state

State production MUST establish canonical a,n, exact scope/key, complete FALSE/TRUE state, coherent cut/phase and competent evidence. A missing record MUST mean unused only if a competent complete-state rule establishes that interpretation. Constructor equality MUST NOT authenticate state or authorize the effect.

<a id="proof"></a>
## IF05 — proof and artifact assessment

Ordered semantic arguments: exact bounded proof identity and bytes; exact public inputs in n,a,r order; exact owning proof-relation/domain/schema reference; exact compatible verifier/key/artifact and provenance references; bounded verification occurrence and required protocol-relevant context; and authoritative verification/source evidence. Every consumed representation/reference/provenance/status or protocol-state fact is an actual dependency when used. Private memberSecret, leaf and path remain proof-construction witnesses, not new public inputs or TSE components.

A completed verifier result is exactly proof-valid or proof-invalid under that same relation and those same inputs. Inability to complete is separate. A provider's FALSE return, contract revert or precompile failure is not by itself a correct proof-invalid classification; its exact source-owned interpretation and artifact correspondence must establish what occurred. Root acceptedness and current unused status still require separate checks. No profile Boolean may hide an unrecorded verifier call, alternate public input, changed artifact, actor-derived data or unresolved source authority.

The current PE-TSE grammar cannot execute Groth16, Poseidon, arbitrary cryptographic verification or an external call. An independently source-authenticated verification result may be a declared read fact under S70; that is not the same as inventing an executable PE-TSE verifier function. Complete capability-program closure must expose the exact contributing proof/PI/artifact/source facts and all actual acquisition/verification dependencies under the governing boundary, instead of declaring a result Boolean to be the whole computation.

<a id="status"></a>
## IF06 — status conditions

For each actual root/state/proof/input-assessment interface, AUTHORITATIVE denotes independently established competence for the exact meaning/scope. AVAILABLE denotes possession of the required bounded input/result material at the applicable boundary. VALID denotes the source-defined shape/domain/context/coherence and completeness conditions for that interface, not merely parse success. AUTHENTICATED denotes exact assertion/evidence validation under the competent source chain. These are separate facts and separate status reads when declared by the program.

The existing BOOL3->BOOL3 stage functions propagate these independently validated statuses. They neither authenticate a signer nor decide source competence. A status FALSE or UNRESOLVED does not license normalizing arbitrary input into a trusted Boolean. Component PROJECT retains S70's exact status-first execution and value/normalization equality. Gate comparison retains validation-first and independently sufficient MC; complete E instead requires coherent completion of every assigned rule before D.

<a id="dependency"></a>
## IF07 — full acquisition and dependency closure

Every consumed interface input, source assertion, representation conversion, status, proof/reference/artifact value, relevant scope/cut/currentness fact, call argument and result must belong to the actual E dependency basis at its correct boundary. The E root's read inventory must enumerate actual required inputs; it cannot use one all-other-rules Boolean, a whole snapshot, or a digest as a substitute for a missing semantic decomposition.

Pure expression reads/calls use the existing admitted operation templates and exact argument bundles. Independently established source evidence remains explicit source/authentication nodes and exact bytes. Work done outside the expression interpreter does not disappear: its owning interface must state how all actual contributing source/operation/input dependencies are represented and validated. No transcript schema extension, arbitrary host call or recursive provider graph import is silently introduced by this draft.

All actual executed branches and repeated READ occurrences remain; unexecuted declared operations do not create occurrence nodes. A complete success package must be byte-replayable under the governing constructor. Full fresh unchanged-D sufficiency ranges over its entire actual least closure, not just the comparison projection or final component results. The 21 recovery rows and failed-U terminality remain unchanged.

<a id="privacy"></a>
## IF08 — evidence scope and disclosure

Independent source-interface adequacy/ownership and full two-context component/composition privacy analysis precede admission. Current occurrence truth, full owning records, histories and fresh maps belong at use. Source proofs, acquisition paths, ordering/cut coordinates and verification evidence do not become public merely because the public inputs include n,a,r. All additional source/interface surfaces must be included in the complete privacy universe and actor graph; an existing 57-field local template is not proof that external interface surfaces are complete.

This contract supplies exact semantic assessment duties and an executable scalar byte procedure plus pure finite expression definitions. It does not appoint a source, authenticate absent facts, define a concrete authority mechanism, reopen the selected admission-domain choice or claim a full admitted capability program.

# Complete-result aggregation source draft

Local owner: E284-DRAFT-INTERFACE-SOURCE, anchor completion. This section is also included in the exact registered local source-interface-contract.md; it is not an authenticated successor source. No complete E is asserted by a Boolean fold.

<a id="completion"></a>
## Exact finite aggregation

The fragment has five ordered BOOL3 result inputs: (1) assigned action/public-input validity, (2) proof/public-input/domain/artifact coherence, (3) complete proof-verification result, (4) root acceptedness, (5) scoped unused eligibility. FALSE means a completed, validly established negative for that assigned rule; TRUE means a completed positive; UNRESOLVED means that required assigned result is not complete. These are separate declared channels, not a wildcard “other rules” result. The actual complete R must justify the channel assignments and add explicit channels/definitions for any additional required independent result before this can become a whole-E program.

BOOL-RESOLVED(x)=NOT EQUAL(x,UNRESOLVED). FIVE-RESOLVED evaluates that for every input. FIVE-SATISFIED is AND of the five results. FIVE-COMPLETE-CLASSIFIER returns UNRESOLVED whenever any input is unresolved; otherwise TRUE iff all five are TRUE and FALSE otherwise. The exact expression uses only existing literal, equal, not, and, or, arg and apply. No conditional operator or new result type is introduced. Source-type non-values and validation failures must still obey the governing precondition/input validation; they cannot be forged as completed FALSE.

The construction is the explicit expression OR(AND(allResolved,allSatisfied),AND(NOT(allResolved),UNRESOLVED)). It prevents the concrete error AND(FALSE,UNRESOLVED,...)=FALSE from being represented as a rejecting D. S70 Evaluation.run can produce a completion package from a resolved Boolean; therefore the complete-R root must propagate unresolved required input instead of relying on ordinary short-circuit AND as a completeness test.

A root with these five explicit input fields reads each declared field at entry under the existing constructor. This preserves every supplied result READ even where the pure fold short-circuits. It does not prove that the source computations, rule assignments, proof artifacts, raw root/state reads or external acquisition dependencies producing those results are complete. fields.tsv and operations.tsv in this directory expose this narrow executable fragment; they are not the complete-E acquisition program and must not replace the existing comparison/profile records.

The gate-comparison procedure is different. An independently sufficient authenticated MC can remain decisive despite unrelated unresolved predicate input once earlier validation passes. The new E completion guard does not replace or weaken that rule, alter the nine-case v/b table, or change recovery.

The finite case table exhausts all 3^5=243 result vectors. It validates this aggregation function only, not authoritative inputs, privacy, full R, full program admission or an actual E/D occurrence.

### Incorporated proposal: complete-e

Every assigned required result MUST complete coherently before E produces D. One known negative MUST NOT mask another required unresolved result. Once complete, acceptance MUST require all applicable rules satisfied; otherwise the complete result is rejection. Successful completion and exactly one D MUST occur at the same semantic boundary; inability of a begun E to achieve it MUST terminate as incomplete Evaluation failure with no D.
