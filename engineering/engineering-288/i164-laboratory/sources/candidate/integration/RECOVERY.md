# Recovery and reproducibility

This is a delta checkpoint, not a replacement of the reviewed metadata baseline. Required predecessor:
Engineering-288C-I164-prospective-candidate-metadata.zip
18817005 bytes, 439 entries
SHA-256 31f3c7827ccad8e4d1a846bfee0a7e3dae25c560749bd0927e85ea81ce7839b3

The predecessor contains all candidate/native/runtime/source/saved fixtures and preservation pins. Keep its bytes unchanged. The irrelevant staging fragment stays only in that immutable predecessor, not this new package. Do not substitute a newly rebuilt candidate or claim canonical HEAD recovery.

1. Extract this checkpoint into a new directory (delta).
2. Run `python3 delta/recover.py --predecessor /absolute/path/Engineering-288C-I164-prospective-candidate-metadata.zip --destination /absolute/path/new-recovered-root`.
   This verifies delta manifest, exact predecessor archive and all predecessor member hashes/CRC, extracts into a nonexistent destination and adds only the new integration/ and review/ files. No historical/candidate file is overwritten.
3. From the recovered root, use Python 3 with the same dependencies as the predecessor. `PYTHONDONTWRITEBYTECODE=1 python3 integration/candidate_pipeline.py binding --output /tmp/new-binding.json` validates actual candidate/source bytes and emits its downstream binding.
4. Ingest: `PYTHONDONTWRITEBYTECODE=1 python3 integration/candidate_pipeline.py ingest --export support/fixtures/ord-early.json --context SYMBOLIC-U-ONE --binding /tmp/new-binding.json --output /tmp/new-occurrences.json`. Use SYMBOLIC-U-TWO for the other retained context. Output paths must not exist.
5. Reopen: `PYTHONDONTWRITEBYTECODE=1 python3 integration/candidate_pipeline.py validate --export support/fixtures/ord-early.json --input /tmp/new-occurrences.json`. Returns valid true and final_binding BLOCKED.
6. `PYTHONDONTWRITEBYTECODE=1 python3 integration/checks.py` and `... integration/check_output_mutations.py` reproduce focused adapter checks only. Preserve supplied result files before optional reruns. No completed independent review or runtime lifecycle needs repeating.
7. `... candidate_pipeline.py final-bind` must reject; no claim object can discharge missing qualifications or model obligations.

For existing results, results/checks.json and output-mutations.json are fresh adapter receipts; review/ results are prior independent results inspected and preserved. Failures are separate and not counted as completed checks. Binding output identity includes adapter code bytes; edits require a new checkpoint and will change binding/output identities.
