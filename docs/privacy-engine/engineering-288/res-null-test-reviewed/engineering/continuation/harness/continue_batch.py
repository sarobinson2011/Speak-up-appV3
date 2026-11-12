"""Harness-only continuation. Candidate and original assertion/guard ASTs remain fixed."""
import ast,copy,hashlib,json,os,sys,time,traceback
from pathlib import Path
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;P=H.parent;ROOT=P/'source'
batch_id=sys.argv[1];BATCH=P/'batches'/batch_id;RAW=BATCH/'raw'
plan=json.loads((H/'FULL-PLAN.json').read_bytes());bp=json.loads((H/'BATCH-PLAN.json').read_bytes());spec=next(b for b in bp['batches'] if b['id']==batch_id)
fixed=(ROOT/'tests/focused.py').read_bytes()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert ident(fixed)==bp['source_test_identity']
assert ident((ROOT/'code/managed_coverage.py').read_bytes())=={'bytes':519785,'sha256':'414e30bea79178fbf4ecfebc4519fb7eaa41e5df48b80f0126686a53f0f12633'}
assert ident((ROOT/'code/correspondence.py').read_bytes())=={'bytes':10053,'sha256':'b0b36c61bd24130648fc55b97a9331c0fedbdf95479a6fdf3429d600406fdee5'}
started=time.monotonic();tree=ast.parse(fixed);main=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='main')
def utc():return datetime.now(timezone.utc).isoformat()
def save(path,v):
 with open(path,'x') as f:json.dump(v,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
def phase(name,**details):
 row={'utc':utc(),'seconds':time.monotonic()-started,'phase':name,**details}
 with open(BATCH/'phases.jsonl','a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
phase('start',batch=batch_id,original_sequences=spec['sequences'])
# Execute only original module definitions, not its original main/footer.
module_nodes=[n for n in tree.body if n.lineno<141]
g={'__file__':str(ROOT/'tests/focused.py'),'__name__':'_fixed_focused_definitions'}
sys.argv=[str(ROOT/'tests/focused.py'),str(RAW)]
exec(compile(ast.Module(body=module_nodes,type_ignores=[]),str(ROOT/'tests/focused.py'),'exec'),g)
cursor=0;next_original=None;current=None;check_started=None;skipped=[]
def record(name,layer,status,detail=None):
 global cursor
 assert current is not None and name==current['name'] and layer==current['layer'],'PLANNED-ASSERTION-LABEL-OR-LAYER'
 row={'sequence':len(g['ROWS'])+1,'original_sequence':current['original_sequence'],'utc':utc(),'name':name,'layer':layer,'status':status,'detail':detail,
      'case':current['case'],'callsite':current['callsite'],'assertion_AST_sha256':current['assertion_AST_sha256'],'check_seconds':time.monotonic()-check_started}
 g['ROWS'].append(row);save(RAW/('%04d.json'%row['sequence']),row)
 with open(RAW/'progress.jsonl','a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(row,sort_keys=True),flush=True);cursor+=1
g['record']=record
def next_check(line,column):
 global next_original,current,check_started
 assert next_original is not None and 1<=next_original<=316
 item=plan[next_original-1];next_original+=1
 assert item['callsite']['line']==line and item['callsite']['column']==column,'ORIGINAL-ASSERTION-ORDER'
 if item['original_sequence'] not in spec['sequences']:
  skipped.append(item['original_sequence']);return False
 assert cursor<len(spec['sequences']) and item['original_sequence']==spec['sequences'][cursor],'BATCH-ORDER'
 current=item;check_started=time.monotonic();return True
g['next_check']=next_check
class Wrap(ast.NodeTransformer):
 def visit_Expr(self,node):
  if isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id in ('check','reject'):
   call=node.value;h=hashlib.sha256(ast.dump(call,include_attributes=False).encode()).hexdigest()
   assert any(p['callsite']['line']==call.lineno and p['callsite']['column']==call.col_offset and p['assertion_AST_sha256']==h for p in plan),'ASSERTION-AST-CHANGED'
   condition=ast.Call(func=ast.Name(id='next_check',ctx=ast.Load()),args=[ast.Constant(call.lineno),ast.Constant(call.col_offset)],keywords=[])
   return ast.copy_location(ast.If(test=condition,body=[node],orelse=[]),node)
  return self.generic_visit(node)
def execute(nodes,wrap=False):
 nodes=copy.deepcopy(nodes);t=ast.Module(body=nodes,type_ignores=[])
 if wrap:t=Wrap().visit(t)
 ast.fix_missing_locations(t);exec(compile(t,str(ROOT/'tests/focused.py'),'exec'),g)
def statements(a,b):return [n for n in main.body if a<=n.lineno<=b]
def save_state():
 state={k:g[k] for k in ('fast','cat','representatives','summaries')}
 state['coverage']=[list(x) for x in sorted(g['coverage'],key=repr)];state['occurrences']=sorted(g['occurrences']);state['guard']=dict(g['GUARD']);state['source_test_identity']=ident(fixed)
 path=BATCH/'setup-state.json';save(path,state);save(BATCH/'setup-state-identity.json',ident(path.read_bytes()))
def load_state():
 idx=next(i for i,b in enumerate(bp['batches']) if b['id']==batch_id);previous=P/'batches'/bp['batches'][idx-1]['id'];path=previous/'setup-state.json'
 ex=json.loads((previous/'exit.json').read_bytes());res=json.loads((previous/'raw/RESULT.json').read_bytes())
 assert ex['returncode']==0 and not ex['timed_out'] and res['result']=='PASS'
 assert ident(path.read_bytes())==json.loads((previous/'setup-state-identity.json').read_bytes())
 state=json.loads(path.read_bytes());assert state['source_test_identity']==ident(fixed)
 for k in ('fast','cat','representatives','summaries'):g[k]=state[k]
 g['coverage']={tuple(x) for x in state['coverage']};g['occurrences']=set(state['occurrences']);g['GUARD']['forbidden_calls']+=state['guard']['forbidden_calls']
 save(BATCH/'consumed-state.json',{'path':str(path),'identity':ident(path.read_bytes()),'meaning':'Exact pure-model setup from prior successful batch; not authenticated basis and not assertion credit.'})
try:
 # Same candidate module loader, same exact guard functions and forbidden code objects.
 execute(statements(44,44));execute(statements(49,53));phase('modules-loaded-original-guards-active')
 if spec['mode']=='matrix-initial':
  execute(statements(56,58));execute(statements(88,88))
 else:
  load_state();g['fixtures']=json.loads((ROOT/'fixtures/retained-decref-cases.json').read_bytes())
 if spec['mode'] in ('matrix-initial','matrix-rest'):
  outer=copy.deepcopy(next(n for n in main.body if isinstance(n,ast.For) and n.lineno==89))
  lo,hi=spec['fixture_start'],spec['fixture_stop']
  # Retain original enumerate indices. Only setup needed for this batch/aggregate is reconstructed.
  guard=ast.parse('if not (FIXTURE_LO <= num < FIXTURE_HI):\n continue').body[0]
  outer.body.insert(0,guard);g['FIXTURE_LO']=lo;g['FIXTURE_HI']=hi
  inner=next(n for n in outer.body if isinstance(n,ast.For) and n.lineno==91)
  inner.body.insert(0,ast.parse("phase('matrix-setup-start', fixture=num, branch=branch, assertion_credit=False)").body[0])
  inner.body.append(ast.parse("phase('matrix-setup-complete', fixture=num, branch=branch, recorded_rows=len(ROWS))").body[0])
  g['phase']=phase;next_original=45 if lo==0 else 45+lo*6
  execute([outer],wrap=True);assert next_original==45+hi*6
  g['write'](RAW/'normal-model-identities.json',g['summaries'])
 elif spec['mode']=='context-one':
  next_original=189;execute(statements(105,105),wrap=True)
  loop=copy.deepcopy(next(n for n in main.body if isinstance(n,ast.For) and n.lineno==106))
  loop.body.insert(0,ast.parse("if ctx != 'SYMBOLIC-U-ONE':\n continue").body[0]);execute([loop],wrap=True);assert next_original==252
 elif spec['mode']=='context-two':
  next_original=252;loop=copy.deepcopy(next(n for n in main.body if isinstance(n,ast.For) and n.lineno==106))
  loop.body.insert(0,ast.parse("if ctx != 'SYMBOLIC-U-TWO':\n continue").body[0]);execute([loop],wrap=True);assert next_original==314
 else:
  next_original=314;execute(statements(136,139),wrap=True);assert next_original==317
 assert [r['original_sequence'] for r in g['ROWS']]==spec['sequences'] and cursor==len(spec['sequences']),'BATCH-COVERAGE'
 assert not any(r['original_sequence']<=145 for r in g['ROWS']),'COMPLETED-ASSERTION-REPLAY'
 save_state();phase('batch-checks-complete',recorded_rows=len(g['ROWS']),guard=dict(g['GUARD']))
 sys.setprofile(None)
 result={'result':'PASS','batch':batch_id,'rows':len(g['ROWS']),'original_sequences':spec['sequences'],'counts':{s:sum(r['status']==s for r in g['ROWS']) for s in ('PASS','REJECTED','FAIL')},'seconds':time.monotonic()-started,'utc':utc(),
 'skipped_original_assertions_without_evaluation':skipped,'guard':g['GUARD'],'public_authentication':'UNEXECUTED','authenticated_constructed_path':'UNEXECUTED','full_public_negative_derivations':0,'setup_credit':0,'candidate_unchanged':True}
 save(RAW/'RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
except BaseException as e:
 sys.setprofile(None);traceback.print_exc();save(RAW/'FAILURE.json',{'utc':utc(),'type':type(e).__name__,'message':str(e),'completed_rows':len(g['ROWS']),'current_original_sequence':current['original_sequence'] if current else None,'next_original_sequence':next_original,'guard':g['GUARD']});raise
