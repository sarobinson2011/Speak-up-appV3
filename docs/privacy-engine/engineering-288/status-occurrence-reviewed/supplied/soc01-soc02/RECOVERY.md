# Offline recovery

Verify the outer archive size/SHA-256, safe unique regular membership, CRC and exact MANIFEST.json. Extract into a new persistent directory, preserving paths. The checkpoint contains the complete retained correction root and its original archives; no host session or external repository is needed. Root code and stable filesystem remain trusted prerequisites.

CPython 3.12.14, optimization disabled, -I -B is required for source instruction inspection. No application or worker is executed and no database is opened. The corrected pristine validation command is:

    python3 -I -B corrected/code/smoke_occurrences.py check corrected/results/occurrence-connection.json

When independently authorized, new closure controls may run with a new output directory:

    python3 -I -B tests/correction_controls.py --root /absolute/checkpoint/corrected --output /absolute/new/closure-controls

tests/reproduce.py accepts an optional new absolute output directory and reproduces only the nine exact old witnesses with original/code/smoke_occurrences.py. The old module uses the byte-identical dependencies under corrected/ if a full original root is absent. The complete historical target remains embedded in inputs/independent-review.zip. Do not rerun the whole prior review or supplied suites.

The package omits redundant original/recovered dependency-tree copies. The delivered corrected/ tree preserves all 463 original retained correction members and both input archives. Only the new outer MANIFEST.json describes the delivered correction checkpoint. Nested retained manifests keep their original scope. New changed-file identities and source-stability checks distinguish corrected code from predecessor code. The original pristine receipt is deliberately retained unchanged; tightening validation does not require regenerating its observations.
