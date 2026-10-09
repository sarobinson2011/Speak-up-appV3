"""Conditional exact-byte spool + retained independent parser with trusted local state.
No source authentication, profile integration, signature or qualification is claimed.
"""
import copy,fcntl,hashlib,hmac,json,os,resource,secrets,select,signal,stat,subprocess,time,sys,ssl
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LIMIT=256*1024*1024;STATE_LIMIT=128*1024;PIPE_LIMIT=65536
FORMAT='CP4V-TRUSTED-LOCAL-RECOVERY-1'
MODEL='dd946419e4fd4c657a0a0d663b145e958ddf3c4957bf006b94b5c3f7ec96e74d'
CONTRACT='2bbd9d52e1591bc12adc9cc0983c1686ade2cfc4cbcbeb95b6025259d5bf07fc'
TEXT='dc5776088dfc860e25a42e260b245b607969f6c49346bd6912eecc0ef53d8a74'
DESC='c79ea7fa8e27de3fb051c50f4f50d52cecb51c3d3e0025c9569b174d27882f5f'
class Error(Exception):pass
class Interrupted(Error):pass
def need(x,s):
 if not x:raise Error(s)
def wire(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def load_json(p,maxbytes=STATE_LIMIT):
 with Path(p).open('rb') as f:b=f.read(maxbytes+1)
 need(len(b)<=maxbytes,'JSON capability')
 def unique(xs):
  d={}
  for k,v in xs:need(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(b,object_pairs_hook=unique)
def fsyncdir(d):
 fd=os.open(d,os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
def atom(path,data,fault=None):
 path=Path(path);tmp=path.with_name(path.name+'.part')
 need(not tmp.is_symlink() and not path.is_symlink(),'symlink checkpoint')
 with tmp.open('wb') as f:
  f.write(data)
  if fault:fault('after_write')
  f.flush();os.fsync(f.fileno())
  if fault:fault('after_fsync')
 os.replace(tmp,path)
 if fault:fault('after_replace')
 fsyncdir(path.parent)
 if fault:fault('after_dir_fsync')
def seal(payload,key):
 b=wire(payload);return wire({'payload':payload,'mac':hmac.new(key,b,hashlib.sha256).hexdigest()})
def unseal(path,key):
 d=load_json(path);need(set(d)=={'payload','mac'},'checkpoint envelope');need(hmac.compare_digest(d['mac'],hmac.new(key,wire(d['payload']),hashlib.sha256).hexdigest()),'corrupt checkpoint or wrong key');return d['payload']
def keygen(path):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb') as f:f.write(secrets.token_bytes(32));f.flush();os.fsync(f.fileno())
 fsyncdir(p.parent)
def keyread(path):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb') as f:
  s=os.fstat(f.fileno());b=f.read(33)
 need(stat.S_ISREG(s.st_mode) and not s.st_mode&0o077 and s.st_uid==os.geteuid() and len(b)==32,'private 32-byte local execution key required');return b

def runtime():
 files={}
 for binary in ('emitter_service','validator_service'):
  cp=subprocess.run(['ldd',str(ROOT/'native'/binary)],capture_output=True,text=True,timeout=5);need(cp.returncode==0 and 'not found' not in cp.stdout,'native dependencies unavailable')
  for line in cp.stdout.splitlines():
   for word in line.split():
    if word.startswith('/'):
     p=str(Path(word).resolve());files[p]=sha(p)
 return files

def code_identity():
 paths=['cli.py','adapter/__init__.py','adapter/core.py','native/emitter_service.cpp','native/validator_service.cpp','native/emitter_service','native/validator_service','retained/link_stream/native.cpp']
 return {'format':FORMAT,'files':{p:sha(ROOT/p) for p in paths},'runtime':runtime(),'python':{'version':sys.version,'executable_sha256':sha(Path(sys.executable).resolve()),'openssl':ssl.OPENSSL_VERSION},'native_address_space_limit_bytes':1610612736,'parent_address_space_limit_bytes':536870912}

def check_file(entry):
 need(set(entry)=={'path','bytes','sha256'},'exact input identity fields')
 need('.env' not in Path(entry['path']).parts,'environment files excluded')
 p=Path(entry['path']);need(p.is_absolute() and not p.is_symlink() and p.is_file(),'exact regular input path');need(p.stat().st_size==entry['bytes'] and sha(p)==entry['sha256'],'input byte mutation: '+p.name)

def validate_manifest(m):
 need(set(m)=={'format','model','contract','descriptor','source','expected','serialization','laboratory_only'},'source manifest fields')
 need(m['format']=='CP4V-BYTE-SOURCE-1' and m['laboratory_only'] is True,'conditional source only')
 need(m['serialization']=='S90-FCR-S70-STATIC-LINKS-TSV','serialization binding')
 for k in ['model','contract','descriptor']:check_file(m[k])
 src=m['source'];need(src['kind'] in ['deterministic-laboratory-emitter','immutable-laboratory-file'],'source kind')
 need(set(src)==({'kind'} if src['kind']=='deterministic-laboratory-emitter' else {'kind','file'}),'source fields')
 if src['kind']=='immutable-laboratory-file':
  need(src['file']['bytes']<=LIMIT,'fixture file capability <=256 MiB');check_file(src['file'])
 exp=m['expected'];need(set(exp)=={'bytes','sha256'} and type(exp['bytes']) is int and 0<=exp['bytes']<=2**61-1,'expected length')
 need(type(exp['sha256']) is str and len(exp['sha256'])==64 and all(c in '0123456789abcdef' for c in exp['sha256']),'expected digest')
 if m['model']['sha256']==MODEL:need(m['contract']['sha256']==CONTRACT and m['descriptor']['sha256']==DESC and exp=={'bytes':19909380154846,'sha256':TEXT} and src['kind']=='deterministic-laboratory-emitter','retained model/contract/4U exact correspondence')
 return m

class Service:
 def __init__(self,args):
  self.buf=b''
  def limits():resource.setrlimit(resource.RLIMIT_AS,(1610612736,1610612736));resource.setrlimit(resource.RLIMIT_FSIZE,(LIMIT,LIMIT));resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))
  self.p=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=limits)
  try:self.ready=self.read(55);need(self.ready.get('ready') is True,'worker not ready')
  except BaseException:self.close();raise
 def read(self,seconds):
  deadline=time.monotonic()+seconds
  while b'\n' not in self.buf:
   left=deadline-time.monotonic();need(left>0,'worker deadline; last durable state preserved')
   r,_,_=select.select([self.p.stdout],[],[],left);need(bool(r),'worker deadline; last durable state preserved')
   b=os.read(self.p.stdout.fileno(),4096)
   if not b:
    err=self.p.stderr.read(8192).decode(errors='replace');raise Error('worker exited: '+err)
   self.buf+=b;need(len(self.buf)<=PIPE_LIMIT,'worker response capability')
  line,self.buf=self.buf.split(b'\n',1);return json.loads(line)
 def ask(self,text):
  need(len(text)<PIPE_LIMIT,'request capability');self.p.stdin.write(text.encode()+b'\n');self.p.stdin.flush();return self.read(58)
 def close(self):
  if self.p.poll() is None:
   self.p.terminate()
   try:self.p.wait(timeout=2)
   except subprocess.TimeoutExpired:self.p.kill();self.p.wait()
  for f in [self.p.stdin,self.p.stdout,self.p.stderr]:
   try:f.close()
   except (BrokenPipeError,OSError):pass

