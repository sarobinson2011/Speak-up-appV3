"""Finite native occurrence/group consumer; no builder, expansion or ledger binding."""
import ast, copy, hashlib, json, stat, zipfile, argparse, sys
from pathlib import Path
from dataclasses import dataclass
COMPONENT_SHA='94791c65c3502d85fc452c0e9c100391f5d0199f7690462e92b91c1a600caa8b'
BUNDLE_SHA='e724e49952a6501ab45952416fdd422e9a989cf05f81b8e29254a50088b0a09b'
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
def trusted(archive):
 raw=regular(archive);need(len(raw)==45747644 and digest(raw)==COMPONENT_SHA,'COMPONENT-IDENTITY')
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();need(len(names)==60 and len(set(names))==60 and z.testzip() is None,'ZIP-INTEGRITY')
  m=parse(z.read('MANIFEST.json'));need(set(names)==set(m)|{'MANIFEST.json'},'MEMBERSHIP')
  for n,i in m.items():
   b=z.read(n);same({'bytes':len(b),'sha256':digest(b)},i,'MEMBER:'+n)
  b=z.read('outputs/bundle.json');need(digest(b)==BUNDLE_SHA,'REVIEWED-BUNDLE')
  return parse(b),parse(z.read('provenance/candidate-members.json'))
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

def sources(bundle,pins):
 root=Path(__file__).resolve().parents[1]/'sources';raw=regular(root/'expand_candidate.py')
 for name in ('expand_candidate.py','bind_ledger.py','prospective_procedure.py'):
  p=('compiler/' if name=='prospective_procedure.py' else 'native/code/')+name
  b=regular(root/name);same({'bytes':len(b),'sha256':digest(b)},pins[p],'SOURCE-IDENTITY:'+p)
 node=next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name=='pairs')
 need(digest(ast.dump(node,include_attributes=False).encode())==bundle['native_contract']['pure_consumer']['ast_sha256'],'PAIRS-AST')
 env={'need':need};exec(compile(ast.Module(body=[node],type_ignores=[]),'<pinned-pure-pairs>','exec'),env)
 return env['pairs']

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

def representation(bundle,contexts):
 return {'format':'I164-FINITE-NATIVE-REPRESENTATION-1','source_bundle_sha256':BUNDLE_SHA,'component_sha256':COMPONENT_SHA,
 'acquisition_id':bundle['acquisition_id'],'bindings':copy.deepcopy(bundle['bindings']),'native_contract':copy.deepcopy(bundle['native_contract']),
 'contexts':[{'context':c.name,'occurrences':[{'index':t.index,'key':list(t.key),'class':t.class_id,'payload_hex':t.payload.hex(),'metadata':parse(t.metadata)} for t in c.tokens],
 'groups':[{'range':parse(r),'rows':[list(x) for x in g.entries()]} for r,g in zip(c.ranges,c.groups)],
 'ordered_edges':[{'ordinal':o,'source_index':a,'target_index':b,'source_key':list(ka),'target_key':list(kb)} for o,a,b,ka,kb in c.edges],
 'duties':parse(c.duties)} for c in contexts],
 'obligations':copy.deepcopy(bundle['obligations']),'classification':'UNKNOWN','qualification':'UNAVAILABLE','assessment':'SOURCE-ONLY',
 'finite_consumer_acceptance':True,'complete_native_model':False,'ledger_rebound':False,'production_cardinalities':None,'global_lifetime_bound':None,
 'canonical_registration':False,'full_expansion_ready':False,'final_binding':'BLOCKED','stream_identities':'UNCOMPUTED','actual_admission':False,'backup':'KERNEL-ONLY'}
def run(archive,submitted=None):
 b,pins=trusted(archive);fn=sources(b,pins);native=construct(b,fn);expected=representation(b,native)
 if submitted is not None:same(submitted,expected,'NATIVE-REPRESENTATION-SUBSTITUTION')
 return expected

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--component',required=True,type=Path);ap.add_argument('--submitted',type=Path);ap.add_argument('--output',required=True,type=Path);a=ap.parse_args()
 need(not a.output.exists() and not str(a.output.resolve()).startswith('/tmp/'),'NEW-PERSISTENT-OUTPUT');a.output.mkdir(parents=True)
 def guard(event,args):
  if event=='sqlite3.connect':raise Rejected('NO-DATABASES')
 sys.addaudithook(guard)
 try:
  result=run(a.component,parse(regular(a.submitted)) if a.submitted else None)
  (a.output/'native.json').write_bytes(enc(result)+b'\n')
  summary={'status':'PASS finite native representation','contexts':[{'context':c['context'],'tokens':len(c['occurrences']),'groups':len(c['groups']),'ordered_edges':len(c['ordered_edges'])} for c in result['contexts']], 'obligations':11,'native_sha256':digest(regular(a.output/'native.json')),'final_binding':'BLOCKED','actual_admission':False}
  (a.output/'result.json').write_bytes(enc(summary)+b'\n');print(json.dumps(summary),flush=True)
 except BaseException:
  import traceback
  (a.output/'failure.txt').write_text(traceback.format_exc());raise
if __name__=='__main__':main()
