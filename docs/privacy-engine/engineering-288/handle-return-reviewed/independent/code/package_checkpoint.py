"""Seal the completed current-slice review; does not execute validators."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat,zipfile
base=Path(__file__).resolve().parents[1];workspace=base.parent
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(n):return json.loads((base/n).read_bytes())
primary=read('independent-primary/RESULT.json');recovered=read('independent-recovered/RESULT.json');cli=read('cli-recovered/RESULT.json');composition=read('results/composition.json')
for name,r in [('independent-primary',primary),('independent-recovered',recovered)]:
 rows=[json.loads(x) for x in (base/name/'progress.jsonl').read_text().splitlines()]
 assert r['result']=='PASS' and r['error'] is None and r['checks']==rows and len(rows)==r['assertions'] and all(x['result'] in ('PASS','REJECTED') for x in rows)
 for label in ('coordinated journal and claims journal-derivation','coordinated journal and claims journal-semantic'):
  assert any(x['check']==label and x['error']['message']=='HANDLE-VALIDATED-JOURNAL' for x in rows)
 for label in ('mandatory state derivation actually invoked','journal expectation is fresh validated empty evidence','pristine public after nested mutations'):
  assert any(x['check']==label and x['result']=='PASS' for x in rows)
 assert read(name+'/core/source-audit.json')['result']=='PASS'
assert cli['returncode']==0 and cli['stderr_bytes']==0 and cli['answer']['runtime_handle_chain']=='UNAVAILABLE'
archive=workspace/'upload/I164-handle-return-correspondence-1(1).zip';raw=archive.read_bytes();pin={'bytes':42330497,'sha256':'6b486b1ca0c49da010face18132507020a07f3db84602d62a7c75af0305caa8e'}
assert identity(raw)==pin==read('results/integrity.json')['identity']
preservation={}
with zipfile.ZipFile(archive) as z:
 assert len(z.infolist())==1088 and z.testzip() is None
 expected={n:z.read(n) for n in z.namelist()};dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
 for name in ('hr-input','hr-recovered'):
  root=workspace/name;files={};seen_dirs=set()
  def walk(p):
   for e in os.scandir(p):
    q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
    if stat.S_ISDIR(mode):seen_dirs.add(n);walk(q)
    else:assert stat.S_ISREG(mode),(name,n);files[n]=q
  walk(root);assert set(files)==set(expected) and seen_dirs==dirs
  assert all(p.read_bytes()==expected[n] for n,p in files.items())
  preservation[name]={'exact_unchanged_regular_members':1088,'parent_directories':len(dirs),'all_source_and_evidence_bytes_unchanged':True}
(base/'results/preservation-after-tests.json').write_text(json.dumps(preservation,indent=2)+'\n')
failed=read('failures/public-key-lookup-attempt-1/results/RESULT.json');assert failed['result']=='FAIL' and failed['assertions']==7 and failed['error']['type']=='KeyError'
interrupted=read('failures/interrupted-execution-attempt-2/PRESERVATION.json');assert interrupted['progress_rows']=={'independent-primary':179,'independent-recovered':4} and interrupted['included_in_completed_totals'] is False
counts=(f"Fresh independent controls passed **{primary['assertions']} primary assertions and {recovered['assertions']} recovered-root assertions**. "
 "A separate fresh process ran the actual public CLI successfully from the separately recovered final root, with both contexts and the exact saved receipt. "
 "Totals include the independent defining-source/guard audit, full/public validation and explicitly categorized internal, authentication and constructed controls. None is runtime handle execution evidence. "
 "One reviewer harness attempt stopped after seven assertions on a missing public-key map lookup. Its exact script, source oracle and failure/results are preserved under failures/public-key-lookup-attempt-1 and excluded from completed totals. "
 "The correction uses independently source-derived public keys plus the retained observer-key fixture; no implementation changed. "
 "The execution service later disconnected during two incomplete runs. Their 179 primary and four recovered progress rows, exact scripts and available artifacts are preserved under failures/interrupted-execution-attempt-2, excluded from completed totals. Neither had a completion record and neither process remained on the subsequent check; the deeper interruption cause is UNKNOWN. "
 "Completed totals come from the subsequent shorter independently recorded groups. No new candidate defect was found by the completed controls.")
verdict=('**SUPPORTED within the bounded source-derived conditional return-correspondence contract.** '
 'The mandatory handle relation preserves exact response bytes and request/instance/evidence bindings in both contexts, rejects the focused semantic and receipt mutations, and isolates validation expectations from returned trees. '
 '**No residual defect witness was found in this scope. Runtime handle return-chain qualification remains unavailable.**')
report=(base/'REPORT.md').read_text();assert report.count('{{COUNTS}}')==report.count('{{VERDICT}}')==1
(base/'REPORT.md').write_text(report.replace('{{COUNTS}}',counts).replace('{{VERDICT}}',verdict))
cp={
 'checkpoint':'Formal-Lab6-I164-handle-return-correspondence-independent-review','review_target':'I164-handle-return-correspondence-1.zip','input':{**pin,'entries':1088,'manifested_hashes':1087},
 'review_author':'Formal-Lab[6]','construction_author':'Engineering supplied construction; not this reviewer','author_independent':True,'canonical':False,
 'verdict':'SUPPORTED within bounded source-derived conditional handle return correspondence; runtime return-chain qualification unavailable','residual_defect_witness':None,
 'source_relation':{'selector':'handle','forwarded_parameters':['packet','inject'],'default_inject':None,'backend':'Authority.handle','assignment':'result = getattr(self._live, method)(*args)','run_return':'result','wrapper_return':"self._run('handle', packet, inject)",'forwarding':'same source-defined reference; no conversion/copy','logical_type':'exact Python bytes','retained_recording_type':'lowercase bytes_hex STRING','declarations':3,'forwarding_edges':2,'readiness':'READY; live present; retired absent','normal_lock_exit_required':True,'backend_inner_handler':'Exception','outer_run_handler':'BaseException','error_response_can_return_normally':True,'failure_or_nonexecution_inferred_from_ok':False,'process_termination_is_Python_unwind':False,'independent_AST_and_guard_audit':True},
 'validation':{'mandatory_state_derivation_observed':True,'predecessor_exact_receipt_required':True,'journal_value_comparison_before_whole_evidence_gate':True,'coordinated_semantic_and_derivation_rejection':'HANDLE-VALIDATED-JOURNAL','returned_nested_trees_do_not_change_expectations':True,'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'conditional_projector_is_evidence_admission_API':False,'new_authentication_signatures':0,'fixture_bytes_exact_and_signatures_independently_verified':True},
 'independent_results':{'primary_assertions':primary['assertions'],'primary_categories':primary['categories'],'primary_completed_groups':len(primary['groups']),'recovered_assertions':recovered['assertions'],'recovered_categories':recovered['categories'],'recovered_completed_groups':len(recovered['groups']),'fresh_offline_CLI_processes':1,'failed_attempt_assertions':[7],'interrupted_attempt_progress_rows':[179,4],'failed_or_interrupted_attempts_in_completed_totals':False,'constructed_cases_are_execution_evidence':False},
 'supplied_results':{'primary':101,'additional_internal':21,'recovered':101,'process_check':1,'inspected_not_executed':True,'prior_membership_failure_assertions':[0,0],'failed_attempts_in_completed_totals':False,'intermediate_recovery_archive_entries':1068,'intermediate_outer_archive_newly_verified':False},
 'identities':{'current_code':primary['source'],'new_receipt':composition['current_receipt'],'unchanged_state_receipt':composition['prior_receipt']},
 'preservation':{'state_members_byte_identical':1016,'prior_review_included_records_byte_identical':33,'exact_prior_review':composition['exact_predecessor_review'],'compact_omission':'Only redundant embedded state input ZIP','historical_external_archival_dependencies':'Documented unchanged; not executable dependencies','prior_functions_AST_identical':48,'other_top_level_AST_identical':True,'new_producer_functions':composition['new_functions'],'prior_context_fields_unchanged':True,'historical_evidence_relationships_ordinals_and_prior_closures':'PRESERVED','prior_failed_records_and_bytes':'PRESERVED; causes UNKNOWN; original-root retention remains supplied assertion','implementation_modified':False},
 'observation_limits':{'actual_handle_three_link_execution_chain':'UNAVAILABLE','actual_handle_call_count':None,'packet_observation':None,'inject_observed':False,'inject_unknown_is_observed_None':False,'underlying_response_observation':None,'run_result_observation':None,'wrapper_return_observation':None,'saved_journal_rows':0,'zero_saved_rows_are_lifetime_zero':False,'captured_handle_calls_in_saved_trace':0,'physical_result_or_connection_identity':None,'traced_invocations':18,'separate_observer_Client_state_call':1,'observer_frame':None,'observer_join_to_handle_links':None,'complete_runtime_or_repetition_coverage':False,'method_specific_action_semantics_reproved':False,'exhaustive_interrupt_feasibility_proven':False,'missing_launcher_frames_and_prior_observation_limits':'PRESERVED'},
 'environment':primary['environment'],
 'boundaries':{'all_eleven_obligations':'PRESERVED','inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','accounting_reservations_nonce_ownership_uncertainty':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','admission':False},
 'operations':{'runtime_changes':False,'new_acquisition':False,'requests_issued':0,'new_signatures':0,'session_operations':0,'database_connections':0,'completed_suite_or_review_reruns':False,'smoke_pipeline_lifecycle_reruns':False,'Git_operations':False,'policy_adoption':False}}
(base/'CHECKPOINT.json').write_text(json.dumps(cp,indent=2)+'\n')
(base/'input').mkdir(exist_ok=False);(base/'input/I164-handle-return-correspondence-1.zip').write_bytes(raw)
members={}
for p in sorted(base.rglob('*')):
 if p.is_file():
  assert stat.S_ISREG(p.lstat().st_mode) and p.name!='MANIFEST.json';members[p.relative_to(base).as_posix()]=identity(p.read_bytes())
(base/'MANIFEST.json').write_text(json.dumps({'format':'INDEPENDENT-REVIEW-MANIFEST-1','members':members},indent=2)+'\n')
dest=workspace/'Formal-Lab6-I164-handle-return-correspondence-independent-review.zip';partial=dest.with_suffix('.zip.partial');assert not dest.exists() and not partial.exists()
with partial.open('xb') as h:
 with zipfile.ZipFile(h,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n in sorted(set(members)|{'MANIFEST.json'}):
   info=zipfile.ZipInfo(n,date_time=(2026,10,28,0,0,0));info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(base/n).read_bytes())
 h.flush();os.fsync(h.fileno())
with zipfile.ZipFile(partial) as z:assert z.testzip() is None and set(z.namelist())==set(members)|{'MANIFEST.json'}
os.replace(partial,dest);print(dest)
