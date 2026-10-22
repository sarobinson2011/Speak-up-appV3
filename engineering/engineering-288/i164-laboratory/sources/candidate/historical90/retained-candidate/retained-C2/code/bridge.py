"""Offline-only bridge; no operational admission, signer or network transport."""
import sys,json,zipfile,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'retained/transport'))
sys.path.insert(0,str(ROOT/'retained/executor-basis/retained/kernel/candidate/executor'))
import transport as t
import session as e
import abi as a
from session_identity import Identity,checked
VERSION='I164-OFFLINE-EXECUTOR-TRANSPORT-CONNECTION-4-SESSION-IDENTITY'

class SharedAllowances:
 """Retained reserve/governed interface, backed by the transport's SINGLE authority.
 The historical 1024-only implementation remains unchanged, not instantiated here.
 """
 OPS={'status':'query','state-query':'query','rpc-query':'query','reconcile-query':'query','backup':'snapshot','state-snapshot':'snapshot'}
 def __init__(self,transport,terminal_repair,identity):self.transport=transport;self.pilot=transport.config['pilot'];self._terminal_repair=terminal_repair;self.identity=identity
 @checked
 def reserve(self,operation,request_id):
  t.need(operation in self.OPS,'ACCOUNTING-OPERATION')
  return self.transport.charge(self.OPS[operation],None,request_id,'other')
 def governed(self,operation,request_id,action):
  receipt=self.reserve(operation,request_id);return receipt,action()
 def repair_anchor(self):self._terminal_repair() # internal only; no returned observation

