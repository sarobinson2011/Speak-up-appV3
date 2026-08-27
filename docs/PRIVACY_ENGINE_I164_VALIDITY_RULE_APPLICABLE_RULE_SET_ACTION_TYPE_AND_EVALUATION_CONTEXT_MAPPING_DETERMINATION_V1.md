# Privacy Engine I164 Validity Rule, Applicable Rule-Set, Action-Type and Evaluation-Context Mapping Determination V1

## 1. Status and Determination

This document records the bounded Engineering[193] mapping determination for the 16 reviewed-current `still-ambiguous` A04 rows.

Final mapping determination:

**complete selected A04 mapping package not constructible**

This is a mapping determination only.

It does not perform evidence-path reclassification, transition an A04 row, assess evidence availability or sufficiency, assess a requirement, produce a requirement result, determine an implementation defect, perform a security assessment or determine compatibility, conformance, certification or operational readiness.

No partial terminal acceptance is created.

## 2. Authority and Subject Boundary

`STATE.md` remains the single canonical development authority.

Protocol authority remains exclusively with the published Privacy Engine protocol generation.

The Privacy Engine is the primary implementation-independent privacy participation protocol.

I164 identifies one fixed Speak-up-appV3 implementation baseline examined under the accepted Complete Implementation Profile V2.

Speak-up-appV3 is one bounded implementation and application realization of the Privacy Engine. It does not define, own, narrow, replace or become the Privacy Engine protocol.

The preserved authority direction is:

> Privacy Engine protocol  
> -> implementation-independent authority  
> -> I164 as one bounded implementation  
> -> Speak Up as one application adapter and use case

## 3. Selected Architectural Question

Engineering[193] addresses exactly one architectural question:

> Can the 16 reviewed-current still-ambiguous A04 rows be completely mapped from I164 through a generation-derived rule ledger identifying each action type, bounded evaluation context, applicable proof and non-proof rule, and exact implementation realization, without manufacturing rule identity, completeness, authority or Evaluation semantics?

The required construction is:

> Complete A04 package  
> = complete action-type inventory  
> + complete bounded evaluation-context inventory  
> + complete applicable rule-set inventory  
> + complete proof-rule inventory  
> + complete non-proof-rule inventory  
> + exact rule-to-implementation assignments  
> + exact rule-context relationships  
> + exact evidence anchors  
> + complete negative-obligation coverage  
> + privacy-preserving representation boundaries

If any term remains unresolved, the complete selected A04 mapping package is not constructible.

## 4. Handover Verification

### 4.1 Formal corpus

| Field | Independently verified value |
|---|---|
| File | `privacy-engine-formal-corpus.zip` |
| SHA-256 | `fca8619d2b215c14869e0dd7c5573d907dbddc930d49f53db112303c4fd54dd2` |
| Distinct files | 112 |
| Directory entries | 1 |
| ZIP integrity | passed |
| Git archive comment | `3bc4086267e37384cb19d244f56ebfe177a74666` |

### 4.2 I164 implementation archive

| Field | Independently verified value |
|---|---|
| File | `implementation-baseline-engineering-164.zip` |
| SHA-256 | `7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847` |
| ZIP integrity | passed |
| Git archive comment | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |
| Parent | `5e12cca624ffccf43637de4b9dc42de4af3979bc` |
| Tracked paths | 308 |
| Blobs | 305 |
| Gitlinks | 3 |

The three Gitlinks are:

- `contracts/lib/forge-std`;
- `contracts/lib/openzeppelin-contracts`;
- `contracts/lib/openzeppelin-contracts-upgradeable`.

### 4.3 Git provenance

| Field | Independently verified value |
|---|---|
| File | `privacy-engine-git-provenance.txt` |
| Format | `PRIVACY-ENGINE-HANDOVER-GIT-PROVENANCE/1` |
| SHA-256 | `0042328fb7567ef9dfbd25e67564021523d1fd738d49483dc48e30f0b9c67f39` |
| Records | 25 |
| Record range | `engineering-164`; `engineering-169` through `engineering-192` |
| Raw commit identities | all reproduced |
| Raw payload lengths | all matched |
| Supplied local engineering refs | all matched |
| Supplied remote engineering refs | all matched |
| Trees | all matched |
| Parents | all matched |
| Changed-file identities | all matched |
| Generic-tag refs | none supplied or inferred |

The Engineering[192] raw commit payload was independently extracted as 291 bytes and reproduced:

`3bc4086267e37384cb19d244f56ebfe177a74666`

## 5. Profile V2 Basis

The accepted Complete Implementation Profile V2 remains the sole requirement-selection basis:

| Disposition | Rows |
|---|---:|
| Applicable | 478 |
| Non-applicable | 244 |
| Resolved through permitted specification choice | 7 |
| Conditionally applicable | 0 |
| Total | 729 |

No requirement-level assessment has been performed.

No requirement result exists.

## 6. Engineering[192] Verification and Preserved A03 Effect

Engineering[192] artifact:

`docs/PRIVACY_ENGINE_I164_PROTOCOL_SURFACE_PROTOCOL_OPERATION_AND_PUBLISHED_RESULT_IDENTITY_VERSION_AND_REALIZATION_MAPPING_DETERMINATION_CORRECTION_INDEPENDENT_REREVIEW_V1.md`

| Field | Independently verified value |
|---|---|
| SHA-256 | `874f8dc5c32f4f89e23441dcb897251621e164c4ddc9dc36f26358105b8be833` |
| Git blob | `0a7b9eb22406ee6780d5cc90668fe99e27de9103` |
| Length | 48,091 bytes |
| Lines | 1,037 |
| Canonical rereview payload length | 6,324 bytes |
| Canonical rereview payload SHA-256 | `5e9175730af337ba46911ba11c3d477c6f893b6e68f70f809ef9c6a2f7c4b3b3` |
| Final review result | accepted |

