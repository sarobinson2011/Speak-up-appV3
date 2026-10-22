"""Read-only semantic fold of saved RETRY-3 records. Never calls Authority or signer."""
import sys,copy,base64,json
from functools import lru_cache
from common import *
pinned_sources()
# Only retained deterministic decoders are called. No candidate lifecycle/signer runs.
sys.path.insert(0,str(ROOT/'reference/executor'));import abi
sys.path.insert(0,str(ROOT/'reference/retained'));import signed_eth,lab_evm
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
PUB=json.loads((ROOT/'reference/public-keys.json').read_text())
DOMAIN=b'I164-ARCHITECTURE-A-AUTHORIZED-INPUTS-V2\n'
SIGNER='7e5f4552091a69125d5dfcb7b8c2659029395bdf'
BODIES={'head':[],'retire':['intent_hex'],'open':['message_hex','key','signature'],'decide':['kind'],'sign':['action'],'release':['action','tx'],'retry_release':['action','tx','prior_attempt','retry_id'],'query':['action'],'observe':['action','transaction','query','outcome','manager','nonce_consumed','source','qualification'],'backup':['id']}
def verify_signature(role,value,sig):
 try:Ed25519PublicKey.from_public_bytes(bytes.fromhex(PUB[role])).verify(hexbytes(sig,64),VERSION.encode()+b'\0'+enc(value))
 except Exception as e:raise Invalid('AUTHENTICATION') from e

def config_binding(config,meta):
 keys(config,'version pilot session start_nonce manager model profile config');need(config['version']==VERSION,'VERSION');text(config['pilot']);text(config['session']);integer(config['start_nonce'],0,2**64-1);hexbytes(config['manager'],20)
 for k in ['model','profile','config']:digest(config[k])
 keys(meta,'format incarnation');need(meta['format']=='I164-NONCE-OWNERSHIP-1','LEDGER-FORMAT');digest(meta['incarnation'])
 return sha(enc({'ownership':sha(enc(meta)),'ownership_code':sha((ROOT/'reference/runtime/ownership.py').read_bytes()),'accounting_code':sha((ROOT/'reference/runtime/accounting.py').read_bytes()),'config':config,'code':sha((ROOT/'reference/runtime/authority.py').read_bytes()),'principals':PUB,'retained':{n:sha((ROOT/'reference/retained'/n).read_bytes()) for n in ['anchor.py','stages.py','signed_eth.py','lab_evm.py']}}))

def intent(raw,u,config):
 x=parse(raw,262144)
 if x.get('format')=='I164-UNSIGNED-COMPACT-LAB-1':
  keys(x,'format identity calldata_base64');need(type(x['identity']) is dict,'IDENTITY')
  try:b=base64.b64decode(x['calldata_base64'],validate=True)
  except Exception as e:raise Invalid('BASE64') from e
  need(base64.b64encode(b).decode()==x['calldata_base64'] and len(b)<=70148,'COMPACT')
  need(not {'arguments','calldata_hex','signed_evm_hex','signed_evm_base64'}&set(x['identity']),'COMPACT-FIELDS')
  x=dict(x['identity'],calldata_hex=b.hex(),arguments=abi.decode(x['identity']['method'],b))
 keys(x,'chain registry executor nonce calldata_hex value gas_limit config decision source model contract profile scope key_epoch method arguments carrier gas_price conditional_comparison_hex')
 need(x['carrier']=='I164-UNSIGNED-INTENT-LAB-1','INTENT-VERSION')
 for k in ['chain','nonce','value','gas_limit','gas_price','key_epoch']:decimal(x[k])
 for k in ['registry','executor']:hexbytes(x[k],20)
 for k in ['config','decision','source','model','contract','profile','scope']:digest(x[k])
 need(x['method'] in ['signPetition','signPetitionWithZKProof'],'METHOD');b=hexbytes(x['calldata_hex']);need(len(b)<=70148,'INVOCATION-SIZE')
 # ABI encode rejects bool/float integer substitutions; exact decode bytes and typed object match.
 same(abi.decode(x['method'],b),x['arguments'],'ABI-DECODE');need(abi.encode(x['method'],x['arguments'])==b,'ABI-ENCODE')
 ub=u.encode();need(x['arguments']['d']['u']==sha(b'I164-PILOT-U-V1\0'+len(ub).to_bytes(8,'big')+ub),'U-JOIN')
 need(x['decision']==sha(enc(x['arguments']['d'])),'DECISION-JOIN')
 need(all(x[k]==config[k] for k in ['config','model','profile']),'GOVERNING')
 need((x['chain'],x['executor'],x['value'],x['gas_limit'],x['gas_price'])==('1313161555',SIGNER,'0','100000000','0'),'LAB-POLICY')
 if x['method']=='signPetition':need(len(hexbytes(x['arguments']['authData']))<=4096,'AUTHDATA-BOUND')
 capsule=parse(hexbytes(x['conditional_comparison_hex']),65536);need(capsule.get('format')=='I164-COMPUTED-COMPARISON-CAPSULE-1' and capsule.get('permit_for_conditional_test') is True,'CAPSULE')
 return x

