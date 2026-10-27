"""Seal HF-01 review evidence, preserving implementation and original inputs."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,shutil,stat,zipfile
base=Path(__file__).resolve().parents[1];workspace=base.parent
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(n):return json.loads((base/n).read_bytes())
primary=read('independent-primary/RESULT.json');recovered=read('independent-recovered-2/RESULT.json');cli=read('cli-recovered/RESULT.json');composition=read('results/composition.json');integrity=read('results/integrity.json');reverts=read('results/witness-reverts.json')
assert primary['assertions']==97 and recovered['assertions']==29 and reverts['assertions']==7
for name,result in [('independent-primary',primary),('independent-recovered-2',recovered)]:
 assert result['failure'] is None and result['result']=='PASS focused controls'
 rows=[json.loads(s) for s in (base/name/'progress.jsonl').read_text().splitlines()]
 assert rows==result['checks'] and len(rows)==result['assertions'] and all(r['result'] in ('PASS','REJECTED') for r in rows)
assert cli['returncode']==0 and cli['stderr_bytes']==0 and cli['answer']['result']=='PASS'
witnesses={name:read(name+'/RESULT.json') for name in ['head-witness-primary','head-witness-recovered']}
for name,result in witnesses.items():
 assert result['checks']['semantic']['result']=='ACCEPTED' and result['checks']['derivation']['result']=='ACCEPTED'
 assert result['checks']['public_receipt']['result']=='REJECTED' and result['checks']['pristine_public']['result']=='PASS'
 assert len(result['changed_members'])==7 and sum(len(x['different_byte_offsets']) for x in result['changed_members'].values())==128
assert (base/'head-witness-primary/altered-derived-receipt.json').read_bytes()==(base/'head-witness-recovered/altered-derived-receipt.json').read_bytes()
archive=workspace/'upload/I164-recovery-field-correspondence-1(1).zip';raw=archive.read_bytes();pin={'bytes':39038102,'sha256':'c92840a853097a9fe5fd1cd80134649fdd25a7463422cce81361a46bec70f8cf'}
assert identity(raw)==pin==integrity['identity'] and integrity['entries']==617 and len(integrity['nested_archives'])==18
preserved=[]
with zipfile.ZipFile(archive) as z:
 expected={n:z.read(n) for n in z.namelist()};assert len(expected)==617
 dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
 for name in ['hf-input','hf-recovered-2']:
  root=workspace/name;files={};seen_dirs=set()
  def walk(parent):
   for entry in os.scandir(parent):
    p=Path(entry.path);n=p.relative_to(root).as_posix();mode=entry.stat(follow_symlinks=False).st_mode
    if stat.S_ISDIR(mode):seen_dirs.add(n);walk(p)
    else:assert stat.S_ISREG(mode);files[n]=p
  walk(root);assert set(files)==set(expected) and seen_dirs==dirs
  assert all(p.read_bytes()==expected[n] for n,p in files.items())
  preserved.append({'root':name,'exact_unchanged_members':len(files),'parent_directories':len(seen_dirs),'all_bytes_and_regular_types_verified':True})
 # The first rejected root is failure provenance, not a strict valid root.
 failed=workspace/'hf-recovered';declared_unchanged=all((failed/n).is_file() and (failed/n).read_bytes()==b for n,b in expected.items());assert declared_unchanged
 extra={p.relative_to(failed).as_posix():identity(p.read_bytes()) for p in failed.rglob('*') if p.is_file() and p.relative_to(failed).as_posix() not in expected}
 partial=(base/'failures/recovered-root-extra-member/unexpected-partial.bin').read_bytes()
 neighbor=expected['retained/references/retained/fields/retained/occurrence/retained/correction/basis/candidate/managed-route/directory-relations.json']
 failed_record={'declared_members_unchanged':617,'current_extra_regular_members':extra,'rejected_root_not_cleaned_by_reviewer':True,'preserved_unexpected_bytes_are_prefix_of_declared_neighbor':neighbor.startswith(partial),'source_of_extra_entry':'UNKNOWN'}
(base/'results/preservation-after-tests.json').write_text(json.dumps({'result':'PASS original declared bytes preserved','input':pin,'strict_roots':preserved,'first_recovered_root_failure':failed_record},indent=2)+'\n')
target=base/'input/I164-recovery-field-correspondence-1.zip';target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();shutil.copyfile(archive,target)
cp={
 'checkpoint':'Formal-Lab6-I164-recovery-field-correspondence-independent-review',
 'review_target':'I164-recovery-field-correspondence-1.zip','target':{**pin,'entries':617},
 'review_author':'Formal-Lab[6]','construction_author':'SU-Engineering[288D]','author_independent':True,'canonical':False,
 'verdict':'NOT SUPPORTED for full requested coordinated recovery-head correspondence assurance; HF-01 OPEN',
 'supported_scope':['Source-derived three-field mappings, guards and normal continuations','Exact boolean constants and inherited head type','Legitimate pinned-input public receipt and prior component continuity','Public rejection of altered derived receipt'],
 'finding':{'id':'HF-01','status':'OPEN','summary':'Internal semantic and derivation interfaces accept coordinated substituted head and derive a mixed-evidence receipt','semantic_interface':'connected_recovery(data, catalogue, altered_evidence)','derivation_interface':'derive_recovery(data, catalogue, altered_evidence)','old_head':'0'*64,'new_head':'1'+'0'*63,'changed_members':7,'changed_bytes':128,'member_lengths_unchanged':True,'current_source_and_database_bytes_unchanged':True,'reproduced_in_fresh_recovered_root':True,'public_validation_bypass':False,'public_altered_receipt':'REJECTED','public_pristine_receipt':'PASS','original_trace_sha256':'9558e9987e53e117c5b49efa56c00b0e17389aa95e5c5d2d897ddde2b6b4a12a','altered_trace_sha256':'0ba7774c5d28d94c1ccc22a5651d61e360243e787960f0544aa9dc1b412c8f10','scope':'Requested coordinated semantic assurance, not admission of unpinned replacement evidence','minimality':'Each of seven one-member restorations rejects this fixed construction; global byte-minimality not claimed'},
 'independent_results':{'primary_focused_assertions':97,'primary_categories':primary['categories'],'recovered_focused_assertions':29,'witness_member_restoration_assertions':7,'new_offline_CLI_processes':1,'minimal_witness_processes':2,'exploratory_probe_processes':1,'accepted_witnesses_not_counted_as_passing_controls':True,'constructed_cases_primary':primary['constructed_cases'],'constructed_cases_recovered':recovered['constructed_cases']},
 'supplied_results':{'primary':117,'recovered':30,'input_gates':5,'fresh_process':1,'inspected_not_executed':True,'recovery_input':'610-member pre-documentation archive distinct from 617-member target','damaged_temporary_archives':'Not supplied; reported/observed identities and unknown cause retained'},
 'source':primary['source'],'new_receipt':composition['new_receipt'],'unchanged_reference_receipt':composition['prior_receipt'],
 'source_audit':{'fields':3,'head_chain_entries':16,'programs':['ManagedAuthority.recover','ManagedAuthority._validate','Authority.state'],'guards_independently_derived':True},
 'preservation':{'predecessor_members':552,'prior_independent_noninput_members':34,'status_field_root_members':489,'SOC_closed_root_members':467,'candidate_and_draft_identity_maps':[666,163],'old_context_fields_relationships_ordinals_and_obligations_unchanged':True,'prior_closures_preserved_not_rerun':True,'implementation_modified':False},
 'observations':{'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'recovery_invocations':1,'status_returns':2,'traced_invocations':18,'separate_observer_Client_state_calls':1,'validator_scalar':'NOT CAPTURED','Authority_state_and_ingest_frames':'UNAVAILABLE','assignment_and_historical_launcher_frames':'UNAVAILABLE','two_contexts_not_extra_executions':True,'no_new_observations':True},
 'environment':primary['environment'],
 'failure_provenance':{'supplied_packaging_discrepancies':2,'causes':'UNKNOWN','independent_first_recovery':'Rejected undeclared partial regular member before predecessor consumption; zero assertions completed','rejected_root_and_unexpected_bytes_preserved':True,'new_clean_root_actual_members_verified':617},
 'boundaries':{'all_eleven_obligations_preserved':True,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','admission':False},
 'prohibited_operations':{'runtime_changes':False,'acquisition':False,'database_connections':0,'session_operations':False,'completed_review_reruns':False,'smoke_pipeline_lifecycle_reruns':False,'policy_adoption':False,'Git_save':False},
 'next_task':'Bounded HF-01 correction: anchor recovery-head expectations and joins to the same independently validated current evidence as the predecessor chain; reject this semantic/derivation witness without hardcoded zero heads or domain narrowing.',
 'handoff':'Return finding and preserved scoped support to Engineering-Anchor[2]; no new admission or operational authority.'
}
(base/'CHECKPOINT.json').write_text(json.dumps(cp,indent=2)+'\n')
members={}
for p in sorted(base.rglob('*')):
 if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts:
  assert stat.S_ISREG(p.lstat().st_mode);members[p.relative_to(base).as_posix()]=identity(p.read_bytes())
(base/'MANIFEST.json').write_text(json.dumps({'format':'Formal-Lab6-recovery-field-independent-review-1','members':members},indent=2)+'\n')
dest=workspace/'Formal-Lab6-I164-recovery-field-correspondence-independent-review.zip';partial_path=workspace/(dest.name+'.partial');assert not dest.exists() and not partial_path.exists()
with partial_path.open('xb') as handle:
 with zipfile.ZipFile(handle,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name in sorted([*members,'MANIFEST.json']):
   info=zipfile.ZipInfo(name,date_time=(2026,10,27,0,0,0));info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(base/name).read_bytes())
 handle.flush();os.fsync(handle.fileno())
with zipfile.ZipFile(partial_path) as z:assert z.testzip() is None and set(z.namelist())==set(members)|{'MANIFEST.json'}
os.replace(partial_path,dest);print(dest)