The accepted A03 mapping determination remains:

**complete selected A03 mapping package not constructible**

All 18 A03 rows remain reviewed-current `still-ambiguous`.

Engineering[192] did not transition an evidence path, alter the reviewed-current totals, perform requirement assessment or make I164 protocol authority.

## 7. Accepted A04 Predecessor Chain

The complete predecessor chain was independently reconstructed.

| Engineering slice | Artifact role | SHA-256 | Result |
|---|---|---|---|
| Engineering[169] | Mapping declaration | `a6e488f8a246dcf14c2a3a3e0df8226833ccec8720d12c6798a971a0d3ee6890` | declaration |
| Engineering[170] | Acceptance review | `7f435cf93d835ee3106e995c355a4d2019f2de81eaed5df2a5e9448b4bac20db` | accepted |
| Engineering[171] | Immutable pre-correction reclassification | `e7c31445ad77c2b6f592e88b846202286f003b039a717939b7f6d198d6672d46` | rejected pending correction |
| Engineering[172] | Review | `cc4e5b82a2fba611fa68032ff6eef25c45c18c9ed3d7fbc963766513fbca5b8d` | rejected pending correction |
| Corrected Engineering[171] | Corrected reclassification | `f40638d8468749afe5d260fdf01e456fc27d3afd9febf75bfe2d59e2fa6d36ff` | rereviewed |
| Engineering[173] | Correction record | `df1346947f347bb1c89569bafeb64fcee467680f88de5b4e318d9f0c7f97c1d9` | exact mechanical correction |
| Engineering[174] | Independent rereview | `ba5b8d9c6512e36f7d0d3b0e0aedd195ac0e1652cb0d7bfeeef2f17c0ab44b1f` | accepted |

Engineering[170] canonical acceptance payload independently reproduced:

- length: 883 bytes;
- SHA-256: `3c2a25b20c119d399cf3e954c26fd465834c82b6835b430f5375552fb1a1be06`.

No later artifact changed the reviewed-current A04 state.

## 8. Guarded A04 Row Ledger

The 25 rows below preserve exact Profile V2 order, identifier, RF family, SF home, strength, published applicability, predecessor state and guarded Profile V2 row hash.

| Identifier | RF | SF | Strength | Published applicability | Reviewed-current state | Profile row SHA-256 |
|---|---|---|---|---|---|---|
| PE-VALID-001 | RF-18 | SF-06 | MUST | Every proof-verification result used during Protocol Action Evaluation | bounded | `7d82dc07bd79d4def802486bc4a9ddf17818d624c6a4151cef3037255e9d65a6` |
| PE-VALID-002 | RF-18 | SF-06 | MUST | Every proof-verification result contributing to complete Evaluation | bounded | `54eb03910727d11bffbcf962b3103ad5833fbba90751f78d452ca459a38365fa` |
| PE-VALID-003 | RF-18 | SF-06 | MUST | Every Protocol Action validity determination basis | still-ambiguous | `1ceb5a51e6f98b3cf3902b5063582f415cb747ea8c9ae197f986e193e238a642` |
| PE-VALID-004 | RF-18 | SF-06 | MUST NOT | Every successful proof-verification result | bounded | `7388241381908c563e95d3c6af38ec57bd7c9f6f475d6dd7f40c70aee1073221` |
| PE-VALID-005 | RF-18 | SF-06 | MUST | Every Protocol Action whose applicable rule set includes non-proof validity conditions | still-ambiguous | `3641fba2e7a21fac5990ba5ad83b9f6a735891b1af60cc8c602f7dbfaf964216` |
| PE-VALID-006 | RF-18 | SF-06 | MUST | Every non-proof protocol-validity condition | still-ambiguous | `ffa5be8d7f931d358ddf6c00e062d10ad153bb75e9686fe6c9b30566288de155` |
| PE-VALID-007 | RF-18 | SF-06 | MUST | Every current-generation Protocol Action Evaluation basis | still-ambiguous | `9faa7f0bd22629669ac6360f18edccd49757f5e63307dca13873e4354ea7ad8d` |
| PE-VALID-008 | RF-18 | SF-06 | MUST | Every required proof-invalid verification result | bounded | `eb7c653e8f9352e9810df7534d4fc3b42458a0f0dcc84ec76192c57cf90a74c5` |
| PE-VALID-009 | RF-18 | SF-06 | MUST | Every interpretation of protocol validity | still-ambiguous | `1dc84bc2c6797fbd43663a4eb6e47ddc0146e45a2dda7df9a5e68fcbebf50453` |
| PE-VALID-010 | RF-18 | SF-06 | MUST NOT | Every proof-valid or protocol-valid classification | bounded | `99f8a72909867dc4f795ee44a9a03acf70b972c4580710453316f5415cb14e91` |
| PE-VALID-011 | RF-18 | SF-06 | MUST NOT | Every protocol-valid Protocol Action and interpretation of it | bounded | `002133d7aad0ace021cd9a793c907d7a8d814c194875f93e7be5e34f94d4be23` |
| PE-VALID-012 | RF-18 | SF-06 | MUST | Every evidence, validity, failure, and diagnostic surface | still-ambiguous | `da1fc4ae5e8b9c469f2a9bb090299baf688cfba8d7c3f512d1369c247f503259` |
| PE-RULE-001 | RF-21 | SF-07 | MUST | Every Protocol Action | still-ambiguous | `191e877c310d4fd89f413976575c6345007b3f0f839b0dd1b6b7c3bb081cef9a` |
| PE-RULE-002 | RF-21 | SF-07 | MUST | Every rule included in an applicable Protocol Action rule set | still-ambiguous | `3ff7a7668229d4378a5534f354261f5bbe8280bc01946d90a4347f5ad375b10f` |
| PE-RULE-003 | RF-21 | SF-07 | MUST | Every determination of Protocol Action rule applicability | still-ambiguous | `cc7a96f3acee814907c8a499e0635a3fa78f08e4c6e06f879be89e792790fb7d` |
| PE-RULE-004 | RF-21 | SF-07 | MUST | Every Protocol Action admitted for authoritative Evaluation | still-ambiguous | `d093184d7625f5aff135a4dc9734a1fb81a9334cc56e9497941bc9c667d6fb8b` |
| PE-RULE-005 | RF-21 | SF-07 | MUST NOT | Every implementation, application, transport, deployment, and operational policy | still-ambiguous | `2ec13801ebe56173a4cb5a0c94e4a2d2bdabbf7080370c4c72b12fcabc1811f7` |
| PE-RULE-006 | RF-21 | SF-07 | MUST | Every Protocol Action validity classification basis | still-ambiguous | `68f91fc6b4e0bde9886efad8647ebd8cb0a114f765bacba3b1f466bdf0e3c659` |
| PE-RULE-007 | RF-21 | SF-07 | MUST | Every applicable Protocol Action rule set | still-ambiguous | `8175acc8c41c77ac1d6eb8b7573e3b2e1fbdd1aff952a8ca1458d20212f26e77` |
| PE-RULE-008 | RF-21 | SF-07 | MUST | Every protocol-validity interpretation | still-ambiguous | `dd1e2cd94b1d2be69f18b059327610dfe817e5143cba456208d4922d485c7152` |
| PE-RULE-013 | RF-21 | SF-07 | MUST NOT | Every comparison of Protocol Action validity across materially different evaluation contexts | still-ambiguous | `34906a8cb7585f018fd03f11d4d84023e6e1ff75ad0e83d60996770b35b014fd` |
| PE-RULE-009 | RF-21 | SF-07 | MUST NOT | Every application interpretation and external claim associated with a Protocol Action | bounded | `1564edfd6bf23d75f9e882fbd2f16bc181809af75c2bc47599208903c6d42285` |
| PE-RULE-010 | RF-21 | SF-07 | MUST | Every action-local uniqueness or authorization rule | bounded | `a1526a95299f6c919589b65f6dcf762cbe8f42a9d893fea031b71782741c591a` |
| PE-RULE-011 | RF-21 | SF-07 | MUST NOT | Every implementation, transaction, transport, retry, storage, and diagnostic identifier | bounded | `849a1e1c86dfe28414d53cc432d9ad1fcc816f6030eafaee4033cbfd7554be71` |
| PE-RULE-012 | RF-21 | SF-07 | MUST | Every Protocol Action prepared for complete Evaluation | still-ambiguous | `f074aa4a9cd24ae6e5695575f82e4bc864235bccaf6a8f539688cc5d55867d4a` |

