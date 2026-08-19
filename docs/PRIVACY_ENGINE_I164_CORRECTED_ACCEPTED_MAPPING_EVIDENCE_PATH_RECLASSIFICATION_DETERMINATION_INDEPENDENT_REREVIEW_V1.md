# Privacy Engine I164 Corrected Accepted Mapping Evidence-Path Reclassification Determination Independent Re-review V1

Review date: 2026-08-19.

STATE.md remains the single canonical development authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

## 1. Purpose and Status

This record independently re-reviews the exact Engineering[173] correction of:

`docs/PRIVACY_ENGINE_I164_ACCEPTED_MAPPING_EVIDENCE_PATH_RECLASSIFICATION_DETERMINATION_V1.md`

It answers one architectural question:

> Did Engineering[173] correct exactly the 11 Engineering[172]-identified transcription defects, without any other byte, semantic, mapping, classification, evidence-path, protocol, implementation, privacy, or assessment change, such that the corrected Engineering[171] determination may become the reviewed-current successor evidence-path basis?

This is an independent re-review only.

It does not:

- modify the Privacy Engine protocol;
- modify the published Protocol Specification V1;
- modify Complete Implementation Profile V2;
- modify the fixed I164 implementation baseline;
- create or change an accepted mapping;
- reclassify another requirement;
- resolve an unresolved relationship;
- resolve a permitted-choice row;
- perform requirement-level assessment;
- assign a requirement result;
- determine an implementation defect;
- perform a security assessment;
- establish conformance, compatibility, certification, or operational readiness;
- designate a Reference Implementation;
- or make Speak-up-appV3 the Privacy Engine.

## 2. Authority and System Boundary

The preserved authority chain is:

> Privacy Engine protocol  
> `->` implementation-independent authority  
> `->` I164 as one bounded implementation baseline  
> `->` Speak Up as one application adapter and use case

The following remain distinct:

> Privacy Engine protocol authority  
> `!=` I164 implementation governance  
> `!=` Speak Up application meaning

I164 identifies the fixed Speak-up-appV3 implementation baseline under examination.

I164 does not define, own, narrow, replace, or become the Privacy Engine protocol.

## 3. Supplied-Package Verification

| Supplied item | Required identity | Independently verified |
|---|---|---|
| Formal corpus compressed data | No ZIP errors | yes |
| Formal corpus file count | 93 distinct files | yes |
| Formal-corpus SHA-256 | `a73cd448b3e73e92fe83bfdb7011922ac2cfb3212ad3eebab161e15b5e31ea32` | yes |
| I164 implementation archive SHA-256 | `7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847` | yes |
| Git-provenance SHA-256 | `2f88306c58add2039cd2268f4fe228c813833d4500b05c948101d3222d9b10ab` | yes |
| Git-provenance format | `PRIVACY-ENGINE-HANDOVER-GIT-PROVENANCE/1` | yes |

The Git-provenance record was treated as untracked handover metadata only.

It is not:

- part of the formal corpus;
- protocol documentation;
- an implementation artifact;
- protocol authority;
- requirement evidence;
- or a requirement result.

## 4. Guarded Formal Artifacts

