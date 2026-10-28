"""Seal completed review and exact input; never execute candidate validation."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat,zipfile
b=Path(__file__).resolve().parents[1];w=b.parent
def ident(v):return {'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()}
def read(n):return json.loads((b/n).read_bytes())
primary=read('independent-primary/RESULT.json');recovered=read('independent-recovered/RESULT.json');composition=read('results/composition.json');cli=read('cli-recovered/RESULT.json');reconciliation=read('results/progress-reconciliation.json')
assert primary['result']==recovered['result']=='PASS' and primary['checks']==172 and recovered['checks']==131
for mode,r in [('primary',primary),('recovered',recovered)]:
 assert len(r['rows'])==r['checks'] and not r['failures_included'] and all(x['result'] in ('PASS','REJECTED') for x in r['rows'])
 assert read('independent-'+mode+'/core/source-audit.json')['result']=='PASS'
assert cli['exit_code']==0 and cli['stderr_bytes']==0 and cli['predecessor_derive_handle_observed']
assert reconciliation['result']=='EXACT-RECORD-RECONCILIATION' and reconciliation['unique_complete_record_start']==15 and not reconciliation['failed_rows_included_in_success_totals']
archive=w/'upload/I164-outside-catch-classification-correction-1(1).zip';raw=archive.read_bytes();pin={'bytes':60424906,'sha256':'08499f314151aef36bdbe711ad6f821bf1258d28a8c0d65fd693e3b0db4a3ba5'};assert ident(raw)==pin==read('results/integrity.json')['identity']
preserved={}
with zipfile.ZipFile(archive) as z:
 assert len(z.infolist())==1508 and z.testzip() is None;expected={n:z.read(n) for n in z.namelist()};dirs={p.as_posix() for n in expected for p in PurePosixPath(n).parents if p.as_posix()!='.'}
 for name in ('oc-input','oc-recovered'):
  root=w/name;files={};seen_dirs=set()
  def walk(p):
   for e in os.scandir(p):
    q=Path(e.path);n=q.relative_to(root).as_posix();m=e.stat(follow_symlinks=False).st_mode
    if stat.S_ISDIR(m):seen_dirs.add(n);walk(q)
    else:assert stat.S_ISREG(m),n;files[n]=q
  walk(root);assert set(files)==set(expected) and seen_dirs==dirs;assert all(p.read_bytes()==expected[n] for n,p in files.items())
  preserved[name]={'members':1508,'directories':len(dirs),'all_bytes_and_regular_exact_membership_unchanged':True}
(b/'results/preservation-after-tests.json').write_text(json.dumps(preserved,indent=2)+'\n')
for n,count in [('import-guard-attempt-1',0),('historical-record-key-attempt-1',15)]:
 d=read('failures/'+n+'/results/RESULT.json');assert d['result']=='FAIL' and d['checks']==count
counts=f"Fresh independent testing passed **{primary['checks']} primary checks in {len(primary['groups'])} completed groups and {recovered['checks']} recovered-root checks in {len(recovered['groups'])} completed groups**, plus a separate fresh-process execution of the actual current public CLI. Both contexts and the exact original current receipt passed, with no stderr. Integrity/composition checks and failed-attempt records are separate from those totals. Constructed cases and source analysis are not runtime observations."
p=b/'REPORT.md';report=p.read_text();assert report.count('{{COUNTS}}')==1;p.write_text(report.replace('{{COUNTS}}',counts))
source_audit=read('independent-primary/core/source-audit.json');assert source_audit['stages']['client-call']['source']['sha256'] in p.read_text() and source_audit['stages']['manager-call']['source']['sha256'] in p.read_text()
checkpoint={
 'checkpoint':'Formal-Lab6-I164-outside-catch-classification-correction-independent-review',
 'review_target':'I164-outside-catch-classification-correction-1.zip','input':{**pin,'entries':1508,'manifested_hashes':1507},
 'review_author':'Formal-Lab[6]','construction_author':'Engineering','author_independent':True,'implementation_modified':False,'canonical':False,
 'verdict':'SUPPORTED within stated terminal-classification contract and currently modeled paths; prior prefix-termination caveat CLOSED; original helper/storage corrections preserved',
 'residual_defect_witness':None,
 'meaning':{'true_iff':'terminal unexpected modeled raise outside the dynamically protected region of _dispatch own BaseException catch','ordinary_fixed_ClientFailure':'intentional-fixed-raise; flag false; modeled Python exception true','process_termination':'flag false; terminal Python exception not established (null)','normal_return':'flag false; no terminal exception modeled','catch_location_separate':True,'runtime_exception_and_unwind_evidence':'UNAVAILABLE','flag_is_permission_or_global_exception_absence_proof':False,'earlier_modeled_exception_or_storage_separate':True},
 'source_assessment':{'source_oracle':'independent defining AST catch membership and dynamic direct-call propagation','modeled_stages':12,'protected_region_stages':[k for k,v in source_audit['stages'].items() if v['protected']],'outside_region_stages':[k for k,v in source_audit['stages'].items() if not v['protected']],'single_flag_assignment':True,'direct_consumers':source_audit['direct_consumers'],'generic_projection_validation':'full result regeneration and equality','operational_or_admission_consumer_in_audited_sources':False,'helper_alone_validates_path_reachability_or_evidence':False},
 'witnesses':{'six_old_prefix_true_flags_reproduced':True,'prefix_termination_now_false':True,'earliest_helper_false_flag_reproduced':True,'earliest_failed_storage_false_flag_and_false_retention_reproduced':True,'unexpected_helper_and_storage_raises_now_true':True,'failed_or_terminating_storage_confirmation':None,'ordinary_fixed_raise_not_unexpected':True,'later_termination_does_not_erase_prior_conditional_storage':True,'coordinated_post_termination_continuation_rejected':True,'both_contexts':True},
 'validation':{'source_validation':True,'semantic_validation':True,'mandatory_derivation':True,'public_receipt_validation':True,'actual_predecessor_derive_handle_observed':True,'current_receipt_accepted_exact':True,'old_version_receipt_rejected':True,'coordinated_source_and_claim_changes_rejected':True,'nested_results_do_not_change_expectations':True,'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'versions':{'catalogue':'I164-CLIENT-HANDLE-STATIC-2','receipt':'I164-CLIENT-HANDLE-RETURN-CORRESPONDENCE-2','classification':'I164-CLIENT-TERMINAL-CLASSIFICATION-1'}},
 'independent_results':{'primary_checks':primary['checks'],'primary_groups':len(primary['groups']),'primary_categories':primary['categories'],'recovered_checks':recovered['checks'],'recovered_groups':len(recovered['groups']),'recovered_categories':recovered['categories'],'separate_public_CLI_process':1,'reviewer_failed_attempt_counts':[0,15],'failed_attempts_in_completed_totals':False,'progress_reconciliation':reconciliation,'constructed_cases_are_runtime_evidence':False},
 'supplied_results':{'primary_checks':131,'recovered_checks':129,'process_validation':1,'inspected_not_run':True,'failed_attempt_counts':[81,103],'failed_attempts_in_completed_totals':False,'failure_interpretations_independently_corroborated':True,'intermediate_recovery_archive_newly_verified':False,'intermediate_recovery':composition['intermediate_recovery']},
 'preservation':{'original_members_byte_identical':1282,'prior_review_non_input_records_byte_identical':171,'prior_independent_counts':[217,149],'prior_independent_CLI':1,'prior_extra_caveat_cases':6,'prior_refused_root_and_partial_bytes_preserved':True,'prior_supplied_counts':{'focused':17,'recovered':168,'process':1,'pre_correction_separate':170},'source_changes':composition['source_changes'],'exact_receipt_change_paths':composition['receipt_change_paths'],'all_other_receipt_fields_unchanged':True,'historical_sources_evidence_relationships_ordinals_and_prior_support':'PRESERVED','archival_availability_qualifications':'PRESERVED; absent historical compact dependencies not newly verified'},
 'current_receipt':composition['current_receipt'],'previous_receipt':composition['prior_receipt'],
 'environment':primary['environment'],
 'observation_limits':{'traced_invocations':18,'separate_frameless_Client_state_observer':1,'runtime_handle_return_chain':'UNAVAILABLE','actual_handle_call_count':None,'packet_inject_reference_exception_and_cleanup_observations':'UNAVAILABLE','saved_journal_rows':0,'empty_journal_is_lifetime_zero':False,'complete_interruption_or_runtime_coverage':False,'instruction_level_feasibility_established':False,'outer_callback_cleanup_projection':'PARTIAL; unchanged','new_durable_records_or_cleanup_completion':False,'missing_launcher_frame_provenance':'PRESERVED','arbitrary_Python_introspection_resistance':False,'new_host_or_wheel_byte_authentication_qualification':False},
 'boundaries':{'all_eleven_obligations':'PRESERVED','inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','accounting_reservations_nonce_ownership_uncertainty':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','admission':False},
 'operations':{'runtime_changes':False,'requests':0,'new_signatures':0,'database_connections':0,'session_operations':0,'acquisitions':0,'dependency_installation':False,'host_probe':False,'completed_suite_or_review_reruns':False,'Git_operations':False,'policy_adoption':False}}
(b/'CHECKPOINT.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
(b/'input').mkdir(exist_ok=False);(b/'input/I164-outside-catch-classification-correction-1.zip').write_bytes(raw)
members={}
for p in sorted(b.rglob('*')):
 if p.is_file():
  assert stat.S_ISREG(p.lstat().st_mode) and p.name!='MANIFEST.json';members[p.relative_to(b).as_posix()]=ident(p.read_bytes())
(b/'MANIFEST.json').write_text(json.dumps({'format':'INDEPENDENT-REVIEW-MANIFEST-1','members':members},indent=2)+'\n')
dest=w/'Formal-Lab6-I164-outside-catch-classification-correction-independent-review.zip';partial=dest.with_suffix('.zip.partial');assert not dest.exists() and not partial.exists()
with partial.open('xb') as f:
 with zipfile.ZipFile(f,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n in sorted(set(members)|{'MANIFEST.json'}):
   info=zipfile.ZipInfo(n,date_time=(2026,10,28,0,0,0));info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(b/n).read_bytes())
 f.flush();os.fsync(f.fileno())
with zipfile.ZipFile(partial) as z:assert z.testzip() is None and set(z.namelist())==set(members)|{'MANIFEST.json'}
os.replace(partial,dest);print(dest)
