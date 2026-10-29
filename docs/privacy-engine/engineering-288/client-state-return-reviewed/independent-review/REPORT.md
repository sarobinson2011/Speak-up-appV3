# Independent review: bounded client-state forwarding and `_data` detachment

**Verdict: SUPPORTED within the stated static/conditional correspondence contract and currently modeled paths.** No residual implementation defect witness was found in this scope. This is not evidence of a runtime state-return chain, complete runtime coverage, completed model construction, qualification, readiness or admission.

The exact target is **I164-client-state-return-correspondence-1.zip**, 61,624,841 bytes, 1,688 entries, SHA-256 `0ae24141a77f42eb96ed0f8d144f612d7a8045e04f7aa47dcaa8d1750f886907`. Review author: **Formal-Lab[6]**, separate from construction author **SU-Engineering[288D]**. No implementation, candidate, historical source or evidence bytes were modified. Review completed 29 October 2026.

## Integrity, recovery and preservation

The supplied attachment's exact outer identity, CRC, safe unique regular entries, exact membership and all **1,687 manifested hashes** passed. Two independently extracted final roots each contained exactly **1,688 regular files and 574 implied directories**, with the same bytes after testing. All 18 present nested archive occurrences passed CRC, safe exact membership and their manifest checks. There are 23 interpretable manifests in the decoded target; ten retain declared omissions from compact historical review copies. Those omissions remain enumerated in `results/composition.json`. Missing historical outer archives and two historical omitted forensic copies are not claimed as newly recovered or verified. The existing preserved forensic evidence is unchanged.

The prior verified review archive was recovered by its exact known identity (60,073,099 bytes, 134 entries, SHA-256 `7c64e87084d3b7a2257794486198b35d2ba40ebdaefb272424a0e8c7e04a7759`) for byte comparison, not a review rerun. Its embedded prior target matched the reviewed 60,424,906-byte/1,508-entry classification correction. All **1,508 predecessor members** and **133 non-input independent-review records** in the new target match those exact prior bytes. The redundant embedded input ZIP is the only omission from this immediate review copy. Earlier 172/131 classification and 217/149 forwarding results, separate CLI results, six caveat cases, original failures, partial-file evidence and the 31-row progress reconciliation remain unchanged and retain their original scopes. The duplication mechanism in that historical reconciliation remains UNKNOWN.

All **62 existing producer functions** and its other top-level statements remain byte-identical; eight state/copy functions were added. Runtime source changes are zero. Every prior context field, relationship, ordinal, evidence record, obligation identity and limit is preserved. The prior extension component identities were relocated exactly, with a new current extension, prior-receipt identity, client-state relation and explicit limits. This review reuses prior scoped support; it does not requalify every historical component.

Engineering's intermediate recovery archive (61,274,079 bytes, 1,650 entries, SHA-256 `5d9c912c7aae177c962aaf43ccf20ba9641a32126d611127418ab0d4385cdfb7`) is a retained supplied continuity identity, not newly verified outer bytes. Independent recovery used the final 1,688-entry target. The mandatory executable predecessor chain is present and its current saved-input validation succeeded from both final roots.

## Independent source findings

The defining `prospective_entry.py` is 9,485 bytes, SHA-256 `a1d80c523ae220228a6b27cac42b5e57a006336e858a8e7db0a75355d6cf2ae9`; the defining `lab_bootstrap.py` is 11,481 bytes, SHA-256 `245d4f36d687834aeee064a60d4414b15f7b8babfdb5dec192aa995d93af2b78`. These are the retained source files under the occurrence correction/launcher roots. The independent AST oracle checks their statements, anchors, ancestor guards and normal-prefix ordering, not the generated catalogue's assertions alone.

