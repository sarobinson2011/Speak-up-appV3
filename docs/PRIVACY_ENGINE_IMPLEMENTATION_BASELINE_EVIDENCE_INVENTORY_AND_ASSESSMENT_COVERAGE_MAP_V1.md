# Privacy Engine Implementation Baseline Evidence Inventory and Assessment Coverage Map V1

Inventory date: 2026-08-15.

STATE.md remains the single canonical development authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

## 1. Purpose and Status

This record inventories the fixed engineering-164 implementation baseline and maps every accepted Complete Implementation Profile V2 row to a bounded later evidence treatment.

It answers one architectural question:

> Does the tracked engineering-164 implementation baseline contain one identifiable, bounded, and privacy-safe evidence path for every Profile V2 requirement that must later be assessed?

Determination status: **evidence inventory and assessment coverage map completed**.

Assessment-readiness status: **not yet ready for requirement-level assessment because identified evidence paths remain ambiguous**.

This is an evidence-availability record. It assigns no requirement result and determines no implementation defect.

## 2. Plain-Language Position

Profile V2 fixes what must later be checked. engineering-164 fixes which tracked implementation is the subject. This record identifies where later evidence may come from and where the implementation-to-requirement evidence relationship is still ambiguous.

A source file, test, generated artifact, deployment, or runtime observation is only a candidate evidence item. Its existence does not establish requirement satisfaction.

## 3. Authority and Preservation

> Published Protocol Generation -> Published Protocol Specification V1 -> Complete Implementation Profile V2 -> engineering-164 implementation baseline -> later assessment

No downstream item acquires authority over an upstream item. This record does not modify STATE.md, Profile V2, the published specification, the baseline tree, or any implementation material.

## 4. Guarded Formal Baselines

| Artifact | SHA-256 |
|---|---|
| STATE.md | `228886af0db33a801db40d834c1a1070ed8f330d6708d8e6674021e3a2d3be33` |
| docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2.md | `279fc80cb2998df8c4fddcc2ea25e4091897571c57a7d5905100857612b2d79c` |
| docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2_IMPLEMENTATION_ASSESSMENT_BASIS_AND_SCOPE_DETERMINATION_V1.md | `a3547f19e187cb9b0c5493c75832a9bebd95c2462387cdc120907fc413ce89af` |
| docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2_STATUS_SYNCHRONIZATION_V1.md | `d8bce61c2366e4a5ca6d6d87ef4875944956acd1b8303e73f2f901c7a1ba1e27` |
| docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2_COMPOSITION_REREVIEW_V1.md | `093f3d2178bc890e7bed9dc56aea164f36918a01e49caef2ed8d777777dd0d11` |
| docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_IDENTITY_VERSION_CORRECTION_V1.md | `c37a3fa1985a11243ff0b1103d5d7ca911f77e76a14f00f4c12a368e4f7ad88a` |
| docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V1.md | `2570e94fa7d06a3f136b5384bd879e343a25bbb33c3b4fc3f7c9ee0ecb1b9b23` |
| docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_COMPOSITION_REREVIEW_V1.md | `fe51c48bb7992482ca341af943b396b46457773999452d1cfb2a02807557bc41` |
| docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_COMPOSITION_CORRECTION_V1.md | `6c8cbe0ffe6687045375f33c2316a1baf8ee1d026cfde1bfdc258769d70d4b26` |
| docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_COMPOSITION_REVIEW_V1.md | `5855fa1765a8492e08f7718c7c6b7d400fff343e03caa666f9a5fdeaa6184709` |
| docs/PRIVACY_ENGINE_IMPLEMENTATION_PROFILE_SCOPE_DETERMINATION_V1.md | `03fe5d180a4056c6e66356c1804f8883006daab52a80ec12676483ad75fd0a17` |
| docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_V1.md | `f2c12b60f24fe8fe8eddf27dc2d59814aceba42b907160c54ad3868bde7da393` |
| docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_PUBLICATION_RECORD_V1.md | `d655359c296d6d6aefffd3e6faa0fd47f6506ec9d64a871ade9f9eb469108029` |
| docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_FINAL_CONSOLIDATION_REREVIEW_V1.md | `7bf415870a2e630157d1cf186e45764513e87b5f13b2ac790373d4de5df13bb7` |

The published specification retains 729 byte-identical normative rows, 729 unique identifiers, the guarded ordered identifier sequence, the guarded 715-row unchanged set, and the guarded Sections 3, 8, and 38.

## 5. Fixed Implementation Baseline

| Baseline field | Fixed value |
|---|---|
| Repository | Speak-up-appV3 |
| Tag | `engineering-164` |
| Commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Git tree | `6271b80f2fa6167961e18c5b4c229d25374497a7` |
| Tracked paths | 308 |
| Blob paths | 305 |
| Gitlink paths | 3 |
| Supplied formal-corpus archive SHA-256 | `e8a82a1f1016b886712a588ac6c457e0fc742521cfd1a489897bac27aed7b311` |
| Supplied implementation archive SHA-256 | `7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847` |
| Supplied implementation archive embedded commit | `003e984ea73a2dede092443893dfbc9e74121e14` |
| Competing implementation branch | None selected |

The commit and tree identify the baseline. Deployment and runtime instances remain later evidence associated with that baseline; they are not baseline identity.

## 6. Inventory Classification

Responsibility follows actual bounded responsibility rather than directory, filename, framework, or Speak-up terminology. `mixed` means one tracked item contains both included protocol-facing and excluded application-owned or operational responsibility. `ambiguous-status` preserves a tracked item whose current responsibility cannot be silently inferred.

| Responsibility classification | Paths |
|---|---:|
| ambiguous-status | 2 |
| application-owned | 22 |
| dependency | 3 |
| evidence-support | 104 |
| historical-inactive | 9 |
| mixed | 65 |
| protocol-facing | 103 |

| Material kind | Paths |
|---|---:|
| Git dependency link | 3 |
| application documentation | 2 |
| application presentation asset | 9 |
| application source | 9 |
| bounded implementation documentation | 51 |
| build or dependency input | 18 |
| circuit source | 1 |
| client interface and runtime source | 3 |
| client runtime source | 3 |
| configuration and runtime source | 1 |
| configuration schema | 1 |
| contract source | 10 |
| deployment or verification operation | 23 |
| formal or boundary documentation | 83 |
| generation or verification operation | 6 |
| historical source or operation | 9 |
| indexer source | 14 |
| integrity manifest | 1 |
| interface and runtime source | 4 |
| operational documentation | 3 |
| persistence migration | 3 |
| persistence source | 6 |
| runtime integration source | 1 |
| runtime source | 13 |
| sample interface payload | 1 |
| test | 17 |
| tracked generated cryptographic artifact | 6 |
| tracked runtime snapshot | 1 |
| tracked source with unresolved current responsibility | 2 |
| utility contract source | 1 |
| verification operation | 2 |
| verification support contract | 1 |

These classifications inventory candidate evidence responsibility only. They do not establish correctness, completeness, currency, or sufficiency.

## 7. Complete Tracked-Path Inventory

Every engineering-164 tree entry appears exactly once. Blob SHA-256 is supplemental integrity information; Git object identity and the guarded tree remain the baseline identity.

