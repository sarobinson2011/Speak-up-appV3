# 4L implementation and verification results

Checkpoint 4K's exact ZIP SHA-256 `d4b75689e3531b890511e46ecdef5ba1298620e45152076bf05f867857abcb4d`, all 3,702 manifested members and CRC were verified. The 4L dependency check reverified 2,231 preserved historical source/amendment/model/backend/fixture members. Normative sources, active 4I amendment, selected contract, complete retained model, V2 message preimage builder and canonical Ed25519 binary are unchanged. The transport phase guard and implementation/source-fixture pins changed deliberately.

Final regression: **336 tests passed, zero failures/errors**, in 85.79 seconds including four admission CLI checks. The separate all-phase start/pause/resume/terminal/corruption script passed **16 CLI checks**: **20 CLI checks total**. Full per-test evidence is in `results/checks-4L-verified/check-results.json`; CLI evidence is in `results/4L-cli-recovery.json`. Correctness suite runtime is not a throughput benchmark. The pre-final-guard 335-test run and developmental failures remain historical logs, not substituted for final results.

Tests cover complete GAMMA/DELTA fixtures across all three phases and both codecs; independent exhaustive equal/unequal byte and disconnected closure oracles; missing/unavailable values; wrong owners/contexts/records/types/model/profile/contract/phase/attempt; duplicate/conflicting/extra assignments; noncanonical and truncated encodings; reserved IDs, set order and nested types; forced hash-bucket collisions; arbitrary chunk boundaries; input mutation; corrupted equality database and inherited journal attacks; interrupted acquisition/index/native rows; repeated/terminal recovery; exact agreement with the uninterrupted Python link path; absent qualifications; actual-mode rejection; and fail-closed legacy occurrence acquisition.

Demonstrated fixes: (1) the old unchecked `typed_value` JSON conversion is excluded from occurrence use; (2) a static-only transport guard and missing gate phase names in the Python validator prevented occurrence integration; (3) a terminal cache mutation failure could be lost during recollection of an unused declared carrier member. The final implementation preserves that failure and suppresses positive dispositions/budgets. Developmental runs before the corrected phase guard/mutation handling are retained. No definition was changed.

## Bounded larger fixture

Four required occurrence values each contain an 8,388,608-byte BYTES body, with two exact equal groups. All bytes are acquired, canonicalized/validated, hashed and compared as owning values; this is not signature padding. The independent oracle enumerates only the four-token fixture and checks each scope's exact links, counts and closure.

| Final process | Seconds | Peak RSS |
|---|---:|---:|
| Independent construction/signing | 0.701 | 261,736 KiB |
| Validation plus interruption before ledger commit and resume | 1.383 | 34,992 KiB Python |

Input storage is 68,399,771 bytes; final validation work uses about 87.6 MB durable storage (see JSON for exact value), excluding transient peak copies. Validation RSS excludes child peak; the unchanged native backend/index are small for this fixture. The complete retained native index's separate 4K result (489,856 KiB RSS) is reused, not represented as a simultaneous 4L full-model memory measurement.

Two pre-final-guard subprocesses used 0.705/1.408 seconds; the final corrected fixture construction and validation used 0.701/1.383 seconds. **All four measured subprocesses total approximately 4.20 seconds.** Each was below 60 seconds; the final two shared one externally enforced 60-second corrective attempt. Total remains below 180 seconds. Preflight estimates and the explicit corrective-budget update precede execution in PREFLIGHT-4L.md. No full retained stream was generated, replayed, validated or hashed.

The 8 MiB individual values exceed the ordinary 1 MiB scalar buffer and pass through streamed BYTES/hex handling. This demonstrates bounded value-size scaling, not complete-model source-directory scaling. The latter has a demonstrated remaining metadata code limit: the minimum inline reference directory alone is over 91 MB, exceeding the 16 MiB carrier. The complete 91,157,453,467-pair universe and required serialized full hashes remain untouched/uncomputed.

## Verdict

Bounded owning-value adapters and recovery are implemented and verified for the declared fixed-token source directory and supported codecs. **The full retained-contract first kernel is not yet code-complete.** Remaining metadata-catalog capacity work and source-specific containing-record projection coverage are identified in COMPLETION-CHECKLIST-4L.md. Full-stream execution, final full-model witness and genuine authoritative qualifications are separate outstanding obligations. Actual admission remains disabled.

`results/4L-fresh-restore.json` records restoration from the preseal ZIP, recursive retained-input recovery, CLI recovery and focused occurrence tests. Its preseal digest names the archive tested before adding that result; PACKAGE-MANIFEST.json and the final ZIP receipt cover the sealed deliverable.

A separate local capability experiment (`results/4L-projection-boundary.json`) demonstrates the nullable-field projection gap using a schema-valid complete ASSESSOR-EVENT READ record and a rejected standalone null-as-BYTES value. This is recorded as remaining adapter code, not a protocol defect or a failed equality comparison.
