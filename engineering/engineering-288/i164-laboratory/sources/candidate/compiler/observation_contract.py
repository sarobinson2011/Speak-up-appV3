"""Bounded source-derived argument continuity and completion evidence.

Compile pinned bytes for instruction positions only; never execute them here.
No submitted completion label, generated expected list or digest stands in for values.
"""
import ast,dis,hashlib,json,types
from functools import lru_cache
from pathlib import Path
import program_coverage as pc
from value_observer import untyped
AUTH='support/reference/runtime/authority.py'
ACCT='support/reference/runtime/accounting.py'
EVM='support/reference/retained/lab_evm.py'
SIGNED='support/reference/retained/signed_eth.py'
# Only arguments that these exact pinned bodies do not reassign/mutate.
# accounting.validate's state is NOT captured by the old observer; no value claim.
ARGS={(AUTH,'Authority.sign'):('r','inject'),(AUTH,'Authority.save'):('request','kind','proof','s'),(AUTH,'Authority.blob'):('raw',),(AUTH,'Authority.get'):('ref',),(AUTH,'fault'):('point','want'),(EVM,'tx'):('nonce','to','data','gas','key'),(SIGNED,'validate'):('raw','expected'),(ACCT,'validate'):()}
CALLEES={(AUTH,'Authority.sign'):('self.sign',),(AUTH,'Authority.save'):('self.save',),(AUTH,'Authority.blob'):('self.blob',),(AUTH,'Authority.get'):('self.get','a.get'),(AUTH,'fault'):('fault',),(EVM,'tx'):('evm.tx',),(SIGNED,'validate'):('signed_eth.validate',),(ACCT,'validate'):('accounting.validate','validate')}
def need(ok,why):
 if not ok:raise ValueError(why)
def exact(a,b,why):need(json.dumps(a,sort_keys=True,separators=(',',':'))==json.dumps(b,sort_keys=True,separators=(',',':')),why)
def raw_source(root,source):
 pins=pc.literal('PINS');need(source in pins,'OBS-SOURCE-DOMAIN');raw=(Path(root)/source).read_bytes();need(hashlib.sha256(raw).hexdigest()==pins[source],'OBS-SOURCE-PIN');return raw
def fn(raw,name):
 body=ast.parse(raw).body
 for part in name.split('.'):
  found=[n for n in body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name==part];need(len(found)==1,'OBS-SOURCE-FUNCTION');n=found[0];body=n.body
 return n
def position(n):return {'line':n.lineno,'end_line':n.end_lineno,'column':n.col_offset,'end_column':n.end_col_offset}
@lru_cache(maxsize=32)
def codes(raw):
 def walk(code):
  yield code
  for c in code.co_consts:
   if isinstance(c,types.CodeType):yield from walk(c)
 return tuple(walk(compile(raw,'<pinned-observation-source>','exec',dont_inherit=True,optimize=0)))
def opnames(raw,name,pos):
 found=[c for c in codes(raw) if c.co_qualname==name];need(len(found)==1,'OBS-CODE-AMBIGUOUS')
 need(type(pos) is dict and set(pos)=={'line','end_line','column','end_column'} and all(type(v) is int for v in pos.values()),'OBS-POSITION')
 return {i.opname for i in dis.get_instructions(found[0],show_caches=True) if (i.positions.lineno,i.positions.end_lineno,i.positions.col_offset,i.positions.end_col_offset)==(pos['line'],pos['end_line'],pos['column'],pos['end_column']) and i.opname!='CACHE'}
def call_node(e,root):
 caller=e['caller'];need(type(caller) is dict,'OBS-CALLER');raw=raw_source(root,caller['source']);parent=fn(raw,caller['function'])
 matches=[n for n in ast.walk(parent) if isinstance(n,ast.Call) and position(n)==caller['position']]
 need(len(matches)==1,'OBS-CALL-SOURCE-SITE');n=matches[0];need(ast.unparse(n.func) in CALLEES[(e['source'],e['function'])],'OBS-CALL-TARGET');return n
