# Exact checkpoint 4P commands

Requirements: Python 3.11+, sqlite3, cryptography (fixture signing only), Linux
native validator/backend executables shipped in the package. Retained backend
build kit/version/prerequisites remain in crypto_backend and BACKEND-REVIEW-4G.md.
From a fresh extraction, run in Engineering-288-checkpoint-4P:

```sh
python3 verify_package.py
python3 prepare_retained.py
python3 verify_4p_inputs.py
python3 coverage_4p.py
python3 -m unittest tests.test_generated_events -v
python3 -m unittest discover -s tests -v
python3 run_4p_cli.py
```

prepare_retained restores exact historical packages and executable permissions;
it never expands the retained model or processes a full stream. The historical
4O ZIP and recursive predecessors remain exact input evidence. Active 4P fixtures
are newly signed with current code pins; older fixture code pins are historical
and must not be edited to manufacture compatibility.

Construct an independently signed complete conditional fixture:

```sh
python3 -m fixtures.generated_events work/example --phase PRE-EXECUTION
python3 -m integrated_auth keygen --key work/example.key
python3 -m integrated_auth start --manifest work/example/manifest.json --trusted work/example/trusted.json --checkpoint work/example.job --key work/example.key --new-bytes 1
python3 -m integrated_auth resume --manifest work/example/manifest.json --trusted work/example/trusted.json --checkpoint work/example.job --key work/example.key --new-bytes 67108864 --seconds 50
python3 -m integrated_auth resume --manifest work/example/manifest.json --trusted work/example/trusted.json --checkpoint work/example.job --key work/example.key --seconds 50
```

Exit 3 means paused, 0 conditional completion, 2 rejected. Repeat resume if paused.
Use E or PRE-COMMITMENT for the other phases. Full fixtures are also supplied in
fixtures/4P-E, fixtures/4P-PRE-EXECUTION and fixtures/4P-PRE-COMMITMENT, plus the
bounded larger fixture. Do not move live jobs. Preserve the original source
files, manifest/trusted bytes, key, job, stage/input directories and contained
native/crypto jobs. A CP4O journal must not be reused under changed CP4P code.

Interruption during generated validation rebuilds its scratch event maps and
revalidates from the first required value. Completed exact snapshots/indexes and
native link states are reused under the existing verified scheduler. Authentication
retains exact-prefix rereading; terminal resume still exact-checks all input and
artifact bytes. No timestamp/permission/journal-only identity or qualification.
The new tests inject interruption within event projection and before ledger
publication, then compare every value and scoped stream digest to the independent
uninterrupted oracle. Corruption/mutation rejects rather than producing success.

Only after reading PREFLIGHT-4P.md:

```sh
python3 run_4p_bench.py
```

The supervisor enforces 60-second individual and 180-second aggregate throughput
limits. A fresh benchmark work directory is required. Benchmark evidence is
performance-only. None of these commands processes either full retained stream.
