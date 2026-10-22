# Independent review — bounded runtime recovery and laboratory bootstrap

Reviewer: Codex, separate from implementation author SU-Engineering[288C]. I did not author the supplied launcher. This checkpoint is for Engineering-Anchor[2].

**Scoped verdict: CORRECTIONS REQUIRED.** The delivered package is not independently accepted as a cleanly recoverable, executable runtime/bootstrap package. BR-01 prevents recovery from the declared reviewed dependencies; BR-02 leaves a required retained native authentication helper non-executable. The bounded bootstrap/managed-close mechanics have conditional support under the explicitly described test fixture and environment. There is no acceptance of persistent initialization or compatibility with Steve's prepared environment.

## Integrity and preservation

The supplied archive is exactly **12,197,057 bytes; 416 entries; SHA-256 8081d716e9bf20cc527092e383e534285c84358a686118a9843bc047b88cf3b8**. CRC, unique safe member paths, exact manifest membership and all member hashes passed. All 416 extracted input members remained unchanged after review.

The 666-member candidate manifest matches the previously reviewed current candidate exactly. All **666 candidate files, 90 historical files, 43 relationships and ordinal-bearing artifacts** were independently compared. No candidate source, launcher source, configuration, supplied result or earlier closure was edited. Existing scoped support remains at its original scope; no lifecycle or completed review was rerun.

The earlier draft archive, its embedded SOURCE-ONLY integration and the two unchanged candidate-recovery dependency ZIPs were verified. Existing candidate bytes were reused after identity checking and copied into a fresh strict test root. The draft was recovered freshly from its exact ZIP and embedded dependency. Recovery of candidate predecessors was not rerun. The historical managed-occurrence archive is a provenance reference in the supplied package; its source-use excerpt was inspected, but its original ZIP container was not freshly reverified in this review. Current candidate bytes independently establish the runtime sources used here.

## BR-01 — accidental partial output made a mandatory dependency

`provenance/draft-members.json` requires **164** files. The exact reviewed draft archive and its recovered SOURCE-ONLY integration declare **163**. Their sole membership difference is:

```
outputs/.model-input.json.b9MfMd
bytes: 23,330,816
SHA-256: cc896f5e4fb4d558731ec08a625164e29cb3826904f5dc3f67d085de8fe63d3f
```

This is an exact prefix of the declared `outputs/model-input.json`, not a declared member of either dependency archive. The other 163 identities agree. The required file is not supplied by the documented recovery.

**Smallest reproduced witness:** an exact 666-file candidate plus the clean 163-file recovered draft. Both `inputs(...)` and `recover_runtime(...)` reject with `TREE-MEMBERSHIP`; a fresh CLI process reproduces the runtime-recovery rejection before creating a destination. See results/BR-01.json and results/BR-01-fresh-process.log.

For isolation only, the reviewer constructed a separate **as-pinned test fixture**, containing those 163 exact files plus the exact required prefix. The gate then passed and recovered all 93 runtime files. This distinguishes the erroneous dependency from a general candidate/runtime failure. It is not an approved recovery method or a correction. Do not add the partial file to Steve's strict recovered composition to bypass this finding.

Required correction: derive the draft dependency manifest from the declared archive/recovered members, preserve incidental partials outside strict roots, and update affected provenance/bindings consistently. No candidate byte or SOURCE-ONLY semantic change is required by this finding. Existing temporary states bound to the old manifest remain evidence, not objects to rewrite into a new binding.

## BR-02 — recovered native authentication helper cannot execute

The recovered `retained-candidate/native/bin/pe-rfc8032-stream` has the correct source-pinned SHA-256:

```
3d8b65ea87eb5b5a680c9c51c6897a8c32641f1580947046d1cc6c7f765c152b
```

It is created with mode **0644**, without execute permission. `recover_runtime` writes file bytes but does not establish executable permissions. The retained `provider.authenticate` opens this binary, verifies its hash, and executes the same opened inode through `/proc/self/fd`. The retained source therefore establishes the need for execution, independently of a filename convention.

**Smallest reproduced witness:** a tiny correctly signed authentication packet, using an existing public laboratory seed, passed directly to the unchanged retained authentication primitive. It reaches the correctly hashed helper and rejects with `Blocked: BACKEND-UNAVAILABLE`, caused by `PermissionError: [Errno 13] Permission denied`. Exact packet, public key, file identity, mode and traceback are in results/BR-02.json. This is a primitive-level availability witness; the empty claim is not asserted to satisfy a complete policy or appointment. No database, lifecycle, network request or production signing occurred in this check.

This finding does not invalidate the observed successful genesis/head bootstrap path. It prevents extending those successes to executable compatibility of the recovered runtime dependency set. Required correction: recover and verify the necessary executable mode for the exact authenticated helper, without weakening content identity or same-inode execution checks. The reviewer did not change permissions or repair the launcher.

## Runtime provenance and arrangement

The expected layout was derived independently from the current source tree: the complete 90-file historical `retained-candidate` tree, plus the exact current authority/accounting/ownership modules under `prospective`, totals **93** files. All 93 recovered bytes match their candidate sources; the supplied recovered copy and a fresh runtime-only recovery agree. Five retained runtime modules also match their current reference copies exactly.

The import path is source-established: prospective authority selects `retained-candidate/code`; runtime selects `retained-C2/code/bridge.py`; bridge selects the executor session beneath `retained/executor-basis/retained/kernel/candidate/executor`. A fresh-process observation verified 16 loaded runtime modules against their exact recovered paths/hashes and verified the current candidate's `compiler/live_connection.py`. This is not substitution of historical modules by basename. Byte/layout provenance is supported; BR-02 qualifies executable usability.

