"""Package declared immutable inputs and new results; no validator execution."""
from pathlib import Path
import sys,json,hashlib,stat,os,zipfile,types
TASK=Path('/workspace/i164-control-offline');BASE=Path('/workspace/scratch/3da0de3fef10')
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def read_declared(root):
 m=json.loads((root/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};actual=set();seen=set()
 for base,ds,fs in os.walk(root,followlinks=False):
  for n in ds:
   p=Path(base)/n;assert stat.S_ISDIR(p.lstat().st_mode);seen.add(p.relative_to(root).as_posix())
  for n in fs:
   p=Path(base)/n;assert stat.S_ISREG(p.lstat().st_mode);actual.add(p.relative_to(root).as_posix())
 assert actual==expected and seen==dirs,(actual-expected,expected-actual)
 files={n:(root/n).read_bytes() for n in m}
 assert all(identity(files[n])==pin for n,pin in m.items());return files
spec=BASE/'git-bare/extension/tools/checkpoint.py';mod=types.ModuleType('pack');mod.__file__=str(spec);exec(compile(spec.read_bytes(),str(spec),'exec'),mod.__dict__)
def add_results(files,name):
 r=TASK/'results'/name;result=json.loads((r/'RESULT.json').read_bytes());assert result['result']=='PASS';progress=[json.loads(x) for x in (r/'progress.jsonl').read_text().splitlines()];assert progress==result['rows'] and len(progress)==result['checks'];lines=(TASK/(name+'.stdout')).read_text().splitlines();actual=[x for x in lines if x and x.split(' ',1)[0].isdigit()];assert len(actual)==len(progress),(name,len(actual),len(progress))
 for i,(line,row) in enumerate(zip(actual,progress),1):assert line==f"{i} {row['check']} {row['result']}"
 for p in r.rglob('*'):
  if p.is_file():files['results/'+name+'/'+p.relative_to(r).as_posix()]=p.read_bytes()
 files['results/'+name+'/process.stdout']=(TASK/(name+'.stdout')).read_bytes();return result
if sys.argv[1]=='cut':
 files=read_declared(TASK/'input')
 # These files were fully written before the source-variant controls began.
 # The cut makes no claim that the ongoing primary campaign is complete.
 for n in ('control-exception.json','fixtures.json'):
  p=TASK/'results/primary'/n;before=p.stat();b=p.read_bytes();after=p.stat();assert (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns);files['results/primary/'+n]=b
 files['provenance/cut-stage.txt']=b'Frozen immutable source inputs and already-written canonical receipt/fixtures while the primary source-variant controls continued. No primary completion inferred. Final packaging separately reconciles completed primary/process/recovery results.\n'
 files['failures/initial-membership/failed-root-MANIFEST.json']=(BASE/'control-work/checkpoint/MANIFEST.json').read_bytes()
 files['failures/second-membership/failed-root-MANIFEST.json']=(BASE/'control-work/candidate/MANIFEST.json').read_bytes()
 files['failures/environment-note.txt']=b'Two zero-control attempts stopped at exact predecessor membership gates. The second root passed its initial complete gate before an undeclared file was later encountered. A workspace synchronizer was present, but causation is not established. Failed roots were left unrepaired. A separate root outside the synchronized working tree was reconstructed from declared archive bytes for the subsequent checks; no gate was weakened and no candidate code changed. Runtime source and historical evidence are unchanged.\n'
 target=TASK/'recovery-cut.zip';pin=mod.pack(files,target);(TASK/'cut-identity.json').write_bytes(enc(pin));print(json.dumps(pin));mod.verify(target,TASK/'recovered');print('Recovered frozen cut; no candidate execution')
elif sys.argv[1]=='final':
 files=read_declared(TASK/'recovered');groups={name:add_results(files,name) for name in ('primary','recovered','public')}
 frozen=json.loads((TASK/'recovered/MANIFEST.json').read_bytes());files['provenance/recovery-cut-manifest.json']=(TASK/'recovered/MANIFEST.json').read_bytes();files['provenance/recovery-cut-identity.json']=(TASK/'cut-identity.json').read_bytes()
 files['provenance/recovery-cut-note.txt']=b'The frozen tested input cut excludes the final process-result/provenance additions. Every frozen member remains byte-identical. The cut ZIP is retained externally; its exact manifest and identity are included. No reconstruction of its original compression bytes is claimed.\n'
 files['provenance/packaging-tool.py']=Path(__file__).read_bytes()
 files['provenance/environment-note-clarification.txt']=b"The frozen failure note's phrase 'outside the synchronized working tree' was not established by a watcher-scope check. The established fact is recovery into a separate local path, /workspace/i164-control-offline. Synchronizer processes were observed, but their involvement and the origins of the undeclared files remain UNESTABLISHED. A process-environment inspection was denied; no escalation or bypass was attempted. This clarification preserves the original note and does not change code, control results or the membership gates.\n"
 predecessor=json.loads(files['retained/bare/RESULTS.json']);review=json.loads(files['retained/review/CHECKPOINT.json'])
 result={'checkpoint':'I164-control-callback-exception-correspondence-1','construction_author':'SU-Engineering[288D]','independent_review':'PENDING','new_engineering_controls':{name:{'checks':r['checks'],'outcomes':{kind:sum(x['result']==kind for x in r['rows']) for kind in ('PASS','REJECTED')},'seconds':r['seconds'],'result_identity':identity(files['results/'+name+'/RESULT.json']),'progress_and_stdout_reconciled':True} for name,r in groups.items()},'new_engineering_completed_controls':sum(r['checks'] for r in groups.values()),'actual_CLI_counted_once_in_public_group':True,'environment':groups['primary']['environment'],'new_failed_attempts':[json.loads(files['failures/initial-membership/RECORD.json']),json.loads(files['failures/second-membership/RECORD.json'])],
 'prior_results_not_rerun':{'independent_controls':review['independent_controls'],'review':identity(files['retained/review/CHECKPOINT.json']),'Engineering_primary_result_progress_stdout':[308,307,303],'cause':'UNESTABLISHED','missing_progress_ordinal':304,'missing_progress_record':{'check':'adjacent normal-callback stored failure preserved 1','result':'PASS'},'missing_stdout_ordinals':[304,305,306,307,308],'separate_recovered_public':[78,5],'original_reconciliation':predecessor['primary_log_reconciliation'],'prior_failures_and_partials':'PRESERVED EXACTLY'},
 'implementation':json.loads(files['provenance/changed-files.json']),'operations':{'runtime_changes':0,'requests':0,'acquisitions':0,'database_connections':0,'session_operations':0,'Git_saves':0,'completed_suite_reruns':0,'completed_review_reruns':0,'pipelines':0},
 'limits':{'runtime_control_exception_revocation_chain':'UNAVAILABLE','control_exception_producer_history':'UNAVAILABLE','selected_owner_continuity':'Explicit conditional premise; not runtime exclusivity','owner_failure_guard_applicable':False,'existing_cause_context_suppression':'UNKNOWN','subsequent_client_execution_established':False,'outer_cleanup_complete':False,'control_constructor_exception_expansion':False,'saved_traced_invocations':18,'separate_unjoined_observer':1,'repetition_lifetime_completeness':False,'physical_reference_identity':'UNESTABLISHED','durability_exclusivity_qualification':'UNESTABLISHED'},'preservation':predecessor['preservation'],'new_receipt':identity(files['results/primary/control-exception.json']),'frozen_members_unchanged':all(identity(files[n])==v for n,v in frozen.items())}
 assert result['frozen_members_unchanged'];files['RESULTS.json']=enc(result)
 files['START-HERE.txt']=b'Read README.md, SEMANTICS.md, RESULTS.json and RECOVERY.md. This is one new SOURCE-ONLY static control-callback exception continuation, pending independent review. All earlier reviewed evidence and failures remain separate. Do not execute application/session code or rerun completed campaigns.\n'
 files['provenance/final-added-files.json']=enc({n:identity(b) for n,b in sorted(files.items()) if n not in frozen})
 target=BASE/'I164-control-callback-exception-correspondence-1.zip';pin=mod.pack(files,target);(TASK/'FINAL-IDENTITY.json').write_bytes(enc(pin));print(json.dumps({'archive':str(target),'identity':pin,'new_engineering_controls':result['new_engineering_controls']}))
else:raise ValueError('Unknown packaging stage')
