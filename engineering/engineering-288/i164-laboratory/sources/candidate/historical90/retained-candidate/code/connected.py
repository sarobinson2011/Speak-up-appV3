import strict_types as strict
import evidence_record as er
"""Normal offline connected interface; the service is the ONLY authoritative anchor.
Local executor.db is a recoverable replica, not a retirement/release authority.
"""
from pathlib import Path
import sqlite3
from anchor import *
from runtime import Guard,executor as e
class OfflineSink:
 def __init__(self):self.sent=[]
 def send(self,raw):self.sent.append(bytes(raw))
def implementation(guard,prerequisites):return sha(enc({'guard':guard.binding,'prerequisites':prerequisites,'version':'SOLE-ANCHOR-1'}))
def evaluate(packet,expected,evm,pre):
 if 'outcome_provider_policy' in pre:
  import provider
  return provider.validate(packet,expected,evm,pre['outcome_provider_policy'])
 import outcome
 return outcome.validate(packet,expected,evm,bytes.fromhex(pre['outcome_lab_public_key']))
class Connected:
 def __init__(self,directory,service,prerequisites,create=False):
  self.guard=Guard();self.service=service;self.prerequisites=parse(enc(prerequisites));self.executor=None;self.outbox=None
  need(service.config['implementation']==implementation(self.guard,self.prerequisites),'IMPLEMENTATION-OR-PREREQUISITES')
  # Validate service BEFORE opening/creating a replica. No genesis or fallback here.
  service.fresh();p=Path(directory);p.mkdir(exist_ok=True,parents=True)
  code=self.guard.base.executor_code();code['sole_anchor']=service.config['implementation']
  try:
   self.executor=e.Session(p/'executor.db',service.config['pilot'],create,bound_code=code)
   out=p/'pending.db';need(out.exists()!=create,'OUTBOX-EXISTS-OR-MISSING')
   self.outbox=sqlite3.connect('file:'+str(out.resolve())+'?mode='+('rwc' if create else 'rw'),uri=True,isolation_level=None)
   self.outbox.execute('PRAGMA synchronous=FULL')
   if create:
    self.outbox.executescript('CREATE TABLE meta(binding TEXT);CREATE TABLE requests(op TEXT PRIMARY KEY,request BLOB NOT NULL);')
    self.outbox.execute('INSERT INTO meta VALUES (?)',(service.binding,))
   need(self.outbox.execute('PRAGMA integrity_check').fetchone()==('ok',),'OUTBOX-CORRUPT')
   need(self.outbox.execute('SELECT binding FROM meta').fetchall()==[(service.binding,)],'OUTBOX-BINDING')
   self.recover()
  except BaseException:self.close();raise
 def close(self):
  if self.outbox:self.outbox.close();self.outbox=None
  if self.executor:self.executor.close();self.executor=None
 def check(self):
  self.guard.check();need(self.service.config['implementation']==implementation(self.guard,self.prerequisites),'IDENTITY-BINDING')
 def recover(self,crash=None):
  self.check();s,events=self.service.history();plans=[]
  if 'outcome_lab_public_key' in self.prerequisites:
   import outcome
   for u,v in s['u'].items():
    saved=v.get('saved')
    if saved is None:continue
    need(saved.get('format')=='C4-CONDITIONAL-EVIDENCE','C4-SAVED-FORMAT')
    body=er.load(saved['ref'],self.service.blob)
    expected=outcome.context(self.service.config,self.service.binding,v,u,saved['op'],saved['query_ordinal'])
    result=evaluate(body['evidence'],expected,self.service.blob(v['record']['tx_ref'],MAX_TRANSACTION),self.prerequisites)
    need(sha(enc(result))==saved['result_sha256'],'C4-SAVED-COMPUTATION')
    receipt=self.service.resolve(saved['op'])['receipt']
    need(receipt is not None and strict.same(receipt['seq'],saved['seq']) and receipt['request']['kind']=='OBSERVE_EVIDENCE' and receipt['request']['u']==u and receipt['request']['body_hash']==sha(enc(body)),'C4-SAVED-RECEIPT')
  for event in events:
   plan=event.get('plan')
   if plan:
    payload=self.service.blob(plan['payload'],e.MAX_LOG);x=e.parse(payload,e.MAX_LOG)
    need(x['u']==event['request']['u'] and x['record']==event['after']['u'][x['u']]['record'],'PLAN-JOIN')
    blobs=[self.service.blob(k.removeprefix('BLOB/'),max(MAX_INTENT,MAX_TRANSACTION)) for k in plan['blobs']]
    plans.append((payload,x,blobs))
  self.executor._reload();local=self.executor.db.execute('SELECT payload FROM log ORDER BY seq').fetchall()
  need(len(local)<=len(plans),'UNAUTHORIZED-LOCAL-HISTORY')
  for n,(raw,) in enumerate(local):need(raw==plans[n][0],'LOCAL-HISTORY-SUBSTITUTION')
  for payload,x,blobs in plans[len(local):]:
   self.check();self.service.fresh() # unavailable service blocks even replay
   need(x['previous']==self.executor.head,'PLAN-PREDECESSOR')
   self.executor._publish(x['u'],x['record'],blobs)
   if crash=='after_local':raise Uncertain('INTERRUPTED-REPLICA-REPAIR')
  need(self.executor.head==s['coordinates']['executor_head'],'EXECUTOR-HEAD')
  # A concurrent service advance blocks action; next recovery may catch up.
  latest=self.service.fresh();need(latest['head']==s['head'],'CONCURRENT-ADVANCE')
  self.check();return s
 def _advance(self,op,kind,u,body=None,crash=None):
  s=self.recover()
  # Pending is only a negative constraint. Only service receipts can resolve it.
  for oldop,raw in self.outbox.execute('SELECT op,request FROM requests'):
   prior=parse(raw,4096);receipt=self.service.resolve(oldop)['receipt']
   need(receipt is not None,'UNRESOLVED-DISPATCH-FROZEN')
   need(receipt['request']==prior,'PENDING-SUBSTITUTION')
  request={'binding':self.service.binding,'expected':s['head'],'op':op,'kind':kind,'u':u,'body_hash':sha(enc(body or {}))}
  # A restored stale outbox cannot grant permission; permanent service OP/U wins.
  self.outbox.execute('INSERT INTO requests VALUES (?,?)',(op,enc(request)))
  if crash=='before_service':raise Uncertain('BEFORE-SERVICE')
  result=self.service.commit(s['head'],op,kind,u,body,fault=crash if crash in ['before','partial','ack_loss'] else None)
  if crash=='after_service':raise Uncertain('AFTER-SERVICE-COMMIT')
  self.recover('after_local' if crash=='after_local' else None)
  self.check();return result
 def retire_compact(self,u,intent,op,crash=None):
  """Explicit new-session representation; old jobs are never migrated."""
  return self.retire(u,e.compact_intent(u,intent),op,crash)
 def retire(self,u,intent,op,crash=None):
  self.check();raw=e.enc(intent) if type(intent) is dict else bytes(intent);i,_=e.validate_intent(u,raw)
  for k in ['model','profile','config']:need(i[k]==self.prerequisites[k],'INTENT-PREREQUISITES')
  need(i['chain']=='1313161555','CHAIN')
  return self._advance(op,'RETIRE',u,{'intent_hex':raw.hex()},crash)
 def seal_conditional(self,u,op):
  if self.prerequisites.get('staging_required'):
   state=self.recover();need(state['u'][u].get('stage',{}).get('status')=='AUTHENTICATED-CONDITIONAL','STAGING-NOT-FINALIZED')
  return self._advance(op,'SEAL',u)
 def submit_conditional(self,u,op,sink,crash=None):
  need(type(sink) is OfflineSink,'OFFLINE-SINK-ONLY')
  # Reject a known-ineligible release before publishing a pending request.
  # Service commit still arbitrates concurrent changes; this is not authority.
  current=self.recover();need(u in current['u'] and current['u'][u]['record']['status']=='SEALED','ONE-SUBMISSION-PRECHECK')
  result=self._advance(op,'ATTEMPT',u,crash=crash)
  need(result['release'],'RECOVERY-NEVER-RELEASES')
  s=self.service.fresh();need(s['head']==result['receipt']['head'],'RELEASE-HEAD-CHANGED')
  r=s['u'][u]['record'];need(r['status']=='UNCERTAIN','RELEASE-STATE')
  raw=self.service.blob(r['tx_ref'],MAX_TRANSACTION)
  need(self.executor._blob(r['tx_ref'],e.MAX_TRANSACTION)==raw,'RELEASE-EXACT-BYTES')
  if 'outcome_lab_public_key' in self.prerequisites:
   v=s['u'][u];need(v.get('near') is not None,'NO-PREPARED-NEAR')
   prepared=parse(self.service.blob(v['near']['ref'],MAX_INTENT),MAX_INTENT)
   from runtime import retained
   near=bytes.fromhex(prepared['near_hex']);need(retained.t.exact_near(prepared['near_spec'],raw,near)==v['near']['transaction_id'] and sha(near)==v['near']['signed_sha256'],'RELEASE-EXACT-NEAR')
   raw=near
  self.check();sink.send(raw)
  if crash=='after_send':raise Uncertain('SEND-ACK-UNKNOWN')
  return {'conditional_send':True,'actual_admission':False}
 def save_conditional_observation(self,u,op,outcome,crash=None):
  # An externally returned fixture observation is charged atomically with storage.
  s=self.recover();v=s['u'][u]
  body={'binding':self.service.binding,'u':u,'intent':v['intent'],'transaction':v['record'].get('tx_ref'),'attempt':v['attempt'],'outcome':outcome,'source':'LAB-ONLY'}
  return self._advance(op,'OBSERVE',u,body,crash)
 def bind_near_conditional(self,u,op,near_spec,near_bytes):
  return self._advance(op,'BIND_NEAR',u,{'near_spec':near_spec,'near_hex':bytes(near_bytes).hex()})
 def save_outcome_evidence(self,u,op,packet,crash=None):
  # No observation is returned before its durable, service-owned charge.
  import outcome
  s=self.recover();v=s['u'][u]
  expected=outcome.context(self.service.config,self.service.binding,v,u,op,s['counts']['query']+1)
  body=parse(enc({'evidence':packet}),er.MAX_BODY)
  evaluate(body['evidence'],expected,self.service.blob(v['record']['tx_ref'],MAX_TRANSACTION),self.prerequisites)
  return self._advance(op,'OBSERVE_EVIDENCE',u,body,crash)
 def internal_terminal_repair(self,crash=None):
  s=self.recover();counts=copy_counts(s)
  for u,v in s['u'].items():
   if v['record']['status']!='UNCERTAIN' or v['saved'] is None:continue
   out=er.load(v['saved']['ref'],self.service.blob)
   if v['saved'].get('format')=='C4-CONDITIONAL-EVIDENCE':
    import outcome
    expected=outcome.context(self.service.config,self.service.binding,v,u,v['saved']['op'],v['saved']['query_ordinal'])
    result=evaluate(out['evidence'],expected,self.service.blob(v['record']['tx_ref'],MAX_TRANSACTION),self.prerequisites)
    need(sha(enc(result))==v['saved']['result_sha256'],'C4-SAVED-COMPUTATION')
    if result['conditional_terminal'] is None:continue
   elif out['outcome']=='NOT-EXECUTED':continue
   self._advance('repair-'+sha(enc([u,v['saved']])),'REPAIR',u,crash=crash)
  need(copy_counts(self.recover())==counts,'REPAIR-ACCOUNTING-CHANGED')
  # No result observation or release; None is intentional.
 def operational_submit(self,*args,**kwargs):raise Blocked('OPERATIONAL-AUTHENTICATION-QUALIFICATION-UNAVAILABLE')
def copy_counts(s):return enc([s['counts'],s['partitions']])
