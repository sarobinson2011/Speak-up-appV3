# Saved-input recovery

Verify the final checkpoint's externally supplied byte count, SHA-256, entry count, CRC, safe unique regular-file membership and every MANIFEST.json identity before using candidate inputs. Extract to a new persistent directory without overlaying or repairing a failed root. tools/checkpoint.py retains the packaging/inspection utility; its --zip CHECKPOINT --extract NEW_ROOT form performs that archive gate. tests/offline.py:verify_root checks exact files, implied directory membership and entry types before loading candidate code. The adapter separately checks the complete strict retained/owner tree before consuming predecessor inputs.

For separately authorized offline validation, the public command is:

`python3 -I -B NEW_ROOT/code/correspondence.py --root NEW_ROOT --receipt NEW_ROOT/results/primary/stored-failure-revocation.json`

Use the recorded CPython 3.12.14 / Cryptography 50.0.2 profile for the retained chain. This is not runtime/platform, ownership, filesystem or durability qualification. Saved control results are evidence to reuse, not instructions to repeat completed work.

The unchanged predecessor is I164-owner-lock-finalization-correspondence-1.zip: 74,161,617 bytes, 2,495 entries, SHA-256 09f8b6d8c527f4032977f4e2862ba9a23e0e678a6f8294a5050603a26fb43a9b. Its review is Formal-Lab6-I164-owner-lock-finalization-independent-review.zip: 72,716,975 bytes, 69 entries, SHA-256 ad56746db089bddf2bcdd814f57b957aa2ef434a50f820bbade988bcde961e41. They were verified read-only and reused. All 2,495 target members are retained/owner; all 68 non-input review members are retained/review. The reviewed predecessor receipt is 4,348,225 bytes, SHA-256 6f2d1ac375017fd2f92923522aeba36defb89992d7fd071dd385e11d991d3c42.

Preserve all prior original-outer-archive and intermediate-cut qualifications. Decoded retained trees are not recompressed substitutes for original ZIP byte streams. The old 25,690,112-byte forensic partial (SHA-256 ed75ee885f67eca2938340b1aa5c423a9e60c04bceedfd3f90933cba0c44345e) remains inside retained/owner/retained/review/failures/recovered-membership/forensic-extra.bin, outside that predecessor's strict retained/exit tree. Its origin is UNESTABLISHED. Original failed root gates and the old interrupted process remain preserved and excluded from completed totals. No deletion or repair is authorized.

The new recovered-root checks use a recorded packaging cut containing the exact implementation, primary receipt and control code. The final checkpoint adds results/provenance without changing those tested bytes. Its cut manifest and identity are retained. Read RESULTS.json, provenance/changed-files.json and preserved failures before independent review. No Git save or new runtime operation is part of this checkpoint.
