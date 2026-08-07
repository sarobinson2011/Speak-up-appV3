# Privacy Engine Protocol Specification V1

STATE.md remains canonical.

## 1. Specification Status

This document is the cumulative developer-facing Privacy Engine Protocol
Specification.

Current composition status:

- SF-01 — Authority, Scope, and Normative Interpretation: composed;
- SF-02 — Protocol Generation, Publication, Versioning, and Lineage: composed;
- SF-03–SF-16: not yet composed.

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
- SF-02 — Protocol Generation, Publication, Versioning, and Lineage.

These sections authoritatively contain:

- RF-01 — Specification identity, derivation, completeness, and authority;
- RF-02 — Protocol definition, scope, and invariant ownership;
- RF-03 — Protocol generation, publication, and Published Protocol;
- RF-04 — Succession, lineage, versioning, deprecation, and migration;
- RF-05 — Normative language, interpretation, applicability, and strength.

The current document does not define the later operational, cryptographic,
state-transition, application, implementation-profile, conformance, or
certification requirements assigned to SF-03–SF-16.

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

## 22. Current Composition Boundary

This cumulative document currently contains the authoritative normative homes
for RF-01–RF-05 only.

The following section families remain deliberately uncomposed:

- SF-03 — terminology and subject relationships;
- SF-04 — identity and privacy;
- SF-05 — interfaces and published results;
- SF-06 — proof and public-input semantics;
- SF-07 — validity and Protocol Actions;
- SF-08 — Evaluation, Determination, acceptance, and rejection;
- SF-09 — protocol state;
- SF-10 — transitions and commitment;
- SF-11 — history and failure;
- SF-12 — application boundaries;
- SF-13 — implementation;
- SF-14 — implementation profiles and reference implementations;
- SF-15 — conformance and certification;
- SF-16 — semantic preservation and exclusions.

Their absence is explicit and must not be interpreted as implicit definition,
permission, prohibition, or completion.

This slice does not define:

- privacy subjects or privacy semantics;
- proofs, proof systems, or public inputs;
- Protocol Actions;
- Evaluation or Determination;
- acceptance or rejection;
- Protocol State Transition occurrences;
- application-specific meaning;
- runtime execution;
- blockchain consensus;
- transaction formats;
- transport;
- relay mechanics;
- database or storage mechanics;
- implementation profiles;
- reference implementations;
- conformance assessment;
- certification;
- RF-49 semantic-preservation requirements;
- or RF-50 final exclusion requirements.

These are local composition-boundary statements. They do not relocate or
duplicate the authoritative homes reserved for later requirement families.

Privacy-language discipline remains mandatory throughout composition. This
document introduces no actor identity, reusable participant identity,
cross-action linkage, identity-bearing diagnostic, or runtime correlation
identifier.

## 23. Engineering[144] Traceability

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

Source references record semantic provenance and composition support.

They do not create independent normative authority.

The authoritative normative home of each Engineering[144] requirement is the
SF-01 or SF-02 section in which that requirement appears.

The traceability direction is:

> established formal source
> -> normative requirement family
> -> one authoritative specification destination
> -> stable normative requirement

The composition invariants are:

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

## 24. Conclusion

SF-01 and SF-02 establish the normative foundation of the cumulative Privacy
Engine Protocol Specification.

They define:

- specification identity, derivation, status, scope, and completeness;
- normative language, applicability, identifiers, and traceability;
- the Privacy Engine Protocol and its invariant ownership;
- Protocol Generation identity and completeness;
- Protocol Publication;
- Published Protocol identity and immutability;
- Protocol Succession;
- Protocol Lineage;
- versioning and semantic change;
- compatible and breaking evolution;
- deprecation and migration;
- coexistence and retirement;
- and downstream generation-reference requirements.

Protocol, Protocol Generation, Protocol Publication, Published Protocol,
Protocol Succession, and Protocol Lineage remain distinct.

The Protocol Specification remains derived, portable, implementation-facing,
and non-authoritative.

Protocol authority always remains with the published Privacy Engine protocol generation.

The cumulative Protocol Specification is ready to receive SF-03 and SF-04
without reopening the ontology or redefining the requirements composed here.
