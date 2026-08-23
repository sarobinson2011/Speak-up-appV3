# Privacy Engine I164 Protocol Action Occurrence Identity, Admission and Repeated-Presentation Mapping Determination V1

Determination date: 2026-08-22.

STATE.md remains the single canonical development authority.

Protocol authority always remains with the published Privacy Engine protocol generation.

## 1. Purpose and Status

This record determines whether fixed implementation baseline I164 contains an exact, stable and evidence-supported implementation-owned mapping for:

- one Protocol Action occurrence;
- the boundary at which a candidate is admitted as that occurrence for authoritative Evaluation;
- and the treatment of repeated presentations, retries, fallback attempts and uncertain transport outcomes.

The selected unresolved relationships are:

- `U-ACTION-IDENTITY`;
- `U-ACTION-ADMISSION`;
- `U-RETRY`.

Engineering[181] is a mapping determination only.

It is not:

- an acceptance review;
- evidence-path reclassification;
- requirement assessment;
- a requirement result;
- an implementation-defect determination;
- a security assessment;
- a compatibility, conformance, certification or operational-readiness determination;
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
| Formal-corpus files | 100 distinct files |
| Formal-corpus SHA-256 | `143dce1289748b9d58af3d20c6e083e52e00cf502c9e27601cc711c7d5313e91` |
| Implementation archive SHA-256 | `7932bbee3c099f10ae6d4c6632f6d090bd797ddcd6adc3506c72a338eb226847` |
| Git-provenance SHA-256 | `079a5337824af7ff22d369bcddbbb1d624fcb20603688834e371ec3bfabd85e1` |
| Provenance format | `PRIVACY-ENGINE-HANDOVER-GIT-PROVENANCE/1` |

The provenance record remains untracked handover metadata only.

It is not protocol documentation, an implementation artifact, protocol authority, mapping authority, acceptance authority, reclassification authority, review authority, requirement evidence or a requirement result.

## 4. Fixed I164 Baseline

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

Every blob path, blob SHA-256, Git blob identity, mode and tree position was independently verified.

Engineering[164] and Engineering[169] through Engineering[180] were independently verified for:

- tag-object type;
- local ref;
- remote ref;
- resolved commit;
- resolved tree;
- parent;
- exact raw commit payload;
- independently reproduced commit identity;
- every changed-file Git blob;
- every changed-file SHA-256;
- and equality of local ref, remote ref and resolved commit.

Historical overwritten Engineering[171] and Engineering[175] bytes were independently reconstructed and matched their immutable tagged identities.

## 5. Guarded Authority and Evidence Chain

The following identities remain guarded:

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
| Engineering[173] correction record | `df1346947f347bb1c89569bafeb64fcee467680f88de5b4e318d9f0c7f97c1d9` |
| Engineering[174] | `ba5b8d9c6512e36f7d0d3b0e0aedd195ac0e1652cb0d7bfeeef2f17c0ab44b1f` |
| Immutable Engineering[175] | `1eb8ed90926975001e1976ad4e05edbb3e81f70aa703754e053cf1f768449085` |
| Corrected declaration | `aebc191a9b723c3397dc41c7471fdac48a0e11ae9969511d79205334cc40eeef` |
| Engineering[176] | `fc0a4fef49c3a8db3b8affd79eebea051d30a9ee2c77291af8d0c157da4e8a6c` |
| Engineering[177] correction record | `f4ee5e9d86a2d75d9c524107f2c15680acc20b11a62971aade3171ad027fe2ca` |
| Engineering[178] | `488a419790d202ddb667fb968c945041561685dcf01223f3185402e2890c429e` |
| Engineering[179] | `d56e8dfa2a7489fe366798d78ce903874807773729090750144c096307503b64` |
| Engineering[180] | `622eb3746ee15b25bc278a903d4a76cb593a18823afdf417b407059202f5dc66` |

No guarded artifact is modified by Engineering[181].

## 6. Engineering[180] Reviewed-Current Basis

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

The complete 729-row transition serialization was independently reconstructed as:

`identifier|L174-state|L179-state|profile-row-sha256`

It contains:

- 729 rows;
- 729 unique identifiers;
- exactly one changed row;
- `PE-SUBJ-010: still-ambiguous -> bounded`;
- no other changed row;
- LF row separators;
- no trailing LF;
- and SHA-256 `ac5ba6f99e12ee2581d885f044b8186cc950d8c91289d70a34781b473887295c`.

The reviewed-current totals entering Engineering[181] are:

| State | Rows |
|---|---:|
| bounded | 217 |
| still-ambiguous | 268 |
| missing-evidence-path | 0 |
| not-required | 244 |
| **Total** | **729** |

## 7. Governing Formal Action Boundary

A candidate effort is not automatically a Protocol Action occurrence.

The governing sequence is:

> attempts(X, candidateA)  
> `!=` Protocol Action occurrence
>
> admittedForEvaluation(candidateA)  
> `->` instantiates(candidateA, A)
>
> instantiates(candidateA, A)  
> `->` one bounded Protocol Action occurrence exists

A complete implementation-owned mapping therefore requires all three of:

1. a stable positive identity function for `A`;
2. an exact authoritative admission boundary;
3. a rule determining whether repeated authoritative presentations concern the same `A` or distinct occurrences.

Operational similarity, identical fields, transport continuity, uniqueness enforcement or downstream observation cannot silently supply those relationships.