The guarded placement of `PE-RULE-013` before `PE-RULE-009` is preserved.

The nine already-bounded rows remain bounded.

The 16 selected rows remain `still-ambiguous`.

## 9. Exact I164 Candidate Anchor Register

Every Engineering[169] anchor was independently verified against I164. The following register identifies the principal and additional Engineering[193] candidate material.

| Tracked path | Git blob | SHA-256 |
|---|---|---|
| `ZK_ARTIFACTS_MANIFEST.json` | `e7bd40673ccad23283182a27c129c240807287be` | `e048ca3b210a4d40c8ff722a8ec5e793e1f340965c2bc6867287bc4dedaec896` |
| `frontend/src/hooks/useZKProof.js` | `985e8adb8410a134fa010d2fa49ee179e47edfb5` | `8df56093b0a5a3ed8121e3cbe45761d0cfc967bc0fcdd108222944f5901a575a` |
| `frontend/src/components/M2SignButton.jsx` | `42d27697f8ee796210f649257c94247220728f99` | `16faf8dba309411ebc40ae00c66cbfda4b2e32e48c18b46d422bcffc7c1e96f2` |
| `frontend/src/config.js` | `3facdc8697b1a1165892b3b791c75f8729ea15a2` | `165471f0585cdd3b62123bd99fd0c678e01097f65d8d6c4983f6ed4bbb82033f` |
| `zk/v3-groth16/circuits/sign_petition.circom` | `165ed8cfa1029dd0a937ab6e885af020fbf991e5` | `a64783f8873df0c9dda7f7e44607e076f0b2af94c9cd609e4619e4b0fbcf2e02` |
| `contracts/src/v3/Groth16Verifier.sol` | `bf3bd28b1e89e8672219aa5aea6e54605d1b5bfe` | `b1216366353f3dbf478e1e03add31077bbe4bc76d5a4e40aaba574cd5841bd87` |
| `contracts/src/PetitionRegistry.sol` | `a593c4023fc1ce9c835013a5ad40a310e5bfd032` | `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` |
| `contracts/src/AnonymousMembershipRegistry.sol` | `31835a9feeeff6691335cca655b1f9e31ceba0d6` | `2b883cbca96f074c52d0471aaa62681ae042b8315d5e1260ab114541650c7978` |
| `contracts/src/AdmissionRegistry.sol` | `d406932f0fb9d6a711b5c2fc319d03f3edce7d5c` | `77a9bdca7dc4e04d9c0c37c2529b8ef344fd8924f3ba4cec6c7bc1485d470807` |
| `backend/src/routes/membership.js` | `089960203a7f3c9848fccea22908a98f2cbeae4b` | `fe1990c1435191e6496e2dd08e666f147a51a8ac77218f4c756eba31addf52e3` |
| `backend/src/services/reflect/preparedPaths.js` | `4539c2b798346067665c60b6be65c7727c86944f` | `c9382608e5c3ac3406f2895a01b12d13ce852f6410275ee3ff40fd16cef66593` |
| `backend/src/membership/indexer.js` | `5ecca0f5d5b09f0eae03a11f60a2794d45bd4832` | `e2cdeb3fe1ae9da860af8ac7ba30eec60a5dd1afbfb52a7531c52fd6d441ec49` |
| `backend/src/routes/relay.js` | `23a4d5f37a5dafa2cfd39030e1d42bff9807e3e7` | `1f748b519358c4d4653dfce5d13d6f54cab4a3cd7cb70d8f1937a75a06990f7a` |
| `backend/src/services/indexerFreshness.js` | `cdcf3077e0ab7f231b53726f8eb90bac1a76a0ef` | `66b870d2087ecef424019933e2aa90451244869a6c6929c5e7b595109fd4a794` |
| `backend/src/services/relayExecution.js` | `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` | `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` |
| `backend/src/services/tempestConfig.js` | `3923ff0f3213dd7f1c1d14e1a8d37589d0f25d4f` | `ef1778d8c44568a42a3ac0118564f7d638c54ad9f3b3554dfa4d53fb9903622c` |
| `backend/src/services/tempestDomains.js` | `8b3fb406078f413ac1625ea283aecdee703cd5a3` | `b2254d48517d920f890ee683418c3a76e277f17fa549338ffaa05389af56ac78` |
| `backend/src/indexer/petitions/processor.js` | `b38e89799c61a846025390325f882c2a69ce9759` | `addfa0e87da3c1a94628d30024556fa9ba644df46c78fb27caac7529e18b3437` |
| `backend/src/indexer/petitions/handlers.js` | `4912bfe988996712f700b1506171f6a8e46ba75e` | `f2f7fab14b9c5c310e823c6c8df8556b894792659dc158658ab9289b69ccdcd7` |
| `backend/src/db/repositories/petitions.js` | `5b65178963e1b9f85100c7f8238de4b69737aabe` | `68076c4b5bbd0aa1efc5a5454c180bf9b990af118fda5fc5dc67169babbf828b` |
| `backend/migrations/001_ground_truth_indexer_v0.sql` | `14b61bd874fe48a2957efa73923c5467dc7ccca4` | `8f3c0a70b0a5923efbdffd324a0b1c96e202d40217dcd11ba90a2ec78606d31e` |
| `backend/migrations/002_remove_petition_signature_admission_commitment.sql` | `0ff4dd77d299a8cd03775ab4c308fbf0c7893f1a` | `707eb9396da26a002d6b5c78d928d43a8d37003c300e09f4344814368d3d9d9a` |
| `contracts/test/AnonymousMembershipRegistry.t.sol` | `f2c6f2519935f9f8af482cbcc94a825496c7c7c4` | `438ecdf06f28dae8184514d04d9591d73bfc6862b8fd37aed819750e439fbc77` |
| `contracts/test/PetitionRegistry.SettlementReference.t.sol` | `793c4d3b746d4533d0efb33a2fb729c332f71268` | `689b7f302d502e9b51bbc111bc4cfd2a5f0b17b8d2a65448042e55ac42984b4f` |
| `backend/src/services/tempestExecution.test.js` | `ba2970c8bc858b575091b3fe2643cd6db3ef6e6a` | `d86b8c6237f692c2eeb3113928aa37e1a23c8712909bddc167cb1f85bd414d7f` |
| `zk/v3-groth16/test-golden-proof.js` | `6aebd8f293a8b2f97d266f34084c5e9b6409de5e` | `a2744c49785c905a552e9612f7a4e536e028ea59d5a8ba7978dd534a73b4cbd7` |
| `zk/v3-groth16/test-on-chain.sh` | `04e8e1bc545fd4c87e5f6792b8f960999c68717d` | `a097eccc184fc0489288158df789fd1adb8bef516b7c973c03edf0d6fec93f7a` |
| `contracts/script/UpgradePetitionRegistry.s.sol` | `b696299874b027aba2c7783d8ddeb5cd57658dc1` | `79db955bd2ace55e4e507293f561b4b2dac0591db4e80ac206afe4ce67836e05` |
| `contracts/verify-groth16-verifier.sh` | `55254ced62afe57e06a38079b05b833b3d23c4a8` | `d807e204efbff0120d6bffab005334a60f56f82568e13d0e11891bb5f6eb8bd9` |

