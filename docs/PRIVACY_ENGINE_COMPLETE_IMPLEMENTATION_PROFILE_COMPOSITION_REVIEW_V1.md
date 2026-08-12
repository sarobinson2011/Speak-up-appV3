# Privacy Engine Complete Implementation Profile Composition Review V1

Review date: 2026-08-12.

STATE.md remains the single canonical development authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

## 1. Review Status

Engineering[159] completed an independent composition review of Privacy Engine
Complete Implementation Profile V1.

Review status: **completed — rejected pending identified correction**.

The review found one blocking disposition defect and no non-blocking finding.

The reviewed profile remains unchanged.

## 2. Purpose

This document records whether Privacy Engine Complete Implementation Profile V1
correctly classifies all 729 published normative requirements for the Generic
Complete Privacy Engine Protocol Implementation Target.

It records independent review evidence and one final determination.

It does not repair or amend the reviewed profile.

## 3. Scope

The review covers:

- profile identity, source, target, and authority;
- all 729 Requirement Disposition Ledger entries;
- published metadata and identifier order;
- every applicable, non-applicable, conditional, and permitted-choice disposition;
- included and excluded capability boundaries;
- privacy, neutral naming, and application separation;
- implementation freedom;
- dependencies;
- and downstream authority preservation.

It does not inspect or assess the current codebase.

## 4. Authority and Dependency Position

The governing direction remains:

> Published Protocol Generation
> -> Published Protocol Specification
> -> Implementation Profile
> -> Implementation
> -> Conformance
> -> Certification

The review is informative and derivative.

It is not authoritative over the profile, Protocol Specification, or published
protocol generation.

No downstream artifact acquires authority over an upstream artifact.

## 5. Reviewed Artifacts

The review inspected:

- STATE.md;
- Privacy Engine Protocol Specification V1;
- Privacy Engine Protocol Specification Publication Record V1;
- Privacy Engine Implementation Profile Scope Determination V1;
- Privacy Engine Complete Implementation Profile V1;
- the Protocol Specification Composition Map;
- all specification review and correction records;
- the Implementation Profile, Implementation, Protocol Realization, and
  Reference Implementation models;
- the application, adapter, runtime, integration, compatibility, conformance,
  and certification models;
- and the complete S01-S68 formal source corpus.

The current implementation was not inspected.

## 6. Guarded Baselines

| Guarded artifact | Verified SHA-256 | Result |
|---|---|---|
| Complete Implementation Profile | `68e69c3693f34ad34faa64eb712f65f520e89d64dc3f1d1a847854c3fda57c7a` | Pass |
| Published Protocol Specification | `f2c12b60f24fe8fe8eddf27dc2d59814aceba42b907160c54ad3868bde7da393` | Pass |
| Publication Record | `d655359c296d6d6aefffd3e6faa0fd47f6506ec9d64a871ade9f9eb469108029` | Pass |
| Implementation Profile Scope Determination | `03fe5d180a4056c6e66356c1804f8883006daab52a80ec12676483ad75fd0a17` | Pass |
| Engineering[155] final consolidation re-review | `7bf415870a2e630157d1cf186e45764513e87b5f13b2ac790373d4de5df13bb7` | Pass |

Every guarded artifact matched before review.

The Publication Record determines the source specification `published`.

The Scope Determination determines `first Implementation Profile scope determined`.

## 7. Review Method

The review:

1. guarded every required artifact;
2. reconstructed the normative-row, undeclared-row, identifier, and section digests;
3. compared all specification and ledger metadata;
4. resolved every S01-S68 source;
5. verified structure, order, family completeness, and disposition totals;
6. reviewed every ledger row using its complete requirement, applicability,
   authoritative home, source context, target relationship, justification,
   condition, choice, dependency effect, and preservation result;
7. reviewed mixed-boundary and exception rows independently of family-level
   classification;
8. applied rejection rather than silent repair when one disposition failed;
9. and performed no current-codebase assessment.

