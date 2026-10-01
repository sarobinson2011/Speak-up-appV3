# Privacy Engine Normative Requirement Set Model V1

STATE.md remains canonical.

# 1. Purpose

This document defines the architectural model of a normative requirement set within the Privacy Engine Protocol Specification.

It establishes:

- what a normative requirement set is;
- where a normative requirement set derives its authority;
- how a normative requirement set is identified;
- how its scope is bounded;
- how normative requirements become members of the set;
- how requirement identity is preserved within the set;
- how requirements may be organized without semantic modification;
- how requirement-set completeness is defined;
- how the set relates to individual normative requirements;
- how the set relates to normative statements and informative material;
- how the set relates to the implementation-facing protocol specification;
- how implementations satisfy requirements contained within the set;
- how the set supports conformance and certification;
- how protocol semantics remain preserved.

This document defines the bounded architectural composition of multiple normative requirements.

It does not define any actual Privacy Engine protocol requirement.

It does not define protocol behavior, implementation interfaces, algorithms, implementation profiles, conformance procedures, or certification procedures.

# 2. Scope

This document is limited to the architectural model of one normative requirement set.

It applies to a normative requirement set derived from one identified published Privacy Engine protocol generation and expressed within its implementation-facing Privacy Engine Protocol Specification.

It does not define:

- substantive protocol behavior;
- concrete normative requirements;
- concrete implementation obligations;
- requirement wording;
- requirement-strength vocabulary;
- applicability conditions for any actual requirement;
- implementation APIs;
- protocol operations;
- algorithms;
- data structures;
- wire formats;
- proof systems;
- implementation profiles;
- reference implementations;
- conformance-assessment procedures;
- evidence requirements;
- certification procedures;
- compatibility rules;
- requirement identifier syntax;
- specification numbering conventions;
- editorial publication procedures.

Those subjects are defined elsewhere when required.

This document does not reopen or expand the completed Privacy Engine formal ontology.

# 3. Definition of a Normative Requirement Set

A Privacy Engine normative requirement set is the bounded architectural composition of the normative requirements derived from one identified published Privacy Engine protocol generation for expression within its implementation-facing protocol specification.

Let:

- `P` be one published Privacy Engine protocol generation;
- `N` be one normative requirement set;
- `R` be one normative requirement;
- `S` be one normative statement;
- `E` be informative material;
- `I` be one implementation.

Then:

> derives(N, P)

A normative requirement set contains normative requirements:

> contains(N, R)

Every normative requirement contained within the set derives from the same published protocol generation:

> contains(N, R) → derives(R, P)

The requirement set is a bounded composition.

It is not itself a normative requirement.

Therefore:

> set(N)

> requirement(R)

> N ≠ R

The requirement set organizes normative requirements.

The individual requirement remains the semantic object that carries one identifiable obligation, prohibition, recommendation, discouragement, permission, or implementation-defined constraint.

The requirement set does not create, merge, weaken, strengthen, reinterpret, or replace the requirements it contains.

# 4. Requirement-Set Authority and Derivation

A normative requirement set derives from one identified published Privacy Engine protocol generation.

Formally:

> derives(N, P)

Derivation establishes the source of the set's normative content.

The requirement set does not obtain authority from:

- its document location;
- its title;
- its numbering;
- its editorial organization;
- its publication format;
- implementation convention;
- reference implementation behavior;
- conformance precedent;
- certification precedent;
- external practice.

Its normative content is derived only from the published protocol generation.

The derivation relationship is bounded:

> derives(N, P₁) ∧ derives(N, P₂) → P₁ = P₂

One normative requirement set must not silently combine normative requirements from multiple published protocol generations.

Requirements belonging to different published protocol generations may be compared or mapped elsewhere.

They must not be presented as one undifferentiated authoritative requirement set.

The requirement set is therefore generation-specific.

The valid authority path is:

> P → N

The invalid authority path is:

> N → P

The requirement set derives from the published protocol generation.

It does not define the published protocol generation.

# 5. Requirement-Set Identity

A normative requirement set must possess a stable and uniquely distinguishable identity.

Formally:

> identity(N)

A requirement-set identifier may identify the set:

> identifies(IDₙ, N)

The identifier is not the set itself:

> IDₙ ≠ N

Requirement-set identity distinguishes:

- one requirement set from another;
- one protocol generation's set from another generation's set;
- one complete membership boundary from a materially different membership boundary;
- the semantic composition from its editorial presentation.