def fault_expectation(call,root):
 # Evaluate only the source's two simple string comparisons. Unsupported edits fail closed.
 f=fn(raw_source(root,AUTH),'fault');need(len(f.body)==2 and all(isinstance(n,ast.If) for n in f.body),'FAULT-SOURCE-FORM')
 values={k:untyped(call['values'][k]) for k in ['point','want']};need(type(values['point']) is str and (values['want'] is None or type(values['want']) is str),'FAULT-ARGUMENTS')
 def ev(n):
  if isinstance(n,ast.Name) and n.id in values:return values[n.id]
  if isinstance(n,ast.Constant) and type(n.value) is str:return n.value
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Add):return ev(n.left)+ev(n.right)
  if isinstance(n,ast.Compare) and len(n.ops)==len(n.comparators)==1 and isinstance(n.ops[0],ast.Eq):return ev(n.left)==ev(n.comparators[0])
  raise ValueError('FAULT-UNSUPPORTED-SOURCE-EXPRESSION')
 first,second=f.body;need(not first.orelse and not second.orelse,'FAULT-SOURCE-ELSE')
 if ev(first.test):
  need(len(first.body)==1 and isinstance(first.body[0],ast.Raise),'FAULT-RAISE-FORM');raised=first.body[0];ex=raised.exc
  need(isinstance(ex,ast.Call) and isinstance(ex.func,ast.Name) and ex.func.id=='OSError' and len(ex.args)==1 and not ex.keywords,'FAULT-EXCEPTION-FORM')
  return {'kind':'UNWIND','exception':{'type':ex.func.id,'message':ev(ex.args[0])},'position':position(raised)}
 if ev(second.test):return {'kind':'UNRESOLVED','gap':'process-exit branch has no supported completion observation'}
 return {'kind':'NORMAL-RETURN'}
def completion(frame,root):
 """Classify terminal event, not complete caller handler/transaction behavior.

 Generic ambiguous instruction spans and generator suspension remain unresolved.
 A preceding exception alone never implies that a later return is an unwind.
 """
 call=frame[0];last=frame[-1];need(call['event']=='call' and last['event']=='return','OBS-COMPLETION-FRAME')
 for i,e in enumerate(frame):
  exact([e['source'],e['function'],e['frame']],[call['source'],call['function'],call['frame']],'OBS-COMPLETION-IDENTITY')
  need(e['event']==('call' if i==0 else 'return' if i==len(frame)-1 else 'exception'),'OBS-COMPLETION-EVENT-ORDER')
  need(bool(opnames(raw_source(root,e['source']),e['function'],e['position'])),'OBS-COMPLETION-INSTRUCTION')
 raw=raw_source(root,last['source']);ops=opnames(raw,last['function'],last['position']);need(bool(ops),'OBS-INSTRUCTION-SITE')
 exceptions=[e for e in frame if e['event']=='exception'];ret=untyped(last['result']);returns={'RETURN_VALUE','RETURN_CONST'}
 if (last['source'],last['function'])==(AUTH,'fault'):
  want=fault_expectation(call,root)
  if want['kind']=='UNWIND':
   need(len(exceptions)==1 and exceptions[0]['exception']==want['exception'] and exceptions[0]['position']==want['position'] and last['position']==want['position'] and ret is None and ops=={'RAISE_VARARGS'},'FAULT-UNWIND-EVIDENCE')
  elif want['kind']=='NORMAL-RETURN':need(not exceptions and ret is None and bool(ops & returns),'FAULT-NORMAL-EVIDENCE')
  else:raise ValueError('FAULT-UNSUPPORTED-COMPLETION')
  return {'kind':want['kind'],'basis':'pinned fault source conditions, exact arguments, exception and terminal instruction','prior_exception_observed':bool(exceptions)}
 if ops <= returns or (ops & returns and not ops & {'YIELD_VALUE','YIELD_FROM'} and ret is not None):
  code=next(c for c in codes(raw) if c.co_qualname==last['function'])
  need(not exceptions or bool(dis.Bytecode(code).exception_entries),'OBS-NORMAL-AFTER-UNHANDLED-EXCEPTION')
  return {'kind':'NORMAL-RETURN','basis':'pinned return instruction: unambiguous span or non-null result excluding exception unwind and suspension; prior exception alone does not imply unwind','prior_exception_observed':bool(exceptions)}
 if not ops & (returns|{'YIELD_VALUE','YIELD_FROM'}) and exceptions and exceptions[-1]['position']==last['position'] and ret is None:
  return {'kind':'UNWIND','basis':'exception and null terminal event at the same non-return, non-yield source instruction span','prior_exception_observed':True}
 return {'kind':'UNRESOLVED','basis':'instruction span or continuation does not uniquely establish normal completion or unwind','prior_exception_observed':bool(exceptions)}
