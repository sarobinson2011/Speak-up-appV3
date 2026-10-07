# Actual checkpoint 4D results

## Verified inputs

Saved CP4C: SHA-256 `ca4c968c22e738b5e98a4a90c0214bbcbd6d7b44fd9c15acafb8c71cb1dda9f7`, 34,683,510 bytes. ZIP CRC and all 140 manifested member hashes passed. Nested CP4B, CP4A, CP3 and CP2 archive hashes were checked against retained pins; used CP2 members were independently checked against its exact manifest before acquisition. The accepted sources, selected contract and complete CP2 model are unchanged. Their identities are in `SOURCE-INPUT-MANIFEST.json`.

## Executed tests

`results/final-checks/check-results.json`: **153 tests passed, zero failures/errors**, with four passing admission CLI scenarios, in 28.024486 seconds overall. This includes the 120 retained CP4C checks and 33 ledger/construction checks. ACTUAL mode rejects; successful finite cases remain explicitly conditional. All outputs retain `profile_admitted=false` and `actual_qualification_established=false`.

`results/ledger-cases/results.json`: **15 saved ledger scenarios passed** their expected outcomes, plus **two constructor CLI cases** whose output equals the independently authored accepted-form templates. Cases cover both conditional fixture families and ACTUAL rejection, absent source bytes, missing duties, wrong node references, conflicting exact/computational classification, insufficient whole-view interaction coverage, absent qualification, wrong multiplicity, exceeded budget, degenerate NV scope, unavailable assessments and bad-signature precedence. Each saved case pins its exact request and external fixture-contract hashes.

The unit suite also covers each of the eight exact-duty families, missing node/structural/potential coverage, illegal/duplicate/overlapping intervals, duplicate stripe cardinality, exact model/policy/target/coalition joins, external disposition omission, attempted computational waiver of an exact duty, missing classifier/observer/decomposition/NV qualification, missing source decomposition terms, experiment/envelope mismatch, exact repetition-unit/count checks, over-envelope repetition, strict maximum one rejection, meaningful maximum-zero cases, UNION capping at one, unsupported theorems, NV checks with no ARGUMENT, and unqualified ACTUAL outputs. Fifty independently constructed small exhaustive models verify potential-stripe counts without using the production predicate.

The positive GAMMA and DELTA fixtures now cover every node and structural/potential edge in their separate tiny models; their source-owned coverage recipes independently include whole-graph interactions. Qualification is assumed only within the explicitly declared laboratory source contracts. They are not full-model profiles and supply no actual authority.

An initial negative test expected a partial potential count of three after invalid row references. The validator correctly discarded the invalid coverage records and reported zero; the test expectation was corrected to accept only a count at most three, while requiring rejection. The saved preliminary failure log remains in `results/ledger-tests-initial.log`. Subsequent complete runs passed. Intermediate passing logs are retained separately; `final-checks` is the definitive final run.

## Full-model mechanical construction and recheck

The first populated construction completed in **24.759 seconds**, reusing the saved expansion and processing its 18 token and 175 structural source segments. It constructed 4,119 node-class rows and 21,182 structural-template rows, totaling complete correspondence for 426,984 nodes and 4,368,254 structural occurrences. It preserved the exact potential domain of 91,157,453,467 pairs without enumerating it. No full pair or signed-link row stream was generated, read, replayed or hashed.

`results/inventory-source-recheck.json` records independent recomputation of **all 193** segment summaries from pinned source bytes and exact equality of all five populated duty-data files. This took **24.261 seconds** wall time; peak child RSS was **240,660 KiB** (about 235 MiB). That is construction/recheck evidence, not a benchmark of either full stream. Source IDs, provenance and ranges are inspectable in `ledger_data/`, with concrete query examples in `results/node-query.json`, `structural-query.json` and `potential-query.json`.

The node exposure count remains 14,210 CONFIDENTIAL, 6 PUBLIC and 412,768 UNKNOWN. All retained-model privacy dispositions remain NOT-ESTABLISHED. The exact source/qualification failures are saved in `results/actual-ledger-status.json`.

## Recovery

`results/inventory-recovery/results.json`: a fresh construction paused after two committed source segments (exit 3, 1.267 seconds), then resumed to all 193 segments (exit 0, 23.934 seconds). Every populated duty-data file hash matched uninterrupted construction exactly. The existing CP4C supplied-link pause/resume implementation and its tests are retained unchanged; its private journal remains separate from source authentication.

No performance benchmark ran in checkpoint 4D. Benchmark execution was therefore **zero seconds** against the retained ceiling of 60 seconds per benchmark and three minutes aggregate. Construction/verification timings above are actual bounded correctness-run measurements, not full-stream throughput estimates.

## Exact unresolved compatibility result

`results/record-grammar-boundary.json` records three expected rejections: the accepted OBLIGATION template parser, the implemented OBLIGATION parser and the accepted FIELD-LABEL.surface_id primitive all reject the retained literal `$record` identity. This is not hidden as a passed admission check. Its source/model/contract hashes and executable reproducer are provided. It remains an explicit obstacle to full-model V4 record instantiation, in addition to missing governing policy and independent qualification.

## Package recovery check

The first fresh-extraction attempt failed before extraction with `BadZipFile`. Although the packaging command had verified a 41,653,736-byte archive, a subsequent read observed 37,961,843 bytes with a different hash. The cause remains unknown; no still-running construction process was observed. `results/package-first-restore-failure.json` preserves both identities. Packaging now verifies a temporary ZIP, fsyncs it and atomically publishes it. The rebuilt archive passed a fresh temporary-directory extraction, every package member hash, the populated inventory audit, static constructor and conditional collector. See `results/package-restore-smoke.json`. The final deliverable also includes these receipts and receives fresh ZIP/member verification; no full stream was executed.
