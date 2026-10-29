# IS-01 independent closure review

**Scoped verdict: IS-01 CLOSED within the retained in-memory exact-type correspondence contract.** No residual witness was found in this bounded review. This does not establish runtime status forwarding, physical reference identity, complete execution coverage, readiness, final binding or admission.

Target: **I164-IS01-correction.zip**, **68,317,556 bytes; 2,053 entries**, SHA-256 `5915d8d409d043e9dd95535e91880263e26c776220b8c6d48bf75690e3fc60a9`.

Review author: **Formal-Lab[6]**, independent of construction author **SU-Engineering[288D]**. Date: 29 October 2026. No implementation code was changed. Engineering's correction and its controls are supplied evidence, not independent confirmation.

## Identity, recovery and preservation

The requested identity, CRC, safe unique regular-file membership and all **2,052 manifested hashes** passed. Every successful or failed test root was verified unchanged at the end: **seven roots**, each with **2,053 files and 646 implied directories**. The failed review assertion did not alter its input root. Present nested archives comprise **18 occurrences**, each verified for CRC, membership and member hashes. The 28 interpretable manifest documents retain their recorded compact-history qualifications.

All **1,845 original target members** match the exact previously reviewed target archive. All **157 non-input members** of the prior independent review match its exact delivered archive, including witnesses, failed attempts, the two preserved forensic partial files and their UNKNOWN cause. The prior review's sole omitted member is its redundant embedded original ZIP; its decoded bytes are present under `original/`. Both historical outer archives were available locally for exact identity and member comparison. Their omission from a decoded recovery layout is not a new runtime dependency or permission to reconstruct different archive bytes.

The supplied intermediate recovery archive is a continuity record, not a newly verified outer archive: 68,223,178 bytes / 2,038 entries / SHA-256 `299ad9399c4731c65dad2661da66ca2b15b65aa2b972effc759925d931475113`. All 2,037 entries in its retained input manifest match the final checkpoint, and that manifest's canonical serialization matches its recorded identity. Independent recovery used the **final 2,053-entry archive**. Historical missing outer archives and forensic snapshot manifests remain qualified exactly as before; they are not treated as new executable-root requirements.

Declared intentional implementation changes match the actual bytes and supplied diffs:

| Current component | Bytes | SHA-256 |
|---|---:|---|
| `code/managed_coverage.py` | 194,665 | `4eaf2faa53a149d56161fbb4247e2eb18661244a5c5afc1023d2ab73422e900e` |
| `code/correspondence.py` | 17,994 | `0a8c0f97e769eca4c0629136b6eac28d1473094691a1d11beaf4d7412316d79d` |

All **70 inherited producer functions**, their preceding source text and unrelated historical validators remain unchanged. Five existing status-extension functions gain local type checks, and two producer helpers are added. `compile_status_forward` remains unchanged. The connecting adapter adds local type preflight and the new decoded-original recovery gate; its public `validate`, derivation/assembly and evidence-comparison function bodies are unchanged. The final adapter adds one explicit root-directory lstat guard relative to Engineering's primary test adapter. Runtime source changes: **zero**.

The corrected receipt is **2,776,568 bytes**, SHA-256 `4db6c9d4da0110055f483fdf5ef958a12edd9362b8315704ff0cf5143470c468`. Its only differences from the affected receipt are the two current extension component identities. Both context rows, historical evidence, relationships, ordinals, prior findings and obligation bindings are unchanged. The authenticated 56,813-byte remaining-obligations document still contains exactly O01–O11; its identity is not itself an eleven-entry list.

## Original witness reproduction and corrected rejection

Fresh execution against `original/code` reproduced the original same-valued `str`-subclass reason acceptance, adjacent `int`/`dict` output subclasses, semantic-row acceptance and the subclassed literal `phase` key in both contexts. Full old `semantic` and `derive_status` calls accepted coordinated wrong-type reasons in both contexts and regenerated builtin strings. Full old `constructed_projection` accepted the key witness in SYMBOLIC-U-TWO. Monitoring confirmed that all three full old calls invoked the actual retained predecessor. This is a focused reproduction of IS-01, not a rerun of the previous review campaign.

The corrected APIs reject those witnesses through return-input, submitted-output and semantic-claim boundaries. Tests changed each of the six source-literal status keys separately, not just the original `phase` key. Adjacent tests covered nested lists/dictionaries, scope and reference containers, scalar subclasses, metaclass-equality hooks, wrong builtin field types, tuple substitutions, snapshot keys, source byte types and nested catalogue/boundary types.

The correction checks exact class identity using `is`, before value equality, encoding, coercion or copying. The tree walk accepts only exact builtin representation containers and scalar leaves, with exact string dictionary keys; the existing field/source checks then enforce the narrower status requirements. The generic allowance for a builtin leaf is not permission to use it in the wrong field. Independent tripwires confirmed rejection of wrong-type input/output/claims without calling JSON encoding or deepcopy. Foreign metaclass equality and container hooks were not invoked.

Repeated references to a finite representational value remain accepted. Cycles reject as non-finite representations. The change adds no reason-length ceiling, epoch cap, call-count limit, lifetime bound, phase restriction or policy. Existing finite-number serialization behavior is unchanged.

