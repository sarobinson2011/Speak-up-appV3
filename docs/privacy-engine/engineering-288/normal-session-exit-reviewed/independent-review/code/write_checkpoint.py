from pathlib import Path
import json
W=Path(__file__).resolve().parents[2];R=W/'ns-review'
a=json.loads((R/'results/final-audit.json').read_bytes());c=json.loads((R/'results/composition.json').read_bytes())
assert a['result']=='PASS' and a['completed_independent_controls']==312
checkpoint={'checkpoint':'Formal-Lab6-I164-normal-session-exit-independent-review','review_date':'2026-10-29','target':'I164-normal-session-exit-correspondence-1.zip','input':{'bytes':70593959,'entries':2331,'sha256':'c9c8d2106617970e8008fadc3c60f61813c64e7ce07e24a60bc92ac1029b954a','manifested_hashes':2330},'review_author':'Formal-Lab[6]','construction_author':'SU-Engineering[288D]','author_independent':True,'implementation_changed':False,'verdict':'SUPPORTED within the bounded mandatory SOURCE-ONLY normal session-exit correspondence contract','smallest_residual_witness':None,'integrity':{'CRC':'PASS','safe_exact_membership':'PASS','all_manifested_hashes':'PASS','declared_changes':'PASS','recovery_dependencies':'PASS','present_nested_archive_occurrences':len(c['present_nested_archives']),'interpretable_manifest_documents':len(c['current_archive']['manifests']),'strict_verified_roots':a['strict_verified_roots'],'prior_outer_archives_newly_verified':False,'supplied_intermediate_outer_archive_newly_verified':False,'supplied_intermediate_unchanged_members':2296,'supplied_intermediate_documented_README_change':c['supplied_intermediate_documented_differences']},'preservation':{'token_predecessor_members':2178,'prior_review_noninput_members':82,'inherited_producer_functions':84,'added_producer_functions':c['added_functions'],'runtime_sources_changed':0,'historical_identities_relationships_ordinals_and_prior_closures':'UNCHANGED','obligations':11,'obligations_identity':c['obligations_identity'],'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False},'new_receipt':c['new_receipt'],'independent':a['independent_groups'],'independent_completed_controls':312,'actual_CLI_check_included':True,'supplied_not_rerun':{'primary':235,'fresh_process':9,'recovered_root':35,'failed_instrumentation_attempt_checks':0,'failed_attempt_excluded':True},'reviewer_failures_excluded':a['failed_attempts_excluded'],'forensic_root':a['forensic_root'],'limits':{'contract':'Source-derived conditional normal continuation; finite constructed outcomes, not observed application execution','selected_owner_continuity':'Explicit constructed premise; unknown continuity does not identify the popped owner','physical_object_identity':None,'host_path_resolution':None,'normal_exit_runtime_chain':'UNAVAILABLE','saved_traced_invocations':18,'separate_frameless_Client_state_observer':'UNJOINED','normal_close_relation':'Source interpreter; opaque operation outcomes remain constructed premises','physical_closure':False,'durability':False,'runtime_exclusivity':False,'persistent_marker_absence':None,'exceptional_and_outer_cleanup':'UNEXPANDED','runtime_unwind':'UNAVAILABLE','owner_lock_release_or_outer_context_exit':'NOT ESTABLISHED','complete_repetition_coverage':False,'operational_obligations_discharged':False,'authorization_renewed':False},'operations':{'requests':0,'database_connections':0,'session_operations':0,'new_acquisitions':0,'host_smokes':0,'completed_suite_reruns':0,'completed_review_reruns':0,'lifecycle_reruns':0,'implementation_changes':0,'policy_changes':0},'environment':a['independent_groups']['primary']['environment']}
(R/'CHECKPOINT.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
report='''# Formal-Lab[6] independent normal session-exit review

**SUPPORTED within the bounded mandatory SOURCE-ONLY normal session-exit correspondence contract.** No residual defect witness was found in this slice. This verdict names **I164-normal-session-exit-correspondence-1.zip**, not a preceding status, token or runtime checkpoint.

Review author: **Formal-Lab[6]**. Construction author: **SU-Engineering[288D]**. I did not author this construction. Engineering's controls are supporting evidence, separately inspected below. Implementation and original evidence were not changed. Review date: 29 October 2026.

## Verified target and recovery

The input is exactly **70,593,959 bytes, 2,331 unique regular-file entries**, SHA-256 `c9c8d2106617970e8008fadc3c60f61813c64e7ce07e24a60bc92ac1029b954a`. CRC, safe paths, exact membership and all **2,330 manifested hashes** pass. Strict roots contain 2,331 files and 699 implied directories. `ns-input` and the new `ns-recovered-v2` passed final membership/type/byte verification after testing.

All **2,178 token-predecessor members** remain exact, as do **82 retained non-input prior-review records**, including that review's manifest. The redundant original token ZIP omitted from the compact prior-review tree is identified by its original bytes/hash and represented by the exact decoded predecessor tree. Its original outer ZIP was not independently re-obtained or recompressed here. The authenticated prior review is reused, not rerun.

The two intentional implementation changes match the declared old/new identities and the complete supplied unified diff: the connecting adapter and five additive producer functions. All **84 inherited producer functions/classes**, their source bodies and non-function AST remain unchanged. The predecessor prefix is byte-identical apart from a new descriptive comment before the extension. Runtime source convenience copies match the actual validated chain's source bytes. Earlier context fields, historical identities, relationships, ordinals, qualifications, evidence and findings are unchanged in the assembled receipt.

The present nested dependencies pass CRC, safe membership and manifest-byte checks: **18 nested archive occurrences**. The top-level tree contains 33 interpretable manifest documents, including compact forensic snapshots and provenance manifests whose omitted/rebased entries are recorded separately. These are not silently treated as newly available original outer archives. The fresh mandatory-chain execution proves the required saved-input recovery composition is available for this scope.

Engineering's intermediate recovery cut is recorded as 70,479,931 bytes / 2,298 entries / SHA-256 `c73070a6b8ad81b0571b34b4034fa0af416a2c1420af0c21066e756063f5e303`. I checked its retained selection against the final tree: **2,296 member bytes are unchanged; README.md is the one explicitly documented wording clarification**. Code, primary receipt, controls and historical evidence are unchanged. The intermediate outer ZIP itself was not freshly verified. Independent recovery used the externally identified final target instead.

## Source-backed correspondence

| Defining source | Exact identity | Relevant source scope |
| --- | --- | --- |
| `source-evidence/prospective_entry.py` | 9,485 bytes; `a1d80c523ae220228a6b27cac42b5e57a006336e858a8e7db0a75355d6cf2ae9` | `_run`, lines 169–195: normal callbacks/failure guard, finally pop, launcher context |
| `source-evidence/lab_bootstrap.py` | 11,481 bytes; `245d4f36d687834aeee064a60d4414b15f7b8babfdb5dec192aa995d93af2b78` | owner_lock 108–117; ManagedSession 119–124; `_session` 127–176; public session 179–186 |
| `source-evidence/live_connection.py` | 5,717 bytes; `7344170ca01a2dbbd3afbeb4a6a55c0b95db0edb1a8d74e4fa4638b6dcfc6da5` | `_quarantine`, `_dispose` 50–56 and close 57–60 |

I independently traversed these ASTs, located the actual yield/tail statements, compared source coordinates, enclosing guards and preceding statements, and derived the seven-stage coverage without taking generated declarations as the oracle. Both contexts require: **session resumption → launcher resumption → close attempt → close completion → local managed clear → unlink attempt → unlink completion**. The source tail after `yield ManagedSession(managed)` is exactly `managed.close(); managed=None`, followed by `(dest/'ACTIVE.json').unlink()` inside the launcher's BaseException-protected region. Public session resumes its `_session` bridge only after the normal token-path continuation.

The current entry actually invokes the unchanged predecessor's `_checked` and `_assemble`, the two operations performed by `derive_token`, and reaches the underlying validated status chain. Monitored calls confirm consumption rather than collection of detached receipts. Its canonical predecessor output must equal the exact saved reviewed token receipt. New catalogue and source expectations are rebuilt from current authenticated inputs. A submitted report cannot define its own authoritative destination, instance or step ordering.

The close case must use the selected context, acquisition, validated instance and selected invocation's `/managed-close` scope; the unchanged source-driven reference interpreter computes it. Manager and wrapper roles come from the validated token reference relation. Session identity is cross-checked against saved start/binding records and the source launcher identity. ACTIVE.json uses the source-derived component and owner-lock destination expression. The recorded path is nominal: owner_lock resolves the parent before yielding its destination, but this review neither resolves a host path nor establishes physical path equivalence.

Selected-owner continuity remains an **explicit conditional premise**. Unknown continuity does not prove which owner was removed. It also does not prohibit source-normal launcher continuation: `_OWNERS.pop(token, None)` discards its result. This is not a new operational exclusivity or persistent-revocation claim.

## Completion, failure and absence

Attempt entry, normal close completion, local clear and unlink completion have separate milestones. True means acknowledged within the constructed prefix; False means not established, not proof that an unobserved effect could not have happened. The local launcher's `managed` slot and the wrapper's manager reference remain distinct. Clearing one does not clear the other or discharge duties.

Normal managed close comes from the existing interpreter's ordered quarantine/dispose/phase path, with implicit None return. Initial labels and opaque operation outcomes are explicit constructed premises. Source-admitted close outside READY, already-CLOSED close with no live reference, and close of a retained reference remain accepted. Normal close without any underlying reference does not prove a database was physically closed.

A focused independent witness confirms the important distinction: let the close interpreter clear live/retired references and reach CLOSED, then model a failure on exiting its lock context. The close result is abrupt; normal close completion, launcher local clear and marker removal are **not** established. Changing that failure into normal close or continuing to later steps is rejected. Partial close prefixes likewise do not establish a Python exception or unwind.

The defining call is `Path.unlink()` with **no arguments**. Independent inspection of this CPython 3.12.14 environment's pathlib source confirms `missing_ok=False` and re-raising FileNotFoundError. No existence precheck, missing-file suppression or `missing_ok=True` is inserted. An explicit missing-file outcome is an exceptional frontier; it preserves earlier constructed close/clear facts but is not successful unlink completion. Present-at-operation contradicts missing-file; absent-at-operation contradicts normal unlink completion. UNKNOWN permits either explicit modeled outcome without inventing an earlier stable observation. Even normal unlink establishes only namespace absence at that completion, not persistent absence or durability.

Missing observations or process termination do not establish normal continuation, a Python exception, unwind, retained error, outer cleanup, lock release, physical closure, durability or renewed authorization. Earlier independently established prefix facts are retained. The synthetic stage markers are source correspondence points, not observed runtime frames or arbitrary bytecode-interruption coverage.

## Independent checks and supplied evidence

| Evidence class | Completed controls | Disposition |
| --- | ---: | --- |
| Fresh independent primary | 260 | 92 positive; 168 expected rejections |
| Fresh independent recovered-root subset | 43 | 11 positive; 32 expected rejections |
| Fresh semantic/derivation process | 3 | 2 positive; 1 expected rejection |
| Fresh public constructed process | 2 | 1 positive; 1 expected rejection |
| Fresh public/CLI process | 4 | 1 actual CLI positive; 3 expected rejections |
| **Independent completed total** | **312** | **107 positive; 205 expected rejections; CLI included once** |
| Engineering primary, inspected only | 235 | 111 positive; 124 rejections |
| Engineering fresh-process records, inspected only | 9 | 4 positive; 5 rejections |
| Engineering recovered records, inspected only | 35 | 7 positive; 28 rejections |

Independent cases cover both contexts; optional control and unknown continuity; source-admitted close phases/reference configurations; every missing stage; adjacent reordering; duplicate completion; wrong owner/manager/wrapper/session/acquisition/invocation/path; foreign normal-pop inputs; coordinated close/path/destination reports; absent-marker contradictions; close/clear/unlink failure frontiers; termination and unobserved prefixes; premature completion, physical/durable/authorization escalation; subclassed keys, values and containers; boolean/integer confusion; and nested mutable return aliases. Repeated equal operations retain distinct invocation-qualified occurrences.

Fresh semantic/derivation calls reproduce the pristine receipt after returned context reversal and nested mutation, then reject coordinated changes to the saved destination bytes and agreeing reports. Fresh public constructed validation rejects coordinated wrong-manager reports. The actual recovered offline CLI accepts the exact two-context saved receipt, while missing relations, duplicate contexts and admission escalation reject. The final receipt is **4,032,928 bytes**, SHA-256 `928726175efbb720b03dc722de67477fa7ea3b3ce43b4c37bbeb2c9a730fea07`.

Tests used **CPython 3.12.14, Cryptography 50.0.2, isolated mode, bytecode writes disabled, optimization 0**. Guards prohibited application/session methods, database/network operations and host-session access; recovered/process guards additionally prohibited writes outside review outputs. No compatibility claim for 41.0.7, new prepared-host qualification or installed-wheel authentication is made. Producer/source code was analyzed or interpreted by the retained correspondence machinery, not invoked as an application session.

## Failed attempts and preserved forensic evidence

Engineering's zero-check instrumentation attempt remains exact and excluded; its 235-check retry/primary records are counted once, not twice. Its monitor failure is not recast as a completed control or a runtime defect.

Five reviewer attempts are also preserved outside completed totals: one zero-control source-fragment formatting failure; one audit that mistakenly included a new comment in its unchanged-prefix equality; one audit that overlooked the documented README-only recovery-cut clarification; and two zero-control recovered-root membership refusals. Corrections were to review machinery/assumptions only. Both failed root gates rejected before candidate code was consumed.

The first recovered root contained an undeclared regular partial `.directory-relations.json.mBen2K` at the full path recorded in `failures/recovered-membership/record.json`: **25,690,112 bytes**, SHA-256 `ed75ee885f67eca2938340b1aa5c423a9e60c04bceedfd3f90933cba0c44345e`. Its origin is **unestablished**. The archive did not declare it; no membership rule was relaxed and it was not silently deleted or adopted. The original root was left intact, every declared member still matches, and exact extra-file bytes/metadata are preserved outside strict recovered roots. A fresh exact extraction, `ns-recovered-v2`, passed the independent controls and final byte audit. The exact archive therefore remains reviewable without attributing the unexplained extra file to candidate behavior.

## Retained limits and disposition

This supports the mandatory source/constructed relation, **not an observed normal-pop → selected close → local clear → unlink runtime chain**. The saved confirmed-close record and its manager return remain predecessor-validated evidence; they are not joined to the selected constructed invocation. Saved marker absence and cooperative-lock assertions retain their original provenance and do not fill missing forwarding frames. The 18 saved traced invocations remain distinct from the separate frameless Client.state observer, which remains unjoined.

Exceptional and outer-cleanup expansion, owner-lock release, complete context-manager exit, physical identity/closure, actual exclusive custody, path resolution, real-storage durability and complete lifetime/repetition coverage remain unestablished. No complete-model, canonical authority, admission or operational obligation discharge follows from this verdict. No additional host/session check is required to support this deliberately static/constructed slice; any claim of an actually executed exit chain would need separately authorized, invocation-linked evidence of its missing steps.

All O01–O11 obligations remain bound to the exact 56,813-byte obligations document (`2c92141711e260a2ef0271635562cbac5a71aae82ac7e1a52b5dbc6f228d3a45`). Four inventory UNKNOWN totals, fourteen lifetime UNKNOWN totals, Decision B, retention, allowances, accounting/reservations/uncertainty and prior scoped closures are preserved. SOURCE-ONLY is unchanged; cumulative-envelope is unadopted; backup remains kernel-only; streams remain UNCOMPUTED; readiness and final binding remain blocked; **admission remains disabled**.

No requests, acquisitions, database connections, session operations, lifecycle, host smoke, completed pipeline/review/suite reruns, implementation changes or policy adoption occurred. This checkpoint is prepared for Engineering-Anchor[2]; no external message was sent.
'''
(R/'REPORT.md').write_text(report)
(R/'START-HERE.md').write_text('''# Normal session-exit independent review

Read REPORT.md for the scoped verdict and CHECKPOINT.json for machine-readable identities/counts. The exact reviewed target is included at input/I164-normal-session-exit-correspondence-1.zip. Results are independently authored by Formal-Lab[6]; Engineering's supplied controls remain inside the target and are not fresh independent observations.

Verdict: SUPPORTED within the bounded SOURCE-ONLY constructed normal session-exit contract. No residual witness in this slice. Runtime exit-chain observations and exceptional/outer-cleanup coverage remain unavailable/unexpanded. Admission remains disabled.

MANIFEST.json binds every review checkpoint member except itself. RECOVERY.md describes exact offline recovery and the forensic extra file that must remain outside strict recovered roots.
''')
(R/'RECOVERY.md').write_text('''# Verify and recover this review checkpoint

Use a new persistent directory. Preserve the original target, every failure and the forensic partial file. Do not normalize historical evidence or place the forensic extra under a strict candidate root.

1. Verify the externally reported review ZIP bytes, SHA-256, entry count and CRC. Refuse duplicate, absolute, parent-traversing, symlink, special or nonregular members. Verify exact membership and every member against this checkpoint's MANIFEST.json.
2. The included input/I164-normal-session-exit-correspondence-1.zip must be 70,593,959 bytes / 2,331 entries / SHA-256 c9c8d2106617970e8008fadc3c60f61813c64e7ce07e24a60bc92ac1029b954a. It is the unchanged input, not a recompressed replacement.
3. After inspecting code/integrity.py, its bounded recovery form is `python3 -I -B REVIEW/code/integrity.py NEW_ROOT REVIEW/input/I164-normal-session-exit-correspondence-1.zip`. This verifies archive identity, CRC, exact safe membership and all 2,330 hashes before extraction. Refuse a pre-existing destination. No implementation, database, host path or session is executed.
4. No completed suite rerun is needed to consume this review. The independently executed code snapshots, progress records, call counters and source oracle are included. The final target's documented public saved-receipt validator is `python3 -I -B NEW_ROOT/code/correspondence.py --root NEW_ROOT --receipt NEW_ROOT/results/primary/normal-session-exit-correspondence.json`. It uses saved inputs only; use the recorded Python 3.12.14 / Cryptography 50.0.2 environment. This is not new host compatibility or operational qualification.
5. `executed-code/primary` preserves the code version used by the primary review; `executed-code/processes` preserves the fresh/recovered process version. The process guard was strengthened to forbid all writes outside review outputs after the unexplained extra file was discovered. `code/` includes final audit/packaging utilities. Failed code attempts and original logs remain under failures/ and are excluded from completed counts.
6. `failures/recovered-membership/forensic-extra.bin` is the exact undeclared partial file from the first recovered root. Its original relative path and metadata are in record.json. It is preserved for review only, not an input, allowed exception to membership, or proof of origin. The failed root gates consumed no candidate code. Reconstruct that forensic layout only as a separately labeled failure root if necessary; never treat it as a valid recovery.

Strict input roots and the input archive passed final byte checks. The checkpoint records prior original-archive identities as continuity, not newly verified original outer archives. Recovered predecessor tree identities and all present required dependencies were verified. No missing compact-review original ZIP is manufactured by recompression.
''')
print(json.dumps({'report_bytes':(R/'REPORT.md').stat().st_size,'checkpoint_bytes':(R/'CHECKPOINT.json').stat().st_size,'verdict':checkpoint['verdict']}))
