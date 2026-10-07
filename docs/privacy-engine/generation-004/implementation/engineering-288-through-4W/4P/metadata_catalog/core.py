"""Bounded canonical JSON-lines directories and exact authenticated index recovery.

Each row is capped at 64 KiB. This is a transport capability, not a new source law.
Complete canonical input identity is checked on every invocation. Partial indexes
are immutable generations, published before the small atomic MACed checkpoint.
"""
import hashlib,hmac,json,os,sqlite3,shutil,tempfile
from pathlib import Path
from collections.abc import Mapping
from v4_ingest.records import require,ValidationError
ROW=65536
FORMAT='CP4M-CATALOG-1'

def wire(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def sync(p):
 from link_recovery.cli import fsync_dir
 with Path(p).open('rb') as f:os.fsync(f.fileno())
 fsync_dir(Path(p).parent)

class DiskMap(dict):
 """Disk mapping. Read-only handles open per operation, never per retained row."""
 def __init__(self,path,readonly=False):
  self.path=Path(path);self.readonly=readonly;self.db=None
  if not readonly:
   self.db=self.connect();self.db.execute('create table if not exists entries(k text primary key,v blob not null) without rowid')
 def connect(self):
  db=sqlite3.connect(('file:'+str(self.path)+'?mode=ro') if self.readonly else str(self.path),uri=self.readonly)
  db.execute('pragma cache_size=-256');db.execute('pragma temp_store=file');return db
 def query(self,sql,args=()):
  db=self.connect() if self.readonly else self.db
  try:yield from db.execute(sql,args)
  finally:
   if self.readonly:db.close()
 def __len__(self):return next(self.query('select count(*) from entries'))[0]
 def __bool__(self):return len(self)>0
 def __iter__(self):
  for k, in self.query('select k from entries order by k'):yield k
 def __getitem__(self,k):
  r=next(self.query('select v from entries where k=?',(k,)),None)
  if r is None:raise KeyError(k)
  return json.loads(r[0])
 def __contains__(self,k):return next(self.query('select 1 from entries where k=?',(k,)),None) is not None
 def __setitem__(self,k,v):
  raw=wire(v);require(type(k) is str and len(k.encode())<=4096 and len(raw)<=ROW,'catalog row capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  self.db.execute('insert into entries values(?,?) on conflict(k) do update set v=excluded.v',(k,raw))
 def add(self,k,v):
  raw=wire(v);require(type(k) is str and len(k.encode())<=4096 and len(raw)<=ROW,'catalog row capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  try:self.db.execute('insert into entries values(?,?)',(k,raw))
  except sqlite3.IntegrityError:require(False,'duplicate/conflicting catalog key',category='INCOMPLETE-EVIDENCE-UNIVERSE')
 def get(self,k,default=None):
  try:return self[k]
  except KeyError:return default
 def keys(self):return iter(self)
 def items(self):
  for k,v in self.query('select k,v from entries order by k'):yield k,json.loads(v)
 def values(self):
  for _,v in self.items():yield v
 def __eq__(self,b):return isinstance(b,Mapping) and len(self)==len(b) and all(k in b and v==b[k] for k,v in self.items())
 def __ne__(self,b):return not self==b
 def close(self):
  if self.db is not None:self.db.close()
 def commit(self):self.db.commit()

def temporary(root,prefix='map'):
 fd,p=tempfile.mkstemp(prefix=prefix,suffix='.scratchdb',dir=root);os.close(fd);return DiskMap(p)

def write_directory(path,kind,binding,rows,count):
 """Rows supplied in strict key order; does not normalize/reorder an input."""
 path=Path(path);h=hashlib.sha256();n=0;last=None;seen=0
 with path.open('wb') as f:
  def put(v):
   nonlocal n
   b=wire(v);require(len(b)<=ROW,'catalog row capability',category='INCOMPLETE-EVIDENCE-UNIVERSE');f.write(b);h.update(b);n+=len(b)
  put({'format':FORMAT,'kind':kind,'binding':binding,'count':count})
  for k,v in rows:
   require(type(k) is str and (last is None or last<k),'strict unique catalog order');put([k,v]);last=k;seen+=1
  require(seen==count,'catalog count');f.flush();os.fsync(f.fileno())
 return {'path':path.name,'bytes':n,'sha256':h.hexdigest()}

def line(f):
 b=f.readline(ROW+1);require(b and len(b)<=ROW and b.endswith(b'\n'),'catalog framing/row capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
 try:v=json.loads(b)
 except (ValueError,RecursionError,UnicodeError) as e:raise ValidationError('catalog canonical JSON') from e
 require(wire(v)==b,'noncanonical/duplicate-key catalog JSON');return v

def acquire(path,entry,kind,binding,root,key,job,*,stop_after=None,tick=None,validate=None):
 """Resume only row boundaries. Full exact source reread precedes every resume.
 Complete DB generations are hashed before reuse; no file metadata identity.
 """
 from link_recovery.cli import atomic_save
 path=Path(path);root=Path(root);root.mkdir(parents=True,exist_ok=True)
 require(path.stat().st_size==entry['bytes'] and sha(path)==entry['sha256'],'changed catalog exact bytes',category='INVALID-EVIDENCE-DIGEST')
 identity={'file':entry,'kind':kind,'binding':binding,'job':job}
 label=hashlib.sha256(wire(identity)).hexdigest();ck=root/(label+'.json');old=None
 if ck.exists():
  raw=ck.read_bytes();require(len(raw)<=ROW,'catalog checkpoint capability');x=json.loads(raw);old=x['payload']
  require(hmac.compare_digest(x['hmac_sha256'],hmac.new(key,wire(old).rstrip(b'\n'),hashlib.sha256).hexdigest()),'corrupt catalog checkpoint')
  require(old['identity']==identity,'incompatible/substituted catalog checkpoint')
  p=root/old['database'];require(p.parent==root and sha(p)==old['database_sha256'],'corrupt catalog index',category='INVALID-EVIDENCE-DIGEST')
  if old['complete']:
   result=DiskMap(p,True);require(len(result)==old['count'],'catalog index count');return result
 db=temporary(root,'building-');seen=0;last=None;offset=0
 if old:
  db.close();shutil.copyfile(p,db.path);db=DiskMap(db.path);seen,last,offset=old['count'],old['last'],old['offset']
 try:
  with path.open('rb') as f:
   header=line(f);require(header=={'format':FORMAT,'kind':kind,'binding':binding,'count':header.get('count')},'catalog kind/exact binding',category='INVALID-ACTION-CONTEXT')
   require(type(header['count']) is int and header['count']>=0,'catalog count domain')
   if old:f.seek(offset)
   added=0
   while seen<header['count']:
    if tick:
     from integrated_auth.collector import Paused
     from link_recovery.cli import PauseRequested
     try:tick()
     except (Paused,PauseRequested):break
    row=line(f);require(type(row) is list and len(row)==2 and type(row[0]) is str,'catalog row')
    k,v=row;require(last is None or last<k,'duplicate/conflicting/incorrectly ordered catalog reference',category='INCOMPLETE-EVIDENCE-UNIVERSE')
    if validate:validate(k,v)
    db.add(k,v);seen+=1;added+=1;last=k
    if stop_after is not None and added>=stop_after:break
   complete=seen==header['count'];offset=f.tell()
   if complete:require(f.read(1)==b'','extra catalog rows/trailing bytes',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  # Recheck after consumption: journal/metadata never authenticate input bytes.
  require(sha(path)==entry['sha256'],'catalog changed during acquisition',category='INVALID-EVIDENCE-DIGEST')
  db.commit();db.close();dh=sha(db.path);dest=root/(dh+'.sqlite');os.replace(db.path,dest);sync(dest)
  record={'identity':identity,'database':dest.name,'database_sha256':dh,'count':seen,'last':last,'offset':offset,'complete':complete,'qualification_established':False}
  atomic_save(ck,record,key)
  if not complete:
   from integrated_auth.collector import Paused
   raise Paused()
  return DiskMap(dest,True)
 finally:
  try:db.close()
  finally:db.path.unlink(missing_ok=True)
