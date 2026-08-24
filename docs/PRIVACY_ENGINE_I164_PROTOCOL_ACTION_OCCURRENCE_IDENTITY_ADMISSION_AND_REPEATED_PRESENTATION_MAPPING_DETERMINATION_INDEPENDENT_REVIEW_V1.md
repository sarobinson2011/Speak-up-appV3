# Privacy Engine I164 Protocol Action Occurrence Identity, Admission and Repeated-Presentation Mapping Determination Independent Review V1

Review date: 2026-08-23.

STATE.md remains the single canonical development authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

## 1. Purpose and Status

This record independently reviews Engineering[181]:

`docs/PRIVACY_ENGINE_I164_PROTOCOL_ACTION_OCCURRENCE_IDENTITY_ADMISSION_AND_REPEATED_PRESENTATION_MAPPING_DETERMINATION_V1.md`

It answers one architectural question:

> Did Engineering[181] correctly determine that I164 does not supply a complete Protocol Action occurrence identity, admission and repeated-presentation mapping package and that `U-ACTION-IDENTITY`, `U-ACTION-ADMISSION` and `U-RETRY` must remain unresolved?

Final review result:

**accepted**

This is exactly one indivisible final review result.

There is no partial acceptance.

Engineering[182] is an independent mapping-determination review only.

It is not:

- evidence-path reclassification;
- requirement assessment;
- a requirement result;
- an implementation-defect determination;
- a security assessment;
- a compatibility, conformance, certification or operational-readiness determination;
- a Reference Implementation designation;
- a protocol-generation occurrence;
- or a publication occurrence.

## 2. Foundational Framing

The Privacy Engine is the primary implementation-independent privacy participation protocol.

I164 identifies one fixed Speak-up-appV3 implementation baseline examined under the accepted Complete Implementation Profile V2.

Speak Up remains one application adapter and use case.

Preserve:

> Privacy Engine protocol  
> `->` implementation-independent authority  
> `->` I164 as one bounded implementation  
> `->` Speak Up as one application adapter and use case

Speak-up-appV3 does not define, own, narrow, replace or become the Privacy Engine protocol.

## 3. Verified Handover Package

| Supplied item | Independently verified value |
|---|---|
| Formal-corpus compressed-data integrity | verified; no errors |
| Formal-corpus files | 101 distinct files |
| Formal-corpus SHA-256 | `c272b589a4a31aa3f70c59367f5a9c2a0308c944a3f7bb99dba3d9ad8f51acd5` |
| Implementation archive SHA-256 | `7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847` |
| Git-provenance SHA-256 | `e0089a8dc8556f4c0cecce921ef281726c7c280e9362ebc8b992b0a8de6ff5d4` |
| Provenance format | `PRIVACY-ENGINE-HANDOVER-GIT-PROVENANCE/1` |

The provenance record remains untracked handover metadata only.

It is not protocol documentation, an implementation artifact, protocol authority, mapping authority, acceptance authority, reclassification authority, review authority, requirement evidence or a requirement result.

## 4. Provenance and Tagged-File Verification

Engineering[164] and Engineering[169] through Engineering[181] were independently verified for:

- tag-object type;
- local ref;
- remote ref;
- resolved commit;
- resolved tree;
- parent;
- exact raw commit payload;
- independently reproduced Git commit identity;
- every changed-file Git blob;
- every changed-file SHA-256;
- and equality of local ref, remote ref and resolved commit.

Every inspected tag was a lightweight tag resolving to a commit.

Every raw commit payload independently reproduced its stated commit identity.

Historical overwritten Engineering[171] and Engineering[175] bytes were independently reconstructed and matched their immutable tagged Git blobs and SHA-256 identities.

No tag was rewritten or moved.

## 5. Fixed I164 Baseline

| Field | Independently verified value |
|---|---|
| Repository | Speak-up-appV3 |
| Baseline identity | I164 |
| Tag | `engineering-164` |
| Commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |
| Archive comment | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Distinct tracked paths | 308 |
| Blob paths | 305 |
| Gitlink paths | 3 |
| Reconstructed root tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |

Every tracked path, mode, blob SHA-256, Git blob identity and tree position was independently verified.

The three Gitlinks were independently preserved as:

| Path | Gitlink identity |
|---|---|
| `contracts/lib/forge-std` | `52c1e835e9ffcfe00bd9f8f51de204b93bc7028a` |
| `contracts/lib/openzeppelin-contracts` | `8ff78ffb6e78463f070eab59487b4ba30481b53c` |
| `contracts/lib/openzeppelin-contracts-upgradeable` | `b933412726bccd822a871116f1427111e649ff54` |

## 6. Guarded Authority and Evidence Chain

The following identities were independently guarded:

| Artifact | SHA-256 |
|---|---|
| `STATE.md` | `228886af0db33a801db40d834c1a1070ed8f330d6708d8e6674021e3a2d3be33` |
| Published Protocol Specification V1 | `f2c12b60f24fe8fe8eddf27dc2d59814aceba42b907160c54ad3868bde7da393` |
| Publication Record V1 | `d655359c296d6d6aefffd3e6faa0fd47f6506ec9d64a871ade9f9eb469108029` |
| Complete Implementation Profile V2 | `279fc80cb2998df8c4fddcc2ea25e4091897571c57a7d5905100857612b2d79c` |
| Profile V2 assessment-basis determination | `a3547f19e187cb9b0c5493c75832a9bebd95c2462387cdc120907fc413ce89af` |
| Engineering[166] | `46294d6e4dc2928409713bad32e510ee2c1749d39fdc0ed27ae70b1219f88175` |
| Engineering[167] | `bdea6dc1f2b9af176de9e354daf654a3c4a8b1eb4bd46c16d1ff0ea3fbfc5cd2` |
| Engineering[168] | `1280eb90b97f9caa21456f8ce8ce58f6211b5ef360d8d2637110a43c4f00e7f2` |
| Engineering[169] | `a6e488f8a246dcf14c2a3a3e0df8226833ccec8720d12c6798a971a0d3ee6890` |
| Engineering[170] | `7f435cf93d835ee3106e995c355a4d2019f2de81eaed5df2a5e9448b4bac20db` |
| Corrected Engineering[171] | `f40638d8468749afe5d260fdf01e456fc27d3afd9febf75bfe2d59e2fa6d36ff` |
| Engineering[172] | `cc4e5b82a2fba611fa68032ff6eef25c45c18c9ed3d7fbc963766513fbca5b8d` |
| Engineering[173] | `df1346947f347bb1c89569bafeb64fcee467680f88de5b4e318d9f0c7f97c1d9` |
| Engineering[174] | `ba5b8d9c6512e36f7d0d3b0e0aedd195ac0e1652cb0d7bfeeef2f17c0ab44b1f` |
| Immutable Engineering[175] | `1eb8ed90926975001e1976ad4e05edbb3e81f70aa703754e053cf1f768449085` |
| Corrected declaration | `aebc191a9b723c3397dc41c7471fdac48a0e11ae9969511d79205334cc40eeef` |
| Engineering[176] | `fc0a4fef49c3a8db3b8affd79eebea051d30a9ee2c77291af8d0c157da4e8a6c` |
| Engineering[177] | `f4ee5e9d86a2d75d9c524107f2c15680acc20b11a62971aade3171ad027fe2ca` |
| Engineering[178] | `488a419790d202ddb667fb968c945041561685dcf01223f3185402e2890c429e` |
| Engineering[179] | `d56e8dfa2a7489fe366798d78ce903874807773729090750144c096307503b64` |
| Engineering[180] | `622eb3746ee15b25bc278a903d4a76cb593a18823afdf417b407059202f5dc66` |
| Engineering[181] | `455704959c14de41f015661b14ce68ce48ee75013657078f7739ce41406dc607` |

No guarded artifact is modified by Engineering[182].

## 7. Engineering[180] Reviewed-Current Basis

Engineering[180] was independently verified as:

| Property | Verified value |
|---|---|
| Commit | `463c8957bd51774251197c59cd64340910a6d88d` |
| Tree | `2975148322eb081e960187182ff6a342f1a3c410` |
| Parent | `cb03b53cb212e2834c7220ccae3ee5781efdc474` |
| Changed-file Git blob | `c5d9441cbda779f00e7eec8536288977cf3803fa` |
| Artifact SHA-256 | `622eb3746ee15b25bc278a903d4a76cb593a18823afdf417b407059202f5dc66` |
| Canonical payload length | 1220 bytes |
| Canonical payload SHA-256 | `979bcb09bf65f96e0bcdd02431a50be02f815f9ffec7c930c7bbbf80b3575af6` |
| Final result | exactly one indivisible `accepted` result |
| Adopted transitions | exactly one |
| Reviewed-current successor basis | Engineering[179] |
| Requirement assessment | none |
| Requirement result | none |

The complete Engineering[180] transition serialization was independently reconstructed as:

`identifier|L174-state|L179-state|profile-row-sha256`

The reconstruction contains:

- 729 rows;
- 729 unique identifiers;
- exactly one changed row;
- `PE-SUBJ-010: still-ambiguous -> bounded`;
- every other row unchanged;
- LF row separators;
- no trailing LF;
- and SHA-256 `ac5ba6f99e12ee2581d885f044b8186cc950d8c91289d70a34781b473887295c`.

The independently derived reviewed-current totals are:

| State | Rows |
|---|---:|
| bounded | 217 |
| still-ambiguous | 268 |
| missing-evidence-path | 0 |
| not-required | 244 |
| **Total** | **729** |

Engineering[179] remains the reviewed-current evidence-path basis.

## 8. Engineering[181] Identity and Determination

Engineering[181] was independently verified as:

| Property | Verified value |
|---|---|
| Commit | `f9f6eec5fd0048d1b4c5120b6a16c6970ea58fa4` |
| Tree | `8948a1c4b38c2477dd67cbc7deca35f8456827d4` |
| Parent | `463c8957bd51774251197c59cd64340910a6d88d` |
| Changed-file Git blob | `c2428c3f752bc301ca494fff77a5bb0dc2642d66` |
| Artifact SHA-256 | `455704959c14de41f015661b14ce68ce48ee75013657078f7739ce41406dc607` |
| Canonical payload length | 1359 bytes |
| Canonical payload SHA-256 | `5c321c1c9c21dc95bf54f6a7ca06e52cc70729890683daae56dbc7c2bce8dc94` |
| Candidate-coordinate records | exactly 14 |
| Determinations | exactly one indivisible determination |
| Partial terminal outcomes | none |
| Evidence-path reclassification | none |
| Requirement assessment | none |
| Requirement result | none |
| Later independent review | required |

Engineering[181] determined:

> mapping package not constructible and selected relationships remain unresolved

The determination was not treated as accepted merely because its source identities and mechanical properties matched.