| Mode | Type | Git object | Path | Blob SHA-256 | Responsibility | Material kind | Candidate evidence classes |
|---|---|---|---|---|---|---|---|
| 100644 | blob | `6b67d1d1563d47c2269ddbfba843d948f241f9fd` | `.gitignore` | `1c9c671faecc440d547b8ddd7997ff2a3f2b03ace8886bcce1f39fae62f125bb` | evidence-support | build or dependency input | TD |
| 100644 | blob | `39b76486335a823222cc869f5d1f7ba91345fda6` | `.gitmodules` | `c9f9b70344fc73f3d0e42f0d75dfe219a98657867323aa8fe92355e1e2d38737` | evidence-support | build or dependency input | TD |
| 100644 | blob | `7c07326d9df12077575f2ac9ebabcb4367a20732` | `CORE-LOOP.txt` | `11687ffbc006686afd2708f77612437ebd6311a4d15457d60511c4e364317795` | mixed | bounded implementation documentation | BD |
| 100644 | blob | `2a15ceb580f4bccdfcddd41ca861ec58023d732a` | `README.md` | `41bbcfd9f938efa2afb1f589058b8601873b30f5344c6f8936d5b9905dccb88c` | mixed | bounded implementation documentation | BD |
| 100644 | blob | `5b774d901d58b4e04e2e09b575a5ad71fc4811f2` | `STATE.md` | `228886af0db33a801db40d834c1a1070ed8f330d6708d8e6674021e3a2d3be33` | mixed | bounded implementation documentation | BD |
| 100644 | blob | `e7bd40673ccad23283182a27c129c240807287be` | `ZK_ARTIFACTS_MANIFEST.json` | `e048ca3b210a4d40c8ff722a8ec5e793e1f340965c2bc6867287bc4dedaec896` | protocol-facing | integrity manifest | TD,RG |
| 100644 | blob | `56f300f016828a2fd56b82caafe8dba6438c02e7` | `backend/.env.example` | `05a398abb5511846c496359d01539026f5774104a46e5c9c56659ed525d54de3` | mixed | configuration schema | TD,DB |
| 100644 | blob | `1c463625e7444599d1a2b0d59ca73d9d508757cb` | `backend/data/state.json` | `16f17f0f875a8823bc66be2b321eeed52ecb74cc802e3fc8f8349d2879f1b211` | application-owned | tracked runtime snapshot | TD,AE |
| 100644 | blob | `14b61bd874fe48a2957efa73923c5467dc7ccca4` | `backend/migrations/001_ground_truth_indexer_v0.sql` | `8f3c0a70b0a5923efbdffd324a0b1c96e202d40217dcd11ba90a2ec78606d31e` | mixed | persistence migration | TD,RO |
| 100644 | blob | `0ff4dd77d299a8cd03775ab4c308fbf0c7893f1a` | `backend/migrations/002_remove_petition_signature_admission_commitment.sql` | `707eb9396da26a002d6b5c78d928d43a8d37003c300e09f4344814368d3d9d9a` | mixed | persistence migration | TD,RO |
| 100644 | blob | `b62d906e1ed0ba87c5bf8cef15339076ed7e5243` | `backend/migrations/003_add_petition_active_flag.sql` | `648492f91a83e75153770beff8d92f21c8c448b6742082d0ff64862bf31ad6ed` | mixed | persistence migration | TD,RO |
| 100644 | blob | `eb61db89cecad37c1cf4bdc8ead3b1ab7f16df89` | `backend/package-lock.json` | `0bccf0e5c072382f0b7eacef672f2b28349f57d9d135bb0100c6cdeb7c854c06` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `b1b8675c24ef875a6a683f608f6108a152d7c61b` | `backend/package.json` | `fbbd950ad49d5a459aee0df1e64f8109ba74e35e968a0f0452de75ff15d5fc7f` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `c81ab1d8a7985bc6fb274c0c04a83c99d9a74621` | `backend/src/db/connection.js` | `954316cd8d1a96b3afe25fd723f4cc8016816bc363f3d03b1c9683ce772ec650` | mixed | persistence source | TD,RO |
| 100644 | blob | `dd4cee3450de65d18812696f09c3cde419837217` | `backend/src/db/migrate.js` | `675143510f6bb51b1df5625cc232a178e0ba81297e4847f5fc59bfa936c195d7` | mixed | persistence source | TD,RO |
| 100644 | blob | `5ba3ec51d9f4d14ce8e23dd8675da933d75feb40` | `backend/src/db/repositories/admission.js` | `34ed33d1bd9fa53c9f076510a8e25a761dcbddf981867d8060d50caf02ac6e7e` | mixed | persistence source | TD,RO |
| 100644 | blob | `90f6ea039850b58f858fc1b79d8f16d285371d5c` | `backend/src/db/repositories/membership.js` | `6d094ce44b0c662ba52069cd20fe52b0f90d3bf02d941156b9e3f69e58d35c40` | protocol-facing | persistence source | TD,RO |
| 100644 | blob | `5b65178963e1b9f85100c7f8238de4b69737aabe` | `backend/src/db/repositories/petitions.js` | `68076c4b5bbd0aa1efc5a5454c180bf9b990af118fda5fc5dc67169babbf828b` | mixed | persistence source | TD,RO |
| 100644 | blob | `7f47bad8336450d7d8c7fcc04cb7a0e3f4039d36` | `backend/src/db/repositories/syncState.js` | `e18038deb6a862a5b2e2d2751e9855d85f39a6365409748e478eca0de97a5411` | mixed | persistence source | TD,RO |
| 100644 | blob | `5727b8cdd813aec671d82e033494e200fa5fc399` | `backend/src/indexer/admission/handlers.js` | `d00f3363fe89c5863ddcff3a585828feeeb0cae702c585a1b78d9b04bffd42bf` | mixed | indexer source | TD,RO |
| 100644 | blob | `ab23dbdd813e286dacf55f64f43219281a14c7fc` | `backend/src/indexer/admission/processor.js` | `780bcc8d4d5909d315e475cd6e8aca42e08a56ba0a59e6bdafb0a70e4a93f411` | mixed | indexer source | TD,RO |
| 100644 | blob | `44b022da62e49234b274b9b905d3f6c97f544b93` | `backend/src/indexer/admission/sync.js` | `43fa83ab65b24eba4352201a718ce5910c9fc0d8ce9814b76924be49d16f300d` | mixed | indexer source | TD,RO |
| 100644 | blob | `21051c2544062e7fefea4ab2474b124b2c1d148f` | `backend/src/indexer/membership/handlers.js` | `8a7e53aaba8c9239558d63b9e9ff83a9619abc0fbf8faa10913b1fc52c04a8e8` | protocol-facing | indexer source | TD,RO |
| 100644 | blob | `ca318d177ef82d1f0806e1bad8befbfecae1e903` | `backend/src/indexer/membership/processor.js` | `edc465f9ed468ef4a28b1ced64f470c02b4e84e292940f203a3fdf4a080fd99c` | protocol-facing | indexer source | TD,RO |
| 100644 | blob | `f9ed554f9686a490e63151a01e60b57943a88f82` | `backend/src/indexer/membership/sync.js` | `a79f991cc4209d60e5ec9f71774ef502a965edab8a16c91f000f7634f74bb68c` | protocol-facing | indexer source | TD,RO |
| 100644 | blob | `4912bfe988996712f700b1506171f6a8e46ba75e` | `backend/src/indexer/petitions/handlers.js` | `f2f7fab14b9c5c310e823c6c8df8556b894792659dc158658ab9289b69ccdcd7` | mixed | indexer source | TD,RO |
| 100644 | blob | `b38e89799c61a846025390325f882c2a69ce9759` | `backend/src/indexer/petitions/processor.js` | `addfa0e87da3c1a94628d30024556fa9ba644df46c78fb27caac7529e18b3437` | mixed | indexer source | TD,RO |
| 100644 | blob | `60c36d8e449fbdc0242266c66d324e2658493d72` | `backend/src/indexer/petitions/sync.js` | `7735ec9432d83595fd5d662036b09fe26123c1252740b4757a5664debd813fc1` | mixed | indexer source | TD,RO |
| 100644 | blob | `1300197b00ff7a61fc6323b6a6df29c897752391` | `backend/src/indexer/reconcilePetitionExistence.js` | `4637cd6f92af69c4a289eda4e779de65b40ffcb20406cffd2ef1855f283826ce` | mixed | indexer source | TD,RO |
| 100644 | blob | `a4810c740ffa6845dc04f5d9bfcb1b04543793e4` | `backend/src/indexer/runAdmissionSync.js` | `753fd6963df8854caac28afe69c67b81ce5e2c6136d4a5a29c3d606fd733d165` | mixed | indexer source | TD,RO |
| 100644 | blob | `bd13b1cdb93ca7d3ee22e42a13e73d90f4a1a79f` | `backend/src/indexer/runMembershipSync.js` | `05683e554ed291fbe5188b20ad83673ecabb7fbad9b739f3ab93677e75cb8c33` | protocol-facing | indexer source | TD,RO |
| 100644 | blob | `9dacf6c3cb26c9ca9ffb8b7482ed6cefd49874c7` | `backend/src/indexer/runPetitionSync.js` | `774eaa2c16f993ebce938f9c552a1e3c7cb661d9707507eccabb155114317ee2` | mixed | indexer source | TD,RO |
| 100644 | blob | `05fd04f7376ba647aa706f42649f6795d46f0d2a` | `backend/src/indexer/runPetitionSyncLoop.js` | `352fc45c32880c180dbba5e787542faddeeb7524ddd2ae1c5221dc7960fab5eb` | mixed | indexer source | TD,RO |
| 100644 | blob | `5ecca0f5d5b09f0eae03a11f60a2794d45bd4832` | `backend/src/membership/indexer.js` | `e2cdeb3fe1ae9da860af8ac7ba30eec60a5dd1afbfb52a7531c52fd6d441ec49` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `465f4b16a2df7de87d3339f6f4dfd6bbfb92788c` | `backend/src/membership/tree.js` | `c3209eab56e74e5e91dd4006891c4cd95dff00d1e0f423b2b468165e439038bc` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `8bbf1a89de9636b15f5a8bf1c920996e3bf9ae1d` | `backend/src/routes/admission.js` | `2eb0e711bbdc87cce7c8088b73f5bc0adaa3d79e472d1be541d7128054db717a` | mixed | interface and runtime source | TD,RO |
| 100644 | blob | `5bba1dff875b82bef073dc4a4ee96b2786f9ec95` | `backend/src/routes/indexer.js` | `1f78db0a184a43c153b64b8691579eb989e9aedf0b3536037f5b508bc5666348` | mixed | interface and runtime source | TD,RO |
| 100644 | blob | `089960203a7f3c9848fccea22908a98f2cbeae4b` | `backend/src/routes/membership.js` | `fe1990c1435191e6496e2dd08e666f147a51a8ac77218f4c756eba31addf52e3` | mixed | interface and runtime source | TD,RO |
| 100644 | blob | `d5eed0799b1e6f69aebe398a33e9e1ec4f070ef9` | `backend/src/routes/petitions.js` | `212c4c2bc6cca17e2e41aa90a71646ce5322631bf5363c6381dba535f15ceeee` | application-owned | application source | TD |
| 100644 | blob | `23a4d5f37a5dafa2cfd39030e1d42bff9807e3e7` | `backend/src/routes/relay.js` | `1f748b519358c4d4653dfce5d13d6f54cab4a3cd7cb70d8f1937a75a06990f7a` | mixed | interface and runtime source | TD,RO |
| 100644 | blob | `9835d76b732d2256bc25e160f292e7c7b040ce49` | `backend/src/server.js` | `125493710dd7b9950b8ddd8b9edfa86b1719308a5e72165b13c76664ad3d756a` | mixed | runtime integration source | TD,RO |
| 100644 | blob | `cdcf3077e0ab7f231b53726f8eb90bac1a76a0ef` | `backend/src/services/indexerFreshness.js` | `66b870d2087ecef424019933e2aa90451244869a6c6929c5e7b595109fd4a794` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `a2f91b3216ccd41906efcfe56bcafbc43cade2d8` | `backend/src/services/reflect/acquisition.js` | `298c1c75c32233e7148dd3e9416501af7889befce701dc1602f6851dbe7d43d3` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `bed7f12804681e9f8f81033a9529f41cdaca0597` | `backend/src/services/reflect/acquisition.test.js` | `1bdf9aebf9a9e0b8dfba3b40814cb0d26077c902c02bb8a961ff7d72644cbd41` | protocol-facing | test | TD,RG |
| 100644 | blob | `55c6c66098437e23b2bae9b4ba36e55bc2281945` | `backend/src/services/reflect/materials.js` | `c72655cfed243f82135be7d16413462b94e0d9a7cd04293b7e8acfdaa4f8bc99` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `ef2bb3d9d90a13b399c51c8bb453b3f2c7e9f4ec` | `backend/src/services/reflect/objectModel.js` | `779b070bcea3967873ea021f180ef3aca831784723645ad7d6d2fb130c47ce64` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `4539c2b798346067665c60b6be65c7727c86944f` | `backend/src/services/reflect/preparedPaths.js` | `c9382608e5c3ac3406f2895a01b12d13ce852f6410275ee3ff40fd16cef66593` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `b9697fb4b00717e2d1e24eb6376a9a90969a6395` | `backend/src/services/reflect/publicationObjects.js` | `54a5042d7471190d0efcef3f1427f2dea261a08d9711184f6d1ee5bb8b83955c` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `67d33e6b193274f40b9b8196efa49f22bf7a5902` | `backend/src/services/reflect/publicationObjects.test.js` | `579f40a72319c50691e4d2e59d7f92b6636cdf456017f482971c6c7de4a66130` | protocol-facing | test | TD,RG |
| 100644 | blob | `2a71570e7ea33e24e0477527e25542f6886874ed` | `backend/src/services/reflect/publicationWindows.js` | `d9c5fd8d8d4e174aa1ed279a292916e7cd12864a3432fb2827c7aff64639eec0` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `fba7e565fa15ed75a34b7119f199a6375c90fda0` | `backend/src/services/reflect/publicationWindows.test.js` | `111bd051008f1a2aac42d49865f209ee4d11fc56288152a553d67209fb92d402` | protocol-facing | test | TD,RG |
| 100644 | blob | `082255fd5c9224bbb80699633b2d260b6d5dd7af` | `backend/src/services/reflect/retrievalProvider.js` | `ce5cf02c981f372e34007e472dd94bc57136026617b316c0024dbba9bb9481c1` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `e4aea822d1310a878d99e89312bbb67da144b14e` | `backend/src/services/reflect/retrievalProvider.test.js` | `92f86500f3ce5d29e2d6e307bc58988dce6191f28ba231881d93d212ffbbd9df` | protocol-facing | test | TD,RG |
| 100644 | blob | `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` | `backend/src/services/relayExecution.js` | `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `3923ff0f3213dd7f1c1d14e1a8d37589d0f25d4f` | `backend/src/services/tempestConfig.js` | `ef1778d8c44568a42a3ac0118564f7d638c54ad9f3b3554dfa4d53fb9903622c` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `8b3fb406078f413ac1625ea283aecdee703cd5a3` | `backend/src/services/tempestDomains.js` | `b2254d48517d920f890ee683418c3a76e277f17fa549338ffaa05389af56ac78` | protocol-facing | runtime source | TD,RO |
| 100644 | blob | `ba2970c8bc858b575091b3fe2643cd6db3ef6e6a` | `backend/src/services/tempestExecution.test.js` | `d86b8c6237f692c2eeb3113928aa37e1a23c8712909bddc167cb1f85bd414d7f` | protocol-facing | test | TD,RG |
| 100644 | blob | `eae6da867b629c35d0d855aac2f43e2864ec3f5e` | `backend/src/utils/decodePetitionMetadata.js` | `81201f66b3beee1f74ea645721c5160c6cfcc0619eed98abe4a85d2cdbbd7c79` | application-owned | application source | TD |
| 100644 | blob | `eab006cb36e258d80de3115a33d3b7957b440704` | `contracts/.gitignore` | `a66aa98c251401646ec2056b123025b0876c40d3bb51a3e8b66c3b5b8e3f0c2a` | evidence-support | build or dependency input | TD,RG |
| 100755 | blob | `605aef3d77650c3107cfd676115f13c10a4ee2bc` | `contracts/deploy-admission-stack-anvil.sh` | `4be674b87e0a6c365a94d403a600e866263a6fa9bcbdf6ed4526925e49711707` | mixed | deployment or verification operation | TD,DB |
| 100755 | blob | `6aefffcbf303e85db74f9ce00d7ae1b6bcd7675b` | `contracts/deploy-admission-stack.sh` | `84beace6f1187202a31e9d4f535a781a9c3123cade8a46434c9526ca69463b88` | mixed | deployment or verification operation | TD,DB |
| 100755 | blob | `f2d76061b7826054a072fa68057bdff98ecd63fe` | `contracts/deploy-membership.sh` | `12b028163da8eff24b9b75462abecc2e011e9208c82708c09ecd5e004df7e39e` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `9abf5cfebf601e8e19f0baecdf957437a8ea2887` | `contracts/foundry.lock` | `969132d6b5ee905a195ecb18e0e566389a3a0636c2a7401a60c85240e767b43d` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `3c77b3c8537273fb242690bf32a3975bb22b4273` | `contracts/foundry.toml` | `f633bc64ae411f56c50edfc6bf33e5d4a976ce09679e2cd393f1693a32003aa3` | evidence-support | build or dependency input | TD,RG |
| 100755 | blob | `1d61c6b3330f216f09f341481abaf82de0455dcd` | `contracts/install-deps.sh` | `b7709c2184b7012e7819ffdad79a43a1b7735bddb971cc2f13f538765f3cde9a` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `6341b57702b03f3cff223261813205511901ba2f` | `contracts/legacy/AttestationAuthorizer.sol` | `9997d0e4df0c4ad7b218d1a55e68dd042e624cf87cc2a4f358fa3fc9bf81de6d` | historical-inactive | historical source or operation | BD |
| 100644 | blob | `557912e3ddacb7906c91f92cd7b22ecb3f51278b` | `contracts/legacy/PetitionRegistry-pre-m2-backup.sol` | `ec4660d3df2540b5366c9bec7846541915211f62fc39a0278f8cb476d90e2a00` | historical-inactive | historical source or operation | BD |
| 100644 | blob | `2529f38bf47bc598a40df2eaef6ecb65a88cd372` | `contracts/legacy/ZKAuthorizer.sol` | `eed209846a11764d8bb4f336fd3676c46ac26947cbdedaac3a4b67081dc91b18` | historical-inactive | historical source or operation | BD |
| 100644 | blob | `d21e8a33db61b4886dfd874966e1ffb64dc21eb7` | `contracts/legacy_script/AURORA_DEPLOY.md` | `461f962a470f8eec5a362a637d6ca10dd61be189188af16065d1877f3108d57c` | historical-inactive | historical source or operation | BD |
| 100644 | blob | `f54bc4f889eeec96ca369398e690652be33a828a` | `contracts/legacy_script/Deploy.s.sol` | `e16875bc7c8f67682f402607f1c99f40527123f7af7a2ed725652d64c9f0e0d8` | historical-inactive | historical source or operation | BD |
| 100644 | blob | `cbba75dc540f5da553137ecc2eea3f2f80aa5d70` | `contracts/legacy_script/DeployGroth16.s.sol` | `16496b1d0aea655f5183a56c665fca36873134de858467e891de465b4f05895e` | historical-inactive | historical source or operation | BD |
| 100644 | blob | `393cd032ab599c122b77f14e65e99bd036d2e136` | `contracts/legacy_script/UpgradePetitionRegistry.s.sol` | `4b580752529b6b73c15cfd4bf63a4f64fb20b202f905ea514caea019e9b3c5f5` | historical-inactive | historical source or operation | BD |
| 100755 | blob | `30d9e61db1c16ec008657b0b220711cd26007452` | `contracts/legacy_script/deploy-all.sh` | `acb3ea9f0ffc85f2e4ff1a02d3178eee7e652e8735dc1a4f757f12e4b86c4fac` | historical-inactive | historical source or operation | BD |
| 100755 | blob | `75e4ee7128472e03fcb9ea25bb7191ea08c60666` | `contracts/legacy_script/verify.sh` | `a78406ce33c3a85c5cc7d9a53f774c14c4a38557b2005812575853c6934aff1f` | historical-inactive | historical source or operation | BD |
| 160000 | commit | `52c1e835e9ffcfe00bd9f8f51de204b93bc7028a` | `contracts/lib/forge-std` | not-applicable-gitlink | dependency | Git dependency link | TD,RG |
| 160000 | commit | `8ff78ffb6e78463f070eab59487b4ba30481b53c` | `contracts/lib/openzeppelin-contracts` | not-applicable-gitlink | dependency | Git dependency link | TD,RG |
| 160000 | commit | `b933412726bccd822a871116f1427111e649ff54` | `contracts/lib/openzeppelin-contracts-upgradeable` | not-applicable-gitlink | dependency | Git dependency link | TD,RG |
| 100755 | blob | `cea26eb49a7475073556df5f81ea7297ded9d78d` | `contracts/ops.sh` | `4e0eb059db191f470b15a5b2ccd48033650239692ac574f3c26caf3b10e15bb7` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `c8f911d67e50bb579513c1a08f75579757a40c4d` | `contracts/package-lock.json` | `49f5dea0ee9a23e6d3595e9ac06e45b54d8b358ac67c1f6e8021b67166558c4f` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `a807afc5df8ccde6709a7198ddf1bf6a85f6b237` | `contracts/package.json` | `c3296734c1ca842e3e57b8856a29b83fbea5db5ce82fed1b838112b31e6e37a1` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `45fb913880701d9d9137b1ff55b82c7a89fe412a` | `contracts/remappings.txt` | `fa69afa01240e689d8d5625e2f532483498df515a375774787a0931001ed76c3` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `cf56961578fedfbcb8e9ed4022e995291a9ec639` | `contracts/script/ClaimAdmissionRefundLive.s.sol` | `26c76d68fa68759c2e728e64c5d4e2af676c08ac442e0fbbcdb931942056d43d` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `4fe4e03045cbc63c772d66a4686994c26dd6941d` | `contracts/script/DeployAdmissionRegistry.s.sol` | `801aef933dd055f51d48167d77f68dbb8e901fcd3950359fe0bcb2bb2d9f73fa` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `441e9f0b215cd398e4c0bcc4eaf5798d05a26a9d` | `contracts/script/DeployAnonymousMembershipRegistry.s.sol` | `61cb7dc1f8de39a03e643b29d805cab635f6e12dc10b6a35ff068df4bbbbeb7a` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `bf9494073c62036eff91f8c26a93e6677e73b474` | `contracts/script/DeployMembership.s.sol` | `0147e5fad3676d64750d0feb7892069edf06c3a032532e6c77a234faa8b27ec1` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `9c781794c55328abec8a196289e9517499f8b5e9` | `contracts/script/DeployPing.s.sol` | `70b74f260fdee852de436f37f065b92be7cb68d5bf4fa4169a262eb1bd8ad524` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `35c56bed9c126f6dc91c5b0be59c393efae2f6ae` | `contracts/script/DeployPoseidonHashes.s.sol` | `f3c25bd5c3aea8c1952e92a308f0ba802d97c561a650f2feaf52fdeca369c677` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `6fbae8bd86aaffbc815cf119d857633065bd1cca` | `contracts/script/FundAdmissionRefundLive.s.sol` | `32c05222c1240e6c8954b56472072fdf24e551682f131dfec6b1da4c0b6bb06d` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `5a48b31154249630446957f774591b98540077bb` | `contracts/script/LinkAdmissionRegistry.s.sol` | `894e20a3ed02bacf16ae5911d70976d03ecce338df5fcb392438011a873a7400` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `78c7569e9d74dda0fc762c1f1218faea92a30ae9` | `contracts/script/SmokeAdmissionFlow.s.sol` | `44bad99d0c28418eefa8468b77f8389d4a3af6c8d43a97e35d7bfdb3aafdc122` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `7ec5eb0fa57fafec05027cea9e2948a9e742837a` | `contracts/script/UpgradeAdmissionRegistry.s.sol` | `f4ae0b9920858e4d5fa43964aff30bd4bfc6bbb8ec0ae774185e1ca1c01d4704` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `b696299874b027aba2c7783d8ddeb5cd57658dc1` | `contracts/script/UpgradePetitionRegistry.s.sol` | `79db955bd2ace55e4e507293f561b4b2dac0591db4e80ac206afe4ce67836e05` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `b1d256eb33113d4b00d1c41bdf317e091a47bc2e` | `contracts/script/ValidateAdmissionLive.s.sol` | `8115033293bd99d31fc2266221b4f115c79870af4b0dcb13c0caac7c110f3267` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `00b273e756b6b3d768acf0ea9ee11884ba64e744` | `contracts/script/gen-poseidon1.js` | `44fa277513c91008d516471a67b1d67017ee985f8a1e4a037306ea9a3b65b989` | mixed | deployment or verification operation | TD,DB |
| 100755 | blob | `94a306788cf315bcdb4e0dec3311348781c960ed` | `contracts/script/upgrade/check-admission.sh` | `86c896d58acba393dd95ec47f8cb9ee4a96c7765d84f9b3f33b0b8d470c13cdd` | mixed | deployment or verification operation | TD,DB |
| 100755 | blob | `64b01e5ed22af4f0e789ab2fec491472ade4f29a` | `contracts/script/upgrade/check-petition.sh` | `e1e1cca2b698b2cb66dd405d7e4897c62be9dee538b351f2609a86d7564e16aa` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `d406932f0fb9d6a711b5c2fc319d03f3edce7d5c` | `contracts/src/AdmissionRegistry.sol` | `77a9bdca7dc4e04d9c0c37c2529b8ef344fd8924f3ba4cec6c7bc1485d470807` | protocol-facing | contract source | TD,DB,RO |
| 100644 | blob | `31835a9feeeff6691335cca655b1f9e31ceba0d6` | `contracts/src/AnonymousMembershipRegistry.sol` | `2b883cbca96f074c52d0471aaa62681ae042b8315d5e1260ab114541650c7978` | protocol-facing | contract source | TD,DB,RO |
| 100644 | blob | `f4461828f7ca3a2deb2fbeb123cf431d173ef53c` | `contracts/src/IncentiveSettlement.sol` | `a3063cb3164acc660ec6416bd1fdb4891cae1a224bf5f6667280d3794a46286b` | mixed | contract source | TD,DB,RO |
| 100644 | blob | `797738e3f577e7a72871766bc48a2c48d8f83cfa` | `contracts/src/MembershipRegistry.sol` | `31329ae83c5294287c55ff0d8efc12f4bc5521ce9b08d71dbeac3e44e9d2860d` | ambiguous-status | tracked source with unresolved current responsibility | TD,AE |
| 100644 | blob | `a593c4023fc1ce9c835013a5ad40a310e5bfd032` | `contracts/src/PetitionRegistry.sol` | `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` | protocol-facing | contract source | TD,DB,RO |
| 100644 | blob | `6cafe1c2beb2f4069881735b5ee67691be13dc6f` | `contracts/src/Ping.sol` | `087fa6f4f8238e28828b9272595a5c0a310c235e556e1b946c913147cf090281` | application-owned | utility contract source | TD |
| 100644 | blob | `f794d82e238704e157fcbc4a90e79f37978edc91` | `contracts/src/interfaces/IAnonymousMembershipRegistry.sol` | `2775e4d5e027e272ef5cea1f053a45dc7a4fd5e364d9bce427a9a65436825ea9` | protocol-facing | contract source | TD,DB,RO |
| 100644 | blob | `aaa992c4cd051aac062b420935e116836e43aed5` | `contracts/src/poseidon/IPoseidon1.sol` | `18d8ede67a0aa402c1ec0ada326f3523a2ce958d7f4c0739f6c62cd54fc41c93` | protocol-facing | contract source | TD,DB,RO |
| 100644 | blob | `760bff6bcd251b696c0ee5ef6d358387ed75c41a` | `contracts/src/poseidon/IPoseidon2.sol` | `a4d604582913c5d509ba5b48064ac67ede3bbeb03800621049345134348e483b` | protocol-facing | contract source | TD,DB,RO |
| 100644 | blob | `139bc658e90b4406c20107b3127ce124cd5d50c1` | `contracts/src/poseidon/Poseidon1.sol` | `23aebba4a34ee3a085ace73a86e6a7875eea5d7ddddc68fcd44b8d24fb3c6978` | protocol-facing | contract source | TD,DB,RO |
| 100644 | blob | `bb29c08e5575a3d6f50f55e03aa25f29e395f100` | `contracts/src/poseidon/Poseidon2.sol` | `77c7a6120c427217496b7d7220ccb14bf37c764dd14a8b90b64398cd0cc23467` | protocol-facing | contract source | TD,DB,RO |
| 100644 | blob | `bf3bd28b1e89e8672219aa5aea6e54605d1b5bfe` | `contracts/src/v3/Groth16Verifier.sol` | `b1216366353f3dbf478e1e03add31077bbe4bc76d5a4e40aaba574cd5841bd87` | protocol-facing | contract source | TD,DB,RO |
| 100644 | blob | `95397dd5efda2dc55d55b4e5f79de906edcb9679` | `contracts/src/v3/Groth16VerifierTest.sol` | `bca81ff9857954e7fd6997658dc3bee612e47e28c6b47c6fd1569bf89d21d373` | protocol-facing | verification support contract | TD,RG |
| 100644 | blob | `93337ea08b9a953e5732c311f71e4bdeb6e5d6ab` | `contracts/test/AdmissionRegistry.ActionLinking.t.sol` | `6019f34a7cd4510de916461c5ad573d6d7c945480b755618f8a48ca1767cad33` | mixed | test | TD,RG |
| 100644 | blob | `0db311e61263eefa84309bbc27299b2e46100fb6` | `contracts/test/AdmissionRegistry.IncentivePayout.t.sol` | `ca1becbf138d4b12e02fee1bdffbb67e56c9a674e4cd213c6a58182b9348d4c9` | protocol-facing | test | TD,RG |
| 100644 | blob | `f3e6b7abd1001ae8be0a7ad1f6421c66ef766fcf` | `contracts/test/AdmissionRegistry.t.sol` | `d3729edd5b04ec5d9d87196e719e7c744b8035f60d95ed777de4f9cbc4ecf852` | protocol-facing | test | TD,RG |
| 100644 | blob | `f2c6f2519935f9f8af482cbcc94a825496c7c7c4` | `contracts/test/AnonymousMembershipRegistry.t.sol` | `438ecdf06f28dae8184514d04d9591d73bfc6862b8fd37aed819750e439fbc77` | protocol-facing | test | TD,RG |
| 100644 | blob | `8181cbd93be3ade5e0d5d27636e7b8c13b08c1ad` | `contracts/test/IncentiveSettlement.Admin.t.sol` | `77f6247e5246c4755094edf30fa9cbdb673bba0432f5a0f5c3c0ef453efcda73` | mixed | test | TD,RG |
| 100644 | blob | `18f305c3faed52b38bfa742bde13bbac2efc4549` | `contracts/test/IncentiveSettlement.BandAssignment.t.sol` | `5c82ad576d18b5a4c0c0428267ad1e9f0a355be1232e30334dde97c91b760e14` | mixed | test | TD,RG |
| 100644 | blob | `c958811cd6756c2621fdbe8230abb2ecf09e63c3` | `contracts/test/IncentiveSettlement.Claim.t.sol` | `58d9b8016729716fdfe8fcb000f5ff02a05b1b83ed0042099ac93b9e4c027c35` | mixed | test | TD,RG |
| 100644 | blob | `b3b0ef139d3511d1a2605de69107fb7d61167325` | `contracts/test/IncentiveSettlement.Invariants.t.sol` | `4c60f2a6616942c9e641410f24d9cb2ee7c2120d241cb2c863a75021dca959a3` | mixed | test | TD,RG |
| 100644 | blob | `9dc470d52620e44108a4dac81e0fd15011b4fbc5` | `contracts/test/IncentiveSettlement.SignatureDomain.t.sol` | `f429f1ac136af219f3f29668b728080d56b9d1dc6b94aec96368826d6c7d2a4e` | mixed | test | TD,RG |
| 100644 | blob | `f5e254028102383f771602ea527eed7936642682` | `contracts/test/MembershipRegistry.t.sol` | `b9a00450a6ffbd6e90f2ae132ffc3fecdcc78ee6816c7c41d12dfcd09f529ea1` | ambiguous-status | tracked source with unresolved current responsibility | TD,AE |
| 100644 | blob | `793c4d3b746d4533d0efb33a2fb729c332f71268` | `contracts/test/PetitionRegistry.SettlementReference.t.sol` | `689b7f302d502e9b51bbc111bc4cfd2a5f0b17b8d2a65448042e55ac42984b4f` | protocol-facing | test | TD,RG |
| 100644 | blob | `6c7c5867d45b2131c3807278b34607707c0391b0` | `contracts/test/Poseidon1.t.sol` | `4b063813eb6f59086ee309821f51574a8faca41ec9453003d7ce158b984b30ce` | protocol-facing | test | TD,RG |
| 100644 | blob | `5425a0e7f818937fa80fb075b3db95c74eec14bc` | `contracts/test/Poseidon2.t.sol` | `b6c222c4846947cabb83b0e9d373e3c120c0bec6a7332a16439f29d31ec55cba` | protocol-facing | test | TD,RG |
| 100755 | blob | `49c6ca58d084b450847c566d48456eaf1342b9d6` | `contracts/verify-admission-stack.sh` | `586fa14d46db617870d3df7a96a5be2fbf4ca64e0bb0f772ab512cd555939e76` | mixed | deployment or verification operation | TD,DB |
| 100755 | blob | `55254ced62afe57e06a38079b05b833b3d23c4a8` | `contracts/verify-groth16-verifier.sh` | `d807e204efbff0120d6bffab005334a60f56f82568e13d0e11891bb5f6eb8bd9` | mixed | deployment or verification operation | TD,DB |
| 100755 | blob | `7ce902cca9d0ad75688dd5896fc66ee36e655648` | `contracts/verify-membership.sh` | `af8dc64eda7912a89c97008b35f17cc2e50a27431e935c252eafc5520613a244` | mixed | deployment or verification operation | TD,DB |
| 100644 | blob | `fea62e639b60974c272d67e8d50e77b2072f45b8` | `docs/ADMISSION_DEPLOYMENT_FLOW_V0.md` | `7e055581f00ad5d209a59d4ea3559645c58355a2ed716c9a9533a8d2f02a61fc` | mixed | bounded implementation documentation | BD |
| 100644 | blob | `a05325ca5064d609cff696459434a68916e9e6c4` | `docs/ADMISSION_RIGHT_MODEL_V0.md` | `5a36daba2021ee06dbc5214c0ee55f424c95274518525f2c835f55102438f219` | mixed | bounded implementation documentation | BD |
| 100644 | blob | `a0e9cf75f252600c1eecedb1b85101273586e175` | `docs/AI_MODERATION.md` | `181304a8347d498674e80e0dce5d1001b77e39468acb3113fe13f3c159f6d431` | application-owned | application documentation | BD |
| 100644 | blob | `0b7add8749676df602b1dc9a85461f76212d60dc` | `docs/ANTI_SYBIL_PRE_POLICY.md` | `c9a2f39fe7bc701bae0060e756aada06b0de1d33e482d65ed6e16a7106e7a2ee` | application-owned | application documentation | BD |
| 100644 | blob | `29a8be6c92b109f48085dbdae7d0c87304bcd44a` | `docs/CONTINUITY_CUSTODY_MODEL_V1.md` | `f906c78ddbf10fc0fe98679dcd73154bc30b6d278eaedafdbe58a3aaad993422` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `a056254ffcf24036fccda78b7c7362b8131f1128` | `docs/ENROLLMENT_FLOW_AND_CONTRACT_SURFACE_V0.md` | `40345a2136528bbaaefb19d9172459fb40dfac30154588e19e888e9eee7dc686` | mixed | bounded implementation documentation | BD |
| 100644 | blob | `2d8ef5e14bad0332f4f6e7c7c5df5a639b811121` | `docs/PRIVACY_ENGINE_APPLICATION_ADAPTER_CONTRACT_V1.md` | `9e94912a8c79ebd949c58734e5f644e376c05c6be23c6a9ebcc4febef9f85486` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `7f0cf4fbe47907ef885e336814b529ca71bf321f` | `docs/PRIVACY_ENGINE_APPLICATION_ADAPTER_MODEL_V1.md` | `a73d049c7a3ec94d67e4755c07fe8904bf2504a68e7304c3a29a547e1069123d` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `54f843a4d3fbc75212d283ff1b6be1215c196155` | `docs/PRIVACY_ENGINE_APPLICATION_REQUEST_MODEL_V1.md` | `a6eef3e412259469bc2906285f8034235e820bacd5a6260a22a6c0a7faa30a77` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `121a9a2dd153f8cb9914c94c35bd28f439fb7592` | `docs/PRIVACY_ENGINE_APPLICATION_RESPONSE_MODEL_V1.md` | `bceee6f9ebf9358ef604fe2b39d72c0284df6b4c8185c6181e69a43811896a86` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `caee10699e0aa50e85562bcf4fd3b55cf07b27a0` | `docs/PRIVACY_ENGINE_APPLICATION_RUNTIME_BOUNDARY_V1.md` | `a0ff330cf1045151948828f69eb06236cc734e19132d0ee70248c46b2e49539c` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `590bc8b765d2e4892d2084859bff2886b5b0804b` | `docs/PRIVACY_ENGINE_CERTIFICATION_BASIS_MODEL_V1.md` | `18dfafb7220ec1256ba5cc7e1f507ae42b31884bfbf28c8ecec75d48ad7e5c94` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `e2ba5a2b8d8c390fc666d888efaeb2588df533b8` | `docs/PRIVACY_ENGINE_CERTIFICATION_DECISION_MODEL_V1.md` | `12cd1f959d9d2de5a09930a4a56ca97a29b737cf8e906110df508a59566c5e45` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `2cb6c032f2a8490ba632ccf4b096eab278a2d97d` | `docs/PRIVACY_ENGINE_CERTIFICATION_MODEL_V1.md` | `6fd43237f3a74a5efffe378e450a625d444629a9b18bbc420709833d9c5ec263` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `fe50900750e3018561695206f7aab5898a5c1301` | `docs/PRIVACY_ENGINE_CERTIFICATION_STATUS_MODEL_V1.md` | `a23b85591a5b5cd1fae1cd1be5466e34df04877910276b5d23178ca22a893a1e` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `2c18e65bcb6f0f1ed9249d60d8c35176546cb892` | `docs/PRIVACY_ENGINE_COMPATIBILITY_CONFORMANCE_MODEL_V1.md` | `ccdd5d6a844c5a5a97597e10e1df28e080fe083c308549bfd85f23b823aaff91` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `d18fda8fd3d2e74d86fd9489acb96480e691fb81` | `docs/PRIVACY_ENGINE_COMPATIBILITY_DECLARATION_MODEL_V1.md` | `30886492336b55519ac194e22bf0a1aa99a2a27b03543502251321d5813a20ec` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `aa955130b652e4d7dca0606f4fa67b4085da73fc` | `docs/PRIVACY_ENGINE_COMPATIBILITY_MODEL_V1.md` | `26ba76f3a0416980c447198c7b5c3f7f97404ce69cbf038a76a29bb869ece2ca` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `43967dbd49b4816bb04b4b589f9c804a907c8a4f` | `docs/PRIVACY_ENGINE_COMPATIBILITY_PROFILE_MODEL_V1.md` | `c0cef341529d1f254150142050400a0cecb4eaa375eca3a640b12bd0634461d9` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `f6a6beab4df08dc083b6fab4f769055fa109b1e5` | `docs/PRIVACY_ENGINE_COMPATIBILITY_STATEMENT_MODEL_V1.md` | `98a9018ef08afdeddd8f00425a6bdc88be1899ff5ece084ab7054eaff66cff8f` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `65f936276203cd67af368f85a0e25ee98506db65` | `docs/PRIVACY_ENGINE_COMPATIBILITY_SURFACE_MODEL_V1.md` | `8a210a1da77f3869bec8abe90b88985f0a9e5c4984b795368d14893af83378d2` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `d6ad746ece592ca457340b46ab115d71c8e75855` | `docs/PRIVACY_ENGINE_COMPATIBILITY_TARGET_MODEL_V1.md` | `284383f23b1d377d97476b18e6781b97fd3bb479062e71b02fc105507c51e293` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `1c54c5e6b4cb4e92bff894403f771e7abdc9614a` | `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_COMPOSITION_CORRECTION_V1.md` | `6c8cbe0ffe6687045375f33c2316a1baf8ee1d026cfde1bfdc258769d70d4b26` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `ad55f2e001a1430b05930037bfcd4c0e1387b95a` | `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_COMPOSITION_REREVIEW_V1.md` | `fe51c48bb7992482ca341af943b396b46457773999452d1cfb2a02807557bc41` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `74d9a773c7c3eaeeb43ff75954cb6a649042bb3f` | `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_COMPOSITION_REVIEW_V1.md` | `5855fa1765a8492e08f7718c7c6b7d400fff343e03caa666f9a5fdeaa6184709` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `93e6f81031a652c2ef56b729290152723fd986f1` | `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_IDENTITY_VERSION_CORRECTION_V1.md` | `c37a3fa1985a11243ff0b1103d5d7ca911f77e76a14f00f4c12a368e4f7ad88a` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `53df57f8101763d9f17429876c9777cd135114b8` | `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V1.md` | `2570e94fa7d06a3f136b5384bd879e343a25bbb33c3b4fc3f7c9ee0ecb1b9b23` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `e9b69e8a075f4c5443b9ac66e289cf2737972208` | `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2.md` | `279fc80cb2998df8c4fddcc2ea25e4091897571c57a7d5905100857612b2d79c` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `96467913f303ebb558e97c641e023939516135ab` | `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2_COMPOSITION_REREVIEW_V1.md` | `093f3d2178bc890e7bed9dc56aea164f36918a01e49caef2ed8d777777dd0d11` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `27262837f959d4ea2744595527cc332ad63bbec3` | `docs/PRIVACY_ENGINE_COMPLETE_IMPLEMENTATION_PROFILE_V2_STATUS_SYNCHRONIZATION_V1.md` | `d8bce61c2366e4a5ca6d6d87ef4875944956acd1b8303e73f2f901c7a1ba1e27` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `ad1a2f3fc96f274cf10a56e843832c6da2ef1e93` | `docs/PRIVACY_ENGINE_CONCRETE_INTERFACE_SPECIFICATION_MODEL_V1.md` | `47597ad21eb98700c6e87fbbe3954d59b5190bf6c6953a6d11df448be8ca99a5` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `dae12e6cf40b2ebf9993db126179cd1d43fa93b0` | `docs/PRIVACY_ENGINE_CONFORMANCE_ARTIFACT_MODEL_V1.md` | `2acdaad7d59c9fee70f149cf6be5a7a12829e7a5c6c1ff83da9fb93da14a88ce` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `522926d9b9c56d7803fd941a45269880cfc76971` | `docs/PRIVACY_ENGINE_CONFORMANCE_ASSESSMENT_MODEL_V1.md` | `33f333cb0bf758c28dda4c4feba0d08fdb931f35964bdd65821474cc2a5a0dc1` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `544a28dce35204dee5fe0b52dbf7b67cadf22555` | `docs/PRIVACY_ENGINE_CONFORMANCE_CLAIM_MODEL_V1.md` | `3fdf2da19fe1131a7f2a6e934ed3de54b21570fa6ef8201f25e6c7ac3d5f00b4` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `2688a60d6d50941dbca38db1ebacc99ebda273fb` | `docs/PRIVACY_ENGINE_CONFORMANCE_EVIDENCE_MODEL_V1.md` | `cc714a81f9fb66b939b1ccd0430aa8f813a7c8907c70e0b35e66e98a01f4a7a6` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `7f4194de1a9cbc80b18fe27777d4500bd24a6931` | `docs/PRIVACY_ENGINE_CONFORMANCE_MODEL_V1.md` | `98f7714339229629f9b9215f48a248d97a458bf764f967809ad00b2d7f978f9f` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `2653765d856274ec09dc8ae423de4a80e1147e7c` | `docs/PRIVACY_ENGINE_CONFORMANCE_PACKAGE_MODEL_V1.md` | `49ac7b8460d7396e0f554a6d9d541de2df3e8d1578631b5c0381b475b2549760` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `0cb46d418e073de0a0bd7019b9d5d3afe63f3b96` | `docs/PRIVACY_ENGINE_CONFORMANCE_REQUIREMENT_MODEL_V1.md` | `83d71bf94e60cddd053c607374025d628a45a700e91c5168cf4c5e9481c8eb5a` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `991a1c056ab81d802fcb83ceeabd876a6ede55b1` | `docs/PRIVACY_ENGINE_CONFORMANCE_REQUIREMENT_SET_MODEL_V1.md` | `01e6769c8937ae71e882fdb9d2393e320fb211d7e968cefe2bc01ec5d7216da0` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `2a2adaa2d745f4eadc62e821e3f9a7e7910f5c64` | `docs/PRIVACY_ENGINE_DEFINITION.md` | `8ca39716f558ba2d7a3e666978b509bec4b44e99cedd0e5db9ec565f0538b7ce` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `ec0b20d9f3943b107e1f3fe195e43d8000f18136` | `docs/PRIVACY_ENGINE_DEPRECATION_AND_MIGRATION_MODEL_V1.md` | `ba25363ea8fd278e1c6c75f57b49d2cf6f38c91bbd3a61a530208971142191a7` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `3eff9ae77b805c9545f14ce4accdf93f5a3346af` | `docs/PRIVACY_ENGINE_FORMAL_ARCHITECTURE_CONSOLIDATION_REVIEW_V1.md` | `74c0d2b82ad4c92edf74d1ec3940c80d77a9d1feffcece56fa7f6d7544f58b67` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `cf6421fedab5e7b00b856cf976c6e52b93dcc507` | `docs/PRIVACY_ENGINE_FORMAL_SPECIFICATION_STRUCTURE_V1.md` | `34155640b256d96e544d32977c32ce496df5726b2b9f23473c12833c1971d090` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `52dc5af5607652857c5c5abc9295886b5e2c1e80` | `docs/PRIVACY_ENGINE_IMPLEMENTATION_MODEL_V1.md` | `f933b8a5d8000370ebe256a48bad4abc30756ed59ed70489fc0fe2acb7601b82` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `2c1f0afe94013b52d4d134881409585df19699cc` | `docs/PRIVACY_ENGINE_IMPLEMENTATION_PROFILE_MODEL_V1.md` | `ad577db16807646768e13286b2d29ac5ad0492ca6e2d7e8c3b12ba0fc628cfef` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `12dcc1d86dc8197a5f508b9025325eea29d935c3` | `docs/PRIVACY_ENGINE_IMPLEMENTATION_PROFILE_SCOPE_DETERMINATION_V1.md` | `03fe5d180a4056c6e66356c1804f8883006daab52a80ec12676483ad75fd0a17` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `870b7e34a92838b65b5ba549127be52cc6c837c8` | `docs/PRIVACY_ENGINE_INTEGRATOR_OBLIGATIONS_V1.md` | `4c6d0943b1155b9bf8e1724362ac742c77beda52a408758b1a948724116b7a05` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `98523c7dff4e607a6bdc80b1863e71c0194e2dad` | `docs/PRIVACY_ENGINE_INTERFACE_CONTRACT_MODEL_V1.md` | `361ba7ebc5e7d08303b691b0c485783a95588b8366fa95ef9d57ac685d8944e4` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `0b5df10f963033b7e416a0d95e48f7bc687e61ef` | `docs/PRIVACY_ENGINE_LAYER_INTERFACE_MAP_V1.md` | `90c4fb7a16da1d010bd9edd295dfd5dc1443d39a60b3fc673dba57aac83aaeb7` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `8ac84f327568db06c1b9f8940742bf884d63d715` | `docs/PRIVACY_ENGINE_NORMATIVE_REQUIREMENT_MODEL_V1.md` | `e1f0c4013965a1b3f03b1ef8bdd0578d18d75c6ab796233ac9a2677e20d31402` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `0d52b7e745b8296104b1eac86bb40fc3a69ac997` | `docs/PRIVACY_ENGINE_NORMATIVE_REQUIREMENT_SET_MODEL_V1.md` | `1ed8c332ff259ecf97fd84e6786e0120e5449cdf2ffa072b5cbadc8abbc47a79` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `3f186672bdccecd8d179d33b00125eec52dcab4a` | `docs/PRIVACY_ENGINE_NORMATIVE_SPECIFICATION_LANGUAGE_V1.md` | `e69499d1696f8adfb04ca9997148552fdabf78ac488ca9ed6e049a1f686fa60f` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `0914a8c0335b727207bd0e8de40475a5c6a5d503` | `docs/PRIVACY_ENGINE_PROTOCOL_ACTION_EVALUATION_MODEL_V1.md` | `ce87a40a508d8e2a5d1ef36635748f4a99e4b26bf794b2f642380ae11fe33790` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `b78e644980b8a8f0525f563206816e416c6c5103` | `docs/PRIVACY_ENGINE_PROTOCOL_ACTION_MODEL_V1.md` | `6a17706ad4f5860a37aed83c7a2f89603defe3e07a87000c41d260610b392a22` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `c66c3fe815975a651beba3a46f80330986127a9c` | `docs/PRIVACY_ENGINE_PROTOCOL_BOUNDARY_V1.md` | `17af925c86cae00a3056cf7a33d25cb171eab65e22f75c32dddd27d45f373924` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `c2c4c9b689d18c4b9d8a20ee80eb261c3fb22964` | `docs/PRIVACY_ENGINE_PROTOCOL_CLAIM_ASSESSMENT_V1.md` | `624f25ac4e2b819f9d41eb9451ce77f54500bd712456755507a9a2ddb21b4409` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `510117f4387c2fb00f392720ea8499a94e30c74b` | `docs/PRIVACY_ENGINE_PROTOCOL_ENFORCEMENT_MODEL_V1.md` | `1b2c56573010d5bf904830907f65fc9ae90a15f05a497c74d63ddb648eb92e20` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `fcc5bd80b45e7025f986ce495fdd1ca0a50efcec` | `docs/PRIVACY_ENGINE_PROTOCOL_EXECUTION_MODEL_V1.md` | `639a35f7237a2d3f99765fc72ec5f1b55bfb349a8d9ea2e54ce4f4f2ebde6963` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `009b42f8b6bb39a059f3210feaeefcd9ffcd6452` | `docs/PRIVACY_ENGINE_PROTOCOL_GENERATION_MODEL_V1.md` | `519f6c87e5284b56ccf8b44797ea0703a93c33521da736a02a7ef077fc05f30a` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `c9a08f9515d7cd08bda8adefddb6096a4183270a` | `docs/PRIVACY_ENGINE_PROTOCOL_LINEAGE_MODEL_V1.md` | `2dae58a7cc003b293694dcc566a4ca05c861543010a20881e457adf48d9c4323` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `c9b05305bd3eccf2f034c0332e725d93b0fbc962` | `docs/PRIVACY_ENGINE_PROTOCOL_MODEL_V1.md` | `b63655447b344dbd3ac96212e9d7e30e5410a4066928a98f5aca56980b5ee0c9` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `0ddb637c7ae91f772392de184fed4668be40eeb5` | `docs/PRIVACY_ENGINE_PROTOCOL_OPERATION_MODEL_V1.md` | `e5c1e8d960aaad8d0ecb0a3facac886cfd120f5ca853e41fb398841ac9631973` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `2f8abcf9d7231293df8ddd2165047f7a6741d9c4` | `docs/PRIVACY_ENGINE_PROTOCOL_PUBLICATION_MODEL_V1.md` | `f42f67372865292ded84f59778aaf791283e12591be5ca49b2c3c9ca3e205344` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `7e84f9703906db916d3971e95c8c9a507c2b879f` | `docs/PRIVACY_ENGINE_PROTOCOL_REALIZATION_MODEL_V1.md` | `2e9a60249a127434c0e7520f942bdda1879012c201b1fe9af31c96be234e5f79` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `15296accfaf78f813b5ef7a337dc842fdf4b4d93` | `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_COMPOSITION_MAP_V1.md` | `b97206e79f0c3010ec429875d9224333e266695d436e3be38f0ce844279558fb` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `af20d2f4b5b7a41a50f3d11056b75567ec3fafb5` | `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_CONSOLIDATION_CORRECTIONS_V1.md` | `9fc2625a7bb05737ee26eb77a56d0e22237231c0477be37ffb7121350fb3fe55` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `315ab1d26e721d863e8c5d56274c444efd61f640` | `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_CONSOLIDATION_REREVIEW_V1.md` | `77a1b0dea3ff86264eacea6d36029f0ab2b09356e4ece7a68d08ee63881df16b` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `c1a1547b94f06bd733bd5ba1c59d0074d377694e` | `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_CONSOLIDATION_REVIEW_V1.md` | `945152df97bb3e43074e7769c4bfa45d9be81a7d24a8a9aa296df6b152f61715` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `cbdceeb3d87bb5f3410fb67c782b1ba253557aa6` | `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_FINAL_CONSOLIDATION_REREVIEW_V1.md` | `7bf415870a2e630157d1cf186e45764513e87b5f13b2ac790373d4de5df13bb7` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `2014c47ea05dde6742590d4aa368a079e6626501` | `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_MODEL_V1.md` | `9db0e2d0e97cdb3d210f076100861305aed769c75d5ff574cea7f4dd3f4d268c` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `6a5e72797b9aab136a279cb4b97fe3f26d725890` | `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_PUBLICATION_RECORD_V1.md` | `d655359c296d6d6aefffd3e6faa0fd47f6506ec9d64a871ade9f9eb469108029` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `199487cf337ed6e2dacbe4546b1ae312d9beff5c` | `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_STATUS_CONSISTENCY_CORRECTION_V1.md` | `0855533e198fe735e64e34af9423cec21c5796970014f8eb227dc89191a1be1d` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `d8abd5123e7bcfbc66b75ae7dd8a0353c18eb85b` | `docs/PRIVACY_ENGINE_PROTOCOL_SPECIFICATION_V1.md` | `f2c12b60f24fe8fe8eddf27dc2d59814aceba42b907160c54ad3868bde7da393` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `360dce66772b1e3cc984d66f5a3d57df9056a0ca` | `docs/PRIVACY_ENGINE_PROTOCOL_STATE_MODEL_V1.md` | `9fe3bb8f26bbec4b207d92c768a5f2c46a6f6eed824071e1a500531056cc78a8` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `78589daf3850e57736e4dc8113374826a3fe0689` | `docs/PRIVACY_ENGINE_PROTOCOL_STATE_TRANSITION_MODEL_V1.md` | `0eb986ffa0094434b93ee5b3c371ad321be8af0f2d9992997daeeec642b92be9` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `93b9a4f57c649e803e2fa484f569f45ceb155de7` | `docs/PRIVACY_ENGINE_PROTOCOL_SUCCESSION_MODEL_V1.md` | `dca363611cb615e7884be06c19046a69830a382981ce50d4326f751ac256d79c` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `b232f7f7411b2e401da2deb5c7a551ee74edfb4c` | `docs/PRIVACY_ENGINE_PROTOCOL_SURFACE_V1.md` | `12b6769910ce071e033a1aae40a8fa751958df32e14bd04f105412eb89844217` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `c4da3ff6f04998d20d4633e33603804fe1b98e4a` | `docs/PRIVACY_ENGINE_PROTOCOL_TRANSITION_ENFORCEMENT_MODEL_V1.md` | `414eaa2aba0322297f1feb7c2f05397a0519f818758bbec5fb2a5cd794a2483f` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `8679aed60b63de5e94f66c578595f68557a90419` | `docs/PRIVACY_ENGINE_PROTOCOL_TRANSITION_MODEL_V1.md` | `3278f3d80a7afd8ebd098ddd90123e2b8ab41426db7e238f20d7377c34242c2a` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `9758ac97dba07d0ee40f6d6301bd6ce16828f194` | `docs/PRIVACY_ENGINE_PROTOCOL_TRANSITION_PRECONDITIONS_MODEL_V1.md` | `36606027c9b5999ef890ec4abd439c7af42de423cc3fc49f5ab99dc1626a3a97` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `a0416ea17f5e78f235d6aab40df5632ca200ea8a` | `docs/PRIVACY_ENGINE_PROTOCOL_USE_CHAIN_CONSOLIDATION_REVIEW_V1.md` | `b563247011f2f2293bf03a2494b55fad92447e3c9fe1625d582deebdf9889522` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `de9682b7ad084c49cd25ff212e236ecfdf3dafca` | `docs/PRIVACY_ENGINE_PUBLISHED_PROTOCOL_MODEL_V1.md` | `3cffe14a415d514342fc92dacc81e40649882ef172fa9267fac93ca595d07683` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `e15f2bdf5ec8de1006ef9493ac5546a3a8b9cf62` | `docs/PRIVACY_ENGINE_PUBLISHED_RESULT_MODEL_V1.md` | `7503b98dd5f9bcb98c5df89fff72fd6ad53b13081b7bd29031610b43df5a0679` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `6d68b5176ac23c9708270c0f3ebea138856c2b32` | `docs/PRIVACY_ENGINE_REFERENCE_IMPLEMENTATION_MODEL_V1.md` | `c59234a1b2bd6b02832a8c6bbbcdf1f160eda6ae8018204ade29acebb554e33d` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `524a73b422fe958e0a77408a43a197d99b581b8c` | `docs/PRIVACY_ENGINE_RUNTIME_MODEL_V1.md` | `15c0ad7a7b87343946ad5d61ba720730791c883f8f4cc1dbd8ad0d4f8a6d2398` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `2db6057ac73aad8240e065e4c2f1d500beea1f8d` | `docs/PRIVACY_ENGINE_SPECIFICATION_SECTION_MODEL_V1.md` | `3fc23550056a9b527bb129a790ae9f9e0e28757f74ba8dd1e1d7f6ff8d18b33c` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `a64170ef232d42c9adcda439fc0396fa5d3136e7` | `docs/PRIVACY_ENGINE_STATE_EVOLUTION_MODEL_V1.md` | `c1a897b6e5d424536e55f283de45f2be47bbdc0ab7ef22b4d60098a0b24c0d02` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `f0e6f115ad8268d8a9b3645a38b8c2c3c304a5f9` | `docs/PRIVACY_ENGINE_SUCCESSOR_STATE_MODEL_V1.md` | `49f0c8bb31e53d35299249ecb4e87d0fa42c80f00214bc9219ba15b7d109163d` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `dfe972616d2e4b53b09831c429a664fcf1f30a7f` | `docs/PRIVACY_ENGINE_VERSIONING_MODEL_V1.md` | `4e26e7d4ed1d62a4c5ed4e817f40c7dae41fd7dad90857ba4622664d608315f9` | evidence-support | formal or boundary documentation | BD |
| 100644 | blob | `ef2bbf18c8941d888c1605637c5c194437b21fa9` | `docs/PRIVACY_THREAT_MODEL.md` | `c56c80ede7d57ca6f0e50905bbdba8d11d0cf13595d8a16d043253d8e9bfd3ab` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `4c9ed29cebba9922afa376e71cc2dcad184c2bf2` | `docs/RELAYER_IMPLEMENTATION_PLAN.md` | `9f0877d2b8f203ab407f95a6c0155925e1794104046086ed4ef08021c2bc907d` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `16668d2883cb0d64690e726c22e6a2d9abfdf14b` | `docs/RELAYER_PROTOCOL_DESIGN.md` | `4e5d35a71cd92f3dd8388a59bcd4b91221c589723a6b3140a66358ee3c50b098` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `7028ee6f6d03adad7f860a0d62c64ce6e7e908a0` | `docs/UNLINKABLE_ENROLLMENT_DESIGN_V0.md` | `e2cfbc37f3fe3dd4291461b02a40cd24fa0e7fd331136eed8ef33d937353f5a3` | mixed | bounded implementation documentation | BD |
| 100644 | blob | `a5482dae7c5c891b6b44d57481a9909d72acdc36` | `docs/ZK_ARTIFACT_PROVENANCE.md` | `699d34953af2b8322e487d9cf0f20dc5b2d000064b275c656ba33bab621940df` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `983c0333f90dcfe988205f11f41ecbd114198b13` | `docs/ZK_CIRCUIT_SPEC.md` | `087a6e9aa40737ea75c06d689761f437d6434419aa5e26382f5b88e6fa614ae3` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `8d59b9ab515f699fac346cb18d3143c909cfe9cf` | `docs/dev/ENGINEERING18_OPERATIONAL_BASELINE_CHECK.md` | `511630cb7fb0deb68426342b5e0435105dfdad4dca37c395ac35d2539a5eb88b` | evidence-support | operational documentation | BD |
| 100644 | blob | `b8aebd07563c05c095da99f8840bc1a36206e368` | `docs/dev/WORKING_COMMANDS.md` | `9141dba60904ef12a2427b2cb342a4d49ac1689c94879b1f940254bb8617fb03` | evidence-support | operational documentation | BD |
| 100644 | blob | `7c8d2cbbd963ee392615a20243aa4c56bcfc82aa` | `docs/engineering/shell-windows.md` | `42c8d7c46ddd10bc52d4b3602a5320017947ccd41fae558090f5b00951291b1d` | evidence-support | operational documentation | BD |
| 100644 | blob | `7c3280feb06de08cb02fa797e222b6ce883f03ec` | `docs/reflect/REFLECT_ACCEPTANCE_BOUNDARY_V1.md` | `151b276d2708fa404e39046200343d20f377150acdc380e65c7a4c255f9957e8` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `0dfd06e43ee6d9804a22db72a0c08735d35714d6` | `docs/reflect/REFLECT_AUTHORITY_CHAIN_COMPLETENESS_V1.md` | `ceb8ab3e3d3bfb6c07dca3a397f630dcfbd3112f39107a49f3741bd322e04ae0` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `3884d73e2db6dd098fe119b94fc69f4e2cf7bee3` | `docs/reflect/REFLECT_AUTHORITY_CHAIN_V1.md` | `086efe99ef3a29561a8629b4f14603c29b7e9dc657097be0d6db7d95bc2aa7ae` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `db1bb98087410b9f9e2ec27a47af3b8f1e9f0996` | `docs/reflect/REFLECT_CONTINUITY_BOUNDARY_V1.md` | `91f8638be839e6dc86049d1eea4b1fb3ee7e3669a30a7896f0cd64fb90e157a9` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `9aa84502933d838c07e42d8be3481e3d406ec4ab` | `docs/reflect/REFLECT_CROSS_STATE_MIXING_REVIEW_V1.md` | `89ba789f72f451020cddc6587da1345eb7b33efd5932b33d1b2d2f61632a096b` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `66dc29b7209f30b136854e8ca8b49eb8f9d5645b` | `docs/reflect/REFLECT_DECISION_BOUNDARY_V1.md` | `125d0491f1fb5e96c94b4792bd9c39ed096dc2fa06e53cc78eeed12cfdc8fe6f` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `a2da707984d7efe75c4865582760318bf992ebd0` | `docs/reflect/REFLECT_EQUIVALENCE_BOUNDARY_V1.md` | `c4199245a375291e8249215c7b91d15e1b523b491c4b118cb2fbb38e9c192597` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `d3d4156bf840d1d2c028254aee93fa06914dd1c4` | `docs/reflect/REFLECT_EVIDENCE_GAP_RESOLUTION_PLAN_V1.md` | `deb9d5fc4eed9e50b80c8e6fe2eecee534be696701e2b9e63071845b58982196` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `ae9a7af00b1187923f5993062c62af06a37d08ba` | `docs/reflect/REFLECT_EVIDENCE_PRIORITIZATION_V1.md` | `0a68cd8c5bb63206aa7d9f5a4610ef1527c7c8f85bdc1a1e49c28ad64556ec29` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `5a0b70b806fd5fc784676d97177e3a3d93d6e492` | `docs/reflect/REFLECT_FAILURE_AND_FALLBACK_V1.md` | `7d14607a5ec11721f8d5fb19862861417be7ae41bca5e640878c81e53524b635` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `a1a375f4dc8f50f148a691d5401f34dde3dfe854` | `docs/reflect/REFLECT_FAILURE_AUTHORITY_MODEL_V1.md` | `33f7bb2c063d4700584fbf103cc945367d82db292d8e6ec12d2f7e4cd016b619` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `4f46362ab5bdd36652688c17a2cdd2e2f2101563` | `docs/reflect/REFLECT_FETCH_POLICY_V1.md` | `2e64e66964b2cedbd7a998dcea6efd7f3098e6ae62457ad8cef8c36ef1bf9398` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `12d37419de596aa80624c1fb028aa4cc89b6266e` | `docs/reflect/REFLECT_IMPLEMENTATION_READINESS_REVIEW_V1.md` | `c5c18712c8efbbfb91fb75a987dd8c45c48eddc9f3dbfcf75fe8047401537bf5` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `29888c9e3fe7c5267a2f7dd4ae4a151b85e151cf` | `docs/reflect/REFLECT_INVARIANT_COVERAGE_REVIEW_V1.md` | `8c963285cf9b5cc329bc75a1e8dedcdb284c0cc125e396e0bada90ecf147aef8` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `b4d30b22e2ecf827bc501f68f494929d200ab349` | `docs/reflect/REFLECT_MINIMUM_ACQUISITION_CONTRACT_V1.md` | `d41b1ada2a5b474acec84f8d41ac6677e4df975477728939418c71a2a9921b8c` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `c14835aba0b6846597ee44f91a852a30e9968b1e` | `docs/reflect/REFLECT_MINIMUM_ACQUISITION_TARGET_CONTRACT_V1.md` | `724d60f81885918924d55ff0cde3d70689ccd7e6ed3d759cf720e31b2f07b0f0` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `592e60e60ddde0a46d1c1b525a01a9c78b6de448` | `docs/reflect/REFLECT_MINIMUM_DISTRIBUTED_ACQUISITION_SEMANTICS_V1.md` | `a627472ec555717a3b5836694ecbfcd2850d39ed112a82d3a8d36a1d01bc80ac` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `38a5d1d0903bf2c7a31033460b396420e5b5f620` | `docs/reflect/REFLECT_MINIMUM_RETRIEVAL_CONTRACT_V1.md` | `ea80b9d38b38224d00e4528ed8231e63932b9af9d34837a3741204a745bcfc6a` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `256e69ae9a9aa92ed8b2cc52854962bc941d94ce` | `docs/reflect/REFLECT_MINIMUM_VALIDATION_CONTRACT_V1.md` | `52297aeb0eeddd6b6698d5bdc5f0bdd8b1e7f85fd8d1d0b943b06cd6a3ca932e` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `4617c93b768fec5d853afcaaf16f0153a4e49e40` | `docs/reflect/REFLECT_MIRROR_SELECTION_V1.md` | `a6f76d1c2e0514c79d3280a3753aa4f204f4c95ed4a01548384363efefc1ab6e` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `68393ff5a483c4f5e4beaf93caa9c4af282147d8` | `docs/reflect/REFLECT_OBJECT_MODEL_V1.md` | `a7672573c6d097f125b397e8d118cefa561c6e28fdd3295655ca0f6926a76940` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `703963f3aab36f319b62bdc741d0614396875cd7` | `docs/reflect/REFLECT_OVERVIEW_V1.md` | `dab5bb94b4ee94ed70d46b2641c06c80c8e6b0e913cfd0e15f87234aad35dea4` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `82150e8199dad02ddff6f5f5018b278ee4645ed6` | `docs/reflect/REFLECT_PRESERVATION_STATE_MODEL_V1.md` | `f6e55314d50288b5a9dfe842a0ce0438ecd80e3c66404f23477b4dc20920937e` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `a76b07d21d7f7a0cbdcc602cba13f13fb377477b` | `docs/reflect/REFLECT_PUBLICATION_WINDOW_V1.md` | `ddba39654591027e0c241587f9889c780121953111e0949593a5862896ceaf08` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `eb677c2017e0d16cfd1910a72179ff3f05ebef5b` | `docs/reflect/REFLECT_RECONSTRUCTION_BOUNDARY_V1.md` | `59acbcaaefa5c37481a8da891400d01d8b1006cbad2cebf6097bebc2d8dc5070` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `ec44eb3ff7bc469ba9f869330d034e42c0e994c2` | `docs/reflect/REFLECT_RETRIEVAL_PROVIDER_EVOLUTION_V1.md` | `dccc91093199975ada8376db4ce153462cb2f8998b39c870306b82947f098f24` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `002f025f02649bb8200721850e8d9e2a862f44fc` | `docs/reflect/REFLECT_RETRIEVED_MATERIAL_CONTRACT_V1.md` | `3da8c29a1285d0b81255b7fbabbe2d9f876b1ee432077251c30170e77726e284` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `86b05ba1dc826b681170c760d32a66d7a0b7f691` | `docs/reflect/REFLECT_RUNTIME_MAPPING_AND_INVARIANT_HARNESS_V1.md` | `f354cea08311870c83fb0c694be0e8a74d8fcec72109b4755f8eacdd17f94345` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `6dad8c321716c8d3b1b64b5cb66c734f8cca3a9a` | `docs/reflect/REFLECT_SELECTION_POLICY_V1.md` | `c0feabce17d7ef1f8c1038ff5b9d3923bf3452568b368e28440a1bcf645e1687` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `d27c5335ecf8c7277aded665f316f12d9c7809ea` | `docs/reflect/REFLECT_STATE_VALIDITY_V1.md` | `49bfb0a3eef7d8bc28699648e019b1eac614d870ce262cbf0b97b877ba05d55c` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `aeb90e9786c10b0a0de93806c24a39bfacf9b69d` | `docs/reflect/REFLECT_TRUST_BOUNDARY_V1.md` | `062e8a457636f9ea39ee2d5e6709b39508c0ce98f0843d81a99d192c881c9582` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `802edaf54210da7a42f9f65579e91bb68f76eb52` | `docs/tempest/TEMPEST_FAILURE_AND_FALLBACK_V1.md` | `c0a52dbae6844904158e7be75dd0b69143dae1cb0932d74f80d1694f091e5e20` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `5419b9d8ca2b47d3cd10aa45b0b6bfecf5537e4a` | `docs/tempest/TEMPEST_OBSERVABILITY_POLICY_V1.md` | `66120c24d95b3d5d2494010d83cf6dd7b77a3fab2c5001d249673f3587a9ac9f` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `a36ba3bdd27459f08863ce16562049cf2c19f396` | `docs/tempest/TEMPEST_OVERVIEW_V1.md` | `8dc9fdce6dc37a06d84a45103c3e6a62fd9ee8dea358c3ec14dbc77333468542` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `c636a35fcfb510691da9015886af31a43bbe0d24` | `docs/tempest/TEMPEST_RELAY_INTERFACE_V1.md` | `c149878714aadecedc7a915f344bbe35c42cc0d3c4e36a67bb860e9643913f0a` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `f2a4372326855bdd7b927c4c1d44cc2dc1070129` | `docs/tempest/TEMPEST_RELAY_SELECTION_V1.md` | `b09eba0f1fc4ac88f6f52ca7578009fad6b30519a77a860e5a042cfa3afd2040` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `6937c74e41d6f3b035af32f3a76a1fac0dc20876` | `docs/tempest/TEMPEST_TREASURY_CONTINUITY_V1.md` | `2ed553d74d4a467399a625702ee3f693c9d1eaf8a7be42472ec3c26e291a25a0` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `63f58fccf45d1d0bbc6c877834c3b1351f04fa64` | `frontend/eslint.config.js` | `692054ce52fe7885fc3699c9ffe6b0d31fa4019b6d5d620092a14ea05a026842` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `8f5cb9ebb7fce70688aa7d6056372f8e2e3f49a1` | `frontend/index.html` | `cb3f0ca5bc70316d227e4c459a0505c5d9289d5362309ceb8e04c62a8609d2fd` | application-owned | application presentation asset | TD |
| 100644 | blob | `cfa620aa887622c3a3be9a494b19295dab9bed2f` | `frontend/package-lock.json` | `874606aec8c3077c98ea3451d1976af9e3588f63cf05696ee323c3d5e73b341b` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `9b8ec83b98a2c11394a2fa7dbdd99949b75e68e2` | `frontend/package.json` | `8bf1e8594059cfc04371a08e80d3d830ae9fb4b0c6fb11e2ff3ce2f445d07914` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` | `frontend/public/favicon.ico` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | application-owned | application presentation asset | TD |
| 100644 | blob | `4b84713d0e324e8faa2c95123b43b3dbaaf6683a` | `frontend/public/zk/sign_petition.wasm` | `996ad4bcf08548125ae15fbf98a9748170647d8609bdbade16003c3cd351dcb3` | protocol-facing | tracked generated cryptographic artifact | TD,RG |
| 100644 | blob | `88cc57d0b532a3531c53aa41d3afef9955a38bf1` | `frontend/public/zk/sign_petition_final.zkey` | `762433cb44fc19ff7ebf575b71f56af75f17b161f87102517a6259086b9b99f1` | protocol-facing | tracked generated cryptographic artifact | TD,RG |
| 100644 | blob | `ab18b9824d790427241e39a6d37fe94b37a599f3` | `frontend/public/zk/verification_key.json` | `8548836eaeb4500e19ca9032852095b257a9a5267206dd4e8180740c8841d14c` | protocol-facing | tracked generated cryptographic artifact | TD,RG |
| 100644 | blob | `8109cc9399ed1a003b0558e6c82ae63c5c2e84ed` | `frontend/src/Analytics.css` | `64f0d4a7d9042ab3206451ac1a1892d5ce93f7541d403ba53b62452da5586603` | application-owned | application presentation asset | TD |
| 100644 | blob | `7180cb177ecedc99337f7fd3216bf4afad4e341f` | `frontend/src/Analytics.jsx` | `80dd45c947d7cd4ecf10cdd644e31c9d9edff11be89ff8b50b86197867920178` | application-owned | application source | TD |
| 100644 | blob | `cfdc97bb94a753f98f305d3b44545aff3bef3e2a` | `frontend/src/App.css` | `67377ead0f424eb123f0d00246f7aaf42c537068bbb2e79ddd19b50652d7b9f9` | application-owned | application presentation asset | TD |
| 100644 | blob | `c45362305cec58040889009ca979fe2dc3337ef1` | `frontend/src/App.jsx` | `6c51af22ac4b66a91083c8c570976414c8083c60fce6999cf5a7d396848b4c00` | application-owned | application source | TD |
| 100644 | blob | `1b2abbcb59cfabf4f2d90777ceabd86cb53775d2` | `frontend/src/HomePage.css` | `8cda2150cd1f992e9bad1ce86c647eb14c23b101f49cfafb2820fd85ef8b9483` | application-owned | application presentation asset | TD |
| 100644 | blob | `0f3ab682ae39aa6f6286138b0386ac9914288809` | `frontend/src/HomePage.jsx` | `158d3793da734b410a9c24baf4b67a2b51634fe62c8e9cca717a2526df2aa335` | application-owned | application source | TD |
| 100644 | blob | `c3d2998f385e3441cc48c3f5a34fc69c5fc24a8a` | `frontend/src/PetitionDetails.css` | `e7fcd149af2a9943f7d06711e2ba38ffd80993f6db374f4023b9715b79e069b6` | application-owned | application presentation asset | TD |
| 100644 | blob | `c7e1df6023e1f14243180e13eccdb2cff3605518` | `frontend/src/PetitionDetails.jsx` | `83f8c391694ba6533e671ae17872f851b959d438df856ddd2907661283a001a2` | application-owned | application source | TD |
| 100644 | blob | `e53f5cff57cba930985995796debc9eac69570ad` | `frontend/src/Petitions.css` | `38f1830814277e4614371435ca5e82b5891d9173ba4669eb1c378e36514f0469` | application-owned | application presentation asset | TD |
| 100644 | blob | `0dae56d4f92af0fc2bf4bf8eb9063337badec060` | `frontend/src/Petitions.jsx` | `9fb6c10f2444c7825c1c6c76a06ea2bad0510783086f28cc51f92d32872862f4` | application-owned | application source | TD |
| 100644 | blob | `a34ad636b74f0b05205d6d74943655ed3e0d9792` | `frontend/src/components/M2IdentityControls.jsx` | `057573fb89a75d370bac6b7ab00476da0ab2f5d3ad170ffea1a5d7da29dfce02` | mixed | client interface and runtime source | TD,RO |
| 100644 | blob | `42d27697f8ee796210f649257c94247220728f99` | `frontend/src/components/M2SignButton.jsx` | `16faf8dba309411ebc40ae00c66cbfda4b2e32e48c18b46d422bcffc7c1e96f2` | mixed | client interface and runtime source | TD,RO |
| 100644 | blob | `d1e18f63ca9966ff9ce26c8a5e73d86f6ac5f6f3` | `frontend/src/components/M2StatusSection.jsx` | `741d2d6b81ca6335db08eb1a64e3d2218ce6d0165da9b13ab2f06dec3fcd57b9` | mixed | client interface and runtime source | TD,RO |
| 100644 | blob | `845783321f5050d464b25f81eab445266e1fc563` | `frontend/src/components/PetitionDisplaySection.jsx` | `34d0b2604c827717c60a3d62b16b212842bf8deac4a65ddde8267ba9e4759d45` | application-owned | application source | TD |
| 100644 | blob | `3facdc8697b1a1165892b3b791c75f8729ea15a2` | `frontend/src/config.js` | `165471f0585cdd3b62123bd99fd0c678e01097f65d8d6c4983f6ed4bbb82033f` | mixed | configuration and runtime source | TD,DB |
| 100644 | blob | `5e227a1008164a8a2bd08c670c771e901361dd33` | `frontend/src/continuityBundle.js` | `c901ba3752165b8cd989382891d9d8e8d588c48fc96bd0cdf3c41c7b1ddb2b21` | protocol-facing | client runtime source | TD,RO |
| 100644 | blob | `985e8adb8410a134fa010d2fa49ee179e47edfb5` | `frontend/src/hooks/useZKProof.js` | `8df56093b0a5a3ed8121e3cbe45761d0cfc967bc0fcdd108222944f5901a575a` | protocol-facing | client runtime source | TD,RO |
| 100644 | blob | `cddeb725f674130f737b67ca1e6e5acd40baee92` | `frontend/src/index.css` | `f45c65f12b1ce5b1f36e59f6e51013377bc4d41f0b0d434459f9884722dd09c7` | application-owned | application presentation asset | TD |
| 100644 | blob | `42a0416dbfcfa61a37a2138f9ac3f497927b344f` | `frontend/src/m2Identity.js` | `3c019252a21925c4f6f4392b4ba1bdf442a6b02a32e17dd5916d89ef1f0dddcb` | protocol-facing | client runtime source | TD,RO |
| 100644 | blob | `86a1d7f1dd9d0e3da03679f1ea19e9c62bed7903` | `frontend/src/main.jsx` | `c089eb4259942b9a77cd0428b73a7f00b494a59989a07a783666839ab9cef913` | application-owned | application source | TD |
| 100644 | blob | `db06a7566dc675120ddd739b8a30f00a70ff8397` | `frontend/src/theme.css` | `547613ef3b2ba4373e613883de15ab9d108f6bc2ab50357995e20ae2f6014bfe` | application-owned | application presentation asset | TD |
| 100644 | blob | `3f905c35dbbc32589e898af7575d647ed16a6fda` | `frontend/vite.config.js` | `e10699546c9bd8e403bed776e693b66aeb103569515d76f20aaaf1351f3eace2` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `f783d3ae48f05448cb40abf7cd80e124d5d1b4a9` | `package.json` | `f82ecaf031ce49ef22787aa294ca121345ac8637ff9b3220de7090a6faa72244` | evidence-support | build or dependency input | TD |
| 100644 | blob | `69ef5a519f6b6ab1ecabf8bb8398efa9e7230dcc` | `request.json` | `9dd3d1a63d41cd439a39e607717d16124b68d8c46c0dec56afc5a677c49a11eb` | protocol-facing | sample interface payload | TD |
| 100755 | blob | `e02a8bfb10b00a5686039454de5bd4d7576276b2` | `scripts/zk/run_golden_proof.sh` | `4ad2be577a8dd3db5d612b30876b3fa1149fa647ee7656f1a04d420c1a0add74` | protocol-facing | verification operation | TD,RG |
| 100755 | blob | `08a776e1471b30c723f75ef2d66e02fb62925c61` | `scripts/zk/verify_manifest.sh` | `06a8df3c7b277c3dc7fa8d7f97215e8b1f80140a9588304dd6fd043ec3038214` | protocol-facing | verification operation | TD,RG |
| 100644 | blob | `9e22680b956eb7545632ccdd495a634fef14b2d4` | `zk/v3-groth16/.gitignore` | `f94a95a7a130241c3e03a22e5acb19047874ae3ad399698f6abbeb2b0cf666c2` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `a63fda39e9eb495f0059d9c3d26c6cd4201a7e4b` | `zk/v3-groth16/ARTIFACTS.md` | `1af3815610ba2e85e217b59e55cdc61872980dba1a091d8127d2a7ca06746022` | protocol-facing | bounded implementation documentation | BD |
| 100644 | blob | `165ed8cfa1029dd0a937ab6e885af020fbf991e5` | `zk/v3-groth16/circuits/sign_petition.circom` | `a64783f8873df0c9dda7f7e44607e076f0b2af94c9cd609e4619e4b0fbcf2e02` | protocol-facing | circuit source | TD,RG |
| 100755 | blob | `c082f357083db53376799d4633d63f24714483da` | `zk/v3-groth16/compile-and-setup-groth16.sh` | `879136b2357c7d27ed2ca0670b592d144af32fcd11c19371d5f6d0ac7c78a56e` | protocol-facing | generation or verification operation | TD,RG |
| 100644 | blob | `bf3bd28b1e89e8672219aa5aea6e54605d1b5bfe` | `zk/v3-groth16/contracts/Groth16Verifier.sol` | `b1216366353f3dbf478e1e03add31077bbe4bc76d5a4e40aaba574cd5841bd87` | protocol-facing | tracked generated cryptographic artifact | TD,RG |
| 100755 | blob | `a149bee9fbb0839df7ecdf1e6803c8272057fb2b` | `zk/v3-groth16/download-powers-of-tau.sh` | `356a6bb9efb5876457f4c3abc4ee503196e912fedcdfb96577ab1982c1c09686` | protocol-facing | generation or verification operation | TD,RG |
| 100755 | blob | `ac5dc272e5f0d24f2fcabea800d60f66ace8ce96` | `zk/v3-groth16/freeze-artifacts.sh` | `73367d017d9146631d8dc36fa2fb700a4d4a3396ff18bd69af8f62450dce0489` | protocol-facing | generation or verification operation | TD,RG |
| 100644 | blob | `e932574e7599067cbfc3baf3ee3d98808e944aca` | `zk/v3-groth16/golden-proof.json` | `01360c724f748b1630b6605bf7464af585643a0d87fcbbb2a21e3fa3025a63b7` | protocol-facing | tracked generated cryptographic artifact | TD,RG |
| 100755 | blob | `9cc0208d7e9d69c2058dbaf9f1f1d006bf9d0bee` | `zk/v3-groth16/install-groth16-deps.sh` | `610f2126c80b587f4210540b746bc42c2927eff1e89debf3615c02d452dea437` | protocol-facing | generation or verification operation | TD,RG |
| 100644 | blob | `ab18b9824d790427241e39a6d37fe94b37a599f3` | `zk/v3-groth16/keys/verification_key.json` | `8548836eaeb4500e19ca9032852095b257a9a5267206dd4e8180740c8841d14c` | protocol-facing | tracked generated cryptographic artifact | TD,RG |
| 100644 | blob | `59b55fe7f8bd9bd91ab95d0732a89507cbced0e2` | `zk/v3-groth16/package-lock.json` | `48f815e8e8dd546a1679caefae3d3e949706ed2f16e9056887b811522d45c093` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `ce41f4a51cd51768bd22e62f5e321afbccb6f315` | `zk/v3-groth16/package.json` | `66241121a4af5f07a978d171a3f5dc4c3994482ef5e9155be9822260c8aa07a3` | evidence-support | build or dependency input | TD,RG |
| 100644 | blob | `6aebd8f293a8b2f97d266f34084c5e9b6409de5e` | `zk/v3-groth16/test-golden-proof.js` | `a2744c49785c905a552e9612f7a4e536e028ea59d5a8ba7978dd534a73b4cbd7` | protocol-facing | generation or verification operation | TD,RG |
| 100755 | blob | `04e8e1bc545fd4c87e5f6792b8f960999c68717d` | `zk/v3-groth16/test-on-chain.sh` | `a097eccc184fc0489288158df789fd1adb8bef516b7c973c03edf0d6fec93f7a` | protocol-facing | generation or verification operation | TD,RG |

