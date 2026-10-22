# IA-01 response-envelope correction

Return to Engineering-Anchor[2] before independent closure review. Supporting integration was reviewed as **correction required**. This checkpoint implements and locally checks that correction; independent closure is pending. Canonical binding remains blocked. Actual admission remains disabled.

## Verified review and provenance

Formal-Lab-Engineering-288C-I164-option-a-integration-review.zip: 16,408,060 bytes, 148 entries, SHA-256 523a5818cceeace3e46382015110766004e006a285a131ee7b2c49e323bb0e2c. Size, hash, CRC, exact extracted membership and every manifest entry passed freshly. The complete supplied archive remains preserved separately; relevant findings, witness and failed review harness evidence are copied under review/.

Formal-Lab freshly reran 74 supplied integration checks and completed nine independent groups, including IA-01. These are distinct counts. Eleven saved exit boundaries were inspected, not newly executed. Its syntax-error and unavailable-Crypto metadata-probe failures remain separately preserved. IA-01 is a projection-coverage defect, not an authentication bypass or demonstrated candidate accounting/privacy defect. Its review-local F1 filename does not reopen the prior closed HEAD/event F1 finding.

## Minimal correction

Only three existing source files change: code/ingest.py, code/register.py and code/pipeline.py. Candidate runtime, accounting, ownership, signing, limits and retained sources are unchanged. Diffs and before/after identities are included.

The ingester now retains each verified original `{response, signature}` envelope alongside its inner working response. RESPONSE objects emitted for projection are the complete envelope. The existing raw JOURNAL response_hex remains unchanged. No evidence is replaced by a hash or success marker.

The register maps signature to `/signature`; request, challenge, ok and the guarded data/error variants map to `/response/<field>`. Outer record and framing remain explicit. A concrete downstream check requires exactly the emitted RESPONSE objects and all their projected rows, rechecks exact envelope bytes against the journal and authenticated request packet, verifies the signature, and exports selector-to-occurrence joins. Each join contains the field class, supporting node, exact projected occurrence, containing envelope, request-only digest, packet digest and challenge. Digests are associations; the complete original values and bytes remain present.

Pipeline output identity is I164-RETRY3-CORRESPONDENCE-INGESTION-2. The model adapter consumes the corrected register fields and containment occurrences through its existing interfaces. No full model construction was needed. `include_projection=False` still returns validated envelope objects internally and explicitly returns null selector coverage; it does not claim emitted coverage. Normal CLI ingestion uses projection and enforces the coverage check.

## Focused evidence

- Original authentic one-response witness preserved exactly: 24,962 bytes, SHA-256 fecc7de5ed339fc8ccdc597a9675686edb9989e03f8c48344cbac03b7118da2f. Fresh execution against retained old adapter code reproduces zero signature rows; corrected integration produces one exact STRING signature occurrence.
- 56 focused response-envelope checks passed. These include 37 saved-export projection/reopening cases, missing/altered/type-confused envelope data, valid lab signatures with mismatched request/challenge, downstream omitted/type-altered projection rows, wrong associations and register paths, model consumption, unanswered response absence, and synthetic HEAD/BACKUP envelope controls.
- All 74 affected integration regression checks passed freshly. CLI ingestion of the minimal witness matches direct integration byte-for-byte.
- No lifecycle, candidate transaction signing, process-exit, mechanics or boundary suite was rerun. Synthetic HEAD/BACKUP are small parser-only records authenticated with the already public laboratory envelope seeds; they are not runtime execution evidence or production credentials.

One fresh harness attempt failed: the synthetic HEAD request inherited an observer principal from an unordered saved journal row. The adapter correctly rejected ROLE before projection. The failed script, complete result list and log are preserved under results/preserved-harness-failure. The fixture was corrected to the source-required executor principal, then the response checks completed. No implementation guard was weakened.

All 90 available historical candidate files freshly match the preserved inventory. All 43 inherited relationships remain byte-exact. This checks the available retained workspace, not Steve's untransferred live repository. All copied reference hashes match. Prior A/B/C support, HEAD/event F1 closure and scoped nonce/retry support remain preserved, without qualification promotion.

## Remaining blockers

The correction does not close canonical-binding readiness. Missing authoritative inputs remain: latest canonical model/register delta HEAD; qualified visibility, custody and observer views; actual phases/producers and appointments; protected lifetime accounting/shared-ledger, custody and rollback evidence; finite lifetime acquisition/recovery/diagnostic directory; genuine outcome scope/truth/finality and serialization evidence.

Separately unfinished implementation remains: complete static nested/framing declarations in both inherited symbolic contexts, full old/new dependency/equality and actor-reachability closure, consistent full model/profile/procedure/register/ledger binding, and separately authorized stream construction/validation. The final-binding function remains a blocking stub, not a positive implementation awaiting boolean flags.

Accepted semantics, Option A provenance, Pilot001 and limits are unchanged. Decision B remains in force; retention/compaction is unapproved. Original retry ZIP remains unavailable. Changed stream identities remain UNCOMPUTED. Operational assurance, full-domain capacity and qualification remain unestablished.
