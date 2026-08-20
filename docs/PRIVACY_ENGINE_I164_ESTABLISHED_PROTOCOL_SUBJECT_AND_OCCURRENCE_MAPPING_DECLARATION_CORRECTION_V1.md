# Privacy Engine I164 Established Protocol Subject and Occurrence Mapping Declaration Correction V1

Correction date: 2026-08-20.

STATE.md remains the single canonical development authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

## 1. Record Identity and Status

| Field | Recorded value |
|---|---|
| Correction-record identifier | `PE-I164-ESTABLISHED-PROTOCOL-SUBJECT-AND-OCCURRENCE-MAPPING-DECLARATION-CORRECTION-V1` |
| Correction-record version | `1` |
| Correction package format | `PE-I164-ESTABLISHED-PROTOCOL-SUBJECT-AND-OCCURRENCE-MAPPING-DECLARATION-CORRECTION/1` |
| Correction date | `2026-08-20` |
| Engineering slice | Engineering[177] |
| Implementation-governance authority | Speak-up-appV3 implementation-governance boundary |
| Protocol authority | Published Privacy Engine protocol generation |
| Development authority | `STATE.md` |
| Fixed implementation baseline | I164 |
| Status | correction completed; awaiting independent re-review |
| Private Actor identity encoded | no |
| Requirement assessment performed | no |
| Requirement result produced | no |
| Reference Implementation designation | no |

Engineering[177] is a mechanically bounded correction occurrence only.

It is not an acceptance review, evidence-path reclassification, requirement assessment, security assessment, implementation change, protocol-generation occurrence, publication occurrence, or requirement result.

## 2. Authority Boundary

The preserved authority chain is:

> Privacy Engine protocol  
> `->` implementation-independent authority  
> `->` I164 as one bounded implementation  
> `->` Speak Up as one application adapter and use case

The Privacy Engine remains the primary implementation-independent privacy participation protocol.

I164 does not define, own, narrow, replace or become the Privacy Engine protocol.

## 3. Verified Handover Package

| Item | Verified value |
|---|---|
| Formal-corpus compressed data | no errors |
| Formal-corpus distinct files | 96 |
| Formal-corpus SHA-256 | `8580ad88b75495cd906dd34ccfc52089d50b17cfe7de31aefd726d6580a2a61c` |
| I164 archive SHA-256 | `7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847` |
| Git-provenance SHA-256 | `ebbe69467e4a06033a7aaac0a56f149dc00913ab4c96b504fa203d2a04bc0426` |
| Git-provenance format | `PRIVACY-ENGINE-HANDOVER-GIT-PROVENANCE/1` |

The provenance record remains untracked handover metadata only. It is not protocol authority, mapping authority, correction authority, acceptance authority, requirement evidence or a requirement result.

## 4. Fixed Basis

| Property | Verified value |
|---|---|
| I164 tag | `engineering-164` |
| I164 commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| I164 tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |
| Tracked paths | 308 |
| Blobs | 305 |
| Gitlinks | 3 |
| Reviewed-current successor basis | corrected Engineering[171] |
| Reviewed historical predecessor | Engineering[167] |
| Successor totals | 216 bounded / 269 still-ambiguous / 0 missing-evidence-path / 244 not-required |

Engineering[174] remains the single accepted final review result establishing the corrected Engineering[171] basis.

No requirement-level assessment or requirement result exists.

## 5. Immutable Engineering[175]

