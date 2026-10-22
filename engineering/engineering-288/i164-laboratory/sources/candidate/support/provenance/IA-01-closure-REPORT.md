# IA-01 closure review

**IA-01 is closed within the authenticated saved-export supporting integration path.** No remaining defect in the corrected envelope/signature correspondence was demonstrated. This is a noncanonical AI laboratory review, not appointed assessor qualification. Return to Engineering-Anchor[2] before further implementation. Canonical binding remains **BLOCKED** and actual admission remains **false**.

## Verified input and comparison

The supplied correction ZIP is exactly 3,213,216 bytes, 139 unique entries, SHA-256 `8217415cbe9b296485f7abc1af00badc49bf960d346c725c7d1a2bc9f54545f1`. CRC, safe paths, exact membership and all 138 covered manifest file sizes/digests passed. The archive has a top-level directory; the input/ copy removes only that directory prefix. Its file bytes match the archive. Source identities are in SOURCE-IDENTITIES.json; verification commands and receipts are included.

The three changed source files match both reported before/after identities. The preserved old files reproduce the predecessor. Forty shared reference/helper files, including correspondence.py, model_adapter.py, the adopted Option A decision, runtime, accounting and ownership code, are byte-identical to the verified predecessor input. New test code does not change the candidate runtime.

The original one-response witness remains exactly 24,962 bytes, SHA-256 `fecc7de5ed339fc8ccdc597a9675686edb9989e03f8c48344cbac03b7118da2f`. It contains an authentic saved response, not a regenerated replacement. The fresh supplied witness execution reports zero parsed signature occurrences with the preserved predecessor and one exact STRING signature occurrence with the correction. The minimal projection grows from 484 to 488 rows. Its complete corrected pipeline output is 1,033,275 bytes. The original omission and prior failed harness evidence remain preserved under input/review/.

## Requirement and implementation correspondence

| Owning source | Reviewed change and evidence |
|---|---|
| reference/CORRESPONDENCE.md, “Exact identity and nested correspondence”, item 6 | Keeps request-only digest distinct from complete-packet digest. Original `{response,signature}` envelope is retained; response binds request, challenge, BOOLEAN ok and guarded data/error. |
| reference/FIELD-CORRESPONDENCE.csv, RESPONSE.signature | register.py build_register maps signature to `/signature`; signed fields map under `/response/`. Source class and original field selector remain unchanged. |
| reference/INTEGRATION-SPEC.md steps 2–3 and exact-source/type/occurrence validation criteria | ingest.py validate_export authenticates original canonical bytes, preserves outer wrapper, and emits explicit response_links. Generic project walks exact nested containers, keys and values. |
| reference/runtime/authority.py handle (lines 98–121) and Scheduler.call (254–255) | Original server construction signs the inner response and returns the outer envelope. The parser retains that same structure. No digest-signing replacement is introduced. |
| code/register.py validate_response_projection | Rechecks server signature, complete envelope bytes against JOURNAL, request-only and packet digests, challenge and actual exact projected rows; requires selected field pointers and exports occurrence joins. |
| code/pipeline.py integrate; code/model_adapter.py declarations and occurrence_relations | Normal integration validates real emitted rows before returning. Model declarations retain mapped fields; containment edges retain envelope/key/value parents. Final binding still refuses. |

Each answered response contributes five explicit field-selector joins: request, challenge, ok, signature, and exactly one of data/error. Recursive projection additionally retains wrapper/framing/nested data and key occurrences. The joins reference the real signature and containing envelope occurrences; digests associate records without replacing exact values. The fresh seven-response example has 4,533 rows and 4,410,958 output bytes, matching Engineering's recorded result. These are example measurements, not maximum capacity bounds. The supporting register remains 424 checklist rows in 41 families; this is not the full instantiated surface universe.

The normal trusted pipeline constructs the objects and links from validated exports; its downstream helper is not an independent admission interface for arbitrary caller-edited internal objects or arbitrary serialized model outputs. With include_projection=False it does not emit an occurrence directory and explicitly returns null response-selector coverage. That mode cannot establish projection coverage. Missing journal responses are valid unanswered records, preserve uncertainty, and yield no manufactured RESPONSE/signature. Missing required fields inside a present envelope reject.

## Fresh and reused evidence

Fresh executions were confined to offline parsing, validation, small synthetic fixtures and local read-only acquisition. No candidate scheduler, transaction signing, lifecycle, native worker, network transaction or process-exit suite ran.

