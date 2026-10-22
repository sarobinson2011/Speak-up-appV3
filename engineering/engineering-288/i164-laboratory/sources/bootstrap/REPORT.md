Version 2: read MARKER-REPAIR.md first. The report below describes the unchanged BR correction and its original 44 controls; 11 fresh marker-only controls are additional and separately recorded.

# BR-01 / BR-02 bounded correction

Implementation author: SU-Engineering[288C], this assistant. Independent closure review pending. No author-independent closure is claimed.

## Findings and source-derived corrections

Both original witnesses were freshly reproduced against the exact 12,197,057-byte submitted bootstrap (8081d716...); original witness records and sources are retained under provenance/review, original launcher/pin under provenance/original, and fresh reproductions under results/old-*. No candidate code changed.

**BR-01:** The old manifest's 164th mandatory file was outputs/.model-input.json.b9MfMd, an undeclared 23,330,816-byte prefix. Exact dependency archive manifests plus the documented recover.py establish only 163 members. code/derive_draft.py verifies the exact draft and embedded integration archives, CRC, safe membership and all hashes, then composes their declared member sets, including manifest bytes. The corrected manifest has 163 entries; all 163 other identities are unchanged. Nothing is excluded by a generic filename filter. Unexpected files still reject. Old partials and old states remain predecessor evidence, not inputs to reconstruct or migrate.

**BR-02:** retained provider.authenticate hashes the exact opened helper inode and executes it via /proc/self/fd. The unchanged byte identity is 3d8b65ea87eb5b5a680c9c51c6897a8c32641f1580947046d1cc6c7f765c152b. Corrected recover_runtime verifies recovered bytes before setting mode 0755 only for that source-required helper, then verifies exact mode and executable access. validate_runtime repeats byte/membership/mode checks before session opening. No candidate source or historical helper is chmodded. Provider content hashing and same-inode execution are unchanged. Mode 0755 is the new recovery permission arrangement, not a claim about an original archived publication mode. Filesystem noexec/interpreter/loader incompatibility may still prevent execution and must reject.

ZIP extraction alone does not necessarily preserve executable bits. implementation/runtime-recovered is a preserved transport copy; use recover_runtime into a new directory to establish and validate runnable layout. Do not directly use the transport copy merely because its bytes match.

## Fresh controls, supplied evidence and failures

44 fresh completed controls: 26 in results/fresh and 18 in results/harness. Separately, two original defects were freshly reproduced against old code, and the original host lock-parser failure was reproduced with the exact supplied lock. Controls include clean declared recovery, duplicate/partial destinations, interrupted recovery, unexpected/missing draft files, actual retained native authentication and invalid signature rejection, altered helper bytes, symlinks and special modes, managed creation/reopening, process interruption and blocked reuse, fresh-process/second-root checks, and strict lock/installed-metadata syntax negatives. Temporary states and logs are preserved. No persistent session was created.

The original 30 author controls and their failures remain supplied evidence inside implementation/. The independent review's 31 temporary controls, separate source-graph/final-close check, public-gate refusals and witnesses are retained as inspected evidence, not rerun as new controls. The host addendum transcript is supplied host evidence, not a new host execution here. Old failure records and prefixes remain preserved; no old result is relabelled as a corrected execution.

Fresh actual runtime tests here used CPython 3.12.14 / Cryptography 50.0.2. As in the prior bounded mechanics tests, tests call private mechanics explicitly and do NOT claim successful public 41.0.7 compatibility. The public environment gate remains unchanged and its mismatch rejection is tested. Native authentication tests verify a retained packet with a public laboratory key; no new key or signature is generated. The empty primitive claim is not a complete appointment/policy.

## Host harness correction

The host addendum establishes supplied version checks: CPython 3.12.14, Cryptography 41.0.7, cffi 2.1.1, pycparser 3.11, SQLite 3.53.1. It also supplies exact identities for the original reports and the complete 11,173-byte lock. It does not establish runtime execution: the earlier probe stopped parsing the lock.

The repaired parser accepts that precise hash-pinned multiline syntax, retains all 125 hashes (100/23/2), and rejects malformed/unfinished continuations, duplicate requirements/hashes, missing hashes, unsupported options, markers and ranges. The Ubuntu probe independently requires the lock's exact original bytes/hash; the parser is not permission to alter it.

The recorded environment contains only three distributions, with no pip. Instead of installing pip or omitting dependency checking, dependency_check.py reads installed Requires-Dist metadata and checks applicable requirements using a narrow, fail-closed numeric-version/marker subset. It does not evaluate arbitrary code; unsupported syntax rejects. Constructed metadata controls are labelled fixtures, not actual installed-host evidence. Actual import/authentication/bootstrap checks follow only if these gates pass.

The updated probe pins this corrected launcher, copies and verifies original report/lock byte identities against the host addendum, enforces the public environment gate, compares interpreter executable identity and environment values, requires exact distribution/lock agreement, checks installed requirement metadata, recovers a fresh temporary runtime, exercises the native primitive, then invokes PUBLIC create/reopen/head paths in fresh processes. No version substitution, test-only override, dependency installation or network execution is used. Failures retain their temporary root and logs.

Original ENVIRONMENT-RESULT.json and COMPATIBILITY-RESULT.json bodies remain unavailable here. The probe preserves them for later semantic reconciliation; their captured hashes are known. Installed wheel bytes are not authenticated merely by matching versions or the lock. A successful probe will establish only the stated bounded runtime compatibility, not operational assurance or complete-domain coverage.

## Preservation and status

All 666 candidate bytes, 90 historical files, 43 relationships, inherited ordinals and exact runtime source bytes remain unchanged. The 93-member runtime layout is unchanged. Only launcher validation/recovery behavior, the 163-member draft pin, the recovery-note supersession notice and corresponding manifests change in the delivered implementation. Exact old/new identities are in CHANGED-IDENTITIES.json. Configuration and synthetic model/profile/config label provenance are unchanged; no fixture digest becomes a current instantiated-model identity. Old session bindings are not rewritten.

SOURCE-ONLY unchanged. Cooperative ownership, trusted process, mandatory managed route and unresolved storage/custody boundaries remain. No lifecycle, completed-review suite, full expansion, network transaction, persistent initialization, policy or limit change. Backup kernel-only; readiness/final binding BLOCKED; streams UNCOMPUTED; admission disabled.