The runtime proof artifacts also preserve these exact SHA-256 identities:

| Path | SHA-256 |
|---|---|
| `frontend/public/zk/sign_petition.wasm` | `996ad4bcf08548125ae15fbf98a9748170647d8609bdbade16003c3cd351dcb3` |
| `frontend/public/zk/sign_petition_final.zkey` | `762433cb44fc19ff7ebf575b71f56af75f17b161f87102517a6259086b9b99f1` |
| `frontend/public/zk/verification_key.json` | `8548836eaeb4500e19ca9032852095b257a9a5267206dd4e8180740c8841d14c` |
| `zk/v3-groth16/golden-proof.json` | `01360c724f748b1630b6605bf7464af585643a0d87fcbbb2a21e3fa3025a63b7` |

## 10. Exact Supported Component Ledger

| Component | Exact realization | Supported relationship | Limitation |
|---|---|---|---|
| Witness preparation | `normalizeInputs`; `normalizeMerkleToMatchRoot`; `generateProof` | Local witness, action-context and path material are prepared for proof construction | Pre-Evaluation construction only |
| Circuit proof relation | `MerkleTreeInclusionProof`; `SignPetition` | Leaf derivation, supplied-root inclusion and action-local nullifier derivation are constrained | Supplied-root inclusion is not accepted-root status |
| Verifier-facing values | Circuit output plus public inputs | Active verifier-facing order is `[nullifier, petitionId/actionId, membershipRoot]` | Ordered values do not establish Action identity or complete Evaluation |
| Proof verification | `Groth16Verifier.verifyProof` | Proof and three public signals produce a bounded Boolean verification result | Proof verification is not complete protocol validity |
| Petition existence | `petitions[petitionId].exists` | Application-target existence gates continued execution | No generation-derived formal rule assignment is established |
| Action-local uniqueness | `usedSignNullifier[petitionId][nullifier]` | The same action-local key cannot be used successfully twice | The key is not participant identity or Action-occurrence identity |
| Verifier configuration | `address(groth16Verifier)` guard | An unconfigured verifier blocks execution | Deployment configuration is not automatically protocol validity |
| Proof-result gate | `groth16Verifier.verifyProof(...)` | A false result blocks continued execution | Revert is not a formal Determination |
| Public-nullifier coherence | `uint256(nullifier) == pubSignals[0]` | Function argument and proof signal are bound | Does not define Action identity |
| Public-action coherence | `petitionId == pubSignals[1]` | Action-context value and proof signal are bound | Application-target identity remains distinct |
| Root inclusion | `hashes[nLevels] === root` | Witness membership is proven under the supplied root | Accepted-root status is not established |
| Accepted-root state | `AnonymousMembershipRegistry.isValidRoot`; `isKnownRoot` | Root-history state exists as a readable implementation component | No active signing-path call or state read connects it to Evaluation |
| Membership path preparation | membership indexer, REFLECT preparation and membership routes | Path material can be reconstructed and supplied to local proof preparation | Distribution and reconstruction are operational, not authoritative root evaluation |
| Relay payload gate | `/api/relay/sign` payload and coherence checks | Request shape and selected public fields are checked | Transport validation is not formal Action admission |
| Freshness gate | `getPetitionIndexerFreshness` | Operational state freshness gates relay dispatch | Freshness policy is not a protocol-validity rule |
| Relay used-state check | `hasSignedPetition` | Already-used state can short-circuit dispatch | Operational precheck is not Evaluation or Determination |
| Frozen submission | `freezeRelaySubmission` | Submission representation is preserved for deterministic execution | Frozen representation is not Action identity |
| TEMPEST execution | seed, permutation, domain selection and fallback | Sequential execution and bounded fallback are implemented | Topology and attempts are operational only |
| Reconciliation | `reconcileRelayExecutionState` | Uncertain submission can be reconciled against used state | Observation cannot reconstruct Action occurrence or Determination |
| Mutation and event | uniqueness assignment and `PetitionSigned` | Successful execution records used state and emits a public action observation | Mutation and event are not formal Evaluation or Determination |
| Indexed observation | processor and handler pipeline | Public chain events are normalized and persisted | Observation and persistence are not protocol authority |
| Persistence uniqueness | `(tx_hash, log_index)` and `(petition_id, nullifier)` | Event idempotence and action-local uniqueness are preserved downstream | Database identity is not Action identity |
| Admission separation | ignored compatibility parameter, zero event field and signature-schema migration | Signing does not create admission-to-action linkage | Separation does not establish the complete applicable rule set |
| Tests | contract, proof, membership and execution tests | Individual implementation behaviours and failure paths are represented | Test presence does not prove formal rule identity or rule-set completeness |
| Deployment candidates | manifest, configuration, upgrade and verification scripts | Concrete addresses, artifacts and operations are identifiable | Deployment material is not protocol authority or a complete rule ledger |

