import strict_types as strict
"""Canonical offline authenticated service boundary. LAB request MAC / response signature; no network.
The in-process channel is not a Python security sandbox or production TLS service.
"""
import hmac,hashlib,secrets,sqlite3
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey,Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from anchor import enc,parse,sha,need,digest,Blocked,Uncertain,MAX_EVENT,MAX_STATE,MAX_INTENT,MAX_TRANSACTION
from runtime import Guard,executor as e
from connected import implementation
REQUEST_LIMIT=3145728+65536+8192 # implementation envelope; adopted action allowances unchanged
RESPONSE_LIMIT=1048576
FORMAT='I164-SERVICE-WIRE-1'
MAX_CALLS=12000*32 # unchanged per-journal implementation cap, NOT a lifetime/action budget
JOURNAL_FORMAT='I164-WIRE-JOURNAL-ATOMIC-2'
def tag(key,raw):return hmac.new(key,raw,hashlib.sha256).hexdigest()
def public(seed):return Ed25519PrivateKey.from_private_bytes(seed).public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
def signature(seed,r):return Ed25519PrivateKey.from_private_bytes(seed).sign(b'I164-LAB-SERVICE-RESPONSE-1\0'+enc(r)).hex()
def policy_binding(principals,response_public):
 return sha(enc({'version':'LAB-INGRESS-POLICY-1','principals':{k:{'credential_sha256':sha(v[0]),'roles':sorted(v[1])} for k,v in sorted(principals.items())},'response_public_key':response_public.hex()}))
def policy_record(config,principals,response_public):
 return {'version':'LAB-INGRESS-POLICY-1','service_binding':sha(enc(config)),'principals':{k:{'credential_sha256':sha(v[0]),'roles':sorted(v[1])} for k,v in sorted(principals.items())},'response_public_key':response_public.hex()}
def exact(x,keys):need(type(x) is dict and set(x)==set(keys),'WIRE-FIELDS')
def receipt_check(receipt,event,binding):
 exact(receipt,['request','seq','head']);need(type(receipt['seq']) is int and receipt['seq']>0,'RECEIPT-SEQ')
 need(sha(enc(event))==receipt['head'] and event['request']==receipt['request'],'RECEIPT-EVENT')
 need(event['after']['binding']==binding and event['after']['seq']==receipt['seq'] and receipt['request']['binding']==binding,'RECEIPT-BINDING')
 need(event['previous']==receipt['request']['expected'],'RECEIPT-PREDECESSOR')
