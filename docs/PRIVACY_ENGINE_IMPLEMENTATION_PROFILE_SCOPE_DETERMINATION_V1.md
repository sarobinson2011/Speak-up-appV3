# Privacy Engine Implementation Profile Scope Determination V1

Publication date: 2026-08-11.

STATE.md remains the single canonical development authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

## 1. Purpose

This document determines the first bounded Implementation Profile target derived
from Privacy Engine Protocol Specification V1.

It answers one architectural question:

> What is the first bounded implementation target for the published Privacy
> Engine Protocol Specification V1?

This record determines profile scope and the next composition step.

It does not create the Implementation Profile itself.

## 2. Scope

This determination assesses:

- profile identity;
- target identity and boundedness;
- included and excluded capabilities;
- generic versus application-specific scope;
- single-profile versus multiple-profile composition;
- the future classification of all 729 normative requirements;
- permitted-choice handling;
- mandatory-obligation preservation;
- privacy and neutral naming;
- application, runtime, implementation, compatibility, conformance, and
  certification boundaries;
- and the exact next composition step.

This record is informative and derivative.

It is not a normative protocol source and has an expected normative citation
count of zero.

## 3. Authority and Dependency Position

The governing dependency direction is:

> Published Protocol Generation
> -> Published Protocol Specification
> -> Implementation Profile
> -> Implementation
> -> Conformance
> -> Certification

The source specification derives from the published protocol generation.

The future profile derives from the source specification.

The future implementation realizes the profile.

No downstream layer acquires authority to redefine an upstream layer.

The scope-selection relation is:

> select(S, T)
> -> preservedSelection(S, T)

If the selected target cannot preserve an applicable requirement:

> select(S, T)
> -> fail

The forbidden paths are:

> select(S, T)
> -> weaken(R)

> select(S, T)
> -> removeMandatory(R)

