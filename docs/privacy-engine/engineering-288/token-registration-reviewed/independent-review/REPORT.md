# Independent review: bounded token registration correspondence

**Scoped verdict: SUPPORTED within the declared normal `_run` token registration and callback-to-revocation correspondence slice.** No residual defect witness was found. The result supports a source-derived, conditional correspondence model; it does not establish runtime registration, callback execution, revocation, physical reference identity or outer cleanup.

Target: **I164-token-registration-correspondence-1.zip**, **69,308,990 bytes; 2,178 entries**, SHA-256 `84c714c62aa6aa3956e5b137d03e584b055c06b26200b6768090ad33a5e4dbeb`. Review author: **Formal-Lab[6]**, independent of construction author **SU-Engineering[288D]**. Date: 29 October 2026. Implementation code and existing evidence were left unchanged.

The exact outer identity, CRC, safe unique regular membership and all **2,177 manifested hashes** passed. Seven extracted layouts, including the failed reviewer attempt's input, were verified unchanged after testing: each has **2,178 files and 668 implied directories**. All 18 present nested archive occurrences passed CRC, membership and hashes. The 31 interpretable manifests retain their prior compact-recovery qualifications.

All **2,053 predecessor members** under `retained/status` match the exact IS-01 correction archive. All **80 non-input members** under `retained/closure-review` match the exact delivered IS-01 independent review, including its failed 153-check attempt. Original IS-01 witnesses, older failures, forensic partial-file evidence and earlier scoped findings remain unchanged. The prior review's omitted embedded ZIP is the explicitly redundant outer form of the decoded predecessor, not an undeclared executable dependency.

The supplied intermediate recovery archive—69,193,487 bytes / 2,151 entries / SHA-256 `f0db3351a2911d9070d01bdd8e95c854932fd2083d27852fa1e6034373e70631`—remains a continuity identity. Its outer archive was not newly verified. All 2,150 retained input-manifest entries match the final checkpoint, and the exact canonical manifest serialization matches the recorded recovery-manifest identity. Fresh independent recovery used the final requested archive. Historical omitted outer archives and forensic snapshot manifests remain qualified; no continuity record is relabeled as a freshly verified historical archive.

The declared current component identities and both complete sections of the supplied code diff match the actual changes:

| Component | Bytes | SHA-256 |
|---|---:|---|
| `code/managed_coverage.py` | 205,451 | `4d485ad7df99bf6d0cd05c41d7091f126090eadc9ebcff39a80e1d25e623e5bc` |
| `code/correspondence.py` | 11,502 | `afca436de30e93020923a12af2e53d2a0b584dcc34ab9f56d5b423d6a1fe9c7d` |

All **78 inherited producer functions** and their preceding source text are unchanged; six token-registration functions are added. Runtime sources and unrelated historical validators are unchanged. Every prior context field, historical identity, relationship, ordinal, obligation binding and limit is preserved. The authenticated remaining-obligations document still contains O01–O11. The new receipt is **3,328,177 bytes**, SHA-256 `1184bbf9366a2c7a8ced902836566b6610a8844cbf97698e78d10e6e91107145`.

Independent source derivation used the defining `prospective_entry.py`: **9,485 bytes**, SHA-256 `a1d80c523ae220228a6b27cac42b5e57a006336e858a8e7db0a75355d6cf2ae9`, principally `_run` at lines 169–195. The reviewer traversed the actual AST by assignments, calls and enclosing regions, independently of the generated catalogue. Source node positions, expressions, guards and the twelve modeled milestones were compared to that oracle. This includes the three ordered statements on source line 174; sharing a line does not collapse their distinct roles.

The source creates `_Owner(wrapper)`, then a fresh `object()` token, then stores that owner in `_OWNERS[token]`. The selected wrapper is supplied inside the launcher's `with` region. If `control is not None`, `_Control(token)` and its callback precede the `Client(token)` callback. The latter is followed by the `owner.failure is not None` test. The normal branch to removal requires the modeled test to complete with no stored owner failure. A non-None failure stops at the separately identified exceptional frontier; it does not establish execution of the following raise or unwind.

The enclosing `try/finally` contains `_OWNERS.pop(token, None)` before launcher context exit. Callback returns and the pop result are discarded. Client/control constructors store the same selected token; owner.wrapper and session.managed connect to the selected validated instance scope. Symbols are invocation-qualified model references, not observed addresses. Different invocation identifiers remain distinct even when other values match.

The finally-entry milestone is anchored to its containing `try/finally` AST node. It is a constructed control-flow milestone, not a newly observed execution of that node or a claimed runtime event at the `finally` keyword. The normal-path ordering is checked separately. Source anchors preserve the outer with/try guards; successful launcher entry and complete outer-lifecycle execution are not established by this slice.

