"""C3 service-side contract. No network construction, credentials or release method."""
import hashlib,json,copy
MAX_INTENT=262144;MAX_TRANSACTION=75088;MAX_STATE=196608;MAX_EVENT=212992;MAX_EVENTS=12000;MAX_U=64
class Blocked(ValueError):pass
class Uncertain(RuntimeError):pass
def need(x,m):
 if not x:raise Blocked(m)
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
# Keep generic/config/request parsing at its inherited ceiling. Only aggregate
# HEAD and event consumers opt into the larger derived representation bounds.
# I164-AGGREGATE-STATE-2: staged one-session envelope; see capacity derivation.
# This is not a new U/action allowance or a bound on external evidence.
def parse(b,limit=65536):
 need(type(b) is bytes and len(b)<=limit,'BYTE-BOUND')
 def pairs(ps):
  d={}
  for k,v in ps:need(k not in d,'DUPLICATE');d[k]=v
  return d
 x=json.loads(b,object_pairs_hook=pairs);need(enc(x)==b,'CANONICAL');return x
def label(x):return type(x) is str and 0<len(x)<=128
def digest(x):return type(x) is str and len(x)==64 and all(c in '0123456789abcdef' for c in x)
def coordinates(x):
 need(type(x) is dict and set(x)=={'executor_head','transport_head','transport_seq'},'COORDINATES')
 need(digest(x['executor_head']) and digest(x['transport_head']) and type(x['transport_seq']) is int and 0<=x['transport_seq']<=MAX_EVENTS,'COORDINATES')
