# Checkpoint 4T — portable static textual identity preparation

Prepared, not executed. Target: `/home/steve/dev/Engineering-288-execution/textual-4T`.

Candidate model: `dd946419e4fd4c657a0a0d663b145e958ddf3c4957bf006b94b5c3f7ec96e74d`.
Active finite contract: `2bbd9d52e1591bc12adc9cc0983c1686ade2cfc4cbcbeb95b6025259d5bf07fc`.
Historical binary completion remains preserved and is not rerun or imported as textual recovery state.

The package includes only required executable/source dependencies, the exact 236,894,099-byte token/structural descriptor, a 6,831,760-byte analytical prefix table, small tests and exact references to retained large inputs. The 382.7 MB candidate model and nested archive chain are not duplicated. Native worker/controller hashes are unchanged from 4A. Native Ubuntu Linux x86_64 compatibility requires GLIBC_2.38, GLIBCXX_3.4.32 and OPENSSL_3.0.0; the read-only host command checks the actual loader/libraries and a tiny independent oracle.

Expected complete text stream: **91,161,821,721 rows**, **19,909,380,154,846 bytes**, including the 67-byte header. This is an analytical exact size, not an executed hash. It contains 91,157,453,467 potential rows plus 4,368,254 unique structural rows. Structural raw and unique counts are equal for the retained model. No 19.91 TB TSV is written.

Read `LOCAL-COMMANDS.md` in order: read-only preflight, optional bounded local throughput probe, then a separately authorized detached execution. A new run requires literal `--authorize-review-hours 48`. This is a proposed textual budget; binary authorization and its two-hour budget have no effect here. No full computation starts during package inspection or installation.

Default segments cover 64 lexical from-token ranks (6,672 segments per pass). The same job can use 32 or 16 for later generation segments without discarding completed records. Every boundary is independently checked against exact expected rows/bytes/first ordinal. Replay uses the exact committed generation intervals; it is explicitly the same generator. Shrinking future generation cannot split an already committed replay interval. If a saved interval persistently cannot replay within the native time cap, stop for a focused replay-controller remedy while preserving all existing progress.

`launch.py` detaches from the terminal, writes durable progress and logs, and prints the PID. Closing a terminal does not stop this process. Ordinary pause or interruption preserves completed segments. See `RECOVERY.md` for power loss, failed segments, snapshots and review-budget extension. Never delete a job to resume it.

Actual admission remains disabled. Text identity, independent supplied-file validation, exact four-file/pure-Ed25519 authentication, final full-model integration and independent qualification remain separate obligations.

## Reproducible bounded developer checks

Use a disposable extraction: `python3 -B /absolute/kit/tests/check_package.py` runs the 17 small tests; `python3 -B /absolute/kit/tests/check_host.py /absolute/Engineering-288-checkpoint-4T.zip` runs the six host/installer tests with explicit positive-capacity fixtures. Neither starts a full job. Tests update their results files, so do not treat that modified extraction as the original sealed kit; use a fresh extraction for actual execution. `python3 -B /absolute/kit/tools/verify.py` is read-only. The metadata proof can be reconstructed in another output directory using `tools/check_descriptor.py --model /absolute/4S/candidate/model.json --output /absolute/disposable-output`; it processes model/descriptor metadata only and requires about 3 GiB available memory, not the full TSV. No such reconstruction is needed for local execution.
