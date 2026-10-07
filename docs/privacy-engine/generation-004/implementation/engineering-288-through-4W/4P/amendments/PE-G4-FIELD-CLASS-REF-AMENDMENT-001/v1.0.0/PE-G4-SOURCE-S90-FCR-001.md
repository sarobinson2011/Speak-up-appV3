# PE-G4-SOURCE-S90-FCR-001 version 1.0.0 — authorized FIELD-CLASS-REF consolidation

# PE-G4-FIELD-CLASS-REF-AMENDMENT-001 version 1.0.0

Authority: explicit user approval, AUTHORITY.json SHA-256 5a33a07373db842ed9efc898cf682407d2032175eb7d2c9cb645ad5c6f24cd63.
This is a narrow compatibility amendment to the preserved Engineering[287]/S90 baseline, not evidence of source or mechanism qualification or protocol publication.

FIELD-LABEL.surface_id has type FIELD-CLASS-REF. Its representation is the unchanged canonical JSON string containing the exact case-sensitive field-class name. Its spelling is either an existing ID or an existing ID immediately followed by `.$record`. Its value MUST be an exact member of the complete source-owned surface register bound to the model. Occurrence-qualified token IDs, aliases, names absent from that register and all other dollar spellings are invalid. Canonical JSON retains its accepted serialization; alternate byte encodings are not introduced.

This type applies solely to FIELD-LABEL.surface_id. General ID and OBLIGATION grammar are unchanged. Owner, coalition, visibility, complete field-class coverage and UNKNOWN rules remain unchanged. A supplied register is an input to local membership checks; only the independent source/model correspondence and qualification rules establish its authority and completeness. Missing register context cannot establish validity and must fail through INCOMPLETE-EVIDENCE-UNIVERSE at admission. Malformed spelling remains a schema failure; a well-spelled absent member is an incomplete-universe failure.

Revised normative schema/grammar/contract are the companion files. PE-G4-SOURCE-S90-FCR-001.md consolidates the preserved S90 text with this exact amendment; its source identifier is PE-G4-SOURCE-S90-FCR-001, version 1.0.0. BINDING.json pins all revised and reused normative bytes. Historical accepted/ and predecessor ZIPs remain immutable. Dependent source/procedure, finite contract, provenance, profile, invocation, evidence and signature bindings must be regenerated or verified unchanged; no prior receipt silently migrates.

Exact affected baseline clauses: security-fields.tsv data row 83 (file line 84), S90 line 890; v4_record_grammar.py ID lines 57–59; ACCEPTANCE-CONTRACT lines 385–390 (S90 451–456) and 615 onward (S90 681 onward). Earlier OBLIGATION edge-reference compatibility is unaffected and does not replace FIELD-LABEL references or prove duty coverage.


## Preserved S90 body with the three explicit replacements above

# PE-G4-SOURCE-S90 — privacy acceptance and qualification contract

Unpublished author construction under existing relation-aware authorization. This source completes S89 R2/R4/R5/R7 by specifying a source-qualified security-assessment contract. It preserves S03–S89 bytes and explicitly governs the selected candidate after them. No new actor, proof input, host-call primitive, public trace or linkage exception is introduced.

<a id="contract"></a>
## contract

The selected G4 privacy admission procedure MUST apply the exact acceptance contract below, including exact and computational obligation dispositions, without relaxing established linkage, actor or unknown-evidence failures.

<a id="policy"></a>
## policy

Security policy parameters MUST come from independently governing source-qualified policy bytes; the profile issuer, privacy signer and implementer MUST NOT select defaults or appoint the parameter authority.

<a id="experiments"></a>
## experiments

Collision, cross-action tracking and actor-information experiments MUST retain their distinct meanings, complete observer views, approved leakage and declared adversary/envelope scope.

<a id="qualification"></a>
## qualification

An argument assessment MUST bind exact policy, source, certificate, grammar, checker, experiment, artifact and premise material under the independently qualified source interface; VALID, INVALID and UNAVAILABLE MUST remain distinct.

<a id="composition"></a>
## composition

Complete whole-view coverage and exact rational composition/budget checks MUST precede computational discharge; collision resistance alone MUST NOT discharge tracking or actor-information obligations.

<a id="decision"></a>
## decision

Admission MUST collect all inherited failures in existing ORDER and accept only when every governing exact/computational obligation and independent source/evidence prerequisite is established.

<a id="schemas"></a>
## schemas

Every new policy, argument, assessor, artifact, observer, invocation and applicability field MUST follow the exact owning schema register and be included in dependency/visibility analysis; opaque evidence MUST NOT conceal omitted surfaces.

<a id="instantiation"></a>
## instantiation

The full privacy model MUST expand every source-established record directory in both symbolic contexts, retaining inherited nodes/edges and all new custody and potential equality edges; a schema template MUST NOT be represented as an instantiated universe.

<a id="applicability"></a>
## applicability

The selected mapping MUST establish security-policy envelope applicability before admission and at each applicable source-validation boundary; a demonstrated additional changing material condition MUST block this two-component profile until explicitly integrated.

<a id="recovery"></a>
## recovery

Security-policy and applicability evidence consumed by an occurrence MUST be included in full actual Dep(D), replay and fresh-map checks; fixed coordinates MUST NOT replace that evidence closure.

<a id="representation"></a>
## representation

For S90 the V4 definition declaration and final-member grammar below MUST supersede S89 V3 selection; no uninstantiated definition declaration or absent policy/appointment MUST be materialized as governing PRIVACY.

<a id="boundary"></a>
## boundary

A completed author definition, exact serialization or mechanically checked budget MUST NOT be represented as independent acceptance, qualified cryptographic evidence, profile admission or execution permission.

## Exact owning acceptance contract

G4 PRIVACY ACCEPTANCE CONTRACT — CONCRETE COMPLETION PROPOSAL
1 October 2026

Status: integrated author construction in candidate source S90 under the
authorized S89 redesign. S90 supplies the V4 final-member grammar; no concrete
V4 governing profile is instantiated. No appointment,
profile admission, publication or implementation adoption is asserted.
This document closes the proposed contract structure, not independent acceptance
of that proposal or evidence that a particular cryptographic construction meets it.

1. Fixed completion criterion

An implementation must be able to determine which evidence is required, how it
is validated, which failures take precedence, and what success means, without
choosing privacy policy itself. No successful construction test is admission.
A parameterized source policy is legitimate only when the parameter authority,
meaning, validation and absence behavior are specified. A blank parameter may
not be filled by the profile issuer or the software implementer.

2. Two kinds of privacy obligation

The complete regenerated graph remains the obligation universe. Its structural,
source-established and potential equality edges remain recorded with exact
provenance. Symbols such as ARBITRARY never establish observed equality.

A. Exact obligations: source ownership, declaration/record joins, exposure,
coalition/visibility completeness, source-established linkage, canonical
encoding, protected actor information, and actual observed counterexamples.
These are resolved by exact evidence validation and inherited S83–S87 rules.
A computational bound cannot excuse an established violation or unknown fact.

B. Computational obligations: a potential graph path whose realization or
information gain is claimed computationally bounded under an explicitly
identified relation and security experiment. No such claim is discharged merely
because an edge has a hash label or distinct action inputs.

Every obligation must receive one disposition: EXACT-SATISFIED,
EXACT-VIOLATION, COMPUTATIONALLY-BOUNDED or NOT-ESTABLISHED. No obligation is
silently dropped. Whole-view obligations must cover paths and interactions, not
only a list of individual equality edges.

3. Governing security policy — external, source-owned, immutable

A selected profile must reference a policy by exact identity, digest and owning
source anchor. The competent policy source must be independently established
under the inherited source rules. The privacy signer and profile issuer cannot
appoint this source or choose its contents.

The policy must specify all of the following, with no empty/default cells:
(a) The protected actor variables, required coalitions and exact observation
    channels. The set must include every inherited protected actor and every
    required observer view; it cannot omit a known disclosure to obtain a PASS.
(b) The authorized public leakage: exactly the approved scoped root, action and
    same-(a,n) duplicate relationships, plus otherwise already authorized public
    outcomes. No other exception may be inferred from a security experiment.
(c) Adversary resources and capabilities: computation model, resource bounds,
    adaptive action selection, concurrency, retries, corruption/auxiliary
    knowledge and any oracle queries. Classical/quantum capabilities must be
    stated explicitly. An excluded capability limits the claim; it must not
    silently remove a coalition required by the source model.
(d) The allowed operating envelope: number of relevant occurrences, comparisons,
    attempts, queries and participants; time/deployment scope where applicable.
    Unbounded activity cannot borrow a finite-envelope bound.
(e) Exact secret-generation and state-distribution assumptions; exact algorithm,
    field, parameter set, encodings, domain constants and relation identities.
(f) Maximum acceptable rational probability/advantage bounds for collision,
    cross-action tracking and actor-information experiments. Numerators and
    positive denominators denote exact fractions in [0,1]; no floating-point
    rounding, generic security-bits label or implicit 1/p bound is sufficient.
(g) The approved assumption set, with exact statements, scope, evidence and
    qualification rule for each. A name such as Poseidon-secure is insufficient.
(h) The qualified argument-assessment mechanism: accepted certificate grammar,
    checking procedure and exact semantic version/digest, trust basis, required
    competence/soundness evidence, and explicit inability behavior.
(i) The composition method and overall budget allocation for all claims and
    observer views, including repeated attempts and lifetime comparisons.

The contract deliberately sets no numerical default. Numerical choices are
protocol parameters supplied by the independently governing policy, not choices
made by implementation code. Until such a policy is established, this selected
candidate cannot obtain computational admission. This does not prevent building
an implementation that reads and enforces the contract.

4. Security claims and their meaning

COLLISION: probability that an adversary within the declared envelope produces
two distinct, canonically encoded, relation-valid input tuples with equal outputs
of the exact nullifier hash. The S89 conditional derivation is a transfer lemma
for this claim. Accepted-proof relation enforcement and soundness are separate
premises and must have their own established bounds or exact justification.

CROSS-ACTION-TRACKING: distinguishing advantage between two source-specified
experiments whose protected actor associations differ across distinct actions
but whose approved public leakage, schedule and permitted auxiliary knowledge
are identical. Each experiment must specify the secret/state sampling and full
coalition view. Advantage is the absolute difference of the probabilities that
the declared adversary outputs one in the two experiments. Missing experiments,
unequal permitted leakage or an incomplete view mean NOT-ESTABLISHED.

ACTOR-INFORMATION: the analogous distinguishing claim for each protected actor
association/attribute, preserving the authorized disclosures. Direct disclosure
of a protected value or a demonstrated reconstruction path is EXACT-VIOLATION,
not an advantage that can be accepted by allocating a larger budget.

These experiments must be provided as exact source-owned definitions and bound
to the concrete producer model. There is no universal substitution of tracking
for collision, or pairwise privacy for coalition privacy. The collision lemma
does not prove either information claim.

5. Admissible security argument

For every computational obligation the argument must identify:
- the exact regenerated obligation IDs and whole-view scope it covers;
- policy/model/source/relation/algorithm/artifact digests;
- the precise experiment and all premises;
- explicit assumption references from the governing policy;
- the complete reduction/certificate and its required artifacts;
- an exact rational bound and its envelope/resource applicability;
- the independently qualified assessment mechanism and its returned evidence.

The source-owned assessor must validate the mathematical/cryptographic argument
under its specified soundness/competence contract. Its evidence must distinguish
completed VALID, completed INVALID and UNAVAILABLE, for these exact inputs.
Its result is a source fact only after independent source and assertion binding;
a caller flag or an unappointed signature cannot establish it.

Signature authentication, byte equality and digest integrity are necessary
binding checks, not argument validity. The existing six-step S89 kernel accepts
only its conditional collision derivation. It cannot be reused as a verifier of
Poseidon security, proof soundness, unlinkability or arbitrary certificates.

Unsupported grammar, missing evaluator qualification, an unapproved assumption,
unproved reduction premise, incompatible envelope or incomplete artifact
correspondence produces NOT-ESTABLISHED. A completed invalid assessment produces
EXACT-VIOLATION for the claimed evidence; neither result permits admission.

This is a source-qualified argument-assessment interface. A general automated
cryptographic theorem prover is not a protocol prerequisite. A realization may
use a formal proof checker or a source-qualified assessment process only if its
exact evidence, competence and assertion semantics satisfy the above contract.
Neither mechanism is appointed by this proposal.

6. Composition and budget checks

Every required observer view and every protected target must be covered. Coverage
is regenerated from the complete model, not supplied by an issuer completion bit.
A proof may cover a whole experiment jointly. Otherwise a source-established
composition argument must join the component claims and their interactions.

For a UNION composition, use the exact sum of the rational failure bounds, capped
at one. UNION does not require independence. A tighter bound, a product bound,
or a conversion between different experiments requires its own validated
argument. Repetition counts must be within the policy envelope; each applicable
term must occur with its correct multiplicity. Do not double-count a term merely
to invent a failure, or omit shared/adaptive interactions to claim success.

For each policy experiment, the composed bound must be at most its specified
maximum. A checked bound exceeding that maximum is a policy failure. Unknown
terms, an unsupported composition theorem or inability to regenerate exact
coverage are NOT-ESTABLISHED. A budget PASS is conditional on all its validated
premises; it is not mathematical injectivity or unconditional anonymity.

7. Ordered acceptance decision

The proposed integrated validator must:
(1) Independently regenerate source/body/program/privacy declarations and verify
    the exact outer bytes and source-policy bindings.
(2) Collect all inherited authority, signature, object digest, component,
    schema, source scope, visibility, universe and owning-record failures.
    A later incomplete security argument cannot mask earlier bad authentication.
(3) Establish the security policy and argument-assessor competence from independent
    source evidence, not from issuer data, the privacy signer, or key equality.
(4) Regenerate the entire graph and exact/computational obligation ledger.
(5) Reject established protected linkages/counterexamples under retained S83–S87.
(6) Validate every argument, premise, scope, certificate and artifact binding;
    validate whole-view coverage and composition; compare exact bounds to policy.
(7) Accept only if every required obligation is established and every inherited
    gate passes. Emit the exact admitted profile/policy/assumption bindings.

The inherited ORDER remains controlling. Model/certificate shape inconsistencies
map to INVALID-PROFILE-SCHEMA; unestablished policy/assessor authority to
INVALID-EVIDENCE-AUTHORITY; missing objects to MISSING-EVIDENCE; signature/digest
failures keep their existing codes; scope/experiment binding failures map to
INVALID-ACTION-CONTEXT; incomplete universe, unsupported/unavailable arguments
or missing premises map to INCOMPLETE-EVIDENCE-UNIVERSE. Established violations
and exceeded bounds map to UNIQUENESS-FAILURE, CORRELATION-FAILURE or
ACTOR-RECONSTRUCTION-RISK according to the protected experiment. A generic
collision argument cannot clear an unrelated failure. No new protocol outcome
subject, proof input or public source trace is introduced.

Externally the existing failure vocabulary remains. Internal evidence retains
whether rejection came from an established violation or inability to establish
admission. Success explicitly means acceptance under the bound governing policy
and its established assumptions. It does not itself authorize an E, D, U,
publication, registry insertion or state transition.

8. Canonical integration requirements

The immutable privacy member must bind the contract version, complete security
policy reference, experiments, allowed assumption references, declared operating
envelope, qualification-mechanism references, complete obligation ledger and
composition/budget rules. Actual occurrence records and admission evidence stay
outside it and sign its final digest with the inherited V2 preimages.

Additional policy/assessment/evidence fields require explicit observer/custody
registration and graph provenance before a complete successor member is claimed.
They cannot be hidden inside an opaque carrier or treated as non-observable by
fiat. Conditional constants and source-derived facts retain their exact scope.
A change to the policy or assumptions changes the bound immutable profile;
it cannot be made by mutating an admitted profile or regenerating signatures.

9. Definition completion versus admission completion

The acceptance contract can be defined without choosing a deployed chain,
provider, signer or concrete Poseidon implementation. A specific selected
profile cannot be admitted without the required exact parameter, source,
assessor, observer, artifact and evidence bindings. Future use-phase observations
are separate and are not prerequisites to defining this static contract.

The source and schema/member-grammar integration is included in this review
candidate. Independent semantic review and actual profile instantiation remain
required. Current relation_admission.py is rejection-only and must not be
called a completed implementation of sections 3–7. No source or profile bytes
are changed by writing this proposal. The closure assessment below identifies
the remaining definition obligations rather than declaring them satisfied.


ENGINEERING[287] S90 CORRECTION — AUTHORIZED AUTHOR CONSTRUCTION

This correction is within the existing construction authorization. It clarifies
S90 #experiments, #qualification, #schemas, #instantiation, #representation and
#decision under CAP-101/102/104/105/106/109. It appoints no source, changes no
S03–S89 byte or prior requirement, and creates no governing member. The separate
NONVACUITY-CONTRACT.txt enacts Steve's approved option A and controls that decision.

1. Canonical record placement; no self digest

The following rules supersede the ambiguous S90 final-member paragraph wherever
that paragraph leaves nested record placement unspecified. The 14 outer keys
and 11 security_contract keys remain exactly those listed by S90. Canonical JSON
is the S88 sorted-key, ASCII-escaped compact encoding followed by one LF;
duplicate object keys, floats/nonfinite numbers and noncanonical input fail.
Primitive and record shapes are exactly v4_record_grammar.py below. Source
semantics/qualification are additional checks, never consequences of shape.

