# Privacy Engine I164 Protocol Action, Rule Evaluation, Determination, and Classification Mapping Declaration V1

## 1. Declaration Status and Purpose

This document is an implementation-owner mapping declaration package.

Its status is:

> draft

It does not claim acceptance.

No implementation-governance acceptance occurrence exists for this declaration.

A later bounded slice may verify the immutable digest of this draft, review every mapping and non-mapping, and create a separate acceptance occurrence if and only if implementation governance accepts it.

Protocol authority always remains with the published Privacy Engine protocol generation.

STATE.md remains the single canonical development authority.

This declaration records relationships about the fixed engineering-164 implementation baseline. It does not modify that baseline, prove runtime behaviour, assess evidence sufficiency, or produce a requirement result.

## 2. Declaration Identity

| Field | Declared value |
|---|---|
| Declaration identifier | `PE-I164-ACTION-EVALUATION-DETERMINATION-CLASSIFICATION-MAPPING-DECLARATION-V1` |
| Declaration title | Privacy Engine I164 Protocol Action, Rule Evaluation, Determination, and Classification Mapping Declaration V1 |
| Declaration version | `1` |
| Declaration status | `draft` |
| Package-format version | `PE-I164-IMPLEMENTATION-OWNER-MAPPING/1` |
| Declaration scope | Engineering[167] ambiguity groups A04–A08 only |
| Scope rows | 88 |
| Declaration authority | Speak-up-appV3 implementation-governance boundary |
| Acceptance required | yes |
| Acceptance occurrence | none |
| Protocol authority | Published Privacy Engine protocol generation |
| Development authority | `STATE.md` |
| Fixed repository | Speak-up-appV3 |
| Fixed baseline tag | `engineering-164` |
| Fixed baseline commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Fixed baseline tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |
| Implementation archive SHA-256 | `7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847` |
| Ordered A04–A08 source-row serialization SHA-256 | `91b2d8acca57a395b738b18001a3e47b9f4c15f382a4c0bb6124bf1ac46f494d` |
| Private Actor identity encoded | no |
| Requirement assessment performed | no |
| Requirement result produced | no |
| Reference Implementation designation | no |

The declaration digest is intentionally not self-embedded. The SHA-256 emitted after file creation is the immutable digest that a later acceptance-review slice must verify.

## 3. Guarded Formal Corpus

| Artifact | SHA-256 |
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
| `docs/PRIVACY_ENGINE_IMPLEMENTATION_BASELINE_EVIDENCE_INVENTORY_AND_ASSESSMENT_COVERAGE_MAP_V1.md` | `46294d6e4dc2928409713bad32e510ee2c1749d39fdc0ed27ae70b1219f88175` |
| `docs/PRIVACY_ENGINE_IMPLEMENTATION_EVIDENCE_PATH_AMBIGUITY_RESOLUTION_DETERMINATION_V1.md` | `bdea6dc1f2b9af176de9e354daf654a3c4a8b1eb4bd46c16d1ff0ea3fbfc5cd2` |
| `docs/PRIVACY_ENGINE_FIXED_BASELINE_IMPLEMENTATION_EVIDENCE_DECLARATION_AUTHORITY_AND_CONSTRUCTION_BOUNDARY_V1.md` | `1280eb90b97f9caa21456f8ce8ce58f6211b5ef360d8d2637110a43c4f00e7f2` |

The supplied formal-corpus archive is `privacy-engine-formal-corpus.zip`.

Its SHA-256 is:

`4e5b15835063318a1982090b598937138b10147d217c618ea89cbfb5cf0fbf4b`

The archive contains 88 files. Its compressed-data integrity and archive-to-local guarded content were verified before this document was constructed.

## 4. Fixed Implementation Baseline

| Baseline field | Verified value |
|---|---|
| Repository | Speak-up-appV3 |
| Tag | `engineering-164` |
| Commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Git tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |
| Implementation archive | `implementation-baseline-engineering-164.zip` |
| Implementation archive SHA-256 | `7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847` |
| Embedded archive commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Tracked paths | 308 |
| Blob paths | 305 |
| Gitlink paths | 3 |
| Reconstructed and resolved tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |

All 305 archived blob paths match the Engineering[166] path set, blob SHA-256 identities, and Git blob identities.

The three Gitlinks retain these identities:

| Path | Gitlink identity |
|---|---|
| `contracts/lib/forge-std` | `52c1e835e9ffcfe00bd9f8f51de204b93bc7028a` |
| `contracts/lib/openzeppelin-contracts` | `8ff78ffb6e78463f070eab59487b4ba30481b53c` |
| `contracts/lib/openzeppelin-contracts-upgradeable` | `b933412726bccd822a871116f1427111e649ff54` |

The baseline subject is exactly I164.

> declaration about I164  
> `!=` component of I164  
> `!=` modification of I164  
> `!=` proof of behaviour  
> `!=` requirement result

## 5. Profile and Coverage Preservation

The published Protocol Specification V1, Complete Implementation Profile V2, Engineering[166], and Engineering[167] each retain 729 ordered and uniquely identified rows.

Every Profile V2 row retains its exact:

- identifier;
- RF family;
- SF home;
- strength;
- published applicability;
- profile disposition;
- order;
- and complete profile-row SHA-256 identity.

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

Engineering[169] does not reclassify any row and does not claim that any A04–A08 row is now bounded.

## 6. Exact Declaration Scope

The scope is extracted only from explicit Engineering[167] ambiguity-group assignments.

| Group | Subject | Rows |
|---|---|---:|
| A04 | Validity rules and applicable rule sets | 25 |
| A05 | Protocol Action mapping | 17 |
| A06 | Protocol Action Evaluation mapping | 20 |
| A07 | Protocol Action Determination mapping | 14 |
| A08 | Acceptance and rejection classification mapping | 12 |
| **Total** |  | **88** |

No membership is inferred from a requirement name.

A01–A03 and A09–A22 remain outside declaration-group scope. Dependencies on those groups may be identified only as unresolved dependencies; they are not resolved or reclassified here.

## 7. Construction and Lifecycle Rules

The Engineering[168] construction rule is:

> explicit formal subject or requirement  
> `+` explicit relationship identity  
> `+` exact I164 material  
> `+` bounded assertion  
> `+` explicit non-mappings  
> `+` declared limitations  
> `+` evidence dependencies  
> `+` accepted declaration authority

Engineering[169] lacks the final term.

Therefore:

> complete proposed package  
> `!=` accepted declaration evidence

The preservation rule is:

> selected formal relationship M  
> `->` bind M to exact I164 evidence  
> `->` preserve M without substitution

If I164 cannot preserve M:

> M `->` unresolved

Forbidden:

> M `->` inferred M'

The lifecycle boundary is:

> draft declaration  
> `!=` accepted declaration  
> `!=` assessment evidence accepted for reliance  
> `!=` evidence sufficiency  
> `!=` requirement result

## 8. Proposed Action-Type and Public-Input Relationship

The bounded proposed action-type label used by this draft is:

`T-I164-ANONYMOUS-PUBLIC-ACTION`

It denotes the current-generation anonymous public-action presentation evidenced by the fixed circuit, proof, relay, and contract-call material.

This label:

- is an implementation-owner mapping coordinate only;
- does not create a new protocol subject;
- does not acquire protocol authority;
- does not import petition meaning into protocol identity;
- and is not accepted until a separate acceptance occurrence exists.

The exact proposed public-input set is:

1. `nullifier`;
2. `petitionId` or `actionId`;
3. `membershipRoot`.

The private witness set remains separate:

- `memberSecret`;
- `membershipPath`;
- `membershipIndices`.

The proof components remain separate:

- `pA`;
- `pB`;
- `pC`.

The fixed ABI also contains an ignored compatibility field whose active signing path supplies and emits only the fixed zero value. That field is not declared as a public input, Action identity, actor identity, or cross-action coordinate.

The action-context value is also consumed as an application-target key. Shared serialization does not merge:

> protocol action-context role  
> `!=` application-target identity  
> `!=` Protocol Action occurrence identity

## 9. Protocol Action Boundary Determination

Exact I164 material supports the following bounded statement:

- `PetitionRegistry.signPetitionWithZKProof` is the active on-chain candidate enforcement surface for the proposed action type.

Exact I164 material does not support declaration of the following without inference:

- the authoritative Protocol Action admission boundary;
- one stable Protocol Action occurrence identity;
- a representation preserving that occurrence across retries;
- or the rule determining whether repeated authoritative presentations are one occurrence or distinct occurrences.

The ABI-decoded contract invocation is an identifiable candidate boundary, but it cannot be declared authoritative because the complete applicable rule set and bounded evaluation context are not established as distinct inputs before the first candidate check.

Accordingly:

> UI intent `!=` Protocol Action  
> proof generation `!=` Protocol Action  
> relay request `!=` automatically Protocol Action  
> contract invocation `!=` automatically declared Protocol Action occurrence  
> retry `!=` automatically same or new Protocol Action  
> transaction `!=` Protocol Action identity  
> application target `!=` Protocol Action identity