class Anchor:
 def __init__(self,backend,config):
  self.backend=backend;self.config=parse(enc(config));self.binding=sha(enc(config));self.last=None
  need(set(config)=={'pilot','session','implementation','backend','origin','limits'},'CONFIG')
  need(label(config['pilot']) and label(config['session']) and digest(config['implementation']) and digest(config['origin']),'CONFIG-BINDING')
  need(set(config['limits'])=={'attempt','query','snapshot','staging_query','staging_snapshot'},'LIMITS')
  ceilings={'attempt':2070,'query':3110,'snapshot':130,'staging_query':2086,'staging_snapshot':85}
  for k,v in config['limits'].items():need(type(v) is int and 0<v<=ceilings[k],'LIMIT')
  self.check_backend()
 def check_backend(self):need(self.backend.identity()==self.config['backend'],'BACKEND-INCARNATION')
 def genesis(self,coords):
  """Administrative fixture provisioning only; never called by reopen/recovery."""
  self.check_backend();coordinates(coords)
  s={'binding':self.binding,'seq':0,'head':self.config['origin'],'counts':{'attempt':0,'query':0,'snapshot':0},'partitions':{'query':0,'snapshot':0},'u':{},'coordinates':coords}
  self.backend.create(enc(s));return s
 def load(self):
  self.check_backend();raw=self.backend.get('HEAD');need(raw is not None,'MISSING-ANCHOR-NO-INIT');s=parse(raw,MAX_STATE)
  need(s['binding']==self.binding,'SESSION-BINDING')
  if s['seq']:
   ev=self.backend.get('SEQ/'+str(s['seq']));need(ev is not None and sha(ev)==s['head'],'PARTIAL-OR-CORRUPT-HEAD');e=parse(ev,MAX_EVENT)
   need(enc(e['after'])==enc({k:v for k,v in s.items() if k!='head'}),'HEAD-EVENT-JOIN')
  else:need(s['head']==self.config['origin'] and not s['u'] and not any(s['counts'].values()),'GENESIS')
  if self.last:
   need(s['seq']>=self.last[0] and (s['seq']!=self.last[0] or s['head']==self.last[1]),'STALE-OR-FORKED-READ')
  self.last=(s['seq'],s['head']);return s,raw
 def blob(self,ref,maximum):
  raw=self.backend.get('BLOB/'+ref);need(raw is not None and len(raw)<=maximum and sha(raw)==ref,'BLOB-INTEGRITY');return raw
 def receipt(self,raw,s):
  r=parse(raw);ev=self.backend.get('SEQ/'+str(r['seq']))
  need(ev is not None and sha(ev)==r['head'] and r['seq']<=s['seq'],'RECEIPT-HISTORY')
  event=parse(ev,MAX_EVENT);need(event['request']==r['request'] and r['request']['binding']==self.binding,'RECEIPT-BINDING')
  return r
 def apply(self,expected,op,kind,u=None,intent=None,transaction=None,arguments=None,coords=None,fault=None):
  """Idempotent service operation. A duplicate/recovery response NEVER grants release."""
  self.check_backend();need(label(op) and digest(expected),'REQUEST')
  args=parse(enc(arguments or {}));coords=parse(enc(coords));coordinates(coords)
  blobs={}
  for name,b,limit in [('intent',intent,MAX_INTENT),('transaction',transaction,MAX_TRANSACTION)]:
   if b is not None:
    b=bytes(b);need(0<len(b)<=limit,'INPUT-SIZE');blobs['BLOB/'+sha(b)]=b
    if name=='intent':intent=b
    else:transaction=b
  req={'binding':self.binding,'expected':expected,'op':op,'kind':kind,'u':u,'intent':sha(intent) if intent is not None else None,'transaction':sha(transaction) if transaction is not None else None,'arguments':args,'coordinates':coords}
  request=enc(req);need(len(request)<=4096,'REQUEST-SIZE')
  prior=self.backend.get('OP/'+op)
  if prior is not None:
   s,_=self.load();receipt=self.receipt(prior,s);need(receipt['request']==req,'OP-SUBSTITUTION')
   for k,b in blobs.items():need(self.backend.get(k)==b,'EXACT-BLOB-SUBSTITUTION')
   self.load();return {'result':'ALREADY-COMMITTED-NO-RELEASE','receipt':receipt,'release':False}
  s,old=self.load();need(s['head']==expected,'EXPECTED-HEAD');need(s['seq']<MAX_EVENTS,'HISTORY-LIMIT');new=copy.deepcopy(s);new.pop('head');new['seq']+=1
  need(coords['transport_seq']>=s['coordinates']['transport_seq'],'HISTORY-REGRESSION');new['coordinates']=coords
  if kind=='RESERVE':
   need(label(u) and u not in s['u'] and len(s['u'])<MAX_U and intent is not None and transaction is None,'U-RESERVATION')
   need(set(args)=={'nonce'} and label(args['nonce']),'NONCE');need(all(v['nonce']!=args['nonce'] for v in s['u'].values()),'NONCE-RESERVED')
   new['u'][u]={'intent':sha(intent),'nonce':args['nonce'],'status':'RESERVED','transaction':None,'evidence':None}
  elif kind=='ATTEMPT':
   need(set(args)==set() and u in s['u'] and s['u'][u]['status']=='RESERVED' and intent is not None and transaction is not None,'ATTEMPT-STATE')
   need(self.blob(s['u'][u]['intent'],MAX_INTENT)==intent,'IMMUTABLE-INTENT')
   need(s['counts']['attempt']<self.config['limits']['attempt'],'EXHAUSTED-attempt');new['counts']['attempt']+=1
   new['u'][u].update(status='UNCERTAIN',transaction=sha(transaction))
  elif kind=='CHARGE':
   need(intent is None and transaction is None and set(args)=={'allowance','partition'},'CHARGE-FIELDS')
   k=args['allowance'];part=args['partition'];need(k in ['query','snapshot'] and part in ['staging','other'],'ALLOWANCE')
   need(u is None or u in s['u'],'CHARGE-U');need(s['counts'][k]<self.config['limits'][k],'EXHAUSTED-'+k)
   if part=='staging':need(s['partitions'][k]<self.config['limits']['staging_'+k],'PARTITION-EXHAUSTED');new['partitions'][k]+=1
   new['counts'][k]+=1
  elif kind=='TERMINAL':
   need(u in s['u'] and s['u'][u]['status']=='UNCERTAIN' and intent is not None and transaction is not None,'TERMINAL-STATE')
   need(self.blob(s['u'][u]['intent'],MAX_INTENT)==intent and self.blob(s['u'][u]['transaction'],MAX_TRANSACTION)==transaction,'TERMINAL-EXACT-BINDING')
   need(set(args)=={'saved_receipt','saved_history','outcome','charged_op'},'EVIDENCE-FIELDS')
   need(digest(args['saved_receipt']) and digest(args['saved_history']),'EVIDENCE-IDENTITY')
   charged=self.backend.get('OP/'+args['charged_op']);need(charged is not None,'MISSING-CHARGE');charged=self.receipt(charged,s)
   q=charged['request'];need(q['kind']=='CHARGE' and q['u']==u and q['arguments']=={'allowance':'query','partition':'staging'},'EVIDENCE-CHARGE')
   need(args['outcome'] in ['SUCCESS','REVERTED'],'NO-EVM-TERMINAL-EVIDENCE')
   # Only a C1-validated saved-evidence caller may invoke: opaque refs are NOT oracle validation.
   new['u'][u].update(status='SUCCESS' if args['outcome']=='SUCCESS' else 'FAILED',evidence=dict(args))
  else:raise Blocked('UNSUPPORTED-TRANSITION')
  event=enc({'request':req,'previous':expected,'after':new});need(len(event)<=MAX_EVENT,'EVENT-CAPACITY')
  head=sha(event);new['head']=head;raw=enc(new);need(len(raw)<=MAX_STATE,'STATE-CAPACITY')
  receipt={'request':req,'seq':new['seq'],'head':head};puts={'OP/'+op:enc(receipt),'SEQ/'+str(new['seq']):event,**blobs}
  # Deduplicate exact existing content blobs; they are never overwritten.
  for k,b in list(blobs.items()):
   existing=self.backend.get(k)
   if existing is not None:need(existing==b,'BLOB-CONFLICT');puts.pop(k)
  try:self.backend.commit(old,raw,puts,fault)
  except (TimeoutError,OSError) as ex:raise Uncertain('WRITE-UNKNOWN: no release; resolve exact OP before further action') from ex
  self.last=(new['seq'],head)
  return {'result':'COMMITTED','receipt':receipt,'release':kind=='ATTEMPT'}
 def resolve(self,op):
  """Internal lookup only; cannot re-authorize a send even if ATTEMPT committed."""
  s,_=self.load();raw=self.backend.get('OP/'+op)
  return {'result':'SAVED-NO-RELEASE' if raw is not None else 'NOT-FOUND-NO-RELEASE','receipt':self.receipt(raw,s) if raw else None,'release':False}
 def restore_anchor(self,*args,**kwargs):raise Blocked('ANCHOR-RESTORE-OR-REPLACEMENT-NOT-AUTHORIZED')