security_contract.policy is exactly {record, algorithms, artifacts, observers,
field_labels}: one POLICY record and arrays of ALGORITHM, ARTIFACT, OBSERVER and
FIELD-LABEL records respectively. The POLICY.policy_digest equals SHA256 of the
independently governing material bytes named by POLICY.policy_source.material_sha256.
It is NOT a digest of the containing POLICY record or profile. approved_by_source
is independent approval material for those exact governing bytes, not a key or
a claim of this serializer. Governing policy bytes must exist before construction.

security_contract.experiments, assumptions and qualification_contracts contain
EXPERIMENT, ASSUMPTION and QUALIFICATION record arrays respectively.
operating_envelope and leakage are the sole ENVELOPE and LEAKAGE records.
All record arrays are in increasing ASCII byte order of their schema identity
field, with no duplicate identity. Ordered semantic sequences inside a record
retain their specified order; predecessor/term order is not inferred from ID
sort order. Empty applicable directories remain prohibited by source validation.

security_contract.obligations contains the complete STATIC obligation TEMPLATE
directory. Each record has exactly obligation_id, kind, target_ids, coalition_id,
node_ids, edge_ids, experiment_id. The full OBLIGATION evidence record additionally
has profile_digest, model_digest, disposition, argument_ids, exact_evidence_refs.
Those five fields are EXTERNAL validation evidence and MUST NOT occur in the
immutable obligation template. They retain their registered types and full
observer/custody duties. EXACT experiment_id is JSON null, with no computational
substitution; COMPUTATIONAL experiment_id must resolve exactly.

security_contract.composition_rules is exactly {directory_id, records}.
directory_id is POLICY.composition_id: it identifies the complete rules DIRECTORY,
not one COMPOSITION record. Every records element has exactly composition_id,
policy_id, experiment_id, method, theorem_ref, qualification_id. External full
COMPOSITION evidence supplies argument_ids, aligned multiplicities and
composed_bound after validating the actual arguments. No result, invocation,
certificate, signature, admission disposition or final profile digest is embedded
in an immutable rule template. Each required experiment has exactly one rule,
and every rule's experiment and policy join must resolve; orphan rules fail.
For UNION, theorem_ref is null and the exact sum law already owned by S90 applies.
For SOURCE-QUALIFIED-THEOREM it is a qualified SOURCE-REF. Null does not establish
the remaining premises. qualification_id still binds the competent assessment
contract for the evidence and coverage premises.

ARGUMENT, ASSESSMENT, ASSESSOR-EVENT and POLICY-APPLICABILITY instances, full
OBLIGATION and COMPOSITION result instances, and their actual source/certificate
material are external. They are bound to the completed outer profile digest.
Static privacy model tokens for these schemas are symbolic fields/classes, never
concrete future record values or a hash of the member into itself. The static
template ledger is an inventory of required duties; it asserts no discharge.

contract_sha256 binds the complete corrected ACCEPTANCE-CONTRACT.txt.
schema_sha256 binds exact security-fields.tsv bytes (the 156 semantic fields).
qualification_interface_sha256 binds qualification-interface.tsv. The additional
framing-register and grammar digests MUST also be included in procedures_sha256
and declaration_input_sha256 at their exact relative paths. format_source remains
S90 and format_source_sha256 binds the full corrected source. These source hashes
are computed after authoring the source, before constructing a future profile;
no literal S90 self digest is written into the source.

All inherited S88 outer fields retain their meaning; policy_sources appends S89
then S90 to the four prior identifiers. Rebuilt model has exactly surfaces,
relations, tokens, structural_edges, equality_stream, actor_graph_policy. Surfaces
use the inherited augmented-node columns; relations use augmented-edge columns;
token/edge/equality layouts follow the retained expansion. Additional fields and
parser surfaces extend these same typed arrays and MUST NOT be an opaque side
graph. Static token indexes are contiguous and all edge references must resolve.

2. Exact external availability representation

The canonical external security-record object is exactly
{format, profile_digest, phase, records}, with format PE-G4-SECURITY-RECORDS-V4,
the final OUTER profile digest, and phase STATIC-ADMISSION/E/PRE-EXECUTION/
PRE-COMMITMENT. records is an object containing all 16 registered schema names.
Each value is exactly {status, justification, instances}. status is PRESENT,
UNAVAILABLE or INAPPLICABLE. PRESENT has a nonempty canonical record array;
the other statuses have an empty array. INAPPLICABLE requires an independently
validated source-reference justification; an issuer cannot switch off a required
experiment, coalition, target, argument or view. UNAVAILABLE always prevents
discharge of the required duty. Its justification may itself be unavailable
(null); such absence establishes no qualified inability assertion.

A completed assessor invocation may produce a PRESENT ASSESSMENT record with
complete_result UNAVAILABLE or INVALID. In either case validated_bound is null;
VALID requires a RATIONAL validated_bound. Result presence is distinct from
VALIDITY. Invalid or unavailable evidence supplies no usable numerical term.
ASSESSOR-EVENT input_bytes/output_bytes may be null only if the independently
qualified event grammar establishes that field is inapplicable at that event;
required-but-missing data makes source/evidence completeness fail. Empty byte
string is present data, distinct from null. No serializer fabricates a bound,
call result, error or cache hit. All other registered fields are present and
typed, except the expressly defined UNION/EXACT null cases above.

The old producer-evidence V2 carrier has a fixed old directory and MUST NOT be
used to claim it encodes these new records. This external canonical object is
source material accompanying the inherited four-file V2 evidence bundles, not
a fifth signed-envelope file or fourth immutable member. Exact bytes must be
supplied and parsed before independently regenerating evidence.tsv/tokens.tsv/
links.tsv. For a security field, token_sha256 is SHA256 of canonical JSON of its
typed value (including its one LF). BYTES fields therefore hash their canonical
hex representation; referenced ARTIFACT.digest separately hashes the decoded
exact artifact octets. The record-token digest hashes its complete canonical
record. Frame/status/presence tokens hash the corresponding typed canonical
value. Every security object field and all exact record/source/parser/visibility
links enter the same signed token/link universe. The V2 domains, headers, object
digest preimage, required three scopes and final-profile joins remain unchanged.
Auxiliary object availability and source authentication are mandatory; having a
matching token digest without the required exact bytes is MISSING-EVIDENCE.

Do not hide the object wrapper, array/directory cardinalities, null tags, status,
phase or justification metadata. security-framing-fields.tsv is the explicit
register of those additional field classes and framing-custody.tsv retains all
seven possible custody roles as UNKNOWN until independently resolved. Its
presence classes expand once per corresponding record field, including a null
field; its per-schema classes expand once per schema directory. The existing
156 semantic fields and their original 1,092 custody cells remain preserved.
Static owning-record class nodes, complete record bytes and source-established
parser subfields still participate in the complete graph and actor analysis.
No framing value is automatically public or eligible for the constant exception.

3. Static universe and actual occurrence universe

At STATIC admission, the independently qualified governing source/model parser
must supply a finite COMPLETE symbolic directory for every applicable field,
record class, event, artifact parser output and old/new producer surface within
the declared operating envelope. It may be a qualified bounded symbolic
representation of all repetition counts/branches; it is never a representative
sample directory or the first invocation trace. Model completeness, coverage and
the exact symbolic multiplicity/guard semantics are independently checked under
the bound source procedure. If that representation cannot be qualified or its
scope is unbounded/unknown, admission fails. No universal compiler or graph
minimizer is implied by this interface.

This duty includes ALL inherited record classes, not just the new security ones:
ReadObject acquisitions, callbacks, retries, failures, diagnostics, cache/history,
transport, verifier calls, observer auxiliary knowledge and all source-established
and actor paths. A repeated owning record remains distinct. Full inherited
field/class/custody/source edges remain; each required directory is expanded in
both distinct symbolic U contexts. No successful fixture fixes multiplicity.
The full potential-equality rule remains left.arbitrary OR right.arbitrary OR
equal symbolic_digest, including old/new and arbitrary/constant pairs. All
structural and equality edges remain in actor reachability. Proven absent paths
need exact source evidence; no constant or permission pruning of the actor graph.

FIELD-LABEL.surface_id identifies a FIELD CLASS in the finite complete surface
register, including framing fields and FIELD-LABEL's own field classes. It does
not create another surface class for each label record or demand infinitely many
labels of labels. Each expanded occurrence inherits its field-class label only
after qualified owner/coalition/visibility validation. Different visibility needs
separate source-qualified classes; UNKNOWN never defaults to CONFIDENTIAL.

During E, either gate and recovery, exact ACTUAL record/event directories replace
symbolic multiplicities only for occurrence evidence. They must belong to the
admitted model's qualified class/envelope coverage and bind all owning header,
phase/attempt/history and full dependency/replay/fresh-map joins. Unexpected
record classes, unmodeled source callbacks or an exceeded scope reject use; the
software cannot extend immutable profile bytes in place. Additional accounting,
material predicates, ordering, coordinates or state effects still require explicit
profile revision and block this two-component candidate in the meantime.

4. Quantification and independent qualification

The security bound is required uniformly for EVERY adversary in the source-owned
declared capability/resource class, with all allowed adaptive schedules, choices,
queries, corruptions, auxiliaries and coalitions. A proof about a chosen benign
adversary returning a constant is not a bound on that class. The two information
experiments must actually differ in each claimed protected association/attribute;
identical worlds or an omitted required target do not discharge that claim. A
whole-view coverage checker must establish all required alternatives, paths and
interactions. Conditioning away an observed disclosure is prohibited. The
collision claim retains its separate relation-valid ordered-tuple meaning.

Source/policy/assessor authority and competence must be established outside the
profile's own claims. An assessment cannot be its own sole competence evidence;
a cyclic chain with no independently established governing basis fails authority
validation. Trust anchors are external source facts under the inherited source
rules, not a new protocol-selected person/key/organization. A valid signature
only authenticates an assertion. Qualification must establish its exact semantic
checking behavior/scope/soundness and approval, with required evidence available.

Approved assumptions remain explicit conditional hypotheses. They cannot be
promoted to proven algorithm facts, used as proof of source competence, or used
to replace required evidence of an argument/premise. If the argument merely
assumes its very target conclusion, it discharges no independent security
obligation; that is circular reasoning. An independently approved primitive
assumption is permitted only with an established reduction/correspondence and
explicit conditional claim. No protocol default for numerical strength is added
by this clarification. The separately approved NONVACUITY-CONTRACT.txt imposes
maximum < 1 and meaningful scope; it sets no numerical default.

5. Failure collection and composition disambiguation

The inherited ORDER is unchanged. All independently detectable failures are
collected; malformed/unavailable later data cannot mask earlier authentication.
An unavailable parser result cannot be used to fabricate further factual errors.
Malformed shape/null tags/template placement: INVALID-PROFILE-SCHEMA.
Wrong supplied profile digest: PROFILE-DIGEST-MISMATCH.
Unestablished independent authority/competence: INVALID-EVIDENCE-AUTHORITY.
Missing required exact object bytes: MISSING-EVIDENCE.
Signature/object digest failures: their unchanged authentication/digest codes.
Unknown/invalid declared visibility: INVALID-SURFACE-LABELS; missing complete
qualified observer view also contributes INCOMPLETE-EVIDENCE-UNIVERSE.
Established context/experiment/envelope mismatch: INVALID-ACTION-CONTEXT.
Unavailable/unsupported argument, scope that cannot be established, incomplete
whole-view/directory/ledger or missing premise: INCOMPLETE-EVIDENCE-UNIVERSE.
An established exceeded budget or completed INVALID assessment contributes the
protected experiment's failure code: COLLISION -> UNIQUENESS-FAILURE;
CROSS-ACTION-TRACKING -> CORRELATION-FAILURE; ACTOR-INFORMATION ->
ACTOR-RECONSTRUCTION-RISK. Internal reason retains INVALID-ARGUMENT distinct
from a demonstrated producer privacy violation. An unqualified INVALID flag
is a qualification/evidence failure, never a known counterexample.

All known protected paths/equalities retain the original applicable failures;
a row can contribute more than one failure (including observed cross-action n).
Known envelope mismatch and missing scope proof are distinct cases, not an
implementer-selected choice between two codes. The decision-case row saying
'INVALID-ACTION-CONTEXT or incomplete evidence' is read under this distinction.

UNION is permitted only when qualified evidence proves that the complete failure
event/advantage decomposition is bounded by these exact terms. Arithmetic alone
does not justify joining arbitrary distinguishing games. Multiplicities align
one-for-one with ordered, distinct argument_ids, are positive integers, and cover
all applicable repetitions/interactions. A single joint argument has one term;
shared terms are not counted twice without source-established multiplicity.
A source-qualified tighter/product/composed-game bound requires its own exact
theorem and qualification. Every required experiment has complete coverage and
is compared to its own source-owned maximum, with no invented policy values.

6. Status of this completed correction

This source-determined correction fixes record placement, external absence,
framing visibility, static-versus-actual coverage, quantification, noncircular
qualification and failure interpretation. It supplies documentary grammar, not
a production V4 acceptance validator, instantiated governing member, source
appointment or security evidence. Author grammar checks do not independently
accept this correction. The historical SUPPLIED package retains its original
BLOCKED verdict. Steve has now approved A; the final assessment is in the
Engineering[287] completion report. Prior review/authorization and execution
receipt questions are not reopened.


ENGINEERING[287] OPTION A — APPROVED NON-VACUITY CONTRACT

Authority: Steve's message 'A' in Engineering[287], 1 October 2026, selects the
explicit option A in the focused definition report. This is protocol-authoring
authorization. It is not policy-source appointment, evidence qualification,
profile admission, publication or permission to execute a transition.

This section governs S90 #nonvacuity and supersedes the earlier OPEN decision
markers. Existing exact privacy protections, leakage exceptions, capability
decisions, numeric-source ownership and independent qualification duties remain.

NV1. Every required computational EXPERIMENT.maximum MUST be a canonical reduced
rational [numerator,positive denominator] with 0 <= numerator < denominator.
Numerical targets still originate in the independently governing policy; there
is no default target, security-bits label, probability 1/p, adversary model or
algorithm assumption. A weak maximum below one remains a visibly weak target;
this floor alone establishes no practically adequate strength.

Validated argument bounds and composed bounds remain canonical probabilities in
[0,1]. Bound one is representable as a pessimistic qualified result; it exceeds
every permitted maximum and cannot discharge admission. The strict maximum law
applies in the V4 experiment grammar and the UNION budget entrypoint, not only
in explanatory text. Maximum zero is permitted, but only a soundly established
zero bound can meet it. Unsupported perfect-security assertions still fail.

NV2. Every required experiment MUST have independently established nonempty
admissible scope and genuine protected alternatives, with uniform protection over
the entire source-owned adversary/capability/resource class and all allowed
adaptive schedules, repeated actions, queries, auxiliaries and required coalitions.
For collision, the scope includes admissible distinct canonical relation-valid
input tuples and the corresponding source-defined adversarial experiment. A
collision impossibility proof over a genuinely nonempty such domain may establish
zero; eliminating the domain is not that proof.

For CROSS-ACTION-TRACKING, the source-owned worlds differ in protected actor
associations across admissible distinct actions, with nonzero support for those
alternatives. For each ACTOR-INFORMATION target the worlds genuinely differ in
that protected association/attribute with nonzero support. Approved public
leakage and permitted schedules/auxiliary knowledge are matched under the exact
experiment semantics. Each required coalition receives the complete view. An
identical-world pair, zero-occurrence-only scope, chosen constant-output benign
adversary, erased required coalition/target, or conditioning away a prohibited
observation does not discharge the intended claim.

These are STATIC model/support duties. They require no invented real A/E/D/U or
two already executed actions. They do not mandate an unbounded adversary or new
corruption policy. Additional restricted model assumptions remain explicit and
independently governed; the claim may not be advertised beyond their scope.

NV3. Support, whole-class quantification, whole-view coverage, exact source scope
and applicability MUST be established under the independently qualified parser/
assessment contracts already bound by POLICY, EXPERIMENT and QUALIFICATION.
The exact world/envelope/target/coalition definitions and validating evidence
are referenced through their existing SOURCE-REFs and argument/premise/artifact
joins; no new proof input, PE-TSE host call, actor subject or public trace is added.

The non-vacuity validation interface takes the exact policy, experiment/world
definitions, envelope, complete model/target/coalition directories and qualification
contracts. Its qualified VALID result binds those exact inputs and establishes
the NV1/NV2 duties. INVALID and UNAVAILABLE are distinct and neither discharges
them. An unqualified VALID flag, arbitrary signature, positive count supplied by
the issuer or a schema-valid world reference cannot establish these semantic facts.
The exact independently qualified checking mechanism/grammar is a policy input;
software must enforce its source-owned contract and cannot invent a substitute.
Callbacks, outputs, errors, retries, caches and observer/dependency surfaces use
the existing assessor/argument/source evidence classes and full expansion law.

Empty or inapplicable directories require independent source justification for
the actual duty. A required computational privacy experiment cannot be marked
inapplicable merely because it cannot meet NV1/NV2. The regenerated full ledger
and complete targets/views control which duties are required. Genuine source-
established inapplicability of a duty is distinct from an empty supported scope
for a claim represented as providing computational privacy.

NV4. Failure collection MUST preserve the inherited ORDER. A malformed or
prohibited maximum is INVALID-PROFILE-SCHEMA. Established model/world/envelope
scope failing NV2 contributes INVALID-ACTION-CONTEXT. Missing required exact
bytes, unestablished authority and failed signature/digest retain their earlier
codes. Unavailable/unsupported non-vacuity assessment or inability to establish
complete support/coverage contributes INCOMPLETE-EVIDENCE-UNIVERSE. All detectable
failures are collected; the earliest wins. The EXCEEDED budget case contributes
the protected experiment's existing uniqueness/correlation/actor failure code.
No new failure code or externally observable result subject is introduced.

