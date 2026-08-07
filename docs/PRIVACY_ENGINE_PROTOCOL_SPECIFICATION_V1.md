# Privacy Engine Protocol Specification V1

STATE.md remains canonical.

## 1. Specification Status

This document is the cumulative developer-facing Privacy Engine Protocol
Specification.

Current composition status:

- SF-01 — Authority, Scope, and Normative Interpretation: composed;
- SF-02 — Protocol Generation, Publication, Versioning, and Lineage: composed;
- SF-03 — Protocol Terminology, Subjects, and Identifiers: composed;
- SF-04 — Privacy, Actor Separation, and Compositional Unlinkability: composed;
- SF-05–SF-16: not yet composed.

The requirements in the composed sections are normative within their declared
scope.

This document does not yet constitute the complete Privacy Engine Protocol
Specification because the remaining authoritative section families have not
been composed.

No absent section, deferred requirement family, supporting reference, or
informative statement may be treated as implicitly completed.

The current composition boundary is defined in Section 22.

## 2. Purpose

This specification provides the portable, implementation-facing normative
composition of one published Privacy Engine protocol generation.

It translates established protocol semantics into stable, explicit,
applicable, and traceable developer obligations.

It does not create protocol semantics.

It does not independently possess protocol authority.

When complete, an implementer must be able to determine the applicable
protocol obligations from this specification without reconstructing protocol
meaning from the internal formal corpus, repository history, composition
reviews, or hidden development context.

## 3. Scope

The current cumulative document composes:

- SF-01 — Authority, Scope, and Normative Interpretation;
- SF-02 — Protocol Generation, Publication, Versioning, and Lineage;
- SF-03 — Protocol Terminology, Subjects, and Identifiers;
- SF-04 — Privacy, Actor Separation, and Compositional Unlinkability.

These sections authoritatively contain:

- RF-01 — Specification identity, derivation, completeness, and authority;
- RF-02 — Protocol definition, scope, and invariant ownership;
- RF-03 — Protocol generation, publication, and Published Protocol;
- RF-04 — Succession, lineage, versioning, deprecation, and migration;
- RF-05 — Normative language, interpretation, applicability, and strength;
- RF-06 — Protocol terminology;
- RF-07 — Protocol subject identity and identity separation;
- RF-08 — Protocol identifiers and occurrence identifiers;
- RF-09 — Private actors and public protocol subjects;
- RF-10 — Privacy, anonymity, and unlinkability;
- RF-11 — Compositional privacy, observability, and forbidden correlation;
- RF-15 — Anonymous membership, continuity, and enrollment separation;
- RF-19 — Nullifier-based uniqueness and action-bounded unlinkability.

The current document does not define the later interface, proof, validity,
Protocol Action lifecycle, Evaluation, Determination, state-transition,
application, implementation-profile, conformance, or certification requirements
assigned to SF-05–SF-16.

RF-49 and RF-50 remain reserved to SF-16.

## 4. Relationship to STATE.md

During repository development and specification composition, `STATE.md` is the
canonical record of current architecture, invariants, deployed state, and
development governance.

If this cumulative working document conflicts with `STATE.md` before final
publication, `STATE.md` wins.

This development-governance rule does not make `STATE.md` protocol authority.

The completed Protocol Specification must be portable. Ordinary implementation
must not depend on access to `STATE.md`, the complete formal corpus,
consolidation reviews, the composition map, or repository history.

The relationship is:

> canonical development state
> -> published protocol generation
> -> portable Protocol Specification

Canonical development-state precedence and final-specification portability are
distinct properties.

## 5. Protocol Authority and Specification Derivation

Protocol authority always remains with the published Privacy Engine protocol generation.

The Protocol Specification derives from one identified published Privacy
Engine protocol generation.

The Protocol Specification communicates protocol-derived obligations in
implementation-facing form. It does not independently define, amend, replace,
or supersede the protocol generation from which it derives.

The authority direction is:

> Published Protocol Generation
> -> Protocol Specification
> -> Implementation Profile
> -> Implementation
> -> Conformance
> -> Certification

No downstream layer may modify an upstream layer.

The foundational derivation invariants are:

> derivesFrom(Spec, P)

> semantics(Spec) = semantics(P)

> obligations(Spec) = obligations(P)

> communicates(Spec, P)
> =/=>
> definesProtocol(Spec, P)

### 5.1 RF-01 — Specification Identity, Derivation, Completeness, and Authority

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-SPEC-001 | RF-01 | MUST | Every Privacy Engine Protocol Specification | A Protocol Specification MUST possess one stable specification identity and MUST identify its specification version. | S03, S08 |
| PE-SPEC-002 | RF-01 | MUST | Every completed Privacy Engine Protocol Specification | A completed Protocol Specification MUST identify exactly one published Privacy Engine protocol generation from which it derives. | S08 |
| PE-SPEC-003 | RF-01 | MUST | Every Privacy Engine Protocol Specification | A Protocol Specification MUST preserve the semantics and obligations of the published protocol generation from which it derives. | S08, S17 |
| PE-SPEC-004 | RF-01 | MUST | Every completed Privacy Engine Protocol Specification | A completed Protocol Specification MUST contain the complete implementation-facing normative composition required to implement its identified published protocol generation without dependence on hidden repository context. | S03, S08 |
| PE-SPEC-005 | RF-01 | MUST NOT | Every incomplete cumulative Protocol Specification | An incomplete cumulative Protocol Specification MUST NOT claim completeness, final publication status, or suitability as the complete conformance basis. | S03, S07, S08 |
| PE-SPEC-006 | RF-01 | MUST NOT | Every Privacy Engine Protocol Specification and every interpretation of it | A Protocol Specification MUST NOT be treated as independent protocol authority or as authority to modify its source protocol generation. | S08, S17, S18 |
| PE-SPEC-007 | RF-01 | MUST | Every cumulative Protocol Specification | A cumulative Protocol Specification MUST state its composition status, composed section families, deferred section families, and current completeness boundary. | S03, S07, S08 |
| PE-SPEC-008 | RF-01 | MUST | Every semantic requirement composed into the Protocol Specification | Each semantic requirement MUST possess exactly one authoritative normative home within the Protocol Specification, excluding every supporting reference from authoritative-home status. | S02, S06, S07, S08 |

## 6. Normative and Informative Material

A normative statement creates, prohibits, recommends, discourages, or permits
behavior within an explicitly declared applicability scope.

An informative statement may explain terminology, rationale, consequences,
examples, diagrams, source relationships, or interpretation context.

Informative material does not independently create protocol obligations.

Headings, introductions, examples, notes, rationale, diagrams, formal
invariants, and traceability records are informative unless they contain an
explicitly identified normative requirement.

Normative requirements in this specification appear in requirement tables and
possess:

- one stable requirement identifier;
- one requirement family;
- one explicit requirement strength;
- one bounded applicability rule;
- one authoritative section;
- one normative requirement statement;
- one or more supporting source references.

## 7. Requirement Language and Applicability

