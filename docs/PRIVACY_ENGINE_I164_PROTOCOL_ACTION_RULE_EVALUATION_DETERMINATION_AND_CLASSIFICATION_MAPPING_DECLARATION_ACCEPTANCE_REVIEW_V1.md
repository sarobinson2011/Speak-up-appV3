# Privacy Engine I164 Protocol Action, Rule Evaluation, Determination, and Classification Mapping Declaration Acceptance Review V1

## 1. Status and Purpose

This document is the separate implementation-governance acceptance review and acceptance occurrence for:

`PE-I164-ACTION-EVALUATION-DETERMINATION-CLASSIFICATION-MAPPING-DECLARATION-V1`

Its acceptance status is:

> accepted

The accepted declaration remains an immutable Engineering[169] artifact. This record does not modify it.

Acceptance means only that the declaration is accepted as the implementation owner’s mapping statement about the fixed I164 baseline for the relationships it explicitly declares.

Acceptance does not prove I164 behaviour, deployment behaviour, runtime behaviour, evidence sufficiency, requirement satisfaction, requirement failure, compatibility, conformance, certification, security, operational readiness, or Reference Implementation status.

STATE.md remains the single canonical development authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

## 2. Acceptance-Record Identity

| Field | Accepted value |
|---|---|
| Acceptance-record identifier | `PE-I164-ACTION-EVALUATION-DETERMINATION-CLASSIFICATION-MAPPING-DECLARATION-ACCEPTANCE-REVIEW-V1` |
| Acceptance-record title | Privacy Engine I164 Protocol Action, Rule Evaluation, Determination, and Classification Mapping Declaration Acceptance Review V1 |
| Acceptance-record version | `1` |
| Acceptance status | `accepted` |
| Acceptance package format | `PE-I164-AEDC-MAPPING-ACCEPTANCE/1` |
| Acceptance occurrence identity | `PE-I164-AEDC-MAPPING-ACCEPTANCE-2026-08-18` |
| Acceptance occurrence integrity identifier | `3c2a25b20c119d399cf3e954c26fd465834c82b6835b430f5375552fb1a1be06` |
| Acceptance date | `2026-08-18` |
| Accepting authority | implementation-governance boundary governing I164 |
| Private Actor identity encoded | no |
| Requirement assessment performed | no |
| Requirement result produced | no |
| Reference Implementation designation | no |

The acceptance-occurrence integrity identifier is the SHA-256 of the canonical acceptance payload recorded in Section 3.

The SHA-256 of this complete file is intentionally emitted after creation and may be bound by the later `engineering-170` repository tag.

## 3. Canonical Acceptance Payload

The canonical payload is the following exact UTF-8 serialization, joined by LF characters with no final LF:

    PE-I164-AEDC-MAPPING-ACCEPTANCE/1
    acceptance-record-id=PE-I164-ACTION-EVALUATION-DETERMINATION-CLASSIFICATION-MAPPING-DECLARATION-ACCEPTANCE-REVIEW-V1
    accepted-declaration-id=PE-I164-ACTION-EVALUATION-DETERMINATION-CLASSIFICATION-MAPPING-DECLARATION-V1
    accepted-declaration-sha256=a6e488f8a246dcf14c2a3a3e0df8226833ccec8720d12c6798a971a0d3ee6890
    baseline-tag=engineering-164
    baseline-commit=003e984ea73a2dede092443893dfbc9e74121e14
    baseline-tree=6271b80f2fa6167961e18c5b4c229d25374497a7
    baseline-archive-sha256=7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847
    scope-serialization-sha256=91b2d8acca57a395b738b18001a3e47b9f4c15f382a4c0bb6124bf1ac46f494d
    engineering-169-tag=engineering-169
    engineering-169-commit=392863755dac71b5d762c26caf3830c987dbbfaf
    engineering-169-tree=91de8930ed29add9b0e7986566319946e0d63bfa
    acceptance-status=accepted
    acceptance-date=2026-08-18

Its SHA-256 is:

`3c2a25b20c119d399cf3e954c26fd465834c82b6835b430f5375552fb1a1be06`

This payload identifies the declaration and baseline. It identifies no Private Actor.