Its architectural reasoning was independently reviewed.

## 9. Governing Protocol Action Boundary

The published Protocol Action model requires:

> attempts(X, candidateA)  
> `!=` Protocol Action occurrence

> admittedForEvaluation(candidateA)  
> `->` instantiates(candidateA, A)

> instantiates(candidateA, A)  
> `->` one bounded Protocol Action occurrence exists

A complete I164 mapping therefore requires:

> completeActionMapping  
> `=` stableActionIdentity  
> `+` exactAdmissionBoundary  
> `+` repeatedPresentationRule

Operational equality cannot silently supply formal occurrence identity.

The independent review therefore required a positive I164 declaration or construction rule for all three relationships.

No such complete declaration or construction rule exists in I164.

## 10. Fixed I164 Candidate Sequence

The independently reconstructed I164 candidate sequence is:

1. local input normalization;
2. local Merkle-path normalization;
3. action-local nullifier derivation;
4. proof generation;
5. local proof verification;
6. UI proof and public-signal normalization;
7. UI used-state pre-check;
8. optional verifier preflight;
9. UI relay-request construction;
10. relay request receipt;
11. payload-shape validation;
12. relay public-signal coherence validation;
13. freshness observation;
14. relay used-state observation;
15. fixed-zero compatibility-field addition;
16. frozen relay-submission construction;
17. TEMPEST seed construction;
18. deterministic slot permutation;
19. domain selection;
20. transport attempt;
21. permitted fallback attempt;
22. uncertain-outcome reconciliation;
23. contract invocation and entry;
24. petition-existence check;
25. nullifier-unused check;
26. verifier call;
27. contract public-signal coherence checks;
28. used-state mutation;
29. event emission;
30. transaction or reconciliation result;
31. relay response;
32. UI outcome;
33. normalized event observation;
34. idempotent persistence;
35. application read-model projection.

This is exact operational evidence.

It does not itself select the formal Protocol Action occurrence or admission boundary.

Downstream observation may occur asynchronously relative to the response path. That scheduling fact does not provide occurrence identity or retry equivalence.

## 11. Candidate Source-Identity Review

Every Engineering[181] candidate record matched the exact I164 tracked path, Git blob and SHA-256 below.

| Candidate | Exact I164 source identity |
|---|---|
| `CAND-A01` | `frontend/src/hooks/useZKProof.js` — `985e8adb8410a134fa010d2fa49ee179e47edfb5` — `8df56093b0a5a3ed8121e3cbe45761d0cfc967bc0fcdd108222944f5901a575a`; `frontend/src/components/M2SignButton.jsx` — `42d27697f8ee796210f649257c94247220728f99` — `16faf8dba309411ebc40ae00c66cbfda4b2e32e48c18b46d422bcffc7c1e96f2` |
| `CAND-A02` | `zk/v3-groth16/circuits/sign_petition.circom` — `165ed8cfa1029dd0a937ab6e885af020fbf991e5` — `a64783f8873df0c9dda7f7e44607e076f0b2af94c9cd609e4619e4b0fbcf2e02`; `frontend/src/hooks/useZKProof.js` — `985e8adb8410a134fa010d2fa49ee179e47edfb5` — `8df56093b0a5a3ed8121e3cbe45761d0cfc967bc0fcdd108222944f5901a575a` |
| `CAND-A03` | `frontend/src/components/M2SignButton.jsx` — `42d27697f8ee796210f649257c94247220728f99` — `16faf8dba309411ebc40ae00c66cbfda4b2e32e48c18b46d422bcffc7c1e96f2` |
| `CAND-A04` | `backend/src/routes/relay.js` — `23a4d5f37a5dafa2cfd39030e1d42bff9807e3e7` — `1f748b519358c4d4653dfce5d13d6f54cab4a3cd7cb70d8f1937a75a06990f7a` |
| `CAND-A05` | `backend/src/services/relayExecution.js` — `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` — `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` |
| `CAND-A06` | `backend/src/services/relayExecution.js` — `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` — `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` |
| `CAND-A07` | `contracts/src/PetitionRegistry.sol` — `a593c4023fc1ce9c835013a5ad40a310e5bfd032` — `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` |
| `CAND-A08` | `contracts/src/PetitionRegistry.sol` — `a593c4023fc1ce9c835013a5ad40a310e5bfd032` — `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26`; `contracts/src/v3/Groth16Verifier.sol` — `bf3bd28b1e89e8672219aa5aea6e54605d1b5bfe` — `b1216366353f3dbf478e1e03add31077bbe4bc76d5a4e40aaba574cd5841bd87` |
| `CAND-A09` | `contracts/src/PetitionRegistry.sol` — `a593c4023fc1ce9c835013a5ad40a310e5bfd032` — `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` |
| `CAND-A10` | `backend/src/services/relayExecution.js` — `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` — `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` |
| `CAND-A11` | `backend/src/services/relayExecution.js` — `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` — `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` |
| `CAND-A12` | `contracts/src/PetitionRegistry.sol` — `a593c4023fc1ce9c835013a5ad40a310e5bfd032` — `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26`; `backend/src/indexer/petitions/processor.js` — `b38e89799c61a846025390325f882c2a69ce9759` — `addfa0e87da3c1a94628d30024556fa9ba644df46c78fb27caac7529e18b3437` |
| `CAND-A13` | `backend/src/indexer/petitions/handlers.js` — `4912bfe988996712f700b1506171f6a8e46ba75e` — `f2f7fab14b9c5c310e823c6c8df8556b894792659dc158658ab9289b69ccdcd7`; `backend/src/db/repositories/petitions.js` — `5b65178963e1b9f85100c7f8238de4b69737aabe` — `68076c4b5bbd0aa1efc5a5454c180bf9b990af118fda5fc5dc67169babbf828b`; `backend/migrations/001_ground_truth_indexer_v0.sql` — `14b61bd874fe48a2957efa73923c5467dc7ccca4` — `8f3c0a70b0a5923efbdffd324a0b1c96e202d40217dcd11ba90a2ec78606d31e` |
| `CAND-A14` | `backend/src/routes/relay.js` — `23a4d5f37a5dafa2cfd39030e1d42bff9807e3e7` — `1f748b519358c4d4653dfce5d13d6f54cab4a3cd7cb70d8f1937a75a06990f7a`; `frontend/src/components/M2SignButton.jsx` — `42d27697f8ee796210f649257c94247220728f99` — `16faf8dba309411ebc40ae00c66cbfda4b2e32e48c18b46d422bcffc7c1e96f2` |

