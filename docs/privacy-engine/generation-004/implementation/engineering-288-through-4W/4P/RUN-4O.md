# Reproduce and recover checkpoint 4O

Use Python 3.12 with SQLite/cryptography and the retained Linux native binaries. Work from the extracted package root in private quiescent storage. Reserve about 4 GiB for nested historical restoration/tests plus the ZIP. No command below launches either full retained stream. Preparation restores the existing compact model/structural descriptor, not a serialized full potential universe.

```sh
python3 verify_package.py
python3 prepare_retained.py
python3 verify_4o_inputs.py
python3 -m unittest tests.test_projections
python3 run_4o_cli.py
python3 coverage_4o.py
```

Full regression: `python3 -m unittest discover -s tests -v`. The declared code boundary is independently reproducible with `python3 -m unittest tests.test_projections.ProjectionTests.test_required_generated_parser_boundary_is_explicit`. The no-standalone bypass regression is `python3 -m unittest tests.test_projections.ProjectionTests.test_standalone_equal_bytes_cannot_bypass_containing_record`.

## Exact integrated pause/resume commands

Use a new key/checkpoint, keeping every path unchanged through recovery:

```sh
python3 -m integrated_auth keygen --key projection-job.key
python3 -m integrated_auth start --manifest fixtures/4O-E/manifest.json --trusted fixtures/4O-E/trusted.json --checkpoint projection-job.json --key projection-job.key --new-bytes 1
python3 -m integrated_auth resume --manifest fixtures/4O-E/manifest.json --trusted fixtures/4O-E/trusted.json --checkpoint projection-job.json --key projection-job.key --new-bytes 67108864 --seconds 50
python3 -m integrated_auth resume --manifest fixtures/4O-E/manifest.json --trusted fixtures/4O-E/trusted.json --checkpoint projection-job.json --key projection-job.key --seconds 50
```

Exit 3 is paused/interrupted with no success; repeat resume until completed or rejected. Exit 0 means only completed conditional fixture checks. Exit 2 is rejection. The last command exercises terminal reuse. Substitute 4O-PRE-EXECUTION or 4O-PRE-COMMITMENT for the other phases, using a different job. Preserve key, input directory, checkpoint and every checkpoint-prefixed stage/artifact, including generated contained `.4h-*.job.json` files. SIGINT/SIGTERM interrupt without successful authentication. Never relocate a live job or reuse CP4N completion receipts under CP4O. A moved or modified input requires a fresh job and full exact validation, not edited journals.

The object record locator is ephemeral and rebuilt from complete canonical bytes; completed semantic indexes/equality artifacts can be reused only after exact input/code/backend/prerequisite checks. Pure Ed25519 and native stream recovery retain prefix reconstruction. See PROJECTIONS-4O.md and retained LIFETIME-4N.md for the trusted quiescent-execution boundary and replay costs.

## Independent fixtures and bounded measurements

```sh
python3 -m fixtures.projections /tmp/4o-new-fixture --phase E --documents 128
```

Fixture construction independently derives canonical values, exact exhaustive small equality/scoped links and V2 signatures. Actual qualification is explicitly absent. The larger saved fixture is fixtures/4O-LARGER. No caller metadata can override the required source-reference joins or containing bytes.

Read PREFLIGHT-4O.md before `python3 run_4o_bench.py`. Use a fresh work/4O-benchmark directory, preserving any old job elsewhere, and preserve packaged result files before reproducing since that command writes new results. Each throughput child is capped below 60 seconds and total below 180. Historical correction/rebound scripts account for all attempts; they are not normal recovery commands. Signing and verification RSS are separate.

`python3 make_package.py` creates an independently hashed archive. `python3 verify_restore_4o.py` then fresh-extracts it, verifies all members/retained inputs, runs projection tests and CLI recovery, and regenerates the finite coverage witness. The packaged fresh-extraction report binds the preseal archive; the final archive's member hashes include that report, avoiding a circular self hash.
