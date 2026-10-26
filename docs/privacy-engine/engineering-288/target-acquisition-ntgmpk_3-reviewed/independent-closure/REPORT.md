# TE-01 / TE-02 independent closure review

**Verdict: CLOSED within the retained bounded offline observation contract.** TE-01 and TE-02 are individually supported for closure. No remaining defect witness was found within that scope. This verdict does not establish readiness, final binding, complete-model verification, production/lifetime bounds or admission.

Reviewer: **Codex, the separate reviewer in this session**, 26 October 2026. Construction/correction author: **SU-Engineering[288D]**, as identified in the supplied CORRECTION.md. The reviewer did not author or modify the correction or candidate implementation. Engineering's results are supplied evidence, not this reviewer's execution results.

## Verified artifact and recovery

The supplied correction is exactly **77,270,588 bytes, 130 unique regular entries**, SHA-256 **`1e0bbb0498e46da537aad3a2e0af2781607d9cbee10043e2a685c4efff310204`**. CRC, canonical safe paths, exact membership and every manifest hash passed. Two extracted copies were checked. The complete changed-identity disclosure agrees with the original archive: 85 changed/added members, 43 unchanged members, two self-excluded metadata files and 16 predecessor-only members retained in the verified external predecessor.

Exactly two implementation files changed: `code/evaluate.py` and `code/adapted_finite_inputs.py`. The other seven implementation files and all six input artifacts are unchanged. Source/component pins were checked against actual bytes. Both recovery transports were independently checked against their exact recovery manifests and unchanged predecessor member maps: **666 candidate members and 163 draft members**. All those recovered bytes were verified again at completion. This preserves historical identities, the 90 historical files, 43 relationships, inherited ordinals and prior scoped findings by exact unchanged membership; completed historical/component reviews were not repeated.

The original construction archive and original review archive were verified as exact dependencies, including CRC and manifests. An initially encountered truncated local copy of the original review was excluded and preserved; the exact 46,702,282-byte review was recovered and verified. It was not rerun. Dependency identities and recovery arrangements are in `DEPENDENCIES.json` and `RECOVERY.md`.

Recovery and later fixture preparation exposed undeclared partial-copy files. Strict checks rejected affected roots. Their bytes and observed identities were preserved outside strict recovered roots; origins remain **UNESTABLISHED**. No declared member was deleted or changed, and no membership rule was relaxed. An initial full-chain attempt stopped during root authentication before candidate imports. After explicit preservation and exact root verification, one independent full chain completed successfully. Initial harness failures and the successful continuations are retained separately; a failed harness is not counted as a passing control. A harness message saying “VALIDATOR MODIFIED FIXTURE” was too broad: declared inputs remained unchanged and the difference was an extra partial-copy file. Subsequent mutation checks separately verified declared bytes and used a read-only process audit hook.

## TE-01 — closed in scope

The old public validator again accepted a root containing an **actual undeclared FIFO**. It also accepted an extra empty directory. The original code and false-acceptance stdout are retained/pinned. The corrected public validator rejects these at `UNSUPPORTED-ROOT-ENTRY` and `UNDECLARED-ROOT-DIRECTORY`. A focused source-load check recorded rejection before candidate payload reads or candidate imports for the FIFO witness.

The corrected scanner derives allowed directories from authoritative declared paths. It uses non-following entry classification, rejects every undeclared name and unsupported entry type, checks exact file/directory membership, then verifies regular payload identities. Legitimate nested trees and declared zero-byte files pass. Actual filesystem controls cover unexpected regular files and directories, FIFOs, file/directory/root symlinks, root type errors, missing members, altered bytes and an extra hard link. Invalid layout/type cases reject without opening special files; byte alteration rejects at the byte-identity check.

**Actual Unix-socket execution remains UNTESTED.** The supplied socket creation failure remains excluded from passing counts. The review performed only synthetic socket, character-device and block-device mode classification; these three checks do not establish actual socket/device filesystem execution. No concurrent adversarial filesystem-mutation or physical-inode uniqueness guarantee is added to the retained stable-input/trusted-process contract.

## TE-02 — closed in scope

The old public validator accepts the pristine original artifacts even though the saved receipt and embedded receipt differ. The smallest original mismatch is the additional `bindings.target_acquisition` in the embedded receipt. Removing only that field makes its canonical bytes equal the original saved receipt. Exact identities are recorded in `results/final-audit.json`.

Corrected public validation rejects the original mismatch specifically at `EMBEDDED-COUNT-RECEIPT`. A private test output-pin map permits reaching that correspondence check without treating the altered fixture as an accepted checkpoint. No implementation/source/component pin is changed.

The serialization contract is sorted compact ASCII JSON, no nonfinite numbers, no duplicate keys, and exactly one trailing LF. Saved bytes must equal their canonical serialization, and serialization of the embedded value must equal those exact saved bytes. Missing/additional LF, CRLF, leading whitespace, pretty printing, duplicate keys, missing embedded evidence, changed values/types, context order, acquisition, obligations and status all reject as appropriate. Validation does not normalize or repair the inputs.

