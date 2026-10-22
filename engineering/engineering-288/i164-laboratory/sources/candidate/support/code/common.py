"""Exact-byte primitives for OFFLINE correspondence. No signer or network."""
import json,hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION='I164-PROSPECTIVE-LAB-RETRY-3'
ZERO='0'*64
class Invalid(ValueError):pass
def need(x,m):
 if not x:raise Invalid(m)
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b,limit=3227648):
 need(type(b) is bytes and len(b)<=limit,'RAW-BOUND')
 def pairs(ps):
  d={}
  for k,v in ps:need(k not in d,'DUPLICATE-KEY');d[k]=v
  return d
 try:x=json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(Invalid('NONFINITE')))
 except (ValueError,UnicodeError) as e:raise Invalid('JSON') from e
 need(enc(x)==b,'CANONICAL-BYTES');return x
def keys(x,n):need(type(x) is dict and set(x)==set(n.split() if isinstance(n,str) else n),'FIELDS:'+str(n))
def integer(x,lo=0,hi=2**256-1):need(type(x) is int and lo<=x<=hi,'INTEGER');return x
def boolean(x):need(type(x) is bool,'BOOLEAN');return x
def text(x,hi=128):need(type(x) is str and 0<len(x)<=hi,'TEXT');return x
def hexbytes(x,size=None):
 need(type(x) is str and len(x)%2==0 and re.fullmatch('[0-9a-f]*',x) is not None,'HEX')
 b=bytes.fromhex(x);need(size is None or len(b)==size,'HEX-SIZE');return b
def digest(x):hexbytes(x,32);return x
def decimal(x):need(type(x) is str and re.fullmatch('0|[1-9][0-9]*',x) is not None and int(x)<2**256,'DECIMAL');return int(x)
def same(a,b,label):need(enc(a)==enc(b),label)
def pinned_sources():
 m=json.loads((ROOT/'reference/hashes.json').read_text())
 for n,h in m.items():need(sha((ROOT/n).read_bytes())==h,'SOURCE-IDENTITY:'+n)
 return m
