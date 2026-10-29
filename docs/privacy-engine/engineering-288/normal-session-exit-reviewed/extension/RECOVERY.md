# Offline recovery

Use a new persistent directory. Preserve the original checkpoint and every failure. Do not overwrite earlier milestones. This is an independent review procedure, not a request to repeat any completed engineering campaign or host smoke.

1. Match the externally supplied final ZIP byte count, SHA-256 and entry count. Verify CRC, unique safe relative regular-file membership and every member's identity against MANIFEST.json before consuming candidate code. Extract without links, special entries or undeclared directories.
2. The bundled `tools/checkpoint.py` implements that archive gate. It can be inspected separately and then used with `--zip CHECKPOINT --extract NEW_ROOT`. `tests/offline.py:verify_root` additionally checks exact recovered directory/file membership and entry types before loading the candidate. `retained/token/MANIFEST.json` is pinned by the new adapter; every predecessor member and directory is rechecked before candidate inputs.
3. The one public offline validation command is:

   `python3 -I -B NEW_ROOT/code/correspondence.py --root NEW_ROOT --receipt NEW_ROOT/results/primary/normal-session-exit-correspondence.json`

   It uses saved inputs only and must reproduce the complete canonical receipt, with both mandatory contexts. It does not connect to databases, resolve host session paths or call application lifecycle methods. Use Python 3.12.14 and Cryptography 50.0.2 for reproducibility of the retained validation chain. This is not host/environment qualification.
4. New focused control code is in `tests/focused.py` and `tests/process_checks.py`. Their recorded results are sufficient for engineering continuity; no rerun is needed for this checkpoint. The mode `recovered` exercises a separate focused subset, not the old campaign. `tests/offline.py` guards database/network/subprocess/host access and application-source execution while recording mandatory-chain entry calls. Full earlier suites in retained trees are provenance only.

The recovered-root controls refer to a recorded intermediate packaging cut with the exact current source, controls and primary receipt. Its manifest and identity are preserved in provenance. The final checkpoint adds process/recovery results and documentation, without changing those tested implementation or receipt bytes. New supplied results are not independent review closure. Failed attempts and their source/control snapshots remain in results and are excluded from completed totals.
