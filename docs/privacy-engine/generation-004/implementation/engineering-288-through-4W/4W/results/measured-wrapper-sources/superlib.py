"""4W local supervision. No qualification, authentication or admission authority."""
import ctypes,fcntl,hashlib,json,os,resource,secrets,signal,subprocess,sys,time,zipfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'runtime'))
from adapter import core
NS=10**9; QUANTUM=15*NS; LOG_CAP=1048576
LIBC=ctypes.CDLL(None,use_errno=True)
def now():return time.clock_gettime_ns(time.CLOCK_BOOTTIME)
def boot():return Path('/proc/sys/kernel/random/boot_id').read_text().strip()
def need(x,msg):core.need(x,msg)
def save(p,obj,key):
 data=core.seal(obj,key);need(len(data)<=core.STATE_LIMIT,'bounded supervisor metadata');core.atom(p,data)
def read(p,key):return core.unseal(p,key)
def binding():
 names=['superlib.py','worker.py','supervisor.py','launch.py','probe.py','probe_worker.py','host.py']
 return {'code':{n:core.sha(ROOT/n) for n in names},'runtime':core.code_identity(),'package_path':str(ROOT),'platform':'Linux pidfd + prctl PDEATHSIG + CLOCK_BOOTTIME'}
def death(parent,limits=False):
 if LIBC.prctl(1,signal.SIGKILL,0,0,0)!=0:raise OSError(ctypes.get_errno(),'prctl')
 if os.getppid()!=parent:os._exit(91)
 if limits:
  resource.setrlimit(resource.RLIMIT_AS,(1610612736,1610612736));resource.setrlimit(resource.RLIMIT_FSIZE,(core.LIMIT,core.LIMIT));resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))
def spawn(args,**kw):
 parent=os.getpid();return subprocess.Popen(args,preexec_fn=lambda:death(parent),**kw)
def killfd(fd,sig=signal.SIGKILL):
 try:signal.pidfd_send_signal(fd,sig)
 except ProcessLookupError:pass
