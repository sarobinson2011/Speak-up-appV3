"""Bounded canonical owning bytes: S70 TSEV1 and S90 JSON+LF."""
import re
from v4_ingest.typed import Codec,ROOTS
from v4_ingest.records import require,primitive,parse
from semantic_stream.storage import Blob

def compare(a,b):
 # Exact unsigned lexicographic comparison; digest collisions are irrelevant.
 ia,ib=iter(a.chunks()),iter(b.chunks());x=y=b''
 while True:
  if not x:x=next(ia,b'')
  if not y:y=next(ib,b'')
  if not x or not y:return (bool(x)>bool(y))-(bool(x)<bool(y))
  n=min(len(x),len(y));u,v=x[:n],y[:n]
  if u!=v:return 1 if u>v else -1
  x,y=x[n:],y[n:]

class Reader:
 def __init__(self,blob):self.blob=blob;self.pos=0
 def take(self,n,cap=1048576):
  require(n<=cap,'typed scalar capability',category='INCOMPLETE-EVIDENCE-UNIVERSE');b=self.slice(n);return b.small(cap)
 def slice(self,n):
  require(0<=n<=len(self.blob)-self.pos,'truncated typed field');b=self.blob.slice(self.pos,n);self.pos+=n;return b
 def number(self,n):return int.from_bytes(self.take(n),'big')
 def end(self):require(self.pos==len(self.blob),'trailing typed octets')

def tse(blob,expected,types,depth=0):
 require(depth<=128,'typed nesting capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
 require(expected in types,'declared owning type');r=Reader(blob)
 require(r.take(5)==b'TSEV1','typed domain');require(r.take(r.number(4))==expected.encode('ascii'),'exact embedded type')
 tag=r.number(1);body=r.slice(r.number(8));r.end();kind,children=types[expected]
 if kind=='PRIMITIVE':
  require(tag==ROOTS[expected],'primitive kind')
  if expected=='PE-TSE-BYTES':return
  raw=body.small(1048576)
  if expected=='PE-TSE-BOOL3':require(raw in (b'\0',b'\1',b'\2'),'canonical BOOL3')
  elif expected=='PE-TSE-ID':
   try:value=raw.decode('ascii')
   except UnicodeError:require(False,'typed ID ASCII')
   primitive('ID',value);require(value!='PE-TSE-SET','reserved typed identifier')
  else:require(re.fullmatch(rb'0|[1-9][0-9]*',raw) is not None,'canonical UINT decimal')
 else:
  require(tag==(16 if kind=='SET' else 17),'derived kind');r=Reader(body);count=r.number(4)
  require(count<=(len(body)-4)//8,'possible derived count')
  if kind=='TUPLE':require(count==len(children),'tuple arity')
  prev=None
  for i in range(count):
   child=r.slice(r.number(8));tse(child,children[0] if kind=='SET' else children[i],types,depth+1)
   if kind=='SET' and prev is not None:require(compare(prev,child)<0,'strictly sorted distinct SET encodings')
   prev=child
  r.end()

def validate(blob,codec,type_id,derived,field_register):
 if codec=='TSEV1':
  require(all(row[0]!='PE-TSE-SET' for row in derived),'reserved type identifier')
  tse(blob,type_id,Codec(derived).types)
 elif codec=='S90-JSON-LF':
  value=parse(blob)
  if type_id.startswith('RECORD:'):
   from v4_ingest.records import validate_record
   validate_record(type_id[7:],value,field_register=field_register)
  else:primitive(type_id,value,field_register=field_register)
 else:require(False,'unsupported owning byte codec',category='INCOMPLETE-EVIDENCE-UNIVERSE')