| Established conditional milestone | Supported implication | Still unestablished |
|---|---|---|
| Registry insertion completed | Selected token/owner registration in the finite model | Actual runtime insertion or an inventory of global owners |
| Finally entry completed | The modeled finally-entry milestone | Removal attempted or completed |
| Removal attempt entered | The modeled pop attempt | Successful pop or selected-owner removal |
| Normal pop completion | Selected key absent at that operation's completion under the exact-builtin/trusted-process conditions | Persistent absence, durability, launcher/database cleanup |
| Normal pop plus explicit registry continuity | Conditional removal of the selected registered owner | Observed owner identity or operational continuity qualification |

With continuity UNKNOWN, normal pop completion remains admitted while selected-owner removal stays UNKNOWN. This adds no runtime guard, ownership policy, storage limit or continuity proof. A false completion flag means that the finite prefix has not established completion; it does not prove that an effect did not occur. Tested stops at insertion, callbacks, finally entry, removal attempt and removal completion preserve earlier acknowledged milestones. In particular, an unobserved pop outcome does not erase completed registration, callback, finally-entry or attempt facts. Conversely, termination or missing observations cannot create successful removal, a Python exception/unwind, retained error, database cleanup or renewed authorization.

The current mandatory path reconstructs the exact IS-01 predecessor, invokes its actual `derive_status`, checks the saved predecessor receipt and regenerates the token catalogue from defining sources. Both ordered context rows require the new relation. Full semantic validation rejects coordinated catalogue/claim changes; full constructed validation rejects coordinated foreign-context references and outputs. The public entry rejects the predecessor receipt as a substitute for the new mandatory relation. A fresh recovered CLI validates the exact current receipt for both contexts with admission disabled.

Fresh independent controls cover normal controlled and client-only paths, unknown continuity, the stored-failure frontier, wrong token/owner/client/control/session/manager links, cross-invocation and stale-scope substitutions, actual omitted/reordered steps, premature or false removal claims, invented cleanup/authority/output destinations and lost earlier facts. Every omission mutation checked that the intended event was actually removed. Exact-type controls cover booleans, nested containers, keys and scalar subclasses at constructed, submitted-output and semantic boundaries. Coordinated declaration/expected-order omissions cannot replace the source oracle. Returned nested results and context lists were mutated; subsequent pristine validations retained their original expectations.

These tests keep representation validity separate from execution evidence. They do not reopen IS-01's closure or rerun a completed predecessor test campaign. Required predecessor validation is part of testing the new mandatory entry.

| Evidence set | Completed result |
|---|---|
| Fresh independent primary | **170 checks**: 67 positive, 103 rejected negatives |
| Distinct independent recovered-root | **51 checks**: 18 positive, 33 rejected negatives |
| Fresh independent full semantic/derivation | **7 checks**: 4 positive, 3 rejected negatives |
| Fresh independent full constructed/public gates | **10 checks**: 3 positive, 7 rejected negatives |
| Separate actual fresh recovered CLI | **1 pass** |
| Engineering supplied primary | **285**, inspected only |
| Engineering supplied fresh-process | **14**, inspected only |
| Engineering supplied recovered-root | **50**, inspected only |
| Engineering supplied CLI | **1**, inspected separately |

There are **238 completed independent controls plus one separate CLI pass**. Counts are not runtime occurrence coverage. The actual environment was CPython **3.12.14**, `-I -B`, optimization disabled, with installed Cryptography **50.0.2**. No dependency installation, new host qualification, 41.0.7 compatibility claim or installed-wheel byte authentication occurred. Guards prohibited application/session method execution, database/network operations, host-session access and writes to recovered inputs.

Two reviewer harness failures are preserved separately. The first completed 11 checks before attempting to parse a multiline source segment without restoring its first-line indentation; its source, traceback, progress and recovery record remain under `failures/reviewer-source-fragment`, excluded from completed totals. The corrected comparison restores the recorded column and dedents before AST parsing. A later zero-control audit attempt compared one producer-diff section to a file containing both producer and adapter diffs; its record is under `failures/reviewer-diff-section`. Both complete sections were then verified exactly. Neither failure changed the candidate or demonstrates a candidate defect.

The 18 saved traced invocations and separate frameless `Client.state()` observer remain distinct and unjoined. No runtime token/owner creation, registry insertion, callback completion, finally-entry, pop-attempt/completion or physical reference observation was established. The source-defined exceptional and outer-cleanup paths remain anchored but unexpanded. The recorded recovery frontier is not the time of a hypothetical later invocation. Registry continuity, exclusivity, custody, durable revocation, complete repetition/lifetime coverage and outer-lifecycle qualification remain unresolved.

All eleven obligations, four inventory UNKNOWN totals, fourteen lifetime UNKNOWN totals, Decision B, retention, allowances, accounting, reservations and uncertainty protections remain. SOURCE-ONLY unchanged; cumulative-envelope unadopted; backup kernel-only; streams UNCOMPUTED; readiness/final binding blocked; admission disabled. No runtime changes, acquisition, request, database connection, session operation, canonical rebinding, policy adoption, Git operation or completed-suite rerun occurred. This checkpoint grants no operational authority.