Source-identity agreement was necessary but not sufficient for acceptance.

Each candidate’s semantic role was independently examined.

## 12. Complete Candidate Determination Review

| Candidate | Exact role | Action-identity review | Admission review | Repeated-presentation review | Independent result |
|---|---|---|---|---|---|
| `CAND-A01` | local construction and proof generation through `generateProof` and `handleM2Sign` | local invocation state is not stable `id(A)` | construction and local verification precede the unresolved authoritative boundary | repeated construction has no formal equality rule | Engineering[181] correct |
| `CAND-A02` | proof relation, proof material and ordered `[nullifier, petitionId/actionId, membershipRoot]` values | proof or public-value identity is not Action identity | proof construction does not instantiate an admitted Action | equal public values or proof material do not establish equal occurrences | Engineering[181] correct |
| `CAND-A03` | serialized UI relay request | request identity is absent and request existence is not Action identity | HTTP submission is transport only | repeated requests remain formally unclassified | Engineering[181] correct |
| `CAND-A04` | relay payload validation, coherence checks, freshness and used-state observation | route fields do not establish `id(A)` | no validation-success point is declared as authoritative admission | already-used handling establishes only operational state | Engineering[181] correct |
| `CAND-A05` | frozen submission and deterministic TEMPEST seed | frozen payload and seed identify operational representation only | freezing and hashing precede execution presentation | equal seed means equal encoded payload, not equal Action occurrence | Engineering[181] correct |
| `CAND-A06` | deterministic slot selection, domain selection and fallback | slot, domain and attempt coordinates are operational | delivery attempt is not admission | one frozen dispatch is operational continuity only | Engineering[181] correct |
| `CAND-A07` | ABI-decoded `signPetitionWithZKProof` invocation and contract entry | calldata and invocation do not declare stable Action identity | contract entry is the strongest candidate presentation but is not declared as admission | operationally distinct invocations have no formal same-or-distinct rule | Engineering[181] correct |
| `CAND-A08` | petition, used-state, verifier and public-signal checks | checks evaluate representations rather than identify the occurrence | no intermediate check is declared as the complete authoritative admission boundary | used-state separates unused from used, not same Action from distinct Action | Engineering[181] correct |
| `CAND-A09` | `(petitionId/actionId, nullifier)` uniqueness state and mutation | strongest stable uniqueness coordinate, but not declared `id(A)` | mutation follows checks and does not define their Evaluation start | later equal-key use is already used; occurrence equivalence remains unresolved | Engineering[181] correct |
| `CAND-A10` | returned transaction hash and possible chain-level replacement context | transaction identity is not Action identity | submission or transaction result is not admission | I164 declares no replacement-continuity rule | Engineering[181] correct |
| `CAND-A11` | reconciliation after controlled or transport failure | observed used state cannot identify the causative presentation | reconciliation occurs after uncertain execution | current attempt, fallback and earlier presentation cannot be distinguished formally | Engineering[181] correct |
| `CAND-A12` | `PetitionSigned` and normalized block, transaction and log observation | event coordinates identify an observation, not every Action candidate | event follows mutation | one successful event omits failed and refused presentations | Engineering[181] correct |
| `CAND-A13` | idempotent persistence and derived application count | database keys identify stored observations | persistence is downstream | storage uniqueness is observation idempotence, not Action equivalence | Engineering[181] correct |
| `CAND-A14` | `{ok, alreadySigned, txHash?}` and UI outcome | response has no stable Action coordinate | response follows pre-check, execution or reconciliation | similar outcomes can arise from distinct operational paths | Engineering[181] correct |

For every candidate, the review also verified:

- exact symbols or serialized shape;
- lifecycle position;
- evidence classes;
- construction, transport, enforcement, execution, mutation or observation role;
- claimed Action-identity status;
- claimed Action-admission status;
- repeated-presentation status;
- explicit non-mappings;
- limitations;
- privacy boundary;
- and conclusion.

No candidate was accepted or rejected merely because its name resembled a formal protocol subject.

## 13. Stable Positive Action-Identity Review

The review independently examined:

- local invocation state;
- proof identity;
- ordered public values;
- `(petitionId/actionId, nullifier)`;
- frozen relay submission;
- TEMPEST seed;
- slot and domain;
- contract calldata;
- contract invocation;
- transaction hash;
- transaction replacement;
- state mutation;
- event coordinates;
- normalized observation;
- database keys;
- and response identity.