class Bridge:
 def __init__(self,directory,config,create=False):
  self.identity=Identity(ROOT,sys.modules[__name__],t,e,a)
  self.p=Path(directory);self.p.mkdir(parents=True,exist_ok=True);self.transport=None;self.executor=None
  try:
   self.transport=t.Session(self.p/'transport.db',self.p/'independent-anchor.db',config,create,bound_code=self.identity.digest('retained/transport/transport.py'))
   self.executor=e.Session(self.p/'executor.db',config['pilot'],create,bound_code=self.identity.executor_code())
   self.allowances=SharedAllowances(self.transport,self.internal_terminal_repair,self.identity)
   t.need(config['prerequisites']['accounting']==self.identity.digest('code/bridge.py'),'ACCOUNTING-PREREQUISITE')
   b={'version':VERSION,'bridge_code':self.identity.digest('code/bridge.py'),'executor':self.executor.binding,'transport':self.transport.binding,'open_session':self.identity.binding}
   self.binding=t.enc(b)
   if create:
    t.need(config['prerequisites']['executor']==t.sha(e.enc(self.executor.binding)),'EXECUTOR-PREREQUISITE')
    self.transport.db.execute('CREATE TABLE guard.bridge(binding BLOB,head TEXT,pending BLOB)')
    self.transport.db.execute('INSERT INTO guard.bridge VALUES (?,?,NULL)',(self.binding,self.executor.head))
    self.transport.db.execute('CREATE TABLE guard.reservations(u TEXT PRIMARY KEY,intent BLOB NOT NULL,digest TEXT NOT NULL,old TEXT NOT NULL,next TEXT NOT NULL,nonce TEXT UNIQUE NOT NULL,binding TEXT NOT NULL)')
    self.transport.db.execute("CREATE TRIGGER guard.reservations_no_update BEFORE UPDATE ON reservations BEGIN SELECT RAISE(ABORT,'IMMUTABLE-RESERVATION'); END")
    self.transport.db.execute("CREATE TRIGGER guard.reservations_no_delete BEFORE DELETE ON reservations BEGIN SELECT RAISE(ABORT,'IMMUTABLE-RESERVATION'); END")
   self.recover()
  except BaseException:self.close();raise
 def close(self):
  if self.executor:self.executor.close();self.executor=None
  if self.transport:self.transport.close();self.transport=None
 def __enter__(self):return self
 def __exit__(self,*args):self.close()
 @checked
 def reservations(self):
  rows=self.transport.db.execute('SELECT u,intent,digest,old,next,nonce,binding FROM guard.reservations').fetchall()
  t.need(len(rows)<=e.MAX_ATTEMPTS,'RESERVATION-LIMIT');out={}
  for u,raw,digest,old,nxt,nonce,binding in rows:
   i,_=e.validate_intent(u,raw)
   t.need(e.sha(raw)==digest and binding==t.sha(self.binding),'RESERVATION-BINDING')
   t.need(nonce==t.enc([i['chain'],i['executor'],i['nonce']]).decode(),'RESERVATION-NONCE')
   r={'status':'RETIRED','intent_ref':digest}
   t.need(nxt==e.sha(e.enc({'previous':old,'u':u,'record':r})),'RESERVATION-TRANSITION')
   out[u]={'raw':raw,'digest':digest,'old':old,'next':nxt}
  return out
 @checked
 def recover(self):
  self.transport.reload();self.executor._reload();reserved=self.reservations()
  rows=self.transport.db.execute('SELECT binding,head,pending FROM guard.bridge').fetchall();t.need(len(rows)==1 and rows[0][0]==self.binding,'BRIDGE-BINDING')
  _,head,pending=rows[0]
  if pending:
   x=t.parse(pending);t.need(x['old']==head and self.executor.head in [head,x['next']],'EXECUTOR-RECOVERY-MISMATCH')
   if x.get('kind')=='RETIRE':
    v=reserved.get(x['u']);t.need(v is not None and v['old']==head and v['next']==x['next'],'MISSING-RESERVATION')
    if self.executor.head==head:
     # Rollback and never-committed are indistinguishable: BOTH retain U.
     # Only re-materialize the already authorized immutable retirement; never seal/send.
     self.executor.retire(x['u'],v['raw'])
    t.need(self.executor.head==x['next'],'RETIREMENT-RECOVERY')
   self.transport.db.execute('UPDATE guard.bridge SET head=?,pending=NULL',(self.executor.head,))
  else:t.need(self.executor.head==head,'EXECUTOR-ROLLBACK-OR-UNTRACKED-WRITE')
  states=self.executor.states
  t.need(set(states)==set(reserved),'RESERVATION-COVERAGE')
  for u,v in reserved.items():
   t.need(states[u]['intent_sha256']==v['digest'] and self.executor._blob(v['digest'],e.MAX_INPUT)==v['raw'],'RESERVATION-INTENT')
 @checked
 def transition(self,u,record,action,crash=None):
  self.recover();old=self.executor.head
  nxt=e.sha(e.enc({'previous':old,'u':u,'record':record}))
  self.transport.db.execute('UPDATE guard.bridge SET pending=?',(t.enc({'old':old,'next':nxt}),))
  if crash=='before_executor':raise RuntimeError('crash before executor commit')
  action()
  if crash=='after_executor':raise RuntimeError('crash after executor commit')
  t.need(self.executor.head==nxt,'UNEXPECTED-EXECUTOR-TRANSITION');self.recover()
 @checked
 def retire(self,u,intent,crash=None):
  frozen=e.enc(intent) if type(intent) is dict else bytes(intent)
  self.recover();reserved=self.reservations()
  t.need(u not in reserved,'U-IRREVERSIBLY-RESERVED: use existing lifecycle')
  i,_=e.validate_intent(u,frozen);p=self.transport.config['prerequisites']
  for field,key in [('model','model'),('profile','profile'),('config','configuration')]:t.need(i[field]==p[key],'INTENT-PREREQUISITE')
  t.need(i['chain']=='1313161555','CHAIN');t.need(len(reserved)<e.MAX_ATTEMPTS,'RESERVATION-LIMIT')
  old=self.executor.head;digest=e.sha(frozen)
  record={'status':'RETIRED','intent_ref':digest};nxt=e.sha(e.enc({'previous':old,'u':u,'record':record}))
  if crash=='before_reservation':raise RuntimeError('crash before reservation acceptance')
  db=self.transport.db;db.execute('BEGIN IMMEDIATE')
  try:
   db.execute('INSERT INTO guard.reservations VALUES (?,?,?,?,?,?,?)',(u,frozen,digest,old,nxt,t.enc([i['chain'],i['executor'],i['nonce']]).decode(),t.sha(self.binding)))
   if crash=='inside_reservation':raise RuntimeError('crash before atomic reservation publication')
   db.execute('UPDATE guard.bridge SET pending=?',(t.enc({'kind':'RETIRE','u':u,'old':old,'next':nxt}),))
   db.execute('COMMIT')
  except BaseException:
   if db.in_transaction:db.execute('ROLLBACK')
   raise
  if crash in ['after_reservation','before_executor']:raise RuntimeError('crash after durable reservation')
  self.executor.retire(u,frozen)
  if crash=='after_executor':raise RuntimeError('crash after executor retirement')
  self.recover()
  if crash=='after_clear':raise RuntimeError('crash after completed retirement')
 @checked
 def seal_conditional(self,u,crash=None):
  self.recover();r=dict(self.executor._latest[u]);_,raw=e.validate_intent(u,self.executor._blob(r['intent_ref'],e.MAX_INPUT));r.update(status='SEALED',tx_ref=e.sha(raw))
  self.transition(u,r,lambda:self.executor.seal(u),crash)
 @checked
 def prepare(self,u,near_spec,near_bytes):
  self.recover();v=self.executor.states[u];t.need(v['status']=='SEALED','NOT-SEALED')
  raw=bytes.fromhex(v['synthetic_transaction_hex']);intent=e.enc(v['intent'])
  # Exact laboratory executor envelope, not a real signed EVM transaction.
  h={'kind':'LAB-RETIRED-EXECUTOR-HANDOFF','u':u,'intent_sha256':t.sha(intent),'evm_sha256':t.sha(raw),'retired':True,'executor_head':self.executor.head,'prerequisites':self.transport.config['prerequisites']}
  return self.transport.prepare(u,intent,raw,near_spec,near_bytes,h)
 @checked
 def submit(self,u,request,simulator,crash=None):
  t.need(type(simulator) is t.OfflineTransport,'OFFLINE-ONLY');self.recover()
  rec,near=self.transport.hydrate(self.transport.states[u]);v=self.executor.states[u]
  t.need(v['status']=='SEALED' and v['intent_sha256']==rec['intent_bytes'] and v['tx_sha256']==rec['evm_bytes'] and self.executor.head==rec['handoff']['executor_head'],'EXECUTOR-TRANSPORT-BINDING')
  receipt=self.transport.charge('attempt',u,request)
  if crash=='after_charge':raise RuntimeError('crash after charged attempt')
  r=dict(self.executor._latest[u]);r['status']='UNCERTAIN'
  self.transition(u,r,lambda:self.executor.submission(u), 'after_executor' if crash=='after_executor' else None)
  t.need(self.executor.states[u]['tx_sha256']==rec['evm_bytes'],'RELEASE-BINDING')
  ack=simulator.send(rec,near)
  if crash=='after_send':raise RuntimeError('crash after simulated delivery')
  t.need(ack=={'txid':rec['txid'],'raw_sha256':t.sha(near)},'ACK-SUBSTITUTION')
  self.transport.publish({'type':'ACK','u':u,'attempt':request,'txid':rec['txid']})
  return {'receipt':receipt,'actual_admission':False}
 def _saved_terminal(self,u):
  """Pure validation of existing records; no query, oracle or new evidence input."""
  state=self.transport.states[u]
  if state['status'] not in ['SUCCESS','FAILED']:return None
  rec,near=self.transport.hydrate(state);out=t.parse(self.transport.blob(state['evidence']))
  self.transport.check_outcome(rec,near,out)
  v=self.executor.states.get(u);reservation=self.reservations().get(u)
  t.need(v is not None and reservation is not None,'TERMINAL-U')
  t.need(rec['u']==u and self.transport.blob(rec['intent_bytes'])==reservation['raw'] and e.enc(v['intent'])==reservation['raw'],'TERMINAL-INTENT')
  t.need(v['intent_sha256']==rec['intent_bytes'] and v.get('tx_sha256')==rec['evm_bytes'],'RESULT-JOIN')
  t.need(self.executor._blob(v['tx_sha256'],e.MAX_TRANSACTION)==self.transport.blob(rec['evm_bytes']),'TERMINAL-EXACT-TRANSACTION')
  i=v['intent'];p=self.transport.config['prerequisites']
  for field,key in [('model','model'),('profile','profile'),('config','configuration')]:t.need(i[field]==p[key],'TERMINAL-PREREQUISITE')
  # Rejoin exact sealed head and subsequent submission from executor history.
  sealed=None;submitted=None
  for seq,raw,h in self.executor.db.execute('SELECT seq,payload,digest FROM log ORDER BY seq'):
   x=e.parse(raw,e.MAX_LOG)
   if x['u']==u:
    r=x['record']
    if r['status']=='SEALED':
     t.need(h==rec['handoff']['executor_head'] and r['intent_ref']==rec['intent_bytes'] and r['tx_ref']==rec['evm_bytes'],'TERMINAL-SEALED-HISTORY');sealed=seq
    if r['status']=='UNCERTAIN':submitted=seq
  t.need(sealed is not None and submitted is not None and sealed<submitted,'NO-EXECUTOR-SUBMISSION')
  events=[]
  for seq,raw,h in self.transport.db.execute('SELECT seq,b,h FROM log ORDER BY seq'):
   x=t.parse(raw)
   if x.get('u')==u:events.append((seq,x,h))
  attempts=[x for x in events if x[1]['type']=='ATTEMPT'];outcomes=[x for x in events if x[1]['type']=='OUTCOME']
  t.need(len(attempts)==1 and len(outcomes)==1,'TERMINAL-EVENT-COVERAGE')
  attempt=attempts[0];seq,event,_=outcomes[0]
  receipt=self.transport.receipts.get(event['request'])
  t.need(event['evidence']==state['evidence'] and receipt is not None and receipt['kind']=='query' and receipt['u']==u and receipt['binding']==state['binding'] and receipt['pilot']==self.transport.config['pilot'] and receipt['partition']=='staging','TERMINAL-RECEIPT')
  t.need(attempt[0]<receipt['seq']<seq and attempt[1]['request']==state['attempt_request'],'TERMINAL-ORDER')
  t.need(state['status']==('SUCCESS' if out['near_outcome']=='SUCCESS' and out['evm_outcome']=='SUCCESS' else 'FAILED'),'TERMINAL-STATUS')
  if out['near_outcome']=='FAILURE':
   t.need(out['evm_outcome']=='NOT-EXECUTED' and v['status']=='UNCERTAIN','PRE-EVM-CONFLICT')
   return None # Saved non-execution cannot justify a retained EVM terminal record.
  ev={'conditional_fixture':True,'tx_sha256':v['tx_sha256'],'intent_sha256':v['intent_sha256'],'outcome':out['evm_outcome'],'finality':'LAB-FINAL','source':'LAB-ORACLE'}
  t.need(out['evm_outcome'] in ['SUCCESS','REVERTED'],'TERMINAL-EVM-OUTCOME')
  if v['status'] in ['SUCCESS','FAILED']:
   t.need(v['status']==state['status'] and e.enc(v['reconciliation'])==e.enc(ev),'TERMINAL-CONFLICT')
   return None
  t.need(v['status']=='UNCERTAIN','NO-EXECUTOR-SUBMISSION')
  r=dict(self.executor._latest[u]);r.update(status=state['status'],reconciliation_ref=e.sha(e.enc(ev)))
  return r,ev
 @checked
 def internal_terminal_repair(self,crash=None):
  """No external observation, charge, lookup, send, seal or retry. Returns None."""
  self.recover()
  # Validate all terminal candidates BEFORE any new terminal publication.
  candidates=[(u,self._saved_terminal(u)) for u in self.transport.states]
  before=(dict(self.transport.counts),dict(self.transport.staging),self.transport.head,self.transport.seq)
  if crash=='after_validation':raise RuntimeError('interrupt after terminal validation')
  for u,candidate in candidates:
   if candidate is None:continue
   r,ev=candidate
   if crash=='before_transition':raise RuntimeError('interrupt before terminal transition')
   self.transition(u,r,lambda u=u,ev=ev:self.executor.reconcile(u,ev),crash if crash in ['before_executor','after_executor'] else None)
   if crash=='after_clear':raise RuntimeError('interrupt after terminal clear')
  t.need(before==(self.transport.counts,self.transport.staging,self.transport.head,self.transport.seq),'INTERNAL-ACCOUNTING-CHANGED')
  # Deliberately no return value: an external status still requires a charged query.
 @checked
 def reconcile(self,u,request,simulator,crash=None):
  self.recover();result=self.transport.reconcile(u,request,simulator)
  if crash=='after_transport_result':raise RuntimeError('crash before executor reconciliation')
  self.internal_terminal_repair()
  state=self.transport.states[u]
  if state['status']=='FAILED':
   out=t.parse(self.transport.blob(state['evidence']))
   if out['near_outcome']=='FAILURE':return dict(result,executor_resolution='UNAVAILABLE-NOT-EXECUTED-INTERPRETATION',actual_admission=False)
  return result
 @checked
 def status(self,request):
  self.recover();receipt,value=self.allowances.governed('status',request,self.executor.status)
  return {'receipt':receipt,'executor':value,'actual_admission':False}
 @checked
 def backup(self,path,request):
  self.recover();dest=Path(path);t.need(not dest.exists(),'BACKUP-EXISTS')
  receipt=self.allowances.reserve('backup',request)
  # Locks remain held. The independent anchor is deliberately excluded.
  with dest.open('xb') as stream:
   with zipfile.ZipFile(stream,'w',zipfile.ZIP_STORED) as z:
    for name in ['executor.db','transport.db']:z.write(self.p/name,name)
    z.writestr('binding.json',self.binding)
   stream.flush();os.fsync(stream.fileno())
  t.fsyncdir(dest.parent)
  return {'receipt':receipt,'sha256':t.sha(dest.read_bytes()),'anchor_included':False,'actual_admission':False}
 @checked
 def operational_submit(self,*args,**kwargs):raise t.Blocked('OPERATIONAL-AUTHENTICATION-QUALIFICATION-AND-REAL-SIGNING-UNAVAILABLE')
