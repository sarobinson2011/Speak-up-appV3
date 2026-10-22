"""C5 offline staged scheduling. Service-owned state; never an operational permit.
The stage envelope is explicitly a LAB transport envelope, not an EVM signature.
"""
import copy, math
from anchor import *
import strict_types as strict
import stage_carrier
from outcome import engine_result
from runtime import retained,executor as e
CHUNK=512
CEILINGS={'signPetition':41972,'signPetitionWithZKProof':21376}
RETRIES=16
# At most 82 appends + begin/finalize + signing + cleanup + 16 retries.
MAX_STAGE_TRANSACTIONS=86+RETRIES
# 4 stage commits/attempt + 16 extra observations*2 + 85 backup charges
# and at most one callback-return bookkeeping event per backup,
# plus retained executor transitions. Fits the existing 12000 service events.
EVENT_RESERVATION=4*MAX_STAGE_TRANSACTIONS+32+2*85+8
RELEASE_FORMAT='I164-EXACT-STAGE-RELEASE-2'
BACKUP_FORMAT='I164-EXCLUSIVE-BACKUP-CALLBACK-1'
PREPARE_FORMAT='I164-EXACT-NEAR-PREPARE-2'

def backup_operation(binding,u,request_id):
 need(label(request_id) and label(u) and digest(binding),'BACKUP-REQUEST-ID')
 return 'backup-'+sha(enc([BACKUP_FORMAT,binding,u,request_id]))

def backup_body(s,st,request_id):
 need(st is not None,'NO-STAGED-SESSION')
 return {'format':BACKUP_FORMAT,'request_id':request_id,'intent':st['intent'],'sid':st['sid']}

def release_binding(s,st,kind):
 need(type(st) is dict and st.get('pending') is not None,'NO-STAGE')
 need(kind in ['STAGE_ATTEMPT','STAGE_RETRY'],'RELEASE-KIND')
 # A canonical immutable snapshot, bound to the captured authoritative head.
 # It includes prior attempt/result coordinates so retries cannot silently
 # select another stage or discard an intervening outcome.
 return {'format':RELEASE_FORMAT,'binding':s['binding'],'expected_head':s['head'],
         'kind':kind,'pilot':st['pilot'],'session':st['session'],'u':st['u'],
         'sid':st['sid'],'intent':st['intent'],'operation':st['operation'],
         'message':st['message'],'meta':st['meta'],'index':st['index'],
         'stage_sha256':sha(enc(st)),'pending':copy.deepcopy(st['pending'])}