def cursor_offset(s):
 if s=='-':return 0
 return int(bytes.fromhex(s).decode().split()[6])

def parent_limit():
 soft,hard=resource.getrlimit(resource.RLIMIT_AS)
 cap=536870912
 if soft!=resource.RLIM_INFINITY:cap=min(cap,soft)
 if hard!=resource.RLIM_INFINITY:cap=min(cap,hard)
 resource.setrlimit(resource.RLIMIT_AS,(cap,hard))

def initialize(job,keypath,manifest,spool_cap=64*1024*1024):
 parent_limit()
 job=Path(job).resolve();need('Speak-up-appV3' not in job.parts,'isolated job required');need(not job.exists(),'new job path required');need(type(spool_cap) is int and 1<=spool_cap<=LIMIT,'spool capability');validate_manifest(manifest);key=keyread(keypath)
 job.mkdir(parents=True,mode=0o700)
 identity={'format':FORMAT,'job_nonce':secrets.token_hex(16),'job_path':str(job),'manifest':manifest,'code':code_identity(),'spool_cap':spool_cap,'trust':'MAC-protected local execution state under a trusted executor and quiescent exact inputs; not source authentication'}
 atom(job/'IDENTITY.json',seal(identity,key))
 state={'format':FORMAT,'identity_sha256':hashlib.sha256(wire(identity)).hexdigest(),'sequence':0,'offset':0,'source_cursor':'-','source_offset':0,'validator_state':'-','spool':None,'status':'PAUSED','result':None,'source_eof':False,'metrics':{'spools_published':0,'spools_evicted':0,'spool_regenerations':0,'generated_bytes':0,'validated_new_bytes':0,'regenerated_bytes':0,'evicted_prefix_bytes_reread':0}}
 atom(job/'STATE.json',seal(state,key));return identity

