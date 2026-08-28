# Privacy Engine I164 Validity Rule, Applicable Rule-Set, Action-Type and Evaluation-Context Mapping Determination Independent Review V1

## 1. Status and Final Review Result

This document records the bounded Engineering[194] independent review of:

`docs/PRIVACY_ENGINE_I164_VALIDITY_RULE_APPLICABLE_RULE_SET_ACTION_TYPE_AND_EVALUATION_CONTEXT_MAPPING_DETERMINATION_V1.md`

Engineering[194] independently reviewed the complete Engineering[193] determination and returns exactly one final review result:

**accepted**

Engineering[193] correctly determined:

**complete selected A04 mapping package not constructible**

Acceptance means only that Engineering[193] correctly maps the exact supported I164 components, preserves the exact non-mappings and material unresolved relationships, applies the complete-package construction rule, and leaves every reviewed-current row state unchanged.

Acceptance does not mean that the selected A04 package is constructible. It does not perform evidence-path reclassification, assess evidence availability or sufficiency, assess a requirement, produce a requirement result, determine an implementation defect, perform a security assessment or determine compatibility, conformance, certification or operational readiness.

No partial terminal acceptance is created.

## 2. Review Question

Engineering[194] addresses exactly one review question:

> Did Engineering[193] correctly determine that the complete selected A04 mapping package is not constructible from I164, while preserving the nine bounded A04 rows, the 16 still-ambiguous A04 rows, all non-A04 rows and the reviewed-current totals?

The review covers the complete Engineering[193] artifact, not only its identities or final sentence.

## 3. Authority and Subject Boundary

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

The untracked Git-provenance handover record is metadata only. It is not protocol documentation, implementation material, mapping authority, review authority, evidence-path authority, requirement evidence or a requirement result.

## 4. Review Discipline

The independent review applied four distinct tests:

1. cryptographic and structural identity verification;
2. exact predecessor-state reconstruction;
3. independent I164 source inspection and relationship testing;
4. scope, privacy, authority and arithmetic preservation.

The preservation rule was:

> selected formal relationship `M`  
> -> inspect exact I164 material  
> -> preserve only the relationship that material supports

If I164 cannot preserve `M` completely:

> `M -> unresolved`

Forbidden:

> `M -> inferred M'`

The complete-package rule was independently applied conjunctively. One unresolved required term is sufficient to prevent construction of the complete package. Exact isolated components do not create partial terminal acceptance.

## 5. Handover Verification

### 5.1 Formal corpus

| Field | Independently verified value |
|---|---|
| File | `privacy-engine-formal-corpus.zip` |
| SHA-256 | `4c3d8f46086dfac1bad7efad3b01afd8a57de4f6c8754e4836697895e61e04e1` |
| Distinct files | 113 |
| Directory entries | 1 |
| ZIP integrity | passed |
| Git archive comment | `845794ec5432469a1595d41f80f6b87d0191d32b` |

### 5.2 I164 implementation archive

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

### 5.3 Git provenance

| Field | Independently verified value |
|---|---|
| File | `privacy-engine-git-provenance.txt` |
| Format | `PRIVACY-ENGINE-HANDOVER-GIT-PROVENANCE/1` |
| SHA-256 | `b808c078679ab1ec1dd114c3101c54959aee3a96fa0f8c5bb3fbb7f2afc10022` |
| Records | 26 |
| Record range | `engineering-164`; `engineering-169` through `engineering-193` |
| Local engineering refs | 26 matched |
| Remote engineering refs | 26 matched |
| Raw commit identities | 26 reproduced |
| Raw payload lengths | 26 matched |
| Trees and parents | 26 matched their raw commit payloads |
| Changed-file records | 30 verified |
| Generic-tag refs | none supplied or inferred |

Every raw payload independently reproduced its stated Git commit identity using the canonical Git commit-object preimage.

Three historical changed-file byte sequences are no longer the current corpus bytes because they were later corrected. They were independently reconstructed through their exact accepted mechanical correction records:

| Historical artifact | Reconstructed SHA-256 | Reconstructed Git blob | Reconstruction |
|---|---|---|---|
| Immutable pre-correction Engineering[171] | `e7c31445ad77c2b6f592e88b846202286f003b039a717939b7f6d198d6672d46` | `608f14b000f1b5faf7569562d674bb609bb79bf2` | removed exactly the 11 later-inserted final U+0060 bytes |
| Immutable Engineering[175] | `1eb8ed90926975001e1976ad4e05edbb3e81f70aa703754e053cf1f768449085` | `ab1d62e2550490693da377cb0bcb47b1160157ea` | reversed exactly the two accepted `0x33 -> 0x63` corrections |
| Immutable pre-correction Engineering[189] | `19654e6487eaac58b5fade78045fe09f5ec3a96b90446dfccb5725e3a79798fa` | `f0f515372fcd77d278e7b8f65fc40b3a99ea65a2` | removed exactly the four later-inserted ASCII commas |

All other changed-file records matched supplied current bytes directly.

## 6. Complete Provenance Record Verification