## 4. Accepted Declaration Identity

| Field | Verified value |
|---|---|
| Declaration identifier | `PE-I164-ACTION-EVALUATION-DETERMINATION-CLASSIFICATION-MAPPING-DECLARATION-V1` |
| Declaration title | Privacy Engine I164 Protocol Action, Rule Evaluation, Determination, and Classification Mapping Declaration V1 |
| Declaration version | `1` |
| Declaration package format | `PE-I164-IMPLEMENTATION-OWNER-MAPPING/1` |
| Pre-acceptance status | `draft` |
| Acceptance required | yes |
| Pre-acceptance occurrence | none |
| Declaration scope | Engineering[167] groups A04–A08 |
| Scope rows | 88 |
| Declaration SHA-256 | `a6e488f8a246dcf14c2a3a3e0df8226833ccec8720d12c6798a971a0d3ee6890` |
| Engineering tag | `engineering-169` |
| Engineering commit | `392863755dac71b5d762c26caf3830c987dbbfaf` |
| Engineering tree | `91de8930ed29add9b0e7986566319946e0d63bfa` |
| Tagged-file SHA-256 | `a6e488f8a246dcf14c2a3a3e0df8226833ccec8720d12c6798a971a0d3ee6890` |

The working-copy declaration and the file contained by `engineering-169` are byte-identical.

Engineering[169] remains historically draft. This separate record creates the required acceptance occurrence without rewriting the declaration.

## 5. Guarded Formal Corpus

The supplied Engineering[170] formal corpus passed compressed-data integrity verification and contains 89 distinct files.

Its SHA-256 is:

`076796e2ca9b041701deef7589f460f96df855b3fb2b7b63abb957ee3f243b60`

The Engineering[169] construction corpus remains separately recorded by Engineering[169] as an 88-file archive with SHA-256:

`4e5b15835063318a1982090b598937138b10147d217c618ea89cbfb5cf0fbf4b`

The additional Engineering[170] corpus member is the immutable Engineering[169] declaration.

| Guarded artifact | SHA-256 |
|---|---|
| `STATE.md` | `228886af0db33a801db40d834c1a1070ed8f330d6708d8e6674021e3a2d3be33` |
| `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_V1.md` | `f2c12b60f24fe8fe8eddf27dc2d59814aceba42b907160c54ad3868bde7da393` |
| `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_PUBLICATION_RECORD_V1.md` | `d655359c296d6d6aefffd3e6faa0fd47f6506ec9d64a871ade9f9eb469108029` |
| `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_FINAL_CONSOLIDATION_REREVIEW_V1.md` | `7bf415870a2e630157d1cf186e45764513e87b5f13b2ac790373d4de5df13bb7` |
| `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2.md` | `279fc80cb2998df8c4fddcc2ea25e4091897571c57a7d5905100857612b2d79c` |
| `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2_COMPOSITION_REREVIEW_V1.md` | `093f3d2178bc890e7bed9dc56aea164f36918a01e49caef2ed8d777777dd0d11` |
| `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_IDENTITY_VERSION_CORRECTION_V1.md` | `c37a3fa1985a11243ff0b1103d5d7ca911f77e76a14f00f4c12a368e4f7ad88a` |
| `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2_STATUS_SYNCHRONIZATION_V1.md` | `d8bce61c2366e4a5ca6d6d87ef4875944956acd1b8303e73f2f901c7a1ba1e27` |
| `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2_IMPLEMENTATION_ASSESSMENT_BASIS_AND_SCOPE_DETERMINATION_V1.md` | `a3547f19e187cb9b0c5493c75832a9bebd95c2462387cdc120907fc413ce89af` |
| Engineering[166] | `46294d6e4dc2928409713bad32e510ee2c1749d39fdc0ed27ae70b1219f88175` |
| Engineering[167] | `bdea6dc1f2b9af176de9e354daf654a3c4a8b1eb4bd46c16d1ff0ea3fbfc5cd2` |
| Engineering[168] | `1280eb90b97f9caa21456f8ce8ce58f6211b5ef360d8d2637110a43c4f00e7f2` |
| Engineering[169] | `a6e488f8a246dcf14c2a3a3e0df8226833ccec8720d12c6798a971a0d3ee6890` |

