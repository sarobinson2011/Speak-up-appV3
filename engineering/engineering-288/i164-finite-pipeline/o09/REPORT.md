# Bounded O09 / finite-pipeline integration

SU-Engineering implementation, pending independent review. SOURCE-ONLY. This connects the unchanged reviewed carrier/copy validator as the fifth mandatory stage of the CF-01-corrected finite pipeline. The first four stages, reviewed worker, recovery contracts, candidate and draft inputs are unchanged.

The public command executes the existing finite-input, consumer, output-verification and mechanical-ledger validators on actual outputs, then executes copies.py and revalidates its actual receipt with the pinned public API. Final receipt format is I164-CONNECTED-FINITE-RECEIPT-2; the fifth stage is mandatory. No final receipt is emitted if any required stage, receipt or summary fails.

copy_bindings derives summary quantities from the current validated receipt and checks the actual result envelope, then binds receipt bytes, result bytes, validator identity, acquisition, evidence archives, current count/source bindings and both contexts. It is an internal post-stage helper, not a substitute public pipeline. CF-01 output_bindings remains byte-for-byte unchanged. Submitted final receipts must exactly match freshly validated outputs.

45,056 bytes means only the two selected database-member payloads (16,384 + 28,672), once for the acquisition. Archives, exports and archive members retain distinct roles; their overlapping bytes are not added. Symbolic contexts do not multiply physical storage. Recorded lock/sidecar/capture assertions are retained in the exact copy receipt and separately identified as recorded assertions. Physical container count, physical storage and lifetime remain UNKNOWN. Global O09 closure is explicitly false.

Independent O09 support is scoped: 27 public controls, ten constructed internal controls and six process checks are distinct from Engineering's 38 controls and four process checks. Those completed review suites were inspected as saved evidence, not rerun. New tests exercise the connection, not re-review the components. Local CPython 3.12.14 / Cryptography 50.0.2 results are not new Steve-host or operational assurance.

All eleven source-only obligations and their other retained representations remain unchanged. Candidate 666-member and draft 163-member exact manifests remain authoritative for preservation, including historical files, relationships and ordinals. This work creates no model expansion, canonical registration, ledger rebinding, qualification, global capacity or admission.

Readiness/final binding BLOCKED; streams UNCOMPUTED; admission disabled; backup kernel-only. No database connections, new acquisition or session operations are performed. Cooperative/stable source ownership remains an inherited boundary; this is not hostile concurrent filesystem assurance.

Recovery failures are retained separately. Undeclared partial files were rejected by strict membership checks, and preserved without attributing their origin. No expected-member hash or membership check was weakened. Selected exact source trees were checked before and after execution. Consult results and failures for actual execution dispositions, rather than treating this report as test evidence.

## Fresh results

One actual five-stage run passed across both contexts. Eighteen focused copy-link controls and eleven final-link/CF-01 controls passed. Three designated fresh-process checks passed: recovered-code positive, coordinated-substitution rejection, and public stale-validator rejection before stage execution. Final-link mutation controls re-check actual outputs and the exact comparison used by the connector; they are not additional full public pipeline runs. All 666 candidate and 163 draft members passed exact before/after checks. No failed test is concealed; recovery failures are separate.
