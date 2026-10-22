"""Versioned offline conditional executor. Immutable SQLite blobs; no real signer/RPC."""
import argparse,fcntl,hashlib,json,os,sqlite3,sys
from pathlib import Path
from abi import encode as abi_encode
VERSION='I164-DURABLE-EXECUTOR-PILOT-3-COMPARISON'
MAX_INPUT=262144
MAX_TRANSACTION=MAX_INPUT+2048
MAX_LOG=8192
MAX_ATTEMPTS=64
MAX_RECONCILIATION=2048

def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def u_wire(u):
 b=u.encode('utf-8');return sha(b'I164-PILOT-U-V1\0'+len(b).to_bytes(8,'big')+b)
class Blocked(ValueError):pass
def need(x,m):
 if not x:raise Blocked(m)
def parse(b,limit=MAX_INPUT):
 b=bytes(b);need(len(b)<=limit,'INPUT-LIMIT')
 def pairs(ps):
  d={}
  for k,v in ps:need(k not in d,'DUPLICATE-KEY');d[k]=v
  return d
 x=json.loads(b,object_pairs_hook=pairs);need(enc(x)==b,'NONCANONICAL');return x

def validate_intent(u,b):
 need(type(u) is str and 0<len(u)<=128,'U-IDENTITY')
 i=parse(b)
 keys={'chain','registry','executor','nonce','calldata_hex','value','gas_limit','config','decision','source','model','contract','profile','scope','key_epoch','method','arguments'}
 need(type(i) is dict and set(i)==keys,'INTENT-FIELDS')
 need(all(type(v) is str and 0<len(v)<=131072 for k,v in i.items() if k!='arguments'),'INTENT-VALUES')
 need(abi_encode(i['method'],i['arguments']).hex()==i['calldata_hex'],'ABI-BINDING')
 need(i['decision']==sha(enc(i['arguments']['d'])),'DECISION-BINDING')
 need(i['arguments']['d']['u']==u_wire(u),'U-BINDING')
 for k in ['chain','nonce','gas_limit','key_epoch']:
  v=i[k];need(v.isascii() and v.isdecimal() and str(int(v))==v and int(v)<2**256,'INTEGER-BINDING')
 for k in ['registry','executor']:
  v=i[k];need(len(v)==40 and all(c in '0123456789abcdef' for c in v),'ADDRESS-BINDING')
 for k in ['config','source','model','contract','profile','scope']:
  v=i[k];need(len(v)==64 and all(c in '0123456789abcdef' for c in v),'DIGEST-BINDING')
 need(len(i['calldata_hex'])%2==0 and all(c in '0123456789abcdef' for c in i['calldata_hex']),'CALLDATA')
 need(i['value']=='0','NONPAYABLE')
 tx=enc({'conditional_test_signature':'LAB-NOT-A-REAL-SIGNATURE','intent':i,'u':u})
 need(len(tx)<=MAX_TRANSACTION,'TRANSACTION-LIMIT')
 return i,tx