Requirement-set identity depends upon:

- the identified published protocol generation from which the set derives;
- the bounded membership of normative requirements belonging to the set;
- the intended scope represented by the set.

Requirement-set identity does not depend upon:

- document pagination;
- section ordering;
- typography;
- formatting;
- filename;
- publication medium;
- explanatory prose;
- examples;
- diagrams;
- editorial reflow.

A change that only alters presentation does not create a new semantic requirement set when:

- the same requirements remain members;
- every requirement retains its identity;
- requirement strength remains unchanged;
- requirement scope remains unchanged;
- requirement applicability remains unchanged;
- requirement satisfaction conditions remain unchanged;
- the set continues to derive from the same published protocol generation.

A change to the semantic membership boundary may produce a different requirement-set composition.

Formally:

> membership(N₁) ≠ membership(N₂) → N₁ ≠ N₂

This distinction applies when the membership difference is semantic rather than merely editorial.

Requirement-set identity must not be inferred solely from similarity of wording.

# 6. Requirement-Set Scope and Boundedness

A normative requirement set has an explicit scope.

The scope identifies the bounded normative surface represented by the set.

Formally:

> scope(N)

The scope may represent:

- the complete normative requirements of one published protocol generation;
- a clearly identified normative subdivision of that generation;
- a clearly identified implementation-facing protocol surface;
- another explicitly bounded subset when the specification architecture requires one.

The scope must be explicit.

A requirement set must not rely upon unstated boundaries.

For every member requirement:

> contains(N, R) → withinScope(R, N)

A requirement outside the defined scope must not be silently treated as a member:

> ¬withinScope(R, N) → ¬contains(N, R)

Scope does not modify requirement semantics.

It determines whether a requirement belongs within the bounded composition.

The requirement set must not use scope to:

- weaken a requirement;
- strengthen a requirement;
- alter requirement applicability;
- conceal an obligation;
- convert normative content into informative content;
- create a requirement not derived from the published protocol generation.

Boundedness requires that the set remain attached to its identified source generation and declared scope.

Formally:

> bounded(N, P, scope(N))

A bounded requirement set does not become a universal collection of all Privacy Engine requirements across all protocol generations, profiles, implementations, or applications.

# 7. Requirement Membership

Requirement membership is the explicit architectural relationship between a normative requirement set and an individual normative requirement.

Formally:

> contains(N, R)

Membership means:

- `R` is one identified normative requirement;
- `R` belongs within the declared scope of `N`;
- `R` derives from the same published protocol generation as `N`;
- `R` remains independently identifiable within the set.

Membership requires:

> contains(N, R) → requirement(R)

> contains(N, R) → derives(R, P)

> contains(N, R) → derives(N, P)

> contains(N, R) → withinScope(R, N)

A member requirement does not lose its identity by entering the set.

Therefore:

> contains(N, R) → preservesIdentity(N, R)

The set must not treat two distinct requirements as one requirement merely because they:

- use similar wording;
- concern the same protocol surface;
- share the same requirement strength;
- apply to the same implementation;
- appear in the same section;
- contribute to the same implementation objective.

Likewise, the set must not divide one requirement into multiple independent requirements merely because its expression spans multiple normative statements.

Requirement membership is semantic membership.

It is not merely:

- proximity in a document;
- inclusion in one section;
- appearance under one heading;
- presence in one file;
- mention by informative material.

Membership must be explicit or deterministically established by the specification structure.

Informative material is not a member of the requirement set.

Normative statements are not members merely because they express member requirements.

The member is the requirement semantic object.

# 8. Membership Integrity and Preservation

A normative requirement set must preserve every member requirement.

Formally:

> contains(N, R) → preserves(N, R)

Preservation means that set membership does not modify:

- requirement identity;
- requirement authority;
- requirement strength;
- requirement scope;
- requirement applicability;
- requirement conditions;
- requirement satisfaction criteria;
- requirement relationship to the published protocol generation.

For a member requirement:

> identity(R within N) = identity(R)

> strength(R within N) = strength(R)

> scope(R within N) = scope(R)

> applicability(R within N) = applicability(R)

> satisfactionConditions(R within N) = satisfactionConditions(R)

The set may not repair, complete, infer, or reinterpret a requirement.

The preservation function is:

> R → preserved(R)

The failure path is:

> R → membership failure

The forbidden path is:

> R → R′