## 8. Evidence-Path Vocabulary

| Code | Evidence-availability meaning |
|---|---|
| TD | Tracked direct evidence: material exists as a tracked baseline path or Git identity. |
| RG | Reproducibly generated evidence: a bounded process may produce build, test, verification, or integrity output from identified inputs. |
| DB | Deployment-bound evidence: usefulness depends on a proven deployment-to-baseline relationship. |
| RO | Runtime-observation evidence: usefulness depends on a bounded observation tied to the baseline, deployment, configuration, and occurrence. |
| BD | Bounded documentation evidence: documentation may establish declared identity, scope, mapping, or interpretation but does not replace behavioral evidence. |
| ME | Missing evidence path: no bounded candidate path is identified. No coverage row currently receives this classification. |
| AE | Ambiguous evidence path: candidates exist, but their exact responsibility, formal mapping, provenance, or choice position is not yet sufficiently bounded. |
| NR | Not required under the preserved Profile V2 non-applicable disposition. |

A coverage path state of `bounded` means only that a later evidence route is identifiable. It does not mean evidence is sufficient or that the requirement is satisfied.

## 9. Evidence Sets

Evidence-set references are compact routing identifiers. Each set remains subordinate to the exact path inventory and the applicable requirement.

| Set | Name | Bounded candidate material | Classes |
|---|---|---|---|
| E01 | Authority and requirements | Published specification, Profile V2, Engineering[165] scope record, and guarded formal corpus. | BD |
| E02 | Baseline provenance | engineering-164 commit, tree, 308-path Git inventory, blob identities, Gitlinks, dependency locks, and build inputs. | TD,RG |
| E03 | Cross-surface privacy and naming | All protocol-facing and mixed tracked surfaces plus later bounded static, diagnostic, logging, and runtime observation. | BD,TD,RG,DB,RO |
| E04 | Membership and continuity | AdmissionRegistry, AnonymousMembershipRegistry, Poseidon sources, circuit witness relation, client continuity helpers, membership tree/path services, tests, and bounded documentation. | BD,TD,RG,DB,RO |
| E05 | Proof construction and artifacts | Circuit, proof hook, tracked runtime artifacts, verification key, verifier exports, golden-proof material, manifest, and generation scripts. | BD,TD,RG |
| E06 | Verification, validity, and uniqueness | Verifier source, PetitionRegistry verification and nullifier surfaces, relay validation, focused tests, deployment binding, and runtime traces. | TD,RG,DB,RO |
| E07 | Action-processing candidates | PetitionRegistry signing surface, client submission surface, relay validation/execution, proof evidence, and later bounded transaction observations. | BD,TD,RG,DB,RO,AE |
| E08 | Transition, state, and history candidates | Current contract state changes and events, protocol-facing indexers and persistence, deployment relations, and runtime observations. | BD,TD,RG,DB,RO,AE |
| E09 | TEMPEST runtime | Relay route, deterministic execution, domain/configuration sources, tests, and bounded TEMPEST documentation. | BD,TD,RG,DB,RO |
| E10 | REFLECT path runtime | REFLECT services, tests, membership path route, tree reconstruction, and bounded REFLECT documentation. | BD,TD,RG,RO |
| E11 | Concrete interface candidates | Contract interfaces and public functions, embedded frontend ABIs, backend routes, configuration surfaces, and bounded interface documentation. | BD,TD,DB,RO,AE |
| E12 | Persistence and indexing | Migrations, repositories, event processors, synchronization logic, and later runtime database observations; application-owned meaning remains excluded. | TD,RG,RO |
| E13 | Reproducible checks | Tracked Solidity, JavaScript, shell, golden-proof, REFLECT, and TEMPEST tests or verification operations; execution results are not baseline identity. | TD,RG |
| E14 | Deployment binding | Deployment and verification scripts, address/configuration records, bytecode and proxy relationships, chain context, and later provenance checks. | BD,TD,DB |
| E15 | Runtime observation | Future bounded chain, API, failure-path, state, history, and observability records tied to the fixed baseline and declared runtime context. | RO |
| E16 | Application boundary | Application-owned and mixed files used only to separate protocol-facing responsibility from petition meaning, metadata, policy, UI, and interpretation. | BD,TD |
| E17 | Historical or inactive material | Legacy directories and paths whose current responsibility is historical, inactive, or unresolved; never silently merged into current behavior. | BD,TD,AE |
| E18 | Permitted-choice position | Baseline structure, declared configuration, implementation documentation, and later observations capable of identifying an exercised choice without inventing a default. | BD,TD,DB,RO,AE |
| E19 | ZK provenance ambiguity | Manifest-to-baseline presence, digest, and consistency inventory, including generation paths for untracked canonical artifacts. | TD,RG,AE |
| E20 | Formal lifecycle mapping ambiguity | Candidate Action, Evaluation, Determination, no-transition, transition, failure, staleness, and re-evaluation surfaces whose exact formal-to-runtime mapping is not yet explicit. | BD,TD,DB,RO,AE |
| E21 | Implementation identity and scope | Engineering[165] baseline identity, Git revision identity, tracked composition, profile target, and bounded responsibility inventory. | BD,TD |

## 10. Protocol, Application, and Implementation-Structure Boundary

Speak-up remains the first reference use case. Petition meaning, lifecycle, metadata, moderation, eligibility, policy, UI, and interpretation remain application-owned. A mixed file contributes only its protocol-facing responsibility to later assessment.

M2, TEMPEST, and REFLECT remain implementation structures. Their files may provide evidence, but their names, topology, algorithms, decomposition, or repository locations do not become Profile V2 identity, protocol law, or a structure another implementation must copy.

Historical, inactive, or ambiguous-status material is never silently merged into current implementation behavior. Its relationship must be independently established before later use.

## 11. Generated, Dependency, Deployment, and Runtime Boundary

The baseline contains tracked cryptographic runtime artifacts, integrity records, build inputs, lockfiles, generation scripts, deployment scripts, and three Git dependency links. Generated outputs not tracked at engineering-164 remain reproducibly generated candidates rather than baseline paths.

Deployment evidence must identify chain and network context, deployed code or bytecode identity, proxy and implementation relationships, configuration state, build relationship, observation occurrence, and material differences from the baseline tree.

Runtime observations must remain bounded to their occurrence and must not be promoted into baseline identity, protocol truth, complete requirement satisfaction, or actor identity.

## 12. ZK Artifact Provenance Inventory

The following records compare the tracked engineering-164 manifest with the tracked engineering-164 tree. They are evidence-availability observations only.

| Manifest item | Path | Baseline presence | Recorded SHA-256 | Observed SHA-256 | Inventory relation |
|---|---|---|---|---|---|
| r1cs_canonical | `zk/v3-groth16/build/sign_petition.r1cs` | absent from tracked baseline | `ae963d20454fdefef6d5f88fe0f5831923ebe0900df9e472b10386cf025f7677` | `not-available` | tracked item absent; reproducible-generation path identified |
| wasm_canonical | `zk/v3-groth16/build/sign_petition_js/sign_petition.wasm` | absent from tracked baseline | `996ad4bcf08548125ae15fbf98a9748170647d8609bdbade16003c3cd351dcb3` | `not-available` | tracked item absent; reproducible-generation path identified |
| zkey_canonical | `zk/v3-groth16/keys/sign_petition_final.zkey` | absent from tracked baseline | `762433cb44fc19ff7ebf575b71f56af75f17b161f87102517a6259086b9b99f1` | `not-available` | tracked item absent; reproducible-generation path identified |
| vkey_canonical | `zk/v3-groth16/keys/verification_key.json` | tracked | `8548836eaeb4500e19ca9032852095b257a9a5267206dd4e8180740c8841d14c` | `8548836eaeb4500e19ca9032852095b257a9a5267206dd4e8180740c8841d14c` | recorded digest matches |
| golden_proof | `zk/v3-groth16/golden-proof.json` | tracked | `7d81531f80ad85682f2673bd0abce43becfd9a416d240d6eba430a2362d2f6fa` | `01360c724f748b1630b6605bf7464af585643a0d87fcbbb2a21e3fa3025a63b7` | recorded digest differs |
| verifier_source | `contracts/src/v3/Groth16Verifier.sol` | tracked | `b1216366353f3dbf478e1e03add31077bbe4bc76d5a4e40aaba574cd5841bd87` | `b1216366353f3dbf478e1e03add31077bbe4bc76d5a4e40aaba574cd5841bd87` | recorded digest matches |
| frontend_wasm_runtime | `frontend/public/zk/sign_petition.wasm` | tracked | `996ad4bcf08548125ae15fbf98a9748170647d8609bdbade16003c3cd351dcb3` | `996ad4bcf08548125ae15fbf98a9748170647d8609bdbade16003c3cd351dcb3` | recorded digest matches |
| frontend_zkey_runtime | `frontend/public/zk/sign_petition_final.zkey` | tracked | `762433cb44fc19ff7ebf575b71f56af75f17b161f87102517a6259086b9b99f1` | `762433cb44fc19ff7ebf575b71f56af75f17b161f87102517a6259086b9b99f1` | recorded digest matches |
| frontend_vkey_runtime | `frontend/public/zk/verification_key.json` | tracked | `8548836eaeb4500e19ca9032852095b257a9a5267206dd4e8180740c8841d14c` | `8548836eaeb4500e19ca9032852095b257a9a5267206dd4e8180740c8841d14c` | recorded digest matches |
| frontend_proof_hook | `frontend/src/hooks/useZKProof.js` | tracked | `e2620d78620e2b0b8fe7a9f316c057747ce695e9a04d37f4e1c455e25609d61f` | `8df56093b0a5a3ed8121e3cbe45761d0cfc967bc0fcdd108222944f5901a575a` | recorded digest differs |
| frontend_sign_button | `frontend/src/components/M2SignButton.jsx` | tracked | `1b0df4df7706acbcde2adb76fb4b86a9991d9eb1305d0cc41084248204704189` | `16faf8dba309411ebc40ae00c66cbfda4b2e32e48c18b46d422bcffc7c1e96f2` | recorded digest differs |
| frontend_config | `frontend/src/config.js` | tracked | `165471f0585cdd3b62123bd99fd0c678e01097f65d8d6c4983f6ed4bbb82033f` | `165471f0585cdd3b62123bd99fd0c678e01097f65d8d6c4983f6ed4bbb82033f` | recorded digest matches |

| Consistency check | Left | Right | Inventory relation |
|---|---|---|---|
| frontend_runtime_wasm_matches_canonical_wasm | `zk/v3-groth16/build/sign_petition_js/sign_petition.wasm` | `frontend/public/zk/sign_petition.wasm` | not directly comparable from tracked baseline |
| frontend_runtime_zkey_matches_canonical_zkey | `zk/v3-groth16/keys/sign_petition_final.zkey` | `frontend/public/zk/sign_petition_final.zkey` | not directly comparable from tracked baseline |
| frontend_runtime_vkey_matches_canonical_vkey | `zk/v3-groth16/keys/verification_key.json` | `frontend/public/zk/verification_key.json` | byte-identical |

Three manifest items are absent from the tracked baseline but have identified generation paths; three tracked items differ from their recorded manifest digests; six tracked items match. These facts create E19 provenance ambiguity. They do not determine a requirement failure, implementation defect, security result, or remediation requirement.

## 13. Formal Lifecycle Mapping Inventory

The tracked runtime/source surface contains no exact textual occurrence of the following formal terms:

| Formal term | Exact runtime/source occurrences |
|---|---:|
| Protocol Action Evaluation | 0 |
| Protocol Action Determination | 0 |
| accepted no-transition | 0 |
| stale authorization | 0 |
| re-evaluation | 0 |
| evaluation context | 0 |
| applicable rule set | 0 |
| transition occurrence | 0 |
| successor state | 0 |

Exact-term absence does not prove semantic absence and is not used as a requirement result. Combined with the lack of one explicit implementation-owned formal lifecycle map, it makes the candidate E07/E08/E20 relationship ambiguous for later assessment.

## 14. Coverage Method

For each Profile V2 row R, this record preserves the identifier, RF family, SF home, strength, published applicability, profile disposition, published order, and byte identity of the complete profile row. It then assigns candidate evidence sets, availability classes, and one path state.

> applicable or permitted-choice -> bounded candidate path or explicit ambiguity

> non-applicable -> preserved Profile V2 decision -> NR

> evidence availability != evidence sufficiency != requirement result

No normative statement is copied into this record, and implementation behavior does not alter profile meaning.

## 15. Coverage Summary

| Profile disposition | Bounded path | Ambiguous path | Not required | Total |
|---|---:|---:|---:|---:|
| applicable | 193 | 285 | 0 | 478 |
| conditionally applicable | 0 | 0 | 0 | 0 |
| non-applicable | 0 | 0 | 244 | 244 |
| resolved through permitted specification choice | 0 | 7 | 0 | 7 |
| **Total** | **193** | **292** | **244** | **729** |

All 244 non-applicable rows remain preserved Profile V2 decisions. No implementation-created exclusion is introduced.

All seven permitted-choice rows have candidate evidence routes but remain ambiguous because the baseline does not contain one explicit bounded declaration of the exercised choice position. No default or choice result is inferred.

## 16. Complete 729-Row Assessment Coverage Map

`Profile row SHA-256` binds each coverage entry to the complete unchanged Profile V2 ledger row without copying its normative source statement or profile justification fields.