| Source | Source-established behavior | Correspondence consequence |
|---|---|---|
| `ManagedSession.state`, launcher line 123 | Directly returns `self.__managed.state()` with no arguments | Same constructed manager-result reference reaches the session return |
| `Client.state`, entry lines 113–114 | Calls `_dispatch(self.__token, 'state', None)` | State invocation needs no packet, request identifier or journal row |
| `_dispatch`, lines 143–160 | Owner lookup/guard precede `try`; state operation, wrapper call, exact dictionary/key check and `_data(result)` are inside the `BaseException` protected region | Correct owner/session/manager links, branch guards and normal continuations are required |
| `_data`, lines 90–98 | Exact primitive branches return the value; lists and string-key dictionaries are recursively rebuilt; unsupported branch raises `RuntimeError('UNSUPPORTED-CLIENT-VALUE')` | Exact values/types and ordered container contents must correspond to a fresh output container at every visited mutable input path |
| `_dispatch`, lines 161–166; `_fail`, 28–29; `_run`, 169–195 | Original caught error is stored before intentional fixed failure; outer callback/revocation/launcher handling is a separate conditional continuation | Intentional failure, unexpected raise, catch location, retained-error premise, cleanup and runtime evidence remain separate |

The six ordered declarations are `manager-return → session-return → dispatch-result → converted-result → dispatch-return → client-return`. The first three refer to the constructed incoming result; the last three to the detached result. Each includes source-defined type/anchor information and context/acquisition/instance/frontier/invocation scope. The retained managed-state readiness and `_run('state')` relation supplies the underlying HEAD binding and normal/exceptional forwarding premises. No request constraint was imported from the handle path.

`_data` is **not deepcopy**. It accepts exact `str`, `int`, `bool`, `NoneType`, exact lists and exact dictionaries with exact string keys. Dictionary insertion order is preserved. Repeated input mutable aliases unfold into different output containers for each visited path; distinct input containers cannot be merged. Output mutable nodes cannot alias any input node or another output occurrence. Immutable object identity is not established. Unsupported subclasses, floats, bytes, tuples and non-string keys fail without a copy/repr hook. The independent controls executed only an AST-extracted, unmodified pure `_data` body against constructed objects and compared an independently encoded graph to the candidate relation. No application module's operational `_data`, Client, manager, session or launcher method was invoked. These are constructed source tests, not runtime/session observations.

A cycle has no finite normal unfolding under this source. The domain analyzer does not infer a particular observed exception or termination. Supported finite acyclic input is also not proof of adequate stack or memory. Failed conversion can have unobserved partial allocations; absence of a completed graph does not prove those allocations absent or release their obligations. Generic nonempty/aliased data tests are distinct from the exact zero-sequence retained HEAD; they are not claims of acquired state variants.

## Mandatory evidence and validation

The actual public path is `validate → derive → derive_client_state → _checked`. `_basis` reloads current inputs, calls the reviewed predecessor's `derive_client`, checks its exact saved serialization, and reconstructs the current source catalogue and evidence basis. Local CPython call monitoring confirmed actual predecessor invocation. The new relation is mandatory in both ordered context rows; the original observer remains a separate record.

The expected state is tied to the predecessor-validated `evidence/recovery-export-0.json` `/head`, not candidate claims or agreement among substituted reports. Its exact export is 1,676 bytes, SHA-256 `9ca34e1d503d9557bc0bff80bf94093ee4e5b5ecd8eebb11e971e0ae2f94617a`; decoded HEAD is 360 bytes, SHA-256 `b67215d0de14ab7e383db93479faacdc7938659f95142063c50686ea9713b4ee`. Typed HEAD checks reject coordinated changed heads before the broader exact-evidence equality check. The binding, ownership incarnation, managed constructor frame, recovery occurrence and acquisition frontier are preserved. This authenticated frontier is not the state or time of an unobserved later call.

Fresh checks rejected coordinated HEAD changes in claims plus evidence, wrong-instance coordinated rows, missing evidence, altered alias semantics plus both context declarations, malformed state shapes/types, stale scopes, reordered/missing hops, wrong methods/arguments, shallow copies, output merges, unsupported destinations and observation/status escalation. Full semantic validation, full derivation, public receipt validation, source validation and focused inner helpers were exercised. Returned nested objects and context ordering were mutated, then pristine inputs were revalidated successfully. Expectations remained isolated. Equal HEAD values in separate constructed invocations retained different occurrence/hop identities. Both symbolic contexts were tested; they are not two physical executions.

