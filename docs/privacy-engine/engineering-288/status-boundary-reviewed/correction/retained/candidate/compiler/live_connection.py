"""Mandatory managed entry point for this bounded laboratory serving slice.
Owns one original, byte-pinned Authority. No raw DB/sign/apply capability is exposed.
This is trusted-process isolation, not protection against Python introspection,
alternate connection owners, hostile key holders or storage rollback.
"""
import copy,threading,json,hashlib
from pathlib import Path
from observation_contract import AUTH,raw_source
import value_flow as vf

class RecoveryBlocked(RuntimeError):pass

class ManagedAuthority:
 def __init__(self,root,path,config,*,ownership_path):
  self._lock=threading.RLock();self._root=Path(root).resolve();self._path=Path(path).resolve();self._owners=Path(ownership_path).resolve();self._config=copy.deepcopy(config)
  self._live=None;self._retired=None;self._phase='CLOSED';self._reason='not opened';self._epoch=0
  import authority
  self._runtime=authority
  if Path(authority.__file__).read_bytes()!=raw_source(self._root,AUTH):raise RecoveryBlocked('SOURCE-MISMATCH')
  vf.s.setup(self._root)
  import ingest
  self._ingest=ingest
 def status(self):
  with self._lock:return {'phase':self._phase,'reason':self._reason,'connection_epoch':self._epoch,'actual_admission':False,'external_nonexecution_established':False,'authorization_renewed':False}
 def _require(self):
  if self._phase!='READY' or self._live is None or self._retired is not None:raise RecoveryBlocked('CONNECTION-'+self._phase)
 def _quarantine(self,reason):
  # Revoke the usable reference BEFORE cleanup or any possibly failing I/O.
  self._phase='QUARANTINED'
  if self._live is not None:self._retired=self._live;self._live=None
  self._reason=reason
 def _run(self,method,*args):
  with self._lock:
   self._require()
   try:
    if self._live.db.in_transaction:raise RecoveryBlocked('UNEXPECTED-ACTIVE-TRANSACTION')
    result=getattr(self._live,method)(*args)
    if self._live.db.in_transaction:raise RecoveryBlocked('UNCOMMITTED-STATE')
    return result
   except BaseException as e:
    self._quarantine(type(e).__name__+':'+str(e));raise
 def state(self):return self._run('state')
 def handle(self,packet,inject=None):return self._run('handle',packet,inject)
 @property
 def binding(self):
  with self._lock:self._require();return self._live.binding
 @property
 def config(self):
  with self._lock:self._require();return copy.deepcopy(self._config)
 def _dispose(self):
  if self._retired is None:return
  self._phase='CLEANUP_UNCERTAIN'
  try:self._retired.close()
  except BaseException as e:
   self._reason='close not confirmed: '+type(e).__name__+':'+str(e);raise
  self._retired=None;self._phase='CLOSED';self._reason='close confirmed'
 def close(self):
  with self._lock:
   self._quarantine('explicit close');self._dispose()
   self._phase='CLOSED';self._reason='close confirmed; no serving connection'
 def _validate(self,a):
  # Full retained ingestion, including exact history/accounting/owner/signature
  # checks. No claim of external anchoring or rollback resistance is implied.
  db=a.db
  if db.in_transaction:raise RecoveryBlocked('REOPEN-ACTIVE-TRANSACTION')
  s=a.state()
  x={'format':'I164-RETRY3-CORRESPONDENCE-EXPORT-1','config':copy.deepcopy(self._config),'expected_head':s['head'],'head':db.execute('SELECT raw FROM head WHERE id=1').fetchone()[0].hex(),
   'events':[[n,b.hex()] for n,b in db.execute('SELECT seq,raw FROM events ORDER BY seq')],
   'blobs':[[n,b.hex()] for n,b in db.execute('SELECT ref,raw FROM blobs ORDER BY ref')],
   'journal':[[n,b.hex(),None if r is None else r.hex()] for n,b,r in db.execute('SELECT challenge,request,response FROM journal ORDER BY challenge')],
   'ownership_meta':db.execute('SELECT raw FROM ownership.meta WHERE id=1').fetchone()[0].hex(),
   'owners':[[n,b.hex(),h] for n,b,h in db.execute('SELECT coord,raw,hash FROM ownership.coordinates ORDER BY coord')]}
  self._ingest.validate_export(x)
  if db.in_transaction:raise RecoveryBlocked('VALIDATION-ACTIVE-TRANSACTION')
  return s['head']
 def recover(self):
  with self._lock:
   if self._phase=='READY':raise RecoveryBlocked('ALREADY-READY')
   if self._live is not None:self._quarantine('interrupted prior disposition')
   # A failed or acknowledgement-lost close MUST be retried to confirmation;
   # do not open a second serving connection while the retired handle is held.
   self._dispose()
   self._phase='OPEN_FAILED';self._reason='open/validation not yet confirmed'
   if not self._path.is_file() or not self._owners.is_file():raise RecoveryBlocked('MISSING-EXISTING-DATABASE')
   a=self._runtime.Authority.__new__(self._runtime.Authority)
   self._retired=a # Retain partially constructed objects for cleanup on failure.
   try:
    # No create, migration, rewritten binding, automatic request or retry.
    self._runtime.Authority.__init__(a,self._path,copy.deepcopy(self._config),ownership_path=self._owners)
    self._phase='VALIDATION_FAILED';head=self._validate(a)
    self._live=a;self._retired=None;self._epoch+=1;self._phase='READY';self._reason='fresh connection and retained history validated'
    return {'status':self.status(),'head':head,'recovery_only':True,'new_attempt_authorized':False}
   except BaseException as e:
    phase=self._phase;self._quarantine(type(e).__name__+':'+str(e));self._retired=a
    if not hasattr(a,'db'):self._retired=None
    else:
     try:self._dispose()
     except BaseException:raise
    self._phase=phase if phase in ('OPEN_FAILED','VALIDATION_FAILED') else 'QUARANTINED';raise

def open_session(root,path,config,*,ownership_path):
 """Normal scheduler/ingress entry point for the managed lab configuration."""
 a=ManagedAuthority(root,path,config,ownership_path=ownership_path);a.recover()
 return a,a._runtime.Scheduler(a)
