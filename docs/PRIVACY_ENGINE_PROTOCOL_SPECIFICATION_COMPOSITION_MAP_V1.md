# Privacy Engine Protocol Specification Composition Map V1

STATE.md remains canonical.

# 1. Purpose

The Privacy Engine Protocol Specification Composition Map defines how the
completed Privacy Engine formal-model corpus is composed into one complete,
non-duplicative, implementation-facing normative Privacy Engine Protocol
Specification.

The map establishes:

- the bounded source corpus;
- the role of every included source;
- the normative requirement families derived from those sources;
- the authoritative specification destination of each requirement family;
- cross-section dependencies;
- traceability rules;
- duplication-control rules;
- bounded editorial-normalization rules;
- privacy-language requirements;
- and the conditions under which normative specification composition may
  proceed.

The map does not redefine protocol semantics.

It does not extend the ontology.

It organizes established semantics for normative composition.

# 2. Scope

This document governs corpus-to-specification composition.

It determines:

- which sources participate directly in specification composition;
- which sources define protocol subjects, relationships, boundaries,
  lifecycles, constraints, or assessment models;
- which sources constrain composition globally;
- which sources produce exclusions rather than specification subjects;
- which requirement family owns each semantic obligation;
- which specification section family owns each requirement family;
- how supporting references remain non-authoritative;
- how earlier and later formulations are normalized without semantic change;
- and whether the corpus is ready for incremental normative composition.

This document does not:

- compose the complete Protocol Specification;
- define runtime algorithms;
- define transaction formats;
- define transport;
- define storage;
- define application-specific meaning;
- define blockchain consensus;
- create an implementation profile;
- create a reference implementation;
- perform conformance assessment;
- perform certification;
- or introduce a new first-class architectural subject.

# 3. Composition Inputs

Let:

- `P` be one published Privacy Engine protocol generation;
- `Spec` be the Protocol Specification derived from `P`;
- `C` be the complete bounded formal source corpus;
- `F` be one source in `C`;
- `R` be one normative requirement;
- `G` be one normative requirement family;
- `N` be one authoritative specification section family;
- `M` be this composition map;
- `D` be one dependency relationship.

The composition inputs are:

1. `STATE.md`;
2. the sixty-six source documents identified in Section 18;
3. the completed Formal Specification Structure;
4. the established normative-language and requirement architecture;
5. the completed foundational consolidation review;
6. the completed protocol-use consolidation review.

The governing relationships are:

> derivesFrom(Spec, P)

> memberOf(F, C)

> maps(M, F, G)

> assigns(M, G, N)

> traceableTo(R, F)

> authoritativeHome(R, N)

`STATE.md` is an authority input.

It is not reduced to one ordinary source row.

# 4. Relationship to STATE.md

`STATE.md` remains the canonical source of truth for current Privacy Engine
architecture, invariants, protocol boundaries, deployed-system interpretation,
and development governance.

If any source document, source-mapping row, supporting reference, editorial
formulation, or future specification text conflicts with `STATE.md`,
`STATE.md` wins.

Formally:

> conflicts(F, STATE)
> -> subordinate(F, STATE)

> conflicts(Spec, STATE)
> -> invalidComposition(Spec)

The composition map must not use an earlier supporting formulation to override
the canonical state.

# 5. Relationship to the Formal Model Corpus

The formal-model corpus is the semantic foundation of the Protocol
Specification.

The formal models define bounded subjects, relationships, lifecycles,
boundaries, and assessment objects.

The Protocol Specification reorganizes those semantics into an
implementation-facing normative composition.

It does not acquire independent semantic authority.

> semantics(Spec) = semantics(P)

> organizes(M, C, Spec)
> =/=> redefines(M, C)

One source document may produce several requirement families.

Several source documents may support one requirement family.

Neither condition creates duplicated normative authority.

# 6. Relationship to the Formal Specification Structure

The composition map reuses the Formal Specification Structure established by
`PRIVACY_ENGINE_FORMAL_SPECIFICATION_STRUCTURE_V1.md`.

The established high-level parts remain valid:

- Introduction;
- Protocol Foundations;
- Architectural Model;
- Identity Model;
- Protocol Objects;
- Protocol Operations;
- Privacy Properties;
- Compatibility;
- Conformance;
- Implementation Guidance;
- Appendices.

Engineering[143] performs bounded editorial normalization by defining sixteen
more precise specification section families within those established parts.

This refinement changes presentation only.

> structure(Specification) != structure(FormalModelCorpus)

> semantics(Specification) = semantics(PublishedProtocol)

The refined section families do not create new architectural subjects.

# 7. Composition Method

The unit of composition is the semantic requirement family.

It is not the source-document count.

For every source:

1. identify its primary source role;
2. identify its bounded architectural subject, relationship, or constraint;
3. identify every directly derived requirement family;
4. assign each requirement family one authoritative specification home;
5. record any supporting destinations;
6. record dependency predecessors;
7. preserve exclusions, privacy constraints, and authority constraints;
8. mark traceability status;
9. consolidate repeated semantic requirements;
10. reject any mapping that creates contradictory normative homes.

The primary mapping path is:

> established formal source
> -> normative requirement family
> -> authoritative specification destination

For every positive source:

> positiveSource(F)
> -> exists G, N:
> maps(M, F, G)
> and assigns(M, G, N)

For every negative assessment:

> negativeAssessment(F)
> -> mapsToExclusion(F, N)

For every consolidation review:

> consolidationReview(F)
> -> constrainsGlobally(F, M)

# 8. Source-Corpus Boundary

The direct bounded source corpus contains sixty-six root-level Privacy Engine
documents.

It includes:

- formal architectural models;
- protocol boundary and contract sources;
- the formal specification architecture;
- the Protocol Claim negative assessment;
- the foundational consolidation review;
- the protocol-use consolidation review.

The broader `/docs` tree contains operational, historical, application,
REFLECT, TEMPEST, ZK, relayer, V0, and developer-supporting material.

Those documents do not automatically become direct normative sources.

A document outside the bounded sixty-six-source corpus may later be used as:

- informative implementation guidance;
- parameter provenance;
- operational evidence;
- historical context;
- or a supporting implementation reference.

Such use requires explicit classification.

> outsideCorpus(F)
> =/=> normativeSource(F)

> historicalContext(F)
> =/=> currentAuthority(F)

The corpus boundary may be expanded only if a later normative composition slice
demonstrates that one established protocol requirement lacks adequate source
traceability.

Such expansion would add source evidence.

It would not add protocol semantics.

# 9. Source-Role Classification

The sixty-six sources have the following primary roles:

| Role | Code | Count | Composition treatment |
|---|---:|---:|---|
| Positive formal model | PF | 45 | Direct normative derivation |
| Boundary or contract source | BC | 7 | Cross-cutting normative derivation |
| Cross-cutting synthesis | CX | 1 | Global invariant support; later dedicated definitions own semantics |
| Specification-architecture source | SA | 10 | Governs normative composition and downstream assessment |
| Negative architectural assessment | NA | 1 | Produces exclusions and prohibited interpretations |
| Consolidation review | CR | 2 | Constrains coverage and coherence globally |

A primary role does not prevent a source from providing secondary support to
another requirement family.

Primary role identifies how the source enters composition.

# 10. Positive Formal Models

A positive formal model establishes one bounded subject, relationship,
lifecycle, assessment object, or semantic process.

Positive formal models produce direct requirement families.

They include models for:

- protocol identity and generation;
- publication, succession, lineage, and versioning;
- interface contracts and protocol operations;
- protocol execution and enforcement;
- protocol state and transition semantics;
- application requests, responses, and adapters;
- implementation and realization;
- compatibility;
- conformance constituents;
- certification constituents;
- Protocol Actions;
- Protocol Action Evaluation and Determination;
- and Protocol State Transition occurrences.

A positive model does not receive an independent specification section merely
because its source document exists.

> positiveModel(F)
> =/=> independentSection(F)

Its semantic requirements are assigned to the section family that owns their
meaning.

# 11. Negative Architectural Assessments

`PRIVACY_ENGINE_PROTOCOL_CLAIM_ASSESSMENT_V1.md` establishes that a proposed
Protocol Claim does not possess independent architectural identity.

Its normative destinations are:

- explicit exclusions;
- prohibited conceptual interpretations;
- terminology constraints;
- application-boundary constraints.

It must not produce:

- a Protocol Claim section;
- a Protocol Claim lifecycle;
- a Protocol Claim identifier;
- a Protocol Claim validity model;
- or a Protocol Claim implementation obligation.

> notFirstClass(ProtocolClaim)

> negativeAssessment(ProtocolClaim)
> -> exclusionDestination(SF-16)

A Protocol Action remains the public protocol occurrence.

Application-defined meaning remains application-owned.

Implementation conformance claims remain separate implementation-assessment
objects and are not Protocol Claims.

# 12. Consolidation Reviews

The corpus contains two consolidation reviews:

1. `PRIVACY_ENGINE_FORMAL_ARCHITECTURE_CONSOLIDATION_REVIEW_V1.md`;
2. `PRIVACY_ENGINE_PROTOCOL_USE_CHAIN_CONSOLIDATION_REVIEW_V1.md`.

The foundational review establishes:

- ontology completeness;
- identity separation;
- bounded semantic ownership;
- coherent layering;
- unique protocol authority;
- no missing first-class foundational subject.

The protocol-use review establishes:

- completeness of the protocol-use chain;
- completeness of lifecycle and failure paths;
- separation of Action, Evaluation, Determination, and Transition identities;
- no missing intermediate first-class subject;
- compositional privacy;
- readiness for normative specification composition.

These reviews constrain the whole specification.

They do not become independent normative sections.

> consolidationReview(F)
> -> constrainsGlobally(F, Spec)

> constrainsGlobally(F, Spec)
> =/=> authoritativeHome(F, N)

# 13. Specification-Architecture Sources

The ten specification-architecture sources are:

1. `PRIVACY_ENGINE_FORMAL_SPECIFICATION_STRUCTURE_V1.md`;
2. `PRIVACY_ENGINE_NORMATIVE_SPECIFICATION_LANGUAGE_V1.md`;
3. `PRIVACY_ENGINE_NORMATIVE_REQUIREMENT_MODEL_V1.md`;
4. `PRIVACY_ENGINE_NORMATIVE_REQUIREMENT_SET_MODEL_V1.md`;
5. `PRIVACY_ENGINE_SPECIFICATION_SECTION_MODEL_V1.md`;
6. `PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_MODEL_V1.md`;
7. `PRIVACY_ENGINE_IMPLEMENTATION_PROFILE_MODEL_V1.md`;
8. `PRIVACY_ENGINE_REFERENCE_IMPLEMENTATION_MODEL_V1.md`;
9. `PRIVACY_ENGINE_CONFORMANCE_MODEL_V1.md`;
10. `PRIVACY_ENGINE_CERTIFICATION_MODEL_V1.md`.

These sources govern:

- specification identity;
- normative and informative classification;
- requirement identity and strength;
- requirement-set composition;
- section composition;
- specification completeness;
- profile derivation;
- reference realization;
- conformance determination;
- certification recognition.

They do not replace the protocol semantics being specified.

# 14. Historical and Supporting Sources

Historical and supporting documents may explain:

- development provenance;
- earlier implementation architecture;
- previous terminology;
- superseded deployment assumptions;
- operational commands;
- implementation-specific machinery;
- or application-specific context.

They do not silently become current normative authority.

Within the bounded corpus,
`PRIVACY_ENGINE_COMPATIBILITY_CONFORMANCE_MODEL_V1.md` is treated as a
cross-cutting synthesis.

Its invariant-preservation principles remain useful.

The later dedicated Compatibility and Conformance models own the separate
formal definitions.

Earlier interface, runtime, and state documents remain valid bounded sources,
subject to the normalization rules in Section 22.

Supporting sources outside the bounded corpus remain informative unless
explicitly admitted by a later traceability decision.

# 15. Normative Destination Model

Every semantic requirement has one authoritative normative home.

A requirement family may contain multiple requirements.

Every individual requirement inherits the authoritative section family assigned
to its requirement family.

> oneSemanticRequirement(R)
> -> oneAuthoritativeNormativeHome(R)

> memberOf(R, G)
> and assigns(M, G, N)
> -> authoritativeHome(R, N)

A source may map to several requirement families.

> maps(M, F, G1)

> maps(M, F, G2)

> G1 != G2

This is multi-family derivation.

It is not duplicated authority.

# 16. Normative Requirement Families

The complete destination-family inventory is:

| ID | Normative requirement family | Authoritative home |
|---|---|---|
| RF-01 | Specification identity, derivation, completeness, and authority | SF-01 |
| RF-02 | Protocol definition, scope, and invariant ownership | SF-01 |
| RF-03 | Protocol generation, publication, and Published Protocol | SF-02 |
| RF-04 | Succession, lineage, versioning, deprecation, and migration | SF-02 |
| RF-05 | Normative language, interpretation, applicability, and strength | SF-01 |
| RF-06 | Protocol terminology | SF-03 |
| RF-07 | Protocol subject identity and identity separation | SF-03 |
| RF-08 | Protocol identifiers and occurrence identifiers | SF-03 |
| RF-09 | Private actors and public protocol subjects | SF-04 |
| RF-10 | Privacy, anonymity, and unlinkability | SF-04 |
| RF-11 | Compositional privacy, observability, and forbidden correlation | SF-04 |
| RF-12 | Interface contracts and concrete interface specifications | SF-05 |
| RF-13 | Protocol surfaces, operations, and Published Results | SF-05 |
| RF-14 | Application requests, responses, and adapters | SF-12 |
| RF-15 | Anonymous membership, continuity, and enrollment separation | SF-04 |
| RF-16 | Proofs and declared public inputs | SF-06 |
| RF-17 | Proof verification | SF-06 |
| RF-18 | Evidence, protocol validity, and non-proof validity conditions | SF-06 |
| RF-19 | Nullifier-based uniqueness and action-bounded unlinkability | SF-04 |
| RF-20 | Protocol Actions | SF-07 |
| RF-21 | Applicable protocol-rule sets and action validity | SF-07 |
| RF-22 | Protocol Action Evaluation | SF-08 |
| RF-23 | Protocol Action Determination | SF-08 |
| RF-24 | Acceptance and rejection | SF-08 |
| RF-25 | Accepted no-transition behavior | SF-08 |
| RF-26 | Published transition mappings, preconditions, and eligibility | SF-09 |
| RF-27 | Protocol State Transition occurrence identity and lifecycle | SF-09 |
| RF-28 | Transition authorization and cardinality | SF-09 |
| RF-29 | Transition execution and preservation | SF-10 |
| RF-30 | Transition commitment, completeness, and atomicity | SF-10 |
| RF-31 | Protocol state, successor state, and state evolution | SF-10 |
| RF-32 | Protocol-state history | SF-11 |
| RF-33 | Public protocol-state consequences | SF-11 |
| RF-34 | Failure classifications and failure separation | SF-11 |
| RF-35 | Stale authorization and re-evaluation | SF-11 |
| RF-36 | Application and adapter authority boundaries | SF-12 |
| RF-37 | Runtime, enforcement, and execution responsibility | SF-12 |
| RF-38 | Implementation identity and implementation obligations | SF-13 |
| RF-39 | Protocol realization | SF-13 |
| RF-40 | Prohibited implementation, runtime, application, and assessment authority | SF-13 |
| RF-41 | Compatibility targets, surfaces, statements, profiles, declarations, and assessment | SF-13 |
| RF-42 | Implementation profiles | SF-14 |
| RF-43 | Reference implementations | SF-14 |
| RF-44 | Published conformance requirements and requirement sets | SF-15 |
| RF-45 | Conformance artifacts, evidence, and packages | SF-15 |
| RF-46 | Conformance claims, assessments, and determinations | SF-15 |
| RF-47 | Certification bases, decisions, and statuses | SF-15 |
| RF-48 | Certification recognition, scope, and authority | SF-15 |
| RF-49 | Protocol-semantic preservation | SF-16 |
| RF-50 | Explicit protocol exclusions and prohibited interpretations | SF-16 |