All exact/source-established protected violations, observed counterexamples and
unknown visibility still reject even if budgets and support checks otherwise pass.
Acceptance requires EVERY governing duty, including NV1–NV4, independent source
and evidence qualification, profile adequacy and inherited gates. It means only
the precise conditional protection justified by that policy and its established
assumptions. Neither a strict maximum, schema validity, successful calculation,
successful serialization nor this authoring decision alone supplies privacy.

CONSTRUCTION DEPENDENCY LAW

Static policy/source/algorithm/parser/qualification/field-label/model material
embedded in or referenced by the immutable member must have an acyclic exact-byte
construction basis before final outer-profile hashing. It may bind earlier
source/body/program/model material where its qualified contract permits, but
must not require its own final outer digest or the final admission decision to
exist as a construction input. The immutable obligation/composition templates
contain no actual result fields. Final-profile-bound argument/result/occurrence
records, signatures and admission evidence follow completed immutable bytes and
remain external. A hidden self-digest in referenced material is not excused by
using SOURCE-REF; circular construction prevents construction/admission.

SELECTED PROFILE BOUNDARY

Non-vacuity and envelope applicability add source-validation duties, not a third
projected material bit. The two-component profile is suitable only if the full
source-owned scope fits its fixed effect, ordering and coordinate/dependency
contracts. A policy that needs additional changing material conditions, runtime
budget-accounting state, ordering or effects must reject this profile until
explicitly revised. No new lifetime-counting mechanism is silently appointed.

CROSS-RECORD ACCEPTANCE JOINS

The active grammar's shape functions establish structure only. A production
validator must also enforce these exact typed joins after independently qualified
regeneration; it may not derive semantic truth from matching identifier spelling.
Each record carrying policy_id names the sole immutable POLICY.policy_id. POLICY
experiment_ids, coalition_ids, assumption_ids, qualification_ids and field_label_ids
are the exact identity directories of the corresponding immutable record arrays,
in their canonical identity order. target_ids is the independently regenerated
complete protected-target directory, matched to source-qualified OBSERVER target
references and model target identities; it is not issuer-selected. envelope_id
and leakage_id name the sole owning records. All required directories are complete;
source-qualified justified inapplicability is the only permitted empty directory.

Every algorithm_id reference resolves in the ALGORITHM directory, every artifact_id
in ARTIFACT, qualification_id in QUALIFICATION, assumption_id in ASSUMPTION and
experiment_id in EXPERIMENT, with exact policy/scope/source/artifact correspondence.
ALGORITHM.artifact_ids and ARTIFACT.algorithm_id agree. Each EXPERIMENT coalition,
target, algorithm, envelope and leakage reference resolves to its owning directory
and exact qualified scope. FIELD-LABEL.surface_id covers a declared full-model
field class exactly once, and its coalition/owner/visibility references are
independently adequate for every expanded instance. Completeness cannot be
established merely because all supplied references resolve.

Static obligation node_ids/edge_ids resolve in the rebuilt model, target/coalition
joins cover the full required universe, and every COMPUTATIONAL experiment_id
resolves. EXACT obligations use null experiment_id and do not acquire a computational
waiver. The complete obligation directory is independently regenerated under the
qualified source/model contract, including exact joins and whole-view interactions;
issuer omissions, invented obligations or classifications inconsistent with a
known exact violation fail. External OBLIGATION instances repeat the immutable
template fields exactly, bind the final outer profile digest and SHA256 of its
canonical immutable model, and add only the specified evidence/result fields.

A COMPOSITION rule is unique for each required experiment. External COMPOSITION
instances repeat its template fields exactly and align distinct argument_ids with
positive multiplicities and qualified bounds. ARGUMENT.composition_id names this
specific rule record, not POLICY's directory identity. ARGUMENT obligation_ids,
experiment, assumptions, qualification, artifacts, envelope and premises match
the independently checked claim. Every ASSESSMENT names exactly its ARGUMENT and
qualified mechanism; exact_input_digest hashes the complete invocation preimage
specified by that exact source-qualified mechanism. The validator reconstructs
that preimage from the supplied exact argument/policy/world/artifact/premise bytes;
it never assumes a generic checker preimage or accepts an opaque matching digest.
Relevant assessor-event records cover the entire qualified invocation and actual
control/read/return/error/retry/cache trace, with exact predecessor/context/attempt
joins. POLICY-APPLICABILITY binds the final profile, exact governing mapping,
current source context, envelope, phase and attempt. No outside record may change
an immutable source policy/template, certify its own authority or omit actual
consumed dependencies. Missing, orphaned or incoherent material fails in the
inherited schema/context/universe/authority categories as applicable.

All graph index/byte/count representations must fit their inherited U32/U64/ordinal
wire domains. A finite but unrepresentable model fails schema validation; no
truncation, wraparound, silent scope reduction or alternative codec is permitted.

V4 MODEL/EVIDENCE BYTE ADAPTER

This is the explicit V4 binding of the existing signed-table fields; it extends
the owning token/link universe and preserves the V2 headers/domains/four-file
preimages. It does not permit using the old V2/V3 decision implementation for V4.
For this V4 member, surface_template_sha256 hashes canonical JSON of model.surfaces
and relation_template_sha256 hashes canonical JSON of model.relations, including
the single terminal LF. These are exact typed template arrays, not issuer prose
or caches. Both arrays and their qualified derivation are independently regenerated.
The V4 adapter supersedes the old submodel-only template preimages for these two
field values; it changes no signature domain, TSV header or object digest framing.

model tokens retain the zero-based contiguous index, id, surface, context, record,
exposure, reuse, arbitrary and symbolic_digest layout of the inherited expansion.
In the static model they contain symbolic values only. STRUCTURAL edges are exact
[left index,right index,one-based relation-template order,relation class] arrays;
source-directory/record-field/frame/parser/custody expansions normalize into that
same layout. Template relation provenance/source meaning remains bound by the
complete source-owned arrays/procedure/model inputs; identical-looking source
relations with distinct provenance have distinct template identities. There are
no hidden edges or anonymous side graphs.

For ledger edge_ids, a structural occurrence is G4-STRUCTURAL-EDGE- followed by
its one-based canonical model.structural_edges array index in ordinary decimal.
A potential equality edge is G4-EQUALITY-PAIR-{left-index}-{right-index}, with
zero-based ordinary-decimal indexes and left < right. node_ids name exact token
id values. These identity constructors are unambiguous, are not actor identifiers,
and do not imply runtime priority. Relation/order/record completeness is checked
against the qualified model, never against a supplied expected-result cache.

The regenerated static signed-token universe is the complete model.tokens array;
its token_sha256 is symbolic_digest. The actual occurrence universe replaces
symbolic values with exact independently authenticated owning record values and
uses their owning-source byte law (the S90 canonical typed JSON law for security
records). Complete actual directories must match admitted field classes/envelope
and occurrence joins. Tokens and links are regenerated from those exact records;
static placeholders cannot be presented as actual equality witnesses.

For every structural edge the signed link is the corresponding token IDs,
f'{relation-template-order:06}', and its relation class. Every static potential
equality pair from the inherited full predicate also supplies a link with
relation_order 000000 and relation_class EQUALS. Actual occurrence equality uses
exact source-qualified owning value equality and all established relations; no
potential symbol is promoted to a known match. The complete links are ordered
lexicographically by the four string cells; identical tuples occur once and
provenance-distinct relations remain separate. No equality stream is sampled.
The signed-token row order is the regenerated token array order. token_order and
link_order use the inherited f'{one-based-row:06}' minimum-width decimal spelling;
the six-character format is not a new link-count cap. Actual comparison-attempt
ordinals and other explicitly closed ORD6 identifiers retain their true limits.

The seven TOKEN_HEADER and five LINK_HEADER cells, literal TAB separators, one
LF after every row, and UTF-8/no-BOM/no-CR constraints are the retained S70 law.
Component evidence uses the inherited complete closure of its source-owned
component seed through the full regenerated graph; it cannot omit a required
security/observer duty. The three distinct scopes/kinds are retained: ROOT-ELIGIBLE,
SCOPED-USED and NOT-APPLICABLE composition. Whole-view computational qualifications
are checked for their exact relevant experiment/target/view scopes in every bundle;
a component PASS cannot replace composition or the other component.

The sole evidence.tsv row retains the fifteen EVIDENCE_HEADER cells and inherited
identity/scope constructors: profile-id#ADMISSION-V1 at static admission, or
profile-id#OCCURRENCE-SET- plus SHA256 of exact scoped tokens.tsv at occurrence;
evidence_id is profile-id#kind-ALL for composition and profile-id#kind-component-id
otherwise. kind is ADMISSION-COMPONENT/ADMISSION-COMPOSITION at static admission
and COMPONENT/COMPOSITION at occurrence. profile_sha256 binds the final outer
container, not a privacy subobject. tokens_sha256 and links_sha256 hash their
complete exact file bytes. The three *_result cells are independently computed
PASS/FAIL for the respective complete uniqueness/correlation/actor contract after
all exact/computational qualification, coverage, composition, budgets and NV duties;
an arbitrary signed PASS is not a result. Inability cannot create admitted evidence.
issued_by and algorithm are the externally appointed evidence authority identity
and ED25519-RFC8032. The signature.txt line and the signed/object-digest preimages
are exactly the retained V2 laws. All authority/semantic/scope failures still collect
in inherited ORDER before acceptance; serializing these cells grants no permission.


APPROVED COMPATIBILITY AMENDMENT PE-G4-FIELD-CLASS-REF-AMENDMENT-001 v1.0.0
# PE-G4-FIELD-CLASS-REF-AMENDMENT-001 version 1.0.0

Authority: explicit user approval, AUTHORITY.json SHA-256 5a33a07373db842ed9efc898cf682407d2032175eb7d2c9cb645ad5c6f24cd63.
This is a narrow compatibility amendment to the preserved Engineering[287]/S90 baseline, not evidence of source or mechanism qualification or protocol publication.

FIELD-LABEL.surface_id has type FIELD-CLASS-REF. Its representation is the unchanged canonical JSON string containing the exact case-sensitive field-class name. Its spelling is either an existing ID or an existing ID immediately followed by `.$record`. Its value MUST be an exact member of the complete source-owned surface register bound to the model. Occurrence-qualified token IDs, aliases, names absent from that register and all other dollar spellings are invalid. Canonical JSON retains its accepted serialization; alternate byte encodings are not introduced.

This type applies solely to FIELD-LABEL.surface_id. General ID and OBLIGATION grammar are unchanged. Owner, coalition, visibility, complete field-class coverage and UNKNOWN rules remain unchanged. A supplied register is an input to local membership checks; only the independent source/model correspondence and qualification rules establish its authority and completeness. Missing register context cannot establish validity and must fail through INCOMPLETE-EVIDENCE-UNIVERSE at admission. Malformed spelling remains a schema failure; a well-spelled absent member is an incomplete-universe failure.

Revised normative schema/grammar/contract are the companion files. PE-G4-SOURCE-S90-FCR-001.md consolidates the preserved S90 text with this exact amendment; its source identifier is PE-G4-SOURCE-S90-FCR-001, version 1.0.0. BINDING.json pins all revised and reused normative bytes. Historical accepted/ and predecessor ZIPs remain immutable. Dependent source/procedure, finite contract, provenance, profile, invocation, evidence and signature bindings must be regenerated or verified unchanged; no prior receipt silently migrates.

Exact affected baseline clauses: security-fields.tsv data row 83 (file line 84), S90 line 890; v4_record_grammar.py ID lines 57–59; ACCEPTANCE-CONTRACT lines 385–390 (S90 451–456) and 615 onward (S90 681 onward). Earlier OBLIGATION edge-reference compatibility is unaffected and does not replace FIELD-LABEL references or prove duty coverage.

## Register semantics and primitive grammar

ID is a nonempty canonical ASCII source-owned identifier; DIGEST is lowercase 64-character SHA256 of exact referenced bytes; BYTES is the complete byte sequence, represented as lowercase even-length hex in canonical JSON. UINT is a nonnegative JSON integer excluding Booleans. RATIONAL is a reduced [numerator,positive denominator] with 0 <= numerator <= denominator. SOURCE-REF is exactly {owner_source_id, source_sha256, source_anchor, material_sha256}; exact material bytes and independently qualified source/anchor interpretation accompany the reference outside the immutable member. Lists are ordered canonical arrays with unique IDs where they denote directories, not sets silently deduplicated by the issuer.

ENUM-EXPERIMENT: COLLISION,CROSS-ACTION-TRACKING,ACTOR-INFORMATION. ENUM-QUALIFIED: VALID,INVALID,UNAVAILABLE. ENUM-EXPOSURE: PUBLIC,CONFIDENTIAL,PRIVATE-ACTOR; UNKNOWN is permitted only as an uninstantiated draft label and blocks admission. ENUM-OBLIGATION: EXACT,COMPUTATIONAL. ENUM-DISPOSITION: EXACT-SATISFIED,EXACT-VIOLATION,COMPUTATIONALLY-BOUNDED,NOT-ESTABLISHED. ENUM-COMPOSITION: UNION,SOURCE-QUALIFIED-THEOREM. ENUM-ASSESSOR-EVENT: READ,CALL,RETURN,ERROR,RETRY,CACHE. ENUM-STAGE: STATIC-ADMISSION,E,PRE-EXECUTION,PRE-COMMITMENT.

ONE means exactly one owning record. ONE-OR-MORE means the exact nonempty source-established directory. POLICY-LIST and other LIST cardinalities mean exactly the governing referenced directory, including zero only where the governing source establishes inapplicability with an explicit justification; the mechanical helper conservatively requires nonempty lists and is not a validator of these justifications. POLICY-APPLICABILITY includes static admission plus E and every actual gate instance where required. No placeholder is a production record.

Every source material reference requires its exact parser/semantics/competence binding. The interface never treats a digest, arbitrary issuer JSON, source name, signed claim or caller completion bit as established source truth. Required status assertions are existing source-result facts whose validity and authentication must be independently established before the pure program consumes them.

## Exact security-fields.tsv