## 8. Exact Engineering[178]-Accepted Relationship Evidence

The corrected declaration retains draft wording because Engineering[177] was a correction occurrence. Engineering[178] independently accepted the following records only with their exact treatments, limitations, non-mappings, dependencies and privacy boundaries.

| Record | Treatment and affected rows | Exact accepted relationship | Explicit non-mappings | Limitations and unresolved dependencies |
|---|---|---|---|---|
| `I164-SR-002` | Proposed supported relationship; `PE-SUBJ-001`, `006`, `007`, `008`, `009` | Ordered public set `nullifier`, `petitionId/actionId`, `membershipRoot` is preserved across circuit output, verifier input, relay payload and contract calldata | Public values are not Private Actor, wallet, sponsor, funding, admission, transport, ownership or reusable participant identities; value continuity does not establish occurrence continuity | Does not establish accepted-root status, complete Action identity or complete Evaluation; deployment and runtime binding not newly produced |
| `I164-SR-003` | Supported component plus unresolved complete relationship; `PE-SUBJ-001`, `002`, `004`, `006`, `007`, `008`, `009`, `010` | Proof submission, frozen operational submission and ABI-decoded `signPetitionWithZKProof` invocation are exact components | UI request, proof generation, relay request, transport attempt, transaction, event and application target are not automatically `A`; function or route naming is not `O` | Contract invocation is a candidate enforcement presentation, not a declared admission boundary; no stable `id(A)` or repeated-presentation rule; `U-ACTION-IDENTITY`, `U-ACTION-ADMISSION`, `U-RETRY`, `U-RULESET`, A02–A05 remain unresolved |
| `I164-SR-004` | Supported component plus unresolved complete relationship; `PE-SUBJ-001`, `002`, `003`, `006`, `007`, `008`, `009` | Circuit constraints, sequential guards, verifier result, revert/fallthrough and downstream observations are exact components | Proof verification is not complete Evaluation; response, revert, mutation, receipt, event, reconciliation and persistence are not Determination | No stable Evaluation start, completion, `id(E)` or `id(D)`; `U-RULESET`, `U-ROOT`, `U-EVAL-IDENTITY`, `U-EVAL-BOUNDARY`, `U-EVAL-REJECTION`, `U-DETERMINATION`, `U-CLASSIFICATION` remain unresolved |
| `I164-SR-006` | Supported component plus unresolved complete relationship; `PE-SUBJ-001`, `002`, `005`, `006`, `007`, `008`, `009`, `010` | Boolean mutation, event emission, normalized observation and persistence projection are exact state-change and observation components | Execution attempt is not `U`; mutation is not automatically `T`, `U`, commitment or public consequence; event is not complete history | No stable `id(T)` or `id(U)`; no complete transition mapping, authorization, commitment or cardinality; A10–A17, `U-DETERMINATION` and `U-CLASSIFICATION` remain unresolved |
| `I164-SR-011` | Proposed supported relationship; `PE-SUBJ-001`, `006`, `007`, `008`, `009` | Shared `petitionId/actionId` serialization preserves distinct protocol-context and application-target roles | Petition, signature, product count, UI success and application truth are not Action identity, validity, Determination, Published Result or Private Actor identity | Application-role separation does not define the missing Action occurrence; A20 remains unresolved |
| `I164-SR-012` | Explicit proposed non-mapping; `PE-SUBJ-001`, `002`, `003`, `005`, `006`, `007`, `008`, `009` | Request, frozen payload, seed, permutation, domain attempt, transaction, response, event, reconciliation, indexer record and row are operational or downstream representations | Request or attempt is not `A`; transaction is not `D`; execution attempt is not `U`; event is not history; row is not protocol authority | Payload preservation does not settle retry equivalence or occurrence continuity; `U-RETRY`, `U-ACTION-IDENTITY`, `U-DETERMINATION`, A05, A07, A11, A16 and A20 remain unresolved |
| `I164-SR-013` | Supported component plus unresolved complete relationship; `PE-SUBJ-001` through `009` | Public values, route values, ABI fields, storage keys, transaction coordinates, event fields and persistence fields are exact representations | Nullifier, action context, root, proof, hash, transaction, event, database key and `T-I164-ANONYMOUS-PUBLIC-ACTION` are not formal occurrence identifiers | No stable `id(A)`, `id(E)`, `id(D)` or `id(U)`; `U-ACTION-IDENTITY`, `U-EVAL-IDENTITY`, `U-DETERMINATION` and A11 remain unresolved |
| `I164-SR-014` | Explicit proposed non-mapping; `PE-SUBJ-001`, `006`, `007`, `008`, `009`, `010` | No I164 implementation label is proposed as a new first-class protocol subject | M2, REFLECT, TEMPEST, relay, slot, domain, request, transaction, event, state item, persistence row, application object and `T-I164-ANONYMOUS-PUBLIC-ACTION` are not new protocol subjects | Formal ontology remains governed solely by the published protocol generation; the record neither expands nor narrows that inventory |

Engineering[181] preserves these accepted boundaries and does not convert supported components into unaccepted positive identities.

## 9. Exact Fixed I164 Candidate Sequence

The fixed candidate path is:

1. `normalizeInputs` validates local proof inputs.
2. `normalizeMerkleToMatchRoot` selects a local path convention reproducing the supplied root.
3. `generateProof` derives the action-local nullifier.
4. `snarkjs.groth16.fullProve` constructs proof material.
5. local `groth16.verify` checks that proof material.
6. `handleM2Sign` normalizes proof and public-signal representations.
7. `hasSignedPetition` performs a pre-submission used-state observation.
8. optional verifier preflight tests candidate public-signal orderings.
9. `relayPayload` is serialized into the UI relay request.
10. `POST /sign` validates request shape and public-signal coherence.
11. indexer freshness and relay-side used-state are observed.
12. `relaySubmission` adds fixed-zero `admissionCommitment`.
13. `freezeRelaySubmission` freezes the operational submission object.
14. `deriveTempestSeed` hashes the exact frozen submission preimage.
15. `deriveTempestPermutation` selects deterministic slot order.
16. each selected slot maps to an execution domain.
17. `signPetitionWithZKProof` submits one transport/execution attempt.
18. controlled or transport failure may trigger reconciliation and fallback.
19. contract entry begins one candidate enforcement presentation.
20. petition existence and nullifier-used state are checked.
21. the configured verifier and proof result are checked.
22. function arguments are checked against public signals.
23. `usedSignNullifier[petitionId][nullifier]` is mutated to `true`.
24. `PetitionSigned` is emitted.
25. the transaction object or reconciled state is returned operationally.
26. the relay returns `{ok, alreadySigned, txHash?}`.
27. the UI records an application-facing outcome.
28. the event is normalized with block, transaction and log coordinates.
29. the observation is inserted idempotently into persistence.
30. the application read model derives its count.

The sequence is exact operational evidence.

It does not itself select the formal Action-occurrence boundary.

## 10. Candidate Coordinate Examination

### CAND-A01 — Local candidate construction and proof generation

| Field | Determination |
|---|---|
| Exact paths | `frontend/src/hooks/useZKProof.js`; `frontend/src/components/M2SignButton.jsx` |
| Git objects | `985e8adb8410a134fa010d2fa49ee179e47edfb5`; `42d27697f8ee796210f649257c94247220728f99` |
| SHA-256 | `8df56093b0a5a3ed8121e3cbe45761d0cfc967bc0fcdd108222944f5901a575a`; `16faf8dba309411ebc40ae00c66cbfda4b2e32e48c18b46d422bcffc7c1e96f2` |
| Exact symbols and shape | `generateProof`; `handleM2Sign`; `{proof:{pA,pB,pC,publicSignals}, nullifier}` |
| Lifecycle and class | local preparation; candidate construction |
| Action identity | no; local invocation state is not serialized as stable `id(A)` |
| Action admission | no; construction and local verification precede authoritative evaluation |
| Repeated-presentation distinction | no; repeated construction has no formal equivalence or distinctness rule |
| Explicit non-mappings | candidate construction, proof generation and UI activity are not Action occurrences |
| Limitation | no occurrence coordinate survives as a declared Action identifier |
| Privacy boundary | private witness material must remain local and must not become public actor identity |
| Conclusion | supported candidate construction only |

### CAND-A02 — Ordered public values and proof material

| Field | Determination |
|---|---|
| Exact paths | `zk/v3-groth16/circuits/sign_petition.circom`; `frontend/src/hooks/useZKProof.js` |
| Git objects | `165ed8cfa1029dd0a937ab6e885af020fbf991e5`; `985e8adb8410a134fa010d2fa49ee179e47edfb5` |
| SHA-256 | `a64783f8873df0c9dda7f7e44607e076f0b2af94c9cd609e4619e4b0fbcf2e02`; `8df56093b0a5a3ed8121e3cbe45761d0cfc967bc0fcdd108222944f5901a575a` |
| Exact symbols and shape | `SignPetition`; `nullifier`; `component main {public [petitionId, membershipRoot]}`; ordered values `[nullifier, petitionId/actionId, membershipRoot]` |
| Lifecycle and class | proof relation; candidate public representation |
| Action identity | no; public inputs and proof material do not constitute the occurrence |
| Action admission | no; relation construction does not instantiate an admitted Action |
| Repeated-presentation distinction | no; value equality preserves roles only |
| Explicit non-mappings | nullifier, action context, root and proof are not formal occurrence identifiers |
| Limitation | no I164 rule guarantees that proof representation equality or inequality determines Action equality |
| Privacy boundary | nullifier remains action-local and must not become participant identity |
| Conclusion | supported public-value relationship only |

### CAND-A03 — UI relay request

| Field | Determination |
|---|---|
| Exact path | `frontend/src/components/M2SignButton.jsx` |
| Git object | `42d27697f8ee796210f649257c94247220728f99` |
| SHA-256 | `16faf8dba309411ebc40ae00c66cbfda4b2e32e48c18b46d422bcffc7c1e96f2` |
| Exact symbols and shape | `relayPayload`; `fetch("/api/relay/sign")`; `petitionId`, `nullifier`, `pA`, `pB`, `pC`, `pubSignals` |
| Lifecycle and class | application-to-relay transport |
| Action identity | no request identifier exists; request existence is explicitly not Action identity |
| Action admission | no; HTTP submission is transport |
| Repeated-presentation distinction | no; another request may repeat or vary the payload without a formal Action rule |
| Explicit non-mappings | UI request and application target are not Action occurrences |
| Limitation | UI disabling and local status are application controls, not protocol identity |
| Privacy boundary | request context and delivery metadata must not identify the actor |
| Conclusion | transport representation only |

### CAND-A04 — Relay validation and pre-dispatch checks