> select(S, T)
> -> inventProtocolSemantics(R')

Protocol authority always remains with the published Privacy Engine protocol generation.

## 4. Guarded Baselines

The assessment used the following guarded published baselines:

| Baseline | Verified value |
|---|---|
| Specification identity | Privacy Engine Protocol Specification V1 |
| Accepted pre-publication specification SHA-256 | `924eaf297edcc3673a38f65069a804ad44d0e88b1458f0ddfa42e973b1a73216` |
| Published-status specification SHA-256 | `f2c12b60f24fe8fe8eddf27dc2d59814aceba42b907160c54ad3868bde7da393` |
| Publication-record SHA-256 | `d655359c296d6d6aefffd3e6faa0fd47f6506ec9d64a871ade9f9eb469108029` |
| Engineering[155] final review SHA-256 | `7bf415870a2e630157d1cf186e45764513e87b5f13b2ac790373d4de5df13bb7` |
| Normative rows | 729 |
| Unique stable identifiers | 729 |
| Semantic-identifier families | 50 |
| All-normative-row SHA-256 | `b758510ded0d650c5e7728967420a6cf9ff85bab53e829ecb4cf102d768530b5` |
| Undeclared 715-row SHA-256 | `a168364c6696efe00b816fb3e333362d5125edbf48a4a6e5dfbd0aaf0c8be431` |
| Ordered identifier-sequence SHA-256 | `9c331b1bbf8a3639bdb11d6e4caf12eaab7cee26fae040ba2990746b6cfad404` |
| Section 3 SHA-256 | `1f8aa38da6a398431a1a1eb5adfd073c466c7bef993d86e490f3d552f293ecc1` |
| Section 8 SHA-256 | `b893860e99405ab0f08421c63d57c7d91e6c3fab09d2d664e115675f366bb61a` |
| Section 38 source-table SHA-256 | `3ecc7e24673006f88f481e2020a72e66ccf0cc8ed454d8d2dde29db28766accb` |
| Publication determination | `published` |

Every attached guarded artifact matched its expected SHA-256 before this record
was created.

## 5. Assessment Method

The assessment:

1. verified the published specification and Publication Record;
2. reconstructed all normative-row and identifier digests;
3. verified all fifty complete identifier families;
4. preserved the intentional historical PE-SURF ordering;
5. verified exact Section 8 and composition-map agreement;
6. resolved every S01–S68 source;
7. inspected the Implementation Profile, Implementation, Protocol Realization,
   and Reference Implementation models;
8. inspected application, adapter, runtime, integration, compatibility,
   conformance, certification, privacy, and authority boundaries;
9. assessed each candidate target independently of the current codebase;
10. tested whether all 729 requirements can receive exactly one justified
    profile disposition;
11. tested whether one coherent first target is sufficient;
12. and applied failure rather than semantic repair wherever preservation would
    be impossible.

## 6. Published Specification Integrity

The published specification remains unchanged.

The assessment verified:

- 729 normative rows;
- 729 unique stable identifiers;
- fifty complete semantic-identifier families;
- all expected family counts;
- exact RF-01 through RF-50 coverage;
- exact Section 8 RF/SF mapping agreement with the composition map;
- the fourteen Engineering[152] corrected rows;
- the 715-row undeclared preservation digest;
- exact S01–S68 source coverage and resolution;
- RF-42 Implementation Profile requirements;
- RF-49 semantic-preservation closure;
- RF-50 explicit-exclusion closure;
- and PE-EXCLUDE-026.

The Publication Record identifies the resulting specification artifact and
determines it `published`.

No normative composition, acceptance, readiness, or publication question is
reopened.

## 7. Implementation Profile Model Constraints

A valid Implementation Profile is:

- uniquely identified;
- derived from exactly one identified Protocol Specification;
- bounded to one declared implementation target;
- complete relative to that target;
- explicit about applicability;
- explicit about permitted choices and dependencies;
- and incapable of acquiring protocol authority.

For every normative requirement `R` in source specification `S`:

> contains(S, R)
> -> classifyForTarget(R, T)

For every applicable requirement:

> applies(F, R)
> -> meaning(F, R) = meaning(S, R)

> applies(F, R)
> -> strength(F, R) = strength(S, R)

> applies(F, R)
> -> applicability(F, R) = preservedApplicability(S, R, T)

Profile narrowing may select a bounded target.

It may not weaken obligations governing that target.

## 8. Candidate Target Boundaries

Four candidate boundaries were assessed:

1. one generic complete Privacy Engine implementation target;
2. one bounded protocol-role or capability target;
3. one application-specific Speak-up implementation target;
4. multiple coordinated implementation targets.

The candidates were assessed for:

- semantic completeness;
- independent implementability;
- future assessability;
- application portability;
- privacy preservation;
- stable identity;
- profile dependency complexity;
- implementation neutrality;
- and ability to classify all 729 requirements without changing published
  semantics.

## 9. Candidate Comparison

| Candidate | Result | Architectural reason |
|---|---|---|
| Generic complete Privacy Engine implementation target | Selected | Provides one stable, application-independent, end-to-end protocol realization and future conformance target |
| Bounded protocol-role or capability target | Rejected as the first target | Prematurely fragments obligations whose validity and preservation cross capability boundaries |
| Application-specific Speak-up target | Rejected | Couples profile identity to petition semantics and weakens portability |
| Multiple coordinated first targets | Rejected | No published architectural requirement currently makes multiple profiles necessary |

The rejection of the alternatives does not prohibit later profiles.

A later profile requires its own distinct, bounded, and specification-derived
target.

## 10. Selected First Target

The selected target is:

> Generic Complete Privacy Engine Protocol Implementation Target

The target denotes one complete composite implementation class capable of
realizing the protocol-owned semantics applicable to an end-to-end Privacy
Engine operation.

It is generic to the Privacy Engine.

It is not specific to petitions, one repository, one deployment, one technology,
or one internal component structure.

The target is independently implementable and provides one coherent future
conformance target.

## 11. Profile Identity

The future profile to be composed for the selected target has the bounded
identity:

> Privacy Engine Complete Implementation Profile V1

That identity denotes one profile definition derived from Privacy Engine
Protocol Specification V1 for the selected generic complete implementation
target.

It remains distinct from:

- the published protocol generation;
- Privacy Engine Protocol Specification V1;
- this scope-determination record;
- every implementation;
- every application;
- every Reference Implementation;
- every Compatibility Profile;
- every conformance artifact or determination;
- and every certification.

This record reserves the bounded composition target.

It does not create or publish the profile.

## 12. Included Protocol Capabilities

The selected target includes the complete protocol-owned capability chain
applicable to end-to-end Privacy Engine operation:

- anonymous membership, private-secret continuity, and enrollment separation;
- private proof generation;
- declared public-input handling;
- proof verification and complete validity evaluation;
- nullifier-based uniqueness and action-bounded unlinkability;
- Protocol Operations and Protocol Actions;
- applicable protocol-rule selection;
- Evaluation and Determination;
- acceptance and rejection;
- accepted no-transition behavior;
- transition mapping, preconditions, eligibility, and authorization;
- transition execution, preservation, commitment, and atomicity;
- protocol state, successor state, and state evolution;
- protocol-state history and public protocol-state consequences;
- failure classification, stale authorization, and re-evaluation;
- Interface Contracts, Concrete Interface Specifications, Protocol Surfaces,
  Protocol Operations, and Published Results;
- runtime enforcement and execution responsibility;
- the protocol-facing side of the application boundary;
- implementation and realization obligations;
- privacy, unlinkability, minimum disclosure, and actor separation;
- semantic preservation;
- and every global exclusion governing downstream realization.

A capability explicitly permitted but not universally required by the source
specification remains subject to the classification and permitted-choice method
defined below.

## 13. Excluded Application and Implementation Material

The selected target excludes application-owned material, including:

- petition meaning;
- petition objects and lifecycle;
- application policy;
- application metadata;
- application UI;
- application moderation;
- application-specific permissions;
- application persistence and read models;
- application-specific outcome interpretation;
- and application truth.

It also excludes implementation-specific and operational material not made
normative by the published specification, including:

- programming language;
- source-tree structure;
- internal component decomposition;
- database and storage design;
- blockchain transaction format;
- relay architecture;
- transport;
- deployment topology;
- treasury management;
- monitoring;
- operational provisioning;
- and provider selection.

The application-owned adapter implementation is outside the selected engine
target.

The protocol-facing interface and every semantic-preservation obligation at
that boundary remain within scope.

## 14. Requirement-Classification Method

The future profile must process the 729 normative rows in their published order.

For each requirement `R`, composition must record:

- stable requirement identifier;
- RF family and authoritative SF home;
- published strength;
- published applicability;
- selected target relationship;
- exactly one profile disposition;
- justification;
- any exact published condition;
- any permitted-choice resolution;
- dependency effect;
- and preservation status.

The four permitted dispositions are:

1. applicable;
2. conditionally applicable;
3. non-applicable under an identified specification rule;
4. resolved through a permitted specification choice.

No requirement may disappear through omission.

A disposition must derive from:

> publishedApplicability(R)
> + selectedTarget(T)
> + declaredCapabilities(T)
> + publishedChoiceBoundary(R)
> + completeDependencyChain(R)

It must not derive from implementation convenience, current behavior, topology,
difficulty, preference, or a desired assessment result.

## 15. Applicability

A requirement is classified `applicable` when its published applicability
governs:

- the profile composition itself;
- the selected complete implementation target;
- a capability included unconditionally within the target;
- a downstream surface necessarily produced by the target;
- or a global privacy, authority, preservation, or exclusion boundary
  applicable to the profile or implementation.

Applicable requirements preserve:

- identity;
- meaning;
- strength;
- applicability;
- prohibitions;
- permissions;
- success behavior;
- failure behavior;
- and source traceability.

## 16. Conditional Applicability

A requirement is classified `conditionally applicable` only when the source
specification declares a condition whose truth determines whether it governs
the selected target.

The profile record must state:

- the exact published condition;
- the capability, occurrence, subject, or lifecycle state to which it applies;
- the applicable result when the condition is true;
- the non-applicable result when the condition is false;
- and any dependency activated by the condition.

Implementation preference must not be represented as a published condition.

An unresolved condition makes profile composition incomplete.

## 17. Non-Applicability

A requirement is classified `non-applicable` only when:

- its published applicability concerns a subject outside the selected target;
- the selected target explicitly excludes that subject;
- no included capability or dependency activates it;
- and the justification follows from the published specification.

Expected examples include requirements whose only subjects are:

- application-owned behavior outside the protocol-facing boundary;
- protocol-generation governance occurrences;
- Protocol Publication occurrences;
- Reference Implementation designation;
- compatibility declarations or assessments;
- conformance artifacts, claims, assessments, or determinations;
- or certification decisions, statuses, and recognition.

Non-applicability does not weaken a requirement.

It records that the published applicability does not govern the selected target.

## 18. Permitted Choices

A choice may be resolved only when the published specification expressly
permits that choice.

For each permitted choice, the future profile must record:

- the governing requirement;
- the complete published choice space;
- the selected or constrained choice;
- whether support is required, excluded, or left implementation-defined;
- the resulting applicability effect;
- and any identity, version, or dependency consequence.

The resolution must satisfy:

> selectedChoice(F, C)
> subsetOf permittedChoices(S, C)

The profile must reject:

- invented choices;
- widened choice spaces;
- prohibited behavior;
- mandatory behavior treated as optional;
- and required profile-level choices left unresolved.

## 19. Mandatory-Obligation Preservation

Every mandatory requirement governing the target remains mandatory.

The profile may not:

- reduce `MUST` to a recommendation or permission;
- reduce `MUST NOT` to discretionary avoidance;
- omit a mandatory success condition;
- omit a mandatory failure condition;
- replace published applicability;
- or substitute profile-local wording for the authoritative requirement.

The preservation model is:

> S
> -> selectedTarget(T)
> -> boundedPreservedProfile(F)
> -> realizedImplementation(I)

If preservation cannot be demonstrated:

> profileConstruction(F)
> -> fail

The failure path must not repair, infer, divide, merge, or synthesize a
replacement obligation.

## 20. Privacy and Unlinkability

The selected target preserves:

> Private actors, public actions.

The profile and every future realization must preserve:

- Private Actor separation;
- anonymous membership privacy;
- action-bounded nullifier meaning;
- cross-action unlinkability;
- minimum disclosure;
- proof and public-input boundaries;
- enrollment and admission separation;
- wallet separation;
- application-identity separation;
- implementation-identity separation;
- and non-identifying public consequences.

No profile classification or target metadata may become a participant identity
or actor-reconstruction bridge.

## 21. Neutral Naming and Anti-Correlation

Profile names, target names, classifications, dependency records, examples,
tests, diagnostics, logs, reports, and observability surfaces must remain
neutral.

They must not encode or imply:

- Private Actor identity;
- reusable participant identity;
- cross-action identity continuity;
- enrollment or admission provenance;
- wallet or ownership provenance;
- sponsor or funding provenance;
- transport or deployment provenance;
- hidden intent;
- or correlation-bearing application meaning.

Neutral naming remains part of the privacy boundary.

## 22. Application and Speak-up Boundary

Speak-up is the first reference use case.

It does not define the selected profile target.

Petition semantics remain application-owned, including:

- what a petition is;
- petition creation and lifecycle;
- petition metadata;
- application eligibility and moderation;
- application-specific display;
- and interpretation of public protocol consequences.

The generic target accepts an application-supplied public action context through
the applicable protocol-facing boundary.

It determines only the protocol-defined validity and consequence of the bounded
Privacy Engine operation.

The application determines the public meaning attached to that result.

The future profile may specify the conditions necessary for application-safe
integration without turning application behavior into protocol semantics.

## 23. Runtime and Implementation Boundary

The selected target defines what one complete implementation class must
preserve.

It does not prescribe how the implementation is internally constructed.

M2, TEMPEST, and REFLECT do not appear as named normative architecture in the
published Protocol Specification.

They may remain implementation structures through which current or future
implementations realize applicable published requirements.

Their names, current decomposition, repository locations, and operational
machinery do not become profile identity or protocol law.

Any implementation variation remains permitted only where all applicable
profile obligations are preserved.

## 24. Compatibility, Conformance, and Certification Boundary

This determination establishes none of:

- compatibility;
- a Compatibility Profile;
- conformance requirements;
- conformance evidence;
- a conformance assessment;
- a conformance determination;
- a certification basis;
- a certification decision;
- a certification status;
- or certification recognition.

The future profile will provide an identified target against which conformance
may later be assessed.

Creating that target is not itself an assessment.

A future conformance or certification process remains separately identified,
bounded, and downstream.

## 25. Protocol Authority

The selected target does not own protocol semantics.

The future profile may organize applicability and resolve explicitly permitted
choices.

It may not:

- modify the published protocol generation;
- amend the source specification;
- create a new protocol generation;
- change specification identity or version;
- create a new Protocol Publication;
- reinterpret application behavior as protocol law;
- or derive authority from an implementation.

The authority chain remains:

> Published Protocol Generation
> -> Privacy Engine Protocol Specification V1
> -> Privacy Engine Complete Implementation Profile V1
> -> implementation

Protocol authority always remains with the published Privacy Engine protocol generation.

## 26. Current-Codebase Assessment Boundary

The current Speak-up codebase is a possible future candidate implementation of
the selected profile.

Engineering[157] did not:

- inspect the codebase for profile satisfaction;
- derive target scope from current behavior;
- identify implementation defects;
- determine compatibility;
- determine conformance;
- assess security or operational readiness;
- issue certification;
- or create implementation work.

The direction remains:

> Published Specification
> -> selected target
> -> future Profile
> -> later implementation assessment

The forbidden direction remains:

> current implementation behavior
> -> inferred Profile
> -> rewritten specification

## 27. Findings

The assessment produced the following findings:

- F-01: the generic complete implementation target is bounded and coherent;
- F-02: it remains independent of application and repository structure;
- F-03: it provides one stable future conformance target;
- F-04: one first profile is sufficient;
- F-05: multiple profiles remain possible but are not currently required;
- F-06: all 729 requirements can receive exactly one justified disposition;
- F-07: permitted choices can be resolved without semantic change;
- F-08: mandatory obligations remain preservable;
- F-09: Speak-up and petition meaning remain outside protocol authority;
- F-10: privacy, unlinkability, and neutral naming remain preserved;
- F-11: M2, TEMPEST, and REFLECT remain implementation structures rather than
  profile authority;
- F-12: the current codebase remains outside assessment;
- F-13: compatibility, conformance, and certification remain unestablished;
- and F-14: protocol authority remains unchanged.

Blocking findings: **none**.

Non-blocking findings: **none**.

## 28. Scope Determination

The Engineering[157] determination is:

> first Implementation Profile scope determined

The selected first target is the Generic Complete Privacy Engine Protocol
Implementation Target.

The future profile identity is Privacy Engine Complete Implementation Profile
V1.

The profile will be generic to the Privacy Engine, complete relative to its
declared target, portable across application use cases, and independent of
current implementation structure.

## 29. Next Composition Step

The exact next composition step is:

> Compose Privacy Engine Complete Implementation Profile V1 from Privacy Engine
> Protocol Specification V1 for the selected Generic Complete Privacy Engine
> Protocol Implementation Target.

The composition must create:

`docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V1.md`

That composition must:

1. preserve the published specification and Publication Record unchanged;
2. process all 729 normative requirements in published order;
3. assign exactly one justified disposition to every requirement;
4. preserve every applicable requirement unchanged by identity and meaning;
5. identify every conditional applicability rule;
6. justify every non-applicable disposition from the published specification;
7. resolve only explicitly permitted choices;
8. record all dependencies and completeness conditions;
9. preserve privacy, unlinkability, neutral naming, application separation, and
   protocol authority;
10. fail if any requirement, choice, condition, or dependency remains
    unresolved;
11. and stop before implementation assessment, conformance, or certification.

This scope record does not perform that composition.

## 30. Explicit Exclusions

Engineering[157] does not:

- modify STATE.md;
- modify the published Protocol Specification;
- modify the Publication Record;
- modify any earlier review or correction record;
- change a normative row or stable identifier;
- create SF-17 or RF-51;
- reopen the formal ontology;
- create a new protocol generation;
- create a new specification identity or version;
- republish the specification;
- create a new Protocol Publication occurrence;
- introduce a first-class profile-publication subject;
- create the actual Implementation Profile;
- define petition semantics;
- prescribe current repository structure;
- assess the current codebase;
- establish compatibility;
- establish conformance;
- issue certification;
- or create implementation work.

This scope-determination record must not be added to the published Protocol
Specification’s normative source table.

Its expected normative citation count is zero.

## 31. Conclusion

Privacy Engine Protocol Specification V1 is published and remains unchanged.

The first bounded Implementation Profile target is the Generic Complete Privacy
Engine Protocol Implementation Target.

The target is application-independent, implementation-neutral, complete
relative to the protocol-owned capability chain, and suitable as one coherent
future conformance target.

Speak-up remains the first reference use case without becoming protocol
semantics.

All 729 normative requirements can be classified through one explicit,
specification-derived disposition process.

One first profile is sufficient.

The next step is composition of Privacy Engine Complete Implementation Profile
V1.

This document creates only the scope determination and composition plan.

Determination: **first Implementation Profile scope determined**.

Protocol authority always remains with the published Privacy Engine protocol generation.