```tsv
surface_id	schema	field	type	cardinality	owner_source_id	owner_anchor	exposure	reuse	phase
SECURITY:POLICY.policy_id	POLICY	policy_id	ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.policy_source	POLICY	policy_source	SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.policy_digest	POLICY	policy_digest	DIGEST	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.approved_by_source	POLICY	approved_by_source	SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.profile_id	POLICY	profile_id	ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.experiment_ids	POLICY	experiment_ids	LIST-ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.coalition_ids	POLICY	coalition_ids	LIST-ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.target_ids	POLICY	target_ids	LIST-ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.assumption_ids	POLICY	assumption_ids	LIST-ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.qualification_ids	POLICY	qualification_ids	LIST-ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.envelope_id	POLICY	envelope_id	ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.leakage_id	POLICY	leakage_id	ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.composition_id	POLICY	composition_id	ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY.field_label_ids	POLICY	field_label_ids	LIST-ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.envelope_id	ENVELOPE	envelope_id	ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.policy_id	ENVELOPE	policy_id	ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.computation_model	ENVELOPE	computation_model	SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.capabilities	ENVELOPE	capabilities	SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.resource_limits	ENVELOPE	resource_limits	SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.occurrence_limit	ENVELOPE	occurrence_limit	UINT	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.comparison_limit	ENVELOPE	comparison_limit	UINT	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.attempt_limit	ENVELOPE	attempt_limit	UINT	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.query_limits	ENVELOPE	query_limits	SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.validity_scope	ENVELOPE	validity_scope	SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.secret_distribution	ENVELOPE	secret_distribution	SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ENVELOPE.state_distribution	ENVELOPE	state_distribution	SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:LEAKAGE.leakage_id	LEAKAGE	leakage_id	ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:LEAKAGE.policy_id	LEAKAGE	policy_id	ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:LEAKAGE.source_refs	LEAKAGE	source_refs	LIST-SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:LEAKAGE.relationship_ids	LEAKAGE	relationship_ids	LIST-ID	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:LEAKAGE.authorized_outcome_refs	LEAKAGE	authorized_outcome_refs	LIST-SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:LEAKAGE.schedule_rule	LEAKAGE	schedule_rule	SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:LEAKAGE.auxiliary_knowledge_rule	LEAKAGE	auxiliary_knowledge_rule	SOURCE-REF	ONE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ALGORITHM.algorithm_id	ALGORITHM	algorithm_id	ID	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ALGORITHM.policy_id	ALGORITHM	policy_id	ID	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ALGORITHM.algorithm_source	ALGORITHM	algorithm_source	SOURCE-REF	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ALGORITHM.field_source	ALGORITHM	field_source	SOURCE-REF	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ALGORITHM.parameters_source	ALGORITHM	parameters_source	SOURCE-REF	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ALGORITHM.encoding_source	ALGORITHM	encoding_source	SOURCE-REF	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ALGORITHM.domain_source	ALGORITHM	domain_source	SOURCE-REF	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ALGORITHM.relation_source	ALGORITHM	relation_source	SOURCE-REF	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ALGORITHM.artifact_ids	ALGORITHM	artifact_ids	LIST-ID	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARTIFACT.artifact_id	ARTIFACT	artifact_id	ID	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARTIFACT.algorithm_id	ARTIFACT	algorithm_id	ID	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARTIFACT.owner	ARTIFACT	owner	SOURCE-REF	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARTIFACT.format_source	ARTIFACT	format_source	SOURCE-REF	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARTIFACT.exact_bytes	ARTIFACT	exact_bytes	BYTES	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARTIFACT.digest	ARTIFACT	digest	DIGEST	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARTIFACT.correspondence_evidence_ref	ARTIFACT	correspondence_evidence_ref	SOURCE-REF	ONE-OR-MORE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.experiment_id	EXPERIMENT	experiment_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.policy_id	EXPERIMENT	policy_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.kind	EXPERIMENT	kind	ENUM-EXPERIMENT	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.coalition_id	EXPERIMENT	coalition_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.target_id	EXPERIMENT	target_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.algorithm_ids	EXPERIMENT	algorithm_ids	LIST-ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.left_world	EXPERIMENT	left_world	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.right_world	EXPERIMENT	right_world	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.observation_rule	EXPERIMENT	observation_rule	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.envelope_id	EXPERIMENT	envelope_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.leakage_id	EXPERIMENT	leakage_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:EXPERIMENT.maximum	EXPERIMENT	maximum	RATIONAL	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSUMPTION.assumption_id	ASSUMPTION	assumption_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSUMPTION.policy_id	ASSUMPTION	policy_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSUMPTION.statement	ASSUMPTION	statement	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSUMPTION.experiment_ids	ASSUMPTION	experiment_ids	LIST-ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSUMPTION.envelope_id	ASSUMPTION	envelope_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSUMPTION.qualification_id	ASSUMPTION	qualification_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSUMPTION.evidence_ref	ASSUMPTION	evidence_ref	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSUMPTION.approved_bound	ASSUMPTION	approved_bound	RATIONAL	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSUMPTION.premise_ids	ASSUMPTION	premise_ids	LIST-ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:QUALIFICATION.qualification_id	QUALIFICATION	qualification_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:QUALIFICATION.policy_id	QUALIFICATION	policy_id	ID	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:QUALIFICATION.authority_source	QUALIFICATION	authority_source	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:QUALIFICATION.assessor_identity	QUALIFICATION	assessor_identity	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:QUALIFICATION.accepted_grammar	QUALIFICATION	accepted_grammar	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:QUALIFICATION.semantic_checker	QUALIFICATION	semantic_checker	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:QUALIFICATION.competence_evidence	QUALIFICATION	competence_evidence	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:QUALIFICATION.soundness_basis	QUALIFICATION	soundness_basis	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:QUALIFICATION.result_schema	QUALIFICATION	result_schema	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:QUALIFICATION.unavailable_rule	QUALIFICATION	unavailable_rule	SOURCE-REF	POLICY-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:FIELD-LABEL.field_label_id	FIELD-LABEL	field_label_id	ID	FULL-SURFACE-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:FIELD-LABEL.policy_id	FIELD-LABEL	policy_id	ID	FULL-SURFACE-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:FIELD-LABEL.surface_id	FIELD-LABEL	surface_id	FIELD-CLASS-REF	FULL-SURFACE-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:FIELD-LABEL.exposure	FIELD-LABEL	exposure	ENUM-EXPOSURE	FULL-SURFACE-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:FIELD-LABEL.owner	FIELD-LABEL	owner	SOURCE-REF	FULL-SURFACE-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:FIELD-LABEL.coalition_ids	FIELD-LABEL	coalition_ids	LIST-ID	FULL-SURFACE-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:FIELD-LABEL.visibility_evidence	FIELD-LABEL	visibility_evidence	SOURCE-REF	FULL-SURFACE-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.argument_id	ARGUMENT	argument_id	ID	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.policy_id	ARGUMENT	policy_id	ID	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.profile_digest	ARGUMENT	profile_digest	DIGEST	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.model_digest	ARGUMENT	model_digest	DIGEST	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.obligation_ids	ARGUMENT	obligation_ids	LIST-ID	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.experiment_id	ARGUMENT	experiment_id	ID	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.assumption_ids	ARGUMENT	assumption_ids	LIST-ID	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.premise_ids	ARGUMENT	premise_ids	LIST-ID	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.certificate_artifact_ids	ARGUMENT	certificate_artifact_ids	LIST-ID	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.qualification_id	ARGUMENT	qualification_id	ID	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.reduction_source	ARGUMENT	reduction_source	SOURCE-REF	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.claimed_bound	ARGUMENT	claimed_bound	RATIONAL	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.envelope_id	ARGUMENT	envelope_id	ID	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ARGUMENT.composition_id	ARGUMENT	composition_id	ID	OBLIGATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSMENT.assessment_id	ASSESSMENT	assessment_id	ID	ARGUMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSMENT.argument_id	ASSESSMENT	argument_id	ID	ARGUMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSMENT.qualification_id	ASSESSMENT	qualification_id	ID	ARGUMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSMENT.invocation_source	ASSESSMENT	invocation_source	SOURCE-REF	ARGUMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSMENT.exact_input_digest	ASSESSMENT	exact_input_digest	DIGEST	ARGUMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSMENT.complete_result	ASSESSMENT	complete_result	ENUM-QUALIFIED	ARGUMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSMENT.validated_bound	ASSESSMENT	validated_bound	RATIONAL	ARGUMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSMENT.artifact_ids	ASSESSMENT	artifact_ids	LIST-ID	ARGUMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSMENT.assumption_ids	ASSESSMENT	assumption_ids	LIST-ID	ARGUMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSMENT.source_assertion_evidence	ASSESSMENT	source_assertion_evidence	SOURCE-REF	ARGUMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.obligation_id	OBLIGATION	obligation_id	ID	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.profile_digest	OBLIGATION	profile_digest	DIGEST	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.model_digest	OBLIGATION	model_digest	DIGEST	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.kind	OBLIGATION	kind	ENUM-OBLIGATION	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.target_ids	OBLIGATION	target_ids	LIST-ID	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.coalition_id	OBLIGATION	coalition_id	ID	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.node_ids	OBLIGATION	node_ids	LIST-ID	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.edge_ids	OBLIGATION	edge_ids	LIST-ID	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.experiment_id	OBLIGATION	experiment_id	ID	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.disposition	OBLIGATION	disposition	ENUM-DISPOSITION	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.argument_ids	OBLIGATION	argument_ids	LIST-ID	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBLIGATION.exact_evidence_refs	OBLIGATION	exact_evidence_refs	LIST-SOURCE-REF	REGENERATED-FULL-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:COMPOSITION.composition_id	COMPOSITION	composition_id	ID	EXPERIMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:COMPOSITION.policy_id	COMPOSITION	policy_id	ID	EXPERIMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:COMPOSITION.experiment_id	COMPOSITION	experiment_id	ID	EXPERIMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:COMPOSITION.method	COMPOSITION	method	ENUM-COMPOSITION	EXPERIMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:COMPOSITION.argument_ids	COMPOSITION	argument_ids	LIST-ID	EXPERIMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:COMPOSITION.multiplicities	COMPOSITION	multiplicities	LIST-UINT	EXPERIMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:COMPOSITION.theorem_ref	COMPOSITION	theorem_ref	SOURCE-REF	EXPERIMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:COMPOSITION.qualification_id	COMPOSITION	qualification_id	ID	EXPERIMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:COMPOSITION.composed_bound	COMPOSITION	composed_bound	RATIONAL	EXPERIMENT-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSOR-EVENT.event_id	ASSESSOR-EVENT	event_id	ID	FULL-INVOCATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSOR-EVENT.assessment_id	ASSESSOR-EVENT	assessment_id	ID	FULL-INVOCATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSOR-EVENT.event_kind	ASSESSOR-EVENT	event_kind	ENUM-ASSESSOR-EVENT	FULL-INVOCATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSOR-EVENT.input_bytes	ASSESSOR-EVENT	input_bytes	BYTES	FULL-INVOCATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSOR-EVENT.output_bytes	ASSESSOR-EVENT	output_bytes	BYTES	FULL-INVOCATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSOR-EVENT.predecessor_ids	ASSESSOR-EVENT	predecessor_ids	LIST-ID	FULL-INVOCATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSOR-EVENT.control_source	ASSESSOR-EVENT	control_source	SOURCE-REF	FULL-INVOCATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSOR-EVENT.owner	ASSESSOR-EVENT	owner	SOURCE-REF	FULL-INVOCATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:ASSESSOR-EVENT.attempt_ordinal	ASSESSOR-EVENT	attempt_ordinal	UINT	FULL-INVOCATION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBSERVER.coalition_id	OBSERVER	coalition_id	ID	FULL-COALITION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBSERVER.policy_id	OBSERVER	policy_id	ID	FULL-COALITION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBSERVER.member_role_refs	OBSERVER	member_role_refs	LIST-SOURCE-REF	FULL-COALITION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBSERVER.protected_target_refs	OBSERVER	protected_target_refs	LIST-SOURCE-REF	FULL-COALITION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:OBSERVER.observation_evidence_refs	OBSERVER	observation_evidence_refs	LIST-SOURCE-REF	FULL-COALITION-LIST	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY:POLICY-APPLICABILITY.applicability_id	POLICY-APPLICABILITY	applicability_id	ID	E-AND-EVERY-GATE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	E-AND-GATE-EVIDENCE
SECURITY:POLICY-APPLICABILITY.policy_id	POLICY-APPLICABILITY	policy_id	ID	E-AND-EVERY-GATE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	E-AND-GATE-EVIDENCE
SECURITY:POLICY-APPLICABILITY.profile_digest	POLICY-APPLICABILITY	profile_digest	DIGEST	E-AND-EVERY-GATE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	E-AND-GATE-EVIDENCE
SECURITY:POLICY-APPLICABILITY.mapping_digest	POLICY-APPLICABILITY	mapping_digest	DIGEST	E-AND-EVERY-GATE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	E-AND-GATE-EVIDENCE
SECURITY:POLICY-APPLICABILITY.context_source	POLICY-APPLICABILITY	context_source	SOURCE-REF	E-AND-EVERY-GATE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	E-AND-GATE-EVIDENCE
SECURITY:POLICY-APPLICABILITY.envelope_id	POLICY-APPLICABILITY	envelope_id	ID	E-AND-EVERY-GATE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	E-AND-GATE-EVIDENCE
SECURITY:POLICY-APPLICABILITY.source_status_evidence	POLICY-APPLICABILITY	source_status_evidence	SOURCE-REF	E-AND-EVERY-GATE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	E-AND-GATE-EVIDENCE
SECURITY:POLICY-APPLICABILITY.dependency_evidence	POLICY-APPLICABILITY	dependency_evidence	SOURCE-REF	E-AND-EVERY-GATE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	E-AND-GATE-EVIDENCE
SECURITY:POLICY-APPLICABILITY.stage	POLICY-APPLICABILITY	stage	ENUM-STAGE	E-AND-EVERY-GATE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	E-AND-GATE-EVIDENCE
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	POLICY-APPLICABILITY	attempt_ordinal	UINT	E-AND-EVERY-GATE	PE-G4-SOURCE-S90	schemas	UNKNOWN	NONE	E-AND-GATE-EVIDENCE
```

## Exact security-relations.tsv

```tsv
from_node	to_node	relation	origin
SECURITY:POLICY.policy_id	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.policy_source	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.policy_digest	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.approved_by_source	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.profile_id	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.experiment_ids	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.coalition_ids	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.target_ids	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.assumption_ids	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.qualification_ids	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.envelope_id	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.leakage_id	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.composition_id	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.field_label_ids	SECURITY:POLICY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.policy_id	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.computation_model	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.capabilities	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.query_limits	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	SECURITY:ENVELOPE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.$record	SECURITY:ENVELOPE.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:LEAKAGE.leakage_id	SECURITY:LEAKAGE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:LEAKAGE.policy_id	SECURITY:LEAKAGE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:LEAKAGE.source_refs	SECURITY:LEAKAGE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	SECURITY:LEAKAGE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	SECURITY:LEAKAGE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	SECURITY:LEAKAGE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	SECURITY:LEAKAGE.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.$record	SECURITY:LEAKAGE.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ALGORITHM.algorithm_id	SECURITY:ALGORITHM.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ALGORITHM.policy_id	SECURITY:ALGORITHM.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	SECURITY:ALGORITHM.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ALGORITHM.field_source	SECURITY:ALGORITHM.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	SECURITY:ALGORITHM.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	SECURITY:ALGORITHM.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ALGORITHM.domain_source	SECURITY:ALGORITHM.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ALGORITHM.relation_source	SECURITY:ALGORITHM.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	SECURITY:ALGORITHM.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.$record	SECURITY:ALGORITHM.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ARTIFACT.artifact_id	SECURITY:ARTIFACT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	SECURITY:ARTIFACT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARTIFACT.owner	SECURITY:ARTIFACT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARTIFACT.format_source	SECURITY:ARTIFACT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	SECURITY:ARTIFACT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARTIFACT.digest	SECURITY:ARTIFACT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	SECURITY:ARTIFACT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ALGORITHM.$record	SECURITY:ARTIFACT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:EXPERIMENT.experiment_id	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:EXPERIMENT.kind	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:EXPERIMENT.target_id	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:EXPERIMENT.left_world	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:EXPERIMENT.right_world	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:EXPERIMENT.maximum	SECURITY:EXPERIMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.$record	SECURITY:EXPERIMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ENVELOPE.$record	SECURITY:EXPERIMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:LEAKAGE.$record	SECURITY:EXPERIMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:OBSERVER.$record	SECURITY:EXPERIMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ASSUMPTION.assumption_id	SECURITY:ASSUMPTION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	SECURITY:ASSUMPTION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSUMPTION.statement	SECURITY:ASSUMPTION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	SECURITY:ASSUMPTION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	SECURITY:ASSUMPTION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	SECURITY:ASSUMPTION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	SECURITY:ASSUMPTION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	SECURITY:ASSUMPTION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	SECURITY:ASSUMPTION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.$record	SECURITY:ASSUMPTION.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:EXPERIMENT.$record	SECURITY:ASSUMPTION.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:QUALIFICATION.$record	SECURITY:ASSUMPTION.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:QUALIFICATION.qualification_id	SECURITY:QUALIFICATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	SECURITY:QUALIFICATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	SECURITY:QUALIFICATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	SECURITY:QUALIFICATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	SECURITY:QUALIFICATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	SECURITY:QUALIFICATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	SECURITY:QUALIFICATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	SECURITY:QUALIFICATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	SECURITY:QUALIFICATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	SECURITY:QUALIFICATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.$record	SECURITY:QUALIFICATION.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:FIELD-LABEL.field_label_id	SECURITY:FIELD-LABEL.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	SECURITY:FIELD-LABEL.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	SECURITY:FIELD-LABEL.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	SECURITY:FIELD-LABEL.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:FIELD-LABEL.owner	SECURITY:FIELD-LABEL.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	SECURITY:FIELD-LABEL.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	SECURITY:FIELD-LABEL.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.$record	SECURITY:FIELD-LABEL.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:OBSERVER.$record	SECURITY:FIELD-LABEL.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ARGUMENT.argument_id	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.policy_id	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.model_digest	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.composition_id	SECURITY:ARGUMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.$record	SECURITY:ARGUMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:EXPERIMENT.$record	SECURITY:ARGUMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ASSUMPTION.$record	SECURITY:ARGUMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:QUALIFICATION.$record	SECURITY:ARGUMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ARTIFACT.$record	SECURITY:ARGUMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ASSESSMENT.assessment_id	SECURITY:ASSESSMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	SECURITY:ASSESSMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	SECURITY:ASSESSMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	SECURITY:ASSESSMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	SECURITY:ASSESSMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	SECURITY:ASSESSMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	SECURITY:ASSESSMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	SECURITY:ASSESSMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	SECURITY:ASSESSMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	SECURITY:ASSESSMENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.$record	SECURITY:ASSESSMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:QUALIFICATION.$record	SECURITY:ASSESSMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ASSESSOR-EVENT.$record	SECURITY:ASSESSMENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:OBLIGATION.obligation_id	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.model_digest	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.kind	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.target_ids	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.node_ids	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.disposition	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	SECURITY:OBLIGATION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.$record	SECURITY:OBLIGATION.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:FIELD-LABEL.$record	SECURITY:OBLIGATION.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:OBSERVER.$record	SECURITY:OBLIGATION.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:COMPOSITION.composition_id	SECURITY:COMPOSITION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:COMPOSITION.policy_id	SECURITY:COMPOSITION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	SECURITY:COMPOSITION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:COMPOSITION.method	SECURITY:COMPOSITION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	SECURITY:COMPOSITION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	SECURITY:COMPOSITION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	SECURITY:COMPOSITION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	SECURITY:COMPOSITION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	SECURITY:COMPOSITION.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ARGUMENT.$record	SECURITY:COMPOSITION.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ASSESSMENT.$record	SECURITY:COMPOSITION.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:EXPERIMENT.$record	SECURITY:COMPOSITION.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ASSESSOR-EVENT.event_id	SECURITY:ASSESSOR-EVENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	SECURITY:ASSESSOR-EVENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	SECURITY:ASSESSOR-EVENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	SECURITY:ASSESSOR-EVENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	SECURITY:ASSESSOR-EVENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	SECURITY:ASSESSOR-EVENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	SECURITY:ASSESSOR-EVENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	SECURITY:ASSESSOR-EVENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	SECURITY:ASSESSOR-EVENT.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:QUALIFICATION.$record	SECURITY:ASSESSOR-EVENT.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:OBSERVER.coalition_id	SECURITY:OBSERVER.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBSERVER.policy_id	SECURITY:OBSERVER.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	SECURITY:OBSERVER.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	SECURITY:OBSERVER.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	SECURITY:OBSERVER.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.$record	SECURITY:OBSERVER.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:POLICY-APPLICABILITY.applicability_id	SECURITY:POLICY-APPLICABILITY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	SECURITY:POLICY-APPLICABILITY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	SECURITY:POLICY-APPLICABILITY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	SECURITY:POLICY-APPLICABILITY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	SECURITY:POLICY-APPLICABILITY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	SECURITY:POLICY-APPLICABILITY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	SECURITY:POLICY-APPLICABILITY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	SECURITY:POLICY-APPLICABILITY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	SECURITY:POLICY-APPLICABILITY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	SECURITY:POLICY-APPLICABILITY.$record	OWNS-RECORD-FIELD	STRUCTURAL
SECURITY:POLICY.$record	SECURITY:POLICY-APPLICABILITY.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:ENVELOPE.$record	SECURITY:POLICY-APPLICABILITY.$record	REQUIRED-SOURCE-OR-EVIDENCE-DEPENDENCY	SOURCE-ESTABLISHED
SECURITY:POLICY-APPLICABILITY.$record	CORE:AUTHORIZATION-HEADER.profile-sha256	BINDS-EXISTING-PROFILE-AND-CONTEXT	SOURCE-ESTABLISHED
SECURITY:POLICY.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.policy_digest	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.approved_by_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.profile_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.experiment_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.coalition_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.target_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.assumption_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.qualification_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.envelope_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.leakage_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.composition_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY.field_label_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.envelope_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.computation_model	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.capabilities	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.resource_limits	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.occurrence_limit	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.comparison_limit	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.attempt_limit	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.query_limits	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.validity_scope	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.secret_distribution	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ENVELOPE.state_distribution	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.leakage_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.source_refs	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.relationship_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.authorized_outcome_refs	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.schedule_rule	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:LEAKAGE.auxiliary_knowledge_rule	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.algorithm_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.field_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.parameters_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.encoding_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.domain_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.relation_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ALGORITHM.artifact_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.artifact_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.algorithm_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.owner	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.format_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.exact_bytes	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.digest	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARTIFACT.correspondence_evidence_ref	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.experiment_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.kind	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.coalition_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.target_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.algorithm_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.left_world	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.right_world	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.observation_rule	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.envelope_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.leakage_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:EXPERIMENT.maximum	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.assumption_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.statement	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.experiment_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.envelope_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.qualification_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.evidence_ref	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.approved_bound	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSUMPTION.premise_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.qualification_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.authority_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.assessor_identity	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.accepted_grammar	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.semantic_checker	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.competence_evidence	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.soundness_basis	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.result_schema	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:QUALIFICATION.unavailable_rule	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.field_label_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.surface_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.exposure	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.owner	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.coalition_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:FIELD-LABEL.visibility_evidence	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.argument_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.profile_digest	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.model_digest	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.obligation_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.experiment_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.assumption_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.premise_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.certificate_artifact_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.qualification_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.reduction_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.claimed_bound	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.envelope_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ARGUMENT.composition_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assessment_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.argument_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.qualification_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.invocation_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.exact_input_digest	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.complete_result	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.validated_bound	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.artifact_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.assumption_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSMENT.source_assertion_evidence	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.obligation_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.profile_digest	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.model_digest	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.kind	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.target_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.coalition_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.node_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.edge_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.experiment_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.disposition	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.argument_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBLIGATION.exact_evidence_refs	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composition_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.experiment_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.method	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.argument_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.multiplicities	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.theorem_ref	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.qualification_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:COMPOSITION.composed_bound	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.assessment_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.event_kind	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.input_bytes	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.output_bytes	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.predecessor_ids	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.control_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.owner	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:ASSESSOR-EVENT.attempt_ordinal	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.coalition_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.member_role_refs	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.protected_target_refs	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:OBSERVER.observation_evidence_refs	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.applicability_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.policy_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.profile_digest	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.mapping_digest	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.context_source	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.envelope_id	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.source_status_evidence	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.dependency_evidence	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.stage	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:membership	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:uniqueness	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:verifier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:privacy-assessor	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:admission	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:carrier	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:transport	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:public-chain-observer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:diagnostic-viewer	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:cache	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:evaluator	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:joint	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:commit	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	PRODUCER-ROLE:recovery	POTENTIAL-CUSTODY-UNKNOWN	STRUCTURAL
```

