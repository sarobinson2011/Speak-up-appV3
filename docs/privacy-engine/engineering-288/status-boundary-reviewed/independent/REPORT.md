# I164 bounded status caller/output correction — independent review

Review author: **Formal-Lab[6] (Codex, this review)**. Construction author: **SU-Engineering[288D]**; the retained prospective Cryptography 50.0.2 launcher/profile has separate SU-Engineering[288C] authorship. This reviewer did not author the submitted correction. Date: 26 October 2026.

**Verdict: SUPPORTED for the bounded status caller/output contract within the declared trusted-process API boundary.** No residual defect witness was found within that scope. This is source/API closure, not positive real-backend or Steve-host qualification, proof of caller authorization, complete observer coverage, or admission.

The exact adopted contract controls this verdict. Its caller, exposure and evidence-handling choices are preserved. Internal status remains potentially sensitive; transient use, coarse errors and lack of new logging do not prove privacy. The cumulative-envelope proposal remains unadopted.

## Verified identity, recovery and preservation

The submitted `I164-status-boundary-correction-1(1).zip` is exactly **4,269,431 bytes**, **463 entries**, SHA-256 **983e8aa849be387c4f92a54953fd24e2271bb090a01a0fb589230f0edad53185**. Independent verification passed CRC, unique safe regular-file membership, exact top-level manifest membership and all **462** manifest member identities. Both extracted review roots remained byte-for-byte identical after testing, with no additional files.

The package contains all source dependencies needed for the bounded checks. Its 37-entry contract/retained dependency map and five basis pins were checked independently. All **42 preserved reference members** and the complete new/unchanged partition in `CHANGED-IDENTITIES.json` agree with actual bytes. The two source archives below were retrieved and verified independently of the construction's preservation report; no predecessor test suite was run.

| Authority artifact | Verified identity | Correspondence |
|---|---|---|
| Status-contract adoption ZIP | 54,869 bytes; 14 entries; SHA-256 `e06103888909cb2100d97dd75ab721fed237a5180444d05bec781c6e2f5d9fdd` | Exact contract and decision copies; CRC, safe exact membership and manifest hashes pass |
| Original 50.0.2 launcher ZIP | 101,857 bytes; 28 entries; SHA-256 `bdef8320320e74c9f79e187da4e6adfe93ce1d4723871f69935c9f8816299e55` | All 28 retained members match, including historical results, 41.0.7 source/configuration and marker/environment machinery |
| Previously verified TE correction parent | 77,270,588 bytes; SHA-256 `1e0bbb0498e46da537aad3a2e0af2781607d9cbee10043e2a685c4efff310204` | Reused byte authority; archive inspection only, no review/pipeline rerun |

The parent contains the candidate transport pinned at SHA-256 `152207d3140b4d9b0d97890b5ce38f5f4ff4bab3bc009af951e489faaf534a42` and draft transport pinned at `7b5c8b6b9535eef62617412b5c111d2c3df06c2d649aa71dbb151bf2cdc8633c`. All **666 candidate** and **163 draft** members match the unchanged retained launcher manifests; the only additional transport member in each is its recovery manifest. Eleven selected candidate/basis files match the parent bytes directly. The remaining-obligation table matches the draft member `source-only/scope/remaining-obligations.json` exactly. All **93 runtime-map source files** are present with the expected candidate bytes. This last check verifies source composition, not execution or a newly recovered runtime's installed filesystem.

The review is additive and leaves historical source, model/directory/relation/duty files, inherited ordinals and evidence unchanged. Unchanged historical files preserve their prior scoped support; byte continuity is not a fresh historical execution or a rerun of prior qualification.

The exact contract has SHA-256 `ef55b55a1aab7427a1f58faa38bf2b5b27af1f0deddf62f73e3764bfbd09fcd6`; its decision has SHA-256 `0ba88241ae82ff0bd416b47d7c81451f431e4a65a4662f9863948623e8ed693c`. The decision is the earlier contract adoption record, including its then-current no-implementation authorization statement. This review neither revises that historical record nor supplies policy/implementation authority.

## Contract correspondence and findings

Source locations below are paths inside the unchanged submitted archive, retained in this checkpoint as `input/I164-status-boundary-correction-1.zip`.

**1. The general client does not receive the former status-capable wrapper.** `code/prospective_entry.py:108–124` exposes only `state()` and `handle()` as ordinary public client methods. It stores an opaque invocation-local token. `:143–166` resolves that token internally, accepts exact `bytes` packets/responses, validates the source state key set, and detaches exact primitive/list/dictionary values. Object/subclass return channels reject without calling copy/repr hooks. `:169–195` discards callback returns and revokes capabilities before close, including uncertain cleanup. Retained aliases cannot attach to a later owner.

