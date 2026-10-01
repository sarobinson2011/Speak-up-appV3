# Privacy Engine Implementation Profile Model V1

Supporting architectural documentation only.

STATE.md remains canonical.

# 1. Purpose

This document defines the architectural model of a Privacy Engine
implementation profile.

A Privacy Engine implementation profile provides one stable and bounded
implementation target derived from one complete Privacy Engine Protocol
Specification.

It identifies and organizes the normative requirements applicable to one
defined implementation role, capability set, or deployment class.

The implementation profile narrows applicability.

It does not redefine protocol semantics.

It does not redefine the Privacy Engine Protocol Specification.

It does not define an implementation.

It does not establish conformance or certification.

The purpose of this document is to define the implementation profile itself as
an implementation-facing architectural object.

# 2. Scope

This document defines:

- the implementation profile;
- implementation-profile identity;
- derivation from one Privacy Engine Protocol Specification;
- profile scope;
- profile boundedness;
- profile applicability;
- profile composition;
- requirement selection;
- preservation of requirement strength;
- treatment of optional and implementation-defined behavior;
- profile dependencies;
- profile completeness;
- the relationship between profiles and implementations;
- the relationship between profiles and reference implementations;
- the relationship between profiles and conformance or certification;
- the relationship between profiles and compatibility;
- preservation of protocol semantics;
- protocol authority.

This document does not define:

- protocol behavior;
- implementation behavior;
- implementation architecture;
- implementation APIs;
- implementation algorithms;
- implementation source structure;
- implementation deployment procedures;
- a concrete implementation profile;
- a reference implementation;
- conformance assessment;
- certification;
- compatibility assessment;
- protocol publication;
- protocol succession;
- protocol lineage.

No actual implementation profile is specified by this document.

This document defines only the architectural model under which such profiles
may later be created.

# 3. Primary Definition

A Privacy Engine implementation profile is a uniquely identified, bounded, and
complete implementation-facing selection and organization of applicable
normative requirements derived from one Privacy Engine Protocol Specification
for one defined implementation role, capability set, or deployment class.

Let:

- `P` be one published Privacy Engine protocol generation;
- `S` be one Privacy Engine Protocol Specification;
- `F` be one implementation profile;
- `R` be one normative requirement;
- `I` be one implementation.

Then:

> derives(S, P)

> derives(F, S)

> applies(F, R)

> implements(I, F)

The architectural progression is:

> P -> S -> F -> I

The published protocol generation is the semantic authority.

The Protocol Specification is the complete implementation-facing composition
derived from that generation.

The implementation profile identifies the bounded requirements and permitted
choices applicable to one declared implementation target.

The implementation realizes that target.

The profile therefore occupies the applicability boundary between the complete
Protocol Specification and an implementation.

It does not create protocol semantics.

It identifies the bounded applicability of existing protocol semantics.

# 4. Implementation Profile Identity

Every implementation profile must possess one stable and unambiguous identity.

Profile identity distinguishes one profile from:

- the Protocol Specification from which it derives;
- other profiles derived from the same specification;
- profiles derived from other specifications;
- implementations claiming to implement the profile;
- reference implementations associated with the profile;
- conformance claims concerning the profile;
- compatibility declarations concerning implementations.

Let:

> identity(F) = profileIdentity

A profile identity must identify exactly one profile definition.

Two profiles with different applicability, scope, dependencies, or resolved
choices are distinct profiles.

Therefore:

> differentBoundary(F1, F2) -> identity(F1) != identity(F2)

A profile must not silently change while retaining an identity that implies
unchanged applicability or unchanged obligations.

A modification that changes any semantically relevant part of the profile may
require a distinct profile identity.

Semantically relevant parts include:

- declared role;
- declared capability set;
- declared deployment class;
- applicable requirements;
- requirement applicability conditions;
- resolved optional choices;
- resolved implementation-defined choices;
- profile dependencies.

Editorial changes that do not alter profile semantics do not necessarily
require a new profile identity.

Profile identity does not confer protocol authority.

It provides stable identification only.

# 5. Derivation from the Protocol Specification

Every implementation profile derives from exactly one identified Privacy
Engine Protocol Specification.

Let:

> derives(F, S)

A profile must not derive directly from:

- an implementation;
- a reference implementation;
- a conformance claim;
- a certification result;
- a compatibility declaration;
- informal implementation practice;
- an unpublished protocol draft;
- an unidentified mixture of specifications.

The profile receives its available normative content from the Protocol
Specification.

The specification itself derives from one published protocol generation:

> derives(S, P)

Therefore:

> derives(F, S) and derives(S, P)

establish the preservation path:

> P -> S -> F

The profile may identify applicability within the specification.

It may not create obligations absent from the specification.

It may not remove obligations that apply to its declared scope.

It may not alter the semantic meaning of any selected requirement.

For every requirement applied by the profile:

> applies(F, R) -> specifiedBy(S, R)

The profile is derivative.

The specification is complete.

The published protocol generation remains authoritative.

# 6. Profile Scope and Boundedness

Every implementation profile must declare one bounded implementation target.

The target may be defined by one or more of:

- implementation role;
- supported capability set;
- deployment class;
- operational responsibility;
- protocol participation boundary;
- specification-defined implementation category.

The declared target determines the boundary within which requirement
applicability is evaluated.

Let:

> scope(F) = T

where `T` is the bounded implementation target described by the profile.

A profile must not claim an undefined or unlimited scope.

A profile boundary must be sufficiently precise to determine:

- which specification requirements are relevant;
- which requirements apply;
- which permitted choices must be resolved;
- which dependencies must be satisfied;
- what an implementation claiming the profile is expected to realize.

Boundedness requires that the profile neither silently expands beyond its
declared target nor silently excludes requirements within that target.

Formally:

> relevant(F, R) -> resolvedApplicability(F, R)

The profile must account for every requirement relevant to its declared scope.

A bounded profile is not necessarily a small profile.

Boundedness concerns the precision of its architectural boundary, not the
number of requirements it applies.

A profile may cover:

- one narrow implementation role;
- several related capabilities;
- one defined deployment class;
- a complete composite implementation target.

In every case, the profile boundary must remain explicit.

# 7. Profile Applicability

Applicability determines whether a normative requirement governs
implementations of a profile.

Let:

> applies(F, R)

mean that normative requirement `R` applies to implementations of profile `F`.

Applicability is derived from:

- the requirement's existing specification meaning;
- the requirement's declared applicability conditions;
- the profile's declared scope;
- the profile's defined capabilities;
- the profile's deployment class;
- permitted specification choices resolved by the profile.

Applicability must not be invented independently of the specification.

A profile may narrow the complete specification to the requirements governing
its declared target.

It may not use narrowing to escape obligations that govern that target.

Therefore:

> relevant(F, R) and mandatoryForScope(S, R, scope(F))
> -> applies(F, R)

A profile must distinguish at least:

- applicable requirements;
- non-applicable requirements;
- conditionally applicable requirements;
- requirements resolved through a permitted specification choice.

Non-applicability must arise from the profile boundary or from applicability
rules already permitted by the specification.

It must not arise from preference, convenience, implementation difficulty, or
post hoc implementation behavior.

Applicability is not reinterpretation.

Applicability answers:

> Does this existing normative requirement govern implementations of this
> profile?

It does not answer:

> What should this normative requirement mean?

Requirement meaning remains fixed by the specification and ultimately by the
published protocol generation.

# 8. Profile Composition

An implementation profile is a bounded implementation-facing composition.

Its composition may include:

- profile identity;
- source Protocol Specification identity;
- declared implementation target;
- declared scope;
- applicability determinations;
- references to applicable normative requirements;
- permitted optional choices;
- resolved implementation-defined choices;
- profile dependencies;
- completeness conditions.

Let:

> composition(F) =
> {
>   identity,
>   sourceSpecification,
>   scope,
>   applicability,
>   choices,
>   dependencies
> }

The profile organizes the applicability of normative requirements.

It does not acquire ownership of those requirements.

The normative requirements remain members of the Protocol Specification
architecture.

Therefore the primary relation is:

> applies(F, R)

rather than:

> contains(F, R)

This distinction preserves requirement identity.

The same normative requirement may apply to multiple profiles without being
duplicated or redefined.

For profiles `F1` and `F2`:

> applies(F1, R) and applies(F2, R)

does not create two normative requirements.

It identifies the applicability of the same requirement to two bounded
implementation targets.

The profile may contain profile-specific applicability records and permitted
choice resolutions.

It must not contain rewritten substitute requirements that compete with the
requirements defined by the Protocol Specification.

# 9. Requirement Selection

Requirement selection is the bounded act by which a profile records that an
existing normative requirement applies to the profile.

Selection identifies applicability.

Selection does not create requirement semantics.

Let:

> selects(F, R) -> applies(F, R)

Selection must be justified by:

- profile scope;
- profile role;
- profile capability set;
- profile deployment class;
- specification-defined applicability;
- a permitted specification choice.

A profile must not select requirements from outside its source Protocol
Specification.

Therefore:

> selects(F, R) -> specifiedBy(S, R)

where:

> derives(F, S)

A profile must not use selection to:

- invent new obligations;
- weaken existing obligations;
- strengthen recommendations without declaring a permitted profile choice;
- permit prohibited behavior;
- prohibit mandatory behavior;
- remove requirements that govern the declared target;
- combine unrelated requirements into a new semantic object;
- replace requirement identity with profile-local wording.

Selection is not invention.

Selection is not requirement authorship.

Selection is the implementation-facing record of bounded applicability.

# 10. Requirement-Strength Preservation

A profile must preserve the normative strength of every requirement it
applies.

Let:

> strength(S, R)

represent the normative strength of requirement `R` in the Protocol
Specification.

Then:

> applies(F, R) -> strength(F, R) = strength(S, R)

A profile must not:

- convert a mandatory requirement into a recommendation;
- convert a prohibition into a discouragement;
- convert a recommendation into an optional statement without permission;
- convert an optional behavior into a mandatory behavior unless the
  specification permits the profile to require that option;
- convert implementation-defined behavior into unconstrained behavior;
- change the applicability condition of a requirement without specification
  authority.

The profile may narrow which requirements apply.

It must not weaken the obligations of requirements that do apply.

Therefore:

> narrowerApplicability(F) != weakerObligation(F)

For each applicable requirement:

> obligation(F, R) = obligation(S, R)

The profile may repeat requirement identifiers or concise references for
organization.

Any repetition remains subordinate to the requirement's authoritative
specification expression.

Profile wording must not create a conflicting interpretation.

# 11. Optional and Implementation-Defined Behavior

A Protocol Specification may permit optional behavior or identify behavior
whose bounded resolution is implementation-defined.

An implementation profile may resolve such choices only within the choice
space permitted by the specification.

Let:

> choicePermitted(S, C)

Then:

> selectsChoice(F, C) -> choicePermitted(S, C)

A profile may:

- require support for a specification-permitted optional capability;
- exclude a specification-permitted optional capability from its target;
- select one permitted alternative;
- constrain a permitted implementation-defined choice;
- leave a choice to the implementation where the specification permits that
  choice to remain implementation-defined.

A profile may not:

- introduce an alternative absent from the specification;
- treat mandatory behavior as optional;
- treat prohibited behavior as permitted;
- leave a mandatory profile-level choice unresolved;
- widen an implementation-defined choice beyond its specification boundary;
- use implementation-defined behavior to alter protocol semantics.

Where a profile resolves a permitted choice:

> profileResolution(F, C) subsetOf permittedChoices(S, C)

Where a profile leaves a choice to implementations:

> implementationChoice(I, C) subsetOf permittedChoices(F, C)

Implementation-defined does not mean semantically unconstrained.

It means that the specification or profile permits the implementation to
choose within an already bounded choice space.

A profile resolution is part of the profile identity when that resolution
changes the target implemented by conforming implementations.

# 12. Profile Dependencies

An implementation profile may depend on another identified implementation
profile where realizing the first profile necessarily requires realizing the
second.

Let:

> depends(F1, F2)

A profile dependency means:

> implements(I, F1) and depends(F1, F2)
> -> implements(I, F2)

Dependencies must be explicit.

A profile must not rely on hidden profile dependencies.

A dependency must identify:

- the depended-upon profile;
- the dependency direction;
- whether the dependency is mandatory or conditionally applicable;
- the condition under which any conditional dependency applies.

A profile dependency does not merge profile identities.

Therefore:

> depends(F1, F2) -> identity(F1) != identity(F2)

unless the two references already identify the same profile.

A profile dependency does not transfer protocol authority.

It does not make one profile semantically authoritative over another.

Each profile remains derived from its own identified source Protocol
Specification.

Where dependent profiles derive from the same specification, their combined
use remains bounded by that specification.

Where profile composition across different specifications is later permitted,
that relationship must be explicitly defined elsewhere and must not be inferred
from this model.

Profile dependency is distinct from:

- specification-section dependency;
- normative-requirement dependency;
- runtime component dependency;
- source-code dependency;
- deployment dependency;
- compatibility;
- protocol succession.

# 13. Profile Completeness

An implementation profile must be complete relative to its declared scope.

Profile completeness does not require every normative requirement in the
Protocol Specification to apply.

It requires every requirement relevant to the profile boundary to be
accounted for.

Let:

> complete(F)

A profile is complete only when:

> for every R:
> relevant(F, R) -> resolvedApplicability(F, R)

For each relevant requirement, the profile must determine whether the
requirement is:

- applicable;
- non-applicable under an identified specification rule;
- conditionally applicable;
- resolved through a permitted choice.

For every applicable requirement:

> applies(F, R) -> preserved(F, R)

