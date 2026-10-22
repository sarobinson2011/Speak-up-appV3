# Recover and validate this bounded draft connection

Verify delivered archive bytes/SHA-256, CRC, exact membership and MANIFEST.json before use. Extract into a fresh folder. Run:

    python3 -B recover.py

This materializes only the embedded exact reviewed SOURCE-ONLY dependency. No candidate code, tests, expansion or lifecycle is run. Preserve existing exact verified candidate roots. If a root is unavailable, use source-only/RECOVERY.md and its unchanged recovery script with:

- discriminator closure: 9,280,888 bytes / 50 entries / SHA-256 a5a928a1d45e792059c70bc727a58fd4186865518fe158b9055fe4cdf861b218
- unknown-method closure: 31,900,862 bytes / 56 entries / SHA-256 5c4f1f9960493de9c3c0ec8c80fda2da0b75b5fb70c079149f422f3d737c3aff

The exact 666-member root manifest is source-only/universe/provenance/root-members.json, SHA-256 feef1fd4b423c067fa073b9aacb788a6553ec6fe99cde2dbfb0154ff25119209. Unexpected files must not be silently admitted or deleted; preserve them separately and determine exact identity before recovery continues.

One complete validation command, using CPython 3.12.14 and the retained cryptography dependency:

    python3 -B code/construction_inputs.py --root /exact/current-root --validate outputs

This consumes actual current inputs and the reviewed mandatory SOURCE-ONLY path, validating the emitted draft objects with the existing procedure validator. It reports bounded draft correspondence only. Full regeneration can take several minutes; no success cache or full model expansion is used.

To construct a new separate copy (not necessary merely to review saved results):

    python3 -B code/construction_inputs.py --root /exact/current-root --output /new/draft-output

Outputs cannot overwrite an existing directory. Keep output and review mutations outside strict candidate/source-only trees. `code/checks.py ROOT` exercises focused static mutations; `code/process_checks.py ROOT` uses the packaged outputs and a separate mutable process fixture. Their logs are not independent review. Do not repeat these or predecessor reviews merely for continuity.

Input review provenance: Engineering-Anchor2-I164-source-only-independent-review.zip, 29,809,796 bytes / 56 entries / 3b852fdb9a1af1aa441923182600762059107ae197659c08511ec7491fdf9052. This archive remains the complete record of its independent controls, failures and partials; its report/summary are copied exactly here as references. It is not required to execute the draft adapter after the exact embedded integration and 666-member root are available.

Embedded input: SOURCE-ONLY integration, 9,569,533 bytes / 107 entries / 7f58a377120157b379058f3aa4642de14625eda243792b8a5b681da9f969596d. All its prior evidence and development provenance are preserved unchanged. No original unavailable retry ZIP is recovered by this package.