Automation validated metadata and integrity.

It did not substitute for semantic disposition review.

## 8. Published Specification Integrity

The published Protocol Specification remains unchanged.

The review independently verified:

- 729 normative rows;
- 729 unique stable identifiers;
- fifty complete semantic-identifier families;
- exact RF-01 through RF-50 coverage;
- the intentional historical PE-SURF ordering;
- exact Section 8 and Composition Map agreement;
- all S01-S68 definitions, uses, and file resolution;
- RF-42, RF-49, RF-50, and PE-EXCLUDE-026;
- and zero profile citations in the published specification.

Verified digests:

| Preserved material | SHA-256 |
|---|---|
| All 729 normative rows | `b758510ded0d650c5e7728967420a6cf9ff85bab53e829ecb4cf102d768530b5` |
| Undeclared 715 rows | `a168364c6696efe00b816fb3e333362d5125edbf48a4a6e5dfbd0aaf0c8be431` |
| Ordered identifier sequence | `9c331b1bbf8a3639bdb11d6e4caf12eaab7cee26fae040ba2990746b6cfad404` |
| Section 3 | `1f8aa38da6a398431a1a1eb5adfd073c466c7bef993d86e490f3d552f293ecc1` |
| Section 8 | `b893860e99405ab0f08421c63d57c7d91e6c3fab09d2d664e115675f366bb61a` |
| Section 38 | `3ecc7e24673006f88f481e2020a72e66ccf0cc8ed454d8d2dde29db28766accb` |

No specification question is reopened.

## 9. Profile Identity and Target

Reviewed profile identity:

> Privacy Engine Complete Implementation Profile V1

Reviewed profile version:

> V1

Reviewed target:

> Generic Complete Privacy Engine Protocol Implementation Target

Reviewed profile SHA-256:

`68e69c3693f34ad34faa64eb712f65f520e89d64dc3f1d1a847854c3fda57c7a`

The target remains generic, complete, application-independent,
implementation-neutral, portable, independently implementable, and independently
assessable.

The profile remains distinct from the specification, implementation,
application, Reference Implementation, conformance, and certification.

Result: **Pass**.

## 10. Ledger Structural Integrity

The Requirement Disposition Ledger contains:

- 729 entries;
- 729 unique identifiers;
- zero missing identifiers;
- zero extra identifiers;
- zero duplicate identifiers;
- exact published identifier order;
- exactly one syntactically valid disposition per entry;
- and no empty ledger field.

The profile records:

- 477 applicable dispositions;
- 0 conditionally applicable dispositions;
- 245 non-applicable dispositions;
- 7 dispositions resolved through permitted specification choice.

These totals accurately describe the reviewed artifact.

They do not all survive semantic review.

Result: **Structural pass; semantic determination deferred to later sections**.

## 11. Published Metadata Preservation

For all 729 ledger entries, the review verified exact preservation of:

- stable identifier;
- RF family;
- authoritative SF home;
- normative strength;
- and published applicability.

Every Section 8 prefix/RF/SF mapping agrees with the Composition Map and ledger.

No normative requirement statement is copied or rewritten in the profile.

Result: **Pass**.

## 12. Row-Level Semantic Review

All 729 ledger entries received independent semantic review.

For each row, the review considered:

- the complete published requirement;
- exact applicability;
- authoritative section;
- definitions and cross-references;
- source context;
- selected target;
- profile justification;
- condition record;
- choice record;
- dependency effect;
- and preservation result.

The review did not treat RF family, SF home, keywords, strength, or generated
totals as sufficient evidence.

Result:

- 728 dispositions sustained;
- 1 disposition rejected;
- 1 blocking finding;
- 0 non-blocking findings.

## 13. Applicable-Disposition Review

All 477 recorded applicable dispositions were reviewed.

Each correctly governs:

- the profile;
- the selected implementation target;
- an included protocol capability;
- a necessarily produced surface;
- or an applicable privacy, authority, preservation, or exclusion boundary.

Every applicable row retains its exact published applicability.

No applicable obligation was found weakened, strengthened, rewritten, or
replaced.

Result: **All 477 recorded applicable dispositions sustained**.

This result does not cure the omitted applicable classification identified in
Section 29.

## 14. Conditional-Disposition Review

The ledger contains zero profile-level conditional dispositions.

The zero total is correct because:

- the selected target is complete;
- every protocol-owned operational branch is included;
- runtime, occurrence, lifecycle, and capability conditions remain preserved
  inside exact published applicability;
- no additional target-level condition is required;
- no conditional obligation is flattened into unconditional protocol behavior;
- and no unresolved condition is concealed.

Result: **Zero conditional dispositions sustained**.

## 15. Non-Applicable-Disposition Review

All 245 recorded non-applicable dispositions were reviewed.

Requirements whose published subjects concern specification construction,
protocol-generation governance, publication, succession, lineage, migration,
application-owned behavior, Reference Implementation designation,
compatibility, conformance, or certification are generally outside the selected
target.

One entry does not satisfy that rule:

> PE-REFIMPL-017

Its published subject is not a Reference Implementation designation.

Its published applicability is:

> Every ordinary implementation

Its obligation directly governs ordinary implementations realizing the selected
profile.

Therefore:

- 244 non-applicable dispositions are sustained;
- 1 non-applicable disposition is rejected.

Result: **Fail**.

## 16. Permitted-Choice Review

The seven permitted-choice dispositions are:

- PE-EVOL-018;
- PE-IFACE-009;
- PE-RUNTIME-005;
- PE-IMPL-005;
- PE-IMPL-011;
- PE-IMPL-013;
- PE-REALIZE-009.

Each source requirement expressly uses `MAY`.

Each profile resolution remains within the published choice space.

No resolution:

- makes mandatory behavior optional;
- permits prohibited behavior;
- introduces an implicit default;
- prescribes application machinery;
- prescribes implementation machinery as protocol law;
- or creates an external profile dependency.

Result: **Pass**.

## 17. Required Exception Review

The required exception rows were independently reviewed.

| Identifier | Reviewed disposition | Result |
|---|---|---|
| PE-GEN-017 | applicable | Pass |
| PE-GEN-020 | applicable | Pass |
| PE-PROFILE-013 | non-applicable | Pass |
| PE-PROFILE-019 | non-applicable | Pass |

PE-GEN-017 governs every Privacy Engine implementation.

PE-GEN-020 preserves generation identity and authority across downstream
implementation and assessment artifacts.

PE-PROFILE-013 is not activated because this complete target has no separate
Implementation Profile dependency.

PE-PROFILE-019 is not activated because the source specification is complete,
accepted, and published.

Result: **Pass**.

## 18. Dependency Review

The selected target has:

- zero unresolved dependencies;
- zero external Implementation Profile dependencies;
- and no hidden profile dependency.

Included capability dependencies remain internal to the one complete profile.

The PE-REFIMPL-017 defect is an applicability misclassification.

It does not create an external Reference Implementation dependency.

Result: **Pass**.

## 19. Included Capability Review

The profile coherently includes:

- anonymous membership and private-secret continuity;
- enrollment separation;
- proofs, public inputs, verification, evidence, and complete validity;
- nullifier uniqueness and action-bounded unlinkability;
- Protocol Operations and Protocol Actions;
- applicable rules, Evaluation, Determination, acceptance, and rejection;
- accepted no-transition behavior;
- transition mapping, authorization, execution, commitment, and atomicity;
- protocol state, history, consequence, failure, and re-evaluation;
- interfaces, surfaces, operations, and Published Results;
- runtime enforcement and reporting;
- implementation and realization obligations;
- and applicable privacy, preservation, authority, and exclusion boundaries.

Result: **Pass**.

