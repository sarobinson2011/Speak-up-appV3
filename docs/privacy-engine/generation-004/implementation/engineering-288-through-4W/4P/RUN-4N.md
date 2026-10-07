# Reproduce checkpoint 4N

Use Python 3.12, SQLite, the retained Python dependencies (including cryptography), and supplied Linux native binaries. Work from the freshly extracted package root in a private, quiescent local directory. Reserve about 3 GiB for nested historical restoration and test artifacts, plus the ZIP. No command below generates either full retained stream. `inputs/links.txt`, restored by prepare_retained, is the historical compact model/structural descriptor, not a serialized full potential/link stream.

```sh
python3 verify_package.py
python3 prepare_retained.py
python3 verify_4n_inputs.py
python3 -m unittest tests.test_lifetime
python3 run_4n_cli.py
```

The verifier checks the exact retained 4M ZIP and every parent manifest member, unchanged accepted/model/amendment/backend/byte-law files, and current code/fixture identities. Preparation restores the unchanged nested predecessor archives/descriptor and executable bits. Full regression: `python3 -m unittest discover -s tests -v`. `run_checks.py --output results/my-4N-checks` also records detailed full-suite and legacy admission CLI results; choose a fresh output directory. These are correctness checks, not permission for a full-scale stream run.

## Pause, resume and terminal reuse through the authenticated collector

Use a new key and job name; do not reuse CP4M journals. The 16-fragment GAMMA and DELTA fixtures are complete conditional small ledgers with shared source dependencies and independent invocation/scoped-link oracles. 4N-MANY has 768 shared fragments.

```sh
python3 -m integrated_auth keygen --key job.key
python3 -m integrated_auth start --manifest fixtures/4N-GAMMA/manifest.json --trusted fixtures/4N-GAMMA/trusted.json --checkpoint job.json --key job.key --new-bytes 1
python3 -m integrated_auth resume --manifest fixtures/4N-GAMMA/manifest.json --trusted fixtures/4N-GAMMA/trusted.json --checkpoint job.json --key job.key --new-bytes 67108864 --seconds 50
python3 -m integrated_auth resume --manifest fixtures/4N-GAMMA/manifest.json --trusted fixtures/4N-GAMMA/trusted.json --checkpoint job.json --key job.key --seconds 50
```

Exit 3 means paused/interrupted with no success; 0 is completed conditional fixture checks; 2 is rejection. Repeat resume until completed or rejected. SIGINT/SIGTERM cause an interrupted result; an abrupt kill leaves only atomically completed receipts reusable. Preserve job.key, job.json, all job.json.* paths, source directories and generated contained `.4h-*.job.json` files. The last command exercises terminal reuse. Never relocate a live job or use a journal to override changed source bytes. See LIFETIME-4N.md for exact rehash/prefix-replay costs and trust boundary.

## Independent fixtures and original failure

```sh
python3 -m fixtures.lifetime /tmp/4n-new-fixture --documents 128 --family GAMMA
python3 reproduce_4m_witness.py
```

The fixture constructor signs under the current implementation identity; modifications to validator code require newly constructed fixtures and jobs, not editing pinned identities in signed material. Both GAMMA and DELTA inherited invocation codecs are covered. The original witness deliberately loads the exact retained 4M implementation in a separate temporary extraction and confirms handle exhaustion under 96; it does not corrupt current fixtures/results.

## Bounded benchmark reproduction

Read PREFLIGHT-4N.md first. `python3 run_4n_bench.py` requires a fresh `work/4N-benchmark` path and runs three externally time-capped child processes (construct/sign, integrated validation/recovery, repeated cycles), with RLIMIT_NOFILE=96. It overwrites the named benchmark result files, so copy packaged results elsewhere before reproducing them. Each child is capped below 60 seconds and total below 180 seconds. This is bounded synthetic performance evidence only. Historical corrective scripts/logs are retained to explain all attempts; they are not part of the normal recovery schedule.

The original test used Linux /proc/self/fd and wait4 RSS reporting; other platforms need equivalent measurement support, not raised limits. Fresh extraction verification is `python3 verify_restore_4n.py` after `python3 make_package.py`; it verifies every extracted member, restores history, verifies identities, runs focused tests and CLI recovery. It records the preseal ZIP identity; final package member hashes independently cover the verification report.
