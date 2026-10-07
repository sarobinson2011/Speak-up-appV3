# Checkpoint 4M results

The demonstrated 4L metadata-catalog capacity blocker is resolved. Executable directories and scheduler maps are disk backed without raising the 16 MiB carrier or 1 MiB receipt caps. Accepted definitions, active 4I amendment, selected contract/model bytes, equality predicate, crypto backend and failure ordering remain unchanged. The exact 4L ZIP and 1,858 selected historical source/model/backend/fixture members verify against their retained hashes.

## Complete metadata size check (not full conformance)

| Operation | Measured wall time | Child peak RSS |
|---|---:|---:|
| Construct all 426,984 retained-token metadata references | 18.162 s | 16,732 KiB |
| Final complete directory acquisition/validation | 26.082 s | 16,060 KiB |
| Final complete scheduler-map snapshot/reopen/compare | 5.823 s | 18,744 KiB |

Parent supervisor peak RSS: 9,600 KiB. All six benchmark attempts combined: **87.606 seconds**, longest 26.082 seconds, within 60 seconds per benchmark and 180 seconds aggregate. Peak child memory is measured separately from the parent; no signing process is involved in this metadata-only experiment. The small integration fixtures are independently signed.

18 retained token shards were byte-verified, covering exactly 426,984 required IDs. Canonical source-file/reference directories total 252,775,296 bytes. Their complete indexed sets were checked by exact legal membership/ownership/reference correspondence, uniqueness and complete required cardinality. Both scheduler input/prerequisite catalogs have 426,984 entries, re-opened and compared completely. The final receipt is 9,761 bytes. Development work tree, including prior immutable generations/oracles, uses 1,340,601,323 bytes. Exact individual identities/counts are in `results/4M-metadata-*.json`.

These references are deliberately synthetic and their value files are unavailable. This proves metadata capacity/completeness, not actual value acquisition, source authentication, executed large prerequisite stages, qualification or a complete model witness. No full pair/link stream was generated, consumed or hashed.

## Tests and development findings

**353 tests passed, four admission CLI checks passed, and 19 catalog/recovery CLI commands passed.** Fresh extraction passed all five steps in 21.964 seconds, including 17 new tests and 19 recovery commands. Final unit/CLI results and timings are in `results/checks-4M-sealed/check-results.json` and `results/4M-cli.json`. New tests cover canonical framing; missing/duplicate/conflicting/extra rows; exact header/owner/source/reference joins; corrupt databases/checkpoints; cross-job and prerequisite substitution; controlled and interrupted publication; repeated resumes; three phases; exact independently signed small oracle results; terminal reuse; and changed inputs. Retained equality, native recovery, crypto, ledger and ordered-failure regressions are included.

Two larger scheduler attempts failed an assertion after 6.174 and 6.226 seconds: the first published input map was empty despite 426,984 committed input/prerequisite rows. Small live-cursor reproductions did not identify the underlying cause. The final implementation uses SQLite's established snapshot/backup API for disk-to-disk publication plus mandatory copied-count checking. The corrected large run passed, as do independent small exact-content tests. The earlier failure cause is not claimed conclusively diagnosed. Both failed attempts remain in the aggregate benchmark budget and retained logs.

Early recovery regressions found (and corrected) a raw KeyError on a corrupt main-journal envelope and unnecessary pre-scheduler reparsing of trusted data for inline historical carriers. The first full regression had 353 passing tests and four passing CLI checks, but its input-set stability gate failed because the exact verified 4L parent ZIP was added to the retained directory during that run. No test failure was hidden. The final sealed regression repeats the gate with the input set fixed. Earlier logs are retained as development evidence.

A separate bounded witness demonstrates the remaining semantic-document connection lifetime boundary: 92 small documents completed under a 96-descriptor process limit, then acquisition failed. See `results/4M-semantic-handle-boundary.json`; do not mistake successful metadata catalogs for bounded many-document semantic acquisition.

Fresh extraction checks are recorded in `results/4M-fresh-extraction.json`. It validates the preseal ZIP manifest, restores exact historical dependencies, verifies source identities and executes the new catalog tests and CLI recovery checks. The final ZIP adds the restore report/status only; the final sealer independently verifies every member's size/hash and ZIP CRC.

Actual admission and authoritative qualification remain disabled/unestablished. First-kernel code completeness is not claimed. See COMPLETION-CHECKLIST-4M.md for two remaining code tasks, separate full-stream/final-witness execution and missing authoritative inputs.

One initial restore invocation preceded completion of the atomic ZIP publish and found no ZIP. It did not inspect a partial archive. The recorded successful restore ran after publication; the premature attempt log is retained.