| Field | Determination |
|---|---|
| Exact path | `backend/src/routes/relay.js` |
| Git object | `23a4d5f37a5dafa2cfd39030e1d42bff9807e3e7` |
| SHA-256 | `1f748b519358c4d4653dfce5d13d6f54cab4a3cd7cb70d8f1937a75a06990f7a` |
| Exact symbols and shape | `router.post("/sign")`; payload-shape checks; public-signal coherence; freshness; `hasSignedPetition`; `relaySubmission` |
| Lifecycle and class | relay request validation and operational gating |
| Action identity | no; route fields and request handling do not establish `id(A)` |
| Action admission | no; the relay does not declare its validation-success point as the authoritative evaluation boundary |
| Repeated-presentation distinction | operational already-used handling only |
| Explicit non-mappings | request acceptance, payload validation and relay dispatch are not formal Action admission |
| Limitation | proof validity and the complete applicable rule set are not authoritatively evaluated at this boundary |
| Privacy boundary | rate-limit and request metadata must not become Action or actor identity |
| Conclusion | supported operational gate only |

### CAND-A05 — Frozen relay submission and TEMPEST seed

| Field | Determination |
|---|---|
| Exact path | `backend/src/services/relayExecution.js` |
| Git object | `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` |
| SHA-256 | `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` |
| Exact symbols and shape | `freezeRelaySubmission`; `encodeTempestSeedPreimage`; `deriveTempestSeed`; exact ABI encoding of submission fields |
| Lifecycle and class | preserved operational submission and deterministic selection input |
| Action identity | no; seed identity is exact-payload identity only and is explicitly not a formal subject identifier |
| Action admission | no; freezing and hashing precede transport execution |
| Repeated-presentation distinction | no; identical seed implies equal encoded payload, not equal Action occurrence |
| Explicit non-mappings | frozen payload and seed are not Action or retry-equivalence identities |
| Limitation | proof or representation differences may alter the seed without establishing a different Action, while equal payloads do not prove one Action |
| Privacy boundary | seed, slot and domain must not expose actor or transport attribution |
| Conclusion | operational determinism only |

### CAND-A06 — Slot, domain and fallback attempts

| Field | Determination |
|---|---|
| Exact path | `backend/src/services/relayExecution.js` |
| Git object | `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` |
| SHA-256 | `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` |
| Exact symbols and shape | `deriveTempestPermutation`; `selectDomainHandleForSlot`; `dispatchRelayExecution`; `shouldContinueRelayExecution` |
| Lifecycle and class | transport selection, execution attempt and fallback |
| Action identity | no; slot, domain and attempt coordinates are operational |
| Action admission | no; attempting delivery is not admission |
| Repeated-presentation distinction | only sequential fallback for one frozen submission call is defined operationally |
| Explicit non-mappings | transport attempt and execution attempt are not Action or State Transition occurrences |
| Limitation | the loop does not declare whether multiple authoritative presentations concern one Action or distinct Actions |
| Privacy boundary | topology and fallback path must not become actor or Action provenance |
| Conclusion | bounded operational fallback only |

### CAND-A07 — Contract invocation and entry

| Field | Determination |
|---|---|
| Exact path | `contracts/src/PetitionRegistry.sol` |
| Git object | `a593c4023fc1ce9c835013a5ad40a310e5bfd032` |
| SHA-256 | `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` |
| Exact symbol and shape | `signPetitionWithZKProof(uint256,bytes32,bytes32,uint256[2],uint256[2][2],uint256[2],uint256[3])` |
| Lifecycle and class | candidate on-chain enforcement presentation |
| Action identity | no; calldata and invocation do not supply stable `id(A)` |
| Action admission | not established; entry is not declared as authoritative admission |
| Repeated-presentation distinction | no; each invocation is distinguishable operationally but formal occurrence equality is undeclared |
| Explicit non-mappings | invocation and transaction are not automatically Action occurrences |
| Limitation | contract entry precedes guards but contains no implementation-owned instantiation or admission declaration |
| Privacy boundary | public invocation must not become Private Actor identity |
| Conclusion | strongest candidate enforcement presentation, but not a mapped admission boundary |

### CAND-A08 — Contract guards, verifier result and coherence checks

| Field | Determination |
|---|---|
| Exact paths | `contracts/src/PetitionRegistry.sol`; `contracts/src/v3/Groth16Verifier.sol` |
| Git objects | `a593c4023fc1ce9c835013a5ad40a310e5bfd032`; `bf3bd28b1e89e8672219aa5aea6e54605d1b5bfe` |
| SHA-256 | `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26`; `b1216366353f3dbf478e1e03add31077bbe4bc76d5a4e40aaba574cd5841bd87` |
| Exact symbols and shape | petition existence; nullifier-used guard; `verifyProof`; nullifier/public-signal equality; action-context/public-signal equality |
| Lifecycle and class | enforcement checks and bounded verification components |
| Action identity | no; checks evaluate representations rather than identify the occurrence |
| Action admission | no exact boundary; selecting any intermediate guard would infer an undeclared start point |
| Repeated-presentation distinction | used-state check distinguishes unused from already used, not same Action from distinct Action |
| Explicit non-mappings | proof verification is not complete Evaluation; Boolean result is not Action identity or Determination |
| Limitation | `U-RULESET`, `U-ROOT`, Evaluation identity and Evaluation boundary remain unresolved; supplied-root proof relation must not be promoted into accepted-root status |
| Privacy boundary | verification fields must not reconstruct actor identity |
| Conclusion | supported evaluation components only |