| Identifier | RF | SF | Strength | Published applicability | Profile disposition | Evidence sets | Availability | Path state | Profile row SHA-256 |
|---|---|---|---|---|---|---|---|---|---|
| PE-SPEC-001 | RF-01 | SF-01 | MUST | Every Privacy Engine Protocol Specification | non-applicable | E01 | NR | not-required | `09939546915b674579bb91e78e0484a3c49c0effe6cd3bd1dda583ef247569a5` |
| PE-SPEC-002 | RF-01 | SF-01 | MUST | Every completed Privacy Engine Protocol Specification | non-applicable | E01 | NR | not-required | `00f31cc80bd4ef21d60966327e1d82a450ea808f573f2ff14744deda4e78ec4d` |
| PE-SPEC-003 | RF-01 | SF-01 | MUST | Every Privacy Engine Protocol Specification | non-applicable | E01 | NR | not-required | `d0871a71c82480af494a92ced1215c1834cc4e80a09272d7e85cf339b844c07f` |
| PE-SPEC-004 | RF-01 | SF-01 | MUST | Every completed Privacy Engine Protocol Specification | non-applicable | E01 | NR | not-required | `8a1391949ea6a260a5f4b08843d750620183cad18be6dbf67ee2d66b1197266c` |
| PE-SPEC-005 | RF-01 | SF-01 | MUST NOT | Every incomplete cumulative Protocol Specification | non-applicable | E01 | NR | not-required | `73b9e95d299d39d2b7a80e8f282a7298a1f59300373626984e4fe189cac26dd7` |
| PE-SPEC-006 | RF-01 | SF-01 | MUST NOT | Every Privacy Engine Protocol Specification and every interpretation of it | applicable | E01 | BD | bounded | `732ca07d64df9153dc8b40bbc739830253a2d9852135f48d4e97a7a92544c7bf` |
| PE-SPEC-007 | RF-01 | SF-01 | MUST | Every cumulative Protocol Specification | non-applicable | E01 | NR | not-required | `6ef9fddbcab273de00849dcb77d68d03d392d0540c9a4b2a74a8c5f028819320` |
| PE-SPEC-008 | RF-01 | SF-01 | MUST | Every semantic requirement composed into the Protocol Specification | applicable | E01 | BD | bounded | `a2d95dffe79ea42b8be366bb24a6df6dc682b03bed5df0d3b654050e6c71bb0c` |
| PE-NORM-001 | RF-05 | SF-01 | MUST | Every statement in the Protocol Specification | applicable | E01 | BD | bounded | `5daa1cc43741716f47e920fdd328e155364fcf817ff843c3db37e594de12c0dd` |
| PE-NORM-002 | RF-05 | SF-01 | MUST | Every requirement using `MUST` | applicable | E01 | BD | bounded | `3850897963294860a2295abd5ed90f1adcb22583b1547d50642fd165572d8b1b` |
| PE-NORM-003 | RF-05 | SF-01 | MUST | Every requirement using `MUST NOT` | applicable | E01 | BD | bounded | `e21700a64e7ad0fb90cb3b943288fe375ddf85797bb5a5b670b6956d14b21727` |
| PE-NORM-004 | RF-05 | SF-01 | MUST | Every requirement using `SHOULD` | applicable | E01 | BD | bounded | `783f7325ca944d33c07adc633333373ab89b706fce3b2d56904ea5749ca48310` |
| PE-NORM-005 | RF-05 | SF-01 | MUST | Every requirement using `SHOULD NOT` | applicable | E01 | BD | bounded | `92c1e4dd310859fa0ef288f64f7ec8b7e241a93be00dac108b6b24e0ba0f0d0c` |
| PE-NORM-006 | RF-05 | SF-01 | MUST | Every requirement using `MAY` | applicable | E01 | BD | bounded | `9470199ded75ee4ab74d48233b15e79da45b384f560596703ea923d895326562` |
| PE-NORM-007 | RF-05 | SF-01 | MUST | Every declaration of implementation-defined behavior | applicable | E01 | BD | bounded | `224a80c10ad5d0140ca074cebbc3c7f1acb32e35c0e98197e20eb3c078dccb9b` |
| PE-NORM-008 | RF-05 | SF-01 | MUST | Every normative requirement | applicable | E01 | BD | bounded | `905b17f7e97e7bf64746f71675deab0bb8ce2d09e8e3ba916f323924ad7c2c23` |
| PE-NORM-009 | RF-05 | SF-01 | MUST | Every interpretation of a normative requirement | applicable | E01 | BD | bounded | `28c71ec7f1b73716cab6b49cabb2861558652b709dba8a6319cc83035d505ad1` |
| PE-NORM-010 | RF-05 | SF-01 | MUST NOT | Every supporting cross-reference and informative statement | applicable | E01 | BD | bounded | `af9049bc0bce78e9be82cd64bbf4b00fd1ae2352304db3319c178667401c2ff5` |
| PE-NORM-011 | RF-05 | SF-01 | MUST | Every normative requirement | applicable | E01 | BD | bounded | `64050844c880c3863fa930f85b5c448c8d16c4f5d6a183e2ac637998eb6da0f8` |
| PE-NORM-012 | RF-05 | SF-01 | MUST NOT | Every requirement identifier lifecycle | applicable | E01 | BD | bounded | `defb9f0c8ffba34f5fa5dc4455548ea3097f957ba405c482981b04a962fed365` |
| PE-NORM-013 | RF-05 | SF-01 | MUST | Every normative requirement | applicable | E01 | BD | bounded | `c793887eb5adca2ea58dc2f4157978b236f0a0a7d7cba7893a0f251383bc0a35` |
| PE-NORM-014 | RF-05 | SF-01 | MUST | Every apparently obligatory specification statement | applicable | E01 | BD | bounded | `35240275dd43ce24f6c1e65861d5f90224678e5f847b0a537adc21f16bdab0f3` |
| PE-PROT-001 | RF-02 | SF-01 | MUST | Every Privacy Engine Protocol definition | non-applicable | E01 | NR | not-required | `2db3811c11d969e627f3c953d85668d8bd0e87b3608ead56060ae859733fd3e1` |
| PE-PROT-002 | RF-02 | SF-01 | MUST | Every published Privacy Engine protocol generation | non-applicable | E01 | NR | not-required | `fc929e5d1d9842e788865586b7f991b6e2805d1003037d6b43ecc6fdeeaf9c82` |
| PE-PROT-003 | RF-02 | SF-01 | MUST | Every protocol invariant | non-applicable | E01 | NR | not-required | `f2a0999d861bb6f0040110112563ebd6fdbfb0167d9734543014e4490bf82340` |
| PE-PROT-004 | RF-02 | SF-01 | MUST NOT | Every downstream specification, profile, implementation, application, assessment, and certification artifact | applicable | E01,E02,E21 | BD,TD | bounded | `9c5eb141ae399653022f5d77474dc300fb2f99b8b255e237c77369c03c11a164` |
| PE-PROT-005 | RF-02 | SF-01 | MUST | Every claim of complete protocol realization | applicable | E01,E02,E21 | BD,TD | bounded | `6ccdb6021296e1e0810ed2a3d798a001d7f3903115ced51722e2f9a83424dbad` |
| PE-PROT-006 | RF-02 | SF-01 | MUST NOT | Every application and implementation using the Privacy Engine Protocol | applicable | E01,E02,E21 | BD,TD | bounded | `06c4d95cbdc913c80308d07d6d54d029055f3681ff8cefab10920d5a2cc68fc8` |
| PE-GEN-001 | RF-03 | SF-02 | MUST | Every Privacy Engine Protocol Generation | non-applicable | E01 | NR | not-required | `2f65253005cff2cb98d408333f962f0c19205e89587829bb80e5cac994f33b8d` |
| PE-GEN-002 | RF-03 | SF-02 | MUST | Every Privacy Engine Protocol Generation | non-applicable | E01 | NR | not-required | `aea9803ccf90709d3fac1d7f6fc76fc75d20fdf0c6df221283cb2adf69829f25` |
| PE-GEN-003 | RF-03 | SF-02 | MUST NOT | Every incomplete protocol fragment or partial change | non-applicable | E01 | NR | not-required | `73942bba109202bcdc40b992a3dbc13ce52723ca2e725f5373107226ba3eb470` |
| PE-GEN-004 | RF-03 | SF-02 | MUST | Every Protocol Generation lifecycle | non-applicable | E01 | NR | not-required | `f578600a08d53eb7a17d7a9f28022c3590f8384c1d053728d5791bb0e6e2d579` |
| PE-GEN-005 | RF-03 | SF-02 | MUST | Every Protocol Publication | non-applicable | E01 | NR | not-required | `759c076dec5c4c35fb0842c213c8afb904aecbea311603d4eb2c724cc95a4d73` |
| PE-GEN-006 | RF-03 | SF-02 | MUST | Every Protocol Publication | non-applicable | E01 | NR | not-required | `6ac3aa9120be5b131cebaef096358c9044f1c89f0e0b63868944bcbd77a2f931` |
| PE-GEN-007 | RF-03 | SF-02 | MUST NOT | Every incomplete or ambiguous publication occurrence | non-applicable | E01 | NR | not-required | `7e0c59fff9e25d4cc277a8b74d43ab07becdb781ef4aed23408f1365233c526d` |
| PE-GEN-008 | RF-03 | SF-02 | MUST NOT | Every Protocol Publication | non-applicable | E01 | NR | not-required | `6611afb2d9abe620cb5397a7d8a9f2e8ff693bb3873f6fa689f814b5a4db4262` |
| PE-GEN-009 | RF-03 | SF-02 | MUST | Every Published Protocol | non-applicable | E01 | NR | not-required | `7801f83a2872ba16254019b77ca72e9ee95c21dfc86cb7e67a6dda916817007e` |
| PE-GEN-010 | RF-03 | SF-02 | MUST | Every Published Protocol | non-applicable | E01 | NR | not-required | `6ec101e485cfd95037b050f2c83ae08f5d7d3cb48f764eb9093bdefe3b8bdd7b` |
| PE-GEN-011 | RF-03 | SF-02 | MUST NOT | Every Published Protocol | non-applicable | E01 | NR | not-required | `79961389a76492ebf58a90952cab5d5d2c3f5bf73ccb83c5f3c979e82837010c` |
| PE-GEN-012 | RF-03 | SF-02 | MUST | Every published Privacy Engine protocol generation | non-applicable | E01 | NR | not-required | `bcc089d5efa526e7c07e65825a0ce4823499bf6ee12836be67baa18b7d773d6b` |
| PE-GEN-013 | RF-03 | SF-02 | MUST | Every Protocol Publication claiming completeness | non-applicable | E01 | NR | not-required | `705c4ba92ddbc4cb5782eecbc005e745a24c3b765fbd82606bf155af43b3cd54` |
| PE-GEN-014 | RF-03 | SF-02 | MUST | Every Published Protocol | non-applicable | E01 | NR | not-required | `f5fb9518aaa5376f6a06da1285785f9eb1a068ac6c71c43383241692eaabd5ec` |
| PE-GEN-015 | RF-03 | SF-02 | MUST | Every correction, clarification, or replacement affecting published material | non-applicable | E01 | NR | not-required | `c7889738aa6a39e7d3dd5f0f4b69670e2683a148a878082b561259b4e69781c2` |
| PE-GEN-016 | RF-03 | SF-02 | MUST NOT | Every incomplete publication | non-applicable | E01 | NR | not-required | `bce23eb87a3a50591190c474230137e348c5d36cc102e477b711eb49e8ee9bf0` |
| PE-EVOL-001 | RF-04 | SF-02 | MUST | Every Protocol Succession relationship | non-applicable | E01 | NR | not-required | `01c7ed1fa307b35d17b24a172928ea0f50a845a66a51064c20de9f1e423d5a0a` |
| PE-EVOL-002 | RF-04 | SF-02 | MUST | Every successor Protocol Generation | non-applicable | E01 | NR | not-required | `2bd2f837982062ac4fad58caa8f455e828e78067ac53824f73455925012121e5` |
| PE-EVOL-003 | RF-04 | SF-02 | MUST | Every Protocol Succession relationship | non-applicable | E01 | NR | not-required | `9589a94e7f582ed415b4162a1d792c9ce028139a5318898fbf47fb694a5e7250` |
| PE-EVOL-004 | RF-04 | SF-02 | MUST NOT | Every Protocol Succession relationship | non-applicable | E01 | NR | not-required | `04b271775459ef022fd0d9d84c2a34a7f81f4bc7ad665ce0cf5df02d5d09ea2b` |
| PE-EVOL-005 | RF-04 | SF-02 | MUST NOT | Every Protocol Publication | non-applicable | E01 | NR | not-required | `b3c61608bd9c2bf61f4b70d8b3e578e50ecb801a8deec4d5fd89a2044e4bfa93` |
| PE-EVOL-006 | RF-04 | SF-02 | MUST | Every Protocol Lineage | non-applicable | E01 | NR | not-required | `654a40bcf5fe084e6f1954192e9e6a5ceaa56d12bbc731821b3a936a6a77ba73` |
| PE-EVOL-007 | RF-04 | SF-02 | MUST | Every Protocol Lineage membership claim | non-applicable | E01 | NR | not-required | `7ac355e190f71442edb837075aeb16b7ba492694c54ecc905207faa9532b6471` |
| PE-EVOL-008 | RF-04 | SF-02 | MUST | Every Protocol Lineage | non-applicable | E01 | NR | not-required | `9c3a1b680e2a93409a2b69b188107118ce213b29f8a8f59ad5caf4aae21ce0ac` |
| PE-EVOL-009 | RF-04 | SF-02 | MUST NOT | Every Protocol Lineage | non-applicable | E01 | NR | not-required | `4368a78d5ad35854135e2227fa4336e8d163b666741d04f0347310d95afd94ff` |
| PE-EVOL-010 | RF-04 | SF-02 | MUST | Every Protocol Lineage model | non-applicable | E01 | NR | not-required | `bb210f74b25c2ef1f2424525c024e69aa50b87ea8367738db97b12fcc61601be` |
| PE-EVOL-011 | RF-04 | SF-02 | MUST NOT | Every Protocol Lineage membership claim | non-applicable | E01 | NR | not-required | `0b89e6d92a118978574412f551c67790d58f43b7ae50f2b901caf88a57525fe3` |
| PE-EVOL-012 | RF-04 | SF-02 | MUST | Every published Protocol Generation | non-applicable | E01 | NR | not-required | `74f9b18a37bb992e046528abc8c08770e5d349e6324155bb0968908f44133096` |
| PE-EVOL-013 | RF-04 | SF-02 | MUST NOT | Every protocol version designation | non-applicable | E01 | NR | not-required | `6339859d87c25cec84bfacfa07cf0594fd1730b4a0f7b84c725b9b1f4545fb65` |
| PE-EVOL-014 | RF-04 | SF-02 | MUST | Every protocol semantic change | non-applicable | E01 | NR | not-required | `315fbf2b4fa540ba5f58ab84f6ca9bc7ee1d20ef531cb459491840c9a12b2c78` |
| PE-EVOL-015 | RF-04 | SF-02 | MUST NOT | Every published Protocol Generation | non-applicable | E01 | NR | not-required | `12fd6b51f9a39dfebcdcc1e0dccce9013740a3a47b626e96621ef83b4ddc951c` |
| PE-EVOL-016 | RF-04 | SF-02 | MUST | Every classification of a protocol change | non-applicable | E01 | NR | not-required | `33f45f4bb971b7a862acf02cc1a624af1d50e7553aeedbaa1a577996f3b0283b` |
| PE-EVOL-017 | RF-04 | SF-02 | MUST | Every claim of compatible evolution | non-applicable | E01 | NR | not-required | `5382f1f950a9139d2c4c52b89bb50e47b4e5d7150c266fffb745716dc195e2e7` |
| PE-EVOL-018 | RF-04 | SF-02 | MAY | Every implementation variation within one published generation | resolved through permitted specification choice | E01,E02,E18 | BD,TD | ambiguous | `64fb1f2a6e5e56c3da55f7bf1c377913e13c459ffb0dfb25380d619a77c1b366` |
| PE-EVOL-019 | RF-04 | SF-02 | MUST | Every compatible successor generation | non-applicable | E01 | NR | not-required | `767a2be580a9b080311ac9c31e5fedb9573d23aba7acf99fc3ee8022889b319b` |
| PE-EVOL-020 | RF-04 | SF-02 | MUST | Every breaking protocol evolution | non-applicable | E01 | NR | not-required | `8e64c8e247f7deac568cd515cd3d85658dc7982a0cc97cd5995146fe7f2b38d6` |
| PE-EVOL-021 | RF-04 | SF-02 | MUST NOT | Every compatibility claim | non-applicable | E01 | NR | not-required | `7dfa3b44b8219e8aafeff641f8c298fb6b215e7a34b5f9dc9b30d6c9d1f47470` |
| PE-EVOL-022 | RF-04 | SF-02 | MUST | Every Protocol Generation deprecation | non-applicable | E01 | NR | not-required | `47035d43cb0fc4c641c0fe0f54fac03d5f797ee602c2244615876593e6fd1f64` |
| PE-EVOL-023 | RF-04 | SF-02 | MUST NOT | Every Protocol Generation deprecation | non-applicable | E01 | NR | not-required | `424ecd771769004f7ad728384f5b9f5dab624919e5564f732335cbda0d2cd1e4` |
| PE-EVOL-024 | RF-04 | SF-02 | MUST | Every published migration | non-applicable | E01 | NR | not-required | `8c8ee097cc9be591975b0ee333dc93a5701ae98bb35c9083372b377c984e1e70` |
| PE-EVOL-025 | RF-04 | SF-02 | MUST | Every mandatory migration obligation | non-applicable | E01 | NR | not-required | `ab2f7ff8195eca4107f721efc1920dd0279e26f28e3c5d2cfc4995002f8baeaa` |
| PE-EVOL-026 | RF-04 | SF-02 | MUST NOT | Every migration | non-applicable | E01 | NR | not-required | `d1674d04a09dfccd45977149e23e1683412c8ae3c0629e67176d656dd3fa9b7e` |
| PE-EVOL-027 | RF-04 | SF-02 | MUST NOT | Every deprecation or migration statement | non-applicable | E01 | NR | not-required | `25526d9980dcaf40feba335f45c91dbd23137236e80d3c1707838e55823ef84c` |
| PE-EVOL-028 | RF-04 | SF-02 | MUST | Every environment supporting multiple published Protocol Generations | non-applicable | E01 | NR | not-required | `72e292ba39f50fb8e187b46f771e1750144342ff6986eb7f08da337b02292ca6` |
| PE-EVOL-029 | RF-04 | SF-02 | MUST NOT | Every coexistence arrangement | non-applicable | E01 | NR | not-required | `95ff2033eaabd7b679b2d3cd19751252b02696bb9fc4abc90cb872a21b73fcf2` |
| PE-EVOL-030 | RF-04 | SF-02 | MUST | Every Protocol Generation retirement | non-applicable | E01 | NR | not-required | `324d9cd3a587645a32f07a32e71f46c776a10549844fbb24b7e67e50f237fc1f` |
| PE-EVOL-031 | RF-04 | SF-02 | MUST NOT | Every Protocol Generation retirement | non-applicable | E01 | NR | not-required | `df1a68693abcf92b5668b2b92d7fb77fb34194c0eec985c154307ba820c1820c` |
| PE-EVOL-032 | RF-04 | SF-02 | MUST | Every lifecycle interpretation | non-applicable | E01 | NR | not-required | `b7792219d175ce27015699646ab10d432239bae5c0062cea9b57c3c20b432264` |
| PE-SPEC-009 | RF-01 | SF-01 | MUST | Every implementation profile | applicable | E01 | BD | bounded | `58443321526592464b8fdbb847251262f3704db7286132cae0f5508c6dcb2063` |
| PE-GEN-017 | RF-03 | SF-02 | MUST | Every Privacy Engine implementation | applicable | E01,E02,E21 | BD,TD | bounded | `3397a56471f645b66fcd4d0f9217357c000b95af8fd49a0b05534a7dc79b51ad` |
| PE-GEN-018 | RF-03 | SF-02 | MUST | Every conformance determination | non-applicable | E01 | NR | not-required | `f996e7e03c3a8871ba552417eb7a0cdc7f225f369f6e578615903a839dfd4fc6` |
| PE-GEN-019 | RF-03 | SF-02 | MUST | Every certification | non-applicable | E01 | NR | not-required | `c1f8316d053970f9d9564a572cedd4306e679a73b9bcdbc67242903786273363` |
| PE-GEN-020 | RF-03 | SF-02 | MUST NOT | Every downstream implementation or assessment artifact | applicable | E01,E02,E21 | BD,TD | bounded | `f941c63650309caaf0838be7e67fc3e724f35dc8d2bb13b9453e0b6053030674` |
| PE-TERM-001 | RF-06 | SF-03 | MUST | Every use of a canonical Protocol Specification term | applicable | E01,E03,E11 | BD,TD,RO | bounded | `c0588f32b0973d42bbb8320a7eaebd2ed3610a2ff3592f77763acab51b75ef5c` |
| PE-TERM-002 | RF-06 | SF-03 | MUST | Every downstream section, profile, implementation, application adapter, assessment, and supporting artifact | applicable | E01,E03,E11 | BD,TD,RO | bounded | `b961be0d02654cc996ec0ca523ce17295d6bf9fa7196a9a52dc1ab1e2a74918c` |
| PE-TERM-003 | RF-06 | SF-03 | MUST | Every term that may denote either a protocol type or an occurrence | applicable | E01,E03,E11 | BD,TD,RO | bounded | `ecb9852e4875d25c1515d959e55e67f1740f7883bc9b001ce86fd73b00fbd65c` |
| PE-TERM-004 | RF-06 | SF-03 | MUST | Every specification definition involving a semantic subject, identifier, or representation | applicable | E01,E03,E11 | BD,TD,RO | bounded | `da65720c03fe9f7e63a3b9e090a218c9c6fe442b2cd647f28ffa920e7860555b` |
| PE-TERM-005 | RF-06 | SF-03 | MUST NOT | Every alias, abbreviation, implementation name, application label, and editorial synonym | applicable | E01,E03,E11 | BD,TD,RO | bounded | `65fbbd14a48386551b304143219dd26a68513dc22e653aa769db29450214be43` |
| PE-TERM-006 | RF-06 | SF-03 | MUST NOT | Every terminology decision and editorial reorganization | applicable | E01,E03,E11 | BD,TD,RO | bounded | `4e8c44366c74c5b5d0df13f95d276b4dae89a4d5dba6ed974f9c0b1541d28814` |
| PE-TERM-007 | RF-06 | SF-03 | MUST | Every permitted local alias for a canonical protocol term | applicable | E01,E03,E11 | BD,TD,RO | bounded | `bee042939106240442ef355829f34b994b1c1e49e09be22c620d2781a8be8d7b` |
| PE-SUBJ-001 | RF-07 | SF-03 | MUST | Every established identified protocol subject | applicable | E01,E03,E07,E08,E11,E20 | BD,TD,RO | ambiguous | `db5dfcdcc9e919dd54e61c2b28665520d1b863de80b473392e41f2e868811630` |
| PE-SUBJ-002 | RF-07 | SF-03 | MUST | Every Protocol Action, Protocol Action Evaluation, Protocol Action Determination, and Protocol State Transition | applicable | E01,E03,E07,E08,E11,E20 | BD,TD,RO | ambiguous | `bef9445371062635eb2353db40087d0c76de5d6ae51a49d120d9b85352e8bdbc` |
| PE-SUBJ-003 | RF-07 | SF-03 | MUST | Every Protocol Action Evaluation and its Protocol Action Determination | applicable | E01,E03,E07,E08,E11,E20 | BD,TD,RO | ambiguous | `536a3de883fcfc4a0126e5addbcd51ac027daec7c3784c54c21443487e59e1a0` |
| PE-SUBJ-004 | RF-07 | SF-03 | MUST | Every Protocol Operation and associated Protocol Action | applicable | E01,E03,E07,E08,E11,E20 | BD,TD,RO | ambiguous | `0183ca8ff30767db8163e98d8a4abf072d11b474f396f51c35a6d2fe93a1eca6` |
| PE-SUBJ-005 | RF-07 | SF-03 | MUST | Every Protocol Transition and governed Protocol State Transition | applicable | E01,E03,E07,E08,E11,E20 | BD,TD,RO | ambiguous | `d3ac3c09b9da393b8aeb46aa5995d398f7aef9fc0c4756de2022bda5feb1e934` |
| PE-SUBJ-006 | RF-07 | SF-03 | MUST | Every relationship between identified protocol subjects | applicable | E01,E03,E07,E08,E11,E20 | BD,TD,RO | ambiguous | `d13f8beed523b872c84dbacb2410fda27acec08c57cb12e019dd591b97ed6330` |
| PE-SUBJ-007 | RF-07 | SF-03 | MUST | Every protocol subject referenced through an implementation, application, runtime mechanism, or application interpretation | applicable | E01,E03,E07,E08,E11,E20 | BD,TD,RO | ambiguous | `90ff71b2eff17a812d40e371c0683b31b45881bc61848e34e29ba03f5a06a88b` |
| PE-SUBJ-008 | RF-07 | SF-03 | MUST | Every downstream representation or reference to an established protocol subject | applicable | E01,E03,E07,E08,E11,E20 | BD,TD,RO | ambiguous | `088c3e4331cc99a20c4883ed8a24e4f845cfec25890f07ceb3b40711ebd9693d` |
| PE-SUBJ-009 | RF-07 | SF-03 | MUST NOT | Every relationship, composition, representation, and implementation convenience involving distinct subjects | applicable | E01,E03,E07,E08,E11,E20 | BD,TD,RO | ambiguous | `953c0b76c2ae4e664966f7c9a61394c6945d8ca44c21ec3d8baa617e620568ec` |
| PE-SUBJ-010 | RF-07 | SF-03 | MUST NOT | Every proposed extension to the established protocol-subject inventory | applicable | E01,E03,E07,E08,E11,E20 | BD,TD,RO | ambiguous | `e4b9afaef3b88a041c82e482363f93a367c1451b874965dbc5d0d3c5fd4da641` |
| PE-ID-001 | RF-08 | SF-03 | MUST | Every protocol identifier | applicable | E03,E04,E07,E08,E11 | BD,TD,RO | bounded | `e716145b819399fe5443757d2109e22d39ad82759c73e5b1f79be002100c8452` |
| PE-ID-002 | RF-08 | SF-03 | MUST | Every identified protocol subject and its identifier | applicable | E03,E04,E07,E08,E11 | BD,TD,RO | bounded | `3f20f807602feb8778cab0545ecfb7db8ce1be3bf1760544645c7a1b1c5bc9b5` |
| PE-ID-003 | RF-08 | SF-03 | MUST | Every protocol subject and its syntactic, serialized, stored, transmitted, or displayed representation | applicable | E03,E04,E07,E08,E11 | BD,TD,RO | bounded | `9fe41651242aa637ba8f0c22ae7544182f8881c1698fb6d95836f96a43b3a0c4` |
| PE-ID-004 | RF-08 | SF-03 | MUST NOT | Every relationship between separately identified protocol subjects | applicable | E03,E04,E07,E08,E11 | BD,TD,RO | bounded | `d8593edb735fd23446bec2789f0c3e24051d451cf5ed9caf927d2bb2a002df80` |
| PE-ID-005 | RF-08 | SF-03 | MUST NOT | Every identifier of a Protocol Action occurrence | applicable | E03,E04,E07,E08,E11 | BD,TD,RO | bounded | `e15237d65ebd17e21bc3c70d3f72e2bdaae26bfaa1928713968bd27fea4fdbb1` |
| PE-ID-006 | RF-08 | SF-03 | MUST NOT | Every public Evaluation, Determination, and Protocol State Transition identifier | applicable | E03,E04,E07,E08,E11 | BD,TD,RO | bounded | `688b70cc90a5d0ba38f7d1f5439c64bacd25d74105b7a7bc786adeeeae548a3b` |
| PE-ID-007 | RF-08 | SF-03 | MUST NOT | Every implementation, transaction, retry, transport-attempt, storage, or diagnostic identifier | applicable | E03,E04,E07,E08,E11 | BD,TD,RO | bounded | `a5d857be4666a0f10de7ea78e5f6cfdf721424405fd1d87b258fca97f28ea84a` |
| PE-ID-008 | RF-08 | SF-03 | MUST NOT | Every protocol identifier outside its declared subject and context | applicable | E03,E04,E07,E08,E11 | BD,TD,RO | bounded | `1b517ccf2bf751cd8badc56707a76bf5925d0fd2c60e493a9c38978cba652137` |
| PE-ID-009 | RF-08 | SF-03 | MUST | Every permitted change of protocol-subject representation | applicable | E03,E04,E07,E08,E11 | BD,TD,RO | bounded | `3d29ce940711faab2528430d345152fc4ab116d8e53ec30a2aaa64c55573ae37` |
| PE-ACTSEP-001 | RF-09 | SF-04 | MUST | Every Privacy Engine realization of a public protocol action | applicable | E03,E04,E05,E06,E07,E09,E10 | BD,TD,RG,DB,RO | bounded | `e788781214be44287d966a496db5b943e1a507fd8c878b3da12ea4196644365b` |
| PE-ACTSEP-002 | RF-09 | SF-04 | MUST | Every publicly visible Protocol Action | applicable | E03,E04,E05,E06,E07,E09,E10 | BD,TD,RG,DB,RO | bounded | `baaebdb224f17e55aee0aaa5dd12883034943b659fe71d2cbedf65d13376695b` |
| PE-ACTSEP-003 | RF-09 | SF-04 | MUST | Every relationship between a Private Actor and a public Protocol Action | applicable | E03,E04,E05,E06,E07,E09,E10 | BD,TD,RG,DB,RO | bounded | `06b85d3f1b3273aaa61075a0c8470c9912b57b420b5a8dc1e4e56169dbd67f60` |
| PE-ACTSEP-004 | RF-09 | SF-04 | MUST | Every publicly identified protocol subject | applicable | E03,E04,E05,E06,E07,E09,E10 | BD,TD,RG,DB,RO | bounded | `56295f74f503913f9ba189e987afc95ccb683bb3b6c1dbfa1fe652c40d828367` |
| PE-ACTSEP-005 | RF-09 | SF-04 | MUST | Every public protocol consequence | applicable | E03,E04,E05,E06,E07,E09,E10 | BD,TD,RG,DB,RO | bounded | `74323762cdffd36c5cde1140a92c809e73dc8d9ec6835dea3e052f9d7f4ad3fd` |
| PE-ACTSEP-006 | RF-09 | SF-04 | MUST NOT | Every Protocol Action validity, authorization, uniqueness, and public-consequence rule | applicable | E03,E04,E05,E06,E07,E09,E10 | BD,TD,RG,DB,RO | bounded | `3b2baf8f05e9e6e8a3250a7f3ac98bd3ad366cf2abca358a62a86f6d38ffdd7c` |
| PE-ACTSEP-007 | RF-09 | SF-04 | MUST NOT | Every public Privacy Engine protocol surface | applicable | E03,E04,E05,E06,E07,E09,E10 | BD,TD,RG,DB,RO | bounded | `5f4bb958cf1942a3f88a1591977b855c9e9c0fe7216f8877ea6e51007d71720b` |
| PE-PRIV-001 | RF-10 | SF-04 | MUST | Every Privacy Engine protocol action governed by anonymous-participation semantics | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `d009bf63e0f3f0a198ad957a09412a20aa32860aec2e600d89dc8ef64f75e97a` |
| PE-PRIV-002 | RF-10 | SF-04 | MUST | Every public value and public protocol subject exposed by an anonymous action | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `06bf7bcaf025f7555797da22b3c4d7995dcc5ca4f56b20750455baf7cf5985bf` |
| PE-PRIV-003 | RF-10 | SF-04 | MUST | Every pair or collection of anonymous Protocol Actions in distinct action contexts | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `7e0aa176f9af2d425f28c4ec56dcdc3044a2621acf425d5aafb8d9f33338d038` |
| PE-PRIV-004 | RF-10 | SF-04 | MUST NOT | Every wallet identifier, wallet signature, wallet-derived value, and wallet relationship | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `047076b2459a8e6702c95a7aee2e1701b32f78aa4558f3c70ee147c200018e3a` |
| PE-PRIV-005 | RF-10 | SF-04 | MUST NOT | Every application identifier, account, profile, metadata value, and application-defined relationship | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `2ba054bce384ae9f276b2f8114afef596c61597fcb264e6fe2ac16a15604cd08` |
| PE-PRIV-006 | RF-10 | SF-04 | MUST NOT | Every implementation identifier and implementation-specific internal value | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `1c902d7f402b4839d5b5785b4efe6862c270ccbae85a3d4c4e84d340a806c88a` |
| PE-PRIV-007 | RF-10 | SF-04 | MUST NOT | Every deployment identifier, topology coordinate, service identity, and infrastructure relationship | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `d93b719b012522e358635708da0635bdfd318a91f54b0bf87c21d370c38904f8` |
| PE-PRIV-008 | RF-10 | SF-04 | MUST NOT | Every transport identifier, connection attribute, delivery path, retry path, and request context | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `a108b5a1251b7ff90cc2a764829fe6b75f71c238b52e36219613cdd17eb7a170` |
| PE-PRIV-009 | RF-10 | SF-04 | MUST NOT | Every enrollment right, admission object, funding relationship, sponsor relationship, and associated provenance | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `195e1774fb1097c5b3b668a384d8456211b292db75700410286d861e22a09271` |
| PE-PRIV-010 | RF-10 | SF-04 | MUST | Every action-local public value | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `dd0487fb9edc9bcb77c3f84adc8f6bb20dfc6c72490bb787dba0cf1a133a6b2c` |
| PE-PRIV-011 | RF-10 | SF-04 | MUST | Every privacy-sensitive failure path | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `cb1788553b6fc51ad928b2c4098beb8daa7cff1e31f23e48406dd7f5f94c4ab4` |
| PE-PRIV-012 | RF-10 | SF-04 | MUST NOT | Every implementation, profile, application, conformance claim, diagnostic, and specification interpretation | applicable | E03,E04,E05,E06,E07,E09,E10,E15 | BD,TD,RG,DB,RO | bounded | `5740643ac96288d439d8f0878097c8457abb9d2a755d7e5442e72c1b7465d8ea` |
| PE-COMP-001 | RF-11 | SF-04 | MUST | Every composition of publicly exposed Privacy Engine values, subjects, consequences, and records | applicable | E03,E04,E07,E09,E10,E11,E12,E15 | BD,TD,RG,DB,RO | bounded | `e515d7aa9af6c5d5946f17adc52282e71d7a3b38f0b48b00578009b6578faf3b` |
| PE-COMP-002 | RF-11 | SF-04 | MUST NOT | Every implementation-controlled identifier, timing label, diagnostic, serialization field, log field, storage key, route, and public response | applicable | E03,E04,E07,E09,E10,E11,E12,E15 | BD,TD,RG,DB,RO | bounded | `21e6568ee569d1134fe48a3ce20624c0bd132da4dc25099af506b6499fe06237` |
| PE-COMP-003 | RF-11 | SF-04 | MUST | Every privacy-sensitive field name, variable name, route name, log label, diagnostic, comment, example, test, serialization field, and specification term | applicable | E03,E04,E07,E09,E10,E11,E12,E15 | BD,TD,RG,DB,RO | bounded | `ed4c8f96a700bf07673237b7e5ba33254b3a56c4b763dbdd00e4278293dc99a6` |
| PE-COMP-004 | RF-11 | SF-04 | MUST | Every public observability surface | applicable | E03,E04,E07,E09,E10,E11,E12,E15 | BD,TD,RG,DB,RO | bounded | `587e6ca05588e2c8ea59c9b4a1e26738d5e93364ebe8b10ede4808cbed6a54de` |
| PE-COMP-005 | RF-11 | SF-04 | MUST | Every diagnostic and failure-reporting surface | applicable | E03,E04,E07,E09,E10,E11,E12,E15 | BD,TD,RG,DB,RO | bounded | `f004f7958d685b526194f345718a5224ea1be2c0561663dd770bbb2c1646c8d5` |
| PE-COMP-006 | RF-11 | SF-04 | MUST NOT | Every request history, telemetry record, path-acquisition record, submission record, and operational history | applicable | E03,E04,E07,E09,E10,E11,E12,E15 | BD,TD,RG,DB,RO | bounded | `3903d42cbd3825c12d1cac37eeafdd2ad793dc9986c24f83a819b1cf1dd90edc` |
| PE-COMP-007 | RF-11 | SF-04 | MUST NOT | Every public protocol response, log, status surface, and diagnostic | applicable | E03,E04,E07,E09,E10,E11,E12,E15 | BD,TD,RG,DB,RO | bounded | `0eb19c8b439ae9e2b6ac1a5f33fbf6331a75d8e10d029fa90e470aa18e2f5e20` |
| PE-COMP-008 | RF-11 | SF-04 | MUST | Every information crossing between Privacy Engine layers | applicable | E03,E04,E07,E09,E10,E11,E12,E15 | BD,TD,RG,DB,RO | bounded | `fcb55010cf07b8a425523553fb7cd3d43ea567d0ce483d5b27c84729a8b32793` |
| PE-COMP-009 | RF-11 | SF-04 | MUST | Every implementation composition exposing multiple individually non-identifying surfaces | applicable | E03,E04,E07,E09,E10,E11,E12,E15 | BD,TD,RG,DB,RO | bounded | `f63fa6a3c34ec1d54d7eff9058f179f9a1bf4f2f4ab83669e4899123eed80f78` |
| PE-COMP-010 | RF-11 | SF-04 | MUST NOT | Every informative example, supporting cross-reference, test artifact, assessment record, and documentation surface | applicable | E03,E04,E07,E09,E10,E11,E12,E15 | BD,TD,RG,DB,RO | bounded | `e3958ec091de5d09df07ea1e4abfa91d1b652a516e14c4a8aa34a995d697007e` |
| PE-MEM-001 | RF-15 | SF-04 | MUST | Every anonymous membership identity in the current published protocol generation | applicable | E04,E05,E10,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `3736a17b5c2826b6d3b6c6d04590115c87783ee5bdfd200205da76eb53264484` |
| PE-MEM-002 | RF-15 | SF-04 | MUST | Every claim of anonymous membership continuity | applicable | E04,E05,E10,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `1f11a6dfe6d638dff9fcd6eb5744601e9891bbc1be04cdc7ddbd2607d1c912d0` |
| PE-MEM-003 | RF-15 | SF-04 | MUST | Every replacement of an active `memberSecret` with a different secret | applicable | E04,E05,E10,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `0078087bfc59df954eab6800320620c4b8e7c96f108fdace2f674f07329c4c37` |
| PE-MEM-004 | RF-15 | SF-04 | MUST NOT | Every wallet, backend, application, deployment, transport, and heuristic recovery mechanism | applicable | E04,E05,E10,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `1e0e23f9652cc772a17a61c8549ed72e89fe7cd4c76e50901f736caee3416716` |
| PE-MEM-005 | RF-15 | SF-04 | MUST | Every membership leaf | applicable | E04,E05,E10,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `87c951fe044bf8f43a6c02bd71c93a08f426cb5f35f16bab06685453b6495e16` |
| PE-MEM-006 | RF-15 | SF-04 | MUST | Every membership enrollment or activation | applicable | E04,E05,E10,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `c5d35f72f7624e2e8180988ddb6cc0d1f72c2878caa4d90c9ea1c0ae9ef21c1c` |
| PE-MEM-007 | RF-15 | SF-04 | MUST NOT | Every enrollment right, admission object, funding wallet, sponsor relationship, and accounting state | applicable | E04,E05,E10,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `b954a4f0fb72e25a8a822c499059c2d0937d1b949c90b62801c25b1cffc963c9` |
| PE-MEM-008 | RF-15 | SF-04 | MUST NOT | Every public enrollment, membership-status, readiness, and application surface | applicable | E04,E05,E10,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `e525fac96fdce6f394b0440804437e9ca84a07d3de0dfa0da253d3e8bdbd87bc` |
| PE-UNIQ-001 | RF-19 | SF-04 | MUST | Every anonymous action type requiring one action per member per action context | applicable | E04,E05,E06,E07,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `e92a5cc28dd6af17cd50afd86c5afdd83045782774096fd40852f57137aec949` |
| PE-UNIQ-002 | RF-19 | SF-04 | MUST | Every nullifier in the current published protocol generation | applicable | E04,E05,E06,E07,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `2af6981c81ae65c27d7efe8c96578062ac0fafca86ba363ac07785bd20fe5340` |
| PE-UNIQ-003 | RF-19 | SF-04 | MUST | Every action-layer duplicate-prevention decision in the current published protocol generation | applicable | E04,E05,E06,E07,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `d61bae8ed27c6339de9a49c03cc0d7ef13528c70ad3559b416f92267cd959fd3` |
| PE-UNIQ-004 | RF-19 | SF-04 | MUST NOT | Every public nullifier and nullifier-status record | applicable | E04,E05,E06,E07,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `97d082c8fc5e7313ca27fbaf34f2b7657e05c6d62929569dd09817efe96ff9cd` |
| PE-UNIQ-005 | RF-19 | SF-04 | MUST NOT | Every nullifier outside its declared action context | applicable | E04,E05,E06,E07,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `dbf47322c70c2ce66bc8e26d3c3efbb76f5852ac655642c0b0d78d48eedc40fd` |
| PE-UNIQ-006 | RF-19 | SF-04 | MUST NOT | Every wallet identifier, membership leaf, enrollment identifier, admission object, and application account | applicable | E04,E05,E06,E07,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `3ed53b7852eedcb3877235375c7ed88827f32983864a85977c6306f8b8ca2fbe` |
| PE-UNIQ-007 | RF-19 | SF-04 | MUST NOT | Every duplicate-status response, log, diagnostic, event, and read model | applicable | E04,E05,E06,E07,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `cf5c52ee8395753f542b2aa3684dedd0f9fca09f17e9a6f9bb745c8cfcded13e` |
| PE-UNIQ-008 | RF-19 | SF-04 | MUST NOT | Every interpretation of nullifier-enforced uniqueness | applicable | E04,E05,E06,E07,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `072a5032b26e43d4d7c9493e95f9ad19a2e5147d4cde3985cb101d4176f21fd2` |
| PE-IFACE-001 | RF-12 | SF-05 | MUST | Every Privacy Engine Interface Contract | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `ae76fee54c89bcb507f3649a1cc493a3ba040fd1f977aad5d1d95f86bade9747` |
| PE-IFACE-002 | RF-12 | SF-05 | MUST | Every Privacy Engine Interface Contract | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `f9822ac4ce8b6ef52dc7c3e43e06d5e8682bec4a627015b01ca7adce59927d97` |
| PE-IFACE-003 | RF-12 | SF-05 | MUST | Every Privacy Engine Interface Contract | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `36a49a2b9236471c1253ca2e6b45b61973f833fd740aa8873718c0c3960293ae` |
| PE-IFACE-004 | RF-12 | SF-05 | MUST | Every Interface Contract and every concrete realization of it | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `7219c3392d6e22fbef6c706e11c4d3b4d6e8fc3cdc989bc5cf976429d7ca8c91` |
| PE-IFACE-005 | RF-12 | SF-05 | MUST | Every Concrete Interface Specification | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `e0dba9ff6b715f26ba38c26d86ed570eb9b157af4066b3ca3316d1b139071bff` |
| PE-IFACE-006 | RF-12 | SF-05 | MUST | Every Concrete Interface Specification | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `abfb0263ad994071d4042ab7b7b092162c54731f057aa9506dc13ba22acae79e` |
| PE-IFACE-007 | RF-12 | SF-05 | MUST | Every Concrete Interface Specification | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `161414424e48204cb88446b79a54e6f2994b27453049a4cfae766307054794f7` |
| PE-IFACE-008 | RF-12 | SF-05 | MUST | Every Concrete Interface Specification and its governing Interface Contract | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `24bf84dddf5a274688ce4d12423155121f737e3999552521c62ee8bec97b0e97` |
| PE-IFACE-009 | RF-12 | SF-05 | MAY | Every Interface Contract permitting multiple concrete realizations | resolved through permitted specification choice | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `2f1895a02fc6f7f8b776b32b1e60d1ef7e4faea1d70da7a0e4838c43bee2d1c3` |
| PE-IFACE-010 | RF-12 | SF-05 | MUST | Every representation-only interface change | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `70f89ce0827514ba0fb20c0048126283b805962280b9f8a505e319077a5f34d4` |
| PE-IFACE-011 | RF-12 | SF-05 | MUST | Every change to published Interface Contract meaning | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `35166f75517b9e0819ee89585cbd0e1f8ce47868f959e9c3a7c53fef22be208d` |
| PE-IFACE-012 | RF-12 | SF-05 | MUST NOT | Every Interface Contract and Concrete Interface Specification | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `5c2dbc4b8a0fdcb164896754235d305dca35a2dfeaba2ada433b673e9b60b5c3` |
| PE-IFACE-013 | RF-12 | SF-05 | MUST NOT | Every Interface Contract and Concrete Interface Specification | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `c871735f1170f933baf2b401d754d6e6295a018e40cf47dbb4821eaf5c24bc69` |
| PE-IFACE-014 | RF-12 | SF-05 | MUST | Every public Interface Contract and Concrete Interface Specification | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `1dce738b71ee29d52984a13bd40e7765cde79f03709c3c41f651be4d9a9597a1` |
| PE-SURF-001 | RF-13 | SF-05 | MUST | Every Privacy Engine Protocol Surface | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `ed1a69b15b975ec35199766e279d31ba4ca1d7c354ccb7dc2d3a6350699c259e` |
| PE-SURF-002 | RF-13 | SF-05 | MUST | Every Protocol Surface | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `98325366401c748acd93487a518d423c27c290c9b7b7bc585cd078b1dfbe7d38` |
| PE-SURF-003 | RF-13 | SF-05 | MUST | Every implementation realizing a Protocol Surface | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `5ad6ae7ea906c2fc39bb50bfe93bfb1c22efd40c03c318e5b652903a2281536e` |
| PE-SURF-004 | RF-13 | SF-05 | MUST NOT | Every implementation detail behind a Protocol Surface | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `9dc39ee8dd46ff1b22ccec242a574857f8ed7b9f7b0638676fd4353bee7df41b` |
| PE-SURF-005 | RF-13 | SF-05 | MUST | Every Privacy Engine Protocol Operation | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `a50ad413b75ec94b0064d3e83f720956211692438a3e870cfe943184f60a753e` |
| PE-SURF-006 | RF-13 | SF-05 | MUST | Every Protocol Operation | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `ffb277e580a8825138309dc8a90818ba8b94fe2f2ec39e0167859875f23d6e57` |
| PE-SURF-007 | RF-13 | SF-05 | MUST | Every Protocol Operation and associated Protocol Action | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `b3e6e128d94ffba0dfd4d80a2f312a7d0b01520da25f4244cd695baeb9ab33e8` |
| PE-SURF-008 | RF-13 | SF-05 | MUST | Every offered Protocol Operation | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `efacce49d75cb96ed6c2564dc0a7e5839069a757dc271e5247ac1f211aeed492` |
| PE-SURF-009 | RF-13 | SF-05 | MUST | Every implementation realizing a Protocol Operation | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `c3f4927188c4e65cc2b9188361321ab75c2621bce374d4bf51a75bb19c465c50` |
| PE-SURF-018 | RF-13 | SF-05 | MUST NOT | Every execution or implementation variation realizing a Protocol Operation | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `c6024755c45a47c7ad68d3fe23e24c1a2d685c163b444422855769b5ced45ce3` |
| PE-SURF-010 | RF-13 | SF-05 | MUST | Every Published Result | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `48bcea85ef688c728b8661f1929c7590bb6eddd26ba5de402c8bb709e597fe2f` |
| PE-SURF-011 | RF-13 | SF-05 | MUST | Every Published Result | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `06a605ee229af5da38471b584bd3bc427baf017d830083550172df8bcc3127e0` |
| PE-SURF-012 | RF-13 | SF-05 | MUST | Every Published Result and concrete representation of it | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `8ca005be0b9fd823ef5d48785d76f2f5bd0c6c27904b9841e589e231c8857bad` |
| PE-SURF-013 | RF-13 | SF-05 | MUST | Every concrete realization or translation of a Published Result | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `b598983e09ac6417b8b63555c7c0e5790f67e0ef966ead902da6ca9756e4257c` |
| PE-SURF-014 | RF-13 | SF-05 | MUST NOT | Every Published Result | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `82f367e4132b478d71fc63daf7259e05918e2193bc606fdbfb11d3c9a6ed4937` |
| PE-SURF-015 | RF-13 | SF-05 | MUST NOT | Every Published Result | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `ac36ee3dea19b36f71850ea7c385e83148d0d13d3dc5b7dce5e29505191bdc95` |
| PE-SURF-016 | RF-13 | SF-05 | MUST NOT | Every application interpretation or representation of a Protocol Surface, Protocol Operation, or Published Result | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `607ced3bcf3b79408309340622dd168fdbc90a6262dfd07e84eacdc68ed66efd` |
| PE-SURF-017 | RF-13 | SF-05 | MUST | Every public Protocol Surface, Protocol Operation representation, and Published Result | applicable | E01,E09,E10,E11,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `f0bdaf74ed9ecc4b4d3ad660b572b429dfccdceba9e1669c7d6892530ae606e4` |
| PE-PROOF-001 | RF-16 | SF-06 | MUST | Every proof required by a Privacy Engine Protocol Action | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `7ecd50a3e50ba6e71fabffeb23560a5f311e08a6dbbb79230c500d357b0393cf` |
| PE-PROOF-002 | RF-16 | SF-06 | MUST | Every proof type in a published protocol generation | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `76bac08f6459b62dcf960cb496e98562650965861a7f584578925d98990f90ea` |
| PE-PROOF-003 | RF-16 | SF-06 | MUST | Every current-generation anonymous-action proof | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `1e90facd41696f48e61b431437b8791bedd5c06f6f22e1ad46c0fff3ad8d6408` |
| PE-PROOF-004 | RF-16 | SF-06 | MUST | Every proof relation and proof-construction boundary | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `07c8450bc3715a08748c7d5dac51c674bc795dfaec83cd4fb1dd548ca0a823ef` |
| PE-PROOF-005 | RF-16 | SF-06 | MUST | Every current-generation anonymous-action public-input set | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `14902ea8fc0a732d0ddddd534e681c2ca7938d7ba6b9e9504ecf6f83887d4ac8` |
| PE-PROOF-006 | RF-16 | SF-06 | MUST | Every current-generation declared public-input interpretation | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `ae1be581c8237f415e051ab398b57718f0790ab48a8e4f3f78478415a97d5c39` |
| PE-PROOF-007 | RF-16 | SF-06 | MUST | Every proof and declared public-input set presented together | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `38e92b9d037b891cf136ba1ebd7a90eca477a4f184cecefdda9743f07ee25bab` |
| PE-PROOF-008 | RF-16 | SF-06 | MUST | Every proof-construction process | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `749874f905edb8920601d1fbd9ad2a505aea244626643c639f374af91a820f37` |
| PE-PROOF-009 | RF-16 | SF-06 | MUST | Every proof realization for the current published generation | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `740d274511e90e78a07b8843980e7dd160ccefc00d70977538dc3f80d5e72fad` |
| PE-PROOF-010 | RF-16 | SF-06 | MUST | Every published proof artifact set | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | ambiguous | `80fe3ba8d6cf2d7d5800b67a8e230854895e6dea9affe0c9158f26fdcfe1c989` |
| PE-PROOF-011 | RF-16 | SF-06 | MUST | Every permitted proof or public-input representation | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `03548219bd452b95dc9e5f8cec7eca4c230efcc3e63cbdd3448b4d4a1bdd0404` |
| PE-PROOF-012 | RF-16 | SF-06 | MUST | Every change to a proof system, proof relation, public-input schema, public-input ordering, verifier encoding, or artifact-integrity rule | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `6b19e3ce7fdebc5c04742e75709498e4d32fc1d82f7213931005509b16db9b72` |
| PE-PROOF-013 | RF-16 | SF-06 | MUST NOT | Every proof and proof representation | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `10572c7c42e47853fb312e1395273ece2cccd4516c96a8654edf95cbf6bb4d89` |
| PE-PROOF-014 | RF-16 | SF-06 | MUST NOT | Every declared public input and public-input composition | applicable | E04,E05,E13,E14,E15,E19 | BD,TD,RG,DB,RO | bounded | `6a1248ceda8991d31fa90ad6c89187e842f2a2331ca2ab8b71c3f72cbf9d5a83` |
| PE-VERIFY-001 | RF-17 | SF-06 | MUST | Every required proof verification | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `398bb0389f01b8d1546cb783a544671f1f6f81d21f8621477e20fbb669d85fcf` |
| PE-VERIFY-002 | RF-17 | SF-06 | MUST | Every proof-verification occurrence | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `dd355488a6e4a6a87a607a3fe375c09e4dacd9ab9011e1fc73660690bd10fbfd` |
| PE-VERIFY-003 | RF-17 | SF-06 | MUST | Every correct proof-verification realization | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `79278f2d165dddd6d0d414c00c2768d7eb8c982367148dda90d7cded2d19229c` |
| PE-VERIFY-004 | RF-17 | SF-06 | MUST | Every completed proof-verification occurrence | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `2ce948f78fac89575097a9e0be39686ac9478cc5c5ca2f50fb36f7e165224c3c` |
| PE-VERIFY-005 | RF-17 | SF-06 | MUST | Every proof-valid classification | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `514164bb371cadf32dae9c834bd234e113ff41879c73f357a7c527f2f604634f` |
| PE-VERIFY-006 | RF-17 | SF-06 | MUST | Every proof-invalid classification required for a Protocol Action | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `a06d9fd43448b294199bb99ef672e5e3c14f75c381af3ed9cb699dda00edf23d` |
| PE-VERIFY-007 | RF-17 | SF-06 | MUST | Every inability to complete required proof verification | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `fb99a7b809527fa1a1224e80f9ed48bbe90b0bf279724533003694b45e60f15d` |
| PE-VERIFY-008 | RF-17 | SF-06 | MUST | Every proof-valid verification result used in Protocol Action Evaluation | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `3c31f6adc0ea46685db815d2dd30ad4ab00f6c5d8fece18a08641ccc408bb6e7` |
| PE-VERIFY-009 | RF-17 | SF-06 | MUST NOT | Every proof-valid verification result | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `823033a6b54306c5c9f7f26a33b6f611c9d5706c2e0172e5dec52f328b7439d4` |
| PE-VERIFY-010 | RF-17 | SF-06 | MUST NOT | Every proof-verification occurrence and result | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `ae76ee4c8377f94cdddbd4c61446dd28f6623c794b463f07893d0463800e05b9` |
| PE-VERIFY-011 | RF-17 | SF-06 | MUST NOT | Every proof-verification implementation | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `cd6ce73b287277ad2acb397fc5912386d10b0867c1c903f1119c3d99b52daf05` |
| PE-VERIFY-012 | RF-17 | SF-06 | MUST NOT | Every proof-verification component and result | applicable | E05,E06,E13,E14,E15 | BD,TD,RG,DB,RO | bounded | `8dc44399327f86ccd8b6927f5b980b8dfcb2e7dae17118d42e043e483942c33f` |
| PE-VALID-001 | RF-18 | SF-06 | MUST | Every proof-verification result used during Protocol Action Evaluation | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `7d82dc07bd79d4def802486bc4a9ddf17818d624c6a4151cef3037255e9d65a6` |
| PE-VALID-002 | RF-18 | SF-06 | MUST | Every proof-verification result contributing to complete Evaluation | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `54eb03910727d11bffbcf962b3103ad5833fbba90751f78d452ca459a38365fa` |
| PE-VALID-003 | RF-18 | SF-06 | MUST | Every Protocol Action validity determination basis | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `1ceb5a51e6f98b3cf3902b5063582f415cb747ea8c9ae197f986e193e238a642` |
| PE-VALID-004 | RF-18 | SF-06 | MUST NOT | Every successful proof-verification result | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `7388241381908c563e95d3c6af38ec57bd7c9f6f475d6dd7f40c70aee1073221` |
| PE-VALID-005 | RF-18 | SF-06 | MUST | Every Protocol Action whose applicable rule set includes non-proof validity conditions | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `3641fba2e7a21fac5990ba5ad83b9f6a735891b1af60cc8c602f7dbfaf964216` |
| PE-VALID-006 | RF-18 | SF-06 | MUST | Every non-proof protocol-validity condition | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `ffa5be8d7f931d358ddf6c00e062d10ad153bb75e9686fe6c9b30566288de155` |
| PE-VALID-007 | RF-18 | SF-06 | MUST | Every current-generation Protocol Action Evaluation basis | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `9faa7f0bd22629669ac6360f18edccd49757f5e63307dca13873e4354ea7ad8d` |
| PE-VALID-008 | RF-18 | SF-06 | MUST | Every required proof-invalid verification result | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `eb7c653e8f9352e9810df7534d4fc3b42458a0f0dcc84ec76192c57cf90a74c5` |
| PE-VALID-009 | RF-18 | SF-06 | MUST | Every interpretation of protocol validity | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `1dc84bc2c6797fbd43663a4eb6e47ddc0146e45a2dda7df9a5e68fcbebf50453` |
| PE-VALID-010 | RF-18 | SF-06 | MUST NOT | Every proof-valid or protocol-valid classification | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `99f8a72909867dc4f795ee44a9a03acf70b972c4580710453316f5415cb14e91` |
| PE-VALID-011 | RF-18 | SF-06 | MUST NOT | Every protocol-valid Protocol Action and interpretation of it | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `002133d7aad0ace021cd9a793c907d7a8d814c194875f93e7be5e34f94d4be23` |
| PE-VALID-012 | RF-18 | SF-06 | MUST | Every evidence, validity, failure, and diagnostic surface | applicable | E05,E06,E07,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `da1fc4ae5e8b9c469f2a9bb090299baf688cfba8d7c3f512d1369c247f503259` |
| PE-ACTION-001 | RF-20 | SF-07 | MUST | Every Privacy Engine Protocol Action | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `463004346231b57549d4e4e1afe320117c07aecc502784bdc1c0fa43da308e9f` |
| PE-ACTION-002 | RF-20 | SF-07 | MUST | Every Protocol Action occurrence | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `3c39a5437a128a309481077f8269c6f3bbab15f574be3f3ee220b009af58ac4d` |
| PE-ACTION-003 | RF-20 | SF-07 | MUST | Every Protocol Action | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `86345e5cb0d092c59c2004291c26c497264b190ae7cfdcf9ab4a9a29c5926415` |
| PE-ACTION-004 | RF-20 | SF-07 | MUST | Every Protocol Action occurrence | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `23e1d3e60077600c0dfb2b0dcf6635df02288233228643b7908f6a9a7eacf2ef` |
| PE-ACTION-005 | RF-20 | SF-07 | MUST | Every Protocol Operation, action type, and Protocol Action occurrence | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `279a450caad2bbc7193f5432dc2bce597acd6b46ccfaa14100cfdac21aeea3b0` |
| PE-ACTION-006 | RF-20 | SF-07 | MUST | Every effort to construct, present, submit, or obtain evaluation of a candidate Protocol Action | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `62a35dad1164f717c8cf3075563a945cdf55c85842323828ea42dc55fccbafde` |
| PE-ACTION-007 | RF-20 | SF-07 | MUST | Every candidate admitted to authoritative Protocol Action Evaluation | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `51c54fd25797c77d27a64631d0c8d36fdd25fc5b2d9d551ecfb75a9d83369c9f` |
| PE-ACTION-008 | RF-20 | SF-07 | MUST NOT | Every transport retry, relay attempt, submission retry, implementation retry, and internal processing attempt | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `578436b2cb6b1778d823d4bc746fb5043cc9c76f34102b0b9fbc1284bbfc6098` |
| PE-ACTION-009 | RF-20 | SF-07 | MUST | Every protocol rule governing repeated authoritative presentations | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `5e725254afc94c74929b159c0d02d9e63693760e819794b98d3f732b2c93036d` |
| PE-ACTION-010 | RF-20 | SF-07 | MUST | Every Protocol Action | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `53eb9b4226ffaddcaa8bac0403c1f93b4dfe68753d51c962559da5fe30294283` |
| PE-ACTION-011 | RF-20 | SF-07 | MUST | Every proof-supported Protocol Action | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `a1b72f91e3b6d27d9517922ed57a91d44c1afad80140c80e120d2b5575764041` |
| PE-ACTION-012 | RF-20 | SF-07 | MUST | Every Protocol Action performed through an implementation | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `24ad0dd544294050c02b6f76b929429d7b1db2b30c996bed46c9fde9f775cca1` |
| PE-ACTION-013 | RF-20 | SF-07 | MUST | Every relationship between a Private Actor and Protocol Action | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `57aaf8bb550db022a9938e4ebb7b8967b58a6c3ff98e433016d06953faa3b9d0` |
| PE-ACTION-014 | RF-20 | SF-07 | MUST NOT | Every Protocol Action identifier and representation | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `a9b035df445d69fde2334e241559af9442b62b5f827f513e3e3417b77aa7f581` |
| PE-ACTION-015 | RF-20 | SF-07 | MUST NOT | Every application interpretation of a Protocol Action | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `009c19c28d1f2e7d0f84cab93f5d01fcee58b799b1fa138e744032110d44ff2b` |
| PE-ACTION-016 | RF-20 | SF-07 | MUST | Every relationship from a Protocol Action to a possible Published Result, Determination, or Protocol State Transition | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `0e10cf56ff23b2f68ac6b146d527fa7d642c686629dace4c8001fc2893dc3a4b` |
| PE-ACTION-017 | RF-20 | SF-07 | MUST NOT | Every Protocol Action interpretation and extension | applicable | E06,E07,E09,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `3cadf5eb5d758382528a2a9b4cac93b3e452ebad010f3d51078634d2426a814a` |
| PE-RULE-001 | RF-21 | SF-07 | MUST | Every Protocol Action | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `191e877c310d4fd89f413976575c6345007b3f0f839b0dd1b6b7c3bb081cef9a` |
| PE-RULE-002 | RF-21 | SF-07 | MUST | Every rule included in an applicable Protocol Action rule set | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `3ff7a7668229d4378a5534f354261f5bbe8280bc01946d90a4347f5ad375b10f` |
| PE-RULE-003 | RF-21 | SF-07 | MUST | Every determination of Protocol Action rule applicability | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `cc7a96f3acee814907c8a499e0635a3fa78f08e4c6e06f879be89e792790fb7d` |
| PE-RULE-004 | RF-21 | SF-07 | MUST | Every Protocol Action admitted for authoritative Evaluation | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `d093184d7625f5aff135a4dc9734a1fb81a9334cc56e9497941bc9c667d6fb8b` |
| PE-RULE-005 | RF-21 | SF-07 | MUST NOT | Every implementation, application, transport, deployment, and operational policy | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `2ec13801ebe56173a4cb5a0c94e4a2d2bdabbf7080370c4c72b12fcabc1811f7` |
| PE-RULE-006 | RF-21 | SF-07 | MUST | Every Protocol Action validity classification basis | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `68f91fc6b4e0bde9886efad8647ebd8cb0a114f765bacba3b1f466bdf0e3c659` |
| PE-RULE-007 | RF-21 | SF-07 | MUST | Every applicable Protocol Action rule set | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `8175acc8c41c77ac1d6eb8b7573e3b2e1fbdd1aff952a8ca1458d20212f26e77` |
| PE-RULE-008 | RF-21 | SF-07 | MUST | Every protocol-validity interpretation | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `dd1e2cd94b1d2be69f18b059327610dfe817e5143cba456208d4922d485c7152` |
| PE-RULE-013 | RF-21 | SF-07 | MUST NOT | Every comparison of Protocol Action validity across materially different evaluation contexts | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `34906a8cb7585f018fd03f11d4d84023e6e1ff75ad0e83d60996770b35b014fd` |
| PE-RULE-009 | RF-21 | SF-07 | MUST NOT | Every application interpretation and external claim associated with a Protocol Action | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `1564edfd6bf23d75f9e882fbd2f16bc181809af75c2bc47599208903c6d42285` |
| PE-RULE-010 | RF-21 | SF-07 | MUST | Every action-local uniqueness or authorization rule | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `a1526a95299f6c919589b65f6dcf762cbe8f42a9d893fea031b71782741c591a` |
| PE-RULE-011 | RF-21 | SF-07 | MUST NOT | Every implementation, transaction, transport, retry, storage, and diagnostic identifier | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `849a1e1c86dfe28414d53cc432d9ad1fcc816f6030eafaee4033cbfd7554be71` |
| PE-RULE-012 | RF-21 | SF-07 | MUST | Every Protocol Action prepared for complete Evaluation | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `f074aa4a9cd24ae6e5695575f82e4bc864235bccaf6a8f539688cc5d55867d4a` |
| PE-EVAL-001 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `b794e1fe6e53ffbb50b222286cf379b561a87ef96d406e3ac61b91ca767f58f5` |
| PE-EVAL-002 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `de5afb99cb11fc13cd9e7fb2c7563271d6337d15de8cb4fd2c6737e1029c9d64` |
| PE-EVAL-003 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `252b8c3425f8d716f2ab354076f1464379004766e945d9dd58af76c392a56051` |
| PE-EVAL-004 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `c674cef0f246bb09e88455abe78a9e6f7e25bcac46721ec604447d09209818ca` |
| PE-EVAL-005 | RF-22 | SF-08 | MUST | Every candidate entering the authoritative Evaluation boundary | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `5937e053cd0dcdc19cdb2a3c1fb4fd4f7a77f38f90b8e7c2361c22c23426a52f` |
| PE-EVAL-006 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation after Evaluation begins | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `911f2102f64406e05eede1605ee3d643aa803898143b5f9a2fa0cc462a16fce2` |
| PE-EVAL-007 | RF-22 | SF-08 | MUST NOT | Every Protocol Action Evaluation after Evaluation begins | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `5e2e06d9e78c6b7f92536ced78a475a4a0766220fbdee14a354fe23895d3489b` |
| PE-EVAL-008 | RF-22 | SF-08 | MUST | Every complete Protocol Action Evaluation | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `4a77beb41e5b05c1d69e30c71fc6f84650abe7e57398d8d0b27a839a59c971e9` |
| PE-EVAL-009 | RF-22 | SF-08 | MUST | Every Evaluation component | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `8ed39f47993843934d650ecf16121cc1611a52f9fce98dc383a4288c3e8893f0` |
| PE-EVAL-010 | RF-22 | SF-08 | MUST | Every Evaluation component | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `19934ebfca4668fb1f88a6119aa6f20aff4589154bb043dedcae512ab73c4d99` |
| PE-EVAL-011 | RF-22 | SF-08 | MUST NOT | Every Evaluation component whose assigned rules are not the complete applicable rule set | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `ed92845b5269d4ad64b91bbc0cf665e5e3a991a55e1c6855af90067de34c180b` |
| PE-EVAL-012 | RF-22 | SF-08 | MUST | Every Evaluation containing multiple required components | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `1302030fccbeb4fc0ad48c8084189e9e4be63b16ca97ea0d0cb9a38ca22645ad` |
| PE-EVAL-013 | RF-22 | SF-08 | MUST | Every proof-verification occurrence contributing to Evaluation | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `59ca28d0229604350a1ca345ddb0a8ff5b9ede5aec659b7d3282b8ee97a4db7a` |
| PE-EVAL-014 | RF-22 | SF-08 | MUST | Every relationship between proof verification and Protocol Action Evaluation | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `958979dbb7a0890b9f781993688aad2196521c2911ec21bf4809bde8e5068678` |
| PE-EVAL-015 | RF-22 | SF-08 | MUST NOT | Every proof-verification result | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `9982697d3d870d3a68da9d43b30f945ed9424a7e1cc7b891ef613eadfa875b4d` |
| PE-EVAL-016 | RF-22 | SF-08 | MUST | Every Evaluation whose applicable rule set contains non-proof validity conditions | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `6a5817a8e1abffa62231a22b467b14f019974042252f378e28349c99bf0048b4` |
| PE-EVAL-017 | RF-22 | SF-08 | MUST | Every Protocol Action Evaluation completeness classification | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `a5f23ec94278eec9897fd39a787b74e346910150e01995f8c7025de92161ee03` |
| PE-EVAL-018 | RF-22 | SF-08 | MUST NOT | Every partial or incomplete Protocol Action Evaluation | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `01d20626fd53684f58f2e0ae80c2f5002e6f8825aaea44cd27aff72a40677231` |
| PE-EVAL-019 | RF-22 | SF-08 | MUST NOT | Every Evaluation failure and every pre-evaluation failure | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `fb149a6c3b2dcb41c9e6f1751401f4ce51ffc23275a6eaefa54cff01995eb104` |
| PE-EVAL-020 | RF-22 | SF-08 | MUST NOT | Every Evaluation component, identifier, evidence record, representation, diagnostic, log, field, route, test, example, and observability surface | applicable | E06,E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `6c2c603f9f4112d76da88a050b7f63fdd010ccd55db58b61e0575beba15e3dfc` |
| PE-DETERM-001 | RF-23 | SF-08 | MUST | Every Protocol Action Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `acb6d521ca17e96f1b2eae50cfa1023c31d89c24dc68ca2bba0945371c845aa3` |
| PE-DETERM-002 | RF-23 | SF-08 | MUST | Every relationship between a Protocol Action Evaluation and its Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `c284ccf84d49c0f0ca33496a7231d450b53eda4bb430658dec745c4c5e1c32d3` |
| PE-DETERM-003 | RF-23 | SF-08 | MUST | Every completed Protocol Action Evaluation | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `e403e907a4a3a76aa1c3466ebeb76be2de82d17a7be6faf923d1adbe79501f5e` |
| PE-DETERM-004 | RF-23 | SF-08 | MUST | Every Protocol Action Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `e5ea7de2f9617426d5e649c4b67dd755246a083202dac9cf707c6eb5897a6182` |
| PE-DETERM-005 | RF-23 | SF-08 | MUST | Every Protocol Action Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `fca171d16f442a59e7368b84fa8f7b14202eb15a2438f95639eb0ce3e5b5c9f4` |
| PE-DETERM-006 | RF-23 | SF-08 | MUST | Every valid Protocol Action Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `2684fb6e803ecbbac9ed8b36d9a095a1399b62ea14abfffabdfd666006cd8ca2` |
| PE-DETERM-007 | RF-23 | SF-08 | MUST NOT | Every incomplete or failed Protocol Action Evaluation | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `e88fd27a726b5324a4ea5f7be51209ccd8ca20dd6b72d3bed3ccd9191a6616d1` |
| PE-DETERM-008 | RF-23 | SF-08 | MUST | Every Protocol Action Determination and proof-verification result | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `f01051917e0dddd4e51004b66ddbbd5c80d403e0480216fb7097f35a39d62b8b` |
| PE-DETERM-009 | RF-23 | SF-08 | MUST | Every Protocol Action Determination and Published Result | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `6ba65ed3cd28e322171f04081803fe2f8616b46cf0a55a9988e974c983392b49` |
| PE-DETERM-010 | RF-23 | SF-08 | MUST | Every Protocol Action Determination and possible Protocol State Transition | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `6f643d0cef428c3a2cadcafca4c3ee45fd9d6213da437e34e8c6ac4dced002d6` |
| PE-DETERM-011 | RF-23 | SF-08 | MUST NOT | Every Determination identifier, representation, diagnostic, log, field, route, test, example, and observability surface | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `ed46863d93fad0d0117309bd83bbaea61cbad60e93619d01efcb772fee8b0b19` |
| PE-DETERM-012 | RF-23 | SF-08 | MUST | Every pair of correct Evaluations of the same Action under the same applicable rules and equivalent contexts | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `2ed9091879994779048ff6f6805597b12515ff782a4541e881dc391d9f03c7d9` |
| PE-DETERM-013 | RF-23 | SF-08 | MUST | Every context-dependent Protocol Action Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `4a57c7b835b6ef45e61e5fbe012bb0e906d405e79c6e30760811639aa331442f` |
| PE-DETERM-014 | RF-23 | SF-08 | MUST NOT | Every Protocol Action Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `22ea02f3495357e2aeca7645c4753d22b9b139321706b584854516580f4a14f5` |
| PE-CLASS-001 | RF-24 | SF-08 | MUST | Every valid Protocol Action Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `21af8192b9efc93c8293630dc3819b9ade4adffc2cc5a44e25d3052bb6571bfa` |
| PE-CLASS-002 | RF-24 | SF-08 | MUST | Every correct accepting Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `67c807d2350612a87effd2e6ff72caf5158cd958d4862b248efd591be93be2f0` |
| PE-CLASS-003 | RF-24 | SF-08 | MUST | Every correct rejecting Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `7e688ed43e3867285008f6a314f34098cafbcbf2d4834d03b3fc77053e9e7708` |
| PE-CLASS-004 | RF-24 | SF-08 | MUST | Every correct Protocol Action Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `64aac3f297287d0fcb32ce9bdc699fd85b2d9190e00105dd00396b05eecc209e` |
| PE-CLASS-005 | RF-24 | SF-08 | MUST | Every correct Protocol Action Determination | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `002ec96c92e7058996d49c46f064deecb08554f564886867197e433cb7dceb39` |
| PE-CLASS-006 | RF-24 | SF-08 | MUST NOT | Every incomplete Evaluation, Evaluation failure, and pre-evaluation failure | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `ec2c548ebf4a8102bb694585ba8732ece58effa91783c6ab55e00f1374310542` |
| PE-CLASS-007 | RF-24 | SF-08 | MUST NOT | Every infrastructure, transport, deployment, storage, implementation, and observability failure | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `9efa97358610654b0cf7ffcef7c670d96030898eac1ae53f39a6d79775eee5f8` |
| PE-CLASS-008 | RF-24 | SF-08 | MUST NOT | Every proof-invalid result considered outside complete Protocol Action Evaluation | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `7e6aaff6ca3d7b9a2c4516bfe1406d05418f99bbda1855cecb0a3b4d8496d473` |
| PE-CLASS-009 | RF-24 | SF-08 | MUST NOT | Every erroneous acceptance or rejection classification | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `5ad95ec718c2c1a6f24ae7420eb129546c3103cc474f8311655a58c7085ea435` |
| PE-CLASS-010 | RF-24 | SF-08 | MUST NOT | Every acceptance and rejection classification | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `8090b6d1c87969e405a808ea0dbe03834ff765d134332ab2950cc2a43ba9748f` |
| PE-CLASS-011 | RF-24 | SF-08 | MUST NOT | Every application or external interpretation of acceptance or rejection | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `9c600dbdf8b43648fc091151d6864e663dfc4c1a6e28067f7bf22dc8480f81fa` |
| PE-CLASS-012 | RF-24 | SF-08 | MUST NOT | Every acceptance or rejection representation, identifier, diagnostic, log, field, route, test, example, and observability surface | applicable | E07,E08,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `05371fe45dc21572536a81087104f3d0590721d806e0024739f2cba82f587956` |
| PE-NOTRANS-001 | RF-25 | SF-08 | MUST | Every accepted Protocol Action Determination | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `8c2aa7b3bf881ee3a5c432eb1e57b8335b5e0baaf7f408854d4e95898967997a` |
| PE-NOTRANS-002 | RF-25 | SF-08 | MUST | Every accepted Determination for which no transition is required | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `42586b59e1fe4664f3db6d591a36a21a8678cbe9f760e36ba6d3d51ae1cec67d` |
| PE-NOTRANS-003 | RF-25 | SF-08 | MUST | Every accepted no-transition path | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `5d7a96b125c1d37b654f7dc56034d522e8a89f8203e41408419fe4e04d05379b` |
| PE-NOTRANS-004 | RF-25 | SF-08 | MUST NOT | Every accepted no-transition path | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `c2f710f9aa591e7d97813d6cd86f7c298a618d4e7bbb1d8d69fa62910116ee5e` |
| PE-NOTRANS-005 | RF-25 | SF-08 | MUST NOT | Every inference from Protocol Action acceptance | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `1973a57da25ab424261cac284881540de004c6deb202910cdaedc058c2528c3d` |
| PE-NOTRANS-006 | RF-25 | SF-08 | MUST NOT | Every inference from Protocol Action acceptance | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `e231e0fdb2d21b430e4b532353712147e45b0565bebcb1bf760570c8a50805f0` |
| PE-NOTRANS-007 | RF-25 | SF-08 | MUST NOT | Every inference from Protocol Action acceptance | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `fbf72ae27a7b558072ca93e50a43906c4e4b727532357f23c5c2a688ca8964b8` |
| PE-NOTRANS-008 | RF-25 | SF-08 | MUST NOT | Every rejecting Protocol Action Determination | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `6054dc0db95e719349aa6f31e40696573d25708e9db0012768fca4648075e480` |
| PE-NOTRANS-009 | RF-25 | SF-08 | MUST NOT | Every implementation handling an accepted no-transition path | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `d516a954faa36ff2ab9bbeb833fab72913ef05f695305d22caf61389c981d91b` |
| PE-TRANSMAP-001 | RF-26 | SF-09 | MUST | Every published Protocol Transition mapping | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `d291b696f4d5a7a53d334045e43d4835b8e793286ccbb32dbe4f7eb54e4ffb94` |
| PE-TRANSMAP-002 | RF-26 | SF-09 | MUST | Every published Protocol Transition mapping | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `0dc78696640ce21654dfb1a018e60fd6af906b582c93a4c7ba25acb577b8660e` |
| PE-TRANSMAP-003 | RF-26 | SF-09 | MUST NOT | Every Protocol Transition mapping and every interpretation of it | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `2c60d5d2cde2122e09f493f4fbf29c392b0b7122bf75ffa3d468ba4b85bf5664` |
| PE-TRANSMAP-004 | RF-26 | SF-09 | MUST | Every implementation applying a Protocol Transition mapping | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `f7a477bcf651c98dc6a93ddf1e15cde06a9affe2ad085ffe1eeb19ac17617467` |
| PE-TRANSMAP-005 | RF-26 | SF-09 | MUST | Every published Protocol Transition mapping with transition-specific preconditions | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `82ae56cf13c8a7e2fe1fcb2e50e5eda8c04ca41baf84f45c6023b15c9238c33f` |
| PE-TRANSMAP-006 | RF-26 | SF-09 | MUST | Every transition-eligibility evaluation | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `02a4b817a34199976beb0925feb9ab9a5316216be16c5b7ff2f02813f3e4ab65` |
| PE-TRANSMAP-007 | RF-26 | SF-09 | MUST | Every transition-eligibility evaluation whose complete applicable precondition set is satisfied | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `7e71508c79cdc2370bcb8c49796cd654e2b1cb25082ecde6a14761302c960533` |
| PE-TRANSMAP-008 | RF-26 | SF-09 | MUST | Every transition-eligibility evaluation whose applicable precondition set is not completely satisfied | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `95b022a72912f541869f92750582c154d86c3642ec631be2bc7261d30399b444` |
| PE-TRANSMAP-009 | RF-26 | SF-09 | MUST NOT | Every implementation evaluating transition preconditions | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `408d1c2cdb2c47f88928a498c3e8af10af303157ca5e7c6116d28bff67a3eb5e` |
| PE-TRANSMAP-010 | RF-26 | SF-09 | MUST | Every relationship between transition eligibility and complete Protocol Action Evaluation | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `a233e3ac92b4edaf3e5285acb7f21013d3a44f2669d2f818e500f587b64342e1` |
| PE-TRANSMAP-011 | RF-26 | SF-09 | MUST NOT | Every transition-enforcement result | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `fb4589ec65b3e424ecd69faaed31e24246c84e25213fe21f02e378df57a27f77` |
| PE-TRANSMAP-012 | RF-26 | SF-09 | MUST NOT | Every implementation-local restriction on operation exposure, request handling, or execution capability | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `4e15ecb4f5af6a0c0fcdaa8f4647f9d3abfb99498e0773b2660adb12533015e2` |
| PE-TRANSMAP-013 | RF-26 | SF-09 | MUST NOT | Every mapping, precondition, eligibility, enforcement, diagnostic, log, field, route, test, example, serialization, and observability surface | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `fe44d889a35bd4c64cb6f3b4b57e31b62a005bd62fb5f475908fb45476014dee` |
| PE-TRANSOCC-001 | RF-27 | SF-09 | MUST | Every Protocol State Transition | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `0603e35674df40d79fee8ed453b41952a6ee27f14065a88911628ee1ea651794` |
| PE-TRANSOCC-002 | RF-27 | SF-09 | MUST | Every Protocol State Transition | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `1a1f15b7d0048d0bdc46ff7ff2be75a5e33f4aa059e4c600056eb449ec4048f2` |
| PE-TRANSOCC-003 | RF-27 | SF-09 | MUST | Every relationship between a Protocol Action and a Protocol State Transition | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `5e9b483db2a5daab5c54beeba132ee22cc8aaab416cb4b6d4ce9055fc20559ba` |
| PE-TRANSOCC-004 | RF-27 | SF-09 | MUST | Every relationship between a Protocol Action Evaluation and a Protocol State Transition | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `68b5d98f045e726b5f39957fcc7e1f6687d4d4b0c814ead3c3776872c1a04212` |
| PE-TRANSOCC-005 | RF-27 | SF-09 | MUST | Every relationship between a Protocol Action Determination and a Protocol State Transition | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `fe655b74cea348d05cfb8a135cf42b3e202c5611b70011408eaedb4c123017ac` |
| PE-TRANSOCC-006 | RF-27 | SF-09 | MUST | Every Protocol State Transition occurrence | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `ab829ca230e00327c9ff60b496adc5daa89f999849c67de1aeaad711d8d90721` |
| PE-TRANSOCC-007 | RF-27 | SF-09 | MUST | Every authorization, execution, commitment, and failure stage concerning one Protocol State Transition | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `cdd7e2ab45f13253ed5860d1618e92d6e49f36107b1fddd8a7ae09f4322a7f8d` |
| PE-TRANSOCC-008 | RF-27 | SF-09 | MUST NOT | Every transition lifecycle representation | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `c2cc1d47c45dd95382b9fa13b27cf6a26211606007b51f63b636d4e2072c9d3e` |
| PE-TRANSOCC-009 | RF-27 | SF-09 | MUST | Every terminal Protocol State Transition classification | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `a14a43ad055292d49d74fc5dbb53848840b0fdea8dcc5b28593ac26029fbc674` |
| PE-TRANSOCC-010 | RF-27 | SF-09 | MUST NOT | Every authorized transition that has not reached a terminal classification | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `556682ddf1cb0ac82f8b205efd469eee00e19f0b64c9b036b22b94ee11f0e16f` |
| PE-TRANSOCC-011 | RF-27 | SF-09 | MUST NOT | Every transition identifier, lifecycle record, representation, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `6e96a39eb0ef263eb0f8cc4a777c0c58a5b6db247c0de0d0a5e49e703c92575c` |
| PE-TRANSAUTH-001 | RF-28 | SF-09 | MUST | Every authorization of a Protocol State Transition arising from a Protocol Action | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `293ecbdfcc31b1de48e31dfadac9126f4dda794c4dc15e863702846e2f6c3bc7` |
| PE-TRANSAUTH-002 | RF-28 | SF-09 | MUST NOT | Every rejected Determination, incomplete Evaluation, Evaluation failure, and absence of Determination | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `9c578019662eb2befa29b88afe404e81b1333c6a9985e6b2cdad138e1aa1cd58` |
| PE-TRANSAUTH-003 | RF-28 | SF-09 | MUST | Every transition authorization | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `cffb29e0794e28cbc777f764e17d389302f6a263cb34aaf80be0963b27206af6` |
| PE-TRANSAUTH-004 | RF-28 | SF-09 | MUST | Every transition authorization | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `9649ac42dcdab512c0628da3470aac0e90ec234ae8588ecd90823459deab2da4` |
| PE-TRANSAUTH-005 | RF-28 | SF-09 | MUST NOT | Every accepted Protocol Action Determination | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `504ef364e361266691057e8f1dda69beccdde3f3be1d13a4b6cb2e705ca3338f` |
| PE-TRANSAUTH-006 | RF-28 | SF-09 | MUST NOT | Every transition authorization | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `3dd1e4d5d28c477c9cce3314506129c3b676fca314936eb70d1fc0d6e77c247e` |
| PE-TRANSAUTH-007 | RF-28 | SF-09 | MUST NOT | Every transition authorization | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `22c2dae3e7741bd34cf94a7c88001954ebc3717b57493336fc4434ed1831ef17` |
| PE-TRANSAUTH-008 | RF-28 | SF-09 | MUST NOT | Every transition authorization | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `260f1c221f439807439cb1611f57b7da70af6f516d6d60db92defb5c9948ed72` |
| PE-TRANSAUTH-009 | RF-28 | SF-09 | MUST | Every accepted Determination for which transition cardinality is applicable | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `3bd023390f652c156266481db3a6c3f9ab6b7c5a3dedeaf207352d4ed1b25374` |
| PE-TRANSAUTH-010 | RF-28 | SF-09 | MUST NOT | Every implementation realizing transition authorization | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `26e2622cf747689b0bc054c84e782ad5f6929e9d793b1ea80c2384e1a8877bfa` |
| PE-TRANSAUTH-011 | RF-28 | SF-09 | MUST | Every accepted Determination requiring zero transitions | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `fc799ff5fd57c34fbb01873ebba71e7a557eaf37c2993d4f947a081948a5a63a` |
| PE-TRANSAUTH-012 | RF-28 | SF-09 | MUST | Every accepted Determination authorizing multiple independently committable effects | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `986d698451b1e69420406f26f531e182bda34e0f0b7db5104f578b7949cb2531` |
| PE-TRANSAUTH-013 | RF-28 | SF-09 | MUST | Every accepted Determination authorizing multiple transitions with protocol-defined ordering or dependencies | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `2034126dafdea0a342a42512e65c0adcfeb951b12005d41d3efdf083360f9e02` |
| PE-TRANSAUTH-014 | RF-28 | SF-09 | MUST | Every group of protocol-required state effects that must succeed or fail together | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `c61d407b3e09f3cbd90850c02171ab28d5514650a4cb6c83d4ada6becbfb6a61` |
| PE-TRANSAUTH-015 | RF-28 | SF-09 | MUST NOT | Every authorization of multiple separately identified Protocol State Transitions | applicable | E07,E08,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `cb8ecb91aff7957c842b66af53e91b60c55209b813f7bace825ee4a77ff02afc` |
| PE-TRANSEXEC-001 | RF-29 | SF-10 | MUST | Every Protocol State Transition execution | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `115e93f7e8a8ca59187e51b90a8f3ececaaa585eb67ade8bfb2de002bb6fe152` |
| PE-TRANSEXEC-002 | RF-29 | SF-10 | MUST | Every execution entry | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `7c2f8d01b32b705f42bb1946e9c25dcb4cd1ba2bcfae97df0288631ead35ec95` |
| PE-TRANSEXEC-003 | RF-29 | SF-10 | MUST | Every execution of an authorized Protocol State Transition | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `abde68003dec2c543658a66b603f98c805940c0479313756a560b0f0194562df` |
| PE-TRANSEXEC-004 | RF-29 | SF-10 | MUST | Every implementation executing an authorized Protocol State Transition | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `161e4a961f1402b057f75bf0ae0b4a9463a46c777f83317fd242f3963a95871e` |
| PE-TRANSEXEC-005 | RF-29 | SF-10 | MUST NOT | Every implementation executing an authorized Protocol State Transition | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `0ffef0faab46c16df7736636f5199dd0cbcf375f7648c8e815ebd5782bf34055` |
| PE-TRANSEXEC-006 | RF-29 | SF-10 | MUST NOT | Every execution of authorized `U` | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `3213cb86016949dcfd281f7485c81ee76453f7b413ec7a76baddd001ee6d7d49` |
| PE-TRANSEXEC-007 | RF-29 | SF-10 | MUST | Every relationship between transition eligibility and transition execution | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `b9d82c0eea60a04fc5fcbe1290ee2de4175ec2f5bb6dd90c72c80960e53ba665` |
| PE-TRANSEXEC-008 | RF-29 | SF-10 | MUST NOT | Every completed transition execution | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `03f0e92267e005e187981fbf10174dd9c638545329eb2904457b0e5744b5ed82` |
| PE-TRANSEXEC-009 | RF-29 | SF-10 | MUST NOT | Every successor-state value or representation derived during execution | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `e678c4641d0757d20866faa573f7ef422d38fbf2154a14a5ea27f9869fb47b84` |
| PE-TRANSEXEC-010 | RF-29 | SF-10 | MUST | Every implementation unable to preserve the authorized transition during execution | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `6a98e5d2af6aeaad1764cfbdc58476cf05038aa30d34477449a66a910b42b7fc` |
| PE-TRANSEXEC-011 | RF-29 | SF-10 | MUST NOT | Every failed transition execution | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `52fd168df4710fbbdb35e3e06a338bc66448e2778f3fe71c1bae3eca62a0e1d0` |
| PE-TRANSEXEC-012 | RF-29 | SF-10 | MUST NOT | Every execution representation, instruction, transaction, internal call, storage operation, retry, diagnostic, log, field, route, test, example, serialization, and observability surface | applicable | E08,E09,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `9694938e4ef83b7dba27eae2db91079bf7897b51eef07e4316ecf00e5d67f804` |
| PE-COMMIT-001 | RF-30 | SF-10 | MUST | Every committed Protocol State Transition | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `3393f75b094002d0190a0c990632f8733747a6f4b8566cdc7b791ca992be8748` |
| PE-COMMIT-002 | RF-30 | SF-10 | MUST | Every committed Protocol State Transition | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `c1be3bbd88b6c42b4bde5715feb07b503da8231852e25ff28564d533ac430df2` |
| PE-COMMIT-003 | RF-30 | SF-10 | MUST | Every committed Protocol State Transition | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `59fd7717cb32a93f032b8c3fb835b2ee71fe5c73f88062ce0e83972eadcb3877` |
| PE-COMMIT-004 | RF-30 | SF-10 | MUST | Every committed Protocol State Transition authorized against `Q0` | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `33ae0b69a619ee2832624162312697342b935982c8fb349ef8cae7d3c029aea4` |
| PE-COMMIT-005 | RF-30 | SF-10 | MUST | Every committed Protocol State Transition | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `981bf3ca913b90b323fb994547741c0be75b312b60c247f6e3d18c65db4d9639` |
| PE-COMMIT-006 | RF-30 | SF-10 | MUST | Every committed Protocol State Transition | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `8cdc36df5483e0a535e3ccb3364d707cce2c5ea31e7f0ccaacc6542dbc55f930` |
| PE-COMMIT-007 | RF-30 | SF-10 | MUST | Every committed Protocol State Transition | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `72d9274f59c20209ee6273a8e44bee026a69eb35796fcdab2464166f6740032d` |
| PE-COMMIT-008 | RF-30 | SF-10 | MUST | Every valid authorization and execution context for `U` | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `24b8eca3bdb686c397d3709a4adb6796c8c3bcab07fbe33c79a643db41e69bed` |
| PE-COMMIT-009 | RF-30 | SF-10 | MUST NOT | Every partial execution of a Protocol State Transition | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `faae5f386832dea7baa4c6439dfd8588351704bc51be38447fa4c04ddc2ba541` |
| PE-COMMIT-010 | RF-30 | SF-10 | MUST NOT | Every partial or incomplete state change | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `842ad97c53f8ccb6222b4f55501aa96c379568f89c0bfb30074be3e27e25de1d` |
| PE-COMMIT-011 | RF-30 | SF-10 | MUST NOT | Every Protocol State Transition | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `1a649cbaae448d56a1f3cfe930d89aff1c3235e8aea4299a1c3b01d2a6fc7821` |
| PE-COMMIT-012 | RF-30 | SF-10 | MUST NOT | Every implementation assertion, report, event, record, diagnostic, or representation concerning commitment | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `2d05a30cb42870109e899dd46c170973347667f55608604c8c2a05982ad79446` |
| PE-COMMIT-013 | RF-30 | SF-10 | MUST NOT | Every commitment representation and interpretation | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `9de67628e67599f1dd04734b767280ce66ffd8712d6bcdfe4a77fab0280b018c` |
| PE-STATE-001 | RF-31 | SF-10 | MUST | Every protocol-state representation | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `3e750755356499f8f70fe2e35d1a4afcc28f185a7b267829abf008464ac5bf78` |
| PE-STATE-002 | RF-31 | SF-10 | MUST NOT | Every application, implementation-local, transport, database, cache, UI, operational, diagnostic, and observability state representation | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `d2b0d5945143da6aaa5b3973f89cdbcbe0e68fb342c5f641b973fc3f92341340` |
| PE-STATE-003 | RF-31 | SF-10 | MUST | Every Protocol State Transition authorization | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `e9528b347fbff9acd31ffdb91a6c75fc45324f1b5f902df9335d7955920ccb71` |
| PE-STATE-004 | RF-31 | SF-10 | MUST NOT | Every implementation realizing an authorized transition | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `4bf61d21641c23e6cd4ff4c4b1b34d76b8a7535728e4011393025ec10097e450` |
| PE-STATE-005 | RF-31 | SF-10 | MUST | Every successor-state derivation | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `a93fa77a41ce18d2868fa3982f73b679e322e8376e938c670184d959b034841a` |
| PE-STATE-006 | RF-31 | SF-10 | MUST NOT | Every implementation deriving successor-state material | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `a7b773f2957dadcf421e7ecc2a19153276a742436a7a78f32d7de7d8adeab9a2` |
| PE-STATE-007 | RF-31 | SF-10 | MUST NOT | Every successor-state value derived before commitment | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `ccfccbd369a2fefaea8193a71fdb55793d888523d2050389d625ef6a9b2bceee` |
| PE-STATE-008 | RF-31 | SF-10 | MUST | Every committed Protocol State Transition | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `a5fe8cfc4d27f003a8b91f686eca55a40486c495d6be5ca0f33e6aa636bf6500` |
| PE-STATE-009 | RF-31 | SF-10 | MUST | Every committed Protocol State Transition from `Q0` to `Q1` | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `3816dcbb806afa444572a65a7b7eaf8ddf2b9fae9c7a9ca3d74027ec4640a087` |
| PE-STATE-010 | RF-31 | SF-10 | MUST | Every authoritative protocol-state evolution | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `d3a16c427d0c29fd316d3ac51650c6ff91f71936b9f57c8255a3f8c9b735ab07` |
| PE-STATE-011 | RF-31 | SF-10 | MUST NOT | Every failed, incomplete, partial, simulated, predicted, or merely reported transition | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `cd1e08c6fb17d1dd487ad8117ca2918624ccf9055dacafbb03bb9159e74969f4` |
| PE-STATE-012 | RF-31 | SF-10 | MUST | Every committed protocol-state evolution | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `e60ca3724466b394c1cbb937f27dc1b8d84388c80af8b4c2fdc4626d9d363315` |
| PE-STATE-013 | RF-31 | SF-10 | MUST NOT | Every protocol-state identifier, state representation, successor-state derivation, evolution record, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | applicable | E08,E12,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `431a4fdf622620b19344bd43540e9edb29954f8386df325af91319a540edd3f7` |
| PE-STATEHIST-001 | RF-32 | SF-11 | MUST | Every Protocol State Transition included as a committed state change in authoritative protocol-state history | applicable | E08,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `a8e0ec93be242338100790ce727c552f08e1f52c9c6f32c6e67df287c71a49ca` |
| PE-STATEHIST-002 | RF-32 | SF-11 | MUST | Every authoritative protocol-state history representation | applicable | E08,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `63232577b84e9439a1c98f536ab8da171525bc2af3288809467e0dc0c9401e5e` |
| PE-STATEHIST-003 | RF-32 | SF-11 | MUST NOT | Every failed Protocol State Transition | applicable | E08,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `ed7425bc43e9f4f5fe8b65893d70db454420abef1d5a502d18b11a9b2d48becf` |
| PE-STATEHIST-004 | RF-32 | SF-11 | MUST NOT | Every pre-transition failure | applicable | E08,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `75a719de175dd041be067c7c7a679ce7ca91bf99c058f54d4277679cab765ec4` |
| PE-STATEHIST-005 | RF-32 | SF-11 | MUST NOT | Every partial execution or partial state change | applicable | E08,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `febe673c045a204f0aff91f0423899e7cbd0c442eecab523fabc3d4768f134de` |
| PE-STATEHIST-006 | RF-32 | SF-11 | MUST NOT | Every operational attempt, diagnostic, retry, log, database row, event, report, error, cache record, or observability record | applicable | E08,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `b826f6c60a76492a85e594b08798717a07416d9d8589bfc85660d5aa212647a4` |
| PE-STATEHIST-007 | RF-32 | SF-11 | MUST | Every permitted protocol-state history realization | applicable | E08,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `b994bc0b446a7db59eddd213aaf4f5c2e85fc375b03e8b2790f1606b20436137` |
| PE-STATEHIST-008 | RF-32 | SF-11 | MUST NOT | Every history identifier, entry, representation, ordering record, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | applicable | E08,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `00cd9412dd13c36f15399613e995860fb363f83c32ecaf691e8894e9e422632b` |
| PE-STATECONSEQ-001 | RF-33 | SF-11 | MUST | Every committed Protocol State Transition | applicable | E08,E11,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `251ddf53a0809d07ceecc2630a75ba3f572fc7855a56c9295825b06ef10c4148` |
| PE-STATECONSEQ-002 | RF-33 | SF-11 | MUST | Every public protocol-state consequence | applicable | E08,E11,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `21864c9b98cdaa2f2fcccec9cc6fa1c1d95b4dcd311addb35ae944902ed733d6` |
| PE-STATECONSEQ-003 | RF-33 | SF-11 | MUST | Every relationship between a Published Result and a public protocol-state consequence | applicable | E08,E11,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `d1318d743b6e7198f29f51677d8de81938d34c7cc47b970474932ac6e90ffa8d` |
| PE-STATECONSEQ-004 | RF-33 | SF-11 | MUST | Every relationship between a Protocol Action Determination and a public protocol-state consequence | applicable | E08,E11,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `2668f14f0517cf0d2d0f1c107916ed91fdf17e763d947a88d43e0cc135db1d1e` |
| PE-STATECONSEQ-005 | RF-33 | SF-11 | MUST | Every relationship between authoritative successor state and public protocol-state consequence | applicable | E08,E11,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `9e9adf1463efeff2aa2afb3312b1f4cac898735d1d9acaa86c1c5b81f0e7e982` |
| PE-STATECONSEQ-006 | RF-33 | SF-11 | MUST NOT | Every public protocol-state consequence and every interpretation of it | applicable | E08,E11,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `79c5d39bf7952bb8ab8fdda5dd5a5040c09e69ad002b7103a4e17331cb7e0da4` |
| PE-STATECONSEQ-007 | RF-33 | SF-11 | MUST NOT | Every public protocol-state consequence | applicable | E08,E11,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `b4ae925c5c61a8c08502f27bc4b8c6cea0ec0c44d1b8a4e19bf7f7845c0085c3` |
| PE-STATECONSEQ-008 | RF-33 | SF-11 | MUST NOT | Every public consequence identifier, representation, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | applicable | E08,E11,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `87fd8d0c4ab46bc7190e2e65c0e20690d5d885b5984884973b9b7b2f82a887d1` |
| PE-STATECONSEQ-009 | RF-33 | SF-11 | MUST NOT | Every public consequence recording authorization, membership, eligibility, uniqueness, possession, or another bounded protocol property | applicable | E08,E11,E12,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `8b914757e3e6c0d16f58dc4e7fc191deb505ab7f53a3e4fecca4c6c202a08dce` |
| PE-FAIL-001 | RF-34 | SF-11 | MUST | Every protocol-use failure or implementation-error classification | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `458cc0f198922cc3d426c310225679fbffdc542a648388641b6cad7385a26e9d` |
| PE-FAIL-002 | RF-34 | SF-11 | MUST | Every pre-evaluation failure | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `303f3c2e8534efba704d9d964aabb167f003ecf12909f7edc742b1f04a81040b` |
| PE-FAIL-003 | RF-34 | SF-11 | MUST | Every Protocol Action Evaluation failure | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `412fbb37bc1adbc69f3d617fbfe3537758cc83848ffae8a65248582743b3e01c` |
| PE-FAIL-004 | RF-34 | SF-11 | MUST | Every Protocol Action rejection | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `be322c859c2854cedeb05458bd2a799492ec4f6376b950623438a22c661c46c2` |
| PE-FAIL-005 | RF-34 | SF-11 | MUST | Every accepted no-transition terminal path | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `f52d874883613ecd946f4ac035f38b5b564f06a811e53170e508e6431e0da381` |
| PE-FAIL-006 | RF-34 | SF-11 | MUST | Every pre-transition failure | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `a7359cfc2dedfad3fe95b785eeacb6e58e614f6dd57c9f7b1500a56f83aaca27` |
| PE-FAIL-007 | RF-34 | SF-11 | MUST | Every transition failure | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `54056f36247769c75fdb7331222e5b8bb007618319929bb1c8146bdd8adb8d10` |
| PE-FAIL-008 | RF-34 | SF-11 | MUST NOT | Every stale authorization | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `19efdb01719e8f8229df55e1f0e135936e7a5f05a7866e497b0d97cd50383000` |
| PE-FAIL-009 | RF-34 | SF-11 | MUST | Every implementation error | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `66d1c63819753d05a67e36a7ea2ba52ae9aaf5e6dde1b03f09441e4b9339057a` |
| PE-FAIL-010 | RF-34 | SF-11 | MUST | Every incorrect execution diagnosis | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `b5c02cee6f394e9c1aaf13fc7a1e3e70167906394b0ef8b6677ef5d455335a66` |
| PE-FAIL-011 | RF-34 | SF-11 | MUST | Every incorrect commitment diagnosis | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `fc7299210d24d72152e284912698ac128d7a1ab8d4248e44208db73c8490e3b9` |
| PE-FAIL-012 | RF-34 | SF-11 | MUST | Every incorrect reporting diagnosis | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `50a71bf2af07425bd841f59e456df013afed9ef3c2b3405e519195feb3ba7efe` |
| PE-FAIL-013 | RF-34 | SF-11 | MUST NOT | Every pre-transition failure | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `62b2b3600a82a3f682dba23bbb25779dcf492203f0526e89fa6c98022b8243bb` |
| PE-FAIL-014 | RF-34 | SF-11 | MUST NOT | Every transition failure, stale authorization, implementation error, incorrect execution, incorrect commitment, and incorrect reporting condition | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `a118d1f7ab2790de5c3698e0f93ccaf4f0a6a80af362cda6cdada68b41c78091` |
| PE-FAIL-015 | RF-34 | SF-11 | MUST NOT | Every infrastructure failure, inability to preserve `U`, changed-state condition, partial execution, or reporting error | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `950445c85864fe9c972b6f87a45dfa387a0ad05d5066c7b824be46776500fd26` |
| PE-FAIL-016 | RF-34 | SF-11 | MUST NOT | Every failure, error, staleness, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `1c1202aebdbc99b0968d0585282b7dfaaaba8a3db308005164daa2634db44e63` |
| PE-FAIL-017 | RF-34 | SF-11 | MUST NOT | Every failure classification and implementation-error diagnosis | applicable | E07,E08,E09,E10,E11,E13,E14,E15,E20 | BD,TD,RG,DB,RO | ambiguous | `c62646e3fa8284cd5e7882463233620032685792f05a3d6ad9109ee99a1c0f46` |
| PE-STALEAUTH-001 | RF-35 | SF-11 | MUST | Every transition authorization bounded to one pre-transition protocol state | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `3c6336f14411a295c62514ad171e3ce6859707d54e48099b786bfcbd2edfd930` |
| PE-STALEAUTH-002 | RF-35 | SF-11 | MUST | Every authorized transition before execution and commitment | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `2c65313f038cae433ee19b1587d81787e6c8b702fc181df8d15f37f48e092605` |
| PE-STALEAUTH-003 | RF-35 | SF-11 | MUST | Every authorized transition whose current protocol state remains equivalent to `Q0` | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `dd83f917afe828c5bc58dbeadf962881d6154256dfec8f2282bf464a5e8a89a3` |
| PE-STALEAUTH-004 | RF-35 | SF-11 | MUST | Every authorized transition whose current protocol state materially conflicts with `Q0` | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `194424e9f0e9b86486b5669a533509cd82134a2095e3112744441cfea8883b88` |
| PE-STALEAUTH-005 | RF-35 | SF-11 | MUST NOT | Every stale transition authorization | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `3dd8ca6057c8d512e2a13e5f4b87cdd63037ebd63fb6cc339e35f8bec78435a3` |
| PE-STALEAUTH-006 | RF-35 | SF-11 | MUST NOT | Every implementation resolving applicable-state conflict | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `82ddedf5f1298a308d79805f09576363dad5ce7068aaaf5b35594fa015d9898c` |
| PE-STALEAUTH-007 | RF-35 | SF-11 | MUST NOT | Every stale transition authorization | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `6f2a744e774349c2ce74adf7b1690777dc9cffe20952e01d7f1f7580f4b17ad0` |
| PE-STALEAUTH-008 | RF-35 | SF-11 | MUST | Every materially changed context or state for which the applicable protocol rules require re-evaluation | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `9cee1df3083ef43e111b7c92b88db6cb485c81ffd33cbc14bb0ee00b77ccc156` |
| PE-STALEAUTH-009 | RF-35 | SF-11 | MUST | Every completed required re-evaluation | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `53e942c7f2196c398cd3aa695981cba8c1debbc217b7e75d110abd856a36e8e4` |
| PE-STALEAUTH-010 | RF-35 | SF-11 | MUST NOT | Every required re-evaluation | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `032677fc52886dac713b135876572f922d4f9a315a5cafe3bba435a81ac4ff2c` |
| PE-STALEAUTH-011 | RF-35 | SF-11 | MUST NOT | Every stale-authorization and re-evaluation identifier, record, diagnostic, log, field, route, test, example, serialization, storage key, and observability surface | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `b30fc60a5eae10bfbb1c6d8ea0cd83336536a4bdf982d8e929ffa33f020bf29a` |
| PE-STALEAUTH-012 | RF-35 | SF-11 | MUST NOT | Every stale-authorization condition and representation | applicable | E07,E08,E14,E15,E20 | BD,TD,DB,RO | ambiguous | `195a47af7220b36a3cde4bb764de5db2a13f140167297776f5dd707d047e95f6` |
| PE-APPREP-001 | RF-14 | SF-12 | MUST | Every Application Request | non-applicable | E01 | NR | not-required | `b55ec582476d1ac38cf8f687352def20eb915ca99349c251c519e592b330a718` |
| PE-APPREP-002 | RF-14 | SF-12 | MUST | Every identified Application Request | non-applicable | E01 | NR | not-required | `e768731e2eec25de4579a4a5afc64086b2a258014066d2a3c4c31e4fbac0d35b` |
| PE-APPREP-003 | RF-14 | SF-12 | MUST NOT | Every Application Request | non-applicable | E01 | NR | not-required | `470996553cef9685e631973d74eabd1243b9d4ae4ba94ec39af61e3530a962dc` |
| PE-APPREP-004 | RF-14 | SF-12 | MUST | Every application-owned request value | non-applicable | E01 | NR | not-required | `e1a84f12e714ac49494a5169bd6694d702d3c7867191dae9d60370686612dda0` |
| PE-APPREP-005 | RF-14 | SF-12 | MUST | Every Application Adapter | non-applicable | E01 | NR | not-required | `41643c6164d469aa94bfd83fd20d20f18be9a974f2022755278b9fab1766c007` |
| PE-APPREP-006 | RF-14 | SF-12 | MUST | Every identified Application Adapter | non-applicable | E01 | NR | not-required | `a57266e0abe83dbf8410843b5373c9ca619fea476a3dfc99274727870f988d73` |
| PE-APPREP-007 | RF-14 | SF-12 | MUST | Every adapter translation | non-applicable | E01 | NR | not-required | `d79c916db7b123e43ba1dd876f9b5806af7e01b453c687fc059a5f11f33b740b` |
| PE-APPREP-008 | RF-14 | SF-12 | MUST | Every successful adapter translation | non-applicable | E01 | NR | not-required | `c6cb0fe99794046ebb596d0866e5594cdc7cc5e7e2356cfa58430714b80c7d7e` |
| PE-APPREP-009 | RF-14 | SF-12 | MUST | Every adapter unable to preserve applicable meaning | non-applicable | E01 | NR | not-required | `b3c46dd5b5e435d9f9645c2f5d54cc6ec25020c650d3056b7df5ceaf99df1665` |
| PE-APPREP-010 | RF-14 | SF-12 | MUST NOT | Every adapter translation | non-applicable | E01 | NR | not-required | `b5a5053b1912d22706dd9fadd35c388cec285c9870636fc6ea11722be7a7c500` |
| PE-APPREP-011 | RF-14 | SF-12 | MUST | Every Application Response | non-applicable | E01 | NR | not-required | `cb4d3b39e4a37541e9056ba4625373fe8b84a3a7bcbe2ba828856b87ba002e88` |
| PE-APPREP-012 | RF-14 | SF-12 | MUST | Every identified Application Response | non-applicable | E01 | NR | not-required | `1d58c1a034db47b41298f3006c9b825dc1c146f028c366321b8da74d0e832ec0` |
| PE-APPREP-013 | RF-14 | SF-12 | MUST NOT | Every Application Response | non-applicable | E01 | NR | not-required | `13c0fd0d886c701f51538f157f3a80dcd083c1b1ff2763d07ac8d2fe05ca35a1` |
| PE-APPREP-014 | RF-14 | SF-12 | MUST | Every Application Response derived through translation | non-applicable | E01 | NR | not-required | `b4c6d1b5ee7783310470a6f33a49802cc0c8dd7855f3d7530452cbf2795ae07d` |
| PE-APPREP-015 | RF-14 | SF-12 | MUST NOT | Every Application Request, adapter output, and Application Response | non-applicable | E01 | NR | not-required | `dad6863dd374d5cd04de17de14634f123e6c9995937e163a2eeb13a04a8b05ad` |
| PE-APPREP-016 | RF-14 | SF-12 | MUST | Every request, adapter, response, field, serialization, example, and diagnostic surface | non-applicable | E01 | NR | not-required | `3b698dadebffd4686f67b0ab9e4fd4c161f75c65d6bdd305d8b02d29df16e78c` |
| PE-APPAUTH-001 | RF-36 | SF-12 | MAY | Every application | non-applicable | E01 | NR | not-required | `b778a2e60b751130cb224a2178c1212e2f93eb2791ff1772c0f06f3883ae34b0` |
| PE-APPAUTH-002 | RF-36 | SF-12 | MUST NOT | Every application policy or interpretation | non-applicable | E01 | NR | not-required | `7bdf0cb287abe46132a084dbb729e6da4b5157e5e5268ece81e2fe7462c2810c` |
| PE-APPAUTH-003 | RF-36 | SF-12 | MUST NOT | Every application and Application Request or Response | non-applicable | E01 | NR | not-required | `95cab340add71d40773ad7912f4887257c6974e32ddc2624e2c939d336457643` |
| PE-APPAUTH-004 | RF-36 | SF-12 | MUST | Every Application Adapter | non-applicable | E01 | NR | not-required | `24a0277b051643c5c93be8be15b3e19cd4406243e4a3036806e6b98667047eac` |
| PE-APPAUTH-005 | RF-36 | SF-12 | MUST NOT | Every Application Adapter | non-applicable | E01 | NR | not-required | `2dd63842180ec9c1f609e0d17b007a1be3e1368ecb3c7f4e17b8440785231e51` |
| PE-APPAUTH-006 | RF-36 | SF-12 | MUST | Every integrator | non-applicable | E01 | NR | not-required | `7bf4dca0c24bd9522740c35e4079465b328c68ee2d03f2efc00c3c438208c081` |
| PE-APPAUTH-007 | RF-36 | SF-12 | MUST NOT | Every integration | non-applicable | E01 | NR | not-required | `6d3c0b2328b46c655cf0b2533b7f63c1dbcbd938ea573b482c8774f15fc94cd0` |
| PE-APPAUTH-008 | RF-36 | SF-12 | MUST | Every adapter replacement or application-boundary change | non-applicable | E01 | NR | not-required | `2964534f575628eab8ac0f4339577245d6eb17dde5f1317905004be95be0054f` |
| PE-APPAUTH-009 | RF-36 | SF-12 | MUST NOT | Every application-side validation or default | non-applicable | E01 | NR | not-required | `0ca53022fd3d0fc2a21cc00bd23072971cf92b34883e5389859a6549cb94fded` |
| PE-APPAUTH-010 | RF-36 | SF-12 | MUST | Every application, adapter, and integration failure | non-applicable | E01 | NR | not-required | `3fd9f82090a33a4e8c1b9c05ddf30cb490a846cb52953ce571760fd45ea624ac` |
| PE-APPAUTH-011 | RF-36 | SF-12 | MUST NOT | Every application, adapter, integration record, or observability surface | non-applicable | E01 | NR | not-required | `fb7b4ecc8f6e292c3e9352390339f0f44e1f57d832335475a5f55d4a8922d0d9` |
| PE-APPAUTH-012 | RF-36 | SF-12 | MUST | Every public application, adapter, or integration identifier | non-applicable | E01 | NR | not-required | `3f4560467f5e1e0238569b52dd71c198d40a49c3d14acb5029a682f26f80ab53` |
| PE-RUNTIME-001 | RF-37 | SF-12 | MUST | Every Privacy Engine runtime | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `0075a8bb276d1c0983115b2454a0b46d38ddcb4d2bace207fb6fba6f1be44eca` |
| PE-RUNTIME-002 | RF-37 | SF-12 | MUST | Every identified runtime | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `83df9cfda4208fce54b2a8ca2211de68fd69aa4c4700b1c00e6c9dcdd47d8e91` |
| PE-RUNTIME-003 | RF-37 | SF-12 | MUST NOT | Every runtime | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `c02e7aaaa7b79955927e38d8a4abbc83343a4b84a71daa62f0b822b233293771` |
| PE-RUNTIME-004 | RF-37 | SF-12 | MUST | Every runtime using an implementation | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `7e31b67053a67b8ce19d2cc4b402dd55cece420f6f337880b5a5faa153bacde5` |
| PE-RUNTIME-005 | RF-37 | SF-12 | MAY | Every runtime | resolved through permitted specification choice | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | ambiguous | `377265f7be4ef67a7b2928748827dfa5836cf830f455b960a1441adb7f463e1e` |
| PE-RUNTIME-006 | RF-37 | SF-12 | MUST NOT | Every runtime orchestration path | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `f8af0e7179c06835f915ab018e31ad224005c3346dd59674387aeb042f592b84` |
| PE-RUNTIME-007 | RF-37 | SF-12 | MUST | Every Protocol Enforcement occurrence | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `37fb407782491cf4f449eb58e61368a19f1d616b72bda361815f52183a0a87d5` |
| PE-RUNTIME-008 | RF-37 | SF-12 | MUST NOT | Every Protocol Enforcement occurrence | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `994ad332b3fcd3537a8e5a985ba6be1db8d0684ee7557e2bf9ebfde192a699db` |
| PE-RUNTIME-009 | RF-37 | SF-12 | MUST NOT | Every Protocol Enforcement occurrence | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `074993c2fda79cc619b7f17a6fe2da70b57b2a98c39f0263fb34a334c31eb0a1` |
| PE-RUNTIME-010 | RF-37 | SF-12 | MUST | Every authorized transition execution | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `9d572de3b93f8072a251bd44fa97f6a635139c86fa11dd4595d412dbf97df00a` |
| PE-RUNTIME-011 | RF-37 | SF-12 | MUST NOT | Every transition execution | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `9fe2f98d669c38ab1b58134d8cf10b63f3ad8a31b25f97bce91da3161bd957de` |
| PE-RUNTIME-012 | RF-37 | SF-12 | MUST NOT | Every successful execution | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `996398ffe09239ee0051e2b0949838a3045be0a0c8ec11f67a97dd354724ea83` |
| PE-RUNTIME-013 | RF-37 | SF-12 | MUST | Every runtime result or failure report | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `68188c4b98eccd4c3ea15549e5a29c2157e83c1fb11edd1ac3c20cc1bae379df` |
| PE-RUNTIME-014 | RF-37 | SF-12 | MUST NOT | Every runtime or implementation failure | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `4cf4ead9e6c2930d35108a7584be37369310ba17221b2c0428b7329d562d91ce` |
| PE-RUNTIME-015 | RF-37 | SF-12 | MUST | Every runtime value, log, diagnostic, retry, timing, ordering, topology, and observability surface | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `f08a54ee544d60c9ea3cd8738955ea65316cc37afab64f354f416ba200f8070c` |
| PE-RUNTIME-016 | RF-37 | SF-12 | MUST NOT | Every runtime, enforcement mechanism, execution mechanism, and orchestrator | applicable | E09,E10,E11,E12,E14,E15,E18 | BD,TD,RG,DB,RO | bounded | `2c9f93f9ea85f91366c9874661637a1e65bb0e607f00d5c9c109ecb7969687ba` |
| PE-IMPL-001 | RF-38 | SF-13 | MUST | Every Privacy Engine implementation | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `b26fa880bf047d50d2b91aee437ea254c186c5bf18b2afcd6694bd1e93fd4436` |
| PE-IMPL-002 | RF-38 | SF-13 | MUST | Every implementation | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `7cdd92145f91f0bbb32b47d4c57d47991ca5cc93eec6f29567e1daa50ad81d6d` |
| PE-IMPL-003 | RF-38 | SF-13 | MUST | Every implementation | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `a3f9707c26af79f590450638ba32284cceaac6781f8149fe0532dd0e3401120c` |
| PE-IMPL-004 | RF-38 | SF-13 | MUST | Every materially changed implementation version | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `02e7a94367eb6fee7844ed3416bbc546466b51cd66f1b6ccd8531f222e476253` |
| PE-IMPL-005 | RF-38 | SF-13 | MAY | Every implementation | resolved through permitted specification choice | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | ambiguous | `936a5d3aa550b962011e9341acc77efa92fbdd746a4057664d998125b0ac0922` |
| PE-IMPL-006 | RF-38 | SF-13 | MUST | Every component used by an implementation | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `1e4004434c908146028529e6fef47ae283bd09ae6aa5d0adcae983081ddbbe24` |
| PE-IMPL-007 | RF-38 | SF-13 | MUST | Every implementation deployment or operational instance | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `545b59dcaa192a9f6797130ab0a47ec2350113deb26ecc69974e7d892ab8cbaa` |
| PE-IMPL-008 | RF-38 | SF-13 | MUST NOT | Every implementation identifier | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `14fa94236cbb7bb77ec29ddace2b3a9e482497d1289c3da8bf6c84fe37056d20` |
| PE-IMPL-009 | RF-38 | SF-13 | MUST | Every implementation | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `fdaea272a80028f05ec221c0b439c2b2a013e772b56ffc2a266c8792f2ff00ac` |
| PE-IMPL-010 | RF-38 | SF-13 | MUST | Every implementation claiming a requirement is non-applicable | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `91613591ecebe46f0f74625e3130bcb9eaf71c6fff85fc04c0a26b518354ba08` |
| PE-IMPL-011 | RF-38 | SF-13 | MAY | Every implementation-facing choice explicitly permitted by the applicable profile | resolved through permitted specification choice | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | ambiguous | `c2179ea54d1ea4b77dd2bd235a9f1246a6aff33df9f2e015c9d28e3d6f83950b` |
| PE-IMPL-012 | RF-38 | SF-13 | MUST NOT | Every implementation | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `af8b14ae5ce655bd40190fab1ec7fe343d4ecfb71945240eef5963fced75f675` |
| PE-IMPL-013 | RF-38 | SF-13 | MAY | Multiple implementations of the same applicable profile | resolved through permitted specification choice | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | ambiguous | `d86aa929f308116018735656a54bcb51c97d28e372f779a22f3ac631f8a62b85` |
| PE-IMPL-014 | RF-38 | SF-13 | MUST | Every permitted implementation variation | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `d655d5a31b8505cf71f545c2e8b99103ffddd40f7ed1242968b1c18e24642b4d` |
| PE-IMPL-015 | RF-38 | SF-13 | MUST | Every implementation failure | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `90fce123474fb59b3fe98fb4b2b4f2cb134dd4bbbfa13c28ac68113a90b28f71` |
| PE-IMPL-016 | RF-38 | SF-13 | MUST NOT | Every implementation name, identifier, version, component, deployment, instance, log, diagnostic, test, and observability surface | applicable | E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `023d72c0e2e1c47c783ef8253c9389733fdddf83d990cdb1765b1ee147b8897e` |
| PE-REALIZE-001 | RF-39 | SF-13 | MUST | Every claimed Protocol Realization | applicable | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `a36a6d7645f311d0ca838741e34671762db66a1608c74d2548afcd3db31f1a82` |
| PE-REALIZE-002 | RF-39 | SF-13 | MUST | Every Protocol Realization relationship | applicable | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `27483430e8a4f5b9e1bf6273cddfdff4bd256d6c6d58a8546392afc4f9aa3655` |
| PE-REALIZE-003 | RF-39 | SF-13 | MUST | Every implementation realizing an applicable requirement | applicable | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `10beae36426e3ce318bac0fbb400e00c68cd3976a9fc23c6af78b33cc93f161b` |
| PE-REALIZE-004 | RF-39 | SF-13 | MUST | Every successful realization of an upstream semantic subject | applicable | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `bcd0da1c96b09ff953ed4a3b271d992539f1f6995d544f932a980ac153d81931` |
| PE-REALIZE-005 | RF-39 | SF-13 | MUST | Every realization unable to preserve an applicable subject or requirement | applicable | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `7252f69fee80461345e47b3330d02cd1813aec59b1a801c90978d9a529bd9be5` |
| PE-REALIZE-006 | RF-39 | SF-13 | MUST NOT | Every Protocol Realization | applicable | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `bd434217b353570566b5135bdc221d2f2e6ffd4b3759964118b911c0f6d4823b` |
| PE-REALIZE-007 | RF-39 | SF-13 | MUST NOT | Every Protocol Realization | applicable | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `db190725a5cd88a6b3a77e8db5cb11e512cfe4ea9b8a10204fe86ba58c52785f` |
| PE-REALIZE-008 | RF-39 | SF-13 | MUST | Every complete realization claim | applicable | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `d7ad3d0f14838cfaba62789a16e1a885f4b427fc6cdea98737b3cade151c17dd` |
| PE-REALIZE-009 | RF-39 | SF-13 | MAY | Multiple realizations of the same applicable profile | resolved through permitted specification choice | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | ambiguous | `66a2a1593a001cb30076b6942ea7c9b82da5332d587673be298f7cb1cdb41b26` |
| PE-REALIZE-010 | RF-39 | SF-13 | MUST | Every realization-specific extension | applicable | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `6830028799a8d510ca806aa522f0c1ab3157a79fb29a923a7693c5338bd799c7` |
| PE-REALIZE-011 | RF-39 | SF-13 | MUST | Every realization record, report, or diagnostic | applicable | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `ab1f34fa59238fc88508e6217f1ec10c5a2c5082f1bc20b8b4bcb87f004340f6` |
| PE-REALIZE-012 | RF-39 | SF-13 | MUST NOT | Every implementation and realization | applicable | E01,E02,E03,E13,E14,E15,E18,E21 | BD,TD,RG,DB,RO | bounded | `30accfa510073f382572bd5d366aefd06750d684b0e2752047d896c998db3d11` |
| PE-DOWNAUTH-001 | RF-40 | SF-13 | MUST NOT | Every application, adapter, runtime, integration, implementation, realization, compatibility structure, profile, reference implementation, assessment, report, deployment, and operational surface | applicable | E01,E02,E03,E21 | BD,TD | bounded | `477f51aab37226f8053e46395498c4a0ef3e31364a3782d82b3896ba4a023ca7` |
| PE-DOWNAUTH-002 | RF-40 | SF-13 | MUST NOT | Every downstream structure or surface | applicable | E01,E02,E03,E21 | BD,TD | bounded | `15f4e90286a47103bcb7ae91f0f68e278b1d1203a8c0ed3c452ae9274e13b8c7` |
| PE-DOWNAUTH-003 | RF-40 | SF-13 | MUST NOT | Every downstream structure or surface | applicable | E01,E02,E03,E21 | BD,TD | bounded | `c450c47a9863782c74e5af811071809ab9247e5c0d435da0ea15e65fe2eb5030` |
| PE-DOWNAUTH-004 | RF-40 | SF-13 | MUST NOT | Every downstream structure or surface | applicable | E01,E02,E03,E21 | BD,TD | bounded | `711feabc98e7d4344e0811a3cebfc53d09b49a9e6d7e017c60db21b5310ad3cf` |
| PE-DOWNAUTH-005 | RF-40 | SF-13 | MUST NOT | Every downstream structure or surface | applicable | E01,E02,E03,E21 | BD,TD | bounded | `ff8b8a11dee5db5ed8125ca4abcfbd26c8d9f6c8580c96db01d3b831eca6bb04` |
| PE-DOWNAUTH-006 | RF-40 | SF-13 | MUST NOT | Every downstream structure or surface | applicable | E01,E02,E03,E21 | BD,TD | bounded | `a89e0668f8c29914d53371581fe7f92a9cf18c0e955a431d9b1ca7d54eda4f5e` |
| PE-DOWNAUTH-007 | RF-40 | SF-13 | MUST NOT | Every compatibility, profile, reference, conformance, or certification structure | applicable | E01,E02,E03,E21 | BD,TD | bounded | `ee029e44854df3620baf36f7ea7ed1d88e4bfb1871b13f934d25f0efafc1e897` |
| PE-DOWNAUTH-008 | RF-40 | SF-13 | MUST NOT | Every implementation behavior, compatibility declaration, assessment result, diagnostic, test result, deployment record, report, or observability surface | applicable | E01,E02,E03,E21 | BD,TD | bounded | `31c4d1aa8e6702b05e3e469c1c1ba5f2e1487453faab03fed09071d2f15879c1` |
| PE-DOWNAUTH-009 | RF-40 | SF-13 | MUST | Every conflict between a downstream artifact and its governing upstream requirement | applicable | E01,E02,E03,E21 | BD,TD | bounded | `9ea0301475237c6d1e8fdee137e79d4b8e5633b9e1beafd61485d9fe469702ab` |
| PE-DOWNAUTH-010 | RF-40 | SF-13 | MUST | Every downstream derivation and realization path | applicable | E01,E02,E03,E21 | BD,TD | bounded | `a37792c18fa09483e0bb63a29a56028d4742b9a291dad16489c8766236c41a64` |
| PE-COMPAT-001 | RF-41 | SF-13 | MUST | Every compatibility relationship | non-applicable | E01 | NR | not-required | `d736f337e72ddd48599507555f0c90a4c0eb2cbbcc9936c611d3d72b7a109736` |
| PE-COMPAT-002 | RF-41 | SF-13 | MUST | Every Compatibility Target | non-applicable | E01 | NR | not-required | `3f2dfd58c8bf6ba54277c70595b2be009d892143e7251ac387b43e082ebb3127` |
| PE-COMPAT-003 | RF-41 | SF-13 | MUST | Every identified Compatibility Target | non-applicable | E01 | NR | not-required | `ff00b39124b60596fb2c298e701e68604aa6bcbdbf407ff938892ca9132aa5aa` |
| PE-COMPAT-004 | RF-41 | SF-13 | MUST | Every Compatibility Surface | non-applicable | E01 | NR | not-required | `9848546a41de7f72ef71329fb4b03c389a248e2c183d8b0588167b21deec1955` |
| PE-COMPAT-005 | RF-41 | SF-13 | MUST | Every Compatibility Surface | non-applicable | E01 | NR | not-required | `fdca4d46c4b56b7478d90fbceaef41ff9431f3039c221a4be621337a496b0821` |
| PE-COMPAT-006 | RF-41 | SF-13 | MUST NOT | Every Compatibility Surface | non-applicable | E01 | NR | not-required | `fcc1da46614641adce2666414c613a14d3d133bd728b30c17be3e8f73a6647c6` |
| PE-COMPAT-007 | RF-41 | SF-13 | MUST | Every Compatibility Statement | non-applicable | E01 | NR | not-required | `b197e3a0f8d0926e23a3eb32a8b74536524b23c8fff01aeb1880ac046a7f79db` |
| PE-COMPAT-008 | RF-41 | SF-13 | MUST | Every Compatibility Statement | non-applicable | E01 | NR | not-required | `68daa76a5928011c721eb06342af55b1f9bae1c27173b6fb2121e24569648501` |
| PE-COMPAT-009 | RF-41 | SF-13 | MUST NOT | Every Compatibility Statement | non-applicable | E01 | NR | not-required | `3badbbf8a43c0791b97ae79833385a33ab4347b710e7863d2c1370e3ba7308a8` |
| PE-COMPAT-010 | RF-41 | SF-13 | MUST | Every Compatibility Profile | non-applicable | E01 | NR | not-required | `b7d042adac596ab4389e863b7123b82d70a9efd26190473f636f93d38cd6d8f3` |
| PE-COMPAT-011 | RF-41 | SF-13 | MUST | Every Compatibility Profile | non-applicable | E01 | NR | not-required | `1eeb9302a282288bab8eb792326bda7f542b30551ed1399f76614074c1d71a70` |
| PE-COMPAT-012 | RF-41 | SF-13 | MUST NOT | Every Compatibility Profile | non-applicable | E01 | NR | not-required | `f1f60f1e5d4cd4d571a27258a818b6ca40ef2f963c57015de47d5123a585d2fb` |
| PE-COMPAT-013 | RF-41 | SF-13 | MUST | Every Compatibility Declaration | non-applicable | E01 | NR | not-required | `921c2c69edbb335618b71ee6c23bdb9aeeae7a7fa7c9c0774456aab838e6cac0` |
| PE-COMPAT-014 | RF-41 | SF-13 | MUST | Every Compatibility Declaration | non-applicable | E01 | NR | not-required | `218b59d4739f15dca11449e9b3d3f910431ec560006dd69d44039e4926ebad5a` |
| PE-COMPAT-015 | RF-41 | SF-13 | MUST NOT | Every Compatibility Declaration | non-applicable | E01 | NR | not-required | `d4a0d5e5023c8af6d62498a57c4184fb8ed3b0faf1b584d77364dafdbb2c46b7` |
| PE-COMPAT-016 | RF-41 | SF-13 | MUST | Every Compatibility Assessment | non-applicable | E01 | NR | not-required | `f39d46e41f0064748bce62b969e27dfa833b336e3c430a00370a31aebd3bd321` |
| PE-COMPAT-017 | RF-41 | SF-13 | MUST | Every Compatibility Assessment report | non-applicable | E01 | NR | not-required | `a454983e5e908d49664178334d534cb27bd33a0edbc29f0b462835c92cce4ebe` |
| PE-COMPAT-018 | RF-41 | SF-13 | MUST | Every compatibility target, surface, statement, profile, declaration, and assessment | non-applicable | E01 | NR | not-required | `a6690c2fea38275e17c9691e3aed7b0b7d534d0ed9b661916bc96cace8f4f4c1` |
| PE-COMPAT-019 | RF-41 | SF-13 | MUST NOT | Every compatibility claim or assessment | non-applicable | E01 | NR | not-required | `f8a63c93d8a86d3a1d2790834a7379cd0d6ae0dea1a5a4cc93d595d5e66d1a6f` |
| PE-COMPAT-020 | RF-41 | SF-13 | MUST NOT | Every compatibility claim or assessment | non-applicable | E01 | NR | not-required | `b3a4b647ce9fa6c12cf6206f20b88071a246485b8f778adda2b594f5aa2654e9` |
| PE-COMPAT-021 | RF-41 | SF-13 | MUST NOT | Every compatibility structure or assessment | non-applicable | E01 | NR | not-required | `a80317699e11bc0192493fca19279b7a1bd70c6bbb9dfd562738e1beb0a8eabb` |
| PE-COMPAT-022 | RF-41 | SF-13 | MUST | Every compatibility consequence of protocol evolution or migration | non-applicable | E01 | NR | not-required | `b5848b235b8027e6a62b886dcbc5548c76183d95dd0107153649fe4a9330817c` |
| PE-COMPAT-023 | RF-41 | SF-13 | MUST | Every failed, superseded, withdrawn, or historically retained compatibility statement, declaration, or assessment | non-applicable | E01 | NR | not-required | `cc800c779c9aefc49256cfcc5f8f46fc720a10b53eb0491bf56524d309b4bd60` |
| PE-COMPAT-024 | RF-41 | SF-13 | MUST NOT | Every compatibility identifier, statement, declaration, assessment, field, diagnostic, test, report, and observability surface | non-applicable | E01 | NR | not-required | `57491414732fa0214024070bdd74283c22bd170763e983d5c7650fa03c0d5f8b` |
| PE-PROFILE-001 | RF-42 | SF-14 | MUST | Every Privacy Engine Implementation Profile | applicable | E01 | BD | bounded | `2d5bd7fa0c523dcff561f153b46967be5b7e3b524e226cf23c3af1814fc1e60d` |
| PE-PROFILE-002 | RF-42 | SF-14 | MUST | Every Implementation Profile | applicable | E01 | BD | bounded | `cc8f2e85add983b05104f5612b7d5d542b485b768a7b8b9cf99c82d2c6cfbe66` |
| PE-PROFILE-003 | RF-42 | SF-14 | MUST | Every Implementation Profile | applicable | E01 | BD | bounded | `146d8a72b88459b4e596103a6c955f81116e2c4fe39c052d8eac9f44a5448c0f` |
| PE-PROFILE-004 | RF-42 | SF-14 | MUST | Every Implementation Profile | applicable | E01 | BD | bounded | `387d29df957c5bae1d133fab6cc9006ec33f6837cbfac4b8a755d9d080510e94` |
| PE-PROFILE-005 | RF-42 | SF-14 | MUST | Every Implementation Profile | applicable | E01 | BD | bounded | `39ff99689a718b12b77c74810a6aed54677ffdb8b1427ce7e3bed9046bdf27f3` |
| PE-PROFILE-006 | RF-42 | SF-14 | MUST | Every requirement relevant to an Implementation Profile target | applicable | E01 | BD | bounded | `985e9e89435081fb61ccaf19e885d10005149eeb37cb0ee692e627cf33422eee` |
| PE-PROFILE-007 | RF-42 | SF-14 | MUST NOT | Every Implementation Profile applicability decision | applicable | E01 | BD | bounded | `68bbdd155dc6673e849f0d489d02cfe889c2fbf94f3a0e4ea2d0e36c8ff57e3e` |
| PE-PROFILE-008 | RF-42 | SF-14 | MUST | Every requirement selected by an Implementation Profile | applicable | E01 | BD | bounded | `650349215899b85d72c336cfe171c71392865e118870d0b7110c120541f08b85` |
| PE-PROFILE-009 | RF-42 | SF-14 | MUST | Every applicable requirement in an Implementation Profile | applicable | E01 | BD | bounded | `b26d8e873915c51aa661803cfe18fae8ce9dc87fe071f2ee10eb5d57a5791c1b` |
| PE-PROFILE-010 | RF-42 | SF-14 | MAY | Every choice explicitly permitted by the source Protocol Specification | applicable | E01 | BD | bounded | `fbcc7cb65bdc72ab0b600230c0fed7c833240dc64f3759ab44c7d285c83ab88e` |
| PE-PROFILE-011 | RF-42 | SF-14 | MUST NOT | Every Implementation Profile | applicable | E01 | BD | bounded | `cc67c8b2cf4fec752ef208ae944563f738e16bcb5ab19c7acfbab21d3e93d33d` |
| PE-PROFILE-012 | RF-42 | SF-14 | MUST | Every Implementation Profile composition | applicable | E01 | BD | bounded | `f363fdb56ee74163d8c9f4d2b1ef4a30e66527bab9ce03375bdf43ec9cd9dd8d` |
| PE-PROFILE-013 | RF-42 | SF-14 | MUST | Every Implementation Profile dependency | non-applicable | E01 | NR | not-required | `309045f3c62a09977be3b09e64f5008e3831e2f87f7a5203c3660d8865d1d71e` |
| PE-PROFILE-014 | RF-42 | SF-14 | MUST | Every Implementation Profile | applicable | E01 | BD | bounded | `d8d2ed02747d961621de93e4f6c6704e80c6872ef4987859ecfb6a5d1db80ddb` |
| PE-PROFILE-015 | RF-42 | SF-14 | MUST | Every semantically changed Implementation Profile | applicable | E01 | BD | bounded | `ceedb98497ece2841c98c48a88abace0988d046a304fd1f78a951d26aa1556bd` |
| PE-PROFILE-016 | RF-42 | SF-14 | MAY | One Protocol Specification | applicable | E01 | BD | bounded | `22e67d68ba2dde2ed78a6d443c7652cab0a17ca50d133c80e02a4d3dceefd8f3` |
| PE-PROFILE-017 | RF-42 | SF-14 | MUST NOT | Every Implementation Profile | applicable | E01 | BD | bounded | `4011c78d579aece1e40176d2247bf3e21ea37c14823c7e8bef3329fc1db9e376` |
| PE-PROFILE-018 | RF-42 | SF-14 | MUST NOT | Every Implementation Profile | applicable | E01 | BD | bounded | `6241d8ba925a69090e1da91e5d405dbf9f41ccf5deabc757c41d62d07e35471c` |
| PE-PROFILE-019 | RF-42 | SF-14 | MUST NOT | Every incomplete Protocol Specification | non-applicable | E01 | NR | not-required | `6ec35e69b3a4d1f0984ef9bc460ee876f85e136de482f0a27cd4b6e4f21b7d18` |
| PE-PROFILE-020 | RF-42 | SF-14 | MUST | Every profile construction or preservation failure | applicable | E01 | BD | bounded | `85844d7fa19360b693d0c915944429ef805c4a4dc75a9482745fc8dcce8af748` |
| PE-PROFILE-021 | RF-42 | SF-14 | MUST NOT | Every profile identifier, applicability record, choice record, dependency, report, example, diagnostic, and observability surface | applicable | E01 | BD | bounded | `ab5f517aa03e4b882945cfde9638985ffb0a4757723491b02abc50ddabf94d57` |
| PE-REFIMPL-001 | RF-43 | SF-14 | MUST | Every Privacy Engine Reference Implementation | non-applicable | E01 | NR | not-required | `c9199b610aca247bdc13c2454b4f174aaa15a25eb08c1b4a8f71421dc312810e` |
| PE-REFIMPL-002 | RF-43 | SF-14 | MUST | Every Reference Implementation | non-applicable | E01 | NR | not-required | `767adbbe8dc1e06aa98d97beee03129728323fcbf70e5f0a61a149477b09bc7d` |
| PE-REFIMPL-003 | RF-43 | SF-14 | MUST | Every reference designation | non-applicable | E01 | NR | not-required | `a7f0ad4fdd4d6e326d7e512608adcb31f0764fe316708a863bda07d0d5aeb6cc` |
| PE-REFIMPL-004 | RF-43 | SF-14 | MUST NOT | Every reference designation | non-applicable | E01 | NR | not-required | `538b8fe2933d8fa58e898cd804142f2933b328f028c507de9387da4e7381bc7f` |
| PE-REFIMPL-005 | RF-43 | SF-14 | MUST | Every Reference Implementation | non-applicable | E01 | NR | not-required | `0f1fa892f5fdfed37bbb51dcf7cb8d065a7d2f75d222124a36967f07ed7f6d89` |
| PE-REFIMPL-006 | RF-43 | SF-14 | MUST | Every Reference Implementation realizing an Implementation Profile | non-applicable | E01 | NR | not-required | `7660d23b43e7e1b74a9a9f1d6c2fa6dcd751ca0cbb193cb646f1ffcb0d97cd5f` |
| PE-REFIMPL-007 | RF-43 | SF-14 | MUST | Every Reference Implementation | non-applicable | E01 | NR | not-required | `ea705c4f62cbf8ebfa9322df823331b6aeebda2cf00b7f3b856b7cd84af1bd6a` |
| PE-REFIMPL-008 | RF-43 | SF-14 | MAY | Every Reference Implementation | non-applicable | E01 | NR | not-required | `43df395d8bea1819e6c576597b0463df7f4f7bff4ec72ed8a23ff572885bf919` |
| PE-REFIMPL-009 | RF-43 | SF-14 | MUST NOT | Every implementation choice selected by a Reference Implementation | non-applicable | E01 | NR | not-required | `6ff4ff51e5304a470540ec63d2da9bab9290c9986505d264978dfff33e1791b7` |
| PE-REFIMPL-010 | RF-43 | SF-14 | MAY | One Implementation Profile | non-applicable | E01 | NR | not-required | `a3d2097f0a16074089ab3cae83c2a576d9410b572830f783be7c07d8dedd2ddd` |
| PE-REFIMPL-011 | RF-43 | SF-14 | MAY | One implementation realizing multiple Implementation Profiles | non-applicable | E01 | NR | not-required | `f36e75697babc4d858ff18e62209ddeb8d0f9974ef27b4984149dce023eaa6ac` |
| PE-REFIMPL-012 | RF-43 | SF-14 | MUST | Every materially changed Reference Implementation version | non-applicable | E01 | NR | not-required | `b4386c00185f36d755c26f84914377952133bf2f729b7b5053db3a6170f2aca3` |
| PE-REFIMPL-013 | RF-43 | SF-14 | MUST | Every maintained Reference Implementation version | non-applicable | E01 | NR | not-required | `2342781c4ae3abff5bddd7f13ddeb9979a7907808d8711e59b717523ddabd188` |
| PE-REFIMPL-014 | RF-43 | SF-14 | MUST | Every detected Reference Implementation defect or divergence | non-applicable | E01 | NR | not-required | `dd3a607432c73a10ce47d94843e48f40810565d40b32d24debd2549b963b72e6` |
| PE-REFIMPL-015 | RF-43 | SF-14 | MUST | Every Reference Implementation unable to preserve an applicable obligation | non-applicable | E01 | NR | not-required | `ea70c1e3e19eef35f34efaf43d42f767911b45663fc0953f6ad318e5269b90dd` |
| PE-REFIMPL-016 | RF-43 | SF-14 | MUST | Every ordinary implementation compared with a Reference Implementation | non-applicable | E01 | NR | not-required | `4b108119727c3e5e6c48c371e4693d1f55455fddc043e81fde9fbe8bea01d711` |
| PE-REFIMPL-017 | RF-43 | SF-14 | MUST NOT | Every ordinary implementation | applicable | E01,E02,E17,E21 | BD,TD | bounded | `8801703bc997dbe4e7c5414c065b779d0bf7ffef564e26825d950d9ad38c777a` |
| PE-REFIMPL-018 | RF-43 | SF-14 | MAY | Every conformance, certification, compatibility, testing, or interoperability activity | non-applicable | E01 | NR | not-required | `d8493ef5e9fc614df235e5fba2725f70246370b00b6fdb545434b5c7ccd7b014` |
| PE-REFIMPL-019 | RF-43 | SF-14 | MUST NOT | Every conformance, certification, or compatibility activity using a Reference Implementation | non-applicable | E01 | NR | not-required | `2ebce1e012ba2bb07c323dd146f82d66b2bd137f53b1d8f6e6b69ce02ef6685c` |
| PE-REFIMPL-020 | RF-43 | SF-14 | MUST | Every disagreement between a Reference Implementation and an upstream requirement | non-applicable | E01 | NR | not-required | `bb23a15091ca75cca37624ff6f00f655760f57495235962472148ad0d180bb0c` |
| PE-REFIMPL-021 | RF-43 | SF-14 | MUST NOT | Every reference identifier, designation, implementation record, version, test, diagnostic, report, log, and observability surface | non-applicable | E01 | NR | not-required | `2f43a1ffb7fca8d1baf599f15b106ffe68ae115c4ad294e2ee32e3eb4ed7529b` |
| PE-CONFREQ-001 | RF-44 | SF-15 | MUST | Every Published Conformance Requirement | non-applicable | E01 | NR | not-required | `ae11af10de70abcccd87851d2d70d99078e08ee37d6a2cb2f2a648b4da98dbe2` |
| PE-CONFREQ-002 | RF-44 | SF-15 | MUST | Every Published Conformance Requirement | non-applicable | E01 | NR | not-required | `af8060a177d2b9733bb69ab1eb056eed2b42592a2c7c886c8d41d16503dfb903` |
| PE-CONFREQ-003 | RF-44 | SF-15 | MUST | Every Published Conformance Requirement | non-applicable | E01 | NR | not-required | `8f79b98f1cbc52d1290ec15b0c1818c6899db68bff58909d2e3ab9e4550cff5e` |
| PE-CONFREQ-004 | RF-44 | SF-15 | MUST | Every conformance derivation | non-applicable | E01 | NR | not-required | `ee4fee1b80c5d6e33729a14b0c1a723fef55ea25742acdfb04a421c457ab1dd8` |
| PE-CONFREQ-005 | RF-44 | SF-15 | MUST | Every conformance derivation | non-applicable | E01 | NR | not-required | `40e7491a3cb3892fecf7ea29f76409a8024125b949726f0791977aeebeea3ac3` |
| PE-CONFREQ-006 | RF-44 | SF-15 | MUST NOT | Every Published Conformance Requirement | non-applicable | E01 | NR | not-required | `b6aba3b640e08bd5a9d8d96abd8feb473ba900bdab09664de533019a96163c29` |
| PE-CONFREQ-007 | RF-44 | SF-15 | MUST | Every published Conformance Requirement | non-applicable | E01 | NR | not-required | `9f53e459126e057f5d5b7fbe34b4e263453b0136b8bb57440551307c198cc917` |
| PE-CONFREQ-008 | RF-44 | SF-15 | MUST | Every published Conformance Requirement | non-applicable | E01 | NR | not-required | `503c087e144c4fb3bbb410f7a41043ce352d44e72dc37a58537b663869d0fcbe` |
| PE-CONFREQ-009 | RF-44 | SF-15 | MUST | Every Published Conformance Requirement Set | non-applicable | E01 | NR | not-required | `8a5add41d161f66b35cc80328f028c62c1cbb1ff0c9f1a7e498dda12c01e8923` |
| PE-CONFREQ-010 | RF-44 | SF-15 | MUST | Every Conformance Requirement Set | non-applicable | E01 | NR | not-required | `5b267a932f2d9dcc8c1c44cca5f3d394f1918aaad74090b48da27231ca4f7b3b` |
| PE-CONFREQ-011 | RF-44 | SF-15 | MUST | Every Conformance Requirement Set | non-applicable | E01 | NR | not-required | `6dea50919655246a1c8b67e5576fae914bbbd0fbb0cdb16e99b2eaf81548fbd8` |
| PE-CONFREQ-012 | RF-44 | SF-15 | MUST | Every complete Conformance Requirement Set | non-applicable | E01 | NR | not-required | `62ece37450a4d4400df89da5f78484bb4aaabc3419ecc643b66b8a643012f531` |
| PE-CONFREQ-013 | RF-44 | SF-15 | MUST | Every Conformance Requirement Set constituent | non-applicable | E01 | NR | not-required | `97de3293763f2456ea66c01e72fa5021ea2d9bcb229ee9c4aa08813340afd6eb` |
| PE-CONFREQ-014 | RF-44 | SF-15 | MUST NOT | Every Conformance Requirement Set | non-applicable | E01 | NR | not-required | `3c458581c62a31b0bbc04881b21ed56bed87e5d6c43d8166d0842bdc973140c3` |
| PE-CONFEVID-001 | RF-45 | SF-15 | MUST | Every Conformance Artifact | non-applicable | E01 | NR | not-required | `15530bd7fcf81c666347854eb60243adb20acb0ecdaecd44e5c6bfb9461bf53a` |
| PE-CONFEVID-002 | RF-45 | SF-15 | MUST | Every Conformance Artifact | non-applicable | E01 | NR | not-required | `b7ac6de2b103ba07783bf12325994bf2b2d58ef94c2ac2e265d9258908213438` |
| PE-CONFEVID-003 | RF-45 | SF-15 | MUST | Every Conformance Artifact | non-applicable | E01 | NR | not-required | `d2d7f88b065846286ca435fc9915a9ff8987828ad636bab1ab71fc0d18eea1a6` |
| PE-CONFEVID-004 | RF-45 | SF-15 | MUST | Every Conformance Artifact | non-applicable | E01 | NR | not-required | `80bb968d19cf6c0756a69c3d0f994b044b4afeceaf2c09debb5288e9cfc57dd5` |
| PE-CONFEVID-005 | RF-45 | SF-15 | MUST | Every artifact used as evidence | non-applicable | E01 | NR | not-required | `6db7254e7b10b4efd1a9680737d2030a851e702d2ac8b279a802d2883588cb69` |
| PE-CONFEVID-006 | RF-45 | SF-15 | MUST NOT | Every Conformance Artifact | non-applicable | E01 | NR | not-required | `5acc6daffede6e0a6a41fec16c902fc70cbb32e55e59d35d9d763c607e3534a4` |
| PE-CONFEVID-007 | RF-45 | SF-15 | MUST | Every Conformance Evidence set | non-applicable | E01 | NR | not-required | `3fb6c7b2fdcb776ca9979d9d9c3f47f663292541ef791c4d9dd1ac73823f47ed` |
| PE-CONFEVID-008 | RF-45 | SF-15 | MUST | Every Conformance Evidence set | non-applicable | E01 | NR | not-required | `0de4431445a8dac97aa08cea1426201f109173498077800310344ad19b6cd717` |
| PE-CONFEVID-009 | RF-45 | SF-15 | MUST | Every evidence constituent | non-applicable | E01 | NR | not-required | `72fd7608ef5b90c83b34d87622caa8f9faaca9b703b7073e95a36a93f533d37d` |
| PE-CONFEVID-010 | RF-45 | SF-15 | MUST | Every complete Conformance Evidence set | non-applicable | E01 | NR | not-required | `b47f06225815b8ae2dd13b36e176c21434bf78e8a488264b9c961a685c9c29a4` |
| PE-CONFEVID-011 | RF-45 | SF-15 | MAY | Every Conformance Evidence set | non-applicable | E01 | NR | not-required | `a6e6166d8d7ce619d233f601fe47ca455fa1577ba7702c12de0a0c731b446822` |
| PE-CONFEVID-012 | RF-45 | SF-15 | MUST NOT | Every Conformance Evidence set | non-applicable | E01 | NR | not-required | `4e2326b3dcfc6f843a759e8526b03127336df00007f7fdb9695a912cd2294b21` |
| PE-CONFEVID-013 | RF-45 | SF-15 | MUST | Every Conformance Package | non-applicable | E01 | NR | not-required | `448888e6afdba501b13c9a06891b45897418290cf949fc4f0f94b4c721795770` |
| PE-CONFEVID-014 | RF-45 | SF-15 | MUST | Every Conformance Package | non-applicable | E01 | NR | not-required | `254abf2b30891c82de88210fcb6e7e16dbf8cc26818e4241c22911f82df3dbcd` |
| PE-CONFEVID-015 | RF-45 | SF-15 | MUST | Every Conformance Package | non-applicable | E01 | NR | not-required | `b82ae34c6dd271dd1d52a4ea307a84632c9d4aef137c5621e101fd5003d039d6` |
| PE-CONFEVID-016 | RF-45 | SF-15 | MUST | Every published Conformance Package | non-applicable | E01 | NR | not-required | `45b6694ba06aa9288ab31ea53faf80a4a02d02984dbd1685f3bb75cb70586db4` |
| PE-CONFEVID-017 | RF-45 | SF-15 | MUST | Every Conformance Package constituent | non-applicable | E01 | NR | not-required | `b9774de81bcfa12886fda8c0184a2600c80e55436358629cd41b46bcb6fbb33d` |
| PE-CONFEVID-018 | RF-45 | SF-15 | MUST NOT | Every Conformance Package | non-applicable | E01 | NR | not-required | `544f234253dbc50e1a50ad747d0bbc44723d8d0fc5fa038acb60635ad4507be4` |
| PE-CONFEVID-019 | RF-45 | SF-15 | MUST NOT | Every Conformance Package | non-applicable | E01 | NR | not-required | `5d76ee6bacec35a00739ced6852f5a840b048cab4238a248757e273df4202a2e` |
| PE-CONFORM-001 | RF-46 | SF-15 | MUST | Every Conformance Claim | non-applicable | E01 | NR | not-required | `365e4fb5a5136cb96660c7e837e9e9817121785c2a461a1b03b25d86d0030bd4` |
| PE-CONFORM-002 | RF-46 | SF-15 | MUST | Every Conformance Claim | non-applicable | E01 | NR | not-required | `3d8e3fa01d2600bf30068300f297d96de61d38bb187fd0f1ed4cbfa189744cd1` |
| PE-CONFORM-003 | RF-46 | SF-15 | MUST | Every Conformance Claim | non-applicable | E01 | NR | not-required | `d528eb34e338c95cf8ee8029d4728e4033b26677da86c0c8db62f7432beb6984` |
| PE-CONFORM-004 | RF-46 | SF-15 | MUST | Every Conformance Claim | non-applicable | E01 | NR | not-required | `3c9a180a5baaac9d1f0c9c9027fa6c5611f49bcf7db1addc66c89cefa71982fb` |
| PE-CONFORM-005 | RF-46 | SF-15 | MUST NOT | Every Conformance Claim | non-applicable | E01 | NR | not-required | `851ec6d9de615048fec0d7850b48a7b710974e0b413f72c46a6e6ca0c9b9487a` |
| PE-CONFORM-006 | RF-46 | SF-15 | MUST NOT | Every Conformance Claim | non-applicable | E01 | NR | not-required | `bcfc2fa6b39a48c6522672f63b490d8c77b3488928313828611aac6a4c6fd281` |
| PE-CONFORM-007 | RF-46 | SF-15 | MUST | Every Conformance Assessment | non-applicable | E01 | NR | not-required | `a57a32b648b6c7a33667c0e0ca7cf6784a99235e88909b8c93299083961ab18f` |
| PE-CONFORM-008 | RF-46 | SF-15 | MUST | Every Conformance Assessment | non-applicable | E01 | NR | not-required | `0f11a8ca96b3edf60987c183fc7c5121c36d316d4dca6abe16f448f925b0afb0` |
| PE-CONFORM-009 | RF-46 | SF-15 | MUST | Every Conformance Assessment | non-applicable | E01 | NR | not-required | `01833f35dced259e025c5c5d43c6647b377c2990ff86ae194857d7851dfa3906` |
| PE-CONFORM-010 | RF-46 | SF-15 | MUST | Every complete Conformance Assessment | non-applicable | E01 | NR | not-required | `3bf8f92b9566cf224035cb90e7e3c5b85a8218508b984fa57f90bf607ba73d60` |
| PE-CONFORM-011 | RF-46 | SF-15 | MUST | Every Conformance Assessment | non-applicable | E01 | NR | not-required | `95638869bb767423e0cc17f6081f3340ce33e5df92820d9fd28f9f8347a1d95b` |
| PE-CONFORM-012 | RF-46 | SF-15 | MUST | Every Conformance Assessment | non-applicable | E01 | NR | not-required | `fea6cbb6b8d553b235ac7a25a116f0aeeda16d334710fc23b381f2867f2b5d51` |
| PE-CONFORM-013 | RF-46 | SF-15 | MUST | Every completed Conformance Assessment | non-applicable | E01 | NR | not-required | `313ea7715c78973e2a2c6d597440064730be2813b5e96af2191adc20da64f6df` |
| PE-CONFORM-014 | RF-46 | SF-15 | MUST | Every assessment unable to reach a supported classification | non-applicable | E01 | NR | not-required | `c5214ad8efbfe0ec3f9e17becb3c1f78a47a012d5493a6d5ddb427976661fadb` |
| PE-CONFORM-015 | RF-46 | SF-15 | MUST | Every Conformance Determination | non-applicable | E01 | NR | not-required | `1479439ffe242686f0428b876bef98c883ffc912acdfedd6643988868d6bb273` |
| PE-CONFORM-016 | RF-46 | SF-15 | MUST | Every Conformance Determination | non-applicable | E01 | NR | not-required | `cca34a553a5542923febe6b6b3bafa61154a1dcc589d14363d3682c7a9e221b3` |
| PE-CONFORM-017 | RF-46 | SF-15 | MUST | Every conformant determination | non-applicable | E01 | NR | not-required | `a225af9665b1e60f1e709ba1c793379665516d5f3ee6409cbc7eb4715ae040ac` |
| PE-CONFORM-018 | RF-46 | SF-15 | MUST | Every non-conformant determination | non-applicable | E01 | NR | not-required | `b12b82db45d38708b69dbf101e55a7f18ede2f9984d6895cefaf463221cc115d` |
| PE-CONFORM-019 | RF-46 | SF-15 | MUST | Every Conformance Determination | non-applicable | E01 | NR | not-required | `65fb68f003446fb4b3371f0ded1c48d8a9deca94d1a8a05a8d038996d02f6de1` |
| PE-CONFORM-020 | RF-46 | SF-15 | MUST | Every Conformance Determination | non-applicable | E01 | NR | not-required | `8fda90430388877c72cd6c331e6cd4c38b0f8a89513dafee4538e08ce1191961` |
| PE-CONFORM-021 | RF-46 | SF-15 | MUST NOT | Every partial Conformance Assessment | non-applicable | E01 | NR | not-required | `10b99f23ddceb6749e7570f980fe7b6d3f5d8aafd1ab30f549385381690e97ee` |
| PE-CONFORM-022 | RF-46 | SF-15 | MUST | Every published Conformance Determination | non-applicable | E01 | NR | not-required | `1d21720923e9d4f8ac150e0729834a52695bd5f180e7ae84bfbefb5bd3c8fe54` |
| PE-CONFORM-023 | RF-46 | SF-15 | MUST | Every correction affecting previous conformance | non-applicable | E01 | NR | not-required | `23888ae925c6d978ea3f3179c65ef62b9e763aa4e38b47de927a510e36b39221` |
| PE-CONFORM-024 | RF-46 | SF-15 | MUST | Every conformance or compatibility activity | non-applicable | E01 | NR | not-required | `02f0233e529f36ff68590eb453737751ab6396ee0b22aa34fad4f904d4c18466` |
| PE-CONFORM-025 | RF-46 | SF-15 | MUST | Every conformance or certification activity | non-applicable | E01 | NR | not-required | `491da98657df59198535c787b72e5ab0ec9006a4fd3007221520dc81bde0a0d4` |
| PE-CONFORM-026 | RF-46 | SF-15 | MUST | Every conformance authority | non-applicable | E01 | NR | not-required | `64bdc5b3e392ef1686e5e05529785b1c84e337a3868dd9211ce75f0d0df176f1` |
| PE-CONFORM-027 | RF-46 | SF-15 | MUST NOT | Every claim, assessment, determination, evidence object, report, test, diagnostic, identifier, and metadata surface | non-applicable | E01 | NR | not-required | `25444a2dfce8102d28feee4fdc4ccd42d62cc49d08147dfdaf9db0d2db21b1fc` |
| PE-CERTDET-001 | RF-47 | SF-15 | MUST | Every Certification Basis | non-applicable | E01 | NR | not-required | `03603b8e86f80220694cc294ad5df49530ba5dc73098f3a63221a6239fc7d57d` |
| PE-CERTDET-002 | RF-47 | SF-15 | MUST | Every Certification Basis | non-applicable | E01 | NR | not-required | `a7b33349d010d80fe44073f621d31273ef0dd45bfa5dd01c38a180225e74f879` |
| PE-CERTDET-003 | RF-47 | SF-15 | MUST | Every complete Certification Basis | non-applicable | E01 | NR | not-required | `fb48f02d926af2c1ba2e11d876a2cc9415b247a636ab0cf126f976291d02b9ba` |
| PE-CERTDET-004 | RF-47 | SF-15 | MUST | Every published Certification Basis | non-applicable | E01 | NR | not-required | `f0cee86c3eb139ec5f65ce4bafd4bb363ab90f75e54434a39df477dc8c5016b4` |
| PE-CERTDET-005 | RF-47 | SF-15 | MUST | Every Certification Basis | non-applicable | E01 | NR | not-required | `b2c4f12f5e13ea4024725480011705d9f7fd3a446832198272f4e11701c7a959` |
| PE-CERTDET-006 | RF-47 | SF-15 | MUST NOT | Every Certification Basis | non-applicable | E01 | NR | not-required | `f01f50abeba0078d3358721f3fee347ae7ae08268e9d4752fcaee358fea2bda6` |
| PE-CERTDET-007 | RF-47 | SF-15 | MUST | Every Certification Decision | non-applicable | E01 | NR | not-required | `ce548f39f002ef09e6e5a3ed11e323c74951d4945b2173aba087aed41818810f` |
| PE-CERTDET-008 | RF-47 | SF-15 | MUST | Every Certification Decision | non-applicable | E01 | NR | not-required | `af06f6dbc881c09f321d701f73e495b976c029e14894c30880daa99236740b1e` |
| PE-CERTDET-009 | RF-47 | SF-15 | MUST | Every passing Certification Decision | non-applicable | E01 | NR | not-required | `8b9b8d308bd60556bf5870a3bf96e20bc33de2fab5e33888774457b400794bfd` |
| PE-CERTDET-010 | RF-47 | SF-15 | MUST | Every failing Certification Decision | non-applicable | E01 | NR | not-required | `c523bfddf03e6fa660cc120cc23a149a04c3cdc5e9496dd0d69225133aae5401` |
| PE-CERTDET-011 | RF-47 | SF-15 | MUST | Every Certification Decision | non-applicable | E01 | NR | not-required | `ce7d095c19b81d48b3fec4c2539cb8a881613d4a29f722ca72bef54ef6197a6d` |
| PE-CERTDET-012 | RF-47 | SF-15 | MUST | Every Certification Decision | non-applicable | E01 | NR | not-required | `66105a15db25d8fde6c311799584f061428b86c44c3cd4dd6f8326e3b6385542` |
| PE-CERTDET-013 | RF-47 | SF-15 | MUST NOT | Every Certification Decision | non-applicable | E01 | NR | not-required | `553dac6f2245077b2ca686393b10558ef3e281c0aa6af447b8d8274914456f40` |
| PE-CERTDET-014 | RF-47 | SF-15 | MUST | Every Certification Status | non-applicable | E01 | NR | not-required | `80633629003a3068e31daffdf36ccc06a6f17cd78ec25fc0002afd7665b6235d` |
| PE-CERTDET-015 | RF-47 | SF-15 | MUST | Every Certification Status | non-applicable | E01 | NR | not-required | `03eb6f90f652d8d8fb02ec4c87acb2c5ec0ba015c185df307cd25b4e5265413f` |
| PE-CERTDET-016 | RF-47 | SF-15 | MUST | Every certification lifecycle change | non-applicable | E01 | NR | not-required | `218d89c603b7d5739a4c308a1bb42073c6a4708d7d3d03695e1d80adf9df7f75` |
| PE-CERTDET-017 | RF-47 | SF-15 | MUST | Every Certification Status | non-applicable | E01 | NR | not-required | `f002a37556be7cbe4a2772d5089b223b635b2436573a6fa5fd27cfec9d7df74c` |
| PE-CERTDET-018 | RF-47 | SF-15 | MUST NOT | Every Certification Status | non-applicable | E01 | NR | not-required | `5224847ab309f39fa92120634a6937e15f365695bf179855a6889445fa41ecec` |
| PE-CERTDET-019 | RF-47 | SF-15 | MUST | Every certification lifecycle update | non-applicable | E01 | NR | not-required | `09140eb8a96ffae67c86c5f0f17aac2f21b56f5539ac5b5829e741056000462d` |
| PE-CERT-001 | RF-48 | SF-15 | MUST | Every Privacy Engine Certification | non-applicable | E01 | NR | not-required | `9d4a52787b15333344e683c9c4aae2f069feeb81e8f48e386dffc362e5a2f1c9` |
| PE-CERT-002 | RF-48 | SF-15 | MUST | Every Certification | non-applicable | E01 | NR | not-required | `dc7e629584732324be02b75da88902f21fb109ebbe873b96ad5b8ba43b63b709` |
| PE-CERT-003 | RF-48 | SF-15 | MUST | Every Certification | non-applicable | E01 | NR | not-required | `e35638f91ea6793bc19844b93fea0b47fd3bdcc11f9b64d258f44cb7fb978204` |
| PE-CERT-004 | RF-48 | SF-15 | MUST | Every Certification | non-applicable | E01 | NR | not-required | `f0ebe8b82915d86c8b9cafa688f0e991578f74625dbbdcc3cb821f2b9bb372f1` |
| PE-CERT-005 | RF-48 | SF-15 | MUST | Every Certification | non-applicable | E01 | NR | not-required | `2a4270aeac749a66043df5c4906659092c85b979206fbc88d9be50392841e27b` |
| PE-CERT-006 | RF-48 | SF-15 | MUST | Every Certification | non-applicable | E01 | NR | not-required | `0f9b3f88227ad61282e2d0ad16c6a7b52c54fa1553dd01f6f41eb9e5b28f11fe` |
| PE-CERT-007 | RF-48 | SF-15 | MUST NOT | Every complete-certification claim | non-applicable | E01 | NR | not-required | `d4337ada7bbe28eaac6306c044b185178d04a9faa1914a30a321c4c8225bfab7` |
| PE-CERT-008 | RF-48 | SF-15 | MUST | Every partial Certification | non-applicable | E01 | NR | not-required | `f3748782aaef71986710c2cb14962475a5a7e4077c2970cad96698aef6a38124` |
| PE-CERT-009 | RF-48 | SF-15 | MUST | Every Certification | non-applicable | E01 | NR | not-required | `79e0838e22d8230f851cd7a95a6993f40cc0e1d9f68864601310e4e12bbf8d34` |
| PE-CERT-010 | RF-48 | SF-15 | MUST | Every certification authority | non-applicable | E01 | NR | not-required | `aa86033163882fc018b85b11ffa53fae890904a1797a1160c8b137b4272b13a9` |
| PE-CERT-011 | RF-48 | SF-15 | MUST | Every certification authority action | non-applicable | E01 | NR | not-required | `8b4668ada7ad17367b6deb1c5422f203d180d6f0b6b22ffa8bafd16d4ed21eb2` |
| PE-CERT-012 | RF-48 | SF-15 | MUST | Every Certification | non-applicable | E01 | NR | not-required | `8da7f9ea1626eafd2b7d8b03df0165a98931b37da183e2d195e3018a065391e0` |
| PE-CERT-013 | RF-48 | SF-15 | MUST | Every certification or compatibility statement | non-applicable | E01 | NR | not-required | `53088a9251f6d49946883aba8bcac43eb7def1c4ec9edc4123eba62ba58297a6` |
| PE-CERT-014 | RF-48 | SF-15 | MUST NOT | Every Certification and certification authority | non-applicable | E01 | NR | not-required | `0addbe56cfcfdf6a54b56e904c46241018bcc4ae25ff6c9edd197b2aed18efde` |
| PE-CERT-015 | RF-48 | SF-15 | MUST | Every certification withdrawal | non-applicable | E01 | NR | not-required | `5395ca234c696fbd3217309ca00b08415186a65c6a5dfa5a5d4e2c8e049b7499` |
| PE-CERT-016 | RF-48 | SF-15 | MUST | Every certification reassessment | non-applicable | E01 | NR | not-required | `941eb8dab14efb8b4c13134abbc54fbdd46f26e0a4b2660e2e0e9294ee056452` |
| PE-CERT-017 | RF-48 | SF-15 | MUST | Every certification lifecycle | non-applicable | E01 | NR | not-required | `06e48868410bf20721eaf1b3a0f310d616b199418daadfd95bd946495e83031e` |
| PE-CERT-018 | RF-48 | SF-15 | MUST | Every conformance and certification structure | non-applicable | E01 | NR | not-required | `5f3d862eda4cdf0e657f575b0d20847f4c36f3fb78ad5bee2ddbc4935c92dda1` |
| PE-CERT-019 | RF-48 | SF-15 | MUST | Every conformance and certification naming surface | non-applicable | E01 | NR | not-required | `c5b9d399de87da05bcaeb12cbecebb06c569153b47f11aa00f9c4fbe6be93bf9` |
| PE-CERT-020 | RF-48 | SF-15 | MUST NOT | Every conformance and certification composition | non-applicable | E01 | NR | not-required | `26f3dea1279023b8addff589d1abf255a8119ec07b9e52546127e2719eb7e5d6` |
| PE-SEMPRES-001 | RF-49 | SF-16 | MUST | Every downstream Privacy Engine layer | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `b8666236c30dbf2af7653d07c525bdd1bb0426d85549e43d265d7baa8f5bd57e` |
| PE-SEMPRES-002 | RF-49 | SF-16 | MUST | The complete downstream chain | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `87571890c7b063449e2ec78bb61c93eeef5df39db6c83c9c5e7511cef1dffab3` |
| PE-SEMPRES-003 | RF-49 | SF-16 | MUST | Every selected semantic subject or obligation | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `4fd21a8337f521442722213637eda06019a0f00c50b1190406b427820988f048` |
| PE-SEMPRES-004 | RF-49 | SF-16 | MUST | Every normative requirement crossing a downstream boundary | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `e03296397a647809e45b46eb1618883572f2fa2e9d27c040a9f873392464a5ef` |
| PE-SEMPRES-005 | RF-49 | SF-16 | MUST | Every semantic subject crossing a downstream boundary | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `abeb9fa18da6dd49ca9774698e78571ac1ec12fa3075cfb6d8893039c61241e7` |
| PE-SEMPRES-006 | RF-49 | SF-16 | MUST | Every requirement crossing a downstream boundary | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `435ce62622f2d0fef8c112eb29f675e0b8a444a7cc54925cfac8f23f7796dda0` |
| PE-SEMPRES-007 | RF-49 | SF-16 | MUST | Every requirement crossing a downstream boundary | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `432068eb5b29c8610b92bd380db33bf7d96b3a95f048d355c4164e99789c5e66` |
| PE-SEMPRES-008 | RF-49 | SF-16 | MUST | Every permitted protocol choice | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `4e74742673d76da60998bd2d0b9422471d201a9a9ece80b8ff1e470946a58b6f` |
| PE-SEMPRES-009 | RF-49 | SF-16 | MUST | Every protocol subject and occurrence | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `c7f4119f1f230e34a062f45ccd7454e81abdeec6d5d011d3a954868bbfdd8a38` |
| PE-SEMPRES-010 | RF-49 | SF-16 | MUST | Every downstream representation and surface | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `b739b76852fdea3ddb8254a4cbdf2d3f984b4232b6d785f473c17b68ac6cb381` |
| PE-SEMPRES-011 | RF-49 | SF-16 | MUST | Every proof, public input, verification, and validity boundary | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `77d1d801656135249e3e494edcb73d1160f441b6457dd4f8ebcb8aeac58a908a` |
| PE-SEMPRES-012 | RF-49 | SF-16 | MUST | Every Protocol Action use chain | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `1efd7a5954ad010c9d436326021023686b9f4926deada6e24886bf80565df19f` |
| PE-SEMPRES-013 | RF-49 | SF-16 | MUST | Every transition use chain | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `c9b5bcd46289d24e95e7cd9becbe4537321848340bfa061f427034178da80397` |
| PE-SEMPRES-014 | RF-49 | SF-16 | MUST | Every application or adapter boundary | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `974b097ea101db4da34c980a2a1d51a93d5e479170f55dad330cb11ae4650a16` |
| PE-SEMPRES-015 | RF-49 | SF-16 | MUST | Every runtime or implementation boundary | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `ed24abe58c3d87227d253fc9a5eb5b31adebc8e38ead806ff2a5c1f5bc329b34` |
| PE-SEMPRES-016 | RF-49 | SF-16 | MUST | Every compatibility structure | non-applicable | E01 | NR | not-required | `6767c2ae3f218d732c3da7295802742effee3ea46844573e0f24404420d1faf9` |
| PE-SEMPRES-017 | RF-49 | SF-16 | MUST | Every profile and Reference Implementation boundary | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `df09c3e0d21bc5a45a2773971b5b765a29e148307d2598e16616ae177ddd0f70` |
| PE-SEMPRES-018 | RF-49 | SF-16 | MUST | Every conformance boundary | non-applicable | E01 | NR | not-required | `246d480767f8f4b9d97795a11eb5fe9694be73bab74c2c848bc9a84e02634efc` |
| PE-SEMPRES-019 | RF-49 | SF-16 | MUST | Every certification boundary | non-applicable | E01 | NR | not-required | `a5eecad4d875df671d07bfdd6c2d9cd1f1563f456e0a07e1a886d8f9688b39f3` |
| PE-SEMPRES-020 | RF-49 | SF-16 | MUST | Every successful downstream operation | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `1ba949a2be9855f2cb380afdbd577ac4b738c1869d3a320d8250c8e9c176cd0b` |
| PE-SEMPRES-021 | RF-49 | SF-16 | MUST | Every downstream operation unable to demonstrate preservation | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `096377aff0c94468de364c0ebf4478b0f3df5bd74ea0d00871f6f9b4f26b4bd4` |
| PE-SEMPRES-022 | RF-49 | SF-16 | MUST NOT | Every preservation failure | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `20f1fd5e9027615f6c5df01a8e7d21069eccdbb43e76fc13dea5fc3715aa791b` |
| PE-SEMPRES-023 | RF-49 | SF-16 | MUST NOT | Every downstream layer | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `94997b1cf570b8e914213edfba7579db0d23aae9b0b1f9c1695dce792c1bd36d` |
| PE-SEMPRES-024 | RF-49 | SF-16 | MUST NOT | Every downstream layer | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `b3db8743977c645e160df43181e2ce85bd5cd332f931cc4b4ace431c8b737acb` |
| PE-SEMPRES-025 | RF-49 | SF-16 | MUST NOT | Every downstream layer | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `6ad60a5cf7938c3b742f757b7a9509c68f1ab685b94ac17e5d394164574aee55` |
| PE-SEMPRES-026 | RF-49 | SF-16 | MUST NOT | Every downstream composition | applicable | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10,E11,E12,E14,E15,E20,E21 | BD,TD,RG,DB,RO | ambiguous | `87f0492742f2ccde719148adf90f0aa6f76081e1e9ef7905ca085d9f258c6c98` |
| PE-EXCLUDE-001 | RF-50 | SF-16 | MUST | The complete Protocol Specification | non-applicable | E01 | NR | not-required | `7f17528a3e086e9b647a42ea69cb747c5ecc2acc4ead013bb18f9f9fb25181fc` |
| PE-EXCLUDE-002 | RF-50 | SF-16 | MUST NOT | Every development or protocol interpretation | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `5317c2b67a6332aa0da8e05120bf398212e5a27c8f7baf57df607e7f3072ebb9` |
| PE-EXCLUDE-003 | RF-50 | SF-16 | MUST NOT | Every downstream structure | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `5cecbda9466a6b25e2e11833b01ea1eb7dd435a6968c51ad67039e42aa6f81d8` |
| PE-EXCLUDE-004 | RF-50 | SF-16 | MUST NOT | Every downstream layer | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `2fd9dc128a73907ec830c94e8bdc3a30ce1434819f8b2ff95928da2372f14ac2` |
| PE-EXCLUDE-005 | RF-50 | SF-16 | MUST NOT | Every application interpretation | non-applicable | E01 | NR | not-required | `3e56d545d2794c441160f7476be6253a8094c5a5bc8d9447c45727f039d9e7fb` |
| PE-EXCLUDE-006 | RF-50 | SF-16 | MUST NOT | Every implementation interpretation | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `a6b7e110f31fd4d6aca7b5802054dda9407a05e120f0ac26c98139d83d9b8423` |
| PE-EXCLUDE-007 | RF-50 | SF-16 | MUST NOT | Every reference interpretation | non-applicable | E01 | NR | not-required | `6678a9f9aabbbcbc9e6466bca4e8726345a19448f53cf08411eebc3c40327967` |
| PE-EXCLUDE-008 | RF-50 | SF-16 | MUST NOT | Every compatibility interpretation | non-applicable | E01 | NR | not-required | `4782283bd1c6bda1142e6ee2ab895e62b4ff3954ead5587003b678ebc8025572` |
| PE-EXCLUDE-009 | RF-50 | SF-16 | MUST NOT | Every conformance interpretation | non-applicable | E01 | NR | not-required | `0b351adbfde2bf39bb70408f35a4c73a2d9d4213e3dec6c1438b01ad501fd983` |
| PE-EXCLUDE-010 | RF-50 | SF-16 | MUST NOT | Every certification interpretation | non-applicable | E01 | NR | not-required | `25da3cb119294bb9811b313356ac4057a4d2f604b43a700d7e49070d137b6387` |
| PE-EXCLUDE-011 | RF-50 | SF-16 | MUST NOT | Every evidence or testing interpretation | non-applicable | E01 | NR | not-required | `03b309f1dffcdaec195108296dbf75df33213aa7415d226ba4feaa78bf1286b4` |
| PE-EXCLUDE-012 | RF-50 | SF-16 | MUST NOT | Every protocol-subject identifier | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `d8dd3cfb6aa65e26ce79ad6e536707b25c442cdba50fab1ca0f6995dbed79c74` |
| PE-EXCLUDE-013 | RF-50 | SF-16 | MUST NOT | Every public identifier and metadata surface | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `9a9352281c5e2bd3b9da128c6ae251f200236c0c2eb45118e2d0125503e8452c` |
| PE-EXCLUDE-014 | RF-50 | SF-16 | MUST NOT | Every protocol, assessment, and certification surface | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `d7d825ba6e6e0960c350959aa80360a3fc3913da5e68cba5d0529cd383d9caa8` |
| PE-EXCLUDE-015 | RF-50 | SF-16 | MUST NOT | Every downstream record | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `75fce8680541273c05868236de7b50cad39a7da2cfe5409157100bc080113e38` |
| PE-EXCLUDE-016 | RF-50 | SF-16 | MUST NOT | Every metadata composition | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `5c5d0489d09e86bb9555b1063df238a036d17482e2902013d5f2a3025c52cc0f` |
| PE-EXCLUDE-017 | RF-50 | SF-16 | MUST NOT | Every naming and documentation surface | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `767ea87b852621c9cc2f3493cbc267a336357c999da7663c95601002980f4468` |
| PE-EXCLUDE-018 | RF-50 | SF-16 | MUST | Every proposed new first-class protocol subject | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `4f6d240b0760ec358a70a47a4af5c2dd10e8774d933d8b2e80e6cfb2f1d7815a` |
| PE-EXCLUDE-019 | RF-50 | SF-16 | MUST NOT | Every Protocol Claim interpretation | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `17030567f292c7c410f4ad013e3cb86ca8ff2893d72eae97dd44d9576a6e8535` |
| PE-EXCLUDE-020 | RF-50 | SF-16 | MUST NOT | Every Evaluation or classification model | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `51e6460e809b25f252a08f713cc1bd3aed1880a4cfaecfcc5b3b0adbc52c0ab6` |
| PE-EXCLUDE-021 | RF-50 | SF-16 | MUST NOT | Every transition model | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `a69506e77901bf073459c6c80378ead39b17bacf46a0b7b7731ba68889dab68b` |
| PE-EXCLUDE-022 | RF-50 | SF-16 | MUST NOT | Every certification model | non-applicable | E01 | NR | not-required | `601d286826cfed24a30689950395c2f6cf6e7e8fe2432801d2f587b1523205bd` |
| PE-EXCLUDE-023 | RF-50 | SF-16 | MUST NOT | Every implementation-specific design choice | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `d05518cfba0a4b11e02e6989b65f1fa3a20d2ebc9b67ddd585008e5ecc0685c6` |
| PE-EXCLUDE-024 | RF-50 | SF-16 | MUST NOT | Every application or certification-program choice | non-applicable | E01 | NR | not-required | `e5b8a61641dd0c2787c1d116a0a2352ff149a2ebdb63de13b3934d77b4a24445` |
| PE-EXCLUDE-025 | RF-50 | SF-16 | MUST NOT | The current implementation and codebase | applicable | E01,E02,E03,E16,E17,E21 | BD,TD,RG,DB,RO | bounded | `63f286b67b7ab9f309e686fecbcb6df884443e76b0af6aeb4e4055cd61af772c` |
| PE-EXCLUDE-026 | RF-50 | SF-16 | MUST NOT | The Engineering[150] specification state | non-applicable | E01 | NR | not-required | `e10e02c2d719c00e1a2978a52759c483b17066b969040da288ed1f6acf20c2a9` |