## Exact security-custody.tsv

```tsv
surface_id	potential_role	visibility	evidence_required
SECURITY:POLICY.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.policy_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.approved_by_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.approved_by_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.approved_by_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.approved_by_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.approved_by_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.approved_by_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.approved_by_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.profile_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.profile_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.profile_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.profile_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.profile_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.profile_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.profile_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.experiment_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.experiment_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.experiment_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.experiment_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.experiment_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.experiment_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.experiment_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.coalition_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.coalition_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.coalition_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.coalition_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.coalition_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.coalition_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.coalition_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.target_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.target_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.target_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.target_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.target_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.target_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.target_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.assumption_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.assumption_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.assumption_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.assumption_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.assumption_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.assumption_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.assumption_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.qualification_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.qualification_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.qualification_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.qualification_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.qualification_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.qualification_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.qualification_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.leakage_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.leakage_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.leakage_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.leakage_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.leakage_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.leakage_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.leakage_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.composition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.composition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.composition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.composition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.composition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.composition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.composition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.field_label_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.field_label_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.field_label_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.field_label_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.field_label_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.field_label_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY.field_label_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.computation_model	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.computation_model	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.computation_model	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.computation_model	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.computation_model	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.computation_model	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.computation_model	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.capabilities	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.capabilities	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.capabilities	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.capabilities	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.capabilities	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.capabilities	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.capabilities	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.resource_limits	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.resource_limits	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.resource_limits	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.resource_limits	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.resource_limits	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.resource_limits	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.resource_limits	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.occurrence_limit	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.occurrence_limit	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.occurrence_limit	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.occurrence_limit	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.occurrence_limit	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.occurrence_limit	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.occurrence_limit	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.comparison_limit	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.comparison_limit	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.comparison_limit	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.comparison_limit	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.comparison_limit	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.comparison_limit	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.comparison_limit	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.attempt_limit	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.attempt_limit	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.attempt_limit	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.attempt_limit	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.attempt_limit	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.attempt_limit	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.attempt_limit	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.query_limits	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.query_limits	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.query_limits	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.query_limits	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.query_limits	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.query_limits	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.query_limits	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.validity_scope	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.validity_scope	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.validity_scope	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.validity_scope	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.validity_scope	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.validity_scope	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.validity_scope	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.secret_distribution	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.secret_distribution	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.secret_distribution	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.secret_distribution	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.secret_distribution	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.secret_distribution	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.secret_distribution	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.state_distribution	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.state_distribution	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.state_distribution	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.state_distribution	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.state_distribution	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.state_distribution	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ENVELOPE.state_distribution	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.leakage_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.leakage_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.leakage_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.leakage_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.leakage_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.leakage_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.leakage_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.source_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.source_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.source_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.source_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.source_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.source_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.source_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.relationship_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.relationship_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.relationship_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.relationship_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.relationship_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.relationship_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.relationship_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.authorized_outcome_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.authorized_outcome_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.authorized_outcome_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.authorized_outcome_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.authorized_outcome_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.authorized_outcome_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.authorized_outcome_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.schedule_rule	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.schedule_rule	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.schedule_rule	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.schedule_rule	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.schedule_rule	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.schedule_rule	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.schedule_rule	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.auxiliary_knowledge_rule	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.auxiliary_knowledge_rule	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.auxiliary_knowledge_rule	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.auxiliary_knowledge_rule	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.auxiliary_knowledge_rule	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.auxiliary_knowledge_rule	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:LEAKAGE.auxiliary_knowledge_rule	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.algorithm_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.field_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.field_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.field_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.field_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.field_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.field_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.field_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.parameters_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.parameters_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.parameters_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.parameters_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.parameters_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.parameters_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.parameters_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.encoding_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.encoding_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.encoding_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.encoding_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.encoding_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.encoding_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.encoding_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.domain_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.domain_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.domain_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.domain_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.domain_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.domain_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.domain_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.relation_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.relation_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.relation_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.relation_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.relation_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.relation_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.relation_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.artifact_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.artifact_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.artifact_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.artifact_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.artifact_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.artifact_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ALGORITHM.artifact_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.artifact_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.artifact_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.artifact_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.artifact_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.artifact_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.artifact_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.artifact_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.algorithm_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.algorithm_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.algorithm_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.algorithm_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.algorithm_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.algorithm_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.algorithm_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.owner	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.owner	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.owner	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.owner	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.owner	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.owner	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.owner	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.format_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.format_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.format_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.format_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.format_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.format_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.format_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.exact_bytes	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.exact_bytes	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.exact_bytes	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.exact_bytes	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.exact_bytes	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.exact_bytes	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.exact_bytes	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.correspondence_evidence_ref	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.correspondence_evidence_ref	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.correspondence_evidence_ref	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.correspondence_evidence_ref	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.correspondence_evidence_ref	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.correspondence_evidence_ref	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARTIFACT.correspondence_evidence_ref	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.experiment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.experiment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.experiment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.experiment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.experiment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.experiment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.experiment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.kind	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.kind	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.kind	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.kind	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.kind	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.kind	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.kind	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.coalition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.coalition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.coalition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.coalition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.coalition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.coalition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.coalition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.target_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.target_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.target_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.target_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.target_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.target_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.target_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.algorithm_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.algorithm_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.algorithm_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.algorithm_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.algorithm_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.algorithm_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.algorithm_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.left_world	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.left_world	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.left_world	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.left_world	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.left_world	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.left_world	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.left_world	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.right_world	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.right_world	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.right_world	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.right_world	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.right_world	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.right_world	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.right_world	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.observation_rule	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.observation_rule	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.observation_rule	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.observation_rule	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.observation_rule	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.observation_rule	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.observation_rule	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.leakage_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.leakage_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.leakage_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.leakage_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.leakage_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.leakage_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.leakage_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.maximum	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.maximum	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.maximum	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.maximum	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.maximum	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.maximum	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:EXPERIMENT.maximum	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.assumption_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.assumption_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.assumption_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.assumption_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.assumption_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.assumption_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.assumption_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.statement	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.statement	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.statement	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.statement	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.statement	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.statement	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.statement	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.experiment_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.experiment_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.experiment_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.experiment_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.experiment_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.experiment_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.experiment_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.qualification_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.qualification_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.qualification_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.qualification_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.qualification_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.qualification_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.qualification_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.evidence_ref	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.evidence_ref	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.evidence_ref	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.evidence_ref	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.evidence_ref	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.evidence_ref	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.evidence_ref	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.approved_bound	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.approved_bound	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.approved_bound	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.approved_bound	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.approved_bound	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.approved_bound	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.approved_bound	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.premise_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.premise_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.premise_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.premise_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.premise_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.premise_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSUMPTION.premise_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.qualification_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.qualification_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.qualification_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.qualification_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.qualification_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.qualification_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.qualification_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.authority_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.authority_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.authority_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.authority_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.authority_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.authority_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.authority_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.assessor_identity	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.assessor_identity	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.assessor_identity	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.assessor_identity	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.assessor_identity	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.assessor_identity	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.assessor_identity	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.accepted_grammar	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.accepted_grammar	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.accepted_grammar	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.accepted_grammar	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.accepted_grammar	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.accepted_grammar	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.accepted_grammar	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.semantic_checker	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.semantic_checker	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.semantic_checker	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.semantic_checker	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.semantic_checker	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.semantic_checker	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.semantic_checker	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.competence_evidence	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.competence_evidence	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.competence_evidence	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.competence_evidence	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.competence_evidence	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.competence_evidence	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.competence_evidence	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.soundness_basis	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.soundness_basis	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.soundness_basis	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.soundness_basis	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.soundness_basis	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.soundness_basis	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.soundness_basis	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.result_schema	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.result_schema	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.result_schema	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.result_schema	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.result_schema	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.result_schema	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.result_schema	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.unavailable_rule	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.unavailable_rule	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.unavailable_rule	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.unavailable_rule	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.unavailable_rule	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.unavailable_rule	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:QUALIFICATION.unavailable_rule	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.field_label_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.field_label_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.field_label_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.field_label_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.field_label_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.field_label_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.field_label_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.surface_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.surface_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.surface_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.surface_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.surface_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.surface_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.surface_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.exposure	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.exposure	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.exposure	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.exposure	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.exposure	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.exposure	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.exposure	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.owner	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.owner	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.owner	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.owner	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.owner	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.owner	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.owner	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.coalition_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.coalition_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.coalition_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.coalition_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.coalition_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.coalition_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.coalition_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.visibility_evidence	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.visibility_evidence	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.visibility_evidence	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.visibility_evidence	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.visibility_evidence	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.visibility_evidence	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:FIELD-LABEL.visibility_evidence	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.argument_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.argument_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.argument_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.argument_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.argument_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.argument_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.argument_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.profile_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.profile_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.profile_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.profile_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.profile_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.profile_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.profile_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.model_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.model_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.model_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.model_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.model_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.model_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.model_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.obligation_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.obligation_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.obligation_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.obligation_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.obligation_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.obligation_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.obligation_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.experiment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.experiment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.experiment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.experiment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.experiment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.experiment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.experiment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.assumption_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.assumption_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.assumption_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.assumption_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.assumption_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.assumption_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.assumption_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.premise_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.premise_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.premise_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.premise_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.premise_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.premise_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.premise_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.certificate_artifact_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.certificate_artifact_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.certificate_artifact_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.certificate_artifact_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.certificate_artifact_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.certificate_artifact_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.certificate_artifact_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.qualification_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.qualification_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.qualification_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.qualification_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.qualification_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.qualification_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.qualification_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.reduction_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.reduction_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.reduction_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.reduction_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.reduction_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.reduction_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.reduction_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.claimed_bound	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.claimed_bound	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.claimed_bound	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.claimed_bound	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.claimed_bound	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.claimed_bound	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.claimed_bound	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.composition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.composition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.composition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.composition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.composition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.composition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ARGUMENT.composition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assessment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assessment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assessment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assessment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assessment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assessment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assessment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.argument_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.argument_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.argument_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.argument_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.argument_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.argument_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.argument_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.qualification_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.qualification_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.qualification_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.qualification_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.qualification_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.qualification_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.qualification_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.invocation_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.invocation_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.invocation_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.invocation_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.invocation_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.invocation_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.invocation_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.exact_input_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.exact_input_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.exact_input_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.exact_input_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.exact_input_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.exact_input_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.exact_input_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.complete_result	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.complete_result	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.complete_result	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.complete_result	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.complete_result	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.complete_result	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.complete_result	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.validated_bound	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.validated_bound	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.validated_bound	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.validated_bound	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.validated_bound	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.validated_bound	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.validated_bound	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.artifact_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.artifact_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.artifact_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.artifact_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.artifact_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.artifact_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.artifact_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assumption_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assumption_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assumption_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assumption_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assumption_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assumption_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.assumption_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.source_assertion_evidence	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.source_assertion_evidence	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.source_assertion_evidence	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.source_assertion_evidence	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.source_assertion_evidence	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.source_assertion_evidence	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSMENT.source_assertion_evidence	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.obligation_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.obligation_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.obligation_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.obligation_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.obligation_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.obligation_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.obligation_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.profile_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.profile_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.profile_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.profile_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.profile_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.profile_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.profile_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.model_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.model_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.model_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.model_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.model_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.model_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.model_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.kind	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.kind	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.kind	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.kind	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.kind	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.kind	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.kind	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.target_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.target_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.target_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.target_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.target_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.target_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.target_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.coalition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.coalition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.coalition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.coalition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.coalition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.coalition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.coalition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.node_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.node_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.node_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.node_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.node_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.node_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.node_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.edge_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.edge_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.edge_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.edge_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.edge_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.edge_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.edge_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.experiment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.experiment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.experiment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.experiment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.experiment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.experiment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.experiment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.disposition	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.disposition	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.disposition	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.disposition	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.disposition	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.disposition	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.disposition	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.argument_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.argument_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.argument_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.argument_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.argument_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.argument_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.argument_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.exact_evidence_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.exact_evidence_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.exact_evidence_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.exact_evidence_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.exact_evidence_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.exact_evidence_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBLIGATION.exact_evidence_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.experiment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.experiment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.experiment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.experiment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.experiment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.experiment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.experiment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.method	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.method	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.method	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.method	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.method	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.method	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.method	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.argument_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.argument_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.argument_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.argument_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.argument_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.argument_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.argument_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.multiplicities	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.multiplicities	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.multiplicities	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.multiplicities	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.multiplicities	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.multiplicities	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.multiplicities	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.theorem_ref	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.theorem_ref	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.theorem_ref	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.theorem_ref	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.theorem_ref	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.theorem_ref	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.theorem_ref	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.qualification_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.qualification_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.qualification_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.qualification_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.qualification_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.qualification_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.qualification_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composed_bound	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composed_bound	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composed_bound	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composed_bound	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composed_bound	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composed_bound	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:COMPOSITION.composed_bound	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.assessment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.assessment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.assessment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.assessment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.assessment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.assessment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.assessment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_kind	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_kind	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_kind	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_kind	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_kind	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_kind	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.event_kind	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.input_bytes	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.input_bytes	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.input_bytes	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.input_bytes	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.input_bytes	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.input_bytes	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.input_bytes	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.output_bytes	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.output_bytes	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.output_bytes	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.output_bytes	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.output_bytes	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.output_bytes	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.output_bytes	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.predecessor_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.predecessor_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.predecessor_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.predecessor_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.predecessor_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.predecessor_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.predecessor_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.control_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.control_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.control_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.control_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.control_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.control_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.control_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.owner	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.owner	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.owner	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.owner	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.owner	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.owner	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.owner	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.attempt_ordinal	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.attempt_ordinal	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.attempt_ordinal	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.attempt_ordinal	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.attempt_ordinal	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.attempt_ordinal	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:ASSESSOR-EVENT.attempt_ordinal	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.coalition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.coalition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.coalition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.coalition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.coalition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.coalition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.coalition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.member_role_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.member_role_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.member_role_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.member_role_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.member_role_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.member_role_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.member_role_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.protected_target_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.protected_target_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.protected_target_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.protected_target_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.protected_target_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.protected_target_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.protected_target_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.observation_evidence_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.observation_evidence_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.observation_evidence_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.observation_evidence_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.observation_evidence_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.observation_evidence_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:OBSERVER.observation_evidence_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.applicability_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.applicability_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.applicability_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.applicability_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.applicability_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.applicability_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.applicability_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.profile_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.profile_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.profile_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.profile_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.profile_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.profile_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.profile_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.mapping_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.mapping_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.mapping_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.mapping_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.mapping_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.mapping_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.mapping_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.context_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.context_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.context_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.context_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.context_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.context_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.context_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.source_status_evidence	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.source_status_evidence	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.source_status_evidence	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.source_status_evidence	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.source_status_evidence	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.source_status_evidence	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.source_status_evidence	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.dependency_evidence	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.dependency_evidence	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.dependency_evidence	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.dependency_evidence	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.dependency_evidence	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.dependency_evidence	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.dependency_evidence	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.stage	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.stage	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.stage	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.stage	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.stage	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.stage	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.stage	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY:POLICY-APPLICABILITY.attempt_ordinal	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
```

