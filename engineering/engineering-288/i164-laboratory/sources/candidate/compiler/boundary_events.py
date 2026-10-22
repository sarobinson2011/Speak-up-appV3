"""CPython-3.12.14 event/site contract for the retained boundary observer.
Coordinates without instruction offsets can be ambiguous: never promote these
to exact normal completion. This is not a runtime attestation mechanism.
"""
import ast,sys,json,hashlib
from observation_contract import AUTH,raw_source,fn,codes,opnames,position,need,exact,completion
from value_observer import untyped,typed
FUNCTIONS=('Authority.handle','Authority.sign','Authority.transaction','fault')
def identity(code):
 obj={k:getattr(code,k) for k in ['co_name','co_qualname','co_firstlineno','co_flags','co_argcount','co_kwonlyargcount','co_posonlyargcount','co_nlocals','co_stacksize']}
 for k in ['co_code','co_linetable','co_exceptiontable']:obj[k]=getattr(code,k).hex()
 for k in ['co_names','co_varnames','co_freevars','co_cellvars','co_consts']:obj[k]=typed(getattr(code,k))
 return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def check(x,root):
 need(sys.implementation.name=='cpython' and sys.version_info[:3]==(3,12,14),'EB-INTERPRETER-UNSUPPORTED')
 raw=raw_source(root,AUTH);fs={n:fn(raw,n) for n in FUNCTIONS};cs={n:next(c for c in codes(raw) if c.co_qualname==n) for n in FUNCTIONS}
 stack=[];frames={};classified=[];pending={};calls=0;terminals={n:0 for n in FUNCTIONS};lastline={};transaction_starts=0;transaction_suspends=0
 special={'sql-attempt','authorizer-denial','test-injection'}
 def enrich(e):return dict(e,source=AUTH)
 def compatible_call(e,parent):
  name=e['function']
  if name=='Authority.handle':need(parent is None and calls==0,'EB-ROOT-CALL');return
  need(parent is not None,'EB-MISSING-CALLER');pf=frames[parent]['function'];wanted={'Authority.sign':'self.sign','Authority.transaction':'self.transaction','fault':'fault'}[name]
  need(pf in ({'Authority.handle'} if name=='Authority.sign' else {'Authority.sign'} if name=='fault' else {'Authority.handle','Authority.sign'}),'EB-CALLER-FUNCTION')
  candidates=[n for n in ast.walk(fs[pf]) if isinstance(n,ast.Call) and ast.unparse(n.func)==wanted and n.lineno<=lastline.get(parent,-1)<=n.end_lineno]
  need(len(candidates)==1,'EB-CALLER-SOURCE-SITE')
  if name=='fault':exact(untyped(e['values']['point']),ast.literal_eval(candidates[0].args[0]),'EB-FAULT-CALL-ARGUMENT')
 for index,e in enumerate(x['trace']):
  event=e['event']
  if event in special:
   if event=='sql-attempt' and e['sql'] in ('BEGIN IMMEDIATE','COMMIT','ROLLBACK'):
    need(stack and frames[stack[-1]]['function']=='Authority.transaction','EB-SQL-FRAME-ASSOCIATION')
   continue
  need(event in ('call','line','exception','return'),'EB-EVENT-KIND');name=e['function'];fid=e['frame'];need(name in fs and type(fid) is int and fid>0,'EB-FRAME-IDENTITY')
  ops=opnames(raw,name,e['position']);need(bool(ops) and type(e['line']) is int and e['line']==e['position']['line'],'EB-SOURCE-INSTRUCTION')
  if event=='call':
   need('RESUME' in ops,'EB-CALL-INSTRUCTION');parent=stack[-1] if stack else None
   if fid in pending:
    need(name=='Authority.transaction' and frames[fid]['function']==name and parent==frames[fid]['parent'],'EB-GENERATOR-RESUME-ASSOCIATION')
    exact(e['position'],pending.pop(fid),'EB-GENERATOR-RESUME-SITE');frames[fid]['span']=[enrich(e)];frames[fid]['resumed']=True
   else:
    need(fid not in stack,'EB-LIVE-FRAME-REUSE')
    # An initial call must be at the defining entry, not a generator resume.
    need(e['position']['line']==cs[name].co_firstlineno and 'YIELD_VALUE' not in ops,'EB-ENTRY-SITE')
    compatible_call(e,parent);calls+=1;transaction_starts+=name=='Authority.transaction';frames[fid]={'function':name,'parent':parent,'span':[enrich(e)],'resumed':False}
   stack.append(fid);continue
  need(stack and stack[-1]==fid and frames[fid]['function']==name,'EB-EVENT-FRAME-ASSOCIATION')
  frame=frames[fid]
  if event=='line':
   need('RESUME' not in ops or 'YIELD_VALUE' in ops,'EB-LINE-ENTRY');lastline[fid]=e['line'];continue
  frame['span'].append(enrich(e))
  if event=='exception':
   # Owning boundary validator binds each exact exception site/type/condition.
   need(not ops <= {'RESUME','RETURN_VALUE','RETURN_CONST','LOAD_FAST','LOAD_CONST'},'EB-EXCEPTION-INSTRUCTION');continue
  ret=untyped(e['result']);exceptions=[z for z in frame['span'] if z['event']=='exception'];stack.pop()
  if name=='Authority.transaction':
   if 'YIELD_VALUE' in ops:
    need(ret is None and not exceptions and not frame['resumed'],'EB-GENERATOR-SUSPENSION');pending[fid]=e['position'];kind='SUSPENSION';transaction_suspends+=1
   elif exceptions:
    # Exact source re-raise after rollback, not the earlier yield instruction.
    raises=[n for n in ast.walk(fs[name]) if isinstance(n,ast.Raise) and n.exc is None]
    need(ret is None and ops=={'RAISE_VARARGS'} and any(position(n)==e['position'] for n in raises),'EB-TRANSACTION-UNWIND');kind='UNWIND'
   else:
    need(frame['resumed'] and ret is None and 'RETURN_CONST' in ops,'EB-TRANSACTION-TERMINAL')
    kind='UNRESOLVED-INSTRUCTION-SPAN' # same coordinates also include COMMIT CALL
  elif name=='fault':
   kind=completion(frame['span'],root)['kind'];need(kind in ('UNWIND','NORMAL-RETURN'),'EB-FAULT-COMPLETION')
  elif exceptions and ret is None:
   need('RETURN_VALUE' not in ops and 'RETURN_CONST' not in ops and 'YIELD_VALUE' not in ops and e['position']==exceptions[-1]['position'],'EB-UNWIND-INSTRUCTION');kind='UNWIND'
  else:
   returns=[n for n in ast.walk(fs[name]) if isinstance(n,ast.Return)]
   need(ret is not None and ops=={'RETURN_VALUE'} and any(position(n)==e['position'] for n in returns),'EB-RETURN-INSTRUCTION')
   need(name!='Authority.sign' or not exceptions,'EB-SIGN-NORMAL-AFTER-EXCEPTION');kind='NORMAL-RETURN'
   if name=='Authority.sign':
    q=json.loads(bytes.fromhex(x['request_hex']))['request'];after=json.loads(bytes.fromhex(x['reopened']['head']));p=after['u'][q['u']]['stage']['pending']
    exact(ret,{'action':q['body']['action'],'tx':p['tx'],'recovered':False,'release':False},'EB-SIGN-RETURN-VALUE')
  terminals[name]+=kind!='SUSPENSION';classified.append({'trace_index':index,'function':name,'kind':kind})
 sql=[e['sql'] for e in x['trace'] if e['event']=='sql-attempt']
 need(transaction_starts==transaction_suspends==sql.count('BEGIN IMMEDIATE'),'EB-TRANSACTION-COVERAGE')
 need(terminals['Authority.transaction']==sql.count('COMMIT')+sql.count('ROLLBACK'),'EB-TRANSACTION-COMPLETION-COVERAGE')
 need(len(pending)==transaction_starts-terminals['Authority.transaction'],'EB-SUSPENDED-COVERAGE')
 interrupted=x['process_code']!=0 or x['fault_plan']=='base-after-claim'
 if not interrupted:
  need(not stack and not pending,'EB-INCOMPLETE-FRAMES');need(terminals['Authority.handle']==1 and terminals['Authority.sign']==1,'EB-MISSING-TERMINAL')
 else:
  expected=['Authority.handle','Authority.sign']+(['fault'] if x['process_code']!=0 else [])
  exact([frames[f]['function'] for f in stack],expected,'EB-INTERRUPTED-FRONTIER')
  need(terminals['Authority.handle']==terminals['Authority.sign']==0,'EB-INTERRUPTED-TERMINAL')
 return {'interpreter':'CPython 3.12.14','source_sha256':hashlib.sha256(raw).hexdigest(),'code_identities':{n:identity(c) for n,c in cs.items()},'completions':classified,'frontier':'INCOMPLETE-BY-RECORDED-INTERRUPTION' if interrupted else 'COMPLETE-IN-DECLARED-TRACE-DOMAIN','limitations':['No instruction offsets in retained traces; mixed COMMIT/return spans remain unresolved.','Diagnostic frame IDs may be reused after completion; source-backed active/suspended associations are checked.','Trusted observer and pinned interpreter/source, not operational attestation or complete caller coverage.']}
