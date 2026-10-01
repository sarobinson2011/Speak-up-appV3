# Privacy Engine Reference Implementation Model V1

STATE.md remains canonical.

# 1. Purpose

This document defines the architectural model of a Privacy Engine reference
implementation.

A Privacy Engine reference implementation is an identified, bounded, and
designated implementation that realizes one or more identified Privacy Engine
implementation profiles.

It provides an inspectable implementation realization for purposes including:

- implementation understanding;
- integration;
- testing;
- interoperability;
- implementation comparison;
- conformance support;
- certification support.

This document defines the reference implementation as an architectural object.

It does not define:

- a particular reference implementation;
- implementation source code;
- implementation APIs;
- implementation algorithms;
- implementation deployment;
- protocol behavior;
- protocol semantics;
- conformance procedures;
- certification procedures;
- compatibility procedures.

The reference implementation realizes already-defined implementation
obligations.

It does not create those obligations.

It does not redefine those obligations.

It does not become protocol authority.

Protocol authority always remains with the published protocol generation.

# 2. Scope

This document defines:

- reference implementation identity;
- relationship to implementation profiles;
- reference implementation scope and boundedness;
- reference designation;
- implementation realization;
- permitted implementation choices;
- multiple reference implementations;
- reference stability and versioning;
- divergence, defects, and failure;
- relationship to ordinary implementations;
- relationship to conformance;
- relationship to certification;
- relationship to compatibility;
- relationship to testing and interoperability;
- preservation of protocol semantics;
- protocol authority.

This document applies only to the architectural identity and role of a
reference implementation.

It does not define the internal construction of any implementation.

It does not prescribe:

- programming language;
- source-code organization;
- execution environment;
- deployment topology;
- storage system;
- communication mechanism;
- library selection;
- framework selection;
- algorithm selection where the implementation profile permits choice;
- operational policy;
- governance process;
- release process;
- distribution mechanism.

A reference implementation may embody such choices.

Those choices remain implementation choices unless they are independently
required by the applicable implementation profile.

This document does not introduce a new source of protocol semantics.

It defines a bounded realization object within the established
implementation-facing architecture.

# 3. Primary Definition

A Privacy Engine reference implementation is a uniquely identified, bounded,
and designated implementation that completely realizes one or more identified
Privacy Engine implementation profiles and is maintained as an inspectable
implementation reference without becoming a source of protocol semantics or
protocol authority.

Let:

- `P` be one published Privacy Engine protocol generation;
- `S` be one Privacy Engine Protocol Specification;
- `F` be one Privacy Engine implementation profile;
- `Ir` be one Privacy Engine reference implementation.

Then:

> derives(S, P)

> derives(F, S)

> implements(Ir, F)

> referenceImplementation(Ir, F)

The necessary relationship is:

> referenceImplementation(Ir, F) -> implements(Ir, F)

Reference designation therefore implies that the designated object is an
implementation realization of the identified implementation profile.

Reference designation does not imply that the reference implementation defines
the profile.

It does not imply that the reference implementation defines the Protocol
Specification.

It does not imply that the reference implementation defines the published
protocol generation.

The architectural progression is:

> P -> S -> F -> Ir

The published protocol generation is authoritative.

The Protocol Specification composes the implementation-facing expression of
that generation.

The implementation profile narrows and organizes applicable obligations.

The reference implementation realizes those obligations through one bounded
implementation.

The reference implementation demonstrates one permitted realization.

It does not define the only permitted realization.

# 4. Reference Implementation Identity

A reference implementation must possess a stable and distinguishable identity.

Reference implementation identity must be sufficient to distinguish:

- one reference implementation from another;
- one version of a reference implementation from another;
- one profile realization from another;
- one reference designation from another;
- one implementation scope from another.

Let:

- `Ir1` and `Ir2` be reference implementations.

Then:

> identity(Ir1) = identity(Ir2) -> Ir1 = Ir2