## Exact qualification-interface.tsv

```tsv
operation	phase	exact_inputs	required_output	inability	authority_boundary
policy-read	STATIC	Exact profile, policy reference and independently governing source	Exact canonical policy and qualified ownership/approval evidence	No computational admission	External source qualification under inherited ReadObject/source laws; not PE-TSE host call
assessor-qualification	STATIC	Exact grammar/checker/result schema, authority and competence basis	Source-qualified assessor contract; no self appointment	No usable security assessment	External source qualification under inherited ReadObject/source laws; not PE-TSE host call
argument-assessment	EVIDENCE	Exact argument, policy, artifacts, experiment, premises and envelope	VALID with exact bound; INVALID; or UNAVAILABLE, with invocation/assertion evidence	NOT-ESTABLISHED; never VALID	External source qualification under inherited ReadObject/source laws; not PE-TSE host call
observer-validation	STATIC-AND-EVIDENCE	Full record universe, all required coalitions and actor/endpoint bindings	Exact complete view; source/visibility/coverage evidence	Unknown visibility blocks admission	External source qualification under inherited ReadObject/source laws; not PE-TSE host call
policy-applicability	E-AND-EVERY-GATE	Existing profile/mapping/context, source status and entire envelope	Qualified current applicability/source status; actual dependency evidence	No A/E/D at admission; invalid/inability at existing validation boundary later	External source qualification under inherited ReadObject/source laws; not PE-TSE host call
composition	STATIC-AND-EVIDENCE	Regenerated obligations, VALID assessments and exact multiplicities	Exact rational bound per experiment plus justified whole-view coverage	NOT-ESTABLISHED; no budget PASS	External source qualification under inherited ReadObject/source laws; not PE-TSE host call
non-vacuity-validation	STATIC-AND-APPLICABILITY	Exact source-governed policy, world/envelope/target/coalition/model definitions and qualification contracts	Qualified VALID establishing nonempty genuine scope and whole-class/view coverage; INVALID; or UNAVAILABLE with exact input/assertion binding	No computational discharge; inherited scope/universe/authority failure distinctions	External source qualification under inherited source laws; existing assessor/source evidence classes, not PE-TSE host call
```

## Final-member grammar

The S90 governing PRIVACY member is canonical JSON with exactly: format (PE-G4-PRIVACY-PROFILE-V4), profile_id, format_source, format_source_sha256, policy_sources, components, public_output, declaration_input_sha256, procedures_sha256, model, evidence_contract, appointment, security_contract. The S88 fields retain their exact meanings; policy_sources additionally includes S89/S90. model is the independently regenerated complete instance model, not the schema declaration. security_contract is exactly {contract_sha256, policy, schema_sha256, qualification_interface_sha256, experiments, assumptions, qualification_contracts, operating_envelope, leakage, obligations, composition_rules}. The nested record arrays and directory joins follow the exact registers and governing policy. Actual argument/assessment/invocation/occurrence evidence remains outside immutable bytes and binds the final member digest. The inherited three-member outer framing and signed V2 evidence preimages are unchanged. The governing policy is supplied independently before final immutable construction; its absence prohibits a member, not just admission. No V4 production constructor is claimed in this documentary review packet.

## Exact documentary subprocedure budget.py

```python
"""Exact UNION budget calculation. Does not qualify source facts or grant admission."""
from fractions import Fraction

def rational(value):
 if type(value) is not list or len(value)!=2 or any(type(x) is not int for x in value) or value[1]<=0 or not 0<=value[0]<=value[1]:raise ValueError('canonical probability pair')
 from math import gcd
 if gcd(*value)!=1:raise ValueError('noncanonical rational')
 return Fraction(*value)

def policy_maximum(value):
 limit=rational(value)
 if limit>=1:raise ValueError('computational maximum must be strictly below one')
 return limit

def union_budget(terms,maximum):
 limit=policy_maximum(maximum)
 if type(terms) is not list or not terms:raise ValueError('complete nonempty term list required')
 total=Fraction(0);seen=set()
 for t in terms:
  if type(t) is not dict or set(t)!={'argument_id','bound','multiplicity'}:raise ValueError('exact budget term')
  if type(t['argument_id']) is not str or not t['argument_id'] or t['argument_id'] in seen:raise ValueError('term identity')
  seen.add(t['argument_id'])
  if type(t['multiplicity']) is not int or t['multiplicity']<=0:raise ValueError('multiplicity')
  total+=rational(t['bound'])*t['multiplicity']
 total=min(total,Fraction(1))
 return {'bound':[total.numerator,total.denominator],'budget_result':'WITHIN' if total<=limit else 'EXCEEDED','source_facts_qualified':False,'profile_admitted':False}
```

## Exact documentary subprocedure assemble_definition.py

```python
"""S90 definition declaration and schema graph. No dummy governing policy/profile."""
from pathlib import Path
import csv,json,hashlib,runpy
O=Path(__file__).resolve().parents[1]
D=O/'definition-completion'
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()
def rows(name):return list(csv.DictReader((D/name).open(),delimiter='\t'))
def declaration():
 paths=['sources/PE-G4-SOURCE-S90.md','definition-completion/ACCEPTANCE-CONTRACT.txt','definition-completion/security-fields.tsv','definition-completion/security-relations.tsv','definition-completion/security-custody.tsv','definition-completion/qualification-interface.tsv','definition-completion/budget.py','definition-completion/assemble_definition.py','definition-completion/v4_record_grammar.py','definition-completion/E287-SOURCE-DETERMINED-CORRECTION.txt','definition-completion/security-framing-fields.tsv','definition-completion/framing-custody.tsv','definition-completion/NONVACUITY-CONTRACT.txt']
 fields=rows('security-fields.tsv');rels=rows('security-relations.tsv')
 base=runpy.run_path(str(O/'privacy/expand_privacy.py'))['construct']()
 schemas=sorted({f['schema'] for f in fields})
 nodes=[{'id':f['surface_id'],'kind':'SECURITY-FIELD-TEMPLATE','owner':'PE-G4-SOURCE-S90#schemas','exposure':'UNKNOWN','reuse':'NONE'} for f in fields]
 nodes += [{'id':'SECURITY:'+s+'.$record','kind':'SECURITY-RECORD-TEMPLATE','owner':'PE-G4-SOURCE-S90#schemas','exposure':'UNKNOWN','reuse':'NONE'} for s in schemas]
 # This graph is a schema overapproximation. Repeated records must be expanded
 # using exact source-established directories; template counts are not occurrence counts.
 return {'format':'PE-G4-DEFINITION-DECLARATION-V4','status':'UNINSTANTIATED-DEFINITION-NOT-GOVERNING-PRIVACY','source':'PE-G4-SOURCE-S90','input_sha256':{p:hashlib.sha256((O/p).read_bytes()).hexdigest() for p in paths},'prior_graph':{'tokens':base[2],'structural_edges':base[3],'potential_equality_rule':'left.arbitrary OR right.arbitrary OR equal symbolic_digest'},'security_templates':nodes,'framing_templates':rows('security-framing-fields.tsv'),'framing_custody':rows('framing-custody.tsv'),'security_relations':rels,'security_fields':fields,'record_instantiation':'Exact independently source-validated directory for every schema; no empty defaults; replicate every record in both contexts and every custody/equality edge','owning_header_join':'CORE:AUTHORIZATION-HEADER.profile-sha256','governing_policy':None,'source_appointment':None,'privacy_admission':False}

def instantiate_security(directory):
 """Mechanical expansion only. Caller directories are not authenticated by this function."""
 fields=rows('security-fields.tsv');rels=rows('security-relations.tsv');schemas={f['schema'] for f in fields}
 if type(directory) is not dict or set(directory)!=schemas:raise ValueError('complete directory required')
 one={'POLICY','ENVELOPE','LEAKAGE'}
 for s,ids in directory.items():
  if type(ids) is not list or not ids or any(type(x) is not str or not x or '::' in x for x in ids) or len(set(ids))!=len(ids) or (s in one and len(ids)!=1):raise ValueError('invalid record directory')
 tokens=[];by={}
 for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
  for s in sorted(schemas):
   for record in directory[s]:
    for surface in ['SECURITY:'+s+'.$record']+[f['surface_id'] for f in fields if f['schema']==s]:
     token={'id':context+'::'+surface+'::'+record,'surface':surface,'record':record,'context':context,'exposure':'UNKNOWN','reuse':'NONE','arbitrary':True}
     tokens.append(token);by.setdefault((context,surface),[]).append(token['id'])
 edges=[]
 for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
  for r in rels:
   left=by[(context,r['from_node'])]
   right=by.get((context,r['to_node']),[context+'::'+r['to_node']])
   for a in left:
    for b in right:edges.append([a,b,r['relation'],r['origin']])
 return {'tokens':tokens,'structural_edges':edges,'equality_policy':'All inherited pairs retained; every arbitrary security token potentially equals every old/new token','directory_authenticated':False,'profile_admitted':False}

if __name__=='__main__':
 (O/'definition-completion/DEFINITION-DECLARATION-V4.json').write_bytes(canonical(declaration()))
```

The exact source-owned policy and assessor are realization/profile inputs. The independently governing source validates approval/competence and assertion binding; it is not appointed by this profile. The admission law is fully parameterized by those inputs, and their absence is failure to instantiate/admit this selected profile. This does not permit software to invent thresholds, experiments, leakage or assessor semantics.

## Custody, instantiation and applicability clarification

All POTENTIAL-CUSTODY-UNKNOWN links refer to retained documentary role nodes and appoint no actor. Unknown visibility prohibits admission. Every new arbitrary security token participates in the inherited full potential-equality rule with every old/new token, including arbitrary-to-constant pairs. Source-established relation expansions are retained conservatively across record instances; exact record-field ownership and directory joins are validated separately and cannot be inferred from this overapproximation.

Security-envelope applicability is a source-validation duty at static admission, E and both gate phases wherever the governing policy requires it. The selected profile may use the existing two material predicates only when independently source-qualified applicability proves that no additional changing material condition is needed. If a new policy needs a third material predicate, runtime accounting state, new order or coordinate, this profile is unsuitable and must be explicitly revised before admission. A generic policy reference is not a silent extension of R or an extra BOOL3 result. All external reads and assessor events contributing to E/D must be included in actual owning dependency/replay/fresh evidence, even though the pure PE-TSE program performs no host call.

## Qualified-result absence and signed-evidence integration

Actual security assessment records use the explicit V2 owning-record applicability/availability/presence framing already defined for source evidence. UNAVAILABLE does not carry a fabricated zero bound or a VALID certificate. An inapplicable schema/directory requires source-established justification; the conservative documentary instantiator rejects all empty directories and is not the production validator of justified inapplicability. Every actual parsed artifact subfield and every source call/error/retry/cache surface required by its qualified grammar must extend the instantiated model before admission.

The V2 evidence.tsv/tokens.tsv/links.tsv/signature.txt envelope and their signature/object-digest preimages remain exact. S90 extends the V4 owning-schema register and its token/link universe, not those preimages. All new records, argument/assessment inputs/results, source/visibility/coverage evidence and exact parser-qualified artifacts must be bound by their exact owning tokens/links and final profile digest. The old V2/V3 validators do not validate this extended semantic universe; their tests are retained historical construction checks. No production integrated V4 admission implementation or independent source qualification is supplied by this documentary candidate.


<a id="e287-framing"></a>
## Engineering[287] explicit framing register

BOOL is a JSON Boolean. ENUM-RECORD-STATUS is PRESENT,UNAVAILABLE,INAPPLICABLE. NULL-OR-SOURCE-REF is JSON null or the exact S90 SOURCE-REF. LITERAL-FORMAT is PE-G4-SECURITY-RECORDS-V4. Directory/count/presence values are deterministically extracted from exact parsed record bytes; their validity/visibility remains independently qualified.

## Exact security-framing-fields.tsv