The exact distinctions are:

| Identity class | I164 evidence | Relationship to `id(A)` |
|---|---|---|
| Private Actor identity | intentionally unavailable | must remain distinct |
| nullifier identity | action-local public uniqueness value | not Action-occurrence identity |
| proof identity | proof representation | not Action-occurrence identity |
| request identity | no stable declared request identifier | not Action-occurrence identity |
| transaction identity | transaction hash or replacement context | not Action-occurrence identity |
| event identity | block, transaction and log coordinates | observation identity only |
| state identity | `(petitionId/actionId, nullifier)` used-state key | uniqueness-state identity only |
| persistence identity | `(tx_hash, log_index)` and `(petition_id, nullifier)` | stored-observation identity only |
| application identity | petition and UI/read-model representations | application meaning only |
| Protocol Action occurrence identity | required positive formal coordinate | absent from I164 |

No candidate supplies:

- an exact `id(A)` construction function;
- a declared creation point;
- lifecycle preservation as one Action occurrence;
- or a complete equality rule.

Engineering[181] correctly refused to manufacture `id(A)` from operational equality.

Independent determination:

> `U-ACTION-IDENTITY` remains unresolved.

## 14. Action-Admission Boundary Review

Every plausible I164 admission candidate was independently examined:

| Candidate boundary | Independent determination |
|---|---|
| successful candidate construction | local preparation only |
| successful local proof verification | local preflight only |
| UI request creation | application transport representation |
| relay request receipt | transport receipt |
| payload validation | syntactic validation only |
| relay public-signal coherence | bounded representation check |
| freshness gating | operational availability check |
| relay used-state check | operational state pre-check |
| frozen submission | operational preservation |
| TEMPEST dispatch | transport selection |
| transaction submission | execution attempt |
| contract entry | candidate enforcement presentation, not declared admission |
| petition-existence success | one partial guard |
| nullifier-unused success | one partial state guard |
| proof-verification success | one bounded Evaluation component |
| contract public-signal coherence | one bounded component |
| state mutation | downstream of the checks it cannot retroactively begin |
| event emission | downstream observation source |
| transaction result | operational result |
| reconciliation | uncertain-outcome observation |
| relay response | downstream operational response |
| persistence | downstream projection |

No exact source operation declares:

> admittedForEvaluation(candidateA)  
> `->` instantiates(candidateA, A)

Contract entry is not automatically admission.

Validation success is not automatically admission.

Proof-verification success is not complete admission or complete Evaluation.

Mutation cannot silently become the earlier admission boundary.

The fixed-zero `admissionCommitment` is a deprecated compatibility field, is ignored by the selected contract path and lies outside the ordered public-input set.

It is not:

- Action admission;
- admission identity;
- Action identity;
- or occurrence identity.

Independent determination:

> `U-ACTION-ADMISSION` remains unresolved.

## 15. Repeated-Presentation and Retry Review

| Case | Exact I164 classification | Formal occurrence conclusion |
|---|---|---|
| repeated UI submission after local success | UI disabling or already-signed presentation | application control only |
| repeated UI construction before authoritative state visibility | another proof and request may be constructed | same-versus-distinct Action unresolved |
| repeated relay request after used state becomes visible | `{ok:true, alreadySigned:true}` | used-state equality only |
| repeated relay request before used state becomes visible | another deterministic dispatch may begin | concurrent operational presentation |
| deterministic fallback attempt | same frozen submission uses the next permitted slot/domain | operational continuity only |
| transaction replacement | no selected-path replacement rule | unresolved |
| replayed contract invocation after mutation | nullifier-used guard reverts | repeated used-key presentation only |
| concurrent invocations before ordering resolves | at most one successful used-state mutation | state uniqueness only |
| reconciliation after uncertain transport | `hasSignedPetition` observation may produce `{txHash:null}` | causative presentation cannot be identified |
| later event or indexer observation | one successful mutation is observed and persisted | observation continuity only |

I164 establishes:

> same frozen submission within one dispatch call  
> `->` preserved operational payload

I164 does not establish:

> same frozen submission  
> `->` same Protocol Action occurrence

I164 also does not establish:

> different request, proof, seed, attempt or transaction  
> `->` different Protocol Action occurrence

The review found no exact formal occurrence rule derived solely from:

- payload equality;
- proof equality;
- seed equality;
- used-state equality;
- transaction equality;
- event equality;
- persistence equality;
- or response equality.

Independent determination:

> `U-RETRY` remains unresolved.

## 16. Engineering[178]-Accepted Relationship Review

Engineering[181] relied on exactly the following Engineering[178]-accepted relationships.

