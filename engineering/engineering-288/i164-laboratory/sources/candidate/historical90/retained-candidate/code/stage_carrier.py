"""Conditional transition reference, NOT an on-chain implementation or operational permit.
Uses complete original bytes and a native oracle; does not implement SHA-512 compression.
"""
import copy,hashlib,hmac,json,threading,subprocess
DOMAIN=b'I164-ARCHITECTURE-A-AUTHORIZED-INPUTS-V2\n'
MAX=1048617
METHODS={'signPetition','signPetitionWithZKProof'}
KEYS={'pilot','network','engine','registry','registry_code','auth_manager','auth_code','epoch','configuration','method','operation','inputs','actor','authorizer','executor','profile','model','contract','program','issuer','appointment','public_key_hash','collector_inputs','collector_result','three_scopes','authorized_state','u','history_prefix','phase','expiry','decoder'}
def W(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode()
def H(x):return hashlib.sha256(x).hexdigest()
class Reject(Exception):pass
def need(x,n):
 if not x:raise Reject(n)
HASH_FIELDS={'registry_code','auth_code','configuration','operation','inputs','profile','model','contract','program','appointment','public_key_hash','collector_inputs','collector_result','three_scopes','authorized_state','u','history_prefix'}
ADDRESS_FIELDS={'registry','auth_manager','actor','authorizer','executor'}
def validate_context(c):
 need(type(c)==dict and set(c)==KEYS and len(W(c))<=4096,'CONTEXT')
 need(all(type(v)==str and 0<len(v)<=256 for v in c.values()),'CONTEXT-TYPES')
 for k in HASH_FIELDS|ADDRESS_FIELDS:
  n=64 if k in HASH_FIELDS else 40
  need(len(c[k])==n and all(x in '0123456789abcdef' for x in c[k]),'BINDING-ENCODING')
 for k in ['expiry','epoch','network']:
  need(c[k].isdigit() and str(int(c[k]))==c[k] and int(c[k])<2**64,'UINT64')
 need(c['method'] in METHODS and c['phase']=='PRE-COMMITMENT','METHOD/PHASE')
def decode(raw):
 def unique(pairs):
  d={}
  for k,v in pairs:
   need(k not in d,'DUPLICATE');d[k]=v
  return d
 try:o=json.loads(raw,object_pairs_hook=unique)
 except (ValueError,UnicodeError):raise Reject('ENCODING')
 need(W(o)==raw and set(o)=={'format','bindings','authorized_values'} and o['format']=='I164-A-STAGED-AUTHORIZED-INPUTS-2','CANONICAL')
 c=o['bindings'];validate_context(c);need(type(c)==dict and set(c)==KEYS and len(W(c))<=4096,'CONTEXT')
 need(all(type(v)==str and 0<len(v)<=256 for v in c.values()),'CONTEXT-TYPES')
 need(c['method'] in METHODS and c['phase']=='PRE-COMMITMENT','METHOD/PHASE')
 need(c['expiry'].isdigit() and str(int(c['expiry']))==c['expiry'],'EXPIRY')
 vs=o['authorized_values'];need(type(vs)==list and 1<=len(vs)<=19,'COVERAGE');total=0
 for v in vs:
  need(type(v)==str and len(v)%2==0 and len(v)<=131072,'VALUE')
  try:b=bytes.fromhex(v)
  except ValueError:raise Reject('VALUE')
  need(b.hex()==v,'VALUE');total+=len(b)
 need(total<=524288,'ARENA')
 return o
class Model:
 def __init__(self,context,backend,query_limit=1024,session_limit=1,chunk=512):
  need(chunk in (512,1024),'CHUNK');self.lock=threading.RLock();self.backend=str(backend)
  self.s={'context':copy.deepcopy(context),'queries':1,'backups':1,'query_limit':query_limit,'snapshot_limit':130,'session_limit':session_limit,'chunk':chunk,'sessions':{},'retired':{},'attempts':0,'events':[],'version':0,'previous':None}
 def event(self,kind,**kw):self.s['events'].append(dict(kind=kind,**kw));self.s['version']+=1
 def retire(self,u,intent):
  with self.lock:
   need(u not in self.s['retired'],'U-RETIRED');self.s['retired'][u]={'intent':H(bytes(intent)),'status':'RETIRED'};self.event('RETIRE',u=u)
 def charge(self,kind,request):
  with self.lock:
   need(kind in ('query','snapshot') and type(request)==str and 0<len(request)<=256,'REQUEST');k,limit=('queries','query_limit') if kind=='query' else ('backups','snapshot_limit')
   need(self.s[k]<self.s[limit],'EXHAUSTED');self.s[k]+=1;self.event('CHARGE',category=kind,ordinal=self.s[k],request=request)
   return dict(category=kind,ordinal=self.s[k],request=request,pilot=self.s['context']['pilot'])
 def dispatch(self,action,request,*args,**kwargs):
  with self.lock:
   need(action in ('begin','append','finalize','release','abandon','cleanup'),'ACTION')
   cap=self.s['session_limit']*((MAX+self.s['chunk']-1)//self.s['chunk']+5)+16
   need(self.s['attempts']<cap,'TRANSPORT-EXHAUSTED');self.s['attempts']+=1;self.event('SUBMISSION-ATTEMPT',request=request,ordinal=self.s['attempts'])
   return getattr(self,action)(*args,**kwargs)
 def observe(self,sid,request):
  with self.lock:
   receipt=self.charge('query',request);v=self.s['sessions'][sid]
   return dict(receipt=receipt,sid=sid,offset=v['offset'],state=v['state'],version=self.s['version'],actual_admission=False)
 def repair_internal(self):return None # no observation/disclosure; no synthetic refund
 def begin(self,ctx,msg_hash,total,a,sig,intent,caller):
  with self.lock:
   ctx=copy.deepcopy(ctx);validate_context(ctx);a=bytes(a);sig=bytes(sig);u=ctx['u']
   need(caller==ctx['executor'],'EXECUTOR');need(ctx==self.s['context'],'BINDINGS');need(ctx['method'] in METHODS,'METHOD')
   need(u in self.s['retired'] and self.s['retired'][u]['status']=='RETIRED' and self.s['retired'][u]['intent']==H(bytes(intent)),'RETIREMENT')
   need(H(a)==ctx['public_key_hash'],'KEY-BINDING');need(len(self.s['sessions'])<self.s['session_limit'],'SESSIONS');need(41<=total<=MAX and len(a)==32 and len(sig)==64,'BOUNDS')
   sid=H(b'I164-STAGING-SESSION-1\0'+W(ctx)+bytes.fromhex(msg_hash)+a+sig+total.to_bytes(8,'big'))
   self.s['sessions'][sid]=dict(ctx=ctx,msg_hash=msg_hash,total=total,a=a.hex(),sig=sig.hex(),offset=0,chunks=[],state='OPEN',finalized=False,sequence=0)
   self.s['retired'][u]['status']='SESSION-BOUND';self.event('BEGIN',sid=sid);return sid
 def active(self,sid,caller,now):
  v=self.s['sessions'][sid];need(caller==v['ctx']['executor'],'EXECUTOR');need(v['ctx']==self.s['context'],'STALE-CONFIG');need(now<=int(v['ctx']['expiry']),'EXPIRED');return v
 def append(self,sid,offset,data,caller,now):
  with self.lock:
   v=self.active(sid,caller,now);need(v['state']=='OPEN','TERMINAL');data=bytes(data)
   need(offset==v['offset'],'OFFSET');need(len(data)==min(self.s['chunk'],v['total']-offset) and len(data)>0,'CHUNK')
   v['chunks'].append(data.hex());v['offset']+=len(data);v['sequence']+=1;self.event('APPEND',sid=sid,offset=offset,length=len(data))
 def finalize(self,sid,caller,now):
  with self.lock:
   v=self.active(sid,caller,now);need(v['state']=='OPEN' and v['offset']==v['total'],'INCOMPLETE')
   message=b''.join(bytes.fromhex(x) for x in v['chunks'])
   try:
    need(H(message)==v['msg_hash'] and message.startswith(DOMAIN),'MESSAGE')
    o=decode(message[len(DOMAIN):]);need(o['bindings']==v['ctx'],'MESSAGE-BINDING')
    need(H(open(self.backend,'rb').read())=='3d8b65ea87eb5b5a680c9c51c6897a8c32641f1580947046d1cc6c7f765c152b','BACKEND')
    r=subprocess.run([self.backend,'verify',v['a'],v['sig'],str(len(message)),str(len(message))],input=message,capture_output=True,timeout=5)
    need(r.returncode==0 and json.loads(r.stdout).get('verified') is True,'SIGNATURE')
   except (Reject,subprocess.TimeoutExpired) as e:
    v['state']='FAILED';self.event('FINALIZE-FAIL',sid=sid,reason=str(e));return False
   v['state']='AUTHENTICATED';v['finalized']=True;v['values']=o['authorized_values'];self.event('FINALIZE',sid=sid);return True
 def release(self,sid,method,caller,now,live_values,known,request_bindings,qualified=False,original_checks=True,verifier=True,simulate_rollback=False):
  with self.lock:
   v=self.active(sid,caller,now);need(v['state']=='AUTHENTICATED','NOT-AUTHENTICATED');need(method==v['ctx']['method'],'METHOD');need(request_bindings==v['ctx'],'REQUEST-BINDING')
   # Invocation is retired externally before attempt, and this mark survives modeled EVM rollback.
   u=v['ctx']['u'];need(self.s['retired'][u]['status']=='SESSION-BOUND','U-REPLAY');self.s['retired'][u]['status']='RELEASE-ATTEMPTED'
   failures=[]
   if not original_checks or (method=='signPetitionWithZKProof' and not verifier):failures.append('ORIGINAL-GUARD/VERIFIER')
   if not qualified:failures.append('QUALIFICATION-UNAVAILABLE')
   if len(live_values)!=len(v['values']) or len(known)!=len(v['values']):failures.append('COVERAGE')
   elif not all(x is True for x in known):failures.append('FACTS-UNAVAILABLE')
   elif list(live_values)!=v['values']:failures.append('EQ-FALSE/MC-TRUE')
   if failures or simulate_rollback:
    # External executor freezes failed U. A real EVM revert need not retain contract writes.
    v['state']='FROZEN' if simulate_rollback else 'REJECTED';self.event('RELEASE-FAIL',sid=sid,failures=failures);return dict(conditional_effect=False,failures=failures,actual_admission=False)
   v['state']='CONSUMED';self.event('CONSUME-AND-EFFECT',sid=sid);return dict(conditional_effect=True,actual_admission=False)
 def abandon(self,sid,caller):
  with self.lock:
   v=self.s['sessions'][sid];need(caller==v['ctx']['executor'],'EXECUTOR');need(v['state'] not in ('CONSUMED','ABANDONED'),'TERMINAL');v['state']='ABANDONED';self.event('ABANDON',sid=sid)
 def cleanup(self,sid,caller):
  with self.lock:
   v=self.s['sessions'][sid];need(caller==v['ctx']['executor'],'EXECUTOR');need(v['state'] in ('CONSUMED','ABANDONED','FAILED','REJECTED'),'NOT-TERMINAL')
   need(not v.get('cleaned',False),'ALREADY-CLEANED');v['chunks']=[];v.pop('values',None);v['cleaned']=True;self.event('CLEANUP',sid=sid)
 def snapshot(self,key):
  with self.lock:
   raw=W(self.s);return W(dict(state=self.s,mac=hmac.new(key,raw,'sha256').hexdigest())),(self.s['version'],H(raw))
 @classmethod
 def restore(cls,blob,key,anchor,backend,expected_context):
  o=json.loads(blob);need(o['state']['context']==expected_context,'JOB-BINDING');raw=W(o['state']);need(hmac.compare_digest(o['mac'],hmac.new(key,raw,'sha256').hexdigest()),'MAC');need((o['state']['version'],H(raw))==anchor,'ROLLBACK/SUBSTITUTION')
  v=cls.__new__(cls);v.lock=threading.RLock();v.backend=str(backend);v.s=copy.deepcopy(o['state'])
  for s in v.s['sessions'].values():
   need((s.get('cleaned',False) and not s['chunks'] and s['state'] in ('CONSUMED','ABANDONED','FAILED','REJECTED')) or sum(len(bytes.fromhex(x)) for x in s['chunks'])==s['offset'],'RECOVERY-OFFSET')
  return v
