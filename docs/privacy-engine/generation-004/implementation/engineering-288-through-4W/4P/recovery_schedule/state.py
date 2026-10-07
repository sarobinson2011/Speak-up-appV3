"""Authenticated computation cache under trusted local execution and quiescent inputs.

A MAC authenticates prior execution, not source truth. Every reused stage checks
its exact inputs. Filesystem metadata is never the byte identity criterion.
"""
import contextvars,hashlib,hmac,json,os,time
from pathlib import Path
from link_recovery.cli import atomic_save,read_key,RecoveryError,fsync_dir
from v4_ingest.records import digest,require,canonical
ACTIVE=contextvars.ContextVar('durable_schedule',default=None)
FORMAT='CP4P-DURABLE-STAGES-1'

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()

class Scheduler:
 def __init__(self,checkpoint,key_path,binding,progress=None,fault=None,deadline=None,auth_new_bytes=None):
  self.root=Path(str(checkpoint)+'.stages').resolve();self.root.mkdir(parents=True,exist_ok=True)
  self.key=read_key(key_path);self.binding=binding;self.progress=progress;self.fault=fault
  self.deadline=deadline;self.auth_new_bytes=auth_new_bytes;self.range_hashes=__import__('semantic_stream.lifetime',fromlist=['ByteLRU']).ByteLRU()
  from metadata_catalog.core import temporary
  self.handles=[];self.checked=temporary(self.root,'checked-');self.receipts=temporary(self.root,'receipts-');self.handles.extend([self.checked,self.receipts]);self.events=[];self.reread=0
 def event(self,stage,status,**fields):
  row={'stage':stage,'status':status,**fields};self.events.append(row)
  if len(self.events)>1024:self.events.pop(0)
  if self.progress:self.progress(row)
 def name(self,label):return hashlib.sha256(label.encode()).hexdigest()
 def read(self,label):
  path=self.root/(self.name(label)+'.json')
  if not path.exists():return None
  with path.open('rb') as f:raw=f.read(1048577)
  require(len(raw)<=1048576,'stage receipt capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  def unique(pairs):
   d={}
   for k,v in pairs:
    require(k not in d,'duplicate stage receipt key');d[k]=v
   return d
  x=json.loads(raw,object_pairs_hook=unique);p=x['payload']
  expected=hmac.new(self.key,canonical(p).rstrip(b'\n'),hashlib.sha256).hexdigest()
  require(hmac.compare_digest(expected,x['hmac_sha256']),'corrupt/substituted stage receipt')
  require(p['format']==FORMAT and p['binding']==self.binding and p['label']==label,'stale/incompatible stage receipt')
  self.receipts[label]=digest(raw)
  from metadata_catalog.receipts import unpack
  return unpack(p,self)
 def save(self,label,inputs,result,complete,prerequisites=None,artifacts=None):
  p={'format':FORMAT,'binding':self.binding,'label':label,'inputs':inputs,'prerequisites':prerequisites or {},'artifacts':artifacts or {},'complete':complete,'result':result,'qualification_established':False}
  from metadata_catalog.receipts import pack
  p=pack(p,self.root)
  path=self.root/(self.name(label)+'.json');atomic_save(path,p,self.key,self.fault);self.receipts[label]=sha(path)
  self.event(label,'COMPLETE' if complete else 'PENDING')
 def verify(self,path,expected,force=False):
  path=Path(path).resolve();key=hashlib.sha256((str(path)+'\0'+expected).encode()).hexdigest()
  # Within one invocation, private snapshots/inputs must remain quiescent under
  # trusted executor custody. A fresh Scheduler rehashes; marks alone never pass.
  if not force and key in self.checked:return
  n=0;h=hashlib.sha256();last=time.monotonic()
  with path.open('rb') as f:
   while b:=f.read(1048576):
    if self.deadline is not None and time.monotonic()>=self.deadline:
     from integrated_auth.collector import Paused
     raise Paused()
    h.update(b);n+=len(b)
    if time.monotonic()-last>=1:self.event('exact-input-recheck','PROGRESS',path=str(path),bytes=n);last=time.monotonic()
  got=h.hexdigest();self.reread+=n
  require(got==expected,'changed exact stage input '+str(path),category='INVALID-EVIDENCE-DIGEST');self.checked[key]=True
 def cached(self,label,inputs,fn,done=lambda r:r.get('complete',False),prerequisites=None,outputs=None):
  old=self.read(label)
  if old is not None:
   require(old['inputs']==inputs and old['prerequisites']==(prerequisites or {}),'substituted stage inputs/prerequisites')
   if old['complete']:
    for path,expected in inputs.get('files',{}).items():self.verify(path,expected)
    for path,expected in old['artifacts'].items():self.verify(path,expected)
    self.event(label,'REUSED-EXACT-INPUTS-RECHECKED');return old['result']
  result=fn();self.save(label,inputs,result,bool(done(result)),prerequisites,outputs() if outputs and done(result) else None);return result

 def close(self):
  for h in self.handles:h.close()
  self.handles.clear();self.range_hashes.clear()
