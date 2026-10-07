# Reproducible verification and recovery

Run from the extracted checkpoint 4J directory. Python 3.12, SQLite (standard library), cryptography for fixture signing, Linux x86-64 for the retained pinned crypto/native workers. Backend build dependencies and exact versions remain in crypto_backend/. No new package installation is required in the supplied environment.

Verify first, then restore retained inputs and executable permissions:

```sh
python verify_package.py
python prepare_retained.py
python -m unittest tests.test_semantic_stream -v
python run_4j_cli.py
```

`run_4j_cli.py` performs seven isolated commands: construct independent fixture, create local recovery key, pause, pause again, finish, revalidate terminal state, reject a corrupted journal. No full retained stream is involved. The full regression suite is optional reproduction of the delivered actual result:

```sh
python run_checks.py --output work/4J-reproduced-checks
```

Use a new output directory each time. Verification of the delivered manifest is before reproduction because result-generating scripts intentionally write new measured result files.

The following commands use the delivered complete conditional GAMMA inputs. Exit 3 after start means a deliberate pause; continue with resume. Exit 0 means conditional checks only; exit 2 means rejected. No command enables actual admission.

```sh
mkdir -p work/4j-recovery-demo
python -m integrated_auth keygen --key work/4j-recovery-demo/key
python -m integrated_auth start --manifest fixtures/4J-GAMMA/manifest.json --trusted fixtures/4J-GAMMA/trusted.json --checkpoint work/4j-recovery-demo/journal --key work/4j-recovery-demo/key --new-bytes 83 --chunk-bytes 17 --seconds 50
python -m integrated_auth resume --manifest fixtures/4J-GAMMA/manifest.json --trusted fixtures/4J-GAMMA/trusted.json --checkpoint work/4j-recovery-demo/journal --key work/4j-recovery-demo/key --new-bytes 127 --chunk-bytes 17 --seconds 50
python -m integrated_auth resume --manifest fixtures/4J-GAMMA/manifest.json --trusted fixtures/4J-GAMMA/trusted.json --checkpoint work/4j-recovery-demo/journal --key work/4j-recovery-demo/key --new-bytes 10000000 --seconds 50
```

If the collector journal exists, use resume. If interrupted before its first commit, rerun start; separately committed authentication substages are detected. Keep the exact input directory, manifest, trusted contract, local key, main journal and all scope byte/crypto journals together. A different path, input, implementation or key requires a new job identity, not editing the receipt. An incomplete temporary checkpoint/index is never a completion record. Prefix identity is re-established by exact rereading/hashing, not timestamps.

To reproduce the delivered **bounded** larger complete semantic case in a separate process:

```sh
mkdir -p work/4j-large-reproduction
python -m integrated_auth keygen --key work/4j-large-reproduction/key
timeout 60s python -m integrated_auth start --manifest fixtures/4J-LARGE/manifest.json --trusted fixtures/4J-LARGE/trusted.json --checkpoint work/4j-large-reproduction/journal --key work/4j-large-reproduction/key --new-bytes 268435456 --seconds 55 > work/4j-large-reproduction/result.json
```

Reuse those inputs without signing or reconstruction. Regenerating the larger fixture uses `timeout 60s python run_4j_large.py construct`; this is a separate high-memory laboratory signing process (about 611 MiB measured) and writes the exact current fixture. The `validate` operation measures its own process RSS separately. Run no more than three performance attempts of at most 60 seconds each in a bounded preflight. Delivered results already include three bounded validation measurements; no full-universe execution command is given here.

For independent small fixtures use `python -m fixtures.integrated work/new-fixture --family DELTA`. The source-language constructors are separate from the disk parser/invocation implementation. Original in-memory invocation bytes are compared with the new streamed output in tests. Never replace exact source-specific bytes with a descriptor hash.