The Action occurrence relationship remains unresolved under `U-ACTION-IDENTITY`, `U-ACTION-ADMISSION`, and `U-RETRY`.

## 10. Exact I164 Evidence Register

| Tracked path | Mode | Type | Git object | Blob SHA-256 |
|---|---|---|---|---|
| `STATE.md` | 100644 | blob | `5b774d901d58b4e04e2e09b575a5ad71fc4811f2` | `228886af0db33a801db40d834c1a1070ed8f330d6708d8e6674021e3a2d3be33` |
| `ZK_ARTIFACTS_MANIFEST.json` | 100644 | blob | `e7bd40673ccad23283182a27c129c240807287be` | `e048ca3b210a4d40c8ff722a8ec5e793e1f340965c2bc6867287bc4dedaec896` |
| `docs/PRIVACY_ENGINE_LAYER_INTERFACE_MAP_V1.md` | 100644 | blob | `0b5df10f963033b7e416a0d95e48f7bc687e61ef` | `90c4fb7a16da1d010bd9edd295dfd5dc1443d39a60b3fc673dba57aac83aaeb7` |
| `docs/ZK_ARTIFACT_PROVENANCE.md` | 100644 | blob | `a5482dae7c5c891b6b44d57481a9909d72acdc36` | `699d34953af2b8322e487d9cf0f20dc5b2d000064b275c656ba33bab621940df` |
| `docs/ZK_CIRCUIT_SPEC.md` | 100644 | blob | `983c0333f90dcfe988205f11f41ecbd114198b13` | `087a6e9aa40737ea75c06d689761f437d6434419aa5e26382f5b88e6fa614ae3` |
| `frontend/src/components/M2SignButton.jsx` | 100644 | blob | `42d27697f8ee796210f649257c94247220728f99` | `16faf8dba309411ebc40ae00c66cbfda4b2e32e48c18b46d422bcffc7c1e96f2` |
| `frontend/src/hooks/useZKProof.js` | 100644 | blob | `985e8adb8410a134fa010d2fa49ee179e47edfb5` | `8df56093b0a5a3ed8121e3cbe45761d0cfc967bc0fcdd108222944f5901a575a` |
| `frontend/src/m2Identity.js` | 100644 | blob | `42a0416dbfcfa61a37a2138f9ac3f497927b344f` | `3c019252a21925c4f6f4392b4ba1bdf442a6b02a32e17dd5916d89ef1f0dddcb` |
| `frontend/src/config.js` | 100644 | blob | `3facdc8697b1a1165892b3b791c75f8729ea15a2` | `165471f0585cdd3b62123bd99fd0c678e01097f65d8d6c4983f6ed4bbb82033f` |
| `frontend/public/zk/sign_petition.wasm` | 100644 | blob | `4b84713d0e324e8faa2c95123b43b3dbaaf6683a` | `996ad4bcf08548125ae15fbf98a9748170647d8609bdbade16003c3cd351dcb3` |
| `frontend/public/zk/sign_petition_final.zkey` | 100644 | blob | `88cc57d0b532a3531c53aa41d3afef9955a38bf1` | `762433cb44fc19ff7ebf575b71f56af75f17b161f87102517a6259086b9b99f1` |
| `frontend/public/zk/verification_key.json` | 100644 | blob | `ab18b9824d790427241e39a6d37fe94b37a599f3` | `8548836eaeb4500e19ca9032852095b257a9a5267206dd4e8180740c8841d14c` |
| `backend/src/routes/relay.js` | 100644 | blob | `23a4d5f37a5dafa2cfd39030e1d42bff9807e3e7` | `1f748b519358c4d4653dfce5d13d6f54cab4a3cd7cb70d8f1937a75a06990f7a` |
| `backend/src/services/relayExecution.js` | 100644 | blob | `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` | `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` |
| `backend/src/services/tempestConfig.js` | 100644 | blob | `3923ff0f3213dd7f1c1d14e1a8d37589d0f25d4f` | `ef1778d8c44568a42a3ac0118564f7d638c54ad9f3b3554dfa4d53fb9903622c` |
| `backend/src/services/tempestDomains.js` | 100644 | blob | `8b3fb406078f413ac1625ea283aecdee703cd5a3` | `b2254d48517d920f890ee683418c3a76e277f17fa549338ffaa05389af56ac78` |
| `backend/src/services/indexerFreshness.js` | 100644 | blob | `cdcf3077e0ab7f231b53726f8eb90bac1a76a0ef` | `66b870d2087ecef424019933e2aa90451244869a6c6929c5e7b595109fd4a794` |
| `backend/src/services/tempestExecution.test.js` | 100644 | blob | `ba2970c8bc858b575091b3fe2643cd6db3ef6e6a` | `d86b8c6237f692c2eeb3113928aa37e1a23c8712909bddc167cb1f85bd414d7f` |
| `backend/src/indexer/petitions/processor.js` | 100644 | blob | `b38e89799c61a846025390325f882c2a69ce9759` | `addfa0e87da3c1a94628d30024556fa9ba644df46c78fb27caac7529e18b3437` |
| `backend/src/indexer/petitions/handlers.js` | 100644 | blob | `4912bfe988996712f700b1506171f6a8e46ba75e` | `f2f7fab14b9c5c310e823c6c8df8556b894792659dc158658ab9289b69ccdcd7` |
| `backend/src/db/repositories/petitions.js` | 100644 | blob | `5b65178963e1b9f85100c7f8238de4b69737aabe` | `68076c4b5bbd0aa1efc5a5454c180bf9b990af118fda5fc5dc67169babbf828b` |
| `backend/migrations/001_ground_truth_indexer_v0.sql` | 100644 | blob | `14b61bd874fe48a2957efa73923c5467dc7ccca4` | `8f3c0a70b0a5923efbdffd324a0b1c96e202d40217dcd11ba90a2ec78606d31e` |
| `contracts/src/PetitionRegistry.sol` | 100644 | blob | `a593c4023fc1ce9c835013a5ad40a310e5bfd032` | `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` |
| `contracts/src/AnonymousMembershipRegistry.sol` | 100644 | blob | `31835a9feeeff6691335cca655b1f9e31ceba0d6` | `2b883cbca96f074c52d0471aaa62681ae042b8315d5e1260ab114541650c7978` |
| `contracts/src/interfaces/IAnonymousMembershipRegistry.sol` | 100644 | blob | `f794d82e238704e157fcbc4a90e79f37978edc91` | `2775e4d5e027e272ef5cea1f053a45dc7a4fd5e364d9bce427a9a65436825ea9` |
| `contracts/src/v3/Groth16Verifier.sol` | 100644 | blob | `bf3bd28b1e89e8672219aa5aea6e54605d1b5bfe` | `b1216366353f3dbf478e1e03add31077bbe4bc76d5a4e40aaba574cd5841bd87` |
| `contracts/script/UpgradePetitionRegistry.s.sol` | 100644 | blob | `b696299874b027aba2c7783d8ddeb5cd57658dc1` | `79db955bd2ace55e4e507293f561b4b2dac0591db4e80ac206afe4ce67836e05` |
| `contracts/verify-groth16-verifier.sh` | 100755 | blob | `55254ced62afe57e06a38079b05b833b3d23c4a8` | `d807e204efbff0120d6bffab005334a60f56f82568e13d0e11891bb5f6eb8bd9` |
| `contracts/test/AnonymousMembershipRegistry.t.sol` | 100644 | blob | `f2c6f2519935f9f8af482cbcc94a825496c7c7c4` | `438ecdf06f28dae8184514d04d9591d73bfc6862b8fd37aed819750e439fbc77` |
| `contracts/test/PetitionRegistry.SettlementReference.t.sol` | 100644 | blob | `793c4d3b746d4533d0efb33a2fb729c332f71268` | `689b7f302d502e9b51bbc111bc4cfd2a5f0b17b8d2a65448042e55ac42984b4f` |
| `zk/v3-groth16/circuits/sign_petition.circom` | 100644 | blob | `165ed8cfa1029dd0a937ab6e885af020fbf991e5` | `a64783f8873df0c9dda7f7e44607e076f0b2af94c9cd609e4619e4b0fbcf2e02` |
| `zk/v3-groth16/keys/verification_key.json` | 100644 | blob | `ab18b9824d790427241e39a6d37fe94b37a599f3` | `8548836eaeb4500e19ca9032852095b257a9a5267206dd4e8180740c8841d14c` |
| `zk/v3-groth16/golden-proof.json` | 100644 | blob | `e932574e7599067cbfc3baf3ee3d98808e944aca` | `01360c724f748b1630b6605bf7464af585643a0d87fcbbb2a21e3fa3025a63b7` |
| `zk/v3-groth16/test-golden-proof.js` | 100644 | blob | `6aebd8f293a8b2f97d266f34084c5e9b6409de5e` | `a2744c49785c905a552e9612f7a4e536e028ea59d5a8ba7978dd534a73b4cbd7` |
| `zk/v3-groth16/test-on-chain.sh` | 100755 | blob | `04e8e1bc545fd4c87e5f6792b8f960999c68717d` | `a097eccc184fc0489288158df789fd1adb8bef516b7c973c03edf0d6fec93f7a` |

