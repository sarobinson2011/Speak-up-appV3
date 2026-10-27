# Recover and validate this correction offline

Verify the supplied outer archive size/SHA-256, safe unique regular entry names, CRC and all top-level MANIFEST.json file hashes. Extract into a new persistent directory, never an existing session or evidence master. The full executable input root is original/; no external original ZIP is required for corrected validation. The exact original outer input/review ZIP identities and partial review-copy scope are in DEPENDENCIES.json. Do not rewrite nested historical manifests.

From the extracted root, using Python 3.12.14, optimization disabled and no bytecode writes:

```
python3 -I -B tests/fresh_check.py "$PWD"
```

For independent correction controls, choose an absent persistent output directory outside the checkpoint:

```
python3 -I -B tests/controls.py --root "$PWD" --output /absolute/new/persistent/HF01-review
```

The supplied focused recovered-root run uses tests/recovered_check.py with the extracted root and a new external output-directory argument. The --recovered option of controls.py is an optional reduced primary-suite selection; it is not counted as another supplied run. Do not use --write against the supplied receipt. No automatic correction or retry is performed. tests/input_gates.py may be run only on an additional disposable extraction; it inserts/removes invalid test entries there and restores original bytes. It does not test Unix sockets/devices; that prior limitation remains.

Do not reuse a gate-mutated extraction for positive validation. One separate-process run observed a gate-created FIFO after the gate process had returned; the loader correctly rejected that fixture. Preserve such failures and use a new verified extraction for positive validation. The included failed root's observed type/path and zero-assertion result remain separate from the successful clean-root checks.

The original minimal witness reproduction is already saved. Its preserved exact script is retained/review/code/minimal_head_witness.py and its target is original/. Do not rerun any prior suite or review to reproduce the correction. Do not execute original worker.py, launcher, runtime or session code; the new control entry installs audit/profile guards and parses those source files only as data.

The supplied recovered-root input archive is separately identified in results/recovery-input.json. Its entire code/tests/tools/original dependencies and corrected receipt are compared byte-for-byte with final delivery. Final packaging adds documentation/provenance and result records only; the recovered input and final archive identities are not conflated. Filesystem/ZIP integrity checks are not durability or exclusivity evidence.
