from pathlib import Path
import json,hashlib,ast
B=Path('/workspace/scratch/3da0de3fef10');r=B/'git-token-registration';s=r/'selection';s.mkdir(exist_ok=False)
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def put(n,b):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists();p.write_bytes(b)
mapping={};omitted=[]
for label,root in [('extension',r/'target'),('independent-review',r/'review')]:
 for p in sorted(root.rglob('*')):
  if not p.is_file():continue
  n=p.relative_to(root).as_posix()
  if label=='extension' and n.startswith('retained/'):continue
  raw=p.read_bytes();out=label+'/'+n
  receipt=out=='extension/results/primary/token-registration-correspondence.json'
  if len(raw)>524288 and not receipt or p.suffix in ('.zip','.bin','.db','.sqlite'):
   omitted.append({'selection_path':out,'source_path':p.relative_to(r).as_posix(),'identity':identity(raw),'disposition':'Exact bytes remain in the external independent review / embedded target. Compact Git selection is not a runnable recovery root.'});continue
  put(out,raw);mapping[out]={'source_path':p.relative_to(r).as_posix(),'identity':identity(raw)}
put('provenance/input-verification.json',(r/'verification.json').read_bytes())
priorraw=(B/'git-token-registration-tools/prior-save-receipt.json').read_bytes();assert len(priorraw)==3613 and priorraw.endswith(b'\n\n');priorraw=priorraw[:-1];prior=json.loads(priorraw);assert prior['status']=='PASS' and prior['push_status']=='CONFIRMED' and prior['commit']=='c392939e82734dac5b2f5e965933bc2c834f152a'
put('provenance/prior-internal-status-save.json',priorraw)
for name in ('prospective_entry.py','lab_bootstrap.py','live_connection.py','smoke_occurrences.py'):
 hits=list((r/'target').rglob(name));assert hits
 pins={identity(p.read_bytes())['sha256'] for p in hits}
 # Different historical copies are qualified; select the current source or the
 # exact SOC-closed occurrence adapter referenced by the mandatory chain.
 if name=='smoke_occurrences.py':p=next(p for p in hits if identity(p.read_bytes())['sha256']=='5cc79baac1813284768fcc79cc1cf00d50b3febe02ea6947511ddc8b7427d05b')
 else:
  want={'prospective_entry.py':'a1d80c523ae220228a6b27cac42b5e57a006336e858a8e7db0a75355d6cf2ae9','lab_bootstrap.py':'245d4f36d687834aeee064a60d4414b15f7b8babfdb5dec192aa995d93af2b78','live_connection.py':'7344170ca01a2dbbd3afbeb4a6a55c0b95db0edb1a8d74e4fa4638b6dcfc6da5'}[name]
  p=next(p for p in hits if identity(p.read_bytes())['sha256']==want)
 raw=p.read_bytes();n='source-evidence/'+name;put(n,raw);mapping[n]={'source_path':p.relative_to(r).as_posix(),'identity':identity(raw)}