def validate_observations(x,root):
 """Validate the supported captured argument contract; return fresh classifications."""
 obs=x['observations'];frames={};stack=[];lastid=0;results={}
 request=json.loads(bytes.fromhex(x['request_hex']))['request']
 state=json.loads(bytes.fromhex(x['input']['head']));owner=state['u'][request['u']];pending=owner['stage']['pending']
 def ref_value(n):
  env={'a_id':request['body']['action'],'p':pending,'v':owner,'s':state,'u':request['u']}
  if isinstance(n,ast.Name) and n.id in env:return env[n.id]
  if isinstance(n,ast.Constant) and type(n.value) is str:return n.value
  if isinstance(n,ast.Subscript):return ref_value(n.value)[ref_value(n.slice)]
  raise ValueError('OBS-UNSUPPORTED-REFERENCE-EXPRESSION')
 for i,e in enumerate(obs):
  target=(e['source'],e['function']);need(target in ARGS,'OBS-UNSUPPORTED-TARGET');raw=raw_source(root,e['source']);f=fn(raw,e['function'])
  need(e['definition_line']==f.lineno and type(e['line']) is int and f.lineno<=e['line']<=f.end_lineno,'OBS-FUNCTION-SITE')
  ops=opnames(raw,e['function'],e['position']);need(bool(ops),'OBS-INSTRUCTION-SITE')
  need(e['line']==e['position']['line'],'OBS-LINE-POSITION')
  need(type(e['frame']) is int and e['event'] in ['call','return','exception'],'OBS-EVENT')
  for value in e['values'].values():untyped(value)
  if e['event']=='exception':need(type(e.get('exception')) is dict and set(e['exception'])=={'type','message'} and all(type(v) is str for v in e['exception'].values()),'OBS-EXCEPTION-VALUE')
  for arg in ARGS[target]:need(arg in e['values'],'OBS-MISSING-ARGUMENT:'+arg)
  if e['event']=='call':
   need(e['frame']>lastid and e['frame'] not in frames,'OBS-FRAME-REUSE');lastid=e['frame'];need('RESUME' in ops,'OBS-CALL-ENTRY-SITE')
   node=call_node(e,root);stack.append(e['frame']);frames[e['frame']]=[(i,e)]
   if target==(AUTH,'Authority.sign'):
    exact(untyped(e['values']['r']),request,'OBS-CALL-REQUEST');exact(untyped(e['values']['inject']),x['inject'],'OBS-CALL-INJECTION')
   if target==(AUTH,'fault'):
    need(len(node.args)==2 and isinstance(node.args[0],ast.Constant) and type(node.args[0].value) is str and isinstance(node.args[1],ast.Name) and node.args[1].id=='inject','FAULT-CALL-SOURCE')
    exact(untyped(e['values']['point']),node.args[0].value,'FAULT-CALL-POINT');exact(untyped(e['values']['want']),x['inject'],'FAULT-CALL-INJECTION')
   if target==(AUTH,'Authority.get'):
    need(len(node.args)==1 and not node.keywords,'GET-CALL-SOURCE');exact(untyped(e['values']['ref']),ref_value(node.args[0]),'GET-CALL-REFERENCE')
  else:
   need(bool(stack) and stack[-1]==e['frame'],'OBS-STACK-ANCESTRY');frame=frames[e['frame']];entry=frame[0][1]
   exact([e['source'],e['function'],e['caller']],[entry['source'],entry['function'],entry['caller']],'OBS-FRAME-CALL-SOURCE')
   for arg in ARGS[target]:exact(e['values'][arg],entry['values'][arg],'OBS-ARGUMENT-CONTINUITY:'+arg)
   frame.append((i,e))
   if e['event']=='return':
    stack.pop();classification=completion([v for _,v in frame],root);results[i]=classification
    for j,v in frame:
     if v['event']=='exception':results[j]={'kind':'EXCEPTION-OBSERVED','completion':classification['kind'],'basis':'exception event; complete caller handler/unwind chain remains unproved'}
 need(not stack,'OBS-UNFINISHED-FRAME')
 return results
