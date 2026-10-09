# Durable execution contract

## Prepayment and aggregate budget

Budget means aggregate active wall time, not summed CPU time or an LLM allowance. The launcher MAC-seals and fsyncs a reservation **before spawning the detached daemon**. It covers daemon/worker startup, exact input and runtime checks, model/index initialization, generation, spool checks, independent validation and controlled cleanup.

Reservations are 15-second quanta, renewed durably when less than three seconds remain. The active record includes attempt identity, boot identity, CLOCK_BOOTTIME start/deadline and prepaid duration. No work is authorized by an uncommitted renewal. Normal settlement charges elapsed time and refunds the unused prepaid tail. An uncertain/crashed attempt keeps its entire reservation charged; resuming never refunds or resets it. The uncertain tail is normally at most approximately 18 seconds (15-second quantum plus early renewal margin). Code/runtime/input incompatibility also fails closed and costs the initialization time actually attempted.

A grant adds to the total authorization; it never sets the consumed balance to zero. Grant identifiers are idempotent and capped at 128 entries. The initial `run --authorize-review-hours 2` is accepted only once. `resume` adds no budget. `grant --authorize-review-hours 2 --grant-id review-2` authorizes an additional allowance only when explicitly chosen. A missing/corrupt budget is not reconstructed from progress or backups.

CLI argument parsing, read-only host preflight, installation/input preparation, manual backup and explicit post-run receipt verification are separate metadata operations. The latter may rehash ~620 MB of pinned inputs and load the descriptor index, but never replays the stream. All initialization inside the actual execution attempt is prepaid.

## Independent stop enforcement and overrun

A separate watchdog observes the same MAC-protected durable deadline every 0.1 seconds. It uses a pidfd to signal the exact worker process, avoiding PID reuse. The daemon can be SIGSTOPed and the watchdog still stops the worker at the prepaid deadline. The worker and native children each have Linux parent-death SIGKILL protection; a dead supervisor cannot leave an ungoverned native stream worker. A dead watchdog causes the supervisor to stop the worker too.

On a responsive kernel, deadline detection adds at most one polling interval (~0.1 s) plus scheduling/termination latency. Graceful pause sends SIGTERM to unwind the controller and close its workers; after five seconds the supervisor requests SIGKILL. Cleanup can wait five seconds for the worker and two for the watchdog. Any observed elapsed overrun is recorded and charged even if that takes the charged amount above the grant. Unused time is never refunded when settlement is uncertain.

This is not a hard real-time guarantee: uninterruptible I/O, kernel starvation or suspension can delay termination/accounting. CLOCK_BOOTTIME includes suspend time. A frozen daemon may conservatively charge its stalled interval when it returns, even though the watchdog stopped computation earlier. Such an overcharge is not evidence that computation continued. After an actual daemon crash the prepaid tail remains charged and no offline interval is inferred. Use the provided pause command before planned suspend or maintenance.

## Process and progress lifecycle

The launcher acquires `CONTROL.LOCK` and passes the same open lock into the detached daemon; there is no unlocked launch window. Competing launches, backups and restores fail while a writer holds it. The 4V data lock independently protects parser state. Advisory locks provide coordination, not byte identity or source qualification.

The daemon has its own session and no terminal pipes. Closing the terminal does not stop it. `pause` and `stop` both publish a MAC-bound request; they preserve progress and do not delete the job. Status reads atomic records without starting a worker. Heartbeats occur every 15 seconds, including initialization, with committed offsets, row counts and budget. Three rotating log files are each at most 1 MiB. Persistent state size is independent of segment count. A stalled filesystem can delay logging; it is not concealed as progress.

Exact source-input and code/native/library checks run on reopening. Do not replace the package, runtime libraries, bound inputs or execution key during a job. A live state is bound to the absolute task/data paths and exact host runtime identities; relocation or cross-host migration is not silently accepted.

## Data recovery and backups

All 4V parser, ordering, ordinal, separate count, pending-row, SHA-256 and emitter-cursor state is retained unchanged. The global whole-stream SHA is continued from trusted state, never constructed from segment digests. A missing active spool regenerates at most that spool from its starting cursor and must reproduce its exact identity. Already evicted prefixes are not reread under the retained trusted-executor and immutable-input boundary.

Initialization is published from an isolated `initializing.tmp` directory only after its zero-offset identity/state are durable and bound to the final data path. No validator runs in the unpublished directory. An interrupted unpublished initialization can be rebuilt without losing committed work; it has never had any committed stream progress. Existing published data is never reinitialized.

Back up only after status reports `running=false`. `backup` rechecks the quiescent input/state binding and creates a MAC-manifested archive containing IDENTITY, STATE and an optional active spool. It retains two rotating ZIPs; a temporary ZIP may briefly coexist. The key and live BUDGET are **not** part of the restore payload. Keep a separately protected key backup.

An explicit restore checks every archived byte, source/code/job identity and budget chronology. It preserves current data as `previous-data`, restores only validation state, and leaves the live budget unchanged. Restoring older progress deliberately adds replay from that checkpoint's cursor; it never restores spending capacity. `RESTORE.json` makes the two-directory rename transaction recoverable after interruption. Corrupted current data can be restored explicitly from a verified backup while preserving the corrupted bytes for inspection. There is no automatic fallback.

If a crash leaves an active reservation, `settle` keeps it fully charged and marks it quiescent before a backup or grant. Restore to the original path with the same key and exact inputs. Do not restore an entire old task directory over the current BUDGET. This mechanism does not resist a malicious key-holding operator who deliberately rolls back every local record; trusted custody is an explicit condition, not source authentication.

## Completion and unresolved authority

`verify` rechecks job/code/runtime/input identity, exact expected byte count and whole SHA, EOF, and separate structural/potential counts against a freshly loaded retained descriptor index. It does not rerun any stream. A daemon launch, generated digest, partial result, matching descriptor or budget receipt is never sufficient for success.

The underlying unchanged validator independently checks each actual row's framing, membership, original orientation, strict lexical uniqueness and global ordinal. Legal membership + uniqueness + exact cardinality establishes equality separately for the disjoint structural and potential sets. It does not use a generator receipt as a semantic verdict.

Accepted sources and FIELD-CLASS-REF remain unchanged. File-backed V2 object/signature acquisition, canonical pure Ed25519 authentication, scope closure, qualified ledger/assessor evidence and final-profile integration remain separate. Pure Ed25519 prefix reconstruction costs are not removed by exporting this SHA-256 state. Generated laboratory bytes and trusted local receipts establish no external appointment, source authenticity, competence, qualification or actual admission.
