"""Package declared immutable bytes and reconcile saved process results; no model execution."""
from pathlib import Path
import json,hashlib,stat,zipfile,sys,os
T=Path(__file__).resolve().parents[1]
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def declared(root):
 m=json.loads((root/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();found_dirs=set()
 for b,ds,fs in os.walk(root,followlinks=False):
  for n in ds:
   p=Path(b)/n;assert stat.S_ISDIR(p.lstat().st_mode);found_dirs.add(p.relative_to(root).as_posix())
  for n in fs:
   p=Path(b)/n;assert stat.S_ISREG(p.lstat().st_mode);files.add(p.relative_to(root).as_posix())
 assert files==expected and found_dirs==dirs
 out={n:(root/n).read_bytes() for n in m};assert all(identity(out[n])==pin for n,pin in m.items());return out
def pack(files,path):
 assert not path.exists();files=dict(files);assert 'MANIFEST.json' not in files;files['MANIFEST.json']=enc({n:identity(b) for n,b in sorted(files.items())})
 with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
  for n,b in sorted(files.items()):
   p=Path(n);assert not p.is_absolute() and '..' not in p.parts
   info=zipfile.ZipInfo(n,(2026,10,31,0,0,0));info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
 with zipfile.ZipFile(path) as z:
  assert z.namelist()==sorted(files) and len(set(z.namelist()))==len(files)
  for n,b in files.items():assert z.read(n)==b
 return {**identity(path.read_bytes()),'entries':len(files),'manifested_files':len(files)-1,'CRC_membership_hashes':'PASS'}
def group(files,name):
 r=T/'results'/name;p=T/'processes'/name;result=json.loads((r/'RESULT.json').read_bytes());exit_=json.loads((p/'exit-status.json').read_bytes());assert result['result']=='PASS' and exit_['returncode']==0 and not exit_['timed_out']
 rows=[json.loads(x) for x in (r/'progress.jsonl').read_text().splitlines()];lines=[x for x in (p/'stdout.log').read_text().splitlines() if x and x.split(' ',1)[0].isdigit()]
 assert rows==result['rows'] and len(rows)==result['checks']==len(lines)
 for i,(row,line) in enumerate(zip(rows,lines),1):assert line==f"{i} {row['check']} {row['result']}"
 for base,prefix in ((r,'results/'+name),(p,'processes/'+name)):
  for f in base.rglob('*'):
   if f.is_file():files[prefix+'/'+f.relative_to(base).as_posix()]=f.read_bytes()
 return {'checks':len(rows),'result':identity((r/'RESULT.json').read_bytes()),'exit':exit_,'progress_stdout_reconciled':True,'scope':result['scope'],'CLI_execution_claimed':False}
mode=sys.argv[1]
if mode=='cut':
 files=declared(T/'input');primary=group({},'primary')
 for n in ('client-construction-none.json','fixtures.json'):
  files['results/primary/'+n]=(T/'results/primary'/n).read_bytes()
 files['provenance/frozen-input-manifest.json']=(T/'input/MANIFEST.json').read_bytes();files['provenance/recovery-cut-note.json']=enc({'primary_completed':primary,'purpose':'Immutable new recovery root for fresh-process validation; does not claim recovered completion'})
 pin=pack(files,T/'recovery-cut.zip');(T/'recovery-cut-identity.json').write_bytes(enc(pin));root=T/'recovered';root.mkdir()
 with zipfile.ZipFile(T/'recovery-cut.zip') as z:
  for n in z.namelist():p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
 print(json.dumps({'recovered_root':str(root),'identity':pin}),flush=True)
elif mode=='final':
 files=declared(T/'recovered');frozen={n:identity(b) for n,b in files.items()};groups={n:group(files,n) for n in ('primary','recovered')}
 for area in ('failures','tools'):
  for p in (T/area).rglob('*'):
   if p.is_file():files[area+'/'+p.relative_to(T/area).as_posix()]=p.read_bytes()
 files['provenance/recovery-cut-manifest.json']=(T/'recovered/MANIFEST.json').read_bytes();files['provenance/recovery-cut-identity.json']=(T/'recovery-cut-identity.json').read_bytes()
 prior=json.loads(files['provenance/prior-review-incorporation.json']);receipt=json.loads(files['provenance/prior-git-save-receipt.json'])
 result={'checkpoint':'I164-client-construction-none-correspondence-1','construction_author':'SU-Engineering[288D]','independent_review':'PENDING','new_completed_Engineering_groups':groups,'new_failed_attempts':{'primary_membership':{'controls':0,'exit':1,'preserved':'failures/primary-membership','cause_of_extra_entries':'UNESTABLISHED'},'preparation_tool_error':{'controls':0,'preserved':'failures/preparation-textencoder.txt'}},'prior_independent_scope':prior['independent'],'prior_Engineering_qualified_results':prior['Engineering'],'prior_public_rejection_layers':prior['public_rejection_layers'],'older_accounting':prior['older_accounting'],
 'current_public_checks':{'recovered_pristine':'Actual public validator, fresh process on exact recovered root','required_relation_omissions':'Public required-relation/shape gate; no different layer inferred','coordinated_mutations':'Focused constructed/semantic expectations and source-catalogue checks; not claimed as separate full-public derivations','returned_basis_reuse':'Actual mandatory chain basis; no checker replacement','CLI_execution_claimed':False},
 'preserved_Git_save':{'commit':receipt['commit'],'push_status':receipt['push_status'],'repeated':False},'implementation':json.loads(files['provenance/changed-files.json']),'prior_members_unchanged':all(identity(files[n])==pin for n,pin in frozen.items()),
 'operations':{'runtime_changes':0,'requests':0,'acquisitions':0,'database_connections':0,'session_operations':0,'Git_saves':0,'completed_suite_reruns':0,'completed_review_reruns':0,'pipelines':0},
 'limits':{'static_conditional_only':True,'runtime_client_construction_handler_bare_rethrow_revocation_chain':'UNAVAILABLE','constructor_mechanism_allocation_initializer_progress':'UNESTABLISHED','guard_slot_continuity':'Explicit same-owner exact-None premise; not historical absence of storage','selected_owner_continuity':'Explicit conditional premise; not exclusivity','cause_context_suppression':'UNKNOWN','non_none_constructor_branch_complete':False,'outer_cleanup_complete':False,'separate_Client_state_observer':'UNJOINED','physical_identity_exclusivity_durability_qualification':'UNESTABLISHED','repetition_lifetime_completeness':False},
 'preservation':{'both_acquisitions':'Separate; no cross-acquisition occurrence joins','obligations':11,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False},'receipt':identity(files['results/primary/client-construction-none.json'])}
 assert result['prior_members_unchanged'];files['RESULTS.json']=enc(result)
 target=Path('/workspace/scratch/3da0de3fef10/I164-client-construction-none-correspondence-1.zip');pin=pack(files,target);(T/'FINAL-IDENTITY.json').write_bytes(enc(pin));print(json.dumps({'file':str(target),'identity':pin,'groups':groups}),flush=True)
else:raise ValueError(mode)
