# Exact recovery commands

From the extracted Engineering-288-checkpoint-4H directory (Python 3.12, Linux x86-64; retained binary/build prerequisites in crypto_backend):

```sh
python verify_package.py
python prepare_retained.py
python -m fixtures.integrated work/example --family GAMMA
python -m integrated_auth keygen --key work/local-journal.key
python -m integrated_auth start --manifest work/example/manifest.json --trusted work/example/trusted.json --checkpoint work/collector.json --key work/local-journal.key --new-bytes 83 --chunk-bytes 17 --seconds 50
python -m integrated_auth resume --manifest work/example/manifest.json --trusted work/example/trusted.json --checkpoint work/collector.json --key work/local-journal.key --new-bytes 10000000 --chunk-bytes 65536 --seconds 50
python -m integrated_auth resume --manifest work/example/manifest.json --trusted work/example/trusted.json --checkpoint work/collector.json --key work/local-journal.key --new-bytes 10000000 --seconds 50
python run_4h_cli.py
python run_checks.py --output work/repeated-tests
```

Exit 3 is paused/interrupted, 2 rejected, 0 conditional checks passed only. Key generation creates an owner-only local 32-byte journal key; never use it as a protocol key. Preserve the entire input directory, its exact manifest, independently acquired trusted contract, journal key, collector receipt and every `.bytes`/`.crypto` journal together. Signed fixture private keys are public deterministic laboratory keys, not actual authority keys.

Collector binding includes exact manifest and trusted-contract byte SHA-256, absolute paths, all Python implementation identities in the acquisition/semantic/ledger/crypto path, accepted schema identity and pinned backend binary/build/source identities. Manifests bind exact source/material/outer/security/model/contract and four-file identities. Source objects are read and hashed anew when consumed. Jobs must join the actual source-owned model and evidence contract; metadata never proves that join.

Four-file and pure-crypto stages retain CP4F/4G journals. Every resume rechecks each consumed prefix; pure Ed25519 reconstructs SHA-512(R||A||M) by rereading the original message from byte zero. The collector's token/link stages retain offset and exact consumed-prefix SHA-256. Each invocation rebuilds parser pending bytes, row ordinal, strict previous four-cell ordering and separate counts by replaying every byte up to that offset. It then advances by the requested byte budget. There is no concatenated-segment-hash substitution and no signature over a digest.

Read-ahead: only bytes actually fed to the token/link parser enter the saved offset/digest. An unread tail in the current chunk is discarded at pause. On resume it is read from the original file. EOF and the whole-file expected digest must be observed before completion. Partial input never supplies a complete-stream digest. Atomic collector and stage writes use temporary file, fsync, replace, directory fsync; incomplete temporary files are not receipts. A pre-replace interruption retains the prior commit; a post-replace interruption leaves the new valid commit. Generated acquisition jobs are also installed atomically. Wrong key, corruption, changed contract/model/key/signature/code/path or substituted scope receipts reject.

Completed receipts are reverified, not accepted as source authentication. The ordered collector is rerun on every invocation and recomputes source closure, correspondence, qualifications, ledger prerequisites, dispositions, budgets and signed result consistency. Independent discoverable failures are collected even if another stage fails. PAUSED returns no positive bindings; its current failure list is preliminary because unread suffixes can contain earlier-precedence failures. On completion the complete collected ORDER determines the earliest failure. A terminal rejection is never “repaired” by retaining a prior PASS flag.

Inputs must remain quiescent throughout a run; exact consumed hashes, size and mutation checks detect changes. Timestamps alone are never identity evidence. This is not an adversarial filesystem snapshot service. For hostile concurrent writers, supply an immutable snapshot and protect the local execution/key boundary. No claim of source authority follows from a trusted local journal.

Recovery cost is explicit: the crypto stage needs the entire consumed signed-message prefix again; CP4F may read four-file prefixes twice to reconstruct file/object hashing. Token/link recovery also replays its prefix with full semantic validation. Repeated tiny increments can cause quadratic total work. The `seconds` budget is cooperative; use an external supervisor (for example `timeout 60s`) for a hard wall-clock limit. A replay exceeding its budget leaves the prior usable checkpoint and cannot advance until given an adequate explicitly estimated budget. This makes the current replay strategy unsuitable as the final recovery plan for a roughly 19.91 TB supplied stream. Do not launch that run from these example commands.

If interrupted before the collector's first commit exists, use `start` again with the same manifest, trusted contract, key and checkpoint path. Any already committed byte/crypto substage is discovered and resumed with its exact binding checks. Once the collector receipt exists, use `resume`. Do not edit a rejected receipt to force success; correct independently acquired inputs under a new job/checkpoint identity.
