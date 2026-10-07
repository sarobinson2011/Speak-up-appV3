# Reproduce checkpoint 4M

Python 3.12, SQLite, retained Python dependencies (including cryptography), and the supplied Linux native binaries are required. Preserve the extracted tree and run from its root. No command below launches either full pair/link stream.

```sh
python3 verify_package.py
python3 prepare_retained.py
python3 verify_4m_inputs.py
python3 -m unittest tests.test_catalogs tests.test_schedule tests.test_occurrence
python3 run_4m_cli.py
```

`prepare_retained.py` verifies the exact retained 4L ZIP, restores nested historical packages/descriptor and executable permissions. It does not expand the model or enumerate pairs. `run_4m_cli.py` requires a fresh `work/4M-cli` directory; preserve a prior run by moving it aside if rerunning. Full regression: `python3 run_checks.py --output results/my-4M-checks` with a new output path.

## Integrated recovery

```sh
python3 -m integrated_auth keygen --key job.key
python3 -m integrated_auth start --manifest fixtures/4M-E/manifest.json --trusted fixtures/4M-E/trusted.json --checkpoint job.json --key job.key --new-bytes 1
python3 -m integrated_auth resume --manifest fixtures/4M-E/manifest.json --trusted fixtures/4M-E/trusted.json --checkpoint job.json --key job.key --new-bytes 67108864 --seconds 50
python3 -m integrated_auth resume --manifest fixtures/4M-E/manifest.json --trusted fixtures/4M-E/trusted.json --checkpoint job.json --key job.key --seconds 50
```

Exit 3 means paused/interrupted with no success; 0 means completed conditional fixture checks; 2 means rejection. Repeat `resume` until completed or rejected. Third command exercises terminal reuse. Preserve the input directory, key, `job.json`, `job.json.*` and generated contained `.4h-*.job.json` inputs. Do not relocate a live job: absolute input identity is bound. A fresh location requires a fresh job and exact input revalidation. Do not reuse CP4L journals under CP4M.

## Catalog-only row-boundary recovery

A standalone expectation file contains `file` (path/bytes/sha256), `kind`, full `binding`, and independent `job` identity. The delivered CLI tests construct examples at `work/4M-cli/E/expect.json`.

```sh
python3 -m metadata_catalog work/4M-cli/E/occurrences.jsonl --expectation work/4M-cli/E/expect.json --state another-catalog-state --key work/4M-cli/key --rows 1
python3 -m metadata_catalog work/4M-cli/E/occurrences.jsonl --expectation work/4M-cli/E/expect.json --state another-catalog-state --key work/4M-cli/key
```

This proves transport framing and exact catalog bytes only; semantic membership, source qualification and authentication are explicitly false in its output. Use the integrated collector for source-grounded checks. Corrupt checkpoints are rejected; preserve them for diagnosis and start a new state directory to rebuild, rather than modifying signed completion records.

## Metadata-only size check

Read PREFLIGHT-4M.md first. On a fresh workspace with `work/4M-metadata` absent:

```sh
python3 run_4m_benchmarks.py
```

The supervisor caps each child at 60 seconds and all three at 180 seconds. It reads verified retained token shards only. Generated references deliberately have no actual value files; they cannot be submitted as successful value/authentication evidence. The corrective scripts/logs document this development run, not required extra steps for a clean reproduction. `python3 run_4m_capability.py` is a separate small capability witness, not a throughput benchmark.