Completeness also requires that:

- the source Protocol Specification is identified;
- profile identity is established;
- profile scope is declared;
- permitted profile-level choices are resolved;
- dependencies are identified;
- no required applicability decision remains ambiguous;
- no applicable obligation is silently omitted.

A profile is incomplete when:

- its scope is ambiguous;
- relevant requirements are unaccounted for;
- applicable requirements are omitted;
- prohibited requirements are treated as selectable;
- mandatory choices remain unresolved;
- dependencies are hidden;
- profile wording conflicts with the source specification.

Completeness is bounded completeness.

It is completeness of the declared implementation target.

It is not completeness of the entire Protocol Specification.

# 14. Relationship to Implementations

An implementation profile defines a stable target for implementations.

Let:

> implements(I, F)

An implementation implements a profile only if it realizes every applicable
profile obligation and every profile-level resolved choice.

At minimum:

> implements(I, F)
> -> for every R:
> applies(F, R) -> satisfies(I, R)

The profile defines what requirements apply.

The implementation defines how those requirements are realized, except where
the specification or profile already constrains the realization.

The profile does not define:

- source-code organization;
- internal module boundaries;
- programming language;
- deployment tooling;
- private implementation details;
- algorithms not already constrained by the specification;
- operational procedures not already constrained by the specification.

Multiple implementations may implement the same profile.

Let:

> implements(I1, F)

> implements(I2, F)

This does not require:

> architecture(I1) = architecture(I2)

It requires preservation of the same applicable obligations and resolved
profile choices.

An implementation may implement multiple profiles.

Let:

> implements(I, F1)

> implements(I, F2)

The implementation must satisfy the obligations of both profiles without
creating semantic conflict.

An implementation's existence does not alter the profile.

Implementation behavior does not retroactively determine profile meaning.

# 15. Relationship to Reference Implementations

A reference implementation is an identified implementation associated with one
or more implementation profiles for reference purposes.

Let:

> referenceImplementation(Ir, F)

Then:

> referenceImplementation(Ir, F) -> implements(Ir, F)

A reference implementation may demonstrate one valid realization of a profile.

It may support:

- implementation understanding;
- integration;
- testing;
- interoperability work;
- conformance-tool development;
- explanatory examples.

A reference implementation does not:

- define the profile;
- redefine applicable requirements;
- redefine requirement strength;
- replace the Protocol Specification;
- replace the published protocol generation;
- establish that all different implementations must share its internal design;
- become protocol authority.

Therefore:

> behavior(Ir) does not redefine semantics(F)

and:

> behavior(Ir) does not redefine semantics(S)

Where a reference implementation conflicts with the profile or source
specification, the implementation is incorrect or outdated.

The conflict does not change the profile or protocol semantics.

Reference status does not itself prove conformance.

Any conformance conclusion must follow the separately defined conformance
model.

# 16. Relationship to Conformance and Certification

An implementation profile provides an identified target against which
implementation conformance may later be evaluated.

The profile defines:

- applicable requirements;
- resolved profile choices;
- dependencies;
- the bounded target to be implemented.

Conformance defines whether an implementation satisfies that target.

The distinction is:

> profile defines the target

> conformance evaluates the implementation against the target

Let:

> conforms(I, F)

A necessary condition is:

> conforms(I, F) -> implements(I, F)

Conformance may require evidence that:

> for every R:
> applies(F, R) -> satisfies(I, R)

The full conformance model may additionally define:

- claims;
- evidence;
- assessment;
- test results;
- status;
- scope;
- issuing authority;
- validity;
- withdrawal.

Those subjects are outside this document.

Certification is also outside this document.

Certification may rely on an identified profile as the assessment target.

The profile itself does not:

- perform assessment;
- collect evidence;
- issue a claim;
- issue a certificate;
- grant certification status;
- guarantee implementation correctness.

A profile may exist without any implementation claiming conformance.

An implementation may claim to implement a profile without having been
certified.

The validity of that claim is determined by the applicable conformance and
certification architecture, not by this model.

# 17. Relationship to Compatibility

Implementation profiles and compatibility are related but distinct.

An implementation profile defines:

> what a bounded class of implementations must realize

Compatibility defines:

> the declared or evaluated relationship between an identified implementation
> and an identified protocol target or compatibility surface

A profile may support compatibility analysis by providing a stable
implementation target.

It does not itself constitute:

- a compatibility target;
- a compatibility surface;
- a compatibility statement;
- a compatibility declaration;
- a compatibility profile;
- a compatibility result.

Let:

> implements(I, F)

This relation alone does not necessarily establish every compatibility claim
that may later be made concerning `I`.

