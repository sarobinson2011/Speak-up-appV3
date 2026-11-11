"""Prepared launcher only. Separate explicit authorization is required to launch.
Existing/partial workspaces or service units are preserved and never relaunched.
"""
from pathlib import Path
import sys,os,json,zipfile,hashlib,stat,subprocess,shutil,importlib.util,argparse,pwd,datetime
HOME=Path('/home/steve')
BASE=Path('/srv/Engineering-288-execution/steve')
WORK=BASE/'I164-decref-fast-completion-public-1-20261111'
PYTHON=BASE/'I164-helper-open-runtime-20260825/python/bin/python3'
AUTH='I164-DECREF-FAST-COMPLETION-FULL-PUBLIC-POSITIVE-1-20261111'
UNIT='i164-decref-fast-completion-public-1-20261111.service'
def need(ok,s):
 if not ok:raise RuntimeError(s)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def identity(p):
 h=hashlib.sha256();size=0
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);size+=len(b)
 return {'bytes':size,'sha256':h.hexdigest()}
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
def call(cmd,stem,timeout=30):
 save(WORK/(stem+'.started.json'),{'utc':now(),'command':cmd})
 try:r=subprocess.run(cmd,stdin=subprocess.DEVNULL,capture_output=True,timeout=timeout,check=False)
 except subprocess.TimeoutExpired as e:
  save(WORK/(stem+'.exit.json'),{'utc':now(),'exit':None,'timeout':timeout,'outcome':'UNKNOWN; preserve, no automatic retry'})
  for suffix,data in [('stdout',e.stdout),('stderr',e.stderr)]:
   if data is not None:(WORK/(stem+'.'+suffix)).write_bytes(data)
  raise
 for suffix,data in [('stdout',r.stdout),('stderr',r.stderr)]:
  with (WORK/(stem+'.'+suffix)).open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 save(WORK/(stem+'.exit.json'),{'utc':now(),'exit':r.returncode,'timeout':False});return r
