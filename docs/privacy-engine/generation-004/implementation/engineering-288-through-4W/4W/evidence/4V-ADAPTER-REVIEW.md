# 4V acquisition and recovery review

## Verdict and scope

Implemented: a conditional deterministic byte emitter, bounded seekable spooling, and durable continuation of the **retained independent supplied-row parser**. The new emitter actually writes TSV bytes; the validator reads those bytes. The immutable-file source is an adversarial/laboratory fixture interface capped at 256 MiB, not a production acquisition adapter. The complete retained model index is supported. No full retained stream was processed in 4V.

This is static laboratory acquisition. It is not external source authentication, three-scope correspondence, a completed four-file object, qualification, or admission. `actual_admission`, `source_authenticated`, and `four_file_authentication_complete` remain false, including on success. The 4S model and 4U identity envelope are unchanged. Historical signatures and journals are not current-job receipts.

## Source and implementation correspondence

Accepted source references are preserved in `evidence/TEXTUAL-IDENTITY.json` and the exact parent 4U ZIP: S90-FCR lines 385–390 (closed model), 773–809 (static structural/potential serialization and scope); S70 lines 745–749 (header), 967–987 (exact link bytes and V2 object/signature preimages). No source or identifier law is amended.

`retained/link_stream/native.cpp` is byte-for-byte the retained 4P/4B validator (SHA-256 `f3850b9cb2721d437e9d81810b9b69ca4e360ca7e7d7f1b06b82e70376cdd88c`). The new `validator_service.cpp` includes its **unchanged Index and Parser**, replacing only its file driver with a bounded persistent spool driver and state serialization. Its model lookup and membership predicate remain separate from generation. The new emitter follows the retained generator's lexical iteration/merge, with an explicit resumable byte cursor; the independent small oracle constructs sets and sorts them independently.

| Obligation | Executable check |
|---|---|
| Exact header, TAB/LF framing, ASCII domains, no BOM/CR | retained `Parser.line`; bounded pending line; terminal LF |
| Exact endpoints, relation kind/order, structural membership | retained complete model lookup and structural binary search |
| Original i<j potential orientation, static predicate | retained original-index and fixed-group tests |
| Lexical four-cell uniqueness/order | strictly increasing previous/current tuple |
| Global ordinal | one-based, minimum six decimal digits, checked against cumulative rows |
| Structural completeness | legal unique structural subset and exact structural count |
| Potential completeness | legal unique potential subset and exact predicate cardinality |
| Exact serialized identity | one cumulative SHA-256 state updated with consumed bytes; expected byte count, EOF and whole digest all required |

Completeness is not cardinality alone. For each finite required set R, the parser first establishes every supplied row is in R and no row repeats. Therefore the parsed rows form a subset S of R; |S|=|R| proves S=R. Positive structural relation orders and potential order zero are disjoint. Both equalities are checked separately. A same-cardinality illegal substitution, or a missing row from either component, fails. No sample establishes these full-stream equalities.

## Interface and exact bindings

`CP4V-BYTE-SOURCE-1` binds exact model, contract and descriptor paths/lengths/SHA-256, serialization identifier, source kind and expected complete text length/hash. For the retained 4S model, the adapter additionally requires the pinned contract, descriptor, text digest, byte count and deterministic-laboratory source; arbitrary caller metadata cannot rebind that model. For fixture models the source is explicitly laboratory data, not source-grounded full-model correspondence.

Each job binds a new random nonce, absolute job path, source manifest, spool ceiling, native binaries/sources, retained parser, Python controller/CLI/interpreter identity, native shared-library file hashes and state format. Retained descriptor-to-model correspondence comes from 4U's exact 4T/4S evidence; it is not reasserted by a caller. Native workers hash the descriptor bytes through the same stream used to parse the index.

Source operation: `(cursor, global offset, byte ceiling)` -> `(actual bytes, start, end, new cursor, SHA of spool, EOF flag)`. Cursor includes lexical from/to positions, structural position, potential-emitted flag, global row ordinal, byte offset, header state and partial emitted row. No descriptor hash substitutes for emitted-byte hashing.

Validator operation: `(spool start, exact spool bytes/hash, saved state, new-byte budget)` -> paused/rejected/complete result plus parser/SHA state. A spool is hashed in full before parsing; parsing starts at `consumed_global_offset - spool_start`. Its exact hash is rechecked on each partial-spool invocation. The successful output digest is updated only from bytes actually consumed by the parser driver. Spool hashes are never concatenated or folded into the whole SHA.