- **56 supplied focused checks passed freshly** in a disposable input copy. Their complete result details match the saved 56-check list. These include 37 saved export re-ingestions, original old/new witness, authenticated response variants, negative envelope/association/projection cases, and synthetic HEAD/BACKUP parser fixtures. Reading saved exit snapshots is not freshly exercising those candidate exits.
- **25 independently constructed checks passed freshly**, recorded one by one in evidence/run-1.stdout. They cover exact wrapper/signature/field joins; seven malformed signature types; authentic but type-invalid ok/request/challenge; signed nested integer-to-float substitution; signed error with exact Unicode content and preserved committed state; duplicate/missing/wrong-parent/altered-byte downstream rows; two authentic responses swapped between requests; duplicate JSON keys; model-path substitution; two cold SQLite opens; two saved interruption snapshots; and final-binding refusal despite positive caller flags.
- The two cold opens reconstruct only the minimal saved fixture in isolated SQLite files, close them, acquire via the normal immutable read-only interface and compare the full integration output byte-for-byte. Both databases remain byte-identical. This demonstrates local re-ingestion correspondence, not operational recovery durability or protected rollback resistance.
- **74 integration regressions were inspected as saved evidence**, including their source, result list and log. They were not rerun in this review. Unchanged mechanics and prior A/B/C, HEAD/event F1, nonce-ownership and retry support are reused within their original scopes.

Recorded wall times: supplied focused checker 11.264 seconds; independent controls 1.841 seconds. The Python harness's cumulative child peak RSS was 58,640 KiB and then 65,600 KiB. These are cumulative process-resource measurements, not separately sampled parent/native-worker peaks; no native workers were launched. Each subprocess had a 45-second timeout. Exact commands and actual stderr/stdout are in evidence/commands.json and run-* files.

The supplied failed synthetic HEAD attempt is preserved: an observer principal was inherited where executor was required, and ROLE correctly rejected. The corrected supplied fixture uses the required executor principal. Fresh review intake-harness failures are also preserved: an initial root-prefix lookup KeyError, then a text-edit SyntaxError before execution. Only review harness code was corrected; the final verification passed. Neither failure is candidate defect evidence. No experiment result was overwritten in the immutable input copy.

## Preservation and limits

All 90 historical inventory entries were freshly matched to actual file bytes in the verified retained prospective-retries review archive. All included reference/runtime copies are unchanged against the predecessor. All 43 inherited relationships remain byte-exact, SHA-256 `761772d3372c13cce1c61a551154534cc7d23ea32fc97a18db0794bbfdd27591`.

The compact correction input does **not** contain a second complete current 90-file tree. Engineering's assertion about its retained workspace is therefore supported here by the identical inventory, historical bytes and included unchanged copies; it is not an independent attestation of an untransferred live repository. No mutable remote state was inspected.

Protected quiescent database acquisition, authoritative expected HEAD, trusted code/runtime, shared-ledger coverage, key custody and non-rollback storage remain assumptions/assurance obligations. Public laboratory envelope signing only constructs negative and parser fixtures; it supplies no operational credentials, qualification or genuine outcome evidence. No authentication bypass, privacy failure or accepted-definition defect is claimed.

## Canonical binding remains separate

| Missing authoritative input | Owning role / dependent step |
|---|---|
| Current canonical model/register delta HEAD | SU-Engineering, under Steve's authority; exact baseline reconciliation and final identity allocation/binding. |
| Source-qualified seven-role visibility/custody and complete observer views | Owning source producers and scoped assessors; classifications and full privacy/model arguments. |
| Actual owning phase producers, appointments and qualification | Canonical appointing authority and actual gate/evidence producers; phase-specific qualified evidence. |
| Protected lifetime accounting, complete shared ledger, custody and rollback evidence | Executor, signer, storage/accounting owners and assessors; operational freshness and authorization conservation. |
| Finite lifetime acquisition/recovery/diagnostic directory | Runtime/model producers and qualifiers; complete bounded occurrence and retained-byte coverage. |
| Genuine external outcome scope, truth, finality and serialization bounds | Appointed external evidence providers/observers and assessors; qualified C4 disposition under Decision B. |

Separate unfinished implementation remains: complete static nested/framing declarations in both symbolic contexts; full old/new dependency, potential-equality and actor-reachability closure; consistent model/profile/procedure/register/ledger binding; and separately authorized construction/validation of changed streams. The final-binding implementation is a blocking stub, not a positive binding path that can be completed by supplying boolean flags.

The smallest next substantive task is to pin the exact current canonical model/register delta HEAD through Engineering-Anchor[2] and document reconciliation with this supporting delta, keeping every unresolved source classification explicit. That task does not authorize full model construction or supply missing qualifications.

Option A, accepted semantics and limits remain unchanged. The 101 ordinary / 61 ZK figures remain structural upper bounds, not demonstrated maximum paths or full-domain capacity; the 102 cap is unchanged. Full C5 capacity and prior operational obligations remain open. Decision B remains in force. Retention/compaction and migration remain unapproved; changed stream identities remain **UNCOMPUTED**. Pilot001 and historical artifacts remain unchanged. Actual admission remains disabled.