The expected state shape is independently supported by `retained/candidate/support/reference/runtime/authority.py:67–89`. The source `handle` contract returns signed response bytes (`:98–122`); the new boundary neither re-encodes them nor silently redacts their existing application error contents. This is a status capability/exception-output correction, **not a general content-redaction rule for authenticated application responses**. The test's response bytes are exact fixture bytes, not newly authenticated real responses.

**2. Default CLI output and general failure values meet the selected boundary.** `prospective_entry.py:230–247` calls the new general entry and prints fixed completion/failure text. It does not call historical `main`, serialize status/state, or print a backend traceback. Both argument failure and execution/close failure produce nonzero failure disposition. Independent success/failure tests exercised the actual new CLI body with the retained launcher mechanics and stub backend. A separate unmocked command refused the review environment with exactly the fixed failure message and created no destination.

The old exposure was reproduced using the AST-extracted unchanged historical `main` with a no-storage context stub: `retained/launcher/code/lab_bootstrap.py:188–194` serializes a status reason to stdout. This establishes the old source path and the bounded correction; it is not execution of the historical bootstrap or evidence of missing past launcher frames.

**3. Suppression preserves original failures and uncertainty.** `prospective_entry.py:161–166` retains the original backend exception privately and raises the fixed client error after leaving that handler. Its ordinary cause/context/attribute fields do not reveal the backend diagnostic. The owner remains failed if a callback catches that error, subsequent dispatch rejects, and `:180–185` sends the original failure into the unchanged launcher's failure path. An additional callback error remains represented in the retained exception chain.

The unchanged launcher (`lab_bootstrap.py:148–176`) owns partial-raw cleanup, managed cleanup, exact failure records and retained `ACTIVE` uncertainty. Independent controls covered raw initialization/close failures, managed opening, preflight state/status failures, backend errors, KeyboardInterrupt, SystemExit, caught errors, later callback errors, diagnostic callback failures, close uncertainty and an evidence-write failure. No tested failure became success. Original diagnostic messages remained in the launcher's private evidence where writing succeeded; close failure remained explicit. When the existing evidence write itself failed, no durable record was invented: the outer call still failed, cleanup was attempted and `ACTIVE` remained. Pre-session failure and failure-record completeness remain prior limitations.

**4. Internal diagnostics and separately authorized capture remain possible.** `_Control.status` (`prospective_entry.py:127–140`) returns the exact internal status value, including non-READY status. `run_controlled` (`:210–222`) is explicitly a designated trusted-owner entry; it does not authenticate a caller's evidence authority. A reviewer-controlled evidence sink received the full reason, epoch and all literal False fields. No automatic per-call logger, new canonical status serializer, retention amendment or universal receipt was introduced.

The unchanged `ManagedAuthority.status` (`retained/candidate/compiler/live_connection.py:23–24`) reads under its lock without requiring READY; successful `recover` embeds the nested status (`:76–99`), and `open_session` still discards the recovery return and returns manager/scheduler only to internal launcher code (`:101–104`). The launcher discards the scheduler (`lab_bootstrap.py:157`) and its wrapper stays internal to the new owner. Its existing create-only `BOOTSTRAP-COMPLETE` status evidence remains unchanged (`:158–164`).

Designation and custody are external trusted-owner premises. A control callback must not forward its diagnostic to a general client. The package does not prove that all deployed callers satisfy those premises. Arbitrary Python private-attribute/module/frame introspection, hostile callback code, monkeypatching, OS-stream interference, competing owners, thread/process isolation and timing/fairness are outside this verdict. Ordinary exceptions' tracebacks still reference Python frames; they are not a sandbox. Coarse completion/failure and timing remain observable.

**5. The additive binding is exact in both contexts, without a qualification upgrade.** The saved `provenance/status-correspondence.json` is 34,758 bytes, SHA-256 `5bbc3b72fd1905c5588a6b21b357278cb5367643ea21bd6e3d2dfb360722cf0d`. `code/correspondence.py:26–40` checks the current entry and basis identities and uses the entry's dependency checks. `:53–129` constructs both declared contexts from current authenticated sources, including 19 affected site anchors, seven declared relationships per context, four inherited managed requirement joins and four inherited local declarations. Independent inspection checked every site source identity, AST-selected source span, and coverage in both ordered contexts. Exact serialized validation rederives the binding (`:133–136`).

