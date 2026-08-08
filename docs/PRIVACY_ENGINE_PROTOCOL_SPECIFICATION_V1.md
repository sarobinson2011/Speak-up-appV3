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
- SF-05 — Interface Contracts, Protocol Surfaces, Operations, and Results: composed;
- SF-06 — Proofs, Public Inputs, Verification, Evidence, and Validity: composed;
- SF-07 — Protocol Actions and Applicable Rules: composed;
- SF-08–SF-16: not yet composed.

The requirements in the composed sections are normative within their declared
scope.

This document does not yet constitute the complete Privacy Engine Protocol
Specification because the remaining authoritative section families have not
been composed.

No absent section, deferred requirement family, supporting reference, or
informative statement may be treated as implicitly completed.

The current composition boundary is defined in Section 28.

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
- SF-04 — Privacy, Actor Separation, and Compositional Unlinkability;
- SF-05 — Interface Contracts, Protocol Surfaces, Operations, and Results;
- SF-06 — Proofs, Public Inputs, Verification, Evidence, and Validity;
- SF-07 — Protocol Actions and Applicable Rules.

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
- RF-12 — Interface contracts and concrete interface specifications;
- RF-13 — Protocol surfaces, operations, and Published Results;
- RF-15 — Anonymous membership, continuity, and enrollment separation;
- RF-16 — Proofs and declared public inputs;
- RF-17 — Proof verification;
- RF-18 — Evidence, protocol validity, and non-proof validity conditions;
- RF-19 — Nullifier-based uniqueness and action-bounded unlinkability;
- RF-20 — Protocol Actions;
- RF-21 — Applicable protocol-rule sets and action validity.

The current document does not define the later Evaluation, Determination,
acceptance, rejection, protocol-state, transition, application, runtime,
implementation, implementation-profile, conformance, or certification
requirements assigned to SF-08–SF-16.

RF-14 remains assigned to SF-12.

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

The semantic-family codes introduced by the current cumulative composition are:

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
| PE-IFACE-* | RF-12 | SF-05 |
| PE-SURF-* | RF-13 | SF-05 |
| PE-MEM-* | RF-15 | SF-04 |
| PE-PROOF-* | RF-16 | SF-06 |
| PE-VERIFY-* | RF-17 | SF-06 |
| PE-VALID-* | RF-18 | SF-06 |
| PE-UNIQ-* | RF-19 | SF-04 |
| PE-ACTION-* | RF-20 | SF-07 |
| PE-RULE-* | RF-21 | SF-07 |

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

## 24. SF-05 — Interface Contracts, Protocol Surfaces, Operations, and Results

SF-05 defines the implementation-facing boundary from published interface
meaning to concrete representation, exposed capability, and interface-level
semantic result.

It preserves the established distinction between semantic subjects and their
representations.

It does not define application requests, application responses, application
adapters, runtime machinery, transport, or implementation topology.

### 24.1 Interface Contract and Concrete Interface Specification

An Interface Contract is the bounded published semantic contract through which
one published Privacy Engine protocol generation exposes externally relied-upon
behavior.

A Concrete Interface Specification is one identified syntactic realization of
exactly one Interface Contract for one bounded integration surface.

The relationship is:

> definesBoundedInterfaceMeaning(K)

> derives(K, P)

> realizes(S, K)

> semantics(S) = semantics(K)

The semantic contract and its representation remain distinct:

> K != S

> representationOf(S, K)
> =/=>
> definesProtocolSemantics(S)

An Interface Contract owns its bounded semantic definition.

That bounded ownership does not become protocol authority:

> definesBoundedInterfaceMeaning(K)
> =/=>
> protocolAuthority(K)

Protocol authority always remains with the published Privacy Engine protocol generation.

### 24.2 RF-12 — Interface Contracts and Concrete Interface Specifications

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-IFACE-001 | RF-12 | MUST | Every Privacy Engine Interface Contract | An Interface Contract MUST possess one stable identity, one bounded semantic role, and one version sufficient to distinguish its published meaning. | S02, S17, S20, S22, S31 |
| PE-IFACE-002 | RF-12 | MUST | Every Privacy Engine Interface Contract | An Interface Contract MUST derive from exactly one identified published Privacy Engine protocol generation. | S02, S09, S17, S31 |
| PE-IFACE-003 | RF-12 | MUST | Every Privacy Engine Interface Contract | An Interface Contract MUST define its bounded input semantics, output semantics, Protocol Operations, externally relied-upon behavior, and applicable observable failure semantics. | S22, S31 |
| PE-IFACE-004 | RF-12 | MUST | Every Interface Contract and every concrete realization of it | Interface meaning and concrete representation MUST remain distinct semantic and syntactic roles. | S17, S20, S30, S31 |
| PE-IFACE-005 | RF-12 | MUST | Every Concrete Interface Specification | A Concrete Interface Specification MUST possess one stable specification identity, one specification version, and one bounded integration surface. | S30 |
| PE-IFACE-006 | RF-12 | MUST | Every Concrete Interface Specification | A Concrete Interface Specification MUST identify and realize exactly one governing Interface Contract. | S30, S31 |
| PE-IFACE-007 | RF-12 | MUST | Every Concrete Interface Specification | A Concrete Interface Specification MUST completely define the operation names, invocation forms, field ordering, type constraints, encoding rules, result representations, and externally observable error representations required by its bounded surface. | S30 |
| PE-IFACE-008 | RF-12 | MUST | Every Concrete Interface Specification and its governing Interface Contract | The concrete representation MUST preserve semantic equivalence with the governing Interface Contract. | S20, S30, S31 |
| PE-IFACE-009 | RF-12 | MAY | Every Interface Contract permitting multiple concrete realizations | Multiple Concrete Interface Specifications MAY realize the same Interface Contract when each realization independently preserves the complete bounded interface meaning. | S30 |
| PE-IFACE-010 | RF-12 | MUST | Every representation-only interface change | A representation-only change MUST preserve the identity, semantics, ordering requirements, compatibility boundary, and observable guarantees of the governing Interface Contract. | S22, S30, S31 |
| PE-IFACE-011 | RF-12 | MUST | Every change to published Interface Contract meaning | A change to published interface semantics, obligations, validity, or observable guarantees MUST be represented through the applicable distinct-generation and versioning rules. | S15, S22, S30, S31 |
| PE-IFACE-012 | RF-12 | MUST NOT | Every Interface Contract and Concrete Interface Specification | Implementation algorithms, storage layouts, deployment topology, transport machinery, operational policy, and application-defined meaning MUST NOT become interface semantics unless the published protocol generation expressly defines them as such. | S20, S22, S29, S30, S31 |
| PE-IFACE-013 | RF-12 | MUST NOT | Every Interface Contract and Concrete Interface Specification | An Interface Contract or Concrete Interface Specification MUST NOT independently acquire, transfer, replace, or modify protocol authority. | S02, S17, S30, S31 |
| PE-IFACE-014 | RF-12 | MUST | Every public Interface Contract and Concrete Interface Specification | Every public interface realization MUST preserve the applicable SF-03 and SF-04 identity, privacy, unlinkability, minimum-disclosure, and neutral-naming requirements. | S01, S18, S20, S22, S29, S30, S31 |

