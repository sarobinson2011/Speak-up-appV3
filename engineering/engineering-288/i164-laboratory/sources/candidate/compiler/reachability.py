"""Bounded source-derived sequential reachability obligations, never feasibility proof."""
import ast,json,hashlib
from pathlib import Path
import program_coverage as p

def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def ident(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def loc(n):return p.gr.key(n)
def abrupt(block):
 # Necessary normal-completion constraint only. No inference through suppression/finally.
 for n in block:
  if isinstance(n,(ast.Return,ast.Raise,ast.Break,ast.Continue)):return type(n).__name__
  if isinstance(n,ast.If) and n.orelse and abrupt(n.body) and abrupt(n.orelse):return 'both-if-arms-abrupt'
 return None

def module(raw,path):
 tree=ast.parse(raw);parents={};scope={};functions={};calls=[];nodes=list(ast.walk(tree))
 def walk(n,name):
  if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
   name=name+'.'+n.name if name else n.name
   if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):functions[name]=loc(n)
  scope[id(n)]=name
  for field,v in ast.iter_fields(n):
   children=v if isinstance(v,list) else [v]
   for i,c in enumerate(children):
    if isinstance(c,ast.AST):parents[id(c)]=(n,field,i if isinstance(v,list) else None);walk(c,name)
 walk(tree,'')
 def prior(n):
  out=[];child=n
  while id(child) in parents:
   owner,field,index=parents[id(child)]
   if index is not None:
    seq=getattr(owner,field)
    if isinstance(child,ast.stmt) and all(isinstance(x,ast.stmt) for x in seq):
     group=[]
     for prev in seq[:index]:
      row={'site':loc(prev),'kind':type(prev).__name__,'condition':'normal-completion-required','phase_scope':scope[id(prev)]}
      if isinstance(prev,(ast.Return,ast.Raise,ast.Break,ast.Continue)):row.update(condition='no-normal-successor',reason=type(prev).__name__)
      elif isinstance(prev,ast.If):
       yes,no=abrupt(prev.body),abrupt(prev.orelse)
       row.update(test=ast.unparse(prev.test),test_site=loc(prev.test),body_exit=yes,else_exit=no)
       if yes and no:row['condition']='no-normal-successor'
       elif yes:row['necessary_test_result']='falsy-at-earlier-evaluation'
       elif no:row['necessary_test_result']='truthy-at-earlier-evaluation'
      elif isinstance(prev,(ast.For,ast.While)):row['detail']='loop may complete by exhaustion/false test or break; else depends on no break; no iteration bound inferred'
      elif isinstance(prev,ast.Try):row['detail']='body/handler and finally must permit normal continuation; suppression/override and exception types unresolved'
      elif isinstance(prev,ast.With):row['detail']='context exit may suppress an exception; context protocol unresolved'
      group.append(row)
     out=group+out
   child=owner
  return out
 rows=[]
 for n in nodes:
  if hasattr(n,'lineno') and (isinstance(n,ast.stmt) or type(n).__name__ in ['Call','IfExp','BoolOp','ListComp','SetComp','DictComp','GeneratorExp','Lambda']):
   rows.append({'id':path+':'+loc(n),'site':loc(n),'scope':scope[id(n)],'normal_predecessors':prior(n),'status':'NECESSARY-STATIC-CONDITIONS-NOT-REACHABILITY-PROOF'})
  if isinstance(n,ast.Call):
   callee=ast.unparse(n.func);resolved=None
   # Only lexical declaration candidates, never proof of runtime dispatch or lack of rebinding.
   if isinstance(n.func,ast.Name) and n.func.id in functions:resolved=functions[n.func.id]
   if isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='self':
    owner=scope[id(n)].split('.')[0];resolved=functions.get(owner+'.'+n.func.attr)
   calls.append({'site':loc(n),'caller':scope[id(n)],'expression':callee,'lexical_candidate':resolved,'normal_continuation':'callee-normal-return-required','exceptional_continuation':'propagates-unless-applicable-handler-or-context-exit-suppresses','dispatch_status':'LEXICAL-CANDIDATE-ONLY' if resolved else 'UNRESOLVED-IMPORT-ALIAS-OR-DYNAMIC-DISPATCH'})
 transfers=[]
 for n in nodes:
  if isinstance(n,(ast.Return,ast.Raise,ast.Break,ast.Continue,ast.Yield,ast.Try,ast.With)):
   owners=[];c=n
   while id(c) in parents:
    a,f,i=parents[id(c)]
    if isinstance(a,(ast.FunctionDef,ast.Lambda)):break
    if isinstance(a,(ast.Try,ast.With,ast.For,ast.While)):owners.append({'site':loc(a),'region':f,'kind':type(a).__name__})
    c=a
   transfers.append({'site':loc(n),'kind':type(n).__name__,'scope':scope[id(n)],'enclosing_transfer_boundaries':owners,'resolution':'STRUCTURAL-ONLY; finally/context suppression, matching exception and continuation may require dynamic evidence'})
 return {'source':path,'identity':ident(raw),'sites':sorted(rows,key=lambda x:x['id']),'calls':sorted(calls,key=lambda x:x['site']),'transfers':sorted(transfers,key=lambda x:x['site']),'unsupported':[loc(n) for n in nodes if isinstance(n,(ast.AsyncFunctionDef,ast.AsyncFor,ast.AsyncWith,ast.Await,ast.Match,ast.TryStar,ast.YieldFrom))]}

