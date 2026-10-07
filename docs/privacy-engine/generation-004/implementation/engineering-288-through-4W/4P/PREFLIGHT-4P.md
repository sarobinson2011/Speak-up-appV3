# Bounded computation preflight — 4P

No full retained pair/link stream will be generated, read, replayed or hashed.
The selected model/contract and retained results are reused by exact identity.

Correctness fixtures: independently constructed 96-token model, 4,560 tiny oracle
pairs, 92 generated-field occurrences plus 4 S90 projections, two contexts,
all four parser branches, 12 complete parser/acquisition events. This is a new
small conditional test model, never a reduced retained-model conformance claim.

Bounded larger benchmark: the same complete event/value/scope/ledger fixture with
128 required semantic dependency documents. Estimate 50–100 MiB of source input,
150–350 MiB temporary/snapshot/index disk, 40–120 MiB validator child RSS and
100–350 MiB fixture signing RSS. Supervisor should remain below 20 MiB. Expected
construction 1–3 seconds and validation/interruption/recovery 25–55 seconds,
uncertain by roughly a factor of two. A 96-FD imposed limit is retained. Disk-backed
catalogs use 256 KiB SQLite caches; semantic indexes use the retained 4N pool of
four handles and 1 MiB cache per Store. Parser lexical buffers are 64 KiB, scalar
capability 1 MiB, nesting 128, aggregate LIST-ID record metadata 4 MiB.

The benchmark supervisor kills each child at 59.5 seconds, and stops at 179.5
seconds accumulated benchmark execution. Failed attempts count toward the total.
Only one construction and one validation/recovery child are initially planned.
No benchmark is full conformance evidence. Correctness tests are separate.

Pass/replay costs: initial exact source acquisition and JSON indexing; complete
containing-record and generated-event checks; collision-safe equality indexing;
scoped token/link checking; V2 exact-message pure Ed25519; ordered ledger checks.
Each generated projection revalidates its complete event and input dependencies;
up to 20 parser-field accesses per two-attempt parent can reread the captured
records. Common containing object uses a disk JSON index; exact byte checks remain.
An interrupted generated-event/equality stage redoes validation from its first
required token. Finished acquisition/index/native-link stages reuse verified
snapshots/indexes. Pure Ed25519 resumes by reading its consumed prefix; no exported
curve state or constant-time restart claim. On a new invocation all scheduled
source bytes and receipt prerequisites are exact-checked. Terminal reuse still
hashes the exact input/artifact set. Journals do not authenticate a source or
establish qualification.
