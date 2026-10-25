# Recovery and bounded validation

Verify this checkpoint's reported ZIP size/SHA-256, CRC, safe unique membership and MANIFEST.json before extraction into a new persistent directory. Do not use /tmp. `code/package.py` verifies and extracts without importing application sources.

The exact supplement is included in inputs; it includes the unchanged original inventory. No Steve-host file collection is required. The existing reviewed O06 expression receipt is included as inputs/expression-receipt.json. The prior evaluator and O09 module are byte-identical copies in code. Source pins, compact dependency references and predecessor recovery instructions are in provenance.

Reuse the unchanged verified candidate, draft, count archive/root and copy receipt. Full cold predecessor recovery is owned by I164-O06-finite-integration.zip (156596 bytes, SHA-256 bf22d15a7caf805902d70cb8b29daf9b335fe4c66b6a552d45c30ff9e18647de), its documented O09 predecessor and six external archives. Full identities are in provenance/dependencies.json, predecessor-dependencies.json and recover_predecessor.py::EXTERNAL. The latter is preserved reference code requiring its original connect.py/package; do not execute it standalone here. No historical 666-member fragment substitutes for the current composition. This checkpoint does not replace those dependencies.

Create a JSON configuration with exactly:

    {
      "expression_config": {
        "candidate": "/absolute/verified/candidate",
        "draft": "/absolute/verified/draft",
        "count_archive": "/absolute/pinned/counts.zip",
        "count_root": "/absolute/verified/counts",
        "copy_receipt": "/absolute/validated/05-copies/receipt.json"
      },
      "expression_receipt": "/absolute/this-checkpoint/inputs/expression-receipt.json",
      "inventory_archive": "/absolute/this-checkpoint/inputs/SEND-TO-ANCHOR-inventory-supplement.zip"
    }

Use the prepared CPython 3.12.14 / Cryptography 50.0.2 environment without installing or upgrading dependencies:

    /absolute/prepared/python -I -B /absolute/this-checkpoint/code/inventory_connection.py --config /absolute/config.json --output /absolute/new-persistent-output

For validation of an existing receipt append `--submitted /absolute/receipt.json`. Allow 1–3 minutes for current pinned saved-source validations; no application, database, session, acquisition or complete pipeline execution occurs. A failure preserves failure.txt and stops. Never treat a missing result or stopped validator as success.

Focused new checks, when independently authorized:

    /absolute/prepared/python -I -B /absolute/this-checkpoint/code/check_connection.py --code /absolute/this-checkpoint/code/inventory_connection.py --config /absolute/config.json --output /absolute/new-controls

The normal suite consumes saved evidence, tests constructed receipt mutations, then validates pristine data after public-result mutation. For process tests, place expected.json (the successful new connection receipt) alongside config.json and pass `--case positive`, `--case mixed`, or `--case claim`. Negative process checks require the exact new correspondence rejection, not an unrelated input failure. check_obligations.py adds constructed eleven-obligation and fourteen-lifetime checks; see saved commands.

Recovery limitation: two candidate/draft copied-root attempts acquired undeclared partial files and failed strict membership/parsing. Originals remain unchanged. Their bytes, failures and identities are retained under failures; origin is UNESTABLISHED. They do not count as successful recovered-candidate validation or successful mutation controls. Component-root recovery with the unchanged verified predecessor roots is separately tested. Do not remove fragments silently or relax membership validation.

No sessions need to be reopened, no tests/reviews rerun merely for continuity, and no final-binding or qualification claim follows from recovery.
