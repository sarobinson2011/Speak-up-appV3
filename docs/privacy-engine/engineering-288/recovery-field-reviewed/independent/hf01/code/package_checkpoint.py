"""Seal independent HF-01 review results without changing any input."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,shutil,stat,zipfile
base=Path(__file__).resolve().parents[1];workspace=base.parent
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(n):return json.loads((base/n).read_bytes())
primary=read('independent-primary/RESULT.json');recovered=read('independent-recovered/RESULT.json');cli=read('cli-recovered/RESULT.json');composition=read('results/composition.json');old=read('original-reproduction/RESULT.json')
assert primary['assertions']==69 and recovered['assertions']==34
for name,result in [('independent-primary',primary),('independent-recovered',recovered)]:
 rows=[json.loads(line) for line in (base/name/'progress.jsonl').read_text().splitlines()]
 assert result['result']=='PASS' and result['failure'] is None and result['checks']==rows and len(rows)==result['assertions']
 assert all(r['result'] in ('PASS','REJECTED') for r in rows)
 assert any(r['check']=='original witness semantic' and r['error']['message']=='HF01-HEAD-EXPECTED-STATE' for r in rows)
 assert any(r['check']=='original witness derivation' and r['error']['message']=='HF01-HEAD-EXPECTED-STATE' for r in rows)
assert cli['returncode']==0 and cli['stderr_bytes']==0 and cli['answer']['result']=='PASS'
assert old['checks']['semantic']['result']=='ACCEPTED' and old['checks']['derivation']['result']=='ACCEPTED' and old['checks']['public_receipt']['result']=='REJECTED' and old['checks']['pristine_public']['result']=='PASS'
assert len(old['changed_members'])==7 and sum(len(v['different_byte_offsets']) for v in old['changed_members'].values())==128
assert read('results/original-reproduction-verification.json')['result']=='PASS'
assert read('results/supplied-core-map-comparison.json')['compact_canonical_match']
archive=workspace/'upload/I164-HF01-correction(1).zip';raw=archive.read_bytes();pin={'bytes':39924668,'sha256':'0e2cce5d4519ccaaab35e34af0f89ef01b8a773569fba66008ee7affb1a9529c'}
assert identity(raw)==pin==read('results/integrity.json')['identity']
with zipfile.ZipFile(archive) as z:
 assert len(z.infolist())==732 and z.testzip() is None
 expected={n:z.read(n) for n in z.namelist()};dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
 preservation={}
 for name in ('hfc-input','hfc-recovered-2'):
  root=workspace/name;files={};seen_dirs=set()
  def walk(p):
   for e in os.scandir(p):
    q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
    if stat.S_ISDIR(mode):seen_dirs.add(n);walk(q)
    else:assert stat.S_ISREG(mode),(name,n);files[n]=q
  walk(root);assert set(files)==set(expected) and seen_dirs==dirs
  assert all(p.read_bytes()==expected[n] for n,p in files.items())
  preservation[name]={'exact_regular_members':732,'all_bytes_unchanged':True,'exact_parent_directories':len(dirs)}
 failed=workspace/'hfc-recovered';assert all((failed/n).is_file() and (failed/n).read_bytes()==b for n,b in expected.items())
 preservation['failed_first_root']={'declared_members_unchanged':732,'failed_root_not_cleaned_or_reused':True,'record':'failures/initial-root-membership/RESULT.json','cause':'UNKNOWN'}
(base/'results/preservation-after-tests.json').write_text(json.dumps(preservation,indent=2)+'\n')
counts=(f"The completed fresh independent primary suite passed {primary['assertions']} assertions; the separate recovered-root suite passed {recovered['assertions']}. "
 "One additional fresh-process execution of the actual current offline CLI passed with the exact corrected receipt. The original-witness reproduction is a separate process with its own acceptance/rejection record. "
 "Six constructed premise cases are included in the primary count, explicitly marked as constructed. The earlier incomplete reviewer-harness runs and failed recovered-root gate are preserved separately and are not added to these totals.")
report=(base/'REPORT.md').read_text();assert report.count('{{INDEPENDENT_COUNTS}}')==1;report=report.replace('{{INDEPENDENT_COUNTS}}',counts);(base/'REPORT.md').write_text(report)
checkpoint={
 'checkpoint':'Formal-Lab6-I164-HF01-independent-review','review_target':'I164-HF01-correction.zip','input':{**pin,'entries':732,'manifested_hashes':731},
 'review_author':'Formal-Lab[6]','construction_author':'SU-Engineering[288D]','author_independent':True,'canonical':False,
 'verdict':'HF-01 CLOSED within the retained saved-evidence correspondence contract','finding':'No residual witness found in focused corrected checks; no global completeness claim',
 'original_witness':{'changed_members':7,'changed_bytes':128,'member_lengths_preserved':True,'exact_reproduction_verified':True,'semantic':'ACCEPTED','derivation':'ACCEPTED','public_altered_receipt':'REJECTED already before correction','public_pristine':'PASS'},
 'corrected_witness':{'semantic':'REJECTED','derivation':'REJECTED','reason':'HF01-HEAD-EXPECTED-STATE','fresh_recovered_reproduction':True,'public_old_mixed_receipt':'REJECTED','pristine_saved_receipt':'PASS in both contexts'},
 'correction_basis':{'current_predecessor_actually_invoked':True,'same_evidence_consumed_for_predecessor_and_head_expectation':True,'semantic_comparison_before_whole_map_gate':True,'no_caller_result_cached_as_expectation':True,'no_silent_repair':True,'no_hardcoded_zero_head_or_new_string_bound':True},
 'independent_results':{'primary_assertions':primary['assertions'],'primary_categories':primary['categories'],'recovered_assertions':recovered['assertions'],'recovered_categories':recovered['categories'],'fresh_offline_CLI_processes':1,'old_witness_reproduction_processes':1,'six_constructed_cases_not_runtime_evidence':True,'partial_interrupted_attempts_not_added':True},
 'supplied_results':{'primary':75,'recovered':23,'input_gates':5,'fresh_process':1,'inspected_not_executed':True,'recovery_archive_entries':717,'recovery_outer_archive_not_supplied':True,'current_core_identity_map_matches_reported_compact_canonical_identity':True},
 'identities':{'correspondence.py':primary['source']['correspondence.py'],'managed_coverage.py':primary['source']['managed_coverage.py'],'corrected_receipt':composition['new_receipt'],'original_receipt':composition['old_receipt']},
 'preservation':{'original_members_unchanged':617,'prior_review_noninput_members_unchanged':63,'all_old_context_fields_preserved':True,'prior_scoped_closures_and_historical_identities_relationships_ordinals':'UNCHANGED','implementation_modified':False,'original_witnesses_and_failure_records':'PRESERVED'},
 'environment':primary['environment'],
 'observation_limits':{'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'traced_invocations':18,'saved_normal_recovery_invocations':1,'saved_status_returns':2,'separate_observer_Client_state_call':1,'observer_frame':None,'validator_scalar':'UNAVAILABLE','Authority_state_and_ingestion_frames':'UNAVAILABLE','assignment_and_historical_launcher_frames':'UNAVAILABLE','source_or_constructed_cases_not_new_execution_evidence':True},
 'failure_provenance':{'supplied_FIFO_fixture_completed_assertions':0,'supplied_FIFO_cause':'UNKNOWN','independent_initial_partial_file_bytes':14680064,'independent_initial_root_rejected_before_dependency_import':True,'independent_partial_file_cause':'UNKNOWN','interrupted_reviewer_harness_partial_counts':[17,3],'interrupted_harness_only_change':'Removed per-call pathlib parsing from read-only profile callback','original_failed_roots_and_records_preserved':True},
 'boundaries':{'all_eleven_obligations':'PRESERVED','inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','permanent_accounting_reservations_nonce_ownership_uncertainty':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','admission':False},
 'operations':{'runtime_changes':False,'new_acquisition':False,'host_session_operations':False,'database_connections':0,'completed_review_reruns':False,'smoke_pipeline_lifecycle_reruns':False,'policy_or_canonical_binding_changes':False,'Git_save':False},
 'next_action':'Return scoped HF-01 closure to Engineering-Anchor[2]; unresolved operational evidence, lifetime bounds, qualification and canonical authority remain blockers.'
}
(base/'CHECKPOINT.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
target=base/'input/I164-HF01-correction.zip';target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();shutil.copyfile(archive,target)
members={}
for p in sorted(base.rglob('*')):
 if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts:
  assert stat.S_ISREG(p.lstat().st_mode);members[p.relative_to(base).as_posix()]=identity(p.read_bytes())
(base/'MANIFEST.json').write_text(json.dumps({'format':'Formal-Lab6-HF01-independent-review-1','members':members},indent=2)+'\n')
dest=workspace/'Formal-Lab6-I164-HF01-independent-review.zip';partial=workspace/(dest.name+'.partial');assert not dest.exists() and not partial.exists()
with partial.open('xb') as handle:
 with zipfile.ZipFile(handle,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in sorted([*members,'MANIFEST.json']):
   info=zipfile.ZipInfo(n,date_time=(2026,10,27,0,0,0));info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(base/n).read_bytes())
 handle.flush();os.fsync(handle.fileno())
with zipfile.ZipFile(partial) as z:assert z.testzip() is None and set(z.namelist())==set(members)|{'MANIFEST.json'}
os.replace(partial,dest);print(dest)
