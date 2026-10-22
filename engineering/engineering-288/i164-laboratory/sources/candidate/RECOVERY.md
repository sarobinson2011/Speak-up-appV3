# Recovery and inspection

Verify the externally supplied ZIP size, entries and SHA-256 first. Verify ZIP CRC, safe unique member names, exact membership against MANIFEST.json, and all listed bytes/hashes. The manifest covers every member except itself. Preserve the received archive and original results.

Read REPORT.md, candidate/status.json, candidate/identity.json and provenance/inheritance.json. Prospective canonical registration has not occurred. No canonical HEAD is recovered or designated by this checkpoint.

All bytes needed for this bounded slice are included, including the selected native predecessor metadata/source bytes and actual 90 historical candidate files. Large predecessor archives/models/streams are referenced by exact identities rather than nested. The historical root manifest describes the larger original retrieval; it is not the current package membership manifest.

For read-only candidate correspondence validation in a fresh extraction:

    python3 -B tools/baseline.py validate

This verifies pinned inputs, rebuilds only small declaration/register metadata in memory, and compares candidate bytes. It does not execute runtime signing or construct the large model. Python 3 and the already-used cryptography dependency are needed for saved authenticated export checks; do not install new components as part of inspection.

For optional focused reproduction in a disposable extracted copy, first preserve results under another name, make a new results directory, then run:

    python3 -B tools/check_candidate.py

This reproduces candidate metadata controls and ingests saved fixtures. It does not repeat a lifecycle, execute transactions or rerun prior reviews. Expected final completed checks: 58; saved exports: 12. Earlier failed attempts and prior successful intermediate receipt remain historical evidence and must not be added to that count.

To reconstruct candidate metadata in a disposable copy, preserve candidate/ under another name and run:

    python3 -B tools/baseline.py build

The builder refuses an existing output directory. Native raw files and source hashes remain authoritative inputs; do not normalize native artifacts or edit input pins to make a mismatch pass. tools/acquire.py documents original read-only acquisition from the two exact predecessor archives; normal recovery does not require rerunning it.

Return findings to Engineering-Anchor[2]. No canonical publication, operational admission, stream generation, migration or retention/compaction is authorized.