A requirement family may contain mandatory, prohibited, recommended,
discouraged, optional, or implementation-defined requirements.

Requirement strength belongs to individual requirements.

It is not inferred solely from family membership.

# 17. Specification Section Families

The final Protocol Specification shall be composed through the following
authoritative section families:

| ID | Specification section family | Established Formal Specification part |
|---|---|---|
| SF-01 | Authority, Scope, and Normative Interpretation | Introduction / Protocol Foundations |
| SF-02 | Protocol Generation, Publication, Versioning, and Lineage | Protocol Foundations |
| SF-03 | Protocol Terminology, Subjects, and Identifiers | Architectural Model / Protocol Objects |
| SF-04 | Privacy, Actor Separation, and Compositional Unlinkability | Identity Model / Privacy Properties |
| SF-05 | Interface Contracts, Protocol Surfaces, Operations, and Results | Protocol Objects / Protocol Operations |
| SF-06 | Proofs, Public Inputs, Verification, Evidence, and Validity | Protocol Objects / Protocol Operations |
| SF-07 | Protocol Actions and Applicable Rules | Protocol Objects / Protocol Operations |
| SF-08 | Evaluation, Determination, Acceptance, and Rejection | Protocol Operations |
| SF-09 | Protocol State, Transition Semantics, Preconditions, and Authorization | Architectural Model / Protocol Operations |
| SF-10 | Transition Execution, Commitment, Atomicity, and State Evolution | Protocol Operations |
| SF-11 | History, Public Consequences, Failure, Staleness, and Re-evaluation | Protocol Operations |
| SF-12 | Application, Adapter, Runtime, and Integration Boundaries | Architectural Model / Implementation Guidance |
| SF-13 | Implementation, Realization, Compatibility, and Migration | Compatibility / Implementation Guidance |
| SF-14 | Implementation Profiles and Reference Implementations | Implementation Guidance |
| SF-15 | Conformance and Certification | Conformance |
| SF-16 | Semantic Preservation and Explicit Exclusions | Protocol Foundations / Appendices |

These section families are semantic destinations.

They need not correspond one-to-one with physical files.

A later composition slice may divide one section family into several
specification sections if each resulting section retains one bounded semantic
role.

# 18. Source-to-Destination Mapping

The mapping notation is:

- `PF`: positive formal model;
- `BC`: boundary or contract source;
- `CX`: cross-cutting synthesis;
- `SA`: specification-architecture source;
- `NA`: negative assessment;
- `CR`: consolidation review;
- `P`: privacy constraint preserved;
- `A`: published protocol generation remains sole protocol authority;
- `X`: exclusion or prohibited interpretation preserved;
- `C`: traceability complete.

## 18.1 Application, boundary, and interface sources

| ID | Source | Role | Principal subject | Direct requirement family and home | Supporting destination / predecessor | Preserved boundary | Status |
|---|---|---|---|---|---|---|---|
| S01 | `PRIVACY_ENGINE_APPLICATION_ADAPTER_CONTRACT_V1.md` | BC | Stable application-adapter contract | RF-14, RF-36 -> SF-12; RF-49, RF-50 -> SF-16 | Supports SF-04, SF-05; depends on SF-04–SF-07 | P, A, X | C |
| S02 | `PRIVACY_ENGINE_APPLICATION_ADAPTER_MODEL_V1.md` | PF | Adapter identity and representation translation | RF-14, RF-36 -> SF-12 | Supports SF-05; depends on RF-12 | P, A | C |
| S03 | `PRIVACY_ENGINE_APPLICATION_REQUEST_MODEL_V1.md` | PF | Application-owned request representation | RF-14, RF-36 -> SF-12 | Supports SF-05; depends on RF-13 | P, A, X | C |
| S04 | `PRIVACY_ENGINE_APPLICATION_RESPONSE_MODEL_V1.md` | PF | Application-owned response representation | RF-14, RF-36 -> SF-12 | Supports SF-05; depends on RF-13 | P, A, X | C |
| S05 | `PRIVACY_ENGINE_APPLICATION_RUNTIME_BOUNDARY_V1.md` | BC | Application/runtime responsibility separation | RF-36, RF-37, RF-40 -> SF-12/SF-13 | Depends on SF-07–SF-11 | P, A, X | C |
| S17 | `PRIVACY_ENGINE_CONCRETE_INTERFACE_SPECIFICATION_MODEL_V1.md` | PF | Syntactic realization of an interface contract | RF-12 -> SF-05 | Depends on RF-12 interface meaning; supports SF-12 | A, X | C |
| S26 | `PRIVACY_ENGINE_DEFINITION.md` | BC | Core privacy primitive and application separation | RF-02 -> SF-01; RF-09, RF-10, RF-15, RF-19 -> SF-04; RF-16, RF-17 -> SF-06 | Supports SF-03–SF-12 | P, A, X | C |
| S32 | `PRIVACY_ENGINE_INTEGRATOR_OBLIGATIONS_V1.md` | BC | Integrator preservation obligations | RF-36 -> SF-12; RF-38, RF-40 -> SF-13; RF-49, RF-50 -> SF-16 | Depends on SF-04–SF-13 | P, A, X | C |
| S33 | `PRIVACY_ENGINE_INTERFACE_CONTRACT_MODEL_V1.md` | PF | Published interface meaning | RF-12, RF-13 -> SF-05 | Precedes concrete specifications, operations, adapters | P, A, X | C |
| S34 | `PRIVACY_ENGINE_LAYER_INTERFACE_MAP_V1.md` | BC | Cross-layer information and authority boundaries | RF-11 -> SF-04; RF-12 -> SF-05; RF-36 -> SF-12; RF-40, RF-49 -> SF-13/SF-16 | Supports all operational sections | P, A, X | C |
| S40 | `PRIVACY_ENGINE_PROTOCOL_BOUNDARY_V1.md` | BC | Privacy Engine scope and layer ownership | RF-02 -> SF-01; RF-09–RF-11 -> SF-04; RF-36, RF-40 -> SF-12/SF-13 | Precedes all operational sections | P, A, X | C |
| S54 | `PRIVACY_ENGINE_PROTOCOL_SURFACE_V1.md` | BC | Stable protocol surfaces and replaceable machinery | RF-11, RF-15, RF-19 -> SF-04; RF-12, RF-13 -> SF-05; RF-36 -> SF-12; RF-41 -> SF-13 | Depends on SF-01–SF-04 | P, A, X | C |