Compatibility may depend on additional identified surfaces, versions,
interfaces, or declared targets.

Likewise, a compatibility declaration does not redefine the implementation
profile.

The two remain separate:

> implementation profile -> applicable obligations

> compatibility -> declared or evaluated relationship

Neither relationship transfers protocol authority away from the published
protocol generation.

# 18. Preservation of Protocol Semantics

The implementation profile derives all semantic content from its source
Protocol Specification.

The Protocol Specification derives from one published protocol generation.

Let:

> derives(S, P)

> derives(F, S)

The profile may narrow applicability to one bounded implementation target.

Therefore:

> semantics(F) subsetOf semantics(S)

and:

> semantics(F) subsetOf semantics(P)

This subset relation expresses bounded applicability.

It does not permit altered semantics.

For every applicable normative requirement:

> applies(F, R) -> semantics(F, R) = semantics(S, R)

For every applied obligation:

> applies(F, R) -> obligation(F, R) = obligation(S, R)

For every requirement-strength classification:

> applies(F, R) -> strength(F, R) = strength(S, R)

For every profile choice:

> selectsChoice(F, C) -> choicePermitted(S, C)

The preservation path is:

> P -> preserved(S) -> bounded-preserved(F) -> realized(I)

Success path:

> S -> applicable(F) -> preserved(R)

Failure path:

> S -> profile construction fails

Forbidden path:

> S -> F -> reinterpreted(S')

A profile must fail to define a valid target rather than invent, repair,
weaken, merge, or reinterpret protocol semantics.

Selection chooses existing requirements.

Every later profile operation preserves those requirements.

If a profile cannot preserve an applicable requirement:

> return failure

not:

> choose, repair, weaken, merge, or infer a replacement requirement

The implementation profile is therefore a preservation layer over a bounded
part of the complete Protocol Specification.

# 19. Protocol Authority

The implementation profile is not protocol authority.

The Privacy Engine Protocol Specification is not independent protocol
authority.

The published Privacy Engine protocol generation remains the sole semantic
authority.

The authority chain is:

> published protocol generation
> -> Protocol Specification
> -> implementation profile
> -> implementation

Authority does not flow upward from implementations.

Authority does not originate in profiles.

Authority does not originate in reference implementations.

Authority does not originate in conformance or certification bodies.

The implementation profile may organize applicability.

It may not redefine the source semantics it organizes.

Where conflict exists:

- the implementation does not override the profile;
- the reference implementation does not override the profile;
- the profile does not override the Protocol Specification;
- the Protocol Specification does not override the published protocol
  generation.

Protocol authority always remains with the published protocol generation.

# 20. Explicit Exclusions

This document does not define a concrete Privacy Engine implementation profile.

It does not select any actual:

- implementation role;
- capability set;
- deployment class;
- normative requirement;
- optional capability;
- implementation-defined choice;
- profile dependency.

It does not define:

- application behavior;
- protocol operations;
- protocol interfaces;
- implementation interfaces;
- implementation APIs;
- algorithms;
- data structures;
- wire formats;
- deployment architecture;
- runtime topology;
- security controls;
- privacy mechanisms;
- cryptographic constructions;
- implementation testing;
- conformance tests;
- certification procedures;
- compatibility procedures.

It does not redefine:

- the published protocol generation;
- protocol publication;
- protocol succession;
- protocol lineage;
- the Privacy Engine Protocol Specification;
- specification sections;
- normative requirement sets;
- normative requirements;
- normative specification language;
- implementations;
- reference implementations;
- conformance;
- certification;
- compatibility.

It does not introduce a new semantic authority.

It does not reopen the completed foundational ontology.

It defines one bounded implementation-facing architectural subject:

> the Privacy Engine implementation profile

# 21. Conclusion

A Privacy Engine implementation profile is a uniquely identified, bounded, and
complete implementation-facing selection and organization of applicable
normative requirements derived from one Privacy Engine Protocol Specification
for one defined implementation role, capability set, or deployment class.

The Protocol Specification defines the complete implementation-facing
obligation space.

The implementation profile identifies the bounded applicable obligation space.

The implementation realizes that profile.

The architectural progression is:

> P -> S -> F -> I

The profile narrows:

- scope;
- applicability;
- supported capabilities;
- permitted choices.

The profile preserves:

- normative requirement identity;
- normative requirement meaning;
- requirement strength;
- applicable obligations;
- protocol semantics.

Selection is not invention.

Applicability is not reinterpretation.

Narrowing is not weakening.

Implementation is realization, not authority.

The implementation profile remains derivative and bounded.

Protocol authority always remains with the published protocol generation.