### CAND-A09 — Action-local uniqueness key and state mutation

| Field | Determination |
|---|---|
| Exact path | `contracts/src/PetitionRegistry.sol` |
| Git object | `a593c4023fc1ce9c835013a5ad40a310e5bfd032` |
| SHA-256 | `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26` |
| Exact symbols and shape | `usedSignNullifier[petitionId][nullifier]`; `hasSignedPetition`; assignment to `true` |
| Lifecycle and class | authoritative state item and mutation |
| Action identity | no; `(petitionId/actionId, nullifier)` is an action-local uniqueness-state key, explicitly not formal occurrence identity |
| Action admission | no; mutation occurs after candidate checks and cannot retroactively instantiate an Action at the start of Evaluation |
| Repeated-presentation distinction | establishes that later use of the same key is already used; does not classify the later presentation as the same or a distinct Action |
| Explicit non-mappings | state mutation is not automatically Action, Transition, State Transition, Determination or classification |
| Limitation | uniqueness-state equivalence is weaker than occurrence equivalence |
| Privacy boundary | key remains action-local and must not become reusable participant identity |
| Conclusion | strongest stable uniqueness coordinate, but not `id(A)` |

### CAND-A10 — Transaction result and transaction replacement

| Field | Determination |
|---|---|
| Exact path | `backend/src/services/relayExecution.js` |
| Git object | `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` |
| SHA-256 | `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` |
| Exact symbol and shape | returned `{txHash: tx.hash}` |
| Lifecycle and class | transport/execution result |
| Action identity | no; transaction hash is explicitly not Action identity |
| Action admission | no; transaction submission or result is not admission |
| Repeated-presentation distinction | no transaction-replacement identity, nonce-continuity or replacement rule is defined in the selected I164 path |
| Explicit non-mappings | transaction is not Action occurrence or Determination |
| Limitation | generic chain behaviour cannot be imported as an implementation-owned formal relationship |
| Privacy boundary | transaction identity must not become actor or transport provenance |
| Conclusion | operational transaction reference only |

### CAND-A11 — Reconciliation after uncertain transport outcome

| Field | Determination |
|---|---|
| Exact path | `backend/src/services/relayExecution.js` |
| Git object | `1027ce8b4aef36c0e6d33f9ca238cb574c980ddd` |
| SHA-256 | `10bc89bec4d48859bd8d1dcd5c746fa648f22c39a7b3a5ca876c73c75c6acdff` |
| Exact symbol and shape | `reconcileRelayExecutionState`; `hasSignedPetition`; reconciled `{txHash:null}` |
| Lifecycle and class | operational observation after controlled or transport failure |
| Action identity | no; true used-state does not identify the presentation or transaction that caused it |
| Action admission | no; reconciliation occurs after an uncertain attempt |
| Repeated-presentation distinction | no; it cannot prove whether state arose from the current attempt, a fallback attempt or an earlier presentation |
| Explicit non-mappings | reconciliation and response are not Action occurrence or Determination |
| Limitation | observation of the consequence cannot reconstruct occurrence continuity |
| Privacy boundary | reconciliation must not expose topology or actor attribution |
| Conclusion | bounded state reconciliation only |

### CAND-A12 — Event and normalized observation

| Field | Determination |
|---|---|
| Exact paths | `contracts/src/PetitionRegistry.sol`; `backend/src/indexer/petitions/processor.js` |
| Git objects | `a593c4023fc1ce9c835013a5ad40a310e5bfd032`; `b38e89799c61a846025390325f882c2a69ce9759` |
| SHA-256 | `04e3cbddf6356fe6d83b0f2bec0197ee6fce03dbe94f89867ef5f758b3468a26`; `addfa0e87da3c1a94628d30024556fa9ba644df46c78fb27caac7529e18b3437` |
| Exact symbols and shape | `PetitionSigned`; `normalizeEvent`; petition identifier, nullifier, block, transaction and log coordinates |
| Lifecycle and class | event emission and downstream observation |
| Action identity | no; event and chain coordinates identify an observation, not the formal Action occurrence |
| Action admission | no; event follows mutation |
| Repeated-presentation distinction | only one successful event can be observed for the used key; failed or refused presentations remain outside that observation |
| Explicit non-mappings | event is not Action, Determination, complete history or public consequence identity |
| Limitation | an observed successful mutation cannot define the identity of every candidate or rejected occurrence |
| Privacy boundary | event fields must not be expanded into actor provenance |
| Conclusion | downstream public observation only |

### CAND-A13 — Persistence and application read model

