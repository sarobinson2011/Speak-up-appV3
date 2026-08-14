# Privacy Engine Complete Implementation Profile V2 Implementation-Assessment Basis and Scope Determination V1

Determination date: 2026-08-14.

STATE.md remains the single canonical development authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

## 1. Purpose and Determination Status

This document defines the fixed baselines and bounded scope for a later
assessment of the current Privacy Engine implementation.

It answers one architectural question:

> Can one exact implementation baseline and one complete assessment boundary
> be fixed against accepted Complete Implementation Profile V2 without yet
> assessing the implementation?

Determination status: **basis and scope determined**.

Engineering[165] determines:

> Privacy Engine Complete Implementation Profile V2 implementation-assessment basis and scope determined

This is a preparation record. It performs no requirement-level assessment and
records no implementation result.

## 2. Plain-Language Baseline

Two fixed baselines now exist:

- the requirements baseline is accepted Privacy Engine Complete Implementation
  Profile V2;
- the implementation baseline is the complete tracked Speak-up-appV3
  implementation state at the pushed `engineering-164` tag.

Engineering[165] identifies what will later be compared.

It does not perform the comparison.

The baseline relation is:

> accepted requirements baseline
> -> identified implementation baseline
> -> later bounded assessment

## 3. Scope

This determination defines:

- the fixed Profile V2 assessment basis;
- the exact tracked implementation revision;
- the included and excluded implementation boundaries;
- the application and implementation-structure boundaries;
- permitted evidence classes;
- evidence provenance, stability, and privacy requirements;
- later full-ledger coverage;
- assessment-readiness conditions;
- and explicit failure conditions.

It does not determine whether the implementation satisfies any requirement.

This record is informative and derivative. It contains no normative requirement
statements and acquires no protocol authority.

## 4. Authority and Dependency Position

The governing direction remains:

> Published Protocol Specification V1
> -> accepted Complete Implementation Profile V2
> -> implementation-assessment basis and scope
> -> later implementation assessment
> -> any later conformance or certification work

Profile V2 defines the implementation-facing target.

The implementation baseline provides the later assessment subject.

Neither this record nor the implementation may modify the profile or published
protocol meaning.

## 5. Guarded Documentation Baselines

| Artifact | Guarded SHA-256 |
|---|---|
| Synchronized Complete Implementation Profile V2 | `279fc80cb2998df8c4fddcc2ea25e4091897571c57a7d5905100857612b2d79c` |
| Engineering[164] Status Synchronization Record | `d8bce61c2366e4a5ca6d6d87ef4875944956acd1b8303e73f2f901c7a1ba1e27` |
| Engineering[163] V2 Composition Re-review | `093f3d2178bc890e7bed9dc56aea164f36918a01e49caef2ed8d777777dd0d11` |
| Engineering[162] Identity/Version Correction Record | `c37a3fa1985a11243ff0b1103d5d7ca911f77e76a14f00f4c12a368e4f7ad88a` |
| Corrected Complete Implementation Profile V1 | `2570e94fa7d06a3f136b5384bd879e343a25bbb33c3b4fc3f7c9ee0ecb1b9b23` |
| Engineering[161] Composition Re-review | `fe51c48bb7992482ca341af943b396b46457773999452d1cfb2a02807557bc41` |
| Engineering[160] Composition Correction | `6c8cbe0ffe6687045375f33c2316a1baf8ee1d026cfde1bfdc258769d70d4b26` |
| Engineering[159] Composition Review | `5855fa1765a8492e08f7718c7c6b7d400fff343e03caa666f9a5fdeaa6184709` |
| Implementation Profile Scope Determination | `03fe5d180a4056c6e66356c1804f8883006daab52a80ec12676483ad75fd0a17` |
| Published Protocol Specification V1 | `f2c12b60f24fe8fe8eddf27dc2d59814aceba42b907160c54ad3868bde7da393` |
| Publication Record | `d655359c296d6d6aefffd3e6faa0fd47f6506ec9d64a871ade9f9eb469108029` |
| Final Specification Consolidation Re-review | `7bf415870a2e630157d1cf186e45764513e87b5f13b2ac790373d4de5df13bb7` |

Every guarded artifact matched before this record was created.

## 6. Implementation Baseline Identity

The implementation baseline is:

> Complete tracked Speak-up-appV3 Privacy Engine implementation state at the
> pushed `engineering-164` tag

| Baseline field | Fixed value |
|---|---|
| Repository | Speak-up-appV3 |
| Selected branch position | `main` |
| Baseline tag | `engineering-164` |
| Baseline commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Baseline Git tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |
| Tracked paths in baseline tree | 308 |
| Competing implementation branch selected | None |

