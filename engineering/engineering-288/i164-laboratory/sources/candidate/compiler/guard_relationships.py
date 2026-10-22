"""PG-01: syntactic evaluation guards, not feasibility or dominating-control proof.
A parent-edge extractor; the independent checker uses control-owned subtrees.
"""
import ast,json,hashlib
from pathlib import Path

def key(n):return ':'.join(map(str,[n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__]))
def term(n,polarity):return {'site':key(n),'expression':ast.unparse(n),'predicate':polarity}
def event(name,**values):return dict(event=name,**values)
def rel(n,region,terms,**values):return dict(site=key(n),kind=type(n).__name__,region=region,requires=terms,**values)
def clauses(owner,indices):
 out=[]
 for i in indices:
  g=owner.generators[i];out.append(rel(owner,'comprehension-clause', [event('iteration-value-produced',clause=i,iterable=ast.unparse(g.iter),target=ast.unparse(g.target))]+[term(t,'truthy') for t in g.ifs],clause=i))
 return out

def edge(p,field,index,child,comp_owner=None):
 out=[]
 if isinstance(p,(ast.If,ast.IfExp)) and field in ['body','orelse']:
  out=[rel(p,field,[term(p.test,'truthy' if field=='body' else 'falsy')],test=ast.unparse(p.test),arm='body' if field=='body' else 'else')]
 elif isinstance(p,ast.BoolOp) and field=='values' and index:
  out=[rel(p,'operand-'+str(index),[term(t,'truthy' if isinstance(p.op,ast.And) else 'falsy') for t in p.values[:index]],operator=type(p.op).__name__)]
 elif isinstance(p,ast.Compare) and field=='comparators' and index:
  tests=[]
  for j in range(index):
   left=p.left if j==0 else p.comparators[j-1];tests.append({'site':key(p),'expression':ast.unparse(ast.Compare(left=left,ops=[p.ops[j]],comparators=[p.comparators[j]])),'predicate':'comparison-truthy','evaluation':'prior comparison using already-evaluated operands, not reevaluation'})
  out=[rel(p,'comparator-'+str(index),tests)]
 elif isinstance(p,(ast.For,ast.While)):
  if field in ['body','target']:
   terms=[term(p.test,'truthy')] if isinstance(p,ast.While) else [event('iteration-value-produced',iterable=ast.unparse(p.iter),target=ast.unparse(p.target))]
   out=[rel(p,field,terms)]
  elif field=='orelse':out=[rel(p,'else',[event('normal-loop-exit-without-break')]+([term(p.test,'falsy')] if isinstance(p,ast.While) else [event('iterator-exhausted')]))]
 elif isinstance(p,(ast.ListComp,ast.SetComp,ast.DictComp,ast.GeneratorExp)):
  if isinstance(p,ast.GeneratorExp) and not(field=='generators' and index==0):out.append(rel(p,'evaluation-phase',[event('generator-resumption-required')]))
  out+=clauses(p,range(index if field=='generators' else len(p.generators)))
 elif isinstance(p,ast.comprehension):
  owner,i=comp_owner
  if field=='iter' and isinstance(owner,ast.GeneratorExp) and i==0:out=[rel(owner,'evaluation-phase',[event('generator-creation-outer-iterable')])]
  if field=='target' or field=='ifs':
   tests=[event('iteration-value-produced',clause=i,iterable=ast.unparse(p.iter),target=ast.unparse(p.target))]
   if field=='ifs':tests += [term(t,'truthy') for t in p.ifs[:index]]
   out=[rel(owner,'comprehension-'+field,tests,clause=i)]
   if isinstance(owner,ast.GeneratorExp) and i==0:out.insert(0,rel(owner,'evaluation-phase',[event('generator-resumption-required')]))
 elif isinstance(p,ast.Try):
  if field=='body':out=[rel(p,'try-body',[event('try-entered')])]
  elif field=='orelse':out=[rel(p,'try-else',[event('try-body-completed-normally')])]
  elif field=='finalbody':out=[rel(p,'finally',[event('try-exit-normal-or-abrupt')],limitation='pending exception/return/break remains; finally is not success')]
  elif field=='handlers':out=[rel(p,'handler-dispatch',[event('exception-from-try-body'),event('earlier-handlers-not-selected',count=index)])]
 elif isinstance(p,ast.ExceptHandler) and field=='body':out=[rel(p,'handler-body',[event('handler-selected',exception_type=ast.unparse(p.type) if p.type else 'BARE')])]
 elif isinstance(p,ast.With):
  count=len(p.items) if field=='body' else index if field=='items' else 0
  if count:out=[rel(p,field,[event('context-enter-completed',item=i,expression=ast.unparse(p.items[i].context_expr)) for i in range(count)])]
 elif isinstance(p,ast.withitem) and field=='optional_vars':
  # Its owner supplies a positioned source anchor.
  owner,i=comp_owner;out=[rel(owner,'with-binding',[event('context-enter-completed',item=i,expression=ast.unparse(p.context_expr))])]
 elif isinstance(p,ast.Assert):
  if field=='test':out=[rel(p,'assert-test',[event('assertions-enabled')])]
  if field=='msg':out=[rel(p,'assert-message',[event('assertions-enabled'),term(p.test,'falsy')])]
 elif isinstance(p,(ast.FunctionDef,ast.Lambda)) and field=='body':out=[rel(p,'invocation-boundary',[event('invocation-or-generator-resumption-required')],outer_conditions='definition-time only; not proof they still hold at invocation')]
 elif isinstance(p,ast.ClassDef) and field=='body':out=[rel(p,'class-body',[event('class-definition-executed')])]
 return out

