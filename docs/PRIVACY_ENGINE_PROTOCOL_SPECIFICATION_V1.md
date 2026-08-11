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
- SF-08 — Evaluation, Determination, Acceptance, and Rejection: composed;
- SF-09 — Protocol State, Transition Semantics, Preconditions, and Authorization: composed;
- SF-10 — Transition Execution, Commitment, Atomicity, and State Evolution: composed;
- SF-11 — History, Public Consequences, Failure, Staleness, and Re-evaluation: composed;
- SF-12 — Application, Adapter, Runtime, and Integration Boundaries: composed;
- SF-13 — Implementation, Realization, Compatibility, and Migration: composed;
- SF-14 — Implementation Profiles and Reference Implementations: composed;
- SF-15 — Conformance and Certification: composed;
- SF-16 — Protocol-Semantic Preservation and Explicit Exclusions: composed.

The requirements in the composed sections are normative within their declared
scope.

All sixteen planned section families and all fifty requirement families
now possess authoritative normative homes.

Engineering[151] completed the final consolidation review recorded in
`docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_CONSOLIDATION_REVIEW_V1.md`.

Its determination was `rejected pending identified correction`.

Engineering[152] applied the bounded corrections recorded in
`docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_CONSOLIDATION_CORRECTIONS_V1.md`.

Engineering[153] completed the independent consolidation re-review recorded in
`docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_CONSOLIDATION_REREVIEW_V1.md`.

Engineering[153] confirmed F-01, F-02, F-03, and every other substantive
consolidation category, but identified the blocking informative-status
contradiction F-04. Its determination was `rejected pending identified correction`.

Engineering[154] applied the bounded F-04 informative-status correction recorded
in `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_STATUS_CONSISTENCY_CORRECTION_V1.md`.

Engineering[155] completed the final independent consolidation re-review recorded
in
`docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_FINAL_CONSOLIDATION_REREVIEW_V1.md`.

Engineering[155] independently confirmed that F-04 is resolved, every
Engineering[153] passing result remains preserved, and no additional blocking or
non-blocking defect exists. Its determination is `accepted and publication-ready`.

The specification remains composition-complete and is accepted and
publication-ready.

The specification remains unpublished. Publication requires a separate explicit act.

The current codebase remains unassessed and uncertified.

The current composition boundary is defined in Section 37.

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
- SF-07 — Protocol Actions and Applicable Rules;
- SF-08 — Evaluation, Determination, Acceptance, and Rejection;
- SF-09 — Protocol State, Transition Semantics, Preconditions, and Authorization;
- SF-10 — Transition Execution, Commitment, Atomicity, and State Evolution;
- SF-11 — History, Public Consequences, Failure, Staleness, and Re-evaluation;
- SF-12 — Application, Adapter, Runtime, and Integration Boundaries;
- SF-13 — Implementation, Realization, Compatibility, and Migration;
- SF-14 — Implementation Profiles and Reference Implementations;
- SF-15 — Conformance and Certification;
- SF-16 — Protocol-Semantic Preservation and Explicit Exclusions.

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
- RF-21 — Applicable protocol-rule sets and action validity;
- RF-22 — Protocol Action Evaluation;
- RF-23 — Protocol Action Determination;
- RF-24 — Acceptance and rejection;
- RF-25 — Accepted no-transition behavior;
- RF-26 — Published transition mappings, preconditions, and eligibility;
- RF-27 — Protocol State Transition occurrence identity and lifecycle;
- RF-28 — Transition authorization and cardinality;
- RF-29 — Transition execution and preservation;
- RF-30 — Transition commitment, completeness, and atomicity;
- RF-31 — Protocol state, successor state, and state evolution;
- RF-32 — Protocol-state history;
- RF-33 — Public protocol-state consequences;
- RF-34 — Failure classifications and failure separation;
- RF-35 — Stale authorization and re-evaluation;
- RF-14 — Application requests, responses, and adapters;
- RF-36 — Application and adapter authority boundaries;
- RF-37 — Runtime, enforcement, and execution responsibility;
- RF-38 — Implementation identity and implementation obligations;
- RF-39 — Protocol realization;
- RF-40 — Prohibited implementation, runtime, application, and assessment authority;
- RF-41 — Compatibility targets, surfaces, statements, profiles, declarations, and assessment;
- RF-42 — Implementation profiles;
- RF-43 — Reference implementations;
- RF-44 — Published conformance requirements and requirement sets;
- RF-45 — Conformance artifacts, evidence, and packages;
- RF-46 — Conformance claims, assessments, and determinations;
- RF-47 — Certification bases, decisions, and statuses;
- RF-48 — Certification recognition, scope, and authority;
- RF-49 — Protocol-semantic preservation;
- RF-50 — Explicit protocol exclusions and prohibited interpretations.

Every RF-01–RF-50 family now possesses one authoritative normative home.

The specification's current acceptance and publication status is declared in Section 1.

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
| PE-APPREP-* | RF-14 | SF-12 |
| PE-MEM-* | RF-15 | SF-04 |
| PE-PROOF-* | RF-16 | SF-06 |
| PE-VERIFY-* | RF-17 | SF-06 |
| PE-VALID-* | RF-18 | SF-06 |
| PE-UNIQ-* | RF-19 | SF-04 |
| PE-ACTION-* | RF-20 | SF-07 |
| PE-RULE-* | RF-21 | SF-07 |
| PE-EVAL-* | RF-22 | SF-08 |
| PE-DETERM-* | RF-23 | SF-08 |
| PE-CLASS-* | RF-24 | SF-08 |
| PE-NOTRANS-* | RF-25 | SF-08 |
| PE-TRANSMAP-* | RF-26 | SF-09 |
| PE-TRANSOCC-* | RF-27 | SF-09 |
| PE-TRANSAUTH-* | RF-28 | SF-09 |
| PE-TRANSEXEC-* | RF-29 | SF-10 |
| PE-COMMIT-* | RF-30 | SF-10 |
| PE-STATE-* | RF-31 | SF-10 |
| PE-STATEHIST-* | RF-32 | SF-11 |
| PE-STATECONSEQ-* | RF-33 | SF-11 |
| PE-FAIL-* | RF-34 | SF-11 |
| PE-STALEAUTH-* | RF-35 | SF-11 |
| PE-APPAUTH-* | RF-36 | SF-12 |
| PE-RUNTIME-* | RF-37 | SF-12 |
| PE-IMPL-* | RF-38 | SF-13 |
| PE-REALIZE-* | RF-39 | SF-13 |
| PE-DOWNAUTH-* | RF-40 | SF-13 |
| PE-COMPAT-* | RF-41 | SF-13 |
| PE-PROFILE-* | RF-42 | SF-14 |
| PE-REFIMPL-* | RF-43 | SF-14 |
| PE-CONFREQ-* | RF-44 | SF-15 |
| PE-CONFEVID-* | RF-45 | SF-15 |
| PE-CONFORM-* | RF-46 | SF-15 |
| PE-CERTDET-* | RF-47 | SF-15 |
| PE-CERT-* | RF-48 | SF-15 |
| PE-SEMPRES-* | RF-49 | SF-16 |
| PE-EXCLUDE-* | RF-50 | SF-16 |

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
| PE-SPEC-009 | RF-01 | MUST | Every implementation profile | The Protocol Specification MUST establish the downstream derivation rule requiring the implementation profile to identify the Protocol Specification and published Protocol Generation from which its applicable obligations derive. | S08, S10 |
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
| PE-SURF-007 | RF-13 | MUST | Every Protocol Operation and associated Protocol Action | The exposed Protocol Operation and associated Protocol Action representation MUST preserve the RF-07 distinction between the Protocol Operation capability type and each Protocol Action occurrence classified by that capability. | S02, S18, S23, S24 |
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
| PE-ACTION-013 | RF-20 | MUST | Every relationship between a Private Actor and Protocol Action | Protocol Action representation, processing, and Evaluation presentation MUST preserve the RF-09 Private Actor and public Protocol Action separation invariant throughout the Action lifecycle. | S01, S18, S19, S24 |
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
| PE-RULE-006 | RF-21 | MUST | Every Protocol Action validity classification basis | The validity-classification basis MUST apply the complete RF-18 definition of Protocol Action validity through the complete applicable protocol-rule set within the identified bounded evaluation context without replacing or redefining that definition. | S18, S24, S25 |
| PE-RULE-007 | RF-21 | MUST | Every applicable Protocol Action rule set | The rule set MUST include every applicable proof requirement, public-input requirement, non-proof validity condition, uniqueness condition, state-relative condition, and action-type constraint. | S01, S18, S24, S25, S33 |
| PE-RULE-008 | RF-21 | MUST | Every protocol-validity interpretation | Protocol-rule interpretation and application MUST preserve the RF-18 action-specific, applicable-rule-relative, evaluation-context-bounded validity invariant without widening validity beyond the identified context. | S18, S24, S25 |
| PE-RULE-013 | RF-21 | MUST NOT | Every comparison of Protocol Action validity across materially different evaluation contexts | Validity in one evaluation context MUST NOT be inferred as validity in a materially different evaluation context. | S18, S24, S25 |
| PE-RULE-009 | RF-21 | MUST NOT | Every application interpretation and external claim associated with a Protocol Action | Application meaning, factual meaning, legal meaning, social meaning, or institutional meaning MUST NOT replace or redefine the applicable protocol-rule set or protocol validity. | S18, S24, S25, S28, S29 |
| PE-RULE-010 | RF-21 | MUST | Every action-local uniqueness or authorization rule | The rule MUST preserve the declared action scope without creating reusable participant identity, actor disclosure, or unauthorized cross-action linkage. | S01, S18, S20, S24 |
| PE-RULE-011 | RF-21 | MUST NOT | Every implementation, transaction, transport, retry, storage, and diagnostic identifier | An operational identifier MUST NOT determine, replace, merge, or redefine Protocol Action identity, rule applicability, or protocol validity. | S18, S20, S24 |
| PE-RULE-012 | RF-21 | MUST | Every Protocol Action prepared for complete Evaluation | The Action, complete applicable rule set, and bounded evaluation context MUST be available as distinct preserved inputs to SF-08 without pre-emptively defining Evaluation, Determination, acceptance, or rejection. | S02, S18, S24, S25 |

## 27. SF-08 — Evaluation, Determination, Acceptance, and Rejection

SF-08 defines the complete implementation-facing Evaluation and Determination
boundary for one identified Protocol Action.

Let:

- `A` be one Protocol Action;
- `E` be one Protocol Action Evaluation;
- `D` be one Protocol Action Determination;
- `R` be the complete applicable protocol-rule set;
- `C` be the bounded evaluation context;
- `V` be one proof-verification occurrence;
- `Z` be one proof;
- `PI` be the declared public inputs;
- `X` be a Private Actor;
- `U` be a possible Protocol State Transition.

The occurrence inventory remains:

> A != E

> E != D

> D != U

Evaluation is the process.

Determination is the result of completed Evaluation.

They possess distinct identities and meanings while remaining two bounded
aspects of one architectural model.

No Evaluation Outcome object, acceptance object, or rejection object is
introduced.

### 27.1 Protocol Action Evaluation

A Privacy Engine Protocol Action Evaluation is one identified, bounded
occurrence that evaluates one identified Protocol Action against the complete
applicable protocol-rule set within one bounded evaluation context.

The core relationships are:

> evaluates(E, A)

> applies(E, R)

> evaluatedIn(E, C)

Evaluation may begin only when `A`, `R`, and `C` have been established.

> begins(E, A, R, C)
> ->
> fixedScope(E, A, R, C)

Once Evaluation begins, the Action, rule set, and context are fixed.

An implementation must not silently substitute, merge, widen, narrow, repair,
or infer a replacement Action, rule set, or context.

Where the required Action, complete applicable rule set, or bounded context
cannot be established before Evaluation begins, the condition is
pre-evaluation failure.

Pre-evaluation failure does not create an authoritative Evaluation or
Determination.

Evaluation may contain bounded components for:

- action-type validity;
- declared public-input validity;
- proof-verification requirements;
- proof-to-public-input coherence;
- non-proof validity conditions;
- protocol-state requirements;
- accepted-root requirements;
- uniqueness requirements;
- domain-separation requirements;
- temporal requirements;
- and every other applicable protocol rule.

Each component evaluates only its assigned requirement or explicitly assigned
subset of `R`.

> componentOf(K, E)

> evaluatesAssignedRequirements(K, RK)

> RK subsetOf R

A component does not become complete Evaluation unless its assigned rule set is
the complete applicable rule set.

Proof verification is one possible bounded component:

> verifies(V, Z, PI)

> contributesTo(V, E)

Proof verification remains evidence.

It does not become Evaluation or directly produce Determination, acceptance, or
rejection.

Evaluation completeness is:

> complete(E)
> iff
> evaluatesAll(E, R, A, C)

Completeness requires:

- every applicable rule was evaluated;
- every required component was performed;
- every component remained within its assignment;
- all required component results were available;
- the results were coherently combined;
- and no applicable rule was omitted, substituted, weakened, repaired, or
  inferred.

A partial or incomplete Evaluation cannot produce a Determination.

Evaluation failure occurs when Evaluation begins with fixed `A`, `R`, and `C`
but cannot complete.

> evaluationFailure(E)
> ->
> not existsProtocolActionDetermination(D, E)

Evaluation failure is neither acceptance nor rejection.

### 27.2 RF-22 — Protocol Action Evaluation

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-EVAL-001 | RF-22 | MUST | Every Protocol Action Evaluation | A Protocol Action Evaluation MUST possess one stable occurrence identity identifying exactly one bounded Evaluation occurrence. | S01, S02, S18, S25 |
| PE-EVAL-002 | RF-22 | MUST | Every Protocol Action Evaluation | An Evaluation MUST evaluate exactly one identified Protocol Action. | S18, S24, S25 |
| PE-EVAL-003 | RF-22 | MUST | Every Protocol Action Evaluation | An Evaluation MUST apply exactly one complete applicable protocol-rule set established for the evaluated Action. | S18, S24, S25, S33 |
| PE-EVAL-004 | RF-22 | MUST | Every Protocol Action Evaluation | An Evaluation MUST occur within exactly one bounded protocol-relevant evaluation context. | S18, S24, S25 |
| PE-EVAL-005 | RF-22 | MUST | Every candidate entering the authoritative Evaluation boundary | Authoritative Evaluation MUST begin only after the Action, complete applicable rule set, and bounded evaluation context have been established as distinct inputs. | S18, S24, S25 |
| PE-EVAL-006 | RF-22 | MUST | Every Protocol Action Evaluation after Evaluation begins | The Evaluation MUST preserve its identified Action, complete applicable rule set, and bounded evaluation context throughout the Evaluation. | S18, S25 |
| PE-EVAL-007 | RF-22 | MUST NOT | Every Protocol Action Evaluation after Evaluation begins | An Evaluation MUST NOT substitute, merge, widen, narrow, repair, or infer a replacement Action, rule set, or evaluation context. | S18, S25 |
| PE-EVAL-008 | RF-22 | MUST | Every complete Protocol Action Evaluation | A complete Evaluation MUST evaluate every applicable protocol rule governing the identified Action in the identified context. | S18, S24, S25 |
| PE-EVAL-009 | RF-22 | MUST | Every Evaluation component | An Evaluation component MUST possess an explicit assignment to one applicable requirement or one bounded subset of the complete applicable rule set. | S18, S25, S33 |
| PE-EVAL-010 | RF-22 | MUST | Every Evaluation component | An Evaluation component MUST evaluate only the applicable requirement or bounded subset assigned to that component. | S18, S25, S33 |
| PE-EVAL-011 | RF-22 | MUST NOT | Every Evaluation component whose assigned rules are not the complete applicable rule set | A bounded component MUST NOT be represented as complete Protocol Action Evaluation. | S18, S25, S33 |
| PE-EVAL-012 | RF-22 | MUST | Every Evaluation containing multiple required components | The Evaluation MUST coherently combine every required component result before determining whether the Evaluation is complete. | S18, S25 |
| PE-EVAL-013 | RF-22 | MUST | Every proof-verification occurrence contributing to Evaluation | Proof verification MUST remain bounded evidence concerning the declared proof relation and declared public inputs. | S18, S25 |
| PE-EVAL-014 | RF-22 | MUST | Every relationship between proof verification and Protocol Action Evaluation | Proof verification MUST remain distinct from the complete Evaluation to which it contributes. | S02, S18, S25 |
| PE-EVAL-015 | RF-22 | MUST NOT | Every proof-verification result | A proof-verification result MUST NOT directly produce a Protocol Action Determination, acceptance classification, or rejection classification. | S02, S18, S25 |
| PE-EVAL-016 | RF-22 | MUST | Every Evaluation whose applicable rule set contains non-proof validity conditions | The Evaluation MUST evaluate every applicable non-proof validity condition independently of proof-verification success. | S18, S24, S25 |
| PE-EVAL-017 | RF-22 | MUST | Every Protocol Action Evaluation completeness classification | An Evaluation MUST be classified as complete exactly when it has evaluated every applicable rule for the identified Action within the identified context. | S18, S25 |
| PE-EVAL-018 | RF-22 | MUST NOT | Every partial or incomplete Protocol Action Evaluation | A partial or incomplete Evaluation MUST NOT produce a Determination, acceptance classification, or rejection classification. | S18, S25 |
| PE-EVAL-019 | RF-22 | MUST NOT | Every Evaluation failure and every pre-evaluation failure | Evaluation failure or pre-evaluation failure MUST NOT be represented as a completed Evaluation or as producing a Protocol Action Determination. | S18, S25 |
| PE-EVAL-020 | RF-22 | MUST NOT | Every Evaluation component, identifier, evidence record, representation, diagnostic, log, field, route, test, example, and observability surface | An Evaluation surface MUST NOT identify the Private Actor, extend evidence into actor identification, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | S01, S18, S20, S25 |

### 27.3 Protocol Action Determination

A Privacy Engine Protocol Action Determination is the identified and bounded
authoritative result of one completed Protocol Action Evaluation.

“Authoritative” means authoritative only within the Determination's bounded
classification role.

It does not assign protocol authority to `D`.

Every completed Evaluation produces exactly one Determination:

> complete(E)
> ->
> producesExactlyOne(E, D)

Every Determination derives from exactly one completed Evaluation:

> produces(E, D)
> ->
> complete(E)

> determinationOf(D, E)

The relationship is bidirectionally bounded:

> complete(E)
> <->
> producesExactlyOne(E, D)

A Determination identifies:

- exactly one completed Evaluation;
- exactly one evaluated Protocol Action;
- exactly one complete applicable protocol-rule set;
- exactly one bounded evaluation context;
- and exactly one acceptance or rejection classification.

The relationships are:

> determines(D, A)

> determinedUnder(D, R)

> determinedIn(D, C)

A Determination is distinct from:

- the Evaluation that produced it;
- a proof-verification result;
- a Published Result;
- an Evaluation Outcome object;
- a Protocol State Transition;
- a committed public protocol-state consequence;
- application truth;
- and protocol authority.

Equivalent correct Evaluations must produce equivalent Determinations where
the Action and applicable rules are the same and the contexts are equivalent:

> sameAction(A)
> and sameRules(R)
> and equivalentContext(C1, C2)
> and correct(E1)
> and correct(E2)
> and produces(E1, D1)
> and produces(E2, D2)
> ->
> equivalentDetermination(D1, D2)

Materially different contexts may produce different protocol-validity
classifications:

> not equivalentContext(C1, C2)
> and protocolValid(A, C1)
> =/=>
> protocolValid(A, C2)

Context dependence does not create implementation discretion.

