# Exact recovery and bounded execution

Verify this archive's CRC, safe unique regular membership and all MANIFEST.json entries before use. The included package.py can verify and fresh-extract without executing candidate procedures. Keep original archives and failures unchanged.

Required predecessor identities are in provenance/dependencies.json. The original O09 integration (eadb44...; 5,480,698 bytes) and its six externally pinned recovery archives remain required for a cold recovery. They are not nested here. The unchanged code/recover.py contains all six full identities and composes the exact current 666-member candidate and 163-member draft. Use `python -B code/recover.py --locations /absolute/locations.json --output /absolute/new-recovered-root`; locations.json maps the six EXTERNAL keys to their exact archive paths. Original recovery instructions are retained in provenance/O09-RECOVERY.md. It runs no pipeline. Do not replace the complete composition with a historical candidate root. Reuse already verified roots where present.

The O06 component/review provide prior exact evidence, source mappings and failures; their identities are in dependencies.json. The reviewed copies.py and multiplicity.py are included unchanged and explicitly pinned in connect.py. Existing count, model, bundle and ledger inputs are pinned by provenance/pins.json and their original manifests. The new receipt derives its copy path from this run, not the historical hard-coded receipt path.

Use CPython 3.12.14 without optimization, and the separately prepared Cryptography 50.0.2 environment. No installation or gate bypass is part of this checkpoint. From the recovered component, with the config produced by the unchanged recovery code (or the existing exact config):

    /absolute/prepared/python -I -B /absolute/checkpoint/code/connect.py --config /absolute/recovered/config.json --output /absolute/new-persistent-output

This performs the actual six saved-evidence stages once, normally several minutes (allow 5–15 minutes). Progress appears at each stage and every 30 seconds. Failure stops and leaves logs/failure.txt, with no retry. Do not use /tmp, an existing output, or an input directory as output. No databases are opened; worker/audit protections reject database/network activity. Save all failure output.

Focused new linkage controls (not a repeated full pipeline):

    /absolute/prepared/python -I -B /absolute/checkpoint/code/check_expressions.py --code /absolute/checkpoint/code/connect.py --config /absolute/recovered/config.json --run /absolute/completed-output --output /absolute/new-controls
    /absolute/prepared/python -I -B /absolute/checkpoint/code/check_final.py --code /absolute/checkpoint/code/connect.py --config /absolute/recovered/config.json --run /absolute/completed-output --output /absolute/new-final-controls

For fresh-process/recovered-code checks, recover exact code plus provenance/pins.json to a new persistent root, and run check_expressions.py there with --case positive, --case lifetime-zero, or --case coordinated-count. These validate actual saved receipts against current authoritative inputs; they do not rerun producers. Tests can be requested independently, but no completed suite needs rerunning merely for recovery.

Bulky actual bundle/model/ledger outputs are retained outside this compact package and are byte-identical to pinned predecessor outputs. Their exact identities and per-stage commands/results are included in results/connected. All compact new receipts and logs are included. Reproduce the connection only when authorized, not to manufacture original evidence.