| Field | Determination |
|---|---|
| Exact paths | `backend/src/indexer/petitions/handlers.js`; `backend/src/db/repositories/petitions.js`; `backend/migrations/001_ground_truth_indexer_v0.sql` |
| Git objects | `4912bfe988996712f700b1506171f6a8e46ba75e`; `5b65178963e1b9f85100c7f8238de4b69737aabe`; `14b61bd874fe48a2957efa73923c5467dc7ccca4` |
| SHA-256 | `f2f7fab14b9c5c310e823c6c8df8556b894792659dc158658ab9289b69ccdcd7`; `68076c4b5bbd0aa1efc5a5454c180bf9b990af118fda5fc5dc67169babbf828b`; `8f3c0a70b0a5923efbdffd324a0b1c96e202d40217dcd11ba90a2ec78606d31e` |
| Exact symbols and shape | `handlePetitionSigned`; `insertPetitionSignature`; primary key `(tx_hash, log_index)`; unique `(petition_id, nullifier)`; derived count |
| Lifecycle and class | persistence and application projection |
| Action identity | no; database keys identify stored observations |
| Action admission | no; persistence is downstream |
| Repeated-presentation distinction | insertion idempotence distinguishes duplicate observations, not Action-occurrence equality |
| Explicit non-mappings | database row and count are not Action, Protocol State, Determination or protocol authority |
| Limitation | storage uniqueness cannot be promoted into formal occurrence identity |
| Privacy boundary | persistence must not introduce actor, wallet, admission or transport linkage |
| Conclusion | downstream idempotent observation only |

### CAND-A14 — Relay response and UI outcome

| Field | Determination |
|---|---|
| Exact paths | `backend/src/routes/relay.js`; `frontend/src/components/M2SignButton.jsx` |
| Git objects | `23a4d5f37a5dafa2cfd39030e1d42bff9807e3e7`; `42d27697f8ee796210f649257c94247220728f99` |
| SHA-256 | `1f748b519358c4d4653dfce5d13d6f54cab4a3cd7cb70d8f1937a75a06990f7a`; `16faf8dba309411ebc40ae00c66cbfda4b2e32e48c18b46d422bcffc7c1e96f2` |
| Exact symbols and shape | `{ok, alreadySigned, txHash?}`; `onSuccess`; local `alreadySigned` and `success` states |
| Lifecycle and class | operational and application response |
| Action identity | no; response has no stable Action coordinate |
| Action admission | no; response occurs after dispatch, pre-check or reconciliation |
| Repeated-presentation distinction | `alreadySigned` states the used fact only |
| Explicit non-mappings | response, UI success and application truth are not Action identity, Determination or Published Result |
| Limitation | distinct operational paths can yield similar application-facing outcomes |
| Privacy boundary | response must not reveal topology, actor or provenance |
| Conclusion | operational/application outcome only |

## 11. Stable Positive Action-Identity Determination

I164 supplies no stable positive identity function for one Protocol Action occurrence.

The examined coordinates fail as follows:

| Candidate coordinate | Exact supported role | Why it cannot be `id(A)` |
|---|---|---|
| Local invocation or UI state | candidate construction | not stable across lifecycle and not public protocol identity |
| Proof | bounded evidence material | proof is not the Action and proof equality is not occurrence equality |
| Ordered public values | public roles | public inputs do not constitute the occurrence |
| `(petitionId/actionId, nullifier)` | action-local uniqueness state | collapses used-state equality without defining occurrence equality |
| Frozen submission | preserved operational payload | no retry-equivalence rule; representation is not subject identity |
| TEMPEST seed | deterministic payload-selection input | seed, permutation, slot and domain are operational |
| Contract calldata or invocation | enforcement presentation | invocation is explicitly not automatically the Action |
| Transaction hash | transport/execution coordinate | transaction is not Action identity and may not be stable under replacement |
| Mutation | exact state-change component | consequence component is not Action identity |
| Event or chain coordinates | public observation | event is downstream and does not represent every candidate occurrence |
| Database keys | stored-observation identity | persistence is not protocol authority |
| Response | operational/application result | response is not Action identity or Determination |

Therefore no exact identity coordinate, construction function, lifecycle creation point, stability boundary or equality rule can be recorded without manufacturing a relationship prohibited by the accepted evidence.

The required separations remain:

> identity(A)  
> `!=` identity of Private Actor
>
> identity(A)  
> `!=` nullifier identity
>
> identity(A)  
> `!=` request identity
>
> identity(A)  
> `!=` transaction identity
>
> identity(A)  
> `!=` event identity
>
> identity(A)  
> `!=` database identity

Determination:

> `U-ACTION-IDENTITY` remains unresolved.

## 12. Action-Admission Boundary Determination

Before formal admission, I164 contains a candidate represented through local proof material, public values, requests, frozen operational submissions and contract calldata.

Every plausible boundary fails to provide the required exact admission relationship:

| Candidate boundary | Why it is not established as Action admission |
|---|---|
| successful proof construction | local preparation before authoritative Evaluation |
| successful local proof verification | local preflight only |
| UI request creation | application transport representation |
| relay request receipt | transport receipt |
| payload-shape validation | syntactic validation only |
| relay public-signal coherence | bounded representation check only |
| freshness check | operational gating |
| relay used-state check | operational pre-check |
| frozen submission creation | operational preservation |
| TEMPEST dispatch | transport selection |
| transaction submission | transport/execution attempt |
| contract entry | candidate enforcement presentation, not a declared instantiation boundary |
| petition-existence success | one partial guard only |
| nullifier-unused success | one partial state guard only |
| proof-verification success | bounded Evaluation component only |
| public-signal coherence success | bounded component only |
| state mutation | occurs after checks and cannot retroactively define the start of Evaluation |
| event emission | downstream of mutation |
| response, reconciliation or persistence | downstream operational observation |

No source operation declares:

> admittedForEvaluation(candidateA)  
> `->` instantiates(candidateA, A)

Selecting contract entry would infer admission from invocation.

Selecting successful validation or proof verification would merge admission with an Evaluation component.

Selecting mutation would place admission after the checks that would have evaluated the Action and would merge Action admission with a state-change component.

