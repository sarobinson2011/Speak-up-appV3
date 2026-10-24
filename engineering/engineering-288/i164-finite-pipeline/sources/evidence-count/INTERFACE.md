# Evidence-to-count contract

This adds one offline evidence-consuming entry point to the retained count-input path. It changes no predecessor byte and creates no new counting framework. The retained universe.count_acquisition_bag remains a supplied-count helper whose result explicitly does not authenticate its count inputs. Its result cannot serve as a receipt under this contract.

## Mandatory entry points

code/evidence_counts.py exposes build(root,draft), consume(root,draft,receipt), and validate(root,draft,receipt,result=None), plus equivalent build/consume/validate CLI commands. Each public operation resolves fresh exact input bytes; no successful-object cache or shared mutable result is used. require_ready always rejects this finite-only domain.

The supported evidence domain is exactly the acquisition/evaluation pair named by provenance/BASIS.json and its source-code-pinned SHA-256. Changing the authorized input set needs an explicit new basis; this does not restrict the protocol's permitted external-outcome domain. Both inherited symbolic contexts must be present in their declared order. It is one acquisition viewed in two contexts, not two acquisitions or two physical database sets.

## Validation order

1. Check pinned basis, unique archive membership, CRC and every original manifest entry. Verify all 666 candidate and 163 draft members, exact current input identities, module paths, original export/request/response bytes and evaluation lineage.
2. Resolve the complete original directory set and guarded finite occurrence rows. Derive counts from the existing compiler row adapter, not caller count fields. Bind every directory to exact saved range membership, local contiguous ranges and source occurrence identifiers. Include framing and index records. Snapshot zeros apply only to this fully evaluated export.
3. Reject a submitted receipt if any field, count, membership binding, context, obligation or blocker differs. A matching receipt still must pass step 4; step 3 is only early rejection, never an acceptance certificate.
4. Run ingest.validate_export and the existing prospective_procedure.validate_result for each context. Those validators reestablish authentication, source projection, ancestry/accounting, source/rule/directory bindings, semantic pair and duty results. This is stronger than a capture hash or a retained success label.
5. Feed the evidence-derived complete vectors to the actual universe.count_acquisition_bag. Check count conservation and context conservation. Return a finite selected-acquisition consumption result; keep the helper's original limited-scope result visible.

## Identity and preservation

Receipt identity is SHA-256 of the module's canonical enc(receipt) bytes, excluding any file newline. Archive members and exact evidence identity use original raw bytes, including their original framing. Byte identity is never compared by JSON-serializing bytes.

Each vector key is the existing context|class directory identifier. Each occurrence retains the pinned local ID, record_index and pointer within original saved occurrence evidence. The outer namespace adds acquisition_id and context. Equal observed values remain distinct occurrences. Exact required evidence is retained in the original archives, not replaced with hashes.

A receipt includes 18,678 integer counts, exact evidence and current-input bindings, original eleven-obligation records, membership commitments, finite token/pair results and the new implementation identity. Full retained occurrence and procedure evidence remains available through its exact archive/member associations. Production cardinalities, global lifetime bounds and global byte bounds stay null. Classification UNKNOWN, qualification UNAVAILABLE, SOURCE-ONLY, full_expansion_ready false, final_binding BLOCKED, canonical_registration false, actual_admission false, backup KERNEL-ONLY and stream_identities UNCOMPUTED cannot be escalated.

No cross-acquisition joins, native expansion, ledger construction, session initialization, database connection, request, signer invocation, new allowance, migration, retention, compaction or new policy is part of this interface. Source-owned bounds, operational facts and qualification are separate obligations.