The commit and tree identifiers fix the exact tracked repository state.

The baseline remains distinct from the protocol generation, Protocol
Specification, Profile V2, deployments, runtime observations, evidence,
assessment results, applications, and Private Actors.

## 7. Baseline Stability

The baseline is immutable for this assessment preparation.

Later commits, changed tracked files, generated artifacts, configuration
changes, dependency changes, deployments, or operational changes do not
silently alter it.

If later work chooses a materially changed implementation state, that state
must receive a new exact baseline and a separately bounded assessment.

No other branch or revision is merged into this baseline.

## 8. Included Assessment Boundary

The future assessment includes tracked protocol-facing implementation material
at the baseline revision, including where present:

- protocol-facing contract implementations and their declared relationships;
- proof circuits, verification machinery, and tracked generated cryptographic
  artifacts;
- frontend protocol-facing proof, identity-continuity, interface, and action
  behavior;
- backend protocol-facing relay, path, indexer, persistence, and interface
  behavior;
- runtime enforcement, submission, verification, validity, uniqueness,
  transition, state, and failure behavior;
- configuration schemas, build inputs, dependency locks, deployment
  descriptors, and tracked interface artifacts;
- protocol-facing integration across implementation components;
- privacy, unlinkability, neutral naming, logging, diagnostic, and
  observability behavior;
- and tracked tests or verification material used as later evidence.

Inclusion identifies material eligible for later assessment. It does not state
that the material is complete, correct, or sufficient.

## 9. Excluded Assessment Boundary

The future assessment excludes:

- untracked, ignored, dirty, or later-created workspace state;
- another commit, tag, branch, build, or implementation revision;
- private keys, secrets, credentials, and Private Actor material;
- application-owned petition meaning, policy, lifecycle, moderation,
  eligibility, metadata, UI interpretation, and business truth;
- unrelated application presentation or operational administration;
- third-party provider internals not owned by the implementation;
- live deployment or runtime instance identity as implementation identity;
- protocol, profile, assessment, conformance, certification, or Reference
  Implementation authority inferred from the codebase;
- and any requirement or behavior outside accepted Profile V2.

Exclusion from this assessment boundary does not delete, deprecate, approve, or
declare defective any application-owned or operational behavior.

## 10. Application and Speak-up Boundary

Speak-up remains the first reference use case.

Protocol-facing behavior implemented through Speak-up may be assessed where it
realizes an applicable Profile V2 obligation.

Petition identity, meaning, lifecycle, metadata, moderation, eligibility,
policy, UI, and interpretation remain application-owned and do not become
assessment criteria.

Application code may therefore contain both included protocol-facing behavior
and excluded application-owned behavior. Inclusion follows responsibility, not
directory or filename alone.

## 11. M2, TEMPEST, and REFLECT Boundary

M2, TEMPEST, and REFLECT remain implementation structures only.

Their tracked implementation behavior may supply later evidence for applicable
Profile V2 obligations.

Their names, decomposition, algorithms, topology, repository structure, and
current behavior do not become profile identity, required implementation
design, protocol law, or a comparison standard for another implementation.

## 12. Fixed Profile V2 Assessment Basis

The assessment basis is exactly:

> Privacy Engine Complete Implementation Profile V2

The basis preserves:

- V2 identity and version;
- status `composition accepted`;
- the Generic Complete Privacy Engine Protocol Implementation Target;
- all 729 ledger rows in published order;
- exact RF, SF, strength, and published-applicability mappings;
- all dispositions and permitted-choice boundaries;
- zero unresolved profile conditions, choices, and dependencies;
- zero external Implementation Profile dependencies;
- implementation freedom;
- application separation;
- privacy boundaries;
- and protocol authority.

The implementation baseline cannot narrow, widen, repair, reinterpret, or
optimize this basis.

## 13. Full-Ledger Coverage

Later assessment must account for the complete Profile V2 ledger:

| Profile V2 disposition | Required later coverage |
|---|---:|
| Applicable | 478 |
| Conditionally applicable | 0 |
| Non-applicable | 244 |
| Resolved through permitted specification choice | 7 |
| Total stable identifiers | 729 |

Every identifier must remain in published order.

The 478 applicable dispositions define obligations requiring later supported
assessment.

The 244 non-applicable dispositions remain preserved profile-scope decisions;
they do not become implementation-created exclusions.

Engineering[165] assigns no requirement-level result.

## 14. Permitted-Choice Coverage

