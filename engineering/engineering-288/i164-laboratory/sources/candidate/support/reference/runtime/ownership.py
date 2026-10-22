"""Shared permanent nonce ownership, OFFLINE LAB ONLY.
All participating writers must use the same ledger and guarded paths. Raw SQLite,
clones, external signatures and unregistered writers remain outside that assumption.
No existing signed record is migrated, rewritten, freed or renumbered.
"""
import sqlite3,json,secrets
from pathlib import Path
from anchor import enc,parse,sha,need,MAX_STATE,MAX_INTENT
from runtime import executor
FORMAT='I164-NONCE-OWNERSHIP-1'
MAX_COORDINATES=4096 # fail-closed local storage ceiling, not a new allowance

def attach(db,path):
 need(not db.in_transaction,'ATTACH-IN-TRANSACTION')
 db.execute('ATTACH DATABASE ? AS ownership',(str(Path(path).resolve()),))
 mode=db.execute('PRAGMA ownership.journal_mode=DELETE').fetchone()[0];need(mode=='delete','OWNERSHIP-JOURNAL')
 db.execute('PRAGMA ownership.synchronous=FULL')
 db.execute('BEGIN IMMEDIATE')
 try:
  db.execute('CREATE TABLE IF NOT EXISTS ownership.meta(id INTEGER PRIMARY KEY CHECK(id=1),raw BLOB NOT NULL)')
  db.execute('CREATE TABLE IF NOT EXISTS ownership.coordinates(coord TEXT PRIMARY KEY,raw BLOB NOT NULL,hash TEXT NOT NULL)')
  row=db.execute('SELECT raw FROM ownership.meta WHERE id=1').fetchone()
  if row is None:
   raw=enc({'format':FORMAT,'incarnation':secrets.token_hex(32)});db.execute('INSERT INTO ownership.meta VALUES(1,?)',(raw,));row=(raw,)
  meta=parse(row[0]);need(set(meta)=={'format','incarnation'} and meta['format']==FORMAT,'OWNERSHIP-VERSION')
  db.execute('COMMIT');return sha(row[0])
 except BaseException:
  db.execute('ROLLBACK');raise

def identity(chain,executor_address,nonce):return [chain,executor_address,str(nonce)]
def owner(kind,binding,u,intent):return sha(enc([kind,binding,u,intent]))
def row(db,chain,signer,nonce):
 coord=sha(enc(identity(chain,signer,nonce)));r=db.execute('SELECT raw,hash FROM ownership.coordinates WHERE coord=?',(coord,)).fetchone()
 if r is None:return None
 need(sha(r[0])==r[1],'OWNER-INTEGRITY');x=parse(r[0]);need(set(x)=={'coordinate','owner'} and enc(x['coordinate'])==enc(identity(chain,signer,nonce)),'OWNER-COORDINATE');return x

def require(db,chain,signer,nonce,who):
 x=row(db,chain,signer,nonce);need(x is not None and x['owner']==who,'NONCE-NOT-OWNED')

def claim(db,chain,signer,lo,hi,who):
 need(db.in_transaction and type(lo) is int and type(hi) is int and 0<=lo<=hi<2**256 and hi-lo<=86,'CLAIM-RANGE')
 for n in range(lo,hi+1):
  x=row(db,chain,signer,n)
  if x is not None:need(x['owner']==who,'NONCE-OWNED-BY-OTHER');continue
  need(db.execute('SELECT count(*) FROM ownership.coordinates').fetchone()[0]<MAX_COORDINATES,'OWNERSHIP-CAP')
  raw=enc({'coordinate':identity(chain,signer,n),'owner':who});db.execute('INSERT INTO ownership.coordinates VALUES(?,?,?)',(sha(enc(identity(chain,signer,n))),raw,sha(raw)))

class SignedCarrierGuard:
 """Additional storage guard for UNCHANGED retained Service/SimulatedBackend schema.
 Uses the original objects table in place. Both original objects and ownership
 claims commit in one SQLite multi-database transaction (DELETE/FULL journals).
 No historical job is copied into the prospective schema.
 """
 def __init__(self,path,descriptor,ownership_path):
  self.descriptor=dict(descriptor);self.db=sqlite3.connect(path,isolation_level=None,timeout=15)
  need(self.db.execute('PRAGMA journal_mode').fetchone()[0]=='delete','SIGNED-STORE-MUST-USE-DELETE')
  self.db.execute('PRAGMA synchronous=FULL');self.ledger=attach(self.db,ownership_path)
  self.db.execute('BEGIN IMMEDIATE')
  try:
   raw=self.get('HEAD');need(raw is not None,'EXISTING-SIGNED-HEAD-REQUIRED');self._claims(raw,{})
   self.db.execute('COMMIT')
  except BaseException:
   self.db.execute('ROLLBACK');self.db.close();raise
 def identity(self):return dict(self.descriptor)
 def get(self,k):
  r=self.db.execute('SELECT v FROM objects WHERE k=?',(k,)).fetchone();return r[0] if r else None
 def create(self,raw):raise ValueError('NO-HISTORICAL-RESET-OR-MIGRATION')
 def _claims(self,raw,puts):
  s=parse(raw,MAX_STATE)
  def blob(ref):
   key='BLOB/'+ref;b=puts.get(key) if key in puts else self.get(key);need(b is not None and sha(b)==ref,'SIGNED-BLOB');return b
  for u,v in s['u'].items():
   i,_=executor.validate_intent(u,blob(v['intent']));need(i.get('carrier')=='I164-SIGNED-ETHEREUM-LEGACY-1','SIGNED-CARRIER-ONLY')
   n=int(i['nonce']);need(v['nonce']==sha(enc([i['chain'],i['executor'],i['nonce']])),'SIGNED-RESERVATION')
   who=owner('signed-carrier',s['binding'],u,v['intent']);claim(self.db,i['chain'],i['executor'],n,n,who)
   if v.get('stage') is not None:
    st=v['stage'];message=blob(st['message']);count=(len(message)+511)//512;lo=n-count-2
    need(1<=count<=82 and lo>=0,'SIGNED-STAGE-SCHEDULE');claim(self.db,i['chain'],i['executor'],lo,n+1,who)
 def commit(self,old,new,puts,fault=None):
  if fault=='before':raise TimeoutError('SIMULATED-before-commit')
  self.db.execute('BEGIN IMMEDIATE')
  try:
   need(self.get('HEAD')==old,'CAS-CONFLICT');self._claims(old,{})
   # Detect all incoming reservations/schedules before accepting the HEAD/OP.
   self._claims(new,puts)
   for k,v in puts.items():self.db.execute('INSERT INTO objects VALUES(?,?)',(k,v))
   if fault=='partial':raise OSError('SIMULATED-crash-before-head')
   self.db.execute('UPDATE objects SET v=? WHERE k=?',(new,'HEAD'));self.db.execute('COMMIT')
  except BaseException:
   if self.db.in_transaction:self.db.execute('ROLLBACK')
   raise
  if fault=='ack_loss':raise TimeoutError('SIMULATED-commit-acknowledgement-lost')
 def close(self):self.db.close()