### 27.4 RF-23 — Protocol Action Determination

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-DETERM-001 | RF-23 | MUST | Every Protocol Action Determination | A Protocol Action Determination MUST possess one stable result identity identifying exactly one bounded Determination. | S01, S02, S18, S25 |
| PE-DETERM-002 | RF-23 | MUST | Every relationship between a Protocol Action Evaluation and its Determination | The Evaluation process and resulting Determination MUST remain separately identified and semantically distinct. | S17, S18, S25 |
| PE-DETERM-003 | RF-23 | MUST | Every completed Protocol Action Evaluation | A completed Evaluation MUST produce exactly one Protocol Action Determination. | S18, S25 |
| PE-DETERM-004 | RF-23 | MUST | Every Protocol Action Determination | A Determination MUST derive from exactly one completed Protocol Action Evaluation. | S18, S25 |
| PE-DETERM-005 | RF-23 | MUST | Every Protocol Action Determination | A Determination MUST identify exactly one producing completed Evaluation, one evaluated Action, one complete applicable rule set, and one bounded evaluation context. | S18, S25 |
| PE-DETERM-006 | RF-23 | MUST | Every valid Protocol Action Determination | A valid Determination MUST contain and reference its RF-24 classification without defining an alternative classification model. | S18, S25 |
| PE-DETERM-007 | RF-23 | MUST NOT | Every incomplete or failed Protocol Action Evaluation | An incomplete or failed Evaluation MUST NOT be treated as possessing or producing a Protocol Action Determination. | S18, S25 |
| PE-DETERM-008 | RF-23 | MUST | Every Protocol Action Determination and proof-verification result | A Determination MUST remain distinct from every proof-verification occurrence and proof-verification result contributing to its Evaluation. | S02, S18, S25 |
| PE-DETERM-009 | RF-23 | MUST | Every Protocol Action Determination and Published Result | A Determination MUST remain distinct from every interface-level Published Result and its concrete representation. | S02, S18, S25, S32 |
| PE-DETERM-010 | RF-23 | MUST | Every Protocol Action Determination and possible Protocol State Transition | A Determination MUST remain distinct from transition identity, transition execution, commitment, and every committed public protocol-state consequence. | S18, S25, S27 |
| PE-DETERM-011 | RF-23 | MUST NOT | Every Determination identifier, representation, diagnostic, log, field, route, test, example, and observability surface | A Determination surface MUST NOT identify the Private Actor, become reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | S01, S18, S20, S25 |
| PE-DETERM-012 | RF-23 | MUST | Every pair of correct Evaluations of the same Action under the same applicable rules and equivalent contexts | The Evaluations MUST produce equivalent acceptance or rejection Determinations. | S18, S25 |
| PE-DETERM-013 | RF-23 | MUST | Every context-dependent Protocol Action Determination | The Determination MUST remain bounded to its identified evaluation context without converting material context differences into implementation discretion. | S18, S24, S25 |
| PE-DETERM-014 | RF-23 | MUST NOT | Every Protocol Action Determination | A Determination MUST NOT be represented as an Evaluation Outcome object or as an independently authoritative source of protocol semantics. | S02, S17, S18, S25 |

### 27.5 Acceptance and Rejection

Every valid Determination records exactly one mutually exclusive
classification:

> accepts(D, A)
> xor
> rejects(D, A)

Acceptance means completed Evaluation classified `A` as satisfying the complete
applicable protocol-rule set within `C`.

Rejection means completed Evaluation classified `A` as not satisfying the
complete applicable protocol-rule set within `C`.

The complete validity relation remains:

> protocolValid(A, C)
> iff
> satisfiesAll(A, R, C)

Correct acceptance is:

> correct(D, A, C)
> ->
> (accepts(D, A) iff protocolValid(A, C))

Correct rejection is:

> correct(D, A, C)
> ->
> (rejects(D, A) iff not protocolValid(A, C))

Acceptance and rejection are predicates of `D`.

They are not separately identified objects.

The following remain distinct:

- incomplete Evaluation;
- Evaluation failure;
- pre-evaluation failure;
- infrastructure failure;
- implementation error;
- proof-invalid evidence;
- rejection;
- accepted no-transition;
- transition failure.

A proof-invalid result may establish that one applicable proof requirement was
not satisfied.

It does not independently establish complete Protocol Action rejection until
the complete Evaluation has produced a rejecting Determination.

An erroneous Determination does not change protocol truth:

> incorrectAcceptance(D, A)
> =/=>
> protocolValid(A, C)

> incorrectRejection(D, A)
> =/=>
> not protocolValid(A, C)

Acceptance and rejection classify protocol validity only.

They do not classify application, factual, legal, social, or institutional
truth.

### 27.6 RF-24 — Acceptance and Rejection

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-CLASS-001 | RF-24 | MUST | Every valid Protocol Action Determination | A valid Determination MUST record exactly one mutually exclusive acceptance or rejection classification. | S18, S24, S25 |
| PE-CLASS-002 | RF-24 | MUST | Every correct accepting Determination | Acceptance MUST mean that completed Evaluation established satisfaction of every applicable protocol rule within the identified evaluation context. | S18, S24, S25 |
| PE-CLASS-003 | RF-24 | MUST | Every correct rejecting Determination | Rejection MUST mean that completed Evaluation established non-satisfaction of at least one applicable protocol rule within the identified evaluation context. | S18, S24, S25 |
| PE-CLASS-004 | RF-24 | MUST | Every correct Protocol Action Determination | The Determination MUST accept the Action exactly when the Action is protocol-valid within the identified evaluation context. | S18, S24, S25 |
| PE-CLASS-005 | RF-24 | MUST | Every correct Protocol Action Determination | The Determination MUST reject the Action exactly when the Action is not protocol-valid within the identified evaluation context. | S18, S24, S25 |
| PE-CLASS-006 | RF-24 | MUST NOT | Every incomplete Evaluation, Evaluation failure, and pre-evaluation failure | An incomplete Evaluation, Evaluation failure, or pre-evaluation failure MUST NOT be classified as acceptance or rejection. | S18, S25 |
| PE-CLASS-007 | RF-24 | MUST NOT | Every infrastructure, transport, deployment, storage, implementation, and observability failure | An operational or implementation failure MUST NOT be represented as protocol rejection. | S01, S18, S25 |
| PE-CLASS-008 | RF-24 | MUST NOT | Every proof-invalid result considered outside complete Protocol Action Evaluation | A proof-invalid result alone MUST NOT be represented as a complete rejecting Determination. | S02, S18, S25 |
| PE-CLASS-009 | RF-24 | MUST NOT | Every erroneous acceptance or rejection classification | An incorrect classification MUST NOT redefine the applicable rules, protocol validity, or protocol semantics. | S18, S25 |
| PE-CLASS-010 | RF-24 | MUST NOT | Every acceptance and rejection classification | Acceptance or rejection MUST NOT be represented as a separately identified acceptance object, rejection object, or Evaluation Outcome object. | S02, S17, S18, S25 |
| PE-CLASS-011 | RF-24 | MUST NOT | Every application or external interpretation of acceptance or rejection | Acceptance or rejection MUST NOT be treated as establishing application, factual, legal, social, or institutional truth. | S18, S24, S25 |
| PE-CLASS-012 | RF-24 | MUST NOT | Every acceptance or rejection representation, identifier, diagnostic, log, field, route, test, example, and observability surface | An acceptance or rejection classification MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | S01, S18, S20, S25 |

### 27.7 Accepted No-Transition Behavior

Acceptance does not necessarily authorize or require a Protocol State
Transition.

The applicable protocol rules determine whether an accepted Determination
authorizes zero, one, or multiple separately identified transitions.

SF-08 owns only the successful accepted no-transition terminal path.

SF-09 remains the authoritative home for transition authorization and
cardinality.

The no-transition path is:

> accepts(D, A)

> and noTransitionRequired(D)

> ->
> not existsAuthorizedTransition(U, D)

This path is complete and successful at the Determination boundary.

It is not:

- rejection;
- incomplete Evaluation;
- Evaluation failure;
- pre-transition failure;
- transition failure;
- incomplete execution;
- missing commitment;
- or implementation error.

Acceptance does not imply that a transition exists:

> accepts(D, A)
> =/=>
> exists(U)

Acceptance does not independently authorize a transition:

> accepts(D, A)
> =/=>
> authorizes(D, U)

Acceptance does not establish commitment:

> accepts(D, A)
> =/=>
> committed(U)

A rejected Determination does not authorize an accepted transition:

> rejects(D, A)
> ->
> not authorizesAcceptedTransition(D, U)

The absence of a transition on a protocol-defined no-transition path is the
required successful behavior.

An implementation must not invent a transition, report a missing commitment, or
reinterpret the path as failure.

### 27.8 RF-25 — Accepted No-Transition Behavior

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-NOTRANS-001 | RF-25 | MUST | Every accepted Protocol Action Determination | The applicable protocol rules MUST determine whether the accepted Determination requires no authorized Protocol State Transition. | S18, S25, S27 |
| PE-NOTRANS-002 | RF-25 | MUST | Every accepted Determination for which no transition is required | The Determination MUST terminate successfully without an authorized Protocol State Transition. | S18, S27 |
| PE-NOTRANS-003 | RF-25 | MUST | Every accepted no-transition path | The path MUST be treated as a complete successful terminal path at the Determination boundary. | S18, S27 |
| PE-NOTRANS-004 | RF-25 | MUST NOT | Every accepted no-transition path | An accepted no-transition path MUST NOT be represented as rejection, incomplete Evaluation, Evaluation failure, pre-transition failure, transition failure, incomplete execution, missing commitment, or implementation error. | S18, S27 |
| PE-NOTRANS-005 | RF-25 | MUST NOT | Every inference from Protocol Action acceptance | Acceptance alone MUST NOT be treated as establishing that a Protocol State Transition exists. | S18, S25, S27 |
| PE-NOTRANS-006 | RF-25 | MUST NOT | Every inference from Protocol Action acceptance | Acceptance alone MUST NOT be treated as transition authorization. | S18, S25, S27 |
| PE-NOTRANS-007 | RF-25 | MUST NOT | Every inference from Protocol Action acceptance | Acceptance alone MUST NOT be treated as transition execution or commitment. | S18, S25, S27 |
| PE-NOTRANS-008 | RF-25 | MUST NOT | Every rejecting Protocol Action Determination | A rejecting Determination MUST NOT authorize a transition that requires an accepted Determination. | S18, S25, S27 |
| PE-NOTRANS-009 | RF-25 | MUST NOT | Every implementation handling an accepted no-transition path | An implementation MUST NOT invent a transition, report missing commitment, or reinterpret the protocol-defined absence of a transition as failure. | S18, S27 |

### 27.9 Evaluation and Determination Privacy

SF-08 preserves:

> Private actors, public actions.

Evaluation determines whether the public Action satisfies the complete
applicable protocol-rule set.

It does not determine Private Actor identity.

The identifier non-implications are:

> identifiesEvaluation(id(E), E)
> =/=>
> identifiesActor(id(E), X)

> identifiesDetermination(id(D), D)
> =/=>
> identifiesActor(id(D), X)

Evidence remains bounded:

> establishesEvidence(Z, property)
> =/=>
> identifiesActor(Z, X)

No Evaluation component, evidence record, Determination identifier,
classification, diagnostic, log, field name, variable name, route name,
serialization field, storage key, test, example, comment, documentation
surface, or observability surface may:

- identify the Private Actor;
- infer wallet identity as actor identity;
- carry enrollment or admission provenance;
- introduce reusable participant identity;
- create cross-action linkage;
- extend proof meaning into actor identification;
- expose implementation, deployment, transport, retry, or topology information
  as actor identity;
- or create an actor-reconstruction bridge through composition.

SF-04 remains the authoritative home for privacy and forbidden-correlation
requirements.

SF-08 applies those established requirements to Evaluation and Determination
without redefining them.

### 27.10 Evaluation and Determination Authority

A Protocol Action Evaluation applies protocol rules derived from the published
protocol generation.

A Protocol Action Determination records the result of that Evaluation.

Its bounded classification authority does not become protocol authority.

No Evaluation, Determination, acceptance classification, rejection
classification, implementation, application, proof, verification result, or
evidence record may redefine:

- the protocol generation;
- protocol semantics;
- privacy semantics;
- proof semantics;
- public-input semantics;
- applicable protocol rules;
- protocol validity;
- transition semantics;
- conformance;
- or certification.

Protocol authority always remains with the published Privacy Engine protocol generation.

### 27.11 SF-08 Formal Summary

The Evaluation scope is fixed:

> begins(E, A, R, C)
> ->
> fixedScope(E, A, R, C)

Evaluation completeness is:

> complete(E)
> iff
> evaluatesAll(E, R, A, C)

The complete Evaluation and Determination relationship is:

> complete(E)
> <->
> producesExactlyOne(E, D)

Determination classification is:

> accepts(D, A)
> xor
> rejects(D, A)

Correctness is:

> correct(D, A, C)
> ->
> (accepts(D, A) iff protocolValid(A, C))

> correct(D, A, C)
> ->
> (rejects(D, A) iff not protocolValid(A, C))

Evaluation failure produces no Determination:

> evaluationFailure(E)
> ->
> not existsProtocolActionDetermination(D, E)

Proof verification remains bounded evidence:

> verifies(V, Z, PI)

> contributesTo(V, E)

> verifiesValid(V, Z, PI)
> =/=>
> accepts(D, A)

Accepted no-transition is:

> accepts(D, A)

> and noTransitionRequired(D)

> ->
> not existsAuthorizedTransition(U, D)

Acceptance remains distinct from transition existence, authorization, and
commitment:

> accepts(D, A)
> =/=>
> exists(U)

> accepts(D, A)
> =/=>
> authorizes(D, U)

> accepts(D, A)
> =/=>
> committed(U)

The privacy boundary remains:

> identifiesEvaluation(id(E), E)
> =/=>
> identifiesActor(id(E), X)

> identifiesDetermination(id(D), D)
> =/=>
> identifiesActor(id(D), X)

SF-08 ends with one accepted or rejected Determination, or with an explicit
absence of Determination where Evaluation did not complete.

It does not define transition mappings, transition authorization mechanics,
transition execution, commitment, state evolution, history, or complete
cross-stage failure semantics.

## 28. SF-09 — Protocol State, Transition Semantics, Preconditions, and Authorization

SF-09 defines the transition-applicability boundary following one accepted
Protocol Action Determination.

It establishes published Protocol Transition mappings, transition-specific
preconditions, eligibility, one identified Protocol State Transition
occurrence, authorization, and protocol-defined transition cardinality.

SF-09 does not perform execution or commitment and does not establish
authoritative successor state.

### 28.1 Protocol State Applicability Boundary

Let:

- `Q0` be one applicable pre-transition protocol state;
- `Q1` be one protocol-defined successor state;
- `T` be one published Protocol Transition mapping;
- `U` be one Protocol State Transition occurrence;
- `D` be one accepted Protocol Action Determination;
- `I` be one implementation.

Protocol state is protocol-owned state governed by the published protocol
generation.

Application state, implementation-local state, transport state, database
state, cache state, UI state, and operational state do not become protocol
state merely because they describe, represent, or observe protocol activity.

SF-09 uses `Q0` only to establish transition applicability and authorization.

RF-31 in SF-10 remains the authoritative requirement family for protocol
state, successor state, and state evolution.

### 28.2 Protocol Transition Mapping, Preconditions, and Eligibility

A Protocol Transition is an identified published semantic mapping between
permitted pre-transition and successor-state classes.

It defines permitted state-change semantics.

It is not one state-change occurrence:

> transitionMapping(T)
> =/=>
> transitionOccurrence(U)

Transition preconditions are the complete published transition-specific
conditions governing whether `T` is eligible against the applicable state and
Action context.

Eligibility is bounded to those conditions.

It does not create another complete Protocol Action Evaluation or another
Protocol Action Determination.

### 28.3 RF-26 — Published Transition Mappings, Preconditions, and Eligibility

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-TRANSMAP-001 | RF-26 | MUST | Every published Protocol Transition mapping | A Protocol Transition mapping MUST possess one stable mapping identity within the applicable published protocol generation. | S02, S17, S18, S26 |
| PE-TRANSMAP-002 | RF-26 | MUST | Every published Protocol Transition mapping | The mapping MUST define the permitted semantic relation between its applicable pre-transition-state class and its protocol-defined successor-state class. | S18, S26, S36 |
| PE-TRANSMAP-003 | RF-26 | MUST NOT | Every Protocol Transition mapping and every interpretation of it | A Protocol Transition mapping MUST NOT be represented as one Protocol State Transition occurrence, execution, commitment, history entry, or actor occurrence. | S02, S17, S18, S26, S27 |
| PE-TRANSMAP-004 | RF-26 | MUST | Every implementation applying a Protocol Transition mapping | The implementation MUST preserve the mapping identity and published transition semantics unchanged. | S01, S18, S26, S33, S36 |
| PE-TRANSMAP-005 | RF-26 | MUST | Every published Protocol Transition mapping with transition-specific preconditions | The mapping MUST identify the complete published precondition set governing its eligibility. | S02, S26, S37 |
| PE-TRANSMAP-006 | RF-26 | MUST | Every transition-eligibility evaluation | Eligibility MUST be established against the applicable protocol state, identified mapping, applicable Action context, and complete published transition-precondition set. | S18, S26, S33, S37 |
| PE-TRANSMAP-007 | RF-26 | MUST | Every transition-eligibility evaluation whose complete applicable precondition set is satisfied | The eligibility result MUST preserve the identified mapping and permit only the later processing authorized by the applicable protocol rules. | S18, S33, S37 |
| PE-TRANSMAP-008 | RF-26 | MUST | Every transition-eligibility evaluation whose applicable precondition set is not completely satisfied | The ineligible result MUST preserve the applicable pre-transition protocol state as unchanged by that attempted transition. | S18, S33, S36, S37 |
| PE-TRANSMAP-009 | RF-26 | MUST NOT | Every implementation evaluating transition preconditions | The implementation MUST NOT infer satisfaction, weaken or strengthen a precondition, substitute another condition, repair the applicable state, or derive an alternate mapping. | S01, S18, S33, S36, S37 |
| PE-TRANSMAP-010 | RF-26 | MUST | Every relationship between transition eligibility and complete Protocol Action Evaluation | Transition eligibility MUST remain a bounded transition-specific evaluation distinct from the complete Evaluation defined by RF-22. | S02, S18, S25, S33, S37 |
| PE-TRANSMAP-011 | RF-26 | MUST NOT | Every transition-enforcement result | A transition-enforcement result MUST NOT itself establish acceptance or rejection, create or alter a Determination, authorize or execute a transition occurrence, commit state change, or establish successor state. | S18, S25, S33, S36 |
| PE-TRANSMAP-012 | RF-26 | MUST NOT | Every implementation-local restriction on operation exposure, request handling, or execution capability | An implementation-local restriction MUST NOT be represented as a published transition precondition or as changing protocol eligibility semantics. | S01, S18, S33, S37 |
| PE-TRANSMAP-013 | RF-26 | MUST NOT | Every mapping, precondition, eligibility, enforcement, diagnostic, log, field, route, test, example, serialization, and observability surface | A transition-mapping or eligibility surface MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | S01, S17, S18, S20, S26, S33, S37 |

### 28.4 Protocol State Transition Identity and Lifecycle

A Protocol State Transition is one identified, bounded, protocol-governed
state-change occurrence whose successful commitment completely changes one
applicable pre-transition protocol state into one protocol-defined successor
state.

> transitions(U, Q0, Q1)

> governedBy(U, P)

The occurrence remains distinct from the mapping that governs it:

> T != U

It also remains distinct from every earlier occurrence:

> A != E

> E != D

> D != U

Authorization, execution, commitment, and failure are predicates or stages of
the same `U`.

They are not independently identified first-class subjects.