class Session:
 def __init__(self,path,job,create=False):
  self.path=Path(path);self.lock=open(str(path)+'.lock','a+b')
  try:fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:self.lock.close();raise Blocked('SINGLE-WRITER')
  try:
   need(self.path.exists()!=create,'EXISTS-OR-MISSING')
   need(type(job) is str and 0<len(job)<=128,'JOB-LIMIT')
   self.db=sqlite3.connect('file:'+str(self.path.resolve())+'?mode='+('rwc' if create else 'rw'),uri=True,isolation_level=None)
   self.db.execute('PRAGMA synchronous=FULL');self.db.execute('PRAGMA journal_mode=DELETE')
   root=Path(__file__).resolve().parents[1]
   files=['executor/session.py','executor/abi.py','contract/PetitionRegistryPilot.sol','contract/ABI.json','contract/method-identifiers.json']
   self.binding={'version':VERSION,'code':{n:sha((root/n).read_bytes()) for n in files},'job':job}
   if create:
    self.db.executescript('CREATE TABLE meta (v TEXT); CREATE TABLE log (seq INTEGER PRIMARY KEY,payload BLOB NOT NULL,digest TEXT NOT NULL); CREATE TABLE blobs (digest TEXT PRIMARY KEY,payload BLOB NOT NULL);')
    self.db.execute('INSERT INTO meta VALUES (?)',(enc(self.binding).decode(),));os.chmod(self.path,0o600)
    fd=os.open(str(self.path.parent),os.O_RDONLY);os.fsync(fd);os.close(fd)
   need(self.db.execute('PRAGMA integrity_check').fetchone()==('ok',),'CORRUPT-DB')
   need(self.db.execute('SELECT v FROM meta').fetchall()==[(enc(self.binding).decode(),)],'BINDING')
   self._reload()
  except BaseException:
   if hasattr(self,'db'):self.db.close()
   self.lock.close();raise
 def close(self):self.db.close();self.lock.close()
 def _blob(self,h,limit):
  row=self.db.execute('SELECT length(payload) FROM blobs WHERE digest=?',(h,)).fetchone()
  need(row is not None and row[0]<=limit,'BLOB-MISSING-OR-OVERSIZE')
  b=self.db.execute('SELECT payload FROM blobs WHERE digest=?',(h,)).fetchone()[0]
  need(type(b) is bytes and sha(b)==h,'BLOB-DIGEST');return b
 def _hydrate(self,u,r):
  need(set(r)<= {'status','intent_ref','tx_ref','reconciliation_ref','comparison_ref'} and {'status','intent_ref'}<=set(r),'RECORD-FIELDS')
  i,expected=validate_intent(u,self._blob(r['intent_ref'],MAX_INPUT))
  v={'status':r['status'],'intent':i,'intent_sha256':r['intent_ref']}
  if 'tx_ref' in r:
   raw=self._blob(r['tx_ref'],MAX_TRANSACTION)
   need(raw==expected,'EXACT-TRANSACTION-BINDING')
   v.update(synthetic_transaction_hex=raw.hex(),tx_sha256=r['tx_ref'])
  if 'reconciliation_ref' in r:
   e=parse(self._blob(r['reconciliation_ref'],MAX_RECONCILIATION),MAX_RECONCILIATION);self._check_evidence(v,e)
   need(r['status']==('SUCCESS' if e['outcome']=='SUCCESS' else 'FAILED'),'RESULT-BINDING');v['reconciliation']=e
  if 'comparison_ref' in r:
   e=parse(self._blob(r['comparison_ref'],MAX_INPUT));need(r['status']=='REJECTED' and e['u']==u and e['intent_sha256']==r['intent_ref'] and e['permit'] is False,'COMPARISON-REJECTION-BINDING');v['comparison_rejection']=e
  return v
 @staticmethod
 def _check_evidence(r,e):
  need(type(e) is dict and set(e)=={'conditional_fixture','tx_sha256','intent_sha256','outcome','finality','source'},'EVIDENCE-FIELDS')
  need(e['conditional_fixture'] is True and e['finality']=='LAB-FINAL' and e['source']=='LAB-ORACLE','NO-GENUINE-VERIFIER')
  need(e['tx_sha256']==r['tx_sha256'] and e['intent_sha256']==r['intent_sha256'],'WRONG-EVIDENCE')
  need(e['outcome'] in ['SUCCESS','REVERTED'],'UNRESOLVED')
 def _reload(self):
  latest={};head='0'*64;count=0;nonces=set()
  allowed={None:'RETIRED','RETIRED':('SEALED','REJECTED'),'SEALED':'UNCERTAIN','UNCERTAIN':('SUCCESS','FAILED')}
  for seq,size in self.db.execute('SELECT seq,length(payload) FROM log ORDER BY seq'):
   count+=1;need(count<=MAX_ATTEMPTS*4 and seq==count and size<=MAX_LOG,'LOG-BOUND')
   payload,h=self.db.execute('SELECT payload,digest FROM log WHERE seq=?',(seq,)).fetchone()
   x=parse(payload,MAX_LOG);need(set(x)=={'previous','u','record'} and x['previous']==head and h==sha(payload),'CORRUPT-HISTORY')
   u=x['u'];r=x['record'];prev=latest.get(u);status=r.get('status');a=allowed.get(prev['status'] if prev else None)
   need(status==a if type(a) is str else type(a) is tuple and status in a,'ILLEGAL-TRANSITION')
   need(set(r)==({'status','intent_ref'} if status=='RETIRED' else {'status','intent_ref','tx_ref'} if status in ['SEALED','UNCERTAIN'] else {'status','intent_ref','comparison_ref'} if status=='REJECTED' else {'status','intent_ref','tx_ref','reconciliation_ref'}),'STATE-FIELDS')
   if prev:
    need(r['intent_ref']==prev['intent_ref'] and ('tx_ref' not in prev or r['tx_ref']==prev['tx_ref']),'CHANGED-BINDING')
   hydrated=self._hydrate(u,r)
   if not prev:
    need(len(latest)<MAX_ATTEMPTS,'ATTEMPT-LIMIT');i=hydrated['intent'];nonce=(i['chain'],i['executor'],i['nonce']);need(nonce not in nonces,'NONCE-ALREADY-RESERVED');nonces.add(nonce)
   latest[u]=r;head=h
  self._latest=latest;self.head=head
 @property
 def states(self):
  self._reload();return {u:self._hydrate(u,r) for u,r in self._latest.items()}
 def _publish(self,u,r,blobs=()):
  # No caller reference is retained. BLOB and transition publication share a transaction.
  payload=enc({'previous':self.head,'u':u,'record':r});need(len(payload)<=MAX_LOG,'LOG-LIMIT')
  self.db.execute('BEGIN IMMEDIATE')
  try:
   for b in blobs:
    h=sha(b);row=self.db.execute('SELECT payload FROM blobs WHERE digest=?',(h,)).fetchone()
    need(row is None or row[0]==b,'BLOB-COLLISION')
    self.db.execute('INSERT OR IGNORE INTO blobs VALUES (?,?)',(h,sqlite3.Binary(b)))
   self.db.execute('INSERT INTO log(payload,digest) VALUES (?,?)',(payload,sha(payload)));self.db.execute('COMMIT')
  except BaseException:self.db.execute('ROLLBACK');raise
  self._reload()
 def retire(self,u,intent):
  # Freeze dicts and buffers before validating; accepted records own immutable exact bytes.
  b=enc(intent) if type(intent) is dict else bytes(intent);i,_=validate_intent(u,b)
  self._reload();need(u not in self._latest,'U-UNAVAILABLE');need(len(self._latest)<MAX_ATTEMPTS,'ATTEMPT-LIMIT')
  for v in self.states.values():
   j=v['intent'];need((j['chain'],j['executor'],j['nonce'])!=(i['chain'],i['executor'],i['nonce']),'NONCE-ALREADY-RESERVED')
  self._publish(u,{'status':'RETIRED','intent_ref':sha(b)},[b])
 def reject_comparison(self,u,result):
  self._reload();r=dict(self._latest[u]);need(r['status']=='RETIRED','NOT-RETIRED')
  e=parse(enc(result));need(e['u']==u and e['intent_sha256']==r['intent_ref'] and e['permit'] is False,'COMPARISON-REJECTION-BINDING')
  b=enc(e);r.update(status='REJECTED',comparison_ref=sha(b));self._publish(u,r,[b])
 def seal(self,u):
  self._reload();r=dict(self._latest[u]);need(r['status']=='RETIRED','NOT-RETIRED')
  intent,raw=validate_intent(u,self._blob(r['intent_ref'],MAX_INPUT))
  capsule=parse(bytes.fromhex(intent['arguments']['evidence']))
  need(capsule.get('format')=='I164-COMPUTED-COMPARISON-CAPSULE-1' and capsule.get('permit_for_conditional_test') is True,'COMPARISON-PREVENTS-SEAL')
  r.update(status='SEALED',tx_ref=sha(raw));self._publish(u,r,[raw])
 def submission(self,u):
  self._reload();r=dict(self._latest[u]);need(r['status']=='SEALED','SUBMISSION-PROHIBITED')
  v=self._hydrate(u,r);raw=bytes.fromhex(v['synthetic_transaction_hex'])
  r['status']='UNCERTAIN';self._publish(u,r)
  # Recheck persisted bytes after commit, before any release. Failure stays retired/uncertain.
  need(self._hydrate(u,self._latest[u])['synthetic_transaction_hex']==raw.hex(),'RELEASE-BINDING')
  return raw
 def reconcile(self,u,e):
  frozen=parse(enc(e),MAX_RECONCILIATION);self._reload();r=dict(self._latest[u]);need(r['status']=='UNCERTAIN','NOT-UNCERTAIN')
  self._check_evidence(self._hydrate(u,r),frozen);b=enc(frozen)
  r.update(status='SUCCESS' if frozen['outcome']=='SUCCESS' else 'FAILED',reconciliation_ref=sha(b));self._publish(u,r,[b])
 def status(self):
  self._reload();return {'head':self.head,'states':{u:{'status':r['status'],'intent_sha256':r['intent_ref']} for u,r in self._latest.items()},'actual_admission':False,'conditional_only':True}
 def backup(self,path):
  self._reload();dest=Path(path);need(not dest.exists(),'BACKUP-EXISTS');raw=self.path.read_bytes()
  with dest.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
  fd=os.open(str(dest.parent),os.O_RDONLY);os.fsync(fd);os.close(fd)
  return {'sha256':sha(raw),'head':self.head,'job':self.binding,'restore_requires_latest_external_head':True,'antirollback_established':False}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('action',choices=['init','status','retire','seal','submit-synthetic','reconcile-synthetic','backup']);a.add_argument('--db',required=True);a.add_argument('--job',required=True);a.add_argument('--u');a.add_argument('--input');a.add_argument('--output');a.add_argument('--expected-head');o=a.parse_args();s=None
 try:
  s=Session(o.db,o.job,create=o.action=='init')
  if o.expected_head:need(s.head==o.expected_head,'STALE-RESTORE')
  if o.action=='retire':
   with open(o.input,'rb') as f:b=f.read(MAX_INPUT+1)
   s.retire(o.u,b)
  if o.action=='seal':s.seal(o.u)
  if o.action=='submit-synthetic':s.submission(o.u)
  if o.action=='reconcile-synthetic':
   with open(o.input,'rb') as f:b=f.read(MAX_RECONCILIATION+1)
   s.reconcile(o.u,parse(b,MAX_RECONCILIATION))
  print(json.dumps(s.backup(o.output) if o.action=='backup' else s.status()))
 except Exception as e:print(json.dumps({'result':'BLOCKED','reason':str(e),'actual_admission':False}));sys.exit(2)
 finally:
  if s:s.close()
