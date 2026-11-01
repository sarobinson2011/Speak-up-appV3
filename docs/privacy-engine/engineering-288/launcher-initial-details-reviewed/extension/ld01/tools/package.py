"""Package saved bytes only. Does not execute any validator or test campaign."""
from pathlib import Path
import json,hashlib,zipfile,stat,sys,os
T=Path(__file__).resolve().parents[1]
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def declared(root):
 m=json.loads((root/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};actual=set();found=set()
 for base,ds,fs in os.walk(root,followlinks=False):
  for n in ds:
   p=Path(base)/n;assert stat.S_ISDIR(p.lstat().st_mode);found.add(p.relative_to(root).as_posix())
  for n in fs:
   p=Path(base)/n;assert stat.S_ISREG(p.lstat().st_mode);actual.add(p.relative_to(root).as_posix())
 assert actual==expected and found==dirs
 files={n:(root/n).read_bytes() for n in m};assert all(ident(files[n])==pin for n,pin in m.items());return files
def pack(files,path):
 assert not path.exists();files=dict(files);assert 'MANIFEST.json' not in files;files['MANIFEST.json']=enc({n:ident(b) for n,b in sorted(files.items())})
 with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
  for n,b in sorted(files.items()):
   p=Path(n);assert not p.is_absolute() and '..' not in p.parts and '\\' not in n
   info=zipfile.ZipInfo(n,(2026,10,31,0,0,0));info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
 with zipfile.ZipFile(path) as z:
  assert z.namelist()==sorted(files) and len(z.namelist())==len(set(z.namelist()))
  for n,b in files.items():assert z.read(n)==b
 return {**ident(path.read_bytes()),'entries':len(files),'manifested_files':len(files)-1,'CRC_membership_hashes':'PASS'}
def group(files,name,kind):
 root=T/'results'/name;proc=T/'processes'/name;r=json.loads((root/'RESULT.json').read_bytes());e=json.loads((proc/'exit-status.json').read_bytes());assert r['result']=='PASS' and e['returncode']==0 and not e['timed_out']
 rows=[json.loads(x) for x in (root/'progress.jsonl').read_text().splitlines()];stdout=[x for x in (proc/'stdout.log').read_text().splitlines() if x and x.split(' ',1)[0].isdigit()]
 assert rows==r['rows'] and r['checks']==len(rows)==len(stdout)
 assert all(s==f"{i} {v['check']} {v['result']}" for i,(s,v) in enumerate(zip(stdout,rows),1))
 for base,prefix in ((root,'ld01/results/'+name),(proc,'ld01/processes/'+name)):
  for p in base.rglob('*'):
   if p.is_file():files[prefix+'/'+p.relative_to(base).as_posix()]=p.read_bytes()
 v={'recorded_rows':len(rows),'kind':kind,'scope':r['scope'],'result':ident((root/'RESULT.json').read_bytes()),'exit':e,'stdout_progress_RESULT_reconciled':True}
 if name in ('primary','recovered'):
  launch=json.loads((proc/'launch.json').read_bytes());calls=json.loads((root/'calls.json').read_bytes());base=launch['root'];counts={tag:{fn:sum(c['file']==path and c['function']==fn for c in calls) for fn in ('validate','_basis','_checked')} for tag,path in [('current',base+'/code/correspondence.py'),('predecessor',base+'/retained/client-construction/code/correspondence.py')]}
  assert counts['predecessor']['validate']==1;assert counts['current']['validate']==2
  v['recorded_calls']=counts;v['actual_current_public_positives']=1;v['actual_unchanged_predecessor_public_positives']=1;v['actual_public_contention_gate_negatives']=1;v['full_public_negative_derivations_claimed']=0
 return v
mode=sys.argv[1]
if mode=='cut':
 files=declared(T/'input');pin=pack(files,T/'recovery-cut.zip');(T/'recovery-cut-identity.json').write_bytes(enc(pin));root=T/'recovered';root.mkdir()
 with zipfile.ZipFile(T/'recovery-cut.zip') as z:
  for n in z.namelist():p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
 print(json.dumps({'root':str(root),'identity':pin,'purpose':'Frozen corrected inputs for independent fresh-process recovery; no validation completion implied'}),flush=True)
elif mode=='final':
 files=declared(T/'recovered');frozen={n:ident(b) for n,b in files.items()};groups={}
 plans=[('original-witness','Two original defect observations; not passing acceptance controls'),('focused','New source/real-monitoring controls with synthetic predecessor'),('acquisition-races','New actual reservation failure controls with synthetic predecessor'),('cleanup-local','Qualified cleanup-failure observations; no successful cleanup/reuse claim'),('cleanup-callback','Qualified cleanup-failure observations; no successful cleanup/reuse claim'),('cleanup-release','Qualified cleanup-failure observations; no successful cleanup/reuse claim'),('primary','Actual same-process public reuse after corrected source-boundary interruption'),('recovered','Actual same-process public reuse after corrected C-return interruption in recovered root')]
 for name,kind in plans:groups[name]=group(files,name,kind)
 for area in ('tools','preparation','failures'):
  for p in (T/area).rglob('*'):
   if p.is_file():files['ld01/'+area+'/'+p.relative_to(T/area).as_posix()]=p.read_bytes()
 files['ld01/provenance/recovery-cut-manifest.json']=(T/'recovered/MANIFEST.json').read_bytes();files['ld01/provenance/recovery-cut-identity.json']=(T/'recovery-cut-identity.json').read_bytes()
 assert all(ident(files[n])==pin for n,pin in frozen.items())
 old=json.loads(files['retained/ld01-original/MANIFEST.json']);assert all(ident(files['retained/ld01-original/code/correspondence.py'] if n=='code/correspondence.py' else files[n])==pin for n,pin in old.items())
 result={'checkpoint':'I164-LD01-monitoring-lease-correction-1','author':'SU-Engineering[288D]','independent_closure':'PENDING; author controls do not independently close LD-01','prior_review_verdict':'NOT ACCEPTED AS COMPLETE — LD-01','prior_bounded_source_support':'PRESERVED','new_groups_separate':groups,'prior_independent':{'completed':523,'qualified_rows':80,'subsequent_audit':'zero-replay','defect_observations':2},'prior_Engineering':{'source':66,'primary':862,'recovered':391,'zero_control_failures':3},'historical_qualifications':'All retained without repaired or combined totals','implementation':json.loads(files['ld01/provenance/changed-files.json']),'original_declared_members_recoverable_exactly':True,'frozen_corrected_inputs_unchanged':True,'receipt_update':json.loads(files['ld01/provenance/receipt-component-update.json']),'failure_qualification':'Cleanup failure and termination do not establish completed release; synthetic qualified residual states are separate; original witness reviewer cleanup is not candidate cleanup','actual_reuse':'Both actual full positives occur in the same process as corrected interruption, with candidate cleanup already observed and no reviewer release/restart','validation_layers':'Actual public contention-gate negatives; real API interruption/synthetic predecessor controls; authenticated receipt-comparison-core stale receipt; no full public negative derivation claimed','name_identity_scope':'Recorded CPython3.12.14 profile; no generic alternative-runtime or adversarial concurrent ownership guarantee','runtime_observations':'UNAVAILABLE','preservation':{'both_contexts_and_control_prefixes':'UNCHANGED','stop_before_launcher_cleanup_loop_169':True,'both_acquisitions':'Separate; unchanged','obligations':11,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':True,'cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False},'prohibited_operations':dict.fromkeys(('runtime_changes','requests','acquisitions','database_connections','session_operations','Git_saves','policy_changes','completed_campaign_replays'),0)}
 files['ld01/RESULTS.json']=enc(result);target=Path('/workspace/scratch/3da0de3fef10/I164-LD01-monitoring-lease-correction-1.zip');pin=pack(files,target);(T/'FINAL-IDENTITY.json').write_bytes(enc(pin));print(json.dumps({'file':str(target),'identity':pin,'new_groups':groups}),flush=True)
else:raise ValueError(mode)