class Ingress:
 def __init__(self,service,prerequisites,principals,response_key):
  self.service=service;self.config=parse(enc(service.config));self.pre=parse(enc(prerequisites));self.guard=Guard()
  need(self.config['implementation']==implementation(self.guard,self.pre),'INGRESS-IMPLEMENTATION')
  self.principals={n:(bytes(v[0]),frozenset(v[1])) for n,v in principals.items()};self.response_key=bytes(response_key)
  need(len(self.response_key)==32 and all(len(v[0])==32 for v in self.principals.values()),'LAB-KEY-LENGTH')
  need(len({v[0] for v in self.principals.values()})==len(self.principals),'DISTINCT-CALLER-CREDENTIALS')
  need(self.pre.get('ingress_policy')==policy_binding(self.principals,public(self.response_key)),'SESSION-INGRESS-POLICY')
  need(strict.same(service.provider_policy,self.pre.get('outcome_provider_policy')),'C4-PROVIDER-POLICY')
  need(service.evidence_public==(bytes.fromhex(self.pre['outcome_lab_public_key']) if 'outcome_lab_public_key' in self.pre else None),'C4-POLICY')
  self.policy=policy_record(self.config,self.principals,public(self.response_key))
 def proof(self,receipt):
  if receipt is None:return None
  b=self.service.backend.get('SEQ/'+str(receipt['seq']));need(b is not None,'MISSING-RECEIPT-EVENT')
  event=parse(b,MAX_EVENT);receipt_check(receipt,event,self.service.binding);return event
 def handle(self,packet):
  self.guard.check();need(self.service.config==self.config,'SERVICE-CONFIG-CHANGED')
  need(strict.same(self.service.carrier_policy,self.pre.get('ethereum_carrier')),'CARRIER-POLICY-CHANGED')
  need(strict.same(self.service.provider_policy,self.pre.get('outcome_provider_policy')),'C4-PROVIDER-POLICY-CHANGED')
  need(self.service.evidence_public==(bytes.fromhex(self.pre['outcome_lab_public_key']) if 'outcome_lab_public_key' in self.pre else None),'C4-POLICY-CHANGED')
  need(policy_record(self.config,self.principals,public(self.response_key))==self.policy,'POLICY-CHANGED')
  p=parse(packet,REQUEST_LIMIT);exact(p,['request','mac']);q=p['request']
  exact(q,['format','service','binding','pilot','session','principal','challenge','method','args','policy_sha256'])
  need(q['principal'] in self.principals,'UNAUTHENTICATED-CALLER');key,roles=self.principals[q['principal']]
  need(type(p['mac']) is str and hmac.compare_digest(p['mac'],tag(key,enc(q))),'REQUEST-AUTHENTICATION')
  need(q['policy_sha256']==sha(enc(self.policy)),'INGRESS-POLICY')
  need(q['format']==FORMAT and q['service']==self.config['backend']['service_identity'] and q['binding']==self.service.binding and q['pilot']==self.config['pilot'] and q['session']==self.config['session'],'REQUEST-CONTEXT')
  need(type(q['challenge']) is str and len(q['challenge'])==64 and digest(q['challenge']),'CHALLENGE')
  method=q['method'];a=q['args'];need(type(a) is dict,'ARGUMENTS');need('executor' in roles,'CALLER-OPERATION-DENIED')
  # Roles come ONLY from this service-owned credential map, never request assertions.
  if method=='commit':
   exact(a,['expected','op','kind','u','body'])
   need(a['kind'] in ['RETIRE','SEAL','ATTEMPT','OBSERVE','OBSERVE_EVIDENCE','BIND_NEAR','REPAIR','STAGE_OPEN','STAGE_PREPARE','STAGE_ATTEMPT','STAGE_RETRY','STAGE_QUERY','STAGE_RESULT','STAGE_BACKUP','STAGE_BACKUP_FINISH','STAGE_CLEANUP_READY'],'OPERATION-DENIED')
   if a['kind'] in ['OBSERVE','OBSERVE_EVIDENCE','STAGE_RESULT']:need('lab-result-provider' in roles,'RESULT-PROVIDER-DENIED')
  elif method=='head':exact(a,[])
  elif method=='event':exact(a,['seq']);need(type(a['seq']) is int and 1<=a['seq']<=12000,'EVENT-RANGE')
  elif method=='blob':exact(a,['ref','limit']);need(digest(a['ref']) and type(a['limit']) is int and 0<a['limit']<=max(MAX_INTENT,MAX_TRANSACTION),'BLOB-REQUEST')
  elif method=='resolve':exact(a,['op']);need(type(a['op']) is str and 0<len(a['op'])<=128,'OP')
  else:raise Blocked('OPERATION-DENIED: no genesis, restore, raw write, public status or backup')
  try:
   if method=='commit':
    if a['kind']=='RETIRE':
     exact(a['body'],['intent_hex']);raw=bytes.fromhex(a['body']['intent_hex']);i,_=e.validate_intent(a['u'],raw)
     need(i['chain']=='1313161555','INGRESS-CHAIN')
     for k in ['model','profile','config']:need(i[k]==self.pre[k],'INGRESS-PREREQUISITE')
    result=self.service.commit(a['expected'],a['op'],a['kind'],a['u'],a['body'])
    data={'result':result,'event':self.proof(result['receipt'])}
   elif method=='head':
    s=self.service.fresh();data={'state':s,'event':None if not s['seq'] else parse(self.service.backend.get('SEQ/'+str(s['seq'])),MAX_EVENT)}
   elif method=='event':
    s=self.service.fresh();need(a['seq']<=s['seq'],'UNAVAILABLE-EVENT');data={'event':parse(self.service.backend.get('SEQ/'+str(a['seq'])),MAX_EVENT)}
   elif method=='blob':self.service.fresh();data={'hex':self.service.blob(a['ref'],a['limit']).hex()}
   else:
    self.service.fresh();result=self.service.resolve(a['op']);data={'result':result,'event':self.proof(result['receipt'])}
   status='OK'
  except (OSError,TimeoutError,Uncertain):status='UNKNOWN';data={'reason':'UNCERTAIN-SERVICE-OUTCOME: resolve; no release'}
  except (ValueError,KeyError,TypeError):status='REJECTED';data={'reason':'SERVICE-VALIDATION-REJECTED'}
  response={'policy_sha256':q['policy_sha256'],'format':FORMAT,'service':q['service'],'binding':q['binding'],'pilot':q['pilot'],'session':q['session'],'request_sha256':sha(enc(q)),'challenge':q['challenge'],'status':status,'data':data}
  raw=enc({'response':response,'signature':signature(self.response_key,response)});need(len(raw)<=RESPONSE_LIMIT,'RESPONSE-SIZE');return raw
