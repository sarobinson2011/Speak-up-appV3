# SD-01 bounded correction checkpoint

**Correction implemented and locally supported; independent closure review is pending.** Return to Engineering-Anchor[2] before that review. This checkpoint does not grant canonical registration, qualification or actual admission.

The controlling review archive was verified at 14,147,242 bytes, 205 entries and SHA-256 `748d91a396bfc94fe6ce5b367d17241d464541c96df72bb6805257dccbc2c300`. CRC, safe paths, exact member membership and every covered hash/size passed. Its original report, findings, source identities, receipt, old checker and minimal witness are preserved under preserved-review/. The complete supplied review archive remains retained separately and is not nested in this compact checkpoint.

## What changed

Only one existing module changes: code/static_declarations.py now calls independent source-obligation checks before accepting a catalogue and after emitting rows. New code/response_obligations.py reads the pinned runtime authority/accounting source ASTs directly. It never executes those runtime modules and never obtains its expected response catalogue from schemas(), BODIES, the 424-row checklist, generated declarations or saved examples.

The extractor enumerates apply's admitted method predicates, the saved-HEAD fall-through, explicit early return dictionaries, handle's separate sign/apply dispatch and both sign return paths. Actual response constructors determine success/error envelope keys and signature association. Concrete source constructors establish the returned HEAD closure: counters, partitions, resources, retired entries, stage, pending, last, query and transport members. Local binding aliases map those source objects to the existing record-family names. These aliases and simple expression/type adapters are explicitly bounded to the two supported exact source identities; they are not an inference engine for arbitrary Python. A changed source identity or unsupported source shape stops construction instead of silently guessing support.

The checker requires exact agreement between those source-derived obligations and the proposed response catalogue, including all ten admitted successful request methods, response/error discriminators, returned record fields/types and the existing optional-state guards. Request method/body membership is checked against defining exact-body calls. An omission from schemas() and its regenerated expected bundle can no longer pass merely because both agree.

A separate row check walks the source-derived obligations. It checks expected field/variant rows, parent joins, guards and optional-presence metadata. Framing member names come from framing_templates.py's present/absent constructors, independently of the generator's framing loop; all required framing rows, types and parents must be emitted. The source obligation map and exact source anchors are exported in the new bundle and results/source-response-obligations.json.

Existing declaration types and refinements remain unchanged. Semantic conditions such as release=false, recovered signing state, exact authentication, history and accounting still belong to the unchanged semantic fold before template validation. The source map records signing alternatives and their constructor guards; it does not replace that semantic validation with mere type checks.

All 9,339 pre-existing template rows remain byte-equivalent as data, across the same 59 families. Context slots and the original constructor inventory are unchanged. The bundle identity changes because it now includes independently checked source obligations and coverage evidence. No template count is used as a completeness criterion. No adopted policy, serialization, candidate runtime, allowance or limit changes.

## Original defect and correction evidence

preserved-review/SD-01-minimal.json remains 4,103 bytes, SHA-256 `0b24589fc1be5bcc63b1d1ef6c53af320b478c1a4d1f1b7d312cc7c2b0352c3d`. It contains one signed head response with no events/blobs/owners.

Fresh checks against the preserved old checker reproduce acceptance of the incomplete 9,328-template catalogue followed by rejection of that source-admitted response. Against the correction, the same in-memory head omission rejects during build with SOURCE-RESPONSE-COVERAGE:SUCCESS-RESPONSE. The unchanged complete catalogue accepts the original witness. No source file was edited by these mutation tests.

The same mechanism was exercised for all ten successful response methods; every field in the outer, success, error, signed, release and retry-release response families; selected nested returned-state fields; wrong types/return bindings; error-branch and discriminator omissions; the frozen-result guard; request method/body omissions; all ten framing members; and emitted variant guard/parent/type substitution.

## Fresh checks versus retained evidence

- **109 focused SD-01 checks passed**, including the old witness, omission controls, 38 saved valid exports and narrow IA-01/reopening compatibility controls.
- **67 affected static checks passed**, with results identical to the predecessor's complete result list where compared.
- **Six semantic reconciliation controls passed**. Reconciliation code remains byte-identical; these controls preserve the prior conditional mechanics support.
- The **424-link checklist checker** and its original independent constructor-omission control passed.
- **Three additional positive checks passed**: retained synthetic HEAD/BACKUP parser fixtures and NULL-versus-absent framing. These fixtures came byte-exact from the verified IA-01 predecessor package; they are not new lifecycle evidence.

Timed runs took 37.866, 26.520, 0.062 and 0.499 seconds, each under a 60-second subprocess timeout. Cumulative child peak RSS was 103,564 KiB. No native workers ran; parent memory was not separately sampled. The three additional positive checks were executed separately without a new timing measurement. Exact commands, result lists, stdout and stderr are retained.

Three development attempts failed before a new bundle was emitted: incorrect use of AST Dict.values as a callable; an unrecognized SHA string local reservation; and an unrecognized hexdigest return. Failed module versions and concise error records remain under results/failures/. Only bounded AST adapter handling was corrected; no candidate guard or fixture was weakened. Original review and predecessor failures remain preserved separately.

## Preservation and remaining boundaries

Every existing reference, fixture, provenance and adapter file checked remains unchanged except static_declarations.py. All 90 historical inventory entries were verified against the actual retained historical review archive bytes. All 43 inherited relationships remain byte-exact. This is historical-byte/included-copy verification, not an attestation of an untransferred complete current repository. The compact checkpoint retains the inventories and verification receipt, rather than duplicating that full historical tree.

IA-01 remains supported within its reviewed authenticated saved-export integration path. The normal occurrence projection and selector associations match the unchanged adapter for ordinary/ZK examples and a saved signature-commit cut; repeated re-ingestion is identical. No lifecycle, process-exit suite, transaction, operational signing or full model/stream ran. Pilot001 remains unchanged.

Scope is limited to the pinned authority response dispatch, response/envelope field variants and reachable returned HEAD record closure plus associated framing. It does not establish independently derived completeness for every unrelated family, arbitrary future source revision, complete symbolic expansion or full old/new graph closure. Local expression/type adapters are implementation review obligations, not appointed source qualification. Historical context names remain known; their current canonical binding remains unavailable. UNKNOWN classifications and lifetime multiplicities remain explicit.

Actual canonical reconciliation remains blocked by the authoritative current baseline/HEAD, complete ordered delta chain, current context binding and traceable native-to-interchange inputs described in UNRESOLVED.md. Conditional reconciliation mechanics support is preserved; this correction supplies no canonical authority or missing input.

Accepted semantics, Option A, Decision B, prior A/B/C support, HEAD/event F1 closure, conditional nonce/retry support and adopted limits remain unchanged. Retention/compaction and migration remain unapproved. Broader capacity, source evidence, custody/rollback and qualification obligations remain open. Changed stream identities are UNCOMPUTED; actual admission remains disabled.

The next task is the narrow independent SD-01 closure review in CLOSURE-REVIEW-HANDOVER.md. No further implementation is authorized by this checkpoint itself.