### 24.3 Protocol Surface and Protocol Operation

A Protocol Surface is one identified and bounded externally stable capability
boundary of a published protocol generation.

A Protocol Surface exposes protocol commitments while leaving implementation
machinery replaceable.

A Protocol Operation is one stable, published, bounded capability identified by
an Interface Contract.

A Protocol Operation defines capability.

A Protocol Action is one occurrence of protocol-defined behavior.

The distinction is:

> operationType(O)
> =/=>
> actionOccurrence(A)

A Protocol Operation does not become execution, implementation, transport, or
application behavior.

### 24.4 Published Result

A Published Result is one interface-level semantic result defined according to
a governing Interface Contract and Protocol Operation.

A Published Result is distinct from its concrete representation:

> publishedResult(Y)
> =/=>
> representation(YR)

It is also distinct from a Protocol Action Determination:

> publishedResult(Y)
> =/=>
> determination(D)

A Published Result does not become an Evaluation Outcome object:

> publishedResult(Y)
> =/=>
> evaluationOutcomeObject(Y)

A Published Result is not the committed public protocol-state consequence of a
Protocol State Transition:

> publishedResult(Y)
> =/=>
> publicProtocolConsequence(U, Q1)

These distinctions preserve the later authoritative homes of Determination,
state transition, commitment, and public consequence.

### 24.5 RF-13 — Protocol Surfaces, Operations, and Published Results

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-SURF-001 | RF-13 | MUST | Every Privacy Engine Protocol Surface | A Protocol Surface MUST possess one stable identity and one bounded externally relied-upon capability scope within one published protocol generation. | S02, S09, S22 |
| PE-SURF-002 | RF-13 | MUST | Every Protocol Surface | A Protocol Surface MUST expose only the protocol capabilities, semantic guarantees, compatibility boundaries, and observable behavior defined for that surface. | S09, S22, S31 |
| PE-SURF-003 | RF-13 | MUST | Every implementation realizing a Protocol Surface | Internal implementation machinery MUST remain replaceable when the complete published semantics and guarantees of the Protocol Surface remain preserved. | S09, S22, S23, S31 |
| PE-SURF-004 | RF-13 | MUST NOT | Every implementation detail behind a Protocol Surface | Code structure, storage layout, deployment topology, relay selection, transport, persistence, monitoring, optimization, or helper naming MUST NOT become protocol-surface semantics merely because a current implementation uses it. | S09, S20, S22, S23, S31 |
| PE-SURF-005 | RF-13 | MUST | Every Privacy Engine Protocol Operation | A Protocol Operation MUST possess one stable capability identity defined by one published Interface Contract within one identified protocol generation. | S09, S23, S31 |
| PE-SURF-006 | RF-13 | MUST | Every Protocol Operation | A Protocol Operation MUST define one bounded protocol-owned capability, including its applicable input meaning, output meaning, and externally relied-upon behavior. | S09, S23, S31 |
| PE-SURF-007 | RF-13 | MUST | Every Protocol Operation and associated Protocol Action | The Protocol Operation capability type and each Protocol Action occurrence classified by that capability MUST remain distinct. | S02, S18, S23, S24 |
| PE-SURF-008 | RF-13 | MUST | Every offered Protocol Operation | The governing Interface Contract MUST declare the operation's applicability conditions and the semantic roles of every required input and Published Result. | S23, S31, S32 |
| PE-SURF-009 | RF-13 | MUST | Every implementation realizing a Protocol Operation | An implementation MUST preserve the operation's published capability across execution and implementation variation. | S09, S23 |
| PE-SURF-018 | RF-13 | MUST NOT | Every execution or implementation variation realizing a Protocol Operation | Execution or implementation variation MUST NOT redefine the Protocol Operation's published capability. | S09, S23 |
| PE-SURF-010 | RF-13 | MUST | Every Published Result | A Published Result MUST possess one bounded result identity and MUST identify the governing Interface Contract and Protocol Operation from which its meaning derives. | S31, S32 |
| PE-SURF-011 | RF-13 | MUST | Every Published Result | A Published Result MUST express only the interface-level success semantics, failure semantics, guarantees, and observable meaning defined by its governing Interface Contract. | S31, S32 |
| PE-SURF-012 | RF-13 | MUST | Every Published Result and concrete representation of it | Published Result meaning and its serialized, transported, stored, displayed, or application-facing representation MUST remain distinct. | S20, S30, S32 |
| PE-SURF-013 | RF-13 | MUST | Every concrete realization or translation of a Published Result | Every concrete realization or permitted downstream translation MUST preserve the complete bounded meaning of the same Published Result. | S29, S30, S32 |
| PE-SURF-014 | RF-13 | MUST NOT | Every Published Result | A Published Result MUST NOT be represented as a Protocol Action Evaluation, Protocol Action Determination, acceptance object, rejection object, or separate Evaluation Outcome object. | S02, S18, S25, S32 |
| PE-SURF-015 | RF-13 | MUST NOT | Every Published Result | A Published Result MUST NOT be represented as a committed Protocol State Transition or as an independently authoritative public protocol-state consequence. | S02, S18, S27, S32 |
| PE-SURF-016 | RF-13 | MUST NOT | Every application interpretation or representation of a Protocol Surface, Protocol Operation, or Published Result | Application-defined meaning, terminology, formatting, workflow, or response structure MUST NOT redefine protocol capability, validity, or Published Result meaning. | S09, S24, S29, S32 |
| PE-SURF-017 | RF-13 | MUST | Every public Protocol Surface, Protocol Operation representation, and Published Result | The complete exposed composition MUST preserve the applicable SF-03 and SF-04 identity, privacy, unlinkability, minimum-disclosure, and forbidden-correlation requirements. | S01, S18, S20, S22, S24, S32 |

