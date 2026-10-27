"""Seal this independent review; verify originals remain unchanged."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,shutil,stat,zipfile
base=Path(__file__).resolve().parents[1];workspace=base.parent
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(n):return json.loads((base/n).read_bytes())
primary=read('independent-primary/RESULT.json');recovered=read('independent-recovered/RESULT.json');cli=read('cli-recovered/RESULT.json');composition=read('results/composition.json')
assert primary['assertions']==91 and recovered['assertions']==52
for name,r in [('independent-primary',primary),('independent-recovered',recovered)]:
 rows=[json.loads(x) for x in (base/name/'progress.jsonl').read_text().splitlines()]
 assert r['result']=='PASS' and r['error'] is None and r['checks']==rows and len(rows)==r['assertions']
 assert all(x['result'] in ('PASS','REJECTED') for x in rows)
 assert any(x['check']=='coordinated reports semantic comparison' and x['error']['message']=='BINDING-VALIDATED-INSTANCE-VALUE' for x in rows)
 assert any(x['check']=='coordinated reports derivation comparison' and x['error']['message']=='BINDING-VALIDATED-INSTANCE-VALUE' for x in rows)
assert cli['returncode']==0 and cli['stderr_bytes']==0 and cli['answer']['getter_runtime_evidence']=='UNAVAILABLE'
assert read('results/type-helper-source.json')['matched_sources']
archive=workspace/'upload/I164-binding-return-correspondence-1(1).zip';raw=archive.read_bytes();pin={'bytes':40870457,'sha256':'269e5e439de97fe77fcacba484c544b276457db7643cc5863875ef227331dc4f'}
assert identity(raw)==pin==read('results/integrity.json')['identity']
preservation={}
with zipfile.ZipFile(archive) as z:
 assert len(z.infolist())==844 and z.testzip() is None
 expected={n:z.read(n) for n in z.namelist()};dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
 for name in ('br-input','br-recovered-2'):
  root=workspace/name;files={};seen_dirs=set()
  def walk(p):
   for e in os.scandir(p):
    q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
    if stat.S_ISDIR(mode):seen_dirs.add(n);walk(q)
    else:assert stat.S_ISREG(mode),(name,n);files[n]=q
  walk(root);assert set(files)==set(expected) and seen_dirs==dirs
  assert all(p.read_bytes()==expected[n] for n,p in files.items())
  preservation[name]={'exact_unchanged_regular_members':844,'parent_directories':len(dirs),'source_and_all_declared_evidence_bytes_unchanged':True}
 failed=workspace/'br-recovered';assert all((failed/n).is_file() and (failed/n).read_bytes()==b for n,b in expected.items())
 preservation['initial_failed_root']={'all_declared_844_members_unchanged':True,'failed_root_not_cleaned_or_reused':True,'cause':'UNKNOWN','record':'failures/initial-recovered-membership/RESULT.json'}
(base/'results/preservation-after-tests.json').write_text(json.dumps(preservation,indent=2)+'\n')
counts=(f"The completed fresh independent suites passed {primary['assertions']} primary assertions and {recovered['assertions']} recovered-root assertions. "
 "One separate fresh process ran the actual current public CLI successfully with the exact saved receipt, both contexts, getter execution UNAVAILABLE and admission disabled. "
 "Source-helper inspection is separately recorded. The constructed cases and direct relation checks are labelled by category within these totals; they are not runtime observations. The zero-assertion failed reviewer-oracle attempt and rejected initial recovered tree are not added to completed totals.")
report=(base/'REPORT.md').read_text();assert report.count('{{COUNTS}}')==1;(base/'REPORT.md').write_text(report.replace('{{COUNTS}}',counts))
cp={
 'checkpoint':'Formal-Lab6-I164-binding-return-correspondence-independent-review','review_target':'I164-binding-return-correspondence-1.zip','input':{**pin,'entries':844,'manifested_hashes':843},
 'review_author':'Formal-Lab[6]','construction_author':'SU-Engineering[288D]','author_independent':True,'canonical':False,
 'verdict':'SUPPORTED for bounded source-derived conditional getter correspondence and validated recovery-frontier binding','defect_witness':'None found in focused checks; no complete-runtime-coverage claim',
 'source_derivation':{'property':'ManagedAuthority.binding','return':'self._live.binding','type':'str under retained initialized Authority and typed HEAD premise','guards':['lock entry completes','_require normal continuation: READY, live present, retired absent','receiver/attribute evaluation completes','lock exit completes'],'underlying_constructor':'sha(enc(...))','state_relation':"HEAD binding equals this Authority instance binding",'independent_AST_and_guard_oracle':True,'three_inherited_reference_links_verified':True,'anchor_helper_AST_inspected_not_executed':True},
 'binding_validation':{'mandatory_HF01_derive_recovery_invoked':True,'expected_binding_from_same_validated_predecessor_evidence':True,'semantic_comparison_before_whole_evidence_gate':True,'coordinated_semantic_and_derivation_substitutions':'REJECTED: BINDING-VALIDATED-INSTANCE-VALUE','equal_string_wrong_instance_claims':'REJECTED: BINDING-ANCHOR-LINEAGE','nested_mutations_cannot_change_pristine_expectations':True,'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']},
 'independent_results':{'primary_assertions':primary['assertions'],'primary_categories':primary['categories'],'recovered_assertions':recovered['assertions'],'recovered_categories':recovered['categories'],'fresh_offline_CLI_processes':1,'static_type_helper_inspection':'Separate saved result','source_oracle_failure_assertions':0,'constructed_cases_not_execution_evidence':True},
 'supplied_results':{'primary':95,'recovered':53,'input_gates':4,'process_validation':1,'inspected_not_executed':True,'interrupted_attempt_assertions':13,'interrupted_attempt_excluded':True,'intermediate_recovery_archive_entries':817,'intermediate_outer_archive_freshly_verified':False},
 'identities':{'current_code':primary['source'],'new_receipt':composition['current_receipt'],'unchanged_HF01_receipt':composition['prior_receipt']},
 'preservation':{'HF01_members_unchanged':732,'closure_review_noninput_members_unchanged':72,'prior_producer_functions_AST_identical':31,'prior_context_members_preserved':True,'historical_identities_relationships_ordinals':'UNCHANGED','HF01_and_other_prior_scoped_closures':'PRESERVED; no review rerun','implementation_modified':False},
 'observation_limits':{'actual_getter_execution':'UNAVAILABLE','actual_getter_count':None,'getter_frame':None,'object_identity':None,'underlying_connection_identity':None,'traced_invocations':18,'recovery_invocations':1,'status_returns':2,'separate_observer_Client_state_call':1,'observer_frame':None,'missing_assignment_reference_state_ingestion_and_historical_launcher_frames':'PRESERVED','validated_frontier_is_current_or_lifetime_readiness':False,'two_contexts_are_extra_executions':False},
 'environment':primary['environment'],
 'failure_provenance':{'supplied_13_assertion_interruption_preserved':True,'independent_oracle_attempt':'Zero assertions; AST object identity across separate parses corrected to source coordinates; full failed attempt preserved','independent_recovery_partial_bytes':17301504,'independent_recovery_gate':'REJECTED before predecessor import','independent_recovery_cause':'UNKNOWN','failed_roots_preserved':True},
 'boundaries':{'all_eleven_obligations':'PRESERVED','inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','accounting_reservations_nonce_ownership_uncertainty':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','admission':False},
 'operations':{'runtime_changes':False,'new_acquisition':False,'session_operations':0,'database_connections':0,'completed_suite_or_review_reruns':False,'smoke_pipeline_lifecycle_reruns':False,'policy_or_canonical_binding_changes':False,'Git_save_repeated':False},
 'next_action':'Return scoped support to Engineering-Anchor[2]; missing getter execution evidence and all operational/lifetime/qualification/authority blockers remain. No collection or new construction authorized by this review.'
}
(base/'CHECKPOINT.json').write_text(json.dumps(cp,indent=2)+'\n')
target=base/'input/I164-binding-return-correspondence-1.zip';target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();shutil.copyfile(archive,target)
members={}
for p in sorted(base.rglob('*')):
 if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts:
  assert stat.S_ISREG(p.lstat().st_mode);members[p.relative_to(base).as_posix()]=identity(p.read_bytes())
(base/'MANIFEST.json').write_text(json.dumps({'format':'Formal-Lab6-binding-return-independent-review-1','members':members},indent=2)+'\n')
dest=workspace/'Formal-Lab6-I164-binding-return-correspondence-independent-review.zip';partial=workspace/(dest.name+'.partial');assert not dest.exists() and not partial.exists()
with partial.open('xb') as h:
 with zipfile.ZipFile(h,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in sorted([*members,'MANIFEST.json']):
   info=zipfile.ZipInfo(n,date_time=(2026,10,27,0,0,0));info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(base/n).read_bytes())
 h.flush();os.fsync(h.fileno())
with zipfile.ZipFile(partial) as z:assert z.testzip() is None and set(z.namelist())==set(members)|{'MANIFEST.json'}
os.replace(partial,dest);print(dest)
