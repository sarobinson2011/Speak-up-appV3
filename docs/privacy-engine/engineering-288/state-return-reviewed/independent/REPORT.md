# Independent review: bounded ManagedAuthority.state return correspondence

Formal-Lab[6], 28 October 2026. Construction author: SU-Engineering[288D]. This is an author-independent review of **I164-state-return-correspondence-1.zip**. It does not repeat the completed config, binding, HF-01, SOC, boundary, smoke or pipeline reviews. Implementation and retained evidence remain unchanged.

**Scoped verdict: SUPPORTED** for the bounded source-derived, conditional state-return bridge at the validated saved recovery frontier. No residual defect witness was found by the focused independent controls sealed in this checkpoint. This does not establish an observed backend/run/wrapper return chain or the value of an unobserved later state call.

The exact input is **41,935,972 bytes; 1,016 entries**, SHA-256 `44942004491d883af8c422f10dd38fd1e25cbc4f56e2d53e6345e264d0893fdc`. CRC, safe unique regular membership, exact top-level manifest membership and all **1,015 manifested hashes** passed. Eighteen retained nested ZIP occurrences were verified within their historical manifest scopes. Intentional omissions in compact historical review copies remain explicit archival dependencies; they are not treated as complete decoded historical archives.

## Source-derived relation

The reviewer-owned AST oracle independently checks exact source coordinates, expressions, guards and normal-continuation prefixes. It reuses an AST traversal primitive from prior reviewer work, without invoking an old suite. The backend program is independently compared with its complete defining AST, including the guarded event and accounting checks. The old wrapper propagation checker is read as source, not executed as a fresh trace campaign.

| Source site | Requirement and scope |
| --- | --- |
| `ManagedAuthority.state`, line 42 | Return `self._run('state')`; literal method selector, no extra arguments, no conversion or copy. |
| `_run`, lines 32–41 | Enter the instance lock; call `_require`; test transaction state; assign the delegated call to the single `result` local; test transaction state again; return that local. The dispatch expression is exactly `getattr(self._live,method)(*args)`. |
| `_require`, lines 25–26 | Normal continuation requires phase READY, live reference present and retired reference absent. It is before the `try` block. |
| `Authority.state`, lines 84–90 | Parse selected HEAD bytes, check their binding against this Authority, check event hash and typed after-state when seq is nonzero, validate accounting, then return `s`. The bridge reuses the existing HEAD declaration and validated state; it does not replace authentication, schema or accounting validators. |
| Exception handler | Caught failures evaluate the reason before calling `_quarantine`; a completed quarantine is followed by bare re-raise. Failed reason evaluation does not establish a quarantine call. Failed/interrupted quarantine does not establish absence of partial effects. |
| Lock exit | Lock entry, readiness and lock exit are outside the handler's catch region. Exit failure can supersede a pending return or exception without this handler performing quarantine. Normal forwarding requires normal exit. The retained trusted RLock non-suppression premise remains explicit. |

Defining source identities are unchanged:

- `compiler/live_connection.py`: 5,717 bytes, SHA-256 `7344170ca01a2dbbd3afbeb4a6a55c0b95db0edb1a8d74e4fa4638b6dcfc6da5`.
- `support/reference/runtime/authority.py`: 23,223 bytes, SHA-256 `4565bb30cb637b3cef40a3f1da2b3722840b747ab110fa37eede0cbc2e3b313a`.
- `compiler/managed_observations.py`: 35,124 bytes, SHA-256 `2b4ccd7902d8e270ac8d4b22060d08d184dda1b0e6fcdccae781fd81eef902cc`.

All three new declarations inherit the exact existing HEAD object type and retain UNKNOWN classification and null canonical class, ordinal and multiplicity. The two forwarding edges connect backend return to dispatch assignment and `_run` return to wrapper return. Existing delegation, readiness, live-reference and source-inventory joins agree with independently derived source locations. No new physical occurrence or allowance follows from the two symbolic contexts.

