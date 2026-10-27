from pathlib import Path
import hashlib,json,shutil,stat,zipfile
base=Path(__file__).resolve().parents[1];workspace=base.parent
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
primary=json.loads((base/'independent-primary/RESULT.json').read_bytes());recovered=json.loads((base/'independent-recovered/RESULT.json').read_bytes())
assert primary['assertions']==100 and recovered['assertions']==26 and primary['old_variants_reproduced']==3
archive=workspace/'upload/I164-SOC02-R1-correction(1).zip';raw=archive.read_bytes()
assert identity(raw)=={'bytes':30156228,'sha256':'eb8f0c74f1431a00cfe67e7b756a7e3416385a34bebaa0e2b3981c063898092f'}
preserved=[]
with zipfile.ZipFile(archive) as z:
 expected={n:z.read(n) for n in z.namelist()}
 for dirname in ('r1-input','r1-recovered'):
  root=workspace/dirname;files={p.relative_to(root).as_posix():p for p in root.rglob('*') if not p.is_dir()}
  assert set(files)==set(expected),dirname
  assert all(stat.S_ISREG(p.lstat().st_mode) and p.read_bytes()==expected[n] for n,p in files.items()),dirname
  preserved.append({'root':dirname,'exact_unchanged_files':len(files),'all_bytes_verified':True})
(base/'results/preservation-after-tests.json').write_text(json.dumps({'result':'PASS','input':identity(raw),'roots':preserved},indent=2)+'\n')
target=base/'input/I164-SOC02-R1-correction.zip';target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(archive,target)
cp={
 'checkpoint':'Formal-Lab6-I164-SOC02-R1-independent-review',
 'review_target':'I164-SOC02-R1-correction.zip','target':{**identity(raw),'entries':520},
 'review_author':'Formal-Lab[6]','construction_author':'SU-Engineering[288D]','author_independent':True,'canonical':False,
 'verdict':'SUPPORTED for SOC-02-R1 closure within retained offline saved-evidence observation contract',
 'residual_witness':'None found in bounded tested scope',
 'SOC-01':'Prior scoped closure preserved; completed review not rerun',
 'original_SOC-02_five_variants':'Prior scoped correction support preserved; completed review not rerun',
 'independent_checks':{'primary_assertions':100,'old_variants_reproduced':3,'corrected_semantic_and_derive_rejections':3,'fresh_process_recovered_assertions':26,'overlap_is_not_extra_semantic_coverage':True},
 'supplied_controls':{'primary':35,'recovered_repetition':35,'inspected_not_executed':True},
 'source':primary['source'],'unchanged_pristine_receipt':primary['pristine_receipt'],
 'observations':{'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'traced_invocations':18,'separate_observer_Client_state_calls':1,'no_invented_observer_frame_or_parent':True,'context_views_are_not_extra_executions':True},
 'environment':primary['environment'],
 'preservation':{'input_members':520,'retained_correction_members':463,'candidate_identity_map':666,'draft_identity_map':163,'obligations':11,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'SOURCE_ONLY':'UNCHANGED','Decision_B':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False,'backup':'KERNEL-ONLY','streams':'UNCOMPUTED','historical_launcher_frames':'UNAVAILABLE','implementation_modified':False},
 'limits':['Trusted pinned producer/observer and stable filesystem','Successful saved raw and managed close route only','Sparse trace has no offsets, arguments, full line/exception history, or live/retired snapshots','No arbitrary callback/introspection/forged-observer resistance','Saved export correlated, not reacquired or re-ingested','No new operational durability, ownership, lifetime, canonical model or qualification evidence'],
 'prohibited_operations':{'host_or_session_execution':False,'database_connections':0,'completed_review_reruns':False,'smoke_rerun':False,'pipeline_rerun':False,'lifecycle_rerun':False,'policy_adoption':False},
 'handoff':'Return scoped closure support to Engineering-Anchor[2]; existing substantive blockers remain.'
}
(base/'CHECKPOINT.json').write_text(json.dumps(cp,indent=2)+'\n')
members={p.relative_to(base).as_posix():identity(p.read_bytes()) for p in sorted(base.rglob('*')) if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
(base/'MANIFEST.json').write_text(json.dumps({'format':'Formal-Lab6-SOC02-R1-independent-review-1','members':members},indent=2)+'\n')
dest=workspace/'Formal-Lab6-I164-SOC02-R1-independent-review.zip';assert not dest.exists()
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in sorted([*members,'MANIFEST.json']):
  i=zipfile.ZipInfo(n,date_time=(2026,10,26,0,0,0));i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,(base/n).read_bytes())
print(str(dest))
