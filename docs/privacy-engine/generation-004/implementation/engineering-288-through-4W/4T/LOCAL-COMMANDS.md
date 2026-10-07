# Local commands (Ubuntu; do not change working directory)

Download the 4T ZIP and its separate receipt into `/home/steve/Downloads`. The external local-commands file and chat response also supply a preflight with the exact ZIP hash embedded. The following receipt-based blocks are convenient once both files are present.

## 1. Read-only host preflight; no installation or full enumeration

```bash
python3 - <<'PY'
import hashlib,json,sys,zipfile
from pathlib import Path
sys.dont_write_bytecode=True
z=Path('/home/steve/Downloads/Engineering-288-checkpoint-4T.zip')
r=json.loads(Path('/home/steve/Downloads/Engineering-288-checkpoint-4T-receipt.json').read_bytes())
h=hashlib.sha256()
with z.open('rb') as f:
    for b in iter(lambda:f.read(1048576),b''):h.update(b)
assert h.hexdigest()==r['zip']['sha256'],'ZIP SHA-256 mismatch'
with zipfile.ZipFile(z) as a:
    code=a.read('Engineering-288-checkpoint-4T/bootstrap.py')
    assert hashlib.sha256(code).hexdigest()==r['bootstrap_sha256']
exec(compile(code,'4T-bootstrap','exec'),{'__name__':'__main__','ZIP_PATH':str(z),'MODE':'preflight'})
PY
```

## 2. Optional installation and bounded local throughput probe

Repeat block 1 with MODE changed from `preflight` to `install`. Installation does not start computation. Then run:

```bash
python3 -B /home/steve/dev/Engineering-288-execution/textual-4T/Engineering-288-checkpoint-4T/local_probe.py
```

The probe is capped at 58 seconds per segment and 116 seconds total. Prefer 64 ranks if safely within the stated margin; otherwise 16 if that passes. If neither passes, return the output without starting.

## 3. Later full execution: separate explicit textual authorization

Install using the verified block above (MODE `install`) if not already installed. This command authorizes the proposed 48-hour textual review budget and launches detached:

```bash
python3 -B /home/steve/dev/Engineering-288-execution/textual-4T/Engineering-288-checkpoint-4T/launch.py run --authorize-review-hours 48 --segment-ranks 64
```

Read status without the full terminal dump:

```bash
python3 -B /home/steve/dev/Engineering-288-execution/textual-4T/Engineering-288-checkpoint-4T/run_task.py status
```

You may close the terminal. Logs are under the textual-4T task directory in terminal.log; each slice also has a durable individual log.

## Pause and resume

```bash
python3 -B /home/steve/dev/Engineering-288-execution/textual-4T/Engineering-288-checkpoint-4T/run_task.py pause
```

After it stops, resume the same namespace; use 16 instead of 64 to shrink future generation intervals if necessary:

```bash
python3 -B /home/steve/dev/Engineering-288-execution/textual-4T/Engineering-288-checkpoint-4T/launch.py resume --segment-ranks 64
```

Only after reviewing a budget stop, explicitly grant more time if desired. This records authorization without starting work:

```bash
python3 -B /home/steve/dev/Engineering-288-execution/textual-4T/Engineering-288-checkpoint-4T/run_task.py extend --hours 24
```

Then resume the same job. Do not create a new job to reset the budget.

## Completion and durable snapshot

```bash
python3 -B /home/steve/dev/Engineering-288-execution/textual-4T/Engineering-288-checkpoint-4T/run_task.py verify-completion
python3 -B /home/steve/dev/Engineering-288-execution/textual-4T/Engineering-288-checkpoint-4T/snapshot.py save --task /home/steve/dev/Engineering-288-execution/textual-4T
```

Return the completion snapshot ZIP and its printed SHA, not a massive terminal dump. Same-generator replay does not establish independent supplied-row validation.

For a paused verified backup, restore to a fresh destination using its printed exact SHA:

```bash
python3 -B /home/steve/dev/Engineering-288-execution/textual-4T/Engineering-288-checkpoint-4T/snapshot.py restore --task /home/steve/dev/Engineering-288-execution/textual-4T-restored --snapshot /absolute/path/to/checkpoint.zip --sha256 EXACT_PRINTED_SHA256
```

Then resume using `launch.py resume --task /home/steve/dev/Engineering-288-execution/textual-4T-restored`. Never run both copies. Historical models, binary recovery state and .env are not accessed by these commands.
