Formal-Lab[6] recovery-field independent-review checkpoint

Verify the communicated checkpoint identity, CRC, safe exact regular membership and all MANIFEST.json hashes before extraction into a new persistent directory. The exact target is included as input/I164-recovery-field-correspondence-1.zip: 39,038,102 bytes; 617 entries; SHA-256 c92840a853097a9fe5fd1cd80134649fdd25a7463422cce81361a46bec70f8cf.

code/verify_input.py verifies the target, all manifested members and nested archive scopes. --extract creates a new root and refuses existing destinations. Check actual recovered filesystem membership before consuming it. Preserve an unexpected entry or failed attempt outside any later strict root; do not silently exclude it. The failed independent recovery and unexpected partial bytes in this checkpoint are failure evidence, not valid input members.

The complete 552-member predecessor root and its offline dependencies are retained inside the target. Original predecessor outer ZIPs remain separate; their exact bytes were verified and reused here. Partial historical review manifests retain their original scopes and do not become new manifests for the current package. code/composition.py takes the new root, output record, exact predecessor input ZIP and exact previous independent-review ZIP for the byte-continuity audit.

The new public offline check, on Python 3.12.14 with optimization disabled, is:

```bash
python3 -I -B /absolute/recovered/code/correspondence.py \
  check /absolute/recovered/results/recovery-field-correspondence.json
```

Its success supports the exact retained receipt; it does not close HF-01. Read REPORT.md and CHECKPOINT.json before interpreting the result. No source, implementation or original evidence modification is required.

code/minimal_head_witness.py constructs separate altered saved-report bytes, tests semantic/derivation acceptance and public rejection, and records the still-accepted pristine receipt. head-witness-primary/ and head-witness-recovered/ preserve the exact seven-member witness and changed byte offsets. code/witness_reverts.py checks each member's necessity for that fixed witness. These operations are saved-byte/source checks, not session operations or database connections. Never promote witness files to admitted original evidence.

Independent focused controls, the broader exploratory probe, minimized witness, recovered-root results and supplied Engineering results are separate. The pure constructed-value checks are not runtime evidence. Original archive discrepancies and the failed independent recovered root are preserved with unknown causes.

Do not run retained application/worker/launcher entries, old suites, a host smoke, pipeline, lifecycle, global expansion or Git save as a recovery step. No new limits, retention changes or policy adoption are authorized. All obligations, UNKNOWN totals and existing admission/readiness boundaries remain unchanged. HF-01 is the next bounded correction; no operational prerequisite is discharged by this review.
