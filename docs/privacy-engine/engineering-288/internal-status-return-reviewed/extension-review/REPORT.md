# Independent review: bounded internal status-return correspondence

**Scoped verdict: NOT FULLY SUPPORTED — IS-01 remains in status-dictionary, submitted-output and semantic-claim exact-type validation.** The source mapping, preserved predecessors and correction of the twelve supplied type-acceptance instances are supported within their stated limits. The current extension does not consistently reject the same wrong exact types through all affected in-memory validation entry points. No implementation change was made.

Target: **I164-internal-status-return-correspondence-1.zip**, **62,835,317 bytes; 1,845 entries**, SHA-256 `06d3b32fdf83757b40d9963a45a21ca5a5a80d2ca5c4af813655b4ad465f3864`. Review author: **Formal-Lab[6]**, independent of construction author **SU-Engineering[288D]**. Review date: 29 October 2026.

## IS-01: smallest residual witness

After constructing a legitimate normal projection, replace only the session-return `reason` with a `str` subclass containing the same characters:

```python
class S(str):
    pass

submitted = copy.deepcopy(pristine_projection)
v = submitted['hops'][1]['value']
v['reason'] = S(v['reason'])
assert type(v['reason']) is not str
# Actual current result: True, despite the wrong exact field type.
coverage.validate_status_forward_projection(catalogue, case, validated, submitted)
```

No evidence, archive pin, source, reference binding, value characters or source catalogue is changed. `enc(submitted)` equals the pristine encoding, but the exact Python field type is wrong. Both contexts accept this witness through `validate_status_forward_projection`. Arbitrarily named subclasses `S(str)`, `I(int)` and `D(dict)` also reproduce adjacent output-acceptance variants; the result does not depend on spoofing the builtin type name.

An adjacent source-literal key witness also survives the corrected input check: rebuild the exact builtin return-value dictionary with only its `phase` key replaced by `S('phase')`, preserving all values and the same JSON. `status_forward_projection` accepts normal return in both contexts. Full `constructed_projection` also accepts from a fresh recovered root with actual predecessor validation. The defining manager return constructs exact builtin string literal keys. The corrected loop checks container and field-value types, but set-based field coverage does not check those key types. This is another instance of IS-01, not a claim about arbitrary infrastructure metadata keys.

The same gap reaches full validation. Change just `claims[context]['validated_manager_samples'][0]['value']['reason']` to a string subclass with the original contents. **`semantic` accepts in SYMBOLIC-U-ONE; `derive_status` accepts in SYMBOLIC-U-TWO**, with actual predecessor validation invoked. Fresh recovered-root executions confirm both. Their returned rows contain freshly regenerated builtin strings; they nevertheless accept the supplied wrong-type claim. By contrast, changing the reason's characters rejects, and placing the same subclass in `case['returned']` rejects under the corrected return-input check.

The cause is specific and visible in current code:

- `code/managed_coverage.py:1919`, `validate_status_forward_projection`, checks the submitted result using `same`, whose comparison is JSON serialization equality. It does not apply the new exact-type checks to submitted output values.
- `code/correspondence.py:78`, `_check_rows`, compares manager samples and complete claims using the same serialization-based comparison. `semantic` and `derive_status` reach it through `_checked`.
- The corrected `status_snapshot_value` and the `case['returned']` loop inside `status_forward_projection` do apply exact builtin checks. Those original corrections work for the original field-value/container witnesses; they do not cover literal-key types or the adjacent submitted-output and claim paths.

This is a bounded inconsistency in the promised exact-type contract. **No changed public JSON receipt, runtime status exposure, operational execution or admission bypass is demonstrated.** A Python subclass is not representable in JSON bytes; serializing these same-valued objects produces the already legitimate receipt bytes. The public byte API correctly accepts that legitimate serialization and rejects the tested changed booleans and missing mandatory relation. The residual concerns the in-memory APIs' acceptance of wrong exact types, not a forged different public receipt.

The smallest next correction is to apply the existing source-derived exact-type requirements to status dictionary keys and values at the return-input, submitted-output and semantic-claim boundaries before accepting serialization correspondence. Preserve direct returns, existing diagnostics, source boundaries and legitimate values. No runtime implementation, policy or architecture change is justified by this finding.

## Archive, recovery and preservation

The requested outer identity, CRC, safe unique regular membership and all **1,844 manifested hashes** passed. A strict final extraction has **1,845 regular files and 610 implied directories**. Thirteen new exact roots used for successful checks/reproductions were independently gated and verified unchanged after use. All 18 present nested archive occurrences passed their CRC, exact membership and manifested hashes.

The 26 interpretable manifest documents include historical compact-review qualifications and a preserved forensic snapshot manifest from the prior review's packaging-verifier attempt. That forensic manifest is a record of an earlier package, not a declaration of another executable root. Omitted historical outer ZIPs and the previously qualified absent forensic copies are not newly claimed available or verified. Their exact records and qualifications remain in `results/composition.json` and retained recovery notes.