The saved state is a validated finite snapshot, with eight top-level fields and seq zero. Recursive value comparison enforces its exact field/container/scalar types and values, including integer versus boolean and legitimate null `active`. It is a correspondence check against separately validated input, not a new generic validator for arbitrary alternative HEAD states. Source analysis covers the seq-nonzero branch; this snapshot does not supply execution evidence for that branch.

A separate static check derives the initial HEAD shape directly from Authority's constructor assignment and compares that type shape with both saved context anchors. It reuses the unchanged reviewed string-binding premise. This corroborates the exact snapshot types without treating generated type annotations as their only origin. It does not establish that initialization was observed or revalidate the transitive accounting implementation or full HEAD state space.

The source forwards the same result reference. Constructed symbols therefore must agree across all three links and remain scoped to the selected acquisition, instance, context and frontier. Distinct copied-result symbols reject even when their recorded dictionaries compare equal. Alternative consistent hypothetical symbols are allowed without asserting physical object identity. Defensive copies made by this offline adapter protect validation expectations; they do not describe a copy by `_run` or `ManagedAuthority.state`.

## Mandatory validated-evidence connection

The public path is `validate -> derive -> derive_state -> _checked -> _basis`. Every full semantic or derivation check reloads strict predecessor membership and current source/input bytes, invokes the reviewed config derivation, and requires its exact saved receipt. Read-only call observations during independent controls confirm that this invocation occurs. Completed predecessor test/review scripts are not called.

Expected HEAD is decoded from that freshly validated predecessor evidence. Candidate values and a candidate-supplied baseline cannot redefine it. Exact recursive type/value comparison occurs before the inherited binding/state/configuration/ownership and whole-evidence gates. Coordinated substitutions of the HEAD across saved reports and embedded JSON reject in both semantic validation and derivation with `STATE-VALUE-ORIGIN:/head`. Recorded comparison calls show the unchanged expected HEAD alongside the substituted candidate. This result is not solely an archive-pin rejection or agreement among mutually altered reports.

In both contexts, the new anchor joins exact export member bytes, `/head`, decoded-state identity, instance binding, ownership incarnation, managed constructor frame, session, configuration record, acquisition, recovery occurrence/frame/parent, call/completion records and reference relationships. The inherited HEAD declaration agrees with the predecessor's validated declaration. Independent checks compare these fields with the actual saved records and predecessor receipt.

Both contexts, all three conditional values and both source forwarding edges remain mandatory. Wrong-method delegation, extra arguments, missing links, wrong receivers, copied result symbols, cross-acquisition symbols, stale/wrong-instance claims, changed HEAD or nested values/types, missing recovery evidence and unsupported observation/admission claims reject at their applicable boundaries. Tests distinguish full semantic/derivation/public entry checks from direct internal-relation controls.

Returned context, catalogue, semantic and public-result trees can be mutated without changing subsequent expectations. Fresh pristine semantic output, derivation and public validation continue to match the original receipt. The mandatory source catalogue is freshly re-derived, and returned copies do not become authority.

## Normal and exceptional paths

Constructed path tests are generated from the independently audited region order. They cover normal forwarding; abrupt lock entry, readiness, pre-transaction evaluation, dispatch, post-transaction evaluation, return expression and lock exit; active pre/post transactions; reason failure; interrupted quarantine; and lock exit superseding a rethrow. The checks distinguish whether dispatch completed, whether quarantine was called, and whether it completed. Abrupt paths cannot claim normal return links. Missing exit outcomes, unreached extra outcomes and integer substitutes for boolean transaction outcomes reject.

These are source-conditioned path models. They are not observed exceptions, successful cleanup, exhaustive instruction-level interruption coverage or evidence that every stipulated stage failure is feasible in every concrete run. Prior reference-transfer findings remain authoritative for effects; this bridge does not discharge cleanup obligations.

## Results and preservation

Fresh independent controls passed **108 primary assertions and 80 recovered-root assertions**. One separate fresh process ran the actual current public CLI successfully with both contexts and the exact saved receipt. The assertion totals include the independent defining-source audit and explicitly labelled constructed and internal-relation controls. A separate static initial-HEAD type-origin check also passed. None is a runtime observation. All independent controls completed without a candidate defect; no supplied counts or failed attempts are included in these totals.

