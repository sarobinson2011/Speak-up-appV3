# Recover and inspect

Verify this checkpoint ZIP's separately reported bytes/SHA-256, CRC, unique safe membership and MANIFEST.json before extracting into a NEW persistent directory. Never use /tmp or overwrite a prior result. The unchanged original acquisition/evaluation ZIPs are included under inputs with their exact original identities. They retain the original saved evidence, database copies and failures; the unavailable original retry ZIP is not recovered.

Required external recovered roots:
- Exact 666-member candidate, manifest provenance/candidate-members.json: SHA-256 feef1fd4b423c067fa073b9aacb788a6553ec6fe99cde2dbfb0154ff25119209.
- Exact 163-member draft, manifest provenance/draft-members.json: SHA-256 98328cd843a8a4522be2a0f3e3d4811800087ec65e5cab486be62d94e91b30ed.
- Their retained recovery dependencies remain governed by their original recovery instructions. The prior Git checkpoint records selected sources and external exact members; it is not a substitute standalone runtime/model root.

No candidate or draft overlay is applied: all new files are in this separate integration checkpoint. This avoids falsifying predecessor source identities or silently changing the bootstrap's exact draft binding. For a later Git integration, place the new component beside the existing checkpoint sources with its BASIS/provenance and exact evidence references. Do not overwrite the old strict roots or bootstrap configuration.

Run from the prepared interpreter, supplying actual recovered roots. This is offline saved-evidence validation only. Do not run it merely to refresh prior evidence; use it when validating this new integration or independently reviewing it. Allow roughly 10-20 minutes for a full build/validation on a comparable host; source validation is repeated deliberately and progress lines identify each context and the existing counter call. This is an estimate, not a timeout or a full-run capacity bound.

/home/steve/dev/Engineering-288-execution/I164-python31214-01qgue5t/venv/bin/python -I -B /ABS/CHECKPOINT/code/evidence_counts.py build --root /ABS/current-candidate --draft /ABS/draft-connection --output /ABS/NEW-PERSISTENT-OUTPUT

To validate existing generated output instead, use action validate with --receipt /ABS/receipt.json --consumption /ABS/consumption.json and --output /ABS/NEW-PERSISTENT-VALIDATION. To consume the receipt through the count path use action consume with --receipt and a new output path. No application database is opened by these commands.

Author controls (not independent review): code/checks.py --root /ABS/current-candidate --draft /ABS/draft-connection --built /ABS/build-output --output /ABS/new-controls. It runs focused mutations and source-validator probes, not a lifecycle. Source-mutation fixtures use separate hardlink trees and unlink before replacement; original source inodes are never modified. Fixtures are reproducible from the exact inherited roots and recorded mutations, so large duplicate trees are not nested in this package.

Preserve failed outputs and report any unavailable dependency. Do not reset a session, generate keys, run a request, or rerun acquisition. SOURCE-ONLY; readiness/final binding BLOCKED; streams UNCOMPUTED; admission DISABLED.
