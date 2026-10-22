"""I164 PROSPECTIVE LAB ONLY. Public key=1. NO NETWORK/PRODUCTION CUSTODY.
The exclusive signing boundary is this API under trusted-process assumptions.
It does not prevent someone possessing the public test secret signing elsewhere.
"""
import sys, sqlite3, json, hashlib, hmac, copy, base64
from pathlib import Path
from contextlib import contextmanager
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'retained-candidate/code'))
from anchor import enc,parse,sha,need,Blocked,MAX_STATE,MAX_EVENT,MAX_INTENT,MAX_TRANSACTION
import lab_evm as evm, signed_eth, stages, stage_carrier
from runtime import executor
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey,Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
import ownership, accounting
VERSION='I164-PROSPECTIVE-LAB-RETRY-3'
MAX_ROWS=384000; MAX_EVENTS=12000; REQUEST_LIMIT=3227648; RESPONSE_LIMIT=1048576
SEEDS={x:hashlib.sha256(('PUBLIC-LAB-ONLY-'+x).encode()).digest() for x in ['executor','observer','server']}
def public(seed):return Ed25519PrivateKey.from_private_bytes(seed).public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
PUB={k:public(v) for k,v in SEEDS.items()}
SIGNER='7e5f4552091a69125d5dfcb7b8c2659029395bdf'
def exact(x,keys):need(type(x) is dict and set(x)==set(keys),'FIELDS')
def integer(x,lo,hi):need(type(x) is int and lo<=x<=hi,'INTEGER');return x
def label(x):need(type(x) is str and 0<len(x)<=128,'LABEL');return x
def digest(x):need(type(x) is str and len(x)==64 and all(c in '0123456789abcdef' for c in x),'DIGEST');return x
def sig(who,x):return Ed25519PrivateKey.from_private_bytes(SEEDS[who]).sign(VERSION.encode()+b'\0'+enc(x)).hex()
def verify(who,x,s):Ed25519PublicKey.from_public_bytes(PUB[who]).verify(bytes.fromhex(s),VERSION.encode()+b'\0'+enc(x))
def fault(point,want):
 if point==want:raise OSError('INJECTED-'+point)
 if want=='exit:'+point:
  import os
  os._exit(77)

def unsigned_intent(raw,u):
 i=parse(raw,MAX_INTENT)
 if type(i) is dict and i.get('format')=='I164-UNSIGNED-COMPACT-LAB-1':
  exact(i,['format','identity','calldata_base64']);need(type(i['identity']) is dict and type(i['calldata_base64']) is str,'COMPACT-TYPES')
  data=base64.b64decode(i['calldata_base64'],validate=True);need(base64.b64encode(data).decode()==i['calldata_base64'] and len(data)<=70148,'COMPACT-BYTES')
  identity=i['identity'];need(not {'arguments','calldata_hex','signed_evm_hex','signed_evm_base64'}&set(identity),'COMPACT-FIELDS')
  i=dict(identity,calldata_hex=data.hex(),arguments=executor.abi_decode(identity.get('method'),data))
 need(type(i) is dict and i.get('carrier')=='I164-UNSIGNED-INTENT-LAB-1','UNSIGNED-VERSION')
 need(not {'signed_evm_hex','signed_evm_base64'}&set(i),'PREEXISTING-SIGNATURE')
 exact(i,{'chain','registry','executor','nonce','calldata_hex','value','gas_limit','config','decision','source','model','contract','profile','scope','key_epoch','method','arguments','carrier','gas_price','conditional_comparison_hex'})
 base={k:v for k,v in i.items() if k not in ['carrier','gas_price','conditional_comparison_hex']}
 executor.validate_intent(u,enc(base)) # ABI and exact decision/U bindings; synthetic envelope discarded.
 need(i['chain']=='1313161555' and i['executor']==SIGNER and i['gas_price']=='0' and i['gas_limit']=='100000000','LAB-CARRIER-POLICY')
 need(len(bytes.fromhex(i['calldata_hex']))<=70148,'INVOCATION-BOUND')
 if i['method']=='signPetition':need(len(bytes.fromhex(i['arguments']['authData']))<=4096,'AUTHDATA-BOUND')
 capsule=parse(bytes.fromhex(i['conditional_comparison_hex']),65536)
 need(capsule.get('format')=='I164-COMPUTED-COMPARISON-CAPSULE-1' and capsule.get('permit_for_conditional_test') is True,'CONDITIONAL-ONLY')
 return i