class Job:
 def __init__(self,job,keypath,fault=None):
  parent_limit()
  self.job=Path(job).resolve();self.key=keyread(keypath);self.fault=fault;self.emitter=None;self.validator=None;self.lock=None;self.ready={}
  try:
   self.lock=(self.job/'LOCK').open('a+b');fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
   self.identity=unseal(self.job/'IDENTITY.json',self.key);need(self.identity['job_path']==str(self.job),'cross-job/path substitution')
   self.state=unseal(self.job/'STATE.json',self.key);need(self.state['identity_sha256']==hashlib.sha256(wire(self.identity)).hexdigest(),'cross-job identity substitution');need(self.identity['code']==code_identity(),'incompatible code/backend/runtime')
   self.manifest=validate_manifest(self.identity['manifest']);need(self.state['format']==FORMAT and type(self.state['sequence']) is int and self.state['sequence']>=0,'state format/sequence')
   need(0<=self.state['offset']<=self.state['source_offset']<=self.manifest['expected']['bytes'],'global byte positions')
   if self.state['status']=='REJECTED':raise Error('terminal rejected input; preserve this job')
   need(self.state['status'] in ('PAUSED','PASS-CONDITIONAL-BYTE-VALIDATION'),'state status')
   if self.state['spool'] is None:
    need(self.state['offset']==self.state['source_offset'],'evicted spool has unconsumed bytes')
    for n in ['spool.bin','spool.part']:(self.job/n).unlink(missing_ok=True)
   self.peak_disk=self.disk_bytes();need(self.peak_disk<=self.disk_bound(),'job disk capability')
  except BaseException:self.close();raise
 def close(self):
  for s in [self.emitter,self.validator]:
   if s:s.close()
  if self.lock:self.lock.close()
 def __enter__(self):return self
 def __exit__(self,*a):self.close()
 def disk_bound(self):return self.identity['spool_cap']+4*STATE_LIMIT+4096
 def disk_bytes(self):return sum(p.stat().st_size for p in self.job.iterdir() if p.is_file())
 def save(self,s):
  b=seal(s,self.key);need(len(b)<=STATE_LIMIT,'checkpoint budget');atom(self.job/'STATE.json',b,self.fault);self.state=s;self.peak_disk=max(self.peak_disk,self.disk_bytes());need(self.peak_disk<=self.disk_bound(),'disk ceiling')
 def services(self,which):
  m=self.manifest
  if which=='emit' and self.emitter is None:
   self.emitter=Service([str(ROOT/'native/emitter_service'),m['descriptor']['path'],m['descriptor']['sha256']]);self.ready['emitter']=self.emitter.ready
  if which=='validate' and self.validator is None:
   self.validator=Service([str(ROOT/'native/validator_service'),m['descriptor']['path'],m['descriptor']['sha256'],str(m['expected']['bytes']),m['expected']['sha256']]);self.ready['validator']=self.validator.ready
 def produce(self,cursor,offset):
  part=self.job/'spool.part';need(not part.is_symlink(),'spool symlink');part.unlink(missing_ok=True);cap=self.identity['spool_cap'];src=self.manifest['source']
  if src['kind']=='deterministic-laboratory-emitter':
   self.services('emit');v=self.emitter.ask(f'EMIT {cap} 50 {cursor} {str(part).encode().hex()}');need(v['start']==offset and v['bytes']==v['end']-offset,'emitter global position')
  else:
   p=Path(src['file']['path']);start=time.monotonic();h=hashlib.sha256();n=0
   with p.open('rb') as f,part.open('xb') as out:
    f.seek(offset)
    while n<cap:
     b=f.read(min(1048576,cap-n))
     if not b:break
     out.write(b);h.update(b);n+=len(b)
    out.flush();os.fsync(out.fileno())
   v={'start':offset,'end':offset+n,'bytes':n,'sha256':h.hexdigest(),'cursor_hex':'-','eof':offset+n==src['file']['bytes'],'seconds':time.monotonic()-start,'rss_kib':None}
  need(v['bytes']<=cap and part.stat().st_size==v['bytes'] and sha(part)==v['sha256'],'emitted spool bytes')
  need(v['end']<=self.manifest['expected']['bytes'],'source exceeded expected byte length')
  need(v['bytes']>0 or v['eof'],'no byte progress; preserve checkpoint for review')
  if self.fault:self.fault('spool_fsynced')
  os.replace(part,self.job/'spool.bin');fsyncdir(self.job)
  if self.fault:self.fault('spool_published')
  return v
 def step(self,new_bytes=None,chunk_bytes=65536):
  s=copy.deepcopy(self.state)
  if s['status']=='PASS-CONDITIONAL-BYTE-VALIDATION':return s['result']
  need(type(chunk_bytes) is int and 1<=chunk_bytes<=1048576,'parser buffer capability')
  cap=self.identity['spool_cap'];budget=cap if new_bytes is None else new_bytes;need(type(budget) is int and 1<=budget<=LIMIT,'new byte budget')
  if s['spool'] is None:
   before=s['source_cursor'];v=self.produce(before,s['source_offset']);s['spool']={k:v[k] for k in ['start','end','bytes','sha256','eof','cursor_hex']};s['spool']['cursor_before']=before;s['source_cursor']=v['cursor_hex'];s['source_offset']=v['end'];s['source_eof']=v['eof'];s['sequence']+=1;s['metrics']['spools_published']+=1;s['metrics']['generated_bytes']+=v['bytes'];s['last_emission_seconds']=v['seconds'];self.save(s)
  meta=s['spool'];path=self.job/'spool.bin'
  if not path.exists():
   v=self.produce(meta['cursor_before'],meta['start']);need(all(v[k]==meta[k] for k in ['start','end','bytes','sha256','eof','cursor_hex']),'regenerated current spool differs');s['metrics']['spool_regenerations']+=1;s['metrics']['regenerated_bytes']+=v['bytes'];s['sequence']+=1;self.save(s)
  need(not path.is_symlink() and path.stat().st_size==meta['bytes'],'spool substitution')
  self.services('validate');v=self.validator.ask(f"VALIDATE {meta['start']} {budget} {chunk_bytes} {int(meta['eof'])} 50 {meta['sha256']} {str(path).encode().hex()} {s['validator_state']}")
  need(s['offset']<=v['offset']<=meta['end'],'validator global offset');s['metrics']['validated_new_bytes']+=v['offset']-s['offset'];s['offset']=v['offset'];s['validator_state']=v['state_hex'];s['sequence']+=1;s['status']=v['result'];s['result']={k:x for k,x in v.items() if k!='state_hex'}
  s['result'].update(source_kind=self.manifest['source']['kind'],source_authenticated=False,four_file_authentication_complete=False,independent_row_validator=True,independent_generator=False,expected_whole_stream_sha256=self.manifest['expected']['sha256'],evicted_prefix_bytes_reread=0)
  if v['complete']:need(v['offset']==self.manifest['expected']['bytes'] and meta['eof'] and v['whole_stream_sha256']==self.manifest['expected']['sha256'],'complete exact bytes')
  if self.fault:self.fault('validation_returned')
  self.save(s)
  if v['result']=='REJECTED':return s['result']
  if s['offset']==meta['end']:
   s=copy.deepcopy(s);s['spool']=None;s['sequence']+=1;s['metrics']['spools_evicted']+=1;self.save(s)
   if self.fault:self.fault('eviction_committed')
   path.unlink(missing_ok=True);fsyncdir(self.job)
  return self.state['result']