| Record | Commit | Tree | Parent | Raw bytes | Changed files |
|---|---|---|---|---:|---:|
| engineering-164 | `003e984ea73a2dede092443893dfbc9e74121e14` | `6271b80f2fa6167961e18c5b4c229d25374497a7` | `5e12cca624ffccf43637de4b9dc42de4af3979bc` | 290 | 2 |
| engineering-169 | `392863755dac71b5d762c26caf3830c987dbbfaf` | `91de8930ed29add9b0e7986566319946e0d63bfa` | `8a7a4d222e13e8128968798b28a597cf5aab7f45` | 283 | 1 |
| engineering-170 | `c16aa4f7516917ffbbfae8cc939a8959106a2e46` | `40de12f4fbab9ac7fda3abf76bb4a19ef8959515` | `392863755dac71b5d762c26caf3830c987dbbfaf` | 286 | 1 |
| engineering-171 | `7fc018bc705c4bd990bf48ff3635acc196059ba1` | `933f11fa3556d2eff9a8ec7892c9d56fd4f05859` | `c16aa4f7516917ffbbfae8cc939a8959106a2e46` | 299 | 1 |
| engineering-172 | `7f2c7627ca8eba0dd07bd98e2a8843b84bd0b7ba` | `d3552aec3d34f31d437d9e18bc4ddc6aa636172b` | `7fc018bc705c4bd990bf48ff3635acc196059ba1` | 293 | 1 |
| engineering-173 | `8ba9dfe6adfaeefa1119112065745fb8629415e8` | `5d90214408df0340d7d01c58943cc389a3a4747c` | `7f2c7627ca8eba0dd07bd98e2a8843b84bd0b7ba` | 289 | 2 |
| engineering-174 | `3b249ba36ec3e6de7e4f3ee64c32037aec206b82` | `ecded46e0884bcd2acfe1ae8b741be8dea897cbe` | `8ba9dfe6adfaeefa1119112065745fb8629415e8` | 303 | 1 |
| engineering-175 | `f747b875c96af441e68c4bdc73a4f4f6c6642ce0` | `c7f0e24481c28431377bbaa114559f85899142d9` | `3b249ba36ec3e6de7e4f3ee64c32037aec206b82` | 289 | 1 |
| engineering-176 | `62b7f600129ddd0f55fd695362a7ff991833d5aa` | `893961a1c872768267a8f331cb4a0a6473c0ac96` | `f747b875c96af441e68c4bdc73a4f4f6c6642ce0` | 299 | 1 |
| engineering-177 | `eb98d30d0d168e8eae26422f9a75bbfa4a655ae9` | `876fcfc7fd1dec5ad4e9d0c501ff9f1440784b8d` | `62b7f600129ddd0f55fd695362a7ff991833d5aa` | 300 | 2 |
| engineering-178 | `d851655f313b55cd0a9e93800f4773e4c638fc49` | `07e65bd9fcfe0d64faff4288d3641eb43e8fd5ff` | `eb98d30d0d168e8eae26422f9a75bbfa4a655ae9` | 311 | 1 |
| engineering-179 | `cb03b53cb212e2834c7220ccae3ee5781efdc474` | `efc07a79f0d945fe5ebcf5bbb1a039b4c623913b` | `d851655f313b55cd0a9e93800f4773e4c638fc49` | 301 | 1 |
| engineering-180 | `463c8957bd51774251197c59cd64340910a6d88d` | `2975148322eb081e960187182ff6a342f1a3c410` | `cb03b53cb212e2834c7220ccae3ee5781efdc474` | 312 | 1 |
| engineering-181 | `f9f6eec5fd0048d1b4c5120b6a16c6970ea58fa4` | `8948a1c4b38c2477dd67cbc7deca35f8456827d4` | `463c8957bd51774251197c59cd64340910a6d88d` | 300 | 1 |
| engineering-182 | `ab7a80c0bcebae280fcdaa3adc6d7abaac71e44a` | `12926dea825e7cf5a487526e8a26901d683722c8` | `f9f6eec5fd0048d1b4c5120b6a16c6970ea58fa4` | 288 | 1 |
| engineering-183 | `b88f4816dd264bf55a60a8749e5cbcb7952deab2` | `68f25878e0fc060923ebd85b2590b126eee6d592` | `ab7a80c0bcebae280fcdaa3adc6d7abaac71e44a` | 286 | 1 |
| engineering-184 | `b5ab7ac90a683466d01b82d7010947fbda4d7624` | `2e4e134dfd9116b2a96e35e4493af0d70e3c6b5c` | `b88f4816dd264bf55a60a8749e5cbcb7952deab2` | 297 | 1 |
| engineering-185 | `cf6dbe48059f3a119d7e463e2902603c672ddff3` | `9652d3952be9cf6181a610fb25292f175c5b89b4` | `b5ab7ac90a683466d01b82d7010947fbda4d7624` | 294 | 1 |
| engineering-186 | `d9c4a78a838215910c3857202f72ebd423aa7167` | `21d7df36c86607f4d5a935bdc3bba9c54e82b570` | `cf6dbe48059f3a119d7e463e2902603c672ddff3` | 289 | 1 |
| engineering-187 | `3cff28f8123fe1d5514bb1da3c99e6a498fc2e87` | `6e5797f2dda3f65a1023deb4151aadaa6584444e` | `d9c4a78a838215910c3857202f72ebd423aa7167` | 300 | 1 |
| engineering-188 | `03724cec80f8f326e6ed68ca31481a5b84520906` | `c813fc49d88c349f3395e1edf11184a0ad7ed8cf` | `3cff28f8123fe1d5514bb1da3c99e6a498fc2e87` | 311 | 1 |
| engineering-189 | `459a866aa5c9bd75a8e349161356cf3396b04083` | `864b7cfa580576015497d53b3ec8e3500e77afd5` | `03724cec80f8f326e6ed68ca31481a5b84520906` | 305 | 1 |
| engineering-190 | `7ffda63cdcf632cd0d6cf20f286d1d6419bdf25b` | `9fe9825a338c310a67374050ac73b4b9d5fd0a31` | `459a866aa5c9bd75a8e349161356cf3396b04083` | 322 | 1 |
| engineering-191 | `36bdb6ff73a513fdc73b8db6b8d69f2cd3fd8094` | `96dbbe6d457e71e8fb420270b61098eee5d421ab` | `7ffda63cdcf632cd0d6cf20f286d1d6419bdf25b` | 296 | 2 |
| engineering-192 | `3bc4086267e37384cb19d244f56ebfe177a74666` | `7ce64826ef77aabddc9c9b3e539116fbc5eb4cc7` | `36bdb6ff73a513fdc73b8db6b8d69f2cd3fd8094` | 291 | 1 |
| engineering-193 | `845794ec5432469a1595d41f80f6b87d0191d32b` | `27e62a8ee45e5d3ed8f3974f69b0be2bc3ac4f58` | `3bc4086267e37384cb19d244f56ebfe177a74666` | 304 | 1 |

Every supplied local and remote lightweight engineering-tag ref matched its stated resolved commit. No generic-tag relationship was inferred.

## 7. Complete I164 Baseline Reconstruction

The guarded baseline inventory contains exactly 308 unique tracked paths:

- 305 blobs;
- three Gitlinks.

Every archived blob reproduced its guarded Git object and SHA-256 identity.

The three Gitlinks were restored as:

| Path | Git object |
|---|---|
| `contracts/lib/forge-std` | `52c1e835e9ffcfe00bd9f8f51de204b93bc7028a` |
| `contracts/lib/openzeppelin-contracts` | `8ff78ffb6e78463f070eab59487b4ba30481b53c` |
| `contracts/lib/openzeppelin-contracts-upgradeable` | `b933412726bccd822a871116f1427111e649ff54` |

Reconstruction of the complete nested Git tree from the 305 verified blobs and three Gitlinks independently reproduced:

`6271b80f2fa6167961e18c5b4c229d25374497a7`

The I164 raw commit payload independently reproduced commit:

`003e984ea73a2dede092443893dfbc9e74121e14`

The implementation archive is therefore the fixed I164 subject and not a later implementation revision.

## 8. Profile V2 Basis

The accepted Complete Implementation Profile V2 remains the sole requirement-selection basis:

| Disposition | Rows |
|---|---:|
| applicable | 478 |
| non-applicable | 244 |
| resolved through permitted specification choice | 7 |
| conditionally applicable | 0 |
| total | 729 |

The 729 Profile V2 rows and identifiers remain unique and in guarded order.

No requirement-level assessment has been performed.

No requirement result exists.

## 9. Engineering[192] Verification and Preserved A03 Effect

Engineering[192] artifact:

`docs/PRIVACY_ENGINE_I164_PROTOCOL_SURFACE_PROTOCOL_OPERATION_AND_PUBLISHED_RESULT_IDENTITY_VERSION_AND_REALIZATION_MAPPING_DETERMINATION_CORRECTION_INDEPENDENT_REREVIEW_V1.md`

| Field | Independently verified value |
|---|---|
| SHA-256 | `874f8dc5c32f4f89e23441dcb897251621e164c4ddc9dc36f26358105b8be833` |
| Git blob | `0a7b9eb22406ee6780d5cc90668fe99e27de9103` |
| Length | 48,091 bytes |
| Lines | 1,037 |
| Canonical final-rereview payload length | 6,324 bytes |
| Canonical final-rereview payload SHA-256 | `5e9175730af337ba46911ba11c3d477c6f893b6e68f70f809ef9c6a2f7c4b3b3` |
| Final review result | accepted |

Engineering[192] correctly accepted the mechanically corrected Engineering[189] determination.

The preserved A03 substantive conclusion is:

**complete selected A03 mapping package not constructible**

All 18 A03 rows remain reviewed-current `still-ambiguous`.

Engineering[192] performed no evidence-path transition, altered no reviewed-current total, performed no requirement assessment and did not make I164 protocol authority.

## 10. Accepted A04 Predecessor Chain

The complete accepted predecessor chain was independently reconstructed:

| Slice | Artifact role | SHA-256 | Preserved result |
|---|---|---|---|
| Engineering[169] | Mapping declaration | `a6e488f8a246dcf14c2a3a3e0df8226833ccec8720d12c6798a971a0d3ee6890` | declaration |
| Engineering[170] | Acceptance review | `7f435cf93d835ee3106e995c355a4d2019f2de81eaed5df2a5e9448b4bac20db` | accepted |
| Engineering[171] | Immutable pre-correction reclassification | `e7c31445ad77c2b6f592e88b846202286f003b039a717939b7f6d198d6672d46` | historical pre-correction artifact |
| Engineering[172] | Independent review | `cc4e5b82a2fba611fa68032ff6eef25c45c18c9ed3d7fbc963766513fbca5b8d` | correction required |
| Corrected Engineering[171] | Corrected reclassification | `f40638d8468749afe5d260fdf01e456fc27d3afd9febf75bfe2d59e2fa6d36ff` | corrected candidate |
| Engineering[173] | Mechanical correction record | `df1346947f347bb1c89569bafeb64fcee467680f88de5b4e318d9f0c7f97c1d9` | exactly 11 U+0060 insertions |
| Engineering[174] | Independent rereview | `ba5b8d9c6512e36f7d0d3b0e0aedd195ac0e1652cb0d7bfeeef2f17c0ab44b1f` | accepted |

Engineering[170] canonical acceptance payload independently reproduced:

- length: 883 bytes;
- SHA-256: `3c2a25b20c119d399cf3e954c26fd465834c82b6835b430f5375552fb1a1be06`.

Engineering[174] accepted the corrected reclassification and established the reviewed-current A04 state:

- 9 bounded;
- 16 still-ambiguous;
- 0 missing-evidence-path;
- 0 not-required;
- 25 total.

No later artifact through Engineering[193] changed that A04 state.

## 11. Relevant Accepted A05 Relationship Evidence

Engineering[181] determined that I164 does not supply a complete Protocol Action occurrence identity, admission and repeated-presentation mapping package.

Engineering[182] independently accepted that mapping determination.

Engineering[183] proposed no A05 evidence-path transition.

Engineering[184] independently accepted Engineering[183].

The independently reconstructed accepted A05 relationship preserves:

- `U-ACTION-IDENTITY` unresolved;
- `U-ACTION-ADMISSION` unresolved;
- `U-RETRY` unresolved;
- no complete formal action-type mapping;
- `T-I164-ANONYMOUS-PUBLIC-ACTION` as an implementation-owner coordinate only;
- no positive Action identity, action type or authoritative admission boundary;
- `PE-ACTION-015` as the sole bounded A05 row;
- all other A05 rows `still-ambiguous`;
- all non-A05 rows unchanged;
- reviewed-current totals unchanged at `217 / 268 / 0 / 244`.

These accepted unresolved relationships remain directly material to the Engineering[193] action-type, Evaluation-context and applicable-rule-set questions.

## 12. Engineering[193] Identity Verification

### 12.1 Git identity

| Field | Independently verified value |
|---|---|
| Engineering tag | `engineering-193` |
| Commit | `845794ec5432469a1595d41f80f6b87d0191d32b` |
| Tree | `27e62a8ee45e5d3ed8f3974f69b0be2bc3ac4f58` |
| Parent | `3bc4086267e37384cb19d244f56ebfe177a74666` |
| Raw commit payload length | 304 bytes |
| Changed-file count | 1 |

The complete raw commit payload independently reproduced:

`845794ec5432469a1595d41f80f6b87d0191d32b`

Both supplied `engineering-193` refs resolve to that commit.