## 11. Applicable-Rule and Component Ledger

The proposed action-type coordinate is `T-I164-ANONYMOUS-PUBLIC-ACTION`.

The candidate context coordinates are:

- the published protocol generation;
- Complete Implementation Profile V2;
- the fixed PetitionRegistry execution state;
- the configured verifier;
- the public action-context value;
- the claimed membership root;
- and the action-local uniqueness state.

These coordinates are not declared as one complete formal Evaluation context because accepted-root status, complete rule selection, occurrence identity, and completeness composition remain unresolved.

| Component | Formal rows | Exact I164 material | Stable content anchor | Input and result | Failure behaviour | Evidence classes | Limitation |
|---|---|---|---|---|---|---|---|
| C-WITNESS | PE-VALID-001; PE-EVAL-013 | `frontend/src/hooks/useZKProof.js`; Git blob `985e8adb8410a134fa010d2fa49ee179e47edfb5`; SHA-256 `8df56093b0a5a3ed8121e3cbe45761d0cfc967bc0fcdd108222944f5901a575a` | `normalizeInputs`; `normalizeMerkleToMatchRoot`; `generateProof` | Local witness material and action-context value -> proof-generation input | Local construction failure | TD | Pre-Evaluation construction only; not a Protocol Action or Evaluation |
| C-CIRCUIT | PE-VALID-001; PE-VALID-002; PE-VALID-008; PE-EVAL-013 | `zk/v3-groth16/circuits/sign_petition.circom`; Git blob `165ed8cfa1029dd0a937ab6e885af020fbf991e5`; SHA-256 `a64783f8873df0c9dda7f7e44607e076f0b2af94c9cd609e4619e4b0fbcf2e02` | `MerkleTreeInclusionProof`; `SignPetition`; `component main` | Private witness plus public action-context value and claimed root -> constrained nullifier and proof relation | Unsatisfied constraint prevents proof construction | TD,RG | Establishes inclusion under the supplied root; does not establish accepted-root status |
| C-PUBLIC-ORDER | PE-VALID-001; PE-RULE-007; PE-ACTION-010 | `zk/v3-groth16/circuits/sign_petition.circom`; Git blob `165ed8cfa1029dd0a937ab6e885af020fbf991e5`; SHA-256 `a64783f8873df0c9dda7f7e44607e076f0b2af94c9cd609e4619e4b0fbcf2e02` | `nullifier` output and `main {public [petitionId, membershipRoot]}` | Circuit public values -> ordered public-signal relation | Incoherent ordering cannot satisfy the bound verifier relation | BD,TD,RG | Declared order is nullifier, petitionId/actionId, membershipRoot |
| C-VERIFY | PE-VALID-001; PE-VALID-002; PE-VALID-004; PE-VALID-008; PE-EVAL-013; PE-EVAL-014; PE-EVAL-015 | `contracts/src/v3/Groth16Verifier.sol`; Git blob `bf3bd28b1e89e8672219aa5aea6e54605d1b5bfe`; SHA-256 `b1216366353f3dbf478e1e03add31077bbe4bc76d5a4e40aaba574cd5841bd87` | `verifyProof`; `checkField`; `checkPairing` | Groth16 proof and three public signals -> bounded Boolean proof-verification result | False return or bounded field/precompile failure | TD,RG,DB,RO | Proof verification is one component and is not complete Protocol Action validity |
| C-EXISTS | PE-VALID-005; PE-VALID-006; PE-EVAL-016 | `contracts/src/PetitionRegistry.sol`; Git blob `a593c4023fc1ce9c835013a5ad40a310e5bfd032`; SHA-256 `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` | `signPetitionWithZKProof`: `petitions[petitionId].exists` guard | Application-target key and stored existence flag -> continued execution or revert | `PetitionDoesNotExist` | TD,DB,RO | The implementation check is exact; its generation-derived protocol-rule assignment remains unresolved |
| C-UNIQUE | PE-VALID-005; PE-VALID-007; PE-RULE-007; PE-RULE-010; PE-EVAL-016 | `contracts/src/PetitionRegistry.sol`; Git blob `a593c4023fc1ce9c835013a5ad40a310e5bfd032`; SHA-256 `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` | `usedSignNullifier`; `signPetitionWithZKProof`; `hasSignedPetition` | Action-context key and nullifier -> unused/used result | `NullifierAlreadyUsed` | TD,RG,DB,RO | Supports the proposed action-local uniqueness relationship; not a reusable participant identity |
| C-VERIFIER-CONFIG | PE-RULE-005; PE-CLASS-007 | `contracts/src/PetitionRegistry.sol`; Git blob `a593c4023fc1ce9c835013a5ad40a310e5bfd032`; SHA-256 `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` | `address(groth16Verifier) == address(0)` guard | Verifier configuration -> available or unavailable execution component | `InvalidVerifier` | TD,DB,RO | Deployment/configuration condition; not declared as a protocol-validity rejection |
| C-PROOF-RESULT | PE-VALID-002; PE-VALID-004; PE-VALID-008; PE-EVAL-013; PE-EVAL-014; PE-EVAL-015 | `contracts/src/PetitionRegistry.sol`; Git blob `a593c4023fc1ce9c835013a5ad40a310e5bfd032`; SHA-256 `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` | `groth16Verifier.verifyProof(pA, pB, pC, pubSignals)` | Bound verifier result -> continued execution or revert | `InvalidZKProof` | TD,RG,DB,RO | Does not directly produce a Determination or classification |
| C-PUBLIC-NULLIFIER | PE-VALID-005; PE-VALID-007; PE-RULE-007; PE-EVAL-016 | `contracts/src/PetitionRegistry.sol`; Git blob `a593c4023fc1ce9c835013a5ad40a310e5bfd032`; SHA-256 `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` | `uint256(nullifier) != pubSignals[0]` | Function argument and public signal zero -> coherent or revert | `InvalidZKProof` | TD,RG,DB,RO | Binds the public uniqueness value without defining Action identity |
| C-PUBLIC-ACTION | PE-VALID-005; PE-VALID-007; PE-RULE-007; PE-ACTION-010; PE-EVAL-016 | `contracts/src/PetitionRegistry.sol`; Git blob `a593c4023fc1ce9c835013a5ad40a310e5bfd032`; SHA-256 `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` | `petitionId != pubSignals[1]` | Function action-context value and public signal one -> coherent or revert | `InvalidZKProof` | TD,RG,DB,RO | The shared value does not merge Protocol Action identity with application-target identity |
| C-ROOT-INCLUSION | PE-VALID-001; PE-VALID-007; PE-RULE-007 | `zk/v3-groth16/circuits/sign_petition.circom`; Git blob `165ed8cfa1029dd0a937ab6e885af020fbf991e5`; SHA-256 `a64783f8873df0c9dda7f7e44607e076f0b2af94c9cd609e4619e4b0fbcf2e02` | `hashes[nLevels] === root` | Witness path -> equality with the supplied membership root | Unsatisfied circuit constraint | TD,RG | Proves inclusion under the supplied root only |
| C-ROOT-ACCEPTED | PE-VALID-003; PE-VALID-005; PE-VALID-007; PE-RULE-001; PE-RULE-007; PE-EVAL-003; PE-EVAL-008; PE-EVAL-016 | `contracts/src/AnonymousMembershipRegistry.sol`; Git blob `31835a9feeeff6691335cca655b1f9e31ceba0d6`; SHA-256 `2b883cbca96f074c52d0471aaa62681ae042b8315d5e1260ab114541650c7978` | `isValidRoot` and `isKnownRoot` | Claimed root -> available accepted-root-state read | No active-path result | TD,DB,RO | No call or state read connects this check to `PetitionRegistry.signPetitionWithZKProof`; formal mapping unresolved |
| O-RELAY-PAYLOAD | PE-RULE-005; PE-ACTION-006; PE-EVAL-019; PE-CLASS-006; PE-CLASS-007 | `backend/src/routes/relay.js`; Git blob `23a4d5f37a5dafa2cfd39030e1d42bff9807e3e7`; SHA-256 `1f748b519358c4d4653dfce5d13d6f54cab4a3cd7cb70d8f1937a75a06990f7a` | `POST /sign` payload-shape and public-signal coherence branches | Transport request -> accepted operational payload or HTTP refusal | HTTP 400 | TD,RO | Pre-authoritative operational validation; not formal Evaluation or rejection |
| O-INDEXER-FRESHNESS | PE-RULE-005; PE-EVAL-019; PE-CLASS-007 | `backend/src/services/indexerFreshness.js`; Git blob `cdcf3077e0ab7f231b53726f8eb90bac1a76a0ef`; SHA-256 `66b870d2087ecef424019933e2aa90451244869a6c6929c5e7b595109fd4a794` | `getPetitionIndexerFreshness` | Indexer cursor and latest block -> operational health state | Unknown or degraded status | TD,RO | Operational submission gate; not a protocol-validity rule or rejection |
| O-DISPATCH | PE-ACTION-006; PE-ACTION-008; PE-RULE-011; PE-CLASS-007 | `backend/src/services/relayExecution.js`; Git blob `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd`; SHA-256 `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` | `freezeRelaySubmission`; `dispatchRelayExecution`; `deriveTempestSeed` | Frozen canonical submission -> ordered operational presentation attempts | Executor or transport exception | TD,RG,DB,RO | Seed, slot, domain, retry, and transaction identifiers do not define Protocol Action identity |
| O-RECONCILE | PE-ACTION-008; PE-RULE-011; PE-CLASS-007 | `backend/src/services/relayExecution.js`; Git blob `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd`; SHA-256 `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` | `reconcileRelayExecutionState` | Uncertain operational submission -> bounded used-state observation | Null result or read failure | TD,RG,DB,RO | Reconciliation is not Determination or acceptance |
| O-OBSERVATION | PE-DETERM-009; PE-DETERM-010; PE-CLASS-007 | `backend/src/indexer/petitions/processor.js`; Git blob `b38e89799c61a846025390325f882c2a69ce9759`; SHA-256 `addfa0e87da3c1a94628d30024556fa9ba644df46c78fb27caac7529e18b3437` | `PetitionSigned` normalization and dispatch | Chain log -> downstream normalized observation | Indexer or persistence interruption | TD,RO | Event and indexed record are not Determination or protocol authority |