| Artifact | Independently verified SHA-256 |
|---|---|
| `STATE.md` | `228886af0db33a801db40d834c1a1070ed8f330d6708d8e6674021e3a2d3be33` |
| Published Protocol Specification V1 | `f2c12b60f24fe8fe8eddf27dc2d59814aceba42b907160c54ad3868bde7da393` |
| Publication Record | `d655359c296d6d6aefffd3e6faa0fd47f6506ec9d64a871ade9f9eb469108029` |
| Final Protocol Specification consolidation re-review | `7bf415870a2e630157d1cf186e45764513e87b5f13b2ac790373d4de5df13bb7` |
| Complete Implementation Profile V2 | `279fc80cb2998df8c4fddcc2ea25e4091897571c57a7d5905100857612b2d79c` |
| Profile V2 composition re-review | `093f3d2178bc890e7bed9dc56aea164f36918a01e49caef2ed8d777777dd0d11` |
| Profile identity/version correction | `c37a3fa1985a11243ff0b1103d5d7ca911f77e76a14f00f4c12a368e4f7ad88a` |
| Profile V2 status synchronization | `d8bce61c2366e4a5ca6d6d87ef4875944956acd1b8303e73f2f901c7a1ba1e27` |
| Profile V2 assessment-basis record | `a3547f19e187cb9b0c5493c75832a9bebd95c2462387cdc120907fc413ce89af` |
| Engineering[166] | `46294d6e4dc2928409713bad32e510ee2c1749d39fdc0ed27ae70b1219f88175` |
| Engineering[167] | `bdea6dc1f2b9af176de9e354daf654a3c4a8b1eb4bd46c16d1ff0ea3fbfc5cd2` |
| Engineering[168] | `1280eb90b97f9caa21456f8ce8ce58f6211b5ef360d8d2637110a43c4f00e7f2` |
| Engineering[169] | `a6e488f8a246dcf14c2a3a3e0df8226833ccec8720d12c6798a971a0d3ee6890` |
| Engineering[170] | `7f435cf93d835ee3106e995c355a4d2019f2de81eaed5df2a5e9448b4bac20db` |
| Immutable pre-correction Engineering[171] | `e7c31445ad77c2b6f592e88b846202286f003b039a717939b7f6d198d6672d46` |
| Engineering[172] | `cc4e5b82a2fba611fa68032ff6eef25c45c18c9ed3d7fbc963766513fbca5b8d` |
| Corrected Engineering[171] | `f40638d8468749afe5d260fdf01e456fc27d3afd9febf75bfe2d59e2fa6d36ff` |
| Engineering[173] correction record | `df1346947f347bb1c89569bafeb64fcee467680f88de5b4e318d9f0c7f97c1d9` |

No guarded artifact was modified by this re-review.

## 5. Git-Provenance Verification

For each of `engineering-164`, `engineering-169`, `engineering-170`, `engineering-171`, `engineering-172`, and `engineering-173`, the following were independently verified:

- tag-object type is `commit`;
- local lightweight-tag ref;
- remote lightweight-tag ref;
- resolved commit;
- resolved tree;
- parent commit;
- equality of local ref, remote ref, and resolved commit;
- exact raw commit payload;
- Git commit identity recomputed from the raw commit payload;
- every recorded changed-file Git blob identity;
- and every recorded changed-file SHA-256.

### 5.1 Engineering[164]

| Field | Verified value |
|---|---|
| Tag | `engineering-164` |
| Commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |
| Parent | `5e12cca624ffccf43637de4b9dc42de4af3979bc` |
| Archive comment | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Tracked paths | 308 distinct |
| Blob paths | 305 |
| Gitlink paths | 3 |
| Reconstructed root tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |

Every archived blob path, blob SHA-256, Git blob identity, path mode, and tree position matched the guarded inventory.

The three Gitlinks remain:

| Path | Gitlink identity |
|---|---|
| `contracts/lib/forge-std` | `52c1e835e9ffcfe00bd9f8f51de204b93bc7028a` |
| `contracts/lib/openzeppelin-contracts` | `8ff78ffb6e78463f070eab59487b4ba30481b53c` |
| `contracts/lib/openzeppelin-contracts-upgradeable` | `b933412726bccd822a871116f1427111e649ff54` |

The Engineering[164] changed-file identities were independently verified:

| Path | Git blob | SHA-256 |
|---|---|---|
| `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2.md` | `e9b69e8a075f4c5443b9ac66e289cf2737972208` | `279fc80cb2998df8c4fddcc2ea25e4091897571c57a7d5905100857612b2d79c` |
| `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2_STATUS_SYNCHRONIZATION_V1.md` | `27262837f959d4ea2744595527cc332ad63bbec3` | `d8bce61c2366e4a5ca6d6d87ef4875944956acd1b8303e73f2f901c7a1ba1e27` |

### 5.2 Engineering[169]

