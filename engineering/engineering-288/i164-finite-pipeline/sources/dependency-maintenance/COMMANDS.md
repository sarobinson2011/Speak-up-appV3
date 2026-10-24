# Prepared Ubuntu commands — do not run setup as an in-place upgrade

Unpack this assessment into a new persistent directory named:
`/home/steve/Downloads/I164-dependency-maintenance-v1`
Verify the delivered ZIP against the SHA-256 reported in the conversation first.
The helper checks its own script/probe/lock identities against MANIFEST.json,
the original environment records and the pinned interpreter binary. Existing
output paths reject; interrupted work is retained, never resumed by overwrite.

## 1. Read-only original-host build inventory (about 10–60 seconds)

```bash
/home/steve/dev/Engineering-288-execution/I164-python31214-01qgue5t/venv/bin/python -I -B \
  /home/steve/Downloads/I164-dependency-maintenance-v1/I164-dependency-environment.py inventory \
  --output /home/steve/dev/Engineering-288-execution/I164-dependency-inventory-001
```

This imports Cryptography's library backend only, not project modules. It reads
installed package metadata/binary identities and actual bundled OpenSSL; no
application database or session is touched. It cannot authenticate the original
wheel merely from installed versions/RECORD.

## 2. Separate proposed environment setup (about 1–5 minutes, network dependent)

Prepared for selecting the proposed dependency baseline. This performs package
downloads, then installation **only into a new environment**. It changes no gate.
No transaction/network application execution is involved.

```bash
/home/steve/dev/Engineering-288-execution/I164-python31214-01qgue5t/venv/bin/python -I -B \
  /home/steve/Downloads/I164-dependency-maintenance-v1/I164-dependency-environment.py setup \
  --output /home/steve/dev/Engineering-288-execution/I164-python31214-crypto5002-001
```

The lock is platform-specific. Missing/incompatible wheels, identity mismatches,
source builds or extra wheel files reject. No fallback versions. Bundled ensurepip
is used without upgrading it; installation logs retain its identity/version.

## 3. Separate dependency compatibility check (about 10–60 seconds)

```bash
/home/steve/dev/Engineering-288-execution/I164-python31214-01qgue5t/venv/bin/python -I -B \
  /home/steve/Downloads/I164-dependency-maintenance-v1/I164-dependency-environment.py check \
  --environment /home/steve/dev/Engineering-288-execution/I164-python31214-crypto5002-001 \
  --output /home/steve/dev/Engineering-288-execution/I164-crypto5002-compatibility-001
```

Checks authenticated wheel payload correspondence, pip dependency requirements,
exact interpreter/package/backend versions and public cryptographic APIs. It
creates no keys and signs nothing. It does not run I164 saved-export validation,
the bootstrap, native builders, a session or a review suite. A PASS is explicitly
**dependency-only**, not whole-application compatibility or deployment readiness.

Every operation writes RESULT.json and logs into its new output directory and
copies a result to Downloads. Progress appears before each subprocess and every
30 seconds for a running step. No automatic retry. Failure is preserved in
failure.txt. Do not delete it or reuse its destination; report it first.

The proposed environment is not authorized to open I164-lab-session-001. Keep
that session and its 41.0.7 environment unchanged. Any future new-runtime launcher
needs the explicit source/profile changes listed in ASSESSMENT.md.