No generic-tag ref was supplied or inferred.

The sole changed path is:

`docs/PRIVACY_ENGINE_I164_VALIDITY_RULE_APPLICABLE_RULE_SET_ACTION_TYPE_AND_EVALUATION_CONTEXT_MAPPING_DETERMINATION_V1.md`

### 12.2 Artifact identity

| Field | Independently verified value |
|---|---|
| SHA-256 | `4b49dcdfeaf0a98e456471c0be9961cc5661a601a0a57e79b3724e3e90573a2a` |
| Git blob | `40702c845e47f8c5218068c0e5cf3a91ab090a77` |
| Length | 41,828 bytes |
| Lines | 779 |
| Canonical determination payload length | 3,311 bytes |
| Canonical determination payload SHA-256 | `ebb4e4d2ae79468f034737e20411160c5d1858750ca1d0e3460385530c395784` |

The artifact identity, canonical payload and Git provenance agree exactly.

## 13. Guarded A04 Row Ledger

The following 25 rows preserve exact Profile V2 order, identifier, RF family, SF home, strength, published applicability, predecessor state and guarded Profile V2 row hash:

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

All 25 exact Profile V2 row bytes independently reproduced their guarded SHA-256 values.

The guarded position of `PE-RULE-013` before `PE-RULE-009` is preserved.

The ledger contains exactly nine bounded and 16 `still-ambiguous` rows.

## 14. Candidate Anchor Verification

All 35 Engineering[169] evidence-register anchor rows independently matched their I164 path, Git blob and SHA-256 identities.

Engineering[193] identifies the following principal and additional exact anchors:

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

All listed anchors matched. No path, object or digest mismatch remains.

The following tracked runtime artifacts also independently reproduced their recorded SHA-256 identities:

| Path | SHA-256 |
|---|---|
| `frontend/public/zk/sign_petition.wasm` | `996ad4bcf08548125ae15fbf98a9748170647d8609bdbade16003c3cd351dcb3` |
| `frontend/public/zk/sign_petition_final.zkey` | `762433cb44fc19ff7ebf575b71f56af75f17b161f87102517a6259086b9b99f1` |
| `frontend/public/zk/verification_key.json` | `8548836eaeb4500e19ca9032852095b257a9a5267206dd4e8180740c8841d14c` |
| `zk/v3-groth16/golden-proof.json` | `01360c724f748b1630b6605bf7464af585643a0d87fcbbb2a21e3fa3025a63b7` |

## 15. Independent I164 Source Inspection

### 15.1 Witness preparation and proof construction

`frontend/src/hooks/useZKProof.js` independently confirms:

- bounded field and depth checks;
- local `memberSecret` handling;
- `Poseidon1(memberSecret)` leaf derivation;
- path and path-bit normalization;
- local root reconstruction against the supplied root;
- `Poseidon3(memberSecret, petitionId, SIGN_DOMAIN)` nullifier derivation;
- local Groth16 proof construction;
- local proof verification;
- exported verifier calldata.

These are exact construction and preflight components. They do not establish Protocol Action identity, authoritative admission, the complete applicable rule set, complete Evaluation or Determination.

### 15.2 Circuit constraints and verifier-facing values

`zk/v3-groth16/circuits/sign_petition.circom` independently confirms:

- private `memberSecret`, membership siblings and membership indices;
- public `petitionId` and `membershipRoot` inputs;
- public `nullifier` output;
- binary path-index constraints;
- Poseidon2 Merkle reconstruction;
- equality of the reconstructed root with the supplied root;
- Poseidon1 leaf derivation;
- Poseidon3 action-local nullifier derivation;
- `SIGN_DOMAIN = 0x5349474e`;
- depth 16.

The active verifier-facing signal order is independently established as:

1. `nullifier`;
2. `petitionId/actionId`;
3. `membershipRoot`.

The archived golden proof and contract coherence checks confirm that order.

### 15.3 Groth16 verifier

`contracts/src/v3/Groth16Verifier.sol` independently confirms:

- exactly three verifier-facing public values;
- scalar-field checks;
- verification-key linear combination;
- pairing verification;
- one bounded Boolean proof-verification result.

The result concerns the applicable proof relation and ordered public values only.

It is not complete Protocol Action Evaluation or complete protocol validity.

### 15.4 PetitionRegistry active signing path

`PetitionRegistry.signPetitionWithZKProof` independently confirms the following ordered checks and effects:

1. petition existence;
2. unused `(petitionId, nullifier)` state;
3. configured Groth16 verifier;
4. Groth16 proof verification;
5. nullifier and `pubSignals[0]` coherence;
6. petition/action context and `pubSignals[1]` coherence;
7. action-local used-state mutation;
8. `PetitionSigned` emission with zero admission-commitment field.

The compatibility `admissionCommitment` parameter is ignored by this path.

The path does not call `AdmissionRegistry.recordActionLink`.

The path does not read `AnonymousMembershipRegistry`.

The path does not call `isValidRoot` or read `isKnownRoot`.

The checks and effects are exact implementation components. Their presence does not manufacture a complete generation-derived rule ledger or formal Evaluation boundary.

### 15.5 Accepted-root state

`AnonymousMembershipRegistry` independently confirms:

- a depth-16 Poseidon2 incremental Merkle tree;
- a 16-root history window;
- `isKnownRoot` state;
- `isValidRoot(root)` returning `isKnownRoot[root]`;
- deterministic root-history updates;
- leaf registration and root events.

The circuit establishes:

> witness path  
> -> computed root  
> -> equality with supplied `membershipRoot`

The membership registry separately exposes:

> claimed root  
> -> `isKnownRoot` / `isValidRoot`  
> -> accepted-root-state result

The active PetitionRegistry signing path contains no call or state read joining those relationships.

Therefore:

> supplied-root inclusion  
> `!=` accepted-root status

Accepted-root status cannot be inferred from proof success, backend reconstruction, frontend preflight, documentation, deployment proximity or naming.

### 15.6 Membership-path preparation and REFLECT

The membership indexer, membership routes and REFLECT prepared-path surfaces independently confirm:

- deterministic rebuild from indexed leaves;
- leaf-index continuity checks;
- local Merkle-path reconstruction;
- prepared-path normalization;
- local publication-object construction;
- local publication-window selection;
- acquisition and reconstruction;
- exact reconstructed material equality checks before response.

