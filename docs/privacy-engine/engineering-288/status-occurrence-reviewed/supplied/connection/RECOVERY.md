# Recover and inspect

Verify the communicated outer ZIP identity, safe unique regular membership, CRC and all MANIFEST.json members before extracting into a new directory. No symlink, special entry or directory-only entry is needed in this package. Preserve exact paths. The full declared correction tree is already present in retained/correction; do not reconstruct it from a compact selection or overlay an existing tree.

The new offline validator requires CPython 3.12.14 with optimization disabled; use -I -B. It compiles source to inspect instructions but never calls the application, imports Authority or connects to a database. The host Cryptography profile is saved evidence; no installed host profile or host session is needed here.

To inspect the saved result through the new consumer, when independently authorized:

    python3 -I -B code/smoke_occurrences.py check results/occurrence-connection.json

New independent checks can use tests/controls.py with a new absolute output directory. Existing results are reused, not overwritten. Do not run retained/correction tests, smoke worker or historical launcher. No pipeline or lifecycle command is part of recovery.

The public validate API recomputes from pinned archives and authenticated retained source. semantic(ctx, evidence) is an explicit internal negative-control seam and does not admit unpinned evidence. Existing runtime/model validators remain byte-for-byte intact. The complete new result has sorted compact JSON plus final LF serialization; semantic JSON equivalence alone does not satisfy the receipt contract.

The package omits only redundant recovered-root copies made by the new controls; their input tree is precisely the retained correction tree and the same new code/inputs/result. Their saved process outputs remain. All original archives and historical evidence remain exact.