No guarded artifact was modified.

## 6. Fixed I164 Baseline

| Baseline field | Verified value |
|---|---|
| Repository | Speak-up-appV3 |
| Baseline identity | I164 |
| Tag | `engineering-164` |
| Commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Git tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |
| Implementation archive | `implementation-baseline-engineering-164.zip` |
| Archive SHA-256 | `7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847` |
| Embedded archive commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Tracked paths | 308 |
| Blob paths | 305 |
| Gitlink paths | 3 |

All 305 archived blob paths match the I164 Git tree by path and Git blob identity.

The three Gitlinks remain:

| Path | Gitlink identity |
|---|---|
| `contracts/lib/forge-std` | `52c1e835e9ffcfe00bd9f8f51de204b93bc7028a` |
| `contracts/lib/openzeppelin-contracts` | `8ff78ffb6e78463f070eab59487b4ba30481b53c` |
| `contracts/lib/openzeppelin-contracts-upgradeable` | `b933412726bccd822a871116f1427111e649ff54` |

The declaration and this acceptance occurrence are about I164. Neither is a member or modification of I164.

## 7. Profile and Evidence-Path Preservation

All 729 Profile V2 rows remain preserved in exact order with exact identifiers, RF families, SF homes, strengths, published applicability, profile dispositions, and profile-row SHA-256 identities.

Profile V2 remains:

| Disposition | Rows |
|---|---:|
| applicable | 478 |
| non-applicable | 244 |
| resolved through permitted specification choice | 7 |
| **Total** | **729** |

Engineering[167] remains:

| Evidence-path state | Rows |
|---|---:|
| bounded | 193 |
| still-ambiguous | 292 |
| missing-evidence-path | 0 |
| not-required | 244 |
| **Total** | **729** |

The seven permitted-choice rows remain unresolved and `still-ambiguous`:

- `PE-EVOL-018`;
- `PE-IFACE-009`;
- `PE-RUNTIME-005`;
- `PE-IMPL-005`;
- `PE-IMPL-011`;
- `PE-IMPL-013`;
- `PE-REALIZE-009`.

Acceptance changes no Profile V2 disposition and no Engineering[167] state.

## 8. Exact Acceptance Scope

| Group | Subject | Rows |
|---|---|---:|
| A04 | Validity rules and applicable rule sets | 25 |
| A05 | Protocol Action mapping | 17 |
| A06 | Protocol Action Evaluation mapping | 20 |
| A07 | Protocol Action Determination mapping | 14 |
| A08 | Acceptance and rejection classification mapping | 12 |
| **Total** |  | **88** |

The 88 rows are distinct and remain `still-ambiguous`.

Their ordered Engineering[167] source-row serialization SHA-256 is:

`91b2d8acca57a395b738b18001a3e47b9f4c15f382a4c0bb6124bf1ac46f494d`

Every Engineering[169] scope row retains its exact Profile V2 identifier, RF family, SF home, strength, published applicability, profile disposition, Engineering[167] group, Engineering[167] state, profile-row SHA-256, draft treatment, and relationship reference.

Acceptance makes the explicitly declared mapping statements available as accepted implementation-owned mapping evidence. It does not make any of the 88 evidence paths bounded.

## 9. Engineering[168] Construction Review

The required construction rule is:

> explicit formal subject or requirement  
> `+` explicit relationship identity  
> `+` exact I164 material  
> `+` bounded assertion  
> `+` explicit non-mappings  
> `+` declared limitations  
> `+` evidence dependencies  
> `+` accepted declaration authority

Engineering[169] satisfies the first seven terms.

This record supplies the eighth term through the implementation-governance boundary governing I164.

Therefore:

> accepted declaration  
> `=` immutable Engineering[169] package  
> `+` this separate acceptance occurrence

The accepted relationship remains bounded by its exact Engineering[169] statement. Acceptance supplies no missing relationship and performs no assessment.

## 10. Evidence-Register Verification

All 35 Engineering[169] evidence-register entries were reviewed.

For every entry, the following match I164:

- tracked path;
- Git mode;
- Git object type;
- Git object identity;
- blob SHA-256;
- and archived bytes.

No path name or candidate presence was treated as proof of a mapping.

The component evidence bindings used by the accepted declaration are:

| Evidence key | Exact I164 path | Git object | Blob SHA-256 |
|---|---|---|---|
| `EV-PROOF-HOOK` | `frontend/src/hooks/useZKProof.js` | `985e8adb8410a134fa010d2fa49ee179e47edfb5` | `8df56093b0a5a3ed8121e3cbe45761d0cfc967bc0fcdd108222944f5901a575a` |
| `EV-CIRCUIT` | `zk/v3-groth16/circuits/sign_petition.circom` | `165ed8cfa1029dd0a937ab6e885af020fbf991e5` | `a64783f8873df0c9dda7f7e44607e076f0b2af94c9cd609e4619e4b0fbcf2e02` |
| `EV-VERIFIER` | `contracts/src/v3/Groth16Verifier.sol` | `bf3bd28b1e89e8672219aa5aea6e54605d1b5bfe` | `b1216366353f3dbf478e1e03add31077bbe4bc76d5a4e40aaba574cd5841bd87` |
| `EV-PETITION` | `contracts/src/PetitionRegistry.sol` | `a593c4023fc1ce9c835013a5ad40a310e5bfd032` | `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` |
| `EV-MEMBERSHIP` | `contracts/src/AnonymousMembershipRegistry.sol` | `31835a9feeeff6691335cca655b1f9e31ceba0d6` | `2b883cbca96f074c52d0471aaa62681ae042b8315d5e1260ab114541650c7978` |
| `EV-RELAY` | `backend/src/routes/relay.js` | `23a4d5f37a5dafa2cfd39030e1d42bff9807e3e7` | `1f748b519358c4d4653dfce5d13d6f54cab4a3cd7cb70d8f1937a75a06990f7a` |
| `EV-FRESHNESS` | `backend/src/services/indexerFreshness.js` | `cdcf3077e0ab7f231b53726f8eb90bac1a76a0ef` | `66b870d2087ecef424019933e2aa90451244869a6c6929c5e7b595109fd4a794` |
| `EV-EXECUTION` | `backend/src/services/relayExecution.js` | `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` | `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` |
| `EV-OBSERVATION` | `backend/src/indexer/petitions/processor.js` | `b38e89799c61a846025390325f882c2a69ce9759` | `addfa0e87da3c1a94628d30024556fa9ba644df46c78fb27caac7529e18b3437` |

## 11. Component-Entry Review

Each entry was reviewed for formal-row references, exact I164 path, Git object, blob SHA-256, stable content anchor, input and result, failure behaviour, evidence-class assignment, and limitation.

