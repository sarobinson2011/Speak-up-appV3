"""Independent source obligation oracle: push control-owned subtree requirements.
Never reads submitted rows, producer catalogue or the generator's edge function.
"""
import ast

def loc(n):return ':'.join(str(x) for x in (n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__))
def predicate(n,p):return dict(site=loc(n),expression=ast.unparse(n),predicate=p)
def state(name,**args):return dict(event=name,**args)
def relation(n,region,requirements,**extra):return dict(site=loc(n),kind=type(n).__name__,region=region,requires=requirements,**extra)
def expected(raw):
 tree=ast.parse(raw);answer={};unsupported=[]
 def visit(node,stack):
  if hasattr(node,'lineno'):answer[loc(node)]=stack
  if type(node).__name__ in ['AsyncFunctionDef','AsyncFor','AsyncWith','Await','YieldFrom','Match','TryStar'] or isinstance(node,ast.comprehension) and node.is_async:
   unsupported.append(type(node).__name__+':'+str(getattr(node,'lineno','positionless')))
  plans={}
  def put(child,*rules):plans.setdefault(id(child),[]).extend(rules)
  def region(children,*rules):
   for child in children:put(child,*rules)
  if isinstance(node,(ast.If,ast.IfExp)):
   for side,truth in [('body','truthy'),('orelse','falsy')]:
    sub=getattr(node,side);region(sub if isinstance(sub,list) else [sub],relation(node,side,[predicate(node.test,truth)],test=ast.unparse(node.test),arm='body' if side=='body' else 'else'))
  if isinstance(node,ast.BoolOp):
   for i in range(1,len(node.values)):
    put(node.values[i],relation(node,'operand-'+str(i),[predicate(x,'truthy' if type(node.op)==ast.And else 'falsy') for x in node.values[:i]],operator=type(node.op).__name__))
  if isinstance(node,ast.Compare):
   prefix=[];previous=node.left
   for i,(op,right) in enumerate(zip(node.ops,node.comparators)):
    if i:put(right,relation(node,'comparator-'+str(i),list(prefix)))
    prefix.append(dict(site=loc(node),expression=ast.unparse(ast.Compare(left=previous,ops=[op],comparators=[right])),predicate='comparison-truthy',evaluation='prior comparison using already-evaluated operands, not reevaluation'));previous=right
  if isinstance(node,(ast.For,ast.While)):
   condition=[predicate(node.test,'truthy')] if type(node)==ast.While else [state('iteration-value-produced',iterable=ast.unparse(node.iter),target=ast.unparse(node.target))]
   region(node.body,relation(node,'body',condition))
   if isinstance(node,ast.For):put(node.target,relation(node,'target',condition))
   region(node.orelse,relation(node,'else',[state('normal-loop-exit-without-break')]+([predicate(node.test,'falsy')] if type(node)==ast.While else [state('iterator-exhausted')])))
  if isinstance(node,(ast.ListComp,ast.DictComp,ast.SetComp,ast.GeneratorExp)):
   prefix=[]
   for i,generator in enumerate(node.generators):
    phase=[] if not isinstance(node,ast.GeneratorExp) or i==0 else [relation(node,'evaluation-phase',[state('generator-resumption-required')])]
    # Visit the positionless clause ourselves so iterator, target and filter phases differ.
    base=stack+phase+prefix
    if generator.is_async:unsupported.append('comprehension:positionless')
    visit(generator.iter,base+([relation(node,'evaluation-phase',[state('generator-creation-outer-iterable')])] if isinstance(node,ast.GeneratorExp) and i==0 else []))
    iteration=state('iteration-value-produced',clause=i,iterable=ast.unparse(generator.iter),target=ast.unparse(generator.target))
    resumed=[relation(node,'evaluation-phase',[state('generator-resumption-required')])] if isinstance(node,ast.GeneratorExp) and i==0 else []
    visit(generator.target,base+resumed+[relation(node,'comprehension-target',[iteration],clause=i)])
    filters=[]
    for test in generator.ifs:
     visit(test,base+resumed+[relation(node,'comprehension-ifs',[iteration]+list(filters),clause=i)]);filters.append(predicate(test,'truthy'))
    prefix=prefix+[relation(node,'comprehension-clause',[iteration]+filters,clause=i)]
   end=stack+([relation(node,'evaluation-phase',[state('generator-resumption-required')])] if isinstance(node,ast.GeneratorExp) else [])+prefix
   for name in ['elt','key','value']:
    if hasattr(node,name):visit(getattr(node,name),end)
   return
  if isinstance(node,ast.Try):
   region(node.body,relation(node,'try-body',[state('try-entered')]))
   region(node.orelse,relation(node,'try-else',[state('try-body-completed-normally')]))
   region(node.finalbody,relation(node,'finally',[state('try-exit-normal-or-abrupt')],limitation='pending exception/return/break remains; finally is not success'))
   for i,handler in enumerate(node.handlers):put(handler,relation(node,'handler-dispatch',[state('exception-from-try-body'),state('earlier-handlers-not-selected',count=i)]))
  if isinstance(node,ast.ExceptHandler):region(node.body,relation(node,'handler-body',[state('handler-selected',exception_type=ast.unparse(node.type) if node.type else 'BARE')]))
  if isinstance(node,ast.With):
   prior=[]
   for i,item in enumerate(node.items):
    guards=stack+([relation(node,'items',list(prior))] if i else [])
    visit(item.context_expr,guards)
    e=state('context-enter-completed',item=i,expression=ast.unparse(item.context_expr))
    if item.optional_vars:visit(item.optional_vars,guards+[relation(node,'with-binding',[e])])
    prior.append(e)
   region(node.body,relation(node,'body',prior))
   for b in node.body:visit(b,stack+plans.get(id(b),[]))
   return
  if isinstance(node,ast.Assert):
   put(node.test,relation(node,'assert-test',[state('assertions-enabled')]))
   if node.msg:put(node.msg,relation(node,'assert-message',[state('assertions-enabled'),predicate(node.test,'falsy')]))
  if isinstance(node,(ast.FunctionDef,ast.Lambda)):
   sub=node.body;region(sub if isinstance(sub,list) else [sub],relation(node,'invocation-boundary',[state('invocation-or-generator-resumption-required')],outer_conditions='definition-time only; not proof they still hold at invocation'))
  if isinstance(node,ast.ClassDef):region(node.body,relation(node,'class-body',[state('class-definition-executed')]))
  for child in ast.iter_child_nodes(node):visit(child,stack+plans.get(id(child),[]))
 visit(tree,[])
 return answer,unsupported
