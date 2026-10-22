"""Pinned whole-module producer/exception inventory, bounded evidence consumer.
Inventory completeness is syntactic, never exhaustive execution-path coverage.
"""
import ast,json,hashlib
from pathlib import Path
import value_flow as vf
import emission_sources as es
import guard_relationships as gr
m=vf.m
CORE=es.RUNTIME
HELPERS=tuple('support/reference/retained/'+n+'.py' for n in ['anchor','stages','stage_carrier','signed_eth','lab_evm'])+('support/reference/executor/abi.py',)
DOWNSTREAM=('support/code/common.py','support/code/correspondence.py','support/code/ingest.py','integration/candidate_pipeline.py','compiler/exception_flow.py','compiler/value_flow.py')
DOMAIN=CORE+HELPERS+DOWNSTREAM
# Per-function semantics supplement exact source bodies and lexical predicates.
OBLIGATIONS={
'handle':'Authenticate before journal; replay/cap precede insert; journal commits independently; action rollback does not erase journal; caught error may follow committed action; response persistence/serialization failure leaves uncertainty.',
'apply':'Dispatch exact method/body; transactional state/blob/owner updates; permanent U and nonce ownership; atomic charges/holds; preserve uncertainty and no refund/resubmission. Return does not itself establish COMMIT.',
'sign':'Claim commits before signing; ambiguity freezes signing; persisted exact bytes recover without a new attempt; release remains separate. No external non-execution inference.',
'save':'Validate accounting, CAS, size and sequence before head/event writes; callers own atomic commit; required event after bytes equal head excluding head hash.',
'state':'Authenticate source binding and typed head/event correspondence and resource accounting; local check is narrower than full authenticated Fold.',
'packet':'Exact session/binding/expected/method/U/body/challenge; fresh challenge does not renew allowance.',
'call':'Verify server signature and packet hash; rejected or lost response cannot refund a committed action.',
'reserve':'Atomic caller transaction required: attempt charge, verifier where applicable, query hold and shared slot/hold; no refund.',
'record':'Immutable attempt ancestry/action/request/intent/nonce associations; transport entry preserves once-only slot consumption.',
'query':'Consume reserved query once or charge extra query; preserve previous attempt and unresolved obligations.',
'settle':'Release only unused first contingency hold on qualified success; failure consumes once; retries remain consumed.',
'claim':'All inclusive coordinates remain permanently owned; different owner rejects; shared SQLite transaction required.',
'require':'Exact permanent chain/executor/nonce owner required before action/sign/release.',
'attach':'Shared ledger incarnation and DELETE/FULL transaction assumptions; no operational durability or rollback-resistance claim.',
'commit':'Signed-carrier guard checks old and new reservations in one transaction; partial failure rolls back; ack loss may follow commit; no migration.',
'backup':'Kernel counter plus RETAINED-UNCERTAIN marker only; no external backup callback or success.',
'unsigned_intent':'Exact expanded/compact source representation and invocation bytes; no existing signed bytes admitted.',
'acquire':'Read-only immutable SQLite snapshot assumes complete acquisition; nonempty WAL rejects; expected head stays explicit.',
'validate_export':'Authenticate current packets/envelopes/history/owners/blobs; Fold exact transitions; preserve original envelope signature and associations.',
'check_fixture':'VF-01 authenticated current request ancestry and source-compatible suffix; no observed-fault assertion.',
'obligations':'Authenticate current full history before charge/hold continuity claim; no raw-head-only success.',
}
def h(b):return hashlib.sha256(b).hexdigest()
def identity(p):b=p.read_bytes();return {'bytes':len(b),'sha256':h(b)}
def node_id(path,n):return path+':'+es.key(n)
def segment(lines,n):
 if n.lineno==n.end_lineno:return lines[n.lineno-1][n.col_offset:n.end_col_offset].decode()
 return (lines[n.lineno-1][n.col_offset:]+b''.join(lines[n.lineno:n.end_lineno-1])+lines[n.end_lineno-1][:n.end_col_offset]).decode()
def selected(n):return isinstance(n,(ast.stmt,ast.Call,ast.IfExp,ast.BoolOp,ast.ListComp,ast.SetComp,ast.DictComp,ast.GeneratorExp,ast.Lambda,ast.comprehension))
def walk_recursive(n):
 yield n
 for _,v in ast.iter_fields(n):
  if isinstance(v,ast.AST):yield from walk_recursive(v)
  elif isinstance(v,list):
   for c in v:
    if isinstance(c,ast.AST):yield from walk_recursive(c)
