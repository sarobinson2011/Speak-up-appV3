# Actual results — checkpoint 4N

The demonstrated lifecycle blocker is resolved for the implemented conditional path. The final code passed 370 retained/new tests in 140.536 seconds (17 new lifecycle tests), 11 integrated CLI fixture/recovery/corruption commands under RLIMIT_NOFILE=96, and four legacy GAMMA/DELTA conditional/ACTUAL CLI checks. ACTUAL remains rejected. See results/4N-regression-summary.json, the full test log and CLI JSON. Focused tests are rerun from fresh extraction; results/4N-fresh-extraction.json records the exact preseal archive and actual steps.

Exact 4M parent SHA-256: `119413ad8fe330afa823576f3c46efb528b90729162ae46d6f3a7a8a5612cecf`. All 4,431 parent manifest members verified, plus 2,080 unchanged historical/source/model/contract/amendment/backend/byte-law members selected in verify_4n_inputs.py. SOURCE-INPUT-MANIFEST-4N.json adds the current independently constructed fixtures; IMPLEMENTATION-IDENTITY-4N.json binds executable modules/backend. The original failure was rerun from original code: 92 of 128 canonical documents under 96, then Too many open files. No report of earlier implementation was accepted as a substitute for these checks.

## Bounded measurements

All performance attempts, including one stale-fixture rejection, consumed 78.445 seconds aggregate. Longest attempt 25.730 seconds; external ceilings were <60 each /180 aggregate. Correctness suites are recorded separately, not throughput benchmarks. PREFLIGHT-4N.md contains the estimates made before the larger computation. No retained full pair/link stream was generated, replayed, validated or hashed.

| Final-code measurement | Actual evidence |
|---|---|
| Fixture size and meaning | 768 distinct required shared source fragments, two common dependency branches; 19,318,340 input bytes; complete conditional E ledger with owning values and exact three-scope authentication |
| Distinct acquired semantic files | 822 built initially; on interrupted resume, zero new snapshots and zero new canonical index builds, 3,221 index-backed semantic accesses |
| Independent oracle | Three exact assessor invocation SHA-256 identities (783 consumed dependencies each); all three separate structural/potential counts and exact serialized small link hashes match |
| Complete run schedule | Initial collection interrupted immediately before ordered-ledger receipt publication; resume verifies/reuses completed work; terminal resume checks saved inputs/artifacts |
| Validation child | 25.730 s wall, 25.969 s CPU, peak RSS 90,708 KiB (88.6 MiB); peak 32 process handles under 96, before 4/after 4 |
| Fixture construction/signing child | 0.553 s wall, peak RSS 103,848 KiB (101.4 MiB); peak 5 handles; reported separately from validation |
| Supervisor parent | Initial benchmark supervisor measured peak 9,856 KiB (9.6 MiB); this is not the validation/signing RSS |
| Index cache | Four read-only connections maximum per Store, 1 MiB configured SQLite cache; two Stores may overlap; no resident parsed-value cache |
| Acquisition cache | Peak charged 62,021 bytes under 65,536; 5,491 evictions per collection |
| Diagnostic cache | Peak charged 2,954 bytes; max 32 receipts/64 KiB per provider; total invocation count remains separate |
| Retained benchmark work | 96,048,476 apparent bytes after completion (inputs, snapshots, indexes and journals); initial collection disposable Store files40,344,415 bytes removed at cleanup |
| Repeated isolated cycles | Four cycles of 512 new + 512 repeated documents: 2,048 new and2,048 repeated accesses; 2.006 s wall; peak 22,844 KiB child wait4 RSS; peak 12 handles; every cycle returns to 4 and removes temporary root |

FD peaks are sampled every 2 ms and sampled on pool opens; they are measured peaks, not a proof that sampling catches every microsecond. The hard 96 limit remained active throughout. Per-Store pool bounds and cursor closure are enforced independently of sampling. Python cache accounting, configured database caches, RSS and file sizes are distinct measures. Four repeated cycles each reach the same four-index bound, keep zero parsed-value cache bytes and return handles to baseline; tests verify idempotent cleanup and bounded LRU state. These measurements do not establish arbitrary graph-size constant memory or full-model value acquisition.

## Tests and failed development attempts

Coverage includes independent small Python JSON oracles, lazy large arrays, nested iteration, rereads after eviction, exact snapshot/index mutation, containing-object/Store/job substitution, guarded lazy raw/hex reads, malformed/noncanonical or unavailable input, injected parse/spool errors, missing shared dependencies, both invocation codecs, pre-ledger interruption, repeated pause/resume/terminal reuse and corruption. Retained regressions cover canonical owning bytes, hash collisions, scope/phase joins, native link recovery, signed failures, qualification absence, atomic writes and ordered independent failure collection.

One early lifecycle test expected only ValueError for a substituted journal. The implementation correctly rejected it via FileNotFoundError for an absent substituted catalog artifact. The test was corrected to accept either rejection class; no validation was weakened. Final 370-test run passes. Historical development logs remain, explicitly subordinate to the final run.

An initial benchmark passed before a reporting correction split distinct acquired files from newly constructed snapshots. That code change altered the mechanism identity. A corrective attempt copied the old signed fixture and was correctly rejected with INVALID-EVIDENCE-AUTHORITY (exact mechanism code identities), followed by the incomplete-universe consequence. Its 23.871 seconds are included in the 78.445 total. The fixture was rebuilt/signed under final code, then the final benchmark passed on a fresh job. We did not override source pins or reuse that rejection as success. Initial and failed-attempt logs are retained.

The `semantic_acquisition.recovery` string is a retained legacy label; detailed lifetime counters and stage events distinguish actual completed-index reuse from incomplete-document reparse. Recovery is not constant-time: full exact snapshot/index rechecks on eviction, source/snapshot checks on acquisition misses and canonical signature prefix reconstruction remain required. See LIFETIME-4N.md.

## Verdict and boundaries

The concrete handle-retention/cache-lifetime blocker is closed by executable integrated evidence. No additional unresolved code defect was demonstrated in this bounded review. First-kernel code completeness is not claimed: containing-record projections remain the separate demonstrated adapter boundary in results/4L-projection-boundary.json and NEXT-BOUNDED-TASK.md. Full serialized identities, complete retained-scale supplied streams/authentication, final full-model witness and independently authoritative qualifications remain unestablished. A conditional PASS never enables actual admission.
