# TE-01 / TE-02 bounded correction

This is SU-Engineering[288D]'s correction for independent closure review, not an independent closure verdict. It applies only to the retained I164-target-acquisition-ntgmpk_3 offline path.

## TE-01

`evaluate.tree` now checks the root with lstat, derives the exact allowed directory set from the declared file paths, and enumerates every directory entry without following symlinks. It rejects undeclared files/directories, nonregular entries, missing members, file/directory conflicts and unsafe manifest names. It completes name/type validation before opening any payload. Regular-file byte checks remain mandatory. Public output validation checks both roots before consuming outputs; source loading checks them before candidate imports.

Both original witnesses are retained: the prior public validator accepted an undeclared FIFO, and the prior direct checker accepted an extra empty directory. The corrected public entry points reject both. Tests count payload reads to show that unsupported entries reject before file consumption. No source-membership rule was relaxed.

## TE-02

The finite-input constructor makes separate deep copies of the count receipt and its bindings. Adding the target-acquisition binding to bundle.bindings no longer changes the standalone receipt or the bundle's embedded receipt. The target binding is still present in the bundle and downstream representation/ledger bindings.

`receipt_correspondence` requires saved count-receipt.json to equal contract.enc(parse(saved bytes)), then requires contract.enc(bundle.evidence_count_receipt) to equal those exact saved bytes. The serialization contract is sorted, compact, ASCII JSON with no nonfinite numbers and exactly one trailing LF. Duplicate keys reject. Validation does not write, repair or normalize either input. The check runs during construction before writing the bundle and during public validation before finite representation verification.

The pristine predecessor's mismatch and exact alias-return expressions are retained and reproduced. Corrected validation rejects those original saved artifacts specifically at EMBEDDED-COUNT-RECEIPT. Additional mutation fixtures deliberately reseal only their test output pins to exercise semantic receipt checks beyond the generic byte-pin gate. These test fixtures are not accepted checkpoints.

## Preserved boundaries

The acquisition archive, nine source roles, lineage records, configuration/session/ownership identities, candidate and draft transports, legacy acquisition, earlier reviewed integration, governing schemas, consumer, verifier, mechanical ledger and carrier-expression logic are unchanged. Empty journals require no manufactured request; explicit legacy saved-head evidence remains required. Both symbolic contexts and acquisition-qualified keys remain separate from the earlier snapshot.

All eleven obligations, UNKNOWN classifications, four inventory unknowns and fourteen lifetime unknowns remain. SOURCE-ONLY; readiness/final binding BLOCKED; backup KERNEL-ONLY; streams UNCOMPUTED; admission disabled. Factual history/cutoff, production cardinalities, ownership/custody/durability and lifetime completeness remain unestablished. No policy or limit changed.

## Evidence scope

Original review identity: 46,702,282 bytes / 75 entries / SHA-256 b32759c18d6c29d4e7c81270d678534719c24b108b78cb71fc4ce962847bfd41. Original implementation identity: 75,721,424 bytes / 74 entries / SHA-256 df90c233aac5b6a8e00f2bbcb817b2a1aa4fa8f4d4a7a88a55cd952926c665a6. Both archives were verified read-only. Their full archives remain exact external dependencies; selected witness code/results and exact original affected files are included here.

Prior supplied 44 controls and prior independent results are not counted as new tests. New correction results are recorded separately. A Unix socket fixture could not be created because this runtime returned PermissionError; its harness failure is preserved and that case is explicitly unexecuted, not passed. No device-inode test is claimed. The scanner rejects unsupported types by its lstat mode branch, but this statement does not substitute for unexecuted platform-specific tests.

One corrected offline full chain is authorized and recorded. Subsequent fresh-process/recovered-root validation reuses its outputs and performs no reconstruction, database connection, session operation, lifecycle or completed-review rerun.