The fixed-zero `admissionCommitment` field is deprecated, ignored and outside the ordered public inputs. It is not Action admission, admission identity or occurrence identity.

The relationship between admission and later Evaluation therefore remains undeclared.

Pre-evaluation refusal, Evaluation failure and rejection also cannot be classified here because their selected relationships remain outside Engineering[181].

Determination:

> `U-ACTION-ADMISSION` remains unresolved.

## 13. Repeated-Presentation and Retry Determination

| Case | Exact I164 behaviour | Formal occurrence result |
|---|---|---|
| Repeated UI submission after local success | UI disables or reports already signed | application control only; unresolved equivalence |
| Repeated UI construction before authoritative state is visible | another proof/request may be produced | no rule determines same or distinct Action |
| Repeated relay request after used state is visible | relay returns `{ok:true, alreadySigned:true}` | used-state observation only; unresolved equivalence |
| Repeated relay request before used state is visible | another deterministic dispatch may begin | concurrent operational presentation; unresolved equivalence |
| Deterministic fallback attempt | same frozen submission proceeds through another selected slot/domain after permitted failure | operational fallback only; not automatically another Action or proven same Action |
| Transaction replacement | no replacement-continuity rule exists in the selected I164 path | unresolved |
| Replayed contract invocation after mutation | authoritative nullifier-used guard reverts | repeated used-key presentation; same-versus-distinct Action remains unresolved |
| Concurrent contract invocations before ordering resolves | chain ordering allows at most one successful used-state mutation | state uniqueness does not define occurrence identity |
| Reconciliation after uncertain transport | reads `hasSignedPetition`; may return `{txHash:null}` | cannot attribute state to one presentation or transaction |
| Later event/indexer observation | records one successful mutation event | observation continuity, not candidate or Action continuity |

I164 establishes:

> same frozen submission within one dispatch call  
> `->` preserved operational payload

It does not establish:

> same frozen submission  
> `->` same Protocol Action occurrence

It also does not establish:

> different proof, seed, request, attempt or transaction  
> `->` different Protocol Action occurrence

Payload equality alone is insufficient.

Used-state equality alone is insufficient.

Transaction, event and persistence equality are insufficient.

Determination:

> `U-RETRY` remains unresolved.

## 14. Indivisibility of the Selected Mapping Package

The selected package requires all three relationships:

> completeActionMapping  
> `=` stableActionIdentity  
> `+` exactAdmissionBoundary  
> `+` repeatedPresentationRule

The independently derived state is:

> stableActionIdentity = unresolved  
> exactAdmissionBoundary = unresolved  
> repeatedPresentationRule = unresolved

Therefore:

> completeActionMapping = not constructible

Supported components cannot produce a partial terminal outcome.

The singular determination is not divided into accepted and rejected sub-packages.

## 15. A01 Relationship Effect Without Reclassification

The Action-occurrence question is potentially relevant to:

| Identifier | Engineering[180] state | Engineering[181] treatment |
|---|---|---|
| `PE-SUBJ-001` | still-ambiguous | potentially affected; not reclassified |
| `PE-SUBJ-002` | still-ambiguous | potentially affected; not reclassified |
| `PE-SUBJ-004` | still-ambiguous | potentially affected; not reclassified |
| `PE-SUBJ-006` | still-ambiguous | potentially affected; not reclassified |
| `PE-SUBJ-007` | still-ambiguous | potentially affected; not reclassified |
| `PE-SUBJ-008` | still-ambiguous | potentially affected; not reclassified |
| `PE-SUBJ-009` | still-ambiguous | potentially affected; not reclassified |
| `PE-SUBJ-010` | bounded | preserved as bounded |

Engineering[181] changes no row state.

The reviewed-current totals remain:

`217 bounded / 268 still-ambiguous / 0 missing-evidence-path / 244 not-required`.

## 16. Preserved Implementation Coordinate and Public Values

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

The nullifier retains its defined action-local public role.

It is not promoted into Private Actor identity or general participant identity.

## 17. Preserved Non-Mappings

The following remain exact:

> candidate construction  
> `!=` Protocol Action occurrence
>
> UI request  
> `!=` Protocol Action occurrence
>
> relay request  
> `!=` Protocol Action occurrence
>
> transport attempt  
> `!=` Protocol Action occurrence
>
> transaction  
> `!=` automatically Protocol Action occurrence
>
> event  
> `!=` Protocol Action occurrence
>
> database row  
> `!=` Protocol Action occurrence
>
> proof verification  
> `!=` complete Protocol Action Evaluation
>
> response or downstream record  
> `!=` Protocol Action Determination
>
> execution attempt  
> `!=` Protocol State Transition occurrence
>
> application object  
> `!=` protocol subject

These prevent unsupported substitution.

They do not create the missing positive mapping.

## 18. Preserved Unresolved Relationships and Ambiguity Groups

Engineering[181] resolves none of the following relationships outside the selected question:

- `U-RULESET`;
- `U-ROOT`;
- `U-EVAL-IDENTITY`;
- `U-EVAL-BOUNDARY`;
- `U-EVAL-REJECTION`;
- `U-DETERMINATION`;
- `U-CLASSIFICATION`;
- `U-PRIVACY-REVIEW`;
- `U-PROVENANCE`.

The selected relationships also remain unresolved:

- `U-ACTION-IDENTITY`;
- `U-ACTION-ADMISSION`;
- `U-RETRY`.

