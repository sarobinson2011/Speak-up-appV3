"""Seal completed independent review records; no validator is executed here."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat,zipfile
base=Path(__file__).resolve().parents[1];workspace=base.parent
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(n):return json.loads((base/n).read_bytes())
primary=read('independent-primary/RESULT.json');recovered=read('independent-recovered/RESULT.json');cli=read('cli-recovered/RESULT.json');composition=read('results/composition.json')
for name,r in [('independent-primary',primary),('independent-recovered',recovered)]:
 rows=[json.loads(x) for x in (base/name/'progress.jsonl').read_text().splitlines()]
 assert r['result']=='PASS' and r['error'] is None and r['checks']==rows and len(rows)==r['assertions'] and all(x['result'] in ('PASS','REJECTED') for x in rows)
 assert any(x['check']=='coordinated journal and claims journal-derivation' and x['error']['message']=='HANDLE-VALIDATED-JOURNAL' for x in rows)
 for label in ('mandatory handle derivation actually invoked','journal expectation is fresh validated empty evidence','pristine public after nested mutations'):
  assert any(x['check']==label and x['result']=='PASS' for x in rows)
 assert read(name+'/core/source-audit.json')['result']=='PASS'
assert cli['returncode']==0 and cli['stderr_bytes']==0 and cli['answer']['runtime_client_handle_chain']=='UNAVAILABLE'
assert read('results/recovery-gates.json')['result']=='PASS'
archive=workspace/'upload/I164-client-handle-return-correspondence-1(1).zip';raw=archive.read_bytes();pin={'bytes':43439616,'sha256':'1f7b1c7dc58949e76f73cac68afb00ea0373490ac0c07bdada86d954772b4431'}
assert identity(raw)==pin==read('results/integrity.json')['identity']
preservation={}
with zipfile.ZipFile(archive) as z:
 assert len(z.infolist())==1282 and z.testzip() is None
 expected={n:z.read(n) for n in z.namelist()};dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
 for name in ('ch-input','ch-recovered-2'):
  root=workspace/name;files={};seen_dirs=set()
  def walk(p):
   for e in os.scandir(p):
    q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
    if stat.S_ISDIR(mode):seen_dirs.add(n);walk(q)
    else:assert stat.S_ISREG(mode),(name,n);files[n]=q
  walk(root);assert set(files)==set(expected) and seen_dirs==dirs
  assert all(p.read_bytes()==expected[n] for n,p in files.items())
  preservation[name]={'exact_unchanged_regular_members':1282,'parent_directories':len(dirs),'all_source_and_evidence_bytes_unchanged':True}
(base/'results/preservation-after-tests.json').write_text(json.dumps(preservation,indent=2)+'\n')
failure=read('failures/recovered-root-membership/PRESERVATION.json');assert failure['completed_assertions']==0 and failure['included_in_completed_totals'] is False and failure['cause']=='UNKNOWN'
item=failure['unexpected'][0];b=(base/'failures/recovered-root-membership'/item['preserved']).read_bytes();assert identity(b)=={k:item[k] for k in ('bytes','sha256')};assert b==(workspace/'ch-recovered'/item['path']).read_bytes()
counts=(f"Fresh independent controls passed **{primary['assertions']} primary assertions in {len(primary['groups'])} completed groups and {recovered['assertions']} recovered-root assertions in {len(recovered['groups'])} completed groups**. "
 "A separate fresh process ran the actual public CLI from the independently recovered final root, accepted both contexts and the exact original receipt, and produced no stderr. "
 "Integrity/composition and strict-root gate checks are recorded separately from these assertion totals. "
 "The totals distinguish independent source/evidence assertions, source negatives, constructed controls and old-version witness reproductions. Constructed results are not runtime observations. "
 "Fresh entry-process exit codes, exact results and call observations are retained for inspection. No completed predecessor suite was rerun.")
verdict=('**SCOPED SUPPORT for source-derived general-client handle forwarding and mandatory saved-evidence validation in both contexts.** '
 'The original helper/storage classification witness has the corrected disposition; exact bytes, argument routing and validated predecessor provenance are preserved, and focused semantic/derivation/public substitutions reject. '
 '**This is not complete runtime or interruption-classification qualification.** The conditional outside_catch_failure flag retains a stage-dependent process-termination interpretation caveat, detailed below; it must not be used alone to establish a Python exception or unwind. No residual false actual-evidence receipt acceptance was found.')
report=(base/'REPORT.md').read_text();assert report.count('{{COUNTS}}')==report.count('{{VERDICT}}')==1
(base/'REPORT.md').write_text(report.replace('{{COUNTS}}',counts).replace('{{VERDICT}}',verdict))
cp={
 'checkpoint':'Formal-Lab6-I164-client-handle-return-correspondence-independent-review','review_target':'I164-client-handle-return-correspondence-1.zip','input':{**pin,'entries':1282,'manifested_hashes':1281},
 'review_author':'Formal-Lab[6]','construction_author':'Engineering supplied construction; not this reviewer','author_independent':True,'canonical':False,
 'verdict':'SCOPED SUPPORT for source-derived general-client handle forwarding and mandatory saved-evidence validation; original witness corrected; runtime and uniform interruption-flag classification not qualified',
 'residual_false_actual_evidence_acceptance_witness':None,
 'remaining_interpretation_witness':{'kind':'conditional classification ambiguity, not actual evidence acceptance','smallest_outcomes':{'client-call':'process-termination'},'manager_case':None,'callback_and_cleanup':'unobserved','completion':'process-termination','outside_catch_failure':True,'original_exception':None,'fixed_client_failure':None,'destinations':[],'retained_original':False,'comparison':'retain-error and fixed-failure process-termination return False for outside_catch_failure','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'records':'independent-primary/core/constructed-paths.json','Python_unwind_established':False,'runtime_feasibility_established':False,'meaning_requires_clarification_before_use_as_exception_classifier':True,'additional_prefix_cases':6,'additional_records':'results/classification-caveat.json','additional_cases_in_primary_or_recovered_assertion_totals':False},
 'source_relation':{'route':['ManagedAuthority.handle','ManagedSession.handle','_dispatch','Client.handle'],'client_selector':'handle','packet_exact_type':'bytes','response_exact_type':'bytes','manager_default_inject':None,'default_is_observed_value':False,'new_declarations':4,'ordered_value_hops':5,'argument_hops':3,'conditional_reference_edges':4,'forwarding':'same source-defined result reference; exact bytes without normalization','normal_error_response_preserved':True,'dispatch_handler':'BaseException inside try only','original_error':'owner.failure and conditional trusted launcher cleanup/evidence route','fixed_failure':'ClientFailure from None; exact source message','failure_record':'existing launcher evidence only; best effort, no observed bytes or durability','independent_AST_guards_and_order_audit':True},
 'validation':{'mandatory_handle_derivation_observed':True,'exact_predecessor_receipt_required':True,'journal_expectation_fresh_from_validated_predecessor':True,'coordinated_semantic_and_derivation_rejection':'HANDLE-VALIDATED-JOURNAL','returned_nested_trees_do_not_change_expectations':True,'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'conditional_projector_is_evidence_admission_API':False,'new_authentication_signatures':0,'retained_authentication_fixtures':'reused from reviewed handle predecessor; constructed only'},
 'original_classification_witness':{'affected_producer':{'bytes':150190,'sha256':'8bb35aef7eab4f53885e343ecc290cd26eef2d8c23d7c296ae65db2d1207780c'},'independently_reproduced':True,'both_contexts':True,'old_output_exact_original_context':True,'fixed_helper_raise':{'old_outside_catch_failure':False,'current_outside_catch_failure':True,'completion':'unqualified-escape','fixed_publication_established':False},'adjacent_storage_raise':{'old_retained_original':False,'current_retained_original':None,'current_outside_catch_failure':True},'old_submitted_classification_rejected':True,'runtime_execution':False},
 'independent_results':{'primary_assertions':primary['assertions'],'primary_categories':primary['categories'],'primary_completed_groups':len(primary['groups']),'recovered_assertions':recovered['assertions'],'recovered_categories':recovered['categories'],'recovered_completed_groups':len(recovered['groups']),'fresh_offline_CLI_processes':1,'strict_gate_checks':'two legitimate roots accepted; refused root rejected before predecessor code; undeclared bytes unchanged','failed_attempt_assertions':[0],'failed_attempts_in_completed_totals':False,'constructed_cases_are_execution_evidence':False},
 'supplied_results':{'corrected_focused':17,'corrected_recovered':168,'process_check':1,'pre_correction':170,'pre_correction_counts_are_current_coverage':False,'interrupt_delivery':'supplied attempted interrupt did not reach campaign; campaign completed','inspected_not_executed':True,'intermediate_recovery_archive':{'bytes':43294871,'entries':1258,'sha256':'4345d906c90442afa062a72f3793d1a17297d0e58cd108f0cf63afc6ca7c7fbd','outer_archive_newly_verified':False},'independent_recovery_used_final_input':True},
 'identities':{'current_code':primary['source'],'current_receipt':identity((workspace/'ch-input/results/client-handle-correspondence.json').read_bytes()),'unchanged_handle_receipt':identity((workspace/'ch-input/retained/handle/results/handle-correspondence.json').read_bytes())},
 'preservation':{'handle_predecessor_members_byte_identical':1088,'prior_review_records_byte_identical':141,'exact_prior_review':composition['exact_prior_review'],'compact_omission':composition['omitted_redundant_input'],'prior_functions_AST_identical':55,'other_top_level_AST_identical':True,'new_functions':composition['new_functions'],'prior_context_fields_unchanged':True,'historical_sources_evidence_relationships_ordinals_and_prior_closures':'PRESERVED','historical_external_archival_dependencies':'Original documented scope retained; not all archival outer ZIPs newly available/verified','refused_root':'left unchanged; undeclared regular bytes separately preserved; cause UNKNOWN','implementation_modified':False},
 'observation_limits':{'runtime_client_handle_chain':'UNAVAILABLE','actual_client_handle_call_count':None,'captured_client_forwarding_calls':0,'packet_observation':None,'inject_observed':False,'reference_identity_observations':None,'original_exception_observation':None,'fixed_failure_observation':None,'response_return_links':None,'saved_journal_rows':0,'empty_saved_journal_is_lifetime_zero':False,'traced_invocations':18,'separate_observer_Client_state_call':1,'observer_frame':None,'observer_join_to_handle_chain':None,'physical_connection_or_object_identity':None,'failure_record_bytes':None,'durability_established':False,'complete_runtime_or_repetition_coverage':False,'instruction_level_interruption_feasibility':False,'trusted_process_boundary':'PRESERVED; no arbitrary Python introspection protection','missing_launcher_frames_and_other_prior_limits':'PRESERVED'},
 'environment':primary['environment'],
 'boundaries':{'all_eleven_obligations':'PRESERVED','inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','accounting_reservations_nonce_ownership_uncertainty':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','admission':False},
 'operations':{'implementation_changes':False,'requests_issued':0,'new_signatures':0,'database_connections':0,'session_operations':0,'new_acquisition':False,'dependency_changes':False,'completed_suite_or_review_reruns':False,'smoke_pipeline_lifecycle_reruns':False,'Git_operations':False,'policy_adoption':False}}
(base/'CHECKPOINT.json').write_text(json.dumps(cp,indent=2)+'\n')
(base/'input').mkdir(exist_ok=False);(base/'input/I164-client-handle-return-correspondence-1.zip').write_bytes(raw)
members={}
for p in sorted(base.rglob('*')):
 if p.is_file():
  assert stat.S_ISREG(p.lstat().st_mode) and p.name!='MANIFEST.json';members[p.relative_to(base).as_posix()]=identity(p.read_bytes())
(base/'MANIFEST.json').write_text(json.dumps({'format':'INDEPENDENT-REVIEW-MANIFEST-1','members':members},indent=2)+'\n')
dest=workspace/'Formal-Lab6-I164-client-handle-return-correspondence-independent-review.zip';partial=dest.with_suffix('.zip.partial');assert not dest.exists() and not partial.exists()
with partial.open('xb') as h:
 with zipfile.ZipFile(h,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n in sorted(set(members)|{'MANIFEST.json'}):
   info=zipfile.ZipInfo(n,date_time=(2026,10,28,0,0,0));info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(base/n).read_bytes())
 h.flush();os.fsync(h.fileno())
with zipfile.ZipFile(partial) as z:assert z.testzip() is None and set(z.namelist())==set(members)|{'MANIFEST.json'}
os.replace(partial,dest);print(dest)