def capacity(length,method):
 need(type(length) is int and method in CEILINGS and 41<=length<=CEILINGS[method],'PROFILE-MESSAGE-BOUND')
 n=(length+511)//512
 return {'appends':n,'nominal_transactions':n+4,'attempts_with_shared_retries':n+20,'staging_queries':n+36,'staging_backups':1+(n+31)//32+3+16,'verifier_reservation':18,'events_reserved':EVENT_RESERVATION}

def command(meta,message,index):
 n=(len(message)+511)//512
 need(type(index) is int and 0<=index<=n+2,'STAGE-RANGE')
 if index==0:return {'kind':'begin','ordinal':0,'offset':0,'bytes':enc({k:v for k,v in meta.items() if k!='invocation'}).hex(),'target':meta['bindings']['auth_manager']}
 if index<=n:
  off=(index-1)*512
  return {'kind':'append','ordinal':index,'offset':off,'bytes':message[off:off+512].hex(),'target':meta['bindings']['auth_manager']}
 return {'kind':'finalize' if index==n+1 else 'cleanup','ordinal':index,'offset':len(message),'bytes':'','target':meta['bindings']['auth_manager']}

def word(n):
 need(type(n) is int and 0<=n<2**256,'ABI-UINT');return n.to_bytes(32,'big')
def dynamic(b):return word(len(b))+b+b'\0'*((-len(b))%32)
def calldata(meta,sid,cmd):
 # Selectors copied from pinned successful prepared transaction bytes.
 if cmd['kind']=='begin':
  c=enc(meta['bindings'])[:-1];sig=bytes.fromhex(meta['signature'])
  tup=bytes.fromhex(meta['key'])+sig+bytes.fromhex(meta['message_sha256'])+word(meta['total'])+word(192)+dynamic(c)
  invocation=bytes.fromhex(meta['invocation'])
  return bytes.fromhex('fbd68140')+word(64)+word(64+len(tup))+tup+dynamic(invocation)
 if cmd['kind']=='append':return bytes.fromhex('881a874d')+bytes.fromhex(sid)+word(cmd['offset'])+word(96)+dynamic(bytes.fromhex(cmd['bytes']))
 if cmd['kind']=='finalize':return bytes.fromhex('4bb278f3')
 if cmd['kind']=='cleanup':return bytes.fromhex('f474fb90')+bytes.fromhex(sid)
 raise Blocked('UNSUPPORTED-STAGE')
def exact_evm_from_near(spec,near):
 """Slice ORIGINAL argument bytes; pinned NEAR canonical framing/signature verifies them."""
 near=bytes(near)
 need(len(near)<=retained.t.MAX_NEAR,'NEAR-SIZE')
 # Pinned unsigned() ends in argument bytes then uint64 gas + uint128 deposit.
 # A one-byte dummy determines only framing position, never submitted bytes.
 start=len(retained.t.unsigned(spec,b'\0'))-25
 need(start>=4 and len(near)>=start+89,'NEAR-TRUNCATED')
 n=int.from_bytes(near[start-4:start],'little')
 need(0<n<=retained.t.MAX_RAW and len(near)==start+n+24+65,'NEAR-ARGUMENT-LENGTH')
 raw=near[start:start+n]
 retained.t.exact_near(spec,raw,near)
 return raw

def envelope(st,cmd):
 # Explicit binary LAB transaction carrier, not an Ethereum signed transaction.
 # Keeps actual calldata bytes exact; immutable service metadata owns the joins.
 need(type(cmd['calldata_hex']) is str,'ACTUAL-CALLDATA-REQUIRED')
 raw=bytes.fromhex(cmd['calldata_hex'])
 return b'I164-LAB-STAGE-1\0'+bytes.fromhex(cmd['target'])+raw

def cleanup_execution(raw,meta,st):
 # Exact Engine result decoding is reused; this is correspondence, NOT finality/authentication.
 need(type(raw) is str and len(raw)<=32768 and len(raw)%2==0,'CLEANUP-RESULT-BOUND')
 b=bytes.fromhex(raw);need(b.hex()==raw,'CLEANUP-RESULT-ENCODING');z=engine_result(b)
 need(z['status']=='SUCCESS' and z['output_hex']==('0'*63+'1'),'CLEANUP-NOT-EXECUTED')
 expected={'address':meta['bindings']['auth_manager'],'topics':['50ba677aa32abfdd1bda06755bbc91c219971b292427a062b5dc8c6f185afd98',st['sid'],meta['bindings']['u']],
 'data':None}
 need(len(z['logs'])==1,'CLEANUP-EVENT-COUNT');event=z['logs'][0];d=bytes.fromhex(event['data'])
 need(len(d)==96 and int.from_bytes(d[:32],'big') in [2,3,4],'CLEANUP-TERMINAL')
 expected['data']=d[:32].hex()+meta['bindings']['inputs']+meta['message_sha256']
 need(strict.same(event,expected),'CLEANUP-EVENT-BINDING')
 return z

def transition(service,s,new,kind,u,body,op,blob):
 need(u in s['u'],'STAGE-U-NOT-RETIRED');v=s['u'][u]
 st=copy.deepcopy(v.get('stage'))
 def obj(ref):return parse(service.blob(ref,MAX_INTENT),MAX_INTENT)
 if kind=='STAGE_OPEN':
  need(st is None and v['record']['status']=='RETIRED' and not any('stage' in x for x in s['u'].values()),'ONE-LIFETIME-STAGED-SESSION')
  need(set(body)=={'message_hex','key','signature'},'STAGE-OPEN-FIELDS')
  msg=bytes.fromhex(body['message_hex']);need(msg.hex()==body['message_hex'] and msg.startswith(stage_carrier.DOMAIN),'MESSAGE-ENCODING')
  decoded=stage_carrier.decode(msg[len(stage_carrier.DOMAIN):]);c=decoded['bindings']
  caps=([107,62,31,31,50,414,318,4126,62,62,62,107,4126,575,8722] if c['method']=='signPetition' else [107,62,62,266,589,266,383,31,31,50,414,318,62,62,62,107,4126,575,978])
  need(len(decoded['authorized_values'])==len(caps) and all(len(bytes.fromhex(v))<=n for v,n in zip(decoded['authorized_values'],caps)),'PROFILE-VALUE-COVERAGE-OR-BOUND')
  i,_=e.validate_intent(u,service.blob(v['intent'],MAX_INTENT))
  need(i['method']!='signPetition' or len(bytes.fromhex(i['arguments']['authData']))<=4096,'ORDINARY-AUTHDATA-OUTSIDE-PILOT')
  need(len(bytes.fromhex(i['calldata_hex']))<=70148,'INVOCATION-REPRESENTATION')
  cap=capacity(len(msg),c['method'])
  if service.carrier_policy:
   policy=service.carrier_policy
   need(i.get('carrier')==policy['version'] and i['executor']==policy['signer'] and i['chain']==policy['chain'],'CARRIER-INTENT')
   need(i['nonce']==str(int(policy['stage_start_nonce'])+cap['appends']+2),'SIGNING-NONCE-SCHEDULE')
   for k in ['gas_limit','gas_price','value']:need(i[k]==policy[k],'CARRIER-FEES')
  want={'pilot':service.config['pilot'],'method':i['method'],'registry':i['registry'],'executor':i['executor'],'configuration':i['config'],'model':i['model'],'profile':i['profile'],'contract':i['contract'],'network':i['chain'],'u':e.u_wire(u),'inputs':sha(bytes.fromhex(i['calldata_hex'])),'history_prefix':s['head'],'phase':'PRE-COMMITMENT'}
  for k,value in want.items():need(strict.same(c[k],value),'STAGE-BINDING:'+k)
  key=bytes.fromhex(body['key']);sig=bytes.fromhex(body['signature']);need(len(key)==32 and len(sig)==64 and key.hex()==body['key'] and sig.hex()==body['signature'] and sha(key)==c['public_key_hash'],'STAGE-KEY')
  need(s['seq']+EVENT_RESERVATION<=MAX_EVENTS,'HISTORY-CAPACITY-BEFORE-OPEN')
  need(s['counts']['attempt']+cap['nominal_transactions']<=service.config['limits']['attempt'],'ATTEMPT-CAPACITY')
  need(s['partitions']['query']+cap['nominal_transactions']<=service.config['limits']['staging_query'] and s['counts']['query']+cap['nominal_transactions']<=service.config['limits']['query'],'QUERY-CAPACITY')
  sid=sha(b'I164-STAGING-SESSION-1\0'+enc(c)+bytes.fromhex(sha(msg))+key+sig+len(msg).to_bytes(8,'big'))
  meta={'bindings':c,'key':key.hex(),'signature':sig.hex(),'total':len(msg),'message_sha256':sha(msg),'invocation':i['calldata_hex']}
  st={'pilot':service.config['pilot'],'session':service.config['session'],'u':u,'intent':v['intent'],'operation':c['operation'],'message':blob(msg,MAX_INTENT),'meta':blob(enc(meta),MAX_INTENT),'sid':sid,'index':0,'status':'READY','pending':None,'retries':0,'attempts':0,'verifiers':0,'history_prefix':s['head']}
 else:
  need(st is not None,'NO-STAGED-SESSION');msg=service.blob(st['message'],MAX_INTENT);meta=obj(st['meta']);cmd=None if kind in ['STAGE_BACKUP','STAGE_BACKUP_FINISH'] else command(meta,msg,st['index'])
  if kind=='STAGE_PREPARE':
   need(st['status']=='READY' and st['pending'] is None,'STAGE-NOT-READY')
   if cmd['kind']=='cleanup':need(v['record']['status'] in ['SUCCESS','FAILED'],'SIGNING-NOT-TERMINAL')
   need(set(body)==({'format','command','near_spec','near_hex','previous'} if service.carrier_policy else {'command','near_spec','near_hex','previous'}),'PREPARE-FIELDS')
   need(strict.same(body['command'],cmd) and strict.same(body['previous'],s['head']),'STAGE-COMMAND-OR-PREDECESSOR')
   expected_calldata=calldata(meta,st['sid'],cmd).hex()
   raw=envelope(st,dict(cmd,calldata_hex=expected_calldata))
   if service.carrier_policy:
    import signed_eth
    policy=service.carrier_policy
    need(set(policy)=={'version','signer','chain','gas_limit','gas_price','value','stage_start_nonce'} and policy['version']==signed_eth.VERSION,'CARRIER-POLICY')
    need(body['format']==PREPARE_FORMAT,'PREPARE-VERSION')
    raw=exact_evm_from_near(body['near_spec'],bytes.fromhex(body['near_hex']))
    nonce=int(policy['stage_start_nonce'])+st['index']+(1 if cmd['kind']=='cleanup' else 0)
    signed_eth.validate(raw,{k:policy[k] for k in ['signer','chain','gas_limit','gas_price','value']}|dict(nonce=str(nonce),target=cmd['target'],calldata=expected_calldata))
   near=bytes.fromhex(body['near_hex']);need(near.hex()==body['near_hex'],'NEAR-HEX')
   tid=retained.t.exact_near(body['near_spec'],raw,near)
   coord=sha(enc([body['near_spec'][k] for k in ['network','signer','public_key','nonce']]))
   # Permanent service nonce entries survive all executor-only restores.
   need(service.backend.get('STAGE-NONCE/'+coord) is None,'STAGE-NONCE-REUSE')
   for x in s['u'].values():need(x.get('near',{}).get('nonce_coordinate')!=coord,'SIGNING-NONCE-REUSE')
   st['pending']={'ref':blob(enc(body),MAX_INTENT),'evm':blob(raw,MAX_TRANSACTION),'near':blob(near,MAX_TRANSACTION),'txid':tid,'nonce':coord,'attempt':None,'query':None,'result':None,'prepared_head':s['head']};st['status']='PREPARED'
  elif kind in ['STAGE_ATTEMPT','STAGE_RETRY']:
   need(type(body) is dict and set(body)=={'release'} and strict.same(body['release'],release_binding(s,st,kind)),'EXACT-STAGE-RELEASE-BINDING')
   p=st['pending'];need(p is not None,'NO-PREPARED-STAGE')
   if kind=='STAGE_ATTEMPT':need(st['status']=='PREPARED','NO-SECOND-RELEASE')
   else:need(st['status']=='UNCERTAIN' and st['retries']<16 and p['result'] is None,'RETRY-STATE');st['retries']+=1
   need(s['counts']['attempt']<service.config['limits']['attempt'] and st['attempts']<MAX_STAGE_TRANSACTIONS,'ATTEMPT-EXHAUSTED')
   if cmd['kind']=='finalize':
    need(st['verifiers']<18 and s['counts']['verifier']<64 and s['partitions']['verifier']<18,'VERIFIER-RESERVATION')
    st['verifiers']+=1;new['counts']['verifier']+=1;new['partitions']['verifier']+=1
   # Conservatively precharge every finalization attempt before possible transmission.
   new['counts']['attempt']+=1;st['attempts']+=1;p['attempt']=op;p['query']=None;st['status']='UNCERTAIN'
   p['release_binding']=blob(enc(body),4096)
  elif kind in ['STAGE_QUERY','STAGE_BACKUP']:
   k='query' if kind=='STAGE_QUERY' else 'snapshot'
   if k=='query':need(not body and st['status']=='UNCERTAIN' and st['pending'] is not None,'QUERY-STATE')
   else:
    need(type(body) is dict and set(body)=={'format','request_id','intent','sid'},'BACKUP-FIELDS')
    need(strict.same(body,backup_body(s,st,body['request_id'])),'BACKUP-BINDING')
    need(op==backup_operation(service.binding,u,body['request_id']),'BACKUP-OP')
    need(op not in v.get('backups',{}),'BACKUP-ALREADY-AUTHORIZED')
    # Charge and one-shot authorization are the SAME protected transaction.
    # Commit/response loss cannot leave an uncharged callback authorization.
    # This state conservatively means the callback MAY have run, even if its
    # first instruction was never reached. Recovery cannot reset this record.
    new['u'][u].setdefault('backups',{})[op]={'seq':new['seq'],'state':'AUTHORIZED-UNCERTAIN'}
   need(s['counts'][k]<service.config['limits'][k] and s['partitions'][k]<service.config['limits']['staging_'+k],'SHARED-OR-PARTITION-EXHAUSTED')
   new['counts'][k]+=1;new['partitions'][k]+=1
   if k=='query':st['pending']['result']=None;st['pending']['query']={'op':op,'ordinal':new['counts'][k],'attempt':st['pending']['attempt']}
  elif kind=='STAGE_BACKUP_FINISH':
   need(type(body) is dict and set(body)=={'charge','outcome'},'BACKUP-FINISH-FIELDS')
   charge=body['charge'];need(type(charge) is dict and set(charge)=={'request','seq','head'},'BACKUP-RECEIPT')
   q=charge['request'];need(type(q) is dict and label(q.get('op')),'BACKUP-RECEIPT-REQUEST')
   saved=service.backend.get('OP/'+q['op']);need(saved is not None,'BACKUP-NO-CHARGE')
   actual=service.receipt(saved,s)
   need(strict.same(charge,actual) and q['binding']==service.binding and q['u']==u and q['kind']=='STAGE_BACKUP','BACKUP-EXACT-RECEIPT')
   record=v.get('backups',{}).get(q['op'])
   need(record is not None and strict.same(record['seq'],charge['seq']) and record['state']=='AUTHORIZED-UNCERTAIN','BACKUP-FINISH-STATE')
   need(type(body['outcome']) is str and body['outcome'] in ['CALLBACK-RETURNED','CALLBACK-RAISED-UNCERTAIN'],'BACKUP-OUTCOME')
   need(op=='backup-finish-'+sha(enc(charge)),'BACKUP-FINISH-OP')
   # Executor-reported local bookkeeping only, never external completion proof.
   new['u'][u]['backups'][q['op']]['state']=body['outcome']
  elif kind=='STAGE_RESULT':
   p=st['pending'];need(st['status']=='UNCERTAIN' and p is not None and p['query'] is not None and p['result'] is None,'RESULT-STATE')
   charged=service.resolve(p['query']['op'])['receipt']
   need(charged is not None and charged['request']['kind']=='STAGE_QUERY' and charged['request']['u']==u,'MISSING-STAGE-CHARGE')
   event=parse(service.backend.get('SEQ/'+str(charged['seq'])),MAX_EVENT)
   need(strict.same(event['after']['counts']['query'],p['query']['ordinal']),'QUERY-RECEIPT-COORDINATE')
   want={'format':'LAB-STAGE-OUTCOME-1','pilot':st['pilot'],'session':st['session'],'sid':st['sid'],'u':u,'intent':st['intent'],'message':st['message'],'command':cmd,'prepared_head':p['prepared_head'],'near_sha256':p['near'],'transaction_id':p['txid'],'query':p['query'],'outcome':body.get('outcome'),'authenticity':'SIMULATED-NOT-GENUINE-C4'}
   if cmd['kind']=='cleanup' and body.get('outcome')=='SUCCESS':
    cleanup_execution(body.get('cleanup_result'),meta,st);want['cleanup_result']=body['cleanup_result']
   need(strict.same(body,want) and body['outcome'] in ['SUCCESS','REVERTED','UNAVAILABLE'],'RESULT-BINDING')
   p['result']=blob(enc(body),MAX_INTENT)
   if body['outcome']=='SUCCESS':
    st['index']+=1;st['pending']=None;st['status']='AUTHENTICATED-CONDITIONAL' if cmd['kind']=='finalize' else 'COMPLETE' if cmd['kind']=='cleanup' else 'READY'
   elif body['outcome']=='REVERTED':st['status']='FAILED'
   # UNAVAILABLE remains frozen; no reinterpretation as REVERTED.
  elif kind=='STAGE_CLEANUP_READY':
   need(not body and st['status']=='AUTHENTICATED-CONDITIONAL' and v['record']['status'] in ['SUCCESS','FAILED'],'SIGNING-NOT-TERMINAL');st['status']='READY'
  else:raise Blocked('UNKNOWN-STAGE-TRANSITION')
 new['u'][u]['stage']=st
 return kind in ['STAGE_ATTEMPT','STAGE_RETRY']

class Scheduler:
 def __init__(self,connected):self.x=connected;self.service=connected.service
 def state(self,u):
  self.x.check();s=self.service.fresh();need(u in s['u'],'U');return s,s['u'][u].get('stage')
 def advance(self,u,kind,body=None,op=None):
  # No outbox state is an authorization. Each operation uses the current service
  # head; uncertain operations must be resolved by their original request.
  s,st=self.state(u);body=parse(enc(body or {}),MAX_INTENT)
  return self.service.commit(s['head'],op or 'stage-'+sha(enc([s['head'],kind,u,body])),kind,u,body)
 def open(self,u,message,key,signature):return self.advance(u,'STAGE_OPEN',{'message_hex':bytes(message).hex(),'key':bytes(key).hex(),'signature':bytes(signature).hex()})
 def prepare(self,u,spec,near,signed_evm=None):
  s,st=self.state(u);need(st is not None,'NO-SESSION');msg=self.service.blob(st['message'],MAX_INTENT);meta=parse(self.service.blob(st['meta'],MAX_INTENT),MAX_INTENT)
  body={'previous':s['head'],'command':command(meta,msg,st['index']),'near_spec':spec,'near_hex':bytes(near).hex()}
  if signed_evm is not None:
   need(exact_evm_from_near(spec,near)==bytes(signed_evm),'CALLER-SIGNED-BYTES')
   body['format']=PREPARE_FORMAT
  return self.advance(u,'STAGE_PREPARE',body)
 def send(self,u,sink,retry=False,crash=False):
  from connected import OfflineSink
  need(type(sink) is OfflineSink,'OFFLINE-ONLY');s,st=self.state(u);need(st and st['pending'],'NO-STAGE')
  kind='STAGE_RETRY' if retry else 'STAGE_ATTEMPT'
  body={'release':release_binding(s,st,kind)}
  raw=bytes(self.service.blob(body['release']['pending']['near'],MAX_TRANSACTION))
  need(sha(raw)==body['release']['pending']['near'],'RELEASE-BYTE-BINDING')
  op='stage-'+sha(enc([s['head'],kind,u,body]))
  # Never refresh the head after selecting bytes. The service CAS and exact
  # release binding validate selection, charge and frozen bytes together.
  result=self.service.commit(s['head'],op,kind,u,body)
  request={'binding':s['binding'],'expected':s['head'],'op':op,'kind':kind,'u':u,'body_hash':sha(enc(body))}
  need(strict.same(result['receipt']['request'],request),'RELEASE-RECEIPT-BINDING')
  need(result['release'],'NO-RECOVERY-RELEASE');latest,_=self.state(u);need(latest['head']==result['receipt']['head'],'HEAD-CHANGED')
  pending=latest['u'][u]['stage']['pending']
  need(pending['attempt']==op and pending['release_binding']==sha(enc(body)) and pending['near']==sha(raw),'COMMITTED-RELEASE-BYTES')
  self.x.check()
  if crash:raise Uncertain('CHARGED-BEFORE-SEND')
  sink.send(raw)
 def observe_lab(self,u,provider):
  # Charge before invoking the explicitly simulated outcome provider.
  self.advance(u,'STAGE_QUERY');s,st=self.state(u)
  body=provider(s,st)
  return self.advance(u,'STAGE_RESULT',body)
 def backup_status(self,u,request_id):
  # Read-only recovery. A recovered receipt is evidence, never a capability.
  s,st=self.state(u);body=backup_body(s,st,request_id);op=backup_operation(s['binding'],u,request_id)
  found=self.service.resolve(op);charge=found['receipt']
  if charge is None:
   need(op not in s['u'][u].get('backups',{}),'BACKUP-MISSING-RECEIPT')
   return {'receipt':None,'state':'NOT-AUTHORIZED','callback_authorized':False}
  q=charge['request']
  need(q['binding']==s['binding'] and q['op']==op and q['kind']=='STAGE_BACKUP' and q['u']==u and q['body_hash']==sha(enc(body)),'BACKUP-RECOVERED-BINDING')
  # Refresh after resolve to cover a competing commit during the lookup.
  s,st=self.state(u);record=s['u'][u].get('backups',{}).get(op)
  need(record is not None and strict.same(record['seq'],charge['seq']) and record['state'] in ['AUTHORIZED-UNCERTAIN','CALLBACK-RETURNED','CALLBACK-RAISED-UNCERTAIN'],'BACKUP-RECOVERY-STATE')
  return {'receipt':charge,'state':record['state'],'callback_authorized':False}
 def _backup_finish(self,u,charge,outcome):
  return self.advance(u,'STAGE_BACKUP_FINISH',{'charge':charge,'outcome':outcome},'backup-finish-'+sha(enc(charge)))
 def backup(self,u,action,*,request_id):
  # Callers MUST retain this stable logical request ID across restart/retry.
  # A new ID denotes a separate charged request, never recovery of this one.
  need(callable(action),'BACKUP-CALLBACK')
  prior=self.backup_status(u,request_id)
  if prior['receipt'] is not None:return prior
  s,st=self.state(u);body=backup_body(s,st,request_id);op=backup_operation(s['binding'],u,request_id)
  result=self.service.commit(s['head'],op,'STAGE_BACKUP',u,body)
  charge=result['receipt'];request={'binding':s['binding'],'expected':s['head'],'op':op,'kind':'STAGE_BACKUP','u':u,'body_hash':sha(enc(body))}
  need(strict.same(charge['request'],request) and type(result['duplicate']) is bool and result['release'] is False,'BACKUP-CLAIM-RECEIPT')
  if result['duplicate']:return self.backup_status(u,request_id)
  # Only this fresh authenticated response can reach action(). No public
  # resume-from-receipt entry point exists. Durable consumed wire challenges
  # and the protected OP record prevent receipt replay on normal interfaces.
  self.x.check()
  try:action() # trusted offline callback only; not an external completion oracle
  except Exception:
   self._backup_finish(u,charge,'CALLBACK-RAISED-UNCERTAIN')
   raise
  self._backup_finish(u,charge,'CALLBACK-RETURNED')
  return {'receipt':charge,'state':'CALLBACK-RETURNED','callback_authorized':True}
 def recover(self,u):
  self.x.recover();return self.state(u)[1]
 def operational(self,*a,**k):raise Blocked('GENUINE-C4-AND-QUALIFIED-LIVE-COMPARISON-UNAVAILABLE')
