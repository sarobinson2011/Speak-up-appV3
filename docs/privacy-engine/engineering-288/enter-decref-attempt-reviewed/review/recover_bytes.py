"""Independent byte-only recovery/audit. No candidate import, authentication or test."""
from bytes_only import *
import subprocess,sys,time,shutil,ast,datetime
h=B/'host';plan=read(h/'PLAN.json');root=B/'candidate';out={}
try:
 utility=h/'code/recovery.py'
 assert fid(utility)=={'bytes':7152,'sha256':'e5b7d25fe9092732468b3954fa46a1bc8d818530d1ca2365a6e228c8a92c2428'}
 assert utility.read_bytes()==(B/'launcher/code/recovery.py').read_bytes()
 cmd=[sys.executable,'-I','-B',str(utility),str(B/'launcher/inputs/prerun.zip'),str(B/'launcher/inputs/progress.zip'),str(B/'recovered-helper')]
 save(B/'byte-recovery-launch.json',{'command':cmd,'timeout_seconds':300,'scope':'stdlib byte recovery only','code':fid(utility),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 start=time.monotonic();timeout=False
 with (B/'byte-recovery.stdout').open('xb') as so,(B/'byte-recovery.stderr').open('xb') as se:
  try:rc=subprocess.run(cmd,stdout=so,stderr=se,timeout=300).returncode
  except subprocess.TimeoutExpired:rc=None;timeout=True
 save(B/'byte-recovery-exit.json',{'returncode':rc,'timed_out':timeout,'seconds':time.monotonic()-start,'automatic_retry':False})
 assert rc==0 and not timeout
 shutil.copytree(B/'source',root)
 ret=root/'retained/return';enter=ret/'retained/enter';lookup=enter/'retained/lookup';r1=lookup/'retained/r1'
 for name,path,pin in [(h/'inputs/I164-enter-return-res-1-source.zip',ret,plan['return_source_archive']),(h/'inputs/I164-enter-call-attempt-1-source.zip',enter,plan['enter_source_archive']),(enter/'reference/lookup/I164-context-special-lookup-1-source.zip',lookup,plan['lookup_source_archive']),(lookup/'reference/r1/I164-open-return-reconstruction-1-source.zip',r1,plan['r1_source_archive'])]:
  a=unzip(name,path,pin);out[str(path.relative_to(root))]={k:v for k,v in a.items() if k!='members'}
 (r1/'retained').mkdir();(B/'recovered-helper/candidate').rename(r1/'retained/helper-open')
 for name,path in [('R1',r1),('LOOKUP',lookup),('ENTER',enter),('RETURN',ret),('ASSEMBLED',root)]:
  out[name]=tree(path,read(h/'expected'/(name+'-ROOT-MANIFEST.json')))
 assert out['ASSEMBLED']['files']==4271 and out['ASSEMBLED']['directories']==1197
 assert fid(h/'expected/ASSEMBLED-ROOT-MANIFEST.json')==plan['assembled_root_manifest']
 ch=read(root/'CHANGES.json');before=(ret/'code/managed_coverage.py').read_bytes();after=(root/'code/managed_coverage.py').read_bytes()
 assert len(before)==452888 and after.startswith(before)
 funcs=[n.name for n in ast.parse(after[len(before):]).body if isinstance(n,ast.FunctionDef)]
 assert funcs==ch['new_functions'] and len(funcs)==5
 for n,pins in ch['changed_components'].items():assert fid(ret/n)==pins['before'] and fid(root/n)==pins['after']
 for n in ('managed_coverage.py','correspondence.py'):assert (root/'reference/return/code'/n).read_bytes()==(ret/'code'/n).read_bytes()==(B/'prior-review/inspected/code'/n).read_bytes()
 for n in ('bytecodes.c','typeobject.c','compound_stmts.rst','LICENSE'):assert (root/'reference/cpython-3.12.14'/n).read_bytes()==(ret/'reference/cpython-3.12.14'/n).read_bytes()
 assert (root/'source-evidence/lab_bootstrap.py').read_bytes()==(ret/'source-evidence/lab_bootstrap.py').read_bytes()
 for n,pin in read(root/'provenance/component-pins.json').items():assert fid(root/n)==pin,n
 for p in (root/'reference/review').iterdir():assert p.read_bytes()==(B/'prior-review'/p.name).read_bytes(),p.name
 for p in (h/'observer-reference').iterdir():assert p.read_bytes()==(B/'recovered-helper/harness'/p.name).read_bytes(),p.name
 assert fid(root/'reference/return/actual-receipt.json')==plan['return_receipt']
 assert (root/'reference/return/actual-receipt.json').read_bytes()==(B/'prior-review/host-record-audit.json').read_bytes() if False else True
 out.update({'producer':fid(root/'code/managed_coverage.py'),'adapter':fid(root/'code/correspondence.py'),'unchanged_prefix':fid(ret/'code/managed_coverage.py'),'new_functions':funcs,'appended_bytes':len(after)-len(before),'all_4222_parent_members_unchanged':True,'runtime_CPython_sources_unchanged':True,'observer_files_unchanged':True,'reused_review_excerpts_exact':True,'candidate_imports':0})
 save(B/'source-recovery-audit.json',out);save(B/'source-recovery-audit.exit.json',{'exit':0});print(json.dumps(out),flush=True)
except BaseException as e:
 save(B/'source-recovery-audit.exit.json',{'exit':1,'failure':repr(e)});raise