class Authority:
 def __init__(self,path,config,create=False,*,ownership_path):
  self.path=Path(path);self.config=parse(enc(config));exact(config,['version','pilot','session','start_nonce','manager','model','profile','config'])
  need(config['version']==VERSION,'NO-MIGRATION');label(config['pilot']);label(config['session']);integer(config['start_nonce'],0,2**64-1)
  need(type(config['manager']) is str and len(config['manager'])==40 and bytes.fromhex(config['manager']).hex()==config['manager'],'MANAGER')
  for k in ['model','profile','config']:digest(config[k])
  self.db=sqlite3.connect(self.path,timeout=15,isolation_level=None)
  need(self.db.execute('PRAGMA journal_mode').fetchone()[0]=='delete','NEW-DELETE-JOURNAL-REQUIRED')
  self.db.execute('PRAGMA synchronous=FULL')
  self.ownership_binding=ownership.attach(self.db,ownership_path)
  self.binding=sha(enc({'ownership':self.ownership_binding,'ownership_code':sha(Path(ownership.__file__).read_bytes()),'accounting_code':sha(Path(accounting.__file__).read_bytes()),'config':config,'code':sha(Path(__file__).read_bytes()),'principals':{k:v.hex() for k,v in PUB.items()},'retained':{n:sha((ROOT/'retained-candidate/code'/n).read_bytes()) for n in ['anchor.py','stages.py','signed_eth.py','lab_evm.py']}}))
  if create:
   need(not self.db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall(),'EXISTING-NAMESPACE')
   self.db.executescript('CREATE TABLE head (id INTEGER PRIMARY KEY CHECK(id=1),raw BLOB NOT NULL); CREATE TABLE events(seq INTEGER PRIMARY KEY,raw BLOB NOT NULL); CREATE TABLE blobs(ref TEXT PRIMARY KEY,raw BLOB NOT NULL); CREATE TABLE journal(challenge TEXT PRIMARY KEY,request BLOB NOT NULL,response BLOB);')
   s={'binding':self.binding,'seq':0,'head':'0'*64,'counts':{'attempt':0,'query':0,'snapshot':0,'verifier':0},'partitions':{'query':0,'snapshot':0,'verifier':0},'u':{},'active':None,'resources':{'slots':0,'holds':0,'query_holds':0,'extra_queries':0}}
   self.db.execute('INSERT INTO head VALUES(1,?)',(enc(s),))
  self.state()
 def close(self):self.db.close()
 @contextmanager
 def transaction(self):
  self.db.execute('BEGIN IMMEDIATE')
  try:yield;self.db.execute('COMMIT')
  except BaseException:self.db.execute('ROLLBACK');raise
 def blob(self,raw):
  need(type(raw) is bytes and 0<len(raw)<=MAX_INTENT,'BLOB-BOUND');ref=sha(raw)
  old=self.db.execute('SELECT raw FROM blobs WHERE ref=?',(ref,)).fetchone()
  if old:need(old[0]==raw,'BLOB-CONFLICT')
  else:self.db.execute('INSERT INTO blobs VALUES(?,?)',(ref,raw))
  return ref
 def get(self,ref):
  digest(ref);r=self.db.execute('SELECT raw FROM blobs WHERE ref=?',(ref,)).fetchone();need(r is not None and sha(r[0])==ref,'BLOB-INTEGRITY');return r[0]
 def state(self):
  s=parse(self.db.execute('SELECT raw FROM head WHERE id=1').fetchone()[0],MAX_STATE);need(s['binding']==self.binding,'VERSION-BINDING')
  if s['seq']:
   e=self.db.execute('SELECT raw FROM events WHERE seq=?',(s['seq'],)).fetchone();need(e is not None and sha(e[0])==s['head'],'HEAD-EVENT')
   x=parse(e[0],MAX_EVENT);need(enc(x['after'])==enc({k:v for k,v in s.items() if k!='head'}),'HEAD-EVENT-TYPED')
  accounting.validate(s)
  return s
 def save(self,s,request,kind,proof=None):
  accounting.validate(s)
  old=self.state();need(s['head']==old['head'] and s['seq']==old['seq'],'CAS');need(s['seq']<MAX_EVENTS,'EVENT-CAP')
  new=copy.deepcopy(s);previous=new.pop('head');new['seq']+=1
  event=enc({'previous':previous,'request':sha(enc(request)),'kind':kind,'proof':proof,'after':new});need(len(event)<=MAX_EVENT,'EVENT-BOUND')
  new['head']=sha(event);raw=enc(new);need(len(raw)<=MAX_STATE,'STATE-BOUND')
  self.db.execute('INSERT INTO events VALUES(?,?)',(new['seq'],event));self.db.execute('UPDATE head SET raw=? WHERE id=1',(raw,));return new
 def handle(self,packet,inject=None):
  q=parse(packet,REQUEST_LIMIT);exact(q,['request','signature']);r=q['request'];exact(r,['version','binding','pilot','session','principal','challenge','expected','method','u','body'])
  need(r['version']==VERSION and r['binding']==self.binding and r['pilot']==self.config['pilot'] and r['session']==self.config['session'],'REQUEST-CONTEXT')
  need(r['principal'] in ['executor','observer'],'PRINCIPAL');verify(r['principal'],r,q['signature']);digest(r['challenge']);digest(r['expected']);label(r['u']);need(type(r['body']) is dict,'BODY')
  need((r['method']=='observe' and r['principal']=='observer') or (r['method']!='observe' and r['principal']=='executor'),'ROLE')
  with self.transaction():
   need(not self.db.execute('SELECT 1 FROM journal WHERE challenge=?',(r['challenge'],)).fetchone(),'REPLAY')
   need(self.db.execute('SELECT count(*) FROM journal').fetchone()[0]<MAX_ROWS,'JOURNAL-CAP')
   self.db.execute('INSERT INTO journal VALUES(?,?,NULL)',(r['challenge'],packet))
  try:
   if r['method']=='sign':data=self.sign(r,inject)
   else:
    with self.transaction():
     s=self.state();need(r['expected']==s['head'],'STALE');data=self.apply(s,r,inject)
    if r['method'] in ['retire','open']:fault('after_ownership_commit',inject)
    if r['method']=='decide':fault('after_decision_commit',inject)
    if r['method']=='release':fault('after_release_commit',inject)
    if r['method']=='retry_release':fault('after_retry_commit',inject)
    if r['method']=='observe':fault('after_observe_commit',inject)
   response={'request':sha(packet),'challenge':r['challenge'],'ok':True,'data':data}
  except Exception as e:
   response={'request':sha(packet),'challenge':r['challenge'],'ok':False,'error':type(e).__name__+':'+str(e)}
  raw=enc({'response':response,'signature':sig('server',response)});need(len(raw)<=RESPONSE_LIMIT,'RESPONSE-BOUND')
  with self.transaction():self.db.execute('UPDATE journal SET response=? WHERE challenge=?',(raw,r['challenge']))
  return raw
 def stage(self,s,u):
  need(u in s['u'] and s['active']==u and s['u'][u].get('stage') is not None,'STAGE');return s['u'][u]['stage']
 def apply(self,s,r,inject):
  m,u,b=r['method'],r['u'],r['body']
  if m=='head':exact(b,[]);return s
  if m=='retire':
   exact(b,['intent_hex']);raw=bytes.fromhex(b['intent_hex']);need(raw.hex()==b['intent_hex'],'HEX');i=unsigned_intent(raw,u)
   need(u not in s['u'] and len(s['u'])<64,'U-LIMIT');need(all(i[k]==self.config[k] for k in ['model','profile','config']),'GOVERNING')
   reservation=sha(enc([i['chain'],i['executor'],i['nonce']]))
   need(all(x['reservation']!=reservation for x in s['u'].values()),'RESERVATION')
   ownership.claim(self.db,i['chain'],i['executor'],int(i['nonce']),int(i['nonce']),ownership.owner('prospective',self.binding,u,sha(raw)))
   s['u'][u]={'intent':self.blob(raw),'reservation':reservation,'retired':True,'petition':'NOT-ATTEMPTED'}
  elif m=='open':
   exact(b,['message_hex','key','signature']);need(u in s['u'] and s['active'] is None,'ONE-LIFETIME-STAGE');v=s['u'][u];i=unsigned_intent(self.get(v['intent']),u)
   msg=bytes.fromhex(b['message_hex']);need(msg.hex()==b['message_hex'] and msg.startswith(stage_carrier.DOMAIN),'MESSAGE');decoded=stage_carrier.decode(msg[len(stage_carrier.DOMAIN):]);c=decoded['bindings'];n=stages.capacity(len(msg),i['method'])['appends']
   need(int(i['nonce'])==self.config['start_nonce']+n+2,'NONCE-SCHEDULE')
   wanted={'pilot':self.config['pilot'],'method':i['method'],'registry':i['registry'],'executor':SIGNER,'configuration':i['config'],'model':i['model'],'profile':i['profile'],'contract':i['contract'],'network':i['chain'],'u':executor.u_wire(u),'inputs':sha(bytes.fromhex(i['calldata_hex'])),'history_prefix':s['head'],'phase':'PRE-COMMITMENT','auth_manager':self.config['manager']}
   need(all(c[k]==v for k,v in wanted.items()),'STAGE-BINDINGS');key=bytes.fromhex(b['key']);signature=bytes.fromhex(b['signature']);need(len(key)==32 and len(signature)==64 and sha(key)==c['public_key_hash'],'STAGE-KEY')
   Ed25519PublicKey.from_public_bytes(key).verify(signature,msg)
   caps=([107,62,31,31,50,414,318,4126,62,62,62,107,4126,575,8722] if i['method']=='signPetition' else [107,62,62,266,589,266,383,31,31,50,414,318,62,62,62,107,4126,575,978])
   need(len(decoded['authorized_values'])==len(caps) and all(len(bytes.fromhex(x))<=cap for x,cap in zip(decoded['authorized_values'],caps)),'VALUE-CAPS')
   meta={'bindings':c,'key':key.hex(),'signature':signature.hex(),'total':len(msg),'message_sha256':sha(msg),'invocation':i['calldata_hex']}
   sid=sha(b'I164-STAGING-SESSION-1\0'+enc(c)+bytes.fromhex(sha(msg))+key+signature+len(msg).to_bytes(8,'big'))
   ownership.claim(self.db,i['chain'],i['executor'],self.config['start_nonce'],int(i['nonce'])+2,ownership.owner('prospective',self.binding,u,v['intent']))
   v['stage']={'sid':sid,'message':self.blob(msg),'meta':self.blob(enc(meta)),'n':n,'index':0,'nonce':self.config['start_nonce'],'manager':'UNUSED','branch':'UNDECIDED','pending':None,'last':None,'attempts':0,'retries':0,'backups':{},'transport':{},'retry_ids':{}};s['active']=u
  elif m=='decide':
   exact(b,['kind']);st=self.stage(s,u);need(st['pending'] is None,'UNRESOLVED');kind=b['kind'];need(kind in ['begin','append','finalize','proceed','abandon','cleanup'],'ACTION')
   if kind=='abandon':need(st['manager'] in ['OPEN','AUTHENTICATED'] and st['branch'] in ['UNDECIDED','PROCEED'] and s['u'][u]['petition'] in ['NOT-ATTEMPTED','REVERTED'],'ABANDON-STATE')
   elif kind=='cleanup':need(st['manager'] in ['ABANDONED','FAILED','CONSUMED'],'CLEANUP-STATE')
   elif kind=='proceed':need(st['manager']=='AUTHENTICATED' and st['branch']=='UNDECIDED' and s['u'][u]['petition']=='NOT-ATTEMPTED','PROCEED-STATE')
   else:
    need(st['branch']=='UNDECIDED','BRANCH-CLOSED');want='begin' if st['index']==0 else 'append' if st['index']<=st['n'] else 'finalize'
    need(kind==want and ((kind=='begin' and st['manager']=='UNUSED') or (kind!='begin' and st['manager']=='OPEN')),'STAGE-ORDER')
   self.require_ownership(s,u,st['nonce'])
   self.charge(s,st,kind)
   if kind=='abandon':st['branch']='ABANDON'
   if kind=='proceed':st['branch']='PROCEED';s['u'][u]['petition']='UNCERTAIN'
   i=unsigned_intent(self.get(s['u'][u]['intent']),u);meta=parse(self.get(st['meta']),MAX_INTENT);msg=self.get(st['message'])
   if kind=='proceed':target=i['registry'];data=bytes.fromhex(i['calldata_hex']);need(st['nonce']==int(i['nonce']),'SIGNING-NONCE')
   elif kind=='abandon':target=self.config['manager'];data=evm.keccak(b'abandon()')[:4]
   elif kind=='cleanup':target=self.config['manager'];data=stages.calldata(meta,st['sid'],{'kind':'cleanup'})
   else:
    cmd=stages.command(meta,msg,st['index']);target=cmd['target'];data=stages.calldata(meta,st['sid'],cmd)
   template={'signer':SIGNER,'chain':'1313161555','nonce':str(st['nonce']),'target':target,'calldata':data.hex(),'value':'0','gas_limit':'100000000','gas_price':'0'}
   action={'version':VERSION,'binding':self.binding,'pilot':self.config['pilot'],'session':self.config['session'],'sid':st['sid'],'u':u,'intent':s['u'][u]['intent'],'reservation':s['u'][u]['reservation'],'branch':st['branch'],'kind':kind,'index':st['index'],'template':template,'decision_request':sha(enc(r)),'attempt_ordinal':s['counts']['attempt']}
   a=self.blob(enc(action));attempt=accounting.record(self,s,st,r,a);st['pending']={'action':a,'phase':'DECIDED','tx':None,'released':False,'query':None,'first':attempt,'latest':attempt,'reconciliation':None};fault('before_decision_commit',inject)
  elif m=='release':
   exact(b,['action','tx']);st=self.stage(s,u);p=st['pending'];need(p is not None and p['action']==b['action'] and p['phase']=='SIGNED' and p['tx']==b['tx'] and not p['released'],'RELEASE-BINDING')
   action=accounting.ready(self,s,u,first=True);signed_eth.validate(self.get(p['tx']),action['template'])
   p['released']=True;st['transport'][p['latest']]['released']=True;new=self.save(s,r,'release');fault('before_release_commit',inject)
   return {'head':new['head'],'action':p['action'],'tx':p['tx'],'bytes':self.get(p['tx']).hex(),'lab_only':True}
  elif m=='retry_release':
   exact(b,['action','tx','prior_attempt','retry_id']);st=self.stage(s,u);p=st['pending'];rid=digest(b['retry_id'])
   need(p is not None and p['phase']=='SIGNED' and p['released'] and p['query'] is None,'RETRY-STATE')
   need(p['action']==b['action'] and p['tx']==b['tx'] and p['latest']==b['prior_attempt'],'RETRY-BINDING');need(rid not in st['retry_ids'],'RETRY-ID-REPLAY')
   need(p['reconciliation'] is not None,'RECONCILIATION-REQUIRED');e=parse(self.get(p['reconciliation']),MAX_INTENT)
   need(e['outcome']=='UNAVAILABLE' and e['query']['attempt']==p['latest'] and e['action']==p['action'] and e['transaction']==p['tx'],'RETRY-EVIDENCE')
   act=accounting.ready(self,s,u);raw=self.get(p['tx']);signed_eth.validate(raw,act['template'])
   accounting.reserve(self,s,st,act['kind'],retry=True)
   attempt=accounting.record(self,s,st,r,p['action'],p['latest'],p['tx'],rid);st['retry_ids'][rid]=attempt;p['latest']=attempt;p['reconciliation']=None
   st['transport'][attempt]['released']=True
   new=self.save(s,r,'retry-release',attempt);fault('before_retry_commit',inject)
   return {'head':new['head'],'action':p['action'],'attempt':attempt,'tx':p['tx'],'bytes':raw.hex(),'lab_only':True}
  elif m=='query':
   exact(b,['action']);st=self.stage(s,u);p=st['pending'];need(p is not None and p['action']==b['action'],'QUERY-ACTION');accounting.query(s,st,r)
  elif m=='observe':
   exact(b,['action','transaction','query','outcome','manager','nonce_consumed','source','qualification']);st=self.stage(s,u);p=st['pending'];need(p is not None and p['query'] is not None and p['action']==b['action'] and p['tx'] is not None and p['tx']==b['transaction'] and enc(p['query'])==enc(b['query']),'OBSERVATION-BINDING')
   need(b['qualification']=='LAB-ASSUMED-QUALIFIED','UNQUALIFIED-OBSERVATION')
   need(b['source']=='LAB-SYNTHETIC-NOT-FINALITY' and b['outcome'] in ['SUCCESS','REVERTED','UNAVAILABLE'] and type(b['nonce_consumed']) is bool,'LAB-OUTCOME')
   need(p['phase']=='SIGNED' and p['released'],'OBSERVATION-STATE')
   a=parse(self.get(p['action']),MAX_INTENT);kind=a['kind'];proof=self.blob(enc(b));p['query']=None;p['reconciliation']=proof
   if b['outcome']=='UNAVAILABLE':need(b['manager']==st['manager'] and not b['nonce_consumed'],'UNAVAILABLE-STATE')
   else:
    need(b['nonce_consumed'],'NONCE-UNRESOLVED')
    want={'begin':'OPEN','append':'OPEN','finalize':'AUTHENTICATED','proceed':'CONSUMED','abandon':'ABANDONED','cleanup':'CLEANED'}[kind]
    allowed=([want,'FAILED'] if kind in ['append','finalize'] else [want]) if b['outcome']=='SUCCESS' else [st['manager']]
    need(b['manager'] in allowed,'MANAGER-RESULT')
    accounting.settle(s,st,b['outcome']=='REVERTED' or b['manager']=='FAILED')
    st['nonce']+=1
    if b['outcome']=='SUCCESS':
     st['manager']=b['manager']
     if kind in ['begin','append','finalize']:st['index']+=1
     if kind=='proceed':s['u'][u]['petition']='SUCCESS'
     st['last']={'action':p['action'],'tx':p['tx'],'result':proof};st['pending']=None
    elif kind=='proceed':
     s['u'][u]['petition']='REVERTED';st['last']={'action':p['action'],'tx':p['tx'],'result':proof};st['pending']=None
    else:
     # No invented continuation/replacement after failed manager action.
     p['phase']='FAILED-FROZEN';p['result']=proof
   result=self.save(s,r,'observe',proof);fault('before_observe_commit',inject);return result
  elif m=='backup':
   exact(b,['id']);st=self.stage(s,u);key=digest(b['id']);need(key not in st['backups'],'BACKUP-REPLAY');need(s['counts']['snapshot']<130 and s['partitions']['snapshot']<85,'BACKUP-CAP')
   s['counts']['snapshot']+=1;s['partitions']['snapshot']+=1;st['backups'][key]='RETAINED-UNCERTAIN'
   # No callback or external backup success is asserted by this interface.
  else:raise Blocked('METHOD')
  if m in ['retire','open']:fault('before_ownership_commit',inject)
  result=self.save(s,r,m)
  return result
 def require_ownership(self,s,u,nonce):
  v=s['u'][u];i=unsigned_intent(self.get(v['intent']),u)
  need(type(nonce) is int and self.config['start_nonce']<=nonce<=int(i['nonce'])+2,'OUTSIDE-AUTHORIZED-SCHEDULE')
  ownership.require(self.db,i['chain'],i['executor'],nonce,ownership.owner('prospective',self.binding,u,v['intent']))
 def intent(self,s,u):return unsigned_intent(self.get(s['u'][u]['intent']),u)
 def charge(self,s,st,kind):accounting.reserve(self,s,st,kind)
 def sign(self,r,inject):
  exact(r['body'],['action']);u=r['u'];a_id=digest(r['body']['action'])
  with self.transaction():
   s=self.state();need(s['head']==r['expected'],'STALE');st=self.stage(s,u);p=st['pending'];need(p is not None and p['action']==a_id,'ACTION-BINDING')
   bound=parse(self.get(a_id),MAX_INTENT);self.require_ownership(s,u,int(bound['template']['nonce']))
   if p['phase']=='SIGNED':return {'action':a_id,'tx':p['tx'],'recovered':True,'release':False}
   need(p['phase']=='DECIDED','SIGNING-AMBIGUOUS');accounting.ready(self,s,u,first=True);a=parse(self.get(a_id),MAX_INTENT)
   need(a['binding']==self.binding and a['sid']==st['sid'] and a['u']==u and a['intent']==s['u'][u]['intent'] and a['branch']==st['branch'],'SIGNER-AUTHORIZATION')
   need(not(a['kind']=='proceed' and st['branch']=='ABANDON'),'PERMANENT-WITHDRAWAL')
   p['phase']='SIGNING';self.save(s,r,'sign-claim')
  fault('after_sign_claim',inject)
  t=a['template'];raw=bytes.fromhex(evm.tx(int(t['nonce']),t['target'],bytes.fromhex(t['calldata']),gas=int(t['gas_limit']),key=1));signed_eth.validate(raw,t);need(len(raw)<=MAX_TRANSACTION,'TRANSACTION-BOUND')
  fault('after_signature_created',inject)
  with self.transaction():
   s=self.state();st=self.stage(s,u);p=st['pending'];need(p is not None and p['action']==a_id and p['phase']=='SIGNING','SIGNER-FENCE')
   accounting.ready(self,s,u,first=True)
   p['tx']=self.blob(raw);p['phase']='SIGNED';self.save(s,r,'sign-persist',p['tx']);fault('before_signature_commit',inject)
  fault('after_signature_commit',inject)
  return {'action':a_id,'tx':sha(raw),'recovered':False,'release':False}