def inventory(root):
 root=Path(root);obligations=literal("OBLIGATIONS");rows=[];imports=[];functions=[];sources={};unsupported=[]
 for path in literal("SOURCE_DOMAIN"):
  raw=(root/path).read_bytes();lines=raw.splitlines(keepends=True);sources[path]=identity(root/path);tree,ctx=es.tree_info(raw);guard_map,guard_unsupported=gr.derive(raw);unsupported.extend(path+":"+x for x in guard_unsupported)
  for n in walk_recursive(tree):
   if isinstance(n,(ast.Import,ast.ImportFrom)):imports.append({'source':path,'line':n.lineno,'expression':ast.unparse(n),'disposition':'DEPENDENCY-BOUNDARY','gap':'Imported code outside DOMAIN, native library/environment behavior and dynamic import resolution are not exhaustively executed or qualified.'})
   if isinstance(n,(ast.AsyncFunctionDef,ast.AsyncFor,ast.AsyncWith,ast.Match,ast.YieldFrom)):unsupported.append(node_id(path,n))
   if isinstance(n,ast.FunctionDef):
    scope,controls=ctx(n);functions.append({'source':path,'function':'.'.join(scope+[n.name]),'line':n.lineno,'end':n.end_lineno,'source_sha256':sources[path]['sha256'],'obligations':obligations.get(n.name,'Exact typed producer/helper source contract; exceptions propagate to source caller; no independent authorization or final-binding consequence.'),'body_sha256':h(segment(lines,n).encode())})
   if not selected(n):continue
   # comprehension nodes lack positions; generators are represented by their enclosing expression.
   if not hasattr(n,'lineno'):continue
   scope,_legacy_guards=ctx(n);guards=guard_map[es.key(n)];arms=[]
   if isinstance(n,(ast.If,ast.IfExp)):arms=['true','false']
   if isinstance(n,ast.BoolOp):arms=['short-circuit','all-operands']
   if isinstance(n,(ast.ListComp,ast.SetComp,ast.DictComp,ast.GeneratorExp)):
    arms=['zero-iteration','emission','filter-false','iterator/element-exception']
   if isinstance(n,(ast.For,ast.While)):arms=['zero','iteration','normal-exit','break/exception-if-reachable']
   if isinstance(n,ast.Try):arms=['normal','else','finally']+['handler:'+ast.unparse(x.type) if x.type else 'handler:bare' for x in n.handlers]
   if isinstance(n,ast.Call):arms=['return','exception-propagation']
   expression=segment(lines,n)
   rows.append({'id':node_id(path,n),'source':path,'source_sha256':sources[path]['sha256'],'site':es.key(n),'function':'.'.join(scope),'kind':type(n).__name__,'expression':expression,'guards':guards,'guard_scope':'syntactic evaluation relationships, outer-to-inner; invocation boundary separates definition-time conditions; earlier control-flow reachability not derived','branch_obligations':arms,'disposition':'SOURCE-MAPPED; EXECUTION-COMBINATIONS-UNESTABLISHED','gap':{'kind':'UNFINISHED-CHECKING','anchor':node_id(path,n),'required':'Reachability plus this operation/arm and caller-callee exception propagation evidence; executed line alone is not branch or combination coverage.'},'validation':'current authenticated ingest/Fold + value_flow obligations; VF-01 only for its admitted cuts'})
  gr.validate_rows(raw,[r for r in rows if r['source']==path])
  # Independent built-in walker detects synchronized omission from the emitted inventory.
  required={node_id(path,n) for n in ast.walk(tree) if selected(n) and hasattr(n,'lineno')}
  m.need({x['id'] for x in rows if x['source']==path}==required,'PROGRAM-SOURCE-OMISSION')
 return {'format':'I164-PROGRAM-INVENTORY-1','sources':sources,'functions':functions,'sites':rows,'imports':imports,'unsupported':unsupported,'syntactic_inventory_complete':not unsupported,'runtime_path_complete':False,'path_definition':'Every positioned statement/call/conditional expression, all lexical arms; call exception edges retained. Feasible multi-site paths, aliasing, native/environment faults and transitive dependencies are explicit gaps, not enumerated universes. Comprehensions are retained in exact enclosing expressions and AST coverage below.','syntax_nodes':{p:sorted({type(n).__name__ for n in ast.walk(ast.parse((root/p).read_bytes()))}) for p in literal("SOURCE_DOMAIN")}}