class Lock:
 def __init__(self,p):
  self.fd=os.open(p,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
  try:fcntl.flock(self.fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BaseException:os.close(self.fd);raise core.Error('another writer/launch holds the task lock')
 def close(self):os.close(self.fd)
 def __enter__(self):return self
 def __exit__(self,*a):self.close()
def config(task):
 t=Path(task).resolve();key=core.keyread(t/'execution.key');c=read(t/'CONFIG.json',key)
 need(c['task']==str(t),'cross-task substitution');return t,key,c
def budget(t,key,c):
 b=read(t/'BUDGET.json',key);need(b['config_sha256']==hashlib.sha256(core.wire(c)).hexdigest(),'budget/job substitution');need(0<=b['charged_ns'] and 0<=b['authorized_ns'],'budget integer domain');return b
def bsave(t,key,b):b['sequence']+=1;save(t/'BUDGET.json',b,key)
def create(task,m,spool=64*1048576,test_delay=0,quantum=QUANTUM):
 t=Path(task).resolve();need(not t.exists(),'new 4W task namespace required');need('Speak-up-appV3' not in t.parts and '.env' not in t.parts,'isolated task required');need(1<=spool<=core.LIMIT,'spool cap')
 need(set(m)=={'format','model','contract','descriptor','source','expected','serialization','laboratory_only'} and m['laboratory_only'] is True,'laboratory manifest')
 if m['model']['sha256']==core.MODEL:need(test_delay==0 and quantum==QUANTUM,'no test controls on retained model')
 t.mkdir(parents=True,mode=0o700);core.keygen(t/'execution.key');key=core.keyread(t/'execution.key')
 c={'format':'CP4W-SUPERVISOR-1','task':str(t),'nonce':secrets.token_hex(16),'implementation':binding(),'manifest':m,'spool_cap':spool,'test_delay':test_delay,'quantum_ns':quantum,'actual_admission':False}
 save(t/'CONFIG.json',c,key);b={'format':'CP4W-BUDGET-1','config_sha256':hashlib.sha256(core.wire(c)).hexdigest(),'sequence':0,'authorized_ns':0,'charged_ns':0,'lease':None,'attempts':0,'grants':{},'status':'INITIALIZED-NOT-STARTED','observed_stop_overrun_ns':0};save(t/'BUDGET.json',b,key);return c
def grant(t,key,c,seconds,gid):
 b=budget(t,key,c);need(b['lease'] is None,'pause before granting budget');need(0<seconds<=7*24*3600 and len(gid)<=64 and gid,'grant bounds');amount=int(seconds*NS)
 if gid in b['grants']:need(b['grants'][gid]==amount,'grant id reused with different amount');return b
 need(len(b['grants'])<128,'grant catalog capability');b['grants'][gid]=amount;b['authorized_ns']+=amount;bsave(t,key,b);return b
def reserve(t,key,c):
 b=budget(t,key,c)
 if b['lease'] is not None:
  # Unsettled attempt is conservatively fully charged; no refund on uncertainty.
  b['lease']=None;b['status']='RECOVERED-UNCERTAIN-LEASE-FULLY-CHARGED';bsave(t,key,b)
 remaining=b['authorized_ns']-b['charged_ns'];need(remaining>0,'aggregate budget exhausted; explicit additional grant required')
 n=min(c['quantum_ns'],remaining);start=now();b['attempts']+=1;b['charged_ns']+=n;b['lease']={'id':secrets.token_hex(16),'start_ns':start,'deadline_ns':start+n,'reserved_ns':n,'boot_id':boot()};b['status']='RUNNING';bsave(t,key,b);return b

def renew(t,key,c,b):
 lease=b['lease'];remaining=b['authorized_ns']-b['charged_ns'];n=min(c['quantum_ns'],remaining)
 if n<=0 or now()>=lease['deadline_ns']:return False
 lease['deadline_ns']+=n;lease['reserved_ns']+=n;b['charged_ns']+=n;bsave(t,key,b);return True

def settle(t,key,b,status,detail=None):
 lease=b['lease'];end=now()
 if lease:
  elapsed=max(0,end-lease['start_ns']);unused=max(0,lease['reserved_ns']-elapsed);over=max(0,elapsed-lease['reserved_ns']);b['charged_ns']+=over-unused;b['observed_stop_overrun_ns']+=over;b['last_attempt']={'lease_id':lease['id'],'elapsed_ns':elapsed,'unused_refunded_ns':unused,'stop_overrun_ns':over};b['lease']=None
 b['status']=status;b['detail']=detail;bsave(t,key,b)

def log(t,event):
 d=core.wire({'utc_ns':time.time_ns(),**event});need(len(d)<16384,'log record cap');p=t/'progress.log'
 if p.exists() and p.stat().st_size+len(d)>LOG_CAP:
  (t/'progress.log.2').unlink(missing_ok=True)
  if (t/'progress.log.1').exists():os.replace(t/'progress.log.1',t/'progress.log.2')
  os.replace(p,t/'progress.log.1')
 with p.open('ab') as f:f.write(d);f.flush()

def status(t,key,c):
 b=budget(t,key,c);s=None
 if (t/'data/STATE.json').exists():s=read(t/'data/STATE.json',key)
 running=False
 if (t/'CONTROL.LOCK').exists():
  fd=os.open(t/'CONTROL.LOCK',os.O_RDONLY|os.O_NOFOLLOW)
  try:
   try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);fcntl.flock(fd,fcntl.LOCK_UN)
   except BlockingIOError:running=True
  finally:os.close(fd)
 return {'running':running,'status':b['status'],'authorized_seconds':b['authorized_ns']/NS,'charged_or_reserved_seconds':b['charged_ns']/NS,'unreserved_seconds':max(0,b['authorized_ns']-b['charged_ns'])/NS,'active_lease':b['lease'],'attempts':b['attempts'],'offset':s['offset'] if s else 0,'rows':s['result']['rows'] if s and s['result'] else 0,'expected_bytes':c['manifest']['expected']['bytes'],'validation_status':s['status'] if s else 'NOT-INITIALIZED','actual_admission':False}

def backup(t,key,c):
 b=budget(t,key,c);need(b['lease'] is None,'recover/settle interrupted attempt before backup');need((t/'data/STATE.json').exists(),'no initialized state to back up')
 # Validate exact binding and inputs while quiescent; no row generation.
 with core.Job(t/'data',t/'execution.key'):pass
 files={}
 for name in ['IDENTITY.json','STATE.json','spool.bin']:
  p=t/'data'/name
  if p.exists():files[name]={'bytes':p.stat().st_size,'sha256':core.sha(p)}
 meta={'format':'CP4W-BACKUP-1','config_sha256':b['config_sha256'],'budget_sequence':b['sequence'],'charged_ns':b['charged_ns'],'authorized_ns':b['authorized_ns'],'files':files}
 dest=t/'backup.tmp';need(not dest.exists(),'existing backup.tmp: preserve/remove after inspection')
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_STORED) as z:
  z.writestr('BACKUP.json',core.seal(meta,key))
  for name in files:z.write(t/'data'/name,name)
 with dest.open('rb') as f:os.fsync(f.fileno())
 (t/'backup-1.zip').unlink(missing_ok=True)
 if (t/'backup-0.zip').exists():os.replace(t/'backup-0.zip',t/'backup-1.zip')
 os.replace(dest,t/'backup-0.zip');core.fsyncdir(t)
 return {'result':'PASS-QUIESCENT-BACKUP','path':str(t/'backup-0.zip'),'sha256':core.sha(t/'backup-0.zip'),'offset':read(t/'data/STATE.json',key)['offset'],'budget_restored_on_recovery':False}