| Record | Exact treatment and affected rows | Exact components | Preserved relationship, non-mapping and dependency |
|---|---|---|---|
| `I164-SR-002` | Proposed supported relationship; `PE-SUBJ-001`, `006`, `007`, `008`, `009` | `C-CIRCUIT`, `C-VERIFY`, `C-CONTRACT-PRESENTATION`, `O-REQUEST`, `O-DISPATCH` | Ordered public values preserve order and roles only; they are not actor, admission or occurrence identity; accepted-root status, complete Action identity and complete Evaluation remain unestablished |
| `I164-SR-003` | Supported component plus unresolved complete relationship; `PE-SUBJ-001`, `002`, `004`, `006`, `007`, `008`, `009`, `010` | `B-SURFACE`, `B-LAYER`, `C-CLIENT-PRESENTATION`, `O-REQUEST`, `O-DISPATCH`, `C-CONTRACT-PRESENTATION` | Proof submission, frozen submission and contract invocation are exact components; no stable `id(A)`, admission boundary or retry rule; `U-ACTION-IDENTITY`, `U-ACTION-ADMISSION`, `U-RETRY`, `U-RULESET` and A02–A05 remain unresolved |
| `I164-SR-004` | Supported component plus unresolved complete relationship; `PE-SUBJ-001`, `002`, `003`, `006`, `007`, `008`, `009` | `C-CIRCUIT`, `C-VERIFY`, `C-CONTRACT-PRESENTATION`, `O-REQUEST`, `O-RECONCILE`, `C-EVENT`, `O-NORMALIZE`, `O-PERSIST` | Candidate checks are components only; proof verification is not complete Evaluation; downstream outcomes are not Determination; all Evaluation and Determination dependencies remain unresolved |
| `I164-SR-006` | Supported component plus unresolved complete relationship; `PE-SUBJ-001`, `002`, `005`, `006`, `007`, `008`, `009`, `010` | `C-PUBLIC-STATE`, `C-EVENT`, `O-NORMALIZE`, `O-PERSIST` | Mutation, event, normalized observation and persistence are exact components; no stable `id(T)` or `id(U)` exists; A10–A17, `U-DETERMINATION` and `U-CLASSIFICATION` remain unresolved |
| `I164-SR-011` | Proposed supported relationship; `PE-SUBJ-001`, `006`, `007`, `008`, `009` | `B-SURFACE`, `B-LAYER`, `C-CLIENT-PRESENTATION`, `A-READMODEL`, `A-SCHEMA` | Shared `petitionId/actionId` preserves distinct protocol-context and application-target roles; application meaning does not define Action identity; A20 remains unresolved |
| `I164-SR-012` | Explicit proposed non-mapping; `PE-SUBJ-001`, `002`, `003`, `005`, `006`, `007`, `008`, `009` | `O-REQUEST`, `O-DISPATCH`, `O-RECONCILE`, `C-EVENT`, `O-NORMALIZE`, `O-PERSIST`, `A-READMODEL` | Operational and downstream representations are not formal occurrences; payload preservation does not settle retry equivalence; `U-RETRY`, `U-ACTION-IDENTITY`, `U-DETERMINATION`, A05, A07, A11, A16 and A20 remain unresolved |
| `I164-SR-013` | Supported component plus unresolved complete relationship; `PE-SUBJ-001` through `009` | every component and representation in the accepted declaration’s Sections 11 and 12 | Exact syntax and storage do not create semantic identity; no stable `id(A)`, `id(E)`, `id(D)` or `id(U)` exists; `U-ACTION-IDENTITY`, `U-EVAL-IDENTITY`, `U-DETERMINATION` and A11 remain unresolved |
| `I164-SR-014` | Explicit proposed non-mapping; `PE-SUBJ-001`, `006`, `007`, `008`, `009`, `010` | `B-SURFACE`, `B-LAYER` and every accepted implementation component identifier | No I164 label becomes a new protocol subject; ontology remains governed solely by the published protocol generation |

For all eight records, Engineering[181] preserved:

- exact treatment;
- affected A01 rows;
- implementation anchors;
- representation;
- occurrence boundary;
- continuity or identity rule;
- explicit non-mappings;
- evidence dependencies;
- limitations;
- privacy boundary;
- and Engineering[178]-accepted status.

No accepted limitation or unresolved dependency was removed.

## 17. Preserved Non-Mappings

The following remain exact:

> candidate construction  
> `!=` Protocol Action occurrence

> UI request  
> `!=` Protocol Action occurrence

> relay request  
> `!=` Protocol Action occurrence

> transport attempt  
> `!=` Protocol Action occurrence

> transaction  
> `!=` automatically Protocol Action occurrence

> event  
> `!=` Protocol Action occurrence

> database row  
> `!=` Protocol Action occurrence

> proof verification  
> `!=` complete Protocol Action Evaluation

> response or downstream record  
> `!=` Protocol Action Determination

> execution attempt  
> `!=` Protocol State Transition occurrence

> application object  
> `!=` protocol subject

These non-mappings prevent unsupported substitution.

They do not construct the missing positive mapping.

## 18. Implementation Coordinate and Public Values

The implementation-owner coordinate remains:

`T-I164-ANONYMOUS-PUBLIC-ACTION`

It remains:

- an implementation-owner coordinate only;
- not a protocol subject;
- not Protocol Action identity;
- not Private Actor identity;
- not Protocol Operation identity;
- not Evaluation identity;
- not Determination identity;
- not Transition identity;
- and not State Transition identity.

The ordered public values remain:

1. `nullifier`;
2. `petitionId` or `actionId`;
3. `membershipRoot`.

They remain public protocol-facing roles only.

They are not:

- actor identity;
- wallet identity;
- sponsor identity;
- funding identity;
- admission identity;
- transport identity;
- ownership identity;
- application identity;
- reusable participant identity;
- cross-action identity;
- or formal occurrence identity.

## 19. Indivisibility Review

The selected mapping package requires:

> completeActionMapping  
> `=` stableActionIdentity  
> `+` exactAdmissionBoundary  
> `+` repeatedPresentationRule

The independently reviewed state is:

> stableActionIdentity = unresolved  
> exactAdmissionBoundary = unresolved  
> repeatedPresentationRule = unresolved