## 20. Excluded-Material Review

The profile coherently excludes:

- application-owned petition meaning and lifecycle;
- application policy, metadata, UI, moderation, and outcome interpretation;
- protocol-generation governance and publication occurrences;
- succession, lineage, migration, coexistence, and retirement;
- Reference Implementation designation;
- compatibility structures and assessments;
- conformance artifacts, evidence, claims, assessments, and determinations;
- certification bases, decisions, statuses, recognition, and authority;
- and current implementation machinery not constrained by the specification.

Excluding Reference Implementation designation does not permit exclusion of a
requirement whose published subject is every ordinary implementation.

Result: **Pass except for PE-REFIMPL-017 as recorded in Section 29**.

## 21. Privacy and Unlinkability Review

The profile preserves:

> Private actors, public actions.

Applicable requirements continue to preserve:

- anonymity;
- action-bounded unlinkability;
- minimum disclosure;
- proof/public-input boundaries;
- enrollment and admission separation;
- wallet and application separation;
- metadata-composition constraints;
- and the prohibition against actor-reconstruction bridges.

No profile record introduces Private Actor identity, reusable participant
identity, cross-action identity continuity, or prohibited provenance.

Result: **Pass**.

## 22. Neutral-Naming Review

The profile, ledger, dispositions, justifications, conditions, choices,
dependencies, findings, and boundaries use neutral non-actor terminology.

No ledger entry introduces correlation-bearing names or turns operational,
transport, deployment, application, wallet, funding, sponsor, or ownership
metadata into actor identity.

Neutral naming remains part of the privacy boundary.

Result: **Pass**.

## 23. Application and Speak-up Boundary

Speak-up remains a reference use case.

It does not define the profile.

The profile does not promote petition identity, meaning, lifecycle, metadata,
moderation, eligibility, policy, UI, or interpretation into protocol or profile
semantics.

The protocol-facing application boundary remains preserved through applicable
interface, authority, privacy, and semantic-preservation requirements.

Result: **Pass**.

## 24. Runtime and Implementation Variation

The profile preserves implementation freedom for:

- internal decomposition;
- algorithms not constrained by the specification;
- languages and processes;
- storage and transport;
- deployment topology;
- responsibility allocation;
- concrete interface representation;
- and multiple implementations or realizations.

The published obligations remain controlling wherever variation is exercised.

PE-REFIMPL-017 is itself an implementation-freedom obligation: an ordinary
implementation must not be required to copy incidental Reference Implementation
structure or behavior.

Its non-applicable classification therefore conflicts with this preserved
boundary.

Result: **Fail through PE-REFIMPL-017**.

## 25. M2, TEMPEST, and REFLECT Boundary

M2, TEMPEST, and REFLECT remain implementation structures only.

The profile does not:

- use their names as profile identity;
- require their present decomposition;
- require their repository layout;
- turn their operational machinery into protocol law;
- or constrain future implementations to reproduce them.

Result: **Pass**.

## 26. Compatibility, Conformance, and Certification Boundary

The profile creates a future implementation target.

It does not establish:

- compatibility;
- conformance;
- certification;
- a conformance basis or determination;
- a certification basis, decision, status, recognition, or authority;
- security;
- operational readiness;
- or Reference Implementation status.

Result: **Pass**.

## 27. Current-Codebase Assessment Boundary

No profile disposition or review result derives from current Speak-up codebase
behavior.

Engineering[159] did not:

- inspect implementation satisfaction;
- identify implementation defects;
- repair profile applicability to fit the codebase;
- establish compatibility or conformance;
- assess security or operational readiness;
- issue certification;
- or create implementation work.

The current implementation remains unassessed.

Result: **Pass**.

## 28. Protocol Authority

The profile and this review remain derivative.

Neither artifact defines, amends, replaces, weakens, strengthens, supersedes, or
becomes the published protocol generation or Protocol Specification.

This review is not added to Section 38 of the published specification.