The new configuration's model/profile/config digests were independently recomputed from the explicit `UNINSTANTIATED-LAB-PLACEHOLDER-I164-v1:<field>` strings. They are laboratory labels, not verified current instantiated-model identities or fixture-derived qualification. Configuration provenance, SOURCE-ONLY designation and admission-disabled status remain explicit.

## Independent execution and supplied evidence

The author supplied 30 successfully completed controls: 16 in the first run, three in the continuation, and 11 in the final run. Two original harness assertions failed because their expected rejection labels were wrong. Their raw traces, original harness versions, temporary databases and final corrected results were inspected and remain preserved in the unchanged supplied archive. They were not rerun or counted as independent execution.

Fresh independent execution comprised **31 temporary-state controls**, plus a separate loaded-source/final-close-lock control, actual normal/optimized environment-gate refusals, and the two defect witnesses. The temporary-state controls exercised:

- Ordered raw construction, confirmed raw close, mandatory managed validation and facade handoff; only state/status/handle are public.
- Authenticated managed head read, fresh-process reopening and reopening after the read; retained facade state/handle calls reject after confirmed close.
- Existing, partial and dangling-link destination refusal without overwriting existing evidence.
- Cooperative lock contention before creation, during raw construction and during managed handoff; a separate control confirmed the lock remains held during final managed close.
- Constructor interruption before ownership attachment, raw-close failure, managed-close failure, caught interruption, and abrupt process exits after raw initialization or managed handoff.
- ACTIVE/failure-marker preservation and refusal of both automatic reopening and repeated creation after uncertain or incomplete ownership.
- Stale configuration binding and canonically encoded corrupted genesis rejection through managed validation.
- Public session refusal in the actual Cryptography 50.0.2 environment without creating a session destination.

These mechanics tests used the explicitly labelled as-pinned 164-file draft fixture and the private `_session` mechanics under **CPython 3.12.14 / Cryptography 50.0.2**. Fault injection affected only subprocess memory, never candidate files. They do not establish a successful public launcher run in the required 41.0.7 environment, nor close BR-01. Test databases, lock files, markers and failures are retained as laboratory evidence. The dangling-link fixture is represented losslessly by its target metadata in the safe regular-file review ZIP and preserved outside that ZIP as well.

A first review preparation attempt and initial generic membership witness encountered other undeclared partials in available/recovered trees. They were not counted as isolated BR-01 evidence. Exact prefixes were preserved outside strict review roots, clean roots were checked, and the isolated witness was then reproduced. These failures and their corrected interpretation remain in failures/ and results/. Their origin and real-storage durability consequences are unestablished.

## Environment prerequisite and Ubuntu command

The public launcher requires **CPython 3.12.14, optimization disabled and Cryptography 41.0.7**. Actual tests confirmed refusal of Cryptography 50.0.2 and of optimized execution. The gate was not mocked or weakened to claim public compatibility. SQLite, executable identity and installed distributions are recorded, but the version gate does not itself reconcile them to an original prepared-environment report.

Steve's exact ENVIRONMENT-RESULT.json, requirements.lock and COMPATIBILITY-RESULT.json were not available in the attachment and were not located by targeted searches. Their prerequisite remains unresolved. No claim is made that these records do not exist on his Ubuntu host.

After extracting this review, the one bounded diagnostic command is:

```
bash UBUNTU-VERIFY.sh
```

Run it from the extracted review directory. It uses the exact prepared interpreter and known host paths recorded by Engineering. It copies the original environment records into a new `/tmp/I164-bootstrap-review-*` evidence directory, invokes the public environment gate, compares a fully pinned `name==version` lock to installed distributions and runs `pip check` without installing anything. Unsupported lock syntax or missing records stop rather than being reinterpreted. Exact original-report reconciliation remains a separate review of the captured records; the probe does not invent an unknown report schema.

The probe then uses the public recovery/session entry points with only that new temporary root. It stops on BR-01 for a clean draft and also checks for BR-02 before any test database creation. It does not fabricate the partial file, alter pins, chmod a helper or use the private environment-bypassing test entry. Its temporary create/reopen/head checks are reachable only after the public preconditions actually pass. The probe is pinned to this delivered launcher source; changed code requires a corresponding reviewed probe update. Local validation of this probe covered syntax and missing-record refusal, not success under 41.0.7. All failures/evidence remain available; the invoking terminal stays open. The command does not authorize persistent initialization.

## Remaining boundary

Close-return observations and SQLite tests do not establish storage durability, rollback resistance, hostile-process exclusion, exclusive key custody or coverage of all writers. The owner lock is cooperative and destination-specific; Python introspection/raw alternate owners remain outside the retained trusted-process/mandatory-entry contract. Injected exits are not operational crash-durability evidence. Public laboratory keys are not operational credentials. No full producer domain, signing campaign, native model instantiation, stream generation or lifecycle was exercised.

Next action: Engineering should correct BR-01 and BR-02 in the bounded recovery package and submit exact changed identities and focused evidence. The prepared-environment records/temporary host probe are an independent remaining prerequisite. No new limit, retention amendment, policy or outcome restriction is adopted.

**SOURCE-ONLY unchanged; readiness/final binding BLOCKED; backup KERNEL-ONLY; streams UNCOMPUTED; admission disabled. No persistent session was created.**