## 25. SF-06 — Proofs, Public Inputs, Verification, Evidence, and Validity

SF-06 defines the bounded proof and validity path used before complete Protocol
Action Evaluation.

It defines proofs, declared public inputs, proof verification, proof evidence,
non-proof validity conditions, and complete protocol-action validity.

It does not define Evaluation, Determination, acceptance, rejection,
authorization, transition execution, commitment, or application truth.

### 25.1 Proofs and Declared Public Inputs

A proof is one bounded cryptographic evidence object constructed according to
the proof relation and proof-system requirements of the applicable published
protocol generation.

A proof remains distinct from:

- its representation;
- its public inputs;
- its private witness;
- the Protocol Action it supports;
- the Private Actor;
- proof verification;
- complete Protocol Action validity.

The current published generation uses:

- Circom;
- Groth16 over BN254;
- Poseidon hashing;
- a tree depth of 16;
- a root-history window of 16.

The locked declared public-input ordering is:

1. `nullifier`;
2. `petitionId` / `actionId`;
3. `membershipRoot`.

The public-input roles are:

- `nullifier`: action-context-bounded uniqueness;
- `petitionId` / `actionId`: the bounded public action context;
- `membershipRoot`: the membership-state commitment against which the proof is
  evaluated.

Private witness material includes the applicable `memberSecret`, Merkle path,
and leaf-related witness data.

The current relation preserves:

> leaf = Poseidon1(memberSecret)

> nullifier = Poseidon3(memberSecret, actionId, SIGN_DOMAIN)

The public-input set does not contain the `memberSecret`, leaf, Merkle path,
wallet identity, enrollment provenance, admission provenance, relay selection,
path-provider selection, or execution-topology information.

