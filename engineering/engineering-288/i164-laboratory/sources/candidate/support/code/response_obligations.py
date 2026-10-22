"""Bounded AST-to-response obligations, independent of schemas()/template catalogue.
Not a Python verifier: unsupported source shapes fail closed. Never executes runtime.
Record names are local binding aliases; keys/dispatch/returns come from pinned source.
"""
import ast
from common import *
S='STRING';I='INTEGER';B='BOOLEAN';N='NULL'
QUALIFIED_SOURCES={'reference/runtime/authority.py': '4565bb30cb637b3cef40a3f1da2b3722840b747ab110fa37eede0cbc2e3b313a', 'reference/runtime/accounting.py': '7c344469895db20062380e60ad60e055e6fc5121a167720bc64162f2e8aa26cc'}
def ref(n):return {'ref':n}
def nullable(t):return {'union':[N,t]}
def directory(t):return {'directory':t,'key_type':S}
def shape_fail(label):raise Invalid('SOURCE-RESPONSE-SHAPE:'+label)
def source_obligations():
 pinned_sources();trees={};texts={};anchors=[]
 for n,h in QUALIFIED_SOURCES.items():need(sha((ROOT/n).read_bytes())==h,'UNQUALIFIED-RESPONSE-SOURCE:'+n)
 for f in ['reference/runtime/authority.py','reference/runtime/accounting.py']:
  texts[f]=(ROOT/f).read_text();trees[f]=ast.parse(texts[f])
 path='reference/runtime/authority.py';tree=trees[path]
 authority=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Authority');functions={n.name:n for n in authority.body if isinstance(n,ast.FunctionDef)}
 def anchor(node,source=path):
  a={'source':source,'sha256':sha((ROOT/source).read_bytes()),'line':node.lineno,'end_line':node.end_lineno,'expression':ast.get_source_segment(texts[source],node)}
  if a not in anchors:anchors.append(a)
  return a
 def dict_fields(node):
  need(isinstance(node,ast.Dict) and all(isinstance(k,ast.Constant) and type(k.value) is str for k in node.keys),'SOURCE-RESPONSE-DICT')
  names=[k.value for k in node.keys];need(len(names)==len(set(names)),'SOURCE-DUPLICATE-FIELD');return dict(zip(names,node.values))
 def assignments(target,source=path):
  return [n for n in ast.walk(trees[source]) if isinstance(n,ast.Assign) and any(ast.unparse(t)==target for t in n.targets)]
 def constructor(target,source=path):
  nodes=[n for n in assignments(target,source) if isinstance(n.value,ast.Dict)];need(nodes,'SOURCE-CONSTRUCTOR:'+target)
  shapes=[dict_fields(n.value) for n in nodes];need(all(set(x)==set(shapes[0]) for x in shapes),'SOURCE-CONSTRUCTOR-VARIANTS:'+target)
  for n in nodes:anchor(n,source)
  return nodes[0].value
 def primitive(node):
  if isinstance(node,ast.Constant):
   t={str:S,int:I,bool:B,type(None):N}.get(type(node.value));need(t is not None,'SOURCE-CONSTANT');return t
  if isinstance(node,ast.IfExp):
   a,b=primitive(node.body),primitive(node.orelse);need(a==b,'SOURCE-IF-TYPE');return a
  if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Mult) and isinstance(node.left,ast.Constant) and type(node.left.value) is str:return S
  if isinstance(node,ast.Call):
   if isinstance(node.func,ast.Name) and node.func.id in ['len','int']:return I
   if isinstance(node.func,ast.Name) and node.func.id in ['sha','str']:return S
   if isinstance(node.func,ast.Attribute) and node.func.attr in ['hex','hexdigest','blob']:return S
  if isinstance(node,ast.Name) and node.id in ['n']:return I
  if isinstance(node,ast.Name) and node.id in ['a','a_id','attempt','sid','proof','classification','reservation']:return S
  if isinstance(node,ast.Subscript) or isinstance(node,ast.Attribute):return S
  shape_fail(ast.unparse(node))
 def fields(node,overrides=None):
  d=dict_fields(node);overrides=overrides or {};need(set(overrides)<=set(d),'SOURCE-OVERRIDE-MISSING')
  return {k:overrides[k] if k in overrides else primitive(v) for k,v in d.items()}
 # Dispatch comes from top-level apply method predicates, not BODIES or schemas.
 apply=functions['apply'];branches={}
 def method_test(node):
  if isinstance(node,ast.Compare) and ast.unparse(node.left)=='m' and len(node.ops)==1 and isinstance(node.ops[0],ast.Eq) and isinstance(node.comparators[0],ast.Constant) and type(node.comparators[0].value) is str:return node.comparators[0].value
 def chain(node):
  m=method_test(node.test);need(m is not None and m not in branches,'SOURCE-METHOD-DISPATCH');branches[m]=node.body;anchor(node.test)
  if node.orelse:
   if len(node.orelse)==1 and isinstance(node.orelse[0],ast.If):chain(node.orelse[0])
   else:need(len(node.orelse)==1 and isinstance(node.orelse[0],ast.Raise),'SOURCE-METHOD-FALLTHROUGH')
 for node in apply.body:
  if isinstance(node,ast.If) and method_test(node.test) is not None:chain(node)
 need(branches,'SOURCE-NO-METHODS')
 # Terminal fall-through is a saved HEAD; reject changed flow instead of guessing.
 need(ast.unparse(apply.body[-2])=='result = self.save(s, r, m)' and ast.unparse(apply.body[-1])=='return result','SOURCE-FALLTHROUGH-HEAD');anchor(apply.body[-2]);anchor(apply.body[-1])
 groups={};method_map={};variant_origins={};body_keys={}
 for m,body in branches.items():
  calls=[n for stmt in body for n in ast.walk(stmt) if isinstance(n,ast.Call) and ast.unparse(n.func)=='exact' and ast.unparse(n.args[0])=='b']
  need(len(calls)==1,'SOURCE-BODY-GUARD:'+m);body_keys[m]=ast.literal_eval(calls[0].args[1]);anchor(calls[0])
  returns=[n for stmt in body for n in ast.walk(stmt) if isinstance(n,ast.Return)]
  if not returns:family='HEAD'
  elif len(returns)==1 and isinstance(returns[0].value,ast.Name):
   v=returns[0].value.id;need(v=='s' or v=='result' and any(ast.unparse(n).startswith('result = self.save(') for n in body),'SOURCE-HEAD-RETURN');family='HEAD';anchor(returns[0])
  elif len(returns)==1 and isinstance(returns[0].value,ast.Dict):
   # Binding aliases do not define required members; exact return dictionaries do.
   family=m.upper().replace('_','-')+'-RESULT';groups[family]=fields(returns[0].value);anchor(returns[0])
  else:shape_fail('return:'+m)
  method_map[m]=ref(family);variant_origins[m]=[anchor(n) for n in returns] or [anchor(apply.body[-1])]
 # handle dispatch must agree with its separate signing path and apply fallback.
 handle=functions['handle'];dispatch=[n for n in ast.walk(handle) if isinstance(n,ast.If) and ast.unparse(n.test)=="r['method'] == 'sign'"]
 need(len(dispatch)==1 and ast.unparse(dispatch[0].body[0])=='data = self.sign(r, inject)','SOURCE-HANDLE-SIGN');anchor(dispatch[0])
 need(any(isinstance(n,ast.Assign) and ast.unparse(n)=='data = self.apply(s, r, inject)' for n in ast.walk(dispatch[0])),'SOURCE-HANDLE-APPLY')
 sign=functions['sign'];returns=[n for n in ast.walk(sign) if isinstance(n,ast.Return)];need(len(returns)==2,'SOURCE-SIGN-RETURNS')
 typed=[fields(n.value) for n in returns];need(typed[0]==typed[1],'SOURCE-SIGN-SHAPES');groups['SIGNED-RESULT']=typed[0]
 literals=[]
 for n in returns:
  anchor(n);d=dict_fields(n.value);need(isinstance(d['recovered'],ast.Constant) and type(d['recovered'].value) is bool and isinstance(d['release'],ast.Constant) and d['release'].value is False,'SOURCE-SIGN-GUARDS');literals.append(d['recovered'].value)
 need(set(literals)=={False,True},'SOURCE-SIGN-RECOVERY-UNION');method_map['sign']=ref('SIGNED-RESULT');variant_origins['sign']=[anchor(n) for n in returns]
 call=next(n for n in ast.walk(sign) if isinstance(n,ast.Call) and ast.unparse(n.func)=='exact');body_keys['sign']=ast.literal_eval(call.args[1]);anchor(call)
 # Envelopes are extracted from actual response constructors.
 response_nodes=[n for n in ast.walk(handle) if isinstance(n,ast.Assign) and any(ast.unparse(t)=='response' for t in n.targets)]
 need(len(response_nodes)==2,'SOURCE-RESPONSE-UNION');variants={}
 for n in response_nodes:
  anchor(n);d=dict_fields(n.value);ok=ast.literal_eval(d['ok']);need(type(ok) is bool,'SOURCE-OK-TYPE');family='SUCCESS-RESPONSE' if ok else 'ERROR-RESPONSE';variants[str(ok).lower()]=ref(family)
  groups[family]=fields(n.value,{'data':{'request_method_choice':method_map}} if ok else {'error':S})
 raw_nodes=[n for n in ast.walk(handle) if isinstance(n,ast.Assign) and any(ast.unparse(t)=='raw' for t in n.targets)]
 need(len(raw_nodes)==1 and isinstance(raw_nodes[0].value,ast.Call) and ast.unparse(raw_nodes[0].value.func)=='enc','SOURCE-ENVELOPE');d=dict_fields(raw_nodes[0].value.args[0]);need(ast.unparse(d['signature'])=="sig('server', response)" and ast.unparse(d['response'])=='response','SOURCE-SIGNATURE-BINDING');anchor(raw_nodes[0])
 groups['RESPONSE']=fields(raw_nodes[0].value.args[0],{'response':{'choice_by':'ok','variants':variants},'signature':S})
 # Returned HEAD nested fields: exact source constructors + explicit record binding adapters.
 head=constructor('s');hd=dict_fields(head)
 for record,key in [('COUNTS','counts'),('PARTITIONS','partitions'),('RESOURCES','resources')]:groups[record]=fields(hd[key])
 groups['HEAD']=fields(head,{'counts':ref('COUNTS'),'partitions':ref('PARTITIONS'),'resources':ref('RESOURCES'),'u':directory(ref('U-ENTRY')),'active':nullable(S)})
 groups['U-ENTRY']=fields(constructor("s['u'][u]"));groups['U-ENTRY']['stage']=ref('STAGE')
 groups['STAGE']=fields(constructor("v['stage']"),{'pending':nullable(ref('PENDING')),'last':nullable(ref('LAST')),'backups':directory(S),'transport':directory(ref('TRANSPORT-ENTRY')),'retry_ids':directory(S),'nonce':I})
 groups['PENDING']=fields(constructor("st['pending']"),{'tx':nullable(S),'query':nullable(ref('QUERY')),'reconciliation':nullable(S)})
 frozen=assignments("p['result']");need(len(frozen)==1,'SOURCE-FROZEN-RESULT');anchor(frozen[0]);groups['PENDING']['result']=primitive(frozen[0].value)
 need(any(isinstance(n,ast.Assign) and ast.unparse(n)=="p['phase'] = 'FAILED-FROZEN'" for n in ast.walk(apply)),'SOURCE-FROZEN-GUARD')
 groups['LAST']=fields(constructor("st['last']"))
 acc='reference/runtime/accounting.py';groups['QUERY']=fields(constructor("p['query']",acc),{'ordinal':I})
 groups['TRANSPORT-ENTRY']=fields(constructor("st['transport'][ref]",acc))
 return {'format':'I164-SOURCE-RESPONSE-OBLIGATIONS-1','groups':groups,'method_map':method_map,'body_keys':body_keys,'optional':{'U-ENTRY':{'stage':'OPEN has committed for this retired U'},'PENDING':{'result':'phase == FAILED-FROZEN'}},'variant_origins':variant_origins,'sign_recovered_values':sorted(literals),'source_anchors':anchors,'scope':'pinned authority response dispatch, original envelopes and returned HEAD record closure; no universal Python analysis','canonical_registration':False,'actual_admission':False}