Coordinating malformed claims with malformed comparison rows does not evade exact-type checks. Coordinating legitimate builtin but false reason values across raw trace evidence and both context claims rejects against freshly validated predecessor evidence. Missing/reversed/duplicated context claims, wrong instance, stale frontier, missing/reordered hops, changed result references and unsupported qualification claims reject in the exercised paths.

Returned nested output, assembled bundles and public results were mutated. Subsequent pristine derivation/semantic/public validations remained correct. The validation expectations did not become aliases of returned objects.

## Source semantics and public-byte distinction

Independent AST checks reconfirm the manager's six literal keys and selectors, including three literal `False` constants. `ManagedSession.status` still directly returns `self.__managed.status()`. `_Control.status` still looks up `_OWNERS` with its token, calls the fixed failure when no owner exists, and otherwise directly returns `owner.wrapper.status()`.

There is no new `_data`, deepcopy, serialization, `_dispatch` or READY requirement in the runtime path. Source-admitted diagnostics were exercised conditionally in all six phases, including outside READY and with an existing owner failure. Empty, Unicode, NUL-containing and longer reason strings and large nonnegative epochs remained admitted by the existing representation contract. These constructed cases are not proofs that every combination has an operationally reachable history.

Owner absence, source-intended fixed failure, unexpected modeled raise and process termination remain distinct. Termination establishes no Python exception, unwind, retained error, completed cleanup, external nonexecution or renewed authorization. General-client status destinations remain unsupported. Symbolic direct-reference correspondence does not claim observed physical object identity.

**IS-01 was an in-memory type defect, not a demonstrated forged public JSON receipt.** JSON cannot retain a Python subclass distinction. Independently serializing the same-valued subclass witness produces the exact legitimate receipt bytes, and those bytes correctly pass public validation. The wrong-type object itself rejects when submitted to the in-memory APIs. The public exact-bytes contract still rejects a bytes subclass, a missing mandatory relation and the affected old receipt's stale code bindings. Two pristine public validations pass before and after returned-result mutation. These are public API executions; no new host or session command was run.

## Independent versus supplied results

| Evidence | Disposition |
|---|---|
| Independent original-witness reproduction | **14 completed checks**: original acceptances and actual predecessor invocation confirmed |
| Independent corrected recovered-root controls | **154 checks**: 34 positive, 120 rejected negatives |
| Independent corrected fresh full entries | **20 checks**: 5 positive, 15 rejected negatives |
| Independent adjacent source/type/shape controls | **27 checks**: 1 positive, 26 rejected negatives |
| Independent public entries | **6 checks**: 4 positive, 2 rejected negatives |
| Engineering focused | **268**, inspected only; primary adapter precedes the final root-directory guard |
| Engineering fresh process | **21**, inspected only; final code |
| Engineering recovered-root | **269**, inspected only; final code |
| Engineering recovered public entry | **2**, inspected only; final code |
| Engineering original reproductions | **14**, inspected separately |
| Previous review and older supplied results/failures | Preserved unchanged; not rerun or merged |

There are **207 completed corrected checks**, plus **14 completed original-witness checks**. Counts are not runtime occurrence coverage.

A reviewer audit mistakenly treated `unchanged_obligations` as a list instead of its bytes/SHA-256 identity. The initial focused process reached **153 checks** before the same final metadata assertion failed. Its source, progress, failure and recovery records are preserved in `failures/reviewer-obligation-pin-shape`; that attempt is **excluded from completed totals**. The correction verifies the authenticated obligations document and its O01–O11 members. The separately completed 154-check recovered-root group uses the corrected reviewer assertion. No candidate defect, candidate edit or weakened gate is attributed to this harness failure.

Actual environment: **CPython 3.12.14**, isolated mode, bytecode writing disabled, optimization disabled; installed **Cryptography 50.0.2**. No dependency installation, 41.0.7 compatibility claim, installed-wheel byte authentication or new host qualification is made. Guards prohibited application/session method execution, database/network operations, host session access and writes to recovered inputs. Actual predecessor validation was monitored; detached prior summaries did not substitute for it.

## Retained limits and authority boundary

The source-defined direct return is supported conditionally. Runtime ManagedSession.status/_Control.status forwarding frames, physical reference identity, actual forwarding counts, complete history/repetition coverage, owner/token lifetime and outer exception/cleanup observations remain unavailable. The 18 saved traced invocations and separate frameless `Client.state()` observer remain distinct; the observer is unjoined. No constructed control becomes a runtime observation.

All eleven obligations, four inventory UNKNOWN totals, fourteen lifetime UNKNOWN totals, Decision B, retention, allowances, reservations, accounting and uncertainty protections remain. SOURCE-ONLY unchanged; cumulative-envelope unadopted; backup kernel-only; streams UNCOMPUTED; readiness/final binding blocked; admission disabled.

No implementation/runtime change, request, acquisition, database connection, session operation, policy adoption, canonical rebinding, Git operation or completed-suite rerun occurred. Return this scoped IS-01 closure checkpoint to Engineering-Anchor[2]. It grants no operational authority.
