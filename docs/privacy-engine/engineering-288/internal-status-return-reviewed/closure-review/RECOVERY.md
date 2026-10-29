# Recovery and evidence separation

This independent checkpoint contains the exact reviewed correction ZIP at `input/I164-IS01-correction.zip`, reviewer code, audit results, fresh control results and preserved reviewer failures. The correction ZIP in turn contains the unchanged affected implementation, original witnesses, prior independent review records and executable recovery dependencies.

Verify the externally reported review ZIP byte count, entry count and SHA-256, then CRC, safe exact membership and every top-level MANIFEST.json identity. `code/verify_checkpoint.py` checks the review ZIP and its embedded target without executing candidate or test code.

For a newly authorized extraction, `code/integrity.py INPUT_ZIP NEW_EMPTY_ROOT` verifies the exact correction archive identity, CRC, all 2,052 member hashes and safe regular membership, then writes a new root and verifies its exact files/directories. Use persistent evidence directories outside any session. Do not overlay, repair or remove unexplained files from an existing root.

All required current validation dependencies are present. The affected target is decoded under `original/`. The prior review is decoded under `review/`, except its redundant embedded target ZIP. Historical outer-ZIP and forensic compact-manifest qualifications remain recorded in the original recovery documents. The intermediate Engineering recovery outer archive is a continuity record, not independently recovered bytes; its exact retained manifest selection was checked against the final target.

Completed review and Engineering campaigns are evidence to inspect, not instructions to rerun. Reviewer scripts implement only this bounded review, using saved inputs and operation guards. Their records distinguish original acceptance reproduction, corrected focused validation, full semantic/derivation, public byte-entry validation and constructed cases. `recover_script.py` extracts and verifies a new exact root before starting an explicitly selected new review script; it is not needed for normal artifact inspection.

The active current receipt is `results/fresh/corrected-receipt.json` within the correction root. Engineering's `results/primary/corrected-receipt.json` belongs to its pre-final adapter and is deliberately retained as a different identity. It must not replace the current receipt.

`failures/reviewer-obligation-pin-shape` preserves the incorrect reviewer assertion, original 153-check failed attempt and logs. That attempt is excluded from completed totals. Old membership refusals, forensic partial bytes and failed Engineering attempts remain in the embedded correction unchanged. The actual symlink used by the adjacent root-type test remains outside immutable input roots; its target and refusal are recorded as evidence, and the symlink itself is not an archive member.

Environment: CPython 3.12.14 with `-I -B`, optimization disabled, Cryptography 50.0.2. No application/runtime method, request, database connection, session initialization or reopening is required or authorized. No persistent session exists as a result of this review. Runtime forwarding/reference observations remain unavailable; observer unjoined; all obligations/UNKNOWN totals and admission-disabled boundaries remain.
