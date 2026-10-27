"""Package completed independent review; never execute implementation code."""
from pathlib import Path, PurePosixPath
import hashlib,json,os,shutil,stat,zipfile
base=Path(__file__).resolve().parents[1];workspace=base.parent
def identity(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def read(n):return json.loads((base/n).read_bytes())
primary=read('independent-primary/RESULT.json');recovered=read('independent-recovered/RESULT.json');gate=read('input-gates/RESULT.json');cli=read('cli-recovered/RESULT.json');composition=read('results/composition.json');integrity=read('results/integrity.json')
assert primary['assertions']==276 and recovered['assertions']==41 and gate['assertions']==5 and gate['result']=='PASS'
for name,result in [('independent-primary',primary),('independent-recovered',recovered)]:
 assert result['failure'] is None and result['result']=='PASS bounded reference correspondence'
 lines=[json.loads(line) for line in (base/name/'progress.jsonl').read_text().splitlines()]
 assert lines==result['checks'] and len(lines)==result['assertions'] and all(x['result'] in ('PASS','REJECTED') for x in lines)
assert cli['returncode']==0 and cli['stderr_bytes']==0 and cli['answer']['result']=='PASS'
archive=workspace/'upload/I164-reference-transfer-correspondence-1(1).zip';raw=archive.read_bytes()
pin={'bytes':38786604,'sha256':'36e4dfd8199df3a9168e47416d1e2508a8868876170c3586734c5a714adadac9'}
assert identity(raw)==pin==integrity['identity'] and integrity['entries']==552 and len(integrity['nested_archives'])==18
preserved=[]
with zipfile.ZipFile(archive) as z:
 expected={n:z.read(n) for n in z.namelist()};assert len(expected)==552
 allowed_dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
 for dirname in ('rf-input','rf-recovered'):
  root=workspace/dirname;assert stat.S_ISDIR(root.lstat().st_mode);files={};directories=set()
  def walk(parent):
   for entry in os.scandir(parent):
    p=Path(entry.path);name=p.relative_to(root).as_posix();mode=entry.stat(follow_symlinks=False).st_mode
    if stat.S_ISDIR(mode):directories.add(name);walk(p)
    else:assert stat.S_ISREG(mode),name;files[name]=p
  walk(root);assert set(files)==set(expected) and directories==allowed_dirs
  assert all(p.read_bytes()==expected[n] for n,p in files.items())
  preserved.append({'root':dirname,'exact_unchanged_files':len(files),'exact_parent_directories':len(directories),'all_bytes_verified':True,'regular_files_and_directories_only':True})
(base/'results/preservation-after-tests.json').write_text(json.dumps({'result':'PASS','input':pin,'roots':preserved},indent=2)+'\n')
target=base/'input/I164-reference-transfer-correspondence-1.zip';target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();shutil.copyfile(archive,target)
cp={
 'checkpoint':'Formal-Lab6-I164-reference-transfer-correspondence-independent-review',
 'review_target':'I164-reference-transfer-correspondence-1.zip','target':{**pin,'entries':552},
 'review_author':'Formal-Lab[6]','construction_author':'SU-Engineering[288D]','author_independent':True,'canonical':False,
 'verdict':'SUPPORTED for bounded source-derived reference-transfer correspondence, constructed path algebra and exact saved invocation joins',
 'residual_witness':'None demonstrated within the tested bounded contract',
 'independent_checks':{'primary_assertions':276,'primary_categories':primary['categories'],'constructed_case_records_primary':64,'distinct_constructed_scenarios_per_context':32,'fresh_process_recovered_assertions':41,'input_gate_assertions':5,'actual_offline_command_processes':1,'overlap_not_extra_execution_coverage':True},
 'supplied_evidence':{'primary_controls':182,'recovered_repetition':182,'separate_process_checks':1,'constructed_cases_per_run':21,'inspected_not_executed':True,'author_recovery_root':'509-member pre-documentation input; distinguished from delivered 552-member archive'},
 'source_audit':read('independent-primary/source-audit.json')['counts'],
 'source':primary['source'],'new_receipt':composition['new_output'],'prior_field_receipt':composition['prior_output'],
 'preserved_closures':['six-field correspondence','SOC-01','original SOC-02 corrections','SOC-02-R1','status boundary'],
 'preservation':{'retained_field_members_unchanged':489,'prior_independent_noninput_members_unchanged':27,'SOC_closed_members':467,'candidate_identity_map_members':666,'draft_identity_map_members':163,'identity_maps_are_continuity_not_fresh_full_reviews':True,'all_previous_context_fields_relationships_ordinals_and_obligations_preserved':True,'implementation_modified_by_reviewer':False},
 'observations':{'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'traced_invocations':18,'status_returns':2,'separate_observer_Client_state_calls':1,'source_function_joins_per_context':3,'actual_reference_transfers':'UNAVAILABLE','object_identity':'UNESTABLISHED','underlying_connection_identity':'UNESTABLISHED','no_invented_observer_frame_or_parent':True,'no_new_runtime_observations':True,'both_contexts_are_views_not_extra_executions':True},
 'environment':primary['environment'],
 'failure_provenance':{'supplied_initial_attempt':'Zero-check source-location AttributeError preserved','supplied_preparation_attempt':'Manifest-reader KeyError before extraction/import preserved','reviewer_oracle_development_failures':2,'reviewer_control_suite_failures':0,'temporary_environment_outage':'Reviewer patch interrupted; workspace restored; original inputs unchanged','failed_attempts_not_counted_as_passing':True},
 'limits':['Pinned source, trusted process, exclusive owner and mandatory entry retain prior scope','Syntactic guard/normal-continuation coverage is not feasible-path or complete history proof','Constructed default-normal/abrupt gates and stop points are premises, not execution or durable interruption evidence','No arbitrary callbacks, context-manager suppression, foreign mutation or every intra-expression failure modeled','Equal recorded representations never establish reference/object/connection identity','A slot clear cannot prove physical close or discharge outstanding obligations','Sparse saved trace has no live/retired snapshots, local allocation identity or assignment-line histories','Historical launcher-frame provenance unavailable','No prepared-host 41.0.7 or backend compatibility claim'],
 'boundaries':{'obligations':11,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','admission':False},
 'prohibited_operations':{'runtime_behavior_changes':False,'new_acquisition':False,'database_connections':0,'host_session_operations':False,'completed_review_reruns':False,'smoke_reruns':False,'pipeline_reruns':False,'lifecycle_reruns':False,'policy_adoption':False},
 'handoff':'Return this scoped independent support to Engineering-Anchor[2]; no operational or qualification blocker is discharged.'
}
(base/'CHECKPOINT.json').write_text(json.dumps(cp,indent=2)+'\n')
members={}
for p in sorted(base.rglob('*')):
 if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts:
  assert stat.S_ISREG(p.lstat().st_mode);members[p.relative_to(base).as_posix()]=identity(p.read_bytes())
(base/'MANIFEST.json').write_text(json.dumps({'format':'Formal-Lab6-reference-transfer-independent-review-1','members':members},indent=2)+'\n')
dest=workspace/'Formal-Lab6-I164-reference-transfer-correspondence-independent-review.zip';assert not dest.exists()
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in sorted([*members,'MANIFEST.json']):
  info=zipfile.ZipInfo(n,date_time=(2026,10,27,0,0,0));info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(base/n).read_bytes())
print(dest)