where `R′` is a weakened, strengthened, merged, divided, inferred, repaired, or otherwise reinterpreted requirement.

When a requirement cannot be preserved as a member of the set, it must not be silently replaced.

Membership must fail or the specification source must be corrected through the appropriate protocol-authority process.

# 9. Requirement Organization

A normative requirement set may organize its member requirements.

Organization may support:

- specification navigation;
- protocol-surface grouping;
- operation grouping;
- interface grouping;
- role grouping;
- applicability grouping;
- implementation-profile mapping;
- conformance traceability;
- cross-reference structure.

Formally:

> organizes(N, R)

Organization is distinct from membership:

> organizes(N, R) → contains(N, R)

but:

> contains(N, R) does not require one particular editorial location

Organization does not define requirement semantics.

Therefore:

> organization(N) ≠ semantics(N)

Moving a requirement between organizational categories must not alter:

- its identity;
- its normative strength;
- its scope;
- its applicability;
- its satisfaction conditions;
- its source protocol generation.

A requirement may participate in multiple navigational or cross-reference groupings without becoming multiple requirements.

Formally:

> groupedAs(R, G₁)

> groupedAs(R, G₂)

does not imply:

> R₁ ≠ R₂

when both groupings reference the same requirement identity.

Organization must not create hidden obligations through:

- section titles;
- category names;
- table placement;
- diagram position;
- ordering;
- adjacency;
- editorial hierarchy.

All normative obligations remain carried by identified normative requirements.

# 10. Requirement-Set Completeness

Requirement-set completeness is defined relative to:

- one identified published protocol generation;
- one explicitly declared requirement-set scope.

Formally:

> complete(N, P, scope(N))

A requirement set is complete for its declared scope when every normative requirement derived from `P` and belonging within that scope is represented as an identified member of `N`.

Formally:

> complete(N, P, scope(N))
> ↔
> ∀R, derives(R, P) ∧ withinScope(R, N) → contains(N, R)

Completeness also requires that every member belongs legitimately to that scope:

> complete(N, P, scope(N))
> →
> ∀R, contains(N, R) → derives(R, P) ∧ withinScope(R, N)

A protocol-wide requirement set is complete when its declared scope is the complete normative surface of the published protocol generation and every derived normative requirement is represented.

Completeness does not mean:

- that informative explanation is exhaustive;
- that every implementation technique is described;
- that every implementation choice is prescribed;
- that every possible implementation is anticipated;
- that reference code exists;
- that conformance evidence exists;
- that conformance has been assessed;
- that certification has been granted.

Completeness concerns the normative membership boundary.

It does not establish implementation satisfaction.

A complete set may be satisfied or not satisfied by a particular implementation.

An incomplete set must not be represented as the complete normative basis of the identified scope.

Missing requirements must not be replaced by:

- implementation convention;
- informative prose;
- reference implementation behavior;
- assumed common practice;
- conformance precedent;
- certification precedent.

# 11. Relationship to Normative Requirements

Engineering[130] defines the individual normative requirement as the stable semantic object carrying one identifiable normative constraint.

This document defines the bounded composition of those objects.

The relationship is:

> set(N)

> requirement(R)

> contains(N, R)

The requirement remains individually identifiable.

The set supplies:

- bounded membership;
- organization;
- completeness relative to scope;
- specification-level composition.

The set does not supply:

- new requirement authority;
- new requirement strength;
- new applicability;
- new satisfaction conditions;
- new protocol semantics.

A requirement may exist as an identified semantic object before its final editorial placement within the specification.

Its inclusion within a set records that it belongs to the bounded normative composition.

The requirement set must not become a substitute for individual requirement identity.

Conformance, traceability, and satisfaction must remain capable of addressing individual requirements.

# 12. Relationship to Normative Statements and Informative Material

A normative statement expresses a normative requirement.

Formally:

> expresses(S, R)

The normative statement is not the requirement:

> S ≠ R

The requirement set contains the requirement, not the statement merely as wording:

> contains(N, R)

The specification may associate the expressing statement with the member requirement:

> expresses(S, R) ∧ contains(N, R)

A requirement may be expressed by one normative statement or by a bounded set of coordinated normative statements.

That editorial expression does not change requirement-set membership.

Formally:

> expresses(S₁, R)

or:

> expresses({S₁, S₂, ..., Sₙ}, R)

while:

> contains(N, R)

The requirement remains one member when multiple statements express the same semantic object.