Normal returns require a normal managed-state path, exact source shape, valid detachment and all return continuations. Readiness/manager exceptions cannot carry invented successful manager returns. Protected-region failures can reach error storage and intentional fixed `ClientFailure` under explicit normal continuations. Prefix, storage, helper and client-return unexpected raises keep the reviewed catch classification. Termination alone supplies no Python exception, unwind, retained record, successful cleanup, nonexecution or renewed authorization; prior separately stipulated storage is not erased. Missing or abrupt outer continuation remains unresolved. Normal cleanup in the partial model denotes completion of the existing loop/detail handling, not confirmed closure of every connection.

## Results and failure accounting

| Evidence class | Results | Treatment |
|---|---:|---|
| Fresh independent primary | **273 checks in five groups** | Completed, exact result/progress records agree |
| Fresh independent recovered-root | **196 checks in four groups** | Completed using independently recovered final target |
| Separate actual public CLI | **1 fresh process** | Exit 0, empty stderr, exact receipt identity and both contexts |
| Engineering supplied primary | 171 controls | Inspected with source pins/progress; not rerun or counted as independent |
| Engineering supplied recovered-root | 173 controls | Inspected separately |
| Engineering supplied fresh process | 5 assertions | Source and saved output inspected separately |
| Reviewer failed development attempt | 17 checks before assertion failure | Preserved; excluded from completed totals |

The failed reviewer attempt expected only the inner handler guard and omitted the source-derived enclosing `Try.handlers` annotation and the exception-name binding. The corrected reviewer oracle derives both from the AST. No implementation was changed. The failed source, result, progress, stdout and traceback remain under `failures/reviewer-handler-shape-attempt-1`. All earlier supplied and independent failures remain exact in the input; no historical failure was repaired or included in completed counts.

A separate checkpoint-verifier attempt completed the outer ZIP checks, then tried to read an embedded member from an already closed ZipFile. Its original verifier, outer manifest and factual exception/archive-identity record are preserved under `failures/checkpoint-verifier-attempt-1`. This reviewer packaging error was corrected without rerunning candidate tests. It is not a candidate defect or an additional completed control.

Actual environment: **CPython 3.12.14**, isolated `-I`, no optimization, bytecode writes disabled with `-B`, installed **Cryptography 50.0.2**. No prepared-host 41.0.7 compatibility, installed-wheel byte authentication or new host qualification is claimed. Read-only boundary module definitions/verification helpers were allowed where the predecessor requires them; audit guards prohibited application operations, database/network calls, host-session access and input writes.

## Precise remaining limits

The 18 saved traced invocations and the separate frameless `Client.state()` observer remain distinct. No Client/dispatcher/`_data`/session return chain, actual copy topology, physical connection/reference identity, actual state-call count, exception/unwind/cleanup trace or missing launcher-frame provenance was created. Source/case agreement cannot join the observer to absent frames. Sparse evidence does not establish unobserved assignments or comprehensive runtime coverage.

Static declarations, conditional path premises and current exact saved-evidence validation are the supported result. Complete interruption feasibility, resource sufficiency, full repetition coverage, operational ownership, lifetime multiplicities, real-storage durability and canonical authority remain unresolved. No numerical limit, outcome restriction, retention amendment or replacement architecture was introduced. The retained empty journal is not lifetime zero.

All eleven obligations, four inventory UNKNOWN totals and fourteen lifetime UNKNOWN totals remain. Decision B, retention, allowances, accounting, reservations, ownership, nonce and uncertainty protections are unchanged. SOURCE-ONLY remains unchanged; the cumulative envelope is unadopted; backup remains kernel-only; streams remain UNCOMPUTED; readiness/final binding remain blocked; admission is disabled. No requests, signatures, acquisition, database connection, session operation, dependency installation, Git operation, policy adoption, completed-suite rerun or lifecycle run occurred.

This checkpoint is suitable for return to Engineering-Anchor[2] as scoped independent support. It supplies no new operational authority or automatic next execution step.