The constructor's exact pinned return expressions establish two separate deep copies. Nested and reverse mutations reproduce the original alias and confirm isolation after correction. The actual new full chain independently confirms that adding the bundle's target-acquisition binding leaves the saved and embedded receipts unchanged. Shared equal replacement data is not authority: coordinated false receipts can satisfy equality alone, but public sealed-byte validation rejects the substituted current inputs. This distinction is explicitly tested.

Seven process-level mutation cases reach semantic checks with test-only output pins: embedded binding alteration, saved count alteration, saved acquisition alteration, saved context reversal, embedded omission, noncanonical saved bytes and a false ledger summary. All reject; declared input bytes remain unchanged. The final six use an additional process audit hook rejecting filesystem writes. The first retains its actual rejection and independent before/after declared-byte check. CF-01 summary correspondence remains supported.

## Independent execution and arithmetic

One authorized fresh offline chain completed in approximately **305.8 seconds**. It used actual recovered sources and saved acquisition evidence; it made no database connection or session operation. Fresh-process validation of these outputs passed. The only bytes differing from supplied corrected outputs are execution time/duration metadata in RESULT.json and the consequent output-manifest hash. Every other output is byte-identical. Validation of review-generated metadata used its exact independently checked output map, with implementation/component pins unchanged.

| Context | Source occurrences | Framing occurrences | Tokens | Structural pairs | Semantic pairs | Fold duties |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SYMBOLIC-U-ONE | 95 | 950 | 1,045 | 1,039 | 0 | 12 |
| SYMBOLIC-U-TWO | 95 | 950 | 1,045 | 1,039 | 0 | 12 |

Independent accounting reconstructs exact occurrence bytes, acquisition-qualified identities, all 9,339 directory memberships and ranges per context, and source-defined relation joins. The 1,039 structural pairs comprise **950 framing-owner, 86 nearest-declared-ancestor and 3 same-observed-value joins**. Governing semantic emitter domains are absent from the empty-journal/genesis evidence, supporting zero semantic pairs. The 12 authenticated-fold obligations remain duties, not extra Cartesian pairs. All 9,376 relation duties per context retain their ordinals and ranges; many have no instantiated edge. Their duty count is therefore distinct from the 1,039 model-edge count.

The final verification and ledger receipts bind the actual new bundle, native representation, component identities and ledger bytes. Independent checks verify these links and preserve UNKNOWN classifications and all eleven obligations. The two contexts reference one acquisition; they do not multiply physical storage.

## Evidence separation

Supplied Engineering evidence inspected, not rerun as a review: **34 focused controls, five process checks and 13 post-chain checks**, with the unavailable socket control excluded. Their scripts, expected boundaries and results were inspected separately.

Fresh independent evidence consists of:

- 18 actual filesystem/manifest controls and three explicitly synthetic type-classification controls;
- 17 receipt/serialization/alias controls;
- nine old/corrected/public/recovered-root process cases;
- seven process-level receipt/summary substitutions using test-only output pins;
- five final process cases: validation of the new full chain, coordinated count substitution, coordinated stale-acquisition substitution, missing saved receipt and status escalation;
- three focused unchanged acquisition-contract checks: target empty journal/nine roles, legitimate earlier saved-head evidence and rejection when that earlier required request is omitted;
- independent recovery/integrity/preservation checks and source-backed arithmetic on the **new** full-chain outputs.

The focused arithmetic checker was reused against new outputs and unchanged governing sources; no predecessor producer campaign or completed review was executed. Raw failure records remain separate from passing result lists. The executed environment was **CPython 3.12.14, Cryptography 50.0.2, Linux 6.18.55, glibc 2.39**. This is not a new prepared-host Cryptography 41.0.7 compatibility result or installed-wheel byte authentication.

## Retained limits and next step

The earlier acquisition and its saved-head requirement remain exact and supported. The target retains its nine source-role identities and copy lineage; an empty journal requires no invented request/response. Required evidence for request-bearing acquisitions remains mandatory. Checked retained byte facts do not prove recorded lock, source ownership, copying, lifetime or durability assertions. Both symbolic contexts retain acquisition-qualified occurrences without cross-acquisition joins.

All eleven obligations remain; four inventory quantities and all fourteen lifetime totals remain UNKNOWN. Production cardinalities, physical-storage totals, operational ownership/custody/durability, factual history/cutoff, canonical authority and original-record reconciliation remain unresolved. SOURCE-ONLY is unchanged. **Readiness/final binding BLOCKED; backup KERNEL-ONLY; streams UNCOMPUTED; admission disabled.** No policy, limit, retention rule or outcome domain was changed.

Engineering-Anchor[2] can record TE-01 and TE-02 as scoped closed using this checkpoint. The next substantive dependency remains authoritative evidence/decisions establishing the protected production directory universe and lifetime multiplicities, followed by the retained operational and canonical prerequisites. These fixture and selected-snapshot counts do not supply lifetime bounds.