class Scheduler:
 """Authenticated OFFLINE client. Signature requests have no raw-sign escape."""
 def __init__(self,authority,principal='executor'):self.a=authority;self.principal=principal;self.counter=0
 def packet(self,method,u,body=None,expected=None,challenge=None):
  import secrets
  q={'version':VERSION,'binding':self.a.binding,'pilot':self.a.config['pilot'],'session':self.a.config['session'],'principal':self.principal,'challenge':challenge or secrets.token_hex(32),'expected':expected or self.a.state()['head'],'method':method,'u':u,'body':body or {}}
  return enc({'request':q,'signature':sig(self.principal,q)})
 def call(self,method,u,body=None,inject=None):
  packet=self.packet(method,u,body);raw=self.a.handle(packet,inject);out=parse(raw,RESPONSE_LIMIT);verify('server',out['response'],out['signature']);need(out['response']['request']==sha(packet),'RESPONSE-BINDING')
  need(out['response']['ok'],out['response'].get('error','REJECTED'));return out['response']['data']
 def decide(self,u,kind):return self.call('decide',u,{'kind':kind})
 def sign(self,u):return self.call('sign',u,{'action':self.a.state()['u'][u]['stage']['pending']['action']})
 def release(self,u):
  p=self.a.state()['u'][u]['stage']['pending'];return self.call('release',u,{'action':p['action'],'tx':p['tx']})

 def retry(self,u,retry_id):
  p=self.a.state()['u'][u]['stage']['pending']
  return self.call('retry_release',u,{'action':p['action'],'tx':p['tx'],'prior_attempt':p['latest'],'retry_id':retry_id})