These components prepare and distribute material for local proof construction. They do not authoritatively establish accepted-root status, Protocol Action admission, complete Evaluation or Determination.

### 15.7 Relay validation and freshness

`backend/src/routes/relay.js` independently confirms:

- request-rate limiting through an operational IP key;
- `petitionId`, nullifier, proof-shape and public-signal validation;
- nullifier/public-signal coherence;
- action-context/public-signal coherence;
- petition-indexer freshness gating;
- action-local used-state prechecking;
- fixed zero admission commitment in the constructed submission;
- sanitized success and error logging.

These are transport and operational checks.

Payload acceptance, freshness, prechecking and relay receipt are not authoritative Protocol Action admission or complete Evaluation.

### 15.8 TEMPEST execution and reconciliation

The TEMPEST sources independently confirm:

- seven frozen operational slots;
- deterministic seed construction from the frozen submission;
- deterministic permutation;
- two execution-domain mappings;
- sequential dispatch;
- bounded continuation after controlled or transport failure;
- immediate propagation of execution reverts and unclassified failures;
- used-state reconciliation after uncertain submission;
- immutable submission representation.

Seed, permutation, slot, domain, fallback attempt, signer and transaction coordinates remain operational only.

They do not define or reconstruct actor identity, Protocol Action identity, repeated-presentation equivalence, rule applicability, protocol validity, Evaluation or Determination.

### 15.9 Mutation, observation and persistence

The contract, indexer, handlers, repository and migrations independently confirm:

- action-local used-state mutation;
- `PetitionSigned` public event emission;
- omission of admission commitment during normalized signing observation;
- transactional event handling;
- event idempotence by `(tx_hash, log_index)`;
- downstream action-local uniqueness by `(petition_id, nullifier)`;
- derived signature counts;
- migration removal of the admission-commitment column.

Mutation, event, normalized observation, persisted row and derived read model remain distinct from formal Evaluation, Determination, Published Result and protocol authority.

### 15.10 Admission separation

`AdmissionRegistry` independently confirms an economic admission-right lifecycle and membership-activation path.

The active ZK signing path remains separate:

- the compatibility admission field is ignored;
- the relay supplies zero;
- `PetitionSigned` emits zero;
- the signing indexer omits admission commitment;
- the signature schema removes admission commitment;
- no active signing call links the admission right to the signing action.

This establishes a bounded separation relationship only. It does not establish Action identity, action type, authoritative admission, the complete rule set or complete privacy coverage.

### 15.11 Tests, deployment and documentation

The reviewed tests represent bounded component behavior including:

- membership tree and root-history behavior;
- proof-valid and proof-invalid paths;
- public-signal order;
- action-local uniqueness;
- admission/signing separation;
- deterministic execution fallback;
- non-continuation after execution revert;
- reconciliation after transport uncertainty.

Deployment scripts, verifier verification scripts, configuration, manifests and documentation identify bounded candidates and operations.

Test presence, deployment material, documentation and prior runtime observations do not establish protocol rule identity, applicable-rule-set completeness, requirement satisfaction or protocol authority.

## 16. Action-Type Inventory Review

I164 exposes candidate implementation operations including:

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

The source does not exhaustively classify these candidates as Protocol Operations, formal action types, Protocol Actions, preparatory operations, transport operations, application operations, administrative operations, deployment operations or non-protocol machinery.

The accepted A05 evidence preserves the absence of a complete formal action-type mapping.

`T-I164-ANONYMOUS-PUBLIC-ACTION` remains an implementation-owner coordinate only and cannot supply the missing formal identity.

Engineering[193] therefore correctly concludes:

> complete action-type inventory = unresolved

## 17. Bounded Evaluation-Context Review

I164 exposes candidate coordinates including:

- published protocol generation;
- Complete Implementation Profile V2;
- chain and deployment configuration;
- PetitionRegistry execution state;
- configured verifier;
- application-target state;
- supplied membership root;
- available root-history state;
- action-local nullifier state;
- relay freshness;
- transport configuration;
- operational execution state.

No exact I164 representation composes those coordinates into one complete bounded formal Evaluation context.

The source does not establish:

- complete context identity;
- Evaluation start;
- Evaluation completion;
- authoritative Action admission;
- the exact protocol-relevant state included in the context;
- the complete exclusion of operational policy from validity;
- the rule for comparison across materially different contexts.

Engineering[193] therefore correctly concludes:

> complete bounded evaluation-context inventory = unresolved

## 18. Applicable Rule-Set Review

I164 contains exact individual checks, but check presence does not establish generation-derived rule identity or completeness.

The active contract path checks:

- petition existence;
- action-local nullifier state;
- verifier configuration;
- proof verification;
- nullifier coherence;
- action-context coherence.

The circuit constrains:

- leaf derivation;
- supplied-root inclusion;
- action-local nullifier derivation;
- domain separation;
- public-value binding.

The active path does not evaluate accepted-root state.

No exact ledger establishes before authoritative Evaluation begins:

- one formal action type;
- one complete bounded evaluation context;
- every applicable proof requirement;
- every applicable public-input requirement;
- every applicable non-proof validity condition;
- every accepted-root requirement;
- every uniqueness condition;
- every state-relative condition;
- every action-type constraint;
- every exact rule-to-check assignment.

`U-RULESET`, `U-ROOT` and `U-PRIVACY-REVIEW` remain unresolved.

Engineering[193] therefore correctly concludes:

> complete applicable rule-set inventory = unresolved

## 19. Exact Supported Components

Engineering[194] independently confirms every Engineering[193] supported component:

| Component | Independently confirmed relationship | Preserved limitation |
|---|---|---|
| Witness preparation | local witness, action-context and path material are prepared | pre-Evaluation construction only |
| Circuit proof relation | leaf derivation, supplied-root inclusion and action-local nullifier derivation are constrained | supplied-root inclusion is not accepted-root status |
| Verifier-facing values | order is nullifier, action context, supplied root | ordered values do not establish Action identity or complete Evaluation |
| Proof verification | proof and three signals produce a bounded Boolean result | proof verification is not complete protocol validity |
| Petition existence | application-target existence gates continued execution | no formal rule assignment is established |
| Action-local uniqueness | the same `(petitionId/actionId, nullifier)` key cannot succeed twice | the key is not participant or Action-occurrence identity |
| Verifier configuration | an unconfigured verifier blocks execution | deployment configuration is not automatically protocol validity |
| Proof-result gate | false verification blocks continued execution | revert is not Determination |
| Public-nullifier coherence | argument and signal zero are bound | no Action identity is defined |
| Public-action coherence | application target and signal one are bound | application-target identity remains distinct |
| Root inclusion | witness membership is proven under the supplied root | accepted-root status is not established |
| Accepted-root state | readable root-history state exists | no active signing-path relationship exists |
| Membership-path preparation | material is reconstructed and supplied locally | operational distribution is not root Evaluation |
| Relay payload gate | shape and selected public fields are checked | transport validation is not formal admission |
| Freshness gate | operational state freshness gates dispatch | freshness is not a protocol-validity rule |
| Relay used-state check | used state can short-circuit dispatch | operational precheck is not Evaluation or Determination |
| Frozen submission | submission representation is preserved | representation is not Action identity |
| TEMPEST execution | deterministic selection and fallback exist | topology and attempts are operational |
| Reconciliation | uncertain submission can be checked against used state | observation cannot reconstruct Action or Determination |
| Mutation and event | used state and a public action observation are produced | neither is formal Evaluation or Determination |
| Indexed observation | public events are normalized and persisted | observation is not protocol authority |
| Persistence uniqueness | event idempotence and action-local uniqueness are preserved | database identity is not Action identity |
| Admission separation | signing omits active admission linkage | separation does not establish the complete rule set |
| Tests | individual behaviors and failure paths are represented | tests do not prove formal rule identity or completeness |
| Deployment candidates | addresses, artifacts and operations are identifiable | deployment material is not protocol authority or a complete ledger |

Every component remains bounded to its exact supported relationship.

## 20. Exact Non-Mappings

Engineering[194] independently confirms the following non-mappings:

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
28. seed, slot and domain `!=` Action identity or actor provenance;
29. transaction hash `!=` Action identity;
30. event coordinates `!=` Action identity;
31. database key `!=` Action identity;
32. admission compatibility syntax `!=` action identity;
33. admission state `!=` signing identity;
34. `(petitionId/actionId, nullifier)` `!=` reusable participant identity;
35. test presence `!=` applicable-rule-set completeness;
36. runtime observation `!=` protocol authority.

These non-mappings preserve the formal, implementation, operational, application and privacy boundaries. They do not manufacture any missing positive identity.

## 21. Artifact and Deployment-Binding Observations

The I164 `ZK_ARTIFACTS_MANIFEST.json` independently confirms:

1. `baseline_anchor_tag` is `baseline-v0`, not I164;
2. `baseline_anchor_commit` is `e02aacdc0f10e6919d8a759d8829758b58e0367e`, not the I164 commit;
3. manifest public-input order is `petitionId`, `nullifier`, `membershipRoot`;
4. active verifier-facing order is `nullifier`, `petitionId/actionId`, `membershipRoot`;
5. canonical R1CS, WASM and ZKey paths named by the manifest are absent from the I164 archive;
6. tracked runtime WASM and ZKey copies match their manifest hashes;
7. manifest and archived I164 golden-proof hashes differ;
8. manifest and archived I164 proof-hook hashes differ;
9. manifest and archived I164 sign-button hashes differ.

Exact differing values:

| Candidate | Manifest SHA-256 | Archived I164 SHA-256 |
|---|---|---|
| Golden proof | `7d81531f80ad85682f2673bd0abce43becfd9a416d240d6eba430a2362d2f6fa` | `01360c724f748b1630b6605bf7464af585643a0d87fcbbb2a21e3fa3025a63b7` |
| Proof hook | `e2620d78620e2b0b8fe7a9f316c057747ce695e9a04d37f4e1c455e25609d61f` | `8df56093b0a5a3ed8121e3cbe45761d0cfc967bc0fcdd108222944f5901a575a` |
| Sign button | `1b0df4df7706acbcde2adb76fb4b86a9991d9eb1305d0cc41084248204704189` | `16faf8dba309411ebc40ae00c66cbfda4b2e32e48c18b46d422bcffc7c1e96f2` |

Engineering[193] correctly bounds these as source-mapping observations only.

They do not determine an implementation defect, evidence availability or sufficiency, requirement satisfaction or failure, security, compatibility, conformance, certification or operational readiness.

They prevent the manifest from being promoted into a complete exact I164 action-type, applicable-rule-set or Evaluation-context ledger.

## 22. Material Unresolved Relationships

Engineering[194] independently confirms every material unresolved relationship:

| Relationship | Preserved unresolved basis |
|---|---|
| Complete formal action-type inventory | implementation operations are not exhaustively classified as formal action types |
| Protocol Action occurrence identity | accepted A05 work preserves `U-ACTION-IDENTITY` |
| Authoritative Action admission | accepted A05 work preserves `U-ACTION-ADMISSION` |
| Repeated-presentation equivalence | accepted A05 work preserves `U-RETRY` |
| Complete bounded Evaluation context | no complete context identity or boundary is represented |
| Complete applicable rule set | `U-RULESET` remains unresolved |
| Accepted-root evaluation | `U-ROOT` remains unresolved |
| Complete proof-rule inventory | proof components lack complete action/context assignment |
| Complete non-proof-rule inventory | guards lack generation-derived completeness |
| Exact rule-to-check assignment | several checks lack an exact formal rule assignment |
| Evaluation start and completion | no authoritative boundaries are declared |
| Complete validity basis | proof and non-proof components are not composed into complete RF-18 validity |
| Cross-context validity comparison | no complete relationship resolves `PE-RULE-013` |
| Complete negative-obligation coverage | class-specific exclusions cannot establish universal coverage |
| Complete privacy-surface review | `U-PRIVACY-REVIEW` remains material |
| Complete deployment binding | candidates do not form one exact current I164 rule/context ledger |
| Formal Determination identity | revert, mutation, event, response and persistence cannot manufacture it |

The following named unresolved coordinates remain preserved:

- `U-ACTION-IDENTITY`;
- `U-ACTION-ADMISSION`;
- `U-RETRY`;
- `U-RULESET`;
- `U-ROOT`;
- `U-PRIVACY-REVIEW`.

Each independently blocks complete construction where required.

## 23. Privacy and Neutral-Naming Review

The reviewed candidate surfaces include names, fields, comments, tests, logs, diagnostics, routes, persistence, deployment material and documentation.

The preserved privacy rule is:

**Private actors, public actions.**

The independently confirmed bounded privacy relationships are:

- `memberSecret` remains private local proof-construction material;
- the nullifier derives from `memberSecret`, the action-context value and `SIGN_DOMAIN`;
- uniqueness state is keyed by `(petitionId/actionId, nullifier)`;
- the nullifier is not promoted into actor or reusable participant identity;
- the ignored admission compatibility field is supplied and emitted as zero on the active relay path;
- the signing indexer omits admission commitment;
- the signature schema removes the admission-commitment column;
- relay success and error logs omit submission values and topology;
- application, transport, transaction, event and persistence coordinates remain role-bounded.

Operational IP keys, relayer wallets, seed, slot, domain, transaction coordinates, event coordinates, database coordinates and application state are not promoted into formal actor identity, Action identity, rule applicability or protocol validity.

The class-specific boundaries do not establish complete baseline-wide negative-obligation coverage while the positive Action, action-type, Evaluation-context and rule-set identities remain unresolved.

Engineering[193] introduces no actor identity, wallet identity, sponsor identity, funding identity, admission identity, transport identity, topology identity or cross-action identity.

No forbidden linkage or actor provenance is introduced.

## 24. Complete-Package Construction Review

Engineering[193] required:

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

Independent result:

| Required term | Review result |
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

The package is conjunctive.

Multiple independently required terms remain unresolved or incomplete.

Therefore Engineering[193] correctly applied the construction rule and correctly refused partial terminal acceptance.

## 25. Row-State and Arithmetic Preservation

The nine reviewed-current bounded A04 rows remain bounded:

1. `PE-VALID-001`;
2. `PE-VALID-002`;
3. `PE-VALID-004`;
4. `PE-VALID-008`;
5. `PE-VALID-010`;
6. `PE-VALID-011`;
7. `PE-RULE-009`;
8. `PE-RULE-010`;
9. `PE-RULE-011`.

The 16 selected A04 rows remain `still-ambiguous`:

1. `PE-VALID-003`;
2. `PE-VALID-005`;
3. `PE-VALID-006`;
4. `PE-VALID-007`;
5. `PE-VALID-009`;
6. `PE-VALID-012`;
7. `PE-RULE-001`;
8. `PE-RULE-002`;
9. `PE-RULE-003`;
10. `PE-RULE-004`;
11. `PE-RULE-005`;
12. `PE-RULE-006`;
13. `PE-RULE-007`;
14. `PE-RULE-008`;
15. `PE-RULE-013`;
16. `PE-RULE-012`.

No A04 evidence-path transition occurs.

All 704 non-A04 rows remain unchanged.

The reviewed-current totals remain:

| State | Rows |
|---|---:|
| bounded | 217 |
| still-ambiguous | 268 |
| missing-evidence-path | 0 |
| not-required | 244 |
| total | 729 |

The arithmetic reproduces:

`217 + 268 + 0 + 244 = 729`

## 26. Scope and Non-Effects

Engineering[194] does not:

- modify or correct Engineering[193];
- modify any predecessor artifact;
- reopen or weaken a bounded A04 row;
- perform evidence-path reclassification;
- transition an A04 row;
- alter a non-A04 row;
- reopen A01, A02, A03 or A05;
- resolve A05 through A20;
- manufacture a formal rule identity;
- manufacture an action type;
- manufacture an Evaluation context;
- manufacture an applicable rule set;
- infer completeness from check presence;
- promote proof verification into protocol validity;
- promote protocol validity into acceptance or other consequences;
- promote an operational boundary into authoritative Action admission;
- promote a revert, event, mutation, response, diagnostic or persisted observation into formal Determination;
- determine evidence availability or sufficiency;
- perform requirement assessment;
- produce a requirement result;
- determine an implementation defect;
- perform a security assessment;
- determine compatibility, conformance, certification or operational readiness;
- modify `STATE.md`;
- modify Profile V2;
- modify I164 or implementation code;
- rewrite a tag;
- create Profile V3;
- create a protocol generation or publication occurrence;
- create deployment or runtime evidence;
- encode actor identity or provenance;
- introduce wallet, sponsor, funding, admission, transport, topology or cross-action linkage;
- or imply that Speak-up-appV3 defines or owns the Privacy Engine.

## 27. Material-Blocker Determination

No material source blocker was identified.

No material structural blocker was identified.

No material identity blocker was identified.

No material mapping blocker was identified in Engineering[193]'s negative complete-package conclusion.

No material completeness blocker was identified in its preservation of unresolved terms.

No material privacy blocker was introduced by Engineering[193].

No material authority blocker was identified.

No material scope blocker was identified.

No arithmetic blocker was identified.

The absence of a blocker in Engineering[193] does not resolve the underlying A04 ambiguities. It confirms that Engineering[193] correctly preserved them.

## 28. Canonical Final Review Payload

The canonical final-review payload is the exact UTF-8 sequence strictly between the begin-marker and end-marker lines, joined by LF characters with no trailing LF:

canonical-final-review-payload-begin
format=PRIVACY-ENGINE-I164-A04-VALIDITY-RULE-RULE-SET-ACTION-TYPE-EVALUATION-CONTEXT-MAPPING-DETERMINATION-INDEPENDENT-REVIEW/1
engineering-slice=194
review-date=2026-08-27
reviewed-engineering-slice=193
final-review-result=accepted
protocol-authority=published-privacy-engine-protocol-generation
implementation-subject=Speak-up-appV3-I164
implementation-is-protocol=no
formal-corpus-sha256=4c3d8f46086dfac1bad7efad3b01afd8a57de4f6c8754e4836697895e61e04e1
formal-corpus-files=113
formal-corpus-git-archive-comment=845794ec5432469a1595d41f80f6b87d0191d32b
implementation-archive-sha256=7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847
i164-commit=003e984ea73a2dede092443893dfbc9e74121e14
i164-tree=6271b80f2fa6167961e18c5b4c229d25374497a7
i164-parent=5e12cca624ffccf43637de4b9dc42de4af3979bc
i164-tracked-paths=308
i164-blobs=305
i164-gitlinks=3
reconstructed-i164-tree=6271b80f2fa6167961e18c5b4c229d25374497a7
git-provenance-format=PRIVACY-ENGINE-HANDOVER-GIT-PROVENANCE/1
git-provenance-records=26
git-provenance-sha256=b808c078679ab1ec1dd114c3101c54959aee3a96fa0f8c5bb3fbb7f2afc10022
provenance-local-engineering-refs-verified=26
provenance-remote-engineering-refs-verified=26
provenance-raw-commit-identities-reproduced=26
provenance-changed-file-identities-verified=30
generic-tag-ref-in-provenance=none
engineering-192-artifact-sha256=874f8dc5c32f4f89e23441dcb897251621e164c4ddc9dc36f26358105b8be833
engineering-192-canonical-rereview-payload-length=6324
engineering-192-canonical-rereview-payload-sha256=5e9175730af337ba46911ba11c3d477c6f893b6e68f70f809ef9c6a2f7c4b3b3
engineering-192-final-review-result=accepted
engineering-192-a03-effect=complete-selected-a03-mapping-package-not-constructible
engineering-192-a03-transition-count=0
engineering-193-commit=845794ec5432469a1595d41f80f6b87d0191d32b
engineering-193-tree=27e62a8ee45e5d3ed8f3974f69b0be2bc3ac4f58
engineering-193-parent=3bc4086267e37384cb19d244f56ebfe177a74666
engineering-193-raw-commit-payload-length=304
engineering-193-changed-file-count=1
engineering-193-artifact-sha256=4b49dcdfeaf0a98e456471c0be9961cc5661a601a0a57e79b3724e3e90573a2a
engineering-193-artifact-git-blob=40702c845e47f8c5218068c0e5cf3a91ab090a77
engineering-193-artifact-length=41828
engineering-193-artifact-lines=779
engineering-193-canonical-determination-payload-length=3311
engineering-193-canonical-determination-payload-sha256=ebb4e4d2ae79468f034737e20411160c5d1858750ca1d0e3460385530c395784
reviewed-current-evidence-path-basis=engineering-187-accepted-by-engineering-188
reviewed-current-totals=217/268/0/244
selected-group=A04
guarded-a04-rows=25
guarded-profile-row-hashes-verified=25
guarded-order-preserved=yes
pe-rule-013-before-pe-rule-009=yes
preserved-bounded-a04-rows=PE-VALID-001,PE-VALID-002,PE-VALID-004,PE-VALID-008,PE-VALID-010,PE-VALID-011,PE-RULE-009,PE-RULE-010,PE-RULE-011
preserved-still-ambiguous-a04-rows=PE-VALID-003,PE-VALID-005,PE-VALID-006,PE-VALID-007,PE-VALID-009,PE-VALID-012,PE-RULE-001,PE-RULE-002,PE-RULE-003,PE-RULE-004,PE-RULE-005,PE-RULE-006,PE-RULE-007,PE-RULE-008,PE-RULE-013,PE-RULE-012
engineering-169-anchor-rows-verified=35
engineering-193-principal-and-additional-anchor-failures=0
complete-action-type-inventory=unresolved
complete-bounded-evaluation-context-inventory=unresolved
complete-applicable-rule-set-inventory=unresolved
complete-proof-rule-inventory=incomplete
complete-non-proof-rule-inventory=incomplete
exact-rule-to-implementation-assignments=incomplete
exact-rule-context-relationships=incomplete
exact-candidate-anchors=verified
complete-negative-obligation-coverage=incomplete
privacy-preserving-individual-boundaries=supported
complete-privacy-coverage=unresolved
supplied-root-inclusion-equals-accepted-root-status=no
active-signing-path-accepted-root-read=no
u-action-identity=unresolved
u-action-admission=unresolved
u-retry=unresolved
u-ruleset=unresolved
u-root=unresolved
u-privacy-review=unresolved
formal-protocol-rule-equals-implementation-check=no
successful-proof-verification-equals-complete-evaluation=no
proof-valid-equals-protocol-valid=no
implementation-admission-equals-authoritative-action-admission=no
implementation-outcome-equals-formal-determination=no
manifest-observations-bounded-to-source-mapping=yes
private-actors-public-actions=preserved
actor-identity-or-provenance-introduced=no
partial-terminal-acceptance-created=no
a04-evidence-path-transition-performed=no
non-a04-row-modified=no
reviewed-current-totals-changed=no
evidence-availability-determined=no
evidence-sufficiency-determined=no
requirement-assessment-performed=no
requirement-result-produced=no
implementation-defect-determined=no
security-assessment-performed=no
compatibility-conformance-certification-or-readiness-determined=no
material-source-structural-identity-mapping-completeness-privacy-authority-scope-or-arithmetic-blocker=no
accepted-substantive-conclusion=complete-selected-a04-mapping-package-not-constructible
canonical-final-review-payload-end

Canonical final-review payload length:

`4943` bytes.

Canonical final-review payload SHA-256:

`2e0c0eb69b4e2db691c78aa188619f6b2d43b52b242cc5c246416f8aa6d40d43`

## 29. Final Review Determination

Engineering[193] correctly identifies exact I164 components without promoting them into formal rule identity, action type, complete Evaluation, protocol validity, authoritative Action admission or Determination.

It correctly preserves the missing action-type, action-occurrence, admission, repeated-presentation, Evaluation-context, applicable-rule-set, accepted-root, complete validity, privacy-review, deployment-binding and Determination relationships.

It correctly applies the conjunctive complete-package rule.

It introduces no forbidden actor identity or linkage.

It creates no partial terminal acceptance.

It performs no evidence-path transition.

The nine bounded and 16 `still-ambiguous` A04 rows remain unchanged.

All non-A04 rows remain unchanged.

The reviewed-current totals remain:

`217 / 268 / 0 / 244`

The accepted substantive conclusion remains:

**complete selected A04 mapping package not constructible**

Engineering[194] final review result:

**accepted**

Protocol authority remains with the published Privacy Engine protocol generation.