| Component | Formal rows | Evidence and anchor | Input, result, and failure | Evidence classes | Acceptance review |
|---|---|---|---|---|---|
| `C-WITNESS` | PE-VALID-001; PE-EVAL-013 | `EV-PROOF-HOOK`; `normalizeInputs`; `normalizeMerkleToMatchRoot`; `generateProof` | Local witness and action context become proof input; construction may fail locally | TD | Verified as pre-Evaluation construction only |
| `C-CIRCUIT` | PE-VALID-001; PE-VALID-002; PE-VALID-008; PE-EVAL-013 | `EV-CIRCUIT`; `MerkleTreeInclusionProof`; `SignPetition`; `component main` | Witness and public values constrain the proof relation; unsatisfied constraints prevent proof construction | TD,RG | Verified; accepted-root status remains excluded |
| `C-PUBLIC-ORDER` | PE-VALID-001; PE-RULE-007; PE-ACTION-010 | `EV-CIRCUIT`; `nullifier`; `main {public [petitionId, membershipRoot]}` | Circuit relation fixes nullifier, action context, root ordering; incoherence cannot satisfy the bound relation | BD,TD,RG | Verified only for the declared three-value ordering |
| `C-VERIFY` | PE-VALID-001; PE-VALID-002; PE-VALID-004; PE-VALID-008; PE-EVAL-013; PE-EVAL-014; PE-EVAL-015 | `EV-VERIFIER`; `verifyProof`; `checkField`; `checkPairing` | Proof and three public signals produce a bounded Boolean result; invalid field or pairing returns false | TD,RG,DB,RO | Verified as one component, not complete validity |
| `C-EXISTS` | PE-VALID-005; PE-VALID-006; PE-EVAL-016 | `EV-PETITION`; petition-existence guard | Application-target key and stored flag permit continuation or `PetitionDoesNotExist` | TD,DB,RO | Exact implementation check verified; protocol-rule assignment unresolved |
| `C-UNIQUE` | PE-VALID-005; PE-VALID-007; PE-RULE-007; PE-RULE-010; PE-EVAL-016 | `EV-PETITION`; `usedSignNullifier`; `signPetitionWithZKProof`; `hasSignedPetition` | Action context and nullifier produce unused or used state; used state causes `NullifierAlreadyUsed` | TD,RG,DB,RO | Action-local uniqueness verified without participant identity |
| `C-VERIFIER-CONFIG` | PE-RULE-005; PE-CLASS-007 | `EV-PETITION`; zero-verifier guard | Configuration permits execution or causes `InvalidVerifier` | TD,DB,RO | Verified as deployment/configuration condition only |
| `C-PROOF-RESULT` | PE-VALID-002; PE-VALID-004; PE-VALID-008; PE-EVAL-013; PE-EVAL-014; PE-EVAL-015 | `EV-PETITION`; `groth16Verifier.verifyProof` | Verifier result permits continuation or causes `InvalidZKProof` | TD,RG,DB,RO | Verified without Determination or classification |
| `C-PUBLIC-NULLIFIER` | PE-VALID-005; PE-VALID-007; PE-RULE-007; PE-EVAL-016 | `EV-PETITION`; `uint256(nullifier) != pubSignals[0]` | Argument and signal zero are coherent or cause `InvalidZKProof` | TD,RG,DB,RO | Verified without creating Action identity |
| `C-PUBLIC-ACTION` | PE-VALID-005; PE-VALID-007; PE-RULE-007; PE-ACTION-010; PE-EVAL-016 | `EV-PETITION`; `petitionId != pubSignals[1]` | Action-context argument and signal one are coherent or cause `InvalidZKProof` | TD,RG,DB,RO | Verified without merging application-target and Action identities |
| `C-ROOT-INCLUSION` | PE-VALID-001; PE-VALID-007; PE-RULE-007 | `EV-CIRCUIT`; `hashes[nLevels] === root` | Witness path equals supplied root or circuit constraints fail | TD,RG | Inclusion under the supplied root only |
| `C-ROOT-ACCEPTED` | PE-VALID-003; PE-VALID-005; PE-VALID-007; PE-RULE-001; PE-RULE-007; PE-EVAL-003; PE-EVAL-008; PE-EVAL-016 | `EV-MEMBERSHIP`; `isValidRoot`; `isKnownRoot` | Claimed root can be read against accepted-root state; active signing path has no result | TD,DB,RO | Candidate presence verified; formal mapping remains unresolved |
| `O-RELAY-PAYLOAD` | PE-RULE-005; PE-ACTION-006; PE-EVAL-019; PE-CLASS-006; PE-CLASS-007 | `EV-RELAY`; `POST /sign` validation branches | Transport request is operationally admitted or refused with HTTP 400 | TD,RO | Verified as pre-authoritative operational validation |
| `O-INDEXER-FRESHNESS` | PE-RULE-005; PE-EVAL-019; PE-CLASS-007 | `EV-FRESHNESS`; `getPetitionIndexerFreshness` | Cursor and latest block produce operational health or degraded state | TD,RO | Not a protocol-validity rule or rejection |
| `O-DISPATCH` | PE-ACTION-006; PE-ACTION-008; PE-RULE-011; PE-CLASS-007 | `EV-EXECUTION`; `freezeRelaySubmission`; `dispatchRelayExecution`; `deriveTempestSeed` | One frozen submission is presented through ordered attempts; executor or transport failure may occur | TD,RG,DB,RO | Operational preservation verified; retry identity unresolved |
| `O-RECONCILE` | PE-ACTION-008; PE-RULE-011; PE-CLASS-007 | `EV-EXECUTION`; `reconcileRelayExecutionState` | Uncertain submission is observed through bounded used-state read; null or read failure may result | TD,RG,DB,RO | Not Determination or acceptance |
| `O-OBSERVATION` | PE-DETERM-009; PE-DETERM-010; PE-CLASS-007 | `EV-OBSERVATION`; `PetitionSigned` normalization and dispatch | Chain log becomes downstream normalized observation; indexing or persistence may fail | TD,RO | Event and indexed record remain downstream observations |

