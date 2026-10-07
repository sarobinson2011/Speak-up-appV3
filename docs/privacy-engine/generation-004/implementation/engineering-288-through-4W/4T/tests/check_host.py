import contextlib,importlib.util,io,json,os,subprocess,sys,tempfile,time,types,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];W=R.parent;sys.path.insert(0,str(R));import run_task as rt
sp=importlib.util.spec_from_file_location('test_bootstrap',R/'bootstrap.py');bp=importlib.util.module_from_spec(sp);sp.loader.exec_module(bp)
checks=[];start=time.monotonic();zpath=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else W/'Engineering-288-checkpoint-4T.zip'
with tempfile.TemporaryDirectory(prefix='4t-install-',dir=W) as td:
 target=Path(td)/'textual-4T'
 with zipfile.ZipFile(zpath) as z:
  r=bp.preflight(z,target);assert not target.exists() and r['native']['result']=='PASS';checks.append({'name':'actual-cloud-read-only-preflight','result':'PASS-CHECK-BEHAVIOR','observed_preflight_result':r['result'],'errors':r['errors'],'not_user_host':True,'no_target_created':True,'native':r['native'],'available_memory':r['available_memory']})
  memory=bp.memory_available
  try:
   bp.memory_available=lambda:{'effective_available_bytes':1};r=bp.preflight(z,target);assert any('8 GiB' in e for e in r['errors']);checks.append({'name':'insufficient-memory-rejected','result':'PASS'})
  finally:bp.memory_available=memory
  statvfs=bp.os.statvfs
  try:
   def insufficient(path):
    st=statvfs(path);d={k:getattr(st,k) for k in ('f_bavail','f_frsize','f_flag','f_favail')};d['f_bavail']=0;return types.SimpleNamespace(**d)
   bp.os.statvfs=insufficient;r=bp.preflight(z,target);assert any('insufficient disk' in e for e in r['errors']);checks.append({'name':'insufficient-disk-rejected','result':'PASS'})
  finally:bp.os.statvfs=statvfs
 # Isolated positive-capacity fixture for installer tests, not a host-capacity claim.
 bp.memory_available=lambda:{'effective_available_bytes':9*1024**3,'test_fixture_only':True}
 with contextlib.redirect_stdout(io.StringIO()):assert bp.main(zpath,'install',target)==0
 kit=target/R.name;assert not (target/'textual').exists() and not (target/'supervisor').exists();assert os.access(kit/'runner/links',os.X_OK)
 # Isolated positive-capacity fixture for installer tests, not a host-capacity claim.
 bp.memory_available=lambda:{'effective_available_bytes':9*1024**3,'test_fixture_only':True}
 with contextlib.redirect_stdout(io.StringIO()):assert bp.main(zpath,'install',target)==0
 checks.append({'name':'atomic-idempotent-install-does-not-start-job','result':'PASS','positive_memory_capacity_was_test_fixture':True})
 result=subprocess.run([sys.executable,'-B',str(kit/'run_task.py'),'run','--task',str(target/'denied-new-job')],capture_output=True,text=True,timeout=20);assert result.returncode==2 and '--authorize-review-hours 48' in result.stderr and not (target/'denied-new-job').exists();checks.append({'name':'missing-separate-text-budget-rejected-before-job-creation','result':'PASS'})
 # Final kit read-only checks, not a native full-stream invocation.
 result=subprocess.run([sys.executable,'-B',str(kit/'tools/verify.py')],capture_output=True,text=True,timeout=20);assert result.returncode==0,result.stderr;checks.append({'name':'installed-fresh-byte-identities','result':'PASS'})
rt.atomic(R/'results/HOST-INTEGRATION-CHECKS.json',{'result':'PASS','checks':checks,'seconds':time.monotonic()-start,'tested_preseal_zip_sha256':rt.filehash(zpath),'actual_user_host_checked':False,'full_stream_started':False,'installer_code_sha256':rt.filehash(R/'bootstrap.py')})
print(json.dumps({'result':'PASS','checks':len(checks),'seconds':time.monotonic()-start}))