class OfflineChannel:
 def __init__(self,ingress):self.ingress=ingress;self.available=True;self.drop_after=False;self.filter=None
 def exchange(self,packet):
  if not self.available:raise OSError('OFFLINE-INGRESS-UNAVAILABLE')
  response=self.ingress.handle(packet)
  if self.drop_after:self.drop_after=False;raise OSError('OFFLINE-ACK-LOSS')
  return self.filter(packet,response) if self.filter else response
class Client:
 """Implements the reviewed service surface over canonical bytes, not raw Service.
 Replies are durably consumed before returning; no saved response grants release.
 """
 def __init__(self,channel,config,principal,caller_key,response_key,path,create=False,policy=None):
  self.channel=channel;self.config=parse(enc(config));self.binding=sha(enc(config));self.principal=principal;self.caller_key=bytes(caller_key);self.response_key=bytes(response_key);self.last=None
  need(type(policy) is dict and policy.get('service_binding')==self.binding and policy.get('response_public_key')==self.response_key.hex(),'PINNED-INGRESS-POLICY')
  self.policy=parse(enc(policy));need(self.policy['principals'].get(principal,{}).get('credential_sha256')==sha(self.caller_key),'CALLER-POLICY')
  path=Path(path);need(path.exists()!=create,'WIRE-JOURNAL-EXISTS-OR-MISSING')
  self.db=sqlite3.connect('file:'+str(path.resolve())+'?mode='+('rwc' if create else 'rw'),uri=True,isolation_level=None)
  self.db.execute('PRAGMA synchronous=FULL')
  binding=sha(enc({'journal_format':JOURNAL_FORMAT,'policy':sha(enc(self.policy)),'service':self.binding,'principal':principal,'caller_key':sha(self.caller_key),'response_key':sha(self.response_key)}))
  if create:
   self.db.executescript('CREATE TABLE meta(binding TEXT);CREATE TABLE calls(challenge TEXT PRIMARY KEY,request BLOB NOT NULL,state TEXT NOT NULL);');self.db.execute('INSERT INTO meta VALUES (?)',(binding,))
  need(self.db.execute('PRAGMA integrity_check').fetchone()==('ok',),'WIRE-CORRUPT')
  need(self.db.execute('SELECT binding FROM meta').fetchall()==[(binding,)],'WIRE-JOURNAL-BINDING')
  need(self.db.execute('SELECT count(*) FROM calls').fetchone()[0]<=MAX_CALLS,'WIRE-JOURNAL-OVER-CAPACITY')
 def close(self):self.db.close()
 def _call(self,method,args):
  q={'policy_sha256':sha(enc(self.policy)),'format':FORMAT,'service':self.config['backend']['service_identity'],'binding':self.binding,'pilot':self.config['pilot'],'session':self.config['session'],'principal':self.principal,'challenge':secrets.token_hex(32),'method':method,'args':args}
  request=enc(q);packet=enc({'request':q,'mac':tag(self.caller_key,request)});need(len(packet)<=REQUEST_LIMIT,'REQUEST-SIZE')
  # Capacity check and durable reservation share SQLite's writer transaction.
  # Commit MUST return successfully before any ingress exchange can occur.
  # A commit error is uncertain even if rollback finds no active transaction.
  try:
   self.db.execute('BEGIN IMMEDIATE')
   need(self.db.execute('SELECT count(*) FROM calls').fetchone()[0]<MAX_CALLS,'WIRE-JOURNAL-CAPACITY')
   self.db.execute('INSERT INTO calls VALUES (?,?,?)',(q['challenge'],request,'DISPATCHED'))
   self.db.execute('COMMIT')
  except Blocked:
   if self.db.in_transaction:self.db.execute('ROLLBACK')
   raise
  except sqlite3.Error as ex:
   if self.db.in_transaction:
    try:self.db.execute('ROLLBACK')
    except sqlite3.Error:pass
   raise Uncertain('WIRE-RESERVATION-UNKNOWN: no exchange; preserve journal') from ex
  try:raw=self.channel.exchange(packet)
  except (OSError,TimeoutError,Blocked):raise Uncertain('INGRESS-OUTCOME-UNKNOWN')
  p=parse(raw,RESPONSE_LIMIT);exact(p,['response','signature']);r=p['response']
  need(type(p['signature']) is str and len(p['signature'])==128 and all(c in '0123456789abcdef' for c in p['signature']),'SIGNATURE-ENCODING')
  try:Ed25519PublicKey.from_public_bytes(self.response_key).verify(bytes.fromhex(p['signature']),b'I164-LAB-SERVICE-RESPONSE-1\0'+enc(r))
  except (ValueError,TypeError,InvalidSignature) as ex:raise Blocked('RESPONSE-AUTHENTICATION') from ex
  exact(r,['format','service','binding','pilot','session','request_sha256','challenge','status','data','policy_sha256'])
  for k in ['format','service','binding','pilot','session','challenge','policy_sha256']:need(r[k]==q[k],'RESPONSE-CONTEXT')
  need(r['request_sha256']==sha(request),'RESPONSE-REQUEST')
  need(r['status'] in ['OK','REJECTED','UNKNOWN'],'RESPONSE-STATUS')
  n=self.db.execute("UPDATE calls SET state='CONSUMED' WHERE challenge=? AND request=? AND state='DISPATCHED'",(q['challenge'],request)).rowcount
  need(n==1,'RESPONSE-ALREADY-CONSUMED')
  if r['status']=='UNKNOWN':raise Uncertain('SERVICE-OUTCOME-UNKNOWN')
  if r['status']=='REJECTED':raise Blocked('SERVICE-REJECTED')
  return r['data']
 def fresh(self):
  d=self._call('head',{});exact(d,['state','event']);s=d['state'];exact(s,['binding','seq','head','counts','partitions','u','coordinates'])
  need(s['binding']==self.binding and type(s['seq']) is int and 0<=s['seq']<=12000 and digest(s['head']),'HEAD-BINDING')
  extra=['verifier'] if 'verifier' in s['counts'] else []
  exact(s['counts'],['attempt','query','snapshot']+extra);exact(s['partitions'],['query','snapshot']+extra)
  for k,v in s['counts'].items():need(type(v) is int and 0<=v<=(64 if k=='verifier' else self.config['limits'][k]),'COUNTS')
  for k,v in s['partitions'].items():need(type(v) is int and 0<=v<=min(s['counts'][k],(18 if k=='verifier' else self.config['limits']['staging_'+k])),'PARTITIONS')
  if s['seq']:
   need(sha(enc(d['event']))==s['head'] and enc(d['event']['after'])==enc({k:v for k,v in s.items() if k!='head'}),'HEAD-PROOF')
  else:need(d['event'] is None and s['head']==self.config['origin'] and not s['u'] and not any(s['counts'].values()),'GENESIS-PROOF')
  if self.last:need(s['seq']>=self.last[0] and (s['seq']!=self.last[0] or s['head']==self.last[1]),'STALE-RESPONSE')
  self.last=(s['seq'],s['head']);return s
 def history(self):
  s=self.fresh();events=[];prev=self.config['origin']
  for seq in range(1,s['seq']+1):
   d=self._call('event',{'seq':seq});exact(d,['event']);v=d['event']
   need(v['previous']==prev and v['after']['binding']==self.binding and v['after']['seq']==seq,'EVENT-CORRESPONDENCE');prev=sha(enc(v));events.append(v)
  need(prev==s['head'],'HISTORY-HEAD');return s,events
 def blob(self,ref,maximum):
  d=self._call('blob',{'ref':ref,'limit':maximum});exact(d,['hex']);raw=bytes.fromhex(d['hex']);need(len(raw)<=maximum and sha(raw)==ref,'BLOB-PROOF');return raw
 def commit(self,expected,op,kind,u=None,body=None,fault=None):
  need(fault is None,'NO-REMOTE-FAULT-CONTROL')
  d=self._call('commit',{'expected':expected,'op':op,'kind':kind,'u':u,'body':body or {}});exact(d,['result','event']);v=d['result'];exact(v,['receipt','release','duplicate'])
  receipt_check(v['receipt'],d['event'],self.binding)
  req={'binding':self.binding,'expected':expected,'op':op,'kind':kind,'u':u,'body_hash':sha(enc(body or {}))}
  need(v['receipt']['request']==req,'COMMIT-REQUEST-JOIN')
  need(type(v['duplicate']) is bool and type(v['release']) is bool and v['release']==(kind in ['ATTEMPT','STAGE_ATTEMPT','STAGE_RETRY'] and not v['duplicate']),'RELEASE-RULE')
  return v
 def resolve(self,op):
  d=self._call('resolve',{'op':op});exact(d,['result','event']);v=d['result'];exact(v,['result','receipt','release']);need(v['release'] is False,'RESOLUTION-CANNOT-RELEASE')
  if v['receipt'] is not None:
   receipt_check(v['receipt'],d['event'],self.binding);need(v['receipt']['request']['op']==op and v['result']=='SAVED-NO-RELEASE','RESOLVE-JOIN')
  else:need(d['event'] is None and v['result']=='NOT-FOUND-NO-RELEASE','MISSING-RECEIPT')
  return v