No component entry was promoted beyond its Engineering[169] limitation.

## 12. Accepted Asserted Relationships

| Relationship | Engineering[169] subject | Acceptance review |
|---|---|---|
| `ASR-001` | Declared public-input relationship | Accepted for exactly the ordered public set nullifier, petitionId/actionId, membershipRoot |
| `ASR-002` | Private/public separation | Accepted; private witness inputs remain outside relay and contract-call payloads |
| `ASR-003` | Proof relation | Accepted for knowledge, supplied-root inclusion, and action-scoped nullifier derivation; accepted-root status excluded |
| `ASR-004` | Bounded verifier result | Accepted only for the configured proof relation and three supplied public signals |
| `ASR-005` | Public-signal coherence | Accepted for argument binding to public-signal positions zero and one |
| `ASR-006` | Action-local uniqueness | Accepted for the action-context/nullifier relation and state guard; no participant identity |
| `ASR-007` | Operational preservation | Accepted for one frozen submission value across fallback; retry equivalence remains unresolved |
| `ASR-008` | Application-role separation | Accepted; shared serialization does not merge application target with Protocol Action identity |
| `ASR-009` | Observation separation | Accepted; transactions, responses, events, mutations, reconciliation, and indexed records remain downstream or operational representations |

For every asserted relationship:

- the formal subject is preserved;
- the relationship identity is bounded;
- the I164 material is exact;
- the assertion does not exceed that material;
- relevant non-mappings remain binding;
- limitations remain explicit;
- evidence dependencies remain separate;
- and the privacy boundary remains intact.

Acceptance applies only to the bounded assertions above.

## 13. Accepted Explicit Non-Mappings

| Identifier | Accepted boundary |
|---|---|
| `NM-001` | UI request is not Protocol Action |
| `NM-002` | Private witness is not Protocol Action identity |
| `NM-003` | Proof is not Private Actor identity |
| `NM-004` | Proof-generation attempt is not Protocol Action Evaluation |
| `NM-005` | Relay request is not automatically a Protocol Action occurrence |
| `NM-006` | Successful proof verification is not complete Protocol Action validity |
| `NM-007` | Retry or fallback is not automatically a new or merged Action occurrence |
| `NM-008` | TEMPEST operational coordinates are not Action identity or rule applicability |
| `NM-009` | Transaction or transaction hash is not Determination |
| `NM-010` | Contract revert is not automatically formal rejection |
| `NM-011` | Relay or UI response is not Determination |
| `NM-012` | Event is not Determination |
| `NM-013` | State mutation is not acceptance or rejection classification |
| `NM-014` | Reconciliation result is not Determination |
| `NM-015` | Indexer or persistence record is not protocol authority |
| `NM-016` | Application-target identity is not Action occurrence identity |
| `NM-017` | Application meaning is not protocol validity or classification |
| `NM-018` | Runtime success is not evidence sufficiency |
| `NM-019` | Draft declaration is not a requirement result |

No non-mapping creates a positive mapping, merges formal subjects, promotes an operational identifier, imports application semantics into protocol identity, creates actor identity, or weakens an unresolved relationship.

## 14. Preserved Unresolved Relationships

