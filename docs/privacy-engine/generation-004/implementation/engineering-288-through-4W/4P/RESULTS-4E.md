# Actual checkpoint 4E results

* CP4D: exact ZIP SHA-256 `59d4f36f3daf2a11fcf1abf50c82ae0e72c53cd0d632614bb2dd751035c08ef1`; 41,657,534 bytes; CRC and all 443 manifested file hashes passed. CP4C→4B→4A→3→2→1 archive identities were separately rechecked. Results are saved under `results/checkpoint-4D-verification.json` and `results/4E-predecessor-identities.json`.
* Final complete regression: **187 tests, zero failures/errors**, plus four inherited admission CLI cases. Elapsed 31.432584 seconds. `results/4E-final-checks/` contains individual timings, requests, outputs and accepted/retained input integrity checks.
* File-acquisition CLI: **6/6 passed**, including connected and disconnected conditional success, actual rejection, missing authority, missing source together with bad signature, and changed file bytes. Each took approximately 0.2 seconds. Exact inputs and outputs are under `results/4E-cli-cases/`.
* Closure oracle: 80 independently generated nine-node graphs, all nine singleton seeds, static plus both occurrence-gate phases: **2,160 exact closure comparisons**. No production scope algorithm was used by the exhaustive oracle. The six-node disconnected signed fixture requires separate two-node component closures and six-node composition. Scoped links also passed arbitrary chunk-size tests.
* Identifier reconciliation: accepted grammar and implementation reject the literal OBLIGATION node reference but accept real incident structural/potential edge references. Selected FIELD-LABEL.surface_id still rejects the literal `$record` surface. Saved exact model/contract/source identities and resolved edge provenance are in `results/identifier-reconciliation.json`.
* Retained complete static model: verified inventory permits an exact arbitrary-hub reachability deduction for all 426,984 nodes. The 91,157,453,467-pair count is retained, not re-enumerated. `results/4E-retained-static-closure.json` explicitly leaves actual source-qualified seed/view evidence and serialized hashes unestablished.
* No performance benchmarks were executed: **0 seconds** of the bounded benchmark allowance. Correctness-test timings are not full conformance or large-stream performance evidence.

## Retained failed attempts and corrections

The first 185-test complete regression had two assertion failures and two errors. A source/bundle digest disagreement prevented the scoped link parser from seeing a malformed terminal frame, changing the earliest collected failure. File/universe validation now runs independently before dependent source assertions. Overly broad suppression also removed established over-budget values when signed PASS result cells disagreed. The corrected collector retains independently computed negative budget evidence, marks the signed-result inconsistency, and still withholds positive conclusions when prerequisites are absent. The initial log/results are preserved in `results/4E-checks-initial/`; the targeted corrected run passed 38 tests, and the subsequent complete 187-test run passed. No accepted failure vocabulary/order or source clauses changed.

4D's historical archive truncation/rebuild and the earlier original-run “Error in input stream” remain recorded in its exact retained ZIP. This checkpoint supplies no new causal explanation for either event. The old cloud run's reported implementation work is not verified evidence.

## Explicit non-results

No expansion rerun, full pair/link generation, full replay/validation, full serialized hash, actual authority appointment, authoritative semantic qualification, profile admission, publication, registry insertion or runtime effect occurred. The full qualified ledger still needs governing inputs. The exact selected FIELD-LABEL identifier incompatibility remains unresolved.

## Fresh package recovery

A fresh temporary-directory extraction passed every delivered member hash, exact predecessor restoration, the unchanged full-model inventory audit and the file-backed disconnected signed fixture (two-node component closures; six-node composition). No original workspace paths or network input were needed. The commands and actual outputs are in `results/4E-package-restore.json`. The final ZIP includes this receipt and is independently rechecked for every member hash and ZIP CRC.
