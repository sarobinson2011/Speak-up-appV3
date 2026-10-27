# Recover this bounded extension

Verify the delivered ZIP size/SHA-256, CRC, safe unique regular membership and every top-level MANIFEST.json hash before extraction into a new persistent directory. Do not extract over a session or evidence master. Keep nested historical manifests exact. Recovery reads saved files only and requires no database connection.

The entire 844-member reviewed binding checkpoint is decoded under retained/binding/, including all executable predecessor inputs and previous failures. Its original archive identity and the independently reviewed archive identity are in provenance/input-verification.json. The compact review records under retained/binding-review/ intentionally omit two large members: the redundant original input ZIP and the exact failed-root binary. Their identities and full external archive identity are retained. They are not needed by the mandatory executable chain; that review's historical manifest still names them, and has not been rewritten to suggest full decoded membership.

Using Python 3.12.14, optimization disabled and bytecode writes disabled:

```sh
python3 -I -B tests/fresh_check.py "$PWD"
```

This installs the audit/call guards and invokes the current mandatory validator over results/config-correspondence.json. It invokes no previous tests or review scripts and no application/session entry. The direct public CLI is code/correspondence.py --root ROOT --receipt RECEIPT; the guarded wrapper is preferred for independent validation.

For separately authorized independent review, the new controls accept:

```sh
python3 -I -B tests/controls.py --root "$PWD" --output /absolute/new/persistent/config-review
```

--recovered selects the focused recovered-root subset. Do not pass --write against an existing receipt. These are recovery instructions, not an instruction to rerun completed work now.

results/recovery-input.json identifies the separately packed and extracted stable input for Engineering's recovered-root check. Its code, tests, tools, exact retained inputs, failure records, provenance and receipt are compared with this final checkpoint. Completed result records and final documentation are added afterwards and have their own final outer identity. Do not conflate the intermediate recovery input with the final deliverable or prior independent checkpoints.

The completed Git receipt at provenance/previous-git-receipt.json records commit d1f9f3a6468f023701ee7cbd2643ae38731f4529. This task does not repeat that save or commit this new unreviewed extension. Getter execution and physical copy identities remain unavailable. All existing scope, qualification and readiness/admission limitations remain.