def derive(raw):
 tree=ast.parse(raw);parents={};owner={}
 for p in ast.walk(tree):
  for field,value in ast.iter_fields(p):
   if isinstance(value,ast.AST):parents[value]=(p,field,None)
   elif isinstance(value,list):
    for i,c in enumerate(value):
     if isinstance(c,ast.AST):parents[c]=(p,field,i)
  if isinstance(p,(ast.ListComp,ast.SetComp,ast.DictComp,ast.GeneratorExp)):
   for i,g in enumerate(p.generators):owner[g]=(p,i)
  if isinstance(p,ast.With):
   for i,g in enumerate(p.items):owner[g]=(p,i)
 unsupported=[]
 for n in ast.walk(tree):
  if isinstance(n,(ast.AsyncFunctionDef,ast.AsyncFor,ast.AsyncWith,ast.Await,ast.YieldFrom,ast.Match,ast.TryStar)) or isinstance(n,ast.comprehension) and n.is_async:
   unsupported.append(type(n).__name__+':'+str(getattr(n,'lineno','positionless')))
 rows={}
 for n in ast.walk(tree):
  if not hasattr(n,'lineno'):continue
  chain=[];child=n
  while child in parents:
   p,f,i=parents[child];chain.append(edge(p,f,i,child,owner.get(p)));child=p
  relationships=[g for edges in reversed(chain) for g in edges]
  rows[key(n)]=relationships
 return rows,unsupported

def validate_rows(raw,rows):
 # Independently derived by a separate control-owned subtree traversal.
 from guard_oracle import expected
 wanted,unsupported=expected(raw)
 if unsupported:raise ValueError('UNSUPPORTED-GUARD-SYNTAX:'+','.join(unsupported))
 selected={key(n) for n in ast.walk(ast.parse(raw)) if hasattr(n,'lineno') and (isinstance(n,ast.stmt) or type(n).__name__ in ['Call','IfExp','BoolOp','ListComp','SetComp','DictComp','GeneratorExp','Lambda'])}
 if len(rows)!=len(selected) or {r['site'] for r in rows}!=selected:raise ValueError('SOURCE-GUARD-MEMBERSHIP')
 for row in rows:
  if row['site'] not in wanted or json.dumps(row['guards'],sort_keys=True,allow_nan=False)!=json.dumps(wanted[row['site']],sort_keys=True,allow_nan=False):raise ValueError('SOURCE-GUARD-RELATION:'+row['site'])
 return True