### 28.5 RF-27 — Protocol State Transition Occurrence Identity and Lifecycle

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-TRANSOCC-001 | RF-27 | MUST | Every Protocol State Transition | A Protocol State Transition MUST possess one stable occurrence identity identifying exactly one bounded protocol-governed state-change occurrence. | S02, S17, S18, S27 |
| PE-TRANSOCC-002 | RF-27 | MUST | Every Protocol State Transition | The occurrence MUST retain one bounded lifecycle across every applicable authorization, execution, commitment, and failure stage. | S18, S27 |
| PE-TRANSOCC-003 | RF-27 | MUST | Every relationship between a Protocol Action and a Protocol State Transition | The Action and transition occurrence MUST retain distinct identities and semantic roles. | S17, S18, S24, S27 |
| PE-TRANSOCC-004 | RF-27 | MUST | Every relationship between a Protocol Action Evaluation and a Protocol State Transition | The Evaluation and transition occurrence MUST retain distinct identities and semantic roles. | S17, S18, S25, S27 |
| PE-TRANSOCC-005 | RF-27 | MUST | Every relationship between a Protocol Action Determination and a Protocol State Transition | The Determination and transition occurrence MUST retain distinct identities and semantic roles. | S17, S18, S25, S27 |
| PE-TRANSOCC-006 | RF-27 | MUST | Every Protocol State Transition occurrence | The occurrence MUST remain distinct from its governing mapping, pre-transition state, successor state, implementation, history representation, and public consequence. | S02, S17, S18, S26, S27 |
| PE-TRANSOCC-007 | RF-27 | MUST | Every authorization, execution, commitment, and failure stage concerning one Protocol State Transition | Every stage MUST preserve the identity of the same authorized `U`. | S01, S18, S27 |
| PE-TRANSOCC-008 | RF-27 | MUST NOT | Every transition lifecycle representation | Authorization, execution, commitment, or failure MUST NOT be represented as a separately identified first-class transition object. | S02, S17, S18, S27 |
| PE-TRANSOCC-009 | RF-27 | MUST | Every terminal Protocol State Transition classification | A terminal transition MUST be classified as committed or transition failure, but not both. | S18, S27 |
| PE-TRANSOCC-010 | RF-27 | MUST NOT | Every authorized transition that has not reached a terminal classification | Absence of commitment MUST NOT by itself be represented as transition failure. | S18, S27 |
| PE-TRANSOCC-011 | RF-27 | MUST NOT | Every transition identifier, lifecycle record, representation, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A transition-occurrence surface MUST NOT identify the Private Actor, carry enrollment or admission provenance, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | S01, S17, S18, S20, S27 |

### 28.6 Transition Authorization and Cardinality

Transition authorization is the bounded relationship by which one accepted
Determination permits one identified `U` to proceed under the applicable
protocol rules.

> authorizedBy(U, D)
> ->
> accepts(D, A)

Authorization selects `U`.

It does not merely select a class from which an implementation may later
choose a preferred occurrence or outcome.

The complete applicable protocol rules determine whether an accepted
Determination authorizes zero, exactly one, or multiple separately identified
transitions.

> authorizedTransitionCount(D) in {0, 1, n}

### 28.7 RF-28 — Transition Authorization and Cardinality

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-TRANSAUTH-001 | RF-28 | MUST | Every authorization of a Protocol State Transition arising from a Protocol Action | The transition MUST be authorized by one accepted Protocol Action Determination. | S02, S18, S25, S27 |
| PE-TRANSAUTH-002 | RF-28 | MUST NOT | Every rejected Determination, incomplete Evaluation, Evaluation failure, and absence of Determination | The condition MUST NOT authorize an accepted Protocol State Transition. | S18, S25, S27 |
| PE-TRANSAUTH-003 | RF-28 | MUST | Every transition authorization | Authorization MUST identify the authorizing Determination, authorized `U`, governing `T`, applicable `Q0`, required successor-state relation, and every protocol-defined ordering or dependency. | S02, S18, S25, S26, S27 |
| PE-TRANSAUTH-004 | RF-28 | MUST | Every transition authorization | Authorization MUST select one sufficiently bounded transition occurrence rather than a class of later implementation-selected outcomes. | S18, S27 |
| PE-TRANSAUTH-005 | RF-28 | MUST NOT | Every accepted Protocol Action Determination | Acceptance MUST NOT by itself be represented as establishing transition authorization or that a transition occurrence exists. | S18, S25, S27 |
| PE-TRANSAUTH-006 | RF-28 | MUST NOT | Every transition authorization | Authorization MUST NOT be represented as transition execution. | S18, S27 |
| PE-TRANSAUTH-007 | RF-28 | MUST NOT | Every transition authorization | Authorization MUST NOT be represented as transition commitment. | S18, S27 |
| PE-TRANSAUTH-008 | RF-28 | MUST NOT | Every transition authorization | Authorization MUST NOT be represented as an authoritative protocol-state change or authoritative successor state. | S18, S27 |
| PE-TRANSAUTH-009 | RF-28 | MUST | Every accepted Determination for which transition cardinality is applicable | The complete applicable protocol rules MUST determine whether the Determination authorizes zero, exactly one, or multiple transition occurrences. | S02, S18, S25, S27 |
| PE-TRANSAUTH-010 | RF-28 | MUST NOT | Every implementation realizing transition authorization | The implementation MUST NOT choose transition cardinality for convenience, preferred outcome, infrastructure capability, or implementation policy. | S01, S18, S27 |
| PE-TRANSAUTH-011 | RF-28 | MUST | Every accepted Determination requiring zero transitions | The zero-transition authorization relation MUST preserve the successful terminal behavior defined by RF-25 without fabricating a transition occurrence. | S02, S18, S25, S27 |
| PE-TRANSAUTH-012 | RF-28 | MUST | Every accepted Determination authorizing multiple independently committable effects | Each independently committable effect MUST remain one separately identified and separately atomic transition occurrence. | S18, S27 |
| PE-TRANSAUTH-013 | RF-28 | MUST | Every accepted Determination authorizing multiple transitions with protocol-defined ordering or dependencies | Every authorized ordering and dependency MUST be preserved across the separately identified transitions. | S18, S27 |
| PE-TRANSAUTH-014 | RF-28 | MUST | Every group of protocol-required state effects that must succeed or fail together | The effects MUST be represented as one composite atomic Protocol State Transition rather than as independently committable transitions. | S18, S27 |
| PE-TRANSAUTH-015 | RF-28 | MUST NOT | Every authorization of multiple separately identified Protocol State Transitions | Multiple authorized transitions MUST NOT be represented as a separately identified first-class transition-set object. | S02, S17, S18, S27 |

No transition-set object is introduced.

Transition authorization, transition cardinality, and any ordering relation do
not acquire protocol authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

### 28.8 SF-09 Formal Summary

> transitionMapping(T)
> =/=>
> transitionOccurrence(U)

> authorizedBy(U, D)
> ->
> accepts(D, A)

> accepts(D, A)
> =/=>
> exists(U)

> authorizes(D, U)
> =/=>
> executing(U)

> authorizes(D, U)
> =/=>
> committed(U)

> authorizes(D, U)
> =/=>
> transitionsCommittedState(Q0, Q1)

SF-09 authorizes only the identified transition occurrences required by the
complete applicable protocol rules.

It establishes no execution, commitment, or authoritative state change.

## 29. SF-10 — Transition Execution, Commitment, Atomicity, and State Evolution

SF-10 carries each authorized `U` through preserved execution to complete
atomic commitment or explicit transition failure.

It establishes authoritative successor state only through commitment.

### 29.1 Transition Execution and Preservation

Execution is the bounded stage in which an implementation attempts to realize
the already-authorized `U`.

Authorization selects `U`.

Every later transition stage preserves `U`.

Success path:

> U -> preserved(U)

Failure path:

> U -> transitionFailure(U)

Forbidden substitution path:

> U -> U'

where:

> U' != U

If execution cannot preserve `U`, it fails cleanly.

### 29.2 RF-29 — Transition Execution and Preservation

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-TRANSEXEC-001 | RF-29 | MUST | Every Protocol State Transition execution | Execution MUST be the bounded implementation activity that attempts to realize one already-authorized `U`. | S02, S18, S27, S34 |
| PE-TRANSEXEC-002 | RF-29 | MUST | Every execution entry | Execution MUST begin only where the applicable authorization and transition-eligibility conditions permit execution of the identified `U`. | S18, S27, S33, S34 |
| PE-TRANSEXEC-003 | RF-29 | MUST | Every execution of an authorized Protocol State Transition | Execution MUST preserve the transition identity, authorizing Determination, governing mapping, authorized pre-transition state, required successor-state relation, atomicity, and complete protocol-defined effects. | S01, S18, S26, S27, S34 |
| PE-TRANSEXEC-004 | RF-29 | MUST | Every implementation executing an authorized Protocol State Transition | The implementation MUST realize the authorized `U` exactly as defined by the published transition semantics. | S18, S26, S27, S34 |
| PE-TRANSEXEC-005 | RF-29 | MUST NOT | Every implementation executing an authorized Protocol State Transition | The implementation MUST NOT redefine, reinterpret, widen, narrow, repair, merge, divide, or infer replacement semantics for `U`. | S01, S18, S27, S34 |
| PE-TRANSEXEC-006 | RF-29 | MUST NOT | Every execution of authorized `U` | Execution MUST NOT substitute, execute, commit, or report `U'` as `U` where `U' != U`. | S18, S27, S34 |
| PE-TRANSEXEC-007 | RF-29 | MUST | Every relationship between transition eligibility and transition execution | Eligibility and execution MUST remain distinct stages, with eligibility deciding only whether the already-identified transition may proceed. | S18, S33, S34 |
| PE-TRANSEXEC-008 | RF-29 | MUST NOT | Every completed transition execution | Completed execution MUST NOT by itself be represented as commitment or authoritative protocol-state change. | S18, S27, S34 |
| PE-TRANSEXEC-009 | RF-29 | MUST NOT | Every successor-state value or representation derived during execution | Execution machinery and execution output MUST NOT claim or expose derived successor-state material as committed authoritative protocol state before valid RF-30 commitment. | S02, S18, S27, S34, S39 |
| PE-TRANSEXEC-010 | RF-29 | MUST | Every implementation unable to preserve the authorized transition during execution | The implementation MUST fail the execution cleanly while preserving the identity and semantics of the authorized `U`. | S01, S18, S27, S34 |
| PE-TRANSEXEC-011 | RF-29 | MUST NOT | Every failed transition execution | Execution failure MUST NOT authorize an alternate transition, alternate successor state, partial commitment, or semantic substitution. | S18, S27, S34 |
| PE-TRANSEXEC-012 | RF-29 | MUST NOT | Every execution representation, instruction, transaction, internal call, storage operation, retry, diagnostic, log, field, route, test, example, serialization, and observability surface | An execution surface MUST NOT create another architectural transition identity, identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | S01, S17, S18, S20, S27, S34 |

### 29.3 Transition Commitment, Completeness, and Atomicity

Commitment is the successful terminal predicate of one `U`.

Only commitment establishes the complete authoritative state change from `Q0`
to `Q1`.

> committed(U)
> ->
> completeStateChange(U, Q0, Q1)

Within a valid authorization and execution context:

> committed(U)
> iff
> completeStateChange(U, Q0, Q1)

Semantic atomicity means that `U` establishes its complete authorized state
change or establishes no committed state change.

### 29.4 RF-30 — Transition Commitment, Completeness, and Atomicity

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-COMMIT-001 | RF-30 | MUST | Every committed Protocol State Transition | Commitment MUST be the successful terminal predicate of the same identified `U` that was authorized and executed. | S02, S18, S27 |
| PE-COMMIT-002 | RF-30 | MUST | Every committed Protocol State Transition | Commitment MUST derive from one valid accepted Determination and valid authorization of `U`. | S18, S25, S27 |
| PE-COMMIT-003 | RF-30 | MUST | Every committed Protocol State Transition | Commitment MUST follow correct execution that preserves the complete authorized identity and semantics of `U`. | S01, S18, S27, S34 |
| PE-COMMIT-004 | RF-30 | MUST | Every committed Protocol State Transition authorized against `Q0` | Commitment MUST establish that the applicable protocol state remains equivalent to the authorized `Q0` for the protocol-relevant purpose of `U`. | S18, S27, S36 |
| PE-COMMIT-005 | RF-30 | MUST | Every committed Protocol State Transition | Commitment MUST establish the complete protocol-defined state-change relation and the required successor state `Q1`. | S18, S27, S36, S39 |
| PE-COMMIT-006 | RF-30 | MUST | Every committed Protocol State Transition | Commitment MUST establish the absence of omitted required effects and unauthorized additional state effects. | S18, S27, S36 |
| PE-COMMIT-007 | RF-30 | MUST | Every committed Protocol State Transition | Commitment MUST preserve semantic atomicity across every protocol-required effect owned by `U`. | S18, S27, S36 |
| PE-COMMIT-008 | RF-30 | MUST | Every valid authorization and execution context for `U` | Commitment MUST be equivalent to complete state change only within that valid bounded context. | S02, S18, S27 |
| PE-COMMIT-009 | RF-30 | MUST NOT | Every partial execution of a Protocol State Transition | Partial execution MUST NOT be represented as commitment. | S18, S27, S36 |
| PE-COMMIT-010 | RF-30 | MUST NOT | Every partial or incomplete state change | A partial or incomplete state change MUST NOT be represented as commitment or authoritative successor state. | S18, S27, S36 |
| PE-COMMIT-011 | RF-30 | MUST NOT | Every Protocol State Transition | A transition MUST NOT be partially committed. | S18, S27, S36 |
| PE-COMMIT-012 | RF-30 | MUST NOT | Every implementation assertion, report, event, record, diagnostic, or representation concerning commitment | The implementation surface MUST NOT by itself establish protocol commitment. | S01, S18, S27 |
| PE-COMMIT-013 | RF-30 | MUST NOT | Every commitment representation and interpretation | Commitment MUST NOT be represented as a separately identified first-class object or as possessing authority or lifecycle independent of `U`. | S02, S17, S18, S27 |

### 29.5 Protocol State, Successor State, and State Evolution

`Q0` and `Q1` are distinct identified protocol states related by committed
`U`.

The successor-state relation is derived only from:

- the authorized `U`;
- the governing `T`;
- the applicable `Q0`;
- and the complete published transition semantics.

Execution may derive successor-state material.

Only valid commitment establishes `Q1` as authoritative protocol state.

State evolution is therefore:

> Q0
> ->
> committed(U)
> ->
> Q1

### 29.6 RF-31 — Protocol State, Successor State, and State Evolution

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-STATE-001 | RF-31 | MUST | Every protocol-state representation | Protocol state MUST contain only state governed as protocol state by the applicable published protocol generation. | S01, S02, S18, S35 |
| PE-STATE-002 | RF-31 | MUST NOT | Every application, implementation-local, transport, database, cache, UI, operational, diagnostic, and observability state representation | The representation MUST NOT be treated as protocol state merely because it describes, realizes, stores, or observes protocol activity. | S01, S17, S18, S20, S35 |
| PE-STATE-003 | RF-31 | MUST | Every Protocol State Transition authorization | The authorization MUST identify the bounded pre-transition protocol state `Q0` against which `U` is authorized. | S18, S27, S35 |
| PE-STATE-004 | RF-31 | MUST NOT | Every implementation realizing an authorized transition | The implementation MUST NOT select, reconstruct, repair, or substitute a preferred pre-transition protocol state after authorization. | S01, S18, S27, S35 |
| PE-STATE-005 | RF-31 | MUST | Every successor-state derivation | `Q1` MUST be derived only from the authorized `U`, governing `T`, applicable `Q0`, and complete published transition semantics. | S18, S26, S27, S36, S38, S39 |
| PE-STATE-006 | RF-31 | MUST NOT | Every implementation deriving successor-state material | The implementation MUST NOT invent, infer, repair, merge, widen, narrow, substitute, or add application meaning to `Q1`. | S01, S18, S27, S36, S39 |
| PE-STATE-007 | RF-31 | MUST NOT | Every successor-state value derived before commitment | Derived successor-state material MUST NOT be represented as authoritative protocol state. | S02, S18, S27, S34, S39 |
| PE-STATE-008 | RF-31 | MUST | Every committed Protocol State Transition | Only valid commitment of `U` MUST establish `Q1` as authoritative successor state for that transition. | S02, S18, S27, S36, S38, S39 |
| PE-STATE-009 | RF-31 | MUST | Every committed Protocol State Transition from `Q0` to `Q1` | The pre-transition state, successor state, and transition occurrence MUST retain distinct identities and their exact committed relationship. | S17, S18, S27, S35, S38, S39 |
| PE-STATE-010 | RF-31 | MUST | Every authoritative protocol-state evolution | State evolution MUST consist of one applicable `Q0`, one committed `U`, and the protocol-defined authoritative `Q1`. | S18, S27, S35, S38 |
| PE-STATE-011 | RF-31 | MUST NOT | Every failed, incomplete, partial, simulated, predicted, or merely reported transition | The transition condition MUST NOT establish authoritative state evolution or authoritative `Q1`. | S01, S18, S27, S34, S38, S39 |
| PE-STATE-012 | RF-31 | MUST | Every committed protocol-state evolution | The evolution MUST preserve every applicable published protocol invariant and every complete protocol-required effect of `U`. | S18, S27, S35, S36, S38 |
| PE-STATE-013 | RF-31 | MUST NOT | Every protocol-state identifier, state representation, successor-state derivation, evolution record, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A protocol-state surface MUST NOT identify the Private Actor, carry enrollment or admission provenance, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | S01, S17, S18, S20, S27, S35, S38, S39 |

Execution, commitment, state, successor state, and state evolution remain
bounded protocol concepts.

None becomes protocol authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

### 29.7 SF-10 Formal Summary

> authorizedBy(U, D)
> ->
> preserved(U)

> executed(U)
> =/=>
> committed(U)

> derivesPostState(U, Q1)
> =/=>
> establishesPostState(U, Q1)

> committed(U)
> ->
> establishesPostState(U, Q1)

> partialExecution(U)
> =/=>
> committed(U)

> partialStateChange(U)
> =/=>
> committed(U)

> reportsCommitted(I, U)
> =/=>
> committed(U)

Success path:

> U -> preserved(U) -> committed(U)

Failure path:

> U -> transitionFailure(U)

Forbidden path:

> U -> U'

where:

> U' != U

## 30. SF-11 — History, Public Consequences, Failure, Staleness, and Re-evaluation

SF-11 defines the authoritative committed-history boundary, bounded public
protocol-state consequence, complete cross-stage failure classification,
stale authorization, and re-evaluation.

It preserves every earlier occurrence and classification unchanged.

### 30.1 Protocol-State History

Only committed transitions enter authoritative protocol-state history as
committed state changes.

> committed(U)
> ->
> includedInProtocolStateHistory(U, H)

Operational records may describe attempts, failures, retries, diagnostics, or
implementation activity.

They do not thereby become authoritative protocol-state history.

### 30.2 RF-32 — Protocol-State History

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-STATEHIST-001 | RF-32 | MUST | Every Protocol State Transition included as a committed state change in authoritative protocol-state history | The transition MUST have validly committed. | S02, S18, S27 |
| PE-STATEHIST-002 | RF-32 | MUST | Every authoritative protocol-state history representation | The representation MUST preserve each committed transition identity, committed ordering, applicable pre-transition state, authoritative successor state, and bounded public consequence. | S18, S27 |
| PE-STATEHIST-003 | RF-32 | MUST NOT | Every failed Protocol State Transition | A failed transition MUST NOT be included as a committed transition in authoritative protocol-state history. | S18, S27 |
| PE-STATEHIST-004 | RF-32 | MUST NOT | Every pre-transition failure | A pre-transition failure MUST NOT be included as a committed transition in authoritative protocol-state history. | S18, S27 |
| PE-STATEHIST-005 | RF-32 | MUST NOT | Every partial execution or partial state change | Partial execution or partial state change MUST NOT be included as committed history. | S18, S27 |
| PE-STATEHIST-006 | RF-32 | MUST NOT | Every operational attempt, diagnostic, retry, log, database row, event, report, error, cache record, or observability record | An operational record MUST NOT be treated as authoritative protocol-state history merely because it describes protocol activity. | S01, S18, S27 |
| PE-STATEHIST-007 | RF-32 | MUST | Every permitted protocol-state history realization | The realization MUST preserve identical committed transition semantics independently of storage structure, database, blockchain, consensus, event, transaction, or infrastructure choice. | S01, S18, S27 |
| PE-STATEHIST-008 | RF-32 | MUST NOT | Every history identifier, entry, representation, ordering record, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A protocol-state history surface MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | S01, S17, S18, S20, S27 |