The current decoded predecessor was compared to the exact previously reviewed ZIP, and the current retained review was compared to the exact delivered independent review ZIP. All **1,688 predecessor members** and all **90 non-input review records** match. The prior review identity is 60,792,892 bytes / 91 entries / SHA-256 `a8762d3b81d5f5cbedfb95e5afd8d2c083143ed759f88f2b550cfebfb6de4bf6`. Its omitted redundant embedded input ZIP remains separately retained. The prior 273/196 results, CLI validation, reviewer failure and packaging-verifier failure are preserved as prior results, not re-executed or relabeled as current support.

All **70 inherited producer functions** and other top-level statements remain byte-identical. Six functions were added for this extension. Comparing the preserved affected producer to the corrected producer identifies only `status_snapshot_value` and `status_forward_projection` as changed by the exact-type follow-up. The old and current receipts differ only in extension component identities for that follow-up. Every inherited context field, historical evidence identity, relationship, ordinal, obligation identity and prior limit remains unchanged. Runtime sources changed: zero.

Engineering's separate intermediate recovery archive is retained as a continuity identity only: 62,675,133 bytes / 1,818 entries / SHA-256 `9ac476fe75f53a3b8eea5999f2e32d2b819e883692540e7f567250ef92b06051`. Its outer bytes were not newly verified. Independent recovery used the final 1,845-entry target.

## Source-derived findings

Defining sources remain:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `live_connection.py` | 5,717 | `7344170ca01a2dbbd3afbeb4a6a55c0b95db0edb1a8d74e4fa4638b6dcfc6da5` |
| `lab_bootstrap.py` | 11,481 | `245d4f36d687834aeee064a60d4414b15f7b8babfdb5dec192aa995d93af2b78` |
| `prospective_entry.py` | 9,485 | `a1d80c523ae220228a6b27cac42b5e57a006336e858a8e7db0a75355d6cf2ae9` |

The independent AST analysis derives the six selectors/literals, owner/token conditions, method arguments, normal order and exception destinations directly from these defining sources. The generated catalogue is checked against those expectations. Existing reviewed manager-field origins and recovery/reference bindings are reused unchanged.

`ManagedAuthority.status` (lines 23–24) constructs a new dictionary under its instance lock. It selects `_phase`, `_reason` and `_epoch` as `phase`, `reason` and `connection_epoch`; the other three fields—`actual_admission`, `external_nonexecution_established`, `authorization_renewed`—are literal `False`. The source contract uses exact strings for phase/reason, an exact integer for epoch, and exact booleans for these constants.

`ManagedSession.status` (launcher line 122) directly returns `self.__managed.status()` with no arguments. `_Control.__init__` stores its token; `_Control.status` (entry lines 132–136) looks up `_OWNERS.get(self.__token)`, calls `_fail` if the owner is absent, and otherwise directly returns `owner.wrapper.status()`. Neither forwarding method contains a local catch, conversion, copy or serializer. Required hop order is **manager-return → session-return → control-return**, referring to the same conditional result reference. The manager's dictionary creation and subsequent forwarding are separate relationships; no physical address observation is inferred.

The source does **not** check `owner.failure`, READY or `_dispatch` on this path. All six source-written phase literals—CLOSED, READY, QUARANTINED, CLEANUP_UNCERTAIN, OPEN_FAILED and VALIDATION_FAILED—remain available to conditional diagnostic cases. Epoch starts at zero and has the source's positive integer increment; no upper bound or global-identity meaning is introduced. Arbitrary legitimate reason contents remain supported without a new length ceiling. These type/phase conditions are not proof that every combination has an operationally reachable history.

Independent traversal of `_run` confirms creation of the owner and token, storage in `_OWNERS`, conditional `control(_Control(token))` when `control is not None`, and token revocation in `finally`. That is the designated trusted control route; it is not new caller authentication. General `Client` still exposes no status method. Coordinated in-memory source/pin mutations introducing READY/failure guards, copying, `_data`, wrong delegation or wrong token lookup reject at the defining-shape checks. No new output or evidence-capture destination is authorized.

Missing-owner handling reaches the source-intended fixed `ClientFailure`, distinct from an unexpected modeled raise. `raise ... from None` suppresses displayed context; it does not establish that no ambient exception context exists. Neither status forwarder catches locally, and this route is not a `_dispatch` invocation. Normal return, source-intended failure, unexpected raise and process termination remain separate. Termination supplies no Python exception/unwind, retained error, completed cleanup, external nonexecution or renewed authorization. Outer callback, revocation, launcher retention and cleanup remain conditional/unobserved rather than inferred from this small model.

## Mandatory connection and focused controls

