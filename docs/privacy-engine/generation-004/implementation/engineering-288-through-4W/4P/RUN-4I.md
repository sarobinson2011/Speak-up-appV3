# Reproducible verification

Run from the extracted Engineering-288-checkpoint-4I directory. Python 3.12 and the retained test dependencies are as in 4H; the pinned Linux x86-64 RFC8032 binary is unchanged. `prepare_retained.py` restores executable modes and exact retained package/descriptor bytes; it does not generate either full stream.

```sh
python verify_package.py
python prepare_retained.py
python -m unittest tests.test_amendment -v
python run_checks.py --output work/4I-tests
python run_4i_cli.py
python -m v4_ingest record fixtures/4I-RECORD-GAMMA/field-label.json --schema FIELD-LABEL --field-register fixtures/4I-RECORD-GAMMA/field-register.json
python -m v4_ingest security fixtures/4I-RECORD-GAMMA/security.json --field-register fixtures/4I-RECORD-GAMMA/field-register.json
```

The standalone register is a canonical JSON array of exact names, independently acquired for the intended complete model. It is not derived from the candidate labels themselves. Without required register context, FIELD-LABEL ingestion fails. Local success always reports unqualified; complete source ownership/coverage/visibility and authority remain collector duties.

To exercise the amended file-backed collector with pause/resume:

```sh
mkdir -p work/4I-run
python -m integrated_auth keygen --key work/4I-run/key
python -m integrated_auth start --manifest fixtures/4I-RECORD-GAMMA/manifest.json --trusted fixtures/4I-RECORD-GAMMA/trusted.json --checkpoint work/4I-run/collector.json --key work/4I-run/key --new-bytes 83 --chunk-bytes 17 --seconds 50
python -m integrated_auth resume --manifest fixtures/4I-RECORD-GAMMA/manifest.json --trusted fixtures/4I-RECORD-GAMMA/trusted.json --checkpoint work/4I-run/collector.json --key work/4I-run/key --new-bytes 10000000 --seconds 50
```

Exit 3 is paused, 2 rejected, and 0 conditional checks passed only. Do not chain a deliberately paused start to resume using `&&`; a pause is expected. Existing checkpoints bind exact implementation/input identities. 4H receipts cannot grant 4I authentication or semantic success. New source/profile identities require new jobs and journals. RECOVERY-4H.md's exact-prefix replay strategy and its production-scale limitations still apply; none were loosened.

Deterministic reconstruction, only when intentionally reproducing the delivered artifacts:

```sh
python -m amendment_tools.materialize
timeout 60s python -m amendment_tools.dependencies
python -m amendment_tools.fixtures
```

`materialize` writes only the named amended version and explicit runtime projections, never accepted/. `dependencies` reconstructs only catalogs and bindings from saved results, not token/edge expansion or full streams; see PREFLIGHT-4I.md. It hash-verifies all input members it acquires and writes outputs under rebinding/. The elapsed-time result naturally changes between runs. `fixtures` rebuilds four independent conditional datasets and their signatures, not a full retained-model witness. Compare semantic identities using results/4I-dependency-impact.json and results/4I-profile-dependencies.json, not a prior execution timestamp.

For a concrete saved duty query against the rebound provenance, use:

```sh
python -m ledger_kernel.query node 36511 --output rebinding/ledger
```

The legacy ledger inventory builder's default still describes the historical CP2 construction. Do not overwrite that inventory to label it amended. The new BINDING.json explicitly joins the unchanged saved model/coverage to regenerated class provenance and the revised contract.
