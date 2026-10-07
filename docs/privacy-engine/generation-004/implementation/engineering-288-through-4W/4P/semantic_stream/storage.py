"""Private exact-byte spools and disk JSON index. No stored PASS is trusted.

All offsets refer to consumed, privately copied bytes. JSON structures are lazy;
large hex values never become Python strings. SQLite cache and lexical buffers
are capped. Indexes are disposable; CP4K reuses complete indexes only through exact-byte
checks and authenticated trusted-executor receipts.
"""
import contextvars,hashlib,json,os,re,sqlite3,tempfile
from pathlib import Path
from collections.abc import Mapping,Sequence
ACTIVE=contextvars.ContextVar('semantic_store',default=None)
CHUNK=65536
SMALL=65536
STRING_LIMIT=1048576
DEPTH=128

def require(v,msg):
 from v4_ingest.records import require as check
 check(v,msg,category='INCOMPLETE-EVIDENCE-UNIVERSE' if 'capability' in msg else 'INVALID-PROFILE-SCHEMA')

class Blob:
 def __init__(self,store,path,start=0,size=None,guard=None):
  self.store,self.path,self.start=store,Path(path),start;self.guard=guard;self.size=self.path.stat().st_size-start if size is None else size
 def cache_weight(self):return 256+len(str(self.path).encode())
 def __len__(self):return self.size
 def exact_sha(self):
  h=hashlib.sha256()
  for b in self.chunks():h.update(b)
  return h.hexdigest()
 def chunks(self):
  if self.guard:self.guard()
  with self.path.open('rb') as f:
   f.seek(self.start);left=self.size
   while left:
    if getattr(self.store,'tick',None):self.store.tick()
    b=f.read(min(CHUNK,left));require(b,'truncated private spool');left-=len(b);yield b
 def small(self,cap=STRING_LIMIT):
  require(self.size<=cap,'individual value capability exceeded');return b''.join(self.chunks())
 def slice(self,start,size):
  require(0<=start<=len(self) and 0<=size<=len(self)-start,'truncated byte slice');return Blob(self.store,self.path,self.start+start,size,self.guard)
 def sha(self):
  if self.guard:self.guard()
  from recovery_schedule.state import ACTIVE as SCHEDULE
  scheduler=SCHEDULE.get();key=(str(self.path),self.start,self.size)
  if scheduler is not None and key in scheduler.range_hashes:return scheduler.range_hashes[key]
  h=hashlib.sha256()
  for b in self.chunks():h.update(b)
  result=h.hexdigest()
  if scheduler is not None:scheduler.range_hashes[key]=result
  return result
 def hex(self):return Hex(self)
 def __eq__(self,other):
  if isinstance(other,bytes):other=Memory(other)
  if not isinstance(other,(Blob,Memory)) or len(self)!=len(other):return False
  return equal_chunks(self.chunks(),other.chunks())
 def __ne__(self,other):return not self==other

class Memory:
 def __init__(self,b):self.b=b
 def __len__(self):return len(self.b)
 def chunks(self):
  for i in range(0,len(self.b),CHUNK):yield self.b[i:i+CHUNK]

def equal_chunks(a,b):
 a,b=iter(a),iter(b);x=y=b''
 while True:
  if not x:x=next(a,b'')
  if not y:y=next(b,b'')
  if not x or not y:return x==y
  n=min(len(x),len(y))
  if x[:n]!=y[:n]:return False
  x,y=x[n:],y[n:]

class Hex:
 def __init__(self,blob,encoded=False):self.blob,self.encoded=blob,encoded
 def __len__(self):return len(self.blob) if self.encoded else 2*len(self.blob)
 def chunks(self):
  for b in self.blob.chunks():yield b if self.encoded else b.hex().encode('ascii')
 def octets(self):
  if not self.encoded:return self.blob
  def parts():
   pending=b''
   for b in self.chunks():
    b=pending+b;n=len(b)//2*2
    yield bytes.fromhex(b[:n].decode('ascii'));pending=b[n:]
   require(not pending,'odd hex')
  return self.blob.store.write(parts())
 def __eq__(self,other):
  if isinstance(other,str):return len(self)==len(other) and equal_chunks(self.chunks(),Memory(other.encode()).chunks())
  return isinstance(other,Hex) and len(self)==len(other) and equal_chunks(self.chunks(),other.chunks())
 def __ne__(self,other):return not self==other

def unhex(v):return v.octets() if isinstance(v,Hex) else bytes.fromhex(v)