The following ambiguity groups remain outside the selected determination:

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

## 19. Minimum Later Evidence Needed

Revisiting the selected question requires one bounded implementation-owned mapping package containing:

1. an exact public, action-local occurrence coordinate;
2. its construction inputs and creation point;
3. an equality rule identifying exactly one Action occurrence;
4. explicit separation from actor, nullifier, request, proof, transaction, event, state and persistence identity;
5. an exact operation declaring candidate admission to the authoritative Evaluation boundary;
6. the candidate state immediately before admission;
7. the conditions required at admission;
8. the relationship between admission, later Evaluation, pre-evaluation refusal, Evaluation failure and rejection;
9. an exhaustive rule for repeated UI submissions, relay requests, fallback attempts, replacements, replayed invocations, used-state handling and reconciliation;
10. lifecycle-preservation rules across implementation representations;
11. privacy evidence showing no actor, wallet, sponsor, funding, admission, transport, ownership, metadata or cross-action linkage;
12. exact tracked-source or implementation-governance anchors;
13. and later independent review before acceptance.

The later evidence must not obtain completeness by renaming an existing operational coordinate.

Absence of this mapping is not converted into an implementation defect or requirement result.

## 20. Privacy and Neutral-Naming Boundary

The governing rule remains:

> Private actors, public actions.

Engineering[181] creates no:

- Private Actor identity;
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
- or actor-reconstruction path.

Candidate identifiers in this record identify public review material only.

They do not identify a Private Actor or create protocol identity.

## 21. Evidence-Layer Separation

The following distinctions remain mandatory:

> candidate component  
> `!=` formal mapping
>
> formal mapping  
> `!=` accepted mapping evidence
>
> accepted mapping evidence  
> `!=` evidence-path boundedness
>
> evidence-path boundedness  
> `!=` evidence availability
>
> evidence availability  
> `!=` evidence sufficiency
>
> evidence sufficiency  
> `!=` requirement assessment
>
> requirement assessment  
> `!=` requirement result

Engineering[181] creates proposed mapping-determination evidence only.

A later independent review must decide whether to accept this determination.

Only a later separate evidence-path reclassification determination may alter row states or totals.

## 22. Canonical Mapping Determination

The canonical mapping-determination payload is the exact UTF-8 byte sequence between the marker lines below, joined by LF characters with no trailing LF:

canonical-mapping-determination-payload-begin
format=PRIVACY-ENGINE-I164-ACTION-OCCURRENCE-MAPPING-DETERMINATION/1
determination-id=PE-I164-ACTION-OCCURRENCE-IDENTITY-ADMISSION-REPEATED-PRESENTATION-MAPPING-DETERMINATION-2026-08-22
engineering-slice=engineering-181
fixed-implementation-baseline=I164
selected-question=Protocol Action occurrence identity, Action admission and repeated-presentation mapping
selected-relationships=U-ACTION-IDENTITY,U-ACTION-ADMISSION,U-RETRY
mapping-package-constructible=no
u-action-identity=unresolved
u-action-admission=unresolved
u-retry=unresolved
supported-components=construction,proof-generation,public-value-preservation,relay-validation,frozen-submission,deterministic-dispatch,fallback,enforcement-presentation,verification-components,uniqueness-state,mutation,event,reconciliation,observation,persistence,response
affected-a01-rows=PE-SUBJ-001,PE-SUBJ-002,PE-SUBJ-004,PE-SUBJ-006,PE-SUBJ-007,PE-SUBJ-008,PE-SUBJ-009
pe-subj-010-state=bounded
reviewed-current-successor-basis=engineering-179
reviewed-current-totals=217/268/0/244
evidence-path-reclassification-performed=no
requirement-assessment-performed=no
requirement-result-produced=no
implementation-defect-determined=no
privacy-boundary=Private actors, public actions
later-independent-review-required=yes
final-determination=mapping-package-not-constructible-and-selected-relationships-remain-unresolved
canonical-mapping-determination-payload-end

Canonical mapping-determination payload length:

`1359` bytes

Canonical mapping-determination payload SHA-256:

`5c321c1c9c21dc95bf54f6a7ca06e52cc70729890683daae56dbc7c2bce8dc94`

This is exactly one indivisible mapping determination:

> mapping package not constructible and selected relationships remain unresolved

No partial terminal outcome exists.

## 23. Final Determination

I164 contains exact candidate construction, proof, public-value, relay, deterministic fallback, contract-enforcement, uniqueness-state, mutation, event, reconciliation, observation, persistence and response components.

It does not contain an exact implementation-owned relationship that:

- gives one Protocol Action occurrence a stable positive identity;
- identifies the boundary at which a candidate becomes that Action for authoritative Evaluation;
- and determines whether every repeated presentation is the same Action occurrence, a different occurrence or an operational retry only.

Accordingly:

- `U-ACTION-IDENTITY` remains unresolved;
- `U-ACTION-ADMISSION` remains unresolved;
- `U-RETRY` remains unresolved;
- the complete proposed mapping package is not constructible;
- `PE-SUBJ-010` remains bounded;
- no A01 row is reclassified;
- reviewed-current totals remain `217 / 268 / 0 / 244`;
- no requirement assessment is performed;
- no requirement result is produced;
- no implementation defect is determined;
- and later independent review is required.

Determination:

**mapping package not constructible and selected relationships remain unresolved.**
