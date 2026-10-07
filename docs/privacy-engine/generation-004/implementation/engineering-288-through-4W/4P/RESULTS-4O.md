# Checkpoint4O actual results and limits

The S90 containing-record obstacle is resolved through the source-grounded projection path. The retained READ/null witness now works in an independently constructed, signed conditional fixture without changing standalone BYTES validation. A demonstrated equal-byte standalone-carrier bypass was reproduced and fixed. Actual admission remains disabled.

The final validator passed 390 tests in 203.925 seconds, including 20 projection tests; final refinements additionally exercise empty READ bytes and unavailable containing material. The saved package's fresh extraction reruns all 20 projection tests, 16 CLI commands across E/PRE-EXECUTION/PRE-COMMITMENT, package/input verification and the finite coverage witness. See results/4O-final-regression-tests.log, results/4O-regression-summary.json, results/4O-cli.json and results/4O-fresh-extraction.json. Development logs are retained separately, not promoted over final results.

## Exact parent and dependency reuse

Engineering-288-checkpoint-4N.zip is preserved exactly: SHA-256 `ed47173e3d90a6168d164914553387b854bdb1a7d7b300b470b75486c55ffa82`; all 5,508 manifest members were checked. The affected implementation changes are explicit; 3,111 selected historical/source/model/contract/amendment/backend/byte-law/fixture members remain byte-identical. The accepted full-model identity remains `08d6e7fb1e0cf37cc7effa76b50eaff0459abc158d9c6f0da52c6c58372b14f1`; selected contract `2bbd9d52e1591bc12adc9cc0983c1686ade2cfc4cbcbeb95b6025259d5bf07fc`; canonical backend `3d8b65ea87eb5b5a680c9c51c6897a8c32641f1580947046d1cc6c7f765c152b`. Source/input and implementation manifests record all full identities. No accepted model/contract serialization or identifier decision changed. New test profiles/source materials were regenerated with current exact implementation pins; historical signed fixtures remain historical.

## Bounded computation

PREFLIGHT-4O.md was written before the larger fixture. All throughput attempts total 24.922 seconds, with the longest 8.324 seconds. Every attempt was externally bounded below 60 seconds; cumulative ceiling 180 seconds. The full correctness suite's runtime is separately reported and is not a throughput benchmark. No retained full pair/link stream was processed.

| Final-code measurement | Result |
|---|---|
| Fixture |32 projected token occurrences, both contexts, 16 selected projection forms, 128 required shared dependencies; complete small security/ledger/trace fixture|
| Independent oracle |All 32 exact projected byte strings checked against saved equality-group files; three separate structural/potential sets and exact small serialized link hashes match|
| Construction/signing |0.301 s wall; peak 69,416 KiB RSS (67.8 MiB), separately measured|
| Validation and recovery |8.125 s wall,8.223 s CPU; peak 46,384 KiB RSS (45.3 MiB)|
| Supervisor parent |9,728 KiB peak RSS (9.5 MiB), separately measured|
| Open handles |Peak 36 under RLIMIT_NOFILE=96; before 4 and after 4; private Store roots removed|
| Cache/lifetime |Four pooled indexes per Store; 1 MiB configured SQLite cache; zero resident parsed-value cache; acquisition cache peak 62,021 bytes under 65,536|
| Disk |16,653,312 input bytes;46,353,169 apparent retained work bytes after completion|
| Recovery |Interrupted before ordered-ledger publication, resumed with exact rechecks; 1,152 semantic-index accesses reused, zero canonical document rebuilds in the resumed collection; terminal reuse passed|

Handles are sampled every 2 ms plus at pool opens, so reported peaks are measurements, not continuous proofs. Hard limits and cache bounds are enforced independently. Required graph/model/index memory is separate from bounded caches. Full containing-object/index rehashes after eviction, temporary record-directory reconstruction, exact equality validation and native/authentication prefix reconstruction remain documented recovery costs.

The first benchmark's independent SQLite oracle left one handle open because a connection context manager commits but does not close. The harness was corrected with explicit close and rerun; validator Store cleanup was already correct. The final run returns all handles to baseline. The later no-standalone-carrier enforcement required a fresh signed fixture/job; it was regenerated, not re-pinned by hand. All these runs are counted in 24.922 seconds.

## Independent/adversarial evidence

The exhaustive small oracle validates every S90 schema's fields and complete record, all root/directory framing families, nullable/non-null theorem and assessment cases, reference keys/list ordinals and source-specific event applicability. Integrated fixtures use original V2 signed bytes, canonical pure Ed25519 and the ordered ledger collector. Tests cover wrong binding dimensions/owners/record occurrences, missing/duplicate fields and records, malformed/noncanonical input, unavailability/inapplicability, missing source rules/qualifications, cross-object substitution, snapshot mutation, eviction, exact collision-safe equality, interrupted projection/equality construction, late interruption, repeated resume, journal corruption and terminal reuse in all three phases.

Development failures were accounted for: the original small constructor's field-label list was not lexically sorted once its model exceeded ten classes; sorting fixture labels fixed it without touching accepted data. An early fixture omitted the new projection module from the independent code-pin inventory and was correctly rejected; the constructor was updated. Early unit tests used the wrong source-map/path names; corrected. A slow bytes-only oracle harness took 239.580 seconds and had an arbitrary count-threshold assertion failure; the bounded file-backed harness and exact expected count replaced it. None of these development runs is full conformance evidence. Their logs remain available.

The substantive pre-fix bypass report and exact pre-fix module hash are preserved in results/4O-before-required-projection.json and provenance/4O-before-enforcement. The current regression fixture now rejects that substitution with MISSING-EVIDENCE and no computed budgets. No changes to primitive null grammar or failure precedence were needed.

## Explicit completeness verdict

**First-kernel code completeness for the entire declared finite conditional contract: NOT ESTABLISHED.**596 registered projection classes are implemented. 13 required generated event/acquisition classes still lack a containing-event adapter: ten CP2-RECORD-PARSER and three CP2-REFERENCE-MATERIAL. The finite executable coverage map and rejection witness identify their exact source requirements. This is a concrete remaining implementation gap, not absent qualification disguised as code work. See PROJECTION-COVERAGE-4O.md and NEXT-BOUNDED-TASK.md.

Separately outstanding: required exact serialized full stream identities and retained-scale validation/authentication, final full-model integration witness, actual source/parser/observer/assessor appointments and qualifications, complete actual owning records and qualified guarded directories. No signature, source metadata, laboratory assumption, cache or execution journal establishes those facts. No full stream or actual profile admission is claimed.
