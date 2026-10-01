# Privacy Engine Normative Specification Language V1

STATE.md remains canonical.

# 1. Purpose

This document defines the normative specification language used throughout the
Privacy Engine Protocol Specification.

It establishes how implementation obligations, prohibitions, recommendations,
permissions, and bounded implementation choices are expressed.

It also establishes how normative material is distinguished from informative
material.

This document defines specification language only.

It does not define Privacy Engine protocol behavior.

It does not introduce new protocol semantics, architectural subjects,
implementation components, interfaces, algorithms, or conformance procedures.

# 2. Scope

This document governs the editorial expression and interpretation of requirements
derived from one published Privacy Engine protocol generation.

It applies to:

- normative statements;
- informative statements;
- requirement-strength vocabulary;
- applicability;
- recommendations and permitted exceptions;
- optional behavior;
- implementation-defined behavior;
- notes;
- examples;
- diagrams;
- editorial commentary;
- normative cross-references;
- requirement clarity;
- requirement assessability.

It does not determine which Privacy Engine behaviors are required.

That determination belongs to the semantics of the published protocol generation.

This document determines only how those established requirements are expressed.

# 3. Primary Definition

A Privacy Engine normative specification language is the bounded editorial
language through which requirements derived from one published Privacy Engine
protocol generation are expressed as explicit implementation obligations.

Let:

- P be one published Privacy Engine protocol generation;
- R be one normative specification requirement;
- E be one informative statement;
- I be one implementation.

Then:

> derives(R, P)

Where R applies to I:

> applicable(R, I) → obligation(R, I)

A conforming implementation must satisfy every applicable normative requirement
derived from its target published protocol generation:

> conforming(I, P)
> →
> ∀R ((derives(R, P) ∧ applicable(R, I)) → satisfies(I, R))

Normative specification language communicates established protocol meaning.

It does not create independent protocol meaning.

# 4. Normative and Informative Classification

Specification material is classified as either:

- normative; or
- informative.

Normative material establishes implementation obligations derived from the
published protocol generation.

Informative material explains, illustrates, contextualizes, or editorially
organizes established obligations.

The distinction is:

> normative(R) → may-establish-obligation(R, I)

> informative(E) → ¬obligation(E, I)

Informative material may explain a normative requirement:

> explains(E, R)

But:

> explains(E, R) → ¬obligation(E, I)

unless the same meaning is independently stated in normative material.

Classification must be explicit.

Requirement strength must not depend on tone, emphasis, typography, rhetorical
force, surrounding commentary, or assumed authorial intent.

# 5. Normative Statements

A normative statement expresses one or more implementation obligations derived
from the target published protocol generation.

A normative statement must:

- use an explicit normative requirement category;
- identify the subject to which the requirement applies;
- identify the required, prohibited, recommended, discouraged, permitted, or
  implementation-defined behavior;
- define or inherit a clear applicability scope;
- be interpretable without depending on informative material;
- preserve the semantics of the published protocol generation;
- be sufficiently precise for conformance assessment.

A normative statement must not depend on examples, notes, diagrams, captions, or
editorial commentary for completion of its obligation.

The complete required meaning must be recoverable from normative material alone:

> completeMeaning(R) ⊆ normativeMaterial

A normative statement should contain one primary obligation where practical.

Multiple independent obligations should not be combined where separation improves
interpretation or assessability.

# 6. Informative Statements

An informative statement may provide:

- explanation;
- rationale;
- background;
- context;
- implementation illustration;
- examples;
- notes;
- editorial guidance;
- non-normative diagrams;
- summaries of already-stated normative material.

Informative material must not:

- create an implementation obligation;
- create a prohibition;
- create an exception;
- define applicability;
- establish a default;
- narrow or widen a normative requirement;
- complete an otherwise incomplete normative requirement;
- silently alter requirement strength;
- become an independent source of protocol semantics.

Informative material may restate normative meaning for clarity, but any conflict
between informative and normative material must be resolved in favor of the
normative material.

Any conflict between the normative specification and the published protocol
generation must be resolved in favor of the published protocol generation.

# 7. Requirement-Strength Vocabulary

The Privacy Engine Protocol Specification uses a compact normative vocabulary.

The normative categories are:

- MUST;
- MUST NOT;
- SHOULD;
- SHOULD NOT;
- MAY;
- IMPLEMENTATION-DEFINED.

These categories communicate requirement strength only.

They do not create new protocol semantic classes.

Each category is an editorial representation of meaning already established by
the target published protocol generation.

Normative strength is determined by the designated category:

> strength(R) = designatedCategory(R)

Normative strength must not be inferred from casual wording:

> strength(R) ≠ inferredTone(R)

Words such as:

- required;
- necessary;
- expected;
- normally;
- preferably;
- allowed;
- can;
- ought;
- shall;

must not independently establish normative strength unless they appear as part of
an explicitly defined normative statement.

The uppercase normative vocabulary is the canonical expression of requirement
strength.

# 8. Mandatory Requirements

MUST identifies behavior required for conformance.

For a mandatory requirement R:

> category(R) = MUST

Where R applies to I:

> applicable(R, I) → obligation(R, I)

A conforming implementation must satisfy R:

> conforming(I, P) ∧ derives(R, P) ∧ applicable(R, I)
> →
> satisfies(I, R)

An implementation that violates an applicable MUST requirement does not conform
to the target published protocol generation.

MUST must be used only where no conforming implementation may omit or contradict
the required behavior.

Mandatory behavior must not be expressed only through forceful prose without the
MUST category.

# 9. Prohibited Requirements

MUST NOT identifies behavior forbidden for conformance.

For a prohibited requirement R:

> category(R) = MUST NOT

Where R applies to I:

> applicable(R, I) → prohibited(R, I)

A conforming implementation must not perform the prohibited behavior:

> conforming(I, P) ∧ derives(R, P) ∧ applicable(R, I)
> →
> ¬performs(I, R)

An implementation that violates an applicable MUST NOT requirement does not
conform to the target published protocol generation.

MUST NOT must be used where the prohibited behavior is incompatible with the
published protocol semantics.

A prohibition must not be hidden in a warning, note, rationale, example, or
editorial comment.

# 10. Recommended Requirements

SHOULD identifies behavior expected for conforming implementations where the
published protocol permits a bounded and justified exception.

For a recommended requirement R:

> category(R) = SHOULD

SHOULD means:

- the behavior is the expected implementation direction;
- omission may be permitted only where an applicable exception is consistent
  with the published protocol;
- all mandatory requirements must remain satisfied;
- the implementation must understand the consequences of departure;
- any required declaration of departure must follow the applicable implementation
  profile or conformance rules.

SHOULD must not be used where no valid exception exists.

Where no conforming exception exists, MUST is required.

A SHOULD requirement is not casual advice.

It communicates an expected protocol-preserving implementation choice.

# 11. Discouraged Requirements

SHOULD NOT identifies behavior expected to be avoided where the published protocol
permits a bounded and justified exception.

For a discouraged requirement R:

> category(R) = SHOULD NOT

SHOULD NOT means:

- the behavior is expected to be avoided;
- use may be permitted only where an applicable exception is consistent with the
  published protocol;
- all mandatory and prohibited requirements must remain satisfied;
- the implementation must understand the consequences of departure;
- any required declaration of departure must follow the applicable implementation
  profile or conformance rules.

SHOULD NOT must not replace MUST NOT where the behavior is incompatible with
protocol conformance.

# 12. Optional Behavior

MAY identifies behavior permitted but not required by the published protocol.

For an optional requirement R:

> category(R) = MAY

MAY means:

- the implementation is permitted to perform the identified behavior;
- omission of the behavior does not itself violate conformance;
- performance of the behavior must remain within all applicable normative
  constraints;
- the optional behavior must not alter required protocol semantics.

Optionality concerns whether permitted behavior is performed.

It does not permit an implementation to replace, weaken, or contradict mandatory
behavior.

A statement is not optional merely because it is phrased indirectly.

Optional behavior must be expressed explicitly through MAY.

# 13. Implementation-Defined Behavior

IMPLEMENTATION-DEFINED identifies a bounded choice deliberately left to the
implementation by the published protocol.

For an implementation-defined requirement R:

> category(R) = IMPLEMENTATION-DEFINED

IMPLEMENTATION-DEFINED means:

- the protocol deliberately permits more than one bounded realization;
- the implementation must select one permitted realization;
- the selected realization must be documented where required by the specification,
  implementation profile, or conformance process;
