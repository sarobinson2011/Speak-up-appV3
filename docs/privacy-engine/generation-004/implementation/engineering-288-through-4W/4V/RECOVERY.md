# Exact bounded recovery commands

All commands run from an explicit package path and use a new isolated job. They do not change your current directory, touch Speak-up-appV3, or read `.env`. Replace PACKAGE with the actual extracted directory. Python 3.11+ is required (the intended Ubuntu host has 3.12.3).

Small independent complete fixture, including partial-header pause:

```bash
PACKAGE=/home/steve/dev/Engineering-288-execution/Engineering-288-checkpoint-4V
TASK=/home/steve/dev/Engineering-288-execution/adapter-4V-small
python3 -B "$PACKAGE/tools/verify_package.py"
python3 -B "$PACKAGE/cli.py" fixture --directory "$TASK/inputs"
python3 -B "$PACKAGE/cli.py" keygen --key "$TASK/local-execution.key"
python3 -B "$PACKAGE/cli.py" init --job "$TASK/job" --key "$TASK/local-execution.key" --manifest "$TASK/inputs/source.json" --spool-mib 1
python3 -B "$PACKAGE/cli.py" step --job "$TASK/job" --key "$TASK/local-execution.key" --steps 1 --new-bytes 17 --chunk-bytes 3
python3 -B "$PACKAGE/cli.py" status --job "$TASK/job" --key "$TASK/local-execution.key"
python3 -B "$PACKAGE/cli.py" step --job "$TASK/job" --key "$TASK/local-execution.key" --steps 2 --chunk-bytes 7
```

For interruption, close/stop the running controller, then use the **same** step command, job path and key. Never initialize over an existing job or point a textual/binary historical job at this controller. Job status validates identities and inputs; terminal success can be reused as a local receipt without starting workers. It does not reauthenticate a source. If interrupted before initial STATE exists, no stream bytes have been committed: preserve it and initialize a new isolated job.

The foreground bounded driver does not promise survival of terminal closure; durable state survives process interruption. It is safe to restart. Do not run multiple controllers concurrently (exclusive advisory lock enforces one writer, not cryptographic identity). The production detached supervisor and durable aggregate authorization budget are a next bounded integration task, not an implicit full-run command.

Back up only while the controller is stopped: copy `IDENTITY.json`, `STATE.json`, optional `spool.bin`, and keep a protected separate backup of the local key. Restore to the original absolute job path with identical inputs and code/runtime. A missing active spool is regenerated and checked from its bounded cursor. A different host/runtime/path is deliberately incompatible; migration needs explicit review and a new identity strategy, not relabelling receipts. Retain last good backups; never edit STATE by hand. A fully evicted prefix is not recreated during ordinary recovery.

Focused tests and reproducible build:

```bash
python3 -B "$PACKAGE/tests/test_adapter.py"
# Only if the shipped Linux x86_64 binaries fail compatibility:
python3 -B "$PACKAGE/tools/build.py"
```

A rebuild changes executable identity and invalidates old jobs. Build into a separate package copy and start a new job; keep historical packages/checkpoints. Build requires g++ supporting C++17 and OpenSSL 3 development headers/library. No network installation is performed by these commands. Built and tested here: gcc 13.3.0, Linux x86_64, OpenSSL 3; exact output and system-library identities are in results.

Read-only host preflight (does not create a job):

```bash
python3 -B /home/steve/dev/Engineering-288-execution/Engineering-288-checkpoint-4V/tools/preflight.py --target /home/steve/dev/Engineering-288-execution/adapter-4V
```

The package does not include the 382,700,006-byte model or another extracted 236,894,099-byte descriptor. Reuse the exact 4S model, active selected contract, and installed 4T `inputs/links.txt` at their existing paths. `ACTIVE-BINDINGS.json` pins their hashes. For a **later authorized bounded local probe**, `cli.py manifest --model ABSOLUTE_MODEL --contract ABSOLUTE_CONTRACT --descriptor ABSOLUTE_DESCRIPTOR --out NEW_JSON` verifies these inputs and creates only a source manifest. `tools/benchmark.py` accepts the same three input paths plus `--out NEW_RESULT`; it emits/validates one 64 MiB retained prefix and a complete small synthetic stream, never the full universe. Its measurements are not full conformance evidence. Review the full-run preflight before requesting that separate host test.
