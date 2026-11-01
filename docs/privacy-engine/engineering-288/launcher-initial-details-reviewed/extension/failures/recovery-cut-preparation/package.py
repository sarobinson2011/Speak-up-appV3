"""Package exact saved bytes and reconcile completed records; no validator execution."""
from pathlib import Path
import json,hashlib,stat,zipfile,sys,os
T=Path(__file__).resolve().parents[1]
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def declared(root):
 m=json.loads((root/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();found=set()
 for b,ds,fs in os.walk(root,followlinks=False):
  for n in ds:
   p=Path(b)/n;assert stat.S_ISDIR(p.lstat().st_mode);found.add(p.relative_to(root).as_posix())
  for n in fs:
   p=Path(b)/n;assert stat.S_ISREG(p.lstat().st_mode);files.add(p.relative_to(root).as_posix())
 assert files==expected and found==dirs
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
 r=T/'results'/name;p=T/'processes'/name;result=json.loads((r/'RESULT.json').read_bytes());ex=json.loads((p/'exit-status.json').read_bytes());assert result['result']=='PASS' and ex['returncode']==0 and not ex['timed_out']
 rows=[json.loads(x) for x in (r/'progress.jsonl').read_text().splitlines()];lines=[x for x in (p/'stdout.log').read_text().splitlines() if x and x.split(' ',1)[0].isdigit()]
 assert rows==result['rows'] and len(rows)==result['checks']==len(lines)
 for i,(row,line) in enumerate(zip(rows,lines),1):assert line==f"{i} {row['check']} {row['result']}"
 launch=json.loads((p/'launch.json').read_bytes());calls=json.loads((r/'calls.json').read_bytes());root=launch['root'];counts={}
 for tag,path in [('current',root+'/code/correspondence.py'),('predecessor',root+'/retained/client-construction/code/correspondence.py')]:
  counts[tag]={fn:sum(x['function']==fn and x['file']==path for x in calls) for fn in ('validate','_basis','_checked')}
 if name!='source-corrected':assert counts['predecessor']['validate']==1 and counts['current']['_basis']==1
 for base,prefix in ((r,'results/'+name),(p,'processes/'+name)):
  for f in base.rglob('*'):
   if f.is_file():files[prefix+'/'+f.relative_to(base).as_posix()]=f.read_bytes()
 return {'checks':len(rows),'result':identity((r/'RESULT.json').read_bytes()),'exit':ex,'progress_stdout_reconciled':True,'scope':result['scope'],'recorded_adapter_calls':counts,'CLI_execution_claimed':False}
mode=sys.argv[1]
if mode=='cut':
 files=declared(T/'input');source=group({},'source-corrected');primary=group({},'primary')
 for n in ('launcher-details.json','fixtures.json'):files['results/primary/'+n]=(T/'results/primary'/n).read_bytes()
 files['provenance/frozen-input-manifest.json']=(T/'input/MANIFEST.json').read_bytes();files['provenance/recovery-cut-note.json']=enc({'source_completed':source,'primary_completed':primary,'purpose':'New immutable recovered root; no claim of recovered completion'})
 pin=pack(files,T/'recovery-cut.zip');(T/'recovery-cut-identity.json').write_bytes(enc(pin));root=T/'recovered';root.mkdir()
 with zipfile.ZipFile(T/'recovery-cut.zip') as z:
  for n in z.namelist():p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
 print(json.dumps({'recovered_root':str(root),'identity':pin}),flush=True)
elif mode=='final':
 files=declared(T/'recovered');frozen={n:identity(b) for n,b in files.items()};groups={n:group(files,n) for n in ('source-corrected','primary','recovered')}
 for area in ('failures','tools'):
  for p in (T/area).rglob('*'):
   if p.is_file():files[area+'/'+p.relative_to(T/area).as_posix()]=p.read_bytes()
 files['provenance/recovery-cut-manifest.json']=(T/'recovered/MANIFEST.json').read_bytes();files['provenance/recovery-cut-identity.json']=(T/'recovery-cut-identity.json').read_bytes()
 prior=json.loads(files['provenance/prior-review-incorporation.json']);receipt=json.loads(files['provenance/prior-git-save-receipt.json'])
 result={'checkpoint':'I164-launcher-initial-details-correspondence-1','construction_author':'SU-Engineering[288D]','independent_review':'PENDING','new_completed_Engineering_groups':groups,
  'new_failed_attempts':{'preparation_tool_error':{'controls':0,'preserved':'failures/preparation-textencoder'},'source_initial':{'controls':0,'exit':1,'failure':'ast.Dict.keys list called as a function','preserved':'failures/source-initial','correction':'New producer only; completed source group is separate'}}},
  'prior_independent':prior['independent'],'prior_Engineering':prior['Engineering'],'prior_validation_layers':prior['validation_layers'],'historical_independent':prior['earlier_independent'],'historical_Engineering':prior['earlier_Engineering'],'historical_public_layers':prior['historical_public_layers'],'older_accounting':prior['older_accounting'],
  'current_validation_layers':{'source_group':'New source/producer controls only; no current prerequisite public validation in this group','primary':'One actual unchanged predecessor public validation used by new mandatory derivation','recovered':'One actual current full public positive, including one actual predecessor public validation','public_negative_calls':'Required-relation/type pre-derivation gates only','checked_core_mutants':'Actual authenticated returned basis reused; not separate full public derivations','checked_receipt_mutants':'Same comparison core used by public validator, without another full derivation','full_public_negative_derivations_demonstrated':0,'CLI_execution_claimed':False,'basis_mechanism':'Passive CPython3.12 monitoring return observation; no validation-function replacement; slot contention stops'},
  'preserved_Git_save':{'commit':receipt['commit'],'push_status':receipt['push_status'],'repeated':False},'implementation':json.loads(files['provenance/changed-files.json']),'frozen_members_unchanged':all(identity(files[n])==pin for n,pin in frozen.items()),
  'operations':dict.fromkeys(('runtime_changes','requests','acquisitions','database_connections','session_operations','Git_saves','completed_suite_reruns','completed_review_reruns','pipelines'),0),
  'limits':{'static_conditional_only':True,'runtime_constructor_handler_details_chain':'UNAVAILABLE','exact_dynamic_field_values_types_bytes':'UNAVAILABLE','selected_pending_error':'Original constructor error required; completed pop alone insufficient','delivery_continuity':'Explicit conditional ordinary generator/context-manager delivery premise','selected_owner_continuity':'Explicit conditional premise; not exclusivity','cause_context_suppression':'UNKNOWN','details_completion':'Expression-origin descriptors and source literal fields; not an observed runtime dictionary','cleanup_loop_covered':False,'non_none_constructor_branch_complete':False,'outer_cleanup_complete':False,'separate_Client_state_observer':'UNJOINED','physical_identity_exclusivity_durability_qualification':'UNESTABLISHED','repetition_lifetime_completeness':False},
  'preservation':{'both_acquisitions':'Separate; no cross-acquisition occurrence joins','obligations':11,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False},'receipt':identity(files['results/primary/launcher-details.json'])}
 assert result['frozen_members_unchanged'];files['RESULTS.json']=enc(result)
 target=Path('/workspace/scratch/3da0de3fef10/I164-launcher-initial-details-correspondence-1.zip');pin=pack(files,target);(T/'FINAL-IDENTITY.json').write_bytes(enc(pin));print(json.dumps({'file':str(target),'identity':pin,'groups':groups}),flush=True)
else:raise ValueError(mode)
