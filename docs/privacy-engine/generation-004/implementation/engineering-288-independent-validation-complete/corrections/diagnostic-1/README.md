# Engineering[288] 4W diagnostic correction 1

Purpose: expose worker exit status, signals, bounded stderr and watchdog decisions after an unexplained local exit. This package does NOT establish the cause of the October 7 exit and does not fix a demonstrated semantic-validator defect. The terminal remained open according to the operator. The scope CPU-accounting message alone is not causal evidence.

The original archive is preserved, SHA-256 63d85a1a75640853a06f8764480e474cb21826e2916521a331451e29bb90df2c. All ten runtime files (including emitter, independent validator and adapter) are byte-identical. Only supervisor.py, superlib.py and launch.py of the supervisor binding change; migrate.py is newly bound. Source, model, contract, serialization, input descriptors, equality law, parser state, whole-stream SHA state and the accepted amendment are unchanged.

Install in the separate Engineering-288-checkpoint-4W-diagnostic-1 directory. Use only the external instructions and install_and_migrate.py for this correction. Historical COMMANDS.md/install.py/host.py and earlier test/result documents are retained historical inputs, not the correction's installation instructions.

## Explicit migration

migrate.py --task TASK --old-kit ORIGINAL_KIT acquires the existing writer lock, verifies every manifested original-kit file, verifies current runtime/input identities and MAC-protected state, then publishes a MAC-protected transition plan retaining old/new CONFIG and BUDGET payloads. It changes only the supervisor implementation/config binding and increments the budget record sequence once. It preserves charged time, authorized time, grants, attempts, failure status and every data/IDENTITY.json, data/STATE.json and spool.bin byte.

No key is printed, copied into the deliverable, or migrated to a new job. The same original task and private local key are used. The transition plan contains no key. This is an explicit trusted local implementation transition, not qualification or source authentication.

An interruption after plan/config/budget publication is resumed by rerunning the same migration command. Unexpected bytes, changed code, changed input, cross-job plans or invalid MACs fail closed. No manual journal edits or resets. An incomplete install directory causes a stop for inspection, not automatic overwrite. Launch is refused until the transition completion record exists. Do not use the original CLI after migration.

Original backup files remain historically bound to the original CONFIG and are not relabelled. A new backup made with the corrected CLI is current; it rotates the previous backup to backup-1.zip. Restoring an original backup with the new collector fails correspondence checks. Any rollback would require a separate reviewed transition; do not copy old CONFIG/BUDGET over new state.

## Diagnostics and boundaries

EXIT-DIAGNOSTICS records pre-cleanup and post-cleanup exit codes/signals, supervisor termination request, the last 1024 stderr bytes and total stderr bytes observed. A drain thread prevents stderr backpressure, using bounded buffers. The watchdog reports expired prepaid lease, absent lease, boot mismatch or budget read/integrity error before requesting termination. Diagnostics use the existing bounded rotating progress.log. If the supervisor itself is killed before recording, diagnostics may still be incomplete. An OS cgroup kill can affect all processes; detachment does not promise survival of logout/session teardown.

Aggregate execution accounting remains unchanged. The 15-second prepaid lease and existing enforcement remain in place; we do not silently lengthen leases, grant time, or suppress watchdog checks. Worker rejection and completion remain independent of diagnostic messages. Diagnostic presence proves neither successful validation nor qualifications.

## Recovery commands after installation

python3 -B NEW_KIT/migrate.py --task TASK --old-kit ORIGINAL_KIT
python3 -B NEW_KIT/launch.py backup --task TASK
python3 -B NEW_KIT/launch.py resume --task TASK
python3 -B NEW_KIT/launch.py status --task TASK
python3 -B NEW_KIT/launch.py pause --task TASK
python3 -B NEW_KIT/launch.py verify --task TASK

Resume uses existing unspent authorization; migration never starts workers. Return the migration and backup outputs before resuming. No full retained stream, benchmark, or completed identity run is processed by the correction tests.

## Resource estimate before local migration

Installation is under 2 MiB extracted plus filesystem allocation. Migration checks exact model/contract/descriptor inputs twice (about 1.24 GB read), plus at most several 64 MiB active-spool reads. Hashing uses 1 MiB blocks; Python metadata/state are bounded. No native model index is loaded by migration. Plan storage is small (under the retained 128 KiB metadata bound); a new quiescent backup is at most about 64 MiB. Allow 256 MiB free disk for installation, transition, and temporary backup. Runtime is host/disk dependent, expected seconds to tens of seconds, not a throughput benchmark. Native index startup and up to 64 MiB regeneration happen only on later resume. Evicted multi-terabyte prefixes are not replayed.

Actual admission remains disabled. Authentication, full-model integration and authoritative qualification remain separate outstanding obligations.
