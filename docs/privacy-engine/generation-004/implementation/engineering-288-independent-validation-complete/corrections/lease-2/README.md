# Engineering[288] 4W lease correction 2

This correction addresses demonstrated sensitivity of the supervisor's short renewable lease. It does not change validation semantics, grant more time, reset progress, or establish admission/qualification.

## Evidence and diagnosis

The returned attempt-3 diagnostic explicitly reports WATCHDOG-KILL / PREPAID-LEASE-EXPIRED, a worker SIGKILL, and more than 43 hours of unreserved aggregate allowance. Watchdog observation was 92.770801 ms beyond its read lease deadline. The last progress interval was about 22.19 seconds. This proves lease expiration caused that worker termination; it does NOT establish which scheduling, filesystem, CPU or other delay prevented timely renewal. There is no semantic rejection in the supplied diagnostic. The earlier attempt-2 exit remains unproven; it may share this cause but is not relabelled as established.

A controlled independent 587-byte/14-row fixture reproduces the old policy expiring after a 20-second SIGSTOP of the supervisor. The corrected supervisor tolerates the same pause, resumes byte progress and then honors an explicit graceful pause. This demonstrates the bounded-delay behavior; it does not reproduce or diagnose the underlying laptop stall.

## Explicit lease policy change

Original: reserve 15-second increments; begin renewal with less than 3 seconds remaining.
Corrected: reserve 120-second increments; begin renewal with less than 60 seconds remaining.

The exact aggregate authorization is unchanged. Every increment is limited to the unspent allowance and durably published before becoming authority for the independent watchdog. No expired lease is revived. Initial process/index startup remains charged. CLOCK_BOOTTIME and the separate watchdog are retained. Remaining allowance below a whole increment yields a shorter final lease. At aggregate exhaustion there is no renewal; termination and accounting remain active.

This is delay tolerance, not a promise of indefinite stall survival. A sufficiently long scheduling/IO stall will still stop the job. There is no bypass of a corrupted budget or watchdog check. No shared input, parser, generator, digest law, ordering rule, row count, model or contract changes.

Conservative crash accounting changes: a lost supervisor can leave at most approximately 180 seconds of prepaid tail charged (initial tail up to 120 seconds, renewal just below 60 seconds plus a 120-second increment), instead of about 18 seconds. This is prepaid/uncertain charge, not an extra execution grant. A clean stop refunds demonstrably unused reservation; an uncertain attempt keeps it charged. OS scheduling can delay termination; recorded accounting overrun includes time until supervisor settlement and is not a precise measurement of post-deadline worker CPU time.

New LEASE-RENEWED diagnostics record publication duration, renewal lead, deadline and budget sequence. Progress reports record publication duration and interval. Existing bounded stderr/signal/watchdog diagnostics remain. Sustained IO stalls can themselves delay logging, so logs cannot promise hard-real-time reporting under a frozen OS.

## Installation and recovery

Install separately as Engineering-288-checkpoint-4W-lease-2 using install_and_migrate.py from the hash-checked archive. This migration accepts only the exact preceding Engineering-288-checkpoint-4W-diagnostic-1 kit. The pinned predecessor archive SHA-256 is 0e3f59b6ed3dce376205eba943e7b30dca7bebf0357053210f54eb364cf5d360. ORIGINAL-PACKAGE-MANIFEST.json binds all predecessor members.

migrate.py verifies the predecessor, runtime/input identities and quiescent task under its writer lock. It preserves data/STATE.json (including SHA/parser state), data/IDENTITY.json and any spool.bin byte for byte. CONFIG changes are limited to implementation binding/package path and quantum_ns=120000000000. BUDGET changes only config_sha256 and sequence; charged/authorized time, grants, attempts and saved status remain unchanged. Both old/new configurations and budgets are preserved in the MAC-protected LEASE-2-TRANSITION/PLAN.json. A local trusted executor is still required; MAC journals do not establish source authentication or qualification.

Interrupted plan/config/budget publication is completed by rerunning the same migration command. Unexpected data, input or implementation changes fail closed. An incomplete installation directory causes a stop for inspection. Never edit journals, reset the task, or copy an old budget back. The new launcher refuses an incomplete migration. Old tools must not be used on the migrated task.

Old backups retain old configuration bindings. A new backup after migration is current. This is not a relabelling of old signatures or receipts. No signature or external appointment is fabricated. New and old historical kits remain separate. The code and earlier recorded results in other files are retained historical inputs; use this README and the external lease-2 instructions for current commands.

After successful migration and backup, use the new launch.py for resume/status/pause/backup/verify with the same independent-4W task path. Resume spends only existing authorized time. No full-stream run is launched by install or migration.

## Resources and tests

Installation is under 2 MiB plus filesystem allocation. Allow 256 MiB free for installation/transition and a temporary 64 MiB backup. Migration reads the approximately 620 MB exact model/contract/descriptor inputs twice plus bounded spool hashes, using 1 MiB hashing blocks and bounded metadata. Expected local cost is seconds to tens of seconds, disk dependent; no model index is constructed by migration. Later resume reloads indexes and may regenerate the current <=64 MiB spool. Evicted multi-terabyte prefixes are not reread.

Tests cover a 20-second supervisor stall under old/new policy, delayed publication and aggregate-budget arithmetic, no expired-lease resurrection, migration interruption/corruption/substitution/mutation, exact resumed oracle agreement, pause/repeated resume, concurrent writer exclusion, watchdog/exit diagnostics, budget exhaustion and crash charging. Full retained streams and throughput benchmarks are not run. Recorded harness failures are retained: one corruption test initially matched the predecessor format string and changed no bytes; one test expected only one of the old supervisor's two deadline status labels. Both test assertions were corrected without weakening MAC checks; confirmed results are separate.

Actual admission remains disabled. Full-stream completion, final full-model integration, authentication and authoritative qualifications remain outstanding.