### 25.2 RF-16 — Proofs and Declared Public Inputs

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-PROOF-001 | RF-16 | MUST | Every proof required by a Privacy Engine Protocol Action | A proof MUST possess one bounded evidence identity distinct from its encoding, public inputs, private witness, supported Protocol Action, and Private Actor. | S18, S19, S24 |
| PE-PROOF-002 | RF-16 | MUST | Every proof type in a published protocol generation | The published protocol generation MUST declare the proof relation, proof-system requirements, public-input schema, private-witness boundary, and verification semantics applicable to the proof type. | S01, S19, S20, S22, S24 |
| PE-PROOF-003 | RF-16 | MUST | Every current-generation anonymous-action proof | The proof relation MUST establish knowledge of the applicable membership secret and membership witness, inclusion under the declared membership root, and correct nullifier derivation for the declared action context without disclosing the Private Actor. | S01, S19, S20, S24 |
| PE-PROOF-004 | RF-16 | MUST | Every proof relation and proof-construction boundary | Public inputs and private witness material MUST remain explicitly separated according to the applicable published proof relation. | S01, S19, S20 |
| PE-PROOF-005 | RF-16 | MUST | Every current-generation anonymous-action public-input set | The declared public inputs MUST occur in the exact ordered sequence `nullifier`, `petitionId` or `actionId`, `membershipRoot`. | S01, S20, S22, S24 |
| PE-PROOF-006 | RF-16 | MUST | Every current-generation declared public-input interpretation | `nullifier` MUST remain bounded to action-context uniqueness, `petitionId` or `actionId` MUST remain bounded to action context, and `membershipRoot` MUST remain bounded to the applicable membership-state commitment. | S01, S19, S20, S24 |
| PE-PROOF-007 | RF-16 | MUST | Every proof and declared public-input set presented together | The proof representation, public-input values, ordering, action context, and proof relation MUST form one coherent verification input. | S01, S20, S24 |
| PE-PROOF-008 | RF-16 | MUST | Every proof-construction process | Proof construction MUST keep `memberSecret`, Merkle path, membership leaf, and other private witness material outside public inputs and public protocol surfaces. | S01, S19, S20 |
| PE-PROOF-009 | RF-16 | MUST | Every proof realization for the current published generation | The proof realization MUST use the published generation's declared Circom and Groth16-over-BN254 proof semantics and compatible verifier artifacts. | S01, S19, S22 |
| PE-PROOF-010 | RF-16 | MUST | Every published proof artifact set | Proof artifacts, verification keys, verifier artifacts, public-input ordering, and associated provenance MUST satisfy the published artifact-integrity and reproducibility requirements. | S01, S22 |
| PE-PROOF-011 | RF-16 | MUST | Every permitted proof or public-input representation | A representation MUST preserve the complete proof relation, proof-system semantics, verifier compatibility, input meaning, and input ordering of the identified published generation. | S01, S20, S22, S30 |
| PE-PROOF-012 | RF-16 | MUST | Every change to a proof system, proof relation, public-input schema, public-input ordering, verifier encoding, or artifact-integrity rule | The change MUST follow the applicable distinct-generation, versioning, publication, and artifact-regeneration requirements. | S01, S15, S22 |
| PE-PROOF-013 | RF-16 | MUST NOT | Every proof and proof representation | A proof or its representation MUST NOT be treated as the Protocol Action occurrence, Private Actor identity, wallet identity, membership identity, application truth, or reusable participant identity. | S18, S19, S20, S24 |
| PE-PROOF-014 | RF-16 | MUST NOT | Every declared public input and public-input composition | A public input or public-input composition MUST NOT exceed its declared role or become a reusable participant identifier, cross-action join key, actor-reconstruction value, or application-only correlation field. | S01, S18, S20, S24 |

### 25.3 Proof Verification

Proof verification is one bounded evaluation of a proof and its declared public
inputs against the applicable proof relation and verifier artifacts.

Let:

- `Z` be one proof;
- `PI` be its declared public-input set;
- `V` be one bounded proof-verification occurrence;
- `E` be the later complete Protocol Action Evaluation.

The relationship is:

> verifies(V, Z, PI)

> contributesTo(V, E)

A completed proof-verification occurrence produces one bounded valid or invalid
verification classification.

An inability to complete verification is a stage-local verification failure.
It is not silently converted into proof validity, proof invalidity, Protocol
Action acceptance, rejection, or commitment.

Proof verification is a bounded evaluation component.

It does not add another first-class subject to the established protocol-use
occurrence inventory.

### 25.4 RF-17 — Proof Verification

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-VERIFY-001 | RF-17 | MUST | Every required proof verification | Proof verification MUST occur as one bounded verification occurrence whose proof, public inputs, proof relation, verifier artifacts, and result are distinguishable. | S18, S19, S25 |
| PE-VERIFY-002 | RF-17 | MUST | Every proof-verification occurrence | Verification MUST evaluate exactly the presented proof and declared public-input set against the applicable published proof relation and verifier artifacts. | S01, S19, S20, S25 |
| PE-VERIFY-003 | RF-17 | MUST | Every correct proof-verification realization | Verification MUST be deterministic for the same proof, public inputs, proof relation, verifier artifacts, and protocol-relevant verification context. | S19, S25 |
| PE-VERIFY-004 | RF-17 | MUST | Every completed proof-verification occurrence | A completed verification MUST produce exactly one bounded proof-valid or proof-invalid classification. | S19, S25 |
| PE-VERIFY-005 | RF-17 | MUST | Every proof-valid classification | A proof-valid classification MUST establish only that the proof and declared public inputs satisfy the applicable published proof relation. | S18, S19, S24, S25 |
| PE-VERIFY-006 | RF-17 | MUST | Every proof-invalid classification required for a Protocol Action | A required proof-invalid classification MUST prevent that proof from satisfying the corresponding applicable proof-verification requirement. | S24, S25 |
| PE-VERIFY-007 | RF-17 | MUST | Every inability to complete required proof verification | Verification failure MUST remain distinguishable from a completed proof-valid classification, completed proof-invalid classification, Protocol Action rejection, and later failure classifications. | S02, S18, S25 |
| PE-VERIFY-008 | RF-17 | MUST | Every proof-valid verification result used in Protocol Action Evaluation | The result MUST contribute only the bounded evidence established by the applicable proof relation. | S18, S24, S25 |
| PE-VERIFY-009 | RF-17 | MUST NOT | Every proof-valid verification result | Successful proof verification MUST NOT independently establish complete Protocol Action validity, acceptance, rejection, transition authorization, transition execution, or commitment. | S02, S18, S24, S25 |
| PE-VERIFY-010 | RF-17 | MUST NOT | Every proof-verification occurrence and result | Proof verification MUST NOT establish Private Actor identity, wallet identity, enrollment provenance, admission provenance, application truth, legal truth, factual truth, or reusable participant identity. | S18, S19, S24, S25 |
| PE-VERIFY-011 | RF-17 | MUST NOT | Every proof-verification implementation | Verifier code structure, deployment address, transaction identity, runtime mechanism, storage, transport, or diagnostic behavior MUST NOT redefine the applicable proof relation or verification semantics. | S01, S20, S25 |
| PE-VERIFY-012 | RF-17 | MUST NOT | Every proof-verification component and result | A proof-verification component or result MUST NOT independently acquire or modify protocol authority. | S02, S17, S18, S25 |

