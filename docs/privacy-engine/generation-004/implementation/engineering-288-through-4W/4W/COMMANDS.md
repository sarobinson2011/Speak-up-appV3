# Local command sequence

Use the delivered `Engineering-288-checkpoint-4W-instructions.txt` for the complete copy-paste preflight/install/probe blocks, including the exact ZIP SHA-256. They use absolute paths, leave the working directory unchanged, and do not inspect `.env` or Speak-up-appV3.

1. **Read-only preflight:** run directly from the downloaded, hash-checked ZIP. Paste its JSON result. No files are extracted and no full validation starts.
2. **Bounded probe:** the separate block installs the checked kit under Engineering-288-execution, prepares only the three pinned input files, and runs a capped local probe in `independent-4W-probe`. All attempts share its durable 180-second ceiling. Paste the result; it is not full-stream evidence.
3. **Later execution only:** after choosing a new initial two-hour budget, use the commands below. No previous binary/textual authorization is reused.

Set these shell variables in each new terminal where you want to use the abbreviated commands (they do not change your directory):

```bash
KIT4W=/home/steve/dev/Engineering-288-execution/Engineering-288-checkpoint-4W
TASK4W=/home/steve/dev/Engineering-288-execution/independent-4W
```

Initialize once (metadata only; published data initialization is charged later):

```bash
python3 -B "$KIT4W/launch.py" init --task "$TASK4W" --manifest /home/steve/dev/Engineering-288-execution/independent-4W-inputs/source.json --spool-mib 64
```

**Later authorization and detached execution — do not run during preflight:**

```bash
python3 -B "$KIT4W/launch.py" run --task "$TASK4W" --authorize-review-hours 2
```

Status (read-only state inspection):

```bash
python3 -B "$KIT4W/launch.py" status --task "$TASK4W"
```

Graceful pause/stop (both preserve progress and budget):

```bash
python3 -B "$KIT4W/launch.py" pause --task "$TASK4W"
python3 -B "$KIT4W/launch.py" status --task "$TASK4W"
```

Wait for `running=false` before backup or restore. `stop` is an equivalent spelling of `pause`. Closing the terminal does not stop the detached job. To resume a paused or crashed attempt using **only remaining authorized time**:

```bash
python3 -B "$KIT4W/launch.py" resume --task "$TASK4W"
```

If a crash left an unsettled reservation, `settle` preserves its full charge and allows quiescent backup/review; it does not process stream bytes:

```bash
python3 -B "$KIT4W/launch.py" settle --task "$TASK4W"
python3 -B "$KIT4W/launch.py" backup --task "$TASK4W"
```

Ordinary paused backup:

```bash
python3 -B "$KIT4W/launch.py" backup --task "$TASK4W"
```

Explicit restoration to the original task path (live budget stays current; original data is preserved as `previous-data`):

```bash
python3 -B "$KIT4W/launch.py" restore --task "$TASK4W" --archive "$TASK4W/backup-0.zip"
python3 -B "$KIT4W/launch.py" resume --task "$TASK4W"
```

Do not delete or overwrite BUDGET, CONFIG or the execution key. A corrupt record is a stop, not permission to reset from zero. If a restore was interrupted, `settle` or the next supervised worker finishes its explicit restore transaction. Before another restore, preserve/archive the prior `previous-data` deliberately; the tool refuses to overwrite it.

**Only after a later review chooses another two hours**, add it once with an idempotent grant ID:

```bash
python3 -B "$KIT4W/launch.py" grant --task "$TASK4W" --authorize-review-hours 2 --grant-id review-2
python3 -B "$KIT4W/launch.py" resume --task "$TASK4W"
```

Exact completion verification (metadata/input/index checks only; no stream replay):

```bash
python3 -B "$KIT4W/launch.py" verify --task "$TASK4W"
python3 -B "$KIT4W/launch.py" backup --task "$TASK4W"
```

Return the final verification JSON and backup hash/archive when complete. Completion remains conditional independent row validation of generated static laboratory bytes. Actual admission remains disabled.