## 11. Action-Type Inventory Determination

I164 exposes numerous candidate implementation operations:

- petition creation;
- legacy authorization-based signing;
- ZK-supported signing;
- commenting;
- membership registration;
- admission funding, activation, refund and settlement;
- configuration and upgrade operations;
- proof construction;
- relay request handling;
- transport dispatch and fallback;
- membership-path publication and retrieval;
- indexing and persistence.

Implementation names and entrypoints do not establish which of these are:

- Protocol Operations;
- formal action types;
- Protocol Actions;
- preparatory operations;
- transport operations;
- application operations;
- administrative operations;
- deployment operations;
- or non-protocol implementation machinery.

The accepted A05 mapping evidence preserves:

- `U-ACTION-IDENTITY`;
- `U-ACTION-ADMISSION`;
- `U-RETRY`;
- the absence of a complete formal action-type mapping.

`T-I164-ANONYMOUS-PUBLIC-ACTION` remains an implementation-owner coordinate only. It is not a manufactured protocol subject or formal action type.

Therefore the complete action-type inventory is unresolved.

## 12. Bounded Evaluation-Context Inventory Determination

I164 exposes candidate context coordinates:

- the published protocol generation;
- Complete Implementation Profile V2;
- Aurora chain and deployment configuration;
- PetitionRegistry execution state;
- configured verifier;
- application-target state;
- claimed membership root;
- available root-history state;
- action-local nullifier state;
- relay freshness;
- transport configuration;
- and operational execution state.

These coordinates are not preserved as one complete formal Evaluation context.

No exact I164 representation establishes:

- the complete context identity;
- the Evaluation start boundary;
- the Evaluation completion boundary;
- the authoritative Action-admission boundary;
- the exact protocol-relevant state included in the context;
- the exclusion of operational policy from validity;
- or the rule governing comparison across materially different contexts.