### 25.5 Evidence and Complete Protocol Validity

Proof verification contributes bounded evidence to the later complete
Evaluation.

It does not independently establish complete protocol validity:

> verifiesValid(V, Z, PI)
> =/=>
> protocolValid(A, C)

It does not independently establish acceptance:

> verifiesValid(V, Z, PI)
> =/=>
> accepts(D, A)

It does not independently establish commitment:

> verifiesValid(V, Z, PI)
> =/=>
> committed(U)

Complete Protocol Action validity is defined by satisfaction of every applicable
protocol rule in one bounded evaluation context:

> applicableRules(A, R)

> protocolValid(A, C)
> iff
> satisfiesAll(A, R, C)

Applicable non-proof validity conditions can include:

- action-type requirements;
- public-input shape and domain requirements;
- proof-to-public-input coherence;
- accepted-root requirements;
- protocol-state requirements;
- uniqueness and replay-prevention requirements;
- domain-separation requirements;
- temporal requirements;
- other conditions derived from the published protocol generation.

Protocol validity is protocol-relative and context-bounded.

It does not establish application, factual, legal, social, or institutional
truth.

### 25.6 RF-18 — Evidence, Protocol Validity, and Non-Proof Validity Conditions

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-VALID-001 | RF-18 | MUST | Every proof-verification result used during Protocol Action Evaluation | The result MUST remain bounded evidence concerning exactly the proof relation and public-input relationship evaluated by that verification occurrence. | S18, S24, S25 |
| PE-VALID-002 | RF-18 | MUST | Every proof-verification result contributing to complete Evaluation | The result MUST contribute to the later Protocol Action Evaluation without replacing the Action, applicable rule set, Evaluation, or Determination. | S02, S18, S24, S25 |
| PE-VALID-003 | RF-18 | MUST | Every Protocol Action validity determination basis | Complete Protocol Action validity MUST mean satisfaction of every applicable protocol rule within one bounded evaluation context. | S18, S24, S25 |
| PE-VALID-004 | RF-18 | MUST NOT | Every successful proof-verification result | Successful proof verification MUST NOT be represented as complete Protocol Action validity unless proof verification constitutes the complete applicable protocol-rule set for that action and context. | S02, S18, S24, S25 |
| PE-VALID-005 | RF-18 | MUST | Every Protocol Action whose applicable rule set includes non-proof validity conditions | Every applicable non-proof validity condition MUST remain represented and evaluated as part of the complete applicable protocol-rule set. | S18, S24, S25 |
| PE-VALID-006 | RF-18 | MUST | Every non-proof protocol-validity condition | A non-proof validity condition MUST derive from the identified published protocol generation and MUST possess a bounded applicability rule for the affected action and context. | S02, S24, S25 |
| PE-VALID-007 | RF-18 | MUST | Every current-generation Protocol Action Evaluation basis | The applicable validity basis MUST account for required action shape, public-input coherence, accepted-root status, nullifier uniqueness, replay prevention, domain separation, protocol-state requirements, and every other applicable generation-derived condition. | S01, S20, S24, S25 |
| PE-VALID-008 | RF-18 | MUST | Every required proof-invalid verification result | A required proof-invalid result MUST prevent the Protocol Action from satisfying the corresponding applicable proof requirement. | S24, S25 |
| PE-VALID-009 | RF-18 | MUST | Every interpretation of protocol validity | Protocol validity MUST remain action-specific, applicable-rule-relative, and bounded to the identified evaluation context. | S24, S25 |
| PE-VALID-010 | RF-18 | MUST NOT | Every proof-valid or protocol-valid classification | Proof validity or protocol validity MUST NOT independently become Protocol Action acceptance, rejection, transition authorization, transition execution, or commitment. | S02, S18, S24, S25 |
| PE-VALID-011 | RF-18 | MUST NOT | Every protocol-valid Protocol Action and interpretation of it | Protocol validity MUST NOT be represented as application truth, external factual truth, legal truth, social truth, institutional recognition, or a Protocol Claim. | S18, S24, S25, S28 |
| PE-VALID-012 | RF-18 | MUST | Every evidence, validity, failure, and diagnostic surface | The surface MUST preserve SF-03 and SF-04 identity separation, Private Actor non-disclosure, role-bounded public values, neutral naming, and compositional unlinkability. | S01, S18, S20, S24, S25 |

## 26. SF-07 — Protocol Actions and Applicable Rules

SF-07 defines the complete Protocol Action occurrence and applicable-rule
boundary required before authoritative Evaluation.

It does not define the complete Evaluation process, Determination, acceptance,
rejection, state transition, commitment, application request, application
response, or application adapter.

### 26.1 Protocol Action Definition

A Privacy Engine Protocol Action is one bounded occurrence of protocol-defined
behavior presented through an implementation for Evaluation under the
applicable rules of one published Privacy Engine protocol generation.

Let:

- `P` be one published protocol generation;
- `I` be one implementation;
- `X` be one Private Actor;
- `O` be one Protocol Operation capability;
- `A` be one Protocol Action occurrence;
- `T` be the applicable action type;
- `PI` be the declared public-input set;
- `R` be the complete applicable protocol-rule set;
- `C` be the bounded evaluation context;
- `Z` be a proof supporting the action where required.

The action-side relationships are:

> occurrenceOf(A, T)