```tsv
surface_id	schema	field	type	cardinality	owner_source_id	owner_anchor	exposure	reuse	phase
SECURITY-FRAME:ROOT.format	ROOT	format	LITERAL-FORMAT	ONE	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ROOT.profile_digest	ROOT	profile_digest	DIGEST	ONE	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ROOT.phase	ROOT	phase	ENUM-STAGE	ONE	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ROOT.schema_directory	ROOT	schema_directory	LIST-ID	ONE	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.status	ALGORITHM	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.justification	ALGORITHM	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.instance_count	ALGORITHM	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.record_directory	ALGORITHM	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.status	ARGUMENT	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.justification	ARGUMENT	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.instance_count	ARGUMENT	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.record_directory	ARGUMENT	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARTIFACT.status	ARTIFACT	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARTIFACT.justification	ARTIFACT	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARTIFACT.instance_count	ARTIFACT	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARTIFACT.record_directory	ARTIFACT	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.status	ASSESSMENT	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.justification	ASSESSMENT	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.instance_count	ASSESSMENT	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.record_directory	ASSESSMENT	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.status	ASSESSOR-EVENT	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.justification	ASSESSOR-EVENT	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.instance_count	ASSESSOR-EVENT	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.record_directory	ASSESSOR-EVENT	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.status	ASSUMPTION	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.justification	ASSUMPTION	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.instance_count	ASSUMPTION	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.record_directory	ASSUMPTION	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.status	COMPOSITION	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.justification	COMPOSITION	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.instance_count	COMPOSITION	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.record_directory	COMPOSITION	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.status	ENVELOPE	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.justification	ENVELOPE	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.instance_count	ENVELOPE	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.record_directory	ENVELOPE	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.status	EXPERIMENT	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.justification	EXPERIMENT	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.instance_count	EXPERIMENT	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.record_directory	EXPERIMENT	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:FIELD-LABEL.status	FIELD-LABEL	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:FIELD-LABEL.justification	FIELD-LABEL	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:FIELD-LABEL.instance_count	FIELD-LABEL	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:FIELD-LABEL.record_directory	FIELD-LABEL	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:LEAKAGE.status	LEAKAGE	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:LEAKAGE.justification	LEAKAGE	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:LEAKAGE.instance_count	LEAKAGE	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:LEAKAGE.record_directory	LEAKAGE	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.status	OBLIGATION	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.justification	OBLIGATION	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.instance_count	OBLIGATION	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.record_directory	OBLIGATION	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBSERVER.status	OBSERVER	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBSERVER.justification	OBSERVER	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBSERVER.instance_count	OBSERVER	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBSERVER.record_directory	OBSERVER	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.status	POLICY	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.justification	POLICY	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.instance_count	POLICY	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.record_directory	POLICY	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.status	POLICY-APPLICABILITY	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.justification	POLICY-APPLICABILITY	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.instance_count	POLICY-APPLICABILITY	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.record_directory	POLICY-APPLICABILITY	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.status	QUALIFICATION	status	ENUM-RECORD-STATUS	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.justification	QUALIFICATION	justification	NULL-OR-SOURCE-REF	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.instance_count	QUALIFICATION	instance_count	UINT	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.record_directory	QUALIFICATION	record_directory	LIST-ID	ONE-PER-SCHEMA-DIRECTORY	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:policy_id	POLICY	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:policy_source	POLICY	present:policy_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:policy_digest	POLICY	present:policy_digest	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:approved_by_source	POLICY	present:approved_by_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:profile_id	POLICY	present:profile_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:experiment_ids	POLICY	present:experiment_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:coalition_ids	POLICY	present:coalition_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:target_ids	POLICY	present:target_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:assumption_ids	POLICY	present:assumption_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:qualification_ids	POLICY	present:qualification_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:envelope_id	POLICY	present:envelope_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:leakage_id	POLICY	present:leakage_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:composition_id	POLICY	present:composition_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY.present:field_label_ids	POLICY	present:field_label_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:envelope_id	ENVELOPE	present:envelope_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:policy_id	ENVELOPE	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:computation_model	ENVELOPE	present:computation_model	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:capabilities	ENVELOPE	present:capabilities	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:resource_limits	ENVELOPE	present:resource_limits	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:occurrence_limit	ENVELOPE	present:occurrence_limit	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:comparison_limit	ENVELOPE	present:comparison_limit	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:attempt_limit	ENVELOPE	present:attempt_limit	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:query_limits	ENVELOPE	present:query_limits	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:validity_scope	ENVELOPE	present:validity_scope	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:secret_distribution	ENVELOPE	present:secret_distribution	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ENVELOPE.present:state_distribution	ENVELOPE	present:state_distribution	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:LEAKAGE.present:leakage_id	LEAKAGE	present:leakage_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:LEAKAGE.present:policy_id	LEAKAGE	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:LEAKAGE.present:source_refs	LEAKAGE	present:source_refs	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:LEAKAGE.present:relationship_ids	LEAKAGE	present:relationship_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:LEAKAGE.present:authorized_outcome_refs	LEAKAGE	present:authorized_outcome_refs	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:LEAKAGE.present:schedule_rule	LEAKAGE	present:schedule_rule	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:LEAKAGE.present:auxiliary_knowledge_rule	LEAKAGE	present:auxiliary_knowledge_rule	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.present:algorithm_id	ALGORITHM	present:algorithm_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.present:policy_id	ALGORITHM	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.present:algorithm_source	ALGORITHM	present:algorithm_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.present:field_source	ALGORITHM	present:field_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.present:parameters_source	ALGORITHM	present:parameters_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.present:encoding_source	ALGORITHM	present:encoding_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.present:domain_source	ALGORITHM	present:domain_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.present:relation_source	ALGORITHM	present:relation_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ALGORITHM.present:artifact_ids	ALGORITHM	present:artifact_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARTIFACT.present:artifact_id	ARTIFACT	present:artifact_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARTIFACT.present:algorithm_id	ARTIFACT	present:algorithm_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARTIFACT.present:owner	ARTIFACT	present:owner	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARTIFACT.present:format_source	ARTIFACT	present:format_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARTIFACT.present:exact_bytes	ARTIFACT	present:exact_bytes	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARTIFACT.present:digest	ARTIFACT	present:digest	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARTIFACT.present:correspondence_evidence_ref	ARTIFACT	present:correspondence_evidence_ref	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:experiment_id	EXPERIMENT	present:experiment_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:policy_id	EXPERIMENT	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:kind	EXPERIMENT	present:kind	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:coalition_id	EXPERIMENT	present:coalition_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:target_id	EXPERIMENT	present:target_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:algorithm_ids	EXPERIMENT	present:algorithm_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:left_world	EXPERIMENT	present:left_world	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:right_world	EXPERIMENT	present:right_world	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:observation_rule	EXPERIMENT	present:observation_rule	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:envelope_id	EXPERIMENT	present:envelope_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:leakage_id	EXPERIMENT	present:leakage_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:EXPERIMENT.present:maximum	EXPERIMENT	present:maximum	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.present:assumption_id	ASSUMPTION	present:assumption_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.present:policy_id	ASSUMPTION	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.present:statement	ASSUMPTION	present:statement	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.present:experiment_ids	ASSUMPTION	present:experiment_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.present:envelope_id	ASSUMPTION	present:envelope_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.present:qualification_id	ASSUMPTION	present:qualification_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.present:evidence_ref	ASSUMPTION	present:evidence_ref	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.present:approved_bound	ASSUMPTION	present:approved_bound	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSUMPTION.present:premise_ids	ASSUMPTION	present:premise_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.present:qualification_id	QUALIFICATION	present:qualification_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.present:policy_id	QUALIFICATION	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.present:authority_source	QUALIFICATION	present:authority_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.present:assessor_identity	QUALIFICATION	present:assessor_identity	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.present:accepted_grammar	QUALIFICATION	present:accepted_grammar	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.present:semantic_checker	QUALIFICATION	present:semantic_checker	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.present:competence_evidence	QUALIFICATION	present:competence_evidence	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.present:soundness_basis	QUALIFICATION	present:soundness_basis	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.present:result_schema	QUALIFICATION	present:result_schema	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:QUALIFICATION.present:unavailable_rule	QUALIFICATION	present:unavailable_rule	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:FIELD-LABEL.present:field_label_id	FIELD-LABEL	present:field_label_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:FIELD-LABEL.present:policy_id	FIELD-LABEL	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:FIELD-LABEL.present:surface_id	FIELD-LABEL	present:surface_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:FIELD-LABEL.present:exposure	FIELD-LABEL	present:exposure	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:FIELD-LABEL.present:owner	FIELD-LABEL	present:owner	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:FIELD-LABEL.present:coalition_ids	FIELD-LABEL	present:coalition_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:FIELD-LABEL.present:visibility_evidence	FIELD-LABEL	present:visibility_evidence	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:argument_id	ARGUMENT	present:argument_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:policy_id	ARGUMENT	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:profile_digest	ARGUMENT	present:profile_digest	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:model_digest	ARGUMENT	present:model_digest	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:obligation_ids	ARGUMENT	present:obligation_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:experiment_id	ARGUMENT	present:experiment_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:assumption_ids	ARGUMENT	present:assumption_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:premise_ids	ARGUMENT	present:premise_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:certificate_artifact_ids	ARGUMENT	present:certificate_artifact_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:qualification_id	ARGUMENT	present:qualification_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:reduction_source	ARGUMENT	present:reduction_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:claimed_bound	ARGUMENT	present:claimed_bound	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:envelope_id	ARGUMENT	present:envelope_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ARGUMENT.present:composition_id	ARGUMENT	present:composition_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.present:assessment_id	ASSESSMENT	present:assessment_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.present:argument_id	ASSESSMENT	present:argument_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.present:qualification_id	ASSESSMENT	present:qualification_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.present:invocation_source	ASSESSMENT	present:invocation_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.present:exact_input_digest	ASSESSMENT	present:exact_input_digest	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.present:complete_result	ASSESSMENT	present:complete_result	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.present:validated_bound	ASSESSMENT	present:validated_bound	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.present:artifact_ids	ASSESSMENT	present:artifact_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.present:assumption_ids	ASSESSMENT	present:assumption_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSMENT.present:source_assertion_evidence	ASSESSMENT	present:source_assertion_evidence	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:obligation_id	OBLIGATION	present:obligation_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:profile_digest	OBLIGATION	present:profile_digest	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:model_digest	OBLIGATION	present:model_digest	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:kind	OBLIGATION	present:kind	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:target_ids	OBLIGATION	present:target_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:coalition_id	OBLIGATION	present:coalition_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:node_ids	OBLIGATION	present:node_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:edge_ids	OBLIGATION	present:edge_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:experiment_id	OBLIGATION	present:experiment_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:disposition	OBLIGATION	present:disposition	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:argument_ids	OBLIGATION	present:argument_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBLIGATION.present:exact_evidence_refs	OBLIGATION	present:exact_evidence_refs	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.present:composition_id	COMPOSITION	present:composition_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.present:policy_id	COMPOSITION	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.present:experiment_id	COMPOSITION	present:experiment_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.present:method	COMPOSITION	present:method	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.present:argument_ids	COMPOSITION	present:argument_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.present:multiplicities	COMPOSITION	present:multiplicities	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.present:theorem_ref	COMPOSITION	present:theorem_ref	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.present:qualification_id	COMPOSITION	present:qualification_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:COMPOSITION.present:composed_bound	COMPOSITION	present:composed_bound	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.present:event_id	ASSESSOR-EVENT	present:event_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.present:assessment_id	ASSESSOR-EVENT	present:assessment_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.present:event_kind	ASSESSOR-EVENT	present:event_kind	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.present:input_bytes	ASSESSOR-EVENT	present:input_bytes	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.present:output_bytes	ASSESSOR-EVENT	present:output_bytes	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.present:predecessor_ids	ASSESSOR-EVENT	present:predecessor_ids	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.present:control_source	ASSESSOR-EVENT	present:control_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.present:owner	ASSESSOR-EVENT	present:owner	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:ASSESSOR-EVENT.present:attempt_ordinal	ASSESSOR-EVENT	present:attempt_ordinal	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBSERVER.present:coalition_id	OBSERVER	present:coalition_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBSERVER.present:policy_id	OBSERVER	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBSERVER.present:member_role_refs	OBSERVER	present:member_role_refs	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBSERVER.present:protected_target_refs	OBSERVER	present:protected_target_refs	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:OBSERVER.present:observation_evidence_refs	OBSERVER	present:observation_evidence_refs	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.present:applicability_id	POLICY-APPLICABILITY	present:applicability_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.present:policy_id	POLICY-APPLICABILITY	present:policy_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.present:profile_digest	POLICY-APPLICABILITY	present:profile_digest	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.present:mapping_digest	POLICY-APPLICABILITY	present:mapping_digest	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.present:context_source	POLICY-APPLICABILITY	present:context_source	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.present:envelope_id	POLICY-APPLICABILITY	present:envelope_id	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.present:source_status_evidence	POLICY-APPLICABILITY	present:source_status_evidence	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.present:dependency_evidence	POLICY-APPLICABILITY	present:dependency_evidence	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.present:stage	POLICY-APPLICABILITY	present:stage	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
SECURITY-FRAME:POLICY-APPLICABILITY.present:attempt_ordinal	POLICY-APPLICABILITY	present:attempt_ordinal	BOOL	ONE-PER-RECORD-FIELD	PE-G4-SOURCE-S90	e287-framing	UNKNOWN	NONE	STATIC-AND-EVIDENCE
```

## Exact framing-custody.tsv

```tsv
surface_id	potential_role	visibility	evidence_required
SECURITY-FRAME:ROOT.format	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.format	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.format	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.format	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.format	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.format	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.format	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.profile_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.profile_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.profile_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.profile_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.profile_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.profile_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.profile_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.phase	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.phase	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.phase	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.phase	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.phase	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.phase	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.phase	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.schema_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.schema_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.schema_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.schema_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.schema_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.schema_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ROOT.schema_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.status	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.status	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.status	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.status	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.status	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.status	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.status	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.justification	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.justification	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.justification	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.justification	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.justification	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.justification	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.justification	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.instance_count	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.instance_count	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.instance_count	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.instance_count	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.instance_count	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.instance_count	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.instance_count	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.record_directory	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.record_directory	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.record_directory	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.record_directory	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.record_directory	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.record_directory	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.record_directory	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:policy_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:approved_by_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:approved_by_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:approved_by_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:approved_by_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:approved_by_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:approved_by_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:approved_by_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:profile_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:profile_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:profile_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:profile_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:profile_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:profile_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:profile_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:experiment_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:experiment_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:experiment_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:experiment_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:experiment_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:experiment_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:experiment_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:coalition_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:coalition_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:coalition_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:coalition_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:coalition_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:coalition_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:coalition_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:target_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:target_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:target_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:target_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:target_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:target_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:target_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:assumption_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:assumption_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:assumption_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:assumption_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:assumption_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:assumption_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:assumption_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:qualification_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:qualification_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:qualification_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:qualification_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:qualification_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:qualification_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:qualification_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:leakage_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:leakage_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:leakage_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:leakage_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:leakage_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:leakage_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:leakage_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:composition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:composition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:composition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:composition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:composition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:composition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:composition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:field_label_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:field_label_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:field_label_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:field_label_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:field_label_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:field_label_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY.present:field_label_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:computation_model	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:computation_model	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:computation_model	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:computation_model	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:computation_model	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:computation_model	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:computation_model	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:capabilities	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:capabilities	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:capabilities	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:capabilities	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:capabilities	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:capabilities	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:capabilities	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:resource_limits	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:resource_limits	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:resource_limits	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:resource_limits	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:resource_limits	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:resource_limits	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:resource_limits	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:occurrence_limit	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:occurrence_limit	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:occurrence_limit	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:occurrence_limit	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:occurrence_limit	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:occurrence_limit	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:occurrence_limit	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:comparison_limit	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:comparison_limit	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:comparison_limit	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:comparison_limit	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:comparison_limit	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:comparison_limit	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:comparison_limit	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:attempt_limit	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:attempt_limit	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:attempt_limit	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:attempt_limit	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:attempt_limit	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:attempt_limit	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:attempt_limit	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:query_limits	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:query_limits	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:query_limits	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:query_limits	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:query_limits	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:query_limits	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:query_limits	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:validity_scope	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:validity_scope	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:validity_scope	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:validity_scope	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:validity_scope	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:validity_scope	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:validity_scope	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:secret_distribution	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:secret_distribution	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:secret_distribution	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:secret_distribution	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:secret_distribution	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:secret_distribution	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:secret_distribution	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:state_distribution	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:state_distribution	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:state_distribution	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:state_distribution	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:state_distribution	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:state_distribution	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ENVELOPE.present:state_distribution	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:leakage_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:leakage_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:leakage_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:leakage_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:leakage_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:leakage_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:leakage_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:source_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:source_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:source_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:source_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:source_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:source_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:source_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:relationship_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:relationship_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:relationship_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:relationship_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:relationship_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:relationship_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:relationship_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:authorized_outcome_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:authorized_outcome_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:authorized_outcome_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:authorized_outcome_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:authorized_outcome_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:authorized_outcome_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:authorized_outcome_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:schedule_rule	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:schedule_rule	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:schedule_rule	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:schedule_rule	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:schedule_rule	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:schedule_rule	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:schedule_rule	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:auxiliary_knowledge_rule	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:auxiliary_knowledge_rule	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:auxiliary_knowledge_rule	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:auxiliary_knowledge_rule	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:auxiliary_knowledge_rule	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:auxiliary_knowledge_rule	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:LEAKAGE.present:auxiliary_knowledge_rule	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:algorithm_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:field_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:field_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:field_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:field_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:field_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:field_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:field_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:parameters_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:parameters_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:parameters_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:parameters_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:parameters_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:parameters_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:parameters_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:encoding_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:encoding_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:encoding_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:encoding_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:encoding_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:encoding_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:encoding_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:domain_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:domain_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:domain_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:domain_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:domain_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:domain_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:domain_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:relation_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:relation_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:relation_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:relation_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:relation_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:relation_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:relation_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:artifact_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:artifact_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:artifact_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:artifact_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:artifact_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:artifact_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ALGORITHM.present:artifact_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:artifact_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:artifact_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:artifact_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:artifact_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:artifact_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:artifact_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:artifact_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:algorithm_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:algorithm_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:algorithm_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:algorithm_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:algorithm_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:algorithm_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:algorithm_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:owner	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:owner	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:owner	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:owner	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:owner	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:owner	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:owner	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:format_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:format_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:format_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:format_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:format_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:format_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:format_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:exact_bytes	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:exact_bytes	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:exact_bytes	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:exact_bytes	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:exact_bytes	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:exact_bytes	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:exact_bytes	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:correspondence_evidence_ref	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:correspondence_evidence_ref	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:correspondence_evidence_ref	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:correspondence_evidence_ref	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:correspondence_evidence_ref	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:correspondence_evidence_ref	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARTIFACT.present:correspondence_evidence_ref	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:experiment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:experiment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:experiment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:experiment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:experiment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:experiment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:experiment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:kind	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:kind	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:kind	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:kind	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:kind	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:kind	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:kind	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:coalition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:coalition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:coalition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:coalition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:coalition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:coalition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:coalition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:target_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:target_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:target_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:target_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:target_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:target_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:target_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:algorithm_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:algorithm_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:algorithm_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:algorithm_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:algorithm_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:algorithm_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:algorithm_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:left_world	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:left_world	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:left_world	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:left_world	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:left_world	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:left_world	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:left_world	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:right_world	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:right_world	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:right_world	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:right_world	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:right_world	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:right_world	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:right_world	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:observation_rule	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:observation_rule	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:observation_rule	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:observation_rule	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:observation_rule	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:observation_rule	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:observation_rule	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:leakage_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:leakage_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:leakage_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:leakage_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:leakage_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:leakage_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:leakage_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:maximum	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:maximum	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:maximum	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:maximum	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:maximum	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:maximum	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:EXPERIMENT.present:maximum	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:assumption_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:assumption_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:assumption_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:assumption_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:assumption_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:assumption_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:assumption_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:statement	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:statement	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:statement	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:statement	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:statement	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:statement	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:statement	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:experiment_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:experiment_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:experiment_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:experiment_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:experiment_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:experiment_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:experiment_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:qualification_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:qualification_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:qualification_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:qualification_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:qualification_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:qualification_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:qualification_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:evidence_ref	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:evidence_ref	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:evidence_ref	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:evidence_ref	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:evidence_ref	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:evidence_ref	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:evidence_ref	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:approved_bound	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:approved_bound	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:approved_bound	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:approved_bound	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:approved_bound	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:approved_bound	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:approved_bound	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:premise_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:premise_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:premise_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:premise_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:premise_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:premise_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSUMPTION.present:premise_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:qualification_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:qualification_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:qualification_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:qualification_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:qualification_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:qualification_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:qualification_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:authority_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:authority_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:authority_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:authority_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:authority_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:authority_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:authority_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:assessor_identity	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:assessor_identity	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:assessor_identity	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:assessor_identity	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:assessor_identity	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:assessor_identity	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:assessor_identity	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:accepted_grammar	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:accepted_grammar	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:accepted_grammar	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:accepted_grammar	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:accepted_grammar	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:accepted_grammar	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:accepted_grammar	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:semantic_checker	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:semantic_checker	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:semantic_checker	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:semantic_checker	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:semantic_checker	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:semantic_checker	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:semantic_checker	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:competence_evidence	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:competence_evidence	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:competence_evidence	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:competence_evidence	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:competence_evidence	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:competence_evidence	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:competence_evidence	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:soundness_basis	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:soundness_basis	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:soundness_basis	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:soundness_basis	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:soundness_basis	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:soundness_basis	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:soundness_basis	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:result_schema	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:result_schema	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:result_schema	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:result_schema	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:result_schema	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:result_schema	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:result_schema	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:unavailable_rule	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:unavailable_rule	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:unavailable_rule	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:unavailable_rule	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:unavailable_rule	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:unavailable_rule	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:QUALIFICATION.present:unavailable_rule	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:field_label_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:field_label_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:field_label_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:field_label_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:field_label_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:field_label_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:field_label_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:surface_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:surface_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:surface_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:surface_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:surface_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:surface_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:surface_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:exposure	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:exposure	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:exposure	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:exposure	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:exposure	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:exposure	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:exposure	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:owner	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:owner	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:owner	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:owner	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:owner	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:owner	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:owner	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:coalition_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:coalition_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:coalition_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:coalition_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:coalition_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:coalition_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:coalition_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:visibility_evidence	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:visibility_evidence	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:visibility_evidence	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:visibility_evidence	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:visibility_evidence	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:visibility_evidence	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:FIELD-LABEL.present:visibility_evidence	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:argument_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:argument_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:argument_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:argument_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:argument_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:argument_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:argument_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:profile_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:profile_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:profile_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:profile_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:profile_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:profile_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:profile_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:model_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:model_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:model_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:model_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:model_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:model_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:model_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:obligation_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:obligation_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:obligation_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:obligation_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:obligation_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:obligation_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:obligation_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:experiment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:experiment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:experiment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:experiment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:experiment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:experiment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:experiment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:assumption_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:assumption_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:assumption_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:assumption_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:assumption_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:assumption_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:assumption_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:premise_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:premise_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:premise_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:premise_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:premise_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:premise_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:premise_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:certificate_artifact_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:certificate_artifact_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:certificate_artifact_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:certificate_artifact_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:certificate_artifact_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:certificate_artifact_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:certificate_artifact_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:qualification_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:qualification_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:qualification_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:qualification_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:qualification_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:qualification_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:qualification_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:reduction_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:reduction_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:reduction_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:reduction_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:reduction_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:reduction_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:reduction_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:claimed_bound	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:claimed_bound	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:claimed_bound	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:claimed_bound	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:claimed_bound	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:claimed_bound	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:claimed_bound	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:composition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:composition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:composition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:composition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:composition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:composition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ARGUMENT.present:composition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assessment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assessment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assessment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assessment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assessment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assessment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assessment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:argument_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:argument_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:argument_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:argument_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:argument_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:argument_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:argument_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:qualification_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:qualification_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:qualification_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:qualification_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:qualification_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:qualification_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:qualification_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:invocation_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:invocation_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:invocation_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:invocation_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:invocation_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:invocation_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:invocation_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:exact_input_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:exact_input_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:exact_input_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:exact_input_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:exact_input_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:exact_input_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:exact_input_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:complete_result	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:complete_result	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:complete_result	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:complete_result	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:complete_result	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:complete_result	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:complete_result	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:validated_bound	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:validated_bound	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:validated_bound	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:validated_bound	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:validated_bound	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:validated_bound	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:validated_bound	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:artifact_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:artifact_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:artifact_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:artifact_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:artifact_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:artifact_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:artifact_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assumption_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assumption_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assumption_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assumption_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assumption_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assumption_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:assumption_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:source_assertion_evidence	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:source_assertion_evidence	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:source_assertion_evidence	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:source_assertion_evidence	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:source_assertion_evidence	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:source_assertion_evidence	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSMENT.present:source_assertion_evidence	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:obligation_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:obligation_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:obligation_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:obligation_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:obligation_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:obligation_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:obligation_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:profile_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:profile_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:profile_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:profile_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:profile_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:profile_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:profile_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:model_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:model_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:model_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:model_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:model_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:model_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:model_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:kind	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:kind	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:kind	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:kind	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:kind	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:kind	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:kind	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:target_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:target_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:target_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:target_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:target_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:target_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:target_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:coalition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:coalition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:coalition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:coalition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:coalition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:coalition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:coalition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:node_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:node_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:node_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:node_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:node_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:node_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:node_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:edge_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:edge_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:edge_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:edge_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:edge_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:edge_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:edge_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:experiment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:experiment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:experiment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:experiment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:experiment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:experiment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:experiment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:disposition	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:disposition	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:disposition	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:disposition	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:disposition	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:disposition	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:disposition	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:argument_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:argument_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:argument_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:argument_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:argument_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:argument_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:argument_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:exact_evidence_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:exact_evidence_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:exact_evidence_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:exact_evidence_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:exact_evidence_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:exact_evidence_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBLIGATION.present:exact_evidence_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:experiment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:experiment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:experiment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:experiment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:experiment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:experiment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:experiment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:method	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:method	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:method	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:method	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:method	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:method	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:method	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:argument_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:argument_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:argument_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:argument_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:argument_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:argument_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:argument_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:multiplicities	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:multiplicities	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:multiplicities	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:multiplicities	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:multiplicities	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:multiplicities	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:multiplicities	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:theorem_ref	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:theorem_ref	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:theorem_ref	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:theorem_ref	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:theorem_ref	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:theorem_ref	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:theorem_ref	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:qualification_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:qualification_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:qualification_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:qualification_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:qualification_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:qualification_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:qualification_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composed_bound	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composed_bound	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composed_bound	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composed_bound	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composed_bound	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composed_bound	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:COMPOSITION.present:composed_bound	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:assessment_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:assessment_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:assessment_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:assessment_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:assessment_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:assessment_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:assessment_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_kind	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_kind	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_kind	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_kind	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_kind	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_kind	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:event_kind	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:input_bytes	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:input_bytes	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:input_bytes	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:input_bytes	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:input_bytes	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:input_bytes	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:input_bytes	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:output_bytes	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:output_bytes	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:output_bytes	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:output_bytes	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:output_bytes	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:output_bytes	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:output_bytes	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:predecessor_ids	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:predecessor_ids	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:predecessor_ids	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:predecessor_ids	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:predecessor_ids	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:predecessor_ids	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:predecessor_ids	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:control_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:control_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:control_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:control_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:control_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:control_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:control_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:owner	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:owner	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:owner	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:owner	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:owner	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:owner	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:owner	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:attempt_ordinal	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:attempt_ordinal	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:attempt_ordinal	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:attempt_ordinal	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:attempt_ordinal	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:attempt_ordinal	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:ASSESSOR-EVENT.present:attempt_ordinal	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:coalition_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:coalition_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:coalition_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:coalition_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:coalition_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:coalition_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:coalition_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:member_role_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:member_role_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:member_role_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:member_role_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:member_role_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:member_role_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:member_role_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:protected_target_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:protected_target_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:protected_target_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:protected_target_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:protected_target_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:protected_target_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:protected_target_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:observation_evidence_refs	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:observation_evidence_refs	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:observation_evidence_refs	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:observation_evidence_refs	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:observation_evidence_refs	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:observation_evidence_refs	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:OBSERVER.present:observation_evidence_refs	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:applicability_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:applicability_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:applicability_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:applicability_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:applicability_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:applicability_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:applicability_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:policy_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:policy_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:policy_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:policy_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:policy_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:policy_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:policy_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:profile_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:profile_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:profile_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:profile_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:profile_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:profile_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:profile_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:mapping_digest	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:mapping_digest	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:mapping_digest	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:mapping_digest	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:mapping_digest	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:mapping_digest	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:mapping_digest	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:context_source	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:context_source	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:context_source	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:context_source	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:context_source	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:context_source	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:context_source	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:envelope_id	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:envelope_id	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:envelope_id	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:envelope_id	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:envelope_id	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:envelope_id	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:envelope_id	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:source_status_evidence	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:source_status_evidence	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:source_status_evidence	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:source_status_evidence	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:source_status_evidence	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:source_status_evidence	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:source_status_evidence	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:dependency_evidence	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:dependency_evidence	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:dependency_evidence	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:dependency_evidence	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:dependency_evidence	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:dependency_evidence	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:dependency_evidence	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:stage	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:stage	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:stage	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:stage	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:stage	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:stage	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:stage	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:attempt_ordinal	carrier	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:attempt_ordinal	diagnostic-cache	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:attempt_ordinal	governing-source	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:attempt_ordinal	profile-issuer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:attempt_ordinal	qualified-assessor	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:attempt_ordinal	required-coalition	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
SECURITY-FRAME:POLICY-APPLICABILITY.present:attempt_ordinal	transport-observer	UNKNOWN	Source-owned actor/endpoint association and coalition-complete visibility; no role appoints an actor
```