Therefore the complete bounded evaluation-context inventory is unresolved.

## 13. Applicable Rule-Set Determination

I164 contains individual checks, but check presence does not prove applicable-rule-set completeness.

The active path includes:

- petition existence;
- nullifier-unused state;
- verifier configuration;
- proof verification;
- nullifier coherence;
- action-context coherence;
- mutation and event emission.

The circuit includes:

- leaf derivation;
- supplied-root inclusion;
- action-local nullifier derivation;
- domain separation;
- public-input binding.

The active contract path does not evaluate accepted-root state.

No I164 ledger establishes, before authoritative Evaluation begins:

- one formal action type;
- one complete bounded evaluation context;
- every applicable proof requirement;
- every applicable public-input requirement;
- every applicable non-proof validity condition;
- every accepted-root requirement;
- every uniqueness condition;
- every state-relative condition;
- every action-type constraint;
- and every exact rule-to-check assignment.

Engineering[169] accepted exact component mappings and non-mappings, but explicitly preserved `U-RULESET`, `U-ROOT` and `U-PRIVACY-REVIEW`.

No later accepted artifact resolves those relationships.

Therefore the complete applicable rule-set inventory is unresolved.

## 14. Accepted-Root Relationship

The circuit establishes:

> witness path  
> -> computed root  
> -> equality with supplied `membershipRoot`

`AnonymousMembershipRegistry` separately exposes:

> claimed root  
> -> `isKnownRoot` / `isValidRoot`  
> -> accepted-root-state result

`PetitionRegistry.signPetitionWithZKProof` contains no call or state read connecting these relationships.

Therefore:

> supplied-root inclusion  
> != accepted-root status

Accepted-root status cannot be inferred from:

- proof success;
- the existence of `isValidRoot`;
- backend path reconstruction;
- frontend preflight;
- documentation;
- deployment proximity;
- or naming.

The missing active relationship remains material to `PE-VALID-003`, `PE-VALID-005`, `PE-VALID-006`, `PE-VALID-007`, `PE-VALID-009`, `PE-RULE-001`, `PE-RULE-002`, `PE-RULE-003`, `PE-RULE-004`, `PE-RULE-006`, `PE-RULE-007`, `PE-RULE-008` and `PE-RULE-012`.

## 15. Artifact and Deployment Binding Observations

The I164 artifact manifest is an exact tracked candidate, but it does not supply a complete I164 rule or deployment binding.

Exact observations:

1. `baseline_anchor_tag` identifies `baseline-v0`, not I164.
2. `baseline_anchor_commit` identifies `e02aacdc0f10e6919d8a759d8829758b58e0367e`, not the I164 commit.
3. The manifest declares public-input order `petitionId`, `nullifier`, `membershipRoot`.
4. The active circuit/verifier-facing order is `nullifier`, `petitionId/actionId`, `membershipRoot`.
5. The manifest names canonical R1CS, WASM and ZKey paths that are not tracked in the I164 archive.
6. The runtime frontend WASM and ZKey copies are tracked and match their declared artifact hashes.
7. The manifest golden-proof SHA-256 differs from the archived I164 golden-proof SHA-256.
8. The manifest proof-hook SHA-256 differs from the archived I164 proof-hook SHA-256.
9. The manifest sign-button SHA-256 differs from the archived I164 sign-button SHA-256.

These are source-mapping observations only.

They do not determine:

- an implementation defect;
- evidence availability or sufficiency;
- requirement satisfaction or failure;
- security;
- compatibility;
- conformance;
- certification;
- or operational readiness.

They prevent the manifest from being promoted into a complete exact I164 action-type, rule-set or Evaluation-context ledger.

## 16. Exact Non-Mappings

The following exact non-mappings are preserved:

1. formal protocol rule `!=` implementation check;
2. successful proof verification `!=` complete Protocol Action Evaluation;
3. proof-valid `!=` protocol-valid;
4. protocol-valid `!=` Action acceptance;
5. protocol-valid `!=` Action rejection;
6. protocol-valid `!=` transition authorization;
7. protocol-valid `!=` transition execution;
8. protocol-valid `!=` commitment;
9. implementation entrypoint `!=` formal action type;
10. relay receipt `!=` authoritative Action admission;
11. payload validation `!=` authoritative Action admission;
12. indexer freshness `!=` protocol-validity rule;
13. relay dispatch `!=` authoritative Action admission;
14. contract entry `!=` authoritative Action admission;
15. guard success `!=` complete Evaluation;
16. revert `!=` formal rejection Determination;
17. state mutation `!=` formal Determination;
18. event `!=` formal Determination or Published Result;
19. response `!=` formal Determination;
20. diagnostic `!=` formal Determination;
21. persisted row `!=` formal Determination or protocol authority;
22. supplied-root inclusion `!=` accepted-root status;
23. application meaning `!=` protocol rule or validity;
24. deployment state `!=` protocol rule identity;
25. operational policy `!=` protocol rule identity;
26. rate-limit identity `!=` actor or Action identity;
27. relayer wallet `!=` Private Actor identity;
28. seed, slot and domain `!=` Action identity or provenance;
29. transaction hash `!=` Action identity;
30. event coordinates `!=` Action identity;
31. database key `!=` Action identity;
32. admission compatibility syntax `!=` action identity;
33. admission state `!=` signing identity;
34. `(petitionId/actionId, nullifier)` `!=` reusable participant identity;
35. test presence `!=` applicable-rule-set completeness;
36. runtime observation `!=` protocol authority.

## 17. Privacy and Neutral-Naming Review

The candidate surfaces were reviewed across:

- names;
- fields;
- comments;
- tests;
- logs;
- diagnostics;
- routes;
- persistence;
- deployment material;
- and documentation.

