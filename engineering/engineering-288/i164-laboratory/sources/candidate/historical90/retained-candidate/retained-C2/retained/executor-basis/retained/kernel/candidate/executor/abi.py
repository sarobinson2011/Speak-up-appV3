"""Bounded canonical ABI encoder for this candidate's two signing entry points.
Selectors are compiler output, not SHA3 substitutes. No arbitrary ABI support.
"""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Immutable byte snapshots: never reopen mutable ABI files during encoding.
ABI_BYTES=(ROOT/'contract/ABI.json').read_bytes()
SELECTOR_BYTES=(ROOT/'contract/method-identifiers.json').read_bytes()
def word(n):
 if type(n) is not int or not 0<=n<2**256:raise ValueError('uint256')
 return n.to_bytes(32,'big')
def static(t,v,components=None):
 m=re.fullmatch(r'(.*)\[(\d+)\]',t)
 if m:
  if type(v) is not list or len(v)!=int(m[2]):raise ValueError('array')
  return b''.join(static(m[1],x) for x in v)
 if t=='uint256':return word(v)
 if t=='bytes32':
  if type(v) is not str or not re.fullmatch('[0-9a-f]{64}',v):raise ValueError('bytes32')
  return bytes.fromhex(v)
 if t=='tuple':
  if type(v) is not dict or set(v)!={c['name'] for c in components}:raise ValueError('tuple')
  return b''.join(static(c['type'],v[c['name']],c.get('components')) for c in components)
 raise ValueError('unsupported type')
def canonical_type(x):
 return '('+','.join(canonical_type(c) for c in x['components'])+')' if x['type']=='tuple' else x['type']
def encode(method,values):
 if method not in ('signPetition','signPetitionWithZKProof'):raise ValueError('method')
 abi=json.loads(ABI_BYTES);f=next(x for x in abi if x.get('name')==method and x['type']=='function')
 if type(values) is not dict or set(values)!={c['name'] for c in f['inputs']}:raise ValueError('fields')
 signature=method+'('+','.join(canonical_type(c) for c in f['inputs'])+')'
 selector=bytes.fromhex(json.loads(SELECTOR_BYTES)[signature])
 parts=[]
 for c in f['inputs']:
  v=values[c['name']]
  if c['type']=='bytes':
   if type(v) is not str or not re.fullmatch('(?:[0-9a-f]{2})*',v) or len(v)>131072:raise ValueError('bytes bound')
   b=bytes.fromhex(v);parts.append((False,word(len(b))+b+b'\0'*((-len(b))%32)))
  else:parts.append((True,static(c['type'],v,c.get('components'))))
 offset=sum(len(b) if s else 32 for s,b in parts);head=[];tail=[]
 for s,b in parts:
  if s:head.append(b)
  else:head.append(word(offset));tail.append(b);offset+=len(b)
 result=selector+b''.join(head+tail)
 if len(result)>262144:raise ValueError('call bound')
 return result


def decode(method,raw):
 """Decode the two exact candidate forms; roundtrip detects offsets/padding/trailing bytes."""
 if type(raw) is not bytes or len(raw)>70148 or len(raw)<4:raise ValueError('invocation bound')
 if method not in ('signPetition','signPetitionWithZKProof'):raise ValueError('method')
 fields=next(x['inputs'] for x in json.loads(ABI_BYTES) if x.get('name')==method)
 data=raw[4:]
 def value(f,pos):
  t=f['type']
  if t=='tuple':
   out={}
   for c in f['components']:out[c['name']],pos=value(c,pos)
   return out,pos
  m=re.fullmatch(r'(.*)\[(\d+)\]',t)
  if m:
   out=[]
   for _ in range(int(m[2])):v,pos=value({'type':m[1]},pos);out.append(v)
   return out,pos
  b=data[pos:pos+32]
  if len(b)!=32:raise ValueError('truncated word')
  if t=='uint256':return int.from_bytes(b,'big'),pos+32
  if t=='bytes32':return b.hex(),pos+32
  if t=='bytes':
   off=int.from_bytes(b,'big')
   if off+32>len(data):raise ValueError('offset')
   n=int.from_bytes(data[off:off+32],'big')
   if n>65536 or off+32+n>len(data):raise ValueError('dynamic bound')
   return data[off+32:off+32+n].hex(),pos+32
  raise ValueError('unsupported type')
 out={};pos=0
 for f in fields:out[f['name']],pos=value(f,pos)
 if encode(method,out)!=raw:raise ValueError('noncanonical invocation')
 if method=='signPetition' and len(out['authData'])>8192:raise ValueError('pilot authData bound')
 return out