Therefore:

> completeActionMapping = not constructible

Supported components cannot produce a partial terminal outcome.

Engineering[181] correctly produced exactly one indivisible determination.

Engineering[182] correspondingly produces exactly one indivisible review result.

## 20. A01 Treatment Without Reclassification

| Identifier | Engineering[180] state | Engineering[182] treatment |
|---|---|---|
| `PE-SUBJ-001` | still-ambiguous | unchanged |
| `PE-SUBJ-002` | still-ambiguous | unchanged |
| `PE-SUBJ-003` | still-ambiguous | unchanged |
| `PE-SUBJ-004` | still-ambiguous | unchanged |
| `PE-SUBJ-005` | still-ambiguous | unchanged |
| `PE-SUBJ-006` | still-ambiguous | unchanged |
| `PE-SUBJ-007` | still-ambiguous | unchanged |
| `PE-SUBJ-008` | still-ambiguous | unchanged |
| `PE-SUBJ-009` | still-ambiguous | unchanged |
| `PE-SUBJ-010` | bounded | unchanged |

Engineering[182] changes no row state.

The reviewed-current totals remain:

`217 bounded / 268 still-ambiguous / 0 missing-evidence-path / 244 not-required`.

Only a later separate evidence-path reclassification determination may alter these states or totals.

## 21. Preserved Unresolved Relationships and Ambiguity Groups

The selected relationships remain unresolved:

- `U-ACTION-IDENTITY`;
- `U-ACTION-ADMISSION`;
- `U-RETRY`.

Engineering[182] resolves none of the following outside relationships:

- `U-RULESET`;
- `U-ROOT`;
- `U-EVAL-IDENTITY`;
- `U-EVAL-BOUNDARY`;
- `U-EVAL-REJECTION`;
- `U-DETERMINATION`;
- `U-CLASSIFICATION`;
- `U-PRIVACY-REVIEW`;
- `U-PROVENANCE`.

The following ambiguity groups remain outside this review:

- A02;
- A03;
- A04;
- A05;
- A06;
- A07;
- A08;
- A10;
- A11;
- A15;
- A17;
- A20.

All seven permitted-choice rows remain unchanged.

## 22. Minimum Later Evidence Review

Engineering[181] correctly established that revisiting the selected question requires a bounded implementation-owned package containing:

1. an exact public action-local occurrence coordinate;
2. its construction inputs and creation point;
3. an equality rule identifying exactly one Protocol Action occurrence;
4. explicit separation from actor, nullifier, proof, request, transaction, event, state, persistence and application identities;
5. an exact admission operation;
6. the candidate state immediately before admission;
7. the complete conditions required at admission;
8. the relationship between admission, later Evaluation, pre-evaluation refusal, Evaluation failure and rejection;
9. exhaustive repeated-presentation, retry, fallback, replacement, replay, concurrency, used-state and reconciliation rules;
10. lifecycle preservation across implementation representations;
11. privacy evidence preventing actor, wallet, sponsor, funding, admission, transport, ownership, metadata and cross-action linkage;
12. exact implementation-owned source or governance anchors;
13. and later independent review before acceptance.

This later evidence must declare the missing mapping.

It must not obtain apparent completeness by renaming an existing operational coordinate.

Engineering[182] neither designs that future mapping nor invents future implementation behaviour.

## 23. Privacy Review

The governing invariant remains:

> Private actors, public actions.

Engineering[181] introduces no:

- actor identification;
- wallet linkage;
- sponsor linkage;
- funding linkage;
- admission linkage;
- transport attribution;
- ownership attribution;
- cross-action correlation;
- metadata linkage;
- topology-to-actor mapping;
- reusable participant identity;
- or actor reconstruction.

Its candidate identifiers identify public review material only.

They do not identify a Private Actor or create reusable protocol identity.

Engineering[182] preserves the same boundary.

## 24. Evidence-Layer Separation

The following distinctions remain mandatory:

> candidate component  
> `!=` formal mapping

> formal mapping  
> `!=` accepted mapping evidence

> accepted mapping evidence  
> `!=` evidence-path boundedness

> evidence-path boundedness  
> `!=` evidence availability

> evidence availability  
> `!=` evidence sufficiency

> evidence sufficiency  
> `!=` requirement assessment

> requirement assessment  
> `!=` requirement result

Engineering[182] accepts Engineering[181] only as mapping-determination evidence.

It does not perform evidence-path reclassification or requirement assessment.

## 25. Review Findings

The independent review found:

1. Engineering[181] examined exactly 14 valid I164 candidate-coordinate records.
2. Their tracked paths, Git blobs, SHA-256 identities, symbols and serialized shapes match I164.
3. No examined coordinate supplies stable positive Protocol Action occurrence identity.
4. `(petitionId/actionId, nullifier)` supplies authoritative uniqueness-state equality only.
5. No I164 operation declares the exact candidate-to-Action admission relationship.
6. Contract entry is an enforcement presentation, not a declared admission boundary.
7. Proof verification is a bounded component, not complete Evaluation or admission.
8. Mutation, event emission, persistence and response occur too late to define the missing admission boundary.
9. I164 defines operational fallback and reconciliation without defining formal occurrence equivalence.
10. Payload, proof, seed, state, transaction, event, persistence and response equality remain insufficient.
11. Engineering[181] preserves all relevant Engineering[178]-accepted limitations, dependencies and non-mappings.
12. All non-selected relationships, ambiguity groups and row states remain unchanged.
13. The minimum later-evidence package is complete and does not redesign the missing mapping.
14. Privacy and evidence-layer boundaries are preserved.
15. No material defect exists in Engineering[181].

