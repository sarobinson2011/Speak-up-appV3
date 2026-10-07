# Semantic-document, index and provider lifetime — checkpoint 4N

## Scope and source grounding

This closes the demonstrated 4M resource lifecycle defect, not the definition or qualification boundary. S90 section 3 requires complete actual owning records; its canonical-security-byte clauses (accepted/sources/PE-G4-SOURCE-S90.md, lines 400–413) require exact source objects and typed-field/record identities. Required dependency closure and exact assessor invocation remain mandatory. Eviction cannot discard a semantic duty or become a reason to use symbolic values. The active 4I field-specific amendment, selected contract, model, native predicate/equality code, byte codecs, canonical pure Ed25519 backend and failure ordering are unchanged; see SOURCE-INPUT-MANIFEST-4N.json and results/4N-dependency-impact.json.

The exact 4M archive is retained without alteration. Its original failure witness, independently rerun before this repair, acquired only 92 of 128 tiny documents with RLIMIT_NOFILE=96. Each Document previously kept its SQLite connection until Store.close. The new Store no longer retains every Document/value in a Python dictionary or a cleanup list.

## Implemented lifetime

| Resource | Lifetime and bound |
|---|---|
| Canonical-index writers | One active parser writer per Store; commit and close at canonical EOF; close/remove on interrupted or invalid parse |
| Read-only index connections | LRU pool of four per Store, 256 KiB configured SQLite cache each; eviction closes the connection |
| Document locators | Disk-backed map, 256 KiB SQLite cache; contains descriptors, not parsed Python values or open connections |
| Query cursors | Closed before yielding rows; pages of at most 64 rows permit nested traversal across eviction |
| Acquired-source cache | 64 KiB charged metadata, at most 64 Blob descriptors; exact bytes remain in private/retained files |
| Range-digest cache | 64 KiB charged metadata, at most 64 entries per Scheduler; cleared on close |
| Invocation dependency worklist | Temporary SQLite table with exact digest primary key and completed flags, closed/deleted in finally |
| Invocation diagnostic tail | At most 32 receipts/64 KiB per provider, with total count; all invocations are still acquired, checked and compared |
| Cleanup | Idempotent Store.close closes pool, locator and auxiliary handles, clears refs and removes private scratch, on success or exception |

Cache charges count Python keys/value metadata and a bookkeeping allowance; they are not a byte-perfect heap profiler. Configured SQLite cache budgets and measured whole-process RSS are reported separately. Two Stores can overlap in the scheduler (eight pooled connections / 2 MiB configured index caches total), with separately bounded active writer, catalog and assessor handles. Required model/ledger/live graph indexes, closure traversal state, caller-held records and runtime/library memory are not represented as constant-size caches. Accepted depth/scalar capabilities remain unchanged: 128 nesting levels, 1 MiB ordinary scalar buffer, 64 KiB small-value materialization, streamed large hex. A query page is bounded by 64 rows and those scalar rules. No OS resource limits are increased.

Provider invocation no longer holds a Python map of every dependency Blob/hex string or a resident worklist. It traverses every required dependency into a disk table, emits lexically ordered exact consumed-source bytes, reacquires/rechecks each entry, and streams the two inherited invocation codecs. The independent fixtures reconstruct CALL/trace input bytes without invoking the new provider. Diagnostic tail truncation changes only operational reporting, never duties, invoked assessments, traces, qualifications or admission results.

## Exact reopen and trust boundary

A document descriptor binds the complete containing snapshot path/range/length/hash, canonical index path/hash, implementation and current job bindings, local Store instance, and applicable durable receipt. Reopening an evicted index rehashes the exact entire containing snapshot/range and entire index, checks code/job identity, and checks the authenticated complete receipt and its input/artifact joins. Matching file size, timestamps, inode metadata, permissions, locks or journal possession are not the byte-identity test. Same bytes at a different containing path/range or another Store/job are not silently substituted.

Large Node.raw and Hex reads carry a containing-document guard: they cannot bypass reopen checks after their original index has been evicted. Completed locator values are not held in a resident parsed-value cache. On acquisition-cache misses, both the original input and retained snapshot are forcibly rehashed even if previously checked during the current schedule. Small materialized roots also pass the exact reopen check.

The executor, its MAC key, and private snapshots/indexes must remain trusted and quiescent during an active invocation/handle's use. A currently resident connection or digest-cache hit is not a continuous defense against a malicious concurrent writer. Users must provide immutable input custody or isolate the execution; timestamps/permissions alone are not proof. A fresh Scheduler rechecks inputs; terminal receipt reuse validates the saved prerequisite/artifact graph. This is computation reuse only, never source authentication or competent qualification. Authentication remains the unchanged exact original V2 message and canonical pure Ed25519 backend.

## Recovery costs and cleanup

Completed exact indexes/snapshots can be reused after their byte/receipt checks. An interrupted parser restarts the affected incomplete document; it cannot publish a complete index receipt. Incomplete acquisition and native link work retain their existing recovery behavior. The canonical pure Ed25519 backend still reconstructs state by reading the consumed original-message prefix; no partial signature verification succeeds.

For an evicted document with B snapshot bytes and I index bytes, reopen adds B+I hash I/O, plus receipt/catalog verification. Acquisition eviction can add two source-sized hash passes (original and snapshot). Frequent interleaving of more than four documents deliberately trades I/O for bounded handles; repeated eviction can cause repeated full hashes. Query iteration uses LIMIT 64/OFFSET, which may repeat SQLite scan work for very large arrays. Disk indexes/snapshots grow with total acquired content even though handles/caches do not. No constant-time recovery, constant total memory, one-pass acquisition, or full-scale runtime bound is claimed.

Cleanup removes disposable Store files and closes handles in success/failure paths. Durable completed stage artifacts remain for exact verified reuse. CP4N collector/stage versions reject CP4M journals; source bytes from historical checkpoints remain unchanged. Recovery requires preserving inputs, key, checkpoint and stage artifacts at their bound paths; relocation starts a fresh job. The test suite exercises malformed/missing documents, injected parse/spool exceptions, pre-ledger interruption, repeated resume, corrupt/stale indexes, changed bytes and cross-job substitution. Retained scheduler tests cover atomic receipt-write failures and native/authentication interruption.

## Qualification

A successful conditional laboratory result is an executable implementation result only. Appointments, source ownership and semantics, visibility/classifications, assessor competence/soundness and qualified three-scope evidence require independent authoritative inputs. No cache, index, hash, signature or journal supplies those facts. Actual admission remains disabled.