> governedBy(A, P)

> performedThrough(A, I)

> performs(X, A)

> carries(A, PI)

> supports(Z, A)

> applicableRules(A, R)

> evaluatedIn(A, C)

The Action is distinct from its Private Actor, type, operation capability,
proof, public inputs, implementation, Evaluation, Determination, Published
Result, Protocol State Transition, and application-defined meaning.

### 26.2 Action Attempt, Admission, and Occurrence Identity

An action attempt is an effort to construct, present, submit, or obtain
evaluation of a candidate Protocol Action.

An attempt does not automatically constitute an evaluated Protocol Action.

A candidate enters the Protocol Action model when it is admitted to the
applicable authoritative evaluation boundary:

> admittedForEvaluation(candidateA)
> ->
> instantiates(candidateA, A)

Transport retries, relay attempts, submission retries, and internal processing
attempts do not silently widen or replace the logical action occurrence.

The applicable specification determines whether repeated authoritative
presentations concern one occurrence or distinct occurrences.

That determination cannot infer, merge, or reconstruct Private Actor identity.

### 26.3 RF-20 — Protocol Actions

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-ACTION-001 | RF-20 | MUST | Every Privacy Engine Protocol Action | A Protocol Action MUST be one bounded occurrence of protocol-defined behavior presented through an implementation for Evaluation under the applicable rules of one identified published protocol generation. | S02, S18, S24 |
| PE-ACTION-002 | RF-20 | MUST | Every Protocol Action occurrence | Each Protocol Action MUST possess one stable occurrence identity distinct from every other Protocol Action occurrence. | S18, S24 |
| PE-ACTION-003 | RF-20 | MUST | Every Protocol Action | The Action MUST be bounded to one occurrence, one action type, one declared public-input set, one applicable protocol-rule set, and one bounded evaluation context. | S18, S24 |
| PE-ACTION-004 | RF-20 | MUST | Every Protocol Action occurrence | The occurrence MUST identify its protocol-defined action type and governing published protocol generation. | S24 |
| PE-ACTION-005 | RF-20 | MUST | Every Protocol Operation, action type, and Protocol Action occurrence | Published capability, action-type classification, and individual action occurrence MUST remain distinct. | S02, S18, S23, S24 |
| PE-ACTION-006 | RF-20 | MUST | Every effort to construct, present, submit, or obtain evaluation of a candidate Protocol Action | An action attempt MUST remain distinct from a Protocol Action occurrence admitted to the authoritative evaluation boundary. | S18, S24 |
| PE-ACTION-007 | RF-20 | MUST | Every candidate admitted to authoritative Protocol Action Evaluation | Admission to the applicable authoritative evaluation boundary MUST instantiate one bounded Protocol Action occurrence without identifying its Private Actor. | S18, S24 |
| PE-ACTION-008 | RF-20 | MUST NOT | Every transport retry, relay attempt, submission retry, implementation retry, and internal processing attempt | An operational retry or attempt MUST NOT silently widen, replace, merge, or create the identity of the logical Protocol Action occurrence. | S18, S20, S24 |
| PE-ACTION-009 | RF-20 | MUST | Every protocol rule governing repeated authoritative presentations | The rule MUST determine whether the presentations concern one action occurrence or distinct action occurrences without inferring or merging Private Actor identity. | S18, S24 |
| PE-ACTION-010 | RF-20 | MUST | Every Protocol Action | The Action MUST carry exactly the declared public-input set required for its action type while remaining distinct from those public inputs. | S20, S24 |
| PE-ACTION-011 | RF-20 | MUST | Every proof-supported Protocol Action | The Action and its supporting proof MUST remain distinct, and the proof MUST contribute only its bounded evidence role. | S18, S24, S25 |
| PE-ACTION-012 | RF-20 | MUST | Every Protocol Action performed through an implementation | The Action occurrence MUST remain distinct from the implementation, deployment, transaction, transport, storage, and runtime machinery through which it is presented. | S18, S20, S24 |
| PE-ACTION-013 | RF-20 | MUST | Every relationship between a Private Actor and Protocol Action | The Private Actor and public Protocol Action MUST remain distinct according to `Private actors, public actions`. | S01, S18, S19, S24 |
| PE-ACTION-014 | RF-20 | MUST NOT | Every Protocol Action identifier and representation | An action identifier or representation MUST NOT identify, encode, imply, reconstruct, or become a reusable identifier for the Private Actor. | S01, S18, S20, S24 |
| PE-ACTION-015 | RF-20 | MUST NOT | Every application interpretation of a Protocol Action | Application-defined meaning, terminology, workflow, metadata, or truth MUST NOT become Protocol Action identity or protocol validity. | S18, S24, S28, S29 |
| PE-ACTION-016 | RF-20 | MUST | Every relationship from a Protocol Action to a possible Published Result, Determination, or Protocol State Transition | The Protocol Action MUST remain distinct from every interface result, downstream Determination, and possible state-transition consequence. | S02, S18, S24, S27, S32 |
| PE-ACTION-017 | RF-20 | MUST NOT | Every Protocol Action interpretation and extension | A Protocol Action MUST NOT be represented as a Protocol Claim or used to introduce another first-class subject without satisfying the established closed-ontology test. | S17, S18, S24, S28 |

### 26.4 Applicable Protocol Rules and Action Validity

Every Protocol Action is governed by one complete bounded applicable
protocol-rule set.

The rules derive through the established authority direction:

> derives(Spec, P)

> derives(Profile, Spec)

> implements(I, Profile)