Its expected citation count in the published specification is zero.

Protocol authority always remains with the published Privacy Engine protocol generation.

Result: **Pass**.

## 29. Findings

### F-01 — PE-REFIMPL-017 applicability misclassification

Finding classification: **blocking**.

Published identifier:

> PE-REFIMPL-017

Published RF and SF home:

> RF-43 / SF-14

Published strength:

> MUST NOT

Published applicability:

> Every ordinary implementation

Published requirement:

> An ordinary implementation MUST NOT be required to copy reference source
> structure, language, algorithms, storage, deployment topology, APIs, logging,
> timing, or other behavior not required by the applicable profile.

Profile disposition:

> non-applicable

Profile justification:

> The row is treated as confined to Reference Implementation designation or
> comparison.

Review result:

> rejected

The published subject is every ordinary implementation, not every Reference
Implementation or reference designation.

The Generic Complete Privacy Engine Protocol Implementation Target denotes the
ordinary implementation class that realizes the profile.

The requirement protects implementation freedom by preventing incidental
Reference Implementation structure or behavior from becoming an implementation
obligation.

Reference Implementation designation remains excluded.

The ordinary-implementation obligation remains applicable.

Required correction:

> Change only PE-REFIMPL-017 from `non-applicable` to `applicable` and replace
> its justification, condition, dependency effect, and preservation result with
> records appropriate to an applicable ordinary-implementation obligation.

Expected corrected disposition totals:

- applicable: 478;
- conditionally applicable: 0;
- non-applicable: 244;
- resolved through permitted specification choice: 7;
- total: 729.

Engineering[159] does not perform that correction.

No additional blocking finding exists.

No non-blocking finding exists.

## 30. Review Determination

The Engineering[159] determination is:

> Privacy Engine Complete Implementation Profile V1 composition rejected pending identified correction

The profile cannot pass while PE-REFIMPL-017 remains non-applicable.

No partial pass or conditional pass is issued.

The profile remains unchanged pending a separately bounded correction.

## 31. Future Position

The next bounded work should correct only PE-REFIMPL-017 and the mechanically
dependent profile totals and findings.

That correction must:

- preserve the profile identity and selected target;
- preserve every other ledger entry byte-for-byte;
- preserve the published specification unchanged;
- preserve all profile boundaries;
- record the corrected `478 / 0 / 244 / 7` totals;
- and produce a separately identified correction record.

A later independent re-review must confirm the correction before implementation
assessment begins.

Compatibility, conformance, certification, security, operational-readiness, and
codebase assessment remain future work.

## 32. Explicit Exclusions

Engineering[159] does not:

- modify STATE.md;
- modify the published Protocol Specification;
- modify the Publication Record;
- modify the Scope Determination;
- modify the Complete Implementation Profile;
- modify an earlier review or correction record;
- change a normative row or identifier;
- change a profile ledger entry;
- silently repair PE-REFIMPL-017;
- create SF-17 or RF-51;
- reopen the ontology;
- create a new protocol generation or specification version;
- republish the specification;
- introduce a profile-publication subject;
- mandate M2, TEMPEST, or REFLECT;
- promote application semantics into profile semantics;
- inspect or assess the codebase;
- establish compatibility or conformance;
- issue certification;
- designate a Reference Implementation;
- assess security or operational readiness;
- or perform implementation work.

## 33. Conclusion

Privacy Engine Complete Implementation Profile V1 preserves the published
specification’s integrity, metadata, authority, privacy boundaries, target
identity, and 728 of its 729 row-level dispositions.

PE-REFIMPL-017 is incorrectly classified as non-applicable even though its
published applicability governs every ordinary implementation and therefore the
selected implementation target.

Determination: **Privacy Engine Complete Implementation Profile V1 composition rejected pending identified correction**.

Blocking findings: **1**.

Non-blocking findings: **0**.

Protocol authority always remains with the published Privacy Engine protocol generation.
