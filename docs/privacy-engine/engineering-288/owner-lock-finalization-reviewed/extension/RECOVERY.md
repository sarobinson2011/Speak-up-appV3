# Offline recovery

Match the final checkpoint's externally supplied byte count, entry count and SHA-256. Verify CRC, safe unique regular-file membership and every MANIFEST.json hash before consuming candidate inputs. Extract into a new persistent directory without overlaying a failed root, adding undeclared entries or relaxing type/membership checks. Preserve failures.

`tools/checkpoint.py` is the retained regular-file packaging/inspection utility; after inspecting it, `--zip CHECKPOINT --extract NEW_ROOT` performs the archive gate. `tests/offline.py:verify_root` checks exact recovered files, implied directories and entry types before loading the candidate. The adapter additionally pins and checks the complete strict `retained/exit` predecessor root before consuming its inputs.

For independently authorized offline validation, the current public command is:

`python3 -I -B NEW_ROOT/code/correspondence.py --root NEW_ROOT --receipt NEW_ROOT/results/primary/owner-lock-finalization.json`

Use CPython 3.12.14 / Cryptography 50.0.2 to reproduce the retained chain. This is not host, wheel, filesystem, OS-lock or runtime qualification. The command validates saved evidence only. It does not access host sessions or operate application methods/databases. New focused/process controls have saved results and need not be rerun for engineering continuity; previous campaigns in retained trees are provenance, not instructions to execute them.

The reviewed predecessor is I164-normal-session-exit-correspondence-1.zip: 70,593,959 bytes, 2,331 entries, SHA-256 c9c8d2106617970e8008fadc3c60f61813c64e7ce07e24a60bc92ac1029b954a. Its independent review is 71,870,780 bytes, 104 entries, SHA-256 c6c1952bde68aef3e9434968cd8838cfcbd4ab606e39fcaba112e6f73dada3df. Both were verified read-only and reused. All 2,331 predecessor members are at retained/exit; the 103 non-input review records are retained/review. The reviewed predecessor receipt is 4,032,928 bytes, SHA-256 928726175efbb720b03dc722de67477fa7ea3b3ce43b4c37bbeb2c9a730fea07.

The review's unexplained 25,690,112-byte partial file, SHA-256 ed75ee885f67eca2938340b1aa5c423a9e60c04bceedfd3f90933cba0c44345e, remains at retained/review/failures/recovered-membership/forensic-extra.bin with exact path/metadata records. It is outside the strict retained/exit root. Its origin remains UNESTABLISHED, its failed gates remain excluded, and no deletion or adoption into the target is authorized. Preserve all historical outer-archive and intermediate-cut qualifications exactly as recorded; decoded trees are not newly re-obtained original ZIP byte streams.

New recovered-root results use the recorded intermediate packaging cut containing exact implementation, controls and primary receipt. Its manifest/identity are preserved. The final checkpoint adds results and provenance without changing those tested bytes. Read RESULTS.json and changed-file identities before independent review. All obligations and readiness/admission boundaries remain unchanged.