| Field | Verified value |
|---|---|
| Commit | `392863755dac71b5d762c26caf3830c987dbbfaf` |
| Tree | `91de8930ed29add9b0e7986566319946e0d63bfa` |
| Parent | `8a7a4d222e13e8128968798b28a597cf5aab7f45` |
| Tagged-file Git blob | `1ed88cd50c9d3fa7015441f294e78c31226c6140` |
| Tagged-file SHA-256 | `a6e488f8a246dcf14c2a3a3e0df8226833ccec8720d12c6798a971a0d3ee6890` |

The ordered 88-row Engineering[167] A04-A08 source serialization independently reproduced:

`91b2d8acca57a395b738b18001a3e47b9f4c15f382a4c0bb6124bf1ac46f494d`

### 5.3 Engineering[170]

| Field | Verified value |
|---|---|
| Commit | `c16aa4f7516917ffbbfae8cc939a8959106a2e46` |
| Tree | `40de12f4fbab9ac7fda3abf76bb4a19ef8959515` |
| Parent | `392863755dac71b5d762c26caf3830c987dbbfaf` |
| Tagged-file Git blob | `d08cbfcda8910e3c7ae811a60fdc70f6f74429a6` |
| Tagged-file SHA-256 | `7f435cf93d835ee3106e995c355a4d2019f2de81eaed5df2a5e9448b4bac20db` |

The canonical acceptance payload independently reproduced the acceptance-occurrence integrity identifier:

`3c2a25b20c119d399cf3e954c26fd465834c82b6835b430f5375552fb1a1be06`

The acceptance occurrence remains:

| Field | Preserved value |
|---|---|
| Identity | `PE-I164-AEDC-MAPPING-ACCEPTANCE-2026-08-18` |
| Status | `accepted` |
| Authority | implementation-governance boundary governing I164 |
| Private Actor identity encoded | no |
| Requirement assessment performed | no |
| Requirement result produced | no |
| Reference Implementation designation | no |

### 5.4 Engineering[171]

| Field | Verified value |
|---|---|
| Commit | `7fc018bc705c4bd990bf48ff3635acc196059ba1` |
| Tree | `933f11fa3556d2eff9a8ec7892c9d56fd4f05859` |
| Parent | `c16aa4f7516917ffbbfae8cc939a8959106a2e46` |
| Immutable tagged-file Git blob | `608f14b000f1b5faf7569562d674bb609bb79bf2` |
| Immutable tagged-file SHA-256 | `e7c31445ad77c2b6f592e88b846202286f003b039a717939b7f6d198d6672d46` |

The immutable `engineering-171` tag remains unchanged and continues to identify the pre-correction artifact.

### 5.5 Engineering[172]

| Field | Verified value |
|---|---|
| Commit | `7f2c7627ca8eba0dd07bd98e2a8843b84bd0b7ba` |
| Tree | `d3552aec3d34f31d437d9e18bc4ddc6aa636172b` |
| Parent | `7fc018bc705c4bd990bf48ff3635acc196059ba1` |
| Tagged-file Git blob | `73b659a4146e7a6caec585fbec88420063c4d45c` |
| Tagged-file SHA-256 | `cc4e5b82a2fba611fa68032ff6eef25c45c18c9ed3d7fbc963766513fbca5b8d` |

Engineering[172] contains one final outcome:

- `rejected pending identified correction`.

The rejection concerns only 11 missing final U+0060 characters in copied published-applicability fields.

Engineering[172] records no substantive mapping, transition, state-total, privacy, protocol, implementation, or assessment rejection.

### 5.6 Engineering[173]

| Field | Verified value |
|---|---|
| Commit | `8ba9dfe6adfaeefa1119112065745fb8629415e8` |
| Tree | `5d90214408df0340d7d01c58943cc389a3a4747c` |
| Parent | `7f2c7627ca8eba0dd07bd98e2a8843b84bd0b7ba` |

Exactly two changed files were recorded and independently verified:

| Path | Git blob | SHA-256 |
|---|---|---|
| Corrected Engineering[171] determination | `8776e630a7a730074c90e3173913e46146ec95f8` | `f40638d8468749afe5d260fdf01e456fc27d3afd9febf75bfe2d59e2fa6d36ff` |
| Engineering[173] correction record | `50c2f125de0d2f793a228dcd08162e243020c7ca` | `df1346947f347bb1c89569bafeb64fcee467680f88de5b4e318d9f0c7f97c1d9` |