def check_catalogue(groups,optional):
 o=source_obligations()
 for n,fields in o['groups'].items():need(n in groups and enc(groups[n])==enc(fields),'SOURCE-RESPONSE-COVERAGE:'+n)
 for n,v in o['optional'].items():need(optional.get(n)==v,'SOURCE-RESPONSE-GUARD:'+n)
 # Request dispatch obligations share the same defining source, not an expected catalogue.
 typed=groups['REQUEST']['body']['union'][0];need(typed['choice_by']=='method' and set(typed['variants'])==set(o['method_map']),'SOURCE-REQUEST-METHOD-COVERAGE')
 for m,keys_ in o['body_keys'].items():need(set(groups['BODY-'+m])==set(keys_),'SOURCE-REQUEST-BODY-COVERAGE:'+m)
 return o

def check_rows(rows,o):
 """Independent expected walk over source obligations; includes framing and parent joins."""
 lookup={r['id']:r for r in rows};need(len(lookup)==len(rows),'SOURCE-ROW-DUPLICATE')
 ft=ast.parse((ROOT/'code/framing_templates.py').read_text());returns=[n for n in ast.walk(ft) if isinstance(n,ast.Return) and isinstance(n.value,ast.Dict)]
 frame_keys=[{k.value for k in n.value.keys} for n in returns];need(len(frame_keys)==2 and frame_keys[0]==frame_keys[1],'SOURCE-FRAMING-SHAPE')
 frame_types={'presence':B,'availability':S,'encoding_length':I,'member_count':nullable(I),'exact_bytes':S,'type_tag':S,'key_encoding':nullable(S),'separator_encoding':S,'opening_delimiter':S,'closing_delimiter':S};need(set(frame_types)==frame_keys[0],'SOURCE-FRAMING-FIELDS')
 def visit(record,path,t,parent,guard='present',presence='required'):
  rid=record+':'+path;need(rid in lookup,'SOURCE-MISSING-ROW:'+rid);r=lookup[rid]
  need(enc(r['type'])==enc(t) and r['parent']==parent and r['guard']==guard and r['presence']==presence,'SOURCE-ROW-BINDING:'+rid)
  for f,typ in frame_types.items():
   fid=rid+'#'+f;need(fid in lookup,'SOURCE-MISSING-FRAMING:'+fid);fr=lookup[fid];need(enc(fr['type'])==enc(typ) and fr['parent']==rid and fr['guard']=='derived framing of '+rid and fr['presence']=='required','SOURCE-FRAMING-BINDING:'+fid)
  if not isinstance(t,dict):return
  for k,v in t.get('object',{}).items():
   g=o['optional'].get(record,{}).get(k,'present');p=path+'/'+k;visit(record,p,v,rid,g,'guarded; absent is inapplicable only under inverse guard' if g!='present' else 'required');visit(record,p+'#key',S,rid,g)
  if 'directory' in t:visit(record,path+'/*',t['directory'],rid,'each retained member; lifetime multiplicity unresolved');visit(record,path+'/*#key',S,rid,'member exists')
  for i,v in enumerate(t.get('union',[])):visit(record,path+'/@union/'+str(i),v,rid,'exact type alternative '+str(i))
  for k,v in t.get('variants',{}).items():visit(record,path+'/@variant/'+k,v,rid,t['choice_by']+' == '+k)
  for k,v in t.get('request_method_choice',{}).items():visit(record,path+'/@method/'+k,v,rid,'authenticated request.method == '+k)
 for n,fields in o['groups'].items():visit(n,'',{'object':fields},None)
 return {'source_response_families':sorted(o['groups']),'admitted_methods':sorted(o['method_map']),'independent_of_generated_catalogue':True,'canonical_registration':False}