The preserved privacy rule is:

**Private actors, public actions.**

The exact supported privacy relationships are:

- `memberSecret` remains private proof-construction material;
- the nullifier is derived with the action-context value and `SIGN_DOMAIN`;
- uniqueness state is keyed by `(petitionId/actionId, nullifier)`;
- the nullifier is not promoted into actor identity;
- the ignored admission compatibility field is emitted as zero;
- the signing indexer omits admission commitment;
- the signature schema removes the admission-commitment column;
- relay success and error logs omit submission fields and topology;
- application, transport, transaction, event and persistence coordinates remain role-bounded.

Operational IP keys, relayer wallets, topology, transaction coordinates, event coordinates, database coordinates and application state are excluded from formal rule identity, Action identity and actor identity.

These exact class-specific boundaries do not prove complete baseline-wide negative-obligation coverage while the positive Action, action-type, Evaluation-context and applicable-rule-set identities remain unresolved.

No actor identity, wallet identity, sponsor identity, funding identity, admission identity, transport identity, topology identity or cross-action identity is introduced by this determination.

## 18. Material Unresolved Relationships

The material unresolved relationships are:

| Relationship | Unresolved basis |
|---|---|
| Complete formal action-type inventory | Implementation operations are not exhaustively classified as formal action types |
| Protocol Action occurrence identity | Accepted A05 work preserves `U-ACTION-IDENTITY` |
| Authoritative Action admission | Accepted A05 work preserves `U-ACTION-ADMISSION` |
| Repeated-presentation equivalence | Accepted A05 work preserves `U-RETRY` |
| Complete bounded Evaluation context | No distinct complete context identity or boundary is represented |
| Complete applicable rule set | `U-RULESET` remains unresolved |
| Accepted-root evaluation | `U-ROOT` remains unresolved |
| Complete proof-rule inventory | Individual proof components exist without complete action/context assignment |
| Complete non-proof-rule inventory | Individual guards exist without generation-derived completeness |
| Exact rule-to-check assignment | Several checks have no exact formal rule assignment |
| Evaluation start and completion | No authoritative boundaries are declared |
| Complete validity basis | Proof and non-proof components are not composed into complete RF-18 validity |
| Cross-context validity comparison | No complete bounded relationship resolves `PE-RULE-013` |
| Complete negative-obligation coverage | Class-specific exclusions cannot establish universal coverage |
| Complete privacy-surface review | `U-PRIVACY-REVIEW` remains material |
| Complete deployment binding | Candidate bindings do not form one exact current I164 rule/context ledger |
| Formal Determination identity | Revert, mutation, event, response and persistence cannot manufacture it |

Each unresolved relationship independently prevents complete construction where it is required.

## 19. Completeness Matrix

| Required construction term | Engineering[193] result |
|---|---|
| Complete action-type inventory | unresolved |
| Complete bounded evaluation-context inventory | unresolved |
| Complete applicable rule-set inventory | unresolved |
| Complete proof-rule inventory | partially supported; incomplete |
| Complete non-proof-rule inventory | partially supported; incomplete |
| Exact rule-to-implementation assignments | incomplete |
| Exact rule-context relationships | incomplete |
| Exact candidate anchors | verified |
| Complete negative-obligation coverage | incomplete |
| Privacy-preserving representation boundaries | exact individual boundaries supported; complete coverage unresolved |

Construction of isolated mappings does not establish a complete A04 package.

Exact supported components and exact non-mappings remain available as bounded mapping evidence only.

They do not constitute partial terminal acceptance and do not transition an evidence path.

## 20. Row-State Preservation

The nine reviewed-current bounded A04 rows remain bounded:

- `PE-VALID-001`;
- `PE-VALID-002`;
- `PE-VALID-004`;
- `PE-VALID-008`;
- `PE-VALID-010`;
- `PE-VALID-011`;
- `PE-RULE-009`;
- `PE-RULE-010`;
- `PE-RULE-011`.

The 16 selected A04 rows remain `still-ambiguous`:

- `PE-VALID-003`;
- `PE-VALID-005`;
- `PE-VALID-006`;
- `PE-VALID-007`;
- `PE-VALID-009`;
- `PE-VALID-012`;
- `PE-RULE-001`;
- `PE-RULE-002`;
- `PE-RULE-003`;
- `PE-RULE-004`;
- `PE-RULE-005`;
- `PE-RULE-006`;
- `PE-RULE-007`;
- `PE-RULE-008`;
- `PE-RULE-013`;
- `PE-RULE-012`.

No A04 evidence-path transition occurs.

All non-A04 rows remain unchanged.

The reviewed-current totals remain:

| State | Rows |
|---|---:|
| bounded | 217 |
| still-ambiguous | 268 |
| missing-evidence-path | 0 |
| not-required | 244 |
| total | 729 |

## 21. Scope and Non-Effects

Engineering[193] does not:

- modify Engineering[169] through Engineering[174];
- modify Engineering[189] through Engineering[192];
- reopen or weaken a bounded A04 row;
- perform evidence-path reclassification;
- transition an A04 row;
- alter a non-A04 row;
- resolve A05 through A20;
- manufacture a formal rule identity;
- manufacture an action type;
- manufacture an Evaluation context;
- manufacture an applicable rule set;
- infer rule-set completeness from check presence;
- equate proof verification with protocol validity;
- equate protocol validity with acceptance;
- equate validation with authoritative Action admission;
- equate a revert, mutation, event, response or diagnostic with Determination;
- determine evidence availability or sufficiency;
- perform requirement assessment;
- produce a requirement result;
- determine an implementation defect;
- perform a security assessment;
- determine compatibility, conformance, certification or readiness;
- modify `STATE.md`;
- modify Profile V2;
- modify I164;
- modify implementation code;
- create Profile V3;
- create a protocol generation;
- create a publication occurrence;
- create deployment or runtime evidence;
- encode actor identity or provenance;
- introduce wallet, sponsor, funding, admission, transport, topology or cross-action linkage;
- or imply that Speak-up-appV3 defines or owns the Privacy Engine.