def restore(t,key,c,archive):
 b=budget(t,key,c);need(b['lease'] is None,'settle uncertain execution budget first');tmp=t/'restore.tmp';old=t/'previous-data';need(not tmp.exists() and not old.exists(),'preserve/clear previous explicit restore directories before another restore')
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();need(len(names)==len(set(names)) and set(names)<= {'BACKUP.json','STATE.json','IDENTITY.json','spool.bin'} and {'BACKUP.json','STATE.json','IDENTITY.json'}<=set(names),'backup membership')
  need(z.getinfo('BACKUP.json').file_size<core.STATE_LIMIT,'backup metadata bound');env=json.loads(z.read('BACKUP.json'));need(__import__('hmac').compare_digest(env['mac'],__import__('hmac').new(key,core.wire(env['payload']),hashlib.sha256).hexdigest()),'backup MAC');meta=env['payload']
  need(meta['config_sha256']==b['config_sha256'] and b['sequence']>=meta['budget_sequence'] and b['charged_ns']>=meta['charged_ns'] and b['authorized_ns']>=meta['authorized_ns'],'backup/job/budget substitution or rollback')
  need(set(meta['files'])==set(names)-{'BACKUP.json'},'backup file set');tmp.mkdir()
  for name,e in meta['files'].items():
   need(e['bytes']<=(c['spool_cap'] if name=='spool.bin' else core.STATE_LIMIT) and z.getinfo(name).file_size==e['bytes'],'backup size cap')
   with z.open(name) as src,(tmp/name).open('xb') as out:shutil.copyfileobj(src,out,1048576);out.flush();os.fsync(out.fileno())
   need(core.sha(tmp/name)==e['sha256'],'backup byte corruption')
  identity=read(tmp/'IDENTITY.json',key);s=read(tmp/'STATE.json',key);need(identity['job_path']==str(t/'data') and s['identity_sha256']==hashlib.sha256(core.wire(identity)).hexdigest(),'restored validator binding');need(identity['manifest']==c['manifest'] and identity['code']==core.code_identity(),'stale backup input/code')
 try:before=read(t/'data/STATE.json',key)['offset'] if (t/'data/STATE.json').exists() else None
 except Exception:before='CORRUPT-STATE-PRESERVED-IN-PREVIOUS-DATA'
 # Explicit two-rename recovery transaction. Marker permits deterministic completion.
 save(t/'RESTORE.json',{'format':'CP4W-RESTORE-1','budget_sequence':b['sequence'],'state_sha256':core.sha(tmp/'STATE.json')},key);finish_restore(t,key)
 return {'result':'RESTORED-EXPLICITLY','previous_offset':before,'restored_offset':s['offset'],'budget_charged_ns_unchanged':b['charged_ns'],'old_data_preserved':str(old)}
def finish_restore(t,key):
 if not (t/'RESTORE.json').exists():return
 m=read(t/'RESTORE.json',key);tmp=t/'restore.tmp';data=t/'data';old=t/'previous-data'
 if tmp.exists():
  need(core.sha(tmp/'STATE.json')==m['state_sha256'],'restore transaction changed')
  if data.exists():need(not old.exists(),'restore ambiguity');os.replace(data,old);core.fsyncdir(t)
  os.replace(tmp,data);core.fsyncdir(t)
 else:need(data.exists() and core.sha(data/'STATE.json')==m['state_sha256'],'incomplete restore transaction')
 (t/'RESTORE.json').unlink();core.fsyncdir(t)
