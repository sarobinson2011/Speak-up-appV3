# Recovery, review stop and exact trust boundary

The supervisor persists a reservation **before** each native slice. A normal slice is charged its elapsed generation/replay and checkpoint-checking time; an interrupted reservation is conservatively charged the full 60 seconds. Each step process has a 50-second outer timeout; its native worker has at most 45 seconds. A killed process group leaves at most one uncommitted segment to repeat. Minor startup/final receipt I/O is outside the measured enumeration interval. The cumulative charged computation budget is 7,200 seconds; if fewer than 60 seconds remain, the supervisor stops for review before another slice. Idle time while paused is not charged. A restart cannot reset this ledger. Deleting it while retaining segments rejects.

The 4,096-attempt ceiling is a storage/retry guard, not a reduction of the pair universe. A clean run needs 2,718 successful slices. Timeout, memory/resource failure, code/library mismatch, corruption, lack of budget or too many retries stops without claiming completion. Review the saved log; do not edit charges, drop receipts, lower cardinalities, reset time or change segment size to force progress. A slower host may need a separately reviewed budget/kit; no automatic extension is included.

Generation and replay both resume from durable SHA state and interval chains. They regenerate deterministic bytes, so **they do not reread a stored consumed file prefix**. A completed verified prefix can be reused under the trusted local journal boundary. A crashed uncommitted slice repeats at most its 67,108,864 candidate ranks. Replay walks the independent predicate for every saved interval and compares segment digest and cumulative state transition. No supplied-link validation or Ed25519 prefix reconstruction is being performed here; those costs remain in 4Q for later work.

Pause from another terminal:

```sh
python3 -B /home/steve/dev/Engineering-288-execution/Engineering-288-checkpoint-4R/run_task.py pause --task /home/steve/dev/Engineering-288-execution
```

The current segment may finish; the next does not start. Ctrl-C or SIGTERM to the supervisor requests the same boundary stop. A terminal hangup or power loss may discard an uncommitted segment; the reserved minute is retained. Inspect status, then resume with:

```sh
python3 -B /home/steve/dev/Engineering-288-execution/Engineering-288-checkpoint-4R/run_task.py resume --task /home/steve/dev/Engineering-288-execution
```

Exit codes: 0 completed conditional mechanical identity; 3 paused; 4 review stop; 2 rejected/failed. No code path admits a profile. Stage logs live under supervisor/log-NNNNN.json; progress and final receipts live at PROGRESS.json and COMPLETION.json. Supervisor receipts carry checksums, code/contract/model/plan identities and runtime library hashes; native records bind exact worker/controller/descriptor bytes. A whole-journal adversary who can rewrite every record is not defeated by plain checksums. Externally preserve the receipt/backup digest; journals establish no source authentication or qualification.

## Snapshots

After the supervisor has paused or completed, create a snapshot. This refuses an active locked task and keeps two rotating slots. The reported exact ZIP SHA-256 should be retained separately, ideally with a copy on another durable device.

```sh
python3 -B /home/steve/dev/Engineering-288-execution/Engineering-288-checkpoint-4R/snapshot.py save --task /home/steve/dev/Engineering-288-execution
```

Snapshot creation is not automatic. Explicitly invoke it after a bounded batch or completion. Between backups, same-disk durable journals still preserve each committed segment; total-disk loss requires replaying progress after the last independently preserved snapshot.

To recover to a **fresh** directory, replace SNAPSHOT and SHA256 with the exact saved path and externally retained digest:

```sh
python3 -B /home/steve/dev/Engineering-288-execution/Engineering-288-checkpoint-4R/snapshot.py restore --task /home/steve/dev/Engineering-288-execution-recovered --snapshot SNAPSHOT --sha256 SHA256
python3 -B /home/steve/dev/Engineering-288-execution/Engineering-288-checkpoint-4R/run_task.py resume --task /home/steve/dev/Engineering-288-execution-recovered
```

Restore validates archive membership and exact bytes, code identity and journal continuity, and creates a PAUSE marker. Resume explicitly removes it and checks host runtime/resource bindings. Task path relocation is permitted for this descriptor-only mechanical job because no path-dependent acquired input is referenced; exact inputs/code/runtime remain pinned. This permission does not extend to the later file-backed collector's path-bound jobs.
