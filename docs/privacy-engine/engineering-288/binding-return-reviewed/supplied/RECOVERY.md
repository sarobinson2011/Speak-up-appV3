# Recover this bounded extension

Verify the delivered ZIP's reported size/SHA-256, safe unique regular membership, CRC and every top-level MANIFEST.json hash before extracting into a new persistent directory. Never extract over a session or evidence master. Preserve nested historical manifests unchanged. No database connection is needed for recovery or validation.

The complete HF-01 predecessor is decoded under retained/hf01/ (732 exact members). Its original outer ZIP identity is in DEPENDENCIES.json. Its original/ directory contains the exact 617-member earlier recovery extension and all predecessor sources. retained/review/ contains all 72 non-input closure-review members; that review's manifest still also names its external redundant input ZIP. The delivered top-level manifest describes the actual complete membership here. No external source or database download is needed for this new offline validation.

Using Python 3.12.14, optimization disabled and bytecode writes disabled, the new focused command is:

```sh
python3 -I -B tests/fresh_check.py "$PWD"
```

The wrapper installs audit/call guards and invokes the current mandatory validator over results/binding-correspondence.json. It does not invoke the previous tests, review scripts, worker, launcher or session code. No original database is opened. The explicit current public CLI is code/correspondence.py --root ROOT --receipt RECEIPT; the guarded fresh_check.py wrapper is preferred for independent validation.

For separately authorized independent review, the newly supplied controls accept:

```sh
python3 -I -B tests/controls.py --root "$PWD" --output /absolute/new/persistent/binding-review
```

--recovered selects a smaller focused set for a separately verified recovered root. Do not pass --write against the supplied receipt. tests/input_gates.py requires three arguments: verified source root, absent disposable copy directory and absent result directory. It never uses that gate-mutated copy for positive validation. These commands are recovery instructions, not a request to repeat completed work now.

results/recovery-input.json identifies the separately packaged/extracted stable input used for the supplied recovered-root run. Its code, tests, tools, exact retained inputs, provenance, preserved incomplete attempt and receipt are byte-compared to the delivered checkpoint. Final documentation and completed result records are added afterwards and have their own final outer identity; they are not conflated with the recovered-input ZIP.

The completed host Git save receipt is retained as provenance/previous-git-receipt.json, commit f4e2d6f06f662f64bd26276f05c0f17fa7874b06. This task does not repeat that save or save this new unreviewed extension to Git. All previous independent/support scopes and missing-observation, socket/device, custody, durability, lifetime and qualification limitations remain.
