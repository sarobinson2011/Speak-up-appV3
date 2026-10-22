# Recovery / reproduction

Read REPORT.md and findings.json first. This compact return references the original 18,817,005-byte input archive rather than duplicating it. Retain both together.

Extract this return into `fl4/` in a fresh working directory. Place the original input in `upload/`. Run:

```bash
python -B fl4/tests/audit_input.py 'upload/Engineering-288C-I164-prospective-candidate-metadata.zip' fl4-work/candidate fl4/results/input-audit.json
timeout 60s python -B fl4/tests/audit_metadata.py fl4-work/candidate fl4/results/metadata-audit.json
timeout 120s python -B fl4/tests/review_controls.py fl4-work/candidate fl4/results/independent-controls.json
python -B fl4/tests/source_limits.py fl4-work/candidate fl4/results/source-limits.json
```

Adjust only the uploaded input filename if it has a duplicate suffix. Its bytes/hash must still match. Python3 and the existing cryptography dependency are required; do not install dependencies as part of this review. Preserve prior review outputs before reproduction. The scripts write review results only; candidate code/input bytes remain unchanged. Network use is blocked by the focused control harness. It runs read-only semantic folds of saved bytes, never Authority or runtime lifecycle commands.

The prior-input-corroboration result additionally used the exact SD-01 correction and historical review archives already verified in the preceding session. Those are supplementary byte comparisons, not needed for the primary audit's supplied inventory checks. Their identities are recorded in that result. No absent large predecessor model/archive or stream is claimed freshly verified.

Do not run candidate check_candidate.py in the preserved extraction: it writes its own result files. Do not run build, lifecycle, model expansion, migration, network or stream commands. No additional construction is authorized by this package.

Verify this return ZIP with:

```bash
python -B fl4/tests/verify_return.py /absolute/path/to/Formal-Lab-4-I164-prospective-candidate-metadata-review.zip
```

The external receipt gives ZIP bytes, entries and SHA-256. MANIFEST.json covers every other member. Failures are retained separately; only results/independent-controls.json records the final37-control run.