def module(name):
 p=WORK/'code'/(name+'.py');s=importlib.util.spec_from_file_location('_decref_fast_host_'+name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def existing():
 print('EXISTING WORKSPACE PRESERVED; no launch or retry:',WORK,flush=True)
 for n in ['ONE-ATTEMPT-RESERVATION.json','LAUNCH-RECEIPT.json','validation/results/RESULT.json','validation/process/exit.json','service-exit.json','manager-exit.json']:
  p=WORK/n
  if p.is_file():print(n,p.read_text()[:5000],flush=True)
def main(bundle,authorization=None):
 os.umask(0o077)
 need(authorization in (None,AUTH),'WRONG-ATTEMPT-AUTHORIZATION')
 need(Path.home()==HOME and pwd.getpwuid(os.getuid()).pw_name=='steve','EXPECTED-STEVE-ACCOUNT')
 if WORK.exists():existing();return
 for p in (Path('/srv'),BASE.parent,BASE):need(p.is_dir() and not p.is_symlink(),'PERSISTENT-PARENT-MISSING-OR-SYMLINK')
 need(BASE.stat().st_uid==os.getuid() and not BASE.stat().st_mode&0o077,'PRIVATE-USER-OWNED-PARENT')
 need(PYTHON.is_file(),'QUALIFIED-INSTALLED-INTERPRETER-MISSING:'+str(PYTHON))
 release={k:v.strip('"') for k,v in (x.split('=',1) for x in Path('/etc/os-release').read_text().splitlines() if '=' in x)}
 need(release.get('ID')=='ubuntu' and release.get('VERSION_ID')=='24.04','UBUNTU-RUNNER-QUALIFICATION-REQUIRED')
 bp=identity(bundle)
 with zipfile.ZipFile(bundle) as z:
  names=z.namelist();need(len(names)==len(set(names)),'BUNDLE-DUPLICATE');manifest=json.loads(z.read('MANIFEST.json'));need(set(names)==set(manifest)|{'MANIFEST.json'},'BUNDLE-MEMBERSHIP')
  for i in z.infolist():
   p=Path(i.filename);need(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG),'BUNDLE-ENTRY')
   b=z.read(i.filename)
   if i.filename in manifest:need({'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}==manifest[i.filename],'BUNDLE-BYTES:'+i.filename)
  plan=json.loads(z.read('PLAN.json'))
  retained=Path(plan['launcher_host_path'])
  need(retained.is_file() and not retained.is_symlink(),'MISSING-PRESERVED-RECOVERY-ARCHIVE:'+str(retained))
  need(identity(retained)==plan['launcher_archive'],'PRESERVED-RECOVERY-ARCHIVE-IDENTITY-MISMATCH')
  matches=[retained] # Exact supplied moved path; no search, transfer or substitution.
  need(shutil.disk_usage(BASE).free>=8*1024**3,'REQUIRE-8-GIB-FREE; no cleanup performed')
  WORK.mkdir(mode=0o700);save(WORK/'preparation-launch.json',{'utc':now(),'bundle':bp,'attempt':AUTH,'python':str(PYTHON),'launcher':str(matches[0]),'status':'PREPARING; no candidate validation'})
  for n in names:
   dest=WORK/n;dest.parent.mkdir(parents=True,exist_ok=True)
   with dest.open('xb') as f:f.write(z.read(n));f.flush();os.fsync(f.fileno())
 try:
  common=module('common_r1')
  print('1/4 Check installed runtime and persistent service manager; no runtime installation.',flush=True)
  r=call([str(PYTHON),'-I','-B',str(WORK/'code/runtime_profile.py'),str(WORK/'observer-reference'),str(WORK/'code/expected-runtime.json')],'host-profile')
  need(r.returncode==0 and json.loads(r.stdout)['matches'],'HOST-PROFILE-MISMATCH: exact differing fields recorded; no override or rebuild')
  r=call(['systemd-run','--version'],'systemd-version');need(r.returncode==0 and int(r.stdout.split()[1])>=254,'SYSTEMD-254-REQUIRED')
  r=call(['loginctl','show-user',str(os.getuid()),'--property=Linger','--value'],'user-linger');need(r.returncode==0 and r.stdout.strip()==b'yes','EXISTING-LINGER-YES-REQUIRED')
  r=call(['systemctl','--user','show','basic.target','--property=ActiveState','--value'],'user-manager');need(r.returncode==0 and r.stdout.strip()==b'active','USER-MANAGER-UNAVAILABLE')
  r=call(['systemctl','--user','show',UNIT,'--property=LoadState','--value'],'unit-before');need(r.stdout.strip()==b'not-found','EXISTING-UNIT-CONTENTION')
  print('2/4 Recover exact parent bytes and assemble fixed fast-completion root, exact decref/return/enter-call/lookup parents and nested R1 predecessor (roughly 1–3 minutes).',flush=True)
  # Validate and extract only required nested inputs; original external ZIP unchanged.
  recovery=module('recovery');need(identity(matches[0])==plan['launcher_archive'],'LAUNCHER-CHANGED')
  with zipfile.ZipFile(matches[0]) as z:
   m=json.loads(z.read('MANIFEST.json'));need(len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(m)|{'MANIFEST.json'},'LAUNCHER-MEMBERSHIP')
   for n in ('inputs/prerun.zip','inputs/progress.zip'):
    raw=z.read(n);need(recovery.identity(raw)==m[n],'NESTED-INPUT-BYTES');dest=WORK/n
    with dest.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
  r=call([str(PYTHON),'-I','-B',str(WORK/'code/recovery.py'),str(WORK/'inputs/prerun.zip'),str(WORK/'inputs/progress.zip'),str(WORK/'recovered-helper')],'byte-recovery',300);need(r.returncode==0,'BYTE-RECOVERY-FAILED; partials preserved')
  common.unzip(WORK/'inputs/I164-decref-fast-completion-1-source.zip',WORK/'candidate',plan['source_archive'])
  root=WORK/'candidate';(root/'retained').mkdir();decref=root/'retained/decref'
  common.unzip(WORK/'inputs/I164-enter-decref-attempt-1-source.zip',decref,plan['decref_source_archive'])
  (decref/'retained').mkdir();ret=decref/'retained/return'
  common.unzip(WORK/'inputs/I164-enter-return-res-1-source.zip',ret,plan['return_source_archive'])
  (ret/'retained').mkdir();enter=ret/'retained/enter'
  common.unzip(WORK/'inputs/I164-enter-call-attempt-1-source.zip',enter,plan['enter_source_archive'])
  (enter/'retained').mkdir();lookup=enter/'retained/lookup'
  common.unzip(enter/'reference/lookup/I164-context-special-lookup-1-source.zip',lookup,plan['lookup_source_archive'])
  (lookup/'retained').mkdir();r1=lookup/'retained/r1'
  common.unzip(lookup/'reference/r1/I164-open-return-reconstruction-1-source.zip',r1,plan['r1_source_archive'])
  (r1/'retained').mkdir();(WORK/'recovered-helper/candidate').rename(r1/'retained/helper-open')
  r1check=common.exact_tree(r1,json.loads((WORK/'expected/R1-ROOT-MANIFEST.json').read_bytes()))
  need(r1check['files']==4090 and r1check['directories']==1142,'R1-ASSEMBLED-MEMBERSHIP');save(WORK/'r1-root.json',r1check)
  lookupcheck=common.exact_tree(lookup,json.loads((WORK/'expected/LOOKUP-ROOT-MANIFEST.json').read_bytes()))
  need(lookupcheck['files']==4124 and lookupcheck['directories']==1155,'LOOKUP-ASSEMBLED-MEMBERSHIP');save(WORK/'lookup-root.json',lookupcheck)
  entercheck=common.exact_tree(enter,json.loads((WORK/'expected/ENTER-ROOT-MANIFEST.json').read_bytes()))
  need(entercheck['files']==4169 and entercheck['directories']==1169,'ENTER-ASSEMBLED-MEMBERSHIP');save(WORK/'enter-root.json',entercheck)
  returncheck=common.exact_tree(ret,json.loads((WORK/'expected/RETURN-ROOT-MANIFEST.json').read_bytes()))
  need(returncheck['files']==4222 and returncheck['directories']==1183,'RETURN-ASSEMBLED-MEMBERSHIP');save(WORK/'return-root.json',returncheck)
  decrefcheck=common.exact_tree(decref,json.loads((WORK/'expected/DECREF-ROOT-MANIFEST.json').read_bytes()))
  need(decrefcheck['files']==4271 and decrefcheck['directories']==1197,'DECREF-ASSEMBLED-MEMBERSHIP');save(WORK/'decref-root.json',decrefcheck)
  need(identity(root/'reference/decref/actual-receipt.json')==plan['decref_receipt'],'DECREF-RECEIPT-PIN')
  need(identity(decref/'reference/return/actual-receipt.json')==plan['return_receipt'],'RETURN-RECEIPT-PIN')
  need(identity(ret/'reference/enter/actual-receipt.json')==plan['enter_receipt'],'ENTER-RECEIPT-PIN')
  need(identity(enter/'reference/lookup/actual-receipt.json')==plan['lookup_receipt'],'LOOKUP-RECEIPT-PIN')
  need(identity(lookup/'reference/r1/actual-receipt.json')==plan['r1_receipt'],'R1-RECEIPT-PIN')
  save(WORK/'assembled-root.json',common.exact_tree(root,json.loads((WORK/'expected/ASSEMBLED-ROOT-MANIFEST.json').read_bytes())))
  recovery.verify_root(r1/'retained/helper-open');recovery.verify_harness(WORK/'observer-reference')
  need(identity(WORK/'expected/expected-decref-fast-receipt.json')==plan['expected_receipt'],'EXPECTED-RECEIPT-PIN')
  save(WORK/'PREPARED.json',{'utc':now(),'bundle':bp,'python':str(PYTHON),'source_archive':plan['source_archive'],'decref_receipt':plan['decref_receipt'],'return_receipt':plan['return_receipt'],'enter_receipt':plan['enter_receipt'],'lookup_receipt':plan['lookup_receipt'],'r1_receipt':plan['r1_receipt'],'expected_receipt':plan['expected_receipt'],'status':'PREPARED ONLY','candidate_public_calls':0,'focused_checks_replayed':0,'old_recording_dummy':'reused saved host qualification; not rerun','admission':False})
  if authorization is None:print('Prepared only. Separate launch authorization required. No public validation started.',flush=True);return
  print('3/4 Reserve and start ONE new public positive. Estimate 60–90 minutes; no retry.',flush=True)
  save(WORK/'ONE-ATTEMPT-RESERVATION.json',{'utc':now(),'authorization':authorization,'attempt':AUTH,'bundle':bp,'source_archive':plan['source_archive'],'expected_receipt':plan['expected_receipt'],'automatic_retries':0,'decref_fast_public_calls_authorized':1})
  cmd=['systemd-run','--user','--no-ask-password','--expand-environment=no','--unit='+UNIT,'--service-type=exec','--property=Restart=no','--property=KillMode=control-group','--property=TimeoutStopSec=30s','--property=RuntimeMaxSec='+str(plan['manager_seconds'])+'s','--property=StandardInput=null','--property=StandardOutput=append:'+str(WORK/'service.stdout'),'--property=StandardError=append:'+str(WORK/'service.stderr'),'--property=ExecStopPost='+str(PYTHON)+' -I -B '+str(WORK/'code/manager_exit.py')+' '+str(WORK/'manager-exit.json'),'--working-directory='+str(WORK),str(PYTHON),'-I','-B',str(WORK/'code/service_entry.py'),str(WORK)]
  r=call(cmd,'service-launch');need(r.returncode==0,'SERVICE-LAUNCH-FAILED-OR-UNCERTAIN; inspect same unit, no retry')
  save(WORK/'LAUNCH-RECEIPT.json',{'utc':now(),'unit':UNIT,'workspace':str(WORK),'attempt':AUTH,'status':'START REQUEST ACCEPTED; not completion','soft_seconds':plan['soft_seconds'],'hard_seconds':plan['hard_seconds'],'manager_seconds':plan['manager_seconds']})
  print('4/4 Start request recorded. The service survives terminal/chat disconnect.',flush=True)
  print('Result:',WORK/'validation/results/RESULT.json',flush=True);print('Explicit child exit:',WORK/'validation/process/exit.json',flush=True)
 except BaseException as e:
  import traceback
  save(WORK/'launcher-failure.json',{'utc':now(),'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'reservation_exists':(WORK/'ONE-ATTEMPT-RESERVATION.json').exists(),'automatic_retry':False});raise
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--bundle',type=Path,required=True);p.add_argument('--authorize');a=p.parse_args();main(a.bundle.resolve(),a.authorize)
