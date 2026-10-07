# Costed local envelope

The job consumes 729,259,627,770 binary bytes per complete pass **inside the worker's hash buffers**. It writes none of those rows to disk. Generation plus independent predicate replay therefore hashes approximately 1.459 TB of deterministic bytes without table I/O.

Retained 4A measurements: 497–550 MB/s generation with child peak RSS 12,544 KiB on the recorded AMD EPYC host. Linear generation cost is roughly 22–25 minutes; provision 30–60 minutes for each binary pass, including replay and checkpoint overhead. The Ubuntu computer's actual throughput is unknown. The two-hour aggregate review stop is enforced; a slower machine stops recoverably rather than extending itself. No new throughput benchmark was run in 4R. Native probes and the four-token recovery oracle are package checks, not performance evidence.

Initial memory reservation: **8 GiB available**, including cgroup headroom if applicable. Preflight rejects less. The worker itself has an 8 MiB serialization buffer and small fixed-token/index arrays; the observed retained worker RSS is far below the reservation. The supervisor, Python slice controller and native worker run sequentially as one process family, with at most three live processes and **2 GiB address-space limit each** (at most 6 GiB combined address space). No parallel workers or large model load is introduced. This is a conservative cap, not a new full-model memory measurement.

## Storage calculation

Exact payload sizes and source/code hashes appear in PACKAGE-MANIFEST.json. Its storage block is generated from the actual delivered files. The minimal kit extracts only about 0.6 MB of file contents; filesystem allocation and directory headroom are separately counted. It does not extract 4Q/4P's archive chain, the 382.7 MB model, any 236.9 MB TSV descriptor, the Ed25519 build tree or source fixtures. System Python/native shared libraries are existing runtime dependencies, not copied dependencies.

Conservative checkpoint allocation, on filesystem allocation units at most 4 KiB:

| Item | Bound |
|---|---:|
| 1,359 generation records, 4 KiB each | 5,566,464 bytes |
| 1,359 replay records, 4 KiB each | 5,566,464 bytes |
| Up to 4,096 accounting records, 4 KiB each | 16,777,216 bytes |
| Up to 4,096 bounded slice logs, 16 KiB each | 67,108,864 bytes |
| Fixed control/partial records | 131,072 bytes |
| Live checkpoint allocation total | **95,150,080 bytes** |
| Peak checkpoint copy factor | **4**: live + two backups + one in-progress backup |
| Extra disk safety headroom | **67,108,864 bytes** |

The manifest adds exact allocated package dependencies, a bounded manifest, directory overhead and **two archive-size upper bounds**, then rounds up to the next 64 MiB. The resulting host requirement is **448 MiB free (469,762,048 bytes)** on the task filesystem, plus the computed free-inode requirement (about 44,000). This remains conservative even with two uncompressed-sized backups; actual compressed snapshots will usually be much smaller. The downloaded ZIP already occupies space before the free-space check; the calculation still reserves copies. User-created additional snapshots/log captures outside the two-slot policy need additional space.

Preflight rejects larger allocation units instead of silently relying on this 4 KiB calculation; request a revised storage estimate if that occurs. It checks the nearest existing ancestor when the target does not yet exist, never creates the target during preflight, and rejects read-only/noexec mounts and path symlinks. No runtime or storage sufficiency is inferred from the cloud host.

The native dependencies are dynamically loaded, hashed and bound to the job. They must remain quiescent while running. Rebuilding or changing libraries mid-job is not automatic recovery; preserve the job and review the new execution identity. Segments expose progress every committed slice and native progress during longer slices. Every retained native process stays below 60 seconds; no full enumeration is started by the preflight.

## Recovery cost

A clean run has 2,718 native slices. Reopening reads small receipt chains and exact descriptor/code/library bytes; there is no consumed 729 GB input file to rehash. A failed slice may regenerate at most about 536.9 MB of candidate output (less for exclusions) and repeats no committed prefix under the trusted-journal boundary. The cumulative state chain remains header-anchored and independently replayed. This advantage is specific to deterministic hash-only generation; it does not remove the supplied-link or pure Ed25519 prefix-reread costs of later checkpoints.