> applicableRules(A, R)

> derivesRules(R, P)

Applicability may depend on:

- the Protocol Action type;
- the applicable implementation profile;
- protocol-relevant current state;
- the bounded evaluation context.

Implementation policy may determine whether an implementation offers,
transports, or locally prepares an action.

Implementation policy does not silently become protocol validity.

The complete validity invariant is:

> protocolValid(A, C)
> iff
> satisfiesAll(A, R, C)

The applicable rule set includes every proof and non-proof requirement governing
the Action in that context.

SF-07 establishes the Action and complete applicable-rule boundary.

SF-08 remains the authoritative home for applying that complete rule set through
Evaluation and producing the Determination.

### 26.5 RF-21 — Applicable Protocol-Rule Sets and Action Validity

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-RULE-001 | RF-21 | MUST | Every Protocol Action | The Action MUST be governed by exactly one complete and bounded applicable protocol-rule set for its identified action type and evaluation context. | S02, S18, S24, S33 |
| PE-RULE-002 | RF-21 | MUST | Every rule included in an applicable Protocol Action rule set | Each applicable rule MUST derive from the identified published protocol generation through the established Protocol Specification and implementation-profile direction. | S02, S18, S24, S33 |
| PE-RULE-003 | RF-21 | MUST | Every determination of Protocol Action rule applicability | Applicability MUST be determined only from protocol-defined action type, applicable implementation profile, protocol-relevant state, and bounded evaluation-context conditions. | S24, S33 |
| PE-RULE-004 | RF-21 | MUST | Every Protocol Action admitted for authoritative Evaluation | The complete applicable protocol-rule set MUST be established before authoritative Evaluation begins. | S18, S24, S25 |
| PE-RULE-005 | RF-21 | MUST NOT | Every implementation, application, transport, deployment, and operational policy | Implementation convenience, application policy, transport behavior, deployment state, or operational discretion MUST NOT silently create, remove, weaken, strengthen, or reinterpret a protocol-validity rule. | S18, S24, S33 |
| PE-RULE-006 | RF-21 | MUST | Every Protocol Action validity classification basis | Protocol Action validity MUST mean satisfaction of every applicable protocol rule within the identified bounded evaluation context. | S18, S24, S25 |
| PE-RULE-007 | RF-21 | MUST | Every applicable Protocol Action rule set | The rule set MUST include every applicable proof requirement, public-input requirement, non-proof validity condition, uniqueness condition, state-relative condition, and action-type constraint. | S01, S18, S24, S25, S33 |
| PE-RULE-008 | RF-21 | MUST | Every protocol-validity interpretation | Protocol validity MUST remain action-specific and bounded to the identified evaluation context. | S18, S24, S25 |
| PE-RULE-013 | RF-21 | MUST NOT | Every comparison of Protocol Action validity across materially different evaluation contexts | Validity in one evaluation context MUST NOT be inferred as validity in a materially different evaluation context. | S18, S24, S25 |
| PE-RULE-009 | RF-21 | MUST NOT | Every application interpretation and external claim associated with a Protocol Action | Application meaning, factual meaning, legal meaning, social meaning, or institutional meaning MUST NOT replace or redefine the applicable protocol-rule set or protocol validity. | S18, S24, S25, S28, S29 |
| PE-RULE-010 | RF-21 | MUST | Every action-local uniqueness or authorization rule | The rule MUST preserve the declared action scope without creating reusable participant identity, actor disclosure, or unauthorized cross-action linkage. | S01, S18, S20, S24 |
| PE-RULE-011 | RF-21 | MUST NOT | Every implementation, transaction, transport, retry, storage, and diagnostic identifier | An operational identifier MUST NOT determine, replace, merge, or redefine Protocol Action identity, rule applicability, or protocol validity. | S18, S20, S24 |
| PE-RULE-012 | RF-21 | MUST | Every Protocol Action prepared for complete Evaluation | The Action, complete applicable rule set, and bounded evaluation context MUST be available as distinct preserved inputs to SF-08 without pre-emptively defining Evaluation, Determination, acceptance, or rejection. | S02, S18, S24, S25 |

## 27. Supporting Relationships and Deferred Operational Semantics

SF-03 and SF-04 establish the terminology, identity, and privacy requirements
preserved by SF-05–SF-07.

SF-05 establishes:

- bounded Interface Contract meaning;
- concrete syntactic realization;
- stable Protocol Surfaces;
- Protocol Operation capability;
- and Published Result semantics.

SF-06 establishes:

- proofs and declared public inputs;
- proof verification;
- bounded proof evidence;
- complete protocol validity;
- and non-proof validity conditions.

SF-07 establishes:

- Protocol Action occurrence identity;
- action attempts and admission to Evaluation;
- applicable protocol-rule sets;
- and the complete action-validity boundary required before Evaluation.

The following authoritative homes remain deferred:

- Evaluation, Determination, acceptance, rejection, and accepted no-transition
  behavior: SF-08;
- protocol state, transition mappings, preconditions, transition occurrences,
  and authorization: SF-09;
- transition execution, commitment, atomicity, and state evolution: SF-10;
- history, public consequences, failure, staleness, and re-evaluation: SF-11;
- application requests, responses, adapters, runtime, and integration
  boundaries: SF-12;
- implementation, realization, compatibility, and migration: SF-13;
- implementation profiles and reference implementations: SF-14;
- conformance and certification: SF-15;
- protocol-semantic preservation and complete explicit exclusions: SF-16.