## 18.2 Protocol identity, generation, publication, and evolution sources

| ID | Source | Role | Principal subject | Direct requirement family and home | Supporting destination / predecessor | Preserved boundary | Status |
|---|---|---|---|---|---|---|---|
| S27 | `PRIVACY_ENGINE_DEPRECATION_AND_MIGRATION_MODEL_V1.md` | PF | Deprecation, migration, coexistence, and retirement | RF-04 -> SF-02 | Supports RF-41 in SF-13; depends on RF-03 | A, X | C |
| S44 | `PRIVACY_ENGINE_PROTOCOL_GENERATION_MODEL_V1.md` | PF | Protocol generation identity and completeness | RF-03, RF-04 -> SF-02; RF-40 -> SF-13 | Precedes publication, succession, profiles, conformance | A, X | C |
| S45 | `PRIVACY_ENGINE_PROTOCOL_LINEAGE_MODEL_V1.md` | PF | Membership and ordering of published generations | RF-04 -> SF-02 | Depends on publication and succession | A, X | C |
| S46 | `PRIVACY_ENGINE_PROTOCOL_MODEL_V1.md` | PF | Protocol identity, scope, and semantic invariant | RF-02 -> SF-01; RF-13 -> SF-05 | Precedes all protocol-object sections | A | C |
| S48 | `PRIVACY_ENGINE_PROTOCOL_PUBLICATION_MODEL_V1.md` | PF | Publication occurrence and completeness | RF-03 -> SF-02 | Depends on protocol generation; precedes Published Protocol | A, X | C |
| S53 | `PRIVACY_ENGINE_PROTOCOL_SUCCESSION_MODEL_V1.md` | PF | Ordering of distinct published generations | RF-04 -> SF-02 | Depends on RF-03; supports compatibility and migration | A, X | C |
| S59 | `PRIVACY_ENGINE_PUBLISHED_PROTOCOL_MODEL_V1.md` | PF | Immutable published semantic reference | RF-03 -> SF-02; RF-40 -> SF-13 | Depends on generation and publication; precedes implementation | A, X | C |
| S66 | `PRIVACY_ENGINE_VERSIONING_MODEL_V1.md` | PF | Compatible and breaking protocol evolution | RF-04 -> SF-02; RF-41 -> SF-13; RF-49 -> SF-16 | Depends on RF-02 and RF-03 | P, A, X | C |

## 18.3 Protocol operations, runtime, realization, state, and transition sources

| ID | Source | Role | Principal subject | Direct requirement family and home | Supporting destination / predecessor | Preserved boundary | Status |
|---|---|---|---|---|---|---|---|
| S30 | `PRIVACY_ENGINE_IMPLEMENTATION_MODEL_V1.md` | PF | Implementation identity and variation | RF-38, RF-40 -> SF-13 | Depends on SF-01–SF-12; precedes profiles | A, X | C |
| S42 | `PRIVACY_ENGINE_PROTOCOL_ENFORCEMENT_MODEL_V1.md` | PF | Transition-eligibility evaluation | RF-21 -> SF-07; RF-26 -> SF-09; RF-37 -> SF-12 | Supports RF-22; depends on operation, state, preconditions | A, X | C |
| S43 | `PRIVACY_ENGINE_PROTOCOL_EXECUTION_MODEL_V1.md` | PF | Preservation-based realization of an eligible transition | RF-29, RF-31 -> SF-10; RF-37 -> SF-12 | Depends on RF-26–RF-28 | A, X | C |
| S47 | `PRIVACY_ENGINE_PROTOCOL_OPERATION_MODEL_V1.md` | PF | Published bounded protocol capability | RF-13 -> SF-05 | Precedes Protocol Action and execution | A, X | C |
| S49 | `PRIVACY_ENGINE_PROTOCOL_REALIZATION_MODEL_V1.md` | PF | Semantic preservation by implementations | RF-39, RF-40 -> SF-13; RF-49 -> SF-16 | Depends on the complete normative protocol | A, X | C |
| S51 | `PRIVACY_ENGINE_PROTOCOL_STATE_MODEL_V1.md` | PF | Protocol-owned state and state invariants | RF-31 -> SF-10; RF-40 -> SF-13 | Precedes RF-26–RF-35 | A, X | C |
| S55 | `PRIVACY_ENGINE_PROTOCOL_TRANSITION_ENFORCEMENT_MODEL_V1.md` | PF | Published transition-enforcement boundary | RF-26 -> SF-09; RF-30, RF-31 -> SF-10 | Depends on state, mapping, and preconditions | A, X | C |
| S56 | `PRIVACY_ENGINE_PROTOCOL_TRANSITION_MODEL_V1.md` | PF | Published semantic state-change mapping | RF-26 -> SF-09 | Precedes Protocol State Transition occurrences | A, X | C |
| S57 | `PRIVACY_ENGINE_PROTOCOL_TRANSITION_PRECONDITIONS_MODEL_V1.md` | PF | Transition-specific semantic eligibility | RF-26 -> SF-09; RF-34 -> SF-11 | Depends on state and operation | A, X | C |
| S60 | `PRIVACY_ENGINE_PUBLISHED_RESULT_MODEL_V1.md` | PF | Interface-level semantic result | RF-13 -> SF-05 | Supports RF-33 but remains distinct; depends on interface contract | P, A, X | C |
| S62 | `PRIVACY_ENGINE_RUNTIME_MODEL_V1.md` | PF | Runtime execution responsibility | RF-37, RF-40 -> SF-12/SF-13 | Depends on SF-05–SF-11 | P, A, X | C |
| S64 | `PRIVACY_ENGINE_STATE_EVOLUTION_MODEL_V1.md` | PF | Relationship between source and successor states | RF-31 -> SF-10 | Depends on RF-26, RF-29, RF-30 | A, X | C |
| S65 | `PRIVACY_ENGINE_SUCCESSOR_STATE_MODEL_V1.md` | PF | Protocol-defined successor state | RF-31 -> SF-10 | Depends on transition mapping and execution; commitment establishes authority | A, X | C |

## 18.4 Compatibility sources

| ID | Source | Role | Principal subject | Direct requirement family and home | Supporting destination / predecessor | Preserved boundary | Status |
|---|---|---|---|---|---|---|---|
| S10 | `PRIVACY_ENGINE_COMPATIBILITY_CONFORMANCE_MODEL_V1.md` | CX | Invariant-preservation synthesis | RF-41 -> SF-13; supports RF-44–RF-46 in SF-15 | Depends on protocol invariants; later dedicated models own definitions | P, A, X | C |
| S11 | `PRIVACY_ENGINE_COMPATIBILITY_DECLARATION_MODEL_V1.md` | PF | Complete declared compatibility record | RF-41 -> SF-13 | Depends on target and surface; supports conformance | A, X | C |
| S12 | `PRIVACY_ENGINE_COMPATIBILITY_MODEL_V1.md` | PF | Compatibility-object composition | RF-41 -> SF-13 | Depends on RF-03, RF-38, RF-39 | A, X | C |
| S13 | `PRIVACY_ENGINE_COMPATIBILITY_PROFILE_MODEL_V1.md` | PF | Aggregation of compatibility statements | RF-41 -> SF-13 | Depends on statements and implementation identity | A, X | C |
| S14 | `PRIVACY_ENGINE_COMPATIBILITY_STATEMENT_MODEL_V1.md` | PF | Declared implementation compatibility | RF-41 -> SF-13 | Depends on implementation and published generation | A, X | C |
| S15 | `PRIVACY_ENGINE_COMPATIBILITY_SURFACE_MODEL_V1.md` | PF | Published capability set under compatibility | RF-41 -> SF-13 | Depends on SF-02 and SF-05 | A, X | C |
| S16 | `PRIVACY_ENGINE_COMPATIBILITY_TARGET_MODEL_V1.md` | PF | Identified published-generation compatibility reference | RF-41 -> SF-13 | Depends on RF-03 | A, X | C |