def encode(value):
 if isinstance(value,Node):yield from value.raw().chunks()
 elif isinstance(value,Hex):
  yield b'"';yield from value.chunks();yield b'"'
 elif isinstance(value,dict):
  yield b'{'
  for i,k in enumerate(value if hasattr(value,'db') else sorted(value)):
   if i:yield b','
   yield json.dumps(k,ensure_ascii=True).encode();yield b':';yield from encode(value[k])
  yield b'}'
 elif isinstance(value,(list,tuple)):
  yield b'['
  for i,v in enumerate(value):
   if i:yield b','
   yield from encode(v)
  yield b']'
 else:yield json.dumps(value,ensure_ascii=True,allow_nan=False,separators=(',',':')).encode('ascii')

def canonical(value):
 store=ACTIVE.get()
 if store is None:
  if isinstance(value,Node):store=value.store
  elif isinstance(value,Hex):store=value.blob.store
 require(store is not None,'active semantic store required')
 def chunks():yield from encode(value);yield b'\n'
 return store.write(chunks())

class Node:
 def __init__(self,store,n,start,end,count):self.store,self.n,self.start,self.end,self.count=store,n,start,end,count
 def raw(self):return self.store.bound_slice(self.start,self.end-self.start)
 def __len__(self):return self.count
 def __bool__(self):return bool(self.count)
 def __eq__(self,other):
  if isinstance(self,JDict):
   return isinstance(other,(dict,JDict)) and len(self)==len(other) and all(k in other and v==other[k] for k,v in self.items())
  return isinstance(other,(list,JList)) and len(self)==len(other) and all(x==y for x,y in zip(self,other))
 def __ne__(self,other):return not self==other
class JDict(Node,dict):
 def __iter__(self):
  for k, in self.store.db.execute('select key from children where parent=? order by ordinal',(self.n,)):yield k
 def __getitem__(self,k):
  row=self.store.db.execute('select child from children where parent=? and key=?',(self.n,k)).fetchone()
  if row is None:raise KeyError(k)
  return self.store.value(row[0])
 def __contains__(self,k):return self.store.db.execute('select 1 from children where parent=? and key=?',(self.n,k)).fetchone() is not None
 def get(self,k,d=None):
  try:return self[k]
  except KeyError:return d
 def keys(self):return iter(self)
 def items(self):
  for k,n in self.store.db.execute('select key,child from children where parent=? order by ordinal',(self.n,)):yield k,self.store.value(n)
 def values(self):
  for _,v in self.items():yield v
class JList(Node,list):
 def __iter__(self):
  for n, in self.store.db.execute('select child from children where parent=? order by ordinal',(self.n,)):yield self.store.value(n)
 def __getitem__(self,k):
  if isinstance(k,slice):return [self[i] for i in range(*k.indices(len(self)))]
  if k<0:k+=len(self)
  row=self.store.db.execute('select child from children where parent=? and ordinal=?',(self.n,k)).fetchone()
  if row is None:raise IndexError(k)
  return self.store.value(row[0])
 def __contains__(self,v):return any(x==v for x in self)

class Store:
 def __init__(self,directory=None,tick=None):
  self.tmp=tempfile.TemporaryDirectory(prefix='semantic-4n-',dir=directory);self.root=Path(self.tmp.name);self.count=0;self.docs=[];self.tick=tick;self.closed=False
  from metadata_catalog.core import DiskMap
  from .lifetime import IndexPool
  self.parsed=DiskMap(self.root/'locators.sqlite');self.pool=IndexPool(self);self.last_document=None;self.instance=__import__('uuid').uuid4().hex;self.peak_fds=0;self.documents_built=0;self.documents_reused=0
  from integrated_auth.collector import implementation
  from recovery_schedule.state import ACTIVE as SCHEDULE
  schedule=SCHEDULE.get()
  self.binding=hashlib.sha256(json.dumps({'implementation':implementation(),'job':schedule.binding if schedule is not None else None},sort_keys=True).encode()).hexdigest()
 def observe(self):
  try:self.peak_fds=max(self.peak_fds,len(os.listdir('/proc/self/fd')))
  except OSError:pass
 def metrics(self):return {'documents_built':self.documents_built,'documents_reused':self.documents_reused,'open_index_limit':self.pool.limit,'peak_open_indexes':self.pool.peak,'index_reopens':self.pool.opens,'index_evictions':self.pool.evictions,'index_sqlite_cache_budget_bytes':self.pool.limit*262144,'observed_peak_process_fds':self.peak_fds,'parsed_value_cache_bytes':0,'locator_sqlite_cache_budget_bytes':262144}
 def close(self):
  if self.closed:return
  self.closed=True
  try:
   self.pool.close();self.parsed.close()
   for d in self.docs:
    if hasattr(d,'close'):d.close()
    else:d.db.close()
   self.docs.clear();self.last_document=None
  finally:self.tmp.cleanup()
 def path(self,prefix='blob'):
  require(not self.closed,'semantic store closed');p=self.root/(prefix+'-'+str(self.count));self.count+=1;return p
 def write(self,parts):
  p=self.path()
  try:
   with p.open('wb') as f:
    self.observe()
    for b in parts:
     if self.tick:self.tick()
     f.write(b)
   return Blob(self,p)
  except BaseException:p.unlink(missing_ok=True);raise
 def parse(self,blob):
  require(not self.closed,'semantic store closed')
  key=hashlib.sha256(json.dumps((str(blob.path),blob.start,len(blob))).encode()).hexdigest()
  if key in self.parsed:
   info=self.parsed[key];d=Document.reopen(self,blob,info);self.documents_reused+=1
   # Even a small materialized root requires exact reopening checks.
   self.pool.connection(d);return d.value(0)
  def original(store,b):
   d=Document(store,b);store.last_document=d
   try:return d.parse()
   except BaseException:d.abort();raise
  from recovery_schedule.index import parse as scheduled_parse
  result=scheduled_parse(self,blob,original);d=self.last_document
  self.parsed[key]=d.descriptor();return result

