"""Finite source-anchored path obligations plus explicit unbounded composition gaps."""
import ast,json,hashlib
from pathlib import Path
import program_coverage as p
from signing_values import enc,sha,capture_identity,catalogue_pin
from observation_contract import validate_observations
CONTROL=(ast.Assert,ast.If,ast.IfExp,ast.BoolOp,ast.Compare,ast.For,ast.While,ast.Try,ast.ExceptHandler,ast.With,ast.ListComp,ast.SetComp,ast.DictComp,ast.GeneratorExp,ast.Yield,ast.Return,ast.Raise,ast.Break,ast.Continue)
def key(n):return p.gr.key(n)
def compile(root,package):
 root=Path(root);package=Path(package);records=[];observed={};unwinds={};unresolved={}
 catalogue=(package/'results/execution/INDEX.json').read_bytes()
 if sha(catalogue)!=catalogue_pin():raise ValueError('PATH-CAPTURE-CATALOGUE')
 captures=json.loads(catalogue)
 for c in captures:
  capture=(package/c['path']).read_bytes()
  if len(capture)!=c['bytes'] or sha(capture)!=c['sha256']:raise ValueError('PATH-CAPTURE-BYTES')
  x=json.loads(capture);capture_identity(x,root);classifications=validate_observations(x,root)
  for i,e in enumerate(x['observations']):
   a=e.get('caller') or {};pos=a.get('position')
   if e['event'] in ['return','exception'] and pos:
    anchor=(a.get('source'),pos['line'],pos['column'],pos['end_line'],pos['end_column'],e['event'])
    ref={'capture':c['name'],'capture_sha256':c['sha256'],'observation':i,'producer':e['function'],'producer_source':e['source']}
    classification=classifications[i]
    if e['event']=='return' and classification['kind']!='NORMAL-RETURN':
     target=unwinds if classification['kind']=='UNWIND' else unresolved
     target.setdefault(anchor[:-1],[]).append(dict(ref,classification=classification));continue
    observed.setdefault(anchor,[]).append(ref)
 for path in p.literal('SOURCE_DOMAIN'):
  raw=(root/path).read_bytes();need_hash=p.literal('PINS')[path]
  if sha(raw)!=need_hash:raise ValueError('PATH-SOURCE')
  tree=ast.parse(raw);parents={};scopes={}
  def walk(n,scope):
   if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.Lambda)):scope=scope+[getattr(n,'name','<lambda>')]
   scopes[id(n)]='.'.join(scope)
   for child in ast.iter_child_nodes(n):parents[id(child)]=n;walk(child,scope)
  walk(tree,[])
  def add(n,edge,required,gap,available=None,supported=False):
   c=n
   while id(c) in parents and not (isinstance(c,ast.stmt) or type(c).__name__ in ['Call','IfExp','BoolOp','ListComp','SetComp','DictComp','GeneratorExp','Lambda']):c=parents[id(c)]
   records.append({'id':path+':'+key(n)+':'+edge,'source':path,'source_sha256':need_hash,'anchor':key(n),'expression':ast.get_source_segment(raw.decode(),n),'scope':scopes[id(n)],'edge':edge,'guard_and_sequential_mapping_ref':path+':'+key(c),'required_observation':required,'available_evidence':available or [],'supported_conclusion':'BOUNDED-VALUE-OR-EXCEPTION-CORRESPONDENCE-IN-LISTED-CAPTURES' if supported else 'SOURCE-OBLIGATION-IDENTIFIED; PATH-COVERAGE-NOT-ESTABLISHED','remaining_gap':gap,'external_dependencies':['SOURCE-OWNED-LIFETIME-BOUNDS','AUTHORITY-ACTS','QUALIFIED-CUSTODY-ROLLBACK-AND-OUTCOME-EVIDENCE']})
  for n in ast.walk(tree):
   if isinstance(n,ast.Call):
    for event in ['return','exception']:
     avail=observed.get((path,n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,event),[])
     supported=bool(avail) and all(x['producer'] in ['tx','validate','fault'] and x['producer_source'] in ['support/reference/retained/lab_evm.py','support/reference/retained/signed_eth.py','support/reference/runtime/authority.py'] for x in avail)
     gap=[{'category':'MISSING-LOCAL-TESTS','detail':'Other feasible inputs/guard combinations and exceptional causes at '+key(n)+' remain unexecuted.'}]
     if not supported:gap.insert(0,{'category':'MISSING-LOCAL-OBSERVATION-OR-ORACLE','detail':('Some call events exist but argument/result and binding semantics are not independently completed for this source call.' if avail else 'No source-anchored '+event+' value observation for this exact call site.')})
     site=(path,n.lineno,n.col_offset,n.end_lineno,n.end_col_offset)
     ambiguous=unresolved.get(site,[])
     if event=='exception':gap.append({'category':'MISSING-LOCAL-PROPAGATION-ORACLE','detail':'Callee exception/unwind does not establish complete caller handler, transaction exit or response-persistence behavior at '+key(n)+'.'})
     if ambiguous:gap.append({'category':'AMBIGUOUS-COMPLETION-EVIDENCE','detail':'Retained events do not uniquely establish normal completion or propagation; see unresolved_evidence.'})
     add(n,'CALL-'+event.upper(),'Exact runtime target, arguments, '+('typed result and source-established normal completion' if event=='return' else 'callee exception type/value, separately classified terminal unwind; complete caller chain remains a gap')+', request/attempt and authenticated state obligations.',gap,avail,supported)
     records[-1]['completion_evidence']=unwinds.get(site,[]) if event=='exception' else []
     records[-1]['unresolved_evidence']=ambiguous
     if supported:records[-1]['supported_conclusion']='BOUNDED-NORMAL-CALLEE-RETURN-IN-LISTED-CAPTURES' if event=='return' else 'BOUNDED-CALLEE-EXCEPTION-IN-LISTED-CAPTURES; CALLER-PROPAGATION-UNPROVED'
   elif isinstance(n,CONTROL):
    if isinstance(n,ast.Assert):edges=['ASSERT-TRUE','ASSERT-FALSE-RAISE','ASSERTIONS-DISABLED']
    elif isinstance(n,(ast.If,ast.IfExp)):edges=['TEST-TRUE','TEST-FALSE']
    elif isinstance(n,ast.BoolOp):edges=['OPERAND-'+str(i)+'-EVALUATED-OR-SHORT-CIRCUITED' for i in range(len(n.values))]
    elif isinstance(n,(ast.For,ast.While)):edges=['ITERATION-ENTRY','NORMAL-EXIT','BREAK-EXIT','EXCEPTION-EXIT']
    elif isinstance(n,ast.Try):edges=['BODY-NORMAL','HANDLER-DISPATCH','UNHANDLED-EXCEPTION','FINALLY-OVERRIDE-OR-PRESERVE']
    elif isinstance(n,ast.With):edges=['ENTER','EXIT-NORMAL','EXIT-EXCEPTION-SUPPRESS-OR-PROPAGATE']
    elif isinstance(n,(ast.ListComp,ast.SetComp,ast.DictComp,ast.GeneratorExp)):edges=['ITERATOR-FILTER-ELEMENT-COMBINATIONS','DEFERRED-OR-EXCEPTIONAL-EXIT']
    else:edges=['TRANSFER-OR-EVALUATION-'+type(n).__name__]
    for edge in edges:add(n,edge,'Observed operand/condition values, chosen edge and continuation under exact invocation; preserve obligation state.',[{'category':'MISSING-LOCAL-EDGE-TEST-AND-INFERENCE','detail':'No general branch/transfer observer or feasible-path oracle for this exact '+edge+' at '+key(n)+'. A call value or source line alone is insufficient.'}])
   if isinstance(n,(ast.FunctionDef,ast.Lambda)):
    add(n,'COMPOSED-PATH-FAMILY','Complete ordered invocation, each guarded operation and exception continuation; loops/recursion/generator resumes quantified.',[{'category':'MISSING-LOCAL-COMPOSITION','detail':'No complete feasible-path/exception-dispatch proof for '+scopes[id(n)]+'. Listed individual calls do not cover all ordered combinations.'},{'category':'UNAVAILABLE-SOURCE-BOUND','detail':'Where loops, recursion or repeated invocations apply, no lifetime bound is inferred from finite fixtures or implementation ceilings.'}])
   if isinstance(n,ast.expr) and not isinstance(n,(ast.Call,ast.Constant)):
    add(n,'IMPLICIT-EVALUATION-EXCEPTION','Exact operation/operand success or exception, target/alias and continuation.',[{'category':'MISSING-LOCAL-EXPRESSION-OBSERVATION','detail':'Implicit exceptions during '+type(n).__name__+' evaluation at '+key(n)+' have no complete value/exception observer; explicit call captures do not cover it.'}])
 ids=[r['id'] for r in records]
 if len(ids)!=len(set(ids)):raise ValueError('DUPLICATE-PATH')
 return {'format':'I164-SIGN-EXCEPTION-PATH-DISPOSITIONS-2','domain':'all explicit calls, listed control forms, function/lambda composition families and nonconstant noncall expression exception obligations in exact pinned 15 modules; finite obligation decomposition, not enumeration of all feasible execution paths','sources':{n:p.literal('PINS')[n] for n in p.literal('SOURCE_DOMAIN')},'paths':sorted(records,key=lambda r:r['id']),'unsupported':'transitive imports, native effects, unpinned code and full feasible combinations; implicit operation rows remain gaps','backup':'KERNEL-ONLY','whole_program_coverage':False,'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED'}
def validate(value,root,package):
 if enc(value)!=enc(compile(root,package)):raise ValueError('PATH-DISPOSITION-MISMATCH')
 return True
