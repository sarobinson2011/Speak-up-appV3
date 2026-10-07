"""Bounded computation caches. None of these objects establish qualification."""
import sys,sqlite3
from collections import OrderedDict
from pathlib import Path
from v4_ingest.records import require

def weight(v):
 if isinstance(v,(tuple,list)):return sys.getsizeof(v)+sum(weight(x) for x in v)
 if isinstance(v,dict):return sys.getsizeof(v)+sum(weight(k)+weight(x) for k,x in v.items())
 if hasattr(v,'cache_weight'):return v.cache_weight()
 return sys.getsizeof(v)

class ByteLRU:
 def __init__(self,limit=65536,entries=64):self.limit=limit;self.entries=entries;self.data=OrderedDict();self.bytes=0;self.peak=0;self.evictions=0
 def __len__(self):return len(self.data)
 def __contains__(self,k):return k in self.data
 def __getitem__(self,k):
  v,n=self.data.pop(k);self.data[k]=(v,n);return v
 def __setitem__(self,k,v):
  if k in self.data:self.bytes-=self.data.pop(k)[1]
  n=weight(k)+weight(v)+256
  if n>self.limit:return
  while self.data and (self.bytes+n>self.limit or len(self.data)>=self.entries):
   _,(_,size)=self.data.popitem(last=False);self.bytes-=size;self.evictions+=1
  self.data[k]=(v,n);self.bytes+=n;self.peak=max(self.peak,self.bytes)
 def clear(self):self.data.clear();self.bytes=0

class IndexPool:
 """At most four readonly SQLite connections. No live cursors across yields."""
 def __init__(self,owner,limit=4):self.owner=owner;self.limit=limit;self.data=OrderedDict();self.opens=0;self.evictions=0;self.peak=0
 def connection(self,doc):
  require(not self.owner.closed,'semantic store closed')
  key=doc.identity
  if key in self.data:
   db=self.data.pop(key);self.data[key]=db;return db
  if len(self.data)>=self.limit:self.data.popitem(last=False)[1].close();self.evictions+=1
  doc.verify_reopen()
  db=sqlite3.connect('file:'+str(doc.index_path)+'?mode=ro',uri=True)
  db.execute('pragma cache_size=-256');db.execute('pragma temp_store=file')
  self.data[key]=db;self.opens+=1;self.peak=max(self.peak,len(self.data));self.owner.observe();return db
 def close(self):
  for db in self.data.values():db.close()
  self.data.clear()

class Query:
 def __init__(self,doc,sql,args):self.doc,self.sql,self.args=doc,sql,args
 def fetchone(self):
  c=self.doc.owner.pool.connection(self.doc).execute(self.sql,self.args)
  try:return c.fetchone()
  finally:c.close()
 def __iter__(self):
  offset=0
  while True:
   c=self.doc.owner.pool.connection(self.doc).execute(self.sql+' LIMIT 64 OFFSET ?',(*self.args,offset))
   try:rows=c.fetchmany(64)
   finally:c.close()
   if not rows:return
   yield from rows;offset+=len(rows)
   if len(rows)<64:return
class ReadIndex:
 def __init__(self,doc):self.doc=doc
 def execute(self,sql,args=()):return Query(self.doc,sql,args)
 def close(self):pass

class BoundedLog:
 """Diagnostic tail only. All source invocation/trace checks still execute."""
 def __init__(self):self.cache=ByteLRU(65536,32);self.total=0
 def append(self,v):self.cache[self.total]=v;self.total+=1
 def __iter__(self):
  for v,_ in self.cache.data.values():yield v
 def __len__(self):return len(self.cache)
 def __getitem__(self,n):return list(self)[n]
