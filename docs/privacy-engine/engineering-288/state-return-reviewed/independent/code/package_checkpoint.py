"""Seal completed current-slice review evidence without rerunning tests."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat,zipfile
base=Path(__file__).resolve().parents[1];workspace=base.parent
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(n):return json.loads((base/n).read_bytes())
primary=read('independent-primary/RESULT.json');recovered=read('independent-recovered/RESULT.json');cli=read('cli-recovered/RESULT.json');composition=read('results/composition.json')
for name,r in [('independent-primary',primary),('independent-recovered',recovered)]:
 rows=[json.loads(x) for x in (base/name/'progress.jsonl').read_text().splitlines()]
 assert r['result']=='PASS' and r['error'] is None and r['checks']==rows and len(rows)==r['assertions'] and all(x['result'] in ('PASS','REJECTED') for x in rows)
 for label in ('coordinated HEAD semantic comparison','coordinated HEAD derivation comparison','coordinated three-value reports both contexts'):
  assert any(x['check']==label and x['error']['message']=='STATE-VALUE-ORIGIN:/head' for x in rows)
 for label in ('mandatory config predecessor actually invoked','HEAD comparison used validated original expectation','pristine public after nested mutations'):
  assert any(x['check']==label and x['result']=='PASS' for x in rows)
assert cli['returncode']==0 and cli['stderr_bytes']==0 and cli['answer']['runtime_state_chain']=='UNAVAILABLE'
assert read('results/type-origin.json')['result']=='PASS'
archive=workspace/'upload/I164-state-return-correspondence-1(1).zip';raw=archive.read_bytes();pin={'bytes':41935972,'sha256':'44942004491d883af8c422f10dd38fd1e25cbc4f56e2d53e6345e264d0893fdc'}
assert identity(raw)==pin==read('results/integrity.json')['identity']
preservation={}
with zipfile.ZipFile(archive) as z:
 assert len(z.infolist())==1016 and z.testzip() is None
 expected={n:z.read(n) for n in z.namelist()};dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
 for name in ('st-input','st-recovered'):
  root=workspace/name;files={};seen_dirs=set()
  def walk(p):
   for e in os.scandir(p):
    q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
    if stat.S_ISDIR(mode):seen_dirs.add(n);walk(q)
    else:assert stat.S_ISREG(mode),(name,n);files[n]=q
  walk(root);assert set(files)==set(expected) and seen_dirs==dirs
  assert all(p.read_bytes()==expected[n] for n,p in files.items())
  preservation[name]={'exact_unchanged_regular_members':1016,'parent_directories':len(dirs),'all_source_and_evidence_bytes_unchanged':True}
(base/'results/preservation-after-tests.json').write_text(json.dumps(preservation,indent=2)+'\n')
counts=(f"Fresh independent controls passed **{primary['assertions']} primary assertions and {recovered['assertions']} recovered-root assertions**. "
 "One separate fresh process ran the actual current public CLI successfully with both contexts and the exact saved receipt. "
 "The assertion totals include the independent defining-source audit and explicitly labelled constructed and internal-relation controls. A separate static initial-HEAD type-origin check also passed. None is a runtime observation. "
 "All independent controls completed without a candidate defect; no supplied counts or failed attempts are included in these totals.")
report=(base/'REPORT.md').read_text();assert report.count('{{COUNTS}}')==1;(base/'REPORT.md').write_text(report.replace('{{COUNTS}}',counts))
cp={
 'checkpoint':'Formal-Lab6-I164-state-return-correspondence-independent-review','review_target':'I164-state-return-correspondence-1.zip','input':{**pin,'entries':1016,'manifested_hashes':1015},
 'review_author':'Formal-Lab[6]','construction_author':'SU-Engineering[288D]','author_independent':True,'canonical':False,
 'verdict':'SUPPORTED for bounded source-derived conditional state forwarding at the validated saved recovery frontier','defect_witness':'None found in focused independent controls; runtime return-chain evidence remains unavailable',
 'source_relation':{'selector':'state','arguments':[],'backend':'Authority.state','assignment':'result = getattr(self._live, method)(*args)','run_return':'result','wrapper_return':"self._run('state')",'forwarding':'same source-defined reference; no wrapper copy','declarations':3,'forwarding_edges':2,'types':'exact inherited HEAD object and exact recursively typed separately validated finite state','readiness':'READY; live present; retired absent','normal_exit_required':True,'caught_stages':['pre_transaction','dispatch','post_transaction','return_expression'],'outside_handler':['lock_enter','readiness','lock_exit'],'reason_before_quarantine':True,'quarantine_interruption_effects':'UNKNOWN','wrapper_checker_source_read_not_executed':True,'independent_AST_and_guard_audit':True},
 'validation':{'mandatory_config_derivation_observed':True,'predecessor_exact_receipt_required':True,'HEAD_type_value_comparison_before_full_evidence_gate':True,'coordinated_semantic_and_derivation_rejection':'STATE-VALUE-ORIGIN:/head','returned_nested_trees_do_not_change_expectations':True,'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']},
 'independent_results':{'primary_assertions':primary['assertions'],'primary_categories':primary['categories'],'recovered_assertions':recovered['assertions'],'recovered_categories':recovered['categories'],'fresh_offline_CLI_processes':1,'separate_static_initial_HEAD_type_origin_checks':1,'constructed_cases_are_execution_evidence':False},
 'supplied_results':{'primary':83,'recovered':77,'process_check':1,'inspected_not_executed':True,'membership_failure_assertions':[0,0],'failed_attempts_in_completed_totals':False,'intermediate_recovery_archive_entries':975,'intermediate_outer_archive_newly_verified':False},
 'identities':{'current_code':primary['source'],'new_receipt':composition['current_receipt'],'unchanged_config_receipt':composition['prior_receipt']},
 'preservation':{'config_members_byte_identical':918,'prior_review_included_records_byte_identical':41,'prior_review_archive':composition['exact_external_review'],'historical_archival_omissions':'Documented unchanged; exact external archive retained','prior_functions_AST_identical':42,'other_top_level_AST_identical':True,'new_producer_functions':composition['new_functions'],'prior_context_members_unchanged':True,'historical_evidence_relationships_ordinals_and_prior_closures':'PRESERVED','two_supplied_failure_records_and_bytes':'PRESERVED; cause UNKNOWN; original-root retention remains supplied assertion','implementation_modified':False},
 'observation_limits':{'actual_three_link_execution_chain':'UNAVAILABLE','actual_state_call_count':None,'physical_result_identity':None,'underlying_connection_identity':None,'conditional_values_are_later_observations':False,'saved_state_seq':0,'seq_nonzero_branch':'SOURCE ANALYSIS; not new execution evidence','traced_invocations':18,'separate_observer_Client_state_call':1,'observer_frame':None,'observer_join_to_three_links':None,'complete_runtime_or_repetition_coverage':False,'missing_assignment_state_ingestion_and_historical_launcher_frames':'PRESERVED','current_or_lifetime_readiness_proven':False,'exhaustive_interrupt_feasibility_proven':False},
 'environment':primary['environment'],
 'boundaries':{'all_eleven_obligations':'PRESERVED','inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','accounting_reservations_nonce_ownership_uncertainty':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','admission':False},
 'operations':{'runtime_changes':False,'new_acquisition':False,'session_operations':0,'database_connections':0,'completed_suite_or_review_reruns':False,'smoke_pipeline_lifecycle_reruns':False,'Git_operations':False,'policy_adoption':False}}
(base/'CHECKPOINT.json').write_text(json.dumps(cp,indent=2)+'\n')
(base/'input').mkdir(exist_ok=False);(base/'input/I164-state-return-correspondence-1.zip').write_bytes(raw)
members={}
for p in sorted(base.rglob('*')):
 if p.is_file():
  assert stat.S_ISREG(p.lstat().st_mode) and p.name!='MANIFEST.json';members[p.relative_to(base).as_posix()]=identity(p.read_bytes())
(base/'MANIFEST.json').write_text(json.dumps({'format':'INDEPENDENT-REVIEW-MANIFEST-1','members':members},indent=2)+'\n')
dest=workspace/'Formal-Lab6-I164-state-return-correspondence-independent-review.zip';partial=dest.with_suffix('.zip.partial');assert not dest.exists() and not partial.exists()
with partial.open('xb') as h:
 with zipfile.ZipFile(h,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n in sorted(set(members)|{'MANIFEST.json'}):
   info=zipfile.ZipInfo(n,date_time=(2026,10,28,0,0,0));info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(base/n).read_bytes())
 h.flush();os.fsync(h.fileno())
with zipfile.ZipFile(partial) as z:assert z.testzip() is None and set(z.namelist())==set(members)|{'MANIFEST.json'}
os.replace(partial,dest);print(dest)
