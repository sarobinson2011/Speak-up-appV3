# Privacy Engine Normative Requirement Model V1

STATE.md remains canonical.

# 1. Purpose

This document defines the architectural model of a normative requirement within the Privacy Engine Protocol Specification.

It establishes:

- what a normative requirement is;
- where a normative requirement derives its authority;
- how a normative requirement is identified;
- how a normative requirement is scoped;
- how requirement strength applies;
- how requirement applicability is determined;
- how a requirement is expressed by normative statements;
- how a requirement relates to informative material;
- how a requirement applies to implementations;
- how requirement satisfaction participates in conformance;
- how multiple normative statements may communicate one requirement;
- how protocol semantics remain preserved.

This document defines the semantic object communicated by the normative specification language.

It does not define any actual Privacy Engine protocol requirement.

It does not define protocol behavior, implementation interfaces, algorithms, implementation profiles, conformance procedures, or certification procedures.

# 2. Scope

This document is limited to the architectural model of one normative requirement.

It applies to normative requirements appearing within an implementation-facing Privacy Engine Protocol Specification derived from one published Privacy Engine protocol generation.

It does not define:

- substantive protocol behavior;
- concrete implementation obligations;
- implementation APIs;
- protocol operations;
- algorithms;
- data structures;
- wire formats;
- proof systems;
- implementation profiles;
- reference implementations;
- conformance-assessment procedures;
- certification procedures;
- compatibility rules;
- requirement identifier syntax;
- specification numbering conventions.

Those subjects are defined elsewhere when required.

This document does not reopen or expand the completed Privacy Engine formal ontology.

# 3. Definition of a Normative Requirement

A Privacy Engine normative requirement is one uniquely identifiable semantic obligation, prohibition, recommendation, discouragement, permission, or implementation-defined constraint derived from one published Privacy Engine protocol generation and applicable to identified implementations under stated conditions.

Let:

- `P` be one published Privacy Engine protocol generation;
- `R` be one normative requirement;
- `S` be one normative statement;
- `I` be one implementation.

Then:

> derives(R, P)

A normative requirement is the stable semantic object carried by the normative specification.

A normative statement expresses that object.

An implementation may become obligated by that object when the requirement is applicable.

The requirement is not identical to its wording.

Therefore:

> requirement(R)

> statement(S)

> expresses(S, R)

> S ≠ R

The requirement remains semantically stable throughout expression, applicability determination, implementation, and conformance evaluation.

# 4. Requirement Authority and Derivation

Every normative requirement derives from exactly one identified published Privacy Engine protocol generation.

Formally:

> derives(R, P)

The requirement does not derive its authority from:

- editorial wording;
- section placement;
- document formatting;
- an implementation;
- an implementation profile;
- a reference implementation;
- a conformance assessment;
- a certification result;
- an informative note;
- an example;
- commentary.

The specification identifies and expresses requirements already derived from the published protocol generation.

It does not create independent protocol semantics.

The valid derivation path is:

> P → R → S

where:

> derives(R, P)

> expresses(S, R)

The invalid path is:

> S → new protocol semantics

A normative statement must not introduce a requirement whose semantics are not derived from the published protocol generation.

# 5. Requirement Identity

Every normative requirement must possess a stable and independently referenceable identity.

Requirement identity distinguishes one normative semantic object from another.

Formally:

> identity(R)

A requirement identifier may identify a requirement:

> identifies(ID, R)

But:

> ID ≠ R

The identifier is a reference mechanism.

It is not the semantic requirement itself.

Requirement identity must not depend solely upon:

- wording;
- sentence structure;
- paragraph location;
- section numbering;
- heading text;
- formatting;
- document layout;
- identifier spelling.

A requirement may be reworded without changing its identity only when its complete semantics, strength, scope, and applicability remain unchanged.

Formally:

> equivalentMeaning(S₁, S₂)

> expresses(S₁, R)

> expresses(S₂, R)

does not require:

> text(S₁) = text(S₂)

However:

> changedSemantics(S₁, S₂)

implies that the two statements must not be treated as interchangeable expressions of the same unchanged requirement.

A reference change does not by itself create a new requirement.

A semantic change does.

# 6. Requirement Scope

Every normative requirement must have a bounded and determinable scope.

Requirement scope identifies the architectural subject governed by the requirement.

Formally:

> scope(R, X)

where `X` is the bounded subject governed by `R`.

