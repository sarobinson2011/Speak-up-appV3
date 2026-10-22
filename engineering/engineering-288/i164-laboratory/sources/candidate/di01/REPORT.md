# DI-01 correction — return to Engineering-Anchor[2]

Downstream confirmation remains WITHHELD pending independent closure review. This checkpoint corrects the demonstrated live-object validation defect; it does not claim independent closure or full binding.

Verified Formal-Lab-4-I164-candidate-downstream-integration-review.zip: 1,003,890 bytes, 56 unique entries, SHA-256 c232d11f470af63b510873903ac76b05819028475d0ed9b0e36af54db0df4d19. CRC, exact manifest membership and every size/hash passed. Preserve 52 fresh reviewer controls, the two counterexample processes and separate recovery/harness failures. The review's 102 supplied checks were inspected, not rerun by the reviewer. Full original review ZIP is included unchanged.

## Root cause and affected entry points

Old `Candidate.ingest` returned the caller's binding directly. In the supported `c.ingest(e,context,c.binding)` call, output and validator expectation were the same dictionary. Deleting `out['binding']['downstream_adapter']` therefore also deleted it from `c.binding`. `check_binding` inspected only the remaining references and compared the mutated dictionary to itself. `validate_output` re-ingested using that same incomplete binding. This was reference aliasing, not a cached successful verdict.

The returned blockers list was `baseline.BLOCKERS` itself. Clearing it changed every later result's expected blocker list; final binding still rejected but its reason list became empty. A further affected alias was association_index source dictionaries shared with the candidate metadata in memory. The correction detaches the entire returned result, covering those nested sources and model_input references, rather than just the two demonstrated top-level members.

Only `integration/candidate_pipeline.py` changes in the implementation:
- Canonical serialized binding expectations are retained privately as immutable bytes. `binding` returns a fresh parsed view on each access.
- Required blockers are captured as an immutable tuple from the verified actual candidate status artifact.
- Ingestion snapshots the input binding and returns detached nested data, with a fresh blockers list.
- Validation checks basic current-result structure, snapshots the submitted result, verifies its complete binding against independent expectations and exactly compares a freshly derived result. No prior successful validation is a seal or exemption.

API check_binding/ingest/validate_output and CLI binding/ingest/validate use this same path. final_binding retains its unconditional rejection stub. Arbitrary hostile code replacing private attributes or module code is not an in-process isolation guarantee; this correction isolates normal API inputs and returned mutable values. No concurrent mutation or success certificate authorizes a later changed result: it must be validated again.

## Evidence

Original witness script and the two exact review mutants are preserved in the original review ZIP. Both witnesses were freshly reproduced against the unchanged old adapter before editing; own logs, complete mutants and old source are in original/. Those are demonstrated failures, not positive controls.

`check_di01.py` checks the actual returned live object, deep copies, shallow aliases, repeated validation after prior acceptance, missing/nested adapter/runtime/profile/association bindings, removed/altered blockers, context mismatch and status elevation. Both corrected-code mutants are also serialized and rejected by fresh CLI processes; unchanged results survive serialization. Three affected regressions re-ingest saved ordinary, ZK and retry-commit evidence. No signing, runtime interruption, network or lifecycle is executed. Exact completed counts and rejection reasons are in results/checks.json; fresh-process logs and compressed corrected mutants are retained.

No new development/harness failure occurred in this correction unless explicitly recorded as FAILED.*. Previously preserved failures remain unchanged in the input review and predecessor checkpoints.

## Preservation, identities and consequences

All 13 candidate metadata artifacts, runtime and reviewed supporting adapters are unchanged; all 90 historical files and 43 relationships preserved. Only the downstream adapter identity changes. Existing output receipts tied to the old adapter remain historical evidence and are not relabelled; new outputs must bind the corrected adapter. The metadata candidate identity remains d2b76814433f1d3c96bccdb2eaaa6ddb1521cafcd2c616fc1b93d064995a2130. Exact old/new code identities are in IDENTITIES.json and change.diff.

No new fields/classes, wire records, service events, attempts, allowances or policy rules. Returned JSON schema unchanged; detaching copies changes memory ownership, not governing size bounds. Additional transient copying is not an operational memory/storage bound. 101 ordinary / 61 ZK remain structural upper bounds only. Full-domain/external/lifetime/physical storage obligations remain unresolved.

IA-01 closure, scoped SD-01 closure, conditional metadata support and all prior scoped findings preserved. All adopted limits/decisions and 43 inherited relationships unchanged. Canonical registration has not occurred; complete model binding, classifications, appointments, operational custody/rollback resistance and qualification remain unestablished. Retention/compaction unapproved. Original retry ZIP remains unavailable, recovery provenance unchanged. Stream identities UNCOMPUTED; actual admission disabled. See the retained FULL-BINDING.md for unchanged remaining dependencies.