Coordinated changes to source claims and both context annotations reject when actual pinned source remains unchanged. Missing/duplicated/reversed contexts, omitted sites/relations/duties, changed classification, invented multiplicity/ordinal, erased historical-frame gaps, zeroed unknown totals, admission/full-binding/policy escalation and alternate serialization reject. Mutating a returned derivation or validation result does not change subsequent expectations.

This checks explicit source correspondence; it is not a canonical token allocation or proof of complete symbolic/operational coverage. The 19 sites are declarations, not invocation counts. Context identities do not duplicate physical storage or allowances. Classifications remain UNKNOWN; multiplicities, canonical classes and ordinals remain unallocated. The unchanged observation consumer's reason check establishes string type, not complete reason provenance. Historical handoff/close producer-script and launcher-frame provenance remains **UNAVAILABLE**, and no newly executed fixture fills that historical gap.

## Supplied evidence versus independent testing

Engineering's supplied results were inspected, not rerun or counted as independent controls:

| Supplied material | Assessment |
|---|---|
| 79 primary assertions and 79-assertion fresh repetition | Supporting stub evidence; distinct from this review |
| First recovered attempt | Failed before the primary checks; preserved partial result and traceback |
| 79-assertion corrected recovered repetition and 10 continuation checks | Supporting evidence of the bounded harness correction and negatives |
| 24 adjacent assertions | Supporting value/capability/error controls |
| 22 correspondence assertions | Supporting source-binding controls, including two process executions |

The failed copy rule excluded every directory named `results`, accidentally removing **six required retained-launcher result members**. The saved inventory, missing dependency set and `DEPENDENCY-MEMBERSHIP` traceback agree. The harness repair limits that exclusion to the outer results directory and introduces an explicit continuation path; it did not alter application code. The original failed source/results remain embedded unchanged. Relevant supplied process stdout/stderr hashes were also checked. Repeated process passes are not additional independent semantic coverage.

This review used independently written controls, importing no Engineering test module:

- **203 boundary assertions**, **63 source/binding assertions**, and one no-database/no-network assertion passed in a fresh process.
- The same **267 assertions** passed in a separate fresh process against a complete newly extracted root. This is reproducibility evidence, not a doubled coverage count.
- **18 additional fresh-process checks** passed: 13 contract/dependency membership/identity cases, four basis/input cases and one unmocked public gate refusal. Actual regular files, empty directories, symlinks and FIFOs were exercised. Layout rejection preceded retained payload reads. No socket/device execution claim is made.

The test environment was CPython **3.12.14**, Linux x86_64 with glibc **2.39**, installed Cryptography **50.0.2**, using `-I -B`. Positive tests used reviewer-written in-memory backend stubs with unchanged launcher control flow, empty placeholder state files and mocked environment/runtime seams. Audit guards forbade SQLite connections, network operations and Steve-host paths. There was no real managed lifecycle, acquisition, signing execution, existing-session access or 41.0.7 test. Installed version metadata is not installed-wheel byte authentication. The unmocked profile gate refused this assessment environment; a designated Steve-host positive run remains pending.

## Limits and smallest remaining check

No real-backend run is necessary to support this deliberately narrow source/API verdict. **Positive real-backend integration remains unestablished.** Before claiming that stronger result, the smallest additional check is a separately authorized, disposable fresh-state smoke execution of this exact entry under the exact retained 50.0.2 host profile: confirm managed handoff, one legitimate state read and harmless authenticated request/response, designated internal diagnostic handling, fixed outward output and confirmed close. Preserve exact outputs and environment/code bindings. It does not require opening an existing session, a lifecycle campaign or repeating completed component reviews. No such execution is performed or authorized by this checkpoint.

Caller/evidence-workflow authorization and custody, complete operating/security scope, runtime exclusivity, real-storage durability, rollback resistance, complete historical frame lineage, original-record reconciliation and installed-wheel byte authentication remain unresolved to their prior scopes. The API owner's transient token is not a global call identity, epoch lifetime bound or durable authority.

All **eleven obligations**, **four UNKNOWN inventory totals** and **fourteen UNKNOWN lifetime totals** remain. SOURCE-ONLY is unchanged; readiness/final binding remain BLOCKED; backup is KERNEL-ONLY; streams are UNCOMPUTED; admission is disabled. No implementation, policy, numerical limit, retention rule or architectural adoption changed.

The accompanying checkpoint includes the exact submitted ZIP, independently recovered small authority ZIPs, independent harnesses, immutable-source verification, machine-readable results and stub fixture evidence. It is an independent review record for Engineering-Anchor[2], not a canonical status update or an operational authorization.