The exact component inventory does not establish a complete applicable protocol-rule set.

In particular:

- circuit root equality establishes inclusion under the supplied root;
- `AnonymousMembershipRegistry.isValidRoot` exposes accepted-root state;
- `PetitionRegistry.signPetitionWithZKProof` contains no call or state read connecting that accepted-root state to the active action path.

Therefore accepted-root evaluation is not manufactured from proximity, naming, documentation, or the existence of the standalone root function.

Petition existence is an exact implementation check, but this draft does not infer whether that check is a generation-derived protocol-validity rule or an application-owned admission condition.

Relay payload checks, rate limiting, indexer freshness, executor selection, fallback, transaction submission, and reconciliation remain operational unless an accepted mapping separately establishes a protocol role.

## 12. Asserted Relationships

| Relationship | Subject | Bounded assertion | Exact basis | Lifecycle status |
|---|---|---|---|---|
| ASR-001 | Declared public-input relationship | The proposed action type uses exactly the ordered public set nullifier, petitionId/actionId, membershipRoot. | `sign_petition.circom`; `Groth16Verifier.verifyProof`; `PetitionRegistry.signPetitionWithZKProof` | Draft only |
| ASR-002 | Private/public separation | Private witness inputs remain local to proof construction and are absent from the relay and contract-call payload. | `useZKProof`; circuit private signals; relay payload; contract ABI | Draft only |
| ASR-003 | Proof relation | The proof supports knowledge, Merkle inclusion under the supplied root, and action-scoped nullifier derivation. | `SignPetition`; `MerkleTreeInclusionProof` | Draft only; accepted-root status excluded |
| ASR-004 | Bounded verifier result | The Groth16 verifier result concerns the configured proof relation and three supplied public signals only. | `Groth16Verifier.verifyProof` | Draft only; not complete validity |
| ASR-005 | Public-signal coherence | The contract separately binds nullifier and action-context arguments to public-signal positions zero and one. | `PetitionRegistry.signPetitionWithZKProof` | Draft only |
| ASR-006 | Action-local uniqueness | Nullifier derivation includes the action-context value and the authoritative state guard is keyed by action context and nullifier. | `SignPetition`; `usedSignNullifier` | Draft only; no participant identity |
| ASR-007 | Operational preservation | Relay fallback operates over one frozen submission value without converting operational identifiers into formal Action identity. | `freezeRelaySubmission`; `dispatchRelayExecution` | Draft only; retry equivalence remains unresolved |
| ASR-008 | Application-role separation | The action-context value may also select an application target, but that application object does not become Protocol Action occurrence identity. | `petitionId`; `petitions`; public signal one | Draft only |
| ASR-009 | Observation separation | Transaction hash, event, state mutation, response, reconciliation result, and indexed record remain downstream or operational representations. | Relay, contract, event, indexer, and persistence surfaces | Draft only; none is a Determination |

Every assertion above is proposed only.

No asserted relationship is accepted for assessment reliance in Engineering[169].

## 13. Protocol Action Evaluation Mapping

The following exact source sequence is identifiable as a candidate component-evaluation segment inside `PetitionRegistry.signPetitionWithZKProof`:

1. application-target existence guard;
2. action-local nullifier-used guard;
3. verifier-configuration guard;
4. Groth16 verifier call;
5. nullifier-to-public-signal binding;
6. action-context-to-public-signal binding.

The circuit separately constrains:

- private witness derivation;
- inclusion under the supplied root;
- action-context binding in nullifier derivation;
- and the declared public-output relationship.

These candidate checks cannot be declared one complete Protocol Action Evaluation because I164 does not provide:

- one stable Evaluation occurrence identity;
- one previously established complete applicable-rule set;
- one authoritative Evaluation start boundary;
- one complete bounded evaluation context;
- an active accepted-root-status component;
- an explicit assignment of every applicable generation-derived rule;
- a complete component-result set;
- a coherent all-component combination record;
- or one formal Evaluation-completeness representation.

A successful path through every implemented contract guard establishes only that every implemented guard reached before the state write permitted continuation.

It does not establish that every applicable protocol rule was evaluated.

A reverted path is short-circuiting. Later candidate checks are not necessarily evaluated. Therefore a revert cannot be declared a complete rejecting Evaluation.

The Evaluation mapping remains unresolved under:

- `U-RULESET`;
- `U-ROOT`;
- `U-EVAL-IDENTITY`;
- `U-EVAL-BOUNDARY`;
- and `U-EVAL-REJECTION`.

The preserved formal relationship is:

> proof verification  
> `!=` complete Protocol Action Evaluation

> partial or interrupted component sequence  
> `!=` completed Evaluation

> pre-evaluation or operational failure  
> `!=` Protocol Action Determination

## 14. Protocol Action Determination Mapping

No exact I164 value or representation can be declared as the stable Protocol Action Determination without inference.

The following candidates were inspected and explicitly rejected as automatic mappings:

- successful function fallthrough;
- contract revert;
- transaction object;
- transaction hash;
- transaction receipt;
- relay response;
- `usedSignNullifier` state mutation;
- `PetitionSigned` event;
- reconciliation result;
- indexed database record;
- signature-count projection;
- and application success state.

None is explicitly represented as:

- the result of one completed Evaluation;
- identifying that producing Evaluation;
- identifying the evaluated Action;
- preserving the complete applicable rule set;
- preserving the bounded evaluation context;
- and carrying exactly one formal acceptance or rejection classification.

Therefore:

> no completed Evaluation identity  
> `->` no declared Determination identity

The Determination relationship remains unresolved under `U-DETERMINATION`.

## 15. Acceptance, Rejection, and Non-Classification Ledger

| Observed or candidate condition | Exact surface | Draft treatment | Formal limitation |
|---|---|---|---|
| Completed Evaluation accepted | No exact I164 representation identified | Unresolved | No completed formal Evaluation or Determination identity is available |
| Completed Evaluation rejected | No exact I164 representation identified | Unresolved | No complete all-rule rejecting Evaluation or rejection record is available |
| Incomplete Evaluation | Candidate short-circuit or interrupted component sequence | No formal classification | No formal Evaluation identity or completeness representation is available |
| Malformed relay submission | `POST /sign` HTTP 400 branches | Pre-authoritative operational refusal | Not acceptance or rejection |
| Proof-generation failure | `useZKProof.generateProof` exception path | Construction failure | Not Evaluation or rejection |
| Local proof-preflight failure | `M2SignButton` verifier preflight | Pre-submission failure | Not authoritative Evaluation |
| Indexer-freshness gate | HTTP 503 branch | Operational unavailability | Not protocol rejection |
| Executor controlled failure | `execution_controlled_failure` | Operational failure with fallback | Not protocol rejection |
| Transport failure | `execution_transport_failure` | Operational failure with possible fallback | Not protocol rejection |
| Fallback progression | `dispatchRelayExecution` iteration | Operational continuation | Not a new classification |
| Transaction-submission failure | Executor exception | Operational failure | Not protocol rejection |
| Reverted execution | Ethers call exception or contract custom error | Execution failure candidate | Cannot be declared formal rejection because complete Evaluation is not established |
| Transaction hash returned | `tx.hash` | Submission acknowledgement | Not Determination or acceptance |
| Uncertain execution result | Transport failure after possible submission | Unknown operational state | Not acceptance or rejection |
| Reconciliation state | `hasSignedPetition` observation | Bounded state observation | Not Determination |
| State mutation and `PetitionSigned` event | `usedSignNullifier` write and event emission | Transition and observation candidates | Not Determination or classification |
| Persistence or indexing lag | Indexer and database surfaces | Downstream observation delay | Not protocol rejection |
| Application-level failure | UI, adapter, or application handling | Application outcome | Not protocol acceptance or rejection |

Only a completed formal Evaluation may produce a Determination.

Only a valid Determination may carry exactly one mutually exclusive acceptance or rejection classification.

I164 supplies no exact accepted or rejected Determination representation. Engineering[169] therefore declares neither acceptance nor rejection for any execution surface.