Engineering[173] performed the bounded correction.

It did not perform or predetermine this independent re-review.

## 6. Immutable Pre-correction Defect Reproduction

The immutable Engineering[171] successor ledger was independently reconstructed and contains:

- exactly 729 rows;
- 729 unique identifiers;
- the exact Profile V2 order;
- 729 exact RF families;
- 729 exact SF homes;
- 729 exact strengths;
- 729 exact Profile V2 dispositions;
- 729 exact profile-row SHA-256 values;
- 718 byte-identical published-applicability fields;
- and exactly 11 non-identical published-applicability fields.

For every non-identical field:

> immutable Engineering[171] field  
> `=` exact Profile V2 field  
> `-` final U+0060 character

The exact affected set is:

1. `PE-NORM-002`;
2. `PE-NORM-003`;
3. `PE-NORM-004`;
4. `PE-NORM-005`;
5. `PE-NORM-006`;
6. `PE-TRANSEXEC-006`;
7. `PE-COMMIT-004`;
8. `PE-COMMIT-008`;
9. `PE-STATE-009`;
10. `PE-STALEAUTH-003`;
11. `PE-STALEAUTH-004`.

No other Profile V2 metadata defect was reproduced.

## 7. Independent Byte-Level Comparison

| Property | Independently verified value |
|---|---:|
| Immutable pre-correction length | 314482 bytes |
| Corrected length | 314493 bytes |
| Length delta | +11 bytes |
| Inserted bytes | 11 |
| Inserted byte value | U+0060 / UTF-8 `0x60` |
| Replaced bytes | 0 |
| Deleted bytes | 0 |
| Other changed bytes | 0 |
| LF characters before | 1096 |
| LF characters after | 1096 |
| CRLF sequences before | 0 |
| CRLF sequences after | 0 |

Every pre-correction byte remains in its original order.

Every inserted byte occurs at the final position of the published-applicability field for exactly one of the 11 identified rows.

Removing exactly those 11 inserted bytes from the corrected artifact reconstructs the immutable `engineering-171` tagged artifact byte-for-byte.

The reconstruction independently reproduces:

- SHA-256: `e7c31445ad77c2b6f592e88b846202286f003b039a717939b7f6d198d6672d46`;
- Git blob: `608f14b000f1b5faf7569562d674bb609bb79bf2`.

The corrected bytes independently reproduce:

- SHA-256: `f40638d8468749afe5d260fdf01e456fc27d3afd9febf75bfe2d59e2fa6d36ff`;
- Git blob: `8776e630a7a730074c90e3173913e46146ec95f8`.

## 8. Exact Correction Ledger

| Identifier | Corrected published applicability | Sole inserted byte |
|---|---|---|
| `PE-NORM-002` | Every requirement using `MUST` | final U+0060 |
| `PE-NORM-003` | Every requirement using `MUST NOT` | final U+0060 |
| `PE-NORM-004` | Every requirement using `SHOULD` | final U+0060 |
| `PE-NORM-005` | Every requirement using `SHOULD NOT` | final U+0060 |
| `PE-NORM-006` | Every requirement using `MAY` | final U+0060 |
| `PE-TRANSEXEC-006` | Every execution of authorized `U` | final U+0060 |
| `PE-COMMIT-004` | Every committed Protocol State Transition authorized against `Q0` | final U+0060 |
| `PE-COMMIT-008` | Every valid authorization and execution context for `U` | final U+0060 |
| `PE-STATE-009` | Every committed Protocol State Transition from `Q0` to `Q1` | final U+0060 |
| `PE-STALEAUTH-003` | Every authorized transition whose current protocol state remains equivalent to `Q0` | final U+0060 |
| `PE-STALEAUTH-004` | Every authorized transition whose current protocol state materially conflicts with `Q0` | final U+0060 |

No other field was repaired, normalized, rewritten, or changed.

## 9. Complete Profile V2 Preservation

After correction, all 729 successor-ledger rows match the guarded Profile V2 source rows in exact:

- row order;
- identifier;
- RF family;
- SF home;
- strength;
- published applicability;
- Profile V2 disposition;
- and profile-row SHA-256.

Verified totals:

| Property | Rows |
|---|---:|
| Successor-ledger rows | 729 |
| Unique identifiers | 729 |
| Exact published-applicability fields | 729 |
| Published-applicability mismatches | 0 |
| Exact profile-row SHA-256 values | 729 |

Profile V2 remains:

| Disposition | Rows |
|---|---:|
| applicable | 478 |
| non-applicable | 244 |
| resolved through permitted specification choice | 7 |
| **Total** | **729** |

## 10. Historical and Successor Evidence-Path States

Engineering[167] remains the reviewed historical predecessor:

| Engineering[167] state | Rows |
|---|---:|
| bounded | 193 |
| still-ambiguous | 292 |
| missing-evidence-path | 0 |
| not-required | 244 |
| **Total** | **729** |

The corrected Engineering[171] successor state remains:

| Successor state | Rows |
|---|---:|
| bounded | 216 |
| still-ambiguous | 269 |
| missing-evidence-path | 0 |
| not-required | 244 |
| **Total** | **729** |

The correction changes none of these states or totals.

## 11. Transition Preservation

Exactly 23 evidence-path transitions remain recorded:

- `PE-VALID-001`;
- `PE-VALID-002`;
- `PE-VALID-004`;
- `PE-VALID-008`;
- `PE-VALID-010`;
- `PE-VALID-011`;
- `PE-ACTION-015`;
- `PE-RULE-009`;
- `PE-RULE-010`;
- `PE-RULE-011`;
- `PE-EVAL-011`;
- `PE-EVAL-013`;
- `PE-EVAL-014`;
- `PE-EVAL-015`;
- `PE-EVAL-018`;
- `PE-EVAL-019`;
- `PE-DETERM-007`;
- `PE-DETERM-008`;
- `PE-DETERM-009`;
- `PE-CLASS-006`;
- `PE-CLASS-007`;
- `PE-CLASS-008`;
- `PE-CLASS-011`.

Transition treatment remains:

| Engineering[169] treatment | Total rows | Transitioned | Remained unchanged |
|---|---:|---:|---:|
| Proposed supported relationship | 5 | 5 | 0 |
| Explicit proposed non-mapping | 28 | 18 | 10 |
| Supported component plus unresolved complete relationship | 14 | 0 | 14 |
| Unresolved | 41 | 0 | 41 |
| **Total** | **88** | **23** | **65** |

Exactly 65 A04-A08 rows remain `still-ambiguous`.

Every non-A04-A08 evidence-path state remains exactly at its Engineering[167] state.

No transition was added, removed, reversed, or semantically changed.

## 12. Preserved Permitted-choice Rows

All seven permitted-choice rows remain unresolved and `still-ambiguous`:

- `PE-EVOL-018`;
- `PE-IFACE-009`;
- `PE-RUNTIME-005`;
- `PE-IMPL-005`;
- `PE-IMPL-011`;
- `PE-IMPL-013`;
- `PE-REALIZE-009`.

No permitted specification choice was selected by Engineering[173] or this re-review.

## 13. Preserved Unresolved Relationships

The following 12 relationships remain unresolved:

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

Every complete formal relationship depending on one or more of these remains `still-ambiguous`.

The correction supplies no new relationship evidence and resolves none of these relationships.

## 14. Action Coordinate and Public Inputs

`T-I164-ANONYMOUS-PUBLIC-ACTION` remains an implementation-owner action coordinate only.

It remains:

- not a protocol subject;
- not protocol authority;
- not Protocol Action occurrence identity;
- not Private Actor identity;
- and not an application replacement for Protocol Action.

The ordered public inputs remain exactly:

1. nullifier;
2. petitionId or actionId;
3. membershipRoot.

The public-input relationship remains separate from:

- private witness;
- proof identity;
- Protocol Action occurrence identity;
- application target;
- UI request;
- relay request;
- retry;
- transaction;
- response;
- event;
- state mutation;
- reconciliation;
- and indexed record.

