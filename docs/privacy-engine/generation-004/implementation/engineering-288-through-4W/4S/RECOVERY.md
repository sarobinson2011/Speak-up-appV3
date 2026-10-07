# Reproduce and recover checkpoint 4S

Python 3.12 standard library suffices for model/metadata verification and reconstruction. Kernel collector checks additionally use the exact retained 4P runtime dependencies and canonical native backend. No installation or full computation is triggered by these commands.

After extracting the ZIP into a fresh directory (do not overlay a predecessor), replace `/absolute/path/Engineering-288-checkpoint-4S` below with that directory. No command changes your working directory or accesses `.env` or Speak-up-appV3.

```bash
python3 /absolute/path/Engineering-288-checkpoint-4S/tools/verify_checkpoint.py
python3 /absolute/path/Engineering-288-checkpoint-4S/tools/check_metadata.py
```

The first command validates delivered hashes, exact historical membership, the one-field model edit, candidate joins, the contract/source bindings and the acyclic dependency graph. It only reads model/metadata/package bytes. The second uses small adversarial metadata tests and does not invoke a native stream engine.

For reconstruction in a disposable copy of the extracted 4S directory:

```bash
python3 /absolute/path/Engineering-288-checkpoint-4S/tools/construct_candidate.py
python3 /absolute/path/Engineering-288-checkpoint-4S/tools/rebind_metadata.py
```

Construction uses one complete model in memory (measured peak 2,716,952 KiB, about 2.59 GiB; provision at least 4 GiB available RAM). Candidate and old model together occupy 765,399,950 bytes. Allow 2 GiB task disk for a single extracted 4S copy and reconstruction temporary outputs, or 4 GiB if keeping both ZIP and a second verification extraction. Construction completed in about 16 seconds here; host speeds vary. It writes candidate outputs through `.part` plus fsync/rename, never historical inputs. After interruption, remove only candidate `.part` files and rerun construction from the pinned historical model. There is no expensive partial-state migration to preserve. Regenerated operational timing/result files differ from the delivered manifest; use a disposable copy and compare deterministic candidate/model and binding outputs. To recover the exact delivered checkpoint, extract the original ZIP afresh and verify its manifest instead.

The included exact 4Q ZIP contains the exact 4P ZIP. Restore 4P to a fresh directory using `tools/restore_kernel.py --destination /absolute/fresh/directory`; then the optional focused check is:

```bash
python3 /absolute/path/Engineering-288-checkpoint-4S/tools/check_collector.py --kernel /absolute/fresh/directory/Engineering-288-checkpoint-4P --output /absolute/new-output.json
```

This runs five small binding/recovery checks, not the historical regression suite. It must never be pointed at a full-stream execution job. The preserved 4R completed journal belongs to its original provisional-model job only. It is not resumed, rewritten or adopted into 4S.

SHA checks establish local byte integrity, not source authentication or qualification. The package manifest is not a self-authenticating authority statement. Use the delivered external ZIP receipt/hash to anchor retrieval.

Optional restoration of all 4P historical files needs another 1,543,123,034 bytes of extracted payload plus a temporary 463,062,439-byte archive. Reserve 6 GiB free for combined 4S ZIP/extraction, optional 4P restoration, temporary archive and working checks. No model/stream expansion is performed by restoration.