| Property | Verified value |
|---|---|
| Declaration path | `docs/PRIVACY_ENGINE_I164_ESTABLISHED_PROTOCOL_SUBJECT_AND_OCCURRENCE_MAPPING_DECLARATION_V1.md` |
| Declaration identifier | `PE-I164-ESTABLISHED-SUBJECT-OCCURRENCE-MAPPING-DECLARATION-V1` |
| Declaration version | `1` |
| Package-format version | `PE-I164-IMPLEMENTATION-OWNER-MAPPING/1` |
| Status | draft |
| Acceptance occurrence | none |
| Scope | Engineering[167] ambiguity group A01 only |
| SHA-256 | `1eb8ed90926975001e1976ad4e05edbb3e81f70aa703754e053cf1f768449085` |
| Git blob | `ab1d62e2550490693da377cb0bcb47b1160157ea` |
| Tag | `engineering-175` |
| Commit | `f747b875c96af441e68c4bdc73a4f4f6c6642ce0` |
| Tree | `c7f0e24481c28431377bbaa114559f85899142d9` |
| Ordered A01 serialization SHA-256 | `7050a2bc3c716cd1a3b09cecbfcc2e2f2e6e39cad6b571e0176d3f8f75368274` |

The immutable Engineering[175] artifact remains preserved through its tag, commit, tree, blob and SHA-256. Engineering[177] does not rewrite or move `engineering-175`.

## 6. Engineering[176] Rejection

| Property | Verified value |
|---|---|
| Review path | `docs/PRIVACY_ENGINE_I164_ESTABLISHED_PROTOCOL_SUBJECT_AND_OCCURRENCE_MAPPING_DECLARATION_ACCEPTANCE_REVIEW_V1.md` |
| SHA-256 | `fc0a4fef49c3a8db3b8affd79eebea051d30a9ee2c77291af8d0c157da4e8a6c` |
| Git blob | `f4cea205b569388e694702a7431577596b28520c` |
| Commit | `62b7f600129ddd0f55fd695362a7ff991833d5aa` |
| Tree | `893961a1c872768267a8f331cb4a0a6473c0ac96` |
| Rejection-outcome integrity identifier | `d8c7da24cd3d7223d0a98ac08e93f4f607ae300c1c5fac5ed1c4d4ab1a0175ee` |
| Material defects | 1 |
| Affected component records | 2 |
| Partial acceptance | none |
| Accepted relationship records | 0 of 14 |

Engineering[176] remains the historical rejection outcome.

## 7. Exact Defect

The affected component records are:

1. `O-DISPATCH`;
2. `O-RECONCILE`.

Both concern:

`backend/src/services/relayExecution.js`

Incorrect declaration value:

`1027ce8b4aef36c0e6d33f9ca2383b574c980ddd`

Verified I164 Git object:

`1027ce8b4aef36c0e6d33f9ca238cb574c980ddd`

The values differ only at character 29:

`3 / U+0033 / 0x33 -> c / U+0063 / 0x63`

This was a declaration-evidence transcription defect only. It was not a protocol, implementation, source-file, Profile V2, privacy, runtime, deployment or SHA-256 defect, and it was not a requirement result.

## 8. Byte-Level Correction

| Property | Verified value |
|---|---:|
| Pre-correction byte length | 55505 |
| Corrected byte length | length | 55505 |
| Byte-length delta | 0 |
| LF before and after | 870 |
| CRLF before and after | 0 |
| Differing byte positions | 2 |
| Inserted bytes | 0 |
| Deleted bytes | 0 |
| Reordered bytes | 0 |
| Other changed bytes | 0 |
| Corrected declaration SHA-256 | `aebc191a9b723c3397dc41c7471fdac48a0e11ae9969511d79205334cc40eeef` |
| Corrected content-derived Git blob | `ca1b37b6e7be67e23e7447b1d46ec52de0cc9275` |

Offsets are zero-based offsets into the complete declaration byte sequence.

| Component | Zero-based offset | One-based position | Before | After |
|---|---:|---:|---|---|
| `O-DISPATCH` | 18373 | 18374 | `0x33` | `0x63` |
| `O-RECONCILE` | 18663 | 18664 | `0x33` | `0x63` |

Every byte outside those two offsets remains byte-exact and in its original order.

## 9. Component and Declaration Preservation

All 18 component-register rows were verified.

The corrected rows now use:

`1027ce8b4aef36c0e6d33f9ca238cb574c980ddd`

Their unchanged SHA-256 remains:

`10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff`

The declaration otherwise preserves exactly:

- its identifier, version, package format and draft status;
- absent acceptance occurrence;
- A01-only scope;
- 18 component-register rows;
- 16 representation rows;
- 14 proposed and unaccepted relationship records;
- every relationship treatment and limitation;
- every explicit non-mapping and unresolved dependency;
- every privacy and occurrence boundary;
- the complete formal-subject inventory;
- `T-I164-ANONYMOUS-PUBLIC-ACTION`;
- ordered public values `[nullifier, petitionId/actionId, membershipRoot]`;
- the complete ten-row A01 ledger;
- eight supported-component-plus-unresolved treatments;
- two explicit proposed non-mappings;
- zero evidence-path reclassifications;
- and zero requirement results.

## 10. Preserved Boundaries

`T-I164-ANONYMOUS-PUBLIC-ACTION` remains neither a protocol subject nor Private Actor, Protocol Operation or Protocol Action occurrence identity.

The ordered public values remain public protocol-facing roles only. They do not become reusable participant, wallet, sponsor, funding, admission, transport, ownership, application or formal occurrence identity.

The following separations remain preserved:

> candidate construction `!=` Protocol Action occurrence  
> UI request `!=` Protocol Action occurrence  
> relay request `!=` Protocol Action occurrence  
> transport attempt `!=` Protocol Action occurrence  
> transaction `!=` Protocol Action occurrence  
> event `!=` Protocol Action occurrence  
> database row `!=` Protocol Action occurrence  
> proof verification `!=` complete Protocol Action Evaluation  
> response or downstream record `!=` Protocol Action Determination  
> execution attempt `!=` Protocol State Transition occurrence  
> application object `!=` protocol subject

## 11. Unresolved State

All inherited unresolved relationships remain unresolved:

- `U-ACTION-IDENTITY`;
- `U-ACTION-ADMISSION`;
- `U-RETRY`;
- `U-RULESET`;
- `U-ROOT`;
- `U-EVAL-IDENTITY`;
- `U-EVAL-BOUNDARY`;
- `U-EVAL-REJECTION`;
- `U-DETERMINATION`;
- `U-CLASSIFICATION`;
- `U-PRIVACY-REVIEW`;
- `U-PROVENANCE`.

Dependencies outside A01 remain unresolved, including A02, A03, A04, A05, A06, A07, A08, A10, A11, A15, A17 and A20.

All ten A01 rows remain still-ambiguous.

## 12. Privacy Review

The governing principle remains:

> Private actors, public actions.

The corrected characters encode no actor, action occurrence, wallet, sponsor, funding source, admission source, transport route, ownership claim, topology or correlation relationship.

No identity, provenance, cross-action correlation, metadata bridge, topology-to-actor mapping or actor-reconstruction path was introduced.

Complete baseline-wide privacy evidence remains unresolved under `U-PRIVACY-REVIEW`.

## 13. Lifecycle

The corrected declaration remains draft and unaccepted.

All 14 relationship records remain proposed and unaccepted.

Engineering[177] creates no acceptance occurrence, partial acceptance, evidence-path reclassification, requirement assessment, requirement result, implementation-defect determination, security determination, compatibility result, conformance result, certification result, operational-readiness result, Reference Implementation designation, Profile V3, protocol generation or publication occurrence.

A later independent re-review is required before acceptance.

## 14. Correction Determination

> Exactly the Engineering[176]-identified defect was corrected through exactly two `0x33 -> 0x63` byte replacements; no other byte changed; `O-DISPATCH` and `O-RECONCILE` now match the exact I164 Git object; every other component row remains unchanged and correct; immutable Engineering[175] remains preserved; Engineering[176] remains the historical rejection outcome; the corrected declaration remains draft and unaccepted; all 14 relationship records remain proposed and unaccepted; all ten A01 rows remain still-ambiguous; no evidence-path reclassification was performed; successor totals remain 216 / 269 / 0 / 244; no requirement-level assessment was performed; no requirement result was produced; and a later independent re-review is required before acceptance.