## 17. Assessment-Readiness Determination

The fixed baseline is retrievable and integrity-verifiable; the Profile V2 basis is guarded; all 308 tracked paths and all 729 Profile V2 rows are accounted for; application and implementation boundaries are explicit; and evidence classes remain distinct from baseline and result identity.

Requirement-level assessment must nevertheless remain paused because 292 coverage rows retain an ambiguous evidence path, including all seven permitted-choice rows. The principal ambiguity groups are:

- exact implementation mapping of established protocol subjects and occurrences;
- concrete Interface Contract, Concrete Interface Specification, and Protocol Surface identity/version mapping;
- complete validity-rule, Evaluation, Determination, and classification mapping;
- accepted no-transition, transition lifecycle, state/history/consequence, failure, stale-authorization, and re-evaluation mapping;
- cross-layer semantic-preservation mapping;
- explicit permitted-choice positions;
- and tracked ZK artifact provenance synchronization.

This pause is an evidence-readiness determination only. Ambiguity is not requirement failure, non-satisfaction, implementation defect, incompatibility, non-conformance, insecurity, or a remediation order.

## 18. Privacy and Neutral Naming

> Private actors, public actions.

Inventory, evidence-set, coverage, configuration, deployment, runtime, test, diagnostic, report, and failure naming remains neutral. This record introduces no Private Actor identity, reusable participant identity, cross-action identity continuity, enrollment or admission provenance, wallet or sponsor provenance, transport provenance, metadata correlation, or actor-reconstruction bridge.

