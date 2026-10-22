import strict_types as strict
import evidence_record as er
"""Versioned service contract: authoritative executor plans, budgets and saved results.
Only injected OFFLINE backend is exercised. No local fallback or remote sender.
"""
import copy
from anchor import *
from runtime import executor as e
class Service(Anchor):
 def __init__(self,backend,config,prerequisites=None):
  super().__init__(backend,config)
  self.evidence_public=None
  self.provider_policy=None
  self.carrier_policy=parse(enc(prerequisites.get("ethereum_carrier"))) if prerequisites and "ethereum_carrier" in prerequisites else None
  self.staging_required=bool(prerequisites and prerequisites.get("staging_required"))
  if prerequisites is not None:
   from runtime import Guard
   from connected import implementation
   need(config['implementation']==implementation(Guard(),prerequisites),'C4-IMPLEMENTATION')
   if 'outcome_lab_public_key' in prerequisites:
    self.evidence_public=bytes.fromhex(prerequisites['outcome_lab_public_key'])
    need(len(self.evidence_public)==32,'C4-LAB-KEY')
   if 'outcome_provider_policy' in prerequisites:
    import provider
    self.provider_policy=provider.validate_policy(parse(enc(prerequisites['outcome_provider_policy']),MAX_INTENT))
    need(strict.same(self.provider_policy['governing'],{'model':prerequisites['model'],'profile':prerequisites['profile'],'configuration':prerequisites['config']}),'PROVIDER-GOVERNING')
 def genesis(self,coords):
  # New isolated fixture namespaces only; no existing lifetime migration/reset.
  if not self.staging_required:return super().genesis(coords)
  self.check_backend();coordinates(coords)
  s={'binding':self.binding,'seq':0,'head':self.config['origin'],'counts':{'attempt':0,'query':0,'snapshot':0,'verifier':0},'partitions':{'query':0,'snapshot':0,'verifier':0},'u':{},'coordinates':coords}
  self.backend.create(enc(s));return s
 def check_evidence(self,body,s,u,op,ordinal):
  import outcome
  need(self.evidence_public is not None,'C4-PROVIDER-NOT-CONFIGURED')
  need(set(body)=={'evidence'},'C4-BODY')
  v=s['u'][u];need(v.get('near') is not None,'NO-PREPARED-NEAR')
  prepared=parse(self.blob(v['near']['ref'],MAX_INTENT),MAX_INTENT)
  claim=body['evidence']['statement']['claim']['source'] if self.provider_policy is not None else body['evidence']['claim']
  need(strict.same(claim['near_spec'],prepared['near_spec']) and claim['near_hex']==prepared['near_hex'],'EXACT-PREPARED-NEAR')
  evm=self.blob(v['record']['tx_ref'],MAX_TRANSACTION)
  expected=outcome.context(self.config,self.binding,v,u,op,ordinal)
  if self.provider_policy is not None:
   import provider
   return provider.validate(body['evidence'],expected,evm,self.provider_policy)
  return outcome.validate(body['evidence'],expected,evm,self.evidence_public)

 def fresh(self):
  s,raw=self.load()
  # Conditional no-change write is a freshness barrier, not a new history event.
  # A coherent stale HEAD cannot pass CAS against current service storage.
  try:self.backend.commit(raw,raw,{})
  except (OSError,TimeoutError) as ex:raise Uncertain('FRESHNESS-UNKNOWN') from ex
  return s
 def history(self):
  s=self.fresh();previous=self.config['origin'];events=[]
  for seq in range(1,s['seq']+1):
   b=self.backend.get('SEQ/'+str(seq));need(b is not None,'MISSING-HISTORY')
   x=parse(b,MAX_EVENT);need(x['previous']==previous and x['after']['seq']==seq and x['after']['binding']==self.binding,'HISTORY-JOIN')
   previous=sha(b);events.append(x)
  need(previous==s['head'],'HISTORY-HEAD');return s,events
 def apply(self,*args,**kwargs):raise Blocked('USE-VERSIONED-EXECUTOR-SERVICE-INTERFACE')
 def commit(self,expected,op,kind,u=None,body=None,fault=None):
  need(label(op),'OP');body=parse(enc(body or {}),er.MAX_BODY if kind=='OBSERVE_EVIDENCE' else 2*MAX_INTENT+4096)
  req={'binding':self.binding,'expected':expected,'op':op,'kind':kind,'u':u,'body_hash':sha(enc(body))}
  s=self.fresh();prior=self.backend.get('OP/'+op)
  if prior:
   r=self.receipt(prior,s);need(r['request']==req,'DUPLICATE-SUBSTITUTION')
   if kind=='RETIRE':need(self.blob(s['u'][u]['intent'],MAX_INTENT)==bytes.fromhex(body['intent_hex']),'DUPLICATE-EXACT-INTENT')
   elif kind=='BIND_NEAR':need(self.blob(s['u'][u]['near']['ref'],MAX_INTENT)==enc(body),'DUPLICATE-NEAR')
   elif kind=='OBSERVE_EVIDENCE':need(enc(er.load(s['u'][u]['saved']['ref'],self.blob))==enc(body),'DUPLICATE-EXACT-RESULT')
   elif kind=='OBSERVE':need(self.blob(s['u'][u]['saved']['ref'],MAX_INTENT)==enc(body),'DUPLICATE-EXACT-RESULT')
   elif not kind.startswith('STAGE_'):need(not body,'DUPLICATE-BODY')
   return {'receipt':r,'release':False,'duplicate':True}
  need(expected==s['head'] and s['seq']<MAX_EVENTS,'EXPECTED-HEAD-OR-CAPACITY')
  new=copy.deepcopy(s);new.pop('head');new['seq']+=1;blobs={};plan=None
  def blob(b,limit):
   need(type(b) is bytes and 0<len(b)<=limit,'BLOB-BOUND');h=sha(b);blobs['BLOB/'+h]=b;return h
  def transition(record):
   nonlocal plan
   payload=e.enc({'previous':s['coordinates']['executor_head'],'u':u,'record':record})
   need(len(payload)<=e.MAX_LOG,'PLAN-BOUND')
   plan={'payload':blob(payload,e.MAX_LOG),'blobs':list(blobs.keys())}
   new['coordinates']['executor_head']=sha(payload)
   new['u'][u]['record']=record
  stage_release=False
  if kind.startswith('STAGE_'):
   import stages
   need(self.staging_required,'STAGING-NOT-CONFIGURED')
   stage_release=stages.transition(self,s,new,kind,u,body,op,blob)
  elif kind=='RETIRE':
   need(set(body)=={'intent_hex'},'RETIRE-FIELDS');raw=bytes.fromhex(body['intent_hex']);i,_=e.validate_intent(u,raw)
   if self.carrier_policy:
    need(i.get('carrier')==self.carrier_policy['version'],'CARRIER-VERSION')
    for k,j in [('executor','signer'),('chain','chain'),('gas_limit','gas_limit'),('gas_price','gas_price'),('value','value')]:need(i[k]==self.carrier_policy[j],'CARRIER-POLICY:'+k)
   else:need(not i.get('carrier'),'CARRIER-NOT-CONFIGURED')
   need(u not in s['u'] and len(s['u'])<MAX_U,'U-RESERVED')
   nonce=sha(enc([i['chain'],i['executor'],i['nonce']]))
   need(all(v['nonce']!=nonce for v in s['u'].values()),'NONCE-RESERVED')
   ref=blob(raw,MAX_INTENT);new['u'][u]={'nonce':nonce,'intent':ref,'record':None,'saved':None,'attempt':None}
   transition({'status':'RETIRED','intent_ref':ref})
  elif kind in ['SEAL','ATTEMPT','REPAIR','OBSERVE','OBSERVE_EVIDENCE','BIND_NEAR']:
   need(u in s['u'],'U');v=s['u'][u];record=copy.deepcopy(v['record']);status=record['status']
   raw=self.blob(v['intent'],MAX_INTENT);i,tx=e.validate_intent(u,raw)
   if kind in ['SEAL','ATTEMPT'] and self.staging_required:
    need(v.get('stage',{}).get('status')=='AUTHENTICATED-CONDITIONAL','STAGING-NOT-FINALIZED')
   if kind=='SEAL':
    need(not body and status=='RETIRED','SEAL-STATE')
    capsule=e.parse(bytes.fromhex(i['conditional_comparison_hex'] if i.get('carrier') else i['arguments']['evidence']))
    if i.get('carrier'):need(self.carrier_policy is not None,'NO-CONDITIONAL-CARRIER-POLICY')
    need(capsule.get('format')=='I164-COMPUTED-COMPARISON-CAPSULE-1' and capsule.get('permit_for_conditional_test') is True,'CONDITIONAL-COMPARISON')
    record.update(status='SEALED',tx_ref=blob(tx,MAX_TRANSACTION));transition(record)
   elif kind=='BIND_NEAR':
    from runtime import retained
    need(self.evidence_public is not None and status=='SEALED' and v.get('near') is None,'NEAR-PREPARE-STATE')
    need(set(body)=={'near_spec','near_hex'},'NEAR-PREPARE-FIELDS')
    near=bytes.fromhex(body['near_hex']);need(near.hex()==body['near_hex'],'NEAR-HEX')
    txid=retained.t.exact_near(body['near_spec'],tx,near)
    coords=sha(enc([body['near_spec'][k] for k in ['network','signer','public_key','nonce']]))
    need(all(x.get('near',{}).get('nonce_coordinate')!=coords for x in s['u'].values()) and self.backend.get('STAGE-NONCE/'+coords) is None,'NEAR-NONCE-RESERVED')
    new['u'][u]['near']={'ref':blob(enc(body),MAX_INTENT),'transaction_id':txid,'signed_sha256':sha(near),'nonce_coordinate':coords}
   elif kind=='ATTEMPT':
    need(not body and status=='SEALED','ONE-SUBMISSION');need(self.evidence_public is None or v.get('near') is not None,'NO-IMMUTABLE-NEAR');need(s['counts']['attempt']<self.config['limits']['attempt'],'EXHAUSTED')
    need(self.blob(record['tx_ref'],MAX_TRANSACTION)==tx,'EXACT-TRANSACTION')
    
    if self.staging_required and i['method']=='signPetitionWithZKProof':
     need(s['counts']['verifier']<64 and s['partitions']['verifier']<18,'SHARED-VERIFIER-EXHAUSTED')
     new['counts']['verifier']+=1;new['partitions']['verifier']+=1
    new['counts']['attempt']+=1;new['u'][u]['attempt']=op;record['status']='UNCERTAIN';transition(record)
   elif kind=='OBSERVE':
    need(self.evidence_public is None,'C4-NO-LEGACY-VERDICT-BYPASS')
    # Laboratory result provider only; never treated as authenticated finality.
    need(status=='UNCERTAIN' and v['saved'] is None,'OBSERVATION-STATE')
    need(set(body)=={'binding','u','intent','transaction','attempt','outcome','source'},'RESULT-FIELDS')
    need(body['binding']==self.binding and body['u']==u and body['intent']==v['intent'] and body['transaction']==record['tx_ref'] and body['attempt']==v['attempt'],'RESULT-JOIN')
    need(body['source']=='LAB-ONLY' and body['outcome'] in ['SUCCESS','REVERTED','NOT-EXECUTED'],'RESULT-KIND')
    need(s['counts']['query']<self.config['limits']['query'] and s['partitions']['query']<self.config['limits']['staging_query'],'QUERY-EXHAUSTED')
    new['counts']['query']+=1;new['partitions']['query']+=1
    new['u'][u]['saved']={'ref':blob(enc(body),4096),'op':op,'seq':new['seq']}
   elif kind=='OBSERVE_EVIDENCE':
    need(status=='UNCERTAIN' and v['saved'] is None,'OBSERVATION-STATE')
    need(s['counts']['query']<self.config['limits']['query'] and s['partitions']['query']<self.config['limits']['staging_query'],'QUERY-EXHAUSTED')
    result=self.check_evidence(body,s,u,op,s['counts']['query']+1)
    new['counts']['query']+=1;new['partitions']['query']+=1
    new['u'][u]['saved']={'ref':er.store(enc(body),blob),'op':op,'seq':new['seq'],'query_ordinal':new['counts']['query'],'format':'C4-CONDITIONAL-EVIDENCE','result_sha256':sha(enc(result))}
   else:
    need(not body and status=='UNCERTAIN' and v['saved'] is not None,'NO-SAVED-TERMINAL')
    saved=v['saved'];out=er.load(saved['ref'],self.blob)
    charged=self.backend.get('OP/'+saved['op']);need(charged is not None,'NO-CHARGED-RESULT');receipt=self.receipt(charged,s)
    q=receipt['request'];need(strict.same(receipt['seq'],saved['seq']) and q['kind'] in ['OBSERVE','OBSERVE_EVIDENCE'] and q['u']==u and q['body_hash']==sha(enc(out)),'CHARGE-JOIN')
    if q['kind']=='OBSERVE_EVIDENCE':
     need(saved.get('format')=='C4-CONDITIONAL-EVIDENCE','SAVED-FORMAT')
     result=self.check_evidence(out,s,u,saved['op'],saved['query_ordinal'])
     need(sha(enc(result))==saved['result_sha256'],'SAVED-COMPUTATION')
     need(result['conditional_terminal'] in ['SUCCESS','REVERTED'],'C4-UNCERTAIN-OUTCOME')
     out={'binding':self.binding,'u':u,'intent':v['intent'],'transaction':record['tx_ref'],'attempt':v['attempt'],'outcome':result['conditional_terminal'],'source':'LAB-ONLY'}
    else:need(self.evidence_public is None,'C4-NO-LEGACY-SAVED-BYPASS')
    need(out=={'binding':self.binding,'u':u,'intent':v['intent'],'transaction':record['tx_ref'],'attempt':v['attempt'],'outcome':out['outcome'],'source':'LAB-ONLY'},'SAVED-RESULT-JOIN')
    need(out['outcome'] in ['SUCCESS','REVERTED'],'UNCERTAIN-NOT-EXECUTED')
    ev={'conditional_fixture':True,'tx_sha256':record['tx_ref'],'intent_sha256':v['intent'],'outcome':out['outcome'],'finality':'LAB-FINAL','source':'LAB-ORACLE'}
    record.update(status='SUCCESS' if out['outcome']=='SUCCESS' else 'FAILED',reconciliation_ref=blob(e.enc(ev),e.MAX_RECONCILIATION));transition(record)
  else:raise Blocked('UNSUPPORTED')
  event=enc({'request':req,'previous':expected,'after':new,'plan':plan});need(len(event)<=MAX_EVENT,'EVENT-BOUND');head=sha(event);new['head']=head
  raw=enc(new);need(len(raw)<=MAX_STATE,'STATE-BOUND')
  receipt={'request':req,'seq':new['seq'],'head':head};puts={'SEQ/'+str(new['seq']):event,'OP/'+op:enc(receipt)}
  for k,b in blobs.items():
   old=self.backend.get(k)
   if old is None:puts[k]=b
   else:need(old==b,'BLOB-CONFLICT')
  if kind=='STAGE_PREPARE':
   puts['STAGE-NONCE/'+new['u'][u]['stage']['pending']['nonce']]=enc({'u':u,'op':op,'binding':self.binding})
  old=enc(s)
  try:self.backend.commit(old,raw,puts,fault)
  except (OSError,TimeoutError) as ex:raise Uncertain('SERVICE-COMMIT-UNKNOWN: recover; never release') from ex
  self.last=(new['seq'],head)
  return {'receipt':receipt,'release':kind=='ATTEMPT' or stage_release,'duplicate':False}
