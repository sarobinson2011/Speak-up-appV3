"""Bounded adaptation: selected reviewed pure functions; acceptance is in evaluate.py."""
import ast, copy, hashlib, json, stat, zipfile, argparse, sys
from pathlib import Path
from dataclasses import dataclass
CONTEXTS=('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')
class Rejected(ValueError):pass
def need(v,m):
 if not v:raise Rejected(m)
def enc(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def digest(b):return hashlib.sha256(b).hexdigest()
def parse(b):
 def pairs(items):
  out={}
  for k,v in items:need(k not in out,'DUPLICATE-KEY');out[k]=v
  return out
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(Rejected('NONFINITE')))
def same(a,b,m):need(enc(a)==enc(b),m)
def regular(p):
 p=Path(p);need(stat.S_ISREG(p.lstat().st_mode),'NONREGULAR');return p.read_bytes()
@dataclass(frozen=True)
class Occurrence:
 index:int
 key:tuple
 class_id:str
 payload:bytes
 metadata:bytes
@dataclass(frozen=True)
class Group:
 """Immutable realization of entries(), get(key), parts; source-role keys unique."""
 rows:tuple
 @property
 def parts(self):return ((0,self.rows,True),)
 def entries(self,prefix=None):
  need(prefix is None,'UNSUPPORTED-PREFIX');return iter(self.rows)
 def get(self,key):
  hits=[(i,new) for i,k,parent,new in self.rows if k==key]
  need(len(hits)==1,'UNIQUE-GROUP-KEY');return hits[0]
@dataclass(frozen=True)
class NativeContext:
 name:str
 tokens:tuple
 groups:tuple
 ranges:tuple
 edges:tuple
 duties:bytes
def construct(bundle,fn):
 same([c['context'] for c in bundle['contexts']],list(CONTEXTS),'CONTEXT-ORDER')
 need(len(bundle['obligations']['source_only'])==11,'OBLIGATIONS')
 result=[]
 for c in bundle['contexts']:
  ctx=c['context'];tokens=[];keys=set()
  for i,t in enumerate(c['tokens']):
   need(type(t['index']) is int and t['index']==i,'INDEX');need(t['key'][:2]==[bundle['acquisition_id'],ctx],'KEY-SCOPE')
   key=tuple(t['key']);need(key not in keys,'DUPLICATE-TOKEN');keys.add(key)
   payload=bytes.fromhex(t['exact_bytes_hex']);need(payload.hex()==t['exact_bytes_hex'],'CANONICAL-BYTES')
   tokens.append(Occurrence(i,key,t['class'],payload,enc(t)))
  groups=[];ranges=[];cursor=0
  for r in c['directory_ranges']:
   start,end=r['range'];need(type(start) is int and type(end) is int and start==cursor and start<=end<=len(tokens),'RANGE')
   selected=tokens[start:end];same([list(t.key) for t in selected],r['members'],'RANGE-MEMBERS')
   need(all(t.class_id==r['class'] for t in selected) and r['context']==ctx,'GROUP-CONTEXT-CLASS')
   groups.append(Group(tuple((t.index,enc(list(t.key)).decode(),None,True) for t in selected)))
   ranges.append(enc(r));cursor=end
  need(cursor==len(tokens),'RANGE-COVERAGE')
  edges=[];byordinal={}
  for p in c['structural_pairs']+c['semantic_pairs']:byordinal.setdefault(p['ordinal'],[]).append(p)
  ordinals=set()
  for step in c['lookup_steps']:
   ordinal=step['ordinal'];need(ordinal not in ordinals,'DUPLICATE-ORDINAL');ordinals.add(ordinal)
   need(step['context']==ctx and step['lookup_operator']=='PARENT-RECORD','PROSPECTIVE-KEYED-ONLY')
   sr=Group(tuple(tuple(r) for r in step['source_rows']));tr=Group(tuple(tuple(r) for r in step['target_rows']))
   for rows in (sr.rows,tr.rows):
    need(len({r[1] for r in rows})==len(rows),'DUPLICATE-WORK-KEY')
    for i,k,parent,new in rows:need(type(i) is int and 0<=i<len(tokens) and new is True,'WORK-ROW')
   for i,k,parent,new in tr.rows:need(k==enc(list(tokens[i].key)).decode(),'TARGET-KEY')
   for i,k,parent,new in sr.rows:
    oi,targetnew=tr.get(parent);same(parse(k),[ordinal,list(tokens[i].key),list(tokens[oi].key)],'SOURCE-EDGE-KEY')
   params={'rels':[{'from_node':'SOURCE','to_node':'TARGET'}],'rules':['PARENT-RECORD'],'details':[None],'groups':{('SOURCE',ctx):sr,('TARGET',ctx):tr},'old_rel_n':0}
   actual=list(fn(params,0,ctx));expected=[(p['from_index'],p['to_index']) for p in byordinal.get(ordinal,[])]
   same(actual,expected,'NATIVE-ENDPOINT-ORDER');need(len(actual)==step['count'],'RELATION-COUNT')
   for a,b in actual:edges.append((ordinal,a,b,tokens[a].key,tokens[b].key))
  need(len(edges)==sum(len(x) for x in byordinal.values()),'PAIR-CONSERVATION')
  result.append(NativeContext(ctx,tuple(tokens),tuple(groups),tuple(ranges),tuple(edges),enc({'mechanical':c['mechanical_duties'],'fold':c['fold_obligations'],'retained':c['retained_procedure_result']})))
 return tuple(result)
def representation(bundle,contexts,bundle_identity,component_identity):
 return {'format':'I164-FINITE-NATIVE-REPRESENTATION-1','source_bundle_sha256':bundle_identity['sha256'],'component_sha256':component_identity['sha256'],
 'acquisition_id':bundle['acquisition_id'],'bindings':copy.deepcopy(bundle['bindings']),'native_contract':copy.deepcopy(bundle['native_contract']),
 'contexts':[{'context':c.name,'occurrences':[{'index':t.index,'key':list(t.key),'class':t.class_id,'payload_hex':t.payload.hex(),'metadata':parse(t.metadata)} for t in c.tokens],
 'groups':[{'range':parse(r),'rows':[list(x) for x in g.entries()]} for r,g in zip(c.ranges,c.groups)],
 'ordered_edges':[{'ordinal':o,'source_index':a,'target_index':b,'source_key':list(ka),'target_key':list(kb)} for o,a,b,ka,kb in c.edges],
 'duties':parse(c.duties)} for c in contexts],
 'obligations':copy.deepcopy(bundle['obligations']),'classification':'UNKNOWN','qualification':'UNAVAILABLE','assessment':'SOURCE-ONLY',
 'finite_consumer_acceptance':True,'complete_native_model':False,'ledger_rebound':False,'production_cardinalities':None,'global_lifetime_bound':None,
 'canonical_registration':False,'full_expansion_ready':False,'final_binding':'BLOCKED','stream_identities':'UNCOMPUTED','actual_admission':False,'backup':'KERNEL-ONLY'}