## 19. No Assessment Results

This record does not determine:

- whether any requirement passes, fails, is satisfied, or is unsatisfied;
- whether any evidence item is sufficient for a substantive result;
- whether implementation behavior is correct or defective;
- whether compatibility or conformance exists;
- whether certification should issue;
- whether the implementation is secure or operationally ready;
- whether a deployment correctly realizes the baseline;
- or whether the implementation is or should become a Reference Implementation.

Tests, documentation, builds, deployments, and runtime observations remain candidate evidence only.

## 20. Failure and Preservation Model

> inspect(I164) -> inventoryEvidence(E, I164, C) -> mapCoverage(M, F2, E) -> accountForAllRows(M, 729) -> determineReadiness(D)

> basis(D) = F2

> baseline(D) = I164

> noRequirementResult(D)

> ambiguousEvidencePath -> pauseLaterAssessment

> inferEvidence or mergeRevision or repairImplementation or alterProfile or assessRequirement -> invalid

## 21. Findings

1. The implementation archive and Git tag identify the same engineering-164 commit.
2. The guarded commit resolves to the guarded tree and exactly 308 tracked paths: 305 blobs and three Gitlinks.
3. The complete tracked baseline can be inventoried without merging another revision or deployment.
4. All 729 Profile V2 rows can be represented in exact published order with preserved metadata and byte-identity digests.
5. All 478 applicable, 244 non-applicable, and seven permitted-choice dispositions remain preserved.
6. Protocol-facing, application-owned, mixed, evidence-support, dependency, historical/inactive, and ambiguous-status material can be separated without directory-level assumption.
7. Potential tracked, generated, deployment-bound, runtime-observation, and documentation evidence routes are identifiable.
8. No coverage row lacks every candidate evidence path, but 292 rows retain an ambiguous path.
9. The seven permitted-choice positions remain ambiguous and no default is inferred.
10. Requirement-level assessment is therefore not yet ready to begin.

