# Engineering 288 — checkpoint 4V

**PASS for bounded conditional adapter implementation and preflight.** Actual admission remains disabled. Full retained independent validation has not run.

Implemented and tested:

- Actual deterministic laboratory TSV bytes → bounded durable spool → unchanged retained independent row validator.
- Exact framing, membership, orientation, lexical uniqueness, global ordinals, separate structural/potential completeness and cumulative whole-byte SHA-256.
- Durable parser/SHA/emitter state, atomic publication, bounded spool regeneration/eviction, strict input/code/runtime/job identity checks.
- Independent complete small oracles, 18 malformed-stream variants, interruptions, worker death, corruption, substitution, mutation and terminal reuse.
- Complete synthetic 384-token / 73,536-row case and bounded retained-model prefix; no full retained stream.

Read `ADAPTER-REVIEW.md` for the explicit trusted-local-execution boundary and source clauses. Read `RECOVERY.md` for exact commands. `FULL-VALIDATION-PREFLIGHT.md` separates validator measurements from generation, storage peak from cumulative writes, and ordinary recovery from Ed25519 prefix reconstruction. Machine-readable results are in `results/`.

`evidence/Engineering-288-checkpoint-4U.zip` is the exact retained parent. The unchanged model, selected contract and descriptor are referenced by exact hashes in `ACTIVE-BINDINGS.json`; large input extraction is not duplicated. All other current package files are hashed in `PACKAGE-MANIFEST.json`.

Use standard `unzip`, which restores the executable bits on the two native binaries. If another extractor loses them, after checking the package manifest, restore execution permission only on `native/emitter_service` and `native/validator_service`. Never edit or relocate a live job to bypass identity checks.

Success here is conditional mechanical implementation evidence. Source appointments, four-file authentication, full-model integration, production inputs, semantic/mechanism qualification, and admission are not established. See `COMPLETION-CHECKLIST-4V.md` and `NEXT-BOUNDED-TASK.md`.