producer=r/'target/code/managed_coverage.py';validator=r/'target/code/correspondence.py'
functions={n.name:{'line':n.lineno,'end_line':n.end_lineno} for n in ast.parse(producer.read_bytes()).body if isinstance(n,ast.FunctionDef)}
context=json.loads((r/'target/results/primary/token-registration-correspondence.json').read_bytes())
inspection={'method':'Read-only exact source, AST, saved receipt and mandatory-validator inspection. No code imports, validator/test/review execution or session operation.',
 'producer':identity(producer.read_bytes()),'validator':identity(validator.read_bytes()),'source_files':{n:v for n,v in mapping.items() if n.startswith('source-evidence/')},
 'existing_coverage':{n:functions[n] for n in ['client_handle_source','client_handle_projection','client_state_projection','reference_source','constructed_reference_path','token_registration_source','compile_token_registration','token_registration_projection']},
 'mandatory_path':['validate -> derive -> derive_token -> _checked -> _basis','_basis -> retained IS-01 derive_status -> earlier reviewed mandatory chain','catalogue -> compile_token_registration -> token_registration_source','constructed_projection -> _checked -> _construct_checked -> token_registration_projection'],
 'already_covered':['Exact _run AST and normal launcher statement order (client_handle_source, lines 1427-1428)','ManagedAuthority close/_dispose reference-transfer paths (constructed_reference_path)','Saved close frame, nested backend close, instance binding, handoff-before-close and confirmed-close records (SOC-closed smoke_occurrences.semantic, lines 238-292)','Invocation-specific registry registration and normal pop completion (token_registration_projection); continuity premise required for selected-owner removal'],
 'precise_gap':'No executable invocation-specific normal-exit composition connects the completed _run pop to resumption through session/_session, close of the same yielded manager, post-close local managed=None, and subsequent ACTIVE unlink. Current token projector stops at normal-pop-completion. Existing client projections consume cleanup only in retained-original/fixed-failure cases; normal-success cleanup remains unobserved. Separate source-shape checks and saved close facts do not supply this constructed composition.',
 'proposed_task':'One bounded normal session-exit correspondence in both contexts: completed pop -> launcher resumption -> selected managed.close normal completion -> local managed reference clear -> ACTIVE unlink attempt/completion. Reuse existing close/reference and saved-close checks. Preserve abrupt/unknown frontiers without extending a complete exceptional lifecycle.',
 'source_requirements':{'prospective_entry.py':[173,174,186,188],'lab_bootstrap.py':[164,165,166,167,173,185,186],'live_connection.py':[57,58,59,60]},
 'saved_limits':{'new_token_registration_limits':context['new_token_registration_limits'],'outer_callback_cleanup_projection':context['new_client_state_limits']['outer_callback_cleanup_projection']},
 'retained_sources_suffice_for_constructed_relation':True,'new_operating_authority_required_for_static_construction':False,'missing_runtime_evidence_is_not_an_implementation_defect':True,'next_task_implemented':False}