The scope may concern an identified:

- implementation;
- component;
- interface;
- operation;
- behavior;
- output;
- input;
- state transition;
- observable result;
- implementation choice;
- conformance-relevant condition.

This document does not define any concrete Privacy Engine scope.

It defines only that the scope of each normative requirement must be determinable.

A requirement must not rely on the reader to infer its governed subject from unrelated text.

If the governed subject cannot be determined, the requirement is not adequately assessable.

# 7. Requirement Strength

Every normative requirement has one explicit requirement-strength category.

Requirement strength is expressed using the normative categories defined by the Privacy Engine Normative Specification Language.

The categories include:

- mandatory;
- prohibited;
- recommended;
- discouraged;
- optional;
- implementation-defined.

Formally:

> strength(R, C)

where `C` is one explicit normative category.

If a normative statement expresses a requirement:

> expresses(S, R)

then the normative category used by the statement must communicate the strength of the requirement:

> category(S) = strength(R)

Requirement strength is a semantic property of the requirement.

It is not merely typographical emphasis.

The use of identical requirement vocabulary in two statements does not establish that the statements express the same requirement.

For example:

> category(S₁) = mandatory

> category(S₂) = mandatory

does not imply:

> expresses(S₁, R)

> expresses(S₂, R)

Requirement strength must not be silently changed by:

- paraphrasing;
- cross-reference;
- informative explanation;
- examples;
- implementation guidance;
- editorial restructuring.

# 8. Requirement Applicability

A normative requirement imposes an implementation obligation only when the requirement is applicable to that implementation.

Formally:

> applicable(R, I) → obligation(R, I)

Where a requirement is not applicable:

> ¬applicable(R, I) → ¬obligation(R, I)

Applicability must be determined from explicit normative conditions.

It must not be inferred solely from:

- informative commentary;
- examples;
- implementation conventions;
- reference implementation behavior;
- unstated assumptions;
- certification precedent;
- external practice.

Applicability may depend upon an implementation adopting or exposing an identified protocol capability, role, interface, operation, or implementation choice.

This document does not define any concrete applicability condition.

It defines only the requirement that applicability be explicit and assessable.

Applicability must not be confused with satisfaction.

An applicable requirement may be satisfied or not satisfied.

A non-applicable requirement creates no implementation obligation for the implementation to which it does not apply.

# 9. Requirement Expression

A normative requirement is communicated through one or more normative statements.

Formally:

> expresses(S, R)

A normative statement is the specification-language expression of a requirement.

The statement is not the requirement itself.

Therefore:

> wording(S) ≠ identity(R)

A requirement may be expressed by one complete normative statement:

> expresses(S, R)

A requirement may also be expressed by a bounded set of coordinated normative statements when the complete requirement cannot be communicated safely or clearly in one statement:

> expresses({S₁, S₂, ..., Sₙ}, R)

Where multiple statements express one requirement:

- every statement must contribute to the same bounded semantic object;
- the complete requirement must remain identifiable;
- the statements must not create hidden independent obligations;
- the requirement's strength must remain unambiguous;
- the requirement's scope must remain unambiguous;
- the requirement's applicability must remain unambiguous.

A requirement must not depend upon accidental aggregation of unrelated normative statements.

# 10. Relationship to Normative Statements

The Privacy Engine Normative Specification Language defines how normative statements communicate requirement strength and applicability.

The normative requirement model defines the semantic object communicated by those statements.

The relationship is:

> requirement(R)

> statement(S)

> expresses(S, R)

The statement communicates the requirement.

The requirement supplies the stable semantic identity.

A normative statement must not:

- silently express multiple independently assessable requirements;
- conceal applicability conditions;
- depend on informative material to complete its obligation;
- alter the requirement through editorial wording;
- create semantics not derived from the published protocol generation.

Where one statement appears to contain multiple independently applicable or independently assessable obligations, those obligations should normally be represented as distinct normative requirements.

A useful distinction is:

> independentlyAssessable(X) → independentlyIdentifiableRequirement(X)

This rule prevents unrelated obligations from being concealed inside one editorial statement.

# 11. Relationship to Informative Material

Informative material may explain a normative requirement.

Formally:

> explains(E, R)

where `E` is informative material.

Informative material may provide:

- rationale;
- context;
- examples;
- diagrams;
- implementation guidance;
- commentary;
- explanatory restatement.

Informative material must not independently create an implementation obligation.

