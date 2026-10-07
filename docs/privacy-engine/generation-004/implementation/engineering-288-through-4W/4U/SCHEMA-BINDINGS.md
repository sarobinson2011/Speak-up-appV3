# Applicable accepted fields and exact binding decisions

All line references refer to the byte-exact files under historical/4T/evidence, with full-file hashes in the derivation envelope and package manifest. The active S90-FCR source includes the approved 4I amendment; its bytes are preserved.

| Accepted source / retained schema | Applicable binding | 4U disposition |
| --- | --- | --- |
| S90-FCR lines 385–390; admission_kernel/model.py lines 17–18, 63–71 | Closed model has surfaces, relations, tokens, structural_edges, equality_stream, actor_graph_policy. Retained equality layout is the binary pair stream. | No model change. `/equality_stream/sha256` stays the binary SHA. No `links_sha256` field is invented inside model. |
| S90-FCR lines 773–788; S70 LINK_HEADER at 747 and link_bytes at 967 | Exact structural/potential tuple union, lexical four-string ordering, original endpoint orientation, ordinals, header and TSV byte law. | Whole-model static textual hash/counts recorded in a separate derivation envelope; exact descriptor and completed job retained. |
| S90-FCR lines 789–809; S70 EVIDENCE_HEADER at 748, evidence construction at 979–987 | Future `evidence.tsv.links_sha256` hashes complete exact links.tsv for that bundle's independently grounded scope. `profile_sha256` binds final outer profile. | Potential future binding identified, but no evidence.tsv row is created. No final profile or scope is invented. |
| S70 lines 984–987; retained v4_ingest wire.py signed_payload/object_preimage | Signed bytes: `PE-TSE-PRIVACY-EVIDENCE-V2\n || evidence.tsv || tokens.tsv || links.tsv`. Object bytes: `PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n || L64(evidence.tsv) || L64(tokens.tsv) || L64(links.tsv) || L64(signature.txt)`. L64 is U64-BE byte length followed by exact file bytes. | A links digest cannot replace original links bytes in either preimage. Neither object digest nor signature is computed or populated. Pure Ed25519 semantics remain unchanged. |
| S70 immutable profile at 703, 1201; S90-FCR governing immutable member rules | Outer bytes are final before external evidence signs their digest. | The new engineering envelope is not inserted into immutable profile bytes, which are unavailable. No circular profile/signature dependency is introduced. |

## Exact textual law

Header is `link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n` (67 bytes). UTF-8, no BOM, no CR, literal TAB separators and one LF after every row. Compare tuple strings `(from_token_id,to_token_id,relation_order,relation_class)` lexically. Do not lexically reorient a potential pair: original token indexes obey i<j. Potential tuples use `000000,EQUALS`. Structural tuples retain positive one-based six-digit template order and exact class. Identical four-cell tuples appear once; distinct provenance orders remain distinct. link_order is global one-based decimal of minimum width six, so ordinals above 999999 grow normally.

The exact descriptor has SHA-256 c79ea7fa8e27de3fb051c50f4f50d52cecb51c3d3e0025c9569b174d27882f5f, 236,894,099 bytes. The 6,831,760-byte prefix table has SHA-256 4e38741dcd71df691d76b156d9b91f07b43c6e3f0a540fb9f5013e102f6adf1b. The completed 4T correspondence compared every descriptor token, fixed group and structural row to the candidate model. 4U verifies the exact model/descriptor/report/job identities and reuses that completed comparison; no expansion or pair enumeration repeats.

The cumulative SHA state covers the single header and contiguous exact rows. Whole-stream identity is not a concatenation of segment digests. Return verification finalized all saved prefix states and checked both receipt chains. This establishes consistency of trusted local saved evidence, not independent recomputation or source qualification.

## Dependency impact

`derived/CHANGED-FIELDS.json` is a machine-checkable old/new JSON-pointer comparison for witness assembly, requirements, gap report and dependency graph. Model/source/contract changes are empty. The new envelope has exact references to completion ZIP, original kit, completion receipt, verifier, model/contract, descriptor/prefix, generator code and source clauses. The package manifest binds the new metadata implementation code.

No normative ledger binding, disposition, budget, source provenance or directory selector changes because no governing source/model/contract byte changed. The existing 4S ledger envelope remains exact. New witness metadata references it unchanged. No old signed fixture or recovery receipt is promoted into a new job.

Future bundle construction requires actual final profile, source-owned scopes and token tables. Only a scope proven to have these exact complete textual bytes can reuse this hash. Component scopes and E/PRE-EXECUTION/PRE-COMMITMENT occurrence values cannot inherit this whole-model static hash by name. Independently computed result cells, appointed authority and original-message signatures remain required. Four-file object and cross-bundle source references follow their actual bytes; new scheduler input/prerequisite receipts follow those objects. The graph remains acyclic; the final profile does not depend on signatures over itself.