## 16. Explicit Non-Mappings

| Source or candidate representation | Relationship | Not mapped as |
|---|---|---|
| NM-001 | UI request | Protocol Action |
| NM-002 | Private witness | Protocol Action identity |
| NM-003 | Proof | Private Actor identity |
| NM-004 | Proof-generation attempt | Protocol Action Evaluation |
| NM-005 | Relay request | Automatically a Protocol Action occurrence |
| NM-006 | Successful proof verification | Complete Protocol Action validity |
| NM-007 | Operational retry or fallback attempt | Automatically a new or merged Protocol Action occurrence |
| NM-008 | TEMPEST seed, slot, domain, or fallback position | Protocol Action identity or rule applicability |
| NM-009 | Transaction or transaction hash | Protocol Action Determination |
| NM-010 | Contract revert | Automatically a formal rejection |
| NM-011 | Relay or UI response | Protocol Action Determination |
| NM-012 | Event | Protocol Action Determination |
| NM-013 | State mutation | Acceptance or rejection classification |
| NM-014 | Reconciliation result | Protocol Action Determination |
| NM-015 | Indexer or persistence record | Protocol authority |
| NM-016 | Application-target identity | Protocol Action occurrence identity |
| NM-017 | Application meaning or truth | Protocol validity or classification |
| NM-018 | Runtime success | Evidence sufficiency |
| NM-019 | Draft declaration | Requirement result |

## 17. Unsupported Relationships

| Unresolved relationship | Required mapping | Candidate material inspected | Why declaration is unsupported |
|---|---|---|---|
| U-ACTION-IDENTITY | Stable Protocol Action occurrence identity | `signPetitionWithZKProof`, relay submission, transaction, event, and state key | No exact baseline declaration chooses occurrence coordinates without substituting an operational identifier |
| U-ACTION-ADMISSION | Authoritative Action admission boundary | Relay acceptance and ABI-decoded contract invocation | The complete applicable rule set and context are not established before either candidate boundary |
| U-RETRY | Repeated-presentation identity rule | Frozen submission, deterministic permutation, fallback, and reconciliation | The baseline preserves payload material but does not declare whether repeated authoritative presentations are one or distinct Action occurrences |
| U-RULESET | Complete applicable protocol-rule set | Circuit, verifier, contract guards, relay checks, state reads, tests, and boundary documents | No exhaustive generation-derived ledger assigns every applicable rule and excludes operational policy |
| U-ROOT | Accepted membership-root status | `AnonymousMembershipRegistry.isValidRoot`; circuit root equality; `PetitionRegistry.signPetitionWithZKProof` | The active action path binds proof inclusion to a supplied root but contains no call or state read establishing accepted-root status |
| U-EVAL-IDENTITY | Stable Evaluation occurrence identity | Contract call and sequential checks | No representation separately identifies one formal Evaluation occurrence |
| U-EVAL-BOUNDARY | Evaluation start, completion, and combination rule | Sequential contract guards and verifier call | No complete rule set, completeness state, all-component result, or formal combination record is represented |
| U-EVAL-REJECTION | Complete rejecting Evaluation | Short-circuit revert branches | A failed guard stops later checks; the baseline does not establish evaluation of every applicable rule |
| U-DETERMINATION | Stable Protocol Action Determination | Fallthrough, revert, transaction, response, event, mutation, and indexed record | No exact representation is separately identified as the result of one completed Evaluation |
| U-CLASSIFICATION | Mutually exclusive acceptance or rejection classification | Success and failure surfaces | No valid Determination or separate classification record is available |
| U-PRIVACY-REVIEW | Complete privacy and neutral-naming review of every lifecycle surface | Client, relay, contract, diagnostics, tests, events, and persistence | The declaration itself is reviewed, but complete baseline-wide privacy evidence remains a separate dependency |
| U-PROVENANCE | Synchronized ZK provenance chain | Manifest, runtime artifacts, canonical paths, verifier source, and golden proof | Engineering[166] records three absent canonical items, three recorded-digest differences, and two unavailable canonical-to-runtime comparisons |

Every unresolved relationship retains the affected Engineering[167] rows as `still-ambiguous`.

No unresolved relationship is repaired, substituted, inferred, or converted into a requirement result.

## 18. Evidence-Layer Separation

| Evidence layer | Engineering[169] state | Material | Preserved boundary |
|---|---|---|---|
| Boundary documentation | Available | STATE.md and guarded boundary documents | Intent and boundary evidence only; cannot replace tracked behavior |
| Tracked-direct evidence | Available | Exact engineering-164 blobs and Gitlinks | Supports only the relationships explicitly tied to exact material |
| Reproducibly generated evidence | Procedure available; no new Engineering[169] result | Tracked tests, scripts, artifacts, lockfiles, and generation operations | No test, build, proof, or verifier output is created by this slice |
| Deployment-bound evidence | Dependency identified; not newly verified | Configuration records, scripts, proxy/verifier relationships, and chain identity | No deployment observation is created or promoted |
| Runtime-observation evidence | Dependency identified; not newly created | Potential contract, relay, event, indexer, persistence, and failure observations | No runtime observation is created or promoted |
| Unavailable evidence | Explicitly recorded | Accepted-root integration, complete rule-set declaration, formal occurrence identities, Determination record, classification record | Relationships remain unresolved |
| Evidence still required before assessment | Required | Separate declaration acceptance plus later bounded RG, DB, and RO evidence where applicable | Availability remains distinct from sufficiency and requirement result |

The inherited ZK provenance observations remain unchanged:

- three canonical manifest items are absent from the tracked baseline;
- three tracked items differ from their recorded manifest digests;
- six tracked items match;
- two canonical-to-runtime comparisons cannot be performed from tracked material;
- the canonical and frontend runtime verification keys are byte-identical.

These are availability and dependency observations only.

> evidence availability  
> `!=` evidence sufficiency  
> `!=` requirement result

## 19. Privacy and Neutral-Naming Review

The declaration preserves:

> Private actors, public actions.

This package:

- introduces no Private Actor identity;
- records no concrete private witness value;
- records no participant account;
- records no reusable participant identifier;
- records no funding, admission, transport, or ownership provenance;
- reproduces no sample secret, leaf, proof, nullifier, transaction, or runtime actor-linked value;
- does not promote local storage, relay selection, request handling, transaction sender, event ordering, or persistence metadata into Action, Evaluation, Determination, or classification identity;
- uses neutral declaration, component, relationship, and unresolved-boundary identifiers;
- cites exact source symbols only where required to bind a relationship to I164;
- and keeps action-context public values role-bounded.

The fixed source may contain implementation and application terminology. Citation of an exact tracked symbol does not acquire or extend that symbol’s semantics.

The declaration itself does not create an actor-reconstruction bridge.

## 20. Declaration Lifecycle Position

The Engineering[168] construction rule is satisfied through every term except accepted declaration authority.

Accordingly:

> proposed mapping package complete  
> `+` draft status  
> `+` acceptance required  
> `+` acceptance occurrence none  
> `->` unavailable for assessment reliance

A later bounded acceptance-review slice may:

1. verify the immutable Engineering[169] declaration digest;
2. verify the fixed formal and I164 inputs;
3. review every asserted mapping;
4. review every explicit non-mapping;
5. review every unresolved relationship and limitation;
6. determine whether implementation governance accepts the declaration;
7. and, only if accepted, create a separate integrity-bound acceptance record.

That later review must not silently convert unresolved relationships into mappings.

## 21. Exact 88-Row Declaration Ledger

This ledger preserves the exact Profile V2 and Engineering[167] identity of every A04–A08 row.

`Draft treatment` is a mapping-package treatment only. It is not an Engineering[167] reclassification, acceptance occurrence, evidence-sufficiency judgment, or requirement result.