## 18.5 Conformance and certification constituent sources

| ID | Source | Role | Principal subject | Direct requirement family and home | Supporting destination / predecessor | Preserved boundary | Status |
|---|---|---|---|---|---|---|---|
| S06 | `PRIVACY_ENGINE_CERTIFICATION_BASIS_MODEL_V1.md` | PF | Immutable certification evaluation basis | RF-47 -> SF-15 | Depends on RF-44; precedes certification decision | A, X | C |
| S07 | `PRIVACY_ENGINE_CERTIFICATION_DECISION_MODEL_V1.md` | PF | Certification pass-or-fail evaluation record | RF-47 -> SF-15 | Depends on certification basis and conformance package | A, X | C |
| S09 | `PRIVACY_ENGINE_CERTIFICATION_STATUS_MODEL_V1.md` | PF | Recorded certification state | RF-47 -> SF-15 | Depends on conformance assessment and certification decision | A, X | C |
| S18 | `PRIVACY_ENGINE_CONFORMANCE_ARTIFACT_MODEL_V1.md` | PF | Smallest referenceable evidence object | RF-45 -> SF-15 | Depends on normative requirements; supports evidence and packages | A, X | C |
| S19 | `PRIVACY_ENGINE_CONFORMANCE_ASSESSMENT_MODEL_V1.md` | PF | Evaluation of one conformance claim | RF-46 -> SF-15 | Depends on claim, evidence, profile, and scope | A, X | C |
| S20 | `PRIVACY_ENGINE_CONFORMANCE_CLAIM_MODEL_V1.md` | PF | Implementation assertion of realization | RF-46 -> SF-15 | Depends on implementation, profile, and published generation | A, X | C |
| S21 | `PRIVACY_ENGINE_CONFORMANCE_EVIDENCE_MODEL_V1.md` | PF | Complete traceable evidence set | RF-45 -> SF-15 | Depends on RF-44 and RF-46 | A, X | C |
| S23 | `PRIVACY_ENGINE_CONFORMANCE_PACKAGE_MODEL_V1.md` | PF | Immutable publication unit for conformance artifacts | RF-45 -> SF-15 | Depends on artifacts and claim scope | A, X | C |
| S24 | `PRIVACY_ENGINE_CONFORMANCE_REQUIREMENT_MODEL_V1.md` | PF | Published conformance obligation | RF-44 -> SF-15 | Derived from normative requirements; precedes evidence | A, X | C |
| S25 | `PRIVACY_ENGINE_CONFORMANCE_REQUIREMENT_SET_MODEL_V1.md` | PF | Complete published conformance-requirement collection | RF-44 -> SF-15 | Depends on RF-44 requirements; precedes certification basis | A, X | C |

## 18.6 Specification-architecture sources

| ID | Source | Role | Principal subject | Direct requirement family and home | Supporting destination / predecessor | Preserved boundary | Status |
|---|---|---|---|---|---|---|---|
| S08 | `PRIVACY_ENGINE_CERTIFICATION_MODEL_V1.md` | SA | Certification recognition, scope, and authority | RF-48 -> SF-15; RF-49, RF-50 -> SF-16 | Depends on RF-46, RF-47, profiles, and conformance | A, X | C |
| S22 | `PRIVACY_ENGINE_CONFORMANCE_MODEL_V1.md` | SA | Conformance determination against an implementation profile | RF-46 -> SF-15; RF-49, RF-50 -> SF-16 | Depends on all applicable normative requirements and SF-14 | A, X | C |
| S29 | `PRIVACY_ENGINE_FORMAL_SPECIFICATION_STRUCTURE_V1.md` | SA | Specification organization and dependency direction | RF-01, RF-05 -> SF-01; RF-49 -> SF-16 | Governs all section families | A, X | C |
| S31 | `PRIVACY_ENGINE_IMPLEMENTATION_PROFILE_MODEL_V1.md` | SA | Bounded selection of applicable normative requirements | RF-42 -> SF-14; RF-49, RF-50 -> SF-16 | Depends on complete Protocol Specification | A, X | C |
| S35 | `PRIVACY_ENGINE_NORMATIVE_REQUIREMENT_MODEL_V1.md` | SA | Stable semantic obligation object | RF-05 -> SF-01; RF-49, RF-50 -> SF-16 | Governs every normative requirement | A, X | C |
| S36 | `PRIVACY_ENGINE_NORMATIVE_REQUIREMENT_SET_MODEL_V1.md` | SA | Bounded composition of normative requirements | RF-05 -> SF-01; RF-49, RF-50 -> SF-16 | Depends on normative requirements; precedes sections | A, X | C |
| S37 | `PRIVACY_ENGINE_NORMATIVE_SPECIFICATION_LANGUAGE_V1.md` | SA | Normative expression and interpretation rules | RF-05 -> SF-01; RF-49, RF-50 -> SF-16 | Governs all normative statements | A, X | C |
| S50 | `PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_MODEL_V1.md` | SA | Complete implementation-facing specification identity | RF-01 -> SF-01; RF-49, RF-50 -> SF-16 | Depends on sections and published generation | A, X | C |
| S61 | `PRIVACY_ENGINE_REFERENCE_IMPLEMENTATION_MODEL_V1.md` | SA | Designated inspectable implementation realization | RF-43 -> SF-14; RF-49, RF-50 -> SF-16 | Depends on implementation profiles | A, X | C |
| S63 | `PRIVACY_ENGINE_SPECIFICATION_SECTION_MODEL_V1.md` | SA | Bounded composition of requirement sets | RF-01, RF-05 -> SF-01; RF-49, RF-50 -> SF-16 | Depends on requirement sets; composes Specification | A, X | C |

## 18.7 Protocol-use sources

