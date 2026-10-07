# Checkpoint 4P results

**All thirteen generated-event forms are implemented and tested.** Complete
parser/acquisition events now feed owning values, exact equality, scoped links,
pure Ed25519 authentication and ordered ledger collection. The demonstrated
lazy-ledger deepcopy defect is fixed. First-kernel implementation is complete
for the declared finite conditional contract within its explicit capabilities;
no further required code gap was demonstrated. Full retained-model execution
and authoritative qualification are not established. Actual admission is disabled.

## Verified inputs and unchanged boundaries

4O ZIP SHA-256:
`53a1c31381641fe8056a855fd2c2edf48c0617187e9e212e1205be08dae228bf`.
All 6,173 parent manifest members verified, plus 3,718 selected historical active
files compared byte-for-byte against that parent. Selected contract SHA-256 is
`2bbd9d52e1591bc12adc9cc0983c1686ade2cfc4cbcbeb95b6025259d5bf07fc`;
retained model identity is
`08d6e7fb1e0cf37cc7effa76b50eaff0459abc158d9c6f0da52c6c58372b14f1`.
Active 4I, selected source/model bytes, primitive codecs, equality code, native
link recovery, 4N storage and canonical crypto backend remain unchanged.
SOURCE-INPUT-MANIFEST-4P.json and IMPLEMENTATION-IDENTITY-4P.json record exact
source, fixture and implementation identities. Historical inputs are retained
inside the exact 4O archive; new conditional fixtures are regenerated and signed.

## Actual tests

- **409 regression tests passed in 349.565 seconds**, zero failures/errors.
  Includes 19 new generated-event tests. Full log: results/4P-regression-tests.log;
  summary binds its SHA-256 and exact tested implementation.
- Independent Python/cryptography fixtures implement all thirteen forms, both
  contexts, two attempts, all four parser branches, all three material statuses,
  exact parent/ordinal/field joins and source/model/profile/contract/phase binding.
- Integrated independent 96-token oracle across E, PRE-EXECUTION and
  PRE-COMMITMENT: all exact value bytes, scoped whole-stream digests, separate
  structural/potential counts and canonical signatures match. Explicit
  laboratory hypotheses remain labeled; actual qualification/admission are false.
- Missing/duplicate/extra/conflicting events; wrong source, metadata, grammar,
  parent, phase and ordinals; dishonest status/output; malformed/noncanonical
  inputs; unavailable parent records; null reference and missing list child;
  dependency gaps; byte mutation; replay after eviction; standalone bypass;
  forced equality-index collisions; interruptions and repeated/terminal resumes
  all exercised. Whole nested event JSON/hex is parsed across 1-, 7- and 31-byte
  chunks. Existing adversarial authentication/failure-precedence tests remain.
- **16 CLI checks passed. Fresh extraction passed** package/input verification,
  all 19 generated-event tests, all 16 CLI checks and coverage regeneration in
  220.166 seconds. Results are in results/4P-cli.json and
  results/4P-fresh-extraction.json; recovery commands are in RUN-4P.md.

Correctness tests are not throughput benchmarks. Preflight estimates preceded
both bounded performance runs; the external supervisor enforced their ceilings.

## Bounded performance and cleanup

Complete 96-token conditional fixture with **128 required semantic dependencies**;
source input 36,529,684 bytes. Validation computes real semantic/invocation/event
checks, not opaque padding. All 96 equality-index values and all scoped digests
are compared to independently constructed exact oracles.

| Measurement | Actual |
|---|---:|
| Fixture construction/signing child |0.602 s wall; 140,232 KiB peak RSS|
| Validation + pre-ledger interruption + resumed validation + terminal reuse |43.772 s wall; 44.476 s CPU; 85,484 KiB peak RSS|
| Benchmark supervisor parent |9,856 KiB peak RSS|
| Aggregate benchmark execution |44.374 s (180 s ceiling)|
| Longest benchmark child |43.772 s (60 s ceiling)|
| Peak process handles |42 under imposed 96 limit|
| Handles before / after |4 / 4|
| Retained apparent work disk, including input and recovery state |99,582,232 bytes|
| Peak source acquisition cache |62,149 bytes under 65,536 limit|
| Open semantic indexes |4; 1 MiB configured SQLite cache budget|
| Parsed-value cache |0 bytes|

Resumed validation reports zero new document builds, 4,543 reused indexed document
accesses, 3,499 reopenings and 3,495 evictions. This is reuse of exact-checked
immutable snapshots/indexes, not proof from file metadata. Source files, input
identities and receipt prerequisites are checked again. Scratch stores close
and remove temporary roots on completion; regression tests cover failure cleanup.
Parent memory is separate from signing and validation children. Figures are peak
RSS, not claims that all allocated memory is cache. Disk is apparent file bytes.

Preflight estimates intentionally allowed wider memory/disk ranges; this fixture
was smaller on disk than estimated. Runtime is specific to this machine and
small source law. Do not multiply it by pair count: no retained pair/link stream
was processed, and source record sizes/guard outcomes dominate adapter costs.

## Recovery and limitations

Generated-event scratch directories rebuild after interruption, and all owning
values/dependencies are revalidated before equality-index reuse. The semantic
index pool and completed acquisition snapshots are reusable after exact byte
checks. Native supplied-link recovery preserves its exact stream/digest state;
pure Ed25519 still reconstructs state by rereading the consumed prefix. Terminal
reuse still exact-checks the complete input/artifact set. No constant-time resume,
source authentication from journals, or qualification from signed fixtures.

No full retained stream was generated, replayed, validated or hashed. The
91,157,453,467-pair full-stream identities, complete actual owning-value witness,
final full-model integration and genuine qualified three-scope evidence remain
execution/input obligations. Unsupported production grammars require their
exact concrete source specifications; they are not silently treated as absent.

The initial smoke run deliberately remains as development evidence: it exposed
the lazy-ledger deepcopy error and a fixture phase type spelling (ENUM-PHASE)
that did not match retained ENUM-STAGE. The fixture spelling and demonstrated
ledger implementation defect were corrected. No failed/partial run is counted
as success. Historical 4O reports describe its old boundary, not current 4P.