Informative material may explain a member requirement:

> explains(E, R)

Informative material does not become a normative requirement:

> ¬requirement(E)

Informative material does not become a member of the normative requirement set:

> ¬contains(N, E)

Informative material must not:

- create hidden requirements;
- expand requirement scope;
- change requirement strength;
- alter applicability;
- alter satisfaction conditions;
- compensate for a missing normative requirement;
- become normative through proximity to a requirement.

The requirement set is therefore not the complete document-content set of the protocol specification.

It is the bounded semantic composition of normative requirements only.

# 13. Relationship to the Privacy Engine Protocol Specification

The Privacy Engine Protocol Specification expresses and organizes the normative requirement set in implementation-facing form.

The architectural relationship is:

> published protocol generation
> → normative requirement set
> → normative requirements
> → normative statements
> → implementation-facing specification

The specification may contain:

- normative statements;
- informative explanation;
- notes;
- examples;
- diagrams;
- cross-references;
- implementation guidance;
- editorial structure.

The normative requirement set contains only the identified normative requirements.

The specification is therefore broader in documentary content than the requirement set.

Formally:

> content(Specification) ⊃ expressionOf(N)

where the additional content may be informative rather than normative.

The specification must preserve the requirement set.

Formally:

> expresses(Specification, N)

> semantics(expressionOf(N)) = semantics(N)

The specification must not:

- silently omit member requirements;
- create requirements through informative material;
- alter requirement identities through wording;
- merge distinct requirements without preserving identity;
- divide one requirement into accidental hidden obligations;
- extend the requirement set beyond the published protocol generation;
- claim independent protocol authority.

The requirement set supplies the bounded normative composition that the specification communicates.

The specification does not become the source of protocol semantics merely because it is implementation-facing.

# 14. Relationship to Implementations

An implementation is subject to the normative requirements that are applicable to it.

For a member requirement:

> contains(N, R)

> applicable(R, I) → obligation(R, I)

> ¬applicable(R, I) → ¬obligation(R, I)

The requirement set does not make every contained requirement applicable to every implementation.

Applicability remains a property of each requirement in relation to the identified implementation and stated conditions.

An implementation satisfies an individual requirement when it fulfills that requirement's satisfaction conditions:

> satisfies(I, R)

An implementation fails an individual requirement when it does not fulfill those conditions:

> ¬satisfies(I, R)

Set-level satisfaction is an aggregate description over applicable member requirements.

Formally:

> satisfies(I, N)
> ↔
> ∀R, contains(N, R) ∧ applicable(R, I) → satisfies(I, R)

Set-level satisfaction does not erase individual requirement identity.

It does not convert the requirement set into one indivisible requirement.

The aggregate result is derived from the satisfaction of applicable member requirements.

If an applicable mandatory member requirement is not satisfied, the implementation does not satisfy the complete applicable mandatory requirement set.

The requirement set does not prescribe how an implementation must be internally structured unless an individual member requirement explicitly carries such a constraint from the published protocol generation.

Implementation variation remains permitted wherever the normative requirements permit it.

# 15. Relationship to Conformance and Certification

A normative requirement set provides a bounded normative basis for later conformance evaluation.

The conformance basis consists of the member requirements applicable to the implementation under assessment.

Formally:

> applicableSet(N, I)
> =
> {R | contains(N, R) ∧ applicable(R, I)}

A conformance evaluation may assess whether the implementation satisfies each applicable requirement:

> evaluates(conformanceEvaluation(I, N), satisfies(I, R))

for every:

> R ∈ applicableSet(N, I)

The requirement set does not itself define:

- conformance claims;
- conformance-assessment procedures;
- evidence collection;
- evidence sufficiency;
- test procedures;
- assessment outcomes;
- certification decisions;
- certification status;
- compatibility declarations.

Those remain distinct architectural subjects.

The requirement set supplies the normative population against which assessment may occur.

Conformance does not create or modify requirement-set membership.

Certification does not create or modify requirement-set membership.

Therefore:

> assessment(N) does not redefine N

> certification(N) does not redefine N

A precedent established by one assessment or certification decision must not silently alter the requirement set for later implementations.

Any semantic change must occur through the published protocol-generation authority model, not through assessment practice.

# 16. Preservation of Protocol Semantics

A normative requirement set must preserve the semantics of the published protocol generation from which it derives.

For every member requirement:

> contains(N, R) → semantics(R) ⊆ semantics(P)

The semantics of the set are the bounded composition of the semantics of its member requirements:

> semantics(N)
> =
> ⋃ {semantics(R) | contains(N, R)}

Therefore:

> semantics(N) ⊆ semantics(P)

The requirement set must not contain semantic content outside the published protocol generation.

The requirement set may:

- identify requirements;
- compose requirements;
- organize requirements;
- establish membership;
- establish completeness relative to scope;
- support implementation traceability;
- support conformance traceability.

The requirement set must not:

- add protocol behavior;
- remove protocol behavior;
- reinterpret protocol behavior;
- strengthen protocol obligations;
- weaken protocol obligations;
- repair protocol semantics;
- infer missing protocol semantics;
- substitute implementation convention for protocol semantics.

The preservation path is:

> P → derived requirements → bounded requirement set

The failure path is:

> P → derivation failure

The forbidden path is:

> P → N → P′

where `P′` is an expanded, reduced, repaired, merged, inferred, or otherwise reinterpreted protocol.

Composition must preserve its inputs.

Formally:

> selection chooses {R₁, R₂, ..., Rₙ}

> composition preserves {R₁, R₂, ..., Rₙ}

If composition cannot preserve the selected requirements:

> return failure

It must not choose, repair, merge, infer, or manufacture:

> {R′₁, R′₂, ..., R′ₘ}

# 17. Protocol Authority

A normative requirement set is not an independent protocol authority.

Its authority is entirely derivative.

Formally:

> derives(N, P)

The requirement set may organize and expose normative requirements derived from the published protocol generation.

It may not:

- redefine the published protocol generation;
- override the published protocol generation;
- amend the published protocol generation;
- extend the published protocol generation;
- narrow the published protocol generation;
- resolve protocol ambiguity by invention;
- treat implementation behavior as protocol truth;
- treat conformance precedent as protocol truth;
- treat certification precedent as protocol truth.

If the requirement set conflicts with the published protocol generation, the requirement set is incorrect.

The conflict must not be resolved by granting authority to the requirement set.

The valid authority direction is:

> published protocol generation
> → normative requirement set
> → normative requirements
> → normative statements
> → implementation obligations

Authority must not flow in reverse.

Neither the requirement set, the protocol specification, an implementation, a conformance assessment, nor a certification decision may become the source of published protocol semantics.

Protocol authority always remains with the published protocol generation.

# 18. Explicit Exclusions

This document does not define:

- any actual Privacy Engine protocol requirement;
- any actual implementation obligation;
- any protocol operation;
- any protocol state;
- any protocol transition;
- any interface contract;
- any concrete interface;
- any algorithm;
- any proof system;
- any data structure;
- any encoding;
- any wire format;
- any application behavior;
- any implementation profile;
- any reference implementation;
- any requirement identifier format;
- any specification numbering scheme;
- any conformance-assessment procedure;
- any evidence model;
- any certification procedure;
- any compatibility declaration;
- any protocol-generation publication process;
- any protocol-succession rule.

This document does not:

- redefine the normative specification language;
- redefine the normative requirement model;
- redefine requirement strength;
- redefine applicability;
- redefine satisfaction;
- redefine conformance;
- redefine certification;
- redefine compatibility;
- redefine the published protocol;
- expand the formal ontology.

No normative requirement may be inferred from an example, explanatory sentence, diagram, heading, ordering choice, or exclusion in this architectural model.

# 19. Conclusion

A Privacy Engine normative requirement set is the bounded architectural composition of the normative requirements derived from one identified published Privacy Engine protocol generation for expression within its implementation-facing protocol specification.

The set:

- derives from one published protocol generation;
- possesses a stable identity;
- has an explicit and bounded scope;
- contains independently identifiable normative requirements;
- preserves every member requirement;
- organizes requirements without modifying their semantics;
- may be complete relative to its declared scope;
- supports implementation traceability;
- supplies the normative basis for later conformance evaluation.

The requirement is the individual semantic object.

The requirement set is the bounded composition of those objects.

The normative statement communicates the requirement.

The protocol specification expresses and organizes the requirement set.

The implementation satisfies the applicable requirements contained within the set.

Conformance evaluates that satisfaction.

The requirement set does not create, merge, weaken, strengthen, repair, infer, reinterpret, or replace protocol semantics.

It does not become an independent authority.

Protocol authority always remains with the published protocol generation.