Formally:

> ¬obligation(E, I)

Informative material must not:

- create a requirement;
- complete an incomplete requirement;
- modify requirement strength;
- modify requirement scope;
- modify requirement applicability;
- weaken a requirement;
- strengthen a requirement;
- conceal a requirement;
- override a normative statement;
- introduce new protocol semantics.

Therefore:

> explains(E, R)

does not imply:

> expresses(E, R)

A normative requirement must remain complete and assessable without relying upon informative material to provide missing normative meaning.

# 12. Relationship to Implementations

A normative requirement governs an implementation only when it is applicable to that implementation.

The complete relationship is:

> derives(R, P)

> expresses(S, R)

> applicable(R, I)

> obligation(R, I)

An implementation responds to the semantic requirement.

It is not evaluated merely against the surface wording of the statement.

The requirement remains the stable object across:

- specification expression;
- implementation interpretation;
- implementation behavior;
- conformance evaluation.

An implementation must not substitute:

- reference implementation behavior;
- common practice;
- local convention;
- informative examples;
- inferred intent;

for the applicable normative requirement.

Implementation architecture may differ from the structure of the specification provided that all applicable normative requirements are satisfied and protocol semantics are preserved.

# 13. Requirement Satisfaction

Requirement satisfaction describes whether one implementation fulfills one applicable normative requirement.

Formally:

> satisfies(I, R)

or:

> ¬satisfies(I, R)

Satisfaction is evaluated against the complete semantics of the requirement.

It is not established merely by:

- using matching terminology;
- reproducing specification wording;
- matching a reference implementation's internal structure;
- satisfying only part of a compound obligation;
- satisfying an informative example;
- claiming compatibility.

The meaning of satisfaction depends upon the requirement's strength and normative category.

For example:

- a mandatory requirement requires the mandated condition;
- a prohibited requirement requires the prohibited condition to remain absent;
- a recommended or discouraged requirement may permit a bounded exception under the rules of the normative language;
- an optional requirement permits but does not require the identified behavior;
- an implementation-defined requirement requires the implementation to make and document the permitted implementation choice as specified.

This document does not redefine those categories.

It preserves the categories established by the Privacy Engine Normative Specification Language.

# 14. Relationship to Conformance

Conformance evaluation determines whether an identified implementation satisfies the applicable normative requirements derived from an identified published Privacy Engine protocol generation.

Formally:

> conformanceEvaluation(I, P)

evaluates:

> {R | derives(R, P) ∧ applicable(R, I)}

A conformance evaluation therefore concerns requirement satisfaction:

> evaluates(conformanceEvaluation(I, P), satisfies(I, R))

This document does not redefine:

- conformance claims;
- conformance assessments;
- certification status;
- compatibility statements;
- compatibility profiles;
- compatibility targets;
- compatibility surfaces;
- compatibility declarations;
- protocol realization.

Those remain distinct architectural subjects.

A normative requirement participates in conformance as the semantic object against which implementation satisfaction is evaluated.

Neither the requirement nor its statement independently issues a conformance result.

# 15. Requirement Composition

A normative requirement may contain several semantically necessary clauses when those clauses together define one indivisible obligation.

A requirement may therefore be expressed through several coordinated statements:

> expresses({S₁, S₂, ..., Sₙ}, R)

This does not require the introduction of a new requirement hierarchy.

Composition remains bounded by requirement identity.

Clauses should remain part of one requirement only where they:

- govern the same bounded subject;
- share the same applicability;
- form one indivisible obligation;
- cannot be independently satisfied without changing the meaning of the whole;
- are evaluated together.

Where clauses are independently applicable or independently assessable, they should normally be represented as separate normative requirements.

Therefore:

> independentlyApplicable(X, Y) ∨ independentlyAssessable(X, Y)

normally implies:

> identity(R₁) ≠ identity(R₂)

Requirement composition must not be used to:

- conceal multiple obligations;
- avoid stable requirement identification;
- blur applicability;
- blur requirement strength;
- prevent independent assessment;
- create implicit requirements through cross-reference.

# 16. Requirement Clarity and Assessability

Every normative requirement must be sufficiently clear to support consistent implementation and assessment.

A requirement must make determinable:

- its semantic obligation;
- its governed subject;
- its requirement strength;
- its applicability;
- the condition required for satisfaction;
- any permitted exception;
- any implementation-defined choice.

Formally:

> assessable(R)

requires that:

> determinable(scope(R))

> determinable(strength(R))

> determinable(applicability(R))

> determinable(satisfactionCondition(R))

A requirement is not adequately assessable when its meaning depends upon:

- unstated assumptions;
- informative material supplying missing obligations;
- ambiguous cross-references;
- undefined terminology;
- implementation-specific convention;
- subjective preference without a bounded criterion.

Assessability does not require prescribing one implementation architecture.

It requires that conforming and non-conforming outcomes can be distinguished under the requirement's stated conditions.

# 17. Requirement Cross-References

A normative requirement may reference another normative requirement where the relationship is explicit and necessary.

Formally:

> references(R₁, R₂)

A cross-reference must not silently:

- create a new requirement;
- alter requirement identity;
- alter requirement strength;
- expand requirement scope;
- expand requirement applicability;
- complete an otherwise incomplete obligation;
- convert informative material into normative material.

Each referenced requirement retains its own identity.

Therefore:

> references(R₁, R₂)

does not imply:

> identity(R₁) = identity(R₂)

A cross-reference communicates a relationship between requirements.

It does not merge them unless the specification explicitly defines one composed requirement and preserves clear identity, scope, strength, applicability, and assessability.

# 18. Preservation of Protocol Semantics

The normative requirement model must preserve the semantics of the published Privacy Engine protocol generation.

Formally:

> derives(R, P)

and:

> semantics(R) ⊆ semantics(P)

A requirement must not add semantic content absent from the published protocol generation.

The specification-expression relationship must preserve meaning:

> expresses(S, R) → semantics(S) = semantics(R)

Where several statements express one requirement:

> expresses({S₁, S₂, ..., Sₙ}, R)

the combined normative meaning must equal the requirement's semantics:

> semantics({S₁, S₂, ..., Sₙ}) = semantics(R)

The valid preservation path is:

> P → R → preservedExpression(R)

The failure path is:

> P → R → ambiguous or incomplete expression → failure

The forbidden path is:

> P → editorial inference → R′

where:

> semantics(R′) ∉ semantics(P)

The specification must fail to define a requirement rather than invent, repair, merge, infer, or extend protocol semantics.

# 19. Protocol Authority

A normative requirement does not become an independent source of protocol authority.

A normative statement does not become an independent source of protocol authority.

The normative requirement model does not become an independent source of protocol authority.

The requirement derives from the published protocol generation:

> derives(R, P)

The statement expresses the requirement:

> expresses(S, R)

The specification preserves the semantics of the published protocol generation:

> semantics(Specification) = semantics(P)

If any conflict exists between:

- a normative requirement;
- a normative statement;
- an informative explanation;
- an implementation;
- an implementation profile;
- a reference implementation;
- a conformance assessment;
- a certification result;

and the published protocol generation, the published protocol generation governs.

Protocol authority always remains with the published protocol generation.

# 20. Explicit Exclusions

This document does not define:

- any actual Privacy Engine normative requirement;
- any protocol operation;
- any protocol algorithm;
- any interface contract;
- any API;
- any wire format;
- any proof-system behavior;
- any implementation profile;
- any reference implementation;
- any test vector;
- any conformance procedure;
- any certification procedure;
- any compatibility declaration;
- any requirement identifier syntax;
- any requirement-traceability tool;
- any document-generation process.

This document does not redefine:

- the Privacy Engine formal ontology;
- the published protocol model;
- the protocol generation model;
- protocol publication;
- protocol succession;
- protocol lineage;
- protocol realization;
- conformance;
- certification;
- compatibility;
- normative specification language.

No new first-class architectural ontology is introduced.

# 21. Conclusion

A Privacy Engine normative requirement is one uniquely identifiable semantic obligation, prohibition, recommendation, discouragement, permission, or implementation-defined constraint derived from one published Privacy Engine protocol generation and applicable to identified implementations under stated conditions.

The requirement is the stable semantic object.

The normative statement is its specification expression.

The implementation satisfies or does not satisfy the applicable requirement.

Conformance evaluation assesses that satisfaction.

The requirement's wording may change only where its identity, semantics, strength, scope, and applicability remain preserved.

Informative material may explain the requirement.

It must never independently create, modify, complete, weaken, strengthen, or conceal it.

The normative requirement model organizes and preserves protocol semantics.

It does not create them.

Protocol authority always remains with the published protocol generation.