### 30.3 Public Protocol-State Consequences

A committed `U` establishes one bounded public protocol-state consequence.

> committed(U)
> ->
> publicProtocolConsequence(U, Q1)

The consequence records only the protocol-defined meaning of committed state
change.

It is not an independently identified object between commitment and successor
state.

### 30.4 RF-33 — Public Protocol-State Consequences

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-STATECONSEQ-001 | RF-33 | MUST | Every committed Protocol State Transition | Commitment MUST establish the bounded public protocol-state consequence defined for `U` and authoritative `Q1`. | S02, S18, S27 |
| PE-STATECONSEQ-002 | RF-33 | MUST | Every public protocol-state consequence | The consequence MUST remain bounded to the published protocol meaning of the committed state change. | S01, S18, S27 |
| PE-STATECONSEQ-003 | RF-33 | MUST | Every relationship between a Published Result and a public protocol-state consequence | The interface-level Published Result and committed protocol-state consequence MUST remain distinct semantic roles. | S02, S18, S27, S32 |
| PE-STATECONSEQ-004 | RF-33 | MUST | Every relationship between a Protocol Action Determination and a public protocol-state consequence | The Determination and committed consequence MUST remain distinct, including where both are publicly observable. | S18, S25, S27 |
| PE-STATECONSEQ-005 | RF-33 | MUST | Every relationship between authoritative successor state and public protocol-state consequence | The successor-state representation and its bounded public consequence MUST remain distinct without introducing an intermediate consequence object. | S02, S17, S18, S27 |
| PE-STATECONSEQ-006 | RF-33 | MUST NOT | Every public protocol-state consequence and every interpretation of it | The consequence MUST NOT be represented as application, factual, legal, social, institutional, user-intent, or off-protocol truth. | S01, S17, S18, S27 |
| PE-STATECONSEQ-007 | RF-33 | MUST NOT | Every public protocol-state consequence | The consequence MUST NOT be represented as a separately identified first-class object possessing authority or lifecycle independent of committed `U`. | S02, S17, S18, S27 |
| PE-STATECONSEQ-008 | RF-33 | MUST NOT | Every public consequence identifier, representation, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A public-consequence surface MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | S01, S17, S18, S20, S27 |
| PE-STATECONSEQ-009 | RF-33 | MUST NOT | Every public consequence recording authorization, membership, eligibility, uniqueness, possession, or another bounded protocol property | The recorded property MUST NOT be extended into actor identification, enrollment or admission provenance, hidden intent, or additional correlation meaning. | S01, S18, S27 |

### 30.5 Failure Classification and Separation

A failure classification describes the stage and condition that actually
occurred.

The complete classification boundary distinguishes:

- pre-evaluation failure;
- Evaluation failure;
- rejection;
- accepted no-transition;
- pre-transition failure;
- transition failure;
- stale authorization;
- implementation error;
- incorrect execution;
- incorrect commitment;
- and incorrect reporting.

Causal relationships among classifications do not make them semantically
equivalent.

### 30.6 RF-34 — Failure Classifications and Failure Separation

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-FAIL-001 | RF-34 | MUST | Every protocol-use failure or implementation-error classification | The classification MUST identify the actual bounded lifecycle stage and condition that occurred. | S02, S18, S25, S27, S37 |
| PE-FAIL-002 | RF-34 | MUST | Every pre-evaluation failure | Pre-evaluation failure MUST mean that no valid Protocol Action Evaluation occurrence began. | S18, S25 |
| PE-FAIL-003 | RF-34 | MUST | Every Protocol Action Evaluation failure | Evaluation failure MUST mean that one Evaluation began but did not complete and produced no Determination. | S18, S25 |
| PE-FAIL-004 | RF-34 | MUST | Every Protocol Action rejection | Rejection MUST remain the rejecting classification of one valid Determination produced by one completed Evaluation. | S18, S25 |
| PE-FAIL-005 | RF-34 | MUST | Every accepted no-transition terminal path | Accepted no-transition MUST remain a successful Determination-boundary completion rather than a failure classification. | S02, S18, S25, S27 |
| PE-FAIL-006 | RF-34 | MUST | Every pre-transition failure | Pre-transition failure MUST mean that the post-Determination transition boundary could not validly enter bounded execution. | S18, S27, S37 |
| PE-FAIL-007 | RF-34 | MUST | Every transition failure | Transition failure MUST remain the explicit terminal classification of an authorized transition that does not establish complete commitment. | S18, S27 |
| PE-FAIL-008 | RF-34 | MUST NOT | Every stale authorization | Stale authorization MUST NOT be represented as rejection, Evaluation failure, or proof that the earlier Determination was incorrect. | S18, S25, S27 |
| PE-FAIL-009 | RF-34 | MUST | Every implementation error | Implementation error MUST remain a bounded diagnosis of incorrect realization, classification, commitment, or reporting rather than a redefinition of protocol truth. | S01, S17, S18, S27 |
| PE-FAIL-010 | RF-34 | MUST | Every incorrect execution diagnosis | Incorrect execution MUST identify implementation failure to preserve or correctly realize authorized `U` without becoming semantically equivalent to every transition failure. | S18, S27 |
| PE-FAIL-011 | RF-34 | MUST | Every incorrect commitment diagnosis | Incorrect commitment MUST identify an implementation representation or materialization that does not satisfy valid protocol commitment. | S18, S27 |
| PE-FAIL-012 | RF-34 | MUST | Every incorrect reporting diagnosis | Incorrect reporting MUST remain distinct from the protocol condition incorrectly reported. | S18, S27 |
| PE-FAIL-013 | RF-34 | MUST NOT | Every pre-transition failure | Pre-transition failure MUST NOT be represented as transition failure where bounded execution of `U` did not begin. | S18, S27 |
| PE-FAIL-014 | RF-34 | MUST NOT | Every transition failure, stale authorization, implementation error, incorrect execution, incorrect commitment, and incorrect reporting condition | A later-stage condition MUST NOT be converted into Protocol Action rejection or Evaluation failure. | S01, S18, S25, S27 |
| PE-FAIL-015 | RF-34 | MUST NOT | Every infrastructure failure, inability to preserve `U`, changed-state condition, partial execution, or reporting error | The condition MUST NOT be silently converted into commitment or another semantically different success or failure class. | S01, S18, S27 |
| PE-FAIL-016 | RF-34 | MUST NOT | Every failure, error, staleness, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A failure surface MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, expose implementation or operational metadata as actor identity, or create an actor-reconstruction bridge. | S01, S17, S18, S20, S25, S27 |
| PE-FAIL-017 | RF-34 | MUST NOT | Every failure classification and implementation-error diagnosis | A failure classification or error diagnosis MUST NOT be represented as a separately identified first-class failure object. | S02, S17, S18, S25, S27 |

### 30.7 Stale Authorization and Re-evaluation

Authorization may be bounded to `Q0`:

> authorizedAgainst(U, Q0)

Before commitment, the implementation establishes whether the applicable
current protocol state remains equivalent to `Q0` for the protocol-relevant
purpose of `U`.

Material conflict makes the authorization stale and prohibits commitment under
that authorization.

Where the applicable protocol rules require re-evaluation, re-evaluation
creates new occurrences.

It does not mutate or repair earlier ones.

### 30.8 RF-35 — Stale Authorization and Re-evaluation

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-STALEAUTH-001 | RF-35 | MUST | Every transition authorization bounded to one pre-transition protocol state | The authorization MUST remain explicitly bounded to the identified `Q0`. | S02, S18, S25, S27 |
| PE-STALEAUTH-002 | RF-35 | MUST | Every authorized transition before execution and commitment | The implementation MUST establish whether the applicable current protocol state remains equivalent to authorized `Q0` for the protocol-relevant purpose of `U`. | S01, S18, S27 |
| PE-STALEAUTH-003 | RF-35 | MUST | Every authorized transition whose current protocol state remains equivalent to `Q0` | The equivalence determination MUST remain bounded to transition applicability and MUST preserve the original authorization unchanged. | S18, S27 |
| PE-STALEAUTH-004 | RF-35 | MUST | Every authorized transition whose current protocol state materially conflicts with `Q0` | The authorization MUST be classified as stale for commitment against the conflicting state. | S18, S25, S27 |
| PE-STALEAUTH-005 | RF-35 | MUST NOT | Every stale transition authorization | A stale authorization MUST NOT permit commitment against the materially conflicting state. | S18, S27 |
| PE-STALEAUTH-006 | RF-35 | MUST NOT | Every implementation resolving applicable-state conflict | The implementation MUST NOT select whichever state context produces a preferred result or repair the existing authorization. | S01, S18, S25, S27 |
| PE-STALEAUTH-007 | RF-35 | MUST NOT | Every stale transition authorization | Staleness MUST NOT mutate, invalidate, rewrite, or reclassify the earlier Evaluation or Determination. | S18, S25, S27 |
| PE-STALEAUTH-008 | RF-35 | MUST | Every materially changed context or state for which the applicable protocol rules require re-evaluation | The implementation MUST begin one new Protocol Action Evaluation occurrence under the newly applicable bounded context. | S02, S18, S25, S27 |
| PE-STALEAUTH-009 | RF-35 | MUST | Every completed required re-evaluation | The new Evaluation MUST produce one new Determination and, where applicable, newly authorized transition occurrences whose identities are distinct from every earlier transition occurrence. | S18, S25, S27 |
| PE-STALEAUTH-010 | RF-35 | MUST NOT | Every required re-evaluation | Re-evaluation MUST NOT mutate, repair, replace, or silently reinterpret the earlier `E`, `D`, or `U`. | S01, S17, S18, S25, S27 |
| PE-STALEAUTH-011 | RF-35 | MUST NOT | Every stale-authorization and re-evaluation identifier, record, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A staleness or re-evaluation surface MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | S01, S17, S18, S20, S25, S27 |
| PE-STALEAUTH-012 | RF-35 | MUST NOT | Every stale-authorization condition and representation | Stale authorization MUST NOT be represented as a separately identified first-class stale-authorization object. | S02, S17, S18, S25, S27 |

No stale-authorization object is introduced.

No re-evaluation repair path is introduced.

The preserved path is:

> E1
> ->
> D1
> ->
> stale authorization
> ->
> new E2
> ->
> new D2
> ->
> possible new U2

The forbidden paths are:

> E1 -> repair(E1)

> D1 -> rewrite(D1)

> U1 -> infer(U2)

without the required new Evaluation and Determination.

### 30.9 SF-11 Privacy and Authority

SF-11 preserves:

> Private actors, public actions.

Public state, transition, committed history, and bounded consequence visibility
do not imply participant visibility.

> identifiesTransition(id(U), U)
> =/=>
> identifiesActor(id(U), X)

> identifiesState(id(Q), Q)
> =/=>
> identifiesActor(id(Q), X)

> includedInProtocolStateHistory(U, H)
> =/=>
> identifiesActor(id(U), X)

> publicProtocolConsequence(U, Q1)
> =/=>
> identifiesActor(id(U), X)

No state, mapping, occurrence, authorization relation, execution, commitment,
history, consequence, failure classification, stale authorization,
re-evaluation, implementation, application, actor, proof, Evaluation, or
Determination may redefine protocol semantics or acquire protocol authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

### 30.10 SF-11 Formal Summary

> committed(U)
> ->
> includedInProtocolStateHistory(U, H)

> transitionFailure(U)
> =/=>
> includedAsCommittedTransition(U, H)

> partialExecution(U)
> =/=>
> includedAsCommittedTransition(U, H)

> committed(U)
> ->
> publicProtocolConsequence(U, Q1)

> evaluationFailure(E)
> =/=>
> rejects(D, A)

> transitionFailure(U)
> =/=>
> rejects(D, A)

> transitionFailure(U)
> =/=>
> evaluationFailure(E)

> preTransitionFailure(U)
> =/=>
> transitionFailure(U)

> staleAuthorization(U)
> =/=>
> incorrect(D)

> incorrectExecution(I, U)
> =/=>
> changesSemantics(P)

> staleAuthorization(U)
> ->
> not committed(U)

SF-11 completes the state-and-transition composition boundary.

It does not define the application, runtime, implementation, profile,
conformance, certification, semantic-preservation, or complete-exclusion
requirements reserved to SF-12–SF-16.

## 31. SF-12 — Application, Adapter, Runtime, and Integration Boundaries

SF-12 defines the application-owned representations, translation boundaries,
operational responsibilities, and integration-preservation obligations through
which applications use Privacy Engine capabilities.

Application representation remains distinct from protocol meaning.

Operational responsibility remains distinct from protocol authority.

### 31.1 Application Requests, Adapters, and Application Responses

An Application Request is one bounded application-owned representation
presented toward an application boundary for possible translation into an
applicable protocol-facing representation.

An Application Request is not automatically a Protocol Operation or Protocol
Action. Translation and protocol admission do not occur merely because an
application created a request.

An Application Adapter is the bounded translation boundary between
application-owned representation and the applicable protocol-facing interface
representation.

Translation changes representation only.

Where the applicable meaning cannot be preserved, translation fails:

> input -> preservedTranslation(input)

or:

> input -> translationFailure

never:

> input -> repairedOrInferred(input')

An Application Response is one bounded application-owned representation
derived from an applicable Published Result or other protocol-defined output
exposed through the governing interface.

It is not the Published Result or public protocol-state consequence itself.

#### 31.1.1 RF-14 — Application Requests, Responses, and Adapters

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-APPREP-001 | RF-14 | MUST | Every Application Request | An Application Request MUST remain a bounded application-owned representation presented for possible translation at one identified application boundary. | S29, S41, S43 |
| PE-APPREP-002 | RF-14 | MUST | Every identified Application Request | The request identity and scope MUST identify the request representation without identifying a Private Actor or becoming a reusable cross-action identifier. | S01, S18, S41 |
| PE-APPREP-003 | RF-14 | MUST NOT | Every Application Request | An Application Request MUST NOT be interpreted merely by its existence as a Protocol Operation, Protocol Action, proof, declared public input, Evaluation, Determination, Protocol State Transition, protocol state, or protocol truth. | S18, S23, S24, S41 |
| PE-APPREP-004 | RF-14 | MUST | Every application-owned request value | Each request value MUST remain application-owned until a valid adapter translation establishes its applicable protocol-facing representation under the governing Interface Contract. | S29, S30, S31, S41 |
| PE-APPREP-005 | RF-14 | MUST | Every Application Adapter | An Application Adapter MUST remain a bounded translation boundary between application-owned representation and the applicable protocol-facing interface representation. | S29, S40 |
| PE-APPREP-006 | RF-14 | MUST | Every identified Application Adapter | Adapter identity and scope MUST remain distinct from the application, runtime, implementation, Interface Contract, Concrete Interface Specification, Protocol Operation, Protocol Action, and Private Actor. | S20, S29, S40 |
| PE-APPREP-007 | RF-14 | MUST | Every adapter translation | Translation MUST be governed by the applicable Interface Contract and Concrete Interface Specification and MUST map only representations supported by that boundary. | S29, S30, S31, S40 |
| PE-APPREP-008 | RF-14 | MUST | Every successful adapter translation | A successful translation MUST preserve the complete bounded meaning, identity distinctions, ordering requirements, applicability conditions, and failure semantics of its source representation. | S29, S30, S40, S41, S42 |
| PE-APPREP-009 | RF-14 | MUST | Every adapter unable to preserve applicable meaning | The adapter MUST return bounded translation failure when it cannot preserve the applicable meaning or required representation. | S29, S40, S43 |
| PE-APPREP-010 | RF-14 | MUST NOT | Every adapter translation | Translation MUST NOT repair, infer, widen, narrow, merge, divide, substitute, or invent protocol meaning, protocol subjects, protocol values, or protocol outcomes. | S18, S29, S40, S43 |
| PE-APPREP-011 | RF-14 | MUST | Every Application Response | An Application Response MUST remain a bounded application-owned representation derived from one applicable protocol-defined output exposed through the governing interface. | S29, S32, S42 |
| PE-APPREP-012 | RF-14 | MUST | Every identified Application Response | Response identity and scope MUST identify the response representation without changing the identity of its source output or identifying a Private Actor. | S01, S18, S32, S42 |
| PE-APPREP-013 | RF-14 | MUST NOT | Every Application Response | An Application Response MUST NOT be identified with or substituted for its source Published Result, public protocol-state consequence, Determination, protocol state, or application interpretation. | S18, S27, S32, S42 |
| PE-APPREP-014 | RF-14 | MUST | Every Application Response derived through translation | The response MUST preserve the complete bounded meaning and failure status of its source protocol-defined output while remaining application-owned representation. | S29, S32, S40, S42 |
| PE-APPREP-015 | RF-14 | MUST NOT | Every Application Request, adapter output, and Application Response | Application-facing representation MUST NOT convert protocol output into factual, legal, social, institutional, or application truth or into evidence of user intent or Private Actor identity. | S01, S18, S29, S41, S42 |
| PE-APPREP-016 | RF-14 | MUST | Every request, adapter, response, field, serialization, example, and diagnostic surface | Application-facing representation and translation surfaces MUST preserve SF-03 and SF-04 terminology, identity separation, privacy, unlinkability, minimum-disclosure, and neutral-naming requirements. | S01, S18, S20, S29, S40, S41, S42 |

### 31.2 Application, Adapter, and Integration Authority Boundaries

Applications own application representation, application-local policy, and
application interpretation.

Adapters own bounded representation translation.

Integrators own preservation across connected boundaries.

None owns protocol semantics.

#### 31.2.1 RF-36 — Application and Adapter Authority Boundaries

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-APPAUTH-001 | RF-36 | MAY | Every application | An application MAY define application-local representation, terminology, policy, validation, presentation, persistence, and interpretation within its declared application-owned scope. | S29, S40, S41, S42, S43 |
| PE-APPAUTH-002 | RF-36 | MUST NOT | Every application policy or interpretation | Application policy or interpretation MUST NOT alter protocol validity, applicable protocol obligations, proof meaning, public-input meaning, Evaluation, Determination, transition semantics, commitment, protocol state, compatibility, conformance, or certification. | S18, S21, S29, S43 |
| PE-APPAUTH-003 | RF-36 | MUST NOT | Every application and Application Request or Response | An application or its representations MUST NOT acquire protocol authority or represent application-owned meaning as protocol-defined meaning. | S21, S29, S41, S42 |
| PE-APPAUTH-004 | RF-36 | MUST | Every Application Adapter | An adapter MUST exercise responsibility only for bounded representation handling and translation within its governing interface boundary. | S29, S40 |
| PE-APPAUTH-005 | RF-36 | MUST NOT | Every Application Adapter | An adapter MUST NOT redefine Interface Contract meaning, Protocol Surface meaning, Protocol Operation meaning, Protocol Action identity, proof or public-input meaning, Evaluation, Determination, transition, commitment, state, Published Result, public consequence, validity, privacy, compatibility, conformance, or certification. | S18, S20, S22, S29, S40 |
| PE-APPAUTH-006 | RF-36 | MUST | Every integrator | An integrator MUST preserve every applicable upstream semantic subject, requirement, identity distinction, ordering rule, failure rule, privacy boundary, and authority boundary across the connected application, adapter, runtime, and implementation surfaces. | S20, S21, S29, S44 |
| PE-APPAUTH-007 | RF-36 | MUST NOT | Every integration | Integration MUST NOT authorize semantic repair, inference, substitution, correlation, authority transfer, or the creation of an application-specific alternative protocol path. | S18, S20, S21, S44 |
| PE-APPAUTH-008 | RF-36 | MUST | Every adapter replacement or application-boundary change | The replacement or change MUST preserve every applicable published interface meaning and MUST fail compatibility where that meaning cannot be preserved. | S22, S29, S40, S44 |
| PE-APPAUTH-009 | RF-36 | MUST NOT | Every application-side validation or default | Application validation, defaults, convenience abstractions, or preferred outcomes MUST NOT be treated as protocol validation, protocol defaults, protocol rules, or protocol outcomes. | S29, S40, S41 |
| PE-APPAUTH-010 | RF-36 | MUST | Every application, adapter, and integration failure | Failure MUST be reported within its bounded layer and MUST preserve the distinction between representation failure, runtime failure, implementation failure, and protocol-defined failure. | S18, S27, S43, S44 |
| PE-APPAUTH-011 | RF-36 | MUST NOT | Every application, adapter, integration record, or observability surface | The surface MUST NOT identify a Private Actor, carry enrollment or admission provenance, create reusable participant identity, create cross-action linkage, or compose metadata into an actor-reconstruction bridge. | S01, S18, S20, S21, S44 |
| PE-APPAUTH-012 | RF-36 | MUST | Every public application, adapter, or integration identifier | The identifier MUST remain bounded to its declared non-actor subject without being interpreted as protocol identity, Protocol Action identity, or Private Actor identity. | S01, S18, S20, S44 |

### 31.3 Runtime, Enforcement, Execution, and Integration Responsibility

A Privacy Engine runtime is an identified operational context through which an
implementation performs bounded protocol-facing work.

The runtime may orchestrate mechanisms.

Orchestration does not merge their semantic roles.

Protocol Enforcement evaluates transition eligibility under published
preconditions and contributes to complete Protocol Action Evaluation where
applicable.

Enforcement is not complete Evaluation.

Execution is not enforcement.

Execution is not commitment.

#### 31.3.1 RF-37 — Runtime, Enforcement, and Execution Responsibility

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-RUNTIME-001 | RF-37 | MUST | Every Privacy Engine runtime | A runtime MUST remain an identified operational context through which one or more identified implementations perform bounded protocol-facing work. | S43, S47 |
| PE-RUNTIME-002 | RF-37 | MUST | Every identified runtime | Runtime identity and scope MUST remain distinct from application identity, adapter identity, implementation identity, deployment identity, protocol identity, Protocol Action identity, and Private Actor identity. | S01, S18, S43, S47 |
| PE-RUNTIME-003 | RF-37 | MUST NOT | Every runtime | A runtime MUST NOT interpret application-local meaning as protocol meaning or assume application ownership merely because it receives application-facing material. | S21, S43, S47 |
| PE-RUNTIME-004 | RF-37 | MUST | Every runtime using an implementation | The runtime MUST preserve the identity and declared scope of each implementation through which it realizes protocol-facing work. | S43, S45, S47 |
| PE-RUNTIME-005 | RF-37 | MAY | Every runtime | A runtime MAY receive applicable inputs, invoke validation and enforcement, invoke Evaluation, invoke authorized execution, expose applicable results, and report bounded failure where those responsibilities are assigned by the applicable implementation profile. | S33, S34, S43, S47, S55 |
| PE-RUNTIME-006 | RF-37 | MUST NOT | Every runtime orchestration path | Runtime orchestration order, component topology, retry behavior, transport, storage, or deployment mechanics MUST NOT redefine the semantic identity or ordering requirements of Protocol Actions, Evaluations, Determinations, transitions, commitment, state, history, or consequences. | S18, S20, S27, S43, S47 |
| PE-RUNTIME-007 | RF-37 | MUST | Every Protocol Enforcement occurrence | Enforcement MUST evaluate only the applicable published transition preconditions and MUST contribute its bounded eligibility result to the complete applicable Protocol Action Evaluation where required. | S25, S27, S33 |
| PE-RUNTIME-008 | RF-37 | MUST NOT | Every Protocol Enforcement occurrence | Enforcement MUST NOT be interpreted as the complete Protocol Action Evaluation or as an independent Protocol Action Determination. | S02, S18, S25, S33 |
| PE-RUNTIME-009 | RF-37 | MUST NOT | Every Protocol Enforcement occurrence | Enforcement MUST NOT execute a transition, commit state, construct authoritative successor state, publish a result, or select an alternative transition. | S27, S33, S34 |
| PE-RUNTIME-010 | RF-37 | MUST | Every authorized transition execution | Execution MUST preserve the already-authorized Protocol State Transition occurrence and realize only its published transition mapping. | S27, S34 |
| PE-RUNTIME-011 | RF-37 | MUST NOT | Every transition execution | Execution MUST NOT perform enforcement, substitute another transition occurrence, or treat derived successor-state material as committed authoritative state. | S27, S33, S34, S35 |
| PE-RUNTIME-012 | RF-37 | MUST NOT | Every successful execution | Successful execution MUST NOT be interpreted as commitment until the complete SF-10 commitment requirements have been satisfied. | S27, S34, S35 |
| PE-RUNTIME-013 | RF-37 | MUST | Every runtime result or failure report | Runtime reporting MUST preserve the source result, lifecycle stage, success or failure classification, and applicable identity distinctions without inventing protocol truth. | S18, S27, S32, S43, S47 |
| PE-RUNTIME-014 | RF-37 | MUST NOT | Every runtime or implementation failure | A runtime or implementation failure MUST NOT mutate an earlier Protocol Action, Evaluation, Determination, authorization, transition occurrence, commitment status, or protocol-state history. | S18, S27, S43, S47 |
| PE-RUNTIME-015 | RF-37 | MUST | Every runtime value, log, diagnostic, retry, timing, ordering, topology, and observability surface | The surface MUST preserve SF-04 privacy without exposing or composing runtime metadata as Private Actor identity or cross-action linkage. | S01, S18, S20, S43, S47 |
| PE-RUNTIME-016 | RF-37 | MUST NOT | Every runtime, enforcement mechanism, execution mechanism, and orchestrator | Operational responsibility MUST NOT be interpreted as ownership of protocol semantics or as protocol authority. | S21, S33, S34, S43, S47 |

### 31.4 SF-12 Formal Summary

The SF-12 preservation paths are:

> ApplicationRequest
> -> preservedTranslation
> -> protocolFacingRepresentation

> protocolDefinedOutput
> -> preservedTranslation
> -> ApplicationResponse

> runtimeResponsibility
> =/=> protocolAuthority

> enforcementEligibility(V)
> -> contributesTo(V, E)

> enforcementEligibility(V)
> =/=> completeEvaluation(E)

> executed(U)
> =/=> committed(U)

Protocol authority always remains with the published Privacy Engine protocol generation.

## 32. SF-13 — Implementation, Realization, Compatibility, and Migration

SF-13 defines implementation identity and obligations, the preservation
relationship of protocol realization, the complete prohibition against
downstream semantic authority, and the bounded compatibility architecture.

An implementation realizes applicable protocol obligations.

It does not define them.

### 32.1 Implementation Identity, Scope, and Obligations

A Privacy Engine implementation is one identified technical realization of
the applicable normative requirements selected by one or more applicable
implementation profiles.

Its identity is realization identity only.

#### 32.1.1 RF-38 — Implementation Identity and Implementation Obligations

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-IMPL-001 | RF-38 | MUST | Every Privacy Engine implementation | An implementation MUST be one identified technical realization of the applicable normative requirements selected by its applicable implementation profile or profiles. | S08, S45, S55 |
| PE-IMPL-002 | RF-38 | MUST | Every implementation | Implementation identity MUST be stable and sufficient to distinguish the implementation from other implementations and materially different implementation versions. | S45 |
| PE-IMPL-003 | RF-38 | MUST | Every implementation | The implementation MUST declare a bounded realization scope identifying the roles, capabilities, interfaces, protocol generation, Protocol Specification, and implementation profiles it claims to realize. | S08, S10, S44, S45, S55 |
| PE-IMPL-004 | RF-38 | MUST | Every materially changed implementation version | A materially changed version MUST remain separately identifiable where the change affects applicable obligations, externally observable normative behavior, compatibility, or assessment. | S15, S45 |
| PE-IMPL-005 | RF-38 | MAY | Every implementation | An implementation MAY use multiple components, algorithms, languages, processes, services, storage structures, transports, and deployment mechanisms where every applicable requirement permits that variation. | S20, S45, S46 |
| PE-IMPL-006 | RF-38 | MUST | Every component used by an implementation | Component identity, responsibility, and failure MUST remain attributable to the implementation scope without becoming independent protocol identity or protocol authority. | S20, S44, S45 |
| PE-IMPL-007 | RF-38 | MUST | Every implementation deployment or operational instance | Deployment and instance identity MUST remain distinct from implementation identity, implementation-version identity, profile identity, protocol identity, and Private Actor identity. | S01, S18, S43, S45 |
| PE-IMPL-008 | RF-38 | MUST NOT | Every implementation identifier | An implementation identifier MUST NOT be interpreted as a protocol-generation identifier, Protocol Specification identifier, implementation-profile identifier, reference designation, conformance identity, certification identity, Protocol Action identity, or Private Actor identity. | S01, S08, S18, S45, S55, S56 |
| PE-IMPL-009 | RF-38 | MUST | Every implementation | The implementation MUST satisfy every normative requirement applicable through its identified profile, including applicable success, rejection, failure, privacy, observability, and authority requirements. | S05, S06, S44, S45, S55 |
| PE-IMPL-010 | RF-38 | MUST | Every implementation claiming a requirement is non-applicable | The claim MUST derive from the requirement's published applicability rule and the applicable profile scope rather than implementation preference or existing behavior. | S04, S05, S45, S55 |
| PE-IMPL-011 | RF-38 | MAY | Every implementation-facing choice explicitly permitted by the applicable profile | The implementation MAY select a choice only within the complete bounded choice space permitted by the Protocol Specification and resolved or retained by the applicable profile. | S45, S55 |
| PE-IMPL-012 | RF-38 | MUST NOT | Every implementation | Implementation convenience, cost, infrastructure limitation, preferred result, deployment topology, storage model, transport model, local policy, or existing behavior MUST NOT become protocol discretion or an exception to an applicable requirement. | S20, S21, S44, S45 |
| PE-IMPL-013 | RF-38 | MAY | Multiple implementations of the same applicable profile | Implementations MAY differ technically where every difference remains within permitted implementation choice and preserves equivalent protocol-observable semantics. | S45, S46, S55 |
| PE-IMPL-014 | RF-38 | MUST | Every permitted implementation variation | The variation MUST preserve every applicable requirement, semantic subject, identity distinction, ordering rule, failure behavior, privacy guarantee, and observable protocol outcome. | S18, S44, S45, S46 |
| PE-IMPL-015 | RF-38 | MUST | Every implementation failure | Failure MUST remain explicit, bounded to the failed realization responsibility, and distinguishable from protocol invalidity and from alteration of the governing requirement. | S18, S27, S44, S45 |
| PE-IMPL-016 | RF-38 | MUST NOT | Every implementation name, identifier, version, component, deployment, instance, log, diagnostic, test, and observability surface | The surface MUST NOT identify a Private Actor, create reusable participant identity, create cross-action linkage, or compose implementation metadata into an actor-reconstruction bridge. | S01, S18, S20, S44, S45 |

### 32.2 Protocol Realization

Protocol realization is the bounded preservation relationship through which an
identified implementation realizes applicable published protocol semantics.

The relationship is:

> implementation realizes protocol semantics

not:

> implementation defines protocol semantics

#### 32.2.1 RF-39 — Protocol Realization

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-REALIZE-001 | RF-39 | MUST | Every claimed Protocol Realization | The realization MUST identify one implementation, one applicable Protocol Specification and published protocol generation, the applicable implementation profile or profiles, and one bounded realization scope. | S08, S10, S45, S46, S55 |
| PE-REALIZE-002 | RF-39 | MUST | Every Protocol Realization relationship | The relationship MUST remain a bounded preservation relation between its identified implementation and upstream semantic target rather than a new source of protocol semantics or protocol identity. | S10, S12, S45, S46 |
| PE-REALIZE-003 | RF-39 | MUST | Every implementation realizing an applicable requirement | The implementation MUST preserve the complete meaning, strength, applicability, identity distinctions, conditions, success behavior, and failure behavior of that requirement. | S05, S06, S45, S46, S55 |
| PE-REALIZE-004 | RF-39 | MUST | Every successful realization of an upstream semantic subject | Every later realization layer MUST preserve the same selected subject `T` throughout the declared scope. | S18, S27, S46 |
| PE-REALIZE-005 | RF-39 | MUST | Every realization unable to preserve an applicable subject or requirement | The realization MUST fail explicitly rather than claim successful realization. | S44, S45, S46 |
| PE-REALIZE-006 | RF-39 | MUST NOT | Every Protocol Realization | A realization MUST NOT repair, reinterpret, widen, narrow, merge, divide, substitute, infer, or invent replacement protocol meaning `T'` for the applicable meaning `T`. | S18, S44, S46 |
| PE-REALIZE-007 | RF-39 | MUST NOT | Every Protocol Realization | A realization MUST NOT omit an applicable mandatory requirement or treat a prohibited behavior as a permitted technical choice. | S05, S06, S45, S46, S55 |
| PE-REALIZE-008 | RF-39 | MUST | Every complete realization claim | The claim MUST account for every requirement applicable within its declared scope and for every declared dependency of the applicable profile. | S06, S08, S45, S46, S55 |
| PE-REALIZE-009 | RF-39 | MAY | Multiple realizations of the same applicable profile | Multiple realizations MAY use different internal and operational means where each independently preserves the same required protocol-observable semantics. | S45, S46, S55 |
| PE-REALIZE-010 | RF-39 | MUST | Every realization-specific extension | The extension MUST remain outside protocol semantics without conflicting with, weakening, obscuring, or expanding any applicable protocol obligation. | S21, S44, S45, S46 |
| PE-REALIZE-011 | RF-39 | MUST | Every realization record, report, or diagnostic | The surface MUST remain bounded to realization status and MUST preserve SF-04 privacy, neutral naming, and non-correlation requirements. | S01, S18, S44, S46 |
| PE-REALIZE-012 | RF-39 | MUST NOT | Every implementation and realization | Realizing protocol semantics MUST NOT be interpreted as defining the protocol generation, Protocol Specification, implementation profile, conformance, certification, or protocol authority. | S08, S10, S12, S45, S46, S55 |

### 32.3 Complete Prohibition of Downstream Protocol Authority

RF-40 is the authoritative home for the cross-realization prohibition against
downstream semantic authority.

Local application, adapter, and runtime boundaries in SF-12 remain supporting
applications of this complete prohibition.

#### 32.3.1 RF-40 — Prohibited Implementation, Runtime, Application, and Assessment Authority

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-DOWNAUTH-001 | RF-40 | MUST NOT | Every application, adapter, runtime, integration, implementation, realization, compatibility structure, profile, reference implementation, assessment, report, deployment, and operational surface | A downstream structure or surface MUST NOT acquire or claim protocol authority. | S10, S12, S20, S21, S43, S44, S45, S46, S47 |
| PE-DOWNAUTH-002 | RF-40 | MUST NOT | Every downstream structure or surface | It MUST NOT redefine, replace, amend, supersede, or mutate the identity, membership, publication state, lineage, lifecycle, semantics, or authority of a published protocol generation or Protocol Specification. | S08, S10, S12, S20, S21 |
| PE-DOWNAUTH-003 | RF-40 | MUST NOT | Every downstream structure or surface | It MUST NOT redefine privacy, anonymity, unlinkability, minimum disclosure, actor separation, reusable-identity prohibitions, or compositional-correlation prohibitions. | S01, S18, S20, S21, S44 |
| PE-DOWNAUTH-004 | RF-40 | MUST NOT | Every downstream structure or surface | It MUST NOT redefine proof relations, declared public inputs, verification semantics, evidence meaning, or complete protocol validity. | S18, S20, S21 |
| PE-DOWNAUTH-005 | RF-40 | MUST NOT | Every downstream structure or surface | It MUST NOT redefine Protocol Operation, Protocol Action, applicable-rule, Evaluation, Determination, acceptance, rejection, or accepted no-transition semantics. | S18, S21, S43, S45 |
| PE-DOWNAUTH-006 | RF-40 | MUST NOT | Every downstream structure or surface | It MUST NOT redefine transition mapping, transition-occurrence identity, authorization, execution, commitment, state, history, consequence, failure, staleness, or re-evaluation semantics. | S18, S27, S35, S43, S45 |
| PE-DOWNAUTH-007 | RF-40 | MUST NOT | Every compatibility, profile, reference, conformance, or certification structure | It MUST NOT redefine compatibility truth, profile obligations, conformance, certification, or the upstream semantic basis against which those downstream relationships are evaluated. | S08, S18, S45, S46, S48, S55, S56 |
| PE-DOWNAUTH-008 | RF-40 | MUST NOT | Every implementation behavior, compatibility declaration, assessment result, diagnostic, test result, deployment record, report, or observability surface | The surface MUST NOT be promoted into protocol truth or used to repair, infer, or replace upstream protocol meaning. | S18, S20, S44, S45, S46, S48 |
| PE-DOWNAUTH-009 | RF-40 | MUST | Every conflict between a downstream artifact and its governing upstream requirement | The conflict MUST be resolved in favor of the governing upstream requirement, and the downstream artifact MUST be corrected, narrowed, withdrawn, superseded, or reported as failed. | S08, S10, S12, S44, S45, S46 |
| PE-DOWNAUTH-010 | RF-40 | MUST | Every downstream derivation and realization path | The path MUST preserve the direction `Published Protocol Generation -> Protocol Specification -> Implementation Profile -> Implementation -> Conformance -> Certification` without upward authority transfer. | S02, S08, S10, S18, S45, S55, S56 |

### 32.4 Compatibility Architecture

Compatibility is a bounded declared or assessed relationship between one
identified implementation and one identified published protocol generation
across one declared compatibility surface and scope.

The compatibility architecture contains distinct targets, surfaces,
statements, profiles, declarations, and assessments.

Compatibility does not establish protocol succession, semantic equivalence,
conformance, or certification.

#### 32.4.1 RF-41 — Compatibility Targets, Surfaces, Statements, Profiles, Declarations, and Assessment

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-COMPAT-001 | RF-41 | MUST | Every compatibility relationship | The relationship MUST identify one implementation, one implementation version where relevant, one compatibility target, one compatibility surface, and one bounded compatibility scope. | S45, S48, S50, S54 |
| PE-COMPAT-002 | RF-41 | MUST | Every Compatibility Target | A Compatibility Target MUST identify exactly one published protocol generation used as the reference for the bounded compatibility relationship. | S10, S12, S54 |
| PE-COMPAT-003 | RF-41 | MUST | Every identified Compatibility Target | Target identity MUST remain distinct from the identity of the referenced protocol generation, implementation, deployment, surface, statement, profile, declaration, assessment, conformance object, and certification object. | S18, S54 |
| PE-COMPAT-004 | RF-41 | MUST | Every Compatibility Surface | A Compatibility Surface MUST identify the bounded set of published capabilities from one identified compatibility target that is covered by the compatibility statement or assessment. | S22, S53, S54 |
| PE-COMPAT-005 | RF-41 | MUST | Every Compatibility Surface | The surface MUST be complete within its declared scope and MUST explicitly identify every included capability and every permitted exclusion. | S22, S48, S53 |
| PE-COMPAT-006 | RF-41 | MUST NOT | Every Compatibility Surface | A Compatibility Surface MUST NOT be identified with a Protocol Surface, silently omit an applicable declared capability, or imply compatibility outside its bounded scope. | S22, S53 |
| PE-COMPAT-007 | RF-41 | MUST | Every Compatibility Statement | A Compatibility Statement MUST be a bounded assertion by or about one identified implementation concerning one identified target and one identified surface. | S52, S53, S54 |
| PE-COMPAT-008 | RF-41 | MUST | Every Compatibility Statement | The statement MUST identify its implementation, implementation version where relevant, target, surface, declared scope, claim boundary, and statement identity. | S45, S52, S53, S54 |
| PE-COMPAT-009 | RF-41 | MUST NOT | Every Compatibility Statement | A statement MUST NOT be interpreted as proof of realization, proof of compatibility, conformance, certification, protocol succession, or protocol authority. | S48, S52 |
| PE-COMPAT-010 | RF-41 | MUST | Every Compatibility Profile | A Compatibility Profile MUST remain a bounded aggregation of identified Compatibility Statements associated with one identified implementation. | S51, S52 |
| PE-COMPAT-011 | RF-41 | MUST | Every Compatibility Profile | The profile MUST preserve the identity, target, surface, scope, and asserted meaning of each aggregated statement without merging their target or statement identities. | S51, S52, S54 |
| PE-COMPAT-012 | RF-41 | MUST NOT | Every Compatibility Profile | A Compatibility Profile MUST NOT be treated as an Implementation Profile, MUST NOT select normative implementation obligations, and MUST NOT establish compatibility merely by aggregation. | S48, S51, S55 |
| PE-COMPAT-013 | RF-41 | MUST | Every Compatibility Declaration | A Compatibility Declaration MUST remain the complete identified record of one declared compatibility relationship concerning one implementation, one target, one surface, and one bounded scope. | S49, S52, S53, S54 |
| PE-COMPAT-014 | RF-41 | MUST | Every Compatibility Declaration | The declaration MUST preserve the complete constituent identities, statement provenance, declared scope, version information, and declared compatibility meaning required by its governing compatibility model. | S49, S50, S52, S53, S54 |
| PE-COMPAT-015 | RF-41 | MUST NOT | Every Compatibility Declaration | Publication or persistence of a declaration MUST NOT convert declared compatibility into realized compatibility, protocol truth, conformance, or certification. | S48, S49, S50 |
| PE-COMPAT-016 | RF-41 | MUST | Every Compatibility Assessment | A Compatibility Assessment MUST evaluate only the identified declared compatibility relationship against its identified target, surface, scope, applicable protocol invariants, and available bounded evidence. | S48, S49, S50, S53, S54 |
| PE-COMPAT-017 | RF-41 | MUST | Every Compatibility Assessment report | The report MUST identify its assessed implementation, target, surface, scope, basis, limitations, and bounded result without creating a separate protocol truth or conformance determination. | S48, S50, S53, S54 |
| PE-COMPAT-018 | RF-41 | MUST | Every compatibility target, surface, statement, profile, declaration, and assessment | Each structure MUST retain its own bounded identity and role and MUST remain distinct from every other compatibility structure. | S49, S50, S51, S52, S53, S54 |
| PE-COMPAT-019 | RF-41 | MUST NOT | Every compatibility claim or assessment | Compatibility MUST NOT establish Protocol Succession, Protocol Lineage membership, migration eligibility, generation replacement, or retirement. | S13, S14, S15, S16, S48 |
| PE-COMPAT-020 | RF-41 | MUST NOT | Every compatibility claim or assessment | Compatibility MUST NOT merge protocol-generation identities or establish complete semantic equivalence between distinct generations or implementations. | S13, S15, S16, S48 |
| PE-COMPAT-021 | RF-41 | MUST NOT | Every compatibility structure or assessment | Compatibility MUST NOT be interpreted as an Implementation Profile, complete Protocol Realization, conformance claim, conformance assessment, conformance determination, certification basis, certification decision, certification status, or certification recognition. | S18, S48, S50, S51, S55, S56 |
| PE-COMPAT-022 | RF-41 | MUST | Every compatibility consequence of protocol evolution or migration | The consequence MUST preserve RF-04 ownership of succession, lineage, versioning, deprecation, migration, coexistence, and retirement and MUST identify the affected target and surface explicitly. | S13, S14, S15, S16, S48, S54 |
| PE-COMPAT-023 | RF-41 | MUST | Every failed, superseded, withdrawn, or historically retained compatibility statement, declaration, or assessment | Its lifecycle status MUST remain explicit without mutating the identity or semantics of the target generation, implementation, surface, or historical compatibility record. | S15, S49, S50, S52, S53, S54 |
| PE-COMPAT-024 | RF-41 | MUST NOT | Every compatibility identifier, statement, declaration, assessment, field, diagnostic, test, report, and observability surface | The surface MUST NOT identify a Private Actor, carry enrollment or admission provenance, create reusable participant identity, create cross-action linkage, or compose compatibility metadata into an actor-reconstruction bridge. | S01, S18, S20, S44, S48, S49, S50, S51, S52, S53, S54 |

### 32.5 SF-13 Formal Summary

The realization invariant is:

> selectedMeaning(T)
> -> preservedByImplementation(T)

Success path:

> T -> preserved(T)

Failure path:

> T -> realizationFailure

Forbidden path:

> T -> T'

where:

> T' != T

Compatibility preserves bounded identity:

> compatibility(I, Target, Surface, Scope)

> compatibility(I, Target, Surface, Scope)
> =/=> succession(Target)

> compatibility(I, Target, Surface, Scope)
> =/=> semanticEquivalence(I, Target)

> compatibility(I, Target, Surface, Scope)
> =/=> conformance(I)

> compatibility(I, Target, Surface, Scope)
> =/=> certification(I)

Protocol authority always remains with the published Privacy Engine protocol generation.

## 33. SF-14 — Implementation Profiles and Reference Implementations

SF-14 defines the bounded applicability layer between the Protocol
Specification and implementations and the bounded role of designated,
inspectable reference implementations.

An Implementation Profile selects and organizes applicable requirements.

A Reference Implementation realizes a profile.

Neither defines protocol semantics.

### 33.1 Implementation Profiles

A Privacy Engine Implementation Profile is a uniquely identified, bounded, and
complete implementation-facing selection and organization of applicable
normative requirements derived from one Privacy Engine Protocol Specification.

Completeness is bounded completeness within the declared profile scope.

#### 33.1.1 RF-42 — Implementation Profiles

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-PROFILE-001 | RF-42 | MUST | Every Privacy Engine Implementation Profile | A profile MUST be one uniquely identified, bounded, and complete implementation-facing selection and organization of applicable normative requirements derived from one identified Privacy Engine Protocol Specification. | S08, S55 |
| PE-PROFILE-002 | RF-42 | MUST | Every Implementation Profile | Profile identity MUST distinguish the profile from its source specification, other profiles, compatibility profiles, implementations, reference implementations, conformance artifacts, and certifications. | S18, S51, S55, S56 |
| PE-PROFILE-003 | RF-42 | MUST | Every Implementation Profile | The profile MUST identify one bounded implementation target by role, capability set, deployment class, operational responsibility, or another specification-permitted implementation category. | S55 |
| PE-PROFILE-004 | RF-42 | MUST | Every Implementation Profile | The profile MUST identify exactly one source Protocol Specification and the published protocol generation from which that specification derives. | S08, S10, S55 |
| PE-PROFILE-005 | RF-42 | MUST | Every Implementation Profile | The profile MUST declare a precise scope sufficient to resolve the applicability of every normative requirement relevant to its target. | S05, S06, S55 |
| PE-PROFILE-006 | RF-42 | MUST | Every requirement relevant to an Implementation Profile target | The profile MUST record the requirement as applicable, non-applicable under an identified specification rule, conditionally applicable, or resolved through a permitted specification choice. | S05, S06, S55 |
| PE-PROFILE-007 | RF-42 | MUST NOT | Every Implementation Profile applicability decision | Applicability MUST NOT be invented from preference, convenience, implementation difficulty, existing implementation behavior, deployment topology, or a desired assessment result. | S05, S45, S55 |
| PE-PROFILE-008 | RF-42 | MUST | Every requirement selected by an Implementation Profile | Selection MUST reference the same stable normative requirement defined by the source Protocol Specification and MUST preserve its identity. | S05, S06, S08, S55 |
| PE-PROFILE-009 | RF-42 | MUST | Every applicable requirement in an Implementation Profile | The profile MUST preserve the requirement's complete meaning, operative strength, applicability conditions, prohibitions, permissions, success behavior, and failure behavior unchanged. | S04, S05, S55 |
| PE-PROFILE-010 | RF-42 | MAY | Every choice explicitly permitted by the source Protocol Specification | A profile MAY resolve, constrain, require support for, exclude, or leave the choice implementation-defined only within the choice space permitted by the specification. | S08, S55 |
| PE-PROFILE-011 | RF-42 | MUST NOT | Every Implementation Profile | A profile MUST NOT invent a choice, widen a choice space, treat mandatory behavior as optional, permit prohibited behavior, or omit a mandatory choice that must be resolved at profile level. | S05, S08, S55 |
| PE-PROFILE-012 | RF-42 | MUST | Every Implementation Profile composition | The composition MUST identify the profile, source specification, target, scope, applicability decisions, permitted-choice resolutions, dependencies, and completeness conditions without duplicating normative requirements. | S06, S07, S08, S55 |
| PE-PROFILE-013 | RF-42 | MUST | Every Implementation Profile dependency | The dependency MUST identify the depended-upon profile, direction, applicability condition, and required obligation boundary without merging profile identities or transferring authority. | S55 |
| PE-PROFILE-014 | RF-42 | MUST | Every Implementation Profile | The profile MUST account for every requirement relevant to its declared scope and MUST fail profile construction when any applicable obligation, applicability decision, required choice, or dependency remains unresolved. | S06, S55 |
| PE-PROFILE-015 | RF-42 | MUST | Every semantically changed Implementation Profile | A change to scope, applicability, dependencies, requirement selection, or resolved choices MUST produce a distinguishable profile version or identity where retaining the prior identity would imply unchanged obligations. | S15, S55 |
| PE-PROFILE-016 | RF-42 | MAY | One Protocol Specification | Multiple Implementation Profiles MAY derive from the same specification where each profile has a distinct identity, bounded target, complete applicability resolution, and preserved requirement semantics. | S08, S55 |
| PE-PROFILE-017 | RF-42 | MUST NOT | Every Implementation Profile | A profile MUST NOT modify, replace, weaken, strengthen, supersede, or become the Protocol Specification or published protocol generation from which it derives. | S08, S10, S55 |
| PE-PROFILE-018 | RF-42 | MUST NOT | Every Implementation Profile | A profile MUST NOT be identified with an implementation, Compatibility Profile, conformance assessment, conformance determination, certification basis, certification decision, certification status, or certification recognition. | S18, S51, S55, S56 |
| PE-PROFILE-019 | RF-42 | MUST NOT | Every incomplete Protocol Specification | A complete final Implementation Profile MUST NOT be published from an incomplete Protocol Specification. | S03, S07, S08, S55 |
| PE-PROFILE-020 | RF-42 | MUST | Every profile construction or preservation failure | The profile MUST fail rather than invent, repair, weaken, strengthen, merge, divide, reinterpret, or infer a replacement requirement. | S05, S18, S55 |
| PE-PROFILE-021 | RF-42 | MUST NOT | Every profile identifier, applicability record, choice record, dependency, report, example, diagnostic, and observability surface | The surface MUST NOT identify a Private Actor, create reusable participant identity, create cross-action linkage, or convert implementation-target metadata into an actor-reconstruction bridge. | S01, S18, S20, S55 |

### 33.2 Reference Implementations

A Privacy Engine Reference Implementation is one identified implementation
explicitly designated as an inspectable realization of one identified
Implementation Profile within one declared reference scope.

Reference status is downstream recognition of an implementation role.

It is not protocol authority, conformance, or certification.

#### 33.2.1 RF-43 — Reference Implementations

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-REFIMPL-001 | RF-43 | MUST | Every Privacy Engine Reference Implementation | A Reference Implementation MUST be one identified implementation explicitly designated as an inspectable realization of one identified Implementation Profile within one declared reference scope. | S45, S55, S56 |
| PE-REFIMPL-002 | RF-43 | MUST | Every Reference Implementation | Reference-implementation identity MUST distinguish the implementation, version, realized profile, reference scope, and reference status from every other reference realization. | S45, S55, S56 |
| PE-REFIMPL-003 | RF-43 | MUST | Every reference designation | Reference status MUST be explicit, bounded to one identified implementation-profile relationship and scope, and independently reviewable. | S55, S56 |
| PE-REFIMPL-004 | RF-43 | MUST NOT | Every reference designation | Designation MUST NOT be interpreted as protocol publication, protocol authority, automatic conformance, certification, compatibility, defect freedom, or exclusive implementation status. | S10, S12, S48, S56 |
| PE-REFIMPL-005 | RF-43 | MUST | Every Reference Implementation | The declared reference scope MUST identify exactly which profile obligations, capability set, version, and implementation boundary the reference status covers. | S55, S56 |
| PE-REFIMPL-006 | RF-43 | MUST | Every Reference Implementation realizing an Implementation Profile | The implementation MUST realize every applicable profile requirement within its declared reference scope. | S45, S46, S55, S56 |
| PE-REFIMPL-007 | RF-43 | MUST | Every Reference Implementation | The implementation MUST preserve the applicable profile's required success behavior, failure behavior, privacy constraints, identity separations, and authority boundaries. | S18, S45, S46, S55, S56 |
| PE-REFIMPL-008 | RF-43 | MAY | Every Reference Implementation | A Reference Implementation MAY select one implementation choice where that choice is explicitly permitted by the applicable profile. | S45, S55, S56 |
| PE-REFIMPL-009 | RF-43 | MUST NOT | Every implementation choice selected by a Reference Implementation | The selected choice MUST NOT become a universal requirement, profile amendment, specification amendment, or prohibition against another permitted realization. | S45, S55, S56 |
| PE-REFIMPL-010 | RF-43 | MAY | One Implementation Profile | Multiple Reference Implementations MAY realize the same profile where each independently satisfies every applicable obligation within its declared scope. | S55, S56 |
| PE-REFIMPL-011 | RF-43 | MAY | One implementation realizing multiple Implementation Profiles | The implementation MAY hold separate reference status for multiple profiles only where each profile relationship, version, scope, dependencies, and designation remain explicitly and independently identified. | S55, S56 |
| PE-REFIMPL-012 | RF-43 | MUST | Every materially changed Reference Implementation version | A materially changed version MUST remain separately identifiable where the change affects profile realization, permitted-choice resolution, normative behavior, interoperability behavior, defect status, or reference scope. | S15, S56 |
| PE-REFIMPL-013 | RF-43 | MUST | Every maintained Reference Implementation version | The version MUST remain sufficiently stable, available, and inspectable to support its declared reference uses without silently rewriting its identified historical behavior. | S56 |
| PE-REFIMPL-014 | RF-43 | MUST | Every detected Reference Implementation defect or divergence | The defect or divergence MUST be evaluated against the applicable profile without redefining, weakening, strengthening, or repairing the profile requirement. | S55, S56 |
| PE-REFIMPL-015 | RF-43 | MUST | Every Reference Implementation unable to preserve an applicable obligation | The implementation MUST fail explicitly, and its implementation or designation MUST be corrected, narrowed, suspended, withdrawn, or superseded as appropriate. | S45, S46, S55, S56 |
| PE-REFIMPL-016 | RF-43 | MUST | Every ordinary implementation compared with a Reference Implementation | The ordinary implementation MUST be evaluated against its applicable profile rather than against incidental structure or behavior of the Reference Implementation. | S45, S55, S56 |
| PE-REFIMPL-017 | RF-43 | MUST NOT | Every ordinary implementation | An ordinary implementation MUST NOT be required to copy reference source structure, language, algorithms, storage, deployment topology, APIs, logging, timing, or other behavior not required by the applicable profile. | S45, S55, S56 |
| PE-REFIMPL-018 | RF-43 | MAY | Every conformance, certification, compatibility, testing, or interoperability activity | The activity MAY use a Reference Implementation as supporting evidence, comparison behavior, test infrastructure, fixture, peer, or implementation example. | S48, S55, S56 |
| PE-REFIMPL-019 | RF-43 | MUST NOT | Every conformance, certification, or compatibility activity using a Reference Implementation | Agreement, interoperability, code reuse, designation, or behavioral similarity MUST NOT replace the applicable conformance basis, certification basis, or bounded compatibility assessment. | S48, S55, S56 |
| PE-REFIMPL-020 | RF-43 | MUST | Every disagreement between a Reference Implementation and an upstream requirement | The disagreement MUST be resolved against the applicable Implementation Profile, Protocol Specification, and published protocol generation in that order of derivation. | S08, S10, S55, S56 |
| PE-REFIMPL-021 | RF-43 | MUST NOT | Every reference identifier, designation, implementation record, version, test, diagnostic, report, log, and observability surface | The surface MUST NOT identify a Private Actor, create reusable participant identity, create cross-action linkage, or compose reference-implementation metadata into an actor-reconstruction bridge. | S01, S18, S20, S56 |

### 33.3 SF-14 Formal Summary

The profile path is:

> PublishedProtocolGeneration(P)
> -> ProtocolSpecification(S)
> -> ImplementationProfile(F)
> -> Implementation(I)

For every applicable requirement:

> applies(F, R)
> -> semantics(F, R) = semantics(S, R)

> applies(F, R)
> -> strength(F, R) = strength(S, R)

Profile failure preserves meaning:

> cannotPreserve(F, R)
> -> profileConstructionFailure(F)

Reference realization remains downstream:

> referenceImplementation(Ir, F)
> -> implements(Ir, F)

> behavior(Ir)
> =/=> definesRequirement(F)

> designation(Ir, F)
> =/=> conformance(Ir, F)

> designation(Ir, F)
> =/=> certification(Ir, F)

Protocol authority always remains with the published Privacy Engine protocol generation.

## 34. SF-15 — Conformance and Certification

SF-15 defines the bounded downstream structures through which implementation
satisfaction is expressed, supported, evaluated, determined, and recognized.

Conformance evaluates implementation satisfaction.

Certification recognizes bounded conformance.

Neither creates protocol obligations, protocol semantics, Private Actor
identity, or protocol authority.

### 34.1 Published Conformance Requirements and Requirement Sets

A Published Conformance Requirement is one identified assessable expression of
one existing applicable normative requirement.

A Published Conformance Requirement Set is one identified, immutable, and
complete collection of applicable Published Conformance Requirements within
one declared assessment target and scope.

#### 34.1.1 RF-44 — Published Conformance Requirements and Requirement Sets

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-CONFREQ-001 | RF-44 | MUST | Every Published Conformance Requirement | The requirement MUST be one bounded assessable expression of one existing applicable normative requirement. | S05, S57 |
| PE-CONFREQ-002 | RF-44 | MUST | Every Published Conformance Requirement | The requirement MUST possess a stable identity distinct from its source normative requirement. | S05, S57 |
| PE-CONFREQ-003 | RF-44 | MUST | Every Published Conformance Requirement | The requirement MUST identify its source normative requirement, Protocol Specification, and published protocol generation. | S08, S57 |
| PE-CONFREQ-004 | RF-44 | MUST | Every conformance derivation | Derivation MUST preserve source-requirement identity, complete normative meaning, and source traceability. | S05, S57 |
| PE-CONFREQ-005 | RF-44 | MUST | Every conformance derivation | Derivation MUST preserve operative strength, applicability conditions, and permitted-choice boundaries. | S04, S05, S57 |
| PE-CONFREQ-006 | RF-44 | MUST NOT | Every Published Conformance Requirement | The requirement MUST NOT create, remove, weaken, strengthen, repair, reinterpret, or replace a protocol obligation. | S05, S57 |
| PE-CONFREQ-007 | RF-44 | MUST | Every published Conformance Requirement | Publication MUST make identity, source, meaning, strength, applicability, version, and traceability independently reviewable. | S57 |
| PE-CONFREQ-008 | RF-44 | MUST | Every published Conformance Requirement | The published requirement MUST remain immutable; semantic change MUST create a distinguishable requirement. | S15, S57 |
| PE-CONFREQ-009 | RF-44 | MUST | Every Published Conformance Requirement Set | The set MUST be one identified, bounded, immutable collection of applicable Published Conformance Requirements. | S58 |
| PE-CONFREQ-010 | RF-44 | MUST | Every Conformance Requirement Set | Set identity MUST distinguish its target, scope, version, composition, and source generation. | S58 |
| PE-CONFREQ-011 | RF-44 | MUST | Every Conformance Requirement Set | The set MUST identify exactly one bounded assessment target and one declared assessment scope. | S55, S58 |
| PE-CONFREQ-012 | RF-44 | MUST | Every complete Conformance Requirement Set | The set MUST contain every and only Published Conformance Requirements applicable within its declared target and scope. | S06, S58 |
| PE-CONFREQ-013 | RF-44 | MUST | Every Conformance Requirement Set constituent | Composition MUST preserve constituent identity, meaning, strength, applicability, ordering where relevant, and traceability. | S05, S06, S58 |
| PE-CONFREQ-014 | RF-44 | MUST NOT | Every Conformance Requirement Set | The set MUST NOT evaluate an implementation, become an Implementation Profile, create obligations, or acquire protocol authority. | S55, S58 |

### 34.2 Conformance Artifacts, Evidence, and Packages

A Conformance Artifact records bounded objective implementation information.

Conformance Evidence provides complete traceable support for one claim and
scope.

A Conformance Package publishes preserved constituents for one bounded
assessment.

#### 34.2.1 RF-45 — Conformance Artifacts, Evidence, and Packages

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-CONFEVID-001 | RF-45 | MUST | Every Conformance Artifact | An artifact MUST be one bounded, immutable, referenceable unit documenting objective implementation information relevant to conformance. | S59 |
| PE-CONFEVID-002 | RF-45 | MUST | Every Conformance Artifact | Artifact identity MUST distinguish the artifact, implementation, version, assessment scope, and recorded information. | S59 |
| PE-CONFEVID-003 | RF-45 | MUST | Every Conformance Artifact | The artifact MUST preserve integrity, provenance, authorship or production context, and reference stability. | S59 |
| PE-CONFEVID-004 | RF-45 | MUST | Every Conformance Artifact | Artifact content MUST remain objective, reviewable, and attributable to its declared implementation boundary. | S59 |
| PE-CONFEVID-005 | RF-45 | MUST | Every artifact used as evidence | Use as evidence MUST preserve artifact identity and MUST record the evidentiary relationship separately. | S59, S60 |
| PE-CONFEVID-006 | RF-45 | MUST NOT | Every Conformance Artifact | An artifact MUST NOT establish correctness, conformance, certification, protocol truth, or protocol authority merely by existing. | S59 |
| PE-CONFEVID-007 | RF-45 | MUST | Every Conformance Evidence set | Evidence MUST be one identified, published, complete, and traceable support set for one claim and declared scope. | S60 |
| PE-CONFEVID-008 | RF-45 | MUST | Every Conformance Evidence set | Evidence identity MUST distinguish its claim, implementation, profile, requirement set, scope, version, and constituent artifacts. | S60 |
| PE-CONFEVID-009 | RF-45 | MUST | Every evidence constituent | Evidence MUST trace each supported claim element to applicable requirements and preserved artifacts. | S57, S60 |
| PE-CONFEVID-010 | RF-45 | MUST | Every complete Conformance Evidence set | Evidence MUST account for every applicable conformance requirement within its declared evidentiary scope. | S58, S60 |
| PE-CONFEVID-011 | RF-45 | MAY | Every Conformance Evidence set | Evidence MAY compose testing, inspection, analysis, review, measurement, and preserved artifacts. | S60, S64 |
| PE-CONFEVID-012 | RF-45 | MUST NOT | Every Conformance Evidence set | Evidence MUST NOT perform assessment, determine conformance, establish certification, or become protocol truth. | S60, S64 |
| PE-CONFEVID-013 | RF-45 | MUST | Every Conformance Package | A package MUST be one canonical, identified, immutable publication unit for one bounded conformance assessment. | S61 |
| PE-CONFEVID-014 | RF-45 | MUST | Every Conformance Package | Package identity MUST distinguish its implementation, profile, claim, scope, version, evidence, artifacts, and publication. | S61 |
| PE-CONFEVID-015 | RF-45 | MUST | Every Conformance Package | The package MUST identify its artifacts, evidence, claim references, applicable requirement set, scope, and traceability. | S58, S61 |
| PE-CONFEVID-016 | RF-45 | MUST | Every published Conformance Package | The package MUST remain immutable; changed composition MUST create a distinguishable package. | S15, S61 |
| PE-CONFEVID-017 | RF-45 | MUST | Every Conformance Package constituent | Packaging MUST preserve constituent identity, content, integrity, provenance, scope, and independent meaning. | S59, S60, S61 |
| PE-CONFEVID-018 | RF-45 | MUST NOT | Every Conformance Package | The package MUST NOT merge constituents, perform assessment, or establish conformance by publication. | S61, S64 |
| PE-CONFEVID-019 | RF-45 | MUST NOT | Every Conformance Package | The package MUST NOT constitute certification or replace a Certification Basis, Decision, Status, or recognition. | S61, S65, S66, S67, S68 |

### 34.3 Conformance Claims, Assessments, and Determinations

A Conformance Claim asserts satisfaction.

A Conformance Assessment evaluates the claim.

A Conformance Determination records the bounded result of one completed
assessment.

#### 34.3.1 RF-46 — Conformance Claims, Assessments, and Determinations

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-CONFORM-001 | RF-46 | MUST | Every Conformance Claim | A claim MUST be one bounded assertion that one identified implementation satisfies one identified Implementation Profile within one declared scope. | S62, S64 |
| PE-CONFORM-002 | RF-46 | MUST | Every Conformance Claim | Claim identity MUST distinguish the assertion, implementation, profile, specification, generation, scope, and version. | S62, S64 |
| PE-CONFORM-003 | RF-46 | MUST | Every Conformance Claim | The claim MUST identify its implementation, implementation version where relevant, profile, specification, generation, and assessment scope. | S62 |
| PE-CONFORM-004 | RF-46 | MUST | Every Conformance Claim | The claim MUST remain bounded to its declared implementation-profile relationship and scope. | S62 |
| PE-CONFORM-005 | RF-46 | MUST NOT | Every Conformance Claim | The claim MUST NOT establish Protocol Realization or replace implementation obligations. | S46, S62 |
| PE-CONFORM-006 | RF-46 | MUST NOT | Every Conformance Claim | The claim MUST NOT perform assessment, produce a determination, establish conformance, or establish certification. | S62, S63, S64, S68 |
| PE-CONFORM-007 | RF-46 | MUST | Every Conformance Assessment | An assessment MUST be one identified bounded evaluation of one identified claim concerning one implementation, profile, and scope. | S63, S64 |
| PE-CONFORM-008 | RF-46 | MUST | Every Conformance Assessment | Assessment identity MUST distinguish the evaluation occurrence, claim, implementation, profile, requirement set, evidence, and scope. | S63, S64 |
| PE-CONFORM-009 | RF-46 | MUST | Every Conformance Assessment | The assessment MUST declare the exact target, applicable requirement set, evidence boundary, and assessment scope. | S58, S60, S63 |
| PE-CONFORM-010 | RF-46 | MUST | Every complete Conformance Assessment | The assessment MUST evaluate every applicable requirement within its declared scope. | S58, S63, S64 |
| PE-CONFORM-011 | RF-46 | MUST | Every Conformance Assessment | The assessment MUST use valid, applicable, integrity-preserved, and traceable evidence. | S59, S60, S63 |
| PE-CONFORM-012 | RF-46 | MUST | Every Conformance Assessment | The assessment MUST evaluate the claim without modifying or becoming the claim. | S62, S63 |
| PE-CONFORM-013 | RF-46 | MUST | Every completed Conformance Assessment | Completion MUST produce at most one distinct Conformance Determination for that assessment occurrence. | S63, S64 |
| PE-CONFORM-014 | RF-46 | MUST | Every assessment unable to reach a supported classification | The assessment MUST fail or remain indeterminate without producing a conformant or non-conformant determination. | S63, S64 |
| PE-CONFORM-015 | RF-46 | MUST | Every Conformance Determination | A determination MUST be the bounded authoritative result of one completed Conformance Assessment. | S64 |
| PE-CONFORM-016 | RF-46 | MUST | Every Conformance Determination | Determination identity MUST distinguish its assessment, implementation, profile, scope, requirement set, and classification. | S64 |
| PE-CONFORM-017 | RF-46 | MUST | Every conformant determination | The determination MUST record satisfaction of every applicable requirement within its declared scope. | S64 |
| PE-CONFORM-018 | RF-46 | MUST | Every non-conformant determination | The determination MUST record that at least one applicable requirement within scope was not satisfied. | S64 |
| PE-CONFORM-019 | RF-46 | MUST | Every Conformance Determination | The determination MUST record exactly one classification: conformant within scope or non-conformant within scope. | S64 |
| PE-CONFORM-020 | RF-46 | MUST | Every Conformance Determination | The determination MUST identify its complete bounded scope; no unstated scope is implied. | S64 |
| PE-CONFORM-021 | RF-46 | MUST NOT | Every partial Conformance Assessment | Partial assessment MUST NOT establish complete conformance beyond the requirements actually assessed. | S64 |
| PE-CONFORM-022 | RF-46 | MUST | Every published Conformance Determination | The historical determination MUST remain immutable and independently identifiable. | S15, S64 |
| PE-CONFORM-023 | RF-46 | MUST | Every correction affecting previous conformance | Correction MUST be evaluated through a new assessment producing a new determination where completed. | S64 |
| PE-CONFORM-024 | RF-46 | MUST | Every conformance or compatibility activity | Conformance satisfaction and compatibility relationships MUST remain distinct. | S48, S64 |
| PE-CONFORM-025 | RF-46 | MUST | Every conformance or certification activity | Conformance determination and certification recognition MUST remain distinct. | S64, S68 |
| PE-CONFORM-026 | RF-46 | MUST | Every conformance authority | Conformance authority MUST remain bounded assessment authority within the declared target and scope. | S64 |
| PE-CONFORM-027 | RF-46 | MUST NOT | Every claim, assessment, determination, evidence object, report, test, diagnostic, identifier, and metadata surface | The surface MUST NOT identify a Private Actor, create reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | S01, S18, S20, S64 |

### 34.4 Certification Bases, Decisions, and Statuses

A Certification Basis defines one immutable evaluation basis.

A Certification Decision records one pass-or-fail result.

Certification Status records the lifecycle state of one certification.

#### 34.4.1 RF-47 — Certification Bases, Decisions, and Statuses

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-CERTDET-001 | RF-47 | MUST | Every Certification Basis | A basis MUST be one complete, immutable, identified evaluation basis for one bounded certification decision. | S65 |
| PE-CERTDET-002 | RF-47 | MUST | Every Certification Basis | Basis identity MUST distinguish its subject, target, scope, requirements, packages, determinations, policy, and version. | S65 |
| PE-CERTDET-003 | RF-47 | MUST | Every complete Certification Basis | The basis MUST identify every criterion and supporting conformance structure required for its declared scope. | S57, S58, S61, S64, S65 |
| PE-CERTDET-004 | RF-47 | MUST | Every published Certification Basis | The basis MUST remain immutable; changed criteria or composition MUST create a distinguishable basis. | S15, S65 |
| PE-CERTDET-005 | RF-47 | MUST | Every Certification Basis | The basis MUST declare one bounded certification subject, target, program context, and scope. | S65, S68 |
| PE-CERTDET-006 | RF-47 | MUST NOT | Every Certification Basis | The basis MUST NOT define its decision result, modify conformance, or create protocol obligations. | S65 |
| PE-CERTDET-007 | RF-47 | MUST | Every Certification Decision | A decision MUST be one identified immutable pass-or-fail evaluation of one subject and package against one basis. | S66 |
| PE-CERTDET-008 | RF-47 | MUST | Every Certification Decision | Decision identity MUST distinguish the subject, package, basis, scope, decision occurrence, and classification. | S66 |
| PE-CERTDET-009 | RF-47 | MUST | Every passing Certification Decision | Pass MUST record that the identified subject and package satisfy the identified basis within scope. | S66 |
| PE-CERTDET-010 | RF-47 | MUST | Every failing Certification Decision | Fail MUST record that the identified subject or package does not satisfy the identified basis within scope. | S66 |
| PE-CERTDET-011 | RF-47 | MUST | Every Certification Decision | The decision MUST record exactly one classification: pass or fail. | S66 |
| PE-CERTDET-012 | RF-47 | MUST | Every Certification Decision | The decision MUST identify the exact Certification Basis against which it was made. | S65, S66 |
| PE-CERTDET-013 | RF-47 | MUST NOT | Every Certification Decision | The decision MUST NOT perform conformance assessment, alter evidence, repair failure, or modify a Conformance Determination. | S64, S66 |
| PE-CERTDET-014 | RF-47 | MUST | Every Certification Status | Status MUST be one recorded lifecycle state of one identified certification. | S67, S68 |
| PE-CERTDET-015 | RF-47 | MUST | Every Certification Status | Status identity MUST distinguish the certification, lifecycle occurrence, effective state, authority, and scope. | S67, S68 |
| PE-CERTDET-016 | RF-47 | MUST | Every certification lifecycle change | The change MUST occur through a defined issuance, maintenance, suspension, withdrawal, expiry, or reassessment event. | S67, S68 |
| PE-CERTDET-017 | RF-47 | MUST | Every Certification Status | Status MUST remain distinct from its supporting Certification Decision and historical decisions. | S66, S67 |
| PE-CERTDET-018 | RF-47 | MUST NOT | Every Certification Status | Status MUST NOT become implementation state, conformance truth, protocol truth, or protocol authority. | S64, S67 |
| PE-CERTDET-019 | RF-47 | MUST | Every certification lifecycle update | The update MUST preserve historical bases, decisions, determinations, and prior status occurrences unchanged. | S64, S65, S66, S67 |

### 34.5 Certification Recognition, Scope, and Authority

A Privacy Engine Certification is bounded recognition of one identified
implementation with respect to one identified Implementation Profile.

Certification is based on identified Conformance Determinations and is issued
by one identified certification authority.

#### 34.5.1 RF-48 — Certification Recognition, Scope, and Authority

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-CERT-001 | RF-48 | MUST | Every Privacy Engine Certification | Certification MUST be one bounded recognition of one identified implementation with respect to one identified Implementation Profile. | S68 |
| PE-CERT-002 | RF-48 | MUST | Every Certification | Certification identity MUST distinguish the recognition, implementation, profile, scope, basis, decisions, determinations, authority, and status. | S68 |
| PE-CERT-003 | RF-48 | MUST | Every Certification | The certification subject MUST be exactly one identified implementation. | S45, S68 |
| PE-CERT-004 | RF-48 | MUST | Every Certification | The certification target MUST be exactly one identified Implementation Profile. | S55, S68 |
| PE-CERT-005 | RF-48 | MUST | Every Certification | Certification MUST apply only within its explicitly declared implementation, profile, determination, and recognition scope. | S64, S68 |
| PE-CERT-006 | RF-48 | MUST | Every Certification | Certification MUST be supported by one or more identified conformant Conformance Determinations covering its declared scope. | S64, S68 |
| PE-CERT-007 | RF-48 | MUST NOT | Every complete-certification claim | Complete certification MUST NOT be claimed unless supporting determinations cover every applicable profile requirement within the declared complete scope. | S64, S68 |
| PE-CERT-008 | RF-48 | MUST | Every partial Certification | Partial recognition MUST explicitly identify its bounded scope and MUST remain distinguishable from complete certification. | S68 |
| PE-CERT-009 | RF-48 | MUST | Every Certification | The issuing certification authority MUST possess a stable identity distinct from the certification and assessed implementation. | S68 |
| PE-CERT-010 | RF-48 | MUST | Every certification authority | The authority MUST declare the certification program, responsibilities, recognition boundary, and scope within which it acts. | S68 |
| PE-CERT-011 | RF-48 | MUST | Every certification authority action | Issuance, maintenance, suspension, withdrawal, and update authority MUST remain bounded by the declared program and scope. | S68 |
| PE-CERT-012 | RF-48 | MUST | Every Certification | Recognition MUST remain distinct from conformance assessment without replacing it. | S63, S64, S68 |
| PE-CERT-013 | RF-48 | MUST | Every certification or compatibility statement | Certification recognition and compatibility MUST remain distinct. | S48, S68 |
| PE-CERT-014 | RF-48 | MUST NOT | Every Certification and certification authority | Neither certification nor its authority MUST become protocol authority or redefine upstream semantics. | S08, S10, S68 |
| PE-CERT-015 | RF-48 | MUST | Every certification withdrawal | Withdrawal MUST change certification status only and MUST preserve implementation, profile, determination, decision, and protocol history. | S64, S66, S67, S68 |
| PE-CERT-016 | RF-48 | MUST | Every certification reassessment | Reassessment MUST use new identified evidence, assessment, determination, basis, or decision occurrences where applicable. | S60, S63, S64, S65, S66, S68 |
| PE-CERT-017 | RF-48 | MUST | Every certification lifecycle | Historical Conformance Determinations and Certification Decisions MUST remain immutable through issuance, withdrawal, correction, and reassessment. | S64, S66, S68 |
| PE-CERT-018 | RF-48 | MUST | Every conformance and certification structure | Public identifiers and records MUST preserve Private Actor separation and action-bounded unlinkability. | S01, S18, S20, S64, S68 |
| PE-CERT-019 | RF-48 | MUST | Every conformance and certification naming surface | Names, fields, routes, storage keys, logs, diagnostics, examples, tests, and reports MUST use neutral non-correlation-bearing terminology. | S01, S18, S20 |
| PE-CERT-020 | RF-48 | MUST NOT | Every conformance and certification composition | Composition MUST NOT expose enrollment provenance, wallet identity, reusable participant identity, cross-action linkage, or an actor-reconstruction bridge. | S01, S18, S20, S64, S68 |

### 34.6 SF-15 Formal Summary

The downstream evaluation and recognition path is:

> PublishedProtocolGeneration(P)
> -> ProtocolSpecification(S)
> -> ImplementationProfile(F)
> -> Implementation(I)
> -> ConformanceAssessment(Ac)
> -> ConformanceDetermination(Dc)
> -> Certification(C)

Conformance preserves applicable requirements:

> assesses(Ac, I, F)
> -> preserves(Ac, requirements(F))

A completed determination records one classification:

> conformant(Dc) xor nonConformant(Dc)

An unsupported or indeterminate assessment does not create a determination:

> cannotDetermine(Ac)
> -> assessmentFailure(Ac)

Certification recognizes bounded conformance:

> certification(C, I, F)
> -> supportedBy(C, Dc)

> certification(C, I, F)
> =/=> performsConformanceAssessment(C)

Protocol authority always remains with the published Privacy Engine protocol generation.

## 35. SF-16 — Protocol-Semantic Preservation and Explicit Exclusions

SF-16 closes the complete specification with global preservation and exclusion
requirements.

It references the authoritative local requirements established by SF-01
through SF-15.

It does not duplicate or replace them.

### 35.1 Protocol-Semantic Preservation

Every downstream layer operates over already-established upstream meaning.

No downstream layer creates upstream meaning.

#### 35.1.1 RF-49 — Protocol-Semantic Preservation

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-SEMPRES-001 | RF-49 | MUST | Every downstream Privacy Engine layer | The layer MUST preserve applicable upstream protocol semantics within its declared role and scope. | S03, S08, S46 |
| PE-SEMPRES-002 | RF-49 | MUST | The complete downstream chain | The chain MUST remain Generation to Specification to Profile to Implementation to Conformance to Certification. | S03, S08, S55, S64, S68 |
| PE-SEMPRES-003 | RF-49 | MUST | Every selected semantic subject or obligation | Selection and every later layer MUST preserve the same selected subject or obligation. | S05, S55 |
| PE-SEMPRES-004 | RF-49 | MUST | Every normative requirement crossing a downstream boundary | The boundary MUST preserve stable requirement identity and traceability. | S05, S57 |
| PE-SEMPRES-005 | RF-49 | MUST | Every semantic subject crossing a downstream boundary | The boundary MUST preserve complete normative meaning. | S04, S05, S46 |
| PE-SEMPRES-006 | RF-49 | MUST | Every requirement crossing a downstream boundary | The boundary MUST preserve operative strength unchanged. | S04, S05, S64 |
| PE-SEMPRES-007 | RF-49 | MUST | Every requirement crossing a downstream boundary | The boundary MUST preserve applicability and its governing conditions. | S05, S55 |
| PE-SEMPRES-008 | RF-49 | MUST | Every permitted protocol choice | Every downstream constraint or selection MUST remain within the published choice boundary. | S05, S55 |
| PE-SEMPRES-009 | RF-49 | MUST | Every protocol subject and occurrence | Downstream processing MUST preserve subject identity, occurrence identity, and established identity separation. | S18, S27 |
| PE-SEMPRES-010 | RF-49 | MUST | Every downstream representation and surface | The representation or surface MUST preserve privacy, unlinkability, minimum disclosure, and Private Actor separation. | S01, S18, S20 |
| PE-SEMPRES-011 | RF-49 | MUST | Every proof, public input, verification, and validity boundary | The boundary MUST preserve declared proof meaning, public-input meaning, verification meaning, and complete validity conditions. | S18 |
| PE-SEMPRES-012 | RF-49 | MUST | Every Protocol Action use chain | The chain MUST preserve Action, Evaluation, Determination, acceptance, and rejection identities and semantics. | S18, S24, S25 |
| PE-SEMPRES-013 | RF-49 | MUST | Every transition use chain | The chain MUST preserve mapping, occurrence, authorization, execution, commitment, state, history, consequence, and failure semantics. | S18, S26, S27 |
| PE-SEMPRES-014 | RF-49 | MUST | Every application or adapter boundary | Application representation and adapter translation MUST preserve selected protocol meaning or fail. | S29, S40, S41, S42, S44 |
| PE-SEMPRES-015 | RF-49 | MUST | Every runtime or implementation boundary | Operational responsibility and implementation realization MUST preserve semantics without acquiring semantic ownership. | S43, S45, S46, S47 |
| PE-SEMPRES-016 | RF-49 | MUST | Every compatibility structure | Compatibility MUST preserve its declared target, surface, relationship, scope, and separation from upstream semantics. | S48, S49, S50, S51, S52, S53, S54 |
| PE-SEMPRES-017 | RF-49 | MUST | Every profile and Reference Implementation boundary | Profile selection and reference realization MUST preserve applicable requirements and permitted-choice boundaries. | S55, S56 |
| PE-SEMPRES-018 | RF-49 | MUST | Every conformance boundary | Requirements, evidence, assessment, and determination MUST preserve upstream meaning and bounded scope. | S57, S58, S59, S60, S61, S62, S63, S64 |
| PE-SEMPRES-019 | RF-49 | MUST | Every certification boundary | Basis, decision, status, recognition, and authority MUST preserve supporting conformance meaning and scope. | S65, S66, S67, S68 |
| PE-SEMPRES-020 | RF-49 | MUST | Every successful downstream operation | Success MUST preserve the selected subject or obligation without substitution. | S18, S27, S46 |
| PE-SEMPRES-021 | RF-49 | MUST | Every downstream operation unable to demonstrate preservation | The operation MUST fail, remain unsupported, narrow, withdraw, or be superseded under its defined lifecycle. | S27, S46, S64, S68 |
| PE-SEMPRES-022 | RF-49 | MUST NOT | Every preservation failure | Failure MUST NOT repair, reinterpret, replace, or synthesize missing semantics. | S18, S27, S46 |
| PE-SEMPRES-023 | RF-49 | MUST NOT | Every downstream layer | The layer MUST NOT substitute a different subject, occurrence, requirement, determination, transition, or recognition. | S18, S27, S46 |
| PE-SEMPRES-024 | RF-49 | MUST NOT | Every downstream layer | The layer MUST NOT infer an absent obligation, permission, identity, evidence item, classification, or authority. | S05, S18, S46 |
| PE-SEMPRES-025 | RF-49 | MUST NOT | Every downstream layer | The layer MUST NOT silently widen or narrow identity, meaning, applicability, choice, target, or scope. | S05, S55, S64, S68 |
| PE-SEMPRES-026 | RF-49 | MUST NOT | Every downstream composition | Composition MUST NOT merge distinct subjects or divide one subject into replacement identities or obligations. | S05, S17, S18 |

### 35.2 Explicit Exclusions and Prohibited Interpretations

RF-50 provides the global exclusion closure.

Local prohibitions remain authoritative in their owning sections.

#### 35.2.1 RF-50 — Explicit Protocol Exclusions and Prohibited Interpretations

| Identifier | Family | Strength | Applicability | Normative requirement | Sources |
|---|---|---|---|---|---|
| PE-EXCLUDE-001 | RF-50 | MUST | The complete Protocol Specification | The specification MUST identify prohibited interpretations through authoritative exclusions and supporting local references. | S02, S03 |
| PE-EXCLUDE-002 | RF-50 | MUST NOT | Every development or protocol interpretation | STATE.md MUST NOT be interpreted as published protocol authority. | S01, S08 |
| PE-EXCLUDE-003 | RF-50 | MUST NOT | Every downstream structure | No specification, interface, application, runtime, implementation, profile, assessment, conformance, certification, deployment, report, or observability surface MUST become protocol authority. | S08, S17, S64, S68 |
| PE-EXCLUDE-004 | RF-50 | MUST NOT | Every downstream layer | A downstream layer MUST NOT define, amend, replace, or supersede upstream protocol semantics. | S03, S08, S46 |
| PE-EXCLUDE-005 | RF-50 | MUST NOT | Every application interpretation | Application-owned meaning, policy, request, response, or state MUST NOT become protocol truth. | S29, S40, S41, S42 |
| PE-EXCLUDE-006 | RF-50 | MUST NOT | Every implementation interpretation | Existing implementation behavior, convenience, defect, topology, or machinery MUST NOT become protocol semantics. | S45, S46 |
| PE-EXCLUDE-007 | RF-50 | MUST NOT | Every reference interpretation | Reference behavior, designation, similarity, or interoperability MUST NOT become a normative requirement. | S56 |
| PE-EXCLUDE-008 | RF-50 | MUST NOT | Every compatibility interpretation | Compatibility MUST NOT become succession, semantic equivalence, conformance, certification, or protocol authority. | S48, S49, S50, S51, S52, S53, S54 |
| PE-EXCLUDE-009 | RF-50 | MUST NOT | Every conformance interpretation | Conformance MUST NOT create obligations, redefine realization, become certification, or acquire protocol authority. | S57, S58, S64 |
| PE-EXCLUDE-010 | RF-50 | MUST NOT | Every certification interpretation | Certification MUST NOT perform conformance assessment, redefine semantics, become protocol truth, or acquire protocol authority. | S64, S68 |
| PE-EXCLUDE-011 | RF-50 | MUST NOT | Every evidence or testing interpretation | Artifact existence, evidence, testing, inspection, comparison, or package publication MUST NOT independently establish conformance or certification. | S59, S60, S61, S64, S68 |
| PE-EXCLUDE-012 | RF-50 | MUST NOT | Every protocol-subject identifier | A protocol-subject or occurrence identifier MUST NOT identify or imply a Private Actor. | S01, S18, S20 |
| PE-EXCLUDE-013 | RF-50 | MUST NOT | Every public identifier and metadata surface | The surface MUST NOT create reusable participant identity or identity continuity across bounded actions. | S01, S18, S20 |
| PE-EXCLUDE-014 | RF-50 | MUST NOT | Every protocol, assessment, and certification surface | The surface MUST NOT create cross-action linkage or extend proof meaning into actor identification. | S01, S18, S20 |
| PE-EXCLUDE-015 | RF-50 | MUST NOT | Every downstream record | Enrollment, admission, funding, sponsor, origin, ownership, or wallet provenance MUST NOT be carried into action, assessment, or certification identity. | S01, S18, S20 |
| PE-EXCLUDE-016 | RF-50 | MUST NOT | Every metadata composition | Timing, ordering, transport, runtime, deployment, evidence, assessment, certification, or authority metadata MUST NOT create an actor-reconstruction bridge. | S01, S18, S20 |
| PE-EXCLUDE-017 | RF-50 | MUST NOT | Every naming and documentation surface | Names, fields, routes, keys, logs, diagnostics, examples, tests, and reports MUST NOT bypass privacy or introduce correlation-bearing semantics. | S01, S18, S20 |
| PE-EXCLUDE-018 | RF-50 | MUST | Every proposed new first-class protocol subject | The subject MUST demonstrate independent identity, semantics, validity, lifecycle, and consequence before introduction. | S17, S18, S28 |
| PE-EXCLUDE-019 | RF-50 | MUST NOT | Every Protocol Claim interpretation | A Protocol Claim MUST NOT be introduced as a distinct first-class architectural subject. | S28 |
| PE-EXCLUDE-020 | RF-50 | MUST NOT | Every Evaluation or classification model | An Evaluation Outcome, separate acceptance object, or separate rejection object MUST NOT be introduced. | S18, S25 |
| PE-EXCLUDE-021 | RF-50 | MUST NOT | Every transition model | Authorization, execution, commitment, consequence, failure, or stale authorization MUST NOT become an artificial first-class subject. | S18, S27 |
| PE-EXCLUDE-022 | RF-50 | MUST NOT | Every certification model | Certification outcome MUST NOT become a new protocol subject distinct from Decision, Status, or recognition. | S66, S67, S68 |
| PE-EXCLUDE-023 | RF-50 | MUST NOT | Every implementation-specific design choice | Blockchain consensus, transaction formats, relay, transport, storage, database, deployment topology, language, and source structure MUST NOT become protocol law. | S21, S29, S44, S45 |
| PE-EXCLUDE-024 | RF-50 | MUST NOT | Every application or certification-program choice | Application business meaning, auditor qualification, program operations, governance, accreditation, branding, and commercial policy MUST NOT become protocol law. | S29, S44, S68 |
| PE-EXCLUDE-025 | RF-50 | MUST NOT | The current implementation and codebase | Specification composition MUST NOT be interpreted as a current-codebase compatibility, conformance, certification, security, or operational-readiness assessment. | S02, S17, S64, S68 |
| PE-EXCLUDE-026 | RF-50 | MUST NOT | The Engineering[150] specification state | Composition completion MUST NOT be interpreted as final consolidation, acceptance, certification, publication, or publication readiness before Engineering[151]. | S01, S02, S03 |

### 35.3 SF-16 Formal Summary

For every selected semantic subject or obligation `T`:

> selectionChooses(T)

Success preserves the same `T`:

> T -> preserved(T)

Failure remains failure:

> T -> fail

Substitution is forbidden:

> T -> T'

where:

> T' != T

Therefore:

> cannotPreserve(T)
> -> fail

and never:

> cannotPreserve(T)
> -> repairOrInfer(T')

The complete authority direction remains:

> Published Protocol Generation
> -> Protocol Specification
> -> Implementation Profile
> -> Implementation
> -> Conformance
> -> Certification

No downstream layer modifies an upstream layer.

Private actors remain private.

Public protocol actions and bounded downstream assessment structures remain
public only within their declared non-identifying scope.

Protocol authority always remains with the published Privacy Engine protocol generation.

## 36. Supporting Relationships and Complete Dependency Chain

SF-01 and SF-02 establish specification authority, normative interpretation,
protocol generation, publication, versioning, and lineage.

SF-03 and SF-04 establish terminology, subject identity, Private Actor
separation, privacy, unlinkability, neutral naming, and forbidden correlation.

SF-05 through SF-11 establish interfaces, operations, proofs, validity,
Protocol Actions, Evaluation, Determination, transition mappings, transition
occurrences, authorization, execution, commitment, state, history,
consequence, failure, staleness, and re-evaluation.

SF-12 establishes application representation, adapter translation, integration,
runtime responsibility, and enforcement/execution boundaries.

SF-13 establishes implementation identity, Protocol Realization, downstream
authority prohibitions, compatibility, and migration.

SF-14 establishes Implementation Profiles and Reference Implementations.

SF-15 establishes conformance requirements, requirement sets, artifacts,
evidence, packages, claims, assessments, determinations, certification bases,
decisions, statuses, recognition, scope, and certification authority.

SF-16 closes the specification with global semantic-preservation and explicit
exclusion requirements.

Every RF-01–RF-50 family now possesses exactly one authoritative normative
home.

Supporting relationships increase traceability.

They do not create competing normative authority.

## 37. Current Composition Boundary

This cumulative document now contains authoritative normative homes for:

- SF-01–SF-16;
- RF-01–RF-50.

The cumulative specification contains 729 stable normative requirements:

- 578 requirements preserved unchanged from SF-01–SF-14;
- 14 requirements composed for RF-44;
- 19 requirements composed for RF-45;
- 27 requirements composed for RF-46;
- 19 requirements composed for RF-47;
- 20 requirements composed for RF-48;
- 26 requirements composed for RF-49;
- 26 requirements composed for RF-50;
- 151 requirements added by Engineering[150].

All 430 requirements established through Engineering[148] remain unchanged.

All 148 requirements added by Engineering[149] remain unchanged.

All section-family and requirement-family composition is complete.

Engineering[151] completed final consolidation review and recorded the
determination `rejected pending identified correction`.

Engineering[152] completed the bounded F-01, F-02, and F-03 corrective pass.

Engineering[153] independently confirmed those corrections and every other
substantive consolidation category, but rejected the specification pending
correction of the blocking informative-status contradiction F-04.

Engineering[154] corrected F-04 through the bounded informative-status edits
recorded in
`docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_STATUS_CONSISTENCY_CORRECTION_V1.md`.

Engineering[155] completed final independent consolidation re-review and
independently confirmed:

- F-04 is resolved;
- every Engineering[153] passing result remains preserved;
- no additional blocking or non-blocking defect exists;
- and the specification is accepted and publication-ready.

The final consolidation boundary is complete.

The specification remains unpublished. Publication requires a separate explicit act.

The current implementation and codebase remain unassessed and uncertified.

## 38. Cumulative Traceability

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
| S34 | `PRIVACY_ENGINE_PROTOCOL_EXECUTION_MODEL_V1.md` |
| S35 | `PRIVACY_ENGINE_PROTOCOL_STATE_MODEL_V1.md` |
| S36 | `PRIVACY_ENGINE_PROTOCOL_TRANSITION_ENFORCEMENT_MODEL_V1.md` |
| S37 | `PRIVACY_ENGINE_PROTOCOL_TRANSITION_PRECONDITIONS_MODEL_V1.md` |
| S38 | `PRIVACY_ENGINE_STATE_EVOLUTION_MODEL_V1.md` |
| S39 | `PRIVACY_ENGINE_SUCCESSOR_STATE_MODEL_V1.md` |
| S40 | `PRIVACY_ENGINE_APPLICATION_ADAPTER_MODEL_V1.md` |
| S41 | `PRIVACY_ENGINE_APPLICATION_REQUEST_MODEL_V1.md` |
| S42 | `PRIVACY_ENGINE_APPLICATION_RESPONSE_MODEL_V1.md` |
| S43 | `PRIVACY_ENGINE_APPLICATION_RUNTIME_BOUNDARY_V1.md` |
| S44 | `PRIVACY_ENGINE_INTEGRATOR_OBLIGATIONS_V1.md` |
| S45 | `PRIVACY_ENGINE_IMPLEMENTATION_MODEL_V1.md` |
| S46 | `PRIVACY_ENGINE_PROTOCOL_REALIZATION_MODEL_V1.md` |
| S47 | `PRIVACY_ENGINE_RUNTIME_MODEL_V1.md` |
| S48 | `PRIVACY_ENGINE_COMPATIBILITY_CONFORMANCE_MODEL_V1.md` |
| S49 | `PRIVACY_ENGINE_COMPATIBILITY_DECLARATION_MODEL_V1.md` |
| S50 | `PRIVACY_ENGINE_COMPATIBILITY_MODEL_V1.md` |
| S51 | `PRIVACY_ENGINE_COMPATIBILITY_PROFILE_MODEL_V1.md` |
| S52 | `PRIVACY_ENGINE_COMPATIBILITY_STATEMENT_MODEL_V1.md` |
| S53 | `PRIVACY_ENGINE_COMPATIBILITY_SURFACE_MODEL_V1.md` |
| S54 | `PRIVACY_ENGINE_COMPATIBILITY_TARGET_MODEL_V1.md` |
| S55 | `PRIVACY_ENGINE_IMPLEMENTATION_PROFILE_MODEL_V1.md` |
| S56 | `PRIVACY_ENGINE_REFERENCE_IMPLEMENTATION_MODEL_V1.md` |
| S57 | `PRIVACY_ENGINE_CONFORMANCE_REQUIREMENT_MODEL_V1.md` |
| S58 | `PRIVACY_ENGINE_CONFORMANCE_REQUIREMENT_SET_MODEL_V1.md` |
| S59 | `PRIVACY_ENGINE_CONFORMANCE_ARTIFACT_MODEL_V1.md` |
| S60 | `PRIVACY_ENGINE_CONFORMANCE_EVIDENCE_MODEL_V1.md` |
| S61 | `PRIVACY_ENGINE_CONFORMANCE_PACKAGE_MODEL_V1.md` |
| S62 | `PRIVACY_ENGINE_CONFORMANCE_CLAIM_MODEL_V1.md` |
| S63 | `PRIVACY_ENGINE_CONFORMANCE_ASSESSMENT_MODEL_V1.md` |
| S64 | `PRIVACY_ENGINE_CONFORMANCE_MODEL_V1.md` |
| S65 | `PRIVACY_ENGINE_CERTIFICATION_BASIS_MODEL_V1.md` |
| S66 | `PRIVACY_ENGINE_CERTIFICATION_DECISION_MODEL_V1.md` |
| S67 | `PRIVACY_ENGINE_CERTIFICATION_STATUS_MODEL_V1.md` |
| S68 | `PRIVACY_ENGINE_CERTIFICATION_MODEL_V1.md` |

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
> -> oneAuthoritativeNormativeHome(R)

> sameSemanticRequirement(R1, R2)
> -> oneNormativeRequirement(R)

> supportingReference(N2, R)
> =/=> authoritativeHome(R, N2)

> supportingReference(N2, R)
> =/=> redefines(N2, R)

> traceableTo(R, F)

> semantics(Spec) = semantics(P)

Traceability organizes established semantics.

It does not redefine them.

## 39. Conclusion

SF-01 through SF-16 now provide one cumulative developer-facing normative
composition from the published Privacy Engine protocol generation through
Specification, Implementation Profiles, implementations, conformance, and
certification.

Engineering[150] establishes:

- Published Conformance Requirements as assessable expressions of unchanged
  normative obligations;
- complete bounded Conformance Requirement Sets distinct from Implementation
  Profiles;
- distinct artifact, evidence, package, claim, assessment, and determination
  structures;
- binary completed Conformance Determinations within explicit scope;
- immutable historical assessment and certification records;
- distinct Certification Bases, Decisions, Statuses, and recognition;
- certification as bounded recognition based on identified Conformance
  Determinations;
- bounded certification authority without protocol authority;
- complete privacy and anti-correlation requirements across assessment and
  certification surfaces;
- one global semantic-preservation closure;
- one global explicit-exclusion closure;
- and one authoritative normative home for every RF-01–RF-50 family.

The cumulative specification remains composition-complete.

Engineering[151] completed final consolidation review and rejected the
specification pending identified correction.

Engineering[152] applied the bounded corrections recorded in
`docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_CONSOLIDATION_CORRECTIONS_V1.md`.

Engineering[153] completed the independent consolidation re-review, confirmed
F-01, F-02, F-03, and every other substantive consolidation category, and
rejected the specification pending correction of F-04.

Engineering[154] applied the bounded informative-status correction recorded in
`docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_STATUS_CONSISTENCY_CORRECTION_V1.md`.

Engineering[155] completed final independent consolidation re-review, confirmed
that F-04 is resolved and every Engineering[153] passing result remains
preserved, and found no additional blocking or non-blocking defect.

The specification is accepted and publication-ready.

The specification remains unpublished. Publication requires a separate explicit act.

The current codebase remains unassessed and uncertified.

Private actors remain distinct from every public protocol, implementation,
conformance, certification, metadata, naming, diagnostic, reporting, and
observability surface.

No new first-class protocol subject is introduced.

Protocol authority always remains with the published Privacy Engine protocol generation.