| Relationship | Missing mapping | Candidate material reviewed | Preserved reason and treatment |
|---|---|---|---|
| `U-ACTION-IDENTITY` | Stable Protocol Action occurrence identity | Contract call, relay submission, transaction, event, state key | No exact baseline declaration chooses occurrence coordinates; no substitute inferred |
| `U-ACTION-ADMISSION` | Authoritative Action admission boundary | Relay admission and ABI-decoded invocation | Complete rules and context are not established before either boundary |
| `U-RETRY` | Repeated-presentation identity rule | Frozen submission, permutation, fallback, reconciliation | Payload preservation does not determine whether presentations are one or distinct Actions |
| `U-RULESET` | Complete applicable protocol-rule set | Circuit, verifier, guards, relay checks, state, tests, documents | No exhaustive generation-derived assignment separates all protocol rules from operational policy |
| `U-ROOT` | Accepted membership-root status | Circuit equality, `isValidRoot`, active signing path | The active path contains no call or state read establishing accepted-root status |
| `U-EVAL-IDENTITY` | Stable Evaluation occurrence identity | Invocation and sequential checks | No representation separately identifies one formal Evaluation |
| `U-EVAL-BOUNDARY` | Evaluation start, completion, and combination rule | Sequential guards and verifier call | No complete rules, completeness state, complete results, or combination record |
| `U-EVAL-REJECTION` | Complete rejecting Evaluation | Short-circuit revert branches | Later checks need not run; every applicable rule is not shown as evaluated |
| `U-DETERMINATION` | Stable Determination representation | Fallthrough, revert, transaction, response, event, mutation, indexed record | No candidate is separately the result of one completed Evaluation |
| `U-CLASSIFICATION` | Mutually exclusive acceptance or rejection classification | Success and failure surfaces | No valid Determination or separate classification record exists |
| `U-PRIVACY-REVIEW` | Complete baseline-wide privacy and neutral-naming review | Client, relay, contract, diagnostics, tests, events, persistence | Declaration privacy was reviewed; complete baseline privacy evidence remains separate |
| `U-PROVENANCE` | Synchronized ZK provenance chain | Manifest, runtime artifacts, canonical paths, verifier, golden proof | Recorded absences, digest differences, and unavailable comparisons remain unresolved |

All affected rows remain `still-ambiguous`.

No unresolved relationship is repaired, substituted, inferred, accepted as supported, or converted into a requirement result.

## 15. Action-Type Coordinate and Public Inputs

The accepted implementation-owner coordinate is:

`T-I164-ANONYMOUS-PUBLIC-ACTION`

It remains:

- an implementation-owner mapping coordinate only;
- not a new protocol subject;
- not protocol authority;
- not an application-defined replacement for Protocol Action;
- not a Protocol Action occurrence identity;
- and not a Private Actor identity.

The accepted public-input relationship is exactly:

1. nullifier;
2. petitionId or actionId;
3. membershipRoot.

It remains separate from:

- memberSecret;
- membershipPath;
- membershipIndices;
- proof identity;
- Protocol Action occurrence identity;
- application-target identity;
- UI request;
- relay request;
- retry;
- transaction;
- response;
- event;
- state mutation;
- and indexed record.

The ignored ABI compatibility field remains fixed to zero on the active path and is not mapped as a public input, actor identity, Action identity, or cross-action coordinate.

## 16. Applicable-Rule and Root Boundary

I164 establishes circuit inclusion under the supplied membership root.

I164 separately exposes `AnonymousMembershipRegistry.isValidRoot` through `isKnownRoot`.

`PetitionRegistry.signPetitionWithZKProof` contains no call or state read connecting accepted-root status to the active signing path.

Therefore `U-ROOT` remains unresolved.

This acceptance record does not convert that observation into a requirement result, defect, security finding, remediation instruction, or complete applicable-rule set.

Petition existence remains an exact implementation check. Its generation-derived protocol-rule assignment remains unresolved.

## 17. Evaluation Boundary

Engineering[169] correctly declines to declare:

- stable Evaluation occurrence identity;
- authoritative Evaluation start;
- complete applicable-rule set;
- complete evaluation context;
- complete component evaluation;
- coherent all-component combination;
- or complete rejecting Evaluation.

The preserved relationships are:

> proof verification  
> `!=` complete Protocol Action Evaluation

> partial or interrupted component sequence  
> `!=` completed Evaluation

> pre-evaluation or operational failure  
> `!=` Protocol Action Determination

Successful passage through implemented guards does not establish evaluation of every applicable protocol rule.

Short-circuit reversion does not establish a complete rejecting Evaluation.

## 18. Determination and Classification Boundary