| ID | Source | Role | Principal subject | Direct requirement family and home | Supporting destination / predecessor | Preserved boundary | Status |
|---|---|---|---|---|---|---|---|
| S38 | `PRIVACY_ENGINE_PROTOCOL_ACTION_EVALUATION_MODEL_V1.md` | PF | Evaluation, Determination, acceptance, rejection, and evaluation failure | RF-17, RF-18 -> SF-06; RF-22–RF-25 -> SF-08; RF-34, RF-35 -> SF-11 | Depends on Protocol Action and applicable rules; precedes transition | P, A, X | C |
| S39 | `PRIVACY_ENGINE_PROTOCOL_ACTION_MODEL_V1.md` | PF | Identified public Protocol Action occurrence | RF-07–RF-09 -> SF-03/SF-04; RF-16, RF-18 -> SF-06; RF-20, RF-21 -> SF-07 | Depends on protocol subjects, privacy, and interfaces | P, A, X | C |
| S41 | `PRIVACY_ENGINE_PROTOCOL_CLAIM_ASSESSMENT_V1.md` | NA | Rejection of Protocol Claim as a first-class subject | RF-50 -> SF-16 | Supports SF-03, SF-07, SF-12 | P, A, X | C |
| S52 | `PRIVACY_ENGINE_PROTOCOL_STATE_TRANSITION_MODEL_V1.md` | PF | Identified transition occurrence, authorization, execution, commitment, and consequence | RF-27, RF-28 -> SF-09; RF-29–RF-31 -> SF-10; RF-32–RF-35 -> SF-11; RF-49, RF-50 -> SF-16 | Depends on accepted Determination and transition mapping | P, A, X | C |
| S58 | `PRIVACY_ENGINE_PROTOCOL_USE_CHAIN_CONSOLIDATION_REVIEW_V1.md` | CR | Global protocol-use completeness and non-overlap | Global constraint over SF-03–SF-16 | Depends on S38, S39, S41, S52 | P, A, X | C |

## 18.8 Foundational consolidation source

| ID | Source | Role | Principal subject | Direct requirement family and home | Supporting destination / predecessor | Preserved boundary | Status |
|---|---|---|---|---|---|---|---|
| S28 | `PRIVACY_ENGINE_FORMAL_ARCHITECTURE_CONSOLIDATION_REVIEW_V1.md` | CR | Global ontology completeness and authority coherence | Global constraint over SF-01–SF-16 | Depends on the foundational formal-model corpus | P, A, X | C |

All sixty-six source identifiers are unique.

All sixty-six sources possess complete traceability status.

# 19. Multi-Destination Sources

A multi-destination source produces several independent semantic requirement
families.

Examples include:

- the Privacy Engine Definition;
- the Protocol Surface;
- the Layer Interface Map;
- Integrator Obligations;
- Protocol Action;
- Protocol Action Evaluation;
- Protocol State Transition.

Multi-destination mapping is permitted only where the source contains several
already-established semantic families.

> maps(M, F, G1)
> and maps(M, F, G2)
> and G1 != G2

The requirement families retain separate authoritative homes.

The source document does not become a shared normative home.

# 20. One Authoritative Normative Home

Every normative requirement must be defined exactly once.

> oneSemanticRequirement(R)
> -> oneAuthoritativeNormativeHome(R)

Where the same invariant appears in several sources:

> supports(F1, R)

> supports(F2, R)

> F1 != F2

the sources increase traceability.

They do not create multiple requirements.

> sameSemanticRequirement(R1, R2)
> -> oneNormativeRequirement(R)

If two proposed destination sections both appear to define the same semantic
requirement, composition must select the section owning the requirement family.

The other section may contain only a supporting reference.

# 21. Supporting Cross-References

A supporting cross-reference points to an authoritative requirement.

It does not restate that requirement with altered scope, strength, terminology,
conditions, or exceptions.

> authoritativeHome(R, N1)

> supportingReference(N2, R)

> N1 != N2

> supportingReference(N2, R)
> =/=> authoritativeHome(R, N2)

> supportingReference(N2, R)
> =/=> redefines(N2, R)

A supporting reference should normally identify:

- the requirement identifier;
- the authoritative section;
- the relationship requiring the reference.

It should not reproduce the full normative definition unless necessary for a
short exact dependency statement.

# 22. Duplication Control

The corpus contains repeated statements of core invariants.

Repetition commonly occurs in:

- boundary documents;
- compatibility documents;
- implementation documents;
- conformance documents;
- consolidation reviews;
- protocol-use models.

Repeated statements must be consolidated according to semantic ownership.

The following normalization rules are mandatory.

## 22.1 Protocol authority normalization

Earlier sources sometimes state that authority remains with a published
interface contract.

The authoritative interpretation is:

- an interface contract owns its bounded semantic definition;
- the interface contract derives from the published protocol generation;
- protocol authority remains with the published protocol generation.

> definesBoundedInterfaceMeaning(K)

> derives(K, P)

> definesBoundedInterfaceMeaning(K)
> =/=> protocolAuthority(K)

## 22.2 Runtime authority normalization

Earlier phrases such as `bounded architectural authority` and
`authoritatively verifies` identify bounded execution responsibility.

They do not assign protocol authority to a runtime.

> executionResponsibility(I)
> =/=> protocolAuthority(I)

## 22.3 Protocol Operation and Protocol Action

A Protocol Operation is a published bounded capability.

A Protocol Action is one identified occurrence of protocol-defined behavior
presented for Evaluation.

> operationType(O)
> =/=> actionOccurrence(A)

## 22.4 Protocol Transition and Protocol State Transition

A Protocol Transition is a published semantic mapping between source-state and
successor-state classes.

A Protocol State Transition is one identified state-change occurrence governed
by such a mapping.

> transitionMapping(T)
> =/=> transitionOccurrence(U)

## 22.5 Protocol Enforcement and Protocol Action Evaluation

Protocol Enforcement evaluates transition eligibility under published
preconditions.

It contributes to the complete applicable-rule evaluation where relevant.

It does not create a second Protocol Action Determination model.

> enforcementEligibility(V)
> -> contributesTo(V, E)

> enforcementEligibility(V)
> =/=> determination(D)

## 22.6 Execution, successor state, and commitment

Execution may derive the protocol-prescribed successor-state material.

Execution does not itself establish an authoritative committed state change.

> executed(U)
> =/=> committed(U)

> derivesPostState(U, Q1)
> =/=> establishesPostState(U, Q1)

> committed(U)
> -> establishesPostState(U, Q1)

## 22.7 Published Result and public protocol-state consequence

A Published Result is an interface-level semantic result.

A public protocol-state consequence is the bounded consequence of one committed
Protocol State Transition.

Neither becomes an Evaluation Outcome object.

> publishedResult(Y)
> =/=> evaluationOutcomeObject(Y)

> publicProtocolConsequence(U, Q1)
> =/=> independentConsequenceObject(Q1)

## 22.8 Compatibility and Conformance

The earlier combined Compatibility / Conformance synthesis provides
invariant-preservation constraints.

The dedicated Compatibility and Conformance models own their respective formal
definitions.

No combined synthesis statement may override those later bounded models.

These normalization rules resolve editorial overlap.

They introduce no new semantics.

# 23. Dependency Direction

Specification dependencies are directional.

The complete dependency order is:

> protocol identity, generation, publication, and authority
> ->
> normative language and terminology
> ->
> protocol boundaries, subjects, and identifiers
> ->
> privacy and compositional unlinkability
> ->
> interfaces, operations, proofs, public inputs, and validity
> ->
> Protocol Actions
> ->
> Evaluation and Determination
> ->
> acceptance, rejection, and accepted no-transition behavior
> ->
> transition mappings and preconditions
> ->
> Protocol State Transition authorization
> ->
> transition execution and commitment
> ->
> state, history, and public consequences
> ->
> failure, stale authorization, and re-evaluation
> ->
> application, adapter, runtime, and implementation boundaries
> ->
> compatibility and implementation profiles
> ->
> reference implementations
> ->
> conformance
> ->
> certification

Formally:

> dependsOn(N2, N1)
> -> orderedBefore(N1, N2)

No downstream layer may redefine an upstream requirement.

# 24. Specification Composition Order