The seven permitted-choice rows remain:

- `PE-EVOL-018`;
- `PE-IFACE-009`;
- `PE-RUNTIME-005`;
- `PE-IMPL-005`;
- `PE-IMPL-011`;
- `PE-IMPL-013`;
- `PE-REALIZE-009`.

Later assessment must identify the baseline implementation's evidenced choice
position for each row without inventing a default or widening the permitted
choice space.

No choice is selected or evaluated by this determination.

## 15. Permitted Evidence Classes

Later assessment may use bounded evidence classes including:

- Git commit, tree, tracked-path, and tracked-blob evidence;
- source and interface files;
- tracked generated cryptographic artifacts and integrity manifests;
- dependency locks, build inputs, and deterministic build outputs;
- contract bytecode and deployment-relationship evidence;
- configuration-schema and deployment-descriptor evidence;
- automated tests and static verification;
- execution traces and runtime observations;
- success, rejection, and failure-path evidence;
- privacy-boundary, naming, logging, diagnostic, and observability evidence;
- protocol-facing interface evidence;
- and bounded supporting documentation.

This list permits evidence types. It does not determine that any evidence item
exists or is sufficient.

## 16. Evidence Provenance, Integrity, and Stability

Every later evidence item must:

- identify its exact source and applicable baseline relationship;
- be attributable to the fixed implementation baseline or to one declared
  observation of that baseline;
- preserve content integrity through an appropriate immutable identifier or
  digest;
- identify build, configuration, deployment, or observation context where
  materially relevant;
- remain reproducible or independently inspectable where the evidence class
  permits;
- distinguish historical evidence from later replacement evidence;
- and remain bounded to the requirement and scope for which it is used.

Evidence from another implementation state cannot silently support this
baseline.

## 17. Baseline, Evidence, and Result Separation

The required distinctions are:

> implementation baseline != evidence item

> evidence item != requirement identity

> evidence existence != evidence sufficiency

> test success != requirement satisfaction

> runtime success != complete implementation satisfaction

> assessment result != conformance or certification

Documentation claims may direct inspection but do not replace implementation
evidence.

## 18. Deployment and Runtime Evidence Boundary

Deployment and runtime instances are evidence associated with the fixed
implementation baseline. They are not the baseline's identity.

Later use of deployment evidence must identify, where relevant:

- the baseline source relationship;
- network and chain context;
- deployed code or bytecode identity;
- proxy and implementation relationships;
- configuration and dependency state;
- observation interval or occurrence;
- and any material difference from the baseline tree.

An unproven deployment-to-baseline relationship must fail as evidence rather
than silently redefine the candidate.

## 19. Privacy and Neutral Naming

The determination preserves:

> Private actors, public actions.

Baseline, evidence, requirement, report, test, diagnostic, and observability
naming must remain neutral.

No assessment surface may introduce Private Actor identity, reusable
participant identity, cross-action identity continuity, actor linkage,
enrollment or admission provenance, wallet, sponsor, funding, ownership, or
application-account provenance, metadata correlation, transport provenance, or
an actor-reconstruction bridge.

Naming and documentation surfaces remain part of the privacy boundary.

## 20. Assessment-Readiness Conditions

Later implementation assessment may begin only when:

1. the `engineering-164` baseline remains retrievable and integrity-verifiable;
2. the Profile V2 basis remains byte-for-byte at its guarded hash;
3. included and excluded responsibilities can be applied without ambiguity;
4. evidence can be bound to the baseline without silently mixing revisions;
5. all 729 identifiers can be represented in published order;
6. every applicable row has a defined evidence and evaluation path;
7. every permitted-choice row has a bounded candidate-choice evidence path;
8. deployment and runtime observations remain distinguishable from baseline
   identity;
9. application-owned behavior remains separated from protocol-facing behavior;
10. privacy-safe evidence handling and neutral naming are preserved;
11. no required evidence class depends upon Private Actor reconstruction; and
12. unsupported or ambiguous evaluation can fail explicitly.

These are readiness conditions, not findings that evidence is sufficient.

## 21. Failure Model

Let:

- `F2` be accepted Complete Implementation Profile V2;
- `I164` be the tracked implementation baseline at `engineering-164`;
- `C` be the bounded assessment scope;
- `E` be the evidence boundary;
- `D` be this determination.

Required success path:

> fix(F2)
> -> identify(I164)
> -> bound(C, I164)
> -> defineEvidenceBoundary(E, I164, C)
> -> determineBasisAndScope(D)

Required preservation:

> basis(D) = F2

