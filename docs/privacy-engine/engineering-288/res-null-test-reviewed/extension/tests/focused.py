"""One focused pure-source/model pass. No authenticated basis/core or public run."""
import ast,copy,hashlib,json,os,sys,time,traceback,types
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=False)
D=copy.deepcopy;ROWS=[];START=time.monotonic();FORBIDDEN=set();GUARD={'forbidden_calls':0}
def utc():return datetime.now(timezone.utc).isoformat()
def write(path,value):
 with open(path,'x') as f:json.dump(value,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def record(name,layer,status,detail=None):
 row={'sequence':len(ROWS)+1,'utc':utc(),'name':name,'layer':layer,'status':status,'detail':detail};ROWS.append(row);write(OUT/('%04d.json'%len(ROWS)),row)
 with open(OUT/'progress.jsonl','a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(row,sort_keys=True),flush=True)
def check(name,fn,layer='pure source/model oracle; no authentication'):
 try:
  if fn() is False:raise AssertionError(name)
 except BaseException as e:record(name,layer,'FAIL',type(e).__name__+': '+str(e));raise
 record(name,layer,'PASS')
def reject(name,fn,layer='pure model constraints; no authenticated basis'):
 try:fn()
 except ValueError as e:record(name,layer,'REJECTED',str(e));return
 record(name,layer,'FAIL','expected ValueError');raise AssertionError(name)
def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def change(v,path,val):
 q=D(v);p=q
 for k in path[:-1]:p=p[k]
 p[path[-1]]=val;return q
def profile(frame,event,arg):
 if event=='call' and frame.f_code in FORBIDDEN:
  GUARD['forbidden_calls']+=1;raise RuntimeError('DEFERRED-AUTHENTICATION-PATH-CALLED')
def audit(event,args):
 if event in ('subprocess.Popen','os.system','sqlite3.connect','socket.connect','socket.bind'):raise RuntimeError('OUT-OF-SCOPE:'+event)
sys.addaudithook(audit)
class S(str):pass
class I(int):pass
class L(list):pass
class Q(dict):pass
class B(bytes):pass
NORMAL_FAST={
 'immortal':[{'stage':'decref-fast:'+a,'outcome':b} for a,b in [('continuation','normal'),('operand','bound'),('immortal-test','true'),('break','taken'),('macro-end','completed')]],
 'non-immortal-positive-gt-one':[{'stage':'decref-fast:'+a,'outcome':b} for a,b in [('continuation','normal'),('operand','bound'),('immortal-test','false'),('statistics','no-op'),('decrement-zero-test','nonzero'),('macro-end','completed')]]}
def main():
 m=json.loads((ROOT/'MANIFEST.json').read_bytes())
 check('fixed source checkpoint membership and hashes',lambda:{p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}==set(m)|{'MANIFEST.json'} and all({'bytes':len((ROOT/n).read_bytes()),'sha256':hashlib.sha256((ROOT/n).read_bytes()).hexdigest()}==v for n,v in m.items()),'checkpoint identity; no candidate authentication')
 old=(ROOT/'reference/fast/code/managed_coverage.py').read_bytes();new=(ROOT/'code/managed_coverage.py').read_bytes()
 check('505497-byte producer prefix unchanged',lambda:len(old)==505497 and hashlib.sha256(old).hexdigest()=='3eab9cde9fd0f83eee2ffea7b68e2ca8db0596cdf367fa86c112917c6ec7e96d' and new.startswith(old),'source preservation')
 check('actual seven appended source functions',lambda:[n.name for n in ast.parse(new[len(old):]).body if isinstance(n,ast.FunctionDef)]==['res_null_sources','res_null_catalogue','compile_res_null','validate_res_null','res_null_binding','res_null_projection','validate_res_null_projection'],'source preservation')
 c=load(ROOT/'code/managed_coverage.py','res_null_producer');a=load(ROOT/'code/correspondence.py','res_null_adapter')
 FORBIDDEN.update(getattr(a,n).__code__ for n in ('_basis','_construct_checked','constructed_projection','derive','validate','inputs','parent_root','_assemble'))
 sys.setprofile(profile)
 files={n:(ROOT/'reference/resolution/source'/n).read_bytes() for n in json.loads((ROOT/'reference/resolution/source-index.json').read_bytes())}
 bc=files['Python/bytecodes.c'].decode().splitlines();gc=files['Python/generated_cases.c.h'].decode().splitlines()
 check('independent exact C source comparison and order',lambda:[s.strip() for s in bc[2514:2519]]==['res = _PyObject_CallNoArgs(enter);','Py_DECREF(enter);','if (res == NULL) {','Py_DECREF(exit);','ERROR_IF(true, error);'],'defining-source oracle independent of generated declarations')
 check('generated local pointer type, test and excluded branch operations',lambda:gc[3498].strip()=='PyObject *res;' and [s.strip() for s in gc[3528:3533]]==['res = _PyObject_CallNoArgs(enter);','Py_DECREF(enter);','if (res == NULL) {','Py_DECREF(exit);','if (true) goto pop_1_error;'] and gc[3535].strip()=='STACK_GROW(1);','defining-source oracle independent of generated declarations')
 cats=[json.loads((ROOT/'fixtures'/n).read_bytes()) for n in ['r1-catalogue.json','lookup-catalogue.json','enter-catalogue.json','return-catalogue.json','decref-catalogue.json']]
 args=((ROOT/'source-evidence/lab_bootstrap.py').read_bytes(),files['Python/bytecodes.c'],(ROOT/'reference/cpython-3.12.14/typeobject.c').read_bytes(),*cats,files)
 fast=c.compile_decref_fast(*args);newargs=(*args[:-1],fast,files);cat=c.compile_res_null(*newargs);write(OUT/'catalogue.json',cat)
 check('new independent source-derived catalogue accepted',lambda:c.validate_res_null(*newargs,D(cat)),'pure catalogue correspondence; no authentication')
 check('comparison cases independent oracle',lambda:cat['result_by_completed_C_class']=={'C-NULL':True,'non-NULL/opaque':False,'non-NULL/Python-None':False} and cat['order']==['res-null:continuation','res-null:comparison'])
 for path,val in [(('source','test','line'),2516),(('source','generated_test','line'),3530),(('source','storage_declaration','expression'),'PyObject *exit;'),(('source','comparison'),'Python truth testing'),(('result_by_completed_C_class','non-NULL/Python-None'),True),(('result_by_completed_C_class','C-NULL'),False),(('order',),cat['order'][::-1]),(('declarations',),cat['declarations'][:-1]),(('steps',1,'allowed'),['true','false','raise']), (('required_predecessor_facts',),[]), (('guard_branches','fast_branches'),['immortal'])]:
  reject('catalogue altered '+repr(path),lambda path=path,val=val:c.validate_res_null(*newargs,change(cat,path,val)),'independent source-derived catalogue comparison')
 q=D(cat);q['source']['test']['expression']='if (res != NULL) {';q['result_by_completed_C_class']={k:not v for k,v in q['result_by_completed_C_class'].items()}
 reject('coordinated predicate and decision inversion',lambda:c.validate_res_null(*newargs,q),'independent source-derived catalogue comparison')
 for name,oldtext,newtext in [('Python/bytecodes.c',b'if (res == NULL)',b'if (exit == NULL)'),('Python/generated_cases.c.h',b'if (res == NULL)',b'if (res != NULL)')]:
  fs=dict(files);fs[name]=fs[name].replace(oldtext,newtext);reject('source substitution '+name,lambda fs=fs:c.res_null_sources(fs),'defining source gate; no model authentication')
 defs={n.name:ast.unparse(n) for n in ast.parse((ROOT/'code/correspondence.py').read_bytes()).body if isinstance(n,ast.FunctionDef)}
 check('unchanged substantive predecessor authentication and exact receipt comparison wired',lambda:'p._basis(pd)' in defs['_basis'] and "fresh['saved'] == p.enc(p._assemble(pb))" in defs['_basis'] and 'compile_res_null' in defs['_basis'],'static wiring only; public authentication UNEXECUTED')
 check('actual parent constructed validation mandatory before binding',lambda:"basis['parent_module']._construct_checked(basis['parent_basis']" in defs['_construct_checked'] and defs['_construct_checked'].index('._construct_checked(')<defs['_construct_checked'].index('c.res_null_binding(') and 'validate_res_null_projection' in defs['_construct_checked'],'static wiring only; authenticated constructed path UNEXECUTED')
 check('mandatory rows and exact public receipt comparison wired',lambda:'ctx[RELATION]' in defs['_assemble'] and '_assemble(_basis(inputs(root)))' in defs['derive'] and 'saved == enc(result)' in defs['validate'],'static wiring only; no public derivation')
 shape={'format':'I164-RES-NULL-TEST-1','contexts':[{'context':ctx,'res_null_test_correspondence':{},'decref_fast_completion_correspondence':{}} for ctx in a.CONTEXTS]}
 check('receipt shape gate positive only',lambda:a._receipt_shape(a.enc(shape))==shape,'pre-derivation shape gate only; not public positive')
 for i in range(2):
  for k in ('res_null_test_correspondence','decref_fast_completion_correspondence'):
   q=D(shape);del q['contexts'][i][k];reject('omitted mandatory relation '+str(i)+'/'+k,lambda q=q:a._receipt_shape(a.enc(q)),'pre-derivation shape gate only; no full public negative')
 q=D(shape);q['contexts'].reverse();reject('reordered contexts',lambda:a._receipt_shape(a.enc(q)),'pre-derivation shape gate only')
 # Read-only expected declaration rows from the retained receipt, explicitly not an authenticated basis.
 prior=json.loads((ROOT/'reference/fast/actual-receipt.json').read_bytes());marker={'meaning':'offline row construction only; no authentication performed'}
 rows=a.declaration_rows(prior,cat,marker)
 check('both saved-input mandatory declaration rows accepted',lambda:a.validate_declaration_rows(prior,cat,marker,rows),'pure mandatory-row comparison against retained inputs; no basis')
 for i in range(2):
  for path,val in [((i,'context'),'wrong'),((i,'instance_anchor','context'),'wrong'),((i,'conditional_links',),[]),((i,'test_outcome'),False),((i,'declaration','order'),[])]:
   reject('row mutation '+repr(path),lambda path=path,val=val:a.validate_declaration_rows(prior,cat,marker,change(rows,path,val)),'pure mandatory-row comparison; not public/core validation')
 reject('missing second mandatory row',lambda:a.validate_declaration_rows(prior,cat,marker,rows[:1]),'pure mandatory-row comparison')
 r=a.declaration_rows(prior,cat,marker);r[0]['declaration']['steps'].clear();r[1]['instance_anchor'].clear()
 reject('direct returned rows mutated',lambda:a.validate_declaration_rows(prior,cat,marker,r),'pure mandatory-row comparison after direct output mutation')
 check('mandatory row expectations isolated',lambda:a.declaration_rows(prior,cat,marker)==rows)
 fixtures=json.loads((ROOT/'fixtures/retained-decref-cases.json').read_bytes());coverage=set();representatives={};summaries=[];occurrences=set()
 for num,f in enumerate(fixtures):
  p=f['output'];ctx=p['scope']['context']
  for branch in NORMAL_FAST:
   pb=c.decref_fast_binding(fast,p,p['instance_anchor'],'explicit conditional premise',branch,c.decref_fast_envelope(),files)
   pv={'scope':D(p['scope']),'anchor':D(p['instance_anchor']),'parent_result':D(p),'binding':pb,'outcomes':D(NORMAL_FAST[branch])}
   fp=c.decref_fast_projection(fast,pv,pv,files)
   b=c.res_null_binding(cat,fp,fp['instance_anchor'],'explicit conditional premise','explicit conditional premise',files)
   oo=[{'stage':'res-null:continuation','outcome':'normal'},{'stage':'res-null:comparison','outcome':'true' if p['res_value_role']['C_NULL'] else 'false'}]
   v={'scope':D(fp['scope']),'anchor':D(fp['instance_anchor']),'parent_result':D(fp),'binding':b,'outcomes':oo};out=c.res_null_projection(cat,v,v,files)
   label=str(num)+'/'+branch;expected=p['res_value_role']['C_NULL'];coverage.add((ctx,p['earlier_control_completed_in_model'],p['failure_origin_region'],branch,p['res_value_role']['C_NULL'],p['res_value_role']['python_value_class']));occurrences.add(out['events'][-1]['id'])
   check(label+'/normal comparison accepted',lambda:c.validate_res_null_projection(cat,v,v,out,files),'pure model output comparison; no authenticated basis')
   check(label+'/independent outcome and preserved lineage oracle',lambda:out['res_null_test_outcome'] is expected and out['res_null_test_completed_in_model'] is True and out['res_value_role']==p['res_value_role'] and out['predecessor_projection']==fp and out['binding']['assignment']==p['res_assignment'] and out['last_pending_error_in_model']==fp['last_pending_error_in_model'] and out['helper_error_indicator']=='UNKNOWN' and out['terminal_python_exception_in_model'] is True and out['current_partial_effects'].startswith('UNKNOWN') and all(out[k] is False for k in ['exit_decref_attempt_established','stack_operations_established','dispatch_established','context_manager_entry_established','f_binding_established','physical_release_established','qualified_binary_correspondence','actual_admission']))
   reject(label+'/opposite comparison result',lambda:c.validate_res_null_projection(cat,v,v,change(out,('res_null_test_outcome',),not expected),files),'pure model output comparison')
   summaries.append({'fixture':num,'branch':branch,'context':ctx,'expected_result':expected,'output_identity':a.identity(c.enc(out)),'qualification':'constructed pure model only; no authenticated constructed path or runtime observation'})
   if branch=='immortal' and p['res_value_role']['python_value_class']=='opaque' and ctx not in representatives:representatives[ctx]=(D(v),D(out))
 write(OUT/'normal-model-identities.json',summaries)
 check('48 class variants cover both contexts prefixes origins fast branches and three result classes',lambda:len(coverage)==48 and len(fixtures)==24 and len(occurrences)==8)
 for ctx,(v,out) in representatives.items():
  fp=v['parent_result']
  for premise in ('continuation','res_storage_continuity'):
   q=D(v);q['binding'][premise]='UNESTABLISHED';q['outcomes']=[{'stage':'res-null:continuation','outcome':'unobserved'}];z=c.res_null_projection(cat,q,q,files)
   check(ctx+'/'+premise+' unavailable has no outcome',lambda:z['res_null_test_outcome'] is None and z['res_null_test_completed_in_model'] is False and z['terminal_python_exception_in_model'] is None)
   q['outcomes']=D(v['outcomes']);reject(ctx+'/'+premise+' unavailable cannot compare',lambda q=q:c.res_null_projection(cat,q,q,files))
   q=D(v);del q['binding'][premise];reject(ctx+'/'+premise+' omitted cannot compare',lambda q=q:c.res_null_projection(cat,q,q,files))
  for k in ('conditional_fast_completion_in_model','helper_c_return_completed_in_model','res_assignment_established','res_assignment','res_value_role'):
   q=D(fp);q.pop(k);reject(ctx+'/missing predecessor '+k,lambda q=q:c.res_null_binding(cat,q,v['anchor'],'explicit conditional premise','explicit conditional premise',files),'predecessor premise gate; no inferred comparison outcome')
  for index,frontiers in [(0,('raise','catchable-interruption','process-termination','unobserved')),(1,('interruption','process-termination','unobserved'))]:
   for frontier in frontiers:
    q=D(v);q['outcomes']=q['outcomes'][:index+1];q['outcomes'][-1]['outcome']=frontier;z=c.res_null_projection(cat,q,q,files);uncertain=frontier in ('interruption','process-termination','unobserved')
    check(ctx+'/'+str(index)+'/'+frontier,lambda z=z,uncertain=uncertain:z['res_null_test_outcome'] is None and not z['res_null_test_completed_in_model'] and z['terminal_python_exception_in_model'] is (None if uncertain else True) and z['original_error_pending_in_outer_handler']==fp['original_error_pending_in_outer_handler'] and z['conditional_fast_completion_in_model'] is True and z['C_primitive_python_exception_established'] is False and z['Python_unwind_established'] is False)
    reject(ctx+'/'+frontier+'/false outcome',lambda q=q,z=z:c.validate_res_null_projection(cat,q,q,change(z,('res_null_test_outcome',),False),files),'pure model output comparison at first nonnormal frontier')
  for path,val in [(('scope','invocation'),'wrong'),(('scope','acquisition'),'wrong'),(('anchor','context'),'wrong'),(('binding','res_storage_role','symbol'),'wrong'),(('binding','res_storage_role','assignment_occurrence'),'wrong'),(('binding','res_value_role','C_NULL'),True),(('binding','enter_role',),v['binding']['exit_role']),(('binding','references','owner','symbol'),'wrong'),(('binding','references','token','symbol'),'wrong'),(('binding','original_constructor_error','symbol'),'wrong'),(('binding','selected_fast_completion','id'),'stale'),(('binding','fast_branch'),'zero-count'),(('binding','assignment','from_return_occurrence'),'wrong'),(('outcomes',),v['outcomes'][::-1]),(('outcomes',),v['outcomes'][:1]),(('outcomes',),v['outcomes']+[v['outcomes'][-1]]),(('outcomes',1,'outcome'),'raise'),(('outcomes',1,'outcome'),'true')]:
   q=change(v,path,val);reject(ctx+'/input '+repr(path),lambda q=q:c.res_null_projection(cat,q,q,files),'pure model lineage/order/guard comparison')
  q=D(v);q['binding']['references']['owner']['symbol']='coordinated';q['scope']['invocation']='coordinated'
  reject(ctx+'/coordinated submitted lineage versus fixed selected input',lambda:c.res_null_projection(cat,q,v,files),'pure selected-input comparison; no authenticated basis')
  for path,val in [(('res_null_test_outcome',),0),(('res_null_test_completed_in_model',),1),(('terminal_python_exception_in_model',),False),(('new_model_claims','branch_body_entered'),True),(('exit_decref_attempt_established',),True),(('stack_operations_established',),True),(('runtime_test_arrival',),True),(('helper_error_indicator',),'CLEAR')]:
   reject(ctx+'/output '+repr(path),lambda path=path,val=val:c.validate_res_null_projection(cat,v,v,change(out,path,val),files),'pure model output comparison')
  for path,val in [(('outcomes',),L(v['outcomes'])),(('outcomes',0,'outcome'),S('normal')),(('binding','references',),Q(v['binding']['references']))]:
   q=change(v,path,val);reject(ctx+'/exact input '+repr(path),lambda q=q:c.res_null_projection(cat,q,v,files),'exact input types before normalization')
  for path,val in [(('completion',),S(out['completion'])),(('events',),L(out['events'])),(('new_model_claims',),Q(out['new_model_claims']))]:
   reject(ctx+'/exact output '+repr(path),lambda path=path,val=val:c.validate_res_null_projection(cat,v,v,change(out,path,val),files),'exact output types before normalization')
  q=D(out);q['new_model_claims'][S('res_equals_C_NULL')]=q['new_model_claims'].pop('res_equals_C_NULL');reject(ctx+'/subclass literal key',lambda:c.validate_res_null_projection(cat,v,v,q,files),'exact key types before normalization')
  before_v=D(v);before_cat=D(cat);r=c.res_null_projection(cat,v,v,files);r['binding']['res_storage_role']['symbol']='mutated';r['events'].clear();r['predecessor_projection']['res_value_role']['C_NULL']=True
  reject(ctx+'/direct returned projection mutation',lambda:c.validate_res_null_projection(cat,v,v,r,files),'pure model output comparison after direct returned mutation')
  check(ctx+'/pristine expectations isolated',lambda:v==before_v and cat==before_cat and c.res_null_projection(cat,v,v,files)==out)
  r=c.res_null_binding(cat,fp,v['anchor'],'explicit conditional premise','explicit conditional premise',files);r['assignment']['value'].clear();r['references'].clear()
  check(ctx+'/returned binding isolation',lambda:c.res_null_binding(cat,fp,v['anchor'],'explicit conditional premise','explicit conditional premise',files)==v['binding'] and v==before_v)
 r=c.res_null_catalogue(fast,files);r['source']['definition_identities'].clear();r['result_by_completed_C_class'].clear()
 check('returned catalogue isolation',lambda:c.res_null_catalogue(fast,files)==cat)
 check('new authentication paths remain unexecuted',lambda:GUARD['forbidden_calls']==0,'execution guard; no acceptance claim for unexecuted paths')
 check('fixed source bytes unchanged after pass',lambda:all({'bytes':len((ROOT/n).read_bytes()),'sha256':hashlib.sha256((ROOT/n).read_bytes()).hexdigest()}==pin for n,pin in m.items()),'source preservation')
 return {'public_authentication':'UNEXECUTED','authenticated_constructed_path':'UNEXECUTED','public_runs':0,'full_public_negative_derivations':0,'runtime_source_execution':0,'historical_campaign_replays':0,'independent_acceptance':'PENDING','prior_groups':'151 independent 81/70; 399 Engineering 196/203; one saved public positive; all older groups separate','guard':GUARD}
try:
 details=main();sys.setprofile(None);result={'result':'PASS','rows':len(ROWS),'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')},'finished_utc':utc(),'seconds':time.monotonic()-START,'python':sys.version,'qualifications':details};write(OUT/'RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
except BaseException as e:
 sys.setprofile(None);traceback.print_exc();write(OUT/'FAILURE.json',{'utc':utc(),'exception':type(e).__name__,'message':str(e),'completed_rows':len(ROWS),'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')}});raise