| Identifier | RF | SF | Strength | Published applicability | Profile disposition | E167 group | E167 state | Profile row SHA-256 | Draft treatment | Relationship reference |
|---|---|---|---|---|---|---|---|---|---|---|
| PE-VALID-001 | RF-18 | SF-06 | MUST | Every proof-verification result used during Protocol Action Evaluation | applicable | A04 | still-ambiguous | 7d82dc07bd79d4def802486bc4a9ddf17818d624c6a4151cef3037255e9d65a6 | Proposed supported relationship | ASR-003/ASR-004/ASR-006 |
| PE-VALID-002 | RF-18 | SF-06 | MUST | Every proof-verification result contributing to complete Evaluation | applicable | A04 | still-ambiguous | 54eb03910727d11bffbcf962b3103ad5833fbba90751f78d452ca459a38365fa | Proposed supported relationship | ASR-003/ASR-004/ASR-006 |
| PE-VALID-003 | RF-18 | SF-06 | MUST | Every Protocol Action validity determination basis | applicable | A04 | still-ambiguous | 1ceb5a51e6f98b3cf3902b5063582f415cb747ea8c9ae197f986e193e238a642 | Unresolved | U-RULESET/U-ROOT |
| PE-VALID-004 | RF-18 | SF-06 | MUST NOT | Every successful proof-verification result | applicable | A04 | still-ambiguous | 7388241381908c563e95d3c6af38ec57bd7c9f6f475d6dd7f40c70aee1073221 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-VALID-005 | RF-18 | SF-06 | MUST | Every Protocol Action whose applicable rule set includes non-proof validity conditions | applicable | A04 | still-ambiguous | 3641fba2e7a21fac5990ba5ad83b9f6a735891b1af60cc8c602f7dbfaf964216 | Supported component plus unresolved complete relationship | U-RULESET/U-ROOT/U-PRIVACY-REVIEW |
| PE-VALID-006 | RF-18 | SF-06 | MUST | Every non-proof protocol-validity condition | applicable | A04 | still-ambiguous | ffa5be8d7f931d358ddf6c00e062d10ad153bb75e9686fe6c9b30566288de155 | Unresolved | U-RULESET/U-ROOT |
| PE-VALID-007 | RF-18 | SF-06 | MUST | Every current-generation Protocol Action Evaluation basis | applicable | A04 | still-ambiguous | 9faa7f0bd22629669ac6360f18edccd49757f5e63307dca13873e4354ea7ad8d | Unresolved | U-RULESET/U-ROOT |
| PE-VALID-008 | RF-18 | SF-06 | MUST | Every required proof-invalid verification result | applicable | A04 | still-ambiguous | eb7c653e8f9352e9810df7534d4fc3b42458a0f0dcc84ec76192c57cf90a74c5 | Proposed supported relationship | ASR-003/ASR-004/ASR-006 |
| PE-VALID-009 | RF-18 | SF-06 | MUST | Every interpretation of protocol validity | applicable | A04 | still-ambiguous | 1dc84bc2c6797fbd43663a4eb6e47ddc0146e45a2dda7df9a5e68fcbebf50453 | Unresolved | U-RULESET/U-ROOT |
| PE-VALID-010 | RF-18 | SF-06 | MUST NOT | Every proof-valid or protocol-valid classification | applicable | A04 | still-ambiguous | 99f8a72909867dc4f795ee44a9a03acf70b972c4580710453316f5415cb14e91 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-VALID-011 | RF-18 | SF-06 | MUST NOT | Every protocol-valid Protocol Action and interpretation of it | applicable | A04 | still-ambiguous | 002133d7aad0ace021cd9a793c907d7a8d814c194875f93e7be5e34f94d4be23 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-VALID-012 | RF-18 | SF-06 | MUST | Every evidence, validity, failure, and diagnostic surface | applicable | A04 | still-ambiguous | da1fc4ae5e8b9c469f2a9bb090299baf688cfba8d7c3f512d1369c247f503259 | Supported component plus unresolved complete relationship | U-RULESET/U-ROOT/U-PRIVACY-REVIEW |
| PE-ACTION-001 | RF-20 | SF-07 | MUST | Every Privacy Engine Protocol Action | applicable | A05 | still-ambiguous | 463004346231b57549d4e4e1afe320117c07aecc502784bdc1c0fa43da308e9f | Unresolved | U-ACTION-IDENTITY/U-ACTION-ADMISSION/U-RETRY |
| PE-ACTION-002 | RF-20 | SF-07 | MUST | Every Protocol Action occurrence | applicable | A05 | still-ambiguous | 3c39a5437a128a309481077f8269c6f3bbab15f574be3f3ee220b009af58ac4d | Unresolved | U-ACTION-IDENTITY/U-ACTION-ADMISSION/U-RETRY |
| PE-ACTION-003 | RF-20 | SF-07 | MUST | Every Protocol Action | applicable | A05 | still-ambiguous | 86345e5cb0d092c59c2004291c26c497264b190ae7cfdcf9ab4a9a29c5926415 | Unresolved | U-ACTION-IDENTITY/U-ACTION-ADMISSION/U-RETRY |
| PE-ACTION-004 | RF-20 | SF-07 | MUST | Every Protocol Action occurrence | applicable | A05 | still-ambiguous | 23e1d3e60077600c0dfb2b0dcf6635df02288233228643b7908f6a9a7eacf2ef | Supported component plus unresolved complete relationship | U-ACTION-IDENTITY/U-RETRY |
| PE-ACTION-005 | RF-20 | SF-07 | MUST | Every Protocol Operation, action type, and Protocol Action occurrence | applicable | A05 | still-ambiguous | 279a450caad2bbc7193f5432dc2bce597acd6b46ccfaa14100cfdac21aeea3b0 | Unresolved | U-ACTION-IDENTITY/U-ACTION-ADMISSION/U-RETRY |
| PE-ACTION-006 | RF-20 | SF-07 | MUST | Every effort to construct, present, submit, or obtain evaluation of a candidate Protocol Action | applicable | A05 | still-ambiguous | 62a35dad1164f717c8cf3075563a945cdf55c85842323828ea42dc55fccbafde | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-ACTION-007 | RF-20 | SF-07 | MUST | Every candidate admitted to authoritative Protocol Action Evaluation | applicable | A05 | still-ambiguous | 51c54fd25797c77d27a64631d0c8d36fdd25fc5b2d9d551ecfb75a9d83369c9f | Unresolved | U-ACTION-IDENTITY/U-ACTION-ADMISSION/U-RETRY |
| PE-ACTION-008 | RF-20 | SF-07 | MUST NOT | Every transport retry, relay attempt, submission retry, implementation retry, and internal processing attempt | applicable | A05 | still-ambiguous | 578436b2cb6b1778d823d4bc746fb5043cc9c76f34102b0b9fbc1284bbfc6098 | Supported component plus unresolved complete relationship | U-ACTION-IDENTITY/U-RETRY |
| PE-ACTION-009 | RF-20 | SF-07 | MUST | Every protocol rule governing repeated authoritative presentations | applicable | A05 | still-ambiguous | 5e725254afc94c74929b159c0d02d9e63693760e819794b98d3f732b2c93036d | Unresolved | U-ACTION-IDENTITY/U-ACTION-ADMISSION/U-RETRY |
| PE-ACTION-010 | RF-20 | SF-07 | MUST | Every Protocol Action | applicable | A05 | still-ambiguous | 53eb9b4226ffaddcaa8bac0403c1f93b4dfe68753d51c962559da5fe30294283 | Supported component plus unresolved complete relationship | U-ACTION-IDENTITY/U-RETRY |
| PE-ACTION-011 | RF-20 | SF-07 | MUST | Every proof-supported Protocol Action | applicable | A05 | still-ambiguous | a1b72f91e3b6d27d9517922ed57a91d44c1afad80140c80e120d2b5575764041 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-ACTION-012 | RF-20 | SF-07 | MUST | Every Protocol Action performed through an implementation | applicable | A05 | still-ambiguous | 24ad0dd544294050c02b6f76b929429d7b1db2b30c996bed46c9fde9f775cca1 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-ACTION-013 | RF-20 | SF-07 | MUST | Every relationship between a Private Actor and Protocol Action | applicable | A05 | still-ambiguous | 57aaf8bb550db022a9938e4ebb7b8967b58a6c3ff98e433016d06953faa3b9d0 | Supported component plus unresolved complete relationship | U-ACTION-IDENTITY/U-RETRY |
| PE-ACTION-014 | RF-20 | SF-07 | MUST NOT | Every Protocol Action identifier and representation | applicable | A05 | still-ambiguous | a9b035df445d69fde2334e241559af9442b62b5f827f513e3e3417b77aa7f581 | Supported component plus unresolved complete relationship | U-ACTION-IDENTITY/U-RETRY |
| PE-ACTION-015 | RF-20 | SF-07 | MUST NOT | Every application interpretation of a Protocol Action | applicable | A05 | still-ambiguous | 009c19c28d1f2e7d0f84cab93f5d01fcee58b799b1fa138e744032110d44ff2b | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-ACTION-016 | RF-20 | SF-07 | MUST | Every relationship from a Protocol Action to a possible Published Result, Determination, or Protocol State Transition | applicable | A05 | still-ambiguous | 0e10cf56ff23b2f68ac6b146d527fa7d642c686629dace4c8001fc2893dc3a4b | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-ACTION-017 | RF-20 | SF-07 | MUST NOT | Every Protocol Action interpretation and extension | applicable | A05 | still-ambiguous | 3cadf5eb5d758382528a2a9b4cac93b3e452ebad010f3d51078634d2426a814a | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-RULE-001 | RF-21 | SF-07 | MUST | Every Protocol Action | applicable | A04 | still-ambiguous | 191e877c310d4fd89f413976575c6345007b3f0f839b0dd1b6b7c3bb081cef9a | Unresolved | U-RULESET/U-ROOT |
| PE-RULE-002 | RF-21 | SF-07 | MUST | Every rule included in an applicable Protocol Action rule set | applicable | A04 | still-ambiguous | 3ff7a7668229d4378a5534f354261f5bbe8280bc01946d90a4347f5ad375b10f | Unresolved | U-RULESET/U-ROOT |
| PE-RULE-003 | RF-21 | SF-07 | MUST | Every determination of Protocol Action rule applicability | applicable | A04 | still-ambiguous | cc7a96f3acee814907c8a499e0635a3fa78f08e4c6e06f879be89e792790fb7d | Unresolved | U-RULESET/U-ROOT |
| PE-RULE-004 | RF-21 | SF-07 | MUST | Every Protocol Action admitted for authoritative Evaluation | applicable | A04 | still-ambiguous | d093184d7625f5aff135a4dc9734a1fb81a9334cc56e9497941bc9c667d6fb8b | Unresolved | U-RULESET/U-ROOT |
| PE-RULE-005 | RF-21 | SF-07 | MUST NOT | Every implementation, application, transport, deployment, and operational policy | applicable | A04 | still-ambiguous | 2ec13801ebe56173a4cb5a0c94e4a2d2bdabbf7080370c4c72b12fcabc1811f7 | Supported component plus unresolved complete relationship | U-RULESET/U-ROOT/U-PRIVACY-REVIEW |
| PE-RULE-006 | RF-21 | SF-07 | MUST | Every Protocol Action validity classification basis | applicable | A04 | still-ambiguous | 68f91fc6b4e0bde9886efad8647ebd8cb0a114f765bacba3b1f466bdf0e3c659 | Unresolved | U-RULESET/U-ROOT |
| PE-RULE-007 | RF-21 | SF-07 | MUST | Every applicable Protocol Action rule set | applicable | A04 | still-ambiguous | 8175acc8c41c77ac1d6eb8b7573e3b2e1fbdd1aff952a8ca1458d20212f26e77 | Unresolved | U-RULESET/U-ROOT |
| PE-RULE-008 | RF-21 | SF-07 | MUST | Every protocol-validity interpretation | applicable | A04 | still-ambiguous | dd1e2cd94b1d2be69f18b059327610dfe817e5143cba456208d4922d485c7152 | Unresolved | U-RULESET/U-ROOT |
| PE-RULE-013 | RF-21 | SF-07 | MUST NOT | Every comparison of Protocol Action validity across materially different evaluation contexts | applicable | A04 | still-ambiguous | 34906a8cb7585f018fd03f11d4d84023e6e1ff75ad0e83d60996770b35b014fd | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-RULE-009 | RF-21 | SF-07 | MUST NOT | Every application interpretation and external claim associated with a Protocol Action | applicable | A04 | still-ambiguous | 1564edfd6bf23d75f9e882fbd2f16bc181809af75c2bc47599208903c6d42285 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-RULE-010 | RF-21 | SF-07 | MUST | Every action-local uniqueness or authorization rule | applicable | A04 | still-ambiguous | a1526a95299f6c919589b65f6dcf762cbe8f42a9d893fea031b71782741c591a | Proposed supported relationship | ASR-003/ASR-004/ASR-006 |
| PE-RULE-011 | RF-21 | SF-07 | MUST NOT | Every implementation, transaction, transport, retry, storage, and diagnostic identifier | applicable | A04 | still-ambiguous | 849a1e1c86dfe28414d53cc432d9ad1fcc816f6030eafaee4033cbfd7554be71 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-RULE-012 | RF-21 | SF-07 | MUST | Every Protocol Action prepared for complete Evaluation | applicable | A04 | still-ambiguous | f074aa4a9cd24ae6e5695575f82e4bc864235bccaf6a8f539688cc5d55867d4a | Unresolved | U-RULESET/U-ROOT |
| PE-EVAL-001 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation | applicable | A06 | still-ambiguous | b794e1fe6e53ffbb50b222286cf379b561a87ef96d406e3ac61b91ca767f58f5 | Unresolved | U-EVAL-IDENTITY/U-EVAL-BOUNDARY |
| PE-EVAL-002 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation | applicable | A06 | still-ambiguous | de5afb99cb11fc13cd9e7fb2c7563271d6337d15de8cb4fd2c6737e1029c9d64 | Unresolved | U-EVAL-IDENTITY/U-EVAL-BOUNDARY |
| PE-EVAL-003 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation | applicable | A06 | still-ambiguous | 252b8c3425f8d716f2ab354076f1464379004766e945d9dd58af76c392a56051 | Unresolved | U-EVAL-IDENTITY/U-EVAL-BOUNDARY |
| PE-EVAL-004 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation | applicable | A06 | still-ambiguous | c674cef0f246bb09e88455abe78a9e6f7e25bcac46721ec604447d09209818ca | Unresolved | U-EVAL-IDENTITY/U-EVAL-BOUNDARY |
| PE-EVAL-005 | RF-22 | SF-08 | MUST | Every candidate entering the authoritative Evaluation boundary | applicable | A06 | still-ambiguous | 5937e053cd0dcdc19cdb2a3c1fb4fd4f7a77f38f90b8e7c2361c22c23426a52f | Unresolved | U-EVAL-IDENTITY/U-EVAL-BOUNDARY |
| PE-EVAL-006 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation after Evaluation begins | applicable | A06 | still-ambiguous | 911f2102f64406e05eede1605ee3d643aa803898143b5f9a2fa0cc462a16fce2 | Unresolved | U-EVAL-IDENTITY/U-EVAL-BOUNDARY |
| PE-EVAL-007 | RF-22 | SF-08 | MUST NOT | Every Protocol Action Evaluation after Evaluation begins | applicable | A06 | still-ambiguous | 5e2e06d9e78c6b7f92536ced78a475a4a0766220fbdee14a354fe23895d3489b | Unresolved | U-EVAL-IDENTITY/U-EVAL-BOUNDARY |
| PE-EVAL-008 | RF-22 | SF-08 | MUST | Every complete Protocol Action Evaluation | applicable | A06 | still-ambiguous | 4a77beb41e5b05c1d69e30c71fc6f84650abe7e57398d8d0b27a839a59c971e9 | Unresolved | U-EVAL-IDENTITY/U-EVAL-BOUNDARY |
| PE-EVAL-009 | RF-22 | SF-08 | MUST | Every Evaluation component | applicable | A06 | still-ambiguous | 8ed39f47993843934d650ecf16121cc1611a52f9fce98dc383a4288c3e8893f0 | Supported component plus unresolved complete relationship | U-RULESET/U-EVAL-BOUNDARY/U-PRIVACY-REVIEW |
| PE-EVAL-010 | RF-22 | SF-08 | MUST | Every Evaluation component | applicable | A06 | still-ambiguous | 19934ebfca4668fb1f88a6119aa6f20aff4589154bb043dedcae512ab73c4d99 | Supported component plus unresolved complete relationship | U-RULESET/U-EVAL-BOUNDARY/U-PRIVACY-REVIEW |
| PE-EVAL-011 | RF-22 | SF-08 | MUST NOT | Every Evaluation component whose assigned rules are not the complete applicable rule set | applicable | A06 | still-ambiguous | ed92845b5269d4ad64b91bbc0cf665e5e3a991a55e1c6855af90067de34c180b | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-EVAL-012 | RF-22 | SF-08 | MUST | Every Evaluation containing multiple required components | applicable | A06 | still-ambiguous | 1302030fccbeb4fc0ad48c8084189e9e4be63b16ca97ea0d0cb9a38ca22645ad | Unresolved | U-EVAL-IDENTITY/U-EVAL-BOUNDARY |
| PE-EVAL-013 | RF-22 | SF-08 | MUST | Every proof-verification occurrence contributing to Evaluation | applicable | A06 | still-ambiguous | 59ca28d0229604350a1ca345ddb0a8ff5b9ede5aec659b7d3282b8ee97a4db7a | Proposed supported relationship | ASR-004 |
| PE-EVAL-014 | RF-22 | SF-08 | MUST | Every relationship between proof verification and Protocol Action Evaluation | applicable | A06 | still-ambiguous | 958979dbb7a0890b9f781993688aad2196521c2911ec21bf4809bde8e5068678 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-EVAL-015 | RF-22 | SF-08 | MUST NOT | Every proof-verification result | applicable | A06 | still-ambiguous | 9982697d3d870d3a68da9d43b30f945ed9424a7e1cc7b891ef613eadfa875b4d | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-EVAL-016 | RF-22 | SF-08 | MUST | Every Evaluation whose applicable rule set contains non-proof validity conditions | applicable | A06 | still-ambiguous | 6a5817a8e1abffa62231a22b467b14f019974042252f378e28349c99bf0048b4 | Supported component plus unresolved complete relationship | U-RULESET/U-EVAL-BOUNDARY/U-PRIVACY-REVIEW |
| PE-EVAL-017 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation completeness classification | applicable | A06 | still-ambiguous | a5f23ec94278eec9897fd39a787b74e346910150e01995f8c7025de92161ee03 | Unresolved | U-EVAL-IDENTITY/U-EVAL-BOUNDARY |
| PE-EVAL-018 | RF-22 | SF-08 | MUST NOT | Every partial or incomplete Protocol Action Evaluation | applicable | A06 | still-ambiguous | 01d20626fd53684f58f2e0ae80c2f5002e6f8825aaea44cd27aff72a40677231 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-EVAL-019 | RF-22 | SF-08 | MUST NOT | Every Evaluation failure and every pre-evaluation failure | applicable | A06 | still-ambiguous | fb149a6c3b2dcb41c9e6f1751401f4ce51ffc23275a6eaefa54cff01995eb104 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-EVAL-020 | RF-22 | SF-08 | MUST NOT | Every Evaluation component, identifier, evidence record, representation, diagnostic, log, field, route, test, example, and observability surface | applicable | A06 | still-ambiguous | 6c2c603f9f4112d76da88a050b7f63fdd010ccd55db58b61e0575beba15e3dfc | Supported component plus unresolved complete relationship | U-RULESET/U-EVAL-BOUNDARY/U-PRIVACY-REVIEW |
| PE-DETERM-001 | RF-23 | SF-08 | MUST | Every Protocol Action Determination | applicable | A07 | still-ambiguous | acb6d521ca17e96f1b2eae50cfa1023c31d89c24dc68ca2bba0945371c845aa3 | Unresolved | U-DETERMINATION |
| PE-DETERM-002 | RF-23 | SF-08 | MUST | Every relationship between a Protocol Action Evaluation and its Determination | applicable | A07 | still-ambiguous | c284ccf84d49c0f0ca33496a7231d450b53eda4bb430658dec745c4c5e1c32d3 | Unresolved | U-DETERMINATION |
| PE-DETERM-003 | RF-23 | SF-08 | MUST | Every completed Protocol Action Evaluation | applicable | A07 | still-ambiguous | e403e907a4a3a76aa1c3466ebeb76be2de82d17a7be6faf923d1adbe79501f5e | Unresolved | U-DETERMINATION |
| PE-DETERM-004 | RF-23 | SF-08 | MUST | Every Protocol Action Determination | applicable | A07 | still-ambiguous | e5ea7de2f9617426d5e649c4b67dd755246a083202dac9cf707c6eb5897a6182 | Unresolved | U-DETERMINATION |
| PE-DETERM-005 | RF-23 | SF-08 | MUST | Every Protocol Action Determination | applicable | A07 | still-ambiguous | fca171d16f442a59e7368b84fa8f7b14202eb15a2438f95639eb0ce3e5b5c9f4 | Unresolved | U-DETERMINATION |
| PE-DETERM-006 | RF-23 | SF-08 | MUST | Every valid Protocol Action Determination | applicable | A07 | still-ambiguous | 2684fb6e803ecbbac9ed8b36d9a095a1399b62ea14abfffabdfd666006cd8ca2 | Unresolved | U-DETERMINATION |
| PE-DETERM-007 | RF-23 | SF-08 | MUST NOT | Every incomplete or failed Protocol Action Evaluation | applicable | A07 | still-ambiguous | e88fd27a726b5324a4ea5f7be51209ccd8ca20dd6b72d3bed3ccd9191a6616d1 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-DETERM-008 | RF-23 | SF-08 | MUST | Every Protocol Action Determination and proof-verification result | applicable | A07 | still-ambiguous | f01051917e0dddd4e51004b66ddbbd5c80d403e0480216fb7097f35a39d62b8b | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-DETERM-009 | RF-23 | SF-08 | MUST | Every Protocol Action Determination and Published Result | applicable | A07 | still-ambiguous | 6ba65ed3cd28e322171f04081803fe2f8616b46cf0a55a9988e974c983392b49 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-DETERM-010 | RF-23 | SF-08 | MUST | Every Protocol Action Determination and possible Protocol State Transition | applicable | A07 | still-ambiguous | 6f643d0cef428c3a2cadcafca4c3ee45fd9d6213da437e34e8c6ac4dced002d6 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-DETERM-011 | RF-23 | SF-08 | MUST NOT | Every Determination identifier, representation, diagnostic, log, field, route, test, example, and observability surface | applicable | A07 | still-ambiguous | ed46863d93fad0d0117309bd83bbaea61cbad60e93619d01efcb772fee8b0b19 | Supported component plus unresolved complete relationship | U-DETERMINATION/U-PRIVACY-REVIEW |
| PE-DETERM-012 | RF-23 | SF-08 | MUST | Every pair of correct Evaluations of the same Action under the same applicable rules and equivalent contexts | applicable | A07 | still-ambiguous | 2ed9091879994779048ff6f6805597b12515ff782a4541e881dc391d9f03c7d9 | Unresolved | U-DETERMINATION |
| PE-DETERM-013 | RF-23 | SF-08 | MUST | Every context-dependent Protocol Action Determination | applicable | A07 | still-ambiguous | 4a57c7b835b6ef45e61e5fbe012bb0e906d405e79c6e30760811639aa331442f | Unresolved | U-DETERMINATION |
| PE-DETERM-014 | RF-23 | SF-08 | MUST NOT | Every Protocol Action Determination | applicable | A07 | still-ambiguous | 22ea02f3495357e2aeca7645c4753d22b9b139321706b584854516580f4a14f5 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-CLASS-001 | RF-24 | SF-08 | MUST | Every valid Protocol Action Determination | applicable | A08 | still-ambiguous | 21af8192b9efc93c8293630dc3819b9ade4adffc2cc5a44e25d3052bb6571bfa | Unresolved | U-CLASSIFICATION |
| PE-CLASS-002 | RF-24 | SF-08 | MUST | Every correct accepting Determination | applicable | A08 | still-ambiguous | 67c807d2350612a87effd2e6ff72caf5158cd958d4862b248efd591be93be2f0 | Unresolved | U-CLASSIFICATION |
| PE-CLASS-003 | RF-24 | SF-08 | MUST | Every correct rejecting Determination | applicable | A08 | still-ambiguous | 7e688ed43e3867285008f6a314f34098cafbcbf2d4834d03b3fc77053e9e7708 | Unresolved | U-CLASSIFICATION |
| PE-CLASS-004 | RF-24 | SF-08 | MUST | Every correct Protocol Action Determination | applicable | A08 | still-ambiguous | 64aac3f297287d0fcb32ce9bdc699fd85b2d9190e00105dd00396b05eecc209e | Unresolved | U-CLASSIFICATION |
| PE-CLASS-005 | RF-24 | SF-08 | MUST | Every correct Protocol Action Determination | applicable | A08 | still-ambiguous | 002ec96c92e7058996d49c46f064deecb08554f564886867197e433cb7dceb39 | Unresolved | U-CLASSIFICATION |
| PE-CLASS-006 | RF-24 | SF-08 | MUST NOT | Every incomplete Evaluation, Evaluation failure, and pre-evaluation failure | applicable | A08 | still-ambiguous | ec2c548ebf4a8102bb694585ba8732ece58effa91783c6ab55e00f1374310542 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-CLASS-007 | RF-24 | SF-08 | MUST NOT | Every infrastructure, transport, deployment, storage, implementation, and observability failure | applicable | A08 | still-ambiguous | 9efa97358610654b0cf7ffcef7c670d96030898eac1ae53f39a6d79775eee5f8 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-CLASS-008 | RF-24 | SF-08 | MUST NOT | Every proof-invalid result considered outside complete Protocol Action Evaluation | applicable | A08 | still-ambiguous | 7e6aaff6ca3d7b9a2c4516bfe1406d05418f99bbda1855cecb0a3b4d8496d473 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-CLASS-009 | RF-24 | SF-08 | MUST NOT | Every erroneous acceptance or rejection classification | applicable | A08 | still-ambiguous | 5ad95ec718c2c1a6f24ae7420eb129546c3103cc474f8311655a58c7085ea435 | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-CLASS-010 | RF-24 | SF-08 | MUST NOT | Every acceptance and rejection classification | applicable | A08 | still-ambiguous | 8090b6d1c87969e405a808ea0dbe03834ff765d134332ab2950cc2a43ba9748f | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-CLASS-011 | RF-24 | SF-08 | MUST NOT | Every application or external interpretation of acceptance or rejection | applicable | A08 | still-ambiguous | 9c600dbdf8b43648fc091151d6864e663dfc4c1a6e28067f7bf22dc8480f81fa | Explicit proposed non-mapping | NM-001–NM-019 |
| PE-CLASS-012 | RF-24 | SF-08 | MUST NOT | Every acceptance or rejection representation, identifier, diagnostic, log, field, route, test, example, and observability surface | applicable | A08 | still-ambiguous | 05371fe45dc21572536a81087104f3d0590721d806e0024739f2cba82f587956 | Supported component plus unresolved complete relationship | U-CLASSIFICATION/U-PRIVACY-REVIEW |

## 22. Preserved Determination

Engineering[169] preserves:

> declared implementation intent  
> `!=` tracked-direct behaviour  
> `!=` reproducibly generated evidence  
> `!=` deployment-bound evidence  
> `!=` runtime-observation evidence  
> `!=` evidence sufficiency  
> `!=` requirement result

It also preserves:

> draft declaration  
> `!=` accepted declaration  
> `!=` assessment evidence accepted for reliance  
> `!=` evidence sufficiency  
> `!=` requirement result

Engineering[169] creates no acceptance occurrence and does not claim acceptance.

## 23. Bounded Position

A complete draft I164 Protocol Action, rule Evaluation, Determination, and classification mapping declaration is constructed for the relationships explicitly supported by exact baseline evidence and is ready for separate implementation-owner acceptance review, with all unsupported relationships retained as unresolved.