> baseline(D) = I164

> scope(D) = C

> noAssessmentResult(D)

Failure path:

> ambiguousBaseline or changedBasis or unboundedScope or incoherentEvidence
> -> fail

Forbidden path:

> inferBaseline or mergeRevisions or repairProfile or widenScope or
> assessRequirement
> -> invalid

## 22. No Assessment Results

Engineering[165] records no classification of any requirement as passed,
failed, satisfied, unsatisfied, supported, unsupported, conformant, or
non-conformant.

It does not identify implementation defects, recommend repairs, or determine
whether available evidence is substantively sufficient.

The current implementation remains unassessed.

## 23. Conformance, Certification, Security, and Reference Boundary

This determination does not:

- establish compatibility;
- establish conformance;
- create a Conformance Claim, Assessment, or Determination;
- issue or support certification;
- assess security;
- assess operational readiness;
- designate the implementation as a Reference Implementation;
- or make the baseline a required design for another implementation.

Any such work remains later, distinct, and separately bounded.

`PE-REFIMPL-017` remains applicable and preserves implementation freedom.

## 24. Protocol, Publication, and Profile Preservation

Engineering[165] creates no:

- protocol change or new protocol generation;
- Protocol Specification V2;
- new Protocol Publication occurrence;
- new Profile identity or version;
- Profile V3;
- profile disposition change;
- normative requirement or stable-identifier change;
- implementation modification;
- or status change to any existing artifact.

`PE-PROFILE-015` remains applicable. The already-established V2 identity remains
unchanged, and this determination does not semantically change Profile V2.

## 25. Findings

The basis-and-scope assessment found:

- accepted Profile V2 supplies one fixed requirements baseline;
- the `engineering-164` tag, commit, and tree supply one exact tracked
  implementation baseline;
- no competing branch or implementation revision is selected or merged;
- the included and excluded responsibility boundaries are coherent;
- deployment and runtime instances remain evidence rather than baseline
  identity;
- later evidence classes and integrity conditions are bounded;
- complete 729-row later coverage is required;
- application and implementation-structure separation is preserved;
- privacy and neutral naming are preserved;
- implementation freedom and protocol authority are preserved;
- and no implementation assessment result is produced.

No blocking or non-blocking basis-and-scope finding remains.

## 26. Determination

Engineering[165] determines:

> Privacy Engine Complete Implementation Profile V2 implementation-assessment basis and scope determined

This means only:

- Profile V2 is fixed as the requirements baseline;
- the complete tracked implementation at `engineering-164` is fixed as the
  implementation baseline;
- one assessment boundary is defined;
- permitted evidence classes and integrity requirements are defined;
- and the baseline is ready for a separately bounded implementation-assessment
  phase once the stated readiness conditions are met.

It does not mean that the baseline satisfies Profile V2.

## 27. Future Position

The next permitted direction is:

> fixed Profile V2 requirements baseline
> -> fixed `engineering-164` implementation baseline
> -> separately bounded implementation assessment

The later assessment must preserve this determination's baseline and scope or
create a new explicit basis-and-scope record.

Implementation change, remediation, compatibility, conformance, certification,
security assessment, operational-readiness assessment, and Reference
Implementation designation remain outside Engineering[165].

## 28. Explicit Exclusions

Engineering[165] does not:

- modify STATE.md or any existing formal artifact;
- modify the implementation baseline;
- change Profile V2 or its 729-row ledger;
- copy normative requirement statements;
- introduce SF-17 or RF-51;
- reopen the ontology;
- create a new protocol generation, specification, profile, or publication;
- derive profile meaning from implementation behavior;
- silently select or merge another revision;
- treat deployment identity as implementation identity;
- assess any requirement;
- create requirement-level results;
- identify or repair an implementation defect;
- establish compatibility, conformance, certification, security, or
  operational readiness;
- designate a Reference Implementation;
- require another implementation to reproduce this baseline;
- introduce application-owned semantics into the assessment basis;
- or introduce identity linkage or correlation-bearing naming.

## 29. Conclusion

Engineering[165] fixes the accepted Profile V2 requirements baseline and the
complete tracked Speak-up-appV3 implementation baseline at `engineering-164`.

It defines the included and excluded assessment boundary, permitted evidence
classes, integrity and privacy requirements, complete later ledger coverage,
readiness conditions, and explicit failure behavior.

The implementation remains unassessed.

Determination: **Privacy Engine Complete Implementation Profile V2 implementation-assessment basis and scope determined**.

Protocol authority always remains with the published Privacy Engine protocol generation.
