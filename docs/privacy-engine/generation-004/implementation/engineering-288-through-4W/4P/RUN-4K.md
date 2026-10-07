# Exact commands

Run from the extracted checkpoint directory on Linux x86-64 with Python 3.12, standard SQLite and the retained native binaries. `cryptography` is used only by independent laboratory fixture signing. Pinned backend build dependencies/instructions remain under `crypto_backend/`; no replacement cryptographic backend is introduced.

Verify before running, then materialize the exact retained descriptor and executable permissions:

```sh
python verify_package.py
python prepare_retained.py
python verify_4k_inputs.py
python -m unittest tests.test_schedule -v
python run_4k_cli.py
```

`verify_4k_inputs.py` verifies historical normative/model/backend identities and emits current manifests. Result-generating commands intentionally write new output files; therefore check the delivered package manifest first. The complete regression reproduction is:

```sh
python run_checks.py --output work/4K-reproduced-checks
```

Use a new output directory each time. This is a correctness suite, not a performance benchmark. It does not process either full retained stream. Historical direct-collector fixtures have old code pins; use the delivered 4K fixtures or regenerate with current constructors.

## Pause, resume, finish and terminal reuse

The delivered `4K-COMPLETE` fixture is independently signed, has complete conditional semantic duties and 64 outcomes per world, and is not source-qualified for actual admission. The small DELTA fixture is also included. No provided command enables actual admission.

```sh
mkdir -p work/4k-demo
python -m integrated_auth keygen --key work/4k-demo/key
python -m integrated_auth start --manifest fixtures/4K-COMPLETE/manifest.json --trusted fixtures/4K-COMPLETE/trusted.json --checkpoint work/4k-demo/journal --key work/4k-demo/key --new-bytes 83 --auth-new-bytes 268435456 --chunk-bytes 17 --seconds 50
python -m integrated_auth resume --manifest fixtures/4K-COMPLETE/manifest.json --trusted fixtures/4K-COMPLETE/trusted.json --checkpoint work/4k-demo/journal --key work/4k-demo/key --new-bytes 127 --auth-new-bytes 268435456 --chunk-bytes 17 --seconds 50
python -m integrated_auth resume --manifest fixtures/4K-COMPLETE/manifest.json --trusted fixtures/4K-COMPLETE/trusted.json --checkpoint work/4k-demo/journal --key work/4k-demo/key --new-bytes 268435456 --auth-new-bytes 268435456 --quanta 3 --seconds 50
python -m integrated_auth resume --manifest fixtures/4K-COMPLETE/manifest.json --trusted fixtures/4K-COMPLETE/trusted.json --checkpoint work/4k-demo/journal --key work/4k-demo/key --new-bytes 268435456 --seconds 50
```

Exit 3 is paused/interrupted, exit 0 means conditional checks only, exit 2 is rejected. Stdout is the result; stderr streams progress. An interrupted recheck never reports authentication success. Preserve the input directory, trusted file, key, main journal, `journal.stages/`, all scope `.bytes`/`.crypto` journals and generated source-directory job manifests together at unchanged paths. If the main journal was never committed, retry start; otherwise resume. Old checkpoint versions or relocated/substituted jobs must start fresh. Do not hand-edit receipts.

For tested native partial-row positions, crypto-prefix interruptions, interrupted atomic writes, pre-ledger interruption, index/terminal reuse and mutation/substitution rejection, run `tests.test_schedule`. The tests retain and compare exact digests/counts/verdicts against the separate uninterrupted collector and the retained independent exhaustive oracle tests. Run just the retained oracle/recovery modules with `python -m unittest tests.test_stream tests.test_recovery -v` (these are bounded fixtures).

## Bounded performance reproduction only

Measured results already ship in `results/4K-*`. If reproducing benchmarks, use exactly these three processes, each with the external 60-second ceiling; aggregate ceiling is three minutes. These overwrite benchmark results/current fixture inputs and require new work journals.

```sh
timeout 60s python run_4k_preflight.py
timeout 60s python run_4k_composition.py construct
timeout 60s python run_4k_composition.py validate
```

The retained-index preflight consumes only a 67-byte header, rejects expected incompleteness, and enumerates zero pairs. Composition `validate` needs a fresh `work/4K-composition` location (archive any previous work directory first). Signing and validation run in separate processes. Do not interpret these measurements as full-scale conformance. No full-stream execution command is part of this checkpoint. `RECOVERY-4K.md` gives the practical invocation and trusted-execution boundary.