## 22. Canonical Determination Payload

The canonical determination payload is the exact UTF-8 sequence from the begin marker through the end marker, inclusive, joined by LF characters with no trailing LF:

canonical-determination-payload-begin
format=PRIVACY-ENGINE-I164-A04-VALIDITY-RULE-RULE-SET-ACTION-TYPE-EVALUATION-CONTEXT-MAPPING-DETERMINATION/1
engineering-slice=193
determination-date=2026-08-27
protocol-authority=published-privacy-engine-protocol-generation
implementation-subject=Speak-up-appV3-I164
implementation-is-protocol=no
formal-corpus-sha256=fca8619d2b215c14869e0dd7c5573d907dbddc930d49f53db112303c4fd54dd2
formal-corpus-files=112
formal-corpus-git-archive-comment=3bc4086267e37384cb19d244f56ebfe177a74666
implementation-archive-sha256=7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847
i164-commit=003e984ea73a2dede092443893dfbc9e74121e14
i164-tree=6271b80f2fa6167961e18c5b4c229d25374497a7
i164-parent=5e12cca624ffccf43637de4b9dc42de4af3979bc
i164-tracked-paths=308
i164-blobs=305
i164-gitlinks=3
git-provenance-format=PRIVACY-ENGINE-HANDOVER-GIT-PROVENANCE/1
git-provenance-records=25
git-provenance-sha256=0042328fb7567ef9dfbd25e67564021523d1fd738d49483dc48e30f0b9c67f39
all-provenance-raw-commit-identities=reproduced
all-supplied-engineering-tag-local-remote-relationships=match
generic-tag-ref-in-provenance=none
engineering-192-commit=3bc4086267e37384cb19d244f56ebfe177a74666
engineering-192-raw-commit-payload-length=291
engineering-192-artifact-sha256=874f8dc5c32f4f89e23441dcb897251621e164c4ddc9dc36f26358105b8be833
engineering-192-canonical-rereview-payload-length=6324
engineering-192-canonical-rereview-payload-sha256=5e9175730af337ba46911ba11c3d477c6f893b6e68f70f809ef9c6a2f7c4b3b3
engineering-192-final-review-result=accepted
reviewed-current-evidence-path-basis=engineering-187-accepted-by-engineering-188
reviewed-current-totals=217/268/0/244
selected-group=A04
selected-rows=16
guarded-a04-rows=25
guarded-profile-row-hashes-verified=25
guarded-order-preserved=yes
pe-rule-013-before-pe-rule-009=yes
preserved-bounded-a04-rows=PE-VALID-001,PE-VALID-002,PE-VALID-004,PE-VALID-008,PE-VALID-010,PE-VALID-011,PE-RULE-009,PE-RULE-010,PE-RULE-011
selected-still-ambiguous-a04-rows=PE-VALID-003,PE-VALID-005,PE-VALID-006,PE-VALID-007,PE-VALID-009,PE-VALID-012,PE-RULE-001,PE-RULE-002,PE-RULE-003,PE-RULE-004,PE-RULE-005,PE-RULE-006,PE-RULE-007,PE-RULE-008,PE-RULE-013,PE-RULE-012
complete-action-type-inventory=no
complete-bounded-evaluation-context-inventory=no
complete-applicable-rule-set-inventory=no
complete-proof-rule-inventory=no
complete-non-proof-rule-inventory=no
exact-rule-to-implementation-assignments=partial
exact-rule-context-relationships=partial
exact-candidate-anchors=verified
complete-negative-obligation-coverage=no
privacy-preserving-individual-boundaries=yes
u-action-identity=unresolved
u-action-admission=unresolved
u-retry=unresolved
u-ruleset=unresolved
u-root=unresolved
u-privacy-review=unresolved
private-actors-public-actions=preserved
actor-identity-or-provenance-introduced=no
a04-evidence-path-transition-performed=no
non-a04-row-modified=no
evidence-availability-determined=no
evidence-sufficiency-determined=no
requirement-assessment-performed=no
requirement-result-produced=no
implementation-defect-determined=no
security-assessment-performed=no
compatibility-conformance-certification-or-readiness-determined=no
final-mapping-determination=complete-selected-a04-mapping-package-not-constructible
canonical-determination-payload-end

## 23. Final Mapping Determination

I164 supplies exact circuit constraints, verifier checks, public-input relationships, contract guards, state reads, uniqueness state, relay validation, execution machinery, tests, deployment candidates and bounded observations.

Those components do not establish:

- one complete formal action-type inventory;
- one complete bounded Evaluation-context inventory;
- one complete generation-derived applicable rule set;
- complete proof and non-proof rule inventories;
- or complete exact rule-to-realization and rule-to-context relationships.

At least one required relationship remains unresolved. In fact, multiple independently necessary relationships remain unresolved.

Therefore the one permitted Engineering[193] result is:

**complete selected A04 mapping package not constructible**

No evidence-path transition occurs.

The nine reviewed-current bounded A04 rows remain bounded.

The 16 selected A04 rows remain `still-ambiguous`.

All non-A04 rows and the reviewed-current totals remain unchanged.

No requirement assessment was performed.

No requirement result was produced.

Protocol authority remains with the published Privacy Engine protocol generation.