Distinct reference implementations must not silently share one architectural
identity.

Reference implementation identity may include identified attributes such as:

- implementation name;
- implementation identifier;
- implementation version;
- immutable source revision;
- build identity;
- release identity;
- realized profile identity;
- realized profile version;
- designation status.

This document does not require one concrete identity format.

Reference implementation identity must not be inferred solely from:

- popularity;
- common use;
- origin within the protocol project;
- authorship by protocol designers;
- similarity to another implementation;
- source-code reuse;
- compatibility with another implementation;
- deployment by a recognized operator.

Reference status is explicit.

It is not an emergent consequence of recognition or usage.

A change that materially alters the implementation realization may require a
new reference implementation version identity.

Such changes may include:

- changed profile coverage;
- changed implementation behavior;
- changed permitted-choice resolution;
- changed externally observable behavior;
- changed interoperability behavior;
- changed defect status;
- changed conformance-relevant behavior.

Reference implementation identity does not alter the identity of:

- the implementation profile;
- the Protocol Specification;
- the published protocol generation.

# 5. Relationship to Implementation Profiles

A reference implementation realizes one or more identified implementation
profiles.

The implementation profile defines the applicable obligations.

The reference implementation implements those obligations.

The relationship is:

> profile(F)

> referenceImplementation(Ir, F)

> referenceImplementation(Ir, F) -> implements(Ir, F)

The implementation profile is the realization target.

The reference implementation is one realization of that target.

Therefore:

> target(F) != realization(Ir)

The reference implementation must not redefine:

- profile membership;
- requirement applicability;
- requirement strength;
- requirement meaning;
- permitted choices;
- prohibited choices;
- profile dependencies;
- profile completeness.

For any normative requirement `R` applicable through profile `F`:

> applies(F, R) -> obligation(F, R)

The reference implementation must preserve that obligation:

> referenceImplementation(Ir, F) and applies(F, R)
> -> implementsRequirement(Ir, R)

The reference implementation may not weaken a requirement because its own
implementation uses a narrower or more convenient behavior.

It may not strengthen a requirement merely because its implementation chooses
a stricter behavior.

It may not reinterpret a requirement through incidental source-code behavior.

The governing direction is:

> F -> Ir

The forbidden direction is:

> Ir -> redefine(F)

Where the reference implementation and implementation profile appear to
conflict, the profile remains the implementation-facing authority.

The conflict must be treated as:

- a defect in the reference implementation;
- an error in the reference designation;
- an incomplete realization;
- a version mismatch;
- an interpretation requiring resolution against the Protocol Specification
  and published protocol generation.

The conflict must not be resolved by silently treating implementation behavior
as normative.

# 6. Reference Implementation Scope and Boundedness

Every reference implementation must have an explicit and bounded scope.

The scope identifies what the reference implementation claims to realize.

A reference implementation scope may be bounded by:

- one implementation profile;
- a compatible composition of implementation profiles;
- one implementation role;
- one capability set;
- one deployment class;
- one protocol-generation target;
- one implementation version;
- one declared operational boundary.

Let:

- `scope(Ir)` be the declared scope of reference implementation `Ir`.

Then:

> referenceImplementation(Ir, F) -> F in scope(Ir)

A reference implementation must not be treated as realizing obligations outside
its declared scope.

Therefore:

> F not in scope(Ir) -> noReferenceClaim(Ir, F)

A reference implementation may contain functionality outside its reference
scope.

Such functionality does not automatically acquire reference status.

A codebase may therefore contain:

- reference-profile functionality;
- experimental functionality;
- optional functionality;
- unrelated functionality;
- development tooling;
- test infrastructure;
- deployment support.

Only the explicitly designated and bounded realization belongs to the
reference implementation claim.

Reference implementation scope must be sufficiently complete to support its
designation.

A fragment is not a complete reference implementation of an entire profile
merely because it demonstrates one requirement.

Examples of insufficient whole-profile realization include:

- one code example;
- one isolated algorithm;
- one test vector;
- one interface stub;
- one proof-of-concept component;
- one partial protocol operation;
- one incomplete integration path.

Such objects may be reference material.

They are not reference implementations of a complete implementation profile
unless the declared profile scope itself is correspondingly complete and
bounded.

Reference implementation boundedness prevents reference status from expanding
silently across:

- unimplemented profile obligations;
- adjacent profiles;
- adjacent protocol generations;
- undocumented implementation behavior;
- optional modules;
- experimental modules;
- deployment-specific extensions.

# 7. Reference Designation

Reference implementation status must be established through explicit reference
designation.

Reference designation is the bounded architectural act or record by which an
identified implementation version is declared to serve as a reference
realization of one or more identified implementation profiles.

Let:

- `D` be one reference designation;
- `Ir` be one implementation;
- `F` be one implementation profile.

Then:

> designates(D, Ir, F)

and:

> designates(D, Ir, F) -> referenceImplementation(Ir, F)

A reference designation should identify at least:

- the designated implementation;
- the designated implementation version;
- the realized implementation profile;
- the realized profile version;
- the scope of the designation;
- the status of the designation.

A designation may also identify:

- the designation authority;
- the designation date;
- an immutable implementation revision;
- associated conformance evidence;
- known limitations;
- known defects;
- supersession status.

This document does not define:

- a designation registry;
- a designation manifest;
- a designation file format;
- a designation governance process;
- a designation authority structure;
- a designation approval workflow.

Reference designation does not create protocol semantics.

It does not create implementation-profile obligations.

It records that one identified implementation is intended to serve as a
reference realization of already-existing obligations.

Reference designation must not be inferred merely because an implementation:

- was created first;
- was created by protocol authors;
- is widely deployed;
- is commonly copied;
- is used for testing;
- is used by certification tooling;
- is treated informally as canonical.

Without explicit designation, such an implementation remains an implementation.

Reference designation may be:

- active;
- provisional;
- suspended;
- withdrawn;
- superseded;
- historical.

Designation status must not silently alter the identity or semantics of the
underlying implementation profile.

# 8. Implementation Realization

Implementation realization is the implementation-level preservation and
execution of the obligations defined by an implementation profile.

Let:

- `R` be one normative requirement;
- `F` be one implementation profile;
- `Ir` be one reference implementation.

Then:

> applies(F, R) -> obligation(F, R)

and:

> referenceImplementation(Ir, F)
> -> realizes(Ir, obligations(F))

A reference implementation realizes a profile when it implements all
requirements applicable within the declared profile scope.

Therefore:

> completeRealization(Ir, F)
> -> forAll R: applies(F, R) -> implementsRequirement(Ir, R)

Implementation realization may include:

- executable behavior;
- persistent behavior;
- interface behavior;
- failure behavior;
- validation behavior;
- interoperability behavior;
- security behavior;
- operational behavior where normatively required.

Implementation realization does not require every realization to have the same:

- internal structure;
- source layout;
- control flow;
- programming language;
- algorithms where choice is permitted;
- dependency graph;
- storage layout;
- deployment topology;
- optimization strategy;
- user interface.

The implementation profile defines required outcomes and constraints.

The reference implementation chooses one permitted means of satisfying them.

A reference implementation must preserve both:

- success semantics;
- failure semantics.

Where the profile requires failure, the reference implementation must fail.

It must not silently:

- repair;
- reinterpret;
- weaken;
- skip;
- substitute;
- infer;
- merge;
- broaden.

The realization rule is:

> required(F, X) -> preserve(Ir, X)

The failure rule is:

> cannotPreserve(Ir, X) -> fail(Ir)

The forbidden rule is:

> cannotPreserve(Ir, X) -> choose(X')

where `X'` is a materially different obligation, semantic object, or required
outcome.

# 9. Permitted Implementation Choices

An implementation profile may permit implementation-defined choices.

A reference implementation may select one permitted choice.

That selection demonstrates one valid realization.

It does not convert the selected choice into a universal obligation.

Let:

- `C(F)` be the set of choices permitted by profile `F`;
- `c` be one selected choice;
- `Ir` be one reference implementation.

Then:

> c in C(F)

> selects(Ir, c)

The selection is valid only where:

> permitted(F, c)

The reference implementation must not select a prohibited choice.

It must not select a choice that violates another applicable requirement.

It must not treat an implementation-defined choice as an opportunity to
reinterpret protocol semantics.

Where multiple permitted choices exist:

> permitted(F, c1)

> permitted(F, c2)

> c1 != c2

A reference implementation may select `c1`.

An ordinary implementation may select `c2`.

Both may be valid realizations where all applicable obligations remain
satisfied.

Therefore:

> selects(Ir, c1) does not imply requires(F, c1)

The implementation behavior outside the profile's required behavior remains an
implementation choice.

Let:

- `behavior(Ir)` be the behavior of the reference implementation;
- `requiredBehavior(F)` be behavior required by the profile.

Then:

> behavior(Ir) - requiredBehavior(F) = implementationChoice(Ir)

and:

> implementationChoice(Ir) does not imply obligation(F)

This distinction applies to choices including:

- internal algorithms;
- data structures;
- optimization strategies;
- source organization;
- error wording;
- logging structure;
- deployment mechanics;
- library selection;
- implementation-specific APIs;
- non-normative operational behavior.

A reference implementation should make significant permitted choices
inspectable where doing so supports understanding or interoperability.

Inspectability does not make those choices normative.

# 10. Multiple Reference Implementations

More than one reference implementation may exist for the same implementation
profile.

Let:

- `Ir1` and `Ir2` be distinct reference implementations;
- `F` be one implementation profile.

Then:

> referenceImplementation(Ir1, F)

> referenceImplementation(Ir2, F)

> identity(Ir1) != identity(Ir2)

Multiple reference implementations may differ in:

- programming language;
- internal architecture;
- algorithm selection where permitted;
- performance characteristics;
- deployment environment;
- operational structure;
- implementation-specific interfaces;
- dependency selection.

They must not differ in ways that violate the applicable implementation
profile.

Multiple reference implementations may improve architectural confidence by
demonstrating that the implementation profile does not depend on:

- one programming language;
- one source structure;
- one vendor;
- one library;
- one algorithm where alternatives are permitted;
- one deployment environment;
- one incidental implementation behavior.

Agreement between multiple reference implementations may support:

- interoperability testing;
- comparison;
- defect discovery;
- ambiguity discovery;
- implementation guidance.

Agreement does not create protocol semantics.

Multiple reference implementations that share the same defect do not transform
that defect into a normative requirement.

Disagreement between reference implementations must be resolved against:

1. the applicable implementation profile;
2. the Privacy Engine Protocol Specification;
3. the published protocol generation.

A reference implementation may realize multiple profiles.

Let:

- `F1`, `F2`, ..., `Fn` be implementation profiles.

Then:

> realizes(Ir, {F1, F2, ..., Fn})

is permitted only where:

- each profile is explicitly identified;
- profile versions are identified;
- profile composition is permitted;
- profile dependencies are satisfied;
- profile obligations do not conflict;
- the implementation completely realizes the declared composition.

Reference status for one profile does not automatically extend to another.

Therefore:

> referenceImplementation(Ir, F1)
> does not imply referenceImplementation(Ir, F2)

# 11. Reference Stability and Versioning

Reference implementations may evolve.

Reference stability means that an identified reference implementation version
remains sufficiently fixed and inspectable to support reliable understanding,
integration, testing, interoperability, comparison, and conformance support.

Reference stability does not require permanent immutability of the entire
implementation lineage.

Each materially distinct version must remain separately identifiable.

Let:

- `Ir_v1` be version 1;
- `Ir_v2` be version 2.

Then:

> materialDifference(Ir_v1, Ir_v2)
> -> identity(Ir_v1) != identity(Ir_v2)

A new reference implementation version may be required when there is a material
change to:

- profile realization;
- profile composition;
- normative behavior;
- permitted-choice resolution;
- externally observable behavior;
- interoperability behavior;
- conformance-relevant behavior;
- defect status;
- supported protocol generation;
- supported specification version;
- supported profile version.

A reference implementation version may be corrected without changing the
identity of:

- the published protocol generation;
- the Protocol Specification;
- the implementation profile.

Reference implementation versioning is subordinate to the profile and protocol
hierarchy.

The progression remains:

> P -> S -> F -> Ir_v

A new reference implementation version does not create a new protocol
generation.

It does not create a new Protocol Specification.

It does not create a new implementation profile.

Such upstream objects change only through their own defined architectural
processes.

A version may be:

- current;
- supported;
- superseded;
- deprecated;
- withdrawn;
- historical.

Supersession does not erase the identity of the superseded version.

Historical reference versions may remain useful for:

- compatibility analysis;
- migration testing;
- regression analysis;
- protocol-lineage study;
- implementation comparison.

Reference stability requires that changes must not silently rewrite the meaning
of an existing identified version.

# 12. Divergence, Defects, and Failure

A reference implementation may contain defects.

Reference designation does not imply infallibility.

Therefore:

> referenceImplementation(Ir, F)
> does not imply defectFree(Ir)

A defect exists where the reference implementation fails to preserve an
applicable implementation-profile obligation.

Let:

- `R` be an applicable requirement.

Then:

> applies(F, R)

> violates(Ir, R)

implies:

> defect(Ir)

It does not imply:

> redefine(R, behavior(Ir))

The governing failure direction is:

> profile requirement -> implementation evaluation

The forbidden direction is:

> implementation behavior -> requirement redefinition

Where a reference implementation diverges from the profile, one or more of the
following must occur:

- the implementation is corrected;
- the designation scope is narrowed;
- the designation is suspended;
- the designation is withdrawn;
- the implementation version is superseded;
- the implementation is no longer treated as a valid realization of the
  affected profile.

The implementation profile must not be silently rewritten to legitimize the
divergence.

A defect may include:

- missing required behavior;
- prohibited behavior;
- weakened validation;
- incorrect failure behavior;
- incorrect requirement interpretation;
- incomplete profile coverage;
- incompatible permitted-choice selection;
- incorrect interoperability behavior;
- incorrect security behavior;
- version mismatch;
- undeclared extension affecting normative behavior.

A divergence is not necessarily a defect where it concerns behavior not
constrained by the profile.

Let:

> behaviorDifference(Ir1, Ir2)

If the difference lies entirely within permitted implementation choice:

> permittedDifference(F, Ir1, Ir2)

then the difference does not establish non-conformance.

Reference implementation failure must remain explicit.

A reference implementation must not hide a failure to realize an obligation by:

- substituting an alternative obligation;
- silently degrading behavior;
- broadening accepted input;
- weakening a rejection rule;
- inventing missing state;
- inferring unavailable semantics;
- merging distinct protocol objects;
- treating malformed material as valid.

Where the implementation cannot preserve the required semantic object:

> requiredObject(T)

> cannotPreserve(Ir, T)

the valid path is:

> T -> failure

The forbidden path is:

> T -> T'

where `T'` is a repaired, inferred, substituted, or materially different
object.

# 13. Relationship to Ordinary Implementations

An ordinary implementation and a reference implementation are both
implementations.

The distinction is reference designation and architectural role.

Let:

- `I` be an ordinary implementation;
- `Ir` be a reference implementation;
- `F` be an implementation profile.

Then:

> implements(I, F)

> referenceImplementation(Ir, F)

> referenceImplementation(Ir, F) -> implements(Ir, F)

An ordinary implementation may use a reference implementation for:

- implementation understanding;
- integration guidance;
- interoperability testing;
- expected-behavior comparison;
- test-vector generation;
- defect investigation;
- migration support.

An ordinary implementation is not required to be structurally equivalent to
the reference implementation.

Therefore:

> conforms(I, F)
> does not require equivalentImplementation(I, Ir)

An ordinary implementation need not reproduce:

- source-code structure;
- programming language;
- library choices;
- internal algorithms where alternatives are permitted;
- internal data structures;
- deployment topology;
- non-normative APIs;
- incidental error messages;
- incidental timing;
- incidental logging;
- incidental optimization choices.

An ordinary implementation must satisfy the applicable implementation profile.

It need not imitate the reference implementation.

An implementation may reuse reference implementation code.

Code reuse does not by itself establish:

- conformance;
- certification;
- compatibility;
- correct integration;
- complete profile realization.

An implementation may independently reproduce reference behavior.

Behavioral similarity does not by itself establish that all applicable
requirements are satisfied.

The implementation profile remains the assessment target.

The reference implementation remains one designated realization.

# 14. Relationship to Conformance

Conformance evaluates whether an implementation satisfies the obligations of an
identified implementation profile.

The reference implementation may support conformance work.

It does not define conformance.

The distinction is:

> profile = target

> implementation = realization

> conformance = assessment

Therefore:

> target != realization != assessment

Let:

- `A` be one conformance assessment;
- `I` be one implementation;
- `F` be one implementation profile.

Then:

> assesses(A, I, F)

A reference implementation may itself be assessed:

> assesses(A, Ir, F)

Reference designation does not replace conformance assessment.

It must not be treated as automatic proof that:

> satisfies(Ir, F)

A designation may carry an implementation claim:

> claimsRealization(Ir, F)

A conformance assessment may determine:

> determines(A, satisfies(Ir, F))

This preserves the distinction between:

- designation;
- realization claim;
- actual implementation behavior;
- independent conformance determination.

Agreement with a reference implementation is not sufficient proof of
conformance.

Therefore:

> agrees(I, Ir)
> does not imply conforms(I, F)

Two implementations may agree while both violate the profile.

Disagreement with a reference implementation does not by itself establish
non-conformance.

Therefore:

> disagrees(I, Ir)
> does not imply notConformant(I, F)

The disagreement must be evaluated against the applicable profile
requirements.

A conformance test may use the reference implementation as:

- a comparison implementation;
- an interoperability peer;
- an expected-output source;
- an expected-failure source;
- a test-vector source;
- an integration fixture.

Such use remains supporting evidence.

The normative assessment basis remains the identified implementation profile.

# 15. Relationship to Certification

Certification is an identified authoritative recognition produced through a
defined certification process.

A reference implementation may support certification.

It does not define certification.

It does not certify ordinary implementations.

It does not certify itself merely through reference designation.

Let:

- `C` be one certification result;
- `A` be one conformance assessment;
- `I` be one implementation;
- `F` be one implementation profile.

Then a later certification architecture may establish relationships such as:

> certification(C, I, F)

> basedOn(C, A)

The reference implementation may contribute:

- test infrastructure;
- comparison behavior;
- interoperability fixtures;
- implementation examples;
- expected success cases;
- expected failure cases;
- reference artifacts.

These do not replace:

- certification scope;
- certification authority;
- certification evidence;
- certification decision;
- certification status;
- certification lifecycle.

A reference implementation designation must not be interpreted as a
certification mark.

Use of reference implementation code must not automatically grant
certification.

Behavioral equivalence with a reference implementation must not automatically
grant certification.

Certification remains a distinct architectural subject governed by its own
model.

# 16. Relationship to Compatibility

Compatibility concerns declared or assessed interaction between identified
implementations and identified protocol targets or compatibility surfaces.

A reference implementation may support compatibility work.

It does not define compatibility.

A reference implementation may act as:

- an interoperability peer;
- a compatibility comparison target;
- a migration reference;
- a version-transition aid;
- a compatibility test fixture.

Compatibility with a reference implementation does not automatically establish
compatibility with every implementation of the same profile.

Therefore:

> compatible(I, Ir)
> does not imply compatible(I, allImplementations(F))

Compatibility with a reference implementation also does not automatically
establish conformance.

Therefore:

> compatible(I, Ir)
> does not imply conforms(I, F)

An implementation may conform to the same profile while being incompatible at
an implementation-specific surface that the profile does not standardize.

An implementation may interoperate with a defective reference implementation
while violating the profile.

Compatibility claims must remain bounded by:

- identified implementations;
- identified versions;
- identified profiles;
- identified protocol generations;
- identified compatibility targets;
- identified compatibility surfaces.

Reference implementation behavior must not silently expand the compatibility
surface defined elsewhere.

# 17. Relationship to Testing and Interoperability

A reference implementation may support testing and interoperability by
providing an inspectable realization of an implementation profile.

It may provide or support:

- successful-operation examples;
- required-failure examples;
- test vectors;
- interoperability fixtures;
- protocol interaction examples;
- integration environments;
- comparison outputs;
- regression baselines;
- migration examples;
- debugging support.

Testing against a reference implementation may establish evidence about:

- behavioral agreement;
- behavioral disagreement;
- integration success;
- integration failure;
- interoperability success;
- interoperability failure.

It does not independently establish the normative correctness of either
implementation.

The governing rules are:

> agreement(I, Ir) is evidence

> agreement(I, Ir) is not authority

> disagreement(I, Ir) is evidence

> disagreement(I, Ir) is not a conclusion

Where two implementations disagree, the implementation profile must determine
the required behavior.

Where the profile expression is insufficiently clear, interpretation must
proceed through the Protocol Specification and ultimately the published
protocol generation.

The reference implementation must not become an oracle whose behavior overrides
the specification hierarchy.

Interoperability tests may be symmetric or asymmetric.

A reference implementation may act as:

- producer;
- consumer;
- client;
- server;
- prover;
- verifier;
- publisher;
- reader;
- sender;
- receiver;
- coordinator;
- participant.

Such roles are implementation-specific unless defined by the implementation
profile.

Testing infrastructure included with a reference implementation is not
automatically part of the reference implementation's normative realization
scope.

Its status must be explicit.

# 18. Preservation of Protocol Semantics

The reference implementation must preserve protocol semantics.

Let:

- `P` be the published protocol generation;
- `S` be the Protocol Specification;
- `F` be the implementation profile;
- `Ir` be the reference implementation.

Then:

> derives(S, P)

> derives(F, S)

> referenceImplementation(Ir, F)

The semantic containment relationship is:

> semantics(F) subsetOf semantics(S)

> semantics(S) = implementationFacingExpression(semantics(P))

The reference implementation realizes the applicable semantic subset defined
through the profile.

Therefore:

> realizedSemantics(Ir, F) = semantics(F)

within the declared realization scope.

The reference implementation may contain additional implementation behavior.

That behavior must not:

- contradict the profile;
- weaken the profile;
- expand protocol semantics;
- redefine protocol semantics;
- create hidden obligations;
- alter requirement strength;
- alter requirement applicability;
- alter protocol identity.

The preservation direction is:

> semantics(P)
> -> expressedBy(S)
> -> boundedBy(F)
> -> realizedBy(Ir)

The reference implementation is downstream of protocol semantics.

It is not an upstream semantic source.

A defect in the reference implementation does not modify protocol semantics.

A permitted implementation choice does not modify protocol semantics.

A reference implementation version change does not modify protocol semantics.

A reference designation does not modify protocol semantics.

The prohibited reversal is:

> behavior(Ir)
> -> redefine(F)
> -> redefine(S)
> -> redefine(P)

The required preservation rule is:

> P -> S -> F -> Ir

not:

> Ir -> F' -> S' -> P'

# 19. Protocol Authority

The reference implementation is not protocol authority.

It does not become protocol authority because it is:

- designated;
- maintained by protocol authors;
- widely used;
- commonly copied;
- used in testing;
- used in certification;
- used in interoperability work;
- treated as an implementation reference;
- the first implementation;
- the most complete implementation;
- the most popular implementation.

The implementation profile does not become protocol authority.

The Protocol Specification does not replace the published protocol generation
as semantic authority.

The authority chain remains:

> published protocol generation
> -> Protocol Specification
> -> implementation profile
> -> reference implementation

Authority does not flow upward from implementation behavior.

Where conflict exists:

1. the published protocol generation governs protocol semantics;
2. the Protocol Specification governs its implementation-facing expression;
3. the implementation profile governs applicable implementation obligations;
4. the reference implementation is evaluated against those obligations.

The reference implementation must never be used to silently override:

- a normative requirement;
- requirement strength;
- requirement applicability;
- profile scope;
- specification meaning;
- published protocol semantics.

Protocol authority always remains with the published protocol generation.

# 20. Explicit Exclusions

This document does not define:

- an actual reference implementation;
- reference source code;
- implementation APIs;
- protocol APIs;
- wire formats;
- storage formats;
- database schemas;
- contract interfaces;
- algorithms;
- cryptographic constructions;
- deployment architecture;
- execution topology;
- operational procedures;
- release procedures;
- source-control procedures;
- build procedures;
- packaging procedures;
- distribution procedures;
- test-suite contents;
- test-vector contents;
- interoperability scenarios;
- conformance criteria;
- conformance assessment procedures;
- certification criteria;
- certification authorities;
- certification procedures;
- compatibility criteria;
- compatibility declarations;
- compatibility profiles;
- compatibility surfaces;
- reference designation governance;
- reference designation metadata;
- implementation-profile contents;
- Protocol Specification contents;
- normative requirement contents;
- normative requirement-set contents;
- specification-section contents;
- published protocol semantics;
- protocol authority.

This document does not require:

- one reference implementation;
- one programming language;
- one implementation architecture;
- one source-code organization;
- one deployment environment;
- one vendor;
- one library;
- one algorithm where the profile permits alternatives;
- one implementation-specific interface.

This document does not establish that:

- reference status implies conformance;
- reference status implies certification;
- reference status implies compatibility;
- code reuse implies conformance;
- behavioral agreement implies conformance;
- behavioral disagreement implies non-conformance;
- implementation behavior creates normative requirements;
- implementation defects redefine protocol semantics;
- implementation popularity creates protocol authority.

No new architectural ontology is introduced.

The reference implementation is defined within the existing implementation
realization architecture.

# 21. Conclusion

A Privacy Engine reference implementation is a uniquely identified, bounded,
and designated implementation that completely realizes one or more identified
Privacy Engine implementation profiles and is maintained as an inspectable
implementation reference without becoming a source of protocol semantics or
protocol authority.

The implementation profile defines applicable obligations.

The reference implementation demonstrates one permitted realization of those
obligations.

The reference implementation may support:

- understanding;
- integration;
- testing;
- interoperability;
- comparison;
- conformance;
- certification;
- compatibility.

It does not replace the implementation profile.

It does not define conformance.

It does not define certification.

It does not define compatibility.

It does not define protocol semantics.

It does not become protocol authority.

The central architectural distinction is:

> target != realization != assessment

The governing progression is:

> P -> S -> F -> Ir

The governing realization relationship is:

> referenceImplementation(Ir, F) -> implements(Ir, F)

The implementation profile defines what must be implemented.

The reference implementation demonstrates one permitted implementation.

An implementation choice made by the reference implementation remains an
implementation choice unless independently required by the implementation
profile.

A defect in the reference implementation remains an implementation defect.

It does not become a protocol requirement.

It does not redefine the implementation profile.

It does not redefine the Protocol Specification.

It does not redefine the published protocol generation.

Protocol authority always remains with the published protocol generation.
