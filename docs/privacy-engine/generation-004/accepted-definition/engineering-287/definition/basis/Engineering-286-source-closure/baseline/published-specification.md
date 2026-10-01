<a id="pe-protocol-specification-g3"></a>
# Privacy Engine Protocol Specification PE-G3 Candidate V1

Identifier:
PE-PROTOCOL-SPECIFICATION-G3

Document version:
V1

Successor generation:
PE-PROTOCOL-GENERATION-003

Status:
unreviewed-unpublished-non-authoritative

## Specification Identity

Specification identity artifact: PE-G3-PROTOCOL-SPECIFICATION-IDENTITY-001
Specification identity SHA-256: 81e41f40d33bffc22fd2253f98146d347935ae70c5432ded124d80efd46a3067
Specification identifier: PE-PROTOCOL-SPECIFICATION-G3
Specification version: 3.0.0
Governing generation: PE-PROTOCOL-GENERATION-003

<a id="pe-g3-sf-01"></a>
## SF-01 — Authority, Scope, and Normative Interpretation

<a id="pe-g3-rf-01"></a>
### RF-01 — Specification identity, derivation, completeness, and authority

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-spec-001"></a> PE-G3-SPEC-001 | MUST | applicable | Every Privacy Engine Protocol Specification | A Protocol Specification MUST possess one stable specification identity and MUST identify its specification version. | PE-G3-SOURCE-S03, PE-G3-SOURCE-S08 | NONE |
| <a id="pe-g3-spec-002"></a> PE-G3-SPEC-002 | MUST | applicable | Every completed Privacy Engine Protocol Specification | A completed Protocol Specification MUST identify exactly one published Privacy Engine protocol generation from which it derives. | PE-G3-SOURCE-S08 | NONE |
| <a id="pe-g3-spec-003"></a> PE-G3-SPEC-003 | MUST | applicable | Every Privacy Engine Protocol Specification | A Protocol Specification MUST preserve the semantics and obligations of the published protocol generation from which it derives. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S17 | NONE |
| <a id="pe-g3-spec-004"></a> PE-G3-SPEC-004 | MUST | applicable | Every completed Privacy Engine Protocol Specification | A completed Protocol Specification MUST contain the complete implementation-facing normative composition required to implement its identified published protocol generation without dependence on hidden repository context. | PE-G3-SOURCE-S03, PE-G3-SOURCE-S08 | NONE |
| <a id="pe-g3-spec-005"></a> PE-G3-SPEC-005 | MUST NOT | applicable | Every incomplete cumulative Protocol Specification | An incomplete cumulative Protocol Specification MUST NOT claim completeness, final publication status, or suitability as the complete conformance basis. | PE-G3-SOURCE-S03, PE-G3-SOURCE-S07, PE-G3-SOURCE-S08 | NONE |
| <a id="pe-g3-spec-006"></a> PE-G3-SPEC-006 | MUST NOT | applicable | Every Privacy Engine Protocol Specification and every interpretation of it | A Protocol Specification MUST NOT be treated as independent protocol authority or as authority to modify its source protocol generation. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | NONE |
| <a id="pe-g3-spec-007"></a> PE-G3-SPEC-007 | MUST | applicable | Every cumulative Protocol Specification | A cumulative Protocol Specification MUST state its composition status, composed section families, deferred section families, and current completeness boundary. | PE-G3-SOURCE-S03, PE-G3-SOURCE-S07, PE-G3-SOURCE-S08 | NONE |
| <a id="pe-g3-spec-008"></a> PE-G3-SPEC-008 | MUST | applicable | Every semantic requirement composed into the Protocol Specification | Each semantic requirement MUST possess exactly one authoritative normative home within the Protocol Specification, excluding every supporting reference from authoritative-home status. | PE-G3-SOURCE-S06, PE-G3-SOURCE-S07, PE-G3-SOURCE-S08 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-spec-009"></a> PE-G3-SPEC-009 | MUST | applicable | Every implementation profile | The Protocol Specification MUST establish the downstream derivation rule requiring the implementation profile to identify the Protocol Specification and published Protocol Generation from which its applicable obligations derive. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10 | NONE |

<a id="pe-g3-rf-02"></a>
### RF-02 — Protocol definition, scope, and invariant ownership

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-prot-001"></a> PE-G3-PROT-001 | MUST | applicable | Every Privacy Engine Protocol definition | The Privacy Engine Protocol MUST be defined independently of any particular implementation, application, deployment, transport, storage system, or execution environment. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S17 | NONE |
| <a id="pe-g3-prot-002"></a> PE-G3-PROT-002 | MUST | applicable | Every published Privacy Engine protocol generation | A published protocol generation MUST declare the complete bounded protocol scope represented by that generation. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S10 | NONE |
| <a id="pe-g3-prot-003"></a> PE-G3-PROT-003 | MUST | applicable | Every protocol invariant | Each protocol invariant MUST remain owned by the published protocol generation in which it is defined. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S10, PE-G3-SOURCE-S17 | NONE |
| <a id="pe-g3-prot-004"></a> PE-G3-PROT-004 | MUST NOT | applicable | Every downstream specification, profile, implementation, application, assessment, and certification artifact | A downstream artifact MUST NOT redefine, weaken, strengthen, omit, or silently reinterpret an applicable protocol invariant. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S09, PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | NONE |
| <a id="pe-g3-prot-005"></a> PE-G3-PROT-005 | MUST | applicable | Every claim of complete protocol realization | A claim of complete protocol realization MUST account for every applicable invariant and normative requirement of the identified published protocol generation. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S09 | NONE |
| <a id="pe-g3-prot-006"></a> PE-G3-PROT-006 | MUST NOT | applicable | Every application and implementation using the Privacy Engine Protocol | Application-defined meaning and implementation-defined mechanism MUST NOT be represented as protocol-defined meaning unless the identified published protocol generation explicitly defines it. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | NONE |

<a id="pe-g3-rf-05"></a>
### RF-05 — Normative language, interpretation, applicability, and strength

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-norm-001"></a> PE-G3-NORM-001 | MUST | applicable | Every statement in the Protocol Specification | Every specification statement MUST be classifiable as normative or informative. | PE-G3-SOURCE-S04 | NONE |
| <a id="pe-g3-norm-002"></a> PE-G3-NORM-002 | MUST | applicable | Every requirement using `MUST` | A requirement using `MUST` MUST be interpreted as mandatory throughout its declared applicability scope. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05 | NONE |
| <a id="pe-g3-norm-003"></a> PE-G3-NORM-003 | MUST | applicable | Every requirement using `MUST NOT` | A requirement using `MUST NOT` MUST be interpreted as prohibiting the stated behavior throughout its declared applicability scope. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05 | NONE |
| <a id="pe-g3-norm-004"></a> PE-G3-NORM-004 | MUST | applicable | Every requirement using `SHOULD` | A requirement using `SHOULD` MUST be interpreted as recommended; deviation MUST be bounded, understood, and justified without violating any mandatory requirement. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05 | NONE |
| <a id="pe-g3-norm-005"></a> PE-G3-NORM-005 | MUST | applicable | Every requirement using `SHOULD NOT` | A requirement using `SHOULD NOT` MUST be interpreted as discouraged; contrary behavior MUST be bounded, understood, and justified without violating any mandatory requirement. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05 | NONE |
| <a id="pe-g3-norm-006"></a> PE-G3-NORM-006 | MUST | applicable | Every requirement using `MAY` | A requirement using `MAY` MUST be interpreted as permitting, but not requiring, the stated behavior. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05 | NONE |
| <a id="pe-g3-norm-007"></a> PE-G3-NORM-007 | MUST | applicable | Every declaration of implementation-defined behavior | Implementation-defined behavior MUST be explicitly permitted, bounded by the applicable protocol requirements, and documented by the implementation. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05 | NONE |
| <a id="pe-g3-norm-008"></a> PE-G3-NORM-008 | MUST | applicable | Every normative requirement | Every normative requirement MUST declare a bounded applicability rule identifying the subjects and conditions to which it applies. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05, PE-G3-SOURCE-S06 | NONE |
| <a id="pe-g3-norm-009"></a> PE-G3-NORM-009 | MUST | applicable | Every interpretation of a normative requirement | A normative requirement MUST be interpreted using its identifier, requirement text, defined terminology, applicability rule, authoritative section, and applicable cross-references as one coherent requirement. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05, PE-G3-SOURCE-S07 | NONE |
| <a id="pe-g3-norm-010"></a> PE-G3-NORM-010 | MUST NOT | applicable | Every supporting cross-reference and informative statement | A supporting cross-reference or informative statement MUST NOT independently create, modify, complete, weaken, strengthen, conceal, or relocate a normative obligation. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S07 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-norm-011"></a> PE-G3-NORM-011 | MUST | applicable | Every normative requirement | Every normative requirement MUST possess exactly one stable identifier in the form `PE-<SEMANTIC-FAMILY>-<NNN>`, and that identifier MUST denote exactly one semantic requirement. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S06 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-norm-012"></a> PE-G3-NORM-012 | MUST NOT | applicable | Every requirement identifier lifecycle | A requirement identifier MUST NOT be changed because of editorial reordering and MUST NOT be silently reused for a different semantic requirement. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S06 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-norm-013"></a> PE-G3-NORM-013 | MUST | applicable | Every normative requirement | Every normative requirement MUST record its requirement family, strength, applicability, authoritative section, and supporting source traceability. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S06, PE-G3-SOURCE-S07 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-norm-014"></a> PE-G3-NORM-014 | MUST | applicable | Every apparently obligatory specification statement | Every statement intended to impose an obligation MUST be expressed as a stable identified normative requirement rather than apparently mandatory prose. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05 | NONE |

<a id="pe-g3-sf-02"></a>
## SF-02 — Protocol Generation, Publication, Versioning, and Lineage

<a id="pe-g3-rf-03"></a>
### RF-03 — Protocol generation, publication, and Published Protocol

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-gen-001"></a> PE-G3-GEN-001 | MUST | applicable | Every Privacy Engine Protocol Generation | A Protocol Generation MUST possess one unique and stable generation identity. | PE-G3-SOURCE-S10 | NONE |
| <a id="pe-g3-gen-002"></a> PE-G3-GEN-002 | MUST | applicable | Every Privacy Engine Protocol Generation | A Protocol Generation MUST contain one bounded and complete protocol semantic state. | PE-G3-SOURCE-S10 | NONE |
| <a id="pe-g3-gen-003"></a> PE-G3-GEN-003 | MUST NOT | applicable | Every incomplete protocol fragment or partial change | An incomplete protocol fragment or partial change MUST NOT be represented as a complete Protocol Generation. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S11 | NONE |
| <a id="pe-g3-gen-004"></a> PE-G3-GEN-004 | MUST | applicable | Every Protocol Generation lifecycle | A Protocol Generation MUST retain the same identity through publication, coexistence, deprecation, migration, and retirement. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S13, PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-gen-005"></a> PE-G3-GEN-005 | MUST | applicable | Every Protocol Publication | A Protocol Publication MUST identify exactly one complete Protocol Generation as its publication subject. | PE-G3-SOURCE-S11 | NONE |
| <a id="pe-g3-gen-006"></a> PE-G3-GEN-006 | MUST | applicable | Every Protocol Publication | A Protocol Publication MUST identify the complete published material, generation identity, publication identity, and publication version required to distinguish its result. | PE-G3-SOURCE-S11, PE-G3-SOURCE-S12, PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-gen-007"></a> PE-G3-GEN-007 | MUST NOT | applicable | Every incomplete or ambiguous publication occurrence | An incomplete or ambiguously identified publication MUST NOT establish a Published Protocol. | PE-G3-SOURCE-S11, PE-G3-SOURCE-S12 | NONE |
| <a id="pe-g3-gen-008"></a> PE-G3-GEN-008 | MUST NOT | applicable | Every Protocol Publication | A Protocol Publication MUST NOT be interpreted as Protocol Succession, Protocol Lineage membership, compatibility, deprecation, migration, or retirement unless those relationships are separately and explicitly established. | PE-G3-SOURCE-S11, PE-G3-SOURCE-S13, PE-G3-SOURCE-S14, PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-gen-009"></a> PE-G3-GEN-009 | MUST | applicable | Every Published Protocol | A Published Protocol MUST identify exactly one Protocol Generation and exactly one complete publication of that generation. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S11, PE-G3-SOURCE-S12 | NONE |
| <a id="pe-g3-gen-010"></a> PE-G3-GEN-010 | MUST | applicable | Every Published Protocol | A Published Protocol MUST possess a stable identity distinct from the identity of its Protocol Generation and its Protocol Publication. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S11, PE-G3-SOURCE-S12 | NONE |
| <a id="pe-g3-gen-011"></a> PE-G3-GEN-011 | MUST NOT | applicable | Every Published Protocol | A Published Protocol MUST NOT be silently replaced, partially rewritten, or reinterpreted as a different generation. | PE-G3-SOURCE-S12, PE-G3-SOURCE-S13, PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-gen-012"></a> PE-G3-GEN-012 | MUST | applicable | Every published Privacy Engine protocol generation | Each published Privacy Engine protocol generation MUST remain the protocol authority for its own identified semantics and obligations throughout its recorded lifecycle. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S12, PE-G3-SOURCE-S13, PE-G3-SOURCE-S16, PE-G3-SOURCE-S17 | NONE |
| <a id="pe-g3-gen-013"></a> PE-G3-GEN-013 | MUST | applicable | Every Protocol Publication claiming completeness | A Protocol Publication claiming completeness MUST contain or unambiguously bind every component required to reconstruct the complete published generation. | PE-G3-SOURCE-S11, PE-G3-SOURCE-S12 | NONE |
| <a id="pe-g3-gen-014"></a> PE-G3-GEN-014 | MUST | applicable | Every Published Protocol | A Published Protocol MUST remain immutable after publication. | PE-G3-SOURCE-S12 | NONE |
| <a id="pe-g3-gen-015"></a> PE-G3-GEN-015 | MUST | applicable | Every correction, clarification, or replacement affecting published material | A correction, clarification, or replacement affecting published material MUST be separately identified and MUST preserve the identity and historical content of the earlier Published Protocol. | PE-G3-SOURCE-S12, PE-G3-SOURCE-S13, PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-gen-016"></a> PE-G3-GEN-016 | MUST NOT | applicable | Every incomplete publication | An incomplete publication MUST NOT be used as the authoritative representation of a complete Protocol Generation. | PE-G3-SOURCE-S11, PE-G3-SOURCE-S12 | NONE |
| <a id="pe-g3-gen-017"></a> PE-G3-GEN-017 | MUST | applicable | Every Privacy Engine implementation | An implementation MUST identify exactly which published Protocol Generation it targets. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S12 | NONE |
| <a id="pe-g3-gen-018"></a> PE-G3-GEN-018 | MUST | applicable | Every conformance determination | A conformance determination MUST identify the implementation, implementation profile, Protocol Specification, and published Protocol Generation against which conformance is assessed. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S18 | NONE |
| <a id="pe-g3-gen-019"></a> PE-G3-GEN-019 | MUST | applicable | Every certification | A certification MUST identify the conformance basis and published Protocol Generation to which the certification applies. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S18 | NONE |
| <a id="pe-g3-gen-020"></a> PE-G3-GEN-020 | MUST NOT | applicable | Every downstream implementation or assessment artifact | A downstream implementation, profile, conformance determination, or certification MUST NOT modify the identity, semantics, obligations, lifecycle, or authority of its referenced published Protocol Generation. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | NONE |

<a id="pe-g3-rf-04"></a>
### RF-04 — Succession, lineage, versioning, deprecation, and migration

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-evol-001"></a> PE-G3-EVOL-001 | MUST | applicable | Every Protocol Succession relationship | A Protocol Succession relationship MUST identify exactly one predecessor Protocol Generation and one distinct successor Protocol Generation. | PE-G3-SOURCE-S13 | NONE |
| <a id="pe-g3-evol-002"></a> PE-G3-EVOL-002 | MUST | applicable | Every successor Protocol Generation | A successor Protocol Generation MUST possess an identity distinct from every predecessor generation. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S13 | NONE |
| <a id="pe-g3-evol-003"></a> PE-G3-EVOL-003 | MUST | applicable | Every Protocol Succession relationship | Protocol Succession MUST preserve the identity, published content, lifecycle record, and historical truth of the predecessor generation. | PE-G3-SOURCE-S12, PE-G3-SOURCE-S13 | NONE |
| <a id="pe-g3-evol-004"></a> PE-G3-EVOL-004 | MUST NOT | applicable | Every Protocol Succession relationship | Protocol Succession MUST NOT mutate, rename, merge, delete, or retroactively reinterpret its predecessor generation. | PE-G3-SOURCE-S13 | NONE |
| <a id="pe-g3-evol-005"></a> PE-G3-EVOL-005 | MUST NOT | applicable | Every Protocol Publication | Publication of a generation MUST NOT by itself establish succession from any other generation. | PE-G3-SOURCE-S11, PE-G3-SOURCE-S13 | NONE |
| <a id="pe-g3-evol-006"></a> PE-G3-EVOL-006 | MUST | applicable | Every Protocol Lineage | A Protocol Lineage MUST possess one stable lineage identity distinct from the identities of its member generations. | PE-G3-SOURCE-S14 | NONE |
| <a id="pe-g3-evol-007"></a> PE-G3-EVOL-007 | MUST | applicable | Every Protocol Lineage membership claim | A Protocol Generation MUST be included in a lineage only through an explicit lineage-membership rule supported by the applicable succession structure. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S14 | NONE |
| <a id="pe-g3-evol-008"></a> PE-G3-EVOL-008 | MUST | applicable | Every Protocol Lineage | A Protocol Lineage MUST preserve the separate identities and lifecycle records of all member generations. | PE-G3-SOURCE-S14 | NONE |
| <a id="pe-g3-evol-009"></a> PE-G3-EVOL-009 | MUST NOT | applicable | Every Protocol Lineage | A Protocol Lineage MUST NOT create, inherit, transfer, or replace the protocol authority of any member generation. | PE-G3-SOURCE-S14, PE-G3-SOURCE-S17 | NONE |
| <a id="pe-g3-evol-010"></a> PE-G3-EVOL-010 | MUST | applicable | Every Protocol Lineage model | A Protocol Lineage model MUST permit independent Protocol Generations to remain in separate Protocol Lineages and MUST require an explicit succession relationship before placing generations in one lineage. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S14 | NONE |
| <a id="pe-g3-evol-011"></a> PE-G3-EVOL-011 | MUST NOT | applicable | Every Protocol Lineage membership claim | Lineage membership MUST NOT by itself be interpreted as compatibility, migration eligibility, deprecation, replacement, or semantic equivalence. | PE-G3-SOURCE-S14, PE-G3-SOURCE-S15, PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-evol-012"></a> PE-G3-EVOL-012 | MUST | applicable | Every published Protocol Generation | Every published Protocol Generation MUST possess a stable version designation sufficient to distinguish it from every other published generation. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-evol-013"></a> PE-G3-EVOL-013 | MUST NOT | applicable | Every protocol version designation | A version designation MUST NOT by itself be interpreted as proof of compatibility, incompatibility, succession, migration eligibility, or semantic equivalence. | PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-evol-014"></a> PE-G3-EVOL-014 | MUST | applicable | Every protocol semantic change | A change to protocol-defined semantics, obligations, validity, invariants, or permitted behavior MUST be represented by a distinct Protocol Generation. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S13, PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-evol-015"></a> PE-G3-EVOL-015 | MUST NOT | applicable | Every published Protocol Generation | Semantic change MUST NOT be introduced through silent mutation, editorial replacement, implementation variation, or reinterpretation of an existing Published Protocol. | PE-G3-SOURCE-S12, PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-evol-016"></a> PE-G3-EVOL-016 | MUST | applicable | Every classification of a protocol change | A protocol change MUST be classified according to its semantic effect rather than only its label, release number, implementation impact, or publication format. | PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-evol-017"></a> PE-G3-EVOL-017 | MUST | applicable | Every claim of compatible evolution | A claim of compatible evolution MUST identify the generations, requirements, subjects, and compatibility scope to which the claim applies. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-evol-018"></a> PE-G3-EVOL-018 | MAY | applicable | Every implementation variation within one published generation | An implementation variation MAY occur without a new Protocol Generation only when every applicable protocol semantic and normative requirement remains preserved. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-evol-019"></a> PE-G3-EVOL-019 | MUST | applicable | Every compatible successor generation | A compatible successor generation MUST remain distinctly identified and MUST preserve every predecessor obligation included within the declared compatibility scope. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-evol-020"></a> PE-G3-EVOL-020 | MUST | applicable | Every breaking protocol evolution | Breaking evolution MUST be represented by a distinct successor generation and MUST explicitly identify the affected compatibility boundary. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-evol-021"></a> PE-G3-EVOL-021 | MUST NOT | applicable | Every compatibility claim | Compatibility MUST NOT be used to merge generation identities, mutate historical published truth, or conceal semantic change. | PE-G3-SOURCE-S12, PE-G3-SOURCE-S13, PE-G3-SOURCE-S15 | NONE |
| <a id="pe-g3-evol-022"></a> PE-G3-EVOL-022 | MUST | applicable | Every Protocol Generation deprecation | Deprecation MUST identify the deprecated generation, the effective lifecycle condition, and any published continuation or migration guidance. | PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-evol-023"></a> PE-G3-EVOL-023 | MUST NOT | applicable | Every Protocol Generation deprecation | Deprecation MUST NOT revoke, erase, mutate, or retroactively invalidate the identity, published content, or historical truth of the deprecated generation. | PE-G3-SOURCE-S12, PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-evol-024"></a> PE-G3-EVOL-024 | MUST | applicable | Every published migration | A published migration MUST identify its source target, destination target, applicability conditions, required steps, preserved properties, and explicit failure conditions. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-evol-025"></a> PE-G3-EVOL-025 | MUST | applicable | Every mandatory migration obligation | A mandatory migration obligation MUST be expressed as an identified normative requirement with explicit applicability and requirement strength. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05, PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-evol-026"></a> PE-G3-EVOL-026 | MUST NOT | applicable | Every migration | Migration MUST NOT mutate the identity of a Protocol Generation, Published Protocol, implementation target, conformance determination, or certification. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-evol-027"></a> PE-G3-EVOL-027 | MUST NOT | applicable | Every deprecation or migration statement | A deprecation or migration statement MUST NOT silently redefine compatibility, succession, lineage membership, or protocol semantics. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S14, PE-G3-SOURCE-S15, PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-evol-028"></a> PE-G3-EVOL-028 | MUST | applicable | Every environment supporting multiple published Protocol Generations | Coexisting Protocol Generations MUST remain separately identifiable and MUST retain separate applicability, compatibility, lifecycle, and authority records. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S15, PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-evol-029"></a> PE-G3-EVOL-029 | MUST NOT | applicable | Every coexistence arrangement | Coexistence MUST NOT be interpreted as semantic equivalence, automatic compatibility, shared identity, succession, or migration eligibility. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S14, PE-G3-SOURCE-S15, PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-evol-030"></a> PE-G3-EVOL-030 | MUST | applicable | Every Protocol Generation retirement | Retirement MUST identify the retired generation, retirement scope, effective condition, and consequences for future implementation, assessment, and support. | PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-evol-031"></a> PE-G3-EVOL-031 | MUST NOT | applicable | Every Protocol Generation retirement | Retirement MUST NOT delete, mutate, conceal, or retroactively invalidate the retired generation or its historical protocol truth. | PE-G3-SOURCE-S12, PE-G3-SOURCE-S16 | NONE |
| <a id="pe-g3-evol-032"></a> PE-G3-EVOL-032 | MUST | applicable | Every lifecycle interpretation | Deprecation, migration, coexistence, and retirement MUST be interpreted as distinct bounded lifecycle concepts. | PE-G3-SOURCE-S16 | NONE |

<a id="pe-g3-sf-03"></a>
## SF-03 — Protocol Terminology, Subjects, and Identifiers

<a id="pe-g3-rf-06"></a>
### RF-06 — Protocol terminology

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-term-001"></a> PE-G3-TERM-001 | MUST | applicable | Every use of a canonical Protocol Specification term | A canonical term MUST be interpreted according to its definition and bounded role in this specification. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-term-002"></a> PE-G3-TERM-002 | MUST | applicable | Every downstream section, profile, implementation, application adapter, assessment, and supporting artifact | Every downstream use of a canonical term MUST preserve the same subject, relationship, scope, and identity distinction established by this specification. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-term-003"></a> PE-G3-TERM-003 | MUST | applicable | Every term that may denote either a protocol type or an occurrence | A term that may denote either a type or an occurrence MUST explicitly preserve the applicable type-or-occurrence distinction. | PE-G3-SOURCE-S23, PE-G3-SOURCE-S24, PE-G3-SOURCE-S26, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-term-004"></a> PE-G3-TERM-004 | MUST | applicable | Every specification definition involving a semantic subject, identifier, or representation | The terminology used for a semantic subject, its identifier, and its representation MUST preserve those as distinct concepts. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-term-005"></a> PE-G3-TERM-005 | MUST NOT | applicable | Every alias, abbreviation, implementation name, application label, and editorial synonym | An alias, abbreviation, implementation name, application label, or editorial synonym MUST NOT silently redefine, merge, widen, or narrow a canonical protocol term. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S28 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-term-006"></a> PE-G3-TERM-006 | MUST NOT | applicable | Every terminology decision and editorial reorganization | Terminology or editorial structure MUST NOT introduce a new first-class protocol subject, lifecycle, authority, or semantic boundary. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S28 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-term-007"></a> PE-G3-TERM-007 | MUST | applicable | Every permitted local alias for a canonical protocol term | A permitted local alias MUST map explicitly and unambiguously to exactly one canonical term while preserving its protocol meaning. | PE-G3-SOURCE-S17 | PE-G3-COMPOSITION-MAP-001 |

<a id="pe-g3-rf-07"></a>
### RF-07 — Protocol subject identity and identity separation

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-subj-001"></a> PE-G3-SUBJ-001 | MUST | applicable | Every established identified protocol subject | Every established identified protocol subject MUST retain its own bounded identity according to its defined architectural role. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-subj-002"></a> PE-G3-SUBJ-002 | MUST | applicable | Every Protocol Action, Protocol Action Evaluation, Protocol Action Determination, and Protocol State Transition | Protocol Action, Evaluation, Determination, and Protocol State Transition identities MUST remain mutually distinct. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-subj-003"></a> PE-G3-SUBJ-003 | MUST | applicable | Every Protocol Action Evaluation and its Protocol Action Determination | Evaluation and Determination MUST retain distinct process and result identities while remaining two bounded aspects of one architectural model. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-subj-004"></a> PE-G3-SUBJ-004 | MUST | applicable | Every Protocol Operation and associated Protocol Action | A Protocol Operation capability and each Protocol Action occurrence classified by it MUST remain distinct. | PE-G3-SOURCE-S23, PE-G3-SOURCE-S24 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-subj-005"></a> PE-G3-SUBJ-005 | MUST | applicable | Every Protocol Transition and governed Protocol State Transition | A Protocol Transition mapping and each Protocol State Transition occurrence governed by it MUST remain distinct. | PE-G3-SOURCE-S26, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-subj-006"></a> PE-G3-SUBJ-006 | MUST | applicable | Every relationship between identified protocol subjects | Every subject relationship MUST preserve its declared direction, bounded meaning, and participating subject identities. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | NONE |
| <a id="pe-g3-subj-007"></a> PE-G3-SUBJ-007 | MUST | applicable | Every protocol subject referenced through an implementation, application, runtime mechanism, or application interpretation | A protocol subject MUST remain distinct from the implementation, application, runtime mechanism, and application-defined meaning through which it is represented or used. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-subj-008"></a> PE-G3-SUBJ-008 | MUST | applicable | Every downstream representation or reference to an established protocol subject | Every downstream representation or reference MUST preserve the identity of the same established protocol subject rather than substitute a newly inferred subject. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-subj-009"></a> PE-G3-SUBJ-009 | MUST NOT | applicable | Every relationship, composition, representation, and implementation convenience involving distinct subjects | A relationship, composition, representation, or implementation convenience MUST NOT silently merge distinct protocol subjects or their identities. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-subj-010"></a> PE-G3-SUBJ-010 | MUST NOT | applicable | Every proposed extension to the established protocol-subject inventory | A proposed extension MUST NOT introduce a new first-class subject unless independent identity, meaning, semantic ownership, and irreducible lifecycle necessity are all established. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S28 | NONE |

<a id="pe-g3-rf-08"></a>
### RF-08 — Protocol identifiers and occurrence identifiers

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-id-001"></a> PE-G3-ID-001 | MUST | applicable | Every protocol identifier | Every protocol identifier MUST possess one declared bounded role identifying exactly the subject or occurrence specified by that role. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-id-002"></a> PE-G3-ID-002 | MUST | applicable | Every identified protocol subject and its identifier | A protocol subject and the identifier used to reference it MUST remain distinct. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | NONE |
| <a id="pe-g3-id-003"></a> PE-G3-ID-003 | MUST | applicable | Every protocol subject and its syntactic, serialized, stored, transmitted, or displayed representation | A semantic protocol subject and each representation of it MUST remain distinct. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-id-004"></a> PE-G3-ID-004 | MUST NOT | applicable | Every relationship between separately identified protocol subjects | The identifier of one related protocol subject MUST NOT be substituted for the identifier of another subject. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-id-005"></a> PE-G3-ID-005 | MUST NOT | applicable | Every identifier of a Protocol Action occurrence | A Protocol Action identifier MUST NOT identify, encode, imply, or reconstruct the Private Actor who performed the action. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-id-006"></a> PE-G3-ID-006 | MUST NOT | applicable | Every public Evaluation, Determination, and Protocol State Transition identifier | An Evaluation, Determination, or Protocol State Transition identifier MUST NOT identify, encode, imply, or reconstruct a Private Actor. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-id-007"></a> PE-G3-ID-007 | MUST NOT | applicable | Every implementation, transaction, retry, transport-attempt, storage, or diagnostic identifier | An operational identifier MUST NOT silently become or redefine a protocol-subject or occurrence identifier. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-id-008"></a> PE-G3-ID-008 | MUST NOT | applicable | Every protocol identifier outside its declared subject and context | A protocol identifier MUST NOT be reused outside its declared role as a universal participant identifier, cross-subject join key, or cross-action identity mechanism. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-id-009"></a> PE-G3-ID-009 | MUST | applicable | Every permitted change of protocol-subject representation | A representation change MUST preserve the identity, semantics, relationships, and bounded identifier role of the represented protocol subject. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-tseid-001-a01"></a> PE-G3-TSEID-001-A01 | MUST | applicable | ALWAYS | Every registry, mapping, profile, authorization, U, comparison attempt, definition and recovery table MUST have one identity satisfying its declared grammar. | PE-G3-SOURCE-S69, PE-G3-SOURCE-S70, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseid-001-a02"></a> PE-G3-TSEID-001-A02 | MUST | applicable | ALWAYS | Every registry, mapping, profile, authorization, U, comparison attempt, definition and recovery table MUST remain distinct from every other identity class. | PE-G3-SOURCE-S69, PE-G3-SOURCE-S70, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseid-002"></a> PE-G3-TSEID-002 | MUST | applicable | ALWAYS | Every comparison attempt identity MUST be occurrence-local, contiguous within U and immutable with its result. | PE-G3-SOURCE-S72 | NONE |

<a id="pe-g3-sf-04"></a>
## SF-04 — Privacy, Actor Separation, and Compositional Unlinkability

<a id="pe-g3-rf-09"></a>
### RF-09 — Private actors and public protocol subjects

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-actsep-001"></a> PE-G3-ACTSEP-001 | MUST | applicable | Every Privacy Engine realization of a public protocol action | Every realization MUST preserve the architectural principle `Private actors, public actions`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-actsep-002"></a> PE-G3-ACTSEP-002 | MUST | applicable | Every publicly visible Protocol Action | A publicly visible Protocol Action MUST remain verifiable to its declared protocol extent without disclosure of the Private Actor. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S24, PE-G3-SOURCE-S29 | NONE |
| <a id="pe-g3-actsep-003"></a> PE-G3-ACTSEP-003 | MUST | applicable | Every relationship between a Private Actor and a public Protocol Action | The performer relationship MUST preserve the Private Actor and Protocol Action as distinct subjects. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-actsep-004"></a> PE-G3-ACTSEP-004 | MUST | applicable | Every publicly identified protocol subject | A public protocol-subject identifier MUST identify only its declared protocol subject and role. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S21, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-actsep-005"></a> PE-G3-ACTSEP-005 | MUST | applicable | Every public protocol consequence | A public protocol consequence MUST remain attributable to the applicable public protocol occurrence without becoming attributable to a disclosed Private Actor. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S21, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-actsep-006"></a> PE-G3-ACTSEP-006 | MUST NOT | applicable | Every Protocol Action validity, authorization, uniqueness, and public-consequence rule | A rule governing a public Protocol Action MUST NOT require disclosure of civil, wallet, enrollment, admission, application, implementation, deployment, or transport identity as Private Actor identity. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S24, PE-G3-SOURCE-S29 | NONE |
| <a id="pe-g3-actsep-007"></a> PE-G3-ACTSEP-007 | MUST NOT | applicable | Every public Privacy Engine protocol surface | A public protocol surface MUST NOT require or create a reusable public participant identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S24 | NONE |

<a id="pe-g3-rf-10"></a>
### RF-10 — Privacy, anonymity, and unlinkability

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-priv-001"></a> PE-G3-PRIV-001 | MUST | applicable | Every Privacy Engine protocol action governed by anonymous-participation semantics | The protocol action MUST permit verification of its applicable validity properties without disclosure of the Private Actor. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-priv-002"></a> PE-G3-PRIV-002 | MUST | applicable | Every public value and public protocol subject exposed by an anonymous action | Private Actor identity MUST remain non-inferable from each exposed value or subject within the protocol-defined privacy boundary. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-priv-003"></a> PE-G3-PRIV-003 | MUST | applicable | Every pair or collection of anonymous Protocol Actions in distinct action contexts | Cross-action unlinkability MUST be preserved unless the published protocol generation expressly defines a narrower public relationship that remains non-identifying. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-priv-004"></a> PE-G3-PRIV-004 | MUST NOT | applicable | Every wallet identifier, wallet signature, wallet-derived value, and wallet relationship | Wallet identity MUST NOT be substituted for, used to infer, or represented as anonymous membership identity or Private Actor identity. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S29 | STATE |
| <a id="pe-g3-priv-005"></a> PE-G3-PRIV-005 | MUST NOT | applicable | Every application identifier, account, profile, metadata value, and application-defined relationship | Application identity or application metadata MUST NOT be substituted for, used to infer, or represented as protocol identity or Private Actor identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S29 | NONE |
| <a id="pe-g3-priv-006"></a> PE-G3-PRIV-006 | MUST NOT | applicable | Every implementation identifier and implementation-specific internal value | Implementation identity or internal implementation context MUST NOT be substituted for, used to infer, or represented as protocol identity or Private Actor identity. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S21 | NONE |
| <a id="pe-g3-priv-007"></a> PE-G3-PRIV-007 | MUST NOT | applicable | Every deployment identifier, topology coordinate, service identity, and infrastructure relationship | Deployment identity or infrastructure topology MUST NOT be substituted for, used to infer, or represented as protocol identity or Private Actor identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | NONE |
| <a id="pe-g3-priv-008"></a> PE-G3-PRIV-008 | MUST NOT | applicable | Every transport identifier, connection attribute, delivery path, retry path, and request context | Transport identity or delivery context MUST NOT be substituted for, used to infer, or represented as protocol identity or Private Actor identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | NONE |
| <a id="pe-g3-priv-009"></a> PE-G3-PRIV-009 | MUST NOT | applicable | Every enrollment right, admission object, funding relationship, sponsor relationship, and associated provenance | Enrollment, admission, funding, or sponsor provenance MUST NOT be carried into public-action identity or used as an action-layer correlation value. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S29 | STATE |
| <a id="pe-g3-priv-010"></a> PE-G3-PRIV-010 | MUST | applicable | Every action-local public value | An action-local public value MUST remain bounded to its declared action role, action context, and permitted protocol interpretation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-priv-011"></a> PE-G3-PRIV-011 | MUST | applicable | Every privacy-sensitive failure path | Failure handling MUST preserve Private Actor non-disclosure and the non-identity-bearing role of public values. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S29 | NONE |
| <a id="pe-g3-priv-012"></a> PE-G3-PRIV-012 | MUST NOT | applicable | Every implementation, profile, application, conformance claim, diagnostic, and specification interpretation | A Privacy Engine artifact MUST NOT claim anonymity, unlinkability, metadata protection, or transport protection beyond the bounded guarantees of the identified published protocol generation. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | STATE, PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-tsepriv-001"></a> PE-G3-TSEPRIV-001 | MUST | applicable | ALWAYS | Every mapping profile MUST project only the minimum protocol-owned components required by T. | PE-G3-SOURCE-S70 | NONE |
| <a id="pe-g3-tsepriv-002"></a> PE-G3-TSEPRIV-002 | MUST NOT | applicable | ALWAYS | A projection, authorization or comparison MUST NOT contain Private Actor identity, admission or enrollment provenance, reusable participant identity or an actor-reconstruction bridge. | PE-G3-SOURCE-S70, PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tsepriv-003-a01"></a> PE-G3-TSEPRIV-003-A01 | MUST | applicable | ALWAYS | A blinded component opening MUST remain confidential. | PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tsepriv-003-a02"></a> PE-G3-TSEPRIV-003-A02 | MUST | applicable | ALWAYS | A blinded component opening MUST be disclosed only inside an authorized comparison or independent privacy-validation boundary. | PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tsepriv-004"></a> PE-G3-TSEPRIV-004 | MUST | applicable | ALWAYS | Component identifiers, commitments and result identifiers MUST be assessed in composition for uniqueness, correlation and cross-action linkage before profile admission. | PE-G3-SOURCE-S70, PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tsepriv-005-a01"></a> PE-G3-TSEPRIV-005-A01 | MUST | applicable | ALWAYS | Failure, recovery, retry and observability surfaces MUST preserve Private actors, public actions. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tsepriv-005-a02"></a> PE-G3-TSEPRIV-005-A02 | MUST NOT | applicable | ALWAYS | Failure, recovery, retry and observability surfaces MUST NOT expand disclosure. | PE-G3-SOURCE-S72 | NONE |

<a id="pe-g3-rf-11"></a>
### RF-11 — Compositional privacy, observability, and forbidden correlation

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-comp-001"></a> PE-G3-COMP-001 | MUST | applicable | Every composition of publicly exposed Privacy Engine values, subjects, consequences, and records | The composition MUST remain non-identifying for the Private Actor within the protocol-defined privacy boundary. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-comp-002"></a> PE-G3-COMP-002 | MUST NOT | applicable | Every implementation-controlled identifier, timing label, diagnostic, serialization field, log field, storage key, route, and public response | An implementation-controlled surface MUST NOT create an actor-reconstruction, provenance, or unauthorized cross-action correlation bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S29 | STATE, PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-comp-003"></a> PE-G3-COMP-003 | MUST | applicable | Every privacy-sensitive field name, variable name, route name, log label, diagnostic, comment, example, test, serialization field, and specification term | Privacy-sensitive naming and documentation MUST use neutral terminology that preserves non-attribution and the bounded role of each value. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | STATE, PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-comp-004"></a> PE-G3-COMP-004 | MUST | applicable | Every public observability surface | Public observability MUST expose only the minimum role-bounded information required by the applicable protocol semantics. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S29 | STATE |
| <a id="pe-g3-comp-005"></a> PE-G3-COMP-005 | MUST | applicable | Every diagnostic and failure-reporting surface | A diagnostic MUST describe only the applicable protocol subject, status, or bounded failure classification without identifying or reconstructing the Private Actor. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-comp-006"></a> PE-G3-COMP-006 | MUST NOT | applicable | Every request history, telemetry record, path-acquisition record, submission record, and operational history | Operational history or telemetry MUST NOT create a persistent relationship linking private participation across protocol layers or action contexts. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-comp-007"></a> PE-G3-COMP-007 | MUST NOT | applicable | Every public protocol response, log, status surface, and diagnostic | A public surface MUST NOT expose unnecessary provenance, topology, route, provider, retry, fallback, or execution-path information capable of increasing actor correlation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-comp-008"></a> PE-G3-COMP-008 | MUST | applicable | Every information crossing between Privacy Engine layers | A layer boundary MUST pass only the minimum preserved output required by the receiving layer without carrying unrelated provenance or identity context from the preceding layer. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-comp-009"></a> PE-G3-COMP-009 | MUST | applicable | Every implementation composition exposing multiple individually non-identifying surfaces | The combined surface MUST be assessed and preserved as non-identifying rather than relying only on the independent safety of each component. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-comp-010"></a> PE-G3-COMP-010 | MUST NOT | applicable | Every informative example, supporting cross-reference, test artifact, assessment record, and documentation surface | Supporting or informative material MUST NOT introduce a correlation or identity interpretation prohibited from normative runtime surfaces. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | STATE, PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-tseobs-001"></a> PE-G3-TSEOBS-001 | MUST | applicable | ALWAYS | Public comparison output MUST be limited to U's action-bounded identity and exactly one bounded result or failure classification. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseobs-002"></a> PE-G3-TSEOBS-002 | MUST NOT | applicable | ALWAYS | A comparison result MUST NOT become an independent first-class protocol subject or reusable public participant identifier. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseobs-003"></a> PE-G3-TSEOBS-003 | MUST | applicable | ALWAYS | Diagnostics, logs, events, databases and application observations MUST remain non-authoritative for comparison, recovery and commitment. | PE-G3-SOURCE-S47, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseobs-004"></a> PE-G3-TSEOBS-004 | MUST NOT | applicable | ALWAYS | An observability surface MUST NOT disclose a blind, opening, confidential canonical component or actor-bearing correlation value. | PE-G3-SOURCE-S32, PE-G3-SOURCE-S42 | NONE |
| <a id="pe-g3-tseobs-005"></a> PE-G3-TSEOBS-005 | MUST NOT | applicable | ALWAYS | Absence or inconsistency of non-authoritative observability MUST NOT alter an authoritative comparison result or occurrence state. | PE-G3-SOURCE-S47, PE-G3-SOURCE-S72 | NONE |

<a id="pe-g3-rf-15"></a>
### RF-15 — Anonymous membership, continuity, and enrollment separation

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-mem-001"></a> PE-G3-MEM-001 | MUST | applicable | Every anonymous membership identity in the current published protocol generation | Anonymous membership identity MUST derive solely from private `memberSecret` possession through `leaf = Poseidon1(memberSecret)`. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-mem-002"></a> PE-G3-MEM-002 | MUST | applicable | Every claim of anonymous membership continuity | Anonymous membership continuity MUST mean possession of the same original `memberSecret`. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S29 | STATE |
| <a id="pe-g3-mem-003"></a> PE-G3-MEM-003 | MUST | applicable | Every replacement of an active `memberSecret` with a different secret | A different `memberSecret` MUST establish a different anonymous membership identity. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-mem-004"></a> PE-G3-MEM-004 | MUST NOT | applicable | Every wallet, backend, application, deployment, transport, and heuristic recovery mechanism | A mechanism other than possession of the same original `memberSecret` MUST NOT establish, reconstruct, or simulate anonymous membership continuity. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S29 | STATE |
| <a id="pe-g3-mem-005"></a> PE-G3-MEM-005 | MUST | applicable | Every membership leaf | A membership leaf MUST remain bounded to membership inclusion, path acquisition, and private proof-witness use according to the applicable protocol semantics. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-mem-006"></a> PE-G3-MEM-006 | MUST | applicable | Every membership enrollment or activation | Enrollment or activation MUST attach membership only to the privately controlled membership material presented for that enrollment without importing funding provenance into membership identity. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-mem-007"></a> PE-G3-MEM-007 | MUST NOT | applicable | Every enrollment right, admission object, funding wallet, sponsor relationship, and accounting state | An enrollment or admission artifact MUST NOT be represented as anonymous membership identity or Private Actor identity. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S29 | STATE |
| <a id="pe-g3-mem-008"></a> PE-G3-MEM-008 | MUST NOT | applicable | Every public enrollment, membership-status, readiness, and application surface | A public surface MUST NOT expose a reusable mapping from enrollment or admission provenance to anonymous membership or public action occurrence. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S29 | STATE |

<a id="pe-g3-rf-19"></a>
### RF-19 — Nullifier-based uniqueness and action-bounded unlinkability

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-uniq-001"></a> PE-G3-UNIQ-001 | MUST | applicable | Every anonymous action type requiring one action per member per action context | Uniqueness MUST be enforced within the declared `(actionId, member)` scope. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-uniq-002"></a> PE-G3-UNIQ-002 | MUST | applicable | Every nullifier in the current published protocol generation | A nullifier MUST be derived as `Poseidon3(memberSecret, actionId, SIGN_DOMAIN)`. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-uniq-003"></a> PE-G3-UNIQ-003 | MUST | applicable | Every action-layer duplicate-prevention decision in the current published protocol generation | Nullifier status MUST remain the sole action-layer duplicate-prevention primitive. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-uniq-004"></a> PE-G3-UNIQ-004 | MUST NOT | applicable | Every public nullifier and nullifier-status record | A nullifier or its status MUST NOT be represented as Private Actor identity or reusable participant identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-uniq-005"></a> PE-G3-UNIQ-005 | MUST NOT | applicable | Every nullifier outside its declared action context | A nullifier MUST NOT be reused as a cross-action join key, participant tag, continuity handle, or global identity mechanism. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-uniq-006"></a> PE-G3-UNIQ-006 | MUST NOT | applicable | Every wallet identifier, membership leaf, enrollment identifier, admission object, and application account | A wallet, leaf, enrollment, admission, or application identifier MUST NOT replace the nullifier as the action-layer uniqueness key. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-uniq-007"></a> PE-G3-UNIQ-007 | MUST NOT | applicable | Every duplicate-status response, log, diagnostic, event, and read model | Duplicate-status observability MUST NOT disclose or enable inference of the Private Actor beyond the bounded action-local uniqueness fact. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-uniq-008"></a> PE-G3-UNIQ-008 | MUST NOT | applicable | Every interpretation of nullifier-enforced uniqueness | Scoped nullifier uniqueness MUST NOT be represented as one-person, one-human, one-wallet, or globally reusable participant uniqueness. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S21, PE-G3-SOURCE-S22, PE-G3-SOURCE-S24 | STATE |

<a id="pe-g3-sf-05"></a>
## SF-05 — Interface Contracts, Protocol Surfaces, Operations, and Results

<a id="pe-g3-rf-12"></a>
### RF-12 — Interface contracts and concrete interface specifications

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-iface-001"></a> PE-G3-IFACE-001 | MUST | applicable | Every Privacy Engine Interface Contract | An Interface Contract MUST possess one stable identity, one bounded semantic role, and one version sufficient to distinguish its published meaning. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S20, PE-G3-SOURCE-S22, PE-G3-SOURCE-S31 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-iface-002"></a> PE-G3-IFACE-002 | MUST | applicable | Every Privacy Engine Interface Contract | An Interface Contract MUST derive from exactly one identified published Privacy Engine protocol generation. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S17, PE-G3-SOURCE-S31 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-iface-003"></a> PE-G3-IFACE-003 | MUST | applicable | Every Privacy Engine Interface Contract | An Interface Contract MUST define its bounded input semantics, output semantics, Protocol Operations, externally relied-upon behavior, and applicable observable failure semantics. | PE-G3-SOURCE-S22, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-iface-004"></a> PE-G3-IFACE-004 | MUST | applicable | Every Interface Contract and every concrete realization of it | Interface meaning and concrete representation MUST remain distinct semantic and syntactic roles. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S20, PE-G3-SOURCE-S30, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-iface-005"></a> PE-G3-IFACE-005 | MUST | applicable | Every Concrete Interface Specification | A Concrete Interface Specification MUST possess one stable specification identity, one specification version, and one bounded integration surface. | PE-G3-SOURCE-S30 | NONE |
| <a id="pe-g3-iface-006"></a> PE-G3-IFACE-006 | MUST | applicable | Every Concrete Interface Specification | A Concrete Interface Specification MUST identify and realize exactly one governing Interface Contract. | PE-G3-SOURCE-S30, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-iface-007"></a> PE-G3-IFACE-007 | MUST | applicable | Every Concrete Interface Specification | A Concrete Interface Specification MUST completely define the operation names, invocation forms, field ordering, type constraints, encoding rules, result representations, and externally observable error representations required by its bounded surface. | PE-G3-SOURCE-S30 | NONE |
| <a id="pe-g3-iface-008"></a> PE-G3-IFACE-008 | MUST | applicable | Every Concrete Interface Specification and its governing Interface Contract | The concrete representation MUST preserve semantic equivalence with the governing Interface Contract. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S30, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-iface-009"></a> PE-G3-IFACE-009 | MAY | applicable | Every Interface Contract permitting multiple concrete realizations | Multiple Concrete Interface Specifications MAY realize the same Interface Contract when each realization independently preserves the complete bounded interface meaning. | PE-G3-SOURCE-S30 | NONE |
| <a id="pe-g3-iface-010"></a> PE-G3-IFACE-010 | MUST | applicable | Every representation-only interface change | A representation-only change MUST preserve the identity, semantics, ordering requirements, compatibility boundary, and observable guarantees of the governing Interface Contract. | PE-G3-SOURCE-S22, PE-G3-SOURCE-S30, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-iface-011"></a> PE-G3-IFACE-011 | MUST | applicable | Every change to published Interface Contract meaning | A change to published interface semantics, obligations, validity, or observable guarantees MUST be represented through the applicable distinct-generation and versioning rules. | PE-G3-SOURCE-S15, PE-G3-SOURCE-S22, PE-G3-SOURCE-S30, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-iface-012"></a> PE-G3-IFACE-012 | MUST NOT | applicable | Every Interface Contract and Concrete Interface Specification | Implementation algorithms, storage layouts, deployment topology, transport machinery, operational policy, and application-defined meaning MUST NOT become interface semantics unless the published protocol generation expressly defines them as such. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S22, PE-G3-SOURCE-S29, PE-G3-SOURCE-S30, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-iface-013"></a> PE-G3-IFACE-013 | MUST NOT | applicable | Every Interface Contract and Concrete Interface Specification | An Interface Contract or Concrete Interface Specification MUST NOT independently acquire, transfer, replace, or modify protocol authority. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S30, PE-G3-SOURCE-S31 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-iface-014"></a> PE-G3-IFACE-014 | MUST | applicable | Every public Interface Contract and Concrete Interface Specification | Every public interface realization MUST preserve the applicable SF-03 and SF-04 identity, privacy, unlinkability, minimum-disclosure, and neutral-naming requirements. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S22, PE-G3-SOURCE-S29, PE-G3-SOURCE-S30, PE-G3-SOURCE-S31 | STATE |
| <a id="pe-g3-tseiface-001"></a> PE-G3-TSEIFACE-001 | MAY | applicable | ALWAYS | A concrete interface MAY represent protocol-owned authorization and result fields only with the exact published syntax and semantics. | PE-G3-SOURCE-S30 | NONE |
| <a id="pe-g3-tseiface-002"></a> PE-G3-TSEIFACE-002 | MUST NOT | applicable | ALWAYS | An interface, adapter or implementation MUST NOT define a predicate, infer a missing coordinate, select recovery or substitute an implementation value for authoritative protocol state. | PE-G3-SOURCE-S30, PE-G3-SOURCE-S43 | NONE |
| <a id="pe-g3-tseiface-003"></a> PE-G3-TSEIFACE-003 | MUST NOT | applicable | ALWAYS | A public interface MUST NOT carry a confidential opening unless that interface is the authenticated confidential comparison boundary defined by the profile. | PE-G3-SOURCE-S30 | NONE |

<a id="pe-g3-rf-13"></a>
### RF-13 — Protocol surfaces, operations, and Published Results

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-surf-001"></a> PE-G3-SURF-001 | MUST | applicable | Every Privacy Engine Protocol Surface | A Protocol Surface MUST possess one stable identity and one bounded externally relied-upon capability scope within one published protocol generation. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S22 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-surf-002"></a> PE-G3-SURF-002 | MUST | applicable | Every Protocol Surface | A Protocol Surface MUST expose only the protocol capabilities, semantic guarantees, compatibility boundaries, and observable behavior defined for that surface. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S22, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-surf-003"></a> PE-G3-SURF-003 | MUST | applicable | Every implementation realizing a Protocol Surface | Internal implementation machinery MUST remain replaceable when the complete published semantics and guarantees of the Protocol Surface remain preserved. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S22, PE-G3-SOURCE-S23, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-surf-004"></a> PE-G3-SURF-004 | MUST NOT | applicable | Every implementation detail behind a Protocol Surface | Code structure, storage layout, deployment topology, relay selection, transport, persistence, monitoring, optimization, or helper naming MUST NOT become protocol-surface semantics merely because a current implementation uses it. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S20, PE-G3-SOURCE-S22, PE-G3-SOURCE-S23, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-surf-005"></a> PE-G3-SURF-005 | MUST | applicable | Every Privacy Engine Protocol Operation | A Protocol Operation MUST possess one stable capability identity defined by one published Interface Contract within one identified protocol generation. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S23, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-surf-006"></a> PE-G3-SURF-006 | MUST | applicable | Every Protocol Operation | A Protocol Operation MUST define one bounded protocol-owned capability, including its applicable input meaning, output meaning, and externally relied-upon behavior. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S23, PE-G3-SOURCE-S31 | NONE |
| <a id="pe-g3-surf-007"></a> PE-G3-SURF-007 | MUST | applicable | Every Protocol Operation and associated Protocol Action | The exposed Protocol Operation and associated Protocol Action representation MUST preserve the RF-07 distinction between the Protocol Operation capability type and each Protocol Action occurrence classified by that capability. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S23, PE-G3-SOURCE-S24 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-surf-008"></a> PE-G3-SURF-008 | MUST | applicable | Every offered Protocol Operation | The governing Interface Contract MUST declare the operation's applicability conditions and the semantic roles of every required input and Published Result. | PE-G3-SOURCE-S23, PE-G3-SOURCE-S31, PE-G3-SOURCE-S32 | NONE |
| <a id="pe-g3-surf-009"></a> PE-G3-SURF-009 | MUST | applicable | Every implementation realizing a Protocol Operation | An implementation MUST preserve the operation's published capability across execution and implementation variation. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S23 | NONE |
| <a id="pe-g3-surf-018"></a> PE-G3-SURF-018 | MUST NOT | applicable | Every execution or implementation variation realizing a Protocol Operation | Execution or implementation variation MUST NOT redefine the Protocol Operation's published capability. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S23 | NONE |
| <a id="pe-g3-surf-010"></a> PE-G3-SURF-010 | MUST | applicable | Every Published Result | A Published Result MUST possess one bounded result identity and MUST identify the governing Interface Contract and Protocol Operation from which its meaning derives. | PE-G3-SOURCE-S31, PE-G3-SOURCE-S32 | NONE |
| <a id="pe-g3-surf-011"></a> PE-G3-SURF-011 | MUST | applicable | Every Published Result | A Published Result MUST express only the interface-level success semantics, failure semantics, guarantees, and observable meaning defined by its governing Interface Contract. | PE-G3-SOURCE-S31, PE-G3-SOURCE-S32 | NONE |
| <a id="pe-g3-surf-012"></a> PE-G3-SURF-012 | MUST | applicable | Every Published Result and concrete representation of it | Published Result meaning and its serialized, transported, stored, displayed, or application-facing representation MUST remain distinct. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S30, PE-G3-SOURCE-S32 | NONE |
| <a id="pe-g3-surf-013"></a> PE-G3-SURF-013 | MUST | applicable | Every concrete realization or translation of a Published Result | Every concrete realization or permitted downstream translation MUST preserve the complete bounded meaning of the same Published Result. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S30, PE-G3-SOURCE-S32 | NONE |
| <a id="pe-g3-surf-014"></a> PE-G3-SURF-014 | MUST NOT | applicable | Every Published Result | A Published Result MUST NOT be represented as a Protocol Action Evaluation, Protocol Action Determination, acceptance object, rejection object, or separate Evaluation Outcome object. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S32 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-surf-015"></a> PE-G3-SURF-015 | MUST NOT | applicable | Every Published Result | A Published Result MUST NOT be represented as a committed Protocol State Transition or as an independently authoritative public protocol-state consequence. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S32 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-surf-016"></a> PE-G3-SURF-016 | MUST NOT | applicable | Every application interpretation or representation of a Protocol Surface, Protocol Operation, or Published Result | Application-defined meaning, terminology, formatting, workflow, or response structure MUST NOT redefine protocol capability, validity, or Published Result meaning. | PE-G3-SOURCE-S09, PE-G3-SOURCE-S24, PE-G3-SOURCE-S29, PE-G3-SOURCE-S32 | NONE |
| <a id="pe-g3-surf-017"></a> PE-G3-SURF-017 | MUST | applicable | Every public Protocol Surface, Protocol Operation representation, and Published Result | The complete exposed composition MUST preserve the applicable SF-03 and SF-04 identity, privacy, unlinkability, minimum-disclosure, and forbidden-correlation requirements. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S22, PE-G3-SOURCE-S24, PE-G3-SOURCE-S32 | STATE |
| <a id="pe-g3-surf-019"></a> PE-G3-SURF-019 | MUST | applicable | Every Determination and every later representation or realization of it | Protocol-semantic Determination production MUST remain distinct from representation, serialization, persistence, publication, transport, operational delivery, display, indexing, events, logs, responses and application interpretation. | PE-G3-SOURCE-S25, PE-G3-SOURCE-S30, PE-G3-SOURCE-S32, PE-G3-SOURCE-S42, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-tseresult-001"></a> PE-G3-TSERESULT-001 | MUST | applicable | ALWAYS | Every completed comparison attempt MUST produce exactly one of equivalent, material-conflict or indeterminate. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseresult-002"></a> PE-G3-TSERESULT-002 | MUST | applicable | ALWAYS | A represented comparison result MUST preserve its exact authoritative classification and U binding without expanding its evidentiary claim. | PE-G3-SOURCE-S32 | NONE |
| <a id="pe-g3-tseresult-003-a01"></a> PE-G3-TSERESULT-003-A01 | MUST | applicable | ALWAYS | A commitment digest MUST establish only computational binding of its encoded preimage under the identified algorithm. | PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tseresult-003-a02"></a> PE-G3-TSERESULT-003-A02 | MUST NOT | applicable | ALWAYS | A commitment digest MUST NOT prove any unencoded semantic or identity claim. | PE-G3-SOURCE-S71 | NONE |

<a id="pe-g3-sf-06"></a>
## SF-06 — Proofs, Public Inputs, Verification, Evidence, and Validity

<a id="pe-g3-rf-16"></a>
### RF-16 — Proofs and declared public inputs

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-proof-001"></a> PE-G3-PROOF-001 | MUST | applicable | Every proof required by a Privacy Engine Protocol Action | A proof MUST possess one bounded evidence identity distinct from its encoding, public inputs, private witness, supported Protocol Action, and Private Actor. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-proof-002"></a> PE-G3-PROOF-002 | MUST | applicable | Every proof type in a published protocol generation | The published protocol generation MUST declare the proof relation, proof-system requirements, public-input schema, private-witness boundary, and verification semantics applicable to the proof type. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S22, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-proof-003"></a> PE-G3-PROOF-003 | MUST | applicable | Every current-generation anonymous-action proof | The proof relation MUST establish knowledge of the applicable membership secret and membership witness, inclusion under the declared membership root, and correct nullifier derivation for the declared action context without disclosing the Private Actor. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-proof-004"></a> PE-G3-PROOF-004 | MUST | applicable | Every proof relation and proof-construction boundary | Public inputs and private witness material MUST remain explicitly separated according to the applicable published proof relation. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20 | STATE |
| <a id="pe-g3-proof-005"></a> PE-G3-PROOF-005 | MUST | applicable | Every current-generation anonymous-action public-input set | The declared public inputs MUST occur in the exact ordered sequence `nullifier`, `petitionId` or `actionId`, `membershipRoot`. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S22, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-proof-006"></a> PE-G3-PROOF-006 | MUST | applicable | Every current-generation declared public-input interpretation | `nullifier` MUST remain bounded to action-context uniqueness, `petitionId` or `actionId` MUST remain bounded to action context, and `membershipRoot` MUST remain bounded to the applicable membership-state commitment. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-proof-007"></a> PE-G3-PROOF-007 | MUST | applicable | Every proof and declared public-input set presented together | The proof representation, public-input values, ordering, action context, and proof relation MUST form one coherent verification input. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-proof-008"></a> PE-G3-PROOF-008 | MUST | applicable | Every proof-construction process | Proof construction MUST keep `memberSecret`, Merkle path, membership leaf, and other private witness material outside public inputs and public protocol surfaces. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20 | STATE |
| <a id="pe-g3-proof-009"></a> PE-G3-PROOF-009 | MUST | applicable | Every proof realization for the current published generation | The proof realization MUST use the published generation's declared Circom and Groth16-over-BN254 proof semantics and compatible verifier artifacts. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-proof-010"></a> PE-G3-PROOF-010 | MUST | applicable | Every published proof artifact set | Proof artifacts, verification keys, verifier artifacts, public-input ordering, and associated provenance MUST satisfy the published artifact-integrity and reproducibility requirements. | PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-proof-011"></a> PE-G3-PROOF-011 | MUST | applicable | Every permitted proof or public-input representation | A representation MUST preserve the complete proof relation, proof-system semantics, verifier compatibility, input meaning, and input ordering of the identified published generation. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S22, PE-G3-SOURCE-S30 | STATE |
| <a id="pe-g3-proof-012"></a> PE-G3-PROOF-012 | MUST | applicable | Every change to a proof system, proof relation, public-input schema, public-input ordering, verifier encoding, or artifact-integrity rule | The change MUST follow the applicable distinct-generation, versioning, publication, and artifact-regeneration requirements. | PE-G3-SOURCE-S15, PE-G3-SOURCE-S22 | STATE |
| <a id="pe-g3-proof-013"></a> PE-G3-PROOF-013 | MUST NOT | applicable | Every proof and proof representation | A proof or its representation MUST NOT be treated as the Protocol Action occurrence, Private Actor identity, wallet identity, membership identity, application truth, or reusable participant identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-proof-014"></a> PE-G3-PROOF-014 | MUST NOT | applicable | Every declared public input and public-input composition | A public input or public-input composition MUST NOT exceed its declared role or become a reusable participant identifier, cross-action join key, actor-reconstruction value, or application-only correlation field. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S24 | STATE |

<a id="pe-g3-rf-17"></a>
### RF-17 — Proof verification

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-verify-001"></a> PE-G3-VERIFY-001 | MUST | applicable | Every required proof verification | Proof verification MUST occur as one bounded verification occurrence whose proof, public inputs, proof relation, verifier artifacts, and result are distinguishable. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-verify-002"></a> PE-G3-VERIFY-002 | MUST | applicable | Every proof-verification occurrence | Verification MUST evaluate exactly the presented proof and declared public-input set against the applicable published proof relation and verifier artifacts. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S20, PE-G3-SOURCE-S25 | STATE |
| <a id="pe-g3-verify-003"></a> PE-G3-VERIFY-003 | MUST | applicable | Every correct proof-verification realization | Verification MUST be deterministic for the same proof, public inputs, proof relation, verifier artifacts, and protocol-relevant verification context. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-verify-004"></a> PE-G3-VERIFY-004 | MUST | applicable | Every completed proof-verification occurrence | A completed verification MUST produce exactly one bounded proof-valid or proof-invalid classification. | PE-G3-SOURCE-S19, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-verify-005"></a> PE-G3-VERIFY-005 | MUST | applicable | Every proof-valid classification | A proof-valid classification MUST establish only that the proof and declared public inputs satisfy the applicable published proof relation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-verify-006"></a> PE-G3-VERIFY-006 | MUST | applicable | Every proof-invalid classification required for a Protocol Action | A required proof-invalid classification MUST prevent that proof from satisfying the corresponding applicable proof-verification requirement. | PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-verify-007"></a> PE-G3-VERIFY-007 | MUST | applicable | Every inability to complete required proof verification | Verification failure MUST remain distinguishable from a completed proof-valid classification, completed proof-invalid classification, Protocol Action rejection, and later failure classifications. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-verify-008"></a> PE-G3-VERIFY-008 | MUST | applicable | Every proof-valid verification result used in Protocol Action Evaluation | The result MUST contribute only the bounded evidence established by the applicable proof relation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-verify-009"></a> PE-G3-VERIFY-009 | MUST NOT | applicable | Every proof-valid verification result | Successful proof verification MUST NOT independently establish complete Protocol Action validity, acceptance, rejection, transition authorization, transition execution, or commitment. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-verify-010"></a> PE-G3-VERIFY-010 | MUST NOT | applicable | Every proof-verification occurrence and result | Proof verification MUST NOT establish Private Actor identity, wallet identity, enrollment provenance, admission provenance, application truth, legal truth, factual truth, or reusable participant identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-verify-011"></a> PE-G3-VERIFY-011 | MUST NOT | applicable | Every proof-verification implementation | Verifier code structure, deployment address, transaction identity, runtime mechanism, storage, transport, or diagnostic behavior MUST NOT redefine the applicable proof relation or verification semantics. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S25 | STATE |
| <a id="pe-g3-verify-012"></a> PE-G3-VERIFY-012 | MUST NOT | applicable | Every proof-verification component and result | A proof-verification component or result MUST NOT independently acquire or modify protocol authority. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |

<a id="pe-g3-rf-18"></a>
### RF-18 — Evidence, protocol validity, and non-proof validity conditions

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-valid-001"></a> PE-G3-VALID-001 | MUST | applicable | Every proof-verification result used during Protocol Action Evaluation | The result MUST remain bounded evidence concerning exactly the proof relation and public-input relationship evaluated by that verification occurrence. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-valid-002"></a> PE-G3-VALID-002 | MUST | applicable | Every proof-verification result contributing to complete Evaluation | The result MUST contribute to the later Protocol Action Evaluation without replacing the Action, applicable rule set, Evaluation, or Determination. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-valid-003"></a> PE-G3-VALID-003 | MUST | applicable | Every Protocol Action validity determination basis | Complete Protocol Action validity MUST mean satisfaction of every applicable protocol rule within one bounded evaluation context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-valid-004"></a> PE-G3-VALID-004 | MUST NOT | applicable | Every successful proof-verification result | Successful proof verification MUST NOT be represented as complete Protocol Action validity unless proof verification constitutes the complete applicable protocol-rule set for that action and context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-valid-005"></a> PE-G3-VALID-005 | MUST | applicable | Every Protocol Action whose applicable rule set includes non-proof validity conditions | Every applicable non-proof validity condition MUST remain represented and evaluated as part of the complete applicable protocol-rule set. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-valid-006"></a> PE-G3-VALID-006 | MUST | applicable | Every non-proof protocol-validity condition | A non-proof validity condition MUST derive from the identified published protocol generation and MUST possess a bounded applicability rule for the affected action and context. | PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-valid-007"></a> PE-G3-VALID-007 | MUST | applicable | Every current-generation Protocol Action Evaluation basis | The applicable validity basis MUST account for required action shape, public-input coherence, accepted-root status, nullifier uniqueness, replay prevention, domain separation, protocol-state requirements, and every other applicable generation-derived condition. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | STATE |
| <a id="pe-g3-valid-008"></a> PE-G3-VALID-008 | MUST | applicable | Every required proof-invalid verification result | A required proof-invalid result MUST prevent the Protocol Action from satisfying the corresponding applicable proof requirement. | PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-valid-009"></a> PE-G3-VALID-009 | MUST | applicable | Every interpretation of protocol validity | Protocol validity MUST remain action-specific, applicable-rule-relative, and bounded to the identified evaluation context. | PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-valid-010"></a> PE-G3-VALID-010 | MUST NOT | applicable | Every proof-valid or protocol-valid classification | Proof validity or protocol validity MUST NOT independently become Protocol Action acceptance, rejection, transition authorization, transition execution, or commitment. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-valid-011"></a> PE-G3-VALID-011 | MUST NOT | applicable | Every protocol-valid Protocol Action and interpretation of it | Protocol validity MUST NOT be represented as application truth, external factual truth, legal truth, social truth, institutional recognition, or a Protocol Claim. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25, PE-G3-SOURCE-S28 | NONE |
| <a id="pe-g3-valid-012"></a> PE-G3-VALID-012 | MUST | applicable | Every evidence, validity, failure, and diagnostic surface | The surface MUST preserve SF-03 and SF-04 identity separation, Private Actor non-disclosure, role-bounded public values, neutral naming, and compositional unlinkability. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | STATE |

<a id="pe-g3-sf-07"></a>
## SF-07 — Protocol Actions and Applicable Rules

<a id="pe-g3-rf-20"></a>
### RF-20 — Protocol Actions

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-action-001"></a> PE-G3-ACTION-001 | MUST | applicable | Every Privacy Engine Protocol Action | A Protocol Action MUST be one bounded occurrence of protocol-defined behavior presented through an implementation for Evaluation under the applicable rules of one identified published protocol generation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-action-002"></a> PE-G3-ACTION-002 | MUST | applicable | Every Protocol Action occurrence | Each Protocol Action MUST possess one stable occurrence identity distinct from every other Protocol Action occurrence. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-action-003"></a> PE-G3-ACTION-003 | MUST | applicable | Every Protocol Action | The Action MUST be bounded to one occurrence, one action type, one declared public-input set, one applicable protocol-rule set, and one bounded evaluation context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-action-004"></a> PE-G3-ACTION-004 | MUST | applicable | Every Protocol Action occurrence | The occurrence MUST identify its protocol-defined action type and governing published protocol generation. | PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-action-005"></a> PE-G3-ACTION-005 | MUST | applicable | Every Protocol Operation, action type, and Protocol Action occurrence | Published capability, action-type classification, and individual action occurrence MUST remain distinct. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S23, PE-G3-SOURCE-S24 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-action-006"></a> PE-G3-ACTION-006 | MUST | applicable | Every effort to construct, present, submit, or obtain evaluation of a candidate Protocol Action | An action attempt MUST remain distinct from a Protocol Action occurrence admitted to the authoritative evaluation boundary. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-action-007"></a> PE-G3-ACTION-007 | MUST | applicable | Every candidate admitted to authoritative Protocol Action Evaluation | Admission to the applicable authoritative evaluation boundary MUST instantiate one bounded Protocol Action occurrence without identifying its Private Actor. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-action-008"></a> PE-G3-ACTION-008 | MUST NOT | applicable | Every transport retry, relay attempt, submission retry, implementation retry, and internal processing attempt | An operational retry or attempt MUST NOT silently widen, replace, merge, or create the identity of the logical Protocol Action occurrence. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-action-009"></a> PE-G3-ACTION-009 | MUST | applicable | Every protocol rule governing repeated authoritative presentations | The rule MUST determine whether the presentations concern one action occurrence or distinct action occurrences without inferring or merging Private Actor identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-action-010"></a> PE-G3-ACTION-010 | MUST | applicable | Every Protocol Action | The Action MUST carry exactly the declared public-input set required for its action type while remaining distinct from those public inputs. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-action-011"></a> PE-G3-ACTION-011 | MUST | applicable | Every proof-supported Protocol Action | The Action and its supporting proof MUST remain distinct, and the proof MUST contribute only its bounded evidence role. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-action-012"></a> PE-G3-ACTION-012 | MUST | applicable | Every Protocol Action performed through an implementation | The Action occurrence MUST remain distinct from the implementation, deployment, transaction, transport, storage, and runtime machinery through which it is presented. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-action-013"></a> PE-G3-ACTION-013 | MUST | applicable | Every relationship between a Private Actor and Protocol Action | Protocol Action representation, processing, and Evaluation presentation MUST preserve the RF-09 Private Actor and public Protocol Action separation invariant throughout the Action lifecycle. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S19, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-action-014"></a> PE-G3-ACTION-014 | MUST NOT | applicable | Every Protocol Action identifier and representation | An action identifier or representation MUST NOT identify, encode, imply, reconstruct, or become a reusable identifier for the Private Actor. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-action-015"></a> PE-G3-ACTION-015 | MUST NOT | applicable | Every application interpretation of a Protocol Action | Application-defined meaning, terminology, workflow, metadata, or truth MUST NOT become Protocol Action identity or protocol validity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S28, PE-G3-SOURCE-S29 | NONE |
| <a id="pe-g3-action-016"></a> PE-G3-ACTION-016 | MUST | applicable | Every relationship from a Protocol Action to a possible Published Result, Determination, or Protocol State Transition | The Protocol Action MUST remain distinct from every interface result, downstream Determination, and possible state-transition consequence. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S27, PE-G3-SOURCE-S32 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-action-017"></a> PE-G3-ACTION-017 | MUST NOT | applicable | Every Protocol Action interpretation and extension | A Protocol Action MUST NOT be represented as a Protocol Claim or used to introduce another first-class subject without satisfying the established closed-ontology test. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S28 | NONE |

<a id="pe-g3-rf-21"></a>
### RF-21 — Applicable protocol-rule sets and action validity

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-rule-001"></a> PE-G3-RULE-001 | MUST | applicable | Every Protocol Action | The Action MUST be governed by exactly one complete and bounded applicable protocol-rule set for its identified action type and evaluation context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S33 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-rule-002"></a> PE-G3-RULE-002 | MUST | applicable | Every rule included in an applicable Protocol Action rule set | Each applicable rule MUST derive from the identified published protocol generation through the established Protocol Specification and implementation-profile direction. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S33 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-rule-003"></a> PE-G3-RULE-003 | MUST | applicable | Every determination of Protocol Action rule applicability | Applicability MUST be determined only from protocol-defined action type, applicable implementation profile, protocol-relevant state, and bounded evaluation-context conditions. | PE-G3-SOURCE-S24, PE-G3-SOURCE-S33 | NONE |
| <a id="pe-g3-rule-004"></a> PE-G3-RULE-004 | MUST | applicable | Every Protocol Action admitted for authoritative Evaluation | The complete applicable protocol-rule set MUST be established before authoritative Evaluation begins. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-rule-005"></a> PE-G3-RULE-005 | MUST NOT | applicable | Every implementation, application, transport, deployment, and operational policy | Implementation convenience, application policy, transport behavior, deployment state, or operational discretion MUST NOT silently create, remove, weaken, strengthen, or reinterpret a protocol-validity rule. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S33 | NONE |
| <a id="pe-g3-rule-006"></a> PE-G3-RULE-006 | MUST | applicable | Every Protocol Action validity classification basis | The validity-classification basis MUST apply the complete RF-18 definition of Protocol Action validity through the complete applicable protocol-rule set within the identified bounded evaluation context without replacing or redefining that definition. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-rule-007"></a> PE-G3-RULE-007 | MUST | applicable | Every applicable Protocol Action rule set | The rule set MUST include every applicable proof requirement, public-input requirement, non-proof validity condition, uniqueness condition, state-relative condition, and action-type constraint. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25, PE-G3-SOURCE-S33 | STATE |
| <a id="pe-g3-rule-008"></a> PE-G3-RULE-008 | MUST | applicable | Every protocol-validity interpretation | Protocol-rule interpretation and application MUST preserve the RF-18 action-specific, applicable-rule-relative, evaluation-context-bounded validity invariant without widening validity beyond the identified context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-rule-013"></a> PE-G3-RULE-013 | MUST NOT | applicable | Every comparison of Protocol Action validity across materially different evaluation contexts | Validity in one evaluation context MUST NOT be inferred as validity in a materially different evaluation context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-rule-009"></a> PE-G3-RULE-009 | MUST NOT | applicable | Every application interpretation and external claim associated with a Protocol Action | Application meaning, factual meaning, legal meaning, social meaning, or institutional meaning MUST NOT replace or redefine the applicable protocol-rule set or protocol validity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25, PE-G3-SOURCE-S28, PE-G3-SOURCE-S29 | NONE |
| <a id="pe-g3-rule-010"></a> PE-G3-RULE-010 | MUST | applicable | Every action-local uniqueness or authorization rule | The rule MUST preserve the declared action scope without creating reusable participant identity, actor disclosure, or unauthorized cross-action linkage. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S24 | STATE |
| <a id="pe-g3-rule-011"></a> PE-G3-RULE-011 | MUST NOT | applicable | Every implementation, transaction, transport, retry, storage, and diagnostic identifier | An operational identifier MUST NOT determine, replace, merge, or redefine Protocol Action identity, rule applicability, or protocol validity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S24 | NONE |
| <a id="pe-g3-rule-012"></a> PE-G3-RULE-012 | MUST | applicable | Every Protocol Action prepared for complete Evaluation | The Action, complete applicable rule set, and bounded evaluation context MUST be available as distinct preserved inputs to SF-08 without pre-emptively defining Evaluation, Determination, acceptance, or rejection. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |

<a id="pe-g3-sf-08"></a>
## SF-08 — Evaluation, Determination, Acceptance, and Rejection

<a id="pe-g3-rf-22"></a>
### RF-22 — Protocol Action Evaluation

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-eval-001"></a> PE-G3-EVAL-001 | MUST | applicable | Every Protocol Action Evaluation | A Protocol Action Evaluation MUST possess one stable occurrence identity identifying exactly one bounded Evaluation occurrence. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | STATE, PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-eval-002"></a> PE-G3-EVAL-002 | MUST | applicable | Every Protocol Action Evaluation | An Evaluation MUST evaluate exactly one identified Protocol Action. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-003"></a> PE-G3-EVAL-003 | MUST | applicable | Every Protocol Action Evaluation | An Evaluation MUST apply exactly one complete applicable protocol-rule set established for the evaluated Action. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25, PE-G3-SOURCE-S33 | NONE |
| <a id="pe-g3-eval-004"></a> PE-G3-EVAL-004 | MUST | applicable | Every Protocol Action Evaluation | An Evaluation MUST occur within exactly one bounded protocol-relevant evaluation context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-005"></a> PE-G3-EVAL-005 | MUST | applicable | Every candidate entering the authoritative Evaluation boundary | Authoritative Evaluation MUST begin only after the Action, complete applicable rule set, and bounded evaluation context have been established as distinct inputs. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-006"></a> PE-G3-EVAL-006 | MUST | applicable | Every Protocol Action Evaluation after Evaluation begins | The Evaluation MUST preserve its identified Action, complete applicable rule set, and bounded evaluation context throughout the Evaluation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-007"></a> PE-G3-EVAL-007 | MUST NOT | applicable | Every Protocol Action Evaluation after Evaluation begins | An Evaluation MUST NOT substitute, merge, widen, narrow, repair, or infer a replacement Action, rule set, or evaluation context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-008"></a> PE-G3-EVAL-008 | MUST | applicable | Every complete Protocol Action Evaluation | A complete Evaluation MUST evaluate every applicable protocol rule governing the identified Action in the identified context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-009"></a> PE-G3-EVAL-009 | MUST | applicable | Every Evaluation component | An Evaluation component MUST possess an explicit assignment to one applicable requirement or one bounded subset of the complete applicable rule set. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S33 | NONE |
| <a id="pe-g3-eval-010"></a> PE-G3-EVAL-010 | MUST | applicable | Every Evaluation component | An Evaluation component MUST evaluate only the applicable requirement or bounded subset assigned to that component. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S33 | NONE |
| <a id="pe-g3-eval-011"></a> PE-G3-EVAL-011 | MUST NOT | applicable | Every Evaluation component whose assigned rules are not the complete applicable rule set | A bounded component MUST NOT be represented as complete Protocol Action Evaluation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S33 | NONE |
| <a id="pe-g3-eval-012"></a> PE-G3-EVAL-012 | MUST | applicable | Every Evaluation containing multiple required components | The Evaluation MUST coherently combine every required component result before determining whether the Evaluation is complete. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-013"></a> PE-G3-EVAL-013 | MUST | applicable | Every proof-verification occurrence contributing to Evaluation | Proof verification MUST remain bounded evidence concerning the declared proof relation and declared public inputs. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-014"></a> PE-G3-EVAL-014 | MUST | applicable | Every relationship between proof verification and Protocol Action Evaluation | Proof verification MUST remain distinct from the complete Evaluation to which it contributes. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-eval-015"></a> PE-G3-EVAL-015 | MUST NOT | applicable | Every proof-verification result | A proof-verification result MUST NOT directly produce a Protocol Action Determination, acceptance classification, or rejection classification. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-eval-016"></a> PE-G3-EVAL-016 | MUST | applicable | Every Evaluation whose applicable rule set contains non-proof validity conditions | The Evaluation MUST evaluate every applicable non-proof validity condition independently of proof-verification success. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-017"></a> PE-G3-EVAL-017 | MUST | applicable | Every Protocol Action Evaluation completeness classification | An Evaluation MUST be classified as complete exactly when it has evaluated every applicable rule for the identified Action within the identified context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-018"></a> PE-G3-EVAL-018 | MUST NOT | applicable | Every partial or incomplete Protocol Action Evaluation | A partial or incomplete Evaluation MUST NOT produce a Determination, acceptance classification, or rejection classification. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-019"></a> PE-G3-EVAL-019 | MUST NOT | applicable | Every Evaluation failure and every pre-evaluation failure | Evaluation failure or pre-evaluation failure MUST NOT be represented as a completed Evaluation or as producing a Protocol Action Determination. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-eval-020"></a> PE-G3-EVAL-020 | MUST NOT | applicable | Every Evaluation component, identifier, evidence record, representation, diagnostic, log, field, route, test, example, and observability surface | An Evaluation surface MUST NOT identify the Private Actor, extend evidence into actor identification, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S25 | STATE |
| <a id="pe-g3-eval-021"></a> PE-G3-EVAL-021 | MUST | applicable | Every completed Protocol Action Evaluation | Every completed Protocol Action Evaluation MUST produce exactly one Protocol Action Determination as part of the same protocol-semantic completion transition. | PE-G3-SOURCE-S25 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-eval-022"></a> PE-G3-EVAL-022 | MUST NOT | applicable | Every implementation representation of Evaluation completion and Determination production | An implementation MUST NOT represent Evaluation completion and required Determination production as two protocol-semantic transitions separated by a valid completed-Evaluation state. | PE-G3-SOURCE-S25 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-eval-023"></a> PE-G3-EVAL-023 | MUST | applicable | Every Protocol Action Evaluation completion classification | A Protocol Action Evaluation MUST be in a valid completed state exactly when every applicable completion requirement is satisfied and exactly one corresponding Protocol Action Determination has been produced. | PE-G3-SOURCE-S25 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-eval-024"></a> PE-G3-EVAL-024 | MAY | applicable | Every active incomplete Protocol Action Evaluation | An active Protocol Action Evaluation MAY contain bounded internal steps, completed components and intermediate component state while remaining incomplete. | PE-G3-SOURCE-S25 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-eval-025"></a> PE-G3-EVAL-025 | MUST NOT | applicable | Every internal Evaluation step, component result, intermediate state and readiness condition | An internal step, component result, combined intermediate state or completion-readiness condition MUST NOT be represented as completed Evaluation or as a Protocol Action Determination. | PE-G3-SOURCE-S25 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-eval-026"></a> PE-G3-EVAL-026 | MUST | applicable | Every begun Evaluation unable to establish one valid Determination at its completion boundary | If an Evaluation that has begun cannot establish exactly one valid Determination at the same protocol-semantic boundary as Evaluation completion, the Evaluation MUST terminate as Evaluation failure, MUST remain incomplete, and MUST produce no Determination, acceptance or rejection. | PE-G3-SOURCE-S25 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-tsereeval-001-a01"></a> PE-G3-TSEREEVAL-001-A01 | MUST | applicable | ALWAYS | A new Evaluation MUST create a new E identity. | PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-tsereeval-001-a02"></a> PE-G3-TSEREEVAL-001-A02 | MUST | applicable | ALWAYS | A new Evaluation MUST preserve every earlier E and D without mutation. | PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-tsereeval-002"></a> PE-G3-TSEREEVAL-002 | MUST | applicable | ALWAYS | A new Evaluation MUST produce a new D only if it completes successfully at the Evaluation-completion boundary. | PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-tsereeval-003"></a> PE-G3-TSEREEVAL-003 | MUST | applicable | ALWAYS | Failure before successful completion of a new Evaluation MUST produce no new D, acceptance, authorization or U. | PE-G3-SOURCE-S25 | NONE |

<a id="pe-g3-rf-23"></a>
### RF-23 — Protocol Action Determination

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-determ-001"></a> PE-G3-DETERM-001 | MUST | applicable | Every Protocol Action Determination | A Protocol Action Determination MUST possess one stable result identity identifying exactly one bounded Determination. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | STATE, PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-determ-002"></a> PE-G3-DETERM-002 | MUST | applicable | Every relationship between a Protocol Action Evaluation and its Determination | The Evaluation process and resulting Determination MUST remain separately identified and semantically distinct. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-determ-003"></a> PE-G3-DETERM-003 | MUST | applicable | Every completed Protocol Action Evaluation | A completed Evaluation MUST produce exactly one Protocol Action Determination. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-determ-004"></a> PE-G3-DETERM-004 | MUST | applicable | Every Protocol Action Determination | A Determination MUST derive from exactly one completed Protocol Action Evaluation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-determ-005"></a> PE-G3-DETERM-005 | MUST | applicable | Every Protocol Action Determination | A Determination MUST identify exactly one producing completed Evaluation, one evaluated Action, one complete applicable rule set, and one bounded evaluation context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-determ-006"></a> PE-G3-DETERM-006 | MUST | applicable | Every valid Protocol Action Determination | A valid Determination MUST contain and reference its RF-24 classification without defining an alternative classification model. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-determ-007"></a> PE-G3-DETERM-007 | MUST NOT | applicable | Every incomplete or failed Protocol Action Evaluation | An incomplete or failed Evaluation MUST NOT be treated as possessing or producing a Protocol Action Determination. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-determ-008"></a> PE-G3-DETERM-008 | MUST | applicable | Every Protocol Action Determination and proof-verification result | A Determination MUST remain distinct from every proof-verification occurrence and proof-verification result contributing to its Evaluation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-determ-009"></a> PE-G3-DETERM-009 | MUST | applicable | Every Protocol Action Determination and Published Result | A Determination MUST remain distinct from every interface-level Published Result and its concrete representation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S32 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-determ-010"></a> PE-G3-DETERM-010 | MUST | applicable | Every Protocol Action Determination and possible Protocol State Transition | A Determination MUST remain distinct from transition identity, transition execution, commitment, and every committed public protocol-state consequence. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-determ-011"></a> PE-G3-DETERM-011 | MUST NOT | applicable | Every Determination identifier, representation, diagnostic, log, field, route, test, example, and observability surface | A Determination surface MUST NOT identify the Private Actor, become reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S25 | STATE |
| <a id="pe-g3-determ-012"></a> PE-G3-DETERM-012 | MUST | applicable | Every pair of correct Evaluations of the same Action under the same applicable rules and equivalent contexts | The Evaluations MUST produce equivalent acceptance or rejection Determinations. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-determ-013"></a> PE-G3-DETERM-013 | MUST | applicable | Every context-dependent Protocol Action Determination | The Determination MUST remain bounded to its identified evaluation context without converting material context differences into implementation discretion. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-determ-014"></a> PE-G3-DETERM-014 | MUST NOT | applicable | Every Protocol Action Determination | A Determination MUST NOT be represented as an Evaluation Outcome object or as an independently authoritative source of protocol semantics. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-determ-015"></a> PE-G3-DETERM-015 | MUST NOT | applicable | Every protocol state representing Evaluation completion | A protocol state MUST NOT contain a completed Protocol Action Evaluation without exactly one corresponding Protocol Action Determination. | PE-G3-SOURCE-S25 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-determ-016"></a> PE-G3-DETERM-016 | MUST | applicable | Every Evaluation and Determination identity boundary | Atomic establishment of Evaluation completion and Determination production MUST preserve the distinct identities and meanings of the Evaluation process and Determination result. | PE-G3-SOURCE-S25 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |

<a id="pe-g3-rf-24"></a>
### RF-24 — Acceptance and rejection

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-class-001"></a> PE-G3-CLASS-001 | MUST | applicable | Every valid Protocol Action Determination | A valid Determination MUST record exactly one mutually exclusive acceptance or rejection classification. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-class-002"></a> PE-G3-CLASS-002 | MUST | applicable | Every correct accepting Determination | Acceptance MUST mean that completed Evaluation established satisfaction of every applicable protocol rule within the identified evaluation context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-class-003"></a> PE-G3-CLASS-003 | MUST | applicable | Every correct rejecting Determination | Rejection MUST mean that completed Evaluation established non-satisfaction of at least one applicable protocol rule within the identified evaluation context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-class-004"></a> PE-G3-CLASS-004 | MUST | applicable | Every correct Protocol Action Determination | The Determination MUST accept the Action exactly when the Action is protocol-valid within the identified evaluation context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-class-005"></a> PE-G3-CLASS-005 | MUST | applicable | Every correct Protocol Action Determination | The Determination MUST reject the Action exactly when the Action is not protocol-valid within the identified evaluation context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-class-006"></a> PE-G3-CLASS-006 | MUST NOT | applicable | Every incomplete Evaluation, Evaluation failure, and pre-evaluation failure | An incomplete Evaluation, Evaluation failure, or pre-evaluation failure MUST NOT be classified as acceptance or rejection. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-class-007"></a> PE-G3-CLASS-007 | MUST NOT | applicable | Every infrastructure, transport, deployment, storage, implementation, and observability failure | An operational or implementation failure MUST NOT be represented as protocol rejection. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | STATE |
| <a id="pe-g3-class-008"></a> PE-G3-CLASS-008 | MUST NOT | applicable | Every proof-invalid result considered outside complete Protocol Action Evaluation | A proof-invalid result alone MUST NOT be represented as a complete rejecting Determination. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-class-009"></a> PE-G3-CLASS-009 | MUST NOT | applicable | Every erroneous acceptance or rejection classification | An incorrect classification MUST NOT redefine the applicable rules, protocol validity, or protocol semantics. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-class-010"></a> PE-G3-CLASS-010 | MUST NOT | applicable | Every acceptance and rejection classification | Acceptance or rejection MUST NOT be represented as a separately identified acceptance object, rejection object, or Evaluation Outcome object. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-class-011"></a> PE-G3-CLASS-011 | MUST NOT | applicable | Every application or external interpretation of acceptance or rejection | Acceptance or rejection MUST NOT be treated as establishing application, factual, legal, social, or institutional truth. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-class-012"></a> PE-G3-CLASS-012 | MUST NOT | applicable | Every acceptance or rejection representation, identifier, diagnostic, log, field, route, test, example, and observability surface | An acceptance or rejection classification MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S25 | STATE |

<a id="pe-g3-rf-25"></a>
### RF-25 — Accepted no-transition behavior

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-notrans-001"></a> PE-G3-NOTRANS-001 | MUST | applicable | Every accepted Protocol Action Determination | The applicable protocol rules MUST determine whether the accepted Determination requires no authorized Protocol State Transition. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-notrans-002"></a> PE-G3-NOTRANS-002 | MUST | applicable | Every accepted Determination for which no transition is required | The Determination MUST terminate successfully without an authorized Protocol State Transition. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-notrans-003"></a> PE-G3-NOTRANS-003 | MUST | applicable | Every accepted no-transition path | The path MUST be treated as a complete successful terminal path at the Determination boundary. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-notrans-004"></a> PE-G3-NOTRANS-004 | MUST NOT | applicable | Every accepted no-transition path | An accepted no-transition path MUST NOT be represented as rejection, incomplete Evaluation, Evaluation failure, pre-transition failure, transition failure, incomplete execution, missing commitment, or implementation error. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-notrans-005"></a> PE-G3-NOTRANS-005 | MUST NOT | applicable | Every inference from Protocol Action acceptance | Acceptance alone MUST NOT be treated as establishing that a Protocol State Transition exists. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-notrans-006"></a> PE-G3-NOTRANS-006 | MUST NOT | applicable | Every inference from Protocol Action acceptance | Acceptance alone MUST NOT be treated as transition authorization. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-notrans-007"></a> PE-G3-NOTRANS-007 | MUST NOT | applicable | Every inference from Protocol Action acceptance | Acceptance alone MUST NOT be treated as transition execution or commitment. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-notrans-008"></a> PE-G3-NOTRANS-008 | MUST NOT | applicable | Every rejecting Protocol Action Determination | A rejecting Determination MUST NOT authorize a transition that requires an accepted Determination. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-notrans-009"></a> PE-G3-NOTRANS-009 | MUST NOT | applicable | Every implementation handling an accepted no-transition path | An implementation MUST NOT invent a transition, report missing commitment, or reinterpret the protocol-defined absence of a transition as failure. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |

<a id="pe-g3-sf-09"></a>
## SF-09 — Protocol State, Transition Semantics, Preconditions, and Authorization

<a id="pe-g3-rf-26"></a>
### RF-26 — Published transition mappings, preconditions, and eligibility

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-transmap-001"></a> PE-G3-TRANSMAP-001 | MUST | applicable | Every published Protocol Transition mapping | A Protocol Transition mapping MUST possess one stable mapping identity within the applicable published protocol generation. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S26 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transmap-002"></a> PE-G3-TRANSMAP-002 | MUST | applicable | Every published Protocol Transition mapping | The mapping MUST define the permitted semantic relation between its applicable pre-transition-state class and its protocol-defined successor-state class. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S26, PE-G3-SOURCE-S36 | NONE |
| <a id="pe-g3-transmap-003"></a> PE-G3-TRANSMAP-003 | MUST NOT | applicable | Every Protocol Transition mapping and every interpretation of it | A Protocol Transition mapping MUST NOT be represented as one Protocol State Transition occurrence, execution, commitment, history entry, or actor occurrence. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S26, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transmap-004"></a> PE-G3-TRANSMAP-004 | MUST | applicable | Every implementation applying a Protocol Transition mapping | The implementation MUST preserve the mapping identity and published transition semantics unchanged. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S26, PE-G3-SOURCE-S33, PE-G3-SOURCE-S36 | STATE |
| <a id="pe-g3-transmap-005"></a> PE-G3-TRANSMAP-005 | MUST | applicable | Every published Protocol Transition mapping with transition-specific preconditions | The mapping MUST identify the complete published precondition set governing its eligibility. | PE-G3-SOURCE-S26, PE-G3-SOURCE-S37 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transmap-006"></a> PE-G3-TRANSMAP-006 | MUST | applicable | Every transition-eligibility evaluation | Eligibility MUST be established against the applicable protocol state, identified mapping, applicable Action context, and complete published transition-precondition set. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S26, PE-G3-SOURCE-S33, PE-G3-SOURCE-S37 | NONE |
| <a id="pe-g3-transmap-007"></a> PE-G3-TRANSMAP-007 | MUST | applicable | Every transition-eligibility evaluation whose complete applicable precondition set is satisfied | The eligibility result MUST preserve the identified mapping and permit only the later processing authorized by the applicable protocol rules. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S33, PE-G3-SOURCE-S37 | NONE |
| <a id="pe-g3-transmap-008"></a> PE-G3-TRANSMAP-008 | MUST | applicable | Every transition-eligibility evaluation whose applicable precondition set is not completely satisfied | The ineligible result MUST preserve the applicable pre-transition protocol state as unchanged by that attempted transition. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S33, PE-G3-SOURCE-S36, PE-G3-SOURCE-S37 | NONE |
| <a id="pe-g3-transmap-009"></a> PE-G3-TRANSMAP-009 | MUST NOT | applicable | Every implementation evaluating transition preconditions | The implementation MUST NOT infer satisfaction, weaken or strengthen a precondition, substitute another condition, repair the applicable state, or derive an alternate mapping. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S33, PE-G3-SOURCE-S36, PE-G3-SOURCE-S37 | STATE |
| <a id="pe-g3-transmap-010"></a> PE-G3-TRANSMAP-010 | MUST | applicable | Every relationship between transition eligibility and complete Protocol Action Evaluation | Transition eligibility MUST remain a bounded transition-specific evaluation distinct from the complete Evaluation defined by RF-22. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S33, PE-G3-SOURCE-S37 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transmap-011"></a> PE-G3-TRANSMAP-011 | MUST NOT | applicable | Every transition-enforcement result | A transition-enforcement result MUST NOT itself establish acceptance or rejection, create or alter a Determination, authorize or execute a transition occurrence, commit state change, or establish successor state. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S33, PE-G3-SOURCE-S36 | NONE |
| <a id="pe-g3-transmap-012"></a> PE-G3-TRANSMAP-012 | MUST NOT | applicable | Every implementation-local restriction on operation exposure, request handling, or execution capability | An implementation-local restriction MUST NOT be represented as a published transition precondition or as changing protocol eligibility semantics. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S33, PE-G3-SOURCE-S37 | STATE |
| <a id="pe-g3-transmap-013"></a> PE-G3-TRANSMAP-013 | MUST NOT | applicable | Every mapping, precondition, eligibility, enforcement, diagnostic, log, field, route, test, example, serialization, and observability surface | A transition-mapping or eligibility surface MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S26, PE-G3-SOURCE-S33, PE-G3-SOURCE-S37 | STATE |
| <a id="pe-g3-tmreg-001"></a> PE-G3-TMREG-001 | MUST | applicable | ALWAYS | The successor MUST contain exactly one closed transition-mapping registry with the identity and serialization defined by S69. | PE-G3-SOURCE-S69 | NONE |
| <a id="pe-g3-tmreg-002"></a> PE-G3-TMREG-002 | MUST | applicable | ALWAYS | Each registry row MUST bind one mapping identity, path and digest to one profile identity, path and digest. | PE-G3-SOURCE-S69 | NONE |
| <a id="pe-g3-tmreg-003-a01"></a> PE-G3-TMREG-003-A01 | MUST | applicable | ALWAYS | Mapping-to-profile cardinality MUST be exactly 1:1. | PE-G3-SOURCE-S69 | NONE |
| <a id="pe-g3-tmreg-003-a02"></a> PE-G3-TMREG-003-A02 | MUST | applicable | ALWAYS | Mapping and profile ordinals MUST match. | PE-G3-SOURCE-S69 | NONE |
| <a id="pe-g3-tmreg-004"></a> PE-G3-TMREG-004 | MUST | applicable | ALWAYS | The registry MUST reject duplicates, missing members, digest mismatch, conflicting bindings and unresolved applicability or recovery definitions. | PE-G3-SOURCE-S69 | NONE |
| <a id="pe-g3-tmreg-005-a01"></a> PE-G3-TMREG-005-A01 | MUST | applicable | ALWAYS | An empty validated registry MUST authorize zero transitions. | PE-G3-SOURCE-S69 | NONE |
| <a id="pe-g3-tmreg-005-a02"></a> PE-G3-TMREG-005-A02 | MUST NOT | applicable | ALWAYS | An empty validated registry MUST NOT imply missing or inferred mappings. | PE-G3-SOURCE-S69 | NONE |
| <a id="pe-g3-tmreg-006"></a> PE-G3-TMREG-006 | MUST NOT | applicable | ALWAYS | A mapping MUST NOT be inferred or discovered from an implementation, interface, runtime, storage, application or observed behaviour. | PE-G3-SOURCE-S69 | NONE |
| <a id="pe-g3-tmreg-007"></a> PE-G3-TMREG-007 | MUST | applicable | ALWAYS | Registry membership, mappings and profiles MUST be immutable within one generation. | PE-G3-SOURCE-S69 | NONE |
| <a id="pe-g3-tmreg-008"></a> PE-G3-TMREG-008 | MUST | applicable | ALWAYS | Any registry, mapping or profile change MUST require a distinct future Protocol Generation. | PE-G3-SOURCE-S69 | NONE |
| <a id="pe-g3-tseprof-001"></a> PE-G3-TSEPROF-001 | MUST | applicable | ALWAYS | Every mapping MUST reference one separate immutable normative equivalence profile and its SHA-256. | PE-G3-SOURCE-S70 | NONE |
| <a id="pe-g3-tseprof-002"></a> PE-G3-TSEPROF-002 | MUST | applicable | ALWAYS | Every profile MUST include all scalar, definition, projection and recovery fields required by S70 without blanks or implementation defaults. | PE-G3-SOURCE-S70 | NONE |
| <a id="pe-g3-tseprof-003"></a> PE-G3-TSEPROF-003 | MUST | applicable | ALWAYS | Every profile definition MUST resolve to one authoritative successor source anchor and one total deterministic PE-TSE-EXPR-V2 expression. | PE-G3-SOURCE-S70 | NONE |
| <a id="pe-g3-tseprof-004"></a> PE-G3-TSEPROF-004 | MUST | applicable | ALWAYS | Every component MUST define its type, representation, canonicalization, normalization, authority, availability, validity, authentication, privacy and observability rules. | PE-G3-SOURCE-S70 | NONE |
| <a id="pe-g3-tseprof-005"></a> PE-G3-TSEPROF-005 | MUST | applicable | ALWAYS | Every profile MUST define mutually exclusive equivalence and material-conflict predicates that cover all complete valid inputs. | PE-G3-SOURCE-S70 | NONE |
| <a id="pe-g3-tseprof-006-a01"></a> PE-G3-TSEPROF-006-A01 | MUST | applicable | ALWAYS | Every profile MUST define which differences are immaterial. | PE-G3-SOURCE-S70 | NONE |
| <a id="pe-g3-tseprof-006-a02"></a> PE-G3-TSEPROF-006-A02 | MUST | applicable | ALWAYS | Every profile MUST prove that each immaterial difference is outside the mapping's materiality boundary. | PE-G3-SOURCE-S70 | NONE |
| <a id="pe-g3-tseprof-007"></a> PE-G3-TSEPROF-007 | MUST | applicable | ALWAYS | Every profile MUST define and validate Dep(D) membership and its complete recovery table. | PE-G3-SOURCE-S70 | NONE |
| <a id="pe-g3-tseprof-008-a01"></a> PE-G3-TSEPROF-008-A01 | MUST | applicable | ALWAYS | An incomplete, ambiguous, cyclic, non-total or privacy-invalid profile MUST be inadmissible. | PE-G3-SOURCE-S70 | NONE |
| <a id="pe-g3-tseprof-008-a02"></a> PE-G3-TSEPROF-008-A02 | MUST | applicable | ALWAYS | An incomplete, ambiguous, cyclic, non-total or privacy-invalid profile MUST authorize no transition. | PE-G3-SOURCE-S70 | NONE |

<a id="pe-g3-rf-27"></a>
### RF-27 — Protocol State Transition occurrence identity and lifecycle

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-transocc-001"></a> PE-G3-TRANSOCC-001 | MUST | applicable | Every Protocol State Transition | A Protocol State Transition MUST possess one stable occurrence identity identifying exactly one bounded protocol-governed state-change occurrence. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transocc-002"></a> PE-G3-TRANSOCC-002 | MUST | applicable | Every Protocol State Transition | The occurrence MUST retain one bounded lifecycle across every applicable authorization, execution, commitment, and failure stage. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transocc-003"></a> PE-G3-TRANSOCC-003 | MUST | applicable | Every relationship between a Protocol Action and a Protocol State Transition | The Action and transition occurrence MUST retain distinct identities and semantic roles. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transocc-004"></a> PE-G3-TRANSOCC-004 | MUST | applicable | Every relationship between a Protocol Action Evaluation and a Protocol State Transition | The Evaluation and transition occurrence MUST retain distinct identities and semantic roles. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transocc-005"></a> PE-G3-TRANSOCC-005 | MUST | applicable | Every relationship between a Protocol Action Determination and a Protocol State Transition | The Determination and transition occurrence MUST retain distinct identities and semantic roles. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transocc-006"></a> PE-G3-TRANSOCC-006 | MUST | applicable | Every Protocol State Transition occurrence | The occurrence MUST remain distinct from its governing mapping, pre-transition state, successor state, implementation, history representation, and public consequence. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S26, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transocc-007"></a> PE-G3-TRANSOCC-007 | MUST | applicable | Every authorization, execution, commitment, and failure stage concerning one Protocol State Transition | Every stage MUST preserve the identity of the same authorized `U`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-transocc-008"></a> PE-G3-TRANSOCC-008 | MUST NOT | applicable | Every transition lifecycle representation | Authorization, execution, commitment, or failure MUST NOT be represented as a separately identified first-class transition object. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transocc-009"></a> PE-G3-TRANSOCC-009 | MUST | applicable | Every terminal Protocol State Transition classification | A terminal transition MUST be classified as committed or transition failure, but not both. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transocc-010"></a> PE-G3-TRANSOCC-010 | MUST NOT | applicable | Every authorized transition that has not reached a terminal classification | Absence of commitment MUST NOT by itself be represented as transition failure. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transocc-011"></a> PE-G3-TRANSOCC-011 | MUST NOT | applicable | Every transition identifier, lifecycle record, representation, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A transition-occurrence surface MUST NOT identify the Private Actor, carry enrollment or admission provenance, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-tsecmpid-001"></a> PE-G3-TSECMPID-001 | MUST | applicable | ALWAYS | Each comparison attempt MUST bind one successor generation, mapping, profile, authorization, D, Q0 and U. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tsecmpid-002"></a> PE-G3-TSECMPID-002 | MUST | applicable | ALWAYS | Comparison ordinals MUST begin at 000001 and be contiguous within U. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tsecmpid-003-a01"></a> PE-G3-TSECMPID-003-A01 | MUST | applicable | ALWAYS | Each attempt and result MUST remain immutable history of U. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tsecmpid-003-a02"></a> PE-G3-TSECMPID-003-A02 | MUST | applicable | ALWAYS | Each attempt and result MUST have no lifecycle independent of U. | PE-G3-SOURCE-S72 | NONE |

<a id="pe-g3-rf-28"></a>
### RF-28 — Transition authorization and cardinality

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-transauth-001"></a> PE-G3-TRANSAUTH-001 | MUST | applicable | Every authorization of a Protocol State Transition arising from a Protocol Action | The transition MUST be authorized by one accepted Protocol Action Determination. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transauth-002"></a> PE-G3-TRANSAUTH-002 | MUST NOT | applicable | Every rejected Determination, incomplete Evaluation, Evaluation failure, and absence of Determination | The condition MUST NOT authorize an accepted Protocol State Transition. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transauth-003"></a> PE-G3-TRANSAUTH-003 | MUST | applicable | Every transition authorization | Authorization MUST identify the authorizing Determination, authorized `U`, governing `T`, applicable `Q0`, required successor-state relation, and every protocol-defined ordering or dependency. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S26, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transauth-004"></a> PE-G3-TRANSAUTH-004 | MUST | applicable | Every transition authorization | Authorization MUST select one sufficiently bounded transition occurrence rather than a class of later implementation-selected outcomes. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transauth-005"></a> PE-G3-TRANSAUTH-005 | MUST NOT | applicable | Every accepted Protocol Action Determination | Acceptance MUST NOT by itself be represented as establishing transition authorization or that a transition occurrence exists. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transauth-006"></a> PE-G3-TRANSAUTH-006 | MUST NOT | applicable | Every transition authorization | Authorization MUST NOT be represented as transition execution. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transauth-007"></a> PE-G3-TRANSAUTH-007 | MUST NOT | applicable | Every transition authorization | Authorization MUST NOT be represented as transition commitment. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transauth-008"></a> PE-G3-TRANSAUTH-008 | MUST NOT | applicable | Every transition authorization | Authorization MUST NOT be represented as an authoritative protocol-state change or authoritative successor state. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transauth-009"></a> PE-G3-TRANSAUTH-009 | MUST | applicable | Every accepted Determination for which transition cardinality is applicable | The complete applicable protocol rules MUST determine whether the Determination authorizes zero, exactly one, or multiple transition occurrences. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transauth-010"></a> PE-G3-TRANSAUTH-010 | MUST NOT | applicable | Every implementation realizing transition authorization | The implementation MUST NOT choose transition cardinality for convenience, preferred outcome, infrastructure capability, or implementation policy. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-transauth-011"></a> PE-G3-TRANSAUTH-011 | MUST | applicable | Every accepted Determination requiring zero transitions | The zero-transition authorization relation MUST preserve the successful terminal behavior defined by RF-25 without fabricating a transition occurrence. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transauth-012"></a> PE-G3-TRANSAUTH-012 | MUST | applicable | Every accepted Determination authorizing multiple independently committable effects | Each independently committable effect MUST remain one separately identified and separately atomic transition occurrence. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transauth-013"></a> PE-G3-TRANSAUTH-013 | MUST | applicable | Every accepted Determination authorizing multiple transitions with protocol-defined ordering or dependencies | Every authorized ordering and dependency MUST be preserved across the separately identified transitions. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transauth-014"></a> PE-G3-TRANSAUTH-014 | MUST | applicable | Every group of protocol-required state effects that must succeed or fail together | The effects MUST be represented as one composite atomic Protocol State Transition rather than as independently committable transitions. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-transauth-015"></a> PE-G3-TRANSAUTH-015 | MUST NOT | applicable | Every authorization of multiple separately identified Protocol State Transitions | Multiple authorized transitions MUST NOT be represented as a separately identified first-class transition-set object. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-tseauth-001"></a> PE-G3-TSEAUTH-001 | MUST | applicable | ALWAYS | Every authorization MUST use the canonical header and component-binding serialization defined by S71. | PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tseauth-002"></a> PE-G3-TSEAUTH-002 | MUST | applicable | ALWAYS | The authorization header MUST bind generation, mapping and digest, profile and digest, authorization, U, D, Q0, successor-state relation, coordinate-set digests and component count. | PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tseauth-003"></a> PE-G3-TSEAUTH-003 | MUST | applicable | ALWAYS | Ordering and dependency coordinate sets MUST be canonically serialized and digest-bound even when empty. | PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tseauth-004-a01"></a> PE-G3-TSEAUTH-004-A01 | MUST | applicable | ALWAYS | Each component binding mode MUST be fixed by the published profile. | PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tseauth-004-a02"></a> PE-G3-TSEAUTH-004-A02 | MUST NOT | applicable | ALWAYS | Each component binding mode MUST NOT be chosen per execution. | PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tseauth-005"></a> PE-G3-TSEAUTH-005 | MUST | applicable | ALWAYS | Canonical-value mode MUST bind the exact normalized canonical bytes without implying public disclosure. | PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tseauth-006"></a> PE-G3-TSEAUTH-006 | MUST | applicable | ALWAYS | Blinded mode MUST bind authorization context, component identity, canonical type, canonical bytes and one independent 32-octet blind under PE-TSE-SHA256-COMMITMENT-V1. | PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tseauth-007"></a> PE-G3-TSEAUTH-007 | MUST | applicable | ALWAYS | Commitment opening MUST authenticate its source, recompute every bound coordinate and require exact digest equality before semantic comparison. | PE-G3-SOURCE-S71 | NONE |
| <a id="pe-g3-tseauth-008"></a> PE-G3-TSEAUTH-008 | MUST | applicable | ALWAYS | Missing, invalid, unauthenticated or mismatched authorization material MUST yield indeterminate and prohibit execution and commitment. | PE-G3-SOURCE-S71 | NONE |

<a id="pe-g3-sf-10"></a>
## SF-10 — Transition Execution, Commitment, Atomicity, and State Evolution

<a id="pe-g3-rf-29"></a>
### RF-29 — Transition execution and preservation

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-transexec-001"></a> PE-G3-TRANSEXEC-001 | MUST | applicable | Every Protocol State Transition execution | Execution MUST be the bounded implementation activity that attempts to realize one already-authorized `U`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transexec-002"></a> PE-G3-TRANSEXEC-002 | MUST | applicable | Every execution entry | Execution MUST begin only where the applicable authorization and transition-eligibility conditions permit execution of the identified `U`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S33, PE-G3-SOURCE-S34 | NONE |
| <a id="pe-g3-transexec-003"></a> PE-G3-TRANSEXEC-003 | MUST | applicable | Every execution of an authorized Protocol State Transition | Execution MUST preserve the transition identity, authorizing Determination, governing mapping, authorized pre-transition state, required successor-state relation, atomicity, and complete protocol-defined effects. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S26, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34 | STATE |
| <a id="pe-g3-transexec-004"></a> PE-G3-TRANSEXEC-004 | MUST | applicable | Every implementation executing an authorized Protocol State Transition | The implementation MUST realize the authorized `U` exactly as defined by the published transition semantics. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S26, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34 | NONE |
| <a id="pe-g3-transexec-005"></a> PE-G3-TRANSEXEC-005 | MUST NOT | applicable | Every implementation executing an authorized Protocol State Transition | The implementation MUST NOT redefine, reinterpret, widen, narrow, repair, merge, divide, or infer replacement semantics for `U`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34 | STATE |
| <a id="pe-g3-transexec-006"></a> PE-G3-TRANSEXEC-006 | MUST NOT | applicable | Every execution of authorized `U` | Execution MUST NOT substitute, execute, commit, or report `U'` as `U` where `U' != U`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34 | NONE |
| <a id="pe-g3-transexec-007"></a> PE-G3-TRANSEXEC-007 | MUST | applicable | Every relationship between transition eligibility and transition execution | Eligibility and execution MUST remain distinct stages, with eligibility deciding only whether the already-identified transition may proceed. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S33, PE-G3-SOURCE-S34 | NONE |
| <a id="pe-g3-transexec-008"></a> PE-G3-TRANSEXEC-008 | MUST NOT | applicable | Every completed transition execution | Completed execution MUST NOT by itself be represented as commitment or authoritative protocol-state change. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34 | NONE |
| <a id="pe-g3-transexec-009"></a> PE-G3-TRANSEXEC-009 | MUST NOT | applicable | Every successor-state value or representation derived during execution | Execution machinery and execution output MUST NOT claim or expose derived successor-state material as committed authoritative protocol state before valid RF-30 commitment. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34, PE-G3-SOURCE-S39 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-transexec-010"></a> PE-G3-TRANSEXEC-010 | MUST | applicable | Every implementation unable to preserve the authorized transition during execution | The implementation MUST fail the execution cleanly while preserving the identity and semantics of the authorized `U`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34 | STATE |
| <a id="pe-g3-transexec-011"></a> PE-G3-TRANSEXEC-011 | MUST NOT | applicable | Every failed transition execution | Execution failure MUST NOT authorize an alternate transition, alternate successor state, partial commitment, or semantic substitution. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34 | NONE |
| <a id="pe-g3-transexec-012"></a> PE-G3-TRANSEXEC-012 | MUST NOT | applicable | Every execution representation, instruction, transaction, internal call, storage operation, retry, diagnostic, log, field, route, test, example, serialization, and observability surface | An execution surface MUST NOT create another architectural transition identity, identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34 | STATE |
| <a id="pe-g3-tseexec-001"></a> PE-G3-TSEEXEC-001 | MUST | applicable | ALWAYS | Bounded execution MUST begin only after the immediately preceding comparison returns equivalent. | PE-G3-SOURCE-S34, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseexec-002"></a> PE-G3-TSEEXEC-002 | MUST | applicable | ALWAYS | material-conflict or indeterminate before execution MUST prohibit execution. | PE-G3-SOURCE-S34 | NONE |
| <a id="pe-g3-tseexec-003-a01"></a> PE-G3-TSEEXEC-003-A01 | MUST | applicable | ALWAYS | Execution failure MUST terminally fail U. | PE-G3-SOURCE-S34, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseexec-003-a02"></a> PE-G3-TSEEXEC-003-A02 | MUST | applicable | ALWAYS | Execution failure MUST prohibit partial commitment, repair, resumption or alternate successor-state substitution. | PE-G3-SOURCE-S34, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseexec-004"></a> PE-G3-TSEEXEC-004 | MUST | applicable | ALWAYS | A later execution attempt MUST use a new U and a valid new authorization selected by the total disposition function. | PE-G3-SOURCE-S34, PE-G3-SOURCE-S72 | NONE |

<a id="pe-g3-rf-30"></a>
### RF-30 — Transition commitment, completeness, and atomicity

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-commit-001"></a> PE-G3-COMMIT-001 | MUST | applicable | Every committed Protocol State Transition | Commitment MUST be the successful terminal predicate of the same identified `U` that was authorized and executed. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-commit-002"></a> PE-G3-COMMIT-002 | MUST | applicable | Every committed Protocol State Transition | Commitment MUST derive from one valid accepted Determination and valid authorization of `U`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-commit-003"></a> PE-G3-COMMIT-003 | MUST | applicable | Every committed Protocol State Transition | Commitment MUST follow correct execution that preserves the complete authorized identity and semantics of `U`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34 | STATE |
| <a id="pe-g3-commit-004"></a> PE-G3-COMMIT-004 | MUST | applicable | ALWAYS | Every committed U authorized against Q0 MUST have produced equivalent under its governing immutable profile at the semantic commitment boundary, after successful bounded execution and without an intervening authoritative protocol-state change. | PE-G3-SOURCE-S27, PE-G3-SOURCE-S36, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-commit-005"></a> PE-G3-COMMIT-005 | MUST | applicable | Every committed Protocol State Transition | Commitment MUST establish the complete protocol-defined state-change relation and the required successor state `Q1`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S36, PE-G3-SOURCE-S39 | NONE |
| <a id="pe-g3-commit-006"></a> PE-G3-COMMIT-006 | MUST | applicable | Every committed Protocol State Transition | Commitment MUST establish the absence of omitted required effects and unauthorized additional state effects. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S36 | NONE |
| <a id="pe-g3-commit-007"></a> PE-G3-COMMIT-007 | MUST | applicable | Every committed Protocol State Transition | Commitment MUST preserve semantic atomicity across every protocol-required effect owned by `U`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S36 | NONE |
| <a id="pe-g3-commit-008"></a> PE-G3-COMMIT-008 | MUST | applicable | Every valid authorization and execution context for `U` | Commitment MUST be equivalent to complete state change only within that valid bounded context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-commit-009"></a> PE-G3-COMMIT-009 | MUST NOT | applicable | Every partial execution of a Protocol State Transition | Partial execution MUST NOT be represented as commitment. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S36 | NONE |
| <a id="pe-g3-commit-010"></a> PE-G3-COMMIT-010 | MUST NOT | applicable | Every partial or incomplete state change | A partial or incomplete state change MUST NOT be represented as commitment or authoritative successor state. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S36 | NONE |
| <a id="pe-g3-commit-011"></a> PE-G3-COMMIT-011 | MUST NOT | applicable | Every Protocol State Transition | A transition MUST NOT be partially committed. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S36 | NONE |
| <a id="pe-g3-commit-012"></a> PE-G3-COMMIT-012 | MUST NOT | applicable | Every implementation assertion, report, event, record, diagnostic, or representation concerning commitment | The implementation surface MUST NOT by itself establish protocol commitment. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-commit-013"></a> PE-G3-COMMIT-013 | MUST NOT | applicable | Every commitment representation and interpretation | Commitment MUST NOT be represented as a separately identified first-class object or as possessing authority or lifecycle independent of `U`. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-tsecommit-001"></a> PE-G3-TSECOMMIT-001 | MUST | applicable | ALWAYS | Successful execution MUST be followed by authoritative comparison revalidation at the semantic commitment boundary. | PE-G3-SOURCE-S36 | NONE |
| <a id="pe-g3-tsecommit-002"></a> PE-G3-TSECOMMIT-002 | MUST | applicable | ALWAYS | Only equivalent at revalidation MUST permit commitment. | PE-G3-SOURCE-S36 | NONE |
| <a id="pe-g3-tsecommit-003"></a> PE-G3-TSECOMMIT-003 | MUST | applicable | ALWAYS | material-conflict, indeterminate or revalidation failure after execution MUST terminally fail U and prohibit commitment. | PE-G3-SOURCE-S36 | NONE |
| <a id="pe-g3-tsecommit-004"></a> PE-G3-TSECOMMIT-004 | MUST | applicable | ALWAYS | No partial protocol state or alternate successor state from a failed U MUST become authoritative. | PE-G3-SOURCE-S36, PE-G3-SOURCE-S39 | NONE |
| <a id="pe-g3-tsecommit-005"></a> PE-G3-TSECOMMIT-005 | MUST | applicable | ALWAYS | Revalidation and commitment MUST form one indivisible protocol-semantic decision without requiring any implementation transaction mechanism. | PE-G3-SOURCE-S36, PE-G3-SOURCE-S72 | NONE |

<a id="pe-g3-rf-31"></a>
### RF-31 — Protocol state, successor state, and state evolution

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-state-001"></a> PE-G3-STATE-001 | MUST | applicable | Every protocol-state representation | Protocol state MUST contain only state governed as protocol state by the applicable published protocol generation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S35 | STATE, PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-state-002"></a> PE-G3-STATE-002 | MUST NOT | applicable | Every application, implementation-local, transport, database, cache, UI, operational, diagnostic, and observability state representation | The representation MUST NOT be treated as protocol state merely because it describes, realizes, stores, or observes protocol activity. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S35 | STATE |
| <a id="pe-g3-state-003"></a> PE-G3-STATE-003 | MUST | applicable | Every Protocol State Transition authorization | The authorization MUST identify the bounded pre-transition protocol state `Q0` against which `U` is authorized. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S35 | NONE |
| <a id="pe-g3-state-004"></a> PE-G3-STATE-004 | MUST NOT | applicable | Every implementation realizing an authorized transition | The implementation MUST NOT select, reconstruct, repair, or substitute a preferred pre-transition protocol state after authorization. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S35 | STATE |
| <a id="pe-g3-state-005"></a> PE-G3-STATE-005 | MUST | applicable | Every successor-state derivation | `Q1` MUST be derived only from the authorized `U`, governing `T`, applicable `Q0`, and complete published transition semantics. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S26, PE-G3-SOURCE-S27, PE-G3-SOURCE-S36, PE-G3-SOURCE-S38, PE-G3-SOURCE-S39 | NONE |
| <a id="pe-g3-state-006"></a> PE-G3-STATE-006 | MUST NOT | applicable | Every implementation deriving successor-state material | The implementation MUST NOT invent, infer, repair, merge, widen, narrow, substitute, or add application meaning to `Q1`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S36, PE-G3-SOURCE-S39 | STATE |
| <a id="pe-g3-state-007"></a> PE-G3-STATE-007 | MUST NOT | applicable | Every successor-state value derived before commitment | Derived successor-state material MUST NOT be represented as authoritative protocol state. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34, PE-G3-SOURCE-S39 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-state-008"></a> PE-G3-STATE-008 | MUST | applicable | Every committed Protocol State Transition | Only valid commitment of `U` MUST establish `Q1` as authoritative successor state for that transition. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S36, PE-G3-SOURCE-S38, PE-G3-SOURCE-S39 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-state-009"></a> PE-G3-STATE-009 | MUST | applicable | Every committed Protocol State Transition from `Q0` to `Q1` | The pre-transition state, successor state, and transition occurrence MUST retain distinct identities and their exact committed relationship. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S35, PE-G3-SOURCE-S38, PE-G3-SOURCE-S39 | NONE |
| <a id="pe-g3-state-010"></a> PE-G3-STATE-010 | MUST | applicable | Every authoritative protocol-state evolution | State evolution MUST consist of one applicable `Q0`, one committed `U`, and the protocol-defined authoritative `Q1`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S35, PE-G3-SOURCE-S38 | NONE |
| <a id="pe-g3-state-011"></a> PE-G3-STATE-011 | MUST NOT | applicable | Every failed, incomplete, partial, simulated, predicted, or merely reported transition | The transition condition MUST NOT establish authoritative state evolution or authoritative `Q1`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S34, PE-G3-SOURCE-S38, PE-G3-SOURCE-S39 | STATE |
| <a id="pe-g3-state-012"></a> PE-G3-STATE-012 | MUST | applicable | Every committed protocol-state evolution | The evolution MUST preserve every applicable published protocol invariant and every complete protocol-required effect of `U`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S35, PE-G3-SOURCE-S36, PE-G3-SOURCE-S38 | NONE |
| <a id="pe-g3-state-013"></a> PE-G3-STATE-013 | MUST NOT | applicable | Every protocol-state identifier, state representation, successor-state derivation, evolution record, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A protocol-state surface MUST NOT identify the Private Actor, carry enrollment or admission provenance, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S27, PE-G3-SOURCE-S35, PE-G3-SOURCE-S38, PE-G3-SOURCE-S39 | STATE |
| <a id="pe-g3-tsestate-001"></a> PE-G3-TSESTATE-001 | MUST | applicable | ALWAYS | Current comparison values MUST be obtained only from authenticated protocol-owned authoritative state sources declared by the profile. | PE-G3-SOURCE-S35 | NONE |
| <a id="pe-g3-tsestate-002"></a> PE-G3-TSESTATE-002 | MUST NOT | applicable | ALWAYS | Runtime, application, database, diagnostic and observability state MUST NOT substitute for authoritative protocol state. | PE-G3-SOURCE-S35 | NONE |
| <a id="pe-g3-tsestate-003"></a> PE-G3-TSESTATE-003 | MUST | applicable | ALWAYS | State identifiers, ordering coordinates and dependency coordinates MUST be authenticated and canonicalized before predicate evaluation. | PE-G3-SOURCE-S35 | NONE |
| <a id="pe-g3-tsestate-004"></a> PE-G3-TSESTATE-004 | MUST | applicable | ALWAYS | State evolution and successor-state establishment MUST occur only through a committed U whose final comparison returned equivalent. | PE-G3-SOURCE-S38, PE-G3-SOURCE-S39 | NONE |

<a id="pe-g3-sf-11"></a>
## SF-11 — History, Public Consequences, Failure, Staleness, and Re-evaluation

<a id="pe-g3-rf-32"></a>
### RF-32 — Protocol-state history

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-statehist-001"></a> PE-G3-STATEHIST-001 | MUST | applicable | Every Protocol State Transition included as a committed state change in authoritative protocol-state history | The transition MUST have validly committed. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-statehist-002"></a> PE-G3-STATEHIST-002 | MUST | applicable | Every authoritative protocol-state history representation | The representation MUST preserve each committed transition identity, committed ordering, applicable pre-transition state, authoritative successor state, and bounded public consequence. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-statehist-003"></a> PE-G3-STATEHIST-003 | MUST NOT | applicable | Every failed Protocol State Transition | A failed transition MUST NOT be included as a committed transition in authoritative protocol-state history. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-statehist-004"></a> PE-G3-STATEHIST-004 | MUST NOT | applicable | Every pre-transition failure | A pre-transition failure MUST NOT be included as a committed transition in authoritative protocol-state history. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-statehist-005"></a> PE-G3-STATEHIST-005 | MUST NOT | applicable | Every partial execution or partial state change | Partial execution or partial state change MUST NOT be included as committed history. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-statehist-006"></a> PE-G3-STATEHIST-006 | MUST NOT | applicable | Every operational attempt, diagnostic, retry, log, database row, event, report, error, cache record, or observability record | An operational record MUST NOT be treated as authoritative protocol-state history merely because it describes protocol activity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-statehist-007"></a> PE-G3-STATEHIST-007 | MUST | applicable | Every permitted protocol-state history realization | The realization MUST preserve identical committed transition semantics independently of storage structure, database, blockchain, consensus, event, transaction, or infrastructure choice. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-statehist-008"></a> PE-G3-STATEHIST-008 | MUST NOT | applicable | Every history identifier, entry, representation, ordering record, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A protocol-state history surface MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S27 | STATE |

<a id="pe-g3-rf-33"></a>
### RF-33 — Public protocol-state consequences

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-stateconseq-001"></a> PE-G3-STATECONSEQ-001 | MUST | applicable | Every committed Protocol State Transition | Commitment MUST establish the bounded public protocol-state consequence defined for `U` and authoritative `Q1`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-stateconseq-002"></a> PE-G3-STATECONSEQ-002 | MUST | applicable | Every public protocol-state consequence | The consequence MUST remain bounded to the published protocol meaning of the committed state change. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-stateconseq-003"></a> PE-G3-STATECONSEQ-003 | MUST | applicable | Every relationship between a Published Result and a public protocol-state consequence | The interface-level Published Result and committed protocol-state consequence MUST remain distinct semantic roles. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S32 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-stateconseq-004"></a> PE-G3-STATECONSEQ-004 | MUST | applicable | Every relationship between a Protocol Action Determination and a public protocol-state consequence | The Determination and committed consequence MUST remain distinct, including where both are publicly observable. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-stateconseq-005"></a> PE-G3-STATECONSEQ-005 | MUST | applicable | Every relationship between authoritative successor state and public protocol-state consequence | The successor-state representation and its bounded public consequence MUST remain distinct without introducing an intermediate consequence object. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-stateconseq-006"></a> PE-G3-STATECONSEQ-006 | MUST NOT | applicable | Every public protocol-state consequence and every interpretation of it | The consequence MUST NOT be represented as application, factual, legal, social, institutional, user-intent, or off-protocol truth. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-stateconseq-007"></a> PE-G3-STATECONSEQ-007 | MUST NOT | applicable | Every public protocol-state consequence | The consequence MUST NOT be represented as a separately identified first-class object possessing authority or lifecycle independent of committed `U`. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-stateconseq-008"></a> PE-G3-STATECONSEQ-008 | MUST NOT | applicable | Every public consequence identifier, representation, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A public-consequence surface MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-stateconseq-009"></a> PE-G3-STATECONSEQ-009 | MUST NOT | applicable | Every public consequence recording authorization, membership, eligibility, uniqueness, possession, or another bounded protocol property | The recorded property MUST NOT be extended into actor identification, enrollment or admission provenance, hidden intent, or additional correlation meaning. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | STATE |

<a id="pe-g3-rf-34"></a>
### RF-34 — Failure classifications and failure separation

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-fail-001"></a> PE-G3-FAIL-001 | MUST | applicable | Every protocol-use failure or implementation-error classification | The classification MUST identify the actual bounded lifecycle stage and condition that occurred. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27, PE-G3-SOURCE-S37 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-fail-002"></a> PE-G3-FAIL-002 | MUST | applicable | Every pre-evaluation failure | Pre-evaluation failure MUST mean that no valid Protocol Action Evaluation occurrence began. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-fail-003"></a> PE-G3-FAIL-003 | MUST | applicable | Every Protocol Action Evaluation failure | Evaluation failure MUST mean that one Evaluation began but did not complete and produced no Determination. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-fail-004"></a> PE-G3-FAIL-004 | MUST | applicable | Every Protocol Action rejection | Rejection MUST remain the rejecting classification of one valid Determination produced by one completed Evaluation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-fail-005"></a> PE-G3-FAIL-005 | MUST | applicable | Every accepted no-transition terminal path | Accepted no-transition MUST remain a successful Determination-boundary completion rather than a failure classification. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-fail-006"></a> PE-G3-FAIL-006 | MUST | applicable | Every pre-transition failure | Pre-transition failure MUST mean that the post-Determination transition boundary could not validly enter bounded execution. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S37 | NONE |
| <a id="pe-g3-fail-007"></a> PE-G3-FAIL-007 | MUST | applicable | Every transition failure | Transition failure MUST remain the explicit terminal classification of an authorized transition that does not establish complete commitment. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-fail-008"></a> PE-G3-FAIL-008 | MUST NOT | applicable | Every stale authorization | Stale authorization MUST NOT be represented as rejection, Evaluation failure, or proof that the earlier Determination was incorrect. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-fail-009"></a> PE-G3-FAIL-009 | MUST | applicable | Every implementation error | Implementation error MUST remain a bounded diagnosis of incorrect realization, classification, commitment, or reporting rather than a redefinition of protocol truth. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-fail-010"></a> PE-G3-FAIL-010 | MUST | applicable | Every incorrect execution diagnosis | Incorrect execution MUST identify implementation failure to preserve or correctly realize authorized `U` without becoming semantically equivalent to every transition failure. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-fail-011"></a> PE-G3-FAIL-011 | MUST | applicable | Every incorrect commitment diagnosis | Incorrect commitment MUST identify an implementation representation or materialization that does not satisfy valid protocol commitment. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-fail-012"></a> PE-G3-FAIL-012 | MUST | applicable | Every incorrect reporting diagnosis | Incorrect reporting MUST remain distinct from the protocol condition incorrectly reported. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-fail-013"></a> PE-G3-FAIL-013 | MUST NOT | applicable | Every pre-transition failure | Pre-transition failure MUST NOT be represented as transition failure where bounded execution of `U` did not begin. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-fail-014"></a> PE-G3-FAIL-014 | MUST NOT | applicable | Every transition failure, stale authorization, implementation error, incorrect execution, incorrect commitment, and incorrect reporting condition | A later-stage condition MUST NOT be converted into Protocol Action rejection or Evaluation failure. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-fail-015"></a> PE-G3-FAIL-015 | MUST NOT | applicable | Every infrastructure failure, inability to preserve `U`, changed-state condition, partial execution, or reporting error | The condition MUST NOT be silently converted into commitment or another semantically different success or failure class. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-fail-016"></a> PE-G3-FAIL-016 | MUST NOT | applicable | Every failure, error, staleness, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A failure surface MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, expose implementation or operational metadata as actor identity, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-fail-017"></a> PE-G3-FAIL-017 | MUST NOT | applicable | Every failure classification and implementation-error diagnosis | A failure classification or error diagnosis MUST NOT be represented as a separately identified first-class failure object. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-fail-018"></a> PE-G3-FAIL-018 | MUST | applicable | Every failure before authoritative Evaluation begins | Failure before authoritative Evaluation begins MUST create no authoritative Evaluation, Determination, acceptance or rejection. | PE-G3-SOURCE-S25 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-fail-019"></a> PE-G3-FAIL-019 | MUST NOT | applicable | Every later failure after Determination production | Failure of representation, serialization, persistence, publication, transport, operational delivery, display, indexing or application translation after Determination production MUST NOT erase the Determination, reopen or fail the completed Evaluation, alter its acceptance or rejection classification, or become protocol rejection. | PE-G3-SOURCE-S25, PE-G3-SOURCE-S27, PE-G3-SOURCE-S32, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-fail-020"></a> PE-G3-FAIL-020 | MUST | applicable | Every operational success or failure classification | Operational success or failure MUST remain distinct from Determination production and from formal Evaluation success or failure. | PE-G3-SOURCE-S25, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-tsefail-001"></a> PE-G3-TSEFAIL-001 | MUST | applicable | ALWAYS | An unavailable, invalid, unauthenticated, incomplete or unevaluable required input MUST be classified UNRESOLVED rather than FALSE. | PE-G3-SOURCE-S37 | NONE |
| <a id="pe-g3-tsefail-002-a01"></a> PE-G3-TSEFAIL-002-A01 | MUST | applicable | ALWAYS | An authoritatively evaluated false condition MUST remain FALSE. | PE-G3-SOURCE-S37 | NONE |
| <a id="pe-g3-tsefail-002-a02"></a> PE-G3-TSEFAIL-002-A02 | MUST | applicable | ALWAYS | An authoritatively evaluated false condition MUST be processed by the profile's materiality definition. | PE-G3-SOURCE-S37 | NONE |
| <a id="pe-g3-tsefail-003"></a> PE-G3-TSEFAIL-003 | MUST | applicable | ALWAYS | An independently sufficient authenticated material-conflict witness MUST yield material-conflict despite an unrelated unresolved input. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tsefail-004"></a> PE-G3-TSEFAIL-004 | MUST | applicable | ALWAYS | Without an established sufficient conflict, any unresolved input required for equivalence or conflict exclusion MUST yield indeterminate. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tsefail-005"></a> PE-G3-TSEFAIL-005 | MUST | applicable | ALWAYS | Complete valid inputs producing neither equivalence nor conflict, or both, MUST yield indeterminate and invalidate the profile or evaluation. | PE-G3-SOURCE-S70, PE-G3-SOURCE-S72 | NONE |

<a id="pe-g3-rf-35"></a>
### RF-35 — Stale authorization and re-evaluation

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-staleauth-001"></a> PE-G3-STALEAUTH-001 | MUST | applicable | Every transition authorization bounded to one pre-transition protocol state | The authorization MUST remain explicitly bounded to the identified `Q0`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-staleauth-002"></a> PE-G3-STALEAUTH-002 | MUST | applicable | ALWAYS | Every authorized U MUST execute the PE-TSE-COMPARISON-V2 procedure immediately before execution and again at semantic commitment, using authenticated authorization bindings and authoritative current protocol state. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-staleauth-003-a01"></a> PE-G3-STALEAUTH-003-A01 | MUST | conditional | When comparison returns equivalent, | When comparison returns equivalent, the equivalence determination MUST remain bounded to U and its governing profile. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-staleauth-003-a02"></a> PE-G3-STALEAUTH-003-A02 | MUST | conditional | When comparison returns equivalent, | When comparison returns equivalent, the equivalence determination MUST preserve D and the authorization unchanged. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-staleauth-003-a03"></a> PE-G3-STALEAUTH-003-A03 | MUST | conditional | When comparison returns equivalent, | When comparison returns equivalent, the equivalence determination MUST authorize only the next gate for that U. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-staleauth-004-a01"></a> PE-G3-STALEAUTH-004-A01 | MUST | conditional | When pre-execution comparison returns material-conflict, | When pre-execution comparison returns material-conflict, U MUST terminate with pre-transition failure. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-staleauth-004-a02"></a> PE-G3-STALEAUTH-004-A02 | MUST | conditional | When pre-execution comparison returns material-conflict, | When pre-execution comparison returns material-conflict, U's authorization MUST become terminally stale for U. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-staleauth-004-a03"></a> PE-G3-STALEAUTH-004-A03 | MUST | conditional | When pre-execution comparison returns material-conflict, | When pre-execution comparison returns material-conflict, execution and commitment MUST be prohibited. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-staleauth-004-a04"></a> PE-G3-STALEAUTH-004-A04 | MUST | conditional | When pre-execution comparison returns material-conflict, | When pre-execution comparison returns material-conflict, recovery MUST require a new U under the total disposition function. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-staleauth-005"></a> PE-G3-STALEAUTH-005 | MUST NOT | applicable | Every stale transition authorization | A stale authorization MUST NOT permit commitment against the materially conflicting state. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-staleauth-006"></a> PE-G3-STALEAUTH-006 | MUST NOT | applicable | Every implementation resolving applicable-state conflict | The implementation MUST NOT select whichever state context produces a preferred result or repair the existing authorization. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-staleauth-007"></a> PE-G3-STALEAUTH-007 | MUST NOT | applicable | Every stale transition authorization | Staleness MUST NOT mutate, invalidate, rewrite, or reclassify the earlier Evaluation or Determination. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-staleauth-008"></a> PE-G3-STALEAUTH-008 | MUST | applicable | Every materially changed context or state for which the applicable protocol rules require re-evaluation | The implementation MUST begin one new Protocol Action Evaluation occurrence under the newly applicable bounded context. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-staleauth-009"></a> PE-G3-STALEAUTH-009 | MUST | applicable | Every completed required re-evaluation | The new Evaluation MUST produce one new Determination and, where applicable, newly authorized transition occurrences whose identities are distinct from every earlier transition occurrence. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-staleauth-010"></a> PE-G3-STALEAUTH-010 | MUST NOT | applicable | Every required re-evaluation | Re-evaluation MUST NOT mutate, repair, replace, or silently reinterpret the earlier `E`, `D`, or `U`. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-staleauth-011"></a> PE-G3-STALEAUTH-011 | MUST NOT | applicable | Every stale-authorization and re-evaluation identifier, record, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | A staleness or re-evaluation surface MUST NOT identify the Private Actor, introduce reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | STATE |
| <a id="pe-g3-staleauth-012"></a> PE-G3-STALEAUTH-012 | MUST NOT | applicable | Every stale-authorization condition and representation | Stale authorization MUST NOT be represented as a separately identified first-class stale-authorization object. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-staleauth-013"></a> PE-G3-STALEAUTH-013 | MUST | applicable | Every retry of later Determination representation, publication, transport or delivery | Retry of a later representation, publication, transport or delivery operation MUST preserve the same already-produced Determination and MUST NOT produce another Determination or another Evaluation occurrence. | PE-G3-SOURCE-S25, PE-G3-SOURCE-S27, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-staleauth-014"></a> PE-G3-STALEAUTH-014 | MUST NOT | applicable | Every terminally failed Protocol Action Evaluation | A terminally failed Evaluation MUST NOT later become complete. | PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-staleauth-015"></a> PE-G3-STALEAUTH-015 | MUST | applicable | Every later authoritative re-evaluation after terminal Evaluation failure | Any later authoritative re-evaluation MUST instantiate a new Evaluation occurrence and MUST preserve the failed occurrence without mutation, repair or reinterpretation. | PE-G3-SOURCE-S25, PE-G3-SOURCE-S27 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-tserecov-001-a01"></a> PE-G3-TSERECOV-001-A01 | MUST | applicable | ALWAYS | Dep(D) MUST be the validated least transitive closure defined by S70. | PE-G3-SOURCE-S70, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-tserecov-001-a02"></a> PE-G3-TSERECOV-001-A02 | MUST | applicable | ALWAYS | Dep(D) MUST include every input capable of affecting D. | PE-G3-SOURCE-S70, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-tserecov-002"></a> PE-G3-TSERECOV-002 | MUST | applicable | ALWAYS | Unchanged D MUST be sufficient only when its complete dependency closure remains authoritative, valid, authenticated and semantically unchanged. | PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-tserecov-003"></a> PE-G3-TSERECOV-003 | MUST | applicable | ALWAYS | Every changed or unavailable component MUST be outside Dep(D) before recovery may reuse unchanged D. | PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-tserecov-004"></a> PE-G3-TSERECOV-004 | MUST | applicable | ALWAYS | The stage-partitioned disposition function in S72 MUST select exactly one recovery for every non-success event. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tserecov-005"></a> PE-G3-TSERECOV-005 | MUST | applicable | ALWAYS | Pre-execution material conflict MUST terminally fail U, terminally stale its authorization and require a new U. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tserecov-006"></a> PE-G3-TSERECOV-006 | MUST | conditional | When unchanged D is insufficient or cannot be established, | When unchanged D is insufficient or cannot be established, recovery MUST require new E, successfully produced new D, new authorization and new U. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tserecov-007"></a> PE-G3-TSERECOV-007 | MUST | applicable | ALWAYS | Every predecessor occurrence, authorization, attempt, result and failure classification MUST remain immutable through recovery. | PE-G3-SOURCE-S72 | NONE |

<a id="pe-g3-sf-12"></a>
## SF-12 — Application, Adapter, Runtime, and Integration Boundaries

<a id="pe-g3-rf-14"></a>
### RF-14 — Application requests, responses, and adapters

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-apprep-001"></a> PE-G3-APPREP-001 | MUST | applicable | Every Application Request | An Application Request MUST remain a bounded application-owned representation presented for possible translation at one identified application boundary. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S41, PE-G3-SOURCE-S43 | NONE |
| <a id="pe-g3-apprep-002"></a> PE-G3-APPREP-002 | MUST | applicable | Every identified Application Request | The request identity and scope MUST identify the request representation without identifying a Private Actor or becoming a reusable cross-action identifier. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S41 | STATE |
| <a id="pe-g3-apprep-003"></a> PE-G3-APPREP-003 | MUST NOT | applicable | Every Application Request | An Application Request MUST NOT be interpreted merely by its existence as a Protocol Operation, Protocol Action, proof, declared public input, Evaluation, Determination, Protocol State Transition, protocol state, or protocol truth. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S23, PE-G3-SOURCE-S24, PE-G3-SOURCE-S41 | NONE |
| <a id="pe-g3-apprep-004"></a> PE-G3-APPREP-004 | MUST | applicable | Every application-owned request value | Each request value MUST remain application-owned until a valid adapter translation establishes its applicable protocol-facing representation under the governing Interface Contract. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S30, PE-G3-SOURCE-S31, PE-G3-SOURCE-S41 | NONE |
| <a id="pe-g3-apprep-005"></a> PE-G3-APPREP-005 | MUST | applicable | Every Application Adapter | An Application Adapter MUST remain a bounded translation boundary between application-owned representation and the applicable protocol-facing interface representation. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S40 | NONE |
| <a id="pe-g3-apprep-006"></a> PE-G3-APPREP-006 | MUST | applicable | Every identified Application Adapter | Adapter identity and scope MUST remain distinct from the application, runtime, implementation, Interface Contract, Concrete Interface Specification, Protocol Operation, Protocol Action, and Private Actor. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S29, PE-G3-SOURCE-S40 | NONE |
| <a id="pe-g3-apprep-007"></a> PE-G3-APPREP-007 | MUST | applicable | Every adapter translation | Translation MUST be governed by the applicable Interface Contract and Concrete Interface Specification and MUST map only representations supported by that boundary. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S30, PE-G3-SOURCE-S31, PE-G3-SOURCE-S40 | NONE |
| <a id="pe-g3-apprep-008"></a> PE-G3-APPREP-008 | MUST | applicable | Every successful adapter translation | A successful translation MUST preserve the complete bounded meaning, identity distinctions, ordering requirements, applicability conditions, and failure semantics of its source representation. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S30, PE-G3-SOURCE-S40, PE-G3-SOURCE-S41, PE-G3-SOURCE-S42 | NONE |
| <a id="pe-g3-apprep-009"></a> PE-G3-APPREP-009 | MUST | applicable | Every adapter unable to preserve applicable meaning | The adapter MUST return bounded translation failure when it cannot preserve the applicable meaning or required representation. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S40, PE-G3-SOURCE-S43 | NONE |
| <a id="pe-g3-apprep-010"></a> PE-G3-APPREP-010 | MUST NOT | applicable | Every adapter translation | Translation MUST NOT repair, infer, widen, narrow, merge, divide, substitute, or invent protocol meaning, protocol subjects, protocol values, or protocol outcomes. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S29, PE-G3-SOURCE-S40, PE-G3-SOURCE-S43 | NONE |
| <a id="pe-g3-apprep-011"></a> PE-G3-APPREP-011 | MUST | applicable | Every Application Response | An Application Response MUST remain a bounded application-owned representation derived from one applicable protocol-defined output exposed through the governing interface. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S32, PE-G3-SOURCE-S42 | NONE |
| <a id="pe-g3-apprep-012"></a> PE-G3-APPREP-012 | MUST | applicable | Every identified Application Response | Response identity and scope MUST identify the response representation without changing the identity of its source output or identifying a Private Actor. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S32, PE-G3-SOURCE-S42 | STATE |
| <a id="pe-g3-apprep-013"></a> PE-G3-APPREP-013 | MUST NOT | applicable | Every Application Response | An Application Response MUST NOT be identified with or substituted for its source Published Result, public protocol-state consequence, Determination, protocol state, or application interpretation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S32, PE-G3-SOURCE-S42 | NONE |
| <a id="pe-g3-apprep-014"></a> PE-G3-APPREP-014 | MUST | applicable | Every Application Response derived through translation | The response MUST preserve the complete bounded meaning and failure status of its source protocol-defined output while remaining application-owned representation. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S32, PE-G3-SOURCE-S40, PE-G3-SOURCE-S42 | NONE |
| <a id="pe-g3-apprep-015"></a> PE-G3-APPREP-015 | MUST NOT | applicable | Every Application Request, adapter output, and Application Response | Application-facing representation MUST NOT convert protocol output into factual, legal, social, institutional, or application truth or into evidence of user intent or Private Actor identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S29, PE-G3-SOURCE-S41, PE-G3-SOURCE-S42 | STATE |
| <a id="pe-g3-apprep-016"></a> PE-G3-APPREP-016 | MUST | applicable | Every request, adapter, response, field, serialization, example, and diagnostic surface | Application-facing representation and translation surfaces MUST preserve SF-03 and SF-04 terminology, identity separation, privacy, unlinkability, minimum-disclosure, and neutral-naming requirements. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S29, PE-G3-SOURCE-S40, PE-G3-SOURCE-S41, PE-G3-SOURCE-S42 | STATE |

<a id="pe-g3-rf-36"></a>
### RF-36 — Application and adapter authority boundaries

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-appauth-001"></a> PE-G3-APPAUTH-001 | MAY | applicable | Every application | An application MAY define application-local representation, terminology, policy, validation, presentation, persistence, and interpretation within its declared application-owned scope. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S40, PE-G3-SOURCE-S41, PE-G3-SOURCE-S42, PE-G3-SOURCE-S43 | NONE |
| <a id="pe-g3-appauth-002"></a> PE-G3-APPAUTH-002 | MUST NOT | applicable | Every application policy or interpretation | Application policy or interpretation MUST NOT alter protocol validity, applicable protocol obligations, proof meaning, public-input meaning, Evaluation, Determination, transition semantics, commitment, protocol state, compatibility, conformance, or certification. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S21, PE-G3-SOURCE-S29, PE-G3-SOURCE-S43 | NONE |
| <a id="pe-g3-appauth-003"></a> PE-G3-APPAUTH-003 | MUST NOT | applicable | Every application and Application Request or Response | An application or its representations MUST NOT acquire protocol authority or represent application-owned meaning as protocol-defined meaning. | PE-G3-SOURCE-S21, PE-G3-SOURCE-S29, PE-G3-SOURCE-S41, PE-G3-SOURCE-S42 | NONE |
| <a id="pe-g3-appauth-004"></a> PE-G3-APPAUTH-004 | MUST | applicable | Every Application Adapter | An adapter MUST exercise responsibility only for bounded representation handling and translation within its governing interface boundary. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S40 | NONE |
| <a id="pe-g3-appauth-005"></a> PE-G3-APPAUTH-005 | MUST NOT | applicable | Every Application Adapter | An adapter MUST NOT redefine Interface Contract meaning, Protocol Surface meaning, Protocol Operation meaning, Protocol Action identity, proof or public-input meaning, Evaluation, Determination, transition, commitment, state, Published Result, public consequence, validity, privacy, compatibility, conformance, or certification. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S22, PE-G3-SOURCE-S29, PE-G3-SOURCE-S40 | NONE |
| <a id="pe-g3-appauth-006"></a> PE-G3-APPAUTH-006 | MUST | applicable | Every integrator | An integrator MUST preserve every applicable upstream semantic subject, requirement, identity distinction, ordering rule, failure rule, privacy boundary, and authority boundary across the connected application, adapter, runtime, and implementation surfaces. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S29, PE-G3-SOURCE-S44 | NONE |
| <a id="pe-g3-appauth-007"></a> PE-G3-APPAUTH-007 | MUST NOT | applicable | Every integration | Integration MUST NOT authorize semantic repair, inference, substitution, correlation, authority transfer, or the creation of an application-specific alternative protocol path. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S44 | NONE |
| <a id="pe-g3-appauth-008"></a> PE-G3-APPAUTH-008 | MUST | applicable | Every adapter replacement or application-boundary change | The replacement or change MUST preserve every applicable published interface meaning and MUST fail compatibility where that meaning cannot be preserved. | PE-G3-SOURCE-S22, PE-G3-SOURCE-S29, PE-G3-SOURCE-S40, PE-G3-SOURCE-S44 | NONE |
| <a id="pe-g3-appauth-009"></a> PE-G3-APPAUTH-009 | MUST NOT | applicable | Every application-side validation or default | Application validation, defaults, convenience abstractions, or preferred outcomes MUST NOT be treated as protocol validation, protocol defaults, protocol rules, or protocol outcomes. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S40, PE-G3-SOURCE-S41 | NONE |
| <a id="pe-g3-appauth-010"></a> PE-G3-APPAUTH-010 | MUST | applicable | Every application, adapter, and integration failure | Failure MUST be reported within its bounded layer and MUST preserve the distinction between representation failure, runtime failure, implementation failure, and protocol-defined failure. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S43, PE-G3-SOURCE-S44 | NONE |
| <a id="pe-g3-appauth-011"></a> PE-G3-APPAUTH-011 | MUST NOT | applicable | Every application, adapter, integration record, or observability surface | The surface MUST NOT identify a Private Actor, carry enrollment or admission provenance, create reusable participant identity, create cross-action linkage, or compose metadata into an actor-reconstruction bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S44 | STATE |
| <a id="pe-g3-appauth-012"></a> PE-G3-APPAUTH-012 | MUST | applicable | Every public application, adapter, or integration identifier | The identifier MUST remain bounded to its declared non-actor subject without being interpreted as protocol identity, Protocol Action identity, or Private Actor identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S44 | STATE |
| <a id="pe-g3-tseapp-001-a01"></a> PE-G3-TSEAPP-001-A01 | MAY | applicable | ALWAYS | An application response MAY translate the authoritative bounded result. | PE-G3-SOURCE-S42 | NONE |
| <a id="pe-g3-tseapp-001-a02"></a> PE-G3-TSEAPP-001-A02 | MUST NOT | applicable | ALWAYS | An application response MUST NOT create, change or reinterpret the authoritative bounded result. | PE-G3-SOURCE-S42 | NONE |
| <a id="pe-g3-tseapp-002"></a> PE-G3-TSEAPP-002 | MUST NOT | applicable | ALWAYS | An application surface MUST NOT receive or expose confidential blinds, openings or raw protected components. | PE-G3-SOURCE-S42, PE-G3-SOURCE-S43 | NONE |

<a id="pe-g3-rf-37"></a>
### RF-37 — Runtime, enforcement, and execution responsibility

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-runtime-001"></a> PE-G3-RUNTIME-001 | MUST | applicable | Every Privacy Engine runtime | A runtime MUST remain an identified operational context through which one or more identified implementations perform bounded protocol-facing work. | PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-runtime-002"></a> PE-G3-RUNTIME-002 | MUST | applicable | Every identified runtime | Runtime identity and scope MUST remain distinct from application identity, adapter identity, implementation identity, deployment identity, protocol identity, Protocol Action identity, and Private Actor identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | STATE |
| <a id="pe-g3-runtime-003"></a> PE-G3-RUNTIME-003 | MUST NOT | applicable | Every runtime | A runtime MUST NOT interpret application-local meaning as protocol meaning or assume application ownership merely because it receives application-facing material. | PE-G3-SOURCE-S21, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-runtime-004"></a> PE-G3-RUNTIME-004 | MUST | applicable | Every runtime using an implementation | The runtime MUST preserve the identity and declared scope of each implementation through which it realizes protocol-facing work. | PE-G3-SOURCE-S43, PE-G3-SOURCE-S45, PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-runtime-005"></a> PE-G3-RUNTIME-005 | MAY | applicable | Every runtime | A runtime MAY receive applicable inputs, invoke validation and enforcement, invoke Evaluation, invoke authorized execution, expose applicable results, and report bounded failure where those responsibilities are assigned by the applicable implementation profile. | PE-G3-SOURCE-S33, PE-G3-SOURCE-S34, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-runtime-006"></a> PE-G3-RUNTIME-006 | MUST NOT | applicable | Every runtime orchestration path | Runtime orchestration order, component topology, retry behavior, transport, storage, or deployment mechanics MUST NOT redefine the semantic identity or ordering requirements of Protocol Actions, Evaluations, Determinations, transitions, commitment, state, history, or consequences. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S27, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-runtime-007"></a> PE-G3-RUNTIME-007 | MUST | applicable | Every Protocol Enforcement occurrence | Enforcement MUST evaluate only the applicable published transition preconditions and MUST contribute its bounded eligibility result to the complete applicable Protocol Action Evaluation where required. | PE-G3-SOURCE-S25, PE-G3-SOURCE-S27, PE-G3-SOURCE-S33 | NONE |
| <a id="pe-g3-runtime-008"></a> PE-G3-RUNTIME-008 | MUST NOT | applicable | Every Protocol Enforcement occurrence | Enforcement MUST NOT be interpreted as the complete Protocol Action Evaluation or as an independent Protocol Action Determination. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25, PE-G3-SOURCE-S33 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-runtime-009"></a> PE-G3-RUNTIME-009 | MUST NOT | applicable | Every Protocol Enforcement occurrence | Enforcement MUST NOT execute a transition, commit state, construct authoritative successor state, publish a result, or select an alternative transition. | PE-G3-SOURCE-S27, PE-G3-SOURCE-S33, PE-G3-SOURCE-S34 | NONE |
| <a id="pe-g3-runtime-010"></a> PE-G3-RUNTIME-010 | MUST | applicable | Every authorized transition execution | Execution MUST preserve the already-authorized Protocol State Transition occurrence and realize only its published transition mapping. | PE-G3-SOURCE-S27, PE-G3-SOURCE-S34 | NONE |
| <a id="pe-g3-runtime-011"></a> PE-G3-RUNTIME-011 | MUST NOT | applicable | Every transition execution | Execution MUST NOT perform enforcement, substitute another transition occurrence, or treat derived successor-state material as committed authoritative state. | PE-G3-SOURCE-S27, PE-G3-SOURCE-S33, PE-G3-SOURCE-S34, PE-G3-SOURCE-S35 | NONE |
| <a id="pe-g3-runtime-012"></a> PE-G3-RUNTIME-012 | MUST NOT | applicable | Every successful execution | Successful execution MUST NOT be interpreted as commitment until the complete SF-10 commitment requirements have been satisfied. | PE-G3-SOURCE-S27, PE-G3-SOURCE-S34, PE-G3-SOURCE-S35 | NONE |
| <a id="pe-g3-runtime-013"></a> PE-G3-RUNTIME-013 | MUST | applicable | Every runtime result or failure report | Runtime reporting MUST preserve the source result, lifecycle stage, success or failure classification, and applicable identity distinctions without inventing protocol truth. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S32, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-runtime-014"></a> PE-G3-RUNTIME-014 | MUST NOT | applicable | Every runtime or implementation failure | A runtime or implementation failure MUST NOT mutate an earlier Protocol Action, Evaluation, Determination, authorization, transition occurrence, commitment status, or protocol-state history. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-runtime-015"></a> PE-G3-RUNTIME-015 | MUST | applicable | Every runtime value, log, diagnostic, retry, timing, ordering, topology, and observability surface | The surface MUST preserve SF-04 privacy without exposing or composing runtime metadata as Private Actor identity or cross-action linkage. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | STATE |
| <a id="pe-g3-runtime-016"></a> PE-G3-RUNTIME-016 | MUST NOT | applicable | Every runtime, enforcement mechanism, execution mechanism, and orchestrator | Operational responsibility MUST NOT be interpreted as ownership of protocol semantics or as protocol authority. | PE-G3-SOURCE-S21, PE-G3-SOURCE-S33, PE-G3-SOURCE-S34, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-runtime-017"></a> PE-G3-RUNTIME-017 | MUST | applicable | Every operational failure after a Determination exists | Operational failure after a Determination exists MUST be classified at the actual later lifecycle layer. | PE-G3-SOURCE-S25, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-tseruntime-001-a01"></a> PE-G3-TSERUNTIME-001-A01 | MUST | applicable | ALWAYS | A runtime MUST implement the published profile and gate exactly. | PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-tseruntime-001-a02"></a> PE-G3-TSERUNTIME-001-A02 | MUST NOT | applicable | ALWAYS | A runtime MUST NOT choose predicates, defaults, materiality or recovery. | PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-tseruntime-002"></a> PE-G3-TSERUNTIME-002 | MUST | applicable | ALWAYS | A runtime comparison boundary handling openings MUST authenticate inputs, minimize disclosure and erase non-required opening material after the bounded comparison. | PE-G3-SOURCE-S43 | NONE |
| <a id="pe-g3-tseruntime-003-a01"></a> PE-G3-TSERUNTIME-003-A01 | MUST | applicable | ALWAYS | Operational failure MUST be classified at its actual lifecycle layer. | PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-tseruntime-003-a02"></a> PE-G3-TSERUNTIME-003-A02 | MUST NOT | applicable | ALWAYS | Operational failure MUST NOT become protocol rejection, material conflict or equivalence. | PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-tseruntime-004-a01"></a> PE-G3-TSERUNTIME-004-A01 | MUST | applicable | ALWAYS | Runtime retry MUST preserve immutable history. | PE-G3-SOURCE-S47, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseruntime-004-a02"></a> PE-G3-TSERUNTIME-004-A02 | MUST | applicable | ALWAYS | Runtime retry MUST instantiate new occurrences exactly where the disposition function requires them. | PE-G3-SOURCE-S47, PE-G3-SOURCE-S72 | NONE |

<a id="pe-g3-sf-13"></a>
## SF-13 — Implementation, Realization, Compatibility, and Migration

<a id="pe-g3-rf-38"></a>
### RF-38 — Implementation identity and implementation obligations

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-impl-001"></a> PE-G3-IMPL-001 | MUST | applicable | Every Privacy Engine implementation | An implementation MUST be one identified technical realization of the applicable normative requirements selected by its applicable implementation profile or profiles. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S45, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-impl-002"></a> PE-G3-IMPL-002 | MUST | applicable | Every implementation | Implementation identity MUST be stable and sufficient to distinguish the implementation from other implementations and materially different implementation versions. | PE-G3-SOURCE-S45 | NONE |
| <a id="pe-g3-impl-003"></a> PE-G3-IMPL-003 | MUST | applicable | Every implementation | The implementation MUST declare a bounded realization scope identifying the roles, capabilities, interfaces, protocol generation, Protocol Specification, and implementation profiles it claims to realize. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-impl-004"></a> PE-G3-IMPL-004 | MUST | applicable | Every materially changed implementation version | A materially changed version MUST remain separately identifiable where the change affects applicable obligations, externally observable normative behavior, compatibility, or assessment. | PE-G3-SOURCE-S15, PE-G3-SOURCE-S45 | NONE |
| <a id="pe-g3-impl-005"></a> PE-G3-IMPL-005 | MAY | applicable | Every implementation | An implementation MAY use multiple components, algorithms, languages, processes, services, storage structures, transports, and deployment mechanisms where every applicable requirement permits that variation. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-impl-006"></a> PE-G3-IMPL-006 | MUST | applicable | Every component used by an implementation | Component identity, responsibility, and failure MUST remain attributable to the implementation scope without becoming independent protocol identity or protocol authority. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45 | NONE |
| <a id="pe-g3-impl-007"></a> PE-G3-IMPL-007 | MUST | applicable | Every implementation deployment or operational instance | Deployment and instance identity MUST remain distinct from implementation identity, implementation-version identity, profile identity, protocol identity, and Private Actor identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S43, PE-G3-SOURCE-S45 | STATE |
| <a id="pe-g3-impl-008"></a> PE-G3-IMPL-008 | MUST NOT | applicable | Every implementation identifier | An implementation identifier MUST NOT be interpreted as a protocol-generation identifier, Protocol Specification identifier, implementation-profile identifier, reference designation, conformance identity, certification identity, Protocol Action identity, or Private Actor identity. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S18, PE-G3-SOURCE-S45, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | STATE |
| <a id="pe-g3-impl-009"></a> PE-G3-IMPL-009 | MUST | applicable | Every implementation | The implementation MUST satisfy every normative requirement applicable through its identified profile, including applicable success, rejection, failure, privacy, observability, and authority requirements. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S06, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-impl-010"></a> PE-G3-IMPL-010 | MUST | applicable | Every implementation claiming a requirement is non-applicable | The claim MUST derive from the requirement's published applicability rule and the applicable profile scope rather than implementation preference or existing behavior. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05, PE-G3-SOURCE-S45, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-impl-011"></a> PE-G3-IMPL-011 | MAY | applicable | Every implementation-facing choice explicitly permitted by the applicable profile | The implementation MAY select a choice only within the complete bounded choice space permitted by the Protocol Specification and resolved or retained by the applicable profile. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-impl-012"></a> PE-G3-IMPL-012 | MUST NOT | applicable | Every implementation | Implementation convenience, cost, infrastructure limitation, preferred result, deployment topology, storage model, transport model, local policy, or existing behavior MUST NOT become protocol discretion or an exception to an applicable requirement. | PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45 | NONE |
| <a id="pe-g3-impl-013"></a> PE-G3-IMPL-013 | MAY | applicable | Multiple implementations of the same applicable profile | Implementations MAY differ technically where every difference remains within permitted implementation choice and preserves equivalent protocol-observable semantics. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-impl-014"></a> PE-G3-IMPL-014 | MUST | applicable | Every permitted implementation variation | The variation MUST preserve every applicable requirement, semantic subject, identity distinction, ordering rule, failure behavior, privacy guarantee, and observable protocol outcome. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-impl-015"></a> PE-G3-IMPL-015 | MUST | applicable | Every implementation failure | Failure MUST remain explicit, bounded to the failed realization responsibility, and distinguishable from protocol invalidity and from alteration of the governing requirement. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45 | NONE |
| <a id="pe-g3-impl-016"></a> PE-G3-IMPL-016 | MUST NOT | applicable | Every implementation name, identifier, version, component, deployment, instance, log, diagnostic, test, and observability surface | The surface MUST NOT identify a Private Actor, create reusable participant identity, create cross-action linkage, or compose implementation metadata into an actor-reconstruction bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45 | STATE |

<a id="pe-g3-rf-39"></a>
### RF-39 — Protocol realization

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-realize-001"></a> PE-G3-REALIZE-001 | MUST | applicable | Every claimed Protocol Realization | The realization MUST identify one implementation, one applicable Protocol Specification and published protocol generation, the applicable implementation profile or profiles, and one bounded realization scope. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-realize-002"></a> PE-G3-REALIZE-002 | MUST | applicable | Every Protocol Realization relationship | The relationship MUST remain a bounded preservation relation between its identified implementation and upstream semantic target rather than a new source of protocol semantics or protocol identity. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S12, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-realize-003"></a> PE-G3-REALIZE-003 | MUST | applicable | Every implementation realizing an applicable requirement | The implementation MUST preserve the complete meaning, strength, applicability, identity distinctions, conditions, success behavior, and failure behavior of that requirement. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S06, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-realize-004"></a> PE-G3-REALIZE-004 | MUST | applicable | Every successful realization of an upstream semantic subject | Every later realization layer MUST preserve the same selected subject `T` throughout the declared scope. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-realize-005"></a> PE-G3-REALIZE-005 | MUST | applicable | Every realization unable to preserve an applicable subject or requirement | The realization MUST fail explicitly rather than claim successful realization. | PE-G3-SOURCE-S44, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-realize-006"></a> PE-G3-REALIZE-006 | MUST NOT | applicable | Every Protocol Realization | A realization MUST NOT repair, reinterpret, widen, narrow, merge, divide, substitute, infer, or invent replacement protocol meaning `T'` for the applicable meaning `T`. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S44, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-realize-007"></a> PE-G3-REALIZE-007 | MUST NOT | applicable | Every Protocol Realization | A realization MUST NOT omit an applicable mandatory requirement or treat a prohibited behavior as a permitted technical choice. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S06, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-realize-008"></a> PE-G3-REALIZE-008 | MUST | applicable | Every complete realization claim | The claim MUST account for every requirement applicable within its declared scope and for every declared dependency of the applicable profile. | PE-G3-SOURCE-S06, PE-G3-SOURCE-S08, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-realize-009"></a> PE-G3-REALIZE-009 | MAY | applicable | Multiple realizations of the same applicable profile | Multiple realizations MAY use different internal and operational means where each independently preserves the same required protocol-observable semantics. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-realize-010"></a> PE-G3-REALIZE-010 | MUST | applicable | Every realization-specific extension | The extension MUST remain outside protocol semantics without conflicting with, weakening, obscuring, or expanding any applicable protocol obligation. | PE-G3-SOURCE-S21, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-realize-011"></a> PE-G3-REALIZE-011 | MUST | applicable | Every realization record, report, or diagnostic | The surface MUST remain bounded to realization status and MUST preserve SF-04 privacy, neutral naming, and non-correlation requirements. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S44, PE-G3-SOURCE-S46 | STATE |
| <a id="pe-g3-realize-012"></a> PE-G3-REALIZE-012 | MUST NOT | applicable | Every implementation and realization | Realizing protocol semantics MUST NOT be interpreted as defining the protocol generation, Protocol Specification, implementation profile, conformance, certification, or protocol authority. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S12, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S55 | NONE |

<a id="pe-g3-rf-40"></a>
### RF-40 — Prohibited implementation, runtime, application, and assessment authority

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-downauth-001"></a> PE-G3-DOWNAUTH-001 | MUST NOT | applicable | Every application, adapter, runtime, integration, implementation, realization, compatibility structure, profile, reference implementation, assessment, report, deployment, and operational surface | A downstream structure or surface MUST NOT acquire or claim protocol authority. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S12, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S43, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-downauth-002"></a> PE-G3-DOWNAUTH-002 | MUST NOT | applicable | Every downstream structure or surface | It MUST NOT redefine, replace, amend, supersede, or mutate the identity, membership, publication state, lineage, lifecycle, semantics, or authority of a published protocol generation or Protocol Specification. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S12, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21 | NONE |
| <a id="pe-g3-downauth-003"></a> PE-G3-DOWNAUTH-003 | MUST NOT | applicable | Every downstream structure or surface | It MUST NOT redefine privacy, anonymity, unlinkability, minimum disclosure, actor separation, reusable-identity prohibitions, or compositional-correlation prohibitions. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21, PE-G3-SOURCE-S44 | STATE |
| <a id="pe-g3-downauth-004"></a> PE-G3-DOWNAUTH-004 | MUST NOT | applicable | Every downstream structure or surface | It MUST NOT redefine proof relations, declared public inputs, verification semantics, evidence meaning, or complete protocol validity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S21 | NONE |
| <a id="pe-g3-downauth-005"></a> PE-G3-DOWNAUTH-005 | MUST NOT | applicable | Every downstream structure or surface | It MUST NOT redefine Protocol Operation, Protocol Action, applicable-rule, Evaluation, Determination, acceptance, rejection, or accepted no-transition semantics. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S21, PE-G3-SOURCE-S43, PE-G3-SOURCE-S45 | NONE |
| <a id="pe-g3-downauth-006"></a> PE-G3-DOWNAUTH-006 | MUST NOT | applicable | Every downstream structure or surface | It MUST NOT redefine transition mapping, transition-occurrence identity, authorization, execution, commitment, state, history, consequence, failure, staleness, or re-evaluation semantics. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S35, PE-G3-SOURCE-S43, PE-G3-SOURCE-S45 | NONE |
| <a id="pe-g3-downauth-007"></a> PE-G3-DOWNAUTH-007 | MUST NOT | applicable | Every compatibility, profile, reference, conformance, or certification structure | It MUST NOT redefine compatibility truth, profile obligations, conformance, certification, or the upstream semantic basis against which those downstream relationships are evaluated. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S18, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S48, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-downauth-008"></a> PE-G3-DOWNAUTH-008 | MUST NOT | applicable | Every implementation behavior, compatibility declaration, assessment result, diagnostic, test result, deployment record, report, or observability surface | The surface MUST NOT be promoted into protocol truth or used to repair, infer, or replace upstream protocol meaning. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S48 | NONE |
| <a id="pe-g3-downauth-009"></a> PE-G3-DOWNAUTH-009 | MUST | applicable | Every conflict between a downstream artifact and its governing upstream requirement | The conflict MUST be resolved in favor of the governing upstream requirement, and the downstream artifact MUST be corrected, narrowed, withdrawn, superseded, or reported as failed. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S12, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-downauth-010"></a> PE-G3-DOWNAUTH-010 | MUST | applicable | Every downstream derivation and realization path | The path MUST preserve the direction `Published Protocol Generation -> Protocol Specification -> Implementation Profile -> Implementation -> Conformance -> Certification` without upward authority transfer. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S18, PE-G3-SOURCE-S45, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-tsenonauth-001"></a> PE-G3-TSENONAUTH-001 | MUST | applicable | ALWAYS | No implementation, runtime, adapter, application, database, diagnostic or observability mechanism MUST acquire authority to define or override transition-state equivalence. | PE-G3-SOURCE-S30, PE-G3-SOURCE-S47, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tsenonauth-002"></a> PE-G3-TSENONAUTH-002 | MUST NOT | applicable | ALWAYS | Protocol-semantic atomicity MUST NOT be inferred from implementation transaction, storage, consensus, lock, event or rollback behaviour. | PE-G3-SOURCE-S36, PE-G3-SOURCE-S72 | NONE |

<a id="pe-g3-rf-41"></a>
### RF-41 — Compatibility targets, surfaces, statements, profiles, declarations, and assessment

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-compat-001"></a> PE-G3-COMPAT-001 | MUST | applicable | Every compatibility relationship | The relationship MUST identify one implementation, one implementation version where relevant, one compatibility target, one compatibility surface, and one bounded compatibility scope. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S48, PE-G3-SOURCE-S50, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-002"></a> PE-G3-COMPAT-002 | MUST | applicable | Every Compatibility Target | A Compatibility Target MUST identify exactly one published protocol generation used as the reference for the bounded compatibility relationship. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S12, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-003"></a> PE-G3-COMPAT-003 | MUST | applicable | Every identified Compatibility Target | Target identity MUST remain distinct from the identity of the referenced protocol generation, implementation, deployment, surface, statement, profile, declaration, assessment, conformance object, and certification object. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-004"></a> PE-G3-COMPAT-004 | MUST | applicable | Every Compatibility Surface | A Compatibility Surface MUST identify the bounded set of published capabilities from one identified compatibility target that is covered by the compatibility statement or assessment. | PE-G3-SOURCE-S22, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-005"></a> PE-G3-COMPAT-005 | MUST | applicable | Every Compatibility Surface | The surface MUST be complete within its declared scope and MUST explicitly identify every included capability and every permitted exclusion. | PE-G3-SOURCE-S22, PE-G3-SOURCE-S48, PE-G3-SOURCE-S53 | NONE |
| <a id="pe-g3-compat-006"></a> PE-G3-COMPAT-006 | MUST NOT | applicable | Every Compatibility Surface | A Compatibility Surface MUST NOT be identified with a Protocol Surface, silently omit an applicable declared capability, or imply compatibility outside its bounded scope. | PE-G3-SOURCE-S22, PE-G3-SOURCE-S53 | NONE |
| <a id="pe-g3-compat-007"></a> PE-G3-COMPAT-007 | MUST | applicable | Every Compatibility Statement | A Compatibility Statement MUST be a bounded assertion by or about one identified implementation concerning one identified target and one identified surface. | PE-G3-SOURCE-S52, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-008"></a> PE-G3-COMPAT-008 | MUST | applicable | Every Compatibility Statement | The statement MUST identify its implementation, implementation version where relevant, target, surface, declared scope, claim boundary, and statement identity. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S52, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-009"></a> PE-G3-COMPAT-009 | MUST NOT | applicable | Every Compatibility Statement | A statement MUST NOT be interpreted as proof of realization, proof of compatibility, conformance, certification, protocol succession, or protocol authority. | PE-G3-SOURCE-S48, PE-G3-SOURCE-S52 | NONE |
| <a id="pe-g3-compat-010"></a> PE-G3-COMPAT-010 | MUST | applicable | Every Compatibility Profile | A Compatibility Profile MUST remain a bounded aggregation of identified Compatibility Statements associated with one identified implementation. | PE-G3-SOURCE-S51, PE-G3-SOURCE-S52 | NONE |
| <a id="pe-g3-compat-011"></a> PE-G3-COMPAT-011 | MUST | applicable | Every Compatibility Profile | The profile MUST preserve the identity, target, surface, scope, and asserted meaning of each aggregated statement without merging their target or statement identities. | PE-G3-SOURCE-S51, PE-G3-SOURCE-S52, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-012"></a> PE-G3-COMPAT-012 | MUST NOT | applicable | Every Compatibility Profile | A Compatibility Profile MUST NOT be treated as an Implementation Profile, MUST NOT select normative implementation obligations, and MUST NOT establish compatibility merely by aggregation. | PE-G3-SOURCE-S48, PE-G3-SOURCE-S51, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-compat-013"></a> PE-G3-COMPAT-013 | MUST | applicable | Every Compatibility Declaration | A Compatibility Declaration MUST remain the complete identified record of one declared compatibility relationship concerning one implementation, one target, one surface, and one bounded scope. | PE-G3-SOURCE-S49, PE-G3-SOURCE-S52, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-014"></a> PE-G3-COMPAT-014 | MUST | applicable | Every Compatibility Declaration | The declaration MUST preserve the complete constituent identities, statement provenance, declared scope, version information, and declared compatibility meaning required by its governing compatibility model. | PE-G3-SOURCE-S49, PE-G3-SOURCE-S50, PE-G3-SOURCE-S52, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-015"></a> PE-G3-COMPAT-015 | MUST NOT | applicable | Every Compatibility Declaration | Publication or persistence of a declaration MUST NOT convert declared compatibility into realized compatibility, protocol truth, conformance, or certification. | PE-G3-SOURCE-S48, PE-G3-SOURCE-S49, PE-G3-SOURCE-S50 | NONE |
| <a id="pe-g3-compat-016"></a> PE-G3-COMPAT-016 | MUST | applicable | Every Compatibility Assessment | A Compatibility Assessment MUST evaluate only the identified declared compatibility relationship against its identified target, surface, scope, applicable protocol invariants, and available bounded evidence. | PE-G3-SOURCE-S48, PE-G3-SOURCE-S49, PE-G3-SOURCE-S50, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-017"></a> PE-G3-COMPAT-017 | MUST | applicable | Every Compatibility Assessment report | The report MUST identify its assessed implementation, target, surface, scope, basis, limitations, and bounded result without creating a separate protocol truth or conformance determination. | PE-G3-SOURCE-S48, PE-G3-SOURCE-S50, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-018"></a> PE-G3-COMPAT-018 | MUST | applicable | Every compatibility target, surface, statement, profile, declaration, and assessment | Each structure MUST retain its own bounded identity and role and MUST remain distinct from every other compatibility structure. | PE-G3-SOURCE-S49, PE-G3-SOURCE-S50, PE-G3-SOURCE-S51, PE-G3-SOURCE-S52, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-019"></a> PE-G3-COMPAT-019 | MUST NOT | applicable | Every compatibility claim or assessment | Compatibility MUST NOT establish Protocol Succession, Protocol Lineage membership, migration eligibility, generation replacement, or retirement. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S14, PE-G3-SOURCE-S15, PE-G3-SOURCE-S16, PE-G3-SOURCE-S48 | NONE |
| <a id="pe-g3-compat-020"></a> PE-G3-COMPAT-020 | MUST NOT | applicable | Every compatibility claim or assessment | Compatibility MUST NOT merge protocol-generation identities or establish complete semantic equivalence between distinct generations or implementations. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S15, PE-G3-SOURCE-S16, PE-G3-SOURCE-S48 | NONE |
| <a id="pe-g3-compat-021"></a> PE-G3-COMPAT-021 | MUST NOT | applicable | Every compatibility structure or assessment | Compatibility MUST NOT be interpreted as an Implementation Profile, complete Protocol Realization, conformance claim, conformance assessment, conformance determination, certification basis, certification decision, certification status, or certification recognition. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S48, PE-G3-SOURCE-S50, PE-G3-SOURCE-S51, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-compat-022"></a> PE-G3-COMPAT-022 | MUST | applicable | Every compatibility consequence of protocol evolution or migration | The consequence MUST preserve RF-04 ownership of succession, lineage, versioning, deprecation, migration, coexistence, and retirement and MUST identify the affected target and surface explicitly. | PE-G3-SOURCE-S13, PE-G3-SOURCE-S14, PE-G3-SOURCE-S15, PE-G3-SOURCE-S16, PE-G3-SOURCE-S48, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-023"></a> PE-G3-COMPAT-023 | MUST | applicable | Every failed, superseded, withdrawn, or historically retained compatibility statement, declaration, or assessment | Its lifecycle status MUST remain explicit without mutating the identity or semantics of the target generation, implementation, surface, or historical compatibility record. | PE-G3-SOURCE-S15, PE-G3-SOURCE-S49, PE-G3-SOURCE-S50, PE-G3-SOURCE-S52, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-compat-024"></a> PE-G3-COMPAT-024 | MUST NOT | applicable | Every compatibility identifier, statement, declaration, assessment, field, diagnostic, test, report, and observability surface | The surface MUST NOT identify a Private Actor, carry enrollment or admission provenance, create reusable participant identity, create cross-action linkage, or compose compatibility metadata into an actor-reconstruction bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S44, PE-G3-SOURCE-S48, PE-G3-SOURCE-S49, PE-G3-SOURCE-S50, PE-G3-SOURCE-S51, PE-G3-SOURCE-S52, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | STATE |

<a id="pe-g3-sf-14"></a>
## SF-14 — Implementation Profiles and Reference Implementations

<a id="pe-g3-rf-42"></a>
### RF-42 — Implementation profiles

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-profile-001"></a> PE-G3-PROFILE-001 | MUST | applicable | Every Privacy Engine Implementation Profile | A profile MUST be one uniquely identified, bounded, and complete implementation-facing selection and organization of applicable normative requirements derived from one identified Privacy Engine Protocol Specification. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-002"></a> PE-G3-PROFILE-002 | MUST | applicable | Every Implementation Profile | Profile identity MUST distinguish the profile from its source specification, other profiles, compatibility profiles, implementations, reference implementations, conformance artifacts, and certifications. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S51, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-profile-003"></a> PE-G3-PROFILE-003 | MUST | applicable | Every Implementation Profile | The profile MUST identify one bounded implementation target by role, capability set, deployment class, operational responsibility, or another specification-permitted implementation category. | PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-004"></a> PE-G3-PROFILE-004 | MUST | applicable | Every Implementation Profile | The profile MUST identify exactly one source Protocol Specification and the published protocol generation from which that specification derives. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-005"></a> PE-G3-PROFILE-005 | MUST | applicable | Every Implementation Profile | The profile MUST declare a precise scope sufficient to resolve the applicability of every normative requirement relevant to its target. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S06, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-006"></a> PE-G3-PROFILE-006 | MUST | applicable | Every requirement relevant to an Implementation Profile target | The profile MUST record the requirement as applicable, non-applicable under an identified specification rule, conditionally applicable, or resolved through a permitted specification choice. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S06, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-007"></a> PE-G3-PROFILE-007 | MUST NOT | applicable | Every Implementation Profile applicability decision | Applicability MUST NOT be invented from preference, convenience, implementation difficulty, existing implementation behavior, deployment topology, or a desired assessment result. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S45, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-008"></a> PE-G3-PROFILE-008 | MUST | applicable | Every requirement selected by an Implementation Profile | Selection MUST reference the same stable normative requirement defined by the source Protocol Specification and MUST preserve its identity. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S06, PE-G3-SOURCE-S08, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-009"></a> PE-G3-PROFILE-009 | MUST | applicable | Every applicable requirement in an Implementation Profile | The profile MUST preserve the requirement's complete meaning, operative strength, applicability conditions, prohibitions, permissions, success behavior, and failure behavior unchanged. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-010"></a> PE-G3-PROFILE-010 | MAY | applicable | Every choice explicitly permitted by the source Protocol Specification | A profile MAY resolve, constrain, require support for, exclude, or leave the choice implementation-defined only within the choice space permitted by the specification. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-011"></a> PE-G3-PROFILE-011 | MUST NOT | applicable | Every Implementation Profile | A profile MUST NOT invent a choice, widen a choice space, treat mandatory behavior as optional, permit prohibited behavior, or omit a mandatory choice that must be resolved at profile level. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S08, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-012"></a> PE-G3-PROFILE-012 | MUST | applicable | Every Implementation Profile composition | The composition MUST identify the profile, source specification, target, scope, applicability decisions, permitted-choice resolutions, dependencies, and completeness conditions without duplicating normative requirements. | PE-G3-SOURCE-S06, PE-G3-SOURCE-S07, PE-G3-SOURCE-S08, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-013"></a> PE-G3-PROFILE-013 | MUST | applicable | Every Implementation Profile dependency | The dependency MUST identify the depended-upon profile, direction, applicability condition, and required obligation boundary without merging profile identities or transferring authority. | PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-014"></a> PE-G3-PROFILE-014 | MUST | applicable | Every Implementation Profile | The profile MUST account for every requirement relevant to its declared scope and MUST fail profile construction when any applicable obligation, applicability decision, required choice, or dependency remains unresolved. | PE-G3-SOURCE-S06, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-015"></a> PE-G3-PROFILE-015 | MUST | applicable | Every semantically changed Implementation Profile | A change to scope, applicability, dependencies, requirement selection, or resolved choices MUST produce a distinguishable profile version or identity where retaining the prior identity would imply unchanged obligations. | PE-G3-SOURCE-S15, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-016"></a> PE-G3-PROFILE-016 | MAY | applicable | One Protocol Specification | Multiple Implementation Profiles MAY derive from the same specification where each profile has a distinct identity, bounded target, complete applicability resolution, and preserved requirement semantics. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-017"></a> PE-G3-PROFILE-017 | MUST NOT | applicable | Every Implementation Profile | A profile MUST NOT modify, replace, weaken, strengthen, supersede, or become the Protocol Specification or published protocol generation from which it derives. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-018"></a> PE-G3-PROFILE-018 | MUST NOT | applicable | Every Implementation Profile | A profile MUST NOT be identified with an implementation, Compatibility Profile, conformance assessment, conformance determination, certification basis, certification decision, certification status, or certification recognition. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S51, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-profile-019"></a> PE-G3-PROFILE-019 | MUST NOT | applicable | Every incomplete Protocol Specification | A complete final Implementation Profile MUST NOT be published from an incomplete Protocol Specification. | PE-G3-SOURCE-S03, PE-G3-SOURCE-S07, PE-G3-SOURCE-S08, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-020"></a> PE-G3-PROFILE-020 | MUST | applicable | Every profile construction or preservation failure | The profile MUST fail rather than invent, repair, weaken, strengthen, merge, divide, reinterpret, or infer a replacement requirement. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S18, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-profile-021"></a> PE-G3-PROFILE-021 | MUST NOT | applicable | Every profile identifier, applicability record, choice record, dependency, report, example, diagnostic, and observability surface | The surface MUST NOT identify a Private Actor, create reusable participant identity, create cross-action linkage, or convert implementation-target metadata into an actor-reconstruction bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S55 | STATE |

<a id="pe-g3-rf-43"></a>
### RF-43 — Reference implementations

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-refimpl-001"></a> PE-G3-REFIMPL-001 | MUST | applicable | Every Privacy Engine Reference Implementation | A Reference Implementation MUST be one identified implementation explicitly designated as an inspectable realization of one identified Implementation Profile within one declared reference scope. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-002"></a> PE-G3-REFIMPL-002 | MUST | applicable | Every Reference Implementation | Reference-implementation identity MUST distinguish the implementation, version, realized profile, reference scope, and reference status from every other reference realization. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-003"></a> PE-G3-REFIMPL-003 | MUST | applicable | Every reference designation | Reference status MUST be explicit, bounded to one identified implementation-profile relationship and scope, and independently reviewable. | PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-004"></a> PE-G3-REFIMPL-004 | MUST NOT | applicable | Every reference designation | Designation MUST NOT be interpreted as protocol publication, protocol authority, automatic conformance, certification, compatibility, defect freedom, or exclusive implementation status. | PE-G3-SOURCE-S10, PE-G3-SOURCE-S12, PE-G3-SOURCE-S48, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-005"></a> PE-G3-REFIMPL-005 | MUST | applicable | Every Reference Implementation | The declared reference scope MUST identify exactly which profile obligations, capability set, version, and implementation boundary the reference status covers. | PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-006"></a> PE-G3-REFIMPL-006 | MUST | applicable | Every Reference Implementation realizing an Implementation Profile | The implementation MUST realize every applicable profile requirement within its declared reference scope. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-007"></a> PE-G3-REFIMPL-007 | MUST | applicable | Every Reference Implementation | The implementation MUST preserve the applicable profile's required success behavior, failure behavior, privacy constraints, identity separations, and authority boundaries. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-008"></a> PE-G3-REFIMPL-008 | MAY | applicable | Every Reference Implementation | A Reference Implementation MAY select one implementation choice where that choice is explicitly permitted by the applicable profile. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-009"></a> PE-G3-REFIMPL-009 | MUST NOT | applicable | Every implementation choice selected by a Reference Implementation | The selected choice MUST NOT become a universal requirement, profile amendment, specification amendment, or prohibition against another permitted realization. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-010"></a> PE-G3-REFIMPL-010 | MAY | applicable | One Implementation Profile | Multiple Reference Implementations MAY realize the same profile where each independently satisfies every applicable obligation within its declared scope. | PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-011"></a> PE-G3-REFIMPL-011 | MAY | applicable | One implementation realizing multiple Implementation Profiles | The implementation MAY hold separate reference status for multiple profiles only where each profile relationship, version, scope, dependencies, and designation remain explicitly and independently identified. | PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-012"></a> PE-G3-REFIMPL-012 | MUST | applicable | Every materially changed Reference Implementation version | A materially changed version MUST remain separately identifiable where the change affects profile realization, permitted-choice resolution, normative behavior, interoperability behavior, defect status, or reference scope. | PE-G3-SOURCE-S15, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-013"></a> PE-G3-REFIMPL-013 | MUST | applicable | Every maintained Reference Implementation version | The version MUST remain sufficiently stable, available, and inspectable to support its declared reference uses without silently rewriting its identified historical behavior. | PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-014"></a> PE-G3-REFIMPL-014 | MUST | applicable | Every detected Reference Implementation defect or divergence | The defect or divergence MUST be evaluated against the applicable profile without redefining, weakening, strengthening, or repairing the profile requirement. | PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-015"></a> PE-G3-REFIMPL-015 | MUST | applicable | Every Reference Implementation unable to preserve an applicable obligation | The implementation MUST fail explicitly, and its implementation or designation MUST be corrected, narrowed, suspended, withdrawn, or superseded as appropriate. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-016"></a> PE-G3-REFIMPL-016 | MUST | applicable | Every ordinary implementation compared with a Reference Implementation | The ordinary implementation MUST be evaluated against its applicable profile rather than against incidental structure or behavior of the Reference Implementation. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-017"></a> PE-G3-REFIMPL-017 | MUST NOT | applicable | Every ordinary implementation | An ordinary implementation MUST NOT be required to copy reference source structure, language, algorithms, storage, deployment topology, APIs, logging, timing, or other behavior not required by the applicable profile. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-018"></a> PE-G3-REFIMPL-018 | MAY | applicable | Every conformance, certification, compatibility, testing, or interoperability activity | The activity MAY use a Reference Implementation as supporting evidence, comparison behavior, test infrastructure, fixture, peer, or implementation example. | PE-G3-SOURCE-S48, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-019"></a> PE-G3-REFIMPL-019 | MUST NOT | applicable | Every conformance, certification, or compatibility activity using a Reference Implementation | Agreement, interoperability, code reuse, designation, or behavioral similarity MUST NOT replace the applicable conformance basis, certification basis, or bounded compatibility assessment. | PE-G3-SOURCE-S48, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-020"></a> PE-G3-REFIMPL-020 | MUST | applicable | Every disagreement between a Reference Implementation and an upstream requirement | The disagreement MUST be resolved against the applicable Implementation Profile, Protocol Specification, and published protocol generation in that order of derivation. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-refimpl-021"></a> PE-G3-REFIMPL-021 | MUST NOT | applicable | Every reference identifier, designation, implementation record, version, test, diagnostic, report, log, and observability surface | The surface MUST NOT identify a Private Actor, create reusable participant identity, create cross-action linkage, or compose reference-implementation metadata into an actor-reconstruction bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S56 | STATE |

<a id="pe-g3-sf-15"></a>
## SF-15 — Conformance and Certification

<a id="pe-g3-rf-44"></a>
### RF-44 — Published conformance requirements and requirement sets

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-confreq-001"></a> PE-G3-CONFREQ-001 | MUST | applicable | Every Published Conformance Requirement | The requirement MUST be one bounded assessable expression of one existing applicable normative requirement. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S57 | NONE |
| <a id="pe-g3-confreq-002"></a> PE-G3-CONFREQ-002 | MUST | applicable | Every Published Conformance Requirement | The requirement MUST possess a stable identity distinct from its source normative requirement. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S57 | NONE |
| <a id="pe-g3-confreq-003"></a> PE-G3-CONFREQ-003 | MUST | applicable | Every Published Conformance Requirement | The requirement MUST identify its source normative requirement, Protocol Specification, and published protocol generation. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S57 | NONE |
| <a id="pe-g3-confreq-004"></a> PE-G3-CONFREQ-004 | MUST | applicable | Every conformance derivation | Derivation MUST preserve source-requirement identity, complete normative meaning, and source traceability. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S57 | NONE |
| <a id="pe-g3-confreq-005"></a> PE-G3-CONFREQ-005 | MUST | applicable | Every conformance derivation | Derivation MUST preserve operative strength, applicability conditions, and permitted-choice boundaries. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05, PE-G3-SOURCE-S57 | NONE |
| <a id="pe-g3-confreq-006"></a> PE-G3-CONFREQ-006 | MUST NOT | applicable | Every Published Conformance Requirement | The requirement MUST NOT create, remove, weaken, strengthen, repair, reinterpret, or replace a protocol obligation. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S57 | NONE |
| <a id="pe-g3-confreq-007"></a> PE-G3-CONFREQ-007 | MUST | applicable | Every published Conformance Requirement | Publication MUST make identity, source, meaning, strength, applicability, version, and traceability independently reviewable. | PE-G3-SOURCE-S57 | NONE |
| <a id="pe-g3-confreq-008"></a> PE-G3-CONFREQ-008 | MUST | applicable | Every published Conformance Requirement | The published requirement MUST remain immutable; semantic change MUST create a distinguishable requirement. | PE-G3-SOURCE-S15, PE-G3-SOURCE-S57 | NONE |
| <a id="pe-g3-confreq-009"></a> PE-G3-CONFREQ-009 | MUST | applicable | Every Published Conformance Requirement Set | The set MUST be one identified, bounded, immutable collection of applicable Published Conformance Requirements. | PE-G3-SOURCE-S58 | NONE |
| <a id="pe-g3-confreq-010"></a> PE-G3-CONFREQ-010 | MUST | applicable | Every Conformance Requirement Set | Set identity MUST distinguish its target, scope, version, composition, and source generation. | PE-G3-SOURCE-S58 | NONE |
| <a id="pe-g3-confreq-011"></a> PE-G3-CONFREQ-011 | MUST | applicable | Every Conformance Requirement Set | The set MUST identify exactly one bounded assessment target and one declared assessment scope. | PE-G3-SOURCE-S55, PE-G3-SOURCE-S58 | NONE |
| <a id="pe-g3-confreq-012"></a> PE-G3-CONFREQ-012 | MUST | applicable | Every complete Conformance Requirement Set | The set MUST contain every and only Published Conformance Requirements applicable within its declared target and scope. | PE-G3-SOURCE-S06, PE-G3-SOURCE-S58 | NONE |
| <a id="pe-g3-confreq-013"></a> PE-G3-CONFREQ-013 | MUST | applicable | Every Conformance Requirement Set constituent | Composition MUST preserve constituent identity, meaning, strength, applicability, ordering where relevant, and traceability. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S06, PE-G3-SOURCE-S58 | NONE |
| <a id="pe-g3-confreq-014"></a> PE-G3-CONFREQ-014 | MUST NOT | applicable | Every Conformance Requirement Set | The set MUST NOT evaluate an implementation, become an Implementation Profile, create obligations, or acquire protocol authority. | PE-G3-SOURCE-S55, PE-G3-SOURCE-S58 | NONE |

<a id="pe-g3-rf-45"></a>
### RF-45 — Conformance artifacts, evidence, and packages

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-confevid-001"></a> PE-G3-CONFEVID-001 | MUST | applicable | Every Conformance Artifact | An artifact MUST be one bounded, immutable, referenceable unit documenting objective implementation information relevant to conformance. | PE-G3-SOURCE-S59 | NONE |
| <a id="pe-g3-confevid-002"></a> PE-G3-CONFEVID-002 | MUST | applicable | Every Conformance Artifact | Artifact identity MUST distinguish the artifact, implementation, version, assessment scope, and recorded information. | PE-G3-SOURCE-S59 | NONE |
| <a id="pe-g3-confevid-003"></a> PE-G3-CONFEVID-003 | MUST | applicable | Every Conformance Artifact | The artifact MUST preserve integrity, provenance, authorship or production context, and reference stability. | PE-G3-SOURCE-S59 | NONE |
| <a id="pe-g3-confevid-004"></a> PE-G3-CONFEVID-004 | MUST | applicable | Every Conformance Artifact | Artifact content MUST remain objective, reviewable, and attributable to its declared implementation boundary. | PE-G3-SOURCE-S59 | NONE |
| <a id="pe-g3-confevid-005"></a> PE-G3-CONFEVID-005 | MUST | applicable | Every artifact used as evidence | Use as evidence MUST preserve artifact identity and MUST record the evidentiary relationship separately. | PE-G3-SOURCE-S59, PE-G3-SOURCE-S60 | NONE |
| <a id="pe-g3-confevid-006"></a> PE-G3-CONFEVID-006 | MUST NOT | applicable | Every Conformance Artifact | An artifact MUST NOT establish correctness, conformance, certification, protocol truth, or protocol authority merely by existing. | PE-G3-SOURCE-S59 | NONE |
| <a id="pe-g3-confevid-007"></a> PE-G3-CONFEVID-007 | MUST | applicable | Every Conformance Evidence set | Evidence MUST be one identified, published, complete, and traceable support set for one claim and declared scope. | PE-G3-SOURCE-S60 | NONE |
| <a id="pe-g3-confevid-008"></a> PE-G3-CONFEVID-008 | MUST | applicable | Every Conformance Evidence set | Evidence identity MUST distinguish its claim, implementation, profile, requirement set, scope, version, and constituent artifacts. | PE-G3-SOURCE-S60 | NONE |
| <a id="pe-g3-confevid-009"></a> PE-G3-CONFEVID-009 | MUST | applicable | Every evidence constituent | Evidence MUST trace each supported claim element to applicable requirements and preserved artifacts. | PE-G3-SOURCE-S57, PE-G3-SOURCE-S60 | NONE |
| <a id="pe-g3-confevid-010"></a> PE-G3-CONFEVID-010 | MUST | applicable | Every complete Conformance Evidence set | Evidence MUST account for every applicable conformance requirement within its declared evidentiary scope. | PE-G3-SOURCE-S58, PE-G3-SOURCE-S60 | NONE |
| <a id="pe-g3-confevid-011"></a> PE-G3-CONFEVID-011 | MAY | applicable | Every Conformance Evidence set | Evidence MAY compose testing, inspection, analysis, review, measurement, and preserved artifacts. | PE-G3-SOURCE-S60, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-confevid-012"></a> PE-G3-CONFEVID-012 | MUST NOT | applicable | Every Conformance Evidence set | Evidence MUST NOT perform assessment, determine conformance, establish certification, or become protocol truth. | PE-G3-SOURCE-S60, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-confevid-013"></a> PE-G3-CONFEVID-013 | MUST | applicable | Every Conformance Package | A package MUST be one canonical, identified, immutable publication unit for one bounded conformance assessment. | PE-G3-SOURCE-S61 | NONE |
| <a id="pe-g3-confevid-014"></a> PE-G3-CONFEVID-014 | MUST | applicable | Every Conformance Package | Package identity MUST distinguish its implementation, profile, claim, scope, version, evidence, artifacts, and publication. | PE-G3-SOURCE-S61 | NONE |
| <a id="pe-g3-confevid-015"></a> PE-G3-CONFEVID-015 | MUST | applicable | Every Conformance Package | The package MUST identify its artifacts, evidence, claim references, applicable requirement set, scope, and traceability. | PE-G3-SOURCE-S58, PE-G3-SOURCE-S61 | NONE |
| <a id="pe-g3-confevid-016"></a> PE-G3-CONFEVID-016 | MUST | applicable | Every published Conformance Package | The package MUST remain immutable; changed composition MUST create a distinguishable package. | PE-G3-SOURCE-S15, PE-G3-SOURCE-S61 | NONE |
| <a id="pe-g3-confevid-017"></a> PE-G3-CONFEVID-017 | MUST | applicable | Every Conformance Package constituent | Packaging MUST preserve constituent identity, content, integrity, provenance, scope, and independent meaning. | PE-G3-SOURCE-S59, PE-G3-SOURCE-S60, PE-G3-SOURCE-S61 | NONE |
| <a id="pe-g3-confevid-018"></a> PE-G3-CONFEVID-018 | MUST NOT | applicable | Every Conformance Package | The package MUST NOT merge constituents, perform assessment, or establish conformance by publication. | PE-G3-SOURCE-S61, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-confevid-019"></a> PE-G3-CONFEVID-019 | MUST NOT | applicable | Every Conformance Package | The package MUST NOT constitute certification or replace a Certification Basis, Decision, Status, or recognition. | PE-G3-SOURCE-S61, PE-G3-SOURCE-S65, PE-G3-SOURCE-S66, PE-G3-SOURCE-S67, PE-G3-SOURCE-S68 | NONE |

<a id="pe-g3-rf-46"></a>
### RF-46 — Conformance claims, assessments, and determinations

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-conform-001"></a> PE-G3-CONFORM-001 | MUST | applicable | Every Conformance Claim | A claim MUST be one bounded assertion that one identified implementation satisfies one identified Implementation Profile within one declared scope. | PE-G3-SOURCE-S62, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-002"></a> PE-G3-CONFORM-002 | MUST | applicable | Every Conformance Claim | Claim identity MUST distinguish the assertion, implementation, profile, specification, generation, scope, and version. | PE-G3-SOURCE-S62, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-003"></a> PE-G3-CONFORM-003 | MUST | applicable | Every Conformance Claim | The claim MUST identify its implementation, implementation version where relevant, profile, specification, generation, and assessment scope. | PE-G3-SOURCE-S62 | NONE |
| <a id="pe-g3-conform-004"></a> PE-G3-CONFORM-004 | MUST | applicable | Every Conformance Claim | The claim MUST remain bounded to its declared implementation-profile relationship and scope. | PE-G3-SOURCE-S62 | NONE |
| <a id="pe-g3-conform-005"></a> PE-G3-CONFORM-005 | MUST NOT | applicable | Every Conformance Claim | The claim MUST NOT establish Protocol Realization or replace implementation obligations. | PE-G3-SOURCE-S46, PE-G3-SOURCE-S62 | NONE |
| <a id="pe-g3-conform-006"></a> PE-G3-CONFORM-006 | MUST NOT | applicable | Every Conformance Claim | The claim MUST NOT perform assessment, produce a determination, establish conformance, or establish certification. | PE-G3-SOURCE-S62, PE-G3-SOURCE-S63, PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-conform-007"></a> PE-G3-CONFORM-007 | MUST | applicable | Every Conformance Assessment | An assessment MUST be one identified bounded evaluation of one identified claim concerning one implementation, profile, and scope. | PE-G3-SOURCE-S63, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-008"></a> PE-G3-CONFORM-008 | MUST | applicable | Every Conformance Assessment | Assessment identity MUST distinguish the evaluation occurrence, claim, implementation, profile, requirement set, evidence, and scope. | PE-G3-SOURCE-S63, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-009"></a> PE-G3-CONFORM-009 | MUST | applicable | Every Conformance Assessment | The assessment MUST declare the exact target, applicable requirement set, evidence boundary, and assessment scope. | PE-G3-SOURCE-S58, PE-G3-SOURCE-S60, PE-G3-SOURCE-S63 | NONE |
| <a id="pe-g3-conform-010"></a> PE-G3-CONFORM-010 | MUST | applicable | Every complete Conformance Assessment | The assessment MUST evaluate every applicable requirement within its declared scope. | PE-G3-SOURCE-S58, PE-G3-SOURCE-S63, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-011"></a> PE-G3-CONFORM-011 | MUST | applicable | Every Conformance Assessment | The assessment MUST use valid, applicable, integrity-preserved, and traceable evidence. | PE-G3-SOURCE-S59, PE-G3-SOURCE-S60, PE-G3-SOURCE-S63 | NONE |
| <a id="pe-g3-conform-012"></a> PE-G3-CONFORM-012 | MUST | applicable | Every Conformance Assessment | The assessment MUST evaluate the claim without modifying or becoming the claim. | PE-G3-SOURCE-S62, PE-G3-SOURCE-S63 | NONE |
| <a id="pe-g3-conform-013"></a> PE-G3-CONFORM-013 | MUST | applicable | Every completed Conformance Assessment | Completion MUST produce at most one distinct Conformance Determination for that assessment occurrence. | PE-G3-SOURCE-S63, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-014"></a> PE-G3-CONFORM-014 | MUST | applicable | Every assessment unable to reach a supported classification | The assessment MUST fail or remain indeterminate without producing a conformant or non-conformant determination. | PE-G3-SOURCE-S63, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-015"></a> PE-G3-CONFORM-015 | MUST | applicable | Every Conformance Determination | A determination MUST be the bounded authoritative result of one completed Conformance Assessment. | PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-016"></a> PE-G3-CONFORM-016 | MUST | applicable | Every Conformance Determination | Determination identity MUST distinguish its assessment, implementation, profile, scope, requirement set, and classification. | PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-017"></a> PE-G3-CONFORM-017 | MUST | applicable | Every conformant determination | The determination MUST record satisfaction of every applicable requirement within its declared scope. | PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-018"></a> PE-G3-CONFORM-018 | MUST | applicable | Every non-conformant determination | The determination MUST record that at least one applicable requirement within scope was not satisfied. | PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-019"></a> PE-G3-CONFORM-019 | MUST | applicable | Every Conformance Determination | The determination MUST record exactly one classification: conformant within scope or non-conformant within scope. | PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-020"></a> PE-G3-CONFORM-020 | MUST | applicable | Every Conformance Determination | The determination MUST identify its complete bounded scope; no unstated scope is implied. | PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-021"></a> PE-G3-CONFORM-021 | MUST NOT | applicable | Every partial Conformance Assessment | Partial assessment MUST NOT establish complete conformance beyond the requirements actually assessed. | PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-022"></a> PE-G3-CONFORM-022 | MUST | applicable | Every published Conformance Determination | The historical determination MUST remain immutable and independently identifiable. | PE-G3-SOURCE-S15, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-023"></a> PE-G3-CONFORM-023 | MUST | applicable | Every correction affecting previous conformance | Correction MUST be evaluated through a new assessment producing a new determination where completed. | PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-024"></a> PE-G3-CONFORM-024 | MUST | applicable | Every conformance or compatibility activity | Conformance satisfaction and compatibility relationships MUST remain distinct. | PE-G3-SOURCE-S48, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-025"></a> PE-G3-CONFORM-025 | MUST | applicable | Every conformance or certification activity | Conformance determination and certification recognition MUST remain distinct. | PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-conform-026"></a> PE-G3-CONFORM-026 | MUST | applicable | Every conformance authority | Conformance authority MUST remain bounded assessment authority within the declared target and scope. | PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-conform-027"></a> PE-G3-CONFORM-027 | MUST NOT | applicable | Every claim, assessment, determination, evidence object, report, test, diagnostic, identifier, and metadata surface | The surface MUST NOT identify a Private Actor, create reusable participant identity, create cross-action linkage, or create an actor-reconstruction bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S64 | STATE |

<a id="pe-g3-rf-47"></a>
### RF-47 — Certification bases, decisions, and statuses

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-certdet-001"></a> PE-G3-CERTDET-001 | MUST | applicable | Every Certification Basis | A basis MUST be one complete, immutable, identified evaluation basis for one bounded certification decision. | PE-G3-SOURCE-S65 | NONE |
| <a id="pe-g3-certdet-002"></a> PE-G3-CERTDET-002 | MUST | applicable | Every Certification Basis | Basis identity MUST distinguish its subject, target, scope, requirements, packages, determinations, policy, and version. | PE-G3-SOURCE-S65 | NONE |
| <a id="pe-g3-certdet-003"></a> PE-G3-CERTDET-003 | MUST | applicable | Every complete Certification Basis | The basis MUST identify every criterion and supporting conformance structure required for its declared scope. | PE-G3-SOURCE-S57, PE-G3-SOURCE-S58, PE-G3-SOURCE-S61, PE-G3-SOURCE-S64, PE-G3-SOURCE-S65 | NONE |
| <a id="pe-g3-certdet-004"></a> PE-G3-CERTDET-004 | MUST | applicable | Every published Certification Basis | The basis MUST remain immutable; changed criteria or composition MUST create a distinguishable basis. | PE-G3-SOURCE-S15, PE-G3-SOURCE-S65 | NONE |
| <a id="pe-g3-certdet-005"></a> PE-G3-CERTDET-005 | MUST | applicable | Every Certification Basis | The basis MUST declare one bounded certification subject, target, program context, and scope. | PE-G3-SOURCE-S65, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-certdet-006"></a> PE-G3-CERTDET-006 | MUST NOT | applicable | Every Certification Basis | The basis MUST NOT define its decision result, modify conformance, or create protocol obligations. | PE-G3-SOURCE-S65 | NONE |
| <a id="pe-g3-certdet-007"></a> PE-G3-CERTDET-007 | MUST | applicable | Every Certification Decision | A decision MUST be one identified immutable pass-or-fail evaluation of one subject and package against one basis. | PE-G3-SOURCE-S66 | NONE |
| <a id="pe-g3-certdet-008"></a> PE-G3-CERTDET-008 | MUST | applicable | Every Certification Decision | Decision identity MUST distinguish the subject, package, basis, scope, decision occurrence, and classification. | PE-G3-SOURCE-S66 | NONE |
| <a id="pe-g3-certdet-009"></a> PE-G3-CERTDET-009 | MUST | applicable | Every passing Certification Decision | Pass MUST record that the identified subject and package satisfy the identified basis within scope. | PE-G3-SOURCE-S66 | NONE |
| <a id="pe-g3-certdet-010"></a> PE-G3-CERTDET-010 | MUST | applicable | Every failing Certification Decision | Fail MUST record that the identified subject or package does not satisfy the identified basis within scope. | PE-G3-SOURCE-S66 | NONE |
| <a id="pe-g3-certdet-011"></a> PE-G3-CERTDET-011 | MUST | applicable | Every Certification Decision | The decision MUST record exactly one classification: pass or fail. | PE-G3-SOURCE-S66 | NONE |
| <a id="pe-g3-certdet-012"></a> PE-G3-CERTDET-012 | MUST | applicable | Every Certification Decision | The decision MUST identify the exact Certification Basis against which it was made. | PE-G3-SOURCE-S65, PE-G3-SOURCE-S66 | NONE |
| <a id="pe-g3-certdet-013"></a> PE-G3-CERTDET-013 | MUST NOT | applicable | Every Certification Decision | The decision MUST NOT perform conformance assessment, alter evidence, repair failure, or modify a Conformance Determination. | PE-G3-SOURCE-S64, PE-G3-SOURCE-S66 | NONE |
| <a id="pe-g3-certdet-014"></a> PE-G3-CERTDET-014 | MUST | applicable | Every Certification Status | Status MUST be one recorded lifecycle state of one identified certification. | PE-G3-SOURCE-S67, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-certdet-015"></a> PE-G3-CERTDET-015 | MUST | applicable | Every Certification Status | Status identity MUST distinguish the certification, lifecycle occurrence, effective state, authority, and scope. | PE-G3-SOURCE-S67, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-certdet-016"></a> PE-G3-CERTDET-016 | MUST | applicable | Every certification lifecycle change | The change MUST occur through a defined issuance, maintenance, suspension, withdrawal, expiry, or reassessment event. | PE-G3-SOURCE-S67, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-certdet-017"></a> PE-G3-CERTDET-017 | MUST | applicable | Every Certification Status | Status MUST remain distinct from its supporting Certification Decision and historical decisions. | PE-G3-SOURCE-S66, PE-G3-SOURCE-S67 | NONE |
| <a id="pe-g3-certdet-018"></a> PE-G3-CERTDET-018 | MUST NOT | applicable | Every Certification Status | Status MUST NOT become implementation state, conformance truth, protocol truth, or protocol authority. | PE-G3-SOURCE-S64, PE-G3-SOURCE-S67 | NONE |
| <a id="pe-g3-certdet-019"></a> PE-G3-CERTDET-019 | MUST | applicable | Every certification lifecycle update | The update MUST preserve historical bases, decisions, determinations, and prior status occurrences unchanged. | PE-G3-SOURCE-S64, PE-G3-SOURCE-S65, PE-G3-SOURCE-S66, PE-G3-SOURCE-S67 | NONE |

<a id="pe-g3-rf-48"></a>
### RF-48 — Certification recognition, scope, and authority

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-cert-001"></a> PE-G3-CERT-001 | MUST | applicable | Every Privacy Engine Certification | Certification MUST be one bounded recognition of one identified implementation with respect to one identified Implementation Profile. | PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-002"></a> PE-G3-CERT-002 | MUST | applicable | Every Certification | Certification identity MUST distinguish the recognition, implementation, profile, scope, basis, decisions, determinations, authority, and status. | PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-003"></a> PE-G3-CERT-003 | MUST | applicable | Every Certification | The certification subject MUST be exactly one identified implementation. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-004"></a> PE-G3-CERT-004 | MUST | applicable | Every Certification | The certification target MUST be exactly one identified Implementation Profile. | PE-G3-SOURCE-S55, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-005"></a> PE-G3-CERT-005 | MUST | applicable | Every Certification | Certification MUST apply only within its explicitly declared implementation, profile, determination, and recognition scope. | PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-006"></a> PE-G3-CERT-006 | MUST | applicable | Every Certification | Certification MUST be supported by one or more identified conformant Conformance Determinations covering its declared scope. | PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-007"></a> PE-G3-CERT-007 | MUST NOT | applicable | Every complete-certification claim | Complete certification MUST NOT be claimed unless supporting determinations cover every applicable profile requirement within the declared complete scope. | PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-008"></a> PE-G3-CERT-008 | MUST | applicable | Every partial Certification | Partial recognition MUST explicitly identify its bounded scope and MUST remain distinguishable from complete certification. | PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-009"></a> PE-G3-CERT-009 | MUST | applicable | Every Certification | The issuing certification authority MUST possess a stable identity distinct from the certification and assessed implementation. | PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-010"></a> PE-G3-CERT-010 | MUST | applicable | Every certification authority | The authority MUST declare the certification program, responsibilities, recognition boundary, and scope within which it acts. | PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-011"></a> PE-G3-CERT-011 | MUST | applicable | Every certification authority action | Issuance, maintenance, suspension, withdrawal, and update authority MUST remain bounded by the declared program and scope. | PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-012"></a> PE-G3-CERT-012 | MUST | applicable | Every Certification | Recognition MUST remain distinct from conformance assessment without replacing it. | PE-G3-SOURCE-S63, PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-013"></a> PE-G3-CERT-013 | MUST | applicable | Every certification or compatibility statement | Certification recognition and compatibility MUST remain distinct. | PE-G3-SOURCE-S48, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-014"></a> PE-G3-CERT-014 | MUST NOT | applicable | Every Certification and certification authority | Neither certification nor its authority MUST become protocol authority or redefine upstream semantics. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S10, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-015"></a> PE-G3-CERT-015 | MUST | applicable | Every certification withdrawal | Withdrawal MUST change certification status only and MUST preserve implementation, profile, determination, decision, and protocol history. | PE-G3-SOURCE-S64, PE-G3-SOURCE-S66, PE-G3-SOURCE-S67, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-016"></a> PE-G3-CERT-016 | MUST | applicable | Every certification reassessment | Reassessment MUST use new identified evidence, assessment, determination, basis, or decision occurrences where applicable. | PE-G3-SOURCE-S60, PE-G3-SOURCE-S63, PE-G3-SOURCE-S64, PE-G3-SOURCE-S65, PE-G3-SOURCE-S66, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-017"></a> PE-G3-CERT-017 | MUST | applicable | Every certification lifecycle | Historical Conformance Determinations and Certification Decisions MUST remain immutable through issuance, withdrawal, correction, and reassessment. | PE-G3-SOURCE-S64, PE-G3-SOURCE-S66, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-cert-018"></a> PE-G3-CERT-018 | MUST | applicable | Every conformance and certification structure | Public identifiers and records MUST preserve Private Actor separation and action-bounded unlinkability. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | STATE |
| <a id="pe-g3-cert-019"></a> PE-G3-CERT-019 | MUST | applicable | Every conformance and certification naming surface | Names, fields, routes, storage keys, logs, diagnostics, examples, tests, and reports MUST use neutral non-correlation-bearing terminology. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20 | STATE |
| <a id="pe-g3-cert-020"></a> PE-G3-CERT-020 | MUST NOT | applicable | Every conformance and certification composition | Composition MUST NOT expose enrollment provenance, wallet identity, reusable participant identity, cross-action linkage, or an actor-reconstruction bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20, PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | STATE |

<a id="pe-g3-sf-16"></a>
## SF-16 — Semantic Preservation and Explicit Exclusions

<a id="pe-g3-rf-49"></a>
### RF-49 — Protocol-semantic preservation

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-sempres-001"></a> PE-G3-SEMPRES-001 | MUST | applicable | Every downstream Privacy Engine layer | The layer MUST preserve applicable upstream protocol semantics within its declared role and scope. | PE-G3-SOURCE-S03, PE-G3-SOURCE-S08, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-sempres-002"></a> PE-G3-SEMPRES-002 | MUST | applicable | The complete downstream chain | The chain MUST remain Generation to Specification to Profile to Implementation to Conformance to Certification. | PE-G3-SOURCE-S03, PE-G3-SOURCE-S08, PE-G3-SOURCE-S55, PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-sempres-003"></a> PE-G3-SEMPRES-003 | MUST | applicable | Every selected semantic subject or obligation | Selection and every later layer MUST preserve the same selected subject or obligation. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-sempres-004"></a> PE-G3-SEMPRES-004 | MUST | applicable | Every normative requirement crossing a downstream boundary | The boundary MUST preserve stable requirement identity and traceability. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S57 | NONE |
| <a id="pe-g3-sempres-005"></a> PE-G3-SEMPRES-005 | MUST | applicable | Every semantic subject crossing a downstream boundary | The boundary MUST preserve complete normative meaning. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-sempres-006"></a> PE-G3-SEMPRES-006 | MUST | applicable | Every requirement crossing a downstream boundary | The boundary MUST preserve operative strength unchanged. | PE-G3-SOURCE-S04, PE-G3-SOURCE-S05, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-sempres-007"></a> PE-G3-SEMPRES-007 | MUST | applicable | Every requirement crossing a downstream boundary | The boundary MUST preserve applicability and its governing conditions. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-sempres-008"></a> PE-G3-SEMPRES-008 | MUST | applicable | Every permitted protocol choice | Every downstream constraint or selection MUST remain within the published choice boundary. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S55 | NONE |
| <a id="pe-g3-sempres-009"></a> PE-G3-SEMPRES-009 | MUST | applicable | Every protocol subject and occurrence | Downstream processing MUST preserve subject identity, occurrence identity, and established identity separation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-sempres-010"></a> PE-G3-SEMPRES-010 | MUST | applicable | Every downstream representation and surface | The representation or surface MUST preserve privacy, unlinkability, minimum disclosure, and Private Actor separation. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20 | STATE |
| <a id="pe-g3-sempres-011"></a> PE-G3-SEMPRES-011 | MUST | applicable | Every proof, public input, verification, and validity boundary | The boundary MUST preserve declared proof meaning, public-input meaning, verification meaning, and complete validity conditions. | PE-G3-SOURCE-S18 | NONE |
| <a id="pe-g3-sempres-012"></a> PE-G3-SEMPRES-012 | MUST | applicable | Every Protocol Action use chain | The chain MUST preserve Action, Evaluation, Determination, acceptance, and rejection identities and semantics. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S24, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-sempres-013"></a> PE-G3-SEMPRES-013 | MUST | applicable | Every transition use chain | The chain MUST preserve mapping, occurrence, authorization, execution, commitment, state, history, consequence, and failure semantics. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S26, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-sempres-014"></a> PE-G3-SEMPRES-014 | MUST | applicable | Every application or adapter boundary | Application representation and adapter translation MUST preserve selected protocol meaning or fail. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S40, PE-G3-SOURCE-S41, PE-G3-SOURCE-S42, PE-G3-SOURCE-S44 | NONE |
| <a id="pe-g3-sempres-015"></a> PE-G3-SEMPRES-015 | MUST | applicable | Every runtime or implementation boundary | Operational responsibility and implementation realization MUST preserve semantics without acquiring semantic ownership. | PE-G3-SOURCE-S43, PE-G3-SOURCE-S45, PE-G3-SOURCE-S46, PE-G3-SOURCE-S47 | NONE |
| <a id="pe-g3-sempres-016"></a> PE-G3-SEMPRES-016 | MUST | applicable | Every compatibility structure | Compatibility MUST preserve its declared target, surface, relationship, scope, and separation from upstream semantics. | PE-G3-SOURCE-S48, PE-G3-SOURCE-S49, PE-G3-SOURCE-S50, PE-G3-SOURCE-S51, PE-G3-SOURCE-S52, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-sempres-017"></a> PE-G3-SEMPRES-017 | MUST | applicable | Every profile and Reference Implementation boundary | Profile selection and reference realization MUST preserve applicable requirements and permitted-choice boundaries. | PE-G3-SOURCE-S55, PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-sempres-018"></a> PE-G3-SEMPRES-018 | MUST | applicable | Every conformance boundary | Requirements, evidence, assessment, and determination MUST preserve upstream meaning and bounded scope. | PE-G3-SOURCE-S57, PE-G3-SOURCE-S58, PE-G3-SOURCE-S59, PE-G3-SOURCE-S60, PE-G3-SOURCE-S61, PE-G3-SOURCE-S62, PE-G3-SOURCE-S63, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-sempres-019"></a> PE-G3-SEMPRES-019 | MUST | applicable | Every certification boundary | Basis, decision, status, recognition, and authority MUST preserve supporting conformance meaning and scope. | PE-G3-SOURCE-S65, PE-G3-SOURCE-S66, PE-G3-SOURCE-S67, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-sempres-020"></a> PE-G3-SEMPRES-020 | MUST | applicable | Every successful downstream operation | Success MUST preserve the selected subject or obligation without substitution. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-sempres-021"></a> PE-G3-SEMPRES-021 | MUST | applicable | Every downstream operation unable to demonstrate preservation | The operation MUST fail, remain unsupported, narrow, withdraw, or be superseded under its defined lifecycle. | PE-G3-SOURCE-S27, PE-G3-SOURCE-S46, PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-sempres-022"></a> PE-G3-SEMPRES-022 | MUST NOT | applicable | Every preservation failure | Failure MUST NOT repair, reinterpret, replace, or synthesize missing semantics. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-sempres-023"></a> PE-G3-SEMPRES-023 | MUST NOT | applicable | Every downstream layer | The layer MUST NOT substitute a different subject, occurrence, requirement, determination, transition, or recognition. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-sempres-024"></a> PE-G3-SEMPRES-024 | MUST NOT | applicable | Every downstream layer | The layer MUST NOT infer an absent obligation, permission, identity, evidence item, classification, or authority. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S18, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-sempres-025"></a> PE-G3-SEMPRES-025 | MUST NOT | applicable | Every downstream layer | The layer MUST NOT silently widen or narrow identity, meaning, applicability, choice, target, or scope. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S55, PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-sempres-026"></a> PE-G3-SEMPRES-026 | MUST NOT | applicable | Every downstream composition | Composition MUST NOT merge distinct subjects or divide one subject into replacement identities or obligations. | PE-G3-SOURCE-S05, PE-G3-SOURCE-S17, PE-G3-SOURCE-S18 | NONE |
| <a id="pe-g3-sempres-027"></a> PE-G3-SEMPRES-027 | MUST | applicable | Every Evaluation, Determination, failure, retry, realization, diagnostic and observability surface | Every Evaluation, Determination, failure, retry, representation, publication, transport, delivery, diagnostic and observability surface MUST preserve Private Actor non-disclosure, neutral naming, action-bounded public identity and the prohibition on reusable participant identity, actor provenance and cross-action linkage. | PE-G3-SOURCE-S25, PE-G3-SOURCE-S27, PE-G3-SOURCE-S30, PE-G3-SOURCE-S32, PE-G3-SOURCE-S42, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-tsepres-001"></a> PE-G3-TSEPRES-001 | MUST | applicable | ALWAYS | Every comparison, recovery and commitment MUST preserve the distinct identities and meanings of E, D, authorization, T, U, Q0 and successor state. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tsepres-002-a01"></a> PE-G3-TSEPRES-002-A01 | MUST | applicable | ALWAYS | Predecessor and successor generations MUST coexist. | PE-G3-SOURCE-S69, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tsepres-002-a02"></a> PE-G3-TSEPRES-002-A02 | MUST | applicable | ALWAYS | Any future succession MUST remain directional and non-retroactive. | PE-G3-SOURCE-S69, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tsepres-003"></a> PE-G3-TSEPRES-003 | MUST | applicable | ALWAYS | Candidate acceptance, specification acceptance, Protocol Publication, succession and Protocol Specification Publication MUST remain separate acts. | PE-G3-SOURCE-S69 | NONE |

<a id="pe-g3-rf-50"></a>
### RF-50 — Explicit protocol exclusions and prohibited interpretations

| Requirement | Strength | Applicability | Condition | Normative text | Normative sources | Supporting references |
|---|---|---|---|---|---|---|
| <a id="pe-g3-exclude-001"></a> PE-G3-EXCLUDE-001 | MUST | applicable | The complete Protocol Specification | The specification MUST identify prohibited interpretations through authoritative exclusions and supporting local references. | PE-G3-SOURCE-S03 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-exclude-002"></a> PE-G3-EXCLUDE-002 | MUST NOT | applicable | Every development or protocol interpretation | STATE.md MUST NOT be interpreted as published protocol authority. | PE-G3-SOURCE-S08 | STATE |
| <a id="pe-g3-exclude-003"></a> PE-G3-EXCLUDE-003 | MUST NOT | applicable | Every downstream structure | No specification, interface, application, runtime, implementation, profile, assessment, conformance, certification, deployment, report, or observability surface MUST become protocol authority. | PE-G3-SOURCE-S08, PE-G3-SOURCE-S17, PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-exclude-004"></a> PE-G3-EXCLUDE-004 | MUST NOT | applicable | Every downstream layer | A downstream layer MUST NOT define, amend, replace, or supersede upstream protocol semantics. | PE-G3-SOURCE-S03, PE-G3-SOURCE-S08, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-exclude-005"></a> PE-G3-EXCLUDE-005 | MUST NOT | applicable | Every application interpretation | Application-owned meaning, policy, request, response, or state MUST NOT become protocol truth. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S40, PE-G3-SOURCE-S41, PE-G3-SOURCE-S42 | NONE |
| <a id="pe-g3-exclude-006"></a> PE-G3-EXCLUDE-006 | MUST NOT | applicable | Every implementation interpretation | Existing implementation behavior, convenience, defect, topology, or machinery MUST NOT become protocol semantics. | PE-G3-SOURCE-S45, PE-G3-SOURCE-S46 | NONE |
| <a id="pe-g3-exclude-007"></a> PE-G3-EXCLUDE-007 | MUST NOT | applicable | Every reference interpretation | Reference behavior, designation, similarity, or interoperability MUST NOT become a normative requirement. | PE-G3-SOURCE-S56 | NONE |
| <a id="pe-g3-exclude-008"></a> PE-G3-EXCLUDE-008 | MUST NOT | applicable | Every compatibility interpretation | Compatibility MUST NOT become succession, semantic equivalence, conformance, certification, or protocol authority. | PE-G3-SOURCE-S48, PE-G3-SOURCE-S49, PE-G3-SOURCE-S50, PE-G3-SOURCE-S51, PE-G3-SOURCE-S52, PE-G3-SOURCE-S53, PE-G3-SOURCE-S54 | NONE |
| <a id="pe-g3-exclude-009"></a> PE-G3-EXCLUDE-009 | MUST NOT | applicable | Every conformance interpretation | Conformance MUST NOT create obligations, redefine realization, become certification, or acquire protocol authority. | PE-G3-SOURCE-S57, PE-G3-SOURCE-S58, PE-G3-SOURCE-S64 | NONE |
| <a id="pe-g3-exclude-010"></a> PE-G3-EXCLUDE-010 | MUST NOT | applicable | Every certification interpretation | Certification MUST NOT perform conformance assessment, redefine semantics, become protocol truth, or acquire protocol authority. | PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-exclude-011"></a> PE-G3-EXCLUDE-011 | MUST NOT | applicable | Every evidence or testing interpretation | Artifact existence, evidence, testing, inspection, comparison, or package publication MUST NOT independently establish conformance or certification. | PE-G3-SOURCE-S59, PE-G3-SOURCE-S60, PE-G3-SOURCE-S61, PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-exclude-012"></a> PE-G3-EXCLUDE-012 | MUST NOT | applicable | Every protocol-subject identifier | A protocol-subject or occurrence identifier MUST NOT identify or imply a Private Actor. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20 | STATE |
| <a id="pe-g3-exclude-013"></a> PE-G3-EXCLUDE-013 | MUST NOT | applicable | Every public identifier and metadata surface | The surface MUST NOT create reusable participant identity or identity continuity across bounded actions. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20 | STATE |
| <a id="pe-g3-exclude-014"></a> PE-G3-EXCLUDE-014 | MUST NOT | applicable | Every protocol, assessment, and certification surface | The surface MUST NOT create cross-action linkage or extend proof meaning into actor identification. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20 | STATE |
| <a id="pe-g3-exclude-015"></a> PE-G3-EXCLUDE-015 | MUST NOT | applicable | Every downstream record | Enrollment, admission, funding, sponsor, origin, ownership, or wallet provenance MUST NOT be carried into action, assessment, or certification identity. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20 | STATE |
| <a id="pe-g3-exclude-016"></a> PE-G3-EXCLUDE-016 | MUST NOT | applicable | Every metadata composition | Timing, ordering, transport, runtime, deployment, evidence, assessment, certification, or authority metadata MUST NOT create an actor-reconstruction bridge. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20 | STATE |
| <a id="pe-g3-exclude-017"></a> PE-G3-EXCLUDE-017 | MUST NOT | applicable | Every naming and documentation surface | Names, fields, routes, keys, logs, diagnostics, examples, tests, and reports MUST NOT bypass privacy or introduce correlation-bearing semantics. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S20 | STATE |
| <a id="pe-g3-exclude-018"></a> PE-G3-EXCLUDE-018 | MUST | applicable | Every proposed new first-class protocol subject | The subject MUST demonstrate independent identity, semantics, validity, lifecycle, and consequence before introduction. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S18, PE-G3-SOURCE-S28 | NONE |
| <a id="pe-g3-exclude-019"></a> PE-G3-EXCLUDE-019 | MUST NOT | applicable | Every Protocol Claim interpretation | A Protocol Claim MUST NOT be introduced as a distinct first-class architectural subject. | PE-G3-SOURCE-S28 | NONE |
| <a id="pe-g3-exclude-020"></a> PE-G3-EXCLUDE-020 | MUST NOT | applicable | Every Evaluation or classification model | An Evaluation Outcome, separate acceptance object, or separate rejection object MUST NOT be introduced. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S25 | NONE |
| <a id="pe-g3-exclude-021"></a> PE-G3-EXCLUDE-021 | MUST NOT | applicable | Every transition model | Authorization, execution, commitment, consequence, failure, or stale authorization MUST NOT become an artificial first-class subject. | PE-G3-SOURCE-S18, PE-G3-SOURCE-S27 | NONE |
| <a id="pe-g3-exclude-022"></a> PE-G3-EXCLUDE-022 | MUST NOT | applicable | Every certification model | Certification outcome MUST NOT become a new protocol subject distinct from Decision, Status, or recognition. | PE-G3-SOURCE-S66, PE-G3-SOURCE-S67, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-exclude-023"></a> PE-G3-EXCLUDE-023 | MUST NOT | applicable | Every implementation-specific design choice | Blockchain consensus, transaction formats, relay, transport, storage, database, deployment topology, language, and source structure MUST NOT become protocol law. | PE-G3-SOURCE-S21, PE-G3-SOURCE-S29, PE-G3-SOURCE-S44, PE-G3-SOURCE-S45 | NONE |
| <a id="pe-g3-exclude-024"></a> PE-G3-EXCLUDE-024 | MUST NOT | applicable | Every application or certification-program choice | Application business meaning, auditor qualification, program operations, governance, accreditation, branding, and commercial policy MUST NOT become protocol law. | PE-G3-SOURCE-S29, PE-G3-SOURCE-S44, PE-G3-SOURCE-S68 | NONE |
| <a id="pe-g3-exclude-025"></a> PE-G3-EXCLUDE-025 | MUST NOT | applicable | The current implementation and codebase | Specification composition MUST NOT be interpreted as a current-codebase compatibility, conformance, certification, security, or operational-readiness assessment. | PE-G3-SOURCE-S17, PE-G3-SOURCE-S64, PE-G3-SOURCE-S68 | PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-exclude-026"></a> PE-G3-EXCLUDE-026 | MUST NOT | applicable | The Engineering[150] specification state | Composition completion MUST NOT be interpreted as final consolidation, acceptance, certification, publication, or publication readiness before Engineering[151]. | PE-G3-SOURCE-S03 | STATE, PE-G3-COMPOSITION-MAP-001 |
| <a id="pe-g3-exclude-027"></a> PE-G3-EXCLUDE-027 | MUST NOT | applicable | Every partial Evaluation completion representation | Partial Evaluation completion MUST NOT be represented as a valid terminal protocol state. | PE-G3-SOURCE-S25 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-exclude-028"></a> PE-G3-EXCLUDE-028 | MUST NOT | applicable | Every later Determination mechanism or observation | A later mechanism or observation MUST NOT be treated as creating, replacing or identifying the protocol-semantic completion boundary merely because it represents or reports a Determination. | PE-G3-SOURCE-S25, PE-G3-SOURCE-S30, PE-G3-SOURCE-S32, PE-G3-SOURCE-S42, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-exclude-029"></a> PE-G3-EXCLUDE-029 | MUST NOT | applicable | Every protocol-semantic atomicity interpretation | Protocol-semantic atomicity MUST NOT be inferred from or defined by implementation transaction atomicity, storage atomicity, event emission, response production, logging, persistence, consensus, rollback or any other implementation mechanism. | PE-G3-SOURCE-S25, PE-G3-SOURCE-S30, PE-G3-SOURCE-S43, PE-G3-SOURCE-S47 | PE-G3-TSE-SEMANTIC-DIFFERENCE-001 |
| <a id="pe-g3-tseexclude-001"></a> PE-G3-TSEEXCLUDE-001 | MUST NOT | applicable | ALWAYS | The successor correction MUST NOT invent a concrete mapping or profile where the closed registry is empty. | PE-G3-SOURCE-S69 | NONE |
| <a id="pe-g3-tseexclude-002"></a> PE-G3-TSEEXCLUDE-002 | MUST NOT | applicable | ALWAYS | A digest, commitment or identifier MUST NOT acquire semantic meaning from implementation convention. | PE-G3-SOURCE-S71, PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseexclude-003"></a> PE-G3-TSEEXCLUDE-003 | MUST NOT | applicable | ALWAYS | A failed U MUST NOT be repaired, resumed, reactivated, reinterpreted or converted into a committed occurrence. | PE-G3-SOURCE-S72 | NONE |
| <a id="pe-g3-tseexclude-004"></a> PE-G3-TSEEXCLUDE-004 | MUST NOT | applicable | ALWAYS | The protocol MUST NOT require a database, blockchain, consensus system, storage layout, lock, event model or rollback technology as protocol authority. | PE-G3-SOURCE-S72 | NONE |

## Complete Transition-State Equivalence Semantics

<a id="pe-protocol-specification-g3-sem-authority"></a>
### E266-SEM-AUTHORITY

Published Generation 2 remains complete, immutable and unchanged. Correction can occur only through a distinct future successor. Privacy Engine is the implementation-independent authority. I164 is one bounded Speak-up-appV3 implementation; Speak Up is one application adapter and use case. Neither may define, narrow, repair, replace or become the protocol. M remains zero until separately authorized protocol-owned mappings and profiles exist.

These are proposed successor construction rules. They do not change published Generation 2, select a real successor identity, create a real candidate, perform a lifecycle act or adopt I164. Evaluation completion alone produces D and its occurrence evidence atomically. Failure produces none. Protocol semantic atomicity does not mandate a database, chain, transaction, implementation or runtime.

The procedure listings specify finite byte algorithms. Python notation and synthetic test adapters carry no protocol authority. A different implementation must reproduce the specified bytes and decisions. Synthetic source authority identifiers and test keys are author vectors only. Source authority, source-owned definitions, authenticated current facts, privacy-evidence appointment and installation authorization must be obtained from their separately governing source; possession of a key never appoints authority. A missing authority fact rejects admission and cannot be inferred from implementation behavior.

<a id="pe-protocol-specification-g3-sem-registry"></a>
### E266-SEM-REGISTRY

Registry identifier: PE-G3-TRANSITION-MAPPING-REGISTRY-001.

Mapping identifier: PE-G3-TMAP-{NNNNNN}.

Profile identifier: PE-G3-TSE-PROFILE-{NNNNNN}-V0001.

The mapping and profile ordinals must be identical. One registry row binds exactly one mapping to exactly one profile. No mapping or profile can appear in more than one row. Replacement within one generation is prohibited.

The registry schema is:

registry_order, mapping_id, mapping_path, mapping_sha256, profile_id, profile_path, profile_sha256, applicability_definition_id, recovery_definition_id, status

Rows are ordered by registry_order contiguous from 000001 and equivalently by mapping_id byte order. status is closed-validated-normative-member. The empty serialization is exactly the header followed by LF and contains no data row. That empty registry authorizes zero transitions.


Mapping/profile byte admission precedes insertion. Registry order is ORD6 and unique mapping/profile ordinals agree. An admitted immutable profile is serialized as the container in E266-SEM-PRIVACY; its digest is computed before the mapping and registry that name it. Evidence of admission is external to that immutable container and signs its exact digest. M remains zero in this bounded 40-artifact construction. No sample mapping/profile is included as a candidate member.

<a id="pe-protocol-specification-g3-sem-types"></a>
### E266-SEM-TYPES

All text governed by this section is UTF-8 without BOM, Unicode NFC, LF-only, without trailing horizontal whitespace and with exactly one terminal LF. ASCII terminals are case-sensitive. Unsigned integers in text are canonical decimal: `0` or a non-zero digit followed by zero or more digits. Lowercase hexadecimal contains an even, non-zero number of characters from `0` through `9` and `a` through `f`.

The primitive type roots are exactly `PE-TSE-BOOL3`, `PE-TSE-BYTES`, `PE-TSE-ID` and `PE-TSE-UINT`. A derived type record has the exact TSV schema:

```text
type_order\ttype_id\tkind\telement_type_id\tfield_type_ids
```

`type_order` begins at `0001` and is contiguous. The four primitive roots occur first in the order shown. `kind` is `PRIMITIVE`, `SET` or `TUPLE`. A primitive row uses `NOT-APPLICABLE` in both final cells. A `SET` row names exactly one earlier type in `element_type_id` and uses `NOT-APPLICABLE` in `field_type_ids`. A `TUPLE` row uses `NOT-APPLICABLE` in `element_type_id` and names two or more earlier type IDs, comma-separated without spaces, in field order. Duplicate type IDs, forward references and cycles are invalid. There is no type whose literal identifier is `SET`.

Every typed value has one canonical octet encoding. `U32(n)` and `U64(n)` mean unsigned big-endian 32-bit and 64-bit encodings; overflow is invalid. `A(s)` means the ASCII bytes of `s`. `L32(x)` means `U32(len(x)) || x`; `L64(x)` means `U64(len(x)) || x`. The complete encoding is:

```text
A("TSEV1") || L32(A(type_id)) || kind_octet || L64(body)
```

The four primitive `kind_octet` values and bodies are:

| Type | Octet | Body |
|---|---|---|
| `PE-TSE-BOOL3` | `00` | `00` for FALSE, `01` for TRUE, `02` for UNRESOLVED |
| `PE-TSE-BYTES` | `01` | the represented octets, including the empty string when the owning component permits it |
| `PE-TSE-ID` | `02` | one nonempty ASCII identifier matching `[A-Za-z0-9][A-Za-z0-9._:#-]*`; its identity class applies its narrower grammar before encoding |
| `PE-TSE-UINT` | `03` | canonical decimal ASCII |

A derived `SET` uses `kind_octet = 10`. Its body is `U32(count)` followed by `L64(value)` for each distinct complete canonical element encoding, sorted by unsigned bytewise ascending order. A duplicate encoding is invalid. A derived `TUPLE` uses `kind_octet = 11`. Its body is `U32(field_count)` followed by `L64(value)` for each field in declared order. Each nested value must name the declared element or field type. These rules supply canonical bytes for every primitive and derived value.

The PE-TSE-EXPR-V2 grammar is the following complete ABNF; no Engineering[250] grammar is imported:

```text
expression = literal / argument / reference / tuple-expression / equal-expression / not-expression / and-expression / or-expression / member-expression / apply-expression / status-expression
literal = "literal(" type-id "," hex-bytes ")"
argument = "arg(" ord4 ")"
reference = "ref(" component-id "," side ")"
tuple-expression = "tuple(" type-id "," expression "," expression *( "," expression ) ")"
equal-expression = "equal(" expression "," expression ")"
not-expression = "not(" expression ")"
and-expression = "and(" expression *( "," expression ) ")"
or-expression = "or(" expression *( "," expression ) ")"
member-expression = "member(" expression "," definition-id ")"
apply-expression = "apply(" definition-id *( "," expression ) ")"
status-expression = status-op "(" component-id "," side ")"
status-op = "authoritative" / "available" / "valid" / "authenticated"
side = "AUTHORIZED" / "CURRENT"
ord4 = 4DIGIT
hex-bytes = 2HEXDIG *( 2HEXDIG )
```

ASCII space is prohibited inside an expression. `and` and `or` have at least one argument. `tuple` has at least two. `arg(0001)` denotes the first declared input; `0000`, an ordinal above the definition arity, or `arg` in a zero-input definition is invalid. `apply` evaluates argument expressions left-to-right, binds their canonical values to the callee's `arg` ordinals, and evaluates the callee in a new environment. No caller argument is visible except through those bindings.

`PE-TSE-SET` is a reserved built-in definition identifier and is not a definition record. It may occur only as `apply(PE-TSE-SET,<literal>...)` in a `SET` definition. Its arity is the number of literal arguments, including zero. All literals must have the output set type's element type; the result is the canonical set encoding above. `PE-TSE-SET` is forbidden in `definition_id`, source ownership and every other position.

E260 reserved-identifier completion: PE-TSE-SET is a reserved lexical identifier only for the admitted built-in apply position. Types, definitions, component/field/group IDs, source IDs/anchors, typed PE-TSE-ID values, Evaluation/Determination/read/evidence IDs and trusted appointment identifier fields must not equal it. Referenced type/definition names resolve only to admitted declarations. Opaque PE-TSE-BYTES data may contain arbitrary octets; this does not turn those octets into an identifier or prohibit documentary quotations. Literal SET is additionally forbidden as a type ID. The common identifier predicate and the admission/encoding callers below enforce this rule. Before any outer binding, revalidate_program rebuilds type declarations and the complete admitted program and checks its cached operation graph, so mutating a Python object cannot bypass declaration admission; source appointment cannot override it.

A literal is `literal(type-id,hex-bytes)`. `hex-bytes` decodes to one complete canonical typed-value encoding; its embedded `type_id` must equal the literal's `type-id`. A literal that is not canonical is invalid rather than normalized. `ref(component-id,side)` returns the component's authenticated represented value after its representation decoder, canonicalizer and normalizer have succeeded, as one complete canonical typed-value encoding of the component's `canonical_type_id`.

Definition records have the exact TSV schema:

```text
definition_order\tdefinition_id\tkind\tinput_type_ids\toutput_type_id\texpression\tsource_id\tsource_anchor
```

`definition_order` begins at `0001` and is contiguous. `kind` is `SET`, `CONDITION` or `FUNCTION`. `input_type_ids` is `NONE` or a comma-separated ordered list. A `SET` definition has `NONE` inputs, names an earlier derived type whose kind is `SET`, and has exactly one `apply(PE-TSE-SET,...)` expression. A `CONDITION` returns `PE-TSE-BOOL3`. A `FUNCTION` returns its declared type. Every definition names one owning successor source and anchor. Profile-local, implementation-owned and unresolved definitions are invalid. Admission uses the complete operation dependency graph generated by Profile._admit below, including member calls, every status stage and both component sides. Kahn traversal rejects any combined cycle. Definition IDs retain declared profile order for stable ordinals; it is the combined graph, not a contradictory reverse invocation ordering, that decides acyclicity.


Component records have the exact TSV schema:

```text
component_order\tcomponent_id\trepresented_type_id\trepresentation_decoder_definition_id\tcanonical_type_id\tcanonicalization_definition_id\tnormalization_definition_id\tauthority_source_id\tauthority_anchor\tavailability_condition_definition_id\tvalidity_condition_definition_id\tauthentication_definition_id\tprivacy_class\tobservability_class\tbinding_mode
```

`component_order` begins at `0001` and is contiguous. Every type and definition reference must resolve in the profile's closed type/definition tables. `privacy_class` is `PUBLIC`, `ACTION-BOUNDED` or `CONFIDENTIAL`. `observability_class` is `NONE`, `RESULT-ONLY` or `AUTHENTICATED-CONFIDENTIAL-COMPARISON-ONLY`. `binding_mode` is `CANONICAL-VALUE` or `BLINDED-SHA256-COMMITMENT`. The three condition/authentication definitions must return `PE-TSE-BOOL3`; decoder, canonicalizer and normalizer types must compose exactly from represented type to canonical type. `NONE` is forbidden in every component cell.

`apply` resolves either the reserved built-in above or one definition record, checks exact arity and input types, and evaluates it once in the bound argument environment. `member` requires a `SET` definition and compares complete canonical element encodings. `tuple(TYPE-ID,...)` constructs the explicitly named tuple type, including nested tuples, and requires its exact field count and types. The four status operators return `PE-TSE-BOOL3`. Failure, unavailable authority, failed authentication, invalid representation, noncanonical encoding, type failure or definition failure returns `NO-VALUE` for a non-Boolean result and `UNRESOLVED` for a Boolean result. `not`, `and` and `or` use Kleene strong three-valued truth tables. `equal` returns UNRESOLVED if either operand is NO-VALUE and otherwise compares complete canonical typed encodings. There are no other built-ins, references, substitutions, implicit conversions, collations, clocks, random sources or defaults.

The earlier scalar/profile ownership register remains:

Every profile contains the following scalar fields in this order:

profile-identifier, profile-version, governing-successor-generation, governing-mapping-identifier, profile-sha256-algorithm, projection-component-count, definition-count, equivalence-definition-id, material-conflict-definition-id, applicability-definition-id, determination-dependency-definition-id, comparison-timing-rule, execution-gate, commitment-gate, recovery-definition-id, privacy-classification, observability-classification

Field domains are:

- profile-identifier and governing-mapping-identifier use section 5 grammars and matching ordinals;
- profile-version is V0001;
- governing-successor-generation equals SUCCESSOR-GENERATION-ID;
- profile-sha256-algorithm is SHA-256;
- both counts are ORD6 canonical decimal counts matching their tables;
- every definition reference resolves uniquely within the profile;
- comparison-timing-rule is PRE-EXECUTION-AND-SEMANTIC-COMMITMENT;
- execution-gate and commitment-gate are EQUIVALENT-ONLY;
- privacy-classification is MINIMUM-ACTION-BOUNDED-NON-ACTOR;
- observability-classification is PUBLIC-RESULT-ONLY-NON-AUTHORITATIVE-DIAGNOSTICS.

The projection table schema is:

component_order, component_id, authoritative_source_id, authoritative_source_sha256, authoritative_source_anchor, component_type_definition_id, representation_definition_id, canonicalization_definition_id, normalization_definition_id, authorization_binding_mode, applicable_precondition_definition_ids, applicable_invariant_definition_ids, ordering_coordinate_definition_ids, dependency_coordinate_definition_ids, determination_dependency, equivalence_definition_id, immaterial_difference_definition_id, material_conflict_definition_id, authority_definition_id, availability_definition_id, validity_definition_id, authentication_definition_id, privacy_definition_id, observability_definition_id

component_order is contiguous ORD6. component_id uses LOCAL-ID and is unique. Definition lists are ordered comma-separated identifiers or NONE. authorization_binding_mode is CANONICAL-VALUE or BLINDED-SHA256-COMMITMENT. determination_dependency is INCLUDED or EXCLUDED and must agree with the determination-dependency definition.

The recovery table schema is:

recovery_order, stage, trigger, prerequisite_definition_id, disposition

stage is PRE-EXECUTION, EXECUTION or PRE-COMMITMENT. trigger is MATERIAL-CONFLICT, INDETERMINATE, EXECUTION-FAILURE or REVALIDATION-FAILURE. disposition is NEW-U-FROM-UNCHANGED-D or NEW-E-NEW-D-NEW-U. Rows are contiguous and must implement section 12's total function.

Profile validation rejects the profile unless every count, identity, digest, reference, type, expression, source anchor and cross-field constraint validates; the projection is proven minimal for the mapping; equivalence and conflict cannot both be true; every complete valid input is covered; every incomplete or untrusted evaluation becomes indeterminate; and no implementation-selected choice remains.


The E248 projection table describes the source-owned mapping obligations. Its component identity/order joins the E252 component program table one-to-one; canonical type, representation, canonicalization, normalization, conditions, source authority and binding mode must agree. E256 replaces E248's abbreviated recovery table with the exact 21-row function in E266-SEM-RECOVERY. The canonical spelling of the blinded mode is BLINDED-SHA256-COMMITMENT. CANONICAL-VALUE remains admitted. A legacy BLINDED-SHA256 input is migrated once at the component-mode boundary; serialized output always uses the canonical spelling.

The following complete executable notation governs V2 parsing, synthesis, all operation signatures, evaluation and occurrence bytes. Its dataclass defaults are confined to author fixtures; real source-owned rows must supply source and anchor explicitly and satisfy authenticated source ownership. ReadObject flags mean independently validated source facts, never assertions accepted from an unauthenticated caller. Invalid/missing source validation produces no successful Evaluation package; a comparison at a gate maps such validation failure to indeterminate under E266-SEM-COMPARISON.

### Constructor module: expr_v2.py

````python
"""E256 proposed deterministic expression/transcript construction.

This author model takes source-authenticated read objects as explicit inputs.
It does not appoint a source authority or infer authentication from a signature.
No profile or successor identity is selected by importing this module.
"""
from dataclasses import dataclass
from hashlib import sha256
import re
import json

NA='NOT-APPLICABLE'
B='PE-TSE-BOOL3';Y='PE-TSE-BYTES';I='PE-TSE-ID';U='PE-TSE-UINT'
PRIMITIVES=(B,Y,I,U)
ID=re.compile(r'[A-Za-z0-9][A-Za-z0-9._:#-]*\Z')
BUILTIN='PE-TSE-SET'
H=lambda b:sha256(b).hexdigest()
def need(ok,reason):
    if not ok:raise ValueError(reason)
def identifier(value):
    return isinstance(value,str) and bool(ID.fullmatch(value)) and value!=BUILTIN

def uint(n,width):
    need(isinstance(n,int) and 0<=n<1<<(8*width),'integer overflow')
    return n.to_bytes(width,'big')
def lp(b,width=8):return uint(len(b),width)+b
def tsv(header,rows):
    lines=[header,*rows]
    need(all(len(r)==len(header) for r in lines),'TSV arity')
    need(all(isinstance(c,str) and not any(x in c for x in '\t\r\n') for r in lines for c in r),'TSV cell')
    return ''.join('\t'.join(r)+'\n' for r in lines).encode()

class Types:
    def __init__(self,derived=()):
        self.rows={x:('PRIMITIVE',()) for x in PRIMITIVES}
        for name,kind,children in derived:
            need(identifier(name) and name not in self.rows and name!='SET','type identifier')
            need(kind in ('SET','TUPLE') and len(children)>=(1 if kind=='SET' else 2),'derived kind/arity')
            need(kind!='SET' or len(children)==1,'set arity')
            need(all(c in self.rows for c in children),'forward type')
            self.rows[name]=(kind,tuple(children))
    def encode(self,t,v):
        need(t in self.rows,'unknown type');kind,children=self.rows[t]
        if t==B:need(type(v)==int and v in (0,1,2),'BOOL3');octet=0;body=bytes([v])
        elif t==Y:need(isinstance(v,bytes),'BYTES');octet=1;body=v
        elif t==I:need(identifier(v),'ID');octet=2;body=v.encode('ascii')
        elif t==U:need(type(v)==int and v>=0,'UINT');octet=3;body=str(v).encode()
        elif kind=='SET':
            octet=16;values=sorted(v);need(len(values)==len(set(values)),'duplicate set value')
            for a in values:need(self.decode(a)[0]==children[0],'set element type')
            body=uint(len(values),4)+b''.join(lp(a) for a in values)
        else:
            octet=17;need(len(v)==len(children),'tuple arity')
            for a,c in zip(v,children):need(self.decode(a)[0]==c,'tuple field type')
            body=uint(len(v),4)+b''.join(lp(a) for a in v)
        return b'TSEV1'+lp(t.encode('ascii'),4)+bytes([octet])+lp(body)
    def decode(self,b):
        need(isinstance(b,bytes) and b.startswith(b'TSEV1'),'value header');pos=5
        def take(n):
            nonlocal pos
            need(pos+n<=len(b),'truncated value');v=b[pos:pos+n];pos+=n;return v
        def length(w):return int.from_bytes(take(w),'big')
        t=take(length(4)).decode('ascii');octet=take(1)[0];body=take(length(8));need(pos==len(b),'trailing value')
        need(t in self.rows,'value type');kind,children=self.rows[t]
        if t==B:need(len(body)==1 and body[0] in (0,1,2),'BOOL3 body');v=body[0]
        elif t==Y:v=body
        elif t==I:v=body.decode('ascii');need(bool(ID.fullmatch(v)),'ID body')
        elif t==U:need(bool(re.fullmatch(rb'0|[1-9][0-9]*',body)),'UINT body');v=int(body)
        else:
            need(len(body)>=4,'derived body');count=int.from_bytes(body[:4],'big');q=4;v=[]
            for _ in range(count):
                need(q+8<=len(body),'derived length');n=int.from_bytes(body[q:q+8],'big');q+=8
                need(q+n<=len(body),'derived data');v.append(body[q:q+n]);q+=n
            need(q==len(body),'derived trailing')
        # encode validates nested values, discriminator, canonical sort and grammar.
        need(self.encode(t,v)==b,'noncanonical value');return t,v

def parse(text):
    need(isinstance(text,str) and text.isascii() and not any(c.isspace() for c in text),'expression bytes')
    pos=0
    def atom():
        nonlocal pos
        start=pos
        while pos<len(text) and text[pos] not in ',()':pos+=1
        s=text[start:pos];need(bool(s),'empty expression token')
        if pos<len(text) and text[pos]=='(':
            pos+=1;args=[]
            if pos<len(text) and text[pos]!=')':
                while True:
                    args.append(atom())
                    if pos<len(text) and text[pos]==',':pos+=1;continue
                    break
            need(pos<len(text) and text[pos]==')','expression closing');pos+=1
            return (s,*args)
        return s
    value=atom();need(pos==len(text) and isinstance(value,tuple),'expression root');return value

@dataclass(frozen=True)
class Definition:
    id:str
    inputs:tuple
    output:str
    expression:tuple
    kind:str='FUNCTION'
    source:str='SYNTHETIC-SOURCE'
    anchor:str='synthetic-definition'

@dataclass(frozen=True)
class Component:
    id:str
    represented:str
    canonical:str
    decoder:str
    canonicalizer:str
    normalizer:str
    available:str
    valid:str
    authenticated:str
    source:str='SYNTHETIC-SOURCE'
    anchor:str='synthetic-component'

@dataclass(frozen=True)
class Field:
    id:str
    type:str
    equality:str
    source:str
    anchor:str

@dataclass(frozen=True)
class ReadObject:
    object_id:str
    value:bytes
    source:str
    anchor:str
    evidence_id:str
    evidence:bytes
    endpoint:bytes
    authoritative:bool=True
    valid:bool=True
    authenticated:bool=True

SIDES=('AUTHORIZED','CURRENT')
STAGES=('AUTHORITATIVE','AVAILABLE','VALID','AUTHENTICATED','DECODE','CANONICALIZE','NORMALIZE','PROJECT')
STATUSES={x.lower():x for x in STAGES[:4]}
EVENT_HEADER='event_order evaluation_id determination_id event_kind operation_id parent_event_order field_id object_id canonical_type_id canonical_sha256 authority_source_id authority_anchor authentication_evidence_id result'.split()
OP_HEADER='operation_order operation_id operation_kind expression_owner_id permitted_read_field_ids permitted_call_operation_ids owner_source_id owner_anchor'.split()

class Profile:
    def __init__(self,types,definitions,components,fields,root_definition,root_fields,groups=()):
        self.types=types;self.defs={d.id:d for d in definitions};self.components={c.id:c for c in components}
        need(len(definitions)<=9999 and len(components)<=9999,'profile ordinal overflow')
        need(len(self.defs)==len(definitions) and len(self.components)==len(components),'duplicate profile ID')
        self.def_order={d.id:i for i,d in enumerate(definitions,1)}
        self.comp_order={c.id:i for i,c in enumerate(components,1)}
        self.fields={f.id:f for f in fields};need(len(self.fields)==len(fields),'duplicate field')
        self.root_definition=root_definition;self.root_fields=tuple(root_fields);self.groups=tuple(groups)
        self.ops={};self.graph={};self._admit()
    def dop(self,d):return 'PE-TSE-OP-DEFINITION-'+f'{self.def_order[d]:04}'
    def sop(self,c,side,stage):return f'PE-TSE-OP-COMPONENT-{self.comp_order[c]:04}-{side}-{stage}'
    def fid(self,c,side,part):return f'PE-TSE-FIELD-COMPONENT-{self.comp_order[c]:04}-{side}-{part}'
    def synth(self,e,env,owner):
        need(isinstance(e,tuple) and len(e)>0,'AST node');op,*a=e
        def sub(x):return self.synth(x,env,owner)
        if op=='literal':
            need(len(a)==2 and a[0] in self.types.rows and isinstance(a[1],str) and bool(re.fullmatch('[0-9a-f]+',a[1])) and len(a[1])%2==0,'literal')
            need(self.types.decode(bytes.fromhex(a[1]))[0]==a[0],'literal type');return a[0]
        if op=='arg':
            need(len(a)==1 and isinstance(a[0],str) and bool(re.fullmatch('[0-9]{4}',a[0])) and 1<=int(a[0])<=len(env),'argument');return env[int(a[0])-1]
        if op=='ref' or op in STATUSES:
            need(len(a)==2 and a[0] in self.components and a[1] in SIDES,'component reference');return self.components[a[0]].canonical if op=='ref' else B
        if op=='tuple':
            need(len(a)>=3 and a[0] in self.types.rows,'tuple type');kind,children=self.types.rows[a[0]]
            need(kind=='TUPLE' and tuple(sub(x) for x in a[1:])==children,'tuple check');return a[0]
        if op=='equal':need(len(a)==2 and sub(a[0])==sub(a[1]),'equal types');return B
        if op in ('not','and','or'):
            need(len(a)>0 and (op!='not' or len(a)==1) and all(sub(x)==B for x in a),'logical operands');return B
        if op=='member':
            need(len(a)==2 and a[1] in self.defs,'member definition');d=self.defs[a[1]]
            need(d.kind=='SET' and sub(a[0])==self.types.rows[d.output][1][0],'member type');return B
        if op=='apply':
            need(len(a)>=1,'apply arity')
            if a[0]=='PE-TSE-SET':
                need(owner.kind=='SET' and e==owner.expression,'SET position');kind,children=self.types.rows[owner.output]
                need(kind=='SET' and all(isinstance(x,tuple) and x[0]=='literal' and sub(x)==children[0] for x in a[1:]),'SET literals');return owner.output
            need(a[0] in self.defs,'callee');d=self.defs[a[0]]
            need(tuple(sub(x) for x in a[1:])==d.inputs,'callee arguments');return d.output
        raise ValueError('unknown operator')
    def _ast_targets(self,e):
        reads=set();calls=set();op,*a=e
        if op in ('ref',*STATUSES):calls.add(self.sop(a[0],a[1],'PROJECT' if op=='ref' else STATUSES[op]))
        elif op=='apply' and a[0]!='PE-TSE-SET':calls.add(self.dop(a[0]))
        elif op=='member':calls.add(self.dop(a[1]))
        for x in a:
            if isinstance(x,tuple):
                r,c=self._ast_targets(x);reads|=r;calls|=c
        return reads,calls
    def _admit(self):
        # The built-in token is not an identifier in any declared ownership,
        # type, field, component, group or occurrence identity position.
        for d in self.defs.values():
            need(all(identifier(x) for x in (d.id,d.source,d.anchor)),'definition identifiers')
        for c in self.components.values():
            need(all(identifier(x) for x in (c.id,c.source,c.anchor)),'component identifiers')
        for f in self.fields.values():
            need(all(identifier(x) for x in (f.id,f.source,f.anchor)),'field identifiers')
        for gid,_,_ in self.groups:need(identifier(gid),'group identifier')
        need(self.root_definition in self.defs and all(f in self.fields for f in self.root_fields),'root binding')
        need(tuple(self.fields[f].type for f in self.root_fields)==self.defs[self.root_definition].inputs,'root input signature')
        for d in self.defs.values():
            need(d.id!='PE-TSE-SET' and bool(ID.fullmatch(d.id)) and d.kind in ('FUNCTION','CONDITION','SET'),'definition header')
            need(all(t in self.types.rows for t in (*d.inputs,d.output)),'definition types')
            need(d.kind!='CONDITION' or d.output==B,'condition result')
            need(d.kind!='SET' or (not d.inputs and self.types.rows[d.output][0]=='SET' and d.expression[0:2]==('apply','PE-TSE-SET')),'SET definition')
            need(self.synth(d.expression,d.inputs,d)==d.output,'definition result')
            if d.kind=='SET':self.types.encode(d.output,[bytes.fromhex(x[2]) for x in d.expression[2:]])
        for c in self.components.values():
            need(c.represented in self.types.rows and c.canonical in self.types.rows,'component types')
            for name,ins,out in [(c.decoder,(c.represented,),c.canonical),(c.canonicalizer,(c.canonical,),c.canonical),(c.normalizer,(c.canonical,),c.canonical),(c.available,(B,),B),(c.valid,(B,),B),(c.authenticated,(B,),B)]:
                need(name in self.defs and self.defs[name].inputs==ins and self.defs[name].output==out,'stage signature')
            for side in SIDES:
                for part,t in [('REPRESENTATION',c.represented),('VALUE',c.canonical),*[(f'STATUS-{s}',B) for s in STAGES[:4]]]:
                    f=self.fid(c.id,side,part)
                    need(f in self.fields and self.fields[f].type==t,'component field')
        def add(op,kind,owner,reads,calls,source,anchor):
            need(op not in self.ops,'operation duplicate')
            self.ops[op]=(kind,owner,set(reads),set(calls),source,anchor);self.graph[op]=set(calls)
        root=self.defs[self.root_definition]
        add('PE-TSE-OP-ROOT','EVALUATION-ROOT',root.id,self.root_fields,[self.dop(root.id)],root.source,root.anchor)
        for d in self.defs.values():
            reads,calls=self._ast_targets(d.expression);add(self.dop(d.id),'DEFINITION',d.id,reads,calls,d.source,d.anchor)
        for c in self.components.values():
            for side in SIDES:
                for stage in STAGES:
                    reads=[];calls=[]
                    if stage in STAGES[:4]:
                        reads=[self.fid(c.id,side,'STATUS-'+stage)]
                        if stage!='AUTHORITATIVE':calls=[self.dop(getattr(c,stage.lower()))]
                    elif stage=='DECODE':reads=[self.fid(c.id,side,'REPRESENTATION')];calls=[self.dop(c.decoder)]
                    elif stage=='CANONICALIZE':calls=[self.sop(c.id,side,'DECODE'),self.dop(c.canonicalizer)]
                    elif stage=='NORMALIZE':calls=[self.sop(c.id,side,'CANONICALIZE'),self.dop(c.normalizer)]
                    else:
                        reads=[self.fid(c.id,side,'VALUE')]
                        calls=[self.sop(c.id,side,s) for s in (*STAGES[:4],'NORMALIZE')]
                    add(self.sop(c.id,side,stage),'COMPONENT-STAGE',c.id,reads,calls,c.source,c.anchor)
        seen_fields=set()
        for gid,fields,rule in self.groups:
            need(len(fields)>=2 and len(set(fields))==len(fields) and not seen_fields.intersection(fields),'identity group fields')
            need(all(f in self.fields for f in fields),'identity group field reference');seen_fields.update(fields)
            ts={self.fields[f].type for f in fields};need(len(ts)==1 and rule in self.defs,'identity group type')
            need(len({self.fields[f].equality for f in fields})==1,'identity group semantic equality')
            d=self.defs[rule];t=next(iter(ts));need(d.inputs==(t,t) and d.output==B,'identity rule signature')
            self.ops['PE-TSE-OP-ROOT'][3].add(self.dop(rule));self.graph['PE-TSE-OP-ROOT'].add(self.dop(rule))
        # The complete operation graph includes status-definition and ref-stage edges.
        pending={k:set(v) for k,v in self.graph.items()};self.topology=[]
        need(all(v in pending for edges in pending.values() for v in edges),'unknown operation edge')
        while pending:
            ready=sorted(k for k,v in pending.items() if not v)
            need(bool(ready),'combined operation cycle');k=ready[0];self.topology.append(k);del pending[k]
            for edges in pending.values():edges.discard(k)
        for d in self.defs.values():
            def walk(e):
                op,*a=e
                if op=='member':need(self.def_order[a[1]]<self.def_order[d.id],'definition forward reference')
                if op=='apply' and a[0]!='PE-TSE-SET':need(self.def_order[a[0]]<self.def_order[d.id],'definition forward reference')
                for x in a:
                    if isinstance(x,tuple):walk(x)
            walk(d.expression)
        # Identity and semantic equality rules are pure: no external read or stage.
        def pure(op):
            reachable=set();todo=[op]
            while todo:
                x=todo.pop()
                if x in reachable:continue
                reachable.add(x);need(self.ops[x][0]=='DEFINITION' and not self.ops[x][2],'impure equality');todo.extend(self.graph[x])
        for _,_,rule in self.groups:pure(self.dop(rule))
        for f in self.fields.values():
            need(f.type in self.types.rows and f.equality in self.defs,'field type/equality')
            d=self.defs[f.equality];need(d.inputs==(f.type,f.type) and d.output==B,'semantic equality signature');pure(self.dop(d.id))
    def operation_bytes(self):
        return tsv(OP_HEADER,[[f'{i:04}',op,kind,owner,','.join(sorted(reads)) or 'NONE',','.join(sorted(calls)) or 'NONE',source,anchor] for i,(op,(kind,owner,reads,calls,source,anchor)) in enumerate(self.ops.items(),1)])


def revalidate_program(program):
    """Re-admit declarative rows before outer binding; mutable Python caches
    are not evidence that the immutable serialized program was admitted.
    """
    rows=list(program.types.rows.items())
    need([name for name,_ in rows[:4]]==list(PRIMITIVES),'primitive order')
    types=Types([(name,kind,children) for name,(kind,children) in rows[4:]])
    need(list(types.rows.items())==rows,'canonical type declarations')
    rebuilt=Profile(types,list(program.defs.values()),list(program.components.values()),list(program.fields.values()),program.root_definition,program.root_fields,program.groups)
    for name in ('defs','components','fields','def_order','comp_order','ops','graph','topology'):
        need(getattr(program,name)==getattr(rebuilt,name),('program re-admission',name))
    return rebuilt

class Evaluation:
    def __init__(self,p,objects,eid='SYNTHETIC-E',did='SYNTHETIC-D'):
        need(identifier(eid) and identifier(did),'occurrence identifiers')
        self.p=p;self.objects=objects;self.eid=eid;self.did=did;self.events=[];self.stack=[]
        self.invocations={};self.values={};self.reads={};self.returns={};self.group_instances=[];self.completed=None
    def event(self,kind,op,parent,field=NA,obj=NA,t=NA,digest=NA,source=NA,anchor=NA,auth=NA,result=NA):
        order=f'{len(self.events)+1:06}'
        self.events.append([order,self.eid,self.did,kind,op,f'{parent:06}',field,obj,t,digest,source,anchor,auth,result]);return int(order)
    def value_cells(self,v):
        if v is None:return NA,NA,'NO-VALUE'
        t,x=self.p.types.decode(v);self.values[H(v)]=v
        return t,H(v),('FALSE','TRUE','UNRESOLVED')[x] if t==B else 'VALUE'
    def read(self,field):
        op,enter=self.stack[-1];need(field in self.p.ops[op][2],'unadmitted read');f=self.p.fields[field]
        o=self.objects.get(field);need(o is not None,'missing authenticated read object')
        need(o.authoritative and o.valid and o.authenticated,'invalid read validation')
        need((o.source,o.anchor)==(f.source,f.anchor),'read authority')
        need(identifier(o.object_id) and identifier(o.evidence_id) and bool(o.evidence) and bool(o.endpoint),'read evidence')
        need(self.p.types.decode(o.value)[0]==f.type,'read canonical type')
        t,dg,result=self.value_cells(o.value)
        n=self.event('READ',op,enter,field,o.object_id,t,dg,o.source,o.anchor,o.evidence_id,result)
        self.reads[n]=(field,o);return o.value
    def invoke(self,op,args=(),root=False):
        kind,owner,_,_,source,anchor=self.p.ops[op]
        need(all(a is not None for a in args),'unresolved argument environment')
        bundle=uint(len(args),4)+b''.join(lp(a) for a in args)
        encoded=self.p.types.encode(Y,bundle);dg=H(encoded);self.values[dg]=encoded
        if root:parent=0;obj=self.eid+'-INPUT-000000'
        else:
            caller,ce=self.stack[-1];need(op in self.p.ops[caller][3],'unadmitted call')
            parent=self.event('CALL',op,ce,obj=self.eid+f'-INPUT-{len(self.events)+1:06}',t=Y,digest=dg,source=source,anchor=anchor,result='ARGUMENTS')
            obj=self.events[parent-1][7]
        self.invocations[obj]=encoded
        enter=self.event('ENTER',op,parent,obj=obj,t=Y,digest=dg,source=source,anchor=anchor,result='ARGUMENTS')
        self.stack.append((op,enter))
        if kind=='EVALUATION-ROOT':
            values=[self.read(f) for f in self.p.root_fields]
            result=self.invoke(self.p.dop(self.p.root_definition),values)
            self.make_groups()
        elif kind=='DEFINITION':
            d=self.p.defs[owner];need(tuple(self.p.types.decode(a)[0] for a in args)==d.inputs,'invocation argument types')
            result=self.eval(d.expression,args,d)
        else:result=self.stage(op)
        t,dg,res=self.value_cells(result)
        ret=self.event('RETURN',op,enter,obj=self.eid+f'-OP-{enter:06}',t=t,digest=dg,source=source,anchor=anchor,result=res)
        self.returns[enter]=(ret,result);self.stack.pop();return result
    def missing(self,t):return self.p.types.encode(B,2) if t==B else None
    def eval(self,e,args,owner):
        op,*a=e;T=self.p.types
        def ev(x):return self.eval(x,args,owner)
        if op=='literal':return bytes.fromhex(a[1])
        if op=='arg':return args[int(a[0])-1]
        if op=='ref' or op in STATUSES:return self.invoke(self.p.sop(a[0],a[1],'PROJECT' if op=='ref' else STATUSES[op]))
        if op=='tuple':
            v=[ev(x) for x in a[1:]];return None if any(x is None for x in v) else T.encode(a[0],v)
        if op=='equal':
            left=ev(a[0]);right=ev(a[1]);return T.encode(B,2 if left is None or right is None else int(left==right))
        if op=='not':
            x=T.decode(ev(a[0]))[1];return T.encode(B,{0:1,1:0,2:2}[x])
        if op in ('and','or'):
            seen=[]
            for x in a:
                v=T.decode(ev(x))[1];seen.append(v)
                if (op=='and' and v==0) or (op=='or' and v==1):return T.encode(B,v)
            return T.encode(B,2 if 2 in seen else (1 if op=='and' else 0))
        if op=='member':
            v=ev(a[0]);s=self.invoke(self.p.dop(a[1]));return T.encode(B,2 if v is None or s is None else int(v in T.decode(s)[1]))
        if op=='apply':
            v=[ev(x) for x in a[1:]]
            if a[0]=='PE-TSE-SET':return T.encode(owner.output,v)
            d=self.p.defs[a[0]]
            return self.missing(d.output) if any(x is None for x in v) else self.invoke(self.p.dop(d.id),v)
        raise ValueError('unhandled admitted expression')
    def stage(self,op):
        _,cid,_,_,_,_=self.p.ops[op];c=self.p.components[cid]
        tail=op.split(f'-{self.p.comp_order[cid]:04}-',1)[1];side,stage=tail.split('-',1)
        def call(s):return self.invoke(self.p.sop(cid,side,s))
        if stage in STAGES[:4]:
            value=self.read(self.p.fid(cid,side,'STATUS-'+stage))
            return value if stage=='AUTHORITATIVE' else self.invoke(self.p.dop(getattr(c,stage.lower())),[value])
        if stage=='DECODE':return self.invoke(self.p.dop(c.decoder),[self.read(self.p.fid(cid,side,'REPRESENTATION'))])
        if stage in ('CANONICALIZE','NORMALIZE'):
            value=call('DECODE' if stage=='CANONICALIZE' else 'CANONICALIZE')
            return self.missing(c.canonical) if value is None else self.invoke(self.p.dop(c.canonicalizer if stage=='CANONICALIZE' else c.normalizer),[value])
        for s in STAGES[:4]:
            if self.p.types.decode(call(s))[1]!=1:return self.missing(c.canonical)
        value=call('NORMALIZE');expected=self.read(self.p.fid(cid,side,'VALUE'))
        return value if value==expected else self.missing(c.canonical)
    def make_groups(self):
        for gid,fields,rule in self.p.groups:
            members=[n for n,(f,o) in self.reads.items() if f in fields]
            if len(members)<2:continue
            for i,a in enumerate(members):
                for b in members[i+1:]:
                    x=self.reads[a][1];y=self.reads[b][1]
                    need((x.source,x.anchor,x.value)==(y.source,y.anchor,y.value),'alias authority/value mismatch')
                    result=self.invoke(self.p.dop(rule),[x.value,y.value])
                    need(self.p.types.decode(result)==(B,1),'identity rule failed')
            self.group_instances.append((gid,tuple(members)))
    def run(self):
        try:
            value=self.invoke('PE-TSE-OP-ROOT',root=True)
            need(value is not None and self.p.types.decode(value)!=(B,2),'Evaluation incomplete')
            t,dg,result=self.value_cells(value);root=self.p.defs[self.p.root_definition]
            self.event('DETERMINATION','PE-TSE-OP-ROOT',1,obj=self.did,t=t,digest=dg,source=root.source,anchor=root.anchor,result=result)
            transcript=tsv(EVENT_HEADER,self.events)
            package=self.graph_bytes(transcript,value)
            self.completed=dict(transcript=transcript,determination=value,**package)
            return self.completed
        except Exception:
            self.completed=None
            raise
    def graph_bytes(self,transcript,determination):
        T=self.p.types;nodes={};edges=[];alias={};group_rows=[]
        rid=lambda n:self.eid+f'-READ-{n:06}'
        for i,(gid,members) in enumerate(self.group_instances,1):
            ids=[rid(n) for n in members];representative=min(ids)
            for node in ids:alias[node]=representative
            group_rows.append([f'{i:06}',self.eid+f'-IG-{i:06}',gid,','.join(ids),'TRUE'])
        def node(id,kind,value,obj,source,anchor,equality,aliases=()):
            t,_=T.decode(value)
            envelope=b''.join(lp(x.encode(),4) for x in [id,obj,t,H(value),source,anchor,*aliases])
            nodes[id]=(kind,value,obj,source,anchor,equality,tuple(aliases),envelope)
        root=self.p.defs[self.p.root_definition]
        node(self.did,'DETERMINATION',determination,self.did,root.source,root.anchor,'BYTE-IDENTITY')
        tid=self.eid+'-TRANSCRIPT';node(tid,'TRANSCRIPT',T.encode(Y,transcript),tid,root.source,root.anchor,'BYTE-IDENTITY')
        def edge(a,b,k,n,field):edges.append([a,b,k,f'{n:06}',field])
        for event in self.events:
            n=int(event[0]);kind=event[3];op=event[4];parent=int(event[5])
            if kind=='ENTER':
                oid=self.eid+f'-OP-{n:06}';ret,value=self.returns[n];t,dg,_=self.value_cells(value)
                body=lp(op.encode(),4)+uint(n,8)+lp(t.encode(),4)+lp(dg.encode(),4)
                source,anchor=self.p.ops[op][4:]
                node(oid,'OPERATION',T.encode(Y,body),op,source,anchor,'BYTE-IDENTITY')
                if parent==0:edge(self.did,oid,'DEFINITION',n,'determination')
                else:
                    caller=int(self.events[parent-1][5]);edge(self.eid+f'-OP-{caller:06}',oid,'DEFINITION',parent,'callee')
            elif kind=='READ':
                field,o=self.reads[n];raw=rid(n);id=alias.get(raw,raw)
                if id not in nodes:
                    members=[r for r,a in alias.items() if a==id] or [raw]
                    objects=sorted({self.reads[int(r.rsplit('-',1)[1])][1].object_id for r in members})
                    node(id,'READ',o.value,','.join(objects),o.source,o.anchor,self.p.fields[field].equality,sorted(members))
                aid=self.eid+f'-AUTH-{n:06}';sid=self.eid+f'-SOURCE-{n:06}'
                node(aid,'AUTHENTICATION',T.encode(Y,o.evidence),o.evidence_id,o.source,o.anchor,'BYTE-IDENTITY')
                node(sid,'AUTHORITY',T.encode(Y,o.endpoint),o.source,o.source,o.anchor,'BYTE-IDENTITY')
                edge(self.eid+f'-OP-{parent:06}',id,'VALUE',n,'value');edge(id,aid,'AUTHENTICATION',n,'authentication');edge(id,sid,'AUTHORITY',n,'authority')
            elif kind=='DETERMINATION':edge(self.did,tid,'PRODUCTION',n,'transcript')
        seen=set();unique=[]
        for e in edges:
            need(e[0] in nodes and e[1] in nodes and e[0]!=e[1],'edge endpoints')
            if tuple(e) not in seen:seen.add(tuple(e));unique.append(e)
        graph={n:set() for n in nodes}
        for a,b,*_ in unique:graph[a].add(b)
        todo=[self.did];closure=set()
        def visit(n,active):
            need(n not in active,'occurrence graph cycle')
            if n in closure:return
            active.add(n)
            for x in sorted(graph[n]):visit(x,active)
            active.remove(n);closure.add(n)
        visit(self.did,set());need(closure==set(nodes),'orphan occurrence node')
        node_rows=[];value_rows=[]
        for i,(id,(kind,value,obj,source,anchor,eq,aliases,envelope)) in enumerate(nodes.items(),1):
            node_rows.append([f'{i:06}',id,','.join(aliases) or 'NONE',obj,kind,T.decode(value)[0],H(value),H(envelope),source,anchor,eq])
            value_rows.append([id,value.hex(),envelope.hex()])
        return dict(
            groups=tsv('group_order identity_group_id group_template_id member_read_occurrence_ids identity_rule_result'.split(),group_rows),
            nodes=tsv('node_order node_id alias_read_occurrence_ids source_object_ids node_class canonical_type_id canonical_sha256 envelope_sha256 authority_source_id authority_anchor semantic_equality_definition_id'.split(),node_rows),
            values=tsv('node_id canonical_value_hex metadata_envelope_hex'.split(),value_rows),
            edges=tsv('edge_order from_node_id to_node_id dependency_class transcript_event_order production_field'.split(),[[f'{i:06}',*r] for i,r in enumerate(unique,1)]),
            invocations=tsv('invocation_id canonical_arguments_hex'.split(),[[k,v.hex()] for k,v in self.invocations.items()]),
            dep=tsv(['node_id'],[[n] for n in sorted(closure)]))

def replay(profile,objects,package,eid='SYNTHETIC-E',did='SYNTHETIC-D'):
    expected=Evaluation(profile,objects,eid,did).run()
    need(set(package)==set(expected) and all(package[k]==v for k,v in expected.items()),'occurrence replay mismatch')
    return True

def unchanged(profile,package,refreshed_objects,node_validation):
    """BOOL3 unchangedness; complete fresh authority/validity/authentication status.

    node_validation is source-validated evidence, with exactly one 0/1/2 value
    per existing closure node. It does not derive current authority from logs.
    Missing fresh object means unavailable (2); a proved mismatch dominates (0).
    """
    import csv,io
    rows=lambda b:list(csv.DictReader(io.StringIO(b.decode()),delimiter='\t'))
    nodes=rows(package['nodes']);ids={n['node_id'] for n in nodes}
    need(set(node_validation)==ids and all(type(x)==int and x in (0,1,2) for x in node_validation.values()),'fresh node validation domain')
    oldvalues={r['node_id']:bytes.fromhex(r['canonical_value_hex']) for r in rows(package['values'])}
    events={r['event_order']:r for r in rows(package['transcript']) if r['event_kind']=='READ'}
    unresolved=False
    for n in nodes:
        status=node_validation[n['node_id']]
        if status==0:return 0
        if status==2:unresolved=True;continue
        if n['node_class']!='READ':continue
        prior=oldvalues[n['node_id']]
        for alias in n['alias_read_occurrence_ids'].split(','):
            event=events[alias.rsplit('-',1)[1]];o=refreshed_objects.get(event['field_id'])
            if o is None:unresolved=True;continue
            if not (o.authoritative and o.valid and o.authenticated):return 0
            if (o.object_id,o.source,o.anchor)!=(event['object_id'],event['authority_source_id'],event['authority_anchor']):return 0
            try:t,_=profile.types.decode(o.value)
            except (ValueError,UnicodeError):return 0
            if t!=n['canonical_type_id'] or H(o.value)!=n['canonical_sha256']:return 0
            runner=Evaluation(profile,{})
            result=runner.invoke(profile.dop(n['semantic_equality_definition_id']),[prior,o.value],root=True)
            truth=profile.types.decode(result)[1]
            if truth==0:return 0
            if truth==2:unresolved=True
    return 2 if unresolved else 1
````

<a id="pe-protocol-specification-g3-sem-dependency"></a>
### E266-SEM-DEPENDENCY

The expr_v2 module in E266-SEM-TYPES is the exact E256 dependency constructor. Its OP_HEADER and EVENT_HEADER are literal ordered schemas; permitted read fields and permitted call operations are separate columns. Operation IDs are generated by dop and sop, root first, definitions in declared order, then component order, AUTHORIZED before CURRENT and STAGES order. Root arguments are reads of root_fields in that order. Every invocation stores the full canonical argument bundle; ENTER/CALL/RETURN events name its digest and exact bytes remain in the arguments table.

Component PROJECT first tests AUTHORITATIVE, AVAILABLE, VALID and AUTHENTICATED, then NORMALIZE and the authenticated canonical VALUE field. DECODE reads REPRESENTATION; CANONICALIZE calls DECODE; NORMALIZE calls CANONICALIZE. Each named function receives the one typed result of its preceding stage. The authenticated VALUE must equal normalized bytes. Status fields are real READ occurrences with source and evidence edges. Member calls invoke the zero-input SET operation and are recorded even when returning an empty set.

The Evaluation methods define every event cell, not an issuer-selected subset. A skipped branch produces no events. Each READ has a distinct event occurrence ID, even when object IDs repeat. Group templates expand to actual matching READ occurrence IDs; at least two observed members are required to form an instance. The pure typed binary identity function checks every pair. Only identical canonical values, types and authority may collapse; the lowest occurrence ID is the representative. The values table preserves canonical typed bytes and a separate metadata envelope and digest. No metadata envelope is passed to the component semantic-equality function.

Evaluation.run constructs D, transcript, arguments, groups, nodes, values, edges and dependency closure as one package. replay regenerates every byte from the admitted program and authenticated input objects and requires exact equality. An extra/missing event, argument, node, edge, value or alias fails replay. A failed Evaluation exposes no completed package. immutable prior occurrences remain immutable.

unchanged evaluates the entire actual dependency closure with a complete fresh validation-status map. A proved difference or invalidity yields FALSE; otherwise any unavailable validation or equality yields UNRESOLVED; only every matched identity, type, authority, canonical digest and TRUE semantic equality yields TRUE. This is a sufficient unchanged-D test, not permission to repair a failed U. Admitted but unexecuted operations have no occurrence dependency node.

<a id="pe-protocol-specification-g3-sem-privacy"></a>
### E266-SEM-PRIVACY

This section replaces the incomplete owning-schema and admission constructors. The six fixed schema registers and component field registers are defined by SCHEMAS and PrivacyProfile.schemas below. Field order is exact. AUTHORIZATION-HEADER uses its inherited 14 field values; its canonical authorization header remains the inherited field_order/field_name/field_value TSV, not a new commitment encoding. RECOVERY-RESULT.disposition encodes U classification ACTIVE, PRE-TRANSITION-FAILURE, TRANSITION-FAILURE or COMMITTED from the 21-row function; it is not a substitute for that function's authorization/E/D permissions. COMPONENT rows expose represented/canonical octets as lowercase hex. In canonical-value mode blind/opening are NOT-APPLICABLE. In blinded mode opening is L64(canonical bytes) followed by 32 raw blind octets, represented as lowercase hex. Source authentication of the opening remains mandatory.

Approved correlation amendment: regenerate the complete multigraph. For correlation reachability alone remove equality edges whose endpoints carry the same permitted non-NONE constant reuse class, validated from the owning literal or bounded-enumeration domain. Reject any remaining path joining PUBLIC tokens from distinct U contexts. No token or relation is removed from evidence. Parallel prohibited paths still reject. Uniqueness is unchanged. Actor reconstruction uses the full graph, including allowed constant equality edges. The user explicitly approved this bounded replacement of E254 section 4; the old any-mixed-path predicate is retained only for regression comparison and is not the governing procedure.

Owning constants are only the literal or closed-domain fields assigned by PrivacyProfile, with exact field/value checks in owning_records. Component IDs, types and ordinals are constants only within the immutable admitted profile. All other fields have NONE reuse. Public observability comprises only U and one of the five classification literals. Co-observed public fields have an explicit join. expression_relations conservatively traverses every AST branch, member and apply, and propagates argument dependencies; the issuer cannot choose relation rows.

Privacy label owner_source_id resolves the immutable profile namespace plus -SOURCE-SNN. Each privacy-schema-SCHEMA anchor is a virtual typed endpoint to the matching fixed schema register definition, or to the component schema generator for COMPONENT-ORD4, inside that source’s PRIVACY range. privacy-relation-constructor is the virtual typed endpoint to PrivacyProfile._relations in S70’s PRIVACY range. Virtual endpoints are digest-and-byte-range-bound; they are not nonexistent HTML anchors.

Static admission precedes registry insertion and is separate from occurrence evidence. It uses exactly two distinct symbolic U contexts, every owning field occurrence and potential equality of every arbitrary nonconstant cell. This conservative abstraction may reject safe profiles; it cannot be weakened by successful sampled occurrences. Occurrence evidence instead uses all exact authenticated owning records in the supplied comparison scope. Every nonconstant observable action record in that scope must be supplied; an unproven completeness boundary is invalid. Hash collision evidence rejects authorization; no digest assumption makes equality mathematically injective.

The canonical immutable profile container has the exact ordered members SOURCE-OWNED-BODY, EXPRESSION-PROGRAM and PRIVACY. Each member is L64(ASCII member name) followed by L64(exact bytes), after PE-TSE-IMMUTABLE-PROFILE-V1 and LF. SOURCE-OWNED-BODY is the canonical source-owned scalar and projection record serialization, not issuer prose: the 17 scalar fields above as field: SP value LF in their stated order, followed by the canonical projection TSV above and the exact 21-row recovery TSV. Counts and references bind the program; independently authenticated source ownership, projection minimality, comparison coverage and disjointness are admission prerequisites. No occurrence evidence belongs inside the profile. EXPRESSION-PROGRAM and PRIVACY canonical JSON generation is specified below; immutable bytes are final before the outside evidence signs their digest.

E258 cross-representation admission and occurrence joins: for each component ordinal, the expression-program component, source-owned projection row and privacy component register must agree on component identity, canonical type and binding mode before the outer profile can be admitted. Regeneration of internally inconsistent bytes is not validation. The earliest structural inconsistency is INVALID-PROFILE-SCHEMA.

Occurrence validation consumes a source-authenticated complete comparison-history list for each supplied U context. Its exact values are `{U-ID}-TSE-CMP-{ORD6}` contiguous from 000001; the current owning comparison attempt is the final list member. The authorization header's generation and mapping must equal the validated immutable source-owned body. A comparison-result row repeats the current attempt cells exactly. A recovery comparison event must use the same stage and result; execution-failure follows PRE-EXECUTION equivalent; revalidation-failure follows PRE-COMMITMENT indeterminate; commitment-success follows PRE-COMMITMENT equivalent. Public classification is the comparison result for comparison and commitment-success events, pre-transition-failure for that disposition, and transition-failure for the remaining terminal failure disposition. Missing authenticated history or a failed join is INVALID-ACTION-CONTEXT and cannot be repaired by regenerating signatures.

E260 owning-reference completion: authorization header successor-state-relation-definition-id must resolve in program.defs before evidence can pass. It must equal the relation selected by the independently authenticated immutable mapping. The authenticated_mapping input is an exact ordered fact view with MAPPING_FACT_FIELDS below. It is extracted from the governing mapping after independent source authentication, not appointed by a privacy signer and not a new mapping artifact or serializer. Its generation, mapping ID/digest, profile ID/digest, selected relation ID and exact input/output type signature are checked against the immutable body, header and admitted program. The relation is a source-owned CONDITION or FUNCTION returning PE-TSE-BOOL3; its argument types remain exactly source-defined. No new fixed arity or implementation-selected relation is introduced. Source ownership and anchor adequacy remain mandatory before this view is admitted. Missing, extra, unauthenticated or inconsistent mapping facts cannot be substituted with header assertions and yield INVALID-ACTION-CONTEXT.

The remaining owning-reference audit distinguishes decidable joins from external facts. Component IDs/types/order/modes, profile/scalar/projection references, generation/mapping/profile binding, complete authorization digest, occurrence-local comparison history, result/recovery attempt identity and outcome joins are checked mechanically. Comparison history is bounded to the six-digit ORD6 domain. Q0/current-state facts and coordinate values require independently authenticated protocol sources; their truth cannot be reconstructed from digest spelling or a privacy signature. The exact authorization byte constructor below permits the comparison attempt's authorization_sha256 to be recomputed, without adding that digest to its own preimage. No privacy PASS constitutes execution permission, and diagnostic inconsistency does not mutate an authoritative result.

E262 canonical decision model: the caller's Python profile and program objects are untrusted representations. Admission rebuilds the program from its declarative records and rebuilds the complete privacy model from those validated declarations. Schemas, byfield, byid, relations and expression dependencies must equal the regenerated structures; any mismatch contributes INVALID-PROFILE-SCHEMA, the earliest failure in ORDER. Existing byte, digest and surface-label checks remain. After checking the supplied outer binding, the validator discards the supplied profile for decision purposes. All subsequent authority, component/composition scope, owning-schema, occurrence, universe, label, disclosure, signature and graph checks consume the same fresh canonical model. No partially validated cache influences a result. Failure collection retains the existing ordered precedence. This does not authenticate source truth, appoint authority or prove external scope completeness.

The trusted privacy appointment is supplied outside the profile/evidence by the source authority: authority_id, algorithm, public_key, key_fingerprint_sha256, owner_source_id, owner_anchor. Exact appointment equality is tested before signature verification. No self-signed appointment is admitted. The unchanged V2 signed-payload and object-digest preimages are implemented below, without a self digest. Both admission and occurrence require a component bundle for every component plus composition; kind/scope cannot be interchanged. validate_closed is the governing integrated entrypoint. Lower-level validate is only its evidence subroutine. All detectable failures are collected and the earliest code in ORDER wins; a later malformed context cannot mask earlier invalid authentication. The failure-subset test tests ordering, not semantic completeness by itself.

### Constructor module: privacy_v2.py

````python
"""Proposed E256 finite privacy schema and evidence constructors.

Admission uses an explicit conservative two-context symbolic universe; occurrence
validation uses exact field bytes. Evidence is outside the immutable profile.
Correlation uses the user's approved constant-edge amendment. Actor testing
retains the complete graph, including permitted constant equality edges.
"""
from expr_v2 import H,lp,tsv,need,NA
from dataclasses import dataclass
from itertools import combinations,product
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
from cryptography.exceptions import InvalidSignature
import json,re

SCHEMAS={
'AUTHORIZATION-HEADER':'serialization-domain successor-generation-id mapping-id mapping-sha256 profile-id profile-sha256 authorization-id transition-occurrence-id determination-id authorized-state-id successor-state-relation-definition-id ordering-coordinate-set-digest dependency-coordinate-set-digest component-count'.split(),
'COMPONENT-BINDING':'component_order component_id binding_mode canonical_type_id authorization_context_digest bound_value'.split(),
'COMPARISON-ATTEMPT':'comparison_attempt_id generation_id mapping_id mapping_sha256 profile_id profile_sha256 authorization_id authorization_sha256 transition_occurrence_id determination_id authorized_state_id authorized_state_sha256 current_state_id current_state_sha256 stage result failure_code'.split(),
'COMPARISON-RESULT':'comparison_attempt_id transition_occurrence_id result failure_code'.split(),
'RECOVERY-RESULT':'transition_occurrence_id comparison_attempt_id stage event unchanged_d_sufficiency disposition'.split(),
'OBSERVABILITY-OUTPUT':'transition_occurrence_id classification'.split(),
}
LABEL_HEADER='label_order schema_id field_order field_name exposure action_context_rule permitted_reuse_class derived_from_field_ids derivation_class owner_source_id owner_anchor'.split()
SURFACE_HEADER='surface_order surface_id record_class field_name exposure action_context_rule permitted_reuse_class derived_from_surface_ids derivation_class owner_source_id owner_anchor'.split()
REL_HEADER='relation_order from_surface_id to_surface_id relation_class condition_definition_id owner_source_id owner_anchor'.split()
TOKEN_HEADER='token_order surface_id action_context_id token_id token_sha256 exposure permitted_reuse_class'.split()
LINK_HEADER='link_order from_token_id to_token_id relation_order relation_class'.split()
EVIDENCE_HEADER='evidence_id evidence_kind profile_id profile_sha256 scope_id component_id surface_template_sha256 relation_template_sha256 tokens_sha256 links_sha256 correlation_result uniqueness_result actor_reconstruction_result issued_by algorithm'.split()
ORDER=['INVALID-PROFILE-SCHEMA','PROFILE-DIGEST-MISMATCH','INVALID-EVIDENCE-AUTHORITY','MISSING-EVIDENCE','INVALID-EVIDENCE-AUTHENTICATION','INVALID-EVIDENCE-DIGEST','INVALID-SURFACE-LABELS','INVALID-ACTION-CONTEXT','INCOMPLETE-EVIDENCE-UNIVERSE','COMPONENT-COUNT-MISMATCH','UNNECESSARY-COMPONENT','PUBLIC-PRIVATE-VALUE','REUSABLE-IDENTIFIER','OPENING-DISCLOSURE','UNIQUENESS-FAILURE','CORRELATION-FAILURE','ACTOR-RECONSTRUCTION-RISK','COMPONENT-FAILURE']
SCHEMA_OWNER={'AUTHORIZATION-HEADER':'S71','COMPONENT-BINDING':'S71','COMPARISON-ATTEMPT':'S72','COMPARISON-RESULT':'S72','RECOVERY-RESULT':'S72','OBSERVABILITY-OUTPUT':'S72'}
PUBLIC_CLASSES={'equivalent','material-conflict','indeterminate','pre-transition-failure','transition-failure'}
MODES={'CANONICAL-VALUE':'CANONICAL-VALUE','BLINDED-SHA256':'BLINDED-SHA256-COMMITMENT','BLINDED-SHA256-COMMITMENT':'BLINDED-SHA256-COMMITMENT'}

@dataclass(frozen=True)
class PrivacyComponent:
    id:str
    mode:str
    canonical_type:str
    necessity:str='PREDICATE-INPUT'
    privacy:str='CONFIDENTIAL'

@dataclass(frozen=True)
class Surface:
    order:int
    schema:str
    field:str
    exposure:str
    reuse:str
    domain:str
    component:str=NA
    @property
    def id(self):return f'PE-TSE-SURFACE-{self.order:06}'
    @property
    def field_id(self):return self.schema+'.'+self.field

class PrivacyProfile:
    def __init__(self,id,components,appointment,public_output=False,expression_dependencies=()):
        need(isinstance(id,str) and id.isascii() and id,'profile identity')
        need(len({c.id for c in components})==len(components),'component duplicate')
        need(type(public_output)==bool,'output exposure policy')
        self.id=id;self.components=tuple(components);self.appointment=dict(appointment);self.public_output=public_output
        self.expression_dependencies=tuple(expression_dependencies)
        self.schemas={k:list(v) for k,v in SCHEMAS.items()}
        for n,c in enumerate(components,1):
            need(c.mode in MODES and c.privacy in ('PUBLIC','ACTION-BOUNDED','CONFIDENTIAL','PRIVATE-ACTOR'),'component policy')
            self.schemas[f'COMPONENT-{n:04}']=['represented_value','canonical_value','blind','opening']
        self.surfaces=[]
        for schema,fields in self.schemas.items():
            for name in fields:
                exposure='PUBLIC' if schema=='OBSERVABILITY-OUTPUT' and public_output else 'CONFIDENTIAL'
                reuse='NONE';domain='OPAQUE';component=NA
                if name.replace('-','_')=='transition_occurrence_id':domain='ACTION-IDENTITY'
                if name in ('result','classification','failure_code','stage','event','unchanged_d_sufficiency','disposition','binding_mode','serialization-domain','canonical_type_id','component_id','component_order','component-count'):
                    reuse='GENERATION-CONSTANT';domain='CONSTANT:'+schema+'.'+name
                if schema.startswith('COMPONENT-0'):
                    c=components[int(schema[-4:])-1];component=c.id;domain='COMPONENT:'+c.id+'.'+name
                    if name in ('represented_value','canonical_value') and c.privacy in ('PUBLIC','PRIVATE-ACTOR'):exposure=c.privacy
                self.surfaces.append(Surface(len(self.surfaces)+1,schema,name,exposure,reuse,domain,component))
        self.byfield={s.field_id:s for s in self.surfaces};self.byid={s.id:s for s in self.surfaces}
        self.relations=self._relations()
        self.labels,self.surface_bytes,self.relation_bytes=self._tables()
        payload={'format':'PE-TSE-PRIVACY-PROFILE-CONSTRUCTION-V1','profile_id':id,
                 'components':[c.__dict__ for c in components],'appointment':appointment,'public_output':public_output,
                 'schemas':self.schemas,'expression_dependencies':self.expression_dependencies,
                 'labels_sha256':H(self.labels),'surfaces_sha256':H(self.surface_bytes),'relations_sha256':H(self.relation_bytes)}
        # This canonical JSON is the privacy subobject, not a replacement for the
        # complete future mapping/profile serializer. An outer digest binds it.
        self.bytes=(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode()
        self.sha256=H(self.bytes)
        self.binding_sha256=self.sha256
    def _relations(self):
        triples=set()
        def add(a,b,k):
            need(a in self.byfield and b in self.byfield,'relation field reference')
            if a!=b:triples.add((self.byfield[a].id,self.byfield[b].id,k))
        # Every same-named identity reference has a source-defined relationship.
        aliases={}
        for s in self.surfaces:aliases.setdefault(s.field.replace('-','_'),[]).append(s.field_id)
        for name,fields in aliases.items():
            if name.endswith('_id'):
                for a,b in combinations(fields,2):add(a,b,'REFERENCES')
        for n,c in enumerate(self.components,1):
            prefix=f'COMPONENT-{n:04}.'
            add(prefix+'represented_value',prefix+'canonical_value','DERIVES')
            add(prefix+'canonical_value','COMPONENT-BINDING.bound_value','ENCODES')
            if MODES[c.mode]=='BLINDED-SHA256-COMMITMENT':
                add(prefix+'blind','COMPONENT-BINDING.bound_value','ENCODES')
                add(prefix+'canonical_value',prefix+'opening','ENCODES');add(prefix+'blind',prefix+'opening','ENCODES')
        for s in self.surfaces:
            if s.schema=='AUTHORIZATION-HEADER':add(s.field_id,'COMPONENT-BINDING.authorization_context_digest','DERIVES')
        add('COMPONENT-BINDING.authorization_context_digest','COMPONENT-BINDING.bound_value','ENCODES')
        add('COMPARISON-ATTEMPT.result','COMPARISON-RESULT.result','REFERENCES')
        add('COMPARISON-ATTEMPT.failure_code','COMPARISON-RESULT.failure_code','REFERENCES')
        add('COMPARISON-RESULT.result','OBSERVABILITY-OUTPUT.classification','DERIVES')
        add('COMPARISON-RESULT.failure_code','OBSERVABILITY-OUTPUT.classification','DERIVES')
        # Each entry is generated by the source-owned expression-AST walker,
        # identifying an exact input surface and output surface, not issuer prose.
        for a,b,k in self.expression_dependencies:
            need(k in ('REFERENCES','EQUALS','AUTHENTICATES','DERIVES'),'AST relation class');add(a,b,k)
        # Public fields co-observed in one output are observable joins.
        for schema in self.schemas:
            public=[s.field_id for s in self.surfaces if s.schema==schema and s.exposure=='PUBLIC']
            for a,b in combinations(public,2):add(a,b,'OBSERVABLY-JOINABLE')
        return sorted(triples)
    def _tables(self):
        labels=[];surfaces=[]
        for s in self.surfaces:
            namespace=self.id.split('-TSE-PROFILE-',1)[0] if '-TSE-PROFILE-' in self.id else 'SYNTHETIC'
            owner=namespace+'-SOURCE-'+SCHEMA_OWNER.get(s.schema,'S70');anchor='privacy-schema-'+s.schema.lower()
            derived=sorted(a for a,b,k in self.relations if b==s.id and k in ('DERIVES','ENCODES'))
            # Multiple derivation mechanisms remain separate relation rows; labels
            # declare the conservative DERIVES union, which is independently exact.
            dfields=[self.byid[a].field_id for a in derived];kind='DERIVES' if derived else NA
            labels.append([f'{s.order:06}',s.schema,f'{self.schemas[s.schema].index(s.field)+1:04}',s.field,s.exposure,'OCCURRENCE-U',s.reuse,','.join(dfields) or 'NONE',kind,owner,anchor])
            surfaces.append([f'{s.order:06}',s.id,s.schema,s.field,s.exposure,'OCCURRENCE-U',s.reuse,','.join(derived) or 'NONE',kind,owner,anchor])
        namespace=self.id.split('-TSE-PROFILE-',1)[0] if '-TSE-PROFILE-' in self.id else 'SYNTHETIC'
        relations=[[f'{i:06}',a,b,k,'ALWAYS',namespace+'-SOURCE-S70','privacy-relation-constructor'] for i,(a,b,k) in enumerate(self.relations,1)]
        return tsv(LABEL_HEADER,labels),tsv(SURFACE_HEADER,surfaces),tsv(REL_HEADER,relations)
    def schema_bytes(self):
        return tsv('schema_order schema_id field_order field_name'.split(),[[f'{i:04}',schema,f'{j:04}',f] for i,(schema,fields) in enumerate(self.schemas.items(),1) for j,f in enumerate(fields,1)])

@dataclass(frozen=True)
class Token:
    id:str
    surface:str
    context:str
    digest:str
    exposure:str
    reuse:str
    record:int

def universe(profile,contexts,admission=False):
    """contexts: ordered U -> schema -> exact ordered record dictionaries.

    Admission uses exactly two symbolic contexts. It instantiates every schema
    and permits potential equality among all non-fresh non-constant cells.
    That is deliberately conservative; PASS is not sampled occurrence success.
    """
    if admission:
        need(contexts is None,'admission context injection')
        contexts={f'{profile.id}-ADMISSION-U-{i:06}':None for i in (1,2)}
    else:
        need(isinstance(contexts,dict) and len(contexts)>0 and len(contexts)==len(set(contexts)),'action contexts')
        need(all(isinstance(c,str) and c and c.isascii() for c in contexts),'action context ID')
    tokens=[]
    for context,records in sorted(contexts.items()):
        if not admission:need(set(records)==set(profile.schemas),'owning schema universe')
        for schema,fields in profile.schemas.items():
            count=len(profile.components) if schema=='COMPONENT-BINDING' else 1
            if not admission:need(len(records[schema])==count,'record count')
            for j in range(count):
                if not admission:need(list(records[schema][j])==fields,'field order/universe')
                for f in fields:
                    s=profile.byfield[schema+'.'+f]
                    if admission:
                        value=('FRESH:'+context if s.domain=='ACTION-IDENTITY' else 'CONSTANT:'+s.domain if s.reuse!='NONE' else 'ARBITRARY').encode()
                    else:
                        value=records[schema][j][f];need(isinstance(value,str) and value and not any(x in value for x in '\t\r\n'),'field value')
                        if s.domain=='ACTION-IDENTITY':need(value==context,'action identity binding')
                        if schema=='OBSERVABILITY-OUTPUT' and f=='classification':need(value in PUBLIC_CLASSES,'public classification')
                        value=value.encode()
                    tokens.append(Token(f'TOKEN-{len(tokens)+1:06}',s.id,context,H(value),s.exposure,s.reuse,j+1))
    links=set()
    for order,(a,b,k) in enumerate(profile.relations,1):
        for x in tokens:
            if x.surface!=a:continue
            for y in tokens:
                if y.surface!=b or x.context!=y.context:continue
                sx=profile.byid[x.surface];sy=profile.byid[y.surface]
                # Generic binding fields instantiate only their owning component.
                if sx.schema=='COMPONENT-BINDING' and sy.component!=NA and profile.components[x.record-1].id!=sy.component:continue
                if sy.schema=='COMPONENT-BINDING' and sx.component!=NA and profile.components[y.record-1].id!=sx.component:continue
                links.add((x.id,y.id,f'{order:06}',k))
    for x,y in combinations(tokens,2):
        sx=profile.byid[x.surface];sy=profile.byid[y.surface]
        arbitrary=lambda s:s.domain!='ACTION-IDENTITY' and s.reuse=='NONE'
        possible=admission and (arbitrary(sx) or arbitrary(sy))
        if x.digest==y.digest or possible:links.add((x.id,y.id,'000000','EQUALS'))
    # Complete equality relation, including runtime matches, is never issuer-selected.
    return tokens,sorted(links)

def checks(tokens,links,*,inherited=False):
    byid={t.id:t for t in tokens};need(len(byid)==len(tokens),'duplicate token')
    graph={t.id:[] for t in tokens}
    for a,b,order,k in links:
        need(a in byid and b in byid and a!=b,'link endpoint')
        allowed=k=='EQUALS' and byid[a].reuse==byid[b].reuse and byid[a].reuse!='NONE'
        graph[a].append((b,allowed));graph[b].append((a,allowed))
    public=[t for t in tokens if t.exposure=='PUBLIC']
    uniqueness=not any(x.context!=y.context and x.digest==y.digest and not (x.reuse==y.reuse and x.reuse!='NONE') for x,y in combinations(public,2))
    # Preserve E254's any-edge-distinct-simple-path rule, including parallel edges.
    def bad_path(start,end):
        stack=[(start,frozenset([start]),False)]
        while stack:
            n,seen,bad=stack.pop()
            if n==end:
                if bad:return True
                continue
            for nxt,allowed in sorted(graph[n],reverse=True):
                if nxt not in seen:stack.append((nxt,seen|{nxt},bad or not allowed))
        return False
    if inherited:
        correlation=not any(bad_path(x.id,y.id) for x,y in combinations(public,2) if x.context!=y.context)
    else:
        correlation=True;remaining=set(graph)
        while remaining:
            visited=set();todo=[min(remaining)]
            while todo:
                n=todo.pop()
                if n in visited:continue
                visited.add(n);todo.extend(x for x,allowed in graph[n] if not allowed and x not in visited)
            remaining-=visited
            if len({byid[n].context for n in visited if byid[n].exposure=='PUBLIC'})>1:correlation=False;break
    actors={t.id for t in tokens if t.exposure=='PRIVATE-ACTOR'}
    actor=True
    for t in public:
        visited=set();todo=[t.id]
        while todo:
            n=todo.pop()
            if n in visited:continue
            visited.add(n);todo.extend(x for x,_ in graph[n] if x not in visited)
        if visited&actors:actor=False;break
    return {'correlation':correlation,'uniqueness':uniqueness,'actor_reconstruction':actor}

def token_bytes(tokens):
    return tsv(TOKEN_HEADER,[[f'{i:06}',t.surface,t.context,t.id,t.digest,t.exposure,t.reuse] for i,t in enumerate(tokens,1)])
def link_bytes(links):return tsv(LINK_HEADER,[[f'{i:06}',*row] for i,row in enumerate(links,1)])

def evidence(profile,tokens,links,key,admission=False,component=NA):
    if component!=NA:
        seed={t.id for t in tokens if profile.byid[t.surface].component==component};need(bool(seed),'component evidence scope')
        changed=True
        while changed:
            old=len(seed)
            for a,b,_,_ in links:
                if a in seed or b in seed:seed.update([a,b])
            changed=len(seed)!=old
        tokens=[t for t in tokens if t.id in seed];links=[r for r in links if r[0] in seed and r[1] in seed]
    tests=checks(tokens,links);tb=token_bytes(tokens);lb=link_bytes(links)
    kind=('ADMISSION-' if admission else '')+('COMPOSITION' if component==NA else 'COMPONENT')
    scope=profile.id+('#ADMISSION-V1' if admission else '#OCCURRENCE-SET-'+H(tb))
    eid=profile.id+'#'+kind+'-'+('ALL' if component==NA else component)
    row=[eid,kind,profile.id,profile.binding_sha256,scope,component,H(profile.surface_bytes),H(profile.relation_bytes),H(tb),H(lb),*['PASS' if tests[k] else 'FAIL' for k in ['correlation','uniqueness','actor_reconstruction']],profile.appointment['authority_id'],'ED25519-RFC8032']
    eb=tsv(EVIDENCE_HEADER,[row]);signed=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+eb+tb+lb
    sb=(profile.appointment['authority_id']+' '+key.sign(signed).hex()+'\n').encode()
    files={'evidence.tsv':eb,'tokens.tsv':tb,'links.tsv':lb,'signature.txt':sb}
    digest=H(b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n'+b''.join(lp(files[n]) for n in files))
    return files,digest

def validate(profile,trusted_appointment,files,digest,expected_tokens,expected_links,*,admission=False,component=NA,labels=None,components_pass=True):
    """Ordered fail selection; expected universe is independently regenerated.

    Full source appointment and complete outer profile identity must be validated
    before calling this subobject validator. No key possession appoints authority.
    """
    def fail(code):return ('FAIL',code)
    import csv,io
    try:
        need(isinstance(profile,PrivacyProfile),'profile object')
        need(profile.sha256==H(profile.bytes),'profile digest')
    except Exception:return fail('INVALID-PROFILE-SCHEMA')
    if profile.appointment!=trusted_appointment:return fail('INVALID-EVIDENCE-AUTHORITY')
    try:
        pk=bytes.fromhex(trusted_appointment['public_key'])
        need(len(pk)==32 and H(pk)==trusted_appointment['key_fingerprint_sha256'] and trusted_appointment['algorithm']=='ED25519-RFC8032','appointment key')
    except Exception:return fail('INVALID-EVIDENCE-AUTHORITY')
    if not files or set(files)!={'evidence.tsv','tokens.tsv','links.tsv','signature.txt'}:return fail('MISSING-EVIDENCE')
    try:
        line=files['signature.txt'].decode('ascii');a,s=line.rstrip('\n').split(' ')
        need(line.endswith('\n') and line.count('\n')==1 and a==trusted_appointment['authority_id'] and bool(re.fullmatch('[0-9a-f]{128}',s)),'signature line')
        signed=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+files['evidence.tsv']+files['tokens.tsv']+files['links.tsv']
        Ed25519PublicKey.from_public_bytes(pk).verify(bytes.fromhex(s),signed)
    except Exception:return fail('INVALID-EVIDENCE-AUTHENTICATION')
    computed=H(b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n'+b''.join(lp(files[n]) for n in ['evidence.tsv','tokens.tsv','links.tsv','signature.txt']))
    if digest!=computed:return fail('INVALID-EVIDENCE-DIGEST')
    if labels is not None and labels!=profile.labels:return fail('INVALID-SURFACE-LABELS')
    try:
        rows=list(csv.DictReader(io.StringIO(files['evidence.tsv'].decode()),delimiter='\t'));need(len(rows)==1,'evidence rows');r=rows[0]
        if r['profile_sha256']!=profile.binding_sha256 or r['profile_id']!=profile.id:return fail('PROFILE-DIGEST-MISMATCH')
        tokens=expected_tokens;links=expected_links
        if component!=NA:
            seed={t.id for t in tokens if profile.byid[t.surface].component==component}
            while True:
                old=len(seed)
                for a,b,_,_ in links:
                    if a in seed or b in seed:seed.update([a,b])
                if len(seed)==old:break
            tokens=[t for t in tokens if t.id in seed];links=[r for r in links if r[0] in seed and r[1] in seed]
        kind=('ADMISSION-' if admission else '')+('COMPOSITION' if component==NA else 'COMPONENT')
        scope=profile.id+('#ADMISSION-V1' if admission else '#OCCURRENCE-SET-'+H(token_bytes(tokens)))
        need(r['evidence_kind']==kind and r['scope_id']==scope and r['component_id']==component,'evidence scope')
        need(r['surface_template_sha256']==H(profile.surface_bytes) and r['relation_template_sha256']==H(profile.relation_bytes),'template digests')
        need(files['tokens.tsv']==token_bytes(tokens) and files['links.tsv']==link_bytes(links),'universe equality')
        need(r['tokens_sha256']==H(files['tokens.tsv']) and r['links_sha256']==H(files['links.tsv']),'data digests')
    except Exception:return fail('INCOMPLETE-EVIDENCE-UNIVERSE')
    if any(c.necessity not in ('PREDICATE-INPUT','AUTHORIZATION-BINDING','ORDERING-COORDINATE','DEPENDENCY-COORDINATE') for c in profile.components):return fail('UNNECESSARY-COMPONENT')
    if any(c.privacy=='PRIVATE-ACTOR' for c in profile.components):return fail('PUBLIC-PRIVATE-VALUE')
    tests=checks(tokens,links)
    eid=profile.id+'#'+kind+'-'+('ALL' if component==NA else component)
    expected_row=[eid,kind,profile.id,profile.binding_sha256,scope,component,H(profile.surface_bytes),H(profile.relation_bytes),H(token_bytes(tokens)),H(link_bytes(links)),*['PASS' if tests[k] else 'FAIL' for k in ['correlation','uniqueness','actor_reconstruction']],profile.appointment['authority_id'],'ED25519-RFC8032']
    if files['evidence.tsv']!=tsv(EVIDENCE_HEADER,[expected_row]):return fail('INCOMPLETE-EVIDENCE-UNIVERSE')
    for k,code in [('uniqueness','UNIQUENESS-FAILURE'),('correlation','CORRELATION-FAILURE'),('actor_reconstruction','ACTOR-RECONSTRUCTION-RISK')]:
        if not tests[k]:return fail(code)
    if any(r[k+'_result']!=('PASS' if tests[k] else 'FAIL') for k in tests):return fail('INCOMPLETE-EVIDENCE-UNIVERSE')
    if component==NA and not components_pass:return fail('COMPONENT-FAILURE')
    return ('PASS','NONE')
````

### Constructor module: profile_body.py

````python
"""Exact scalar/projection/recovery serialization for a future owning profile.

Authenticated source ownership and source-defined predicate adequacy are verified
before this byte constructor; this module never appoints those source authorities.
"""
from expr_v2 import need,tsv,NA,B
import re
SCALARS='profile-identifier profile-version governing-successor-generation governing-mapping-identifier profile-sha256-algorithm projection-component-count definition-count equivalence-definition-id material-conflict-definition-id applicability-definition-id determination-dependency-definition-id comparison-timing-rule execution-gate commitment-gate recovery-definition-id privacy-classification observability-classification'.split()
PROJECTION='component_order component_id authoritative_source_id authoritative_source_sha256 authoritative_source_anchor component_type_definition_id representation_definition_id canonicalization_definition_id normalization_definition_id authorization_binding_mode applicable_precondition_definition_ids applicable_invariant_definition_ids ordering_coordinate_definition_ids dependency_coordinate_definition_ids determination_dependency equivalence_definition_id immaterial_difference_definition_id material_conflict_definition_id authority_definition_id availability_definition_id validity_definition_id authentication_definition_id privacy_definition_id observability_definition_id'.split()
RECOVERY='recovery_order stage event unchanged_d_sufficiency u_classification authorization_disposition evaluation_required determination_required authorization_required u_required execute_permission commit_permission'.split()

def recovery_rows():
    rows=[]
    def add(stage,event,suff):
        if event=='commitment-success':tail=['COMMITTED','CONSUMED','SAME','SAME','NONE','NONE','PROHIBIT','COMPLETE']
        elif event=='equivalent':tail=['ACTIVE','PRESERVE','SAME','SAME','SAME','SAME','PERMIT' if stage=='PRE-EXECUTION' else 'PROHIBIT','PERMIT' if stage=='PRE-COMMITMENT' else 'PROHIBIT']
        else:tail=['PRE-TRANSITION-FAILURE' if stage=='PRE-EXECUTION' else 'TRANSITION-FAILURE','TERMINALLY-STALE','SAME' if suff=='TRUE' else 'NEW','SAME' if suff=='TRUE' else 'NEW-ON-SUCCESSFUL-COMPLETION','NEW','NEW','PROHIBIT','PROHIBIT']
        rows.append([f'{len(rows)+1:04}',stage,event,suff,*tail])
    for stage,events in [('PRE-EXECUTION',['equivalent','material-conflict','indeterminate']),('EXECUTION',['execution-failure']),('PRE-COMMITMENT',['equivalent','material-conflict','indeterminate','revalidation-failure']),('COMMITMENT',['commitment-success'])]:
        for event in events:
            for suff in ([NA] if event in ('equivalent','commitment-success') else ['TRUE','FALSE','UNRESOLVED']):add(stage,event,suff)
    return rows

def owning_body(scalars,projection,program,privacy,source_identities):
    """source_identities maps authenticated source IDs to exact SHA-256.

    Existence and contents of source anchors are checked against those supplied
    immutable sources before admission. No digest alone supplies authority.
    """
    need(list(scalars)==SCALARS,'scalar order')
    for v in scalars.values():need(isinstance(v,str) and v and not any(c in v for c in '\t\r\n'),'scalar bytes')
    m=re.fullmatch(r'(.+)-TSE-PROFILE-([0-9]{6})-V0001',scalars['profile-identifier'])
    need(m and int(m[2])>0 and scalars['profile-identifier']==privacy.id,'profile grammar')
    need(scalars['governing-mapping-identifier']==m[1]+'-TMAP-'+m[2],'mapping ordinal')
    need(bool(re.fullmatch(r'PE-PROTOCOL-GENERATION-[0-9]{3}',scalars['governing-successor-generation'])),'generation grammar')
    fixed={'profile-version':'V0001','profile-sha256-algorithm':'SHA-256','comparison-timing-rule':'PRE-EXECUTION-AND-SEMANTIC-COMMITMENT','execution-gate':'EQUIVALENT-ONLY','commitment-gate':'EQUIVALENT-ONLY','privacy-classification':'MINIMUM-ACTION-BOUNDED-NON-ACTOR','observability-classification':'PUBLIC-RESULT-ONLY-NON-AUTHORITATIVE-DIAGNOSTICS'}
    need(all(scalars[k]==v for k,v in fixed.items()),'scalar fixed domains')
    need(scalars['projection-component-count']==f'{len(program.components):06}' and scalars['definition-count']==f'{len(program.defs):06}','scalar counts')
    for f in ('equivalence-definition-id','material-conflict-definition-id','applicability-definition-id','determination-dependency-definition-id','recovery-definition-id'):
        need(scalars[f] in program.defs and program.defs[scalars[f]].output==B,'scalar definition reference')
    need(len(projection)==len(program.components)==len(privacy.components),'projection count')
    for i,(r,c,p) in enumerate(zip(projection,program.components.values(),privacy.components),1):
        need(list(r)==PROJECTION and r['component_order']==f'{i:06}' and r['component_id']==c.id==p.id,'projection identity')
        need(p.canonical_type==c.canonical,'cross-representation canonical type')
        need(r['authoritative_source_id']==c.source and r['authoritative_source_anchor']==c.anchor,'source owner')
        need(source_identities.get(c.source)==r['authoritative_source_sha256'] and bool(re.fullmatch('[0-9a-f]{64}',r['authoritative_source_sha256'])),'source digest binding')
        for f,expected in [('component_type_definition_id',c.canonical),('representation_definition_id',c.decoder),('canonicalization_definition_id',c.canonicalizer),('normalization_definition_id',c.normalizer),('availability_definition_id',c.available),('validity_definition_id',c.valid),('authentication_definition_id',c.authenticated)]:need(r[f]==expected,'component program binding')
        mode='BLINDED-SHA256-COMMITMENT' if p.mode=='BLINDED-SHA256' else p.mode
        need(r['authorization_binding_mode']==mode and r['determination_dependency'] in ('INCLUDED','EXCLUDED'),'projection domain')
        for f in ('applicable_precondition_definition_ids','applicable_invariant_definition_ids','ordering_coordinate_definition_ids','dependency_coordinate_definition_ids'):
            ids=[] if r[f]=='NONE' else r[f].split(',')
            need(len(ids)==len(set(ids)) and all(x in program.defs for x in ids),'projection definition list')
            need(ids==sorted(ids,key=program.def_order.get),'projection definition order')
        for f in ('equivalence_definition_id','immaterial_difference_definition_id','material_conflict_definition_id','authority_definition_id','privacy_definition_id','observability_definition_id'):
            need(r[f] in program.defs and program.defs[r[f]].output==B,'projection predicate')
    return ''.join(f'{k}: {scalars[k]}\n' for k in SCALARS).encode()+tsv(PROJECTION,[[r[k] for k in PROJECTION] for r in projection])+tsv(RECOVERY,recovery_rows())

def validate_body(data,program,privacy,source_identities):
    need(isinstance(data,bytes) and data.endswith(b'\n') and b'\r' not in data,'body bytes')
    lines=data.decode().splitlines();need(len(lines)>=17+1+len(program.components)+22,'body length')
    scalars={}
    for k,line in zip(SCALARS,lines[:17]):
        need(line.startswith(k+': '),'scalar line');scalars[k]=line[len(k)+2:]
    need(lines[17].split('\t')==PROJECTION,'projection header')
    projection=[]
    for line in lines[18:18+len(program.components)]:
        row=line.split('\t');need(len(row)==len(PROJECTION),'projection row');projection.append(dict(zip(PROJECTION,row)))
    need(data==owning_body(scalars,projection,program,privacy,source_identities),'canonical complete owning body')
    return scalars,projection
````

### Constructor module: privacy_admission.py

````python
"""Closed author-side admission/occurrence constructor for the E256 privacy model.

The immutable owning profile bytes and its source-appointed authority are inputs,
not objects this procedure may appoint. The caller must first validate the outer
profile against its governing source. This constructor binds that exact digest,
regenerates all privacy tables and evaluates both evidence scopes.
"""
from privacy_v2 import *
from expr_v2 import PRIMITIVES,Types,parse,identifier,B,revalidate_program
from profile_body import validate_body
import csv,io,unicodedata

FAILURES=tuple(ORDER)
FAILURE_INDEX={name:i for i,name in enumerate(FAILURES)}
def first_failure(failures):
    need(set(failures)<=set(FAILURES),'undeclared privacy failure')
    return min(failures,key=FAILURE_INDEX.get) if failures else 'NONE'

def expression_relations(program,components):
    """Conservative exact AST relation algorithm, including unused branches.

    arg flows come from caller operands; entry arguments range over component
    represented/canonical inputs. This over-approximation may reject a safe
    profile, but does not use a sampled execution to prove admission.
    """
    index={c.id:i for i,c in enumerate(components,1)}
    need(set(program.components)==set(index),'component program identity')
    result=set();all_inputs=set()
    for i in index.values():all_inputs.update([f'COMPONENT-{i:04}.represented_value',f'COMPONENT-{i:04}.canonical_value'])
    def walk(e,arguments):
        op,*a=e
        if op=='literal':return set()
        if op=='arg':return set(arguments[int(a[0])-1])
        if op=='ref' or op in ('available','authoritative','valid','authenticated'):
            field=f'COMPONENT-{index[a[0]]:04}.canonical_value'
            if op=='authenticated':result.add((field,'COMPARISON-ATTEMPT.result','AUTHENTICATES'))
            else:result.add((field,'COMPARISON-ATTEMPT.result','REFERENCES'))
            return {field}
        if op=='apply':
            inputs=[walk(x,arguments) for x in a[1:]]
            if a[0]=='PE-TSE-SET':return set().union(*inputs)
            return walk(program.defs[a[0]].expression,inputs)
        if op=='member':
            return walk(a[0],arguments)|walk(program.defs[a[1]].expression,[])
        children=[walk(x,arguments) for x in a if isinstance(x,tuple)]
        if op=='equal':
            for left in children[0]:
                for right in children[1]:
                    if left!=right:result.add((left,right,'EQUALS'))
        return set().union(*children)
    for definition in program.defs.values():
        sources=walk(definition.expression,[all_inputs for _ in definition.inputs])
        for source in sources:result.add((source,'COMPARISON-ATTEMPT.result','DERIVES'))
    return tuple(sorted(result))

def bind_program(profile,program):
    relations=expression_relations(program,profile.components)
    return PrivacyProfile(profile.id,profile.components,profile.appointment,profile.public_output,relations)

def bind_outer(profile,program,source_owned_body,source_identities):
    """Exact future-profile container; no occurrence/admission evidence member.

    source_owned_body is the already validated source-owned mapping/profile
    scalar body, including its existing identities, predicates and recovery
    bindings. This function neither invents nor validates those authority facts.
    The profile's governing source must validate that body before admission.
    """
    revalidate_program(program)
    need(isinstance(source_owned_body,bytes) and source_owned_body,'owning profile body')
    validate_body(source_owned_body,program,profile,source_identities)
    structures={'types':list(program.types.rows.items()),'definitions':[d.__dict__ for d in program.defs.values()],
                'components':[c.__dict__ for c in program.components.values()],'fields':[f.__dict__ for f in program.fields.values()],
                'root_definition':program.root_definition,'root_fields':program.root_fields,'groups':program.groups}
    pb=(json.dumps(structures,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode()
    members=[('SOURCE-OWNED-BODY',source_owned_body),('EXPRESSION-PROGRAM',pb),('PRIVACY',profile.bytes)]
    outer=b'PE-TSE-IMMUTABLE-PROFILE-V1\n'+b''.join(lp(name.encode())+lp(data) for name,data in members)
    profile.binding_sha256=H(outer)
    profile.outer_bytes=outer
    profile.source_identities=dict(source_identities)
    profile.source_owned_body=source_owned_body
    return outer

def read_tsv(b,header):
    need(isinstance(b,bytes) and b.endswith(b'\n') and not b.startswith(b'\xef\xbb\xbf') and b'\r' not in b,'TSV bytes')
    s=b.decode('utf-8');need(unicodedata.normalize('NFC',s)==s,'TSV NFC')
    lines=[line.split('\t') for line in s[:-1].split('\n')]
    need(lines and lines[0]==header and all(len(r)==len(header) and all(c for c in r) for r in lines),'TSV schema')
    return [dict(zip(header,r)) for r in lines[1:]]

MAPPING_FACT_FIELDS='generation_id mapping_id mapping_sha256 profile_id profile_sha256 successor_state_relation_definition_id successor_state_relation_input_type_ids successor_state_relation_output_type_id'.split()

def mapping_facts(profile,program,facts,scalars):
    """Facts are extracted from an independently authenticated immutable mapping.

    This view neither serializes nor appoints a mapping. Its definition role and
    signature are source-owned; the validator joins them to the admitted profile.
    """
    need(isinstance(facts,dict) and list(facts)==MAPPING_FACT_FIELDS,'mapping fact fields')
    for name,value in facts.items():
        need(isinstance(value,str) and value and value.isascii() and not any(c in value for c in '\t\r\n'),'mapping fact cell')
        if name.endswith('_sha256'):need(bool(re.fullmatch('[0-9a-f]{64}',value)),'mapping fact digest')
        if name.endswith('_id'):need(identifier(value),'mapping fact identifier')
    need(facts['generation_id']==scalars['governing-successor-generation'] and facts['mapping_id']==scalars['governing-mapping-identifier'],'mapping fact governing identity')
    need(facts['profile_id']==profile.id and facts['profile_sha256']==profile.binding_sha256,'mapping fact profile binding')
    relation=facts['successor_state_relation_definition_id']
    need(relation in program.defs,'mapping relation reference')
    definition=program.defs[relation]
    need(facts['successor_state_relation_input_type_ids']==(','.join(definition.inputs) or 'NONE'),'mapping relation input signature')
    need(facts['successor_state_relation_output_type_id']==definition.output==B,'mapping relation output signature')
    need(definition.kind in ('CONDITION','FUNCTION') and definition.source in profile.source_identities,'mapping relation source/role')
    return facts

def authorization_bytes(record):
    h=record['AUTHORIZATION-HEADER'][0]
    header=tsv(['field_order','field_name','field_value'],[[f'{i:04}',f,h[f]] for i,f in enumerate(SCHEMAS['AUTHORIZATION-HEADER'],1)])
    bindings=tsv(SCHEMAS['COMPONENT-BINDING'],[[r[f] for f in SCHEMAS['COMPONENT-BINDING']] for r in record['COMPONENT-BINDING']])
    return header+bindings

def owning_records(profile,contexts,program,comparison_history,authenticated_mapping):
    """Validate the complete six-schema occurrence records before tokenization.

    IDs/digests are authenticated protocol inputs, not inferred state. All known
    constants, scalar grammars, component ordinals and redundant bindings are
    checked here. Unknown record kinds and extra/missing fields are rejected.
    """
    need(isinstance(contexts,dict) and contexts,'contexts')
    need(isinstance(comparison_history,dict) and set(comparison_history)==set(contexts),'comparison history domain')
    scalars,_=validate_body(profile.source_owned_body,program,profile,profile.source_identities)
    facts=mapping_facts(profile,program,authenticated_mapping,scalars)
    for u,record in contexts.items():
        need(isinstance(u,str) and bool(re.fullmatch('[A-Za-z0-9][A-Za-z0-9._:#-]*',u)),'context ID')
        need(set(record)==set(profile.schemas),'owning schemas')
        for schema,fields in profile.schemas.items():
            count=len(profile.components) if schema=='COMPONENT-BINDING' else 1
            need(isinstance(record[schema],list) and len(record[schema])==count,'owning cardinality')
            for r in record[schema]:
                need(isinstance(r,dict) and list(r)==fields,'owning field order')
                for name,value in r.items():
                    need(isinstance(value,str) and value and unicodedata.normalize('NFC',value)==value and not any(c in value for c in '\t\r\n'),'owning cell')
                    n=name.replace('-','_')
                    if n.endswith(('_sha256','_digest')):need(bool(re.fullmatch('[0-9a-f]{64}',value)),'owning digest')
                    if n.endswith('_id'):need(identifier(value),'owning ID')
                    if n=='transition_occurrence_id':need(value==u,'owning U')
        h=record['AUTHORIZATION-HEADER'][0];attempt=record['COMPARISON-ATTEMPT'][0]
        result=record['COMPARISON-RESULT'][0];recovery=record['RECOVERY-RESULT'][0];obs=record['OBSERVABILITY-OUTPUT'][0]
        need(h['serialization-domain']=='PE-TSE-AUTHORIZATION-V1','authorization domain')
        need(h['successor-state-relation-definition-id'] in program.defs,'authorization relation reference')
        for header_name,fact_name in [('successor-generation-id','generation_id'),('mapping-id','mapping_id'),('mapping-sha256','mapping_sha256'),('profile-id','profile_id'),('profile-sha256','profile_sha256'),('successor-state-relation-definition-id','successor_state_relation_definition_id')]:
            need(h[header_name]==facts[fact_name],'authorization/mapping fact join')
        need(attempt['authorization_sha256']==H(authorization_bytes(record)),'complete authorization digest')
        need(h['profile-id']==profile.id and attempt['profile_id']==profile.id,'profile ID binding')
        need(h['successor-generation-id']==scalars['governing-successor-generation'],'generation/profile binding')
        need(h['mapping-id']==scalars['governing-mapping-identifier'],'mapping/profile binding')
        need(h['profile-sha256']==profile.binding_sha256,'immutable profile binding')
        need(h['successor-generation-id']==attempt['generation_id'],'generation binding')
        need(h['component-count']==f'{len(profile.components):06}','component count')
        for hn,an in [('mapping-id','mapping_id'),('mapping-sha256','mapping_sha256'),('profile-sha256','profile_sha256'),('authorization-id','authorization_id'),('determination-id','determination_id'),('authorized-state-id','authorized_state_id')]:
            need(h[hn]==attempt[an],'attempt authorization binding')
        need(attempt['stage'] in ('PRE-EXECUTION','PRE-COMMITMENT'),'attempt stage')
        need(attempt['result'] in ('equivalent','material-conflict','indeterminate'),'attempt result')
        history=comparison_history[u]
        need(isinstance(history,list) and 0<len(history)<=999999 and all(isinstance(x,str) for x in history),'comparison history')
        need(history==[f'{u}-TSE-CMP-{i:06}' for i in range(1,len(history)+1)],'comparison history contiguous')
        need(attempt['comparison_attempt_id']==history[-1],'current comparison history binding')
        comparison_codes={'NONE','INVALID-IDENTITY','UNREGISTERED-IDENTITY','DIGEST-MISMATCH','INVALID-PROFILE','INVALID-AUTHORIZATION','INVALID-OPENING','UNAUTHENTICATED-STATE','INCONSISTENT-BOTH-TRUE','INCOMPLETE-PROFILE-COVERAGE','UNRESOLVED-REQUIRED-INPUT'}
        need(attempt['failure_code'] in comparison_codes,'comparison code')
        need((attempt['result']=='indeterminate')==(attempt['failure_code']!='NONE'),'result failure binding')
        for n in ['comparison_attempt_id','transition_occurrence_id','result','failure_code']:need(result[n]==attempt[n],'result attempt binding')
        need(recovery['comparison_attempt_id']==attempt['comparison_attempt_id'],'recovery attempt binding')
        need(recovery['stage'] in ('PRE-EXECUTION','EXECUTION','PRE-COMMITMENT','COMMITMENT'),'recovery stage')
        need(recovery['unchanged_d_sufficiency'] in ('TRUE','FALSE','UNRESOLVED',NA),'recovery sufficiency')
        key=(recovery['stage'],recovery['event'],recovery['unchanged_d_sufficiency'])
        admitted={('PRE-EXECUTION','equivalent',NA):'ACTIVE',('PRE-COMMITMENT','equivalent',NA):'ACTIVE',('COMMITMENT','commitment-success',NA):'COMMITTED'}
        for stage,event in [('PRE-EXECUTION','material-conflict'),('PRE-EXECUTION','indeterminate'),('EXECUTION','execution-failure'),('PRE-COMMITMENT','material-conflict'),('PRE-COMMITMENT','indeterminate'),('PRE-COMMITMENT','revalidation-failure')]:
            for sufficiency in ('TRUE','FALSE','UNRESOLVED'):admitted[stage,event,sufficiency]='PRE-TRANSITION-FAILURE' if stage=='PRE-EXECUTION' else 'TRANSITION-FAILURE'
        need(key in admitted and recovery['disposition']==admitted[key],'recovery lookup')
        comparison_events=('equivalent','material-conflict','indeterminate')
        if recovery['event'] in comparison_events:
            need(recovery['stage']==attempt['stage'] and recovery['event']==attempt['result'],'recovery comparison binding')
        elif recovery['event']=='execution-failure':
            need(recovery['stage']=='EXECUTION' and attempt['stage']=='PRE-EXECUTION' and attempt['result']=='equivalent','execution failure binding')
        elif recovery['event']=='revalidation-failure':
            need(recovery['stage']=='PRE-COMMITMENT' and attempt['stage']=='PRE-COMMITMENT' and attempt['result']=='indeterminate','revalidation failure binding')
        else:
            need(recovery['event']=='commitment-success' and recovery['stage']=='COMMITMENT' and attempt['stage']=='PRE-COMMITMENT' and attempt['result']=='equivalent','commitment success binding')
        need(obs['classification'] in PUBLIC_CLASSES,'observability classification')
        if recovery['event'] in comparison_events or recovery['event']=='commitment-success':observable=attempt['result']
        else:observable='pre-transition-failure' if recovery['disposition']=='PRE-TRANSITION-FAILURE' else 'transition-failure'
        need(obs['classification']==observable,'observability result binding')
        header_bytes=tsv(['field_order','field_name','field_value'],[[f'{i:04}',f,h[f]] for i,f in enumerate(SCHEMAS['AUTHORIZATION-HEADER'],1)])
        for i,(binding,c) in enumerate(zip(record['COMPONENT-BINDING'],profile.components),1):
            need(binding['component_order']==f'{i:04}' and binding['component_id']==c.id and binding['canonical_type_id']==c.canonical_type,'component row binding')
            need(binding['binding_mode']==MODES[c.mode] and binding['authorization_context_digest']==H(header_bytes),'binding mode/context')
            need(bool(re.fullmatch('[0-9a-f]+',binding['bound_value'])) and len(binding['bound_value'])%2==0,'bound value')
            if MODES[c.mode]=='BLINDED-SHA256-COMMITMENT':need(len(binding['bound_value'])==64,'commitment length')
            values=record[f'COMPONENT-{i:04}'][0]
            for name,value in values.items():
                if name in ('blind','opening') and MODES[c.mode]=='CANONICAL-VALUE':
                    need(value==NA,'canonical mode has no opening');continue
                need(bool(re.fullmatch('(?:[0-9a-f]{2})+',value)),'component value hex')
            canonical=bytes.fromhex(values['canonical_value']);represented=bytes.fromhex(values['represented_value'])
            need(program.types.decode(canonical)[0]==c.canonical_type,'canonical type')
            need(program.types.decode(represented)[0]==program.components[c.id].represented,'represented type')
            if MODES[c.mode]=='BLINDED-SHA256-COMMITMENT':
                need(len(values['blind'])==64,'blind length');blind=bytes.fromhex(values['blind'])
                opening=lp(canonical)+blind
                need(bytes.fromhex(values['opening'])==opening,'opening serialization')
                preimage=lp(b'PE-TSE-COMPONENT-COMMITMENT-V1')+bytes.fromhex(binding['authorization_context_digest'])+lp(c.id.encode())+lp(c.canonical_type.encode())+lp(canonical)+blind
                need(binding['bound_value']==H(preimage),'commitment preimage')
            else:need(binding['bound_value']==canonical.hex(),'canonical binding value')
    return contexts

def appointment_valid(appointment,trusted):
    try:
        need(appointment==trusted,'external appointment')
        need(set(trusted)=={'authority_id','algorithm','public_key','key_fingerprint_sha256','owner_source_id','owner_anchor'},'appointment fields')
        key=bytes.fromhex(trusted['public_key'])
        need(len(key)==32 and trusted['algorithm']=='ED25519-RFC8032' and H(key)==trusted['key_fingerprint_sha256'],'appointed key')
        need(all(isinstance(x,str) and x for x in trusted.values()),'appointment values')
        need(all(identifier(trusted[k]) for k in ('authority_id','owner_source_id','owner_anchor')),'appointment identifiers')
        return True
    except (ValueError,KeyError,TypeError):return False

def validate_closed(profile,program,trusted,evidence_objects,*,admission,contexts=None,comparison_history=None,authenticated_mapping=None,outer_profile_bytes=None,outer_profile_sha256=None):
    """Total ordered decision over structural, authority, evidence and policy gates.

    A bundle contains COMPOSITION plus every component, with no extras. Values
    are (four-file-object, object-digest). Admission and occurrence kinds cannot
    be interchanged. An optional outer binding must supply both exact bytes and
    digest; the privacy subobject remains the signed model identity in these
    author vectors. Full admission requires the outer binding produced by
    bind_outer; the lower-level subobject validator remains usable for vectors.
    """
    failures=set()
    try:
        program=revalidate_program(program)
        regenerated=bind_program(profile,program)
        validate_body(profile.source_owned_body,program,profile,profile.source_identities)
        regenerated_outer=bind_outer(regenerated,program,profile.source_owned_body,profile.source_identities)
        if regenerated_outer!=getattr(profile,'outer_bytes',None):failures.add('PROFILE-DIGEST-MISMATCH')
        if regenerated.bytes!=profile.bytes or regenerated.relation_bytes!=profile.relation_bytes:failures.add('INVALID-PROFILE-SCHEMA')
        if regenerated.labels!=profile.labels or regenerated.surface_bytes!=profile.surface_bytes or regenerated.surfaces!=profile.surfaces:failures.add('INVALID-SURFACE-LABELS')
        if H(profile.bytes)!=profile.sha256:failures.add('PROFILE-DIGEST-MISMATCH')
        # Every derived decision-bearing structure must agree. A malformed
        # cache is structural/schema failure, before signature or graph policy.
        for name in ('schemas','byfield','byid','relations','expression_dependencies'):
            if getattr(profile,name,None)!=getattr(regenerated,name):
                failures.add('INVALID-PROFILE-SCHEMA')
    except Exception:return ('FAIL','INVALID-PROFILE-SCHEMA')
    if not isinstance(outer_profile_bytes,bytes) or H(outer_profile_bytes)!=outer_profile_sha256 or outer_profile_sha256!=profile.binding_sha256 or outer_profile_bytes!=getattr(profile,'outer_bytes',None):failures.add('PROFILE-DIGEST-MISMATCH')
    # From here onward all scopes, universes, owning joins and policy checks
    # consume the same freshly rebuilt model, never the supplied caches.
    profile=regenerated
    if not appointment_valid(profile.appointment,trusted):failures.add('INVALID-EVIDENCE-AUTHORITY')
    expected={NA,*[c.id for c in profile.components]}
    if not isinstance(evidence_objects,dict) or set(evidence_objects)!=expected:failures.add('MISSING-EVIDENCE')
    try:
        if not admission:owning_records(profile,contexts,program,comparison_history,authenticated_mapping)
        tokens,links=universe(profile,contexts,admission=admission)
    except Exception:
        failures.add('INVALID-ACTION-CONTEXT');tokens=[];links=[]
    if any(c.necessity not in ('PREDICATE-INPUT','AUTHORIZATION-BINDING','ORDERING-COORDINATE','DEPENDENCY-COORDINATE') for c in profile.components):failures.add('UNNECESSARY-COMPONENT')
    if any(c.privacy=='PRIVATE-ACTOR' for c in profile.components):failures.add('PUBLIC-PRIVATE-VALUE')
    for s in profile.surfaces:
        if s.field in ('blind','opening') and s.exposure!='CONFIDENTIAL':failures.add('OPENING-DISCLOSURE')
        if s.exposure=='PUBLIC' and s.domain=='ACTION-IDENTITY' and s.reuse!='NONE':failures.add('REUSABLE-IDENTIFIER')
    if len(profile.components)!=len(program.components):failures.add('COMPONENT-COUNT-MISMATCH')
    # Collect independently testable failures before applying priority. In
    # particular, bad context cannot hide an earlier bad signature. The lower
    # verifier checks appointment before using its key.
    component_failed=False
    for component in [c.id for c in profile.components]+[NA]:
        try:
            if not isinstance(evidence_objects,dict) or component not in evidence_objects:continue
            files,digest=evidence_objects[component]
            # Byte equality below verifies every signed cell, including claimed results.
            verdict,code=validate(profile,trusted,files,digest,tokens,links,admission=admission,component=component,components_pass=not component_failed)
            if verdict!='PASS':
                failures.add(code)
                if component!=NA:component_failed=True
            r=read_tsv(files['evidence.tsv'],EVIDENCE_HEADER)
            need(len(r)==1,'evidence row count')
            if r[0]['profile_sha256']!=profile.binding_sha256 or r[0]['profile_id']!=profile.id:failures.add('PROFILE-DIGEST-MISMATCH')
        except Exception:failures.add('INCOMPLETE-EVIDENCE-UNIVERSE')
    return ('FAIL',first_failure(failures)) if failures else ('PASS','NONE')
````

<a id="pe-protocol-specification-g3-sem-authorization"></a>
### E266-SEM-AUTHORIZATION

An authorization is the concatenation of the complete canonical header TSV and the complete COMPONENT-BINDING TSV, each with its exact header and terminal LF, with no separator or additional prefix between them. The component table has one ordered row per projection component. SHA-256 of these complete bytes is the comparison attempt authorization_sha256; it is not a field in its own preimage. The original header context digest and blinded-component preimage remain unchanged. The header schema is:

field_order, field_name, field_value

Its exact rows, in order, are:

0001 serialization-domain PE-TSE-AUTHORIZATION-V1
0002 successor-generation-id SUCCESSOR-GENERATION-ID
0003 mapping-id mapping identifier
0004 mapping-sha256 mapping digest
0005 profile-id profile identifier
0006 profile-sha256 profile digest
0007 authorization-id authorization identifier
0008 transition-occurrence-id U identifier
0009 determination-id D identifier
0010 authorized-state-id Q0 identifier
0011 successor-state-relation-definition-id profile definition reference
0012 ordering-coordinate-set-digest coordinate-set digest defined in this block
0013 dependency-coordinate-set-digest coordinate-set digest defined in this block
0014 component-count ORD6 count

Each literal label and value is UTF-8 NFC. The canonical header bytes are the canonical TSV header field_order, field_name, field_value plus those rows and one terminal LF. authorization-context-digest is SHA-256 of those bytes.

Ordering and dependency coordinate sets use schema coordinate_order, coordinate_definition_id, canonical_value_hex. Rows are contiguous, definition-unique and definition-order sorted. The set digest is SHA-256 of the complete canonical TSV including header and terminal LF. Empty sets are header-only TSVs, not omitted values.

The component-binding schema is:

component_order, component_id, binding_mode, canonical_type_id, authorization_context_digest, bound_value

For CANONICAL-VALUE, bound_value is lowercase hexadecimal of the exact normalized canonical bytes. For BLINDED-SHA256-COMMITMENT, it is the commitment digest from E266-SEM-COMMITMENT. The authorization is valid only when all profile components appear once in profile order and the context digest equals the recomputed header digest.

<a id="pe-protocol-specification-g3-sem-commitment"></a>
### E266-SEM-COMMITMENT

The algorithm identifier is PE-TSE-SHA256-COMMITMENT-V1. Its protocol-owned algorithm is SHA-256 as defined by FIPS PUB 180-4. An implementation convention cannot substitute or reinterpret it.

The blind is exactly 32 octets produced by a cryptographically secure random-bit generator whose security claim includes at least 256 bits of input entropy. It must be independently generated for each component and authorization, retained only as confidential opening material, never reused, never derived from actor, enrollment, admission, action, state or other blinds, and never disclosed outside an authorized comparison or independent privacy-validation boundary.

The commitment preimage contains, in order:

1. UTF-8 bytes PE-TSE-COMPONENT-COMMITMENT-V1;
2. authorization-context-digest as 32 raw octets;
3. component identifier UTF-8 bytes;
4. canonical type identifier UTF-8 bytes;
5. canonical component bytes;
6. the 32 raw blind octets.

Items 1, 3, 4 and 5 are encoded as unsigned 64-bit big-endian byte length followed by the exact bytes. Items 2 and 6 are raw fixed 32-octet values without length prefixes. The commitment is SHA-256 of the complete preimage and is textually represented by 64 lowercase hexadecimal characters.

Opening supplies the canonical component bytes and blind through the confidential comparison boundary. Verification recomputes the context digest, preimage and commitment; authenticates the opening source; and requires exact digest equality. The opened authorized value is then evaluated against the independently obtained current value using the profile's equivalence, immaterial-difference and material-conflict definitions. Commitment equality is neither required nor sufficient for semantic equivalence.

Missing, malformed, unauthenticated or mismatched openings, invalid algorithms, canonicalization failure and detected collision evidence produce indeterminate and prohibit execution and commitment. An observed pair of distinct preimages with equal digest invalidates every affected authorization and requires a future-generation algorithm change. Without such evidence, the commitment establishes computational binding only under SHA-256 collision resistance; it does not prove mathematical injectivity, actor identity, admission, provenance, broader state correctness or any unencoded fact.

<a id="pe-protocol-specification-g3-sem-comparison"></a>
### E266-SEM-COMPARISON

Procedure identifier: PE-TSE-COMPARISON-V2.

Each comparison attempt identity is `{U-ID}-TSE-CMP-{ORD6}`. Ordinals begin `000001` and are contiguous within U. The exact attempt fields, in order, are attempt ID; generation ID; mapping ID and digest; profile ID and digest; authorization ID and digest; U ID; D ID; Q0 ID and digest; current-state ID and digest; stage; result; failure code. Stage is `PRE-EXECUTION` or `PRE-COMMITMENT`. Result is `equivalent`, `material-conflict` or `indeterminate`.

Evaluation executes in this order: validate identity grammar, registered relationships and digests; validate profile, authorization, opening evidence and state authentication; evaluate equivalence expression `EQ`; evaluate sufficient-conflict expressions in profile order, producing `MC=TRUE` if any is TRUE, `MC=FALSE` if all are FALSE and `MC=UNRESOLVED` otherwise; then select the first matching row:

| Condition | Result | Failure code |
|---|---|---|
| identity, relationship, digest, profile, authorization, opening or authentication failure | indeterminate | the exact validation failure |
| `EQ=TRUE` and `MC=TRUE` | indeterminate | `INCONSISTENT-BOTH-TRUE` |
| `MC=TRUE` | material-conflict | `NONE` |
| `EQ=TRUE` and `MC=FALSE` | equivalent | `NONE` |
| `EQ=FALSE` and `MC=FALSE` | indeterminate | `INCOMPLETE-PROFILE-COVERAGE` |
| otherwise | indeterminate | `UNRESOLVED-REQUIRED-INPUT` |

The closed comparison failure codes, in order, are `NONE`, `INVALID-IDENTITY`, `UNREGISTERED-IDENTITY`, `DIGEST-MISMATCH`, `INVALID-PROFILE`, `INVALID-AUTHORIZATION`, `INVALID-OPENING`, `UNAUTHENTICATED-STATE`, `INCONSISTENT-BOTH-TRUE`, `INCOMPLETE-PROFILE-COVERAGE` and `UNRESOLVED-REQUIRED-INPUT`. Every attempt produces one immutable result and one code. Only equivalent permits the next gate. An independently sufficient authenticated conflict remains material-conflict despite unrelated unresolved input. No validation failure yields equivalence or absence of a result.

Evaluation failure and comparison indeterminacy are distinct. A comparison returns one immutable classification and code; unsuccessful Evaluation cannot manufacture D or an authoritative dependency graph. Comparison at commitment and the commitment decision form one indivisible protocol-semantic boundary. No implementation transaction is elevated to protocol authority.

<a id="pe-protocol-specification-g3-sem-recovery"></a>
### E266-SEM-RECOVERY

The recovery TSV uses the literal header given below. It has exactly 21 data rows. There is no `ANY` token in serialized output.

| Order | Stage | Event | D sufficiency | U classification | Authorization | Evaluation | D | Authorization required | U required | Execute | Commit |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0001 | PRE-EXECUTION | equivalent | NOT-APPLICABLE | ACTIVE | PRESERVE | SAME | SAME | SAME | SAME | PERMIT | PROHIBIT |
| 0002 | PRE-EXECUTION | material-conflict | TRUE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0003 | PRE-EXECUTION | material-conflict | FALSE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0004 | PRE-EXECUTION | material-conflict | UNRESOLVED | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0005 | PRE-EXECUTION | indeterminate | TRUE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0006 | PRE-EXECUTION | indeterminate | FALSE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0007 | PRE-EXECUTION | indeterminate | UNRESOLVED | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0008 | EXECUTION | execution-failure | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0009 | EXECUTION | execution-failure | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0010 | EXECUTION | execution-failure | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0011 | PRE-COMMITMENT | equivalent | NOT-APPLICABLE | ACTIVE | PRESERVE | SAME | SAME | SAME | SAME | PROHIBIT | PERMIT |
| 0012 | PRE-COMMITMENT | material-conflict | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0013 | PRE-COMMITMENT | material-conflict | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0014 | PRE-COMMITMENT | material-conflict | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0015 | PRE-COMMITMENT | indeterminate | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0016 | PRE-COMMITMENT | indeterminate | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0017 | PRE-COMMITMENT | indeterminate | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0018 | PRE-COMMITMENT | revalidation-failure | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0019 | PRE-COMMITMENT | revalidation-failure | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0020 | PRE-COMMITMENT | revalidation-failure | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0021 | COMMITMENT | commitment-success | NOT-APPLICABLE | COMMITTED | CONSUMED | SAME | SAME | NONE | NONE | PROHIBIT | COMPLETE |

The lookup key is the exact triple `(stage,event,unchanged_d_sufficiency)`. For `equivalent` and `commitment-success`, sufficiency must be `NOT-APPLICABLE`; for every other event it must be TRUE, FALSE or UNRESOLVED. Exactly one row therefore matches every admitted event. Unmatched or multiply matched input is invalid and yields no permission. `NEW-ON-SUCCESSFUL-COMPLETION` retains the Engineering[250] meaning. No failed U may be repaired, resumed, reactivated or committed.

The exact recovery header, with spaces below denoting TAB, is:

```text
recovery_order stage event unchanged_d_sufficiency u_classification authorization_disposition evaluation_required determination_required authorization_required u_required execute_permission commit_permission
```

The Markdown table above supplies its 21 rows in order without transformation. An indeterminate comparison does not prove substantive state conflict or invalidity. The terminal stale authorization follows the failed bounded U disposition; it does not retrospectively alter D or a prior successful Evaluation. New Evaluation produces new D only on successful completion. No failed U is resumed, repaired, reactivated or committed.