class Fold:
 def __init__(self,config,meta,blobs,owners):
  self.config=config;self.binding=config_binding(config,meta);self.blobs=blobs;self.used=set();self.owners=owners;self.actions=set();self.attempts=set();self.kinds=set();self.sign_claims={};self.occurrences=[]
  for ref,b in blobs.items():digest(ref);need(type(b) is bytes and 0<len(b)<=262144 and sha(b)==ref,'BLOB-HASH')
  self.s={'binding':self.binding,'seq':0,'head':ZERO,'counts':{'attempt':0,'query':0,'snapshot':0,'verifier':0},'partitions':{'query':0,'snapshot':0,'verifier':0},'u':{},'active':None,'resources':{'slots':0,'holds':0,'query_holds':0,'extra_queries':0}}
 def get(self,ref):digest(ref);need(ref in self.blobs,'MISSING-BLOB');self.used.add(ref);return self.blobs[ref]
 def obj(self,ref):return parse(self.get(ref),262144)
 def claim(self,u,i,lo,hi):
  need(0<=lo<=hi<2**256 and hi-lo<=86,'COORDINATE-RANGE');owner=sha(enc(['prospective',self.binding,u,self.s['u'][u]['intent']]))
  for n in range(lo,hi+1):
   coord=sha(enc([i['chain'],i['executor'],str(n)]));need(coord in self.owners,'MISSING-OWNER');row=self.owners[coord]
   same(row,{'coordinate':[i['chain'],i['executor'],str(n)],'owner':owner},'NONCE-OWNER')
 def own(self,s,u,nonce):
  i=intent(self.get(s['u'][u]['intent']),u,self.config);need(self.config['start_nonce']<=nonce<=int(i['nonce'])+2,'SCHEDULE');self.claim(u,i,nonce,nonce);return i
 def stage(self,s,u):need(s['active']==u and u in s['u'] and 'stage' in s['u'][u],'ACTIVE-STAGE');return s['u'][u]['stage']
 def reserve(self,s,st,i,kind,retry=False):
  r=s['resources'];need(s['counts']['attempt']<2070 and st['attempts']<102,'ATTEMPT-CAP');need(r['slots']+r['holds']<16,'SLOT-CAP')
  need(s['counts']['query']+r['query_holds']<3110 and s['partitions']['query']+r['query_holds']<2086,'QUERY-HEADROOM')
  if kind=='finalize' or (kind=='proceed' and i['method']=='signPetitionWithZKProof'):
   need(s['counts']['verifier']<64 and s['partitions']['verifier']<18,'VERIFIER-CAP');s['counts']['verifier']+=1;s['partitions']['verifier']+=1
  s['counts']['attempt']+=1;st['attempts']+=1;r['query_holds']+=1
  if retry:r['slots']+=1;st['retries']+=1
  else:r['holds']+=1
 def add_attempt(self,s,st,r,action,parent=None,tx=None,rid=None):
  rec={'binding':self.binding,'pilot':self.config['pilot'],'session':self.config['session'],'u':r['u'],'intent':s['u'][r['u']]['intent'],'sid':st['sid'],'action':action,'parent':parent,'transaction':tx,'ordinal':s['counts']['attempt'],'retry_id':rid,'request':sha(enc(r))};ref=sha(enc(rec));same(self.obj(ref),rec,'ATTEMPT-EXACT');need(ref not in self.attempts,'ATTEMPT-REUSE');self.attempts.add(ref)
  st['transport'][ref]={'slot':'CONSUMED' if parent else 'HELD','queried':False,'released':False};return ref
 def template(self,s,st,i,kind):
  meta=self.obj(st['meta']);msg=self.get(st['message']);w=lambda n:n.to_bytes(32,'big');dyn=lambda b:w(len(b))+b+b'\0'*((-len(b))%32)
  target=self.config['manager']
  if kind=='proceed':need(st['nonce']==int(i['nonce']),'PETITION-NONCE');target=i['registry'];data=hexbytes(i['calldata_hex'])
  elif kind=='abandon':data=lab_evm.keccak(b'abandon()')[:4]
  elif kind=='cleanup':data=bytes.fromhex('f474fb90')+bytes.fromhex(st['sid'])
  elif kind=='finalize':data=bytes.fromhex('4bb278f3')
  elif kind=='append':off=(st['index']-1)*512;data=bytes.fromhex('881a874d')+bytes.fromhex(st['sid'])+w(off)+w(96)+dyn(msg[off:off+512])
  else:
   c=enc(meta['bindings'])[:-1];t=hexbytes(meta['key'])+hexbytes(meta['signature'])+hexbytes(meta['message_sha256'])+w(meta['total'])+w(192)+dyn(c)
   data=bytes.fromhex('fbd68140')+w(64)+w(64+len(t))+t+dyn(hexbytes(meta['invocation']))
  return {'signer':SIGNER,'chain':'1313161555','nonce':str(st['nonce']),'target':target,'calldata':data.hex(),'value':'0','gas_limit':'100000000','gas_price':'0'}
 def advance(self,event,raw,request):
  keys(event,'previous request kind proof after');k=event['kind'];r=request;b=r['body'];u=r['u'];s=copy.deepcopy(self.s);oldhead=s['head'];need(event['previous']==oldhead and event['request']==sha(enc(r)),'EVENT-REQUEST')
  need(k in ['retire','open','decide','sign-claim','sign-persist','release','retry-release','query','observe','backup'],'EVENT-KIND')
  need(r['method']==({'sign-claim':'sign','sign-persist':'sign','retry-release':'retry_release'}.get(k,k)),'METHOD-EVENT');keys(b,BODIES[r['method']])
  if k!='sign-persist':need(r['expected']==oldhead,'STALE-AUTHORIZATION')
  else:need(self.sign_claims.get(sha(enc(r)))==b['action'],'SIGN-PERSIST-ANCESTRY')
  proof=None
  if k=='retire':
   need(u not in s['u'] and len(s['u'])<64,'U-RETIRED');rawi=hexbytes(b['intent_hex']);i=intent(rawi,u,self.config);ref=sha(rawi);need(self.get(ref)==rawi,'INTENT-BYTES');res=sha(enc([i['chain'],i['executor'],i['nonce']]))
   need(all(v['reservation']!=res for v in s['u'].values()),'RESERVATION');s['u'][u]={'intent':ref,'reservation':res,'retired':True,'petition':'NOT-ATTEMPTED'}
   self.s=s;self.claim(u,i,int(i['nonce']),int(i['nonce']))
  elif k=='open':
   need(u in s['u'] and s['active'] is None,'ONE-LIFETIME-STAGE');i=intent(self.get(s['u'][u]['intent']),u,self.config);msg=hexbytes(b['message_hex']);need(msg.startswith(DOMAIN),'DOMAIN');x=parse(msg[len(DOMAIN):],1048576);keys(x,'format bindings authorized_values');need(x['format']=='I164-A-STAGED-AUTHORIZED-INPUTS-2','MESSAGE-FORMAT');c=x['bindings']
   import stage_carrier
   stage_carrier.decode(msg[len(DOMAIN):]);n=(len(msg)+511)//512;need(41<=len(msg)<=({'signPetition':41972,'signPetitionWithZKProof':21376}[i['method']]),'MESSAGE-CAP');need(int(i['nonce'])==self.config['start_nonce']+n+2,'NONCE-SCHEDULE')
   wanted={'pilot':self.config['pilot'],'method':i['method'],'registry':i['registry'],'executor':SIGNER,'configuration':i['config'],'model':i['model'],'profile':i['profile'],'contract':i['contract'],'network':i['chain'],'u':i['arguments']['d']['u'],'inputs':sha(hexbytes(i['calldata_hex'])),'history_prefix':oldhead,'phase':'PRE-COMMITMENT','auth_manager':self.config['manager']};need(all(c[v]==z for v,z in wanted.items()),'STAGE-JOINS')
   key=hexbytes(b['key'],32);sig=hexbytes(b['signature'],64);need(sha(key)==c['public_key_hash'],'STAGE-KEY');Ed25519PublicKey.from_public_bytes(key).verify(sig,msg)
   caps=([107,62,31,31,50,414,318,4126,62,62,62,107,4126,575,8722] if i['method']=='signPetition' else [107,62,62,266,589,266,383,31,31,50,414,318,62,62,62,107,4126,575,978]);need(len(x['authorized_values'])==len(caps) and all(len(hexbytes(v))<=cap for v,cap in zip(x['authorized_values'],caps)),'AUTHORIZED-VALUES')
   meta={'bindings':c,'key':key.hex(),'signature':sig.hex(),'total':len(msg),'message_sha256':sha(msg),'invocation':i['calldata_hex']};mr=sha(enc(meta));need(self.get(mr)==enc(meta) and self.get(sha(msg))==msg,'STAGE-BLOBS');sid=sha(b'I164-STAGING-SESSION-1\0'+enc(c)+bytes.fromhex(sha(msg))+key+sig+len(msg).to_bytes(8,'big'))
   self.claim(u,i,self.config['start_nonce'],int(i['nonce'])+2)
   s['u'][u]['stage']={'sid':sid,'message':sha(msg),'meta':mr,'n':n,'index':0,'nonce':self.config['start_nonce'],'manager':'UNUSED','branch':'UNDECIDED','pending':None,'last':None,'attempts':0,'retries':0,'backups':{},'transport':{},'retry_ids':{}};s['active']=u
  else:
   st=self.stage(s,u);p=st['pending']
   if k=='decide':
    need(p is None,'PENDING-ACTION');kind=b['kind'];need(kind in ['begin','append','finalize','proceed','abandon','cleanup'],'ACTION-KIND')
    if kind=='abandon':need(st['manager'] in ['OPEN','AUTHENTICATED'] and st['branch'] in ['UNDECIDED','PROCEED'] and s['u'][u]['petition'] in ['NOT-ATTEMPTED','REVERTED'],'ABANDON-GUARD')
    elif kind=='cleanup':need(st['manager'] in ['ABANDONED','FAILED','CONSUMED'],'CLEANUP-GUARD')
    elif kind=='proceed':need(st['manager']=='AUTHENTICATED' and st['branch']=='UNDECIDED' and s['u'][u]['petition']=='NOT-ATTEMPTED','PROCEED-GUARD')
    else:need(st['branch']=='UNDECIDED' and kind==('begin' if st['index']==0 else 'append' if st['index']<=st['n'] else 'finalize') and st['manager']==('UNUSED' if kind=='begin' else 'OPEN'),'STAGE-ORDER')
    i=self.own(s,u,st['nonce']);self.reserve(s,st,i,kind)
    if kind=='abandon':st['branch']='ABANDON'
    if kind=='proceed':st['branch']='PROCEED';s['u'][u]['petition']='UNCERTAIN'
    a={'version':VERSION,'binding':self.binding,'pilot':self.config['pilot'],'session':self.config['session'],'sid':st['sid'],'u':u,'intent':s['u'][u]['intent'],'reservation':s['u'][u]['reservation'],'branch':st['branch'],'kind':kind,'index':st['index'],'template':self.template(s,st,i,kind),'decision_request':sha(enc(r)),'attempt_ordinal':s['counts']['attempt']};ar=sha(enc(a));same(self.obj(ar),a,'ACTION-EXACT');need(ar not in self.actions,'ACTION-REUSED');self.actions.add(ar);self.kinds.add(kind);at=self.add_attempt(s,st,r,ar)
    st['pending']={'action':ar,'phase':'DECIDED','tx':None,'released':False,'query':None,'first':at,'latest':at,'reconciliation':None}
   elif k in ['sign-claim','sign-persist','release','retry-release']:
    need(p is not None and b['action']==p['action'],'ACTION-BINDING');a=self.obj(p['action']);self.own(s,u,decimal(a['template']['nonce']));e=st['transport'][p['latest']]
    if k in ['sign-claim','sign-persist','release']:
     need(p['latest']==p['first'] and e['slot']=='HELD' and not e['queried'] and not e['released'],'FIRST-RESERVATION')
    if k=='sign-claim':need(p['phase']=='DECIDED' and a['branch']==st['branch'],'SIGN-CLAIM');p['phase']='SIGNING';self.sign_claims[sha(enc(r))]=p['action']
    elif k=='sign-persist':
     need(p['phase']=='SIGNING','SIGN-FENCE');proof=digest(event['proof']);rawtx=self.get(proof);need(len(rawtx)<=75088,'TX-BOUND');signed_eth.validate(rawtx,a['template']);p['tx']=proof;p['phase']='SIGNED'
    elif k=='release':
     need(p['phase']=='SIGNED' and b['tx']==p['tx'] and not p['released'],'RELEASE-GUARD');signed_eth.validate(self.get(p['tx']),a['template']);p['released']=True;e['released']=True
    else:
     rid=digest(b['retry_id']);need(p['phase']=='SIGNED' and p['released'] and p['query'] is None and b['tx']==p['tx'] and b['prior_attempt']==p['latest'] and rid not in st['retry_ids'] and p['reconciliation'] is not None,'RETRY-GUARD');obs=self.obj(p['reconciliation']);need(obs['outcome']=='UNAVAILABLE' and obs['query']['attempt']==p['latest'] and obs['action']==p['action'] and obs['transaction']==p['tx'],'RETRY-EVIDENCE');signed_eth.validate(self.get(p['tx']),a['template']);i=intent(self.get(s['u'][u]['intent']),u,self.config);self.reserve(s,st,i,a['kind'],True);at=self.add_attempt(s,st,r,p['action'],p['latest'],p['tx'],rid);st['retry_ids'][rid]=at;p['latest']=at;p['reconciliation']=None;st['transport'][at]['released']=True;proof=at
   elif k=='query':
    need(p is not None and p['phase']=='SIGNED' and p['released'] and p['query'] is None and b['action']==p['action'],'QUERY-GUARD');res=s['resources'];e=st['transport'][p['latest']]
    if not e['queried']:need(res['query_holds']>0,'QUERY-HOLD');res['query_holds']-=1;e['queried']=True;cl='ATTEMPT'
    else:need(res['extra_queries']<16 and s['counts']['query']+res['query_holds']<3110 and s['partitions']['query']+res['query_holds']<2086,'EXTRA-QUERY');res['extra_queries']+=1;cl='EXTRA'
    s['counts']['query']+=1;s['partitions']['query']+=1;p['query']={'request':sha(enc(r)),'ordinal':s['counts']['query'],'attempt':p['latest'],'classification':cl};p['reconciliation']=None
   elif k=='observe':
    need(p is not None and p['query'] is not None and p['phase']=='SIGNED' and p['released'],'OBSERVATION-STATE');need(b['action']==p['action'] and b['transaction']==p['tx'],'OBSERVATION-BINDING');same(b['query'],p['query'],'QUERY-EXACT');boolean(b['nonce_consumed']);need(b['qualification']=='LAB-ASSUMED-QUALIFIED' and b['source']=='LAB-SYNTHETIC-NOT-FINALITY' and b['outcome'] in ['SUCCESS','REVERTED','UNAVAILABLE'],'OBSERVATION-QUALIFICATION');a=self.obj(p['action']);kind=a['kind'];proof=sha(enc(b));same(self.obj(proof),b,'OBSERVATION-BLOB');p['query']=None;p['reconciliation']=proof
    if b['outcome']=='UNAVAILABLE':need(b['manager']==st['manager'] and not b['nonce_consumed'],'UNKNOWN-NONEXECUTION')
    else:
     need(b['nonce_consumed'],'NONCE-CONSUMED');want={'begin':'OPEN','append':'OPEN','finalize':'AUTHENTICATED','proceed':'CONSUMED','abandon':'ABANDONED','cleanup':'CLEANED'}[kind];allowed=([want,'FAILED'] if kind in ['append','finalize'] else [want]) if b['outcome']=='SUCCESS' else [st['manager']];need(b['manager'] in allowed,'MANAGER-OUTCOME')
     e=st['transport'][p['first']];need(e['slot']=='HELD','DOUBLE-SETTLE');s['resources']['holds']-=1;failed=b['outcome']=='REVERTED' or b['manager']=='FAILED';e['slot']='CONSUMED' if failed else 'RELEASED';s['resources']['slots']+=int(failed);st['nonce']+=1
     if b['outcome']=='SUCCESS':
      st['manager']=b['manager']
      if kind in ['begin','append','finalize']:st['index']+=1
      if kind=='proceed':s['u'][u]['petition']='SUCCESS'
      st['last']={'action':p['action'],'tx':p['tx'],'result':proof};st['pending']=None
     elif kind=='proceed':s['u'][u]['petition']='REVERTED';st['last']={'action':p['action'],'tx':p['tx'],'result':proof};st['pending']=None
     else:p['phase']='FAILED-FROZEN';p['result']=proof
   elif k=='backup':
    key=digest(b['id']);need(key not in st['backups'] and s['counts']['snapshot']<130 and s['partitions']['snapshot']<85,'BACKUP');s['counts']['snapshot']+=1;s['partitions']['snapshot']+=1;st['backups'][key]='RETAINED-UNCERTAIN'
  need(event['proof']==proof,'EVENT-PROOF');s.pop('head');s['seq']+=1;need(s['seq']<=12000,'EVENT-CAP');same(event['after'],s,'TRANSITION-AFTER-EXACT');need(len(raw)<=212992,'EVENT-BOUND');s['head']=sha(raw);need(len(enc(s))<=196608,'HEAD-BOUND');self.s=s;self.occurrences.append({'seq':s['seq'],'kind':k,'request':event['request'],'head':s['head']});return s
