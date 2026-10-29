# Recovery instructions

First verify the externally reported correction ZIP filename, byte count, entry count and SHA-256. Then verify CRC, safe unique regular-file membership and every root MANIFEST.json identity. tools/checkpoint.py supplies read-only verification/extraction. Extract into a new persistent directory without overlaying any prior root, session or acquisition. Preserve any failure root; do not repair, delete undeclared entries or automatically retry.

The executable root is the extracted correction root. It includes current code/, exact original/ and decoded review/. code/correspondence.py pins original/MANIFEST.json, checks all its files, directories and entry types, then checks/invokes original/retained/state with the existing mandatory client-state and earlier predecessor chain. All current dependency bytes are present. Historical compact-manifest and missing-outer-archive qualifications remain as recorded in original/RECOVERY.md; this correction does not resolve them.

The exact original target archive is retained as its full 1,845-member decoded layout, with unchanged MANIFEST.json and all original identities. Review/ retains all 157 non-input members of the independent review, including its unchanged manifest. The manifest's single absent embedded target ZIP is explicitly redundant with original/ and its verified archive identity is in provenance/input-verification.json. Current validation does not reconstruct or consume that redundant outer ZIP. Byte-for-byte outer comparison requires the original reviewed archive; the verified supplied archive was used in this construction.

The corrected canonical receipt is results/fresh/corrected-receipt.json. The current offline public entry, if independently authorized for a new review, is:

```
python3 -I -B ROOT/code/correspondence.py --root ROOT --receipt ROOT/results/fresh/corrected-receipt.json
```

Use CPython 3.12.14, optimization disabled, and Cryptography 50.0.2, as recorded. This is saved-input source/evidence validation, not the host-qualified session profile. No application source method, request, database connection or session operation is needed. tests/offline.py guards prohibited operations. Completed controls are evidence to inspect, not instructions to rerun this campaign.

For a new independent focused reproduction, tests/witnesses.py takes ORIGINAL_ROOT and an output directory outside it. It exercises only IS-01 acceptances against the exact affected validator. tests/focused.py takes CURRENT_ROOT and a new result directory and checks the corrected boundaries. tests/fresh.py documents full public-entry checks; tests/recovered_cli.py documents the separate public check on the recovered root. They are constructed/saved-evidence controls, not runtime observations. They must never write within immutable original/review/source inputs. All output paths must be new; no automatic overwrite or retry.

results/primary/corrected-receipt.json belongs to the primary adapter before the final no-symlink-root guard. It is preserved with provenance/primary-correspondence.py and primary-focused.py, and is not the current receipt. Fresh and recovered checks use current code pins. Existing supplied controls, independent review checks, original witnesses and new controls remain in separate directories. Failures and progress logs remain exact; do not merge failed work into completed totals.

Runtime forwarding/reference observations and complete repetition/history remain unavailable. All obligations, unknowns and authority boundaries persist. SOURCE-ONLY; readiness/final binding blocked; admission disabled. No operation or new authorization follows from recovery.