## 15. Root, Evaluation, Determination, and Classification Boundaries

The root boundary remains:

- the circuit establishes inclusion under the supplied root;
- `AnonymousMembershipRegistry.isValidRoot` exists independently;
- `PetitionRegistry.signPetitionWithZKProof` contains no call or state read establishing accepted-root status;
- and `U-ROOT` remains unresolved.

The preserved lifecycle separations remain:

> proof verification  
> `!=` complete Protocol Action Evaluation

> partial or interrupted component sequence  
> `!=` completed Evaluation

> pre-evaluation or operational failure  
> `!=` Protocol Action Determination

No fallthrough, revert, transaction, hash, receipt, relay response, mutation, event, reconciliation result, indexed record, aggregate, or application success state is promoted into:

- Protocol Action Determination;
- acceptance;
- rejection;
- or protocol authority.

No correction byte affects these boundaries.

## 16. Evidence-Layer Separation

The following remain distinct:

> evidence-path boundedness  
> `!=` evidence availability  
> `!=` evidence sufficiency  
> `!=` requirement result

A bounded evidence path identifies the route through which later evidence must be obtained and evaluated.

It does not establish:

- availability of every required evidence item;
- sufficiency of available evidence;
- requirement satisfaction;
- requirement failure;
- implementation correctness;
- implementation defect;
- conformance;
- compatibility;
- certification;
- or operational readiness.

Engineering[173] changed copied metadata punctuation only.

## 17. ZK-provenance Preservation

The inherited ZK-provenance observations remain unchanged:

- three canonical manifest items are absent;
- three tracked items differ from recorded manifest digests;
- six tracked items match;
- two canonical-to-runtime comparisons remain unavailable;
- and canonical and frontend runtime verification keys are byte-identical.

These remain evidence-availability and dependency observations only.

Engineering[173] and this re-review:

- generated no cryptographic artifact;
- replaced no cryptographic artifact;
- altered no manifest;
- promoted no runtime artifact;
- and produced no requirement result from these observations.

## 18. Privacy and Neutral-naming Review

The preserved privacy rule is:

> Private actors, public actions.

Because the corrected artifact differs from the immutable artifact only by 11 final U+0060 characters in copied published-applicability fields, the correction introduces no new semantic or naming surface.

It introduces no:

- Private Actor identity;
- reusable participant identity;
- wallet provenance;
- sponsor provenance;
- funding provenance;
- admission provenance;
- transport provenance;
- ownership provenance;
- cross-action correlation surface;
- metadata bridge;
- actor-reconstruction path;
- or privacy-sensitive review identifier.

The affected identifiers identify public formal requirements only.

No correction byte creates or strengthens an identity, provenance, ownership, or correlation relationship.

## 19. Correction Lifecycle Consequence

The verified lifecycle is:

> `engineering-171`  
> `->` immutable pre-correction artifact  
>
> Engineering[172]  
> `->` rejection of the pre-correction artifact  
>
> Engineering[173]  
> `->` exact mechanically bounded correction plus correction record  
>
> Engineering[174]  
> `->` independent re-review of the corrected artifact and correction record

Engineering[172] remains historically correct for the immutable pre-correction artifact.

Engineering[173] remains the correction occurrence.

This record does not rewrite or supersede the immutable meanings of those earlier records.

## 20. Final Review Result

- accepted;
- the immutable pre-correction Engineering[171] artifact was independently reconstructed and verified;
- exactly the 11 Engineering[172]-identified U+0060 insertions and no other byte changes were independently verified;
- all 729 Profile V2 metadata fields are preserved exactly;
- all 23 transitions remain unchanged;
- all 65 remaining A04-A08 rows remain `still-ambiguous`;
- all non-A04-A08 evidence-path states remain unchanged;
- the successor totals remain 216 bounded / 269 still-ambiguous / 0 missing-evidence-path / 244 not-required;
- the corrected Engineering[171] determination is accepted as the reviewed-current successor evidence-path basis;
- Engineering[167] remains the reviewed historical predecessor;
- assessment readiness may resume only for a later bounded assessment slice;
- no requirement-level assessment was performed;
- and no requirement result was produced.
