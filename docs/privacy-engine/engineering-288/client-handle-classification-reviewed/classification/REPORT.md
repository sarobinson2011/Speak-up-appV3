# Bounded interpretation and correction

`outside_catch_failure` now means exactly: **the terminal modeled outcome is an unexpected `raise` at a stage outside the dynamically protected region of `_dispatch`'s own `except BaseException` catch.** It is a conditional source-model predicate, never runtime exception or unwind evidence. “Unexpected” distinguishes the input stage outcome `raise` from ordinary execution of the source-defined `_fail`, whose intended action is itself to raise `ClientFailure`.

The separate `outcome_classification` gives the terminal modeled kind, exact defining source anchor, catch-relative location, conditional catch protection and whether the terminal outcome models a Python exception. Runtime Python exception/unwind evidence is always UNAVAILABLE in this constructed API. Process termination has `terminal_python_exception_in_model=null` (not established), rather than asserting absence of an exception. `python_raise_protected_by_dispatch_catch` describes the dynamic source region if a Python raise occurs there; it does not assert one occurred.

| Terminal modeled case | Kind | Catch-relative location | Flag | Python exception from terminal model |
| --- | --- | --- | --- | --- |
| Prefix stage `raise` | unexpected-raise | caller or before dispatch try | true | conditional, not observed |
| Prefix stage termination | process-termination | same outside location | false | not established |
| Error-storage `raise` | unexpected-raise | handler body, outside its own protected try | true | conditional, not observed |
| Error-storage termination | process-termination | handler body | false | not established |
| Unexpected fixed-helper `raise` | unexpected-raise | helper outside protected region | true | conditional, not observed |
| Ordinary fixed-helper action | intentional-fixed-raise | helper outside protected region | false | source-intended ClientFailure, conditional |
| Fixed-helper termination | process-termination | helper outside protected region | false | not established |
| Normal client byte return | normal-return | client return outside dispatcher | false | no terminal exception modeled |

Thus false does not mean “inside the catch”, “no exception anywhere”, “no pending error”, “no earlier effects” or permission to continue. No global absence of records is inferred from `retained_original=False`: that field concerns the newly modeled storage route, while the separate pending-owner-failure representation is preserved. Any already modeled exception or completed storage before a later termination remains a separate premise. A terminating storage stage leaves storage confirmation UNKNOWN. A normally completed storage stage followed by helper termination can retain its original reference; this does not establish later propagation, a failure file, physical durability or cleanup. All evidence destinations remain source-conditional.

The process-termination case now additionally requires the projected callback and all cleanup outcomes to be unobserved. Contradictory claims of post-termination callback/cleanup continuation reject. This does not resolve recovery obligations or prohibit later recovery in a different authorized process. The classifier cannot establish retained error, cleanup completion, external nonexecution, renewed authorization or admission.

## Defining sources and consumers

The exact retained prospective_entry.py is 9,485 bytes, SHA-256 a1d80c523ae220228a6b27cac42b5e57a006336e858a8e7db0a75355d6cf2ae9. `_fail` at lines 28–29 raises the fixed ClientFailure from None. `_dispatch` at lines 143–166 performs owner lookup/guard before the try, protects lines 148–160, stores `owner.failure = error` in its handler and then calls `_fail` outside that protected try. `Client.handle` at lines 115–116 forwards through `_dispatch`. `_run` at lines 169–195 remains a separate outer continuation.

The exact lab_bootstrap.py is 11,481 bytes, SHA-256 245d4f36d687834aeee064a60d4414b15f7b8babfdb5dec192aa995d93af2b78. Its existing failure/cleanup path is lines 167–176. It does not guarantee every close, error formatting, evidence write, durability or removal of ACTIVE. Exact source paths, bytes and hashes are retained in the predecessor and the source-change audit.

`provenance/flag-consumers.json` records the original definition, assignments and consumers. The old prefix helper assigned true for every nonnormal outcome, while error storage/fixed helper assigned true only for `raise`. Projection validation compares the complete regenerated result. No operational/admission decision in the reviewed code consumes this flag; test assertions were its other direct consumers. The public receipt carries static declarations and saved-evidence gaps, not constructed execution observations.

The correction replaces scattered flag assignments with one terminal classifier derived from the completion and source-anchored event. Two existing producer functions change (`compile_client_handle`, `client_handle_projection`), one helper is added, and the remaining producer functions stay byte/AST-equivalent. The adapter changes only its producer pin, packaged recovery path and local receipt version. The static catalogue is I164-CLIENT-HANDLE-STATIC-2; the public receipt is I164-CLIENT-HANDLE-RETURN-CORRESPONDENCE-2; the classification contract is I164-CLIENT-TERMINAL-CLASSIFICATION-1. Old serialized output is preserved and rejected as current output, not silently repaired. These are explicit local correspondence-format changes, not a privacy policy, allowance or S90 domain amendment.

## Reused independent support

Formal-Lab[6]'s forwarding review is incorporated with scoped support and its explicit process-termination caveat. Its archive is 59,157,073 bytes / 172 entries / SHA-256 18cbb930e1b0db4d42b9e4b7f2af32f521d9f2c50c268216d8c02793c124df9f. CRC, safe unique regular membership and all manifested hashes were verified read-only. Its 217 primary assertions, 149 recovered-root assertions and separate CLI check remain independent historical results. The six additional caveat cases remain outside those totals. Its zero-assertion membership refusal and exact 15,990,784-byte partial file are preserved; their origin remains UNKNOWN.

The reviewed implementation is 43,439,616 bytes / 1,282 entries / SHA-256 1f7b1c7dc58949e76f73cac68afb00ea0373490ac0c07bdada86d954772b4431. Every member is retained unchanged in original/. Supplied 17 corrected focused controls, 168 recovered controls and one process check remain separate from the independent results and this correction. Its 170 pre-correction controls retain their original producer scope. Original helper/storage witnesses, including the first incorrect false helper flag, remain exact. The current controls reuse saved inputs to preserve the corrected helper interpretation in both contexts; they do not execute the historical suites or runtime functions.

## Limits

This is not complete interruption classification or runtime qualification. The existing projector is partial for outer callback/cleanup continuation. An abrupt helper does not prove that the source cannot later propagate an already retained owner.failure; the unrepresented route remains unestablished. The change neither fills that gap nor restricts actual client outcome domains. Conditional `raise`/termination choices are not physical feasibility evidence. Exact response bytes, distinct acquisition/instance-qualified occurrences, prior error routes and both contexts retain their meaning.

The saved smoke has 18 traced invocations and a separate frameless Client.state observer call, no captured handle-return chain, and an empty retained journal. Missing packet/inject, exception, response, reference and cleanup observations remain missing. The two symbolic contexts are not two physical executions. Empty journal is not lifetime zero. No new runtime return chain, Python exception/unwind, historical provenance, complete repetition coverage, storage durability, exclusivity or qualification is claimed.

The current correction still needs independent review. Its focused results and any failed attempts are separately recorded in RESULTS.json. All eleven obligations, four inventory/fourteen lifetime UNKNOWN totals, Decision B, retention, allowances and recovery/security duties remain unchanged. SOURCE-ONLY unchanged; cumulative-envelope unadopted; readiness/final binding blocked; admission disabled.