Incremental normative composition should proceed in the following bounded
order:

1. SF-01 — Authority, Scope, and Normative Interpretation;
2. SF-02 — Protocol Generation, Publication, Versioning, and Lineage;
3. SF-03 — Protocol Terminology, Subjects, and Identifiers;
4. SF-04 — Privacy, Actor Separation, and Compositional Unlinkability;
5. SF-05 — Interface Contracts, Protocol Surfaces, Operations, and Results;
6. SF-06 — Proofs, Public Inputs, Verification, Evidence, and Validity;
7. SF-07 — Protocol Actions and Applicable Rules;
8. SF-08 — Evaluation, Determination, Acceptance, and Rejection;
9. SF-09 — Protocol State, Transition Semantics, Preconditions, and
   Authorization;
10. SF-10 — Transition Execution, Commitment, Atomicity, and State Evolution;
11. SF-11 — History, Public Consequences, Failure, Staleness, and
    Re-evaluation;
12. SF-12 — Application, Adapter, Runtime, and Integration Boundaries;
13. SF-13 — Implementation, Realization, Compatibility, and Migration;
14. SF-14 — Implementation Profiles and Reference Implementations;
15. SF-15 — Conformance and Certification;
16. SF-16 — Semantic Preservation and Explicit Exclusions;
17. complete specification consolidation review.

Several adjacent section families may be composed within one Engineering slice
where their dependency boundary remains explicit.

The composition order is editorial.

Semantic dependency remains authoritative.

# 25. Protocol-Use Chain Placement

The completed protocol-use chain is:

> Private Actor
> ->
> Public Protocol Action
> ->
> Protocol Action Evaluation
> ->
> Protocol Action Determination
> ->
> Acceptance or Rejection
> ->
> Possible Protocol State Transition
> ->
> Possible committed public protocol-state consequence

Its placement is:

- private/public subject boundary: SF-03 and SF-04;
- Protocol Action: SF-07;
- Evaluation and Determination: SF-08;
- transition mapping and authorization: SF-09;
- execution and commitment: SF-10;
- history and public consequence: SF-11;
- implementation and application boundaries: SF-12 and SF-13.

No intermediate first-class subject may be introduced during composition.

# 26. Privacy Requirement Placement

SF-04 is the authoritative home for:

- private actors and public protocol subjects;
- anonymity;
- unlinkability;
- compositional privacy;
- anonymous membership continuity;
- enrollment separation;
- nullifier-based uniqueness;
- forbidden correlation;
- observability constraints.

Other sections may reference SF-04 when defining:

- public inputs;
- Protocol Action identity;
- public state;
- Published Results;
- application adapters;
- implementation logs;
- conformance evidence.

They must not redefine privacy.

> nonIdentifying(S1)
> and nonIdentifying(S2)
> and ...
> and nonIdentifying(Sn)
> -> nonIdentifying(composition(S1, S2, ..., Sn))

# 27. Proof and Validity Placement

SF-06 is the authoritative home for:

- proofs;
- declared public inputs;
- proof verification;
- bounded verification results;
- proof evidence;
- non-proof validity conditions;
- the distinction between cryptographic validity and protocol validity.

SF-07 owns applicable action rules.

SF-08 owns complete Evaluation and Determination.

Proof verification contributes evidence.

It does not independently establish Protocol Action acceptance.

> verifies(V, Z, PI)

> contributesTo(V, E)

> verifiesValid(V, Z, PI)
> =/=> protocolValid(A, C)

> verifiesValid(V, Z, PI)
> =/=> accepts(D, A)

> verifiesValid(V, Z, PI)
> =/=> committed(U)

# 28. State and Transition Placement

SF-09 owns:

- protocol-state definitions needed before transition;
- published transition mappings;
- transition preconditions;
- transition eligibility;
- Protocol State Transition occurrence identity;
- transition authorization;
- transition cardinality.

SF-10 owns:

- transition execution;
- transition preservation;
- successor-state derivation;
- commitment;
- atomicity;
- authoritative post-state establishment;
- state evolution.

SF-11 owns:

- protocol-state history;
- committed public consequences;
- failure;
- staleness;
- re-evaluation.

The transition preservation rule remains:

> U -> preserved(U)

If execution cannot preserve `U`:

> U -> transitionFailure(U)

The forbidden path remains:

> U -> U'

where:

> U' != U

Only commitment establishes authoritative state change.

# 29. Failure-Semantics Placement

SF-11 is the authoritative home for cross-stage failure classification and
separation.

Stage-local sections may define the conditions detected at that stage.

They must reference SF-11 for cross-stage meaning.

The following remain distinct:

- pre-evaluation failure;
- Evaluation failure;
- rejection;
- accepted no-transition;
- pre-transition failure;
- transition failure;
- stale authorization;
- implementation error;
- incorrect execution;
- incorrect reporting.

Required non-equivalences include:

> evaluationFailure(E)
> =/=> rejects(D, A)

> transitionFailure(U)
> =/=> rejects(D, A)

> transitionFailure(U)
> =/=> evaluationFailure(E)

> staleAuthorization(U)
> =/=> incorrect(D)

> incorrectExecution(I, U)
> =/=> changesSemantics(P)

# 30. Application and Implementation Placement

SF-12 owns:

- application requests and responses;
- application-adapter translation;
- application meaning;
- runtime responsibility;
- integration boundaries;
- forbidden information crossings.

SF-13 owns:

- implementation identity;
- implementation obligations;
- realization;
- compatibility;
- prohibited implementation authority;
- version-compatible replacement;
- migration constraints.

The boundary remains:

> applicationDefinesMeaning(App)

> protocolDefinesValidity(P)

> implementationRealizes(I, P)

> implementationRealizes(I, P)
> =/=> implementationDefines(I, P)

Applications interpret public protocol state within application authority.

They do not redefine protocol truth.

# 31. Conformance and Certification Placement

SF-14 owns implementation profiles and reference implementations.

SF-15 owns:

- published conformance requirements;
- conformance requirement sets;
- artifacts;
- evidence;
- packages;
- claims;
- assessments;
- determinations;
- certification bases;
- certification decisions;
- certification statuses;
- certification recognition.

The governing direction is:

> Published Protocol Generation
> ->
> Protocol Specification
> ->
> Implementation Profile
> ->
> Implementation
> ->
> Conformance Determination
> ->
> Certification

A reference implementation demonstrates one permitted realization.

It does not define requirements.

Conformance evaluates implementation satisfaction.

It does not create obligations.

Certification recognizes bounded conformance.

It does not perform conformance assessment or define protocol semantics.

# 32. Traceability Model

Every normative requirement in the final Protocol Specification must possess a
traceability record containing:

- requirement identifier;
- requirement family identifier;
- authoritative specification section;
- source identifier or identifiers;
- requirement strength;
- applicability;
- supporting cross-references;
- semantic-preservation status.

The minimum requirement identifier form is:

> PE-<family>-<number>

The exact editorial identifier syntax may be finalized during the first
normative composition slice.

The identifier must remain stable after publication.

The composition map maintains source-level traceability.

The final specification maintains requirement-level traceability.

Verbose source citations need not appear in every normative paragraph.

A compact traceability appendix or maintained mapping table is sufficient if it
permits complete review.

# 33. Privacy-Language Preservation

Naming and documentation surfaces form part of the privacy boundary.

Specification headings, requirement identifiers, examples, tables,
cross-references, diagnostics, conformance evidence, and certification language
must not introduce:

- wallet-shaped anonymous identity;
- sponsor-shaped identity;
- admission-to-action correlation;
- reusable participant identity;
- cross-action identity;
- identity-bearing diagnostics;
- route-shaped actor identity;
- private-actor reconstruction;
- or application metadata as protocol truth.

Neutral protocol terminology must be used.

Public protocol subjects may possess protocol identity.

That identity must not identify a private actor.

> identifiesProtocolSubject(id(S), S)
> =/=> identifiesActor(id(S), X)

The governing rule remains:

> Private actors, public actions.

# 34. Preservation of Protocol Semantics

Composition must preserve the complete semantics of the published protocol
generation.

> semantics(Spec) = semantics(P)

For every source-derived requirement:

> derives(R, P)

> semantics(R) subsetOf semantics(P)

For every implementation profile:

> derives(Profile, Spec)

> semantics(Profile) subsetOf semantics(Spec)

Editorial composition must not:

- weaken requirements;
- strengthen requirements;
- merge distinct identities;
- split one requirement into contradictory requirements;
- create hidden exceptions;
- convert informative material into normative material;
- convert implementation behavior into protocol law;
- or create application-specific protocol semantics.

# 35. Protocol Authority

Protocol authority always remains with the published Privacy Engine protocol generation.

The Protocol Specification derives from that generation.

Implementation profiles derive from the Protocol Specification.

Implementations realize implementation profiles.

Reference implementations demonstrate permitted realizations.

Conformance evaluates implementations.

Certification recognizes bounded conformance.

No composition map, source document, section, requirement set, implementation,
runtime, application, adapter, compatibility declaration, conformance object,
certification object, proof, verification result, Protocol Action,
Determination, or Protocol State Transition acquires protocol authority.

> maps(M, C, Spec)
> =/=> definesProtocol(M, P)

# 36. Coverage Assessment

Coverage is complete when:

1. every included source has one source role;
2. every positive source maps to one or more requirement families;
3. every negative assessment maps to an exclusion;
4. every consolidation review constrains the map globally;
5. every requirement family has one authoritative section family;
6. every source mapping preserves privacy and authority constraints;
7. every dependency predecessor is ordered before its dependent destination;
8. every repeated invariant is consolidated;
9. every source row has complete traceability status.

The completed assessment establishes:

> forall F in C:
> classified(F)

> positiveSource(F)
> -> existsNormativeDestination(F, N)

> negativeAssessment(F)
> -> existsExclusionDestination(F, SF-16)

> consolidationReview(F)
> -> constrainsGlobally(F, Spec)

All sixty-six source rows are classified.

All positive formal and boundary sources have normative destinations.

The negative assessment has an exclusion destination.

Both consolidation reviews possess global constraint roles.

No formal-model family is omitted.

# 37. Remaining Mapping Gaps

No unresolved architectural mapping gap remains.

The review identified bounded editorial-normalization requirements concerning:

- interface-contract authority wording;
- runtime-authority wording;
- Protocol Operation versus Protocol Action;
- Protocol Transition mapping versus Protocol State Transition occurrence;
- Protocol Enforcement versus complete Protocol Action Evaluation;
- execution and successor-state derivation versus commitment;
- Published Result versus committed public protocol-state consequence;
- earlier combined Compatibility / Conformance synthesis versus later dedicated
  models.

Section 22 resolves each issue without altering established semantics.

Detailed normative wording, individual requirement identifiers, and exact
requirement strength remain future composition work.

Those are composition tasks.

They are not mapping gaps.

# 38. Composition Determination

The bounded assessment determines:

1. the complete relevant formal source corpus is identifiable;
2. every source has a valid primary role;
3. every positive formal model has a normative destination;
4. negative assessment is preserved without artificial ontology;
5. consolidation reviews constrain composition without becoming duplicate
   sections;
6. each semantic requirement can have one authoritative home;
7. supporting references can remain non-authoritative;
8. repeated invariants can be consolidated without semantic loss;
9. dependency order is coherent;
10. the protocol-use chain maps completely;
11. privacy requirements map completely;
12. proof and validity requirements map completely;
13. state, transition, history, and failure requirements map completely;
14. application and implementation boundaries map completely;
15. compatibility, conformance, and certification map correctly;
16. compact traceability is possible without reducing developer usability;
17. privacy-language discipline is preserved;
18. no unresolved source contradiction remains;
19. no new ontology is justified.

Therefore:

> completeCompositionMap(M)

> validCompositionMap(M)

> readyForNormativeComposition(C, Spec)

# 39. Readiness for Normative Specification Composition

The completed Privacy Engine formal corpus can be mapped completely and
non-duplicatively into one implementation-facing normative Protocol
Specification.

Incremental normative specification composition may begin.

Each future slice must:

- compose only its assigned section family or bounded group;
- derive requirements from the mapped source families;
- assign stable requirement identifiers;
- assign explicit requirement strength;
- preserve one authoritative home;
- use supporting references rather than repeated definitions;
- preserve the dependency order;
- preserve privacy-language discipline;
- preserve protocol semantics;
- preserve protocol authority;
- and remain subordinate to `STATE.md`.

After all section families are composed, the complete specification must receive
one final consolidation review.

# 40. Explicit Exclusions

This composition map does not:

- redefine the published protocol generation;
- redefine any established formal subject;
- add a new first-class subject;
- reopen the foundational ontology;
- alter Protocol Action identity;
- merge Evaluation and Determination;
- introduce an Evaluation Outcome object;
- introduce a Protocol Claim;
- merge acceptance and commitment;
- introduce a transition-set object;
- alter transition cardinality;
- merge failure classifications;
- make execution equivalent to commitment;
- make a Published Result equivalent to a public protocol-state consequence;
- make application meaning equivalent to protocol truth;
- make an implementation profile equivalent to the Protocol Specification;
- make a reference implementation authoritative;
- make compatibility equivalent to conformance;
- make conformance equivalent to certification;
- create one specification section per source document;
- duplicate normative authority;
- treat supporting references as normative definitions;
- define blockchain consensus;
- define transaction formats;
- define transport, relay, database, or storage mechanics;
- define application-specific semantics;
- introduce actor identity;
- introduce reusable participant identity;
- introduce cross-action linkage;
- introduce identity-bearing diagnostics;
- or compose the complete final Protocol Specification in this slice.

# 41. Conclusion

The Privacy Engine Protocol Specification Composition Map identifies and maps
the complete bounded sixty-six-source formal corpus.

Every included source possesses:

- a bounded source role;
- an identified architectural subject or constraint;
- one or more valid requirement-family destinations;
- preserved dependency relationships;
- preserved privacy constraints;
- preserved authority constraints;
- and complete traceability status.

The map establishes fifty normative requirement families and sixteen
authoritative specification section families.

Every semantic requirement must have one authoritative normative home.

Supporting references must remain non-authoritative.

Repeated architectural statements must be consolidated without semantic loss.

Earlier and later formulations are reconciled through bounded editorial
normalization rather than ontology expansion.

The protocol-use chain maps completely.

Privacy, proof, validity, state, transition, history, failure, application,
implementation, compatibility, conformance, and certification requirements all
possess valid destinations.

No unresolved architectural contradiction remains.

No new first-class architectural subject is justified.

The completed Privacy Engine formal-model corpus is ready for incremental
composition into one portable, developer-facing normative Protocol
Specification.

STATE.md remains canonical.

Protocol authority always remains with the published Privacy Engine protocol generation.
