"""Shared pilot lifetime accounting. Local durability is not source qualification.
A separate, non-rollback anchor is REQUIRED; restoring both defeats detection.
"""
import sqlite3,json,hashlib,os
from pathlib import Path
LIMITS={'query':1024,'snapshot':130}
OPS={'status':'query','state-query':'query','rpc-query':'query','reconcile-query':'query','backup':'snapshot','state-snapshot':'snapshot'}
def wire(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def H(x):return hashlib.sha256(x).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def atomic(p,b):
 p=Path(p);t=p.with_suffix('.pending')
 with t.open('wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 os.replace(t,p);fd=os.open(p.parent,os.O_RDONLY);os.fsync(fd);os.close(fd)
class Allowances:
 def __init__(self,path,anchor,pilot,create=False):
  self.path=Path(path);self.anchor=Path(anchor);self.pilot=pilot
  need(self.path.resolve()!=self.anchor.resolve(),'separate anchor');need(self.path.exists()!=create,'exists/missing')
  self.db=sqlite3.connect('file:'+str(self.path.resolve())+'?mode='+('rwc' if create else 'rw'),uri=True,timeout=20,isolation_level=None)
  self.db.execute('PRAGMA synchronous=FULL');self.db.execute('PRAGMA journal_mode=DELETE')
  if create:
   need(not self.anchor.exists(),'anchor exists')
   self.db.execute('CREATE TABLE charges(seq INTEGER PRIMARY KEY,record BLOB,hash TEXT UNIQUE)')
   self.db.execute('CREATE TABLE binding(raw BLOB)');self.db.execute('INSERT INTO binding VALUES (?)',(wire({'pilot':pilot,'limits':LIMITS,'version':'I164-SHARED-ALLOWANCES-1'}),))
   atomic(self.anchor,wire(self._state()))
  need(self.db.execute('SELECT raw FROM binding').fetchone()[0]==wire({'pilot':pilot,'limits':LIMITS,'version':'I164-SHARED-ALLOWANCES-1'}),'pilot/configuration mismatch')
 def close(self):self.db.close()
 def _state(self):
  q=s=0;head='0'*64;seq=0
  for n,raw,h in self.db.execute('SELECT seq,record,hash FROM charges ORDER BY seq'):
   v=json.loads(raw);need(n==seq+1 and H(raw)==h and wire(v)==raw and v['previous']==head and v['pilot']==self.pilot and OPS[v['operation']]==v['kind'],'corrupt accounting chain')
   q+=v['kind']=='query';s+=v['kind']=='snapshot';head=h;seq=n
  need(q<=1024 and s<=130,'budget overflow')
  return {'pilot':self.pilot,'sequence':seq,'head':head,'query':q,'snapshot':s}
 def reserve(self,operation,request_id,after_commit=None):
  need(operation in OPS and type(request_id)is str and 0<len(request_id)<=128,'operation/request')
  self.db.execute('BEGIN IMMEDIATE')
  try:
   st=self._state();anchor=json.loads(self.anchor.read_bytes());need(st==anchor,'ROLLBACK-OR-INTERRUPTED-PUBLICATION: frozen')
   kind=OPS[operation];need(st[kind]<LIMITS[kind],'ALLOWANCE-EXHAUSTED: action not begun')
   v={'pilot':self.pilot,'operation':operation,'kind':kind,'request_id':request_id,'previous':st['head'],'ordinal':st[kind]+1};raw=wire(v);h=H(raw)
   reserved_sequence=st['sequence']+1
   self.db.execute('INSERT INTO charges VALUES (?,?,?)',(reserved_sequence,raw,h));self.db.execute('COMMIT')
   # Exclusive database writer is reacquired before publishing the anchor.
   # Any competing process in this short gap sees disagreement and fails closed.
   self.db.execute('BEGIN IMMEDIATE')
   try:
    if after_commit:after_commit()
    now=self._state()
    if json.loads(self.anchor.read_bytes())!=now:atomic(self.anchor,wire(now))
    self.db.execute('COMMIT')
   except BaseException:self.db.execute('ROLLBACK');raise
   return {'sequence':reserved_sequence,'kind':kind,'ordinal':v['ordinal'],'record_sha256':h,'pilot':self.pilot}
  except BaseException:
   if self.db.in_transaction:self.db.execute('ROLLBACK')
   raise
 def _repair(self,strict):
  self.db.execute('BEGIN IMMEDIATE')
  try:
   now=self._state();old=json.loads(self.anchor.read_bytes());need(old['pilot']==self.pilot and old['sequence']<=now['sequence'],'rollback or wrong pilot')
   records=list(self.db.execute('SELECT record,hash FROM charges ORDER BY seq'));prefix={'pilot':self.pilot,'sequence':0,'head':'0'*64,'query':0,'snapshot':0}
   for raw,h in records[:old['sequence']]:
    v=json.loads(raw);prefix[v['kind']]+=1;prefix['sequence']+=1;prefix['head']=h
   need(prefix==old,'anchor substitution')
   if strict:need(old['sequence']<now['sequence'],'NO-REPAIR-REQUIRED: rejected')
   if old!=now:atomic(self.anchor,wire(now))
   self.db.execute('COMMIT')
  except BaseException:self.db.execute('ROLLBACK');raise
 def repair_anchor(self):
  """Trusted internal maintenance: strict forward repair; returns no state."""
  self._repair(True)
 def _observe(self,operation,request_id):
  receipt=self.reserve(operation,request_id)
  self.db.execute('BEGIN IMMEDIATE')
  try:
   value=self._state();need(value==json.loads(self.anchor.read_bytes()),'unpublished authority: observation withheld')
   raw,h=self.db.execute('SELECT record,hash FROM charges WHERE seq=?',(receipt['sequence'],)).fetchone()
   charge=json.loads(raw);need(h==receipt['record_sha256'] and charge['ordinal']==receipt['ordinal'] and charge['kind']==receipt['kind'] and charge['pilot']==receipt['pilot'],'receipt coordinate mismatch')
   self.db.execute('COMMIT');return receipt,value
  except BaseException:self.db.execute('ROLLBACK');raise
 def state(self,request_id='state-observation'):
  return self._observe('state-query',request_id)
 def reconcile_anchor(self,request_id='reconciliation-observation'):
  self._repair(False) # no externally returned repair state, even at exhaustion
  return self._observe('reconcile-query',request_id)
 def governed(self,operation,request_id,action):
  receipt=self.reserve(operation,request_id);return receipt,action()