No accepted mapping selects any of the following as a formal Determination:

- successful function fallthrough;
- revert;
- transaction;
- transaction hash;
- receipt;
- relay response;
- state mutation;
- event;
- reconciliation result;
- indexed record;
- aggregate;
- or application success state.

Formal acceptance and rejection remain unresolved.

Malformed submission, proof-generation failure, local preflight failure, indexer freshness, executor failure, transport failure, fallback progression, transaction-submission failure, revert, uncertain execution state, reconciliation, persistence lag, and application failure remain non-classification outcomes.

No execution success is classified as formal acceptance.

No revert or failure is classified as formal rejection.

## 19. Evidence-Layer Separation

| Evidence layer | Accepted availability position | Binding limitation |
|---|---|---|
| Boundary documentation | Available | Intent and boundary evidence only |
| Tracked-direct evidence | Available | Supports only explicitly bound relationships |
| Reproducibly generated evidence | Procedure available; no new result | No build, test, proof, or verifier output created |
| Deployment-bound evidence | Dependency identified | No deployment observation created or promoted |
| Runtime-observation evidence | Dependency identified | No runtime observation created or promoted |
| Unavailable evidence | Explicitly recorded | Corresponding relationships remain unresolved |
| Evidence required before assessment | Preserved as required | Acceptance alone does not establish sufficiency |

The fixed separation remains:

> evidence availability  
> `!=` evidence sufficiency  
> `!=` requirement result

The inherited ZK provenance position remains unchanged:

- three canonical manifest items are absent from the tracked baseline;
- three tracked items differ from recorded manifest digests;
- six tracked items match;
- two canonical-to-runtime comparisons remain unavailable;
- and canonical and frontend runtime verification keys are byte-identical.

These are availability and dependency observations only.

## 20. Privacy and Neutral-Naming Review

The acceptance occurrence preserves:

> Private actors, public actions.

Review result:

- no Private Actor identity introduced;
- no reusable participant identity introduced;
- no wallet provenance introduced;
- no sponsor provenance introduced;
- no funding provenance introduced;
- no admission provenance introduced;
- no transport provenance introduced;
- no ownership provenance introduced;
- no cross-action correlation surface introduced;
- no metadata bridge introduced;
- no actor-reconstruction path introduced;
- and no private witness or runtime actor-linked value reproduced.

The acceptance occurrence identifies only the declaration, fixed baseline, public scope, neutral implementation-governance authority, and integrity material.

Privacy review result: accepted.

## 21. Authority and Hierarchy

The preserved hierarchy is:

> Privacy Engine protocol authority  
> `!=` I164 implementation governance  
> `!=` Speak Up application meaning

The Privacy Engine remains the primary implementation-independent privacy participation protocol.

I164 remains one bounded implementation baseline.

Speak Up remains one application adapter and use case.

Acceptance governs only the implementation-owned declaration about I164.

It does not grant Speak-up-appV3 authority over the Privacy Engine protocol, published specification, Profile V2, or formal requirement meanings.

## 22. Lifecycle Consequences

This acceptance occurrence establishes:

- Engineering[169] as accepted implementation-owned mapping evidence for its explicit supported relationships;
- Engineering[169] explicit non-mappings as accepted implementation-owned boundary statements;
- Engineering[169] limitations as binding;
- Engineering[169] evidence dependencies as binding;
- and every unsupported relationship as unresolved.

It does not establish:

- implementation behaviour proof;
- reproducibly generated evidence;
- deployment-bound evidence;
- runtime-observation evidence;
- evidence sufficiency;
- requirement satisfaction or failure;
- compatibility;
- conformance;
- certification;
- security assessment;
- operational readiness;
- Reference Implementation designation;
- a Profile V2 change;
- an Engineering[167] reclassification;
- a permitted-choice resolution;
- a new protocol generation;
- or a publication occurrence.

Any correction, supersession, or withdrawal requires a new immutable record and new acceptance occurrence.

Any later evidence-path reclassification or requirement assessment requires a separately bounded determination.

## 23. Final Determination

Engineering[169] is accepted as implementation-owned mapping evidence for the relationships it explicitly declares, with every unsupported relationship remaining unresolved.
