# Actual checkpoint 4S results

- Canonical candidate construction: PASS; 15.923 seconds; process peak RSS 2,716,952 KiB. Separate candidate size 382,700,006 bytes. Only one scalar changed.
- Full ordered token/descriptor correspondence: PASS for 426,984 tokens; 50 fixed, 18 groups, 1,169 exclusions; token JSONL digest and exact native descriptor match retained evidence.
- Focused metadata tests: 12 passed in 1.081 seconds. Includes exact single edit, malformed/stale bindings, DAG cycle/missing-node rejection and non-admission constraints.
- Existing integrated collector: five focused checks passed in 1.12 seconds. Conditional control succeeds; candidate hash relabeling, rehashed substituted model and stale outer fail; old journal rejects changed inputs. Failure precedence is recorded in results/COLLECTOR-CHECKS.json. 192 retained code/dependency files were verified before use.
- Dependency consistency: PASS; 18-node acyclic plan; 269 copied historical members verified; 199 direct old-model reference files inventoried. Ten reused source/catalog/duty artifacts remain exact. The ledger domain and derivation envelope are candidate-bound.
- Full 4P regressions: reused, not rerun. Exact historical summary and fresh-extraction results included.
- Final ZIP fresh-extraction verification: performed after sealing; the external checkpoint receipt contains the exact ZIP hash and result, avoiding a circular receipt/manifest hash dependency.

No binary regeneration/replay or textual computation was performed. No benchmark was run. Model/metadata hashing is distinct from hashing the retained full pair/link streams. Local receipt integrity is not independent source authentication or qualification. Actual admission remains disabled.