## 22. Determination

> Privacy Engine engineering-164 implementation baseline evidence inventory and assessment coverage map completed

This determination means only that the complete tracked baseline has been inventoried, potential evidence routes have been bounded, every Profile V2 row has been accounted for, evidence ambiguities have been recorded, and later assessment readiness has been determined.

Readiness determination: **paused pending bounded resolution of the recorded ambiguous evidence paths**.

## 23. Future Position

A later bounded slice may resolve evidence-path ambiguity without modifying Profile V2 or assessing requirement satisfaction. Requirement-level assessment may begin only after every applicable row and permitted-choice row has one sufficiently bounded evidence and evaluation path under the Engineering[165] readiness conditions.

Any future evidence must remain tied to engineering-164 or explicitly declare a new baseline. It must not silently merge later code, generated artifacts, configuration, deployment state, or runtime observations.

## 24. Explicit Exclusions

Engineering[166] does not modify STATE.md, Profile V2, the published specification, the implementation baseline, source code, contracts, circuits, tests, configuration, generated artifacts, deployment, or runtime state. It does not create Profile V3, a new protocol generation, a new publication occurrence, a requirement result, compatibility, conformance, certification, a security assessment, operational-readiness assessment, implementation defect, repair plan, or Reference Implementation designation.

## 25. Conclusion

The engineering-164 baseline now has one complete tracked-path inventory and one complete Profile V2 assessment coverage map. Every row is preserved and routed without assessment. Ambiguous evidence relationships remain explicit, so requirement-level assessment remains paused rather than inferred.

Determination: **Privacy Engine engineering-164 implementation baseline evidence inventory and assessment coverage map completed**.