Engineering's **83 primary controls, 77 recovered-root controls and one fresh process check** were inspected separately, including result rows, progress records, receipt identity and process outcome. They were not rerun or combined with independent totals. The reported intermediate 975-entry recovery archive has continuity metadata; its external outer bytes were not newly verified. The final 1,016-entry target was independently extracted and validated instead.

Both supplied membership failures remain outside completed totals. Each stopped with `STATE-UNDECLARED-OR-NONREGULAR` before its first assertion. Exact preserved unexpected files were independently hashed:

- First: 5,767,168 bytes; SHA-256 `0d07f3f38d177b726c521669c11de22d4c766d510fa9b0105cdd39702c2650ef`.
- Second: 7,864,320 bytes; SHA-256 `939f377ca87b8f7099405f68c0f5400f72e3abf3edb1aab2d3962cf43d0585e7`.

Their causes remain UNKNOWN. Retention of the author's original failed directories is a supplied assertion; this review verifies the retained exact bytes and records. It does not infer filesystem stability, durability or a cause from those failures. Earlier zero-assertion attempts and the interrupted 13-assertion harness remain in their unchanged predecessor scopes.

All **918 config-predecessor members** and all **41 included config independent-review records** remain byte-identical. The previous independent-review archive was recovered after workspace maintenance and matched its exact 63,598,176-byte, 43-entry identity, SHA-256 `97ccc050f291230f667a8d1fde28d9f655d75a28d72ec6604654d728cb5dcf94`. Its omitted redundant input ZIP and 22,806,528-byte failed-root binary remain in that unchanged external archive; neither is an executable dependency of the new bridge.

All **42 existing producer functions** and other top-level statements remain AST-identical. Six producer functions are added and the connecting adapter changes prospectively. Exact old versions remain retained. Every previous context member and non-replaced top-level receipt field is unchanged. This preserves historical identities, relationships, ordinals, original evidence and prior scoped findings without reopening their reviews.

The unchanged config receipt is 805,314 bytes, SHA-256 `7d82305c3eb4646b0d9072daec9d93186848ac2b8e1aa71d6ac6de77fbbf12a3`. The new state receipt is 942,948 bytes, SHA-256 `7b5f2d1286fd6c3d02a16c15f42da0c3e6491c5582beb882f64115a691bd0186`.

The actual test environment is CPython **3.12.14**, optimization and bytecode writes disabled, with **Cryptography 50.0.2** installed. Audit/call guards prohibit application-source execution, host-session access, database/network connections and child-process spawning inside controls. No host qualification or new 41.0.7 compatibility evidence is claimed. The saved Git receipt remains provenance only; no Git operation occurred.

## Remaining observation limits and boundaries

The saved trace supplies no joined Authority.state → `_run` → wrapper return chain. Actual link values, frames, object-reference observations and call count remain null/UNKNOWN, not zero. The three supplied state values are explicitly conditional values at the validated recovery frontier, not observations of an unrecorded later call.

The distinct `Client.state()` observer keeps its exact handoff record, acquisition-qualified occurrence, caller and value, with no frame, parent frame or invented join to the missing links. It is neither a fabricated backend frame nor an additional invocation caused by evidence copying. The 18 traced invocations and observer retain their previous distinct provenance.

Serialized values and constructed symbols do not establish physical object or connection identity. The validated frontier does not establish current/lifetime readiness, exclusive ownership, actual close, custody, durability or complete repetition coverage. Missing assignment, state, ingestion and historical launcher observations remain explicit. Arbitrary Python introspection, monkeypatching and hostile concurrent mutation remain outside the trusted-process contract.

All eleven obligations, four inventory UNKNOWN totals, fourteen lifetime UNKNOWN totals, Decision B, permanent accounting, reservations, nonce/ownership duties, retention, allowances and uncertainty protections remain unchanged. No policy, numerical cap, replacement architecture, retention permission or outcome restriction is adopted. SOURCE-ONLY is unchanged; cumulative-envelope is unadopted; backup is kernel-only; streams are UNCOMPUTED. Readiness and final binding remain blocked. **Admission remains disabled.**
