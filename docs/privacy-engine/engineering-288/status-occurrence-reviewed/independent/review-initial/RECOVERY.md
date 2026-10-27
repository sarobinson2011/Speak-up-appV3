# Recovery of this review — correct target

The review target is `input/I164-status-smoke-occurrence-connection-1.zip`: 8,512,513 bytes, 485 entries, SHA-256 `20be027e282cf14a2dd1c790b60b788abab585a554152096e80ab29b5e1034f3`. The separate 4,494,310-byte boundary review in `predecessor/` is reused support, not the target or current verdict.

Verify the communicated outer review ZIP identity and exact MANIFEST.json membership/hashes before extracting into a new persistent directory. `code/verify_checkpoint.py` performs read-only archive checks. The target ZIP includes the exact original correction and saved host evidence; no additional download, host path, application execution or database connection is needed.

Read REPORT.md and CHECKPOINT.json. Closure is **not supported** because SOC-01 lets an ordinary returned context list alter the public validator's expectations. SOC-02 records additional internal semantic gaps; those mutations do not pass public acquisition pins. The baseline original receipt and concrete available observations remain supported to the stated sparse evidence limits.

Independent harnesses are included for audit, not automatic rerun. They load the new offline consumer only. Guards prohibit session/application/worker execution and database/network access. The supplied boundary and smoke code must never be executed as part of recovery. No historical review, pipeline or lifecycle command is included.

If a later reviewer is authorized to reproduce this bounded review, recover the exact target root into a fresh directory and use CPython 3.12.14 with optimization disabled:

```bash
python3 -I -B code/independent_checks.py --root /absolute/new/target-root --output /absolute/new/review-evidence
```

`independent-primary/` and `independent-recovered/` preserve full recorded check results, independently corroborated occurrence tables and all witness variants. SOC-01 folders include accepted malformed receipts. SOC-02 folders include the altered trace and derived receipt plus the recorded public rejection. The original evidence is never overwritten. The earliest minimal zero-context witness is also in `witnesses/context-alias/`.

`process-results/` preserves stdout/stderr and results for two legitimate fresh public validations and eight negative recovered-input cases. Its redundant `mutation-root` is omitted from this review ZIP; exact starting bytes and all create/modify/restore operations are recoverable from the embedded target plus `code/process_checks.py`. No live special filesystem entry is packaged. Original and recovered application source files remained byte-identical.

The independent integrity verifier takes the target ZIP, its extracted root, the included predecessor review ZIP and a new output path. It verifies all manifests and exact predecessor equality without executing a review or host test:

```bash
python3 -I -B code/verify_input.py input/I164-status-smoke-occurrence-connection-1.zip /absolute/new/target-root predecessor/Formal-Lab6-I164-status-boundary-independent-review.zip /absolute/new/integrity.json
```

The initial reviewer flat-manifest schema error and the construction's retained development artifacts remain preserved. The construction's first failed packaging ZIP is documented but was not supplied; it is not silently counted as verified.

All eleven obligations and UNKNOWN totals remain. No policy, implementation, numerical limit, retention or admission change is authorized by this review or its recovery.