def compile_coverage(root):
 root=Path(root);obligations=literal("OBLIGATIONS")
 for name,digest in literal("PINS").items():
  if h((root/name).read_bytes())!=digest:raise ValueError("PROGRAM-PIN:"+name)
 c=vf.s.setup(root);import common;common.pinned_sources()
 inv=inventory(root);old=json.loads((root/'guard_emission_outputs/coverage.json').read_bytes())
 # Reuse exact previously reviewed artifact with its candidate source dependency checks.
 m.same(old['binding'],c.binding,'PROGRAM-CANDIDATE-BINDING')
 links={}
 for r in old['sources']['runtime']['sites']:
  links[r['source']+':'+r['site']]={'families':r['families'],'projection_sites':r['projection_sites'],'role':r['role']}
 for r in inv['sites']:
  r['reviewed_mapping']=links.get(r['id'])
  method=None
  for guard in r['guards']:
   if guard.get('arm')=='body' and guard.get('test','').startswith('m == '):method=ast.literal_eval(guard['test'][5:])
  r['dispatch_method']=method
  funcs={'Authority.__init__':['CONFIG','BINDING','HEAD','COUNTS','RESOURCES','OWNERSHIP-META'],'Authority.save':['EVENT','HEAD'],'Authority.blob':['BLOB-STORE'],'Authority.handle':['PACKET','REQUEST','RESPONSE','JOURNAL'],'Authority.sign':['ACTION','SIGNED-TRANSACTION','SIGNED-RESULT','PENDING','HEAD','EVENT'],'Scheduler.packet':['PACKET','REQUEST'],'Scheduler.call':['RESPONSE'],'reserve':['COUNTS','RESOURCES','PARTITIONS','STAGE'],'record':['ATTEMPT','TRANSPORT-ENTRY'],'query':['QUERY','COUNTS','RESOURCES'],'settle':['TRANSPORT-ENTRY','RESOURCES'],'claim':['OWNERSHIP-ROW','OWNERSHIP-ROW-SQL']}
  methods={'head':['HEAD'],'retire':['UNSIGNED-INTENT','COMPACT-INTENT','U-ENTRY','OWNERSHIP-ROW'],'open':['STAGE','STAGE-META','AUTHORIZED-MESSAGE','OWNERSHIP-ROW'],'decide':['ACTION','TEMPLATE','ATTEMPT','PENDING','COUNTS','RESOURCES'],'release':['RELEASE-RESULT','TRANSPORT-ENTRY','PENDING'],'retry_release':['RETRY-ID-ENTRY','ATTEMPT','RELEASE-RESULT','RESOURCES'],'query':['QUERY','COUNTS','RESOURCES'],'observe':['OBSERVATION','LAST','PENDING','RESOURCES'],'backup':['BACKUP-ENTRY','COUNTS','PARTITIONS']}
  names=methods.get(method,funcs.get(r['function'],[]))
  r['associated_families']=[name for name in names if name in old['families']]
  r['association_scope']='function/dispatch transformation relationship; not assertion that every statement emits every associated family'
  r['obligations']=obligations.get(method,obligations.get(r['function'].split('.')[-1], 'Typed helper or downstream validation path; exact expression and caller obligations retained. This row has no independent permission to discharge an obligation.'))

 return {'format':'I164-PROGRAM-COVERAGE-1','candidate':c.binding,'contexts':sorted(c.contexts),'inventory':inv,'reviewed_map':identity(root/'guard_emission_outputs/coverage.json'),'family_connections':old['families'],'procedure':identity(root/'prospective_outputs/procedure.json'),'rules':identity(root/'prospective_outputs/semantic/rules.json'),'directory':identity(root/'compiler_outputs/compiler-output.json'),'code':identity(Path(__file__)),'guard_code':{n:identity(Path(__file__).parent/n) for n in ['guard_relationships.py','guard_oracle.py']},'coverage_scope':'whole-module syntactic source disposition, bounded producer/value and exceptional runtime probes; NOT whole-program execution completeness','backup':'KERNEL-ONLY','blockers':['UNEXECUTED-BRANCH-COMBINATIONS-AND-TRANSITIVE-EXCEPTIONS','SOURCE-OWNED-LIFETIME-AND-EXTERNAL-BOUNDS','AUTHORITY-DESIGNATION-AND-REGISTRATION','QUALIFIED-CLASSIFICATIONS-CUSTODY-ROLLBACK-EVIDENCE','FULL-MODEL-BINDING'],'final_binding':'BLOCKED','full_expansion_ready':False,'actual_admission':False,'stream_identities':'UNCOMPUTED'}
