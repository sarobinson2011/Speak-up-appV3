# Host and full-run preflight

## Compatibility and inputs

The read-only command can run directly from the downloaded ZIP. It verifies package members, executes the two retained ELF self-tests from anonymous memory file descriptors (no extracted disk files), checks shared libraries and Linux pidfd/CLOCK_BOOTTIME support, and checks current RAM/disk. It discovers only named model/contract/descriptor files and 4S/4T archives beneath Downloads and Engineering-288-execution; it does not inspect Speak-up-appV3 or `.env`. Discovery is bounded at 10,000 directories. Exact input members can be verified by streaming from the pinned archives without extracting them.

The separate preparation command copies/extracts only the exact candidate model (382,700,006 bytes), selected contract (312,547 bytes) and descriptor (236,894,099 bytes) into `independent-4W-inputs`. Total: **619,906,652 bytes**. It preserves originals and accepts existing prepared files only if their exact identities match. There is no full archive-chain extraction.

Linux x86_64, Python >=3.11, libcrypto.so.3, libstdc++, libc and the usual GCC runtime libraries are required. The shipped native programs are exact 4V binaries, previously built with gcc 13.3.0/OpenSSL 3. Sources and the original build script are retained. No network dependency installation is performed. If native compatibility fails, return the error; a reviewed rebuild gets a new implementation identity and cannot silently resume an older job.

Cloud compatibility/input checks passed here. That is **not** a statement about Steve's current Ubuntu capacity; the supplied read-only command must establish it locally.

## Bounded measurement and limits

One cloud probe attempt took **18.713 seconds**, including process startup, model/index checks, two 64 MiB spools and regeneration of one deleted active spool. Exactly **134,217,728 new bytes** were independently parsed; **67,108,864 bytes** were regenerated. This is a performance/recovery sample, not full conformance evidence. The first 64 MiB consumed digest also matched the retained 4V prefix observation. No late-position cursor or completed progress was fabricated.

Measured normal 64 MiB segment:

| Stage | Wall time | Approximate rate |
|---|---:|---:|
| Emission, spool fsync and exact-byte check | 0.265 s | 254 MB/s |
| Independent validation, including whole-spool hash | 0.409 s | 164 MB/s |
| Complete steady spool step | 0.678 s | 99 MB/s combined |
| Native index startup (both workers) | 5.610 s | startup only |
| Recovery with input checks, index reload and exact spool regeneration | 6.825 s | not a throughput rate |

The deliberately tiny seven-byte read-buffer interruption check is separately recorded and is not used to estimate normal throughput. Normal reads use 65,536-byte chunks. Parent/probe-worker peak RSS was 16,556 KiB; emitter 472,832 KiB; validator 489,856 KiB. Additional supervisor/watchdog Python processes are small control processes; reserve headroom rather than treating those RSS figures as the whole system's physical usage.

The timed native/adapter/probe-worker paths are byte-identical in the final package. After measurement, focused fail-closed checks were added for missing probe ledgers, stale completion-code bindings, durable parent-directory publication and the fixed portable spool ceiling. Their exact pre-measurement wrapper sources are retained under `results/measured-wrapper-sources`, joined by `MEASURED-IMPLEMENTATION.json`; final guards were tested separately. No second throughput run was needed.

For local probing, each attempt is durably prepaid as **60 seconds**, with a **55-second OS alarm/controller timeout** and bounded termination. At most three attempts fit the fixed **180-second aggregate allowance**. Successful short attempts still consume one 60-second allowance; crashes do not refund it. An existing namespace with a missing, corrupt or incompatible ledger is blocked. Do not delete it or create a new namespace to evade the ceiling. Return a timeout/error for review; no automatic retry occurs.

## Space, memory and I/O

The portable supervisor fixes the spool ceiling at **64 MiB** (a stricter transport limit than 4V's general 256 MiB capability; no record or universe reduction). The 4V live data bound is 67,637,248 logical file bytes. Three rotating logs total at most 3 MiB. Control records are each <=128 KiB; grant history is bounded. There is no per-segment file accumulation.

Conservative peak planning includes six 64 MiB live/backup/temporary/restore/quarantine spool copies, up to three interrupted-probe spool directories, the 619.9 MB prepared inputs, package/install files and control metadata. The **2 GiB free-disk preflight reserve** covers these at the fixed 64 MiB ceiling with margin. Filesystem allocation and unrelated future disk use still matter. One `previous-data` and one incomplete install/restore/backup temporary location are permitted; repeated operations do not accumulate unlimited copies.

Preflight requires **4 GiB currently available RAM**, considering cgroup limits, under the retained **8 GiB planning ceiling**. Native workers retain 1.5 GiB address-space and 64-handle limits each; the 4V Python data worker retains its 512 MiB soft address-space limit. The complete model indexes stay loaded across segments. Actual observed native RSS totals about 940 MiB.

Peak disk stays bounded, but cumulative writes do not disappear. A complete future run would write **19,909,380,154,846 bytes (~19.91 TB)** through spools and perform at least three application-level spool reads (~59.73 TB) for checking and parsing. Some reads may hit cache. Normal spool fsync is measured, not omitted. There would be about **296,673 spools**, roughly three parser/source-state publications per spool, plus constant-size budget/heartbeat writes. The full TSV is never retained.

## Time, recovery and review stop

Linear extrapolation of this cloud normal-spool sample is roughly **56 hours** for emission plus independent validation. Retained 4V samples ranged up to roughly 98 hours. **55–200+ hours remains a provisional planning range**, with no defensible hard upper bound from first-prefix samples. CPU scaling, late lexical scans, actual storage/fsync and contention can change it. Use the new Ubuntu generation and independent-validator measurements separately; binary or hash-only textual rates are not validator rates.

A restart rehashes the exact small inputs and reloads indexes. Typically that reads ~620 MB of model/contract/descriptor binding bytes plus ~474 MB for the two descriptor indexes. First initialization checks inputs twice. At most the current spool is regenerated from its exact cursor; committed evicted prefixes are not reread under the trusted-state boundary. Restoring an older explicit backup adds work since that snapshot and never restores budget. A crash's unused prepaid tail may remain charged.

Propose a **new two-hour aggregate initial review stop**. The package does not authorize or start it. After local preflight and probe, use the separately labelled execution command only when that allowance is chosen. At the stop, save a quiescent backup and review rows/bytes, actual throughput, charged time and available resources. Continue with an explicit additional grant or resume existing unspent time; never reset the job.

Four-file source acquisition/authentication, final full-model integration and qualification remain separate. This supervisor cannot turn generated laboratory rows into signed external evidence. Any later pure Ed25519 run retains its exact-message prefix reconstruction costs; the present SHA recovery does not replace them.
