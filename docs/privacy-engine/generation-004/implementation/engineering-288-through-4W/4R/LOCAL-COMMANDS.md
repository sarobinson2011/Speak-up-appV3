# Local copy-paste steps

Download both Engineering-288-checkpoint-4R.zip and Engineering-288-checkpoint-4R-receipt.json into `/home/steve/Downloads/`. The final chat response additionally pins the ZIP hash directly; these portable instructions use that accompanying externally retained receipt. A checksum is integrity evidence, not source qualification.

**Step 1 — read-only host preflight.** This does not extract/install files, create task directories, change cwd, touch the repository or read .env. The native compatibility probe evaluates six synthetic candidates in anonymous RAM only.

```sh
python3 -B - <<'PY'
from pathlib import Path
import hashlib, json, zipfile
p = Path('/home/steve/Downloads/Engineering-288-checkpoint-4R.zip')
r = json.loads(Path('/home/steve/Downloads/Engineering-288-checkpoint-4R-receipt.json').read_text())
if p.stat().st_size != r['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest() != r['sha256']:
    raise SystemExit('STOP: ZIP does not match the saved receipt')
with zipfile.ZipFile(p) as z:
    code = z.read('Engineering-288-checkpoint-4R/bootstrap.py')
exec(compile(code, '4R-bootstrap', 'exec'), {'__name__': '__main__', 'ZIP_PATH': p, 'MODE': 'preflight'})
PY
```

Only `PASS-HOST-PREFLIGHT` permits the next step. If rejected, keep the full output; no installation has occurred.

**Step 2 — later execution, after preflight PASS.** This explicitly installs into `/home/steve/dev/Engineering-288-execution` and starts/resumes generation and predicate replay. It is intentionally separate from preflight. It does not modify the current working directory or Speak-up-appV3. Expect roughly 30–60 minutes per pass based on the retained different-host measurements; the aggregate review stop is two hours.

```sh
python3 -B - <<'PY'
from pathlib import Path
import hashlib, json, zipfile
p = Path('/home/steve/Downloads/Engineering-288-checkpoint-4R.zip')
r = json.loads(Path('/home/steve/Downloads/Engineering-288-checkpoint-4R-receipt.json').read_text())
if p.stat().st_size != r['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest() != r['sha256']:
    raise SystemExit('STOP: ZIP does not match the saved receipt')
with zipfile.ZipFile(p) as z:
    code = z.read('Engineering-288-checkpoint-4R/bootstrap.py')
exec(compile(code, '4R-bootstrap', 'exec'), {'__name__': '__main__', 'ZIP_PATH': p, 'MODE': 'install-and-run'})
PY
```

A rejected preflight in this second command prevents installation too. Use the pause/resume, snapshot and completion commands in README.md and RECOVERY-AND-LIMITS.md. No full stream was executed while preparing this package.
