# Saved-input recovery

Verify the final supplied archive identity, CRC, exact safe regular membership and every MANIFEST.json hash before candidate consumption. Extract only into a new empty persistent directory, never over a failed root. tests/offline.py checks exact files, implied directories and entry types. The mandatory adapter separately gates all retained/callback members before importing its validator.

For separately authorized offline use, the public command is:

`python3 -I -B NEW_ROOT/code/correspondence.py --root NEW_ROOT --receipt NEW_ROOT/results/primary/callback-bare-rethrow.json`

Use the recorded CPython 3.12.14 / Cryptography 50.0.2 environment. This does not authenticate a host installation or qualify other versions. Reuse saved completed results; recovery does not authorize repeating campaigns.

Predecessor: I164-callback-exception-stored-failure-correspondence-1.zip, 84,555,031 bytes, 2,807 entries, SHA-256 0a39361622d3c05c7f46b258bfd7570d632ab57ee87317103cacce1f52822255. All members are retained/callback. Its exact receipt is 6,418,679 bytes / SHA-256 c5504cf29408dad2e916a2dedd43b654f88fd2e88bb26682e0ceaa31ee2268a0.

Independent review: 82,756,868 bytes, 66 entries, SHA-256 e14858c4bdb77f8aa158d9091bac40f76a6d4548f91d72412b1dbe8fd1be8ec3. All 65 non-input members are retained/review. The embedded duplicate input ZIP is not repeated; its original identity and every decoded input member are preserved. Recompression does not reconstruct its original outer bytes. Existing forensic/intermediate-cut qualifications remain in effect.

Read RESULTS.json for completed new controls versus failed attempts and historical results. Changed-file identities and the exact diff are in provenance/. A frozen recovery cut contains the tested code, primary receipt and controls; the final checkpoint adds completed process results/provenance without changing those tested bytes. Runtime observations remain unavailable. No Git save is part of this work.