References to deferred subjects establish only the cross-section relationships
required to preserve current boundaries.

They do not relocate the deferred requirement families.

RF-14 remains assigned to SF-12.

RF-49 and RF-50 remain reserved to SF-16.

## 28. Current Composition Boundary

This cumulative document currently contains the authoritative normative homes
for:

- RF-01–RF-13;
- RF-15–RF-21.

The following section families remain deliberately uncomposed:

- SF-08 — Evaluation, Determination, acceptance, rejection, and accepted
  no-transition behavior;
- SF-09 — protocol state, transition semantics, preconditions, and
  authorization;
- SF-10 — transition execution, commitment, atomicity, and state evolution;
- SF-11 — history, public consequences, failure, staleness, and re-evaluation;
- SF-12 — application, adapter, runtime, and integration boundaries;
- SF-13 — implementation, realization, compatibility, and migration;
- SF-14 — implementation profiles and reference implementations;
- SF-15 — conformance and certification;
- SF-16 — semantic preservation and explicit exclusions.

Their absence is explicit and is not an implicit definition, permission,
prohibition, or completion.

This cumulative slice does not define:

- complete Protocol Action Evaluation;
- Protocol Action Determination;
- acceptance or rejection;
- accepted no-transition behavior;
- protocol state;
- Protocol Transition preconditions;
- Protocol State Transition authorization or cardinality;
- transition execution or commitment;
- protocol-state history;
- committed public protocol-state consequences;
- cross-stage failure classifications;
- staleness or re-evaluation;
- application request, response, or adapter behavior;
- runtime or integration responsibility;
- implementation or realization mechanics;
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

These are local composition-boundary statements.

They do not relocate or duplicate the authoritative homes reserved for later
requirement families.

The cumulative specification contains 252 stable normative requirements:

- 81 requirements preserved from SF-01 and SF-02;
- 71 requirements preserved from SF-03 and SF-04;
- 100 requirements composed through SF-05, SF-06, and SF-07.

The document remains incomplete until SF-08–SF-16 have been composed and the
complete specification has passed final consolidation review.

## 29. Cumulative Traceability

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
| S30 | `PRIVACY_ENGINE_CONCRETE_INTERFACE_SPECIFICATION_MODEL_V1.md` |
| S31 | `PRIVACY_ENGINE_INTERFACE_CONTRACT_MODEL_V1.md` |
| S32 | `PRIVACY_ENGINE_PUBLISHED_RESULT_MODEL_V1.md` |
| S33 | `PRIVACY_ENGINE_PROTOCOL_ENFORCEMENT_MODEL_V1.md` |

Source references record semantic provenance and composition support.

They do not create independent normative authority.

The authoritative normative home of each requirement is the composed section
family containing its requirement family.

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

Traceability organizes established semantics.

It does not redefine them.

## 30. Conclusion

SF-01 through SF-07 now establish the cumulative normative path from protocol
authority and publication through terminology, privacy, interfaces, proof
evidence, validity, and one bounded Protocol Action ready for Evaluation.

SF-05 establishes:

- Interface Contract identity and bounded semantic meaning;
- Concrete Interface Specification identity and syntactic realization;
- semantic equivalence across permitted representations;
- stable Protocol Surfaces;
- Protocol Operation as published bounded capability;
- Protocol Operation type versus Protocol Action occurrence;
- Published Result identity and semantic preservation;
- Published Result versus representation;
- Published Result versus Determination;
- and Published Result versus committed public protocol-state consequence.

SF-06 establishes:

- proof identity and proof representation;
- the declared proof relation;
- public and private input separation;
- the locked current public-input order;
- proof-to-public-input coherence;
- proof artifact integrity;
- bounded proof verification;
- proof-valid, proof-invalid, and verification-failure separation;
- proof evidence;
- proof validity versus complete protocol validity;
- non-proof validity conditions;
- and protocol validity versus application or external truth.

SF-07 establishes:

- Protocol Action as one bounded first-class occurrence;
- action identity and action boundedness;
- action type versus occurrence;
- action attempt versus admitted occurrence;
- retry and transport-attempt separation;
- declared public inputs;
- applicable protocol-rule completeness;
- context-bounded Protocol Action validity;
- Protocol Action versus Private Actor;
- action identity versus operational identity;
- application meaning versus protocol validity;
- and the complete Action-plus-rules boundary required before SF-08 Evaluation.

The implementation-facing path is:

> published Interface Contract
> -> permitted concrete representation
> -> published Protocol Operation capability
> -> proof and declared public inputs
> -> bounded proof-verification evidence
> -> complete applicable validity conditions
> -> one identified Protocol Action ready for Evaluation

Protocol Operation remains a capability type.

Protocol Action remains one identified occurrence.

Proof verification contributes bounded evidence.

It does not independently establish complete protocol validity, acceptance, or
commitment.

Published Result remains an interface-level semantic result.

It does not become Determination, an Evaluation Outcome object, or a committed
public protocol-state consequence.

Private Actor remains distinct from proofs, public inputs, Protocol Action
identity, interfaces, results, implementations, applications, deployments,
transports, diagnostics, and observability surfaces.

No reusable participant identity, cross-action identity mechanism, Protocol
Claim, Evaluation Outcome object, or other new first-class subject is
introduced.

The 152 requirements established through SF-01–SF-04 remain unchanged.

SF-08–SF-16 remain deliberately deferred.

The cumulative specification remains incomplete pending those sections and the
final consolidation review.

Protocol authority always remains with the published Privacy Engine protocol generation.
