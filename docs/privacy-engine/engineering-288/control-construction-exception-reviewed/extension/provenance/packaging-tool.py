"""Package immutable saved inputs and separately reconciled new controls; no model execution."""
from pathlib import Path
import hashlib,json,os,stat,sys,zipfile
T=Path(__file__).resolve().parents[1]
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def declared(root):
 m=json.loads((root/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};found=set();seen=set()
 for base,ds,fs in os.walk(root,followlinks=False):
  for n in ds:
   p=Path(base)/n;assert stat.S_ISDIR(p.lstat().st_mode);seen.add(p.relative_to(root).as_posix())
  for n in fs:
   p=Path(base)/n;assert stat.S_ISREG(p.lstat().st_mode);found.add(p.relative_to(root).as_posix())
 assert found==expected and seen==dirs,(found-expected,expected-found)
 files={n:(root/n).read_bytes() for n in m};assert all(identity(files[n])==pin for n,pin in m.items());return files
def pack(files,path):
 assert not path.exists();files=dict(files);assert 'MANIFEST.json' not in files
 files['MANIFEST.json']=enc({n:identity(b) for n,b in sorted(files.items())})
 with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
  for n,b in sorted(files.items()):
   p=Path(n);assert not p.is_absolute() and '..' not in p.parts
   info=zipfile.ZipInfo(n,(2026,10,30,0,0,0));info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
 with zipfile.ZipFile(path) as z:
  assert z.namelist()==sorted(files) and len(set(z.namelist()))==len(files)
  for n,b in files.items():assert z.read(n)==b
 return {**identity(path.read_bytes()),'entries':len(files),'manifested_files':len(files)-1,'CRC_exact_membership_hashes':'PASS'}
def group(files,name):
 path=T/'results'/name;p=T/'processes'/name;r=json.loads((path/'RESULT.json').read_bytes());exit_=json.loads((p/'exit-status.json').read_bytes());assert r['result']=='PASS' and exit_['returncode']==0 and not exit_['timed_out']
 progress=[json.loads(x) for x in (path/'progress.jsonl').read_text().splitlines()];stdout=(p/'stdout.log').read_text().splitlines();numbered=[x for x in stdout if x and x.split(' ',1)[0].isdigit()]
 assert progress==r['rows'] and len(progress)==r['checks']==len(numbered)
 for i,(line,row) in enumerate(zip(numbered,progress),1):assert line==f"{i} {row['check']} {row['result']}"
 for base,dest in ((path,'results/'+name),(p,'processes/'+name)):
  for f in base.rglob('*'):
   if f.is_file():files[dest+'/'+f.relative_to(base).as_posix()]=f.read_bytes()
 return {'checks':r['checks'],'outcomes':{k:sum(x['result']==k for x in r['rows']) for k in ('PASS','REJECTED')},'seconds':r['seconds'],'result':identity((path/'RESULT.json').read_bytes()),'progress_stdout_reconciled':True,'exit':exit_}
mode=sys.argv[1]
if mode=='cut':
 files=declared(T/'input')
 for n in ('control-construction.json','fixtures.json'):
  p=T/'results/primary'/n;a=p.stat();b=p.read_bytes();z=p.stat();assert (a.st_size,a.st_mtime_ns)==(z.st_size,z.st_mtime_ns);files['results/primary/'+n]=b
 files['provenance/frozen-input-manifest.json']=(T/'input/MANIFEST.json').read_bytes()
 files['provenance/frozen-cut-note.txt']=b'Frozen immutable implementation/source inputs and already-written canonical receipt/constructed fixtures. This cut does not assert primary campaign completion. Later process results are separately recorded and reconciled.\n'
 pin=pack(files,T/'recovery-cut.zip');(T/'recovery-cut-identity.json').write_bytes(enc(pin));target=T/'recovered';target.mkdir()
 with zipfile.ZipFile(T/'recovery-cut.zip') as z:
  for n in z.namelist():p=target/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
 print(json.dumps({'recovered':str(target),'identity':pin}),flush=True)
elif mode=='final':
 files=declared(T/'recovered');groups={n:group(files,n) for n in ('source-completion','public-final-completion')};frozen=json.loads((T/'recovered/MANIFEST.json').read_bytes())
 files['provenance/recovery-cut-manifest.json']=(T/'recovered/MANIFEST.json').read_bytes();files['provenance/recovery-cut-identity.json']=(T/'recovery-cut-identity.json').read_bytes();files['provenance/packaging-tool.py']=Path(__file__).read_bytes()
 # Include every additional failed/partial attempt, if present; never count it as completion.
 failed=[]
 for area in ('failures',):
  if (T/area).exists():
   for p in (T/area).rglob('*'):
    if p.is_file():files[area+'/'+p.relative_to(T/area).as_posix()]=p.read_bytes();failed.append(area+'/'+p.relative_to(T/area).as_posix())
 for name in ('source_completion.py','recovered_public_completion.py','public_final_completion.py'):
  files['tools/'+name]=(T/'tools'/name).read_bytes()
 interrupted=json.loads((T/'failures/interrupted-processes/RECORD.json').read_bytes())
 interrupted_completion=json.loads((T/'failures/interrupted-completion/RECORD.json').read_bytes())
 for name in ('primary','recovered','public'):
  for area in ('results','processes'):
   a=T/area/name;b=T/'failures/interrupted-processes'/name/area
   if not a.exists():assert not b.exists();continue
   current={p.relative_to(a).as_posix():identity(p.read_bytes()) for p in a.rglob('*') if p.is_file()}
   preserved={p.relative_to(b).as_posix():identity(p.read_bytes()) for p in b.rglob('*') if p.is_file()}
   assert current==preserved,('Interrupted attempt changed after preservation',name,area)
 for area in ('results','processes'):
  a=T/area/'recovered-public-completion';b=T/'failures/interrupted-completion'/area
  assert {p.relative_to(a).as_posix():identity(p.read_bytes()) for p in a.rglob('*') if p.is_file()}=={p.relative_to(b).as_posix():identity(p.read_bytes()) for p in b.rglob('*') if p.is_file()},'Interrupted completion changed after preservation'
 # Verify retained partial rows without promoting the interrupted process to PASS.
 partial=T/'failures/interrupted-processes/primary';pr=[json.loads(x) for x in (partial/'results/progress.jsonl').read_text().splitlines()];ps=[x for x in (partial/'processes/stdout.log').read_text().splitlines() if x and x.split(' ',1)[0].isdigit()]
 assert len(pr)==len(ps)==285
 for i,(line,row) in enumerate(zip(ps,pr),1):assert line==f"{i} {row['check']} {row['result']}"
 partial2=T/'failures/interrupted-completion';pr2=[json.loads(x) for x in (partial2/'results/progress.jsonl').read_text().splitlines()];ps2=[x for x in (partial2/'processes/stdout.log').read_text().splitlines() if x and x.split(' ',1)[0].isdigit()]
 assert len(pr2)==len(ps2)==71
 for i,(line,row) in enumerate(zip(ps2,pr2),1):assert line==f"{i} {row['check']} {row['result']}"
 result={'checkpoint':'I164-control-construction-exception-correspondence-1','construction_author':'SU-Engineering[288D]','independent_review':'PENDING','new_engineering_completed_groups':groups,
  'new_engineering_interrupted_attempts':interrupted,'primary_partial_rows':{'progress_and_stdout_corroborated':285,'completed_group':False,'result_and_exit':'UNRECOVERED','counted_in_completed_groups':False,'replayed':False},
  'interrupted_completion':interrupted_completion,'completion_partial_rows':{'progress_and_stdout_corroborated':71,'row_partitions':interrupted_completion['row_partitions'],'completed_group':False,'result_and_exit':'UNRECOVERED','counted_in_completed_groups':False,'replayed':False},
  'validation_accounting':'Two separate one-check completed groups. The original 285 rows and later 71 rows remain corroborated interrupted evidence; no unqualified combined completed total.',
  'final_public_check_layer':json.loads(files['results/public-final-completion/validator-rejection.json']),
  'prior_independent_scope':{'verdict':'SCOPED SUPPORT WITH RETAINED ACCOUNTING QUALIFICATIONS','result_recorded_rows':520,'corroborated_rows':517,'coordinated_RESULT_progress_stdout':[106,103,103],'qualified_result_only_ordinals':[104,105,106],'historical_partial_public_rows':9,'separately_confirmed_public_check':1,'separate_check_layer':'Public receipt comparison only','separate_check_error':'CONTROL-STALE-OR-ALTERED-RECEIPT','combined_unqualified_total':None,'interrupted_old_public_result_exit':'UNRECOVERED','cause_of_missing_rows':'UNESTABLISHED','rerun':False},
  'prior_supplied_results':{'primary':276,'recovered_root':64,'public_process':7,'rerun':False,'separate_from_current':True},
  'implementation':json.loads(files['provenance/changed-files.json']),'new_failed_attempt_files':failed,'operations':{'runtime_changes':0,'requests':0,'acquisitions':0,'database_connections':0,'session_operations':0,'Git_saves':0,'completed_suite_reruns':0,'completed_review_reruns':0,'pipelines':0},
  'limits':{'static_conditional_only':True,'runtime_construction_error_finally_removal_chain':'UNAVAILABLE','failure_mechanism':'UNESTABLISHED','allocation_initializer_progress':'UNESTABLISHED','selected_owner_continuity':'Explicit conditional premise','existing_cause_context_suppression':'UNKNOWN','outer_cleanup_complete':False,'separate_Client_state_observer':'UNJOINED','physical_identity_exclusivity_durability_qualification':'UNESTABLISHED','repetition_lifetime_completeness':False},
  'preservation':{'obligations':11,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False},
  'new_receipt':identity(files['results/primary/control-construction.json']),'frozen_members_unchanged':all(identity(files[n])==v for n,v in frozen.items())}
 assert result['frozen_members_unchanged'];files['RESULTS.json']=enc(result)
 files['COMPLETION-NOTE.txt']=b'All implementation and frozen input bytes are unchanged. The original primary process preserved 285 corroborated progress/stdout rows but no final RESULT or exit; these remain interrupted evidence outside completed-group totals. The original recovered/public attempts preserved zero controls. Their handles became unavailable and no target process was found in read-only inspection; cause remains UNESTABLISHED. The unfinished source control then completed separately with one intended rejection and exit 0. A sequential fresh recovered-root process used the actual unmodified public validator, observing its private basis return through sys.monitoring without replacing validation functions, and recorded 71 corroborated rows: pristine public acceptance (1), focused recovered controls (64), mandatory public-relation rejections (6). That process also became unavailable during the last public comparison, with no result or exit; its 71 rows remain separately qualified. No CLI execution is claimed. Only the still-unfinished public coordinated comparison was subsequently run once in a separate process, preserving its exact submitted bytes, rejection traceback, result and exit. Its rejection at the public receipt comparison is not attributed to another layer. Do not combine 285, 71 and the two separate one-check completions into an unqualified completed total. No completed-row campaign or prior suite was replayed. See both interrupted-attempt records and the final public witness.\n'
 files['provenance/final-added-files.json']=enc({n:identity(b) for n,b in files.items() if n not in frozen})
 target=Path('/workspace/scratch/3da0de3fef10/I164-control-construction-exception-correspondence-1.zip');pin=pack(files,target);(T/'FINAL-IDENTITY.json').write_bytes(enc(pin));print(json.dumps({'file':str(target),'identity':pin,'groups':groups}),flush=True)
else:raise ValueError(mode)