class Document:
 def __init__(self,owner,blob):
  self.owner=owner;self.document=blob;self.root=owner.root;self.tick=owner.tick
  self.index_path=owner.path('index');self.db=sqlite3.connect(self.index_path);self.complete=False;owner.observe()
  self.db.executescript('pragma journal_mode=off; pragma synchronous=off; pragma cache_size=-256; pragma temp_store=file; create table nodes(id integer primary key,kind text,start integer,end integer,count integer);create table children(parent integer,ordinal integer,key text,child integer,primary key(parent,ordinal));create unique index keys on children(parent,key);')
  self.next=0
 def bound_slice(self,start,size):
  blob=self.document.slice(start,size);blob.guard=lambda:self.owner.pool.connection(self);return blob
 def descriptor(self):return {'index':str(self.index_path),'index_sha256':self.index_sha,'input_sha256':self.input_sha,'input_path':str(self.document.path),'start':self.document.start,'size':len(self.document),'binding':self.binding,'receipt':self.receipt,'owner_instance':self.owner.instance}
 @classmethod
 def reopen(cls,owner,blob,info):
  require(info['owner_instance']==owner.instance and info['binding']==owner.binding and (info['input_path'],info['start'],info['size'])==(str(blob.path),blob.start,len(blob)),'stale/cross-object semantic index')
  d=object.__new__(cls);d.owner=owner;d.document=blob;d.root=owner.root;d.tick=owner.tick;d.index_path=Path(info['index']);d.input_sha=info['input_sha256'];d.index_sha=info['index_sha256'];d.binding=info['binding'];d.receipt=info['receipt'];d.complete=True
  d.identity=hashlib.sha256(json.dumps(info,sort_keys=True).encode()).hexdigest()
  from .lifetime import ReadIndex
  d.db=ReadIndex(d);owner.last_document=d;return d
 def verify_reopen(self):
  require(self.binding==self.owner.binding,'incompatible semantic implementation')
  from recovery_schedule.state import sha,ACTIVE as SCHEDULE
  require(self.document.exact_sha()==self.input_sha,'changed exact semantic snapshot')
  require(sha(self.index_path)==self.index_sha,'changed exact semantic index')
  if self.receipt:
   scheduler=SCHEDULE.get();require(scheduler is not None,'semantic receipt execution context absent')
   old=scheduler.read(self.receipt)
   require(old is not None and old['complete'] and old['inputs']=={'sha256':self.input_sha,'bytes':len(self.document)} and old['artifacts'].get(str(self.index_path))==self.index_sha,'stale/substituted semantic receipt')
 def abort(self):
  if not self.complete:self.db.close();self.index_path.unlink(missing_ok=True)
 def write(self,parts):return self.owner.write(parts)
 def value(self,n):
  if self.tick:self.tick()
  kind,start,end,count=self.db.execute('select kind,start,end,count from nodes where id=?',(n,)).fetchone();raw=self.document.slice(start,end-start)
  if end-start<=SMALL:return json.loads(raw.small(SMALL))
  if kind=='hex' and end-start<=STRING_LIMIT+2:return json.loads(raw.small(STRING_LIMIT+2))
  if kind=='hex':return Hex(self.bound_slice(start+1,end-start-2),True)
  if kind=='dict':return JDict(self,n,start,end,count)
  if kind=='list':return JList(self,n,start,end,count)
  require(False,'individual record scalar capability')
 def parse(self):
  with self.document.path.open('rb') as f:
   f.seek(self.document.start);self.reader=Cursor(f,len(self.document),self.tick)
   n=self.node(0);require(self.reader.take(1)==b'\n' and self.reader.pos==len(self.document),'exact terminal JSON LF/no trailing bytes')
  self.db.commit();self.db.close();self.complete=True
  from recovery_schedule.state import sha
  self.input_sha=self.document.exact_sha();self.index_sha=sha(self.index_path);self.binding=self.owner.binding;self.receipt=None
  self.identity=hashlib.sha256(json.dumps(self.descriptor(),sort_keys=True).encode()).hexdigest()
  from .lifetime import ReadIndex
  self.db=ReadIndex(self);self.reader=None;self.owner.documents_built+=1
  return self.value(n)
 def node(self,depth):
  require(depth<=DEPTH,'nesting capability exceeded');r=self.reader;start=r.pos;c=r.peek();n=self.next;self.next+=1;count=0
  if c in (b'{',b'['):
   require(depth<DEPTH,'nesting capability exceeded')
   kind='dict' if c==b'{' else 'list';close=b'}' if c==b'{' else b']';r.take(1);last=None
   if r.peek()!=close:
    while True:
     key=None
     if kind=='dict':
      key=self.string(key=True);require(last is None or last<key,'canonical strictly sorted unique object keys');last=key;require(r.take(1)==b':','object colon')
     child=self.node(depth+1);self.db.execute('insert into children values(?,?,?,?)',(n,count,key,child));count+=1
     if r.peek()==close:break
     require(r.take(1)==b',','array/object comma')
   r.take(1)
  elif c==b'"':
   self.string();kind='hex' # large strings only survive if exact even hex
  else:
   b=bytearray()
   while r.peek() and r.peek() not in (b',',b']',b'}',b'\n'):
    require(len(b)<4096,'number capability exceeded');b.extend(r.take(1))
   raw=bytes(b)
   require(raw in (b'true',b'false',b'null') or re.fullmatch(rb'(?:0|-[1-9][0-9]*|[1-9][0-9]*)',raw),'canonical integer/bool/null required')
   kind='scalar'
  self.db.execute('insert into nodes values(?,?,?,?,?)',(n,kind,start,r.pos,count));return n
 def string(self,key=False):
  r=self.reader;require(r.take(1)==b'"','JSON string expected');start=r.pos;small=bytearray();hexok=True;escaped=False
  # Scan entire safe runs in C, never byte-loop through invocation hex.
  while True:
   chunk=r.window();require(chunk,'unterminated JSON string')
   m=re.search(rb'["\\\x00-\x1f\x7f-\xff]',chunk);n=m.start() if m else len(chunk)
   if n:
    b=r.take(n);hexok=hexok and re.fullmatch(rb'[0-9a-f]*',b) is not None
    if len(small)+len(b)<=STRING_LIMIT:small.extend(b)
    else:require(hexok and not key,'string capability exceeded')
   c=r.take(1) if m else None
   if c==b'"':break
   if c==b'\\':
    hexok=False;escaped=True;require(r.pos-start<STRING_LIMIT,'escaped string capability exceeded');small.extend(c);small.extend(r.take(1))
   elif c is not None:require(False,'non-ASCII/control JSON string')
  length=r.pos-start-1
  if length<=STRING_LIMIT:
   raw=b'"'+bytes(small)+b'"'
   try:v=json.loads(raw)
   except (ValueError,UnicodeError):require(False,'malformed JSON string')
   require(json.dumps(v,ensure_ascii=True,separators=(',',':')).encode()==raw,'noncanonical JSON string')
   return v if key else None
  require(hexok and not escaped and length%2==0,'large string must be canonical even hex; capability exceeded')
  return None

class Cursor:
 def __init__(self,f,size,tick):self.f,self.size,self.tick=f,size,tick;self.pos=0;self.buf=b'';self.off=0
 def window(self):
  if self.off==len(self.buf):
   if self.tick:self.tick()
   self.buf=self.f.read(min(CHUNK,self.size-self.pos));self.off=0
  return self.buf[self.off:]
 def peek(self):return self.window()[:1]
 def take(self,n):
  out=bytearray()
  while n:
   b=self.window();require(b,'truncated JSON');k=min(n,len(b));out.extend(b[:k]);self.off+=k;self.pos+=k;n-=k
  return bytes(out)