def compile(root):
 root=Path(root);coverage=p.compile_coverage(root)
 sources=[module((root/name).read_bytes(),name) for name in p.literal('SOURCE_DOMAIN')]
 if any(x['unsupported'] for x in sources):raise ValueError('UNSUPPORTED-CONTROL-FLOW')
 # Independent raw-source selection establishes membership, not submitted/generated lists.
 wanted={name+':'+loc(n) for name in p.literal('SOURCE_DOMAIN') for n in ast.walk(ast.parse((root/name).read_bytes())) if hasattr(n,'lineno') and (isinstance(n,ast.stmt) or type(n).__name__ in ['Call','IfExp','BoolOp','ListComp','SetComp','DictComp','GeneratorExp','Lambda'])}
 for m in sources:
  nodes=list(ast.walk(ast.parse((root/m['source']).read_bytes())))
  calls=[loc(n) for n in nodes if isinstance(n,ast.Call)]
  transfers=[loc(n) for n in nodes if isinstance(n,(ast.Return,ast.Raise,ast.Break,ast.Continue,ast.Yield,ast.Try,ast.With))]
  if sorted(calls)!=sorted(x['site'] for x in m['calls']) or sorted(transfers)!=sorted(x['site'] for x in m['transfers']):raise ValueError('SOURCE-TRANSFER-OR-CALL-MEMBERSHIP')
 got=[r['id'] for m in sources for r in m['sites']]
 if len(got)!=len(wanted) or set(got)!=wanted:raise ValueError('SOURCE-MEMBERSHIP')
 return {'format':'I164-REACHABILITY-DRAFT-1','coverage':ident(p.m.enc(coverage)),'candidate':coverage['candidate'],'contexts':coverage['contexts'],'sources':sources,'code':ident(Path(__file__).read_bytes()),'limitations':['EARLIER-OPERAND-NORMAL-EVALUATION','EXCEPTION-MATCHING-AND-FINALLY-OVERRIDE','DYNAMIC-DISPATCH-AND-ALIASES','LOOP-FEASIBILITY-AND-LIFETIME-COUNTS','DEFERRED-CONTINUATION','NATIVE-EXTERNAL-EFFECTS','UNEXECUTED-SOURCE-PATHS'],'runtime_coverage':'NOT-ESTABLISHED-BY-STATIC-MAPPING','full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED','backup':'KERNEL-ONLY'}
def validate(value,root):
 # Always regenerate current source expectations; no cached-object admission.
 expected=compile(root)
 if enc(value)!=enc(expected):raise ValueError('REACHABILITY-MISMATCH')
 return True