## Durable publication and interruption

The local execution key is a private random 32-byte file outside the job. IDENTITY and STATE carry HMAC-SHA256 over canonical JSON. The key is a local integrity mechanism, not an appointed source key.

1. Generate at most the spool ceiling into `spool.part`; fsync it, verify its complete byte hash, rename to `spool.bin`, fsync directory.
2. Atomically publish source cursor and spool identity (`STATE.json.part`, fsync, rename, directory fsync).
3. Validate bytes. Persist cumulative SHA-256 chaining words, pending SHA block and byte length; parser pending row, header flag, lexical predecessor, ordinal/rows, separate counts, consumed position and source cursor.
4. Atomically publish that validator state. Only then publish spool eviction and remove the old spool.

All read bytes on a PAUSED/successful path are represented by completed rows or the saved partial row: saved read-ahead is zero. A terminal parser failure can have unparsed bytes in its last read chunk; `read_ahead_bytes` is null, the consumed-prefix digest is labelled as such, no resumable state is returned, and no whole-stream success is reported. There is never a success based on an incomplete input.

If interruption precedes state publication, the prior state remains authoritative; an orphan spool is discarded/regenerated. If publication succeeded before process death, it is reused. A current spool missing after recovery is regenerated from its saved **starting cursor**, and its exact bytes/hash/end cursor/EOF must match. A mutated present spool is rejected, not silently replaced. No completed prefix is reread merely because its spool was evicted. Atomic-write, partial-header/row, repeated-recovery, eviction and worker-death paths are exercised in tests. Interrupted initialization before STATE exists has consumed zero stream bytes; preserve that directory and initialize a new job path.

Only one live state is authoritative. Backups may retain earlier valid states; restoring one deliberately rolls progress back to that checkpoint and recomputes from its cursor. There is no anti-rollback service and no claim of protection against a malicious key-holding operator. A corrupt state does not trigger automatic fallback to an older checkpoint.

## Trusted execution and immutability boundary

The reuse claim assumes a trusted executor/runtime, custody of the local MAC key and checkpoints, and **quiescent exact bound inputs while a worker runs**. On every reopening, the adapter rehashes all model/contract/descriptor (and small file-source) bytes and compares code/native/runtime identities. A resumed spool is completely hashed before use. Permissions, path, size, timestamps, advisory locks or journal possession are not asserted to prove byte identity. Stat comparisons only supplement byte checks for concurrent writes.

The MAC attests that the executor previously saved a prefix SHA/parser state under this boundary; it is not independent proof of every evicted prefix byte. Without trusted state custody, prior bytes must be regenerated/revalidated from a trusted checkpoint (possibly the start). No cryptographic technique can recover discarded untrusted SHA internal state from a final digest alone. Concurrent malicious input mutation after hashing or a compromised executor/key is outside this conditional boundary; use an independently governed immutable snapshot/acquisition design for genuine source evidence.

Recovery cost is index reload + exact small-input hashing + at most the active spool's regeneration and validation since the last committed state. It is not constant time, and partial-spool resumption rehashes the whole current spool. Avoid tiny production new-byte budgets; consume one spool per normal step.

## Failure and authentication integration boundary

The unchanged parser preserves its local schema/digest/universe failure rules and structural-before-potential finish checks. Its wrapper rejects invalid/corrupt state or unavailable/mutated inputs without producing semantic success. The ordered multi-evidence admission collector is not invoked or replaced by this standalone adapter. A future integration must map these results into that collector and continue collecting independent failures according to the accepted precedence; stopping this local worker is not a verdict on other evidence.

The retained file-backed `large_auth`/`integrated_auth`/recovery scheduler path is still required for genuine source-owned acquisition. This adapter does **not** provide all four files, final outer-profile/V2 object binding, appointed public keys/signatures, scoped owning values, qualifications, assessor evidence, or a source-owned delivery policy. It does not call or modify the canonical pure Ed25519 backend. That backend's prefix reconstruction remains separate; this new SHA-256 state export cannot be used as an Ed25519 recovery state or as a signed message.

## Focused defects found and corrected

An injected validator death exposed `BrokenPipeError` during pipe cleanup, masking the first interruption. Cleanup now closes all pipes without masking that error; the last committed state resumes to the oracle result. Tests also avoid reliance on host-visible `/proc/<child-pid>` in this container by checking actual `getrlimit` values reported by each native child. No accepted definition, retained parser, model or predicate defect was found or changed.