The uppercase terms `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are
the normative requirement-strength vocabulary of this specification.

Their meanings are:

- `MUST` identifies a mandatory requirement;
- `MUST NOT` identifies a prohibited behavior;
- `SHOULD` identifies a recommended behavior from which deviation requires a
  valid bounded reason;
- `SHOULD NOT` identifies a discouraged behavior that requires a valid bounded
  reason before it is performed;
- `MAY` identifies behavior that is permitted but not required;
- implementation-defined behavior is permitted only where a normative
  requirement explicitly assigns a bounded choice to an implementation.

A requirement applies only to the subjects and conditions declared by its
applicability rule.

### 7.1 RF-05 — Normative Language, Interpretation, Applicability, and Strength

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-NORM-001 | RF-05 | MUST | Every statement in the Protocol Specification | Every specification statement MUST be classifiable as normative or informative. | S04 |
| PE-NORM-002 | RF-05 | MUST | Every requirement using `MUST` | A requirement using `MUST` MUST be interpreted as mandatory throughout its declared applicability scope. | S04, S05 |
| PE-NORM-003 | RF-05 | MUST | Every requirement using `MUST NOT` | A requirement using `MUST NOT` MUST be interpreted as prohibiting the stated behavior throughout its declared applicability scope. | S04, S05 |
| PE-NORM-004 | RF-05 | MUST | Every requirement using `SHOULD` | A requirement using `SHOULD` MUST be interpreted as recommended; deviation MUST be bounded, understood, and justified without violating any mandatory requirement. | S04, S05 |
| PE-NORM-005 | RF-05 | MUST | Every requirement using `SHOULD NOT` | A requirement using `SHOULD NOT` MUST be interpreted as discouraged; contrary behavior MUST be bounded, understood, and justified without violating any mandatory requirement. | S04, S05 |
| PE-NORM-006 | RF-05 | MUST | Every requirement using `MAY` | A requirement using `MAY` MUST be interpreted as permitting, but not requiring, the stated behavior. | S04, S05 |
| PE-NORM-007 | RF-05 | MUST | Every declaration of implementation-defined behavior | Implementation-defined behavior MUST be explicitly permitted, bounded by the applicable protocol requirements, and documented by the implementation. | S04, S05 |
| PE-NORM-008 | RF-05 | MUST | Every normative requirement | Every normative requirement MUST declare a bounded applicability rule identifying the subjects and conditions to which it applies. | S04, S05, S06 |
| PE-NORM-009 | RF-05 | MUST | Every interpretation of a normative requirement | A normative requirement MUST be interpreted using its identifier, requirement text, defined terminology, applicability rule, authoritative section, and applicable cross-references as one coherent requirement. | S04, S05, S07 |
| PE-NORM-010 | RF-05 | MUST NOT | Every supporting cross-reference and informative statement | A supporting cross-reference or informative statement MUST NOT independently create, modify, complete, weaken, strengthen, conceal, or relocate a normative obligation. | S02, S04, S07 |
| PE-NORM-011 | RF-05 | MUST | Every normative requirement | Every normative requirement MUST possess exactly one stable identifier in the form `PE-<SEMANTIC-FAMILY>-<NNN>`, and that identifier MUST denote exactly one semantic requirement. | S02, S05, S06 |
| PE-NORM-012 | RF-05 | MUST NOT | Every requirement identifier lifecycle | A requirement identifier MUST NOT be changed because of editorial reordering and MUST NOT be silently reused for a different semantic requirement. | S02, S05, S06 |
| PE-NORM-013 | RF-05 | MUST | Every normative requirement | Every normative requirement MUST record its requirement family, strength, applicability, authoritative section, and supporting source traceability. | S02, S05, S06, S07 |
| PE-NORM-014 | RF-05 | MUST | Every apparently obligatory specification statement | Every statement intended to impose an obligation MUST be expressed as a stable identified normative requirement rather than apparently mandatory prose. | S04, S05 |

## 8. Requirement Identifiers and Traceability

The stable identifier syntax is:

> PE-<SEMANTIC-FAMILY>-<NNN>

The semantic-family codes introduced by this composition slice are:

| Prefix | Requirement family | Authoritative section family |
|---|---|---|
| PE-SPEC-* | RF-01 | SF-01 |
| PE-PROT-* | RF-02 | SF-01 |
| PE-GEN-* | RF-03 | SF-02 |
| PE-EVOL-* | RF-04 | SF-02 |
| PE-NORM-* | RF-05 | SF-01 |
| PE-TERM-* | RF-06 | SF-03 |
| PE-SUBJ-* | RF-07 | SF-03 |
| PE-ID-* | RF-08 | SF-03 |
| PE-ACTSEP-* | RF-09 | SF-04 |
| PE-PRIV-* | RF-10 | SF-04 |
| PE-COMP-* | RF-11 | SF-04 |
| PE-MEM-* | RF-15 | SF-04 |
| PE-UNIQ-* | RF-19 | SF-04 |

The numeric component is three digits and is allocated independently within
each semantic family.

Requirement identifiers are semantic identifiers, not editorial coordinates.

A requirement identifier does not identify:

- an actor;
- a participant;
- an implementation;
- a deployment;
- a protocol operation;
- a runtime action;
- a state-transition occurrence;
- a proof;
- or an application event.

Supporting source references provide composition traceability. They do not
become protocol authority and do not replace the normative requirement.

## 9. Protocol Definition

The Privacy Engine Protocol is the bounded, governed system of published
semantics, rules, invariants, relationships, validity conditions, and permitted
behavior that defines the Privacy Engine independently of any particular
implementation or application.

The Protocol is not interchangeable with any one Protocol Generation,
Protocol Publication, Published Protocol, implementation, application,
conformance determination, or certification.

### 9.1 RF-02 — Protocol Definition, Scope, and Invariant Ownership

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-PROT-001 | RF-02 | MUST | Every Privacy Engine Protocol definition | The Privacy Engine Protocol MUST be defined independently of any particular implementation, application, deployment, transport, storage system, or execution environment. | S09, S17 |
| PE-PROT-002 | RF-02 | MUST | Every published Privacy Engine protocol generation | A published protocol generation MUST declare the complete bounded protocol scope represented by that generation. | S09, S10 |
| PE-PROT-003 | RF-02 | MUST | Every protocol invariant | Each protocol invariant MUST remain owned by the published protocol generation in which it is defined. | S09, S10, S17 |
| PE-PROT-004 | RF-02 | MUST NOT | Every downstream specification, profile, implementation, application, assessment, and certification artifact | A downstream artifact MUST NOT redefine, weaken, strengthen, omit, or silently reinterpret an applicable protocol invariant. | S08, S09, S17, S18 |
| PE-PROT-005 | RF-02 | MUST | Every claim of complete protocol realization | A claim of complete protocol realization MUST account for every applicable invariant and normative requirement of the identified published protocol generation. | S08, S09 |
| PE-PROT-006 | RF-02 | MUST NOT | Every application and implementation using the Privacy Engine Protocol | Application-defined meaning and implementation-defined mechanism MUST NOT be represented as protocol-defined meaning unless the identified published protocol generation explicitly defines it. | S09, S17, S18 |

## 10. Protocol Scope and Invariant Ownership

Protocol scope describes the complete bounded semantic domain governed by one
protocol generation.

Protocol invariant ownership identifies the published protocol generation as
the source of the invariants expressed through this specification.

The specification may organize protocol invariants into implementation-facing
sections. Editorial organization does not transfer ownership or authority.

> organizes(Spec, R)
> =/=>
> ownsProtocolInvariant(Spec, R)

> implementationChoice(I)
> =/=>
> protocolMeaning(I)

An implementation may select behavior only where the applicable requirement
explicitly permits a choice.

An application may assign application meaning only within its later-defined
application boundary. It may not convert that meaning into protocol meaning.

## 11. Protocol Generation

A Protocol Generation is one uniquely identified, bounded, and complete
generation of the Privacy Engine Protocol.

A Protocol Generation identifies a complete protocol semantic state. It is not
a partial update, editorial fragment, implementation release, deployment, or
runtime occurrence.

Generation identity remains stable throughout publication, coexistence,
deprecation, migration, and retirement.

### 11.1 RF-03 — Generation Identity and Completeness

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-GEN-001 | RF-03 | MUST | Every Privacy Engine Protocol Generation | A Protocol Generation MUST possess one unique and stable generation identity. | S10 |
| PE-GEN-002 | RF-03 | MUST | Every Privacy Engine Protocol Generation | A Protocol Generation MUST contain one bounded and complete protocol semantic state. | S10 |
| PE-GEN-003 | RF-03 | MUST NOT | Every incomplete protocol fragment or partial change | An incomplete protocol fragment or partial change MUST NOT be represented as a complete Protocol Generation. | S10, S11 |
| PE-GEN-004 | RF-03 | MUST | Every Protocol Generation lifecycle | A Protocol Generation MUST retain the same identity through publication, coexistence, deprecation, migration, and retirement. | S10, S13, S16 |

## 12. Protocol Publication

A Protocol Publication is the bounded publication occurrence through which one
complete Protocol Generation is made available as an identified Published
Protocol.

Protocol Publication is distinct from:

- the Protocol;
- the Protocol Generation being published;
- the resulting Published Protocol;
- Protocol Succession;
- Protocol Lineage.

Publication does not itself imply succession, compatibility, deprecation,
migration, or retirement.

### 12.1 RF-03 — Publication

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-GEN-005 | RF-03 | MUST | Every Protocol Publication | A Protocol Publication MUST identify exactly one complete Protocol Generation as its publication subject. | S11 |
| PE-GEN-006 | RF-03 | MUST | Every Protocol Publication | A Protocol Publication MUST identify the complete published material, generation identity, publication identity, and publication version required to distinguish its result. | S11, S12, S15 |
| PE-GEN-007 | RF-03 | MUST NOT | Every incomplete or ambiguous publication occurrence | An incomplete or ambiguously identified publication MUST NOT establish a Published Protocol. | S11, S12 |
| PE-GEN-008 | RF-03 | MUST NOT | Every Protocol Publication | A Protocol Publication MUST NOT be interpreted as Protocol Succession, Protocol Lineage membership, compatibility, deprecation, migration, or retirement unless those relationships are separately and explicitly established. | S11, S13, S14, S16 |

## 13. Published Protocol

A Published Protocol is the uniquely identified, complete, and immutable
published protocol object resulting from publication of exactly one Protocol
Generation.

The Published Protocol is distinct from both the publication occurrence and
the generation that the publication publishes.

The relationship is:

> Protocol Generation
> -> Protocol Publication
> -> Published Protocol

These subjects participate in one publication chain without merging their
identities.

### 13.1 RF-03 — Published Protocol Identity

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-GEN-009 | RF-03 | MUST | Every Published Protocol | A Published Protocol MUST identify exactly one Protocol Generation and exactly one complete publication of that generation. | S10, S11, S12 |
| PE-GEN-010 | RF-03 | MUST | Every Published Protocol | A Published Protocol MUST possess a stable identity distinct from the identity of its Protocol Generation and its Protocol Publication. | S10, S11, S12 |
| PE-GEN-011 | RF-03 | MUST NOT | Every Published Protocol | A Published Protocol MUST NOT be silently replaced, partially rewritten, or reinterpreted as a different generation. | S12, S13, S15 |
| PE-GEN-012 | RF-03 | MUST | Every published Privacy Engine protocol generation | Each published Privacy Engine protocol generation MUST remain the protocol authority for its own identified semantics and obligations throughout its recorded lifecycle. | S10, S12, S13, S16, S17 |

## 14. Publication Completeness and Immutability

Publication completeness requires the published material to identify and
contain the complete bounded protocol generation being published.

Immutability preserves historical protocol truth after publication.

A correction or later publication may explain, supersede, deprecate, or succeed
an earlier Published Protocol only through an explicit separately identified
relationship. It may not silently mutate the earlier Published Protocol.

The preservation invariants are:

> published(G)
> ->
> immutable(G)

> laterPublication(G2)
> =/=>
> mutates(G1)

> retired(G)
> =/=>
> deletesHistoricalTruth(G)

### 14.1 RF-03 — Publication Completeness and Immutability

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-GEN-013 | RF-03 | MUST | Every Protocol Publication claiming completeness | A Protocol Publication claiming completeness MUST contain or unambiguously bind every component required to reconstruct the complete published generation. | S11, S12 |
| PE-GEN-014 | RF-03 | MUST | Every Published Protocol | A Published Protocol MUST remain immutable after publication. | S12 |
| PE-GEN-015 | RF-03 | MUST | Every correction, clarification, or replacement affecting published material | A correction, clarification, or replacement affecting published material MUST be separately identified and MUST preserve the identity and historical content of the earlier Published Protocol. | S12, S13, S15 |
| PE-GEN-016 | RF-03 | MUST NOT | Every incomplete publication | An incomplete publication MUST NOT be used as the authoritative representation of a complete Protocol Generation. | S11, S12 |

## 15. Protocol Succession

Protocol Succession is an explicit directed relationship between one identified
predecessor Protocol Generation and one distinct identified successor Protocol
Generation.

Succession records evolution. It does not mutate the predecessor into the
successor and does not erase the predecessor.

Succession is distinct from publication and lineage.

> succeeds(G2, G1)
> ->
> G2 != G1

> succeeds(G2, G1)
> ->
> preservesIdentity(G1)

### 15.1 RF-04 — Protocol Succession

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-EVOL-001 | RF-04 | MUST | Every Protocol Succession relationship | A Protocol Succession relationship MUST identify exactly one predecessor Protocol Generation and one distinct successor Protocol Generation. | S13 |
| PE-EVOL-002 | RF-04 | MUST | Every successor Protocol Generation | A successor Protocol Generation MUST possess an identity distinct from every predecessor generation. | S10, S13 |
| PE-EVOL-003 | RF-04 | MUST | Every Protocol Succession relationship | Protocol Succession MUST preserve the identity, published content, lifecycle record, and historical truth of the predecessor generation. | S12, S13 |
| PE-EVOL-004 | RF-04 | MUST NOT | Every Protocol Succession relationship | Protocol Succession MUST NOT mutate, rename, merge, delete, or retroactively reinterpret its predecessor generation. | S13 |
| PE-EVOL-005 | RF-04 | MUST NOT | Every Protocol Publication | Publication of a generation MUST NOT by itself establish succession from any other generation. | S11, S13 |

## 16. Protocol Lineage

A Protocol Lineage is one uniquely identified bounded organization of Protocol
Generations connected through explicit Protocol Succession relationships.

Lineage records generation relationships. It does not become protocol
authority and does not merge the identities of its members.

Multiple independent lineages may exist.

Lineage membership does not by itself establish compatibility, migration,
deprecation, replacement, or universal ordering.

### 16.1 RF-04 — Protocol Lineage

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-EVOL-006 | RF-04 | MUST | Every Protocol Lineage | A Protocol Lineage MUST possess one stable lineage identity distinct from the identities of its member generations. | S14 |
| PE-EVOL-007 | RF-04 | MUST | Every Protocol Lineage membership claim | A Protocol Generation MUST be included in a lineage only through an explicit lineage-membership rule supported by the applicable succession structure. | S13, S14 |
| PE-EVOL-008 | RF-04 | MUST | Every Protocol Lineage | A Protocol Lineage MUST preserve the separate identities and lifecycle records of all member generations. | S14 |
| PE-EVOL-009 | RF-04 | MUST NOT | Every Protocol Lineage | A Protocol Lineage MUST NOT create, inherit, transfer, or replace the protocol authority of any member generation. | S14, S17 |
| PE-EVOL-010 | RF-04 | MUST | Every Protocol Lineage model | A Protocol Lineage model MUST permit independent Protocol Generations to remain in separate Protocol Lineages and MUST require an explicit succession relationship before placing generations in one lineage. | S13, S14 |
| PE-EVOL-011 | RF-04 | MUST NOT | Every Protocol Lineage membership claim | Lineage membership MUST NOT by itself be interpreted as compatibility, migration eligibility, deprecation, replacement, or semantic equivalence. | S14, S15, S16 |

## 17. Versioning and Semantic Change

Versioning identifies published generations and their relationships. A version
identifier does not independently determine semantic compatibility.

Semantic change modifies protocol-defined meaning, obligations, validity,
invariants, or permitted behavior.

A semantic change must not be applied by mutating an existing Published
Protocol. It requires a distinct Protocol Generation.

Editorial reorganization, informative clarification, and implementation choice
within an already permitted range are not semantic changes when they preserve
all established protocol semantics and obligations.

> semanticChange(G1, G2)
> ->
> G1 != G2

> permittedImplementationVariation(I)
> =/=>
> semanticChange(P)

### 17.1 RF-04 — Versioning and Semantic Change

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-EVOL-012 | RF-04 | MUST | Every published Protocol Generation | Every published Protocol Generation MUST possess a stable version designation sufficient to distinguish it from every other published generation. | S10, S15 |
| PE-EVOL-013 | RF-04 | MUST NOT | Every protocol version designation | A version designation MUST NOT by itself be interpreted as proof of compatibility, incompatibility, succession, migration eligibility, or semantic equivalence. | S15 |
| PE-EVOL-014 | RF-04 | MUST | Every protocol semantic change | A change to protocol-defined semantics, obligations, validity, invariants, or permitted behavior MUST be represented by a distinct Protocol Generation. | S10, S13, S15 |
| PE-EVOL-015 | RF-04 | MUST NOT | Every published Protocol Generation | Semantic change MUST NOT be introduced through silent mutation, editorial replacement, implementation variation, or reinterpretation of an existing Published Protocol. | S12, S15 |
| PE-EVOL-016 | RF-04 | MUST | Every classification of a protocol change | A protocol change MUST be classified according to its semantic effect rather than only its label, release number, implementation impact, or publication format. | S15 |

## 18. Compatible Evolution

Compatible evolution preserves the applicable semantics and obligations of the
generation against which compatibility is claimed.

Implementation variation already permitted by a published generation does not
create a new Protocol Generation.

A separately published successor may be classified as compatible only within
an explicit bounded compatibility scope. Compatibility does not merge
generation identities or permit mutation of the predecessor.

### 18.1 RF-04 — Compatible and Breaking Evolution

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-EVOL-017 | RF-04 | MUST | Every claim of compatible evolution | A claim of compatible evolution MUST identify the generations, requirements, subjects, and compatibility scope to which the claim applies. | S13, S15 |
| PE-EVOL-018 | RF-04 | MAY | Every implementation variation within one published generation | An implementation variation MAY occur without a new Protocol Generation only when every applicable protocol semantic and normative requirement remains preserved. | S09, S15 |
| PE-EVOL-019 | RF-04 | MUST | Every compatible successor generation | A compatible successor generation MUST remain distinctly identified and MUST preserve every predecessor obligation included within the declared compatibility scope. | S13, S15 |
| PE-EVOL-020 | RF-04 | MUST | Every breaking protocol evolution | Breaking evolution MUST be represented by a distinct successor generation and MUST explicitly identify the affected compatibility boundary. | S13, S15 |
| PE-EVOL-021 | RF-04 | MUST NOT | Every compatibility claim | Compatibility MUST NOT be used to merge generation identities, mutate historical published truth, or conceal semantic change. | S12, S13, S15 |

## 19. Deprecation and Migration

Deprecation is an explicit lifecycle designation indicating that use of an
identified Published Protocol is discouraged, restricted, or expected to end
under stated conditions.

Deprecation is not revocation. It does not erase the deprecated generation,
invalidate historical truth, or transfer its protocol authority.

Migration is an explicit bounded relationship from one identified source
generation or implementation target to one identified destination generation
or implementation target.

Migration does not mutate identity. It establishes obligations for movement
between distinct targets.

### 19.1 RF-04 — Deprecation and Migration

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-EVOL-022 | RF-04 | MUST | Every Protocol Generation deprecation | Deprecation MUST identify the deprecated generation, the effective lifecycle condition, and any published continuation or migration guidance. | S16 |
| PE-EVOL-023 | RF-04 | MUST NOT | Every Protocol Generation deprecation | Deprecation MUST NOT revoke, erase, mutate, or retroactively invalidate the identity, published content, or historical truth of the deprecated generation. | S12, S16 |
| PE-EVOL-024 | RF-04 | MUST | Every published migration | A published migration MUST identify its source target, destination target, applicability conditions, required steps, preserved properties, and explicit failure conditions. | S13, S16 |
| PE-EVOL-025 | RF-04 | MUST | Every mandatory migration obligation | A mandatory migration obligation MUST be expressed as an identified normative requirement with explicit applicability and requirement strength. | S04, S05, S16 |
| PE-EVOL-026 | RF-04 | MUST NOT | Every migration | Migration MUST NOT mutate the identity of a Protocol Generation, Published Protocol, implementation target, conformance determination, or certification. | S13, S16 |
| PE-EVOL-027 | RF-04 | MUST NOT | Every deprecation or migration statement | A deprecation or migration statement MUST NOT silently redefine compatibility, succession, lineage membership, or protocol semantics. | S13, S14, S15, S16 |

## 20. Coexistence and Retirement

Multiple published Protocol Generations may coexist.

Coexistence preserves the separate identity, authority, applicability,
compatibility status, and lifecycle record of each generation.

Retirement ends a declared active role, support condition, or permitted future
use of an identified generation within a stated scope.

Retirement does not delete the retired generation or its historical protocol
truth.

### 20.1 RF-04 — Coexistence and Retirement

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-EVOL-028 | RF-04 | MUST | Every environment supporting multiple published Protocol Generations | Coexisting Protocol Generations MUST remain separately identifiable and MUST retain separate applicability, compatibility, lifecycle, and authority records. | S10, S15, S16 |
| PE-EVOL-029 | RF-04 | MUST NOT | Every coexistence arrangement | Coexistence MUST NOT be interpreted as semantic equivalence, automatic compatibility, shared identity, succession, or migration eligibility. | S13, S14, S15, S16 |
| PE-EVOL-030 | RF-04 | MUST | Every Protocol Generation retirement | Retirement MUST identify the retired generation, retirement scope, effective condition, and consequences for future implementation, assessment, and support. | S16 |
| PE-EVOL-031 | RF-04 | MUST NOT | Every Protocol Generation retirement | Retirement MUST NOT delete, mutate, conceal, or retroactively invalidate the retired generation or its historical protocol truth. | S12, S16 |
| PE-EVOL-032 | RF-04 | MUST | Every lifecycle interpretation | Deprecation, migration, coexistence, and retirement MUST be interpreted as distinct bounded lifecycle concepts. | S16 |

## 21. Downstream Implementation and Assessment References

Implementation profiles, implementations, conformance determinations, and
certifications are downstream from the published protocol generation and its
Protocol Specification.

Their complete models are assigned to later section families and are not
composed here.

This section establishes only the generation-reference boundary required by
SF-01 and SF-02.

### 21.1 Generation Target Requirements

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-SPEC-009 | RF-01 | MUST | Every implementation profile | An implementation profile MUST identify the Protocol Specification and published Protocol Generation from which its applicable obligations derive. | S08, S10 |
| PE-GEN-017 | RF-03 | MUST | Every Privacy Engine implementation | An implementation MUST identify exactly which published Protocol Generation it targets. | S08, S10, S12 |
| PE-GEN-018 | RF-03 | MUST | Every conformance determination | A conformance determination MUST identify the implementation, implementation profile, Protocol Specification, and published Protocol Generation against which conformance is assessed. | S08, S10, S18 |
| PE-GEN-019 | RF-03 | MUST | Every certification | A certification MUST identify the conformance basis and published Protocol Generation to which the certification applies. | S08, S10, S18 |
| PE-GEN-020 | RF-03 | MUST NOT | Every downstream implementation or assessment artifact | A downstream implementation, profile, conformance determination, or certification MUST NOT modify the identity, semantics, obligations, lifecycle, or authority of its referenced published Protocol Generation. | S08, S10, S17, S18 |

## 22. SF-03 — Protocol Terminology, Subjects, and Identifiers

SF-03 establishes the canonical terminology, subject identities, identifier
boundaries, and relationship distinctions used by every later section.

It identifies established subjects and preserves their distinctions.

It does not compose their deferred operational lifecycles.

### 22.1 Canonical Terms

The following terms have the stated meanings throughout this specification:

| Term | Canonical meaning |
|---|---|
| Protocol subject | An established semantic object, occurrence, process, result, mapping, relationship, or bounded supporting structure governed by the published protocol generation. |
| Private Actor (`X`) | The private performer of a Protocol Action whose identity is not disclosed by the public protocol occurrence. |
| Protocol Operation (`O`) | A published bounded protocol capability or behavior type; it is not one performed action occurrence. |
| Protocol Action (`A`) | One identified public occurrence of protocol-defined behavior presented for Evaluation. |
| Protocol Action Evaluation (`E`) | One identified bounded evaluation occurrence applying the complete applicable rule set to one Protocol Action in one bounded context. |
| Protocol Action Determination (`D`) | The identified bounded result produced by one completed Protocol Action Evaluation. |
| Protocol Transition (`T`) | A published semantic mapping between a bounded source-state class and a bounded successor-state class. |
| Protocol State Transition (`U`) | One identified protocol-governed state-change occurrence governed by an applicable Protocol Transition mapping. |
| Subject identifier (`id(S)`) | A value or coordinate that identifies one bounded protocol subject according to its declared role without becoming the subject itself. |
| Representation | A syntactic, serialized, stored, transmitted, or displayed expression of a subject; it is not the semantic subject it represents. |
| Public protocol subject | A protocol subject exposed to the extent required for public protocol use or verification without thereby exposing a Private Actor. |
| Action-local public value | A public value whose permitted meaning and use are bounded to one action or action context. |
| Application meaning | Meaning assigned by an application to a public protocol occurrence or consequence; it is not protocol identity or protocol validity. |

The established protocol-use occurrence inventory contains four separately
identified occurrences arranged within three model units:

| Model unit | Identified occurrence | Identity boundary |
|---|---|---|
| Protocol Action | `A` | Public action-occurrence identity |
| Evaluation and Determination | `E` | Evaluation-occurrence identity |
| Evaluation and Determination | `D` | Determination-result identity, relationally dependent upon completed `E` |
| Protocol State Transition | `U` | State-change-occurrence identity |

Protocol Operation and Protocol Transition are classification or mapping
constructs required by later operational sections. They are not silently
collapsed into their associated occurrences.

Private Actor is an established surrounding private subject. It does not
become a public protocol occurrence.

### 22.2 Canonical Relationship and Identity Invariants

The type-and-occurrence distinctions are:

> operationType(O)
> =/=>
> actionOccurrence(A)

> transitionMapping(T)
> =/=>
> transitionOccurrence(U)

The identified protocol-use occurrences remain distinct:

> A != E

> E != D

> D != U

Their identifiers remain non-substitutable:

> id(A) != id(E)

> id(E) != id(D)

> id(D) != id(U)

Relationships connect subjects without merging them:

> evaluates(E, A) =/=> E = A

> determinationOf(D, E) =/=> D = E

> authorizedBy(U, D) =/=> U = D

Subject, identifier, and representation remain distinct:

> identifiesSubject(id(S), S) =/=> id(S) = S

> represents(Rep, S) =/=> Rep = S

### 22.3 RF-06 — Protocol Terminology

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-TERM-001 | RF-06 | MUST | Every use of a canonical Protocol Specification term | A canonical term MUST be interpreted according to its definition and bounded role in this specification. | S02, S17, S18 |
| PE-TERM-002 | RF-06 | MUST | Every downstream section, profile, implementation, application adapter, assessment, and supporting artifact | Every downstream use of a canonical term MUST preserve the same subject, relationship, scope, and identity distinction established by this specification. | S02, S17, S18 |
| PE-TERM-003 | RF-06 | MUST | Every term that may denote either a protocol type or an occurrence | A term that may denote either a type or an occurrence MUST explicitly preserve the applicable type-or-occurrence distinction. | S02, S23, S24, S26, S27 |
| PE-TERM-004 | RF-06 | MUST | Every specification definition involving a semantic subject, identifier, or representation | The terminology used for a semantic subject, its identifier, and its representation MUST preserve those as distinct concepts. | S02, S17, S18 |
| PE-TERM-005 | RF-06 | MUST NOT | Every alias, abbreviation, implementation name, application label, and editorial synonym | An alias, abbreviation, implementation name, application label, or editorial synonym MUST NOT silently redefine, merge, widen, or narrow a canonical protocol term. | S02, S17, S18, S28 |
| PE-TERM-006 | RF-06 | MUST NOT | Every terminology decision and editorial reorganization | Terminology or editorial structure MUST NOT introduce a new first-class protocol subject, lifecycle, authority, or semantic boundary. | S02, S17, S18, S28 |
| PE-TERM-007 | RF-06 | MUST | Every permitted local alias for a canonical protocol term | A permitted local alias MUST map explicitly and unambiguously to exactly one canonical term while preserving its protocol meaning. | S02, S17 |

### 22.4 RF-07 — Protocol Subject Identity and Identity Separation

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-SUBJ-001 | RF-07 | MUST | Every established identified protocol subject | Every established identified protocol subject MUST retain its own bounded identity according to its defined architectural role. | S17, S18, S24, S25, S27 |
| PE-SUBJ-002 | RF-07 | MUST | Every Protocol Action, Protocol Action Evaluation, Protocol Action Determination, and Protocol State Transition | Protocol Action, Evaluation, Determination, and Protocol State Transition identities MUST remain mutually distinct. | S18, S24, S25, S27 |
| PE-SUBJ-003 | RF-07 | MUST | Every Protocol Action Evaluation and its Protocol Action Determination | Evaluation and Determination MUST retain distinct process and result identities while remaining two bounded aspects of one architectural model. | S18, S25 |
| PE-SUBJ-004 | RF-07 | MUST | Every Protocol Operation and associated Protocol Action | A Protocol Operation capability and each Protocol Action occurrence classified by it MUST remain distinct. | S02, S23, S24 |
| PE-SUBJ-005 | RF-07 | MUST | Every Protocol Transition and governed Protocol State Transition | A Protocol Transition mapping and each Protocol State Transition occurrence governed by it MUST remain distinct. | S02, S26, S27 |
| PE-SUBJ-006 | RF-07 | MUST | Every relationship between identified protocol subjects | Every subject relationship MUST preserve its declared direction, bounded meaning, and participating subject identities. | S17, S18 |
| PE-SUBJ-007 | RF-07 | MUST | Every protocol subject referenced through an implementation, application, runtime mechanism, or application interpretation | A protocol subject MUST remain distinct from the implementation, application, runtime mechanism, and application-defined meaning through which it is represented or used. | S17, S18, S24 |
| PE-SUBJ-008 | RF-07 | MUST | Every downstream representation or reference to an established protocol subject | Every downstream representation or reference MUST preserve the identity of the same established protocol subject rather than substitute a newly inferred subject. | S02, S17, S18 |
| PE-SUBJ-009 | RF-07 | MUST NOT | Every relationship, composition, representation, and implementation convenience involving distinct subjects | A relationship, composition, representation, or implementation convenience MUST NOT silently merge distinct protocol subjects or their identities. | S17, S18, S24, S25, S27 |
| PE-SUBJ-010 | RF-07 | MUST NOT | Every proposed extension to the established protocol-subject inventory | A proposed extension MUST NOT introduce a new first-class subject unless independent identity, meaning, semantic ownership, and irreducible lifecycle necessity are all established. | S17, S18, S28 |

### 22.5 RF-08 — Protocol Identifiers and Occurrence Identifiers

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-ID-001 | RF-08 | MUST | Every protocol identifier | Every protocol identifier MUST possess one declared bounded role identifying exactly the subject or occurrence specified by that role. | S18, S24, S25, S27 |
| PE-ID-002 | RF-08 | MUST | Every identified protocol subject and its identifier | A protocol subject and the identifier used to reference it MUST remain distinct. | S17, S18 |
| PE-ID-003 | RF-08 | MUST | Every protocol subject and its syntactic, serialized, stored, transmitted, or displayed representation | A semantic protocol subject and each representation of it MUST remain distinct. | S02, S17, S18 |
| PE-ID-004 | RF-08 | MUST NOT | Every relationship between separately identified protocol subjects | The identifier of one related protocol subject MUST NOT be substituted for the identifier of another subject. | S18, S24, S25, S27 |
| PE-ID-005 | RF-08 | MUST NOT | Every identifier of a Protocol Action occurrence | A Protocol Action identifier MUST NOT identify, encode, imply, or reconstruct the Private Actor who performed the action. | S18, S24 |
| PE-ID-006 | RF-08 | MUST NOT | Every public Evaluation, Determination, and Protocol State Transition identifier | An Evaluation, Determination, or Protocol State Transition identifier MUST NOT identify, encode, imply, or reconstruct a Private Actor. | S18, S25, S27 |
| PE-ID-007 | RF-08 | MUST NOT | Every implementation, transaction, retry, transport-attempt, storage, or diagnostic identifier | An operational identifier MUST NOT silently become or redefine a protocol-subject or occurrence identifier. | S18, S24, S27 |
| PE-ID-008 | RF-08 | MUST NOT | Every protocol identifier outside its declared subject and context | A protocol identifier MUST NOT be reused outside its declared role as a universal participant identifier, cross-subject join key, or cross-action identity mechanism. | S18, S24 |
| PE-ID-009 | RF-08 | MUST | Every permitted change of protocol-subject representation | A representation change MUST preserve the identity, semantics, relationships, and bounded identifier role of the represented protocol subject. | S02, S17, S18 |

## 23. SF-04 — Privacy, Actor Separation, and Compositional Unlinkability

SF-04 establishes the identity and privacy requirements that every later
protocol, application, implementation, observability, and assessment section
must preserve.

The governing principle is:

> Private actors, public actions.

A public Protocol Action may be visible and verifiable.

Its visibility does not imply visibility of its Private Actor.

> identifiesAction(id(A), A)
> =/=>
> identifiesActor(id(A), X)

### 23.1 Identity-Bearing and Non-Identity-Bearing Roles

Public and private values remain bounded to their protocol roles:

| Value or identity surface | Bounded role | Prohibited interpretation |
|---|---|---|
| `memberSecret` | Private possession material from which anonymous membership identity derives | Public identifier, wallet credential, application identity, or backend recovery handle |
| Membership leaf | Membership-layer representation derived from `memberSecret` | Public action identity or cross-action participant tag |
| Nullifier | Public action-context uniqueness value | Private-actor identity or reusable cross-action participant identity |
| Protocol Action identifier | Identifier of one public action occurrence | Identifier of the Private Actor |
| Evaluation, Determination, or transition identifier | Identifier of its exact public protocol subject | Identifier of the Private Actor or a reusable participant |
| Wallet identifier | Implementation or transaction context where present | Anonymous membership identity or Private Actor identity |
| Application identifier | Application-owned context | Protocol identity or Private Actor identity |
| Implementation or deployment identifier | Realization context | Protocol identity or Private Actor identity |
| Transport identifier | Delivery context where unavoidable | Protocol identity, continuity authority, or Private Actor identity |

### 23.2 RF-09 — Private Actors and Public Protocol Subjects

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-ACTSEP-001 | RF-09 | MUST | Every Privacy Engine realization of a public protocol action | Every realization MUST preserve the architectural principle `Private actors, public actions`. | S01, S18, S19, S21, S24 |
| PE-ACTSEP-002 | RF-09 | MUST | Every publicly visible Protocol Action | A publicly visible Protocol Action MUST remain verifiable to its declared protocol extent without disclosure of the Private Actor. | S19, S21, S24, S29 |
| PE-ACTSEP-003 | RF-09 | MUST | Every relationship between a Private Actor and a public Protocol Action | The performer relationship MUST preserve the Private Actor and Protocol Action as distinct subjects. | S18, S24 |
| PE-ACTSEP-004 | RF-09 | MUST | Every publicly identified protocol subject | A public protocol-subject identifier MUST identify only its declared protocol subject and role. | S18, S21, S24 |
| PE-ACTSEP-005 | RF-09 | MUST | Every public protocol consequence | A public protocol consequence MUST remain attributable to the applicable public protocol occurrence without becoming attributable to a disclosed Private Actor. | S18, S21, S24 |
| PE-ACTSEP-006 | RF-09 | MUST NOT | Every Protocol Action validity, authorization, uniqueness, and public-consequence rule | A rule governing a public Protocol Action MUST NOT require disclosure of civil, wallet, enrollment, admission, application, implementation, deployment, or transport identity as Private Actor identity. | S19, S21, S24, S29 |
| PE-ACTSEP-007 | RF-09 | MUST NOT | Every public Privacy Engine protocol surface | A public protocol surface MUST NOT require or create a reusable public participant identity. | S18, S19, S21, S22, S24 |

### 23.3 RF-10 — Privacy, Anonymity, and Unlinkability

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-PRIV-001 | RF-10 | MUST | Every Privacy Engine protocol action governed by anonymous-participation semantics | The protocol action MUST permit verification of its applicable validity properties without disclosure of the Private Actor. | S01, S19, S21, S24 |
| PE-PRIV-002 | RF-10 | MUST | Every public value and public protocol subject exposed by an anonymous action | Private Actor identity MUST remain non-inferable from each exposed value or subject within the protocol-defined privacy boundary. | S18, S19, S21, S24 |
| PE-PRIV-003 | RF-10 | MUST | Every pair or collection of anonymous Protocol Actions in distinct action contexts | Cross-action unlinkability MUST be preserved unless the published protocol generation expressly defines a narrower public relationship that remains non-identifying. | S01, S18, S19, S21, S24 |
| PE-PRIV-004 | RF-10 | MUST NOT | Every wallet identifier, wallet signature, wallet-derived value, and wallet relationship | Wallet identity MUST NOT be substituted for, used to infer, or represented as anonymous membership identity or Private Actor identity. | S01, S19, S20, S21, S22, S29 |
| PE-PRIV-005 | RF-10 | MUST NOT | Every application identifier, account, profile, metadata value, and application-defined relationship | Application identity or application metadata MUST NOT be substituted for, used to infer, or represented as protocol identity or Private Actor identity. | S18, S20, S21, S29 |
| PE-PRIV-006 | RF-10 | MUST NOT | Every implementation identifier and implementation-specific internal value | Implementation identity or internal implementation context MUST NOT be substituted for, used to infer, or represented as protocol identity or Private Actor identity. | S17, S18, S21 |
| PE-PRIV-007 | RF-10 | MUST NOT | Every deployment identifier, topology coordinate, service identity, and infrastructure relationship | Deployment identity or infrastructure topology MUST NOT be substituted for, used to infer, or represented as protocol identity or Private Actor identity. | S18, S20, S21, S22 |
| PE-PRIV-008 | RF-10 | MUST NOT | Every transport identifier, connection attribute, delivery path, retry path, and request context | Transport identity or delivery context MUST NOT be substituted for, used to infer, or represented as protocol identity or Private Actor identity. | S18, S20, S21, S22 |
| PE-PRIV-009 | RF-10 | MUST NOT | Every enrollment right, admission object, funding relationship, sponsor relationship, and associated provenance | Enrollment, admission, funding, or sponsor provenance MUST NOT be carried into public-action identity or used as an action-layer correlation value. | S01, S19, S20, S21, S22, S29 |
| PE-PRIV-010 | RF-10 | MUST | Every action-local public value | An action-local public value MUST remain bounded to its declared action role, action context, and permitted protocol interpretation. | S18, S19, S21, S24 |
| PE-PRIV-011 | RF-10 | MUST | Every privacy-sensitive failure path | Failure handling MUST preserve Private Actor non-disclosure and the non-identity-bearing role of public values. | S18, S20, S21, S29 |
| PE-PRIV-012 | RF-10 | MUST NOT | Every implementation, profile, application, conformance claim, diagnostic, and specification interpretation | A Privacy Engine artifact MUST NOT claim anonymity, unlinkability, metadata protection, or transport protection beyond the bounded guarantees of the identified published protocol generation. | S01, S02, S17, S18 |

### 23.4 RF-11 — Compositional Privacy, Observability, and Forbidden Correlation

Privacy must hold for public surfaces both individually and in composition:

> nonIdentifying(S1)

> and nonIdentifying(S2)

> and ...

> and nonIdentifying(Sn)

> -> nonIdentifying(composition(S1, S2, ..., Sn))

Therefore:

> identifiesProtocolSubject(id(S1), S1)

> and ...

> identifiesProtocolSubject(id(Sn), Sn)

> =/=> identifiesActor(composition(id(S1), ..., id(Sn)), X)

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-COMP-001 | RF-11 | MUST | Every composition of publicly exposed Privacy Engine values, subjects, consequences, and records | The composition MUST remain non-identifying for the Private Actor within the protocol-defined privacy boundary. | S02, S18, S20, S21, S22 |
| PE-COMP-002 | RF-11 | MUST NOT | Every implementation-controlled identifier, timing label, diagnostic, serialization field, log field, storage key, route, and public response | An implementation-controlled surface MUST NOT create an actor-reconstruction, provenance, or unauthorized cross-action correlation bridge. | S01, S02, S18, S20, S21, S22, S29 |
| PE-COMP-003 | RF-11 | MUST | Every privacy-sensitive field name, variable name, route name, log label, diagnostic, comment, example, test, serialization field, and specification term | Privacy-sensitive naming and documentation MUST use neutral terminology that preserves non-attribution and the bounded role of each value. | S01, S02, S18, S20, S21, S22 |
| PE-COMP-004 | RF-11 | MUST | Every public observability surface | Public observability MUST expose only the minimum role-bounded information required by the applicable protocol semantics. | S01, S18, S20, S21, S22, S29 |
| PE-COMP-005 | RF-11 | MUST | Every diagnostic and failure-reporting surface | A diagnostic MUST describe only the applicable protocol subject, status, or bounded failure classification without identifying or reconstructing the Private Actor. | S01, S18, S20, S21, S22 |
| PE-COMP-006 | RF-11 | MUST NOT | Every request history, telemetry record, path-acquisition record, submission record, and operational history | Operational history or telemetry MUST NOT create a persistent relationship linking private participation across protocol layers or action contexts. | S01, S18, S20, S21, S22 |
| PE-COMP-007 | RF-11 | MUST NOT | Every public protocol response, log, status surface, and diagnostic | A public surface MUST NOT expose unnecessary provenance, topology, route, provider, retry, fallback, or execution-path information capable of increasing actor correlation. | S01, S18, S20, S21, S22 |
| PE-COMP-008 | RF-11 | MUST | Every information crossing between Privacy Engine layers | A layer boundary MUST pass only the minimum preserved output required by the receiving layer without carrying unrelated provenance or identity context from the preceding layer. | S01, S20, S21, S22 |
| PE-COMP-009 | RF-11 | MUST | Every implementation composition exposing multiple individually non-identifying surfaces | The combined surface MUST be assessed and preserved as non-identifying rather than relying only on the independent safety of each component. | S02, S18, S20, S21, S22 |
| PE-COMP-010 | RF-11 | MUST NOT | Every informative example, supporting cross-reference, test artifact, assessment record, and documentation surface | Supporting or informative material MUST NOT introduce a correlation or identity interpretation prohibited from normative runtime surfaces. | S01, S02, S17, S18 |

### 23.5 RF-15 — Anonymous Membership, Continuity, and Enrollment Separation

The anonymous-membership identity path is:

> memberSecret
> ->
> leaf

Continuity exists only through possession of the same original
`memberSecret`.

The leaf remains a membership-layer representation. It does not become public
action identity.

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-MEM-001 | RF-15 | MUST | Every anonymous membership identity in the current published protocol generation | Anonymous membership identity MUST derive solely from private `memberSecret` possession through `leaf = Poseidon1(memberSecret)`. | S01, S19, S20, S21, S22 |
| PE-MEM-002 | RF-15 | MUST | Every claim of anonymous membership continuity | Anonymous membership continuity MUST mean possession of the same original `memberSecret`. | S01, S19, S21, S22, S29 |
| PE-MEM-003 | RF-15 | MUST | Every replacement of an active `memberSecret` with a different secret | A different `memberSecret` MUST establish a different anonymous membership identity. | S01, S19, S21, S22 |
| PE-MEM-004 | RF-15 | MUST NOT | Every wallet, backend, application, deployment, transport, and heuristic recovery mechanism | A mechanism other than possession of the same original `memberSecret` MUST NOT establish, reconstruct, or simulate anonymous membership continuity. | S01, S19, S20, S21, S22, S29 |
| PE-MEM-005 | RF-15 | MUST | Every membership leaf | A membership leaf MUST remain bounded to membership inclusion, path acquisition, and private proof-witness use according to the applicable protocol semantics. | S01, S19, S20, S21, S22 |
| PE-MEM-006 | RF-15 | MUST | Every membership enrollment or activation | Enrollment or activation MUST attach membership only to the privately controlled membership material presented for that enrollment without importing funding provenance into membership identity. | S01, S19, S20, S21, S22 |
| PE-MEM-007 | RF-15 | MUST NOT | Every enrollment right, admission object, funding wallet, sponsor relationship, and accounting state | An enrollment or admission artifact MUST NOT be represented as anonymous membership identity or Private Actor identity. | S01, S19, S20, S21, S22, S29 |
| PE-MEM-008 | RF-15 | MUST NOT | Every public enrollment, membership-status, readiness, and application surface | A public surface MUST NOT expose a reusable mapping from enrollment or admission provenance to anonymous membership or public action occurrence. | S01, S19, S20, S21, S22, S29 |

### 23.6 RF-19 — Nullifier-Based Uniqueness and Action-Bounded Unlinkability

The current published protocol generation uses:

> nullifier = Poseidon3(memberSecret, actionId, SIGN_DOMAIN)

The nullifier establishes scoped uniqueness.

It does not establish reusable participant identity.

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-UNIQ-001 | RF-19 | MUST | Every anonymous action type requiring one action per member per action context | Uniqueness MUST be enforced within the declared `(actionId, member)` scope. | S01, S19, S20, S21, S22, S24 |
| PE-UNIQ-002 | RF-19 | MUST | Every nullifier in the current published protocol generation | A nullifier MUST be derived as `Poseidon3(memberSecret, actionId, SIGN_DOMAIN)`. | S01, S19, S20, S22 |
| PE-UNIQ-003 | RF-19 | MUST | Every action-layer duplicate-prevention decision in the current published protocol generation | Nullifier status MUST remain the sole action-layer duplicate-prevention primitive. | S01, S19, S21, S22, S24 |
| PE-UNIQ-004 | RF-19 | MUST NOT | Every public nullifier and nullifier-status record | A nullifier or its status MUST NOT be represented as Private Actor identity or reusable participant identity. | S01, S18, S19, S20, S21, S22, S24 |
| PE-UNIQ-005 | RF-19 | MUST NOT | Every nullifier outside its declared action context | A nullifier MUST NOT be reused as a cross-action join key, participant tag, continuity handle, or global identity mechanism. | S01, S18, S19, S20, S21, S22, S24 |
| PE-UNIQ-006 | RF-19 | MUST NOT | Every wallet identifier, membership leaf, enrollment identifier, admission object, and application account | A wallet, leaf, enrollment, admission, or application identifier MUST NOT replace the nullifier as the action-layer uniqueness key. | S01, S19, S20, S21, S22, S24 |
| PE-UNIQ-007 | RF-19 | MUST NOT | Every duplicate-status response, log, diagnostic, event, and read model | Duplicate-status observability MUST NOT disclose or enable inference of the Private Actor beyond the bounded action-local uniqueness fact. | S01, S18, S20, S21, S22 |
| PE-UNIQ-008 | RF-19 | MUST NOT | Every interpretation of nullifier-enforced uniqueness | Scoped nullifier uniqueness MUST NOT be represented as one-person, one-human, one-wallet, or globally reusable participant uniqueness. | S01, S19, S21, S22, S24 |

## 24. Supporting Relationships and Deferred Operational Semantics

SF-03 and SF-04 establish terminology, identity, and privacy dependencies for
later sections.

They do not yet compose the complete operational semantics of the subjects
they identify.

The following authoritative homes remain deferred:

- interfaces, Protocol Operations, Published Results, requests, responses, and
  adapters: SF-05 and SF-12;
- proofs, declared public inputs, verification, evidence, and validity: SF-06;
- Protocol Actions and applicable rules: SF-07;
- Evaluation, Determination, acceptance, rejection, and accepted
  no-transition behavior: SF-08;
- protocol state, transition mappings, preconditions, transition occurrences,
  authorization, execution, and commitment: SF-09 and SF-10;
- history, public consequences, failure, staleness, and re-evaluation: SF-11;
- runtime, implementation, realization, compatibility, profiles, and reference
  implementations: SF-12–SF-14;
- conformance and certification: SF-15;
- protocol-semantic preservation and complete explicit exclusions: SF-16.

References to these subjects in SF-03 and SF-04 establish only terminology,
identity separation, or privacy dependencies.

They do not relocate the later requirement families.

RF-49 and RF-50 remain reserved to SF-16.

## 25. Current Composition Boundary

This cumulative document currently contains the authoritative normative homes
for:

- RF-01–RF-11;
- RF-15;
- RF-19.

The following section families remain deliberately uncomposed:

- SF-05 — interface contracts, protocol surfaces, operations, and results;
- SF-06 — proofs, public inputs, verification, evidence, and validity;
- SF-07 — Protocol Actions and applicable rules;
- SF-08 — Evaluation, Determination, acceptance, and rejection;
- SF-09 — protocol state, transition semantics, preconditions, and
  authorization;
- SF-10 — transition execution, commitment, atomicity, and state evolution;
- SF-11 — history, public consequences, failure, staleness, and re-evaluation;
- SF-12 — application, adapter, runtime, and integration boundaries;
- SF-13 — implementation, realization, compatibility, and migration;
- SF-14 — implementation profiles and reference implementations;
- SF-15 — conformance and certification;
- SF-16 — semantic preservation and explicit exclusions.

Their absence is explicit and must not be interpreted as implicit definition,
permission, prohibition, or completion.

This slice does not define:

- interface-contract or concrete-interface semantics;
- Published Result semantics;
- proof construction or proof verification;
- declared public-input schemas or ordering;
- complete Protocol Action lifecycle or validity requirements;
- complete Evaluation or Determination semantics;
- acceptance or rejection requirements;
- protocol-state or transition lifecycle requirements;
- transition execution or commitment;
- application request, response, or adapter behavior;
- runtime or implementation mechanics;
- blockchain consensus;
- transaction formats;
- transport or relay mechanics;
- database or storage mechanics;
- implementation profiles;
- reference implementations;
- conformance assessment;
- certification;
- RF-49 semantic-preservation requirements;
- or RF-50 complete exclusion requirements.

These are local composition-boundary statements. They do not relocate or
duplicate the authoritative homes reserved for later requirement families.

The cumulative specification contains 152 stable normative requirements:

- 81 requirements preserved from SF-01 and SF-02;
- 71 requirements composed through SF-03 and SF-04.

The document remains incomplete until SF-05–SF-16 have been composed and the
complete specification has passed final consolidation review.

## 26. Cumulative Traceability

The source codes used in the normative requirement tables are:

| Code | Supporting source |
|---|---|
| S01 | `STATE.md` |
| S02 | `PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_COMPOSITION_MAP_V1.md` |
| S03 | `PRIVACY_ENGINE_FORMAL_SPECIFICATION_STRUCTURE_V1.md` |
| S04 | `PRIVACY_ENGINE_NORMATIVE_SPECIFICATION_LANGUAGE_V1.md` |
| S05 | `PRIVACY_ENGINE_NORMATIVE_REQUIREMENT_MODEL_V1.md` |
| S06 | `PRIVACY_ENGINE_NORMATIVE_REQUIREMENT_SET_MODEL_V1.md` |
| S07 | `PRIVACY_ENGINE_SPECIFICATION_SECTION_MODEL_V1.md` |
| S08 | `PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_MODEL_V1.md` |
| S09 | `PRIVACY_ENGINE_PROTOCOL_MODEL_V1.md` |
| S10 | `PRIVACY_ENGINE_PROTOCOL_GENERATION_MODEL_V1.md` |
| S11 | `PRIVACY_ENGINE_PROTOCOL_PUBLICATION_MODEL_V1.md` |
| S12 | `PRIVACY_ENGINE_PUBLISHED_PROTOCOL_MODEL_V1.md` |
| S13 | `PRIVACY_ENGINE_PROTOCOL_SUCCESSION_MODEL_V1.md` |
| S14 | `PRIVACY_ENGINE_PROTOCOL_LINEAGE_MODEL_V1.md` |
| S15 | `PRIVACY_ENGINE_VERSIONING_MODEL_V1.md` |
| S16 | `PRIVACY_ENGINE_DEPRECATION_AND_MIGRATION_MODEL_V1.md` |
| S17 | `PRIVACY_ENGINE_FORMAL_ARCHITECTURE_CONSOLIDATION_REVIEW_V1.md` |
| S18 | `PRIVACY_ENGINE_PROTOCOL_USE_CHAIN_CONSOLIDATION_REVIEW_V1.md` |
| S19 | `PRIVACY_ENGINE_DEFINITION.md` |
| S20 | `PRIVACY_ENGINE_LAYER_INTERFACE_MAP_V1.md` |
| S21 | `PRIVACY_ENGINE_PROTOCOL_BOUNDARY_V1.md` |
| S22 | `PRIVACY_ENGINE_PROTOCOL_SURFACE_V1.md` |
| S23 | `PRIVACY_ENGINE_PROTOCOL_OPERATION_MODEL_V1.md` |
| S24 | `PRIVACY_ENGINE_PROTOCOL_ACTION_MODEL_V1.md` |
| S25 | `PRIVACY_ENGINE_PROTOCOL_ACTION_EVALUATION_MODEL_V1.md` |
| S26 | `PRIVACY_ENGINE_PROTOCOL_TRANSITION_MODEL_V1.md` |
| S27 | `PRIVACY_ENGINE_PROTOCOL_STATE_TRANSITION_MODEL_V1.md` |
| S28 | `PRIVACY_ENGINE_PROTOCOL_CLAIM_ASSESSMENT_V1.md` |
| S29 | `PRIVACY_ENGINE_APPLICATION_ADAPTER_CONTRACT_V1.md` |

Source references record semantic provenance and composition support.

They do not create independent normative authority.

The authoritative normative home of each requirement is the composed SF-01,
SF-02, SF-03, or SF-04 section containing its requirement family.

The traceability direction remains:

> established formal source
> -> normative requirement family
> -> one authoritative specification destination
> -> stable normative requirement

The composition invariants remain:

> oneSemanticRequirement(R)
> ->
> oneAuthoritativeNormativeHome(R)

> sameSemanticRequirement(R1, R2)
> ->
> oneNormativeRequirement(R)

> supportingReference(N2, R)
> =/=>
> authoritativeHome(R, N2)

> supportingReference(N2, R)
> =/=>
> redefines(N2, R)

> traceableTo(R, F)

> semantics(Spec) = semantics(P)

Traceability organizes established semantics. It does not redefine them.

## 27. Conclusion

SF-01 through SF-04 now establish the cumulative normative foundation,
protocol-generation model, canonical terminology, subject-identity model, and
privacy model of the Privacy Engine Protocol Specification.

SF-03 establishes:

- canonical protocol terminology;
- stable subject interpretation;
- the complete identified protocol-use occurrence inventory;
- subject-identity separation;
- type-and-occurrence separation;
- subject, identifier, and representation separation;
- relationship direction and boundedness;
- downstream preservation of subject identity;
- and the prohibition of terminology-based ontology expansion.

SF-04 establishes:

- Private Actors and public Protocol Actions;
- public action visibility without Private Actor disclosure;
- anonymous-membership identity and continuity boundaries;
- action-local public representation;
- nullifier-based scoped uniqueness;
- cross-action unlinkability;
- separation from wallet, application, implementation, deployment, and
  transport identity;
- compositional privacy;
- privacy-preserving observability and diagnostics;
- and privacy-language discipline across runtime and documentation surfaces.

Protocol Operation remains distinct from Protocol Action occurrence.

Protocol Transition remains distinct from Protocol State Transition
occurrence.

Protocol Action, Evaluation, Determination, and Protocol State Transition
retain their separate identities.

Private Actor remains distinct from every public protocol subject and public
consequence.

No reusable participant identity, cross-action identity mechanism, or
actor-reconstruction bridge is introduced.

No Protocol Claim or other new first-class subject is introduced.

The 81 requirements established by SF-01 and SF-02 remain unchanged.

The cumulative Protocol Specification now contains 152 stable normative
requirements and is ready to receive SF-05 through SF-07 without reopening the
ontology or redefining privacy.

The Protocol Specification remains derived, portable, implementation-facing,
and non-authoritative.

Protocol authority always remains with the published Privacy Engine protocol generation.