put('provenance/next-task-source-inspection.json',enc(inspection))
cp=json.loads((r/'review/CHECKPOINT.json').read_bytes());v=json.loads((r/'verification.json').read_bytes())
prov={'milestone':'Reviewed normal _run token registration/callback-to-revocation correspondence','review':v['review'],'target':v['target'],'verdict':cp['verdict'],'independent':{'controls':238,'fresh_recovered_CLI':1,'groups':cp['independent_groups'],'failed_attempts_excluded':cp['failed_attempts_excluded']},'supplied':cp['supplied_results_inspected_not_rerun'],'counts_separate':True,'selected_owner_continuity_premise':'Required; conditional not qualified','prior_internal_status_save':{'status':prior['status'],'push_status':prior['push_status'],'commit':prior['commit'],'remote_main':prior['remote_main'],'prefix':prior['prefix'],'selection':prior['selection'],'receipt_library_file_id':'libfile_c1e985dcd52081919ad3b175fe9b0341','repeat_save':False},'reuse_check':'No exact new token-registration receipt returned by Library title search. Host command checks matching receipts and exact already-committed selections before writing; no host state inferred from that search.','observation_limits':cp['observation_limits'],'boundaries':cp['boundaries'],'prior_support':'IS-01 and previous scoped support preserved in exact retained predecessor; 207 corrected and 14 witness checks not merged into new counts; prior failed 153-check attempt remains excluded','operations_this_preparation':{'test_runs':0,'review_runs':0,'pipeline_runs':0,'acquisitions':0,'database_connections':0,'session_operations':0,'Git_commits_or_pushes':0,'next_task_implemented':False}}
put('REVIEW-PROVENANCE.json',enc(prov))
put('provenance/selection-origin-map.json',enc(mapping));put('provenance/external-only-records.json',enc(omitted))
put('README.md',b'''# Reviewed normal token registration correspondence

Independent support is incorporated within the constructed normal-path contract. Formal-Lab[6]'s 238 completed independent controls and one fresh recovered CLI pass remain separate from Engineering's 285 primary, 14 fresh-process, 50 recovered-root checks and separate CLI. The reviewer source-fragment attempt (11 checks) and diff-audit attempt (zero completed controls) remain preserved and excluded. Prior support and failures are unchanged.

Finally entry, removal attempt and normal completion remain distinct. Selected-owner removal requires explicit conditional registry continuity. Normal pop with UNKNOWN continuity remains admitted without claiming selected-owner removal. Earlier established prefix facts survive later uncertainty. This is no runtime continuity, physical-reference, revocation, exclusivity or durability qualification. Runtime observations remain unavailable; observer unjoined; exceptional and outer-cleanup gaps remain.

This compact Git selection contains the newly reviewed source, exact current receipt, focused supplied and independent records, provenance and recovery instructions. It is not a runnable full recovery root. Large archives, inherited evidence and omitted duplicate large records remain in the exact external review archive; see RECOVERY.md and provenance/external-only-records.json. No evidence deletion or summary substitution is authorized.

The prepared host command reuses matching successful receipts or committed selections; otherwise it saves only this selection. It preserves unrelated work and verifies the already-saved internal-status milestone. No tests, reviews, pipelines, acquisitions, database connections, sessions or previous Git saves are repeated. NEXT-TASK.md records one unimplemented construction task only.

All eleven obligations, four inventory and fourteen lifetime UNKNOWN totals, Decision B, retention, allowances and uncertainty protections persist. SOURCE-ONLY unchanged; cumulative-envelope unadopted; readiness/final binding blocked; admission disabled.
''')
put('RECOVERY.md',b'''# Compact save recovery

Retain Formal-Lab6-I164-token-registration-independent-review.zip outside Git (a browser duplicate suffix is accepted only with the same bytes). Exact identity: 68,072,093 bytes; 83 entries; SHA-256 f83ef3276c5c2e10b2bc90ee3b95a1703b2b1de57a89c0fcdd3448635aa85641. It contains input/I164-token-registration-correspondence-1.zip: 69,308,990 bytes; 2,178 entries; SHA-256 84c714c62aa6aa3956e5b137d03e584b055c06b26200b6768090ad33a5e4dbeb.

For separately authorized future recovery, verify both archive identities, CRC, safe exact membership and manifested hashes before extraction to a new persistent directory. Preserve failed roots; no overlay, repair or retry. Recover the full embedded target, then follow its original START-HERE.md and RECOVERY.md. Its current receipt is results/primary/token-registration-correspondence.json, also retained exactly under extension/ here (3,328,177 bytes; SHA-256 1184bbf9366a2c7a8ced902836566b6610a8844cbf97698e78d10e6e91107145).

Do not run validators against this compact Git selection. The full retained/status and older dependency trees are in the embedded target and remain unchanged. Historical compact/forensic manifests and omitted outer-archive qualifications remain as recorded. The supplied intermediate recovery archive is a continuity identity in the independent review; the reviewer recovered the final requested target. This preparation verifies the supplied outer review and its exact embedded final target, without relabeling historical archive qualifications or rerunning controls.

provenance/selection-origin-map.json binds every copied source record to its exact verified path and identity. provenance/external-only-records.json lists intentionally uncommitted large records. Review failure files are preserved; counts stay separate. No omission from Git authorizes deletion, compaction, substitution or relaxation of recovery/evidence duties.

Prior internal-status/IS-01 save already completed: c392939e82734dac5b2f5e965933bc2c834f152a, prefix docs/privacy-engine/engineering-288/internal-status-return-reviewed, 357 files, selection manifest 59,809 bytes / SHA-256 359e99b43d670af86438b378fe06f2767d65f6176d511826c2bfe3e207ea4526. The exact host receipt is preserved under provenance/. The new command requires this milestone unchanged and reuses any matching token-registration save; no force or automatic retry.

Completed review/control scripts are retained evidence, not permission to execute them. No operation or admission follows from recovery. All obligations and boundaries remain unchanged.
''')
put('NEXT-TASK.md',b'''# Smallest unfinished source-supported construction

One bounded normal session-exit correspondence: compose the selected _run invocation's completed token-pop continuation with the same launcher's managed close, local reference clear and ACTIVE-marker removal, in both symbolic contexts. Not implemented or authorized by this save.

Exact defining sources:
- prospective_entry.py (9,485 bytes; SHA-256 a1d80c523ae220228a6b27cac42b5e57a006336e858a8e7db0a75355d6cf2ae9): line 173 enters launcher.session; line 174 binds owner.wrapper to the yielded wrapper; lines 186-188 place token pop before leaving that context.
- lab_bootstrap.py (11,481 bytes; SHA-256 245d4f36d687834aeee064a60d4414b15f7b8babfdb5dec192aa995d93af2b78): session lines 185-186 forwards _session's yielded wrapper. _session lines 164-166 resumes after the yield, calls managed.close(), clears the local managed reference only after normal close continuation, then unlinks ACTIVE.json. Lines 167-176 retain the distinct failure path, including keeping ACTIVE despite best-effort cleanup.
- live_connection.py (5,717 bytes; SHA-256 7344170ca01a2dbbd3afbeb4a6a55c0b95db0edb1a8d74e4fa4638b6dcfc6da5): close lines 57-60 quarantines/disposes before publishing the normal CLOSED state; its existing reference/close checks must be reused.

Already covered, and not proposed for reimplementation: client_handle_source lines 1427-1428 checks the exact normal launcher statement order. constructed_reference_path already covers manager close/_dispose reference behavior. The SOC-closed smoke_occurrences.semantic lines 238-292 validates saved launcher/manager/backend close frame relationships, handoff-before-close, instance bindings and the exact confirmed-close record. The new token_registration_projection (lines 2000-2040) enforces the normal token path and stops at normal-pop-completion. Its database_cleanup_completion stays None. Existing client handle/state projections only consume their cleanup premises on retained-original fixed-failure paths; otherwise cleanup premises stay unobserved.

The precise missing executable composition is therefore the same-invocation, same-wrapper/manager normal-exit relation across those already checked pieces. The mandatory current validator calls derive_token -> _checked -> _basis -> reviewed derive_status and compiles the token catalogue; neither its rows nor its constructed entry composes pop completion with launcher resumption, selected managed close, subsequent local clear and marker unlink. Source-shape coverage and separately validated smoke close facts do not supply this static/constructed relation. This was checked in the actual source/producer/validator and saved receipt, without executing them.

The retained source suffices. The proposed slice should distinguish calling close from its normal completion, clearing a local reference from closing a connection, and unlink attempt from completion. A missing/raising/terminated continuation must stop without inventing successful removal, normal context exit, Python unwind, durable closure, obligation discharge or renewed authority. Preserve earlier independently established facts, the token continuity premise and existing exact evidence. Reuse existing exceptional checks; do not expand into a complete outer lifecycle.

This is unfinished construction, not a claimed runtime defect and not a consequence inferred solely from unavailable observations. Runtime token-to-close joins, local managed-clear/unlink observations and operational continuity remain unavailable. Their absence does not block the conditional construction and must not be filled with fabricated frames. Any later runtime-evidence claim would require a separately authorized capture contract and actual execution evidence from the integration/capture owner, plus relevant operator/storage qualification; Steve's project designation alone cannot supply those facts.

No implementation, new collection or qualification is performed here. All eleven obligations, four inventory and fourteen lifetime UNKNOWN totals, Decision B, retention, allowances and existing boundaries remain; cumulative-envelope unadopted; SOURCE-ONLY; readiness/final binding blocked; admission disabled.
''')
files={p.relative_to(s).as_posix():p.read_bytes() for p in s.rglob('*') if p.is_file()}
put('SELECTION-MANIFEST.json',enc({'format':'I164-COMPACT-REVIEWED-SELECTION-1','members':{n:identity(b) for n,b in sorted(files.items())}}))
files={p.relative_to(s).as_posix():p.read_bytes() for p in s.rglob('*') if p.is_file()}
info={'files':len(files),'bytes':sum(map(len,files.values())),'manifest':identity(files['SELECTION-MANIFEST.json']),'large_archives_included':False,'database_included':False,'previous_milestones_modified':False}
(r/'selection-identity.json').write_bytes(enc(info));print(json.dumps(info,indent=2))