- the selected realization must preserve all applicable protocol semantics;
- the choice must remain within the explicitly permitted bounds.

The distinction is:

> MAY = whether permitted behavior is performed

> IMPLEMENTATION-DEFINED = which permitted realization is selected

IMPLEMENTATION-DEFINED must not mean:

- unspecified;
- accidental ambiguity;
- omitted specification work;
- unrestricted vendor discretion;
- permission to invent new protocol semantics;
- permission to alter a mandatory requirement;
- permission to select behavior outside the stated bounds.

Where behavior is not deliberately bounded by the published protocol, it must not
be classified as IMPLEMENTATION-DEFINED.

# 14. Applicability

Every normative requirement must have a clear applicability scope.

Applicability may be established:

- directly in the normative statement; or
- through a clearly normative enclosing scope.

Let R be a normative requirement and I an implementation.

Then:

> applicable(R, I)

means that R imposes the requirement category stated by R upon I.

Non-applicability is not violation:

> ¬applicable(R, I) → ¬violation(I, R)

Applicability must not be inferred solely from:

- informative headings;
- examples;
- notes;
- diagrams;
- implementation convenience;
- unstated assumptions;
- editorial placement.

An implementation must not declare a requirement non-applicable merely because
compliance is inconvenient.

Applicability derives from the normative specification and its target published
protocol generation.

# 15. Normative Interpretation

Normative statements must be interpreted according to:

1. their explicit requirement category;
2. their defined subject;
3. their applicability scope;
4. their stated conditions;
5. their stated exceptions;
6. their relationship to other normative requirements;
7. the semantics of the target published protocol generation.

Normative interpretation must not depend on rhetorical intensity.

A mandatory requirement does not become optional because it is phrased politely
or indirectly.

An informative statement does not become mandatory because it sounds forceful.

An implementation must not resolve normative ambiguity by inventing new protocol
behavior.

Where normative wording admits multiple materially different interpretations,
the specification is defective and must be clarified without altering the
published protocol semantics.

# 16. Recommendations and Exceptions

A permitted departure from SHOULD or SHOULD NOT must remain within the semantic
space allowed by the published protocol generation.

A recommendation must not create an implied exception to a MUST or MUST NOT
requirement.

An exception must be stated normatively.

An exception must identify:

- the requirement to which it applies;
- the conditions under which it applies;
- the behavior permitted by the exception;
- any remaining obligations.

Exceptions must not be created through:

- examples;
- notes;
- rationale;
- diagrams;
- implementation precedent;
- editorial commentary.

No informative explanation may silently widen an exception.

# 17. Notes, Examples, Diagrams, and Commentary

Notes, examples, diagrams, captions, and editorial commentary are informative
unless the same meaning is independently stated in normative material.

An example may demonstrate one conforming realization.

It must not imply that the illustrated realization is the only conforming
realization unless normative material establishes that exclusivity.

A note may explain a requirement.

It must not create, modify, weaken, strengthen, or remove the requirement.

A diagram may represent a normative relationship.

It must not be the sole source of that relationship.

Any relationship required for implementation or conformance must also be stated
normatively in text.

Editorial commentary may explain document organization or drafting intent.

It must not establish protocol behavior.

# 18. Requirement Clarity and Assessability

Every normative requirement must be sufficiently clear that a conformance
assessment can determine whether an implementation satisfies it.

Assessability may be established through:

- runtime testing;
- static inspection;
- interface inspection;
- configuration review;
- artifact validation;
- formal analysis;
- operational evidence;
- documented implementation choices.

Automated testing is not required for every normative statement.

Objective assessability is required.

Normative requirements should avoid:

- undefined subjective terms;
- ambiguous subjects;
- ambiguous pronouns;
- hidden sequencing;
- unstated temporal conditions;
- unexplained defaults;
- incomplete exception conditions;
- undefined failure behavior;
- reliance on implied implementation structure.

Where a protocol requirement concerns failure, the normative statement should
identify the required failure semantics where those semantics are established by
the published protocol.

Where a protocol requirement concerns ordering, the normative statement should
state the required ordering explicitly.

# 19. Cross-Reference Rules

Normative requirements may refer to other normative requirements without
duplicating their content.

A normative cross-reference preserves the referenced obligation:

> normativeReference(R₁, R₂) ∧ obligation(R₂, I)
> →
> obligation(R₂, I)

An informative reference may identify or explain a normative requirement but
creates no additional obligation:

> informativeReference(E, R)
> →
> ¬additionalObligation(E, I)

Cross-references must not conceal:

- requirement strength;
- applicability;
- exceptions;
- required ordering;
- failure behavior;
- prohibited behavior.

A referenced requirement retains its own category, scope, and authority.

A cross-reference must not silently strengthen or weaken the referenced
requirement.

# 20. Preservation of Protocol Semantics

The normative specification language must preserve the semantics of the target
published protocol generation.

Let N be the normative specification derived from published protocol generation P.

Then:

> semantics(N) = semantics(P)

The normative specification may reorganize, restate, partition, cross-reference,
or editorially clarify established protocol meaning.

It must not:

- add protocol behavior;
- remove protocol behavior;
- weaken protocol behavior;
- strengthen protocol behavior;
- create new architectural subjects;
- redefine existing architectural subjects;
- introduce implementation-specific APIs or algorithms;
- convert informative material into an independent source of obligation.

The preservation function is:

> P → expressed(P)

The permitted success path is:

> P → preservedExpression(P)

The required failure path is:

> P → fail

The forbidden path is:

> P → P′

where P′ contains protocol meaning not established by P.

# 21. Relationship to Implementations

A normative requirement constrains an implementation only where:

- the requirement derives from the target published protocol generation; and
- the requirement applies to that implementation.

The relationship is:

> Published Protocol Generation
> →
> Normative Specification Requirement
> →
> Implementation Obligation
> →
> Conforming Implementation

An implementation does not conform merely because it follows informative guidance.

An implementation conforms by satisfying all applicable normative requirements
derived from the target published protocol generation.

Informative guidance may assist implementation.

It cannot substitute for normative compliance.

# 22. Relationship to Conformance and Certification

This document does not define conformance assessments, conformance claims,
certification procedures, or certification status.

It provides the requirement language upon which those processes may operate.

A conformance assessment may evaluate whether:

> satisfies(I, R)

for each applicable normative requirement R derived from the target published
protocol generation.

The assessment method may vary according to the nature of the requirement.

The normative requirement itself must remain sufficiently precise for that
assessment.

This document does not establish that any implementation conforms.

It defines only how assessable obligations are expressed.

# 23. Protocol Authority

Normative specification language communicates the semantics of the published
protocol generation.

It does not create protocol authority.

It does not replace the published protocol generation.

It does not become an independent source of protocol semantics.

Let P be the published protocol generation and N its normative specification.

Then:

> derives(N, P)

> semantics(N) = semantics(P)

But:

> authority(N) ≠ authority(P)

The authority of N is derivative and representational.

The authority of P is protocol-defining.

Where the normative specification conflicts with the published protocol
generation:

> P governs

Protocol authority always remains with the published protocol generation.

# 24. Explicit Exclusions

This document does not define:

- Privacy Engine protocol operations;
- protocol state;
- protocol transitions;
- protocol actors;
- implementation components;
- interface contracts;
- implementation APIs;
- algorithms;
- cryptographic constructions;
- data formats;
- implementation profiles;
- reference implementations;
- conformance tests;
- certification procedures;
- protocol publication;
- protocol succession;
- protocol lineage;
- protocol-generation content;
- new architectural ontology.

It does not decide which future protocol statements are mandatory, prohibited,
recommended, discouraged, optional, or implementation-defined.

It defines how those classifications must be expressed after they have been
derived from the published protocol generation.

# 25. Conclusion

A Privacy Engine normative specification language is the bounded editorial
language through which requirements derived from one published Privacy Engine
protocol generation are expressed as explicit implementation obligations.

Privacy Engine implementation obligations must be expressed through a compact,
explicit, and consistently interpreted normative vocabulary.

Normative material establishes applicable implementation obligations.

Informative material may explain those obligations but must never independently
create, modify, complete, weaken, strengthen, or conceal them.

Requirement strength must be explicit.

Applicability must be explicit.

Exceptions must be normative.

Requirements must be sufficiently clear for conformance assessment.

The normative specification preserves and communicates published protocol
semantics.

It does not create new protocol meaning.

Protocol authority always remains with the published protocol generation.