## 26. Canonical Final Review Result

The canonical final-review payload is the exact UTF-8 byte sequence between the marker lines below, joined by LF characters with no trailing LF:

canonical-final-review-payload-begin
format=PRIVACY-ENGINE-I164-ACTION-OCCURRENCE-MAPPING-DETERMINATION-INDEPENDENT-REVIEW/1
review-id=PE-I164-ACTION-OCCURRENCE-IDENTITY-ADMISSION-REPEATED-PRESENTATION-MAPPING-DETERMINATION-INDEPENDENT-REVIEW-2026-08-23
engineering-slice=engineering-182
reviewed-determination=engineering-181
reviewed-determination-sha256=455704959c14de41f015661b14ce68ce48ee75013657078f7739ce41406dc607
reviewed-canonical-payload-length=1359
reviewed-canonical-payload-sha256=5c321c1c9c21dc95bf54f6a7ca06e52cc70729890683daae56dbc7c2bce8dc94
fixed-implementation-baseline=I164
selected-question=Protocol Action occurrence identity, Action admission and repeated-presentation mapping
selected-relationships=U-ACTION-IDENTITY,U-ACTION-ADMISSION,U-RETRY
reviewed-candidate-coordinate-count=14
mapping-package-constructible=no
u-action-identity=unresolved
u-action-admission=unresolved
u-retry=unresolved
reviewed-determination-result=accepted
accepted-mapping-determination-evidence=engineering-181
pe-subj-010-state=bounded
reviewed-current-evidence-path-basis=engineering-179
reviewed-current-totals=217/268/0/244
evidence-path-reclassification-performed=no
requirement-assessment-performed=no
requirement-result-produced=no
implementation-defect-determined=no
privacy-boundary=Private actors, public actions
final-result=accepted
canonical-final-review-payload-end

Canonical final-review payload length:

`1310` bytes

Canonical final-review payload SHA-256:

`10f72073045200450308621d71f2bb98a5ffe2fb4fd8d1989eca2409e0de9322`

This is exactly one indivisible final review result:

> accepted

## 27. Accepted Effect

Engineering[182] establishes only:

- Engineering[181] as accepted mapping-determination evidence;
- the selected mapping package as not constructible from I164;
- `U-ACTION-IDENTITY` remaining unresolved;
- `U-ACTION-ADMISSION` remaining unresolved;
- `U-RETRY` remaining unresolved;
- exact supported implementation components remaining available as bounded evidence;
- all accepted explicit non-mappings remaining preserved;
- no A01 reclassification;
- `PE-SUBJ-010` remaining bounded;
- Engineering[179] remaining the reviewed-current evidence-path basis;
- reviewed-current totals remaining `217 / 268 / 0 / 244`;
- no requirement assessment;
- no requirement result;
- and no implementation-defect determination.

Engineering[182] does not modify Engineering[181] or any earlier artifact.

## 28. Explicit Exclusions

Engineering[182] does not:

- modify STATE.md;
- modify Engineering[181];
- modify Engineering[179] or Engineering[180];
- modify the corrected declaration;
- modify Engineering[177] or Engineering[178];
- modify the published specification;
- modify the Publication Record;
- modify Profile V2;
- modify Engineering[166] through Engineering[181];
- rewrite an earlier tag;
- modify I164;
- modify an implementation file;
- create partial acceptance;
- perform evidence-path reclassification;
- change `PE-SUBJ-010` from bounded;
- change the `217 / 268 / 0 / 244` totals;
- infer Protocol Action identity from an operational or downstream coordinate;
- infer Action admission from validation, dispatch, invocation, verification, mutation, event, response or persistence;
- infer retry equivalence from operational equality;
- resolve Evaluation, Determination, Transition or State Transition identity;
- resolve an inherited relationship outside the selected question;
- resolve a non-selected ambiguity group;
- resolve a permitted-choice row;
- perform requirement-level assessment;
- produce a requirement result;
- determine an implementation defect;
- perform a security assessment;
- determine compatibility, conformance, certification or operational readiness;
- designate a Reference Implementation;
- create Profile V3;
- create a protocol generation;
- create a publication occurrence;
- merge later implementation code;
- generate or replace cryptographic artifacts;
- alter a manifest;
- create deployment or runtime evidence;
- encode actor identity or provenance;
- or imply that Speak-up-appV3 defines or owns the Privacy Engine.

## 29. Final Review Result

Engineering[181] correctly determined that I164 does not provide:

- a stable positive identity for one Protocol Action occurrence;
- an exact authoritative admission boundary;
- or a complete repeated-presentation and retry-equivalence rule.

No request, proof, payload, seed, slot, domain, invocation, transaction, state item, event, database row, response, application object or convenient name may substitute for those missing relationships.

Accordingly:

- the mapping package remains not constructible from I164;
- `U-ACTION-IDENTITY` remains unresolved;
- `U-ACTION-ADMISSION` remains unresolved;
- `U-RETRY` remains unresolved;
- `PE-SUBJ-010` remains bounded;
- no A01 row is reclassified;
- Engineering[179] remains the reviewed-current evidence-path basis;
- reviewed-current totals remain `217 / 268 / 0 / 244`;
- no requirement assessment is performed;
- no requirement result is produced;
- and no implementation defect is determined.

Final review result:

**accepted**
