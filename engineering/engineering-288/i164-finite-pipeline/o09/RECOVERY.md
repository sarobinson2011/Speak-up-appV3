# Recovery and one bounded command

Verify this ZIP's CRC, safe exact membership and every MANIFEST.json identity before extraction. Use code/package.py verify ARCHIVE --extract NEW_DIRECTORY, or an independent equivalent. No application databases need to be opened.

Six exact external archive identities are enumerated in code/recover.py::EXTERNAL; the embedded count and ledger identities and the two ordered candidate corrections are checked by that existing recovery procedure. The reviewed O09 code is included unchanged and pinned by connect.COPY_PIN. Its independent review and component manifests/provenance are retained here; their full archives are reference dependencies for independent evidence review, not executable runtime requirements. CF-01 predecessor identity is recorded in CHANGED-IDENTITIES.json.

Write locations.json with absolute archive paths for keys inputs, consumer, ledger_review, draft, discriminator and unknown. Then, under CPython 3.12.14 with the compatible reviewed dependencies:

    python3 -B code/recover.py --locations /absolute/locations.json --output /persistent/new-recovery
    python3 -I -B code/connect.py --config /persistent/new-recovery/config.json --output /persistent/new-validation

The recovery command needs its sibling connect import; do not add -I to recovery. Validation uses isolated worker subprocesses. Expect roughly 5–15 minutes, with progress every 30 seconds. Stop on a failure; preserve the failed directory, logs and exact unexpected entries. Do not automatically remove unexpected inputs, retry, connect databases or recreate sessions. Recovery success alone is not validation success.

The final receipt binds both contexts and actual five-stage outputs. Original large bundle/model/ledger outputs are recoverable from the exact predecessor archives and are not repeatedly nested in this compact checkpoint. New receipt, execution logs, identities and focused results are retained here. An unchanged saved O09 receipt may be used for post-stage mutation fixtures only; it does not replace mandatory public pipeline execution.

Focused checks:
    python3 -B code/check_integration.py --code code/connect.py --config /persistent/new-recovery/config.json --run /persistent/new-validation --output /persistent/new-checks
    python3 -B code/check_final.py --code code/connect.py --config /persistent/new-recovery/config.json --run /persistent/new-validation --output /persistent/new-final-checks

These are integration linkage tests, not a renewed component review or operational qualification. Eleven obligations, UNKNOWN classifications and all readiness/admission blockers remain.