The current public path is `validate → derive → derive_status → _checked`. `_basis` reloads the reviewed client-state predecessor, invokes its actual `derive_client_state`, checks the saved serialization and rebuilds the current catalogue/evidence expectations. Independent call monitoring confirmed this invocation; detached prior summaries did not substitute for validation.

Both ordered context rows require `internal_status_return_correspondence`. Saved manager samples remain bound to the exact trace, source-defined selectors, validated instance, ownership incarnation, constructor frame and recovery frontier. Coordinated trace/snapshot/claim substitutions reject against freshly validated evidence. Wrong-instance, stale acquisition/invocation, mixed-context and selected-sample substitutions reject. Missing/reordered hops, missing fields, wrong constants, invented destinations and readiness restrictions reject in the tested paths. Returned nested results and context lists were mutated, then pristine full public/semantic inputs still passed.

All six original type-witness forms were independently reproduced in both contexts against the affected producer: named-builtin subclasses in `_phase`, `_reason` and `_epoch`, plus dictionary/string/integer subclasses in returned representations. All **twelve** corrected input rejections were confirmed. The affected producer is 192,484 bytes, SHA-256 `903b4369f0e9d009b60c60a260e3dc44c399c0a69629eacdf7870a5d7feba7b0`. The current producer is 193,031 bytes, SHA-256 `57786ded29951dcf613e9dd6c8386fae00d92199344c1ab41df52fa49617f038`; the current adapter is 15,150 bytes, SHA-256 `d084342d7e1e217f6b3337bd261a42fc8d213739f05df12f8ae2beae7c8ddd43`.

| Evidence set | Count and disposition |
|---|---|
| Fresh independent primary | **206 checks**: 198 behaved as required; **8 residual false-acceptance confirmations** |
| Fresh independent recovered-root | **165 checks**: 156 behaved as required; **9 residual false-acceptance confirmations** |
| Separate actual public CLI | **1 fresh-process pass**, exact current receipt, both contexts, admission false |
| Engineering corrected focused | **36 controls**, inspected only |
| Engineering recovered-root | **205 correspondence + 34 exact-type checks**, inspected separately |
| Engineering fresh process | **5 assertions**, inspected only |
| Engineering pre-hardening | **204 results**, preserved separately with affected versions |
| Engineering failed harness | **17 checks before failure**, excluded from completed totals |
| Reviewer initial membership refusals | **5 zero-check failures**, separately preserved and excluded |

The seventeen residual confirmations are variants of **one finding, IS-01**, not seventeen independent implementation defects. Source-route, integrity and preservation audits are separate from those control totals. No Engineering suite, old review campaign or lifecycle was rerun.

The supplied failed 17-check attempt is correctly described: it assigned an empty guard list to a source location whose list was already empty, so the mutation was a no-op. Owner absence is represented by the actual source condition and preceding normal-continuation requirements. The corrected supplied control removes the real `owner_guard` field. The failed source, logs, result and traceback remain intact; they are not evidence of a candidate acceptance defect or completed test campaign.

Two initial roots passed extraction verification, then strict validation refused undeclared regular partial files absent from the target ZIP. Their cause is **UNKNOWN**. The original roots and files were left unchanged; stable snapshots of both partial files, their identities, five zero-check failures and reviewer source are preserved in `failures/initial-root-membership`. No gate was weakened and no file removed to make validation pass. Subsequent checks recovered into new empty roots, verified membership before candidate loading in the same process, and passed the final unchanged-root audit.

## Observation limits and boundaries

Actual test environment: **CPython 3.12.14**, `-I -B`, optimization disabled, installed **Cryptography 50.0.2**. No dependency installation, prepared-host 41.0.7 compatibility claim, installed-wheel byte authentication or host probe occurred. Read-only predecessor definitions/verification helpers were permitted where required; application/session/authority methods, database/network/host access and input writes were guarded against execution.

The 18 saved traced invocations and the separate frameless `Client.state()` observer stay distinct. Saved manager status JSON values are not new observations of forwarding frames or Python object identities. The observer remains unjoined. No new ManagedSession.status/_Control.status frames, physical return-reference relationships, actual forwarding counts, lock timing, owner/token lifetime, exception/unwind or cleanup observations were established. Constructed snapshots, references and path outcomes are not execution history. Equal values do not identify calls or objects. The validated frontier is not the time or state of an unobserved later invocation.

All eleven obligations, four inventory UNKNOWN totals and fourteen lifetime UNKNOWN totals remain. Historical identities, prior scoped support, Decision B, retention, allowances, accounting, reservations and uncertainty are unchanged. SOURCE-ONLY remains unchanged; the cumulative envelope is unadopted; backup remains kernel-only; streams remain UNCOMPUTED; readiness/final binding remain blocked; admission disabled.

No runtime changes, requests, signatures, application acquisition, database connection, session operation, global expansion, policy adoption, Git operation or completed-suite rerun occurred. Return this scoped finding and its preserved witness to Engineering-Anchor[2] for the smallest bounded correction; this review grants no operational authority.
