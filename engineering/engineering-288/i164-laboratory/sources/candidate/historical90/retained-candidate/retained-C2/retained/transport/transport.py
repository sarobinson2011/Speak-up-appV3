"""Bounded OFFLINE-ONLY transport. No sockets, RPC, operational signer or admission."""
import fcntl,hashlib,json,os,sqlite3,struct
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
VERSION='I164-OFFLINE-DURABLE-TRANSPORT-1'
MAX_RAW=74829;MAX_NEAR=75088;MAX_EVENT=16384;MAX_EVENTS=12000
class Blocked(ValueError):pass
def need(x,m):
 if not x:raise Blocked(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def parse(b,limit=MAX_EVENT):
 b=bytes(b);need(len(b)<=limit,'SIZE')
 def pairs(a):
  d={}
  for k,v in a:need(k not in d,'DUPLICATE');d[k]=v
  return d
 x=json.loads(b,object_pairs_hook=pairs);need(enc(x)==b,'CANONICAL');return x
def digest(x):return type(x) is str and len(x)==64 and all(c in '0123456789abcdef' for c in x)
def vector(b):return struct.pack('<I',len(b))+b
def unsigned(s,evm):
 need(set(s)=={'network','engine','method','signer','public_key','nonce','block_hash','gas','deposit'},'NEAR-SPEC')
 need(s['network']=='near-testnet' and s['engine']=='aurora' and s['method']=='submit','DESTINATION')
 need(type(s['signer']) is str and 2<=len(s['signer'])<=64 and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-._' for c in s['signer']),'SIGNER')
 need(type(s['nonce']) is int and 0<s['nonce']<2**64,'NONCE')
 need(type(s['gas']) is int and 0<s['gas']<=10**15 and type(s['deposit']) is int and s['deposit']==0,'GAS-DEPOSIT')
 need(digest(s['public_key']) and digest(s['block_hash']),'KEY-BLOCK')
 need(0<len(evm)<=MAX_RAW,'EVM-SIZE')
 return (vector(s['signer'].encode())+b'\0'+bytes.fromhex(s['public_key'])+struct.pack('<Q',s['nonce'])+vector(b'aurora')+bytes.fromhex(s['block_hash'])+struct.pack('<I',1)+b'\x02'+vector(b'submit')+vector(evm)+struct.pack('<Q',s['gas'])+bytes(16))
def exact_near(s,evm,raw):
 expected=unsigned(s,evm);need(len(raw)<=MAX_NEAR and len(raw)==len(expected)+65 and raw[:len(expected)]==expected and raw[len(expected)]==0,'EXACT-NEAR-BINDING')
 try:Ed25519PublicKey.from_public_bytes(bytes.fromhex(s['public_key'])).verify(raw[-64:],bytes.fromhex(sha(expected)))
 except Exception as e:raise Blocked('NEAR-SIGNATURE') from e
 return sha(expected) # NEAR transaction id hashes unsigned transaction, NOT signed envelope.

def fsyncdir(p):
 fd=os.open(str(p),os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)

class Session:
 """Two attached SQLite databases; atomic commits in rollback-journal mode.
 Anchor is separate lab storage. Anti-rollback requires independently protected anchor.
 """
 def __init__(self,db,anchor,config,create=False,bound_code=None):
  self.path=Path(db).resolve();self.anchor=Path(anchor).resolve();self.locks=[];self.db=None
  need(self.path!=self.anchor,'DISTINCT-ANCHOR');self.config=parse(enc(config))
  need(set(config)=={'pilot','attempt_limit','query_limit','snapshot_limit','staging_query_limit','staging_snapshot_limit','prerequisites'},'CONFIG')
  need(type(config['pilot']) is str and config['pilot'].startswith('LAB-TRANSPORT-'),'LAB-ONLY')
  for k,ceiling in [('attempt_limit',2070),('query_limit',3110),('snapshot_limit',130),('staging_query_limit',2086),('staging_snapshot_limit',85)]:need(type(config[k]) is int and 0<config[k]<=ceiling,'LIMIT')
  need(set(config['prerequisites'])=={'model','profile','configuration','collector','executor','accounting','authorization','engine_code'},'PREREQUISITES')
  need(all(digest(v) for v in config['prerequisites'].values()),'PREREQUISITE-DIGEST')
  self.binding={'version':VERSION,'code':sha(Path(__file__).read_bytes()) if bound_code is None else bound_code,'config':self.config}
  try:
   for p in sorted([self.path,self.anchor]):
    need(not p.is_symlink(),'SYMLINK');f=open(str(p)+'.lock','a+b');self.locks.append(f)
    try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise Blocked('CONCURRENT-WRITER')
   need((not self.path.exists() and not self.anchor.exists()) if create else (self.path.is_file() and self.anchor.is_file()),'MISSING-OR-EXISTING-STATE')
   self.db=sqlite3.connect('file:'+str(self.path)+'?mode='+('rwc' if create else 'rw'),uri=True,isolation_level=None)
   self.db.execute('PRAGMA journal_mode=DELETE');self.db.execute('PRAGMA synchronous=FULL')
   self.db.execute('ATTACH DATABASE ? AS guard',(str(self.anchor),));self.db.execute('PRAGMA guard.journal_mode=DELETE');self.db.execute('PRAGMA guard.synchronous=FULL')
   if create:
    self.db.executescript('BEGIN IMMEDIATE;CREATE TABLE meta(b BLOB);CREATE TABLE log(seq INTEGER PRIMARY KEY,b BLOB,h TEXT);CREATE TABLE blobs(h TEXT PRIMARY KEY,b BLOB);CREATE TABLE guard.head(binding TEXT,seq INTEGER,h TEXT);COMMIT;')
    self.db.execute('BEGIN IMMEDIATE');self.db.execute('INSERT INTO meta VALUES (?)',(enc(self.binding),));self.db.execute('INSERT INTO guard.head VALUES (?,?,?)',(sha(enc(self.binding)),0,'0'*64));self.db.execute('COMMIT');fsyncdir(self.path.parent);fsyncdir(self.anchor.parent)
   self.reload()
  except BaseException:self.close();raise
 def close(self):
  if self.db:self.db.close();self.db=None
  for f in self.locks:f.close()
  self.locks=[]
 def __enter__(self):return self
 def __exit__(self,*a):self.close()
 def blob(self,h):
  need(digest(h),'BLOB-REF');r=self.db.execute('SELECT length(b),b FROM blobs WHERE h=?',(h,)).fetchone();need(r is not None and r[0]<=300000 and sha(r[1])==h,'BLOB-INTEGRITY');return bytes(r[1])
 def hydrate(self,r):
  record=parse(self.blob(r['binding']),300000);s=record['near_spec'];raw=self.blob(record['near_bytes']);evm=self.blob(record['evm_bytes']);intent=self.blob(record['intent_bytes']);txid=exact_near(s,evm,raw)
  h=record['handoff'];need(set(h)=={'kind','u','intent_sha256','evm_sha256','retired','executor_head','prerequisites'},'HANDOFF-FIELDS')
  need(h['kind']=='LAB-RETIRED-EXECUTOR-HANDOFF' and h['retired'] is True and h['u']==record['u'] and digest(h['executor_head']),'RETIRED-U')
  need(h['intent_sha256']==sha(intent) and h['evm_sha256']==sha(evm) and h['prerequisites']==self.config['prerequisites'],'HANDOFF-BINDING')
  need(record['txid']==txid and record['pilot']==self.config['pilot'],'JOB-BINDING');return record,raw
 def reload(self):
  need(self.db.execute('PRAGMA integrity_check').fetchone()==('ok',) and self.db.execute('PRAGMA guard.integrity_check').fetchone()==('ok',),'CORRUPT-SQLITE')
  need(self.db.execute('SELECT b FROM meta').fetchall()==[(enc(self.binding),)],'CODE-CONFIG-BINDING')
  self.states={};self.counts={'attempt':0,'query':0,'snapshot':0};self.staging={'query':0,'snapshot':0};self.requests=set();head='0'*64;seq=0;nonces=set();self.receipts={}
  for ix,b,h in self.db.execute('SELECT seq,b,h FROM log ORDER BY seq'):
   seq+=1;need(seq<=MAX_EVENTS and ix==seq,'LOG-BOUND');e=parse(b);need(e['prev']==head and sha(b)==h,'HISTORY');head=h
   typ=e['type'];u=e.get('u');r=self.states.get(u)
   if typ=='PREPARE':
    need(r is None and type(u) is str and 0<len(u)<=128,'U-REUSE');r={'binding':e['binding'],'status':'PREPARED'};self.states[u]=r;rec,_=self.hydrate(r);need(rec['u']==u,'U-BINDING')
    s=rec['near_spec'];nonce=(s['network'],s['signer'],s['public_key'],s['nonce']);need(nonce not in nonces,'NONCE-CONFLICT');nonces.add(nonce)
   elif typ in ['ATTEMPT','QUERY','SNAPSHOT']:
    key=typ.lower();key='snapshot' if typ=='SNAPSHOT' else key
    need(e['partition'] in ['staging','other'],'PARTITION')
    if key in self.staging and e['partition']=='staging':
     self.staging[key]+=1;need(self.staging[key]<=self.config['staging_'+key+'_limit'],'STAGING-PARTITION')
    self.counts[key]+=1;need(self.counts[key]<=self.config[key+'_limit'] and e['ordinal']==self.counts[key],'BUDGET')
    need(e['request'] not in self.requests,'REQUEST-REPLAY');self.requests.add(e['request']);self.receipts[e['request']]={'seq':seq,'hash':h,'ordinal':e['ordinal'],'kind':key,'u':u,'pilot':self.config['pilot'],'binding':e['binding'],'partition':e['partition']}
    need(e['binding']==(r['binding'] if r else sha(enc(self.binding))),'CHARGE-BINDING')
    if typ=='ATTEMPT':need(r is not None and r['status']=='PREPARED','FROZEN');r['status']='UNCERTAIN';r['attempt_request']=e['request']
    if typ=='QUERY' and e['partition']=='staging':need(r is not None,'UNKNOWN-U')
   elif typ=='ACK':
    need(r is not None and r['status']=='UNCERTAIN' and e['attempt']==r['attempt_request'],'ACK-STATE');rec,_=self.hydrate(r);need(e['txid']==rec['txid'],'HASH-SUBSTITUTION')
   elif typ=='OUTCOME':
    need(r is not None and r['status']=='UNCERTAIN','OUTCOME-STATE');need(e['request'] in self.receipts and self.receipts[e['request']]['kind']=='query' and self.receipts[e['request']]['u']==u,'OBSERVATION-RECEIPT')
    rec,raw=self.hydrate(r);v=parse(self.blob(e['evidence']),MAX_EVENT);self.check_outcome(rec,raw,v)
    r['status']='SUCCESS' if v['near_outcome']=='SUCCESS' and v['evm_outcome']=='SUCCESS' else 'FAILED';r['evidence']=e['evidence']
   else:raise Blocked('EVENT-TYPE')
  need(self.db.execute('SELECT binding,seq,h FROM guard.head').fetchall()==[(sha(enc(self.binding)),seq,head)],'ANCHOR-MISMATCH-FREEZE')
  self.head=head;self.seq=seq
 def publish(self,event,blobs=()):
  self.reload();e=dict(event,prev=self.head);b=enc(e);need(len(b)<=MAX_EVENT and self.seq<MAX_EVENTS,'EVENT-BOUND');h=sha(b)
  self.db.execute('BEGIN IMMEDIATE')
  try:
   for raw in blobs:
    raw=bytes(raw);need(len(raw)<=300000,'BLOB-LIMIT');old=self.db.execute('SELECT b FROM blobs WHERE h=?',(sha(raw),)).fetchone();need(old is None or old[0]==raw,'COLLISION');self.db.execute('INSERT OR IGNORE INTO blobs VALUES (?,?)',(sha(raw),raw))
   self.db.execute('INSERT INTO log VALUES (?,?,?)',(self.seq+1,b,h));self.db.execute('UPDATE guard.head SET seq=?,h=?',(self.seq+1,h));self.db.execute('COMMIT')
  except BaseException:self.db.execute('ROLLBACK');raise
  self.reload()
 def prepare(self,u,intent,evm,near_spec,near_bytes,handoff):
  self.reload();need(u not in self.states,'RETIRED-U');intent=bytes(intent);evm=bytes(evm);raw=bytes(near_bytes);s=parse(enc(near_spec));h=parse(enc(handoff));need(len(intent)<=262144,'INTENT-LIMIT');txid=exact_near(s,evm,raw)
  need(h['u']==u and h['retired'] is True and h['kind']=='LAB-RETIRED-EXECUTOR-HANDOFF' and h['prerequisites']==self.config['prerequisites'] and h['intent_sha256']==sha(intent) and h['evm_sha256']==sha(evm) and digest(h['executor_head']),'HANDOFF')
  need(set(h)=={'kind','u','intent_sha256','evm_sha256','retired','executor_head','prerequisites'},'HANDOFF-FIELDS')
  for r in self.states.values():
   old,_=self.hydrate(r);o=old['near_spec'];need((o['network'],o['signer'],o['public_key'],o['nonce'])!=(s['network'],s['signer'],s['public_key'],s['nonce']),'NONCE-CONFLICT')
  rec={'pilot':self.config['pilot'],'u':u,'intent_bytes':sha(intent),'evm_bytes':sha(evm),'near_bytes':sha(raw),'near_spec':s,'handoff':h,'txid':txid}
  b=enc(rec);self.publish({'type':'PREPARE','u':u,'binding':sha(b)},[intent,evm,raw,b]);return txid
 def charge(self,kind,u,request,partition='staging'):
  self.reload();need(kind in self.counts and type(request) is str and 0<len(request)<=128 and request not in self.requests,'REQUEST');need(self.counts[kind]<self.config[kind+'_limit'],'EXHAUSTED-'+kind)
  need(partition in ['staging','other'],'PARTITION')
  if kind in self.staging and partition=='staging':need(self.staging[kind]<self.config['staging_'+kind+'_limit'],'STAGING-EXHAUSTED')
  if kind=='attempt' or (kind=='query' and partition=='staging'):need(u in self.states,'UNKNOWN-U')
  if kind=='attempt':need(self.states[u]['status']=='PREPARED','UNCERTAIN-OR-TERMINAL-FROZEN')
  self.publish({'type':kind.upper(),'u':u,'request':request,'ordinal':self.counts[kind]+1,'partition':partition,'binding':self.states[u]['binding'] if u in self.states else sha(enc(self.binding))});return dict(self.receipts[request])
 def submit(self,u,request,transport,crash=None):
  need(type(transport) is OfflineTransport,'OFFLINE-ONLY')
  if crash=='before_charge':raise RuntimeError('crash before charge')
  receipt=self.charge('attempt',u,request)
  if crash=='after_charge':raise RuntimeError('crash after durable charge')
  rec,raw=self.hydrate(self.states[u])
  ack=transport.send(rec,raw)
  if crash=='after_send':raise RuntimeError('crash after transmission')
  need(ack['txid']==rec['txid'] and ack['raw_sha256']==sha(raw),'ACK-SUBSTITUTION')
  self.publish({'type':'ACK','u':u,'attempt':request,'txid':rec['txid']})
  return {'result':'ACK-ONLY-NOT-EXECUTION','receipt':receipt,'actual_admission':False}
 @staticmethod
 def check_outcome(rec,raw,v):
  need(set(v)=={'kind','network','signer','txid','raw_sha256','finality','near_outcome','evm_outcome'},'OUTCOME-FIELDS')
  need(v['kind']=='LAB-SIMULATED-OUTCOME' and v['network']==rec['near_spec']['network'] and v['signer']==rec['near_spec']['signer'] and v['txid']==rec['txid'] and v['raw_sha256']==sha(raw),'OUTCOME-IDENTITY')
  need(v['finality']=='FINAL' and ((v['near_outcome']=='SUCCESS' and v['evm_outcome'] in ['SUCCESS','REVERTED']) or (v['near_outcome']=='FAILURE' and v['evm_outcome']=='NOT-EXECUTED')),'UNRESOLVED-OUTCOME')
 def reconcile(self,u,request,transport,crash=None):
  need(type(transport) is OfflineTransport,'OFFLINE-ONLY');self.reload();need(u in self.states,'UNKNOWN-U')
  # Terminal reuse is internal computation; externally returned observations still consume a query.
  receipt=self.charge('query',u,request);rec,raw=self.hydrate(self.states[u])
  if crash=='after_charge':raise RuntimeError('crash after query charge')
  if self.states[u]['status'] in ['SUCCESS','FAILED']:
   return {'status':self.states[u]['status'],'receipt':receipt,'terminal_reused':True,'actual_admission':False}
  need(self.states[u]['status']=='UNCERTAIN','NOT-SUBMITTED')
  v=transport.lookup(rec,raw)
  if v is None:return {'status':'UNCERTAIN','receipt':receipt,'actual_admission':False}
  self.check_outcome(rec,raw,v)
  if crash=='after_lookup':raise RuntimeError('crash before result persistence')
  b=enc(v);self.publish({'type':'OUTCOME','u':u,'request':request,'evidence':sha(b)},[b])
  return {'status':self.states[u]['status'],'receipt':receipt,'actual_admission':False}
 def internal_repair(self):self.reload() # no observation emission or network action
 def backup(self,path,request):
  self.charge('snapshot',None,request);dest=Path(path);need(not dest.exists(),'BACKUP-EXISTS')
  with dest.open('xb') as f:
   f.write(self.path.read_bytes());f.flush();os.fsync(f.fileno())
  fsyncdir(dest.parent);return {'head':self.head,'sha256':sha(dest.read_bytes()),'anchor_not_backed_up':True}

class OfflineTransport:
 """In-process, explicitly simulated ledger. No network method exists."""
 def __init__(self):self.seen={};self.nonces={};self.mode='ack';self.outcome=None;self.calls=0
 def send(self,rec,raw):
  self.calls+=1;s=rec['near_spec'];txid=rec['txid'];key=(s['signer'],s['public_key'],s['nonce'])
  if self.mode=='reject':raise Blocked('SIMULATED-REJECTION-NOT-FINAL')
  if self.mode=='timeout_before':raise TimeoutError('SIMULATED-TIMEOUT')
  if key in self.nonces and self.nonces[key]!=txid:raise Blocked('SIMULATED-NONCE-CONFLICT')
  self.nonces[key]=txid;self.seen.setdefault(txid,bytes(raw));need(self.seen[txid]==raw,'SIMULATOR-HASH-COLLISION')
  if self.mode=='ack_loss':raise TimeoutError('ACKNOWLEDGEMENT-LOST')
  return {'txid':('f'*64 if self.mode=='wrong_hash' else txid),'raw_sha256':sha(raw)}
 def lookup(self,rec,raw):return self.outcome