## Exact v4_record_grammar.py

```python
"""Documentary S90 grammar. No qualification, model completeness or admission.

These functions define record placement and absence bytes. They do not construct
a governing profile and do not replace independently qualified source parsers.
"""
import csv
import hashlib
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = list(csv.DictReader((HERE / 'security-fields.tsv').open(), delimiter='\t'))
SCHEMAS = sorted({r['schema'] for r in FIELDS})
SPEC = {s: {r['field']: r['type'] for r in FIELDS if r['schema'] == s} for s in SCHEMAS}
IDENTITY = {s: next(iter(SPEC[s])) for s in SCHEMAS}
ENUM = {
    'EXPERIMENT': {'COLLISION', 'CROSS-ACTION-TRACKING', 'ACTOR-INFORMATION'},
    'QUALIFIED': {'VALID', 'INVALID', 'UNAVAILABLE'},
    'EXPOSURE': {'PUBLIC', 'CONFIDENTIAL', 'PRIVATE-ACTOR'},
    'OBLIGATION': {'EXACT', 'COMPUTATIONAL'},
    'DISPOSITION': {'EXACT-SATISFIED', 'EXACT-VIOLATION', 'COMPUTATIONALLY-BOUNDED', 'NOT-ESTABLISHED'},
    'COMPOSITION': {'UNION', 'SOURCE-QUALIFIED-THEOREM'},
    'ASSESSOR-EVENT': {'READ', 'CALL', 'RETURN', 'ERROR', 'RETRY', 'CACHE'},
    'STAGE': {'STATIC-ADMISSION', 'E', 'PRE-EXECUTION', 'PRE-COMMITMENT'},
}
OBLIGATION_TEMPLATE = ('obligation_id', 'kind', 'target_ids', 'coalition_id', 'node_ids', 'edge_ids', 'experiment_id')
COMPOSITION_TEMPLATE = ('composition_id', 'policy_id', 'experiment_id', 'method', 'theorem_ref', 'qualification_id')

def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')

def unique_object(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError('duplicate JSON key')
        out[k] = v
    return out

def parse(raw):
    if type(raw) is not bytes:
        raise ValueError('byte input')
    value = json.loads(raw.decode('ascii'), object_pairs_hook=unique_object,
                       parse_float=lambda _: (_ for _ in ()).throw(ValueError('floating point')),
                       parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite number')))
    if canonical(value) != raw:
        raise ValueError('noncanonical JSON')
    return value

def exact(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError('exact object keys')

def primitive(kind, value, field_register=None):
    if kind == 'ID':
        if type(value) is not str or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:#-]*', value, re.ASCII) is None:
            raise ValueError('canonical ID')
    elif kind == 'FIELD-CLASS-REF':
        if type(value) is not str or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:#-]*(?:\.\$record)?', value, re.ASCII) is None:
            raise ValueError('canonical field-class spelling')
        if type(field_register) not in (list, tuple, set, frozenset) or not all(type(n) is str for n in field_register) or value not in field_register:
            raise ValueError('exact complete source-owned field-class register membership required')
    elif kind == 'DIGEST':
        if type(value) is not str or re.fullmatch('[0-9a-f]{64}', value) is None:
            raise ValueError('digest')
    elif kind == 'BYTES':
        if type(value) is not str or re.fullmatch('(?:[0-9a-f]{2})*', value) is None:
            raise ValueError('hex bytes')
    elif kind == 'UINT':
        if type(value) is not int or value < 0:
            raise ValueError('unsigned integer')
    elif kind == 'RATIONAL':
        if type(value) is not list or len(value) != 2 or any(type(x) is not int for x in value):
            raise ValueError('rational pair')
        a, b = value
        if b <= 0 or not 0 <= a <= b or math.gcd(a, b) != 1:
            raise ValueError('reduced probability')
    elif kind == 'SOURCE-REF':
        exact(value, ('owner_source_id', 'source_sha256', 'source_anchor', 'material_sha256'))
        for k in ('owner_source_id', 'source_anchor'):
            primitive('ID', value[k])
        for k in ('source_sha256', 'material_sha256'):
            primitive('DIGEST', value[k])
    elif kind.startswith('LIST-'):
        if type(value) is not list:
            raise ValueError('array')
        for item in value:
            primitive(kind[5:], item)
        if kind == 'LIST-ID' and len(set(value)) != len(value):
            raise ValueError('duplicate identity')
    elif kind.startswith('ENUM-'):
        if type(value) is not str or value not in ENUM[kind[5:]]:
            raise ValueError('enum')
    else:
        raise ValueError('unrecognized primitive')

def nullable(schema, record, field):
    # A missing applicable source field is never made zero/empty/VALID.
    if schema == 'ASSESSMENT' and field == 'validated_bound':
        return record.get('complete_result') in {'INVALID', 'UNAVAILABLE'}
    if schema == 'ASSESSOR-EVENT' and field in {'input_bytes', 'output_bytes'}:
        return True  # Source-qualified event grammar establishes exact applicability.
    if schema == 'COMPOSITION' and field == 'theorem_ref':
        return record.get('method') == 'UNION'
    if schema == 'OBLIGATION' and field == 'experiment_id':
        return record.get('kind') == 'EXACT'
    return False

def record_shape(schema, value, template=False, field_register=None):
    keys = OBLIGATION_TEMPLATE if template and schema == 'OBLIGATION' else COMPOSITION_TEMPLATE if template and schema == 'COMPOSITION' else SPEC[schema]
    exact(value, keys)
    for key in keys:
        if value[key] is None:
            if not nullable(schema, value, key):
                raise ValueError('unjustified field absence')
        else:
            primitive(SPEC[schema][key], value[key], field_register)
    if schema == 'ASSESSMENT' and value['complete_result'] != 'VALID' and value['validated_bound'] is not None:
        raise ValueError('nonvalid assessment carries bound')
    if schema == 'COMPOSITION' and value['method'] == 'UNION' and value['theorem_ref'] is not None:
        raise ValueError('UNION has no theorem reference')
    if schema == 'OBLIGATION' and value['kind'] == 'EXACT' and value['experiment_id'] is not None:
        raise ValueError('exact obligation has no experiment')
    if schema == 'EXPERIMENT' and value['maximum'][0] >= value['maximum'][1]:
        raise ValueError('computational maximum must be strictly below one')
    return value

def records(schema, values, template=False, field_register=None):
    if type(values) is not list:
        raise ValueError('record array')
    for value in values:
        record_shape(schema, value, template, field_register)
    ids = [v[IDENTITY[schema]] for v in values]
    if ids != sorted(set(ids)) or any('::' in x for x in ids):
        raise ValueError('unique ordered record IDs')
    return values

def security_shape(value, field_register=None):
    exact(value, ('contract_sha256', 'policy', 'schema_sha256', 'qualification_interface_sha256',
                  'experiments', 'assumptions', 'qualification_contracts', 'operating_envelope',
                  'leakage', 'obligations', 'composition_rules'))
    for k in ('contract_sha256', 'schema_sha256', 'qualification_interface_sha256'):
        primitive('DIGEST', value[k])
    p = value['policy']
    exact(p, ('record', 'algorithms', 'artifacts', 'observers', 'field_labels'))
    record_shape('POLICY', p['record'])
    for key, schema in [('algorithms', 'ALGORITHM'), ('artifacts', 'ARTIFACT'),
                        ('observers', 'OBSERVER'), ('field_labels', 'FIELD-LABEL')]:
        records(schema, p[key], field_register=field_register)
    for key, schema in [('experiments', 'EXPERIMENT'), ('assumptions', 'ASSUMPTION'),
                        ('qualification_contracts', 'QUALIFICATION')]:
        records(schema, value[key])
    record_shape('ENVELOPE', value['operating_envelope'])
    record_shape('LEAKAGE', value['leakage'])
    records('OBLIGATION', value['obligations'], True)
    c = value['composition_rules']
    exact(c, ('directory_id', 'records'))
    primitive('ID', c['directory_id'])
    records('COMPOSITION', c['records'], True)
    if c['directory_id'] != p['record']['composition_id']:
        raise ValueError('composition directory join')
    # Nonempty directories and all semantic/source joins are independent duties.
    # In particular this function grants no validity to an empty experiment set.
    return value

def evidence_shape(value, field_register=None):
    exact(value, ('format', 'profile_digest', 'phase', 'records'))
    if value['format'] != 'PE-G4-SECURITY-RECORDS-V4':
        raise ValueError('evidence format')
    primitive('DIGEST', value['profile_digest'])
    primitive('ENUM-STAGE', value['phase'])
    exact(value['records'], SCHEMAS)
    for schema in SCHEMAS:
        d = value['records'][schema]
        exact(d, ('status', 'justification', 'instances'))
        if type(d['status']) is not str or d['status'] not in {'PRESENT', 'UNAVAILABLE', 'INAPPLICABLE'}:
            raise ValueError('record status')
        if d['justification'] is not None:
            primitive('SOURCE-REF', d['justification'])
        records(schema, d['instances'], field_register=field_register)
        if (d['status'] == 'PRESENT') != bool(d['instances']):
            raise ValueError('status/instances mismatch')
        if d['status'] == 'INAPPLICABLE' and d['justification'] is None:
            raise ValueError('inapplicability needs owning source justification')
        if schema in {'POLICY', 'ENVELOPE', 'LEAKAGE'} and d['status'] == 'PRESENT' and len(d['instances']) != 1:
            raise ValueError('single record schema')
    return value

def field_digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()
```



<a id="nonvacuity"></a>
## nonvacuity

Computational privacy admission MUST enforce a canonical rational maximum strictly below one, independently established nonempty scope and genuine protected alternatives, uniform whole-class and whole-view coverage, and the exact non-vacuity qualification and failure contract below; numerical targets MUST remain independently source-governed and no vacuous claim MAY discharge a required privacy duty.

Owner: PE-G4-CAP-111. Exact contract: NONVACUITY-CONTRACT.txt embedded in the owning acceptance contract above.
