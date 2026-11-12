"""New helper-open focused harness; no old campaign replay."""
from pathlib import Path
import os,sys,types,json,hashlib,copy,time,traceback,importlib.metadata,stat,datetime
D=copy.deepcopy
CONTROL_DEADLINE_SECONDS=6600
CALLS=[]
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def module(p):
 p=Path(p);m=types.ModuleType('helper_open_focused');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def verify_root(root):
 root=Path(root);assert stat.S_ISDIR(root.lstat().st_mode);mp=root/'MANIFEST.json';assert stat.S_ISREG(mp.lstat().st_mode)
 m=json.loads(mp.read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs,n;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in expected,n;files.add(n)
 walk(root);assert files==expected and seen==dirs
 for n,pin in m.items():assert identity((root/n).read_bytes())==pin,n
 return {'files':len(files),'directories':len(dirs),'membership_types_hashes':'PASS','manifest':identity(mp.read_bytes())}
def environment():return {'python':sys.version,'implementation':sys.implementation.name,'cryptography':importlib.metadata.version('cryptography'),'isolated':sys.flags.isolated,'dont_write_bytecode':sys.dont_write_bytecode,'optimization':sys.flags.optimize}
class Records:
 def __init__(self,p):self.path=Path(p).resolve();self.path.mkdir(parents=True,exist_ok=False);self.rows=[];self.start=time.monotonic()
 def save(self,n,v):
  p=self.path/n;t=self.path/(n+'.partial');p.parent.mkdir(parents=True,exist_ok=True)
  with t.open('xb') as f:f.write(enc(v));f.flush();os.fsync(f.fileno())
  t.replace(p)
 def event(self,n,**kw):
  v={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':n,'seconds':time.monotonic()-self.start,**kw}
  with (self.path/'events.jsonl').open('a') as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
  print('EVENT',json.dumps(v),flush=True)
 def row(self,n,result,layer,**kw):
  v={'ordinal':len(self.rows)+1,'check':n,'result':result,'layer':layer,**kw};self.save('rows/'+str(v['ordinal']).zfill(5)+'.json',v);self.rows.append(v)
  with (self.path/'progress.jsonl').open('a') as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
  print('CHECK '+json.dumps(v,sort_keys=True),flush=True)
 def yes(self,n,fn,layer):
  assert time.monotonic()-self.start<CONTROL_DEADLINE_SECONDS,'OPEN-CONTROL-DEADLINE';v=fn();assert v is not False,n;self.row(n,'PASS',layer);return v
 def no(self,n,fn,layer,code=None,exception=ValueError):
  assert time.monotonic()-self.start<CONTROL_DEADLINE_SECONDS,'OPEN-CONTROL-DEADLINE'
  try:fn()
  except exception as e:
   if code:assert code in str(e),(n,str(e),code)
   self.row(n,'REJECTED',layer,error=str(e));return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+n)
 def finish(self,error=None,**kw):
  self.save('calls.json',CALLS)
  self.save('RESULT.json',{'result':'PASS' if error is None else 'FAILED-ATTEMPT','checks':len(self.rows),'rows':self.rows,'error':error,'seconds':time.monotonic()-self.start,'environment':environment(),'scope':'Only new helper-entry/open-attempt controls; no old campaign credit','full_public_negative_derivations':0,'independent_closure':'PENDING',**kw})

# External recovery harness only. Candidate tests/common.py is preserved unchanged.
_OBSERVER=None
def guard(root,out,r):
 global _OBSERVER
 n=module(Path(__file__).with_name('native_observer.py'))
 _OBSERVER=n.Observer(root,out,r,CALLS)
 return _OBSERVER.start,_OBSERVER.captures
def close_observer():
 if _OBSERVER is not None:_OBSERVER.close()
