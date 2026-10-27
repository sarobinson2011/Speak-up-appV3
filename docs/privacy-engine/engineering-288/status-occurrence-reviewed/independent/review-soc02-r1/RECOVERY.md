Formal-Lab[6] SOC-02-R1 independent closure checkpoint

Verify the review ZIP's reported bytes, SHA-256, CRC, safe unique regular membership and MANIFEST.json before extraction into a new persistent directory. The manifest binds all other review members; it does not hash itself. The exact target archive is included under input/I164-SOC02-R1-correction.zip, with its complete predecessor/recovery dependencies.

Target identity: 30,156,228 bytes, 520 entries, SHA-256 eb8f0c74f1431a00cfe67e7b756a7e3416385a34bebaa0e2b3981c063898092f.

code/verify_input.py verifies this identity and all nested archive/manifests and optionally extracts a new target root using --extract. It refuses an existing extraction destination. code/composition.py compares the recovery layout and intentional change against the complete included predecessor archives. It preserves the original scope of copied nested manifests.

Read-only current-receipt validation on CPython 3.12.14, optimization disabled, from a new recovered target root:

```bash
python3 -I -B /absolute/target/corrected/code/smoke_occurrences.py \
  check /absolute/target/corrected/results/occurrence-connection.json \
  --root /absolute/target/corrected
```

This invokes the offline adapter and its existing correspondence validators, not the application or worker. No session or database connection is needed. Do not run worker.py, a host smoke, retained session commands, old test suites, completed reviews, pipelines or lifecycle during recovery. Do not install dependencies or alter source code merely to recover this evidence.

The independent-primary/ and independent-recovered/ results remain separate from supplied Engineering results inside the target. The former records 100 new review assertions and exact old-witness reproduction; the latter records 26 focused assertions in a fresh process against a separately recovered root. Their overlap is not extra semantic coverage or extra producer execution. code/independent_controls.py is retained for reproducibility; do not automatically rerun a completed review.

The previous three witness traces and receipts remain byte-exact within the embedded target's review/independent-primary/residuals/ and its complete prior review ZIP. Original source and original failures remain intact. A read-only reviewer harness assumption failure is retained under failures/ and is not a candidate defect.

Closure is limited to the saved successful close-identity correspondence contract. SOURCE-ONLY, all obligations and UNKNOWN totals, trusted-process/observer assumptions, readiness/final-binding blockers and admission-disabled status remain unchanged.