def validate_coverage(value,root):
 # Source-owned guard oracle runs on submitted rows before generator equality.
 for name in literal('SOURCE_DOMAIN'):
  gr.validate_rows((Path(root)/name).read_bytes(),[r for r in value['inventory']['sites'] if r['source']==name])
 expected=compile_coverage(root);m.same(value,expected,'PROGRAM-COVERAGE-SUBSTITUTION');return True
def observe(export,context,root):
 vf.s.setup(root)
 receipt=vf.inspect(export,context)
 return {'format':'I164-PROGRAM-EVIDENCE-1','coverage_sha256':h(m.enc(compile_coverage(root))),'value_flow':receipt,'exception_location':'NOT-INFERRED','backup':'KERNEL-ONLY','final_binding':'BLOCKED','actual_admission':False}
def validate_evidence(value,export,context,root):
 expected=observe(export,context,root);m.same(value,expected,'PROGRAM-EVIDENCE-SUBSTITUTION');return True

PINS={'support/reference/runtime/authority.py': '4565bb30cb637b3cef40a3f1da2b3722840b747ab110fa37eede0cbc2e3b313a', 'support/reference/runtime/accounting.py': '7c344469895db20062380e60ad60e055e6fc5121a167720bc64162f2e8aa26cc', 'support/reference/runtime/ownership.py': '484bb578e1fff08bd397fea25987c929400bb203ae72cf55b8091db5007b2b18', 'support/reference/retained/anchor.py': '70adfc96e71a158b75a8c9a4dc417204bbac93ec4c60673fbf67e11d92ab5c0c', 'support/reference/retained/stages.py': '010f0d38b3c9f297439c7fe2b3c0345350f9bd566fd05a623273144fb37aaf3d', 'support/reference/retained/stage_carrier.py': '3f64dc786401e5594ba241ac06065bf9508a56cdd2c80fae885777e766999c29', 'support/reference/retained/signed_eth.py': '3e688ebe7fc0e716e8590d620254a53f9dcf508450f9003561eccbb2e58c6d7b', 'support/reference/retained/lab_evm.py': 'ddc078a71c1c978b4d2ff99931c2d605e5fd2b0eb35a88ad1e378cb10447d6b6', 'support/reference/executor/abi.py': 'e6d36c1ae8dfef44faefd6f64fa9b2d5fa1077ac9d62198198aeeebd25541800', 'support/code/common.py': '1d0d557a8dd76264bd06f6879c053bd3f640287093242ee97f9f6000ad083efb', 'support/code/correspondence.py': '5768ff4503be04bdf956b47c40a6bf8a1cd8ae0597f1d55212f562a5b054b8b2', 'support/code/ingest.py': 'a742246454965ad83f6e680dfe0d5f58b47287a38fad3ec88767d077d8fd8a6c', 'integration/candidate_pipeline.py': 'c53bb593ad12362846376fe957e6aa6cf29d783c6472a688fd7e54e29121fed8', 'compiler/exception_flow.py': 'fcbfec920952a910ef6bf0c74fe69f00c1c7e3b857421700fbcf2cf3f46ed816', 'compiler/value_flow.py': 'd0df4d091e3349c79fc4d0a2f66578891f7bfa59f4ad8003e26b44354ab52d18', 'guard_emission_outputs/coverage.json': '49922d4f01b534ba9b11df3b0f534bac943851effde09e8af988725f50204865', 'prospective_outputs/procedure.json': '4ba2258a6008f3acef259fa8c560e612771dfb9ab756a6b8846b07d5a8847bb1', 'prospective_outputs/semantic/rules.json': 'aa5485ceebf704637071d536ecddaa1169e4deb3783c551ec2663804802142b1', 'compiler_outputs/compiler-output.json': 'b75724b3ab871040b3aa8d33c4cd1a5be7e682019a52793b835af72a9146514b'}

SOURCE_DOMAIN=('support/reference/runtime/authority.py', 'support/reference/runtime/accounting.py', 'support/reference/runtime/ownership.py', 'support/reference/retained/anchor.py', 'support/reference/retained/stages.py', 'support/reference/retained/stage_carrier.py', 'support/reference/retained/signed_eth.py', 'support/reference/retained/lab_evm.py', 'support/reference/executor/abi.py', 'support/code/common.py', 'support/code/correspondence.py', 'support/code/ingest.py', 'integration/candidate_pipeline.py', 'compiler/exception_flow.py', 'compiler/value_flow.py')

def literal(name):
 tree=ast.parse(Path(__file__).read_bytes())
 return ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)))
