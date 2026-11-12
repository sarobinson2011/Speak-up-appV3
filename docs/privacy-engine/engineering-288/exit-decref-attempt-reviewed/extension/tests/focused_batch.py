"""Fresh bounded pure-source/model checks only. Never authenticate or run application code."""
import ast,copy,hashlib,json,os,sys,time,traceback,types
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BATCH=sys.argv[1];OUT=Path(sys.argv[2]);OUT.mkdir(parents=True,exist_ok=False)
D=copy.deepcopy;ROWS=[];START=time.monotonic();FORBIDDEN=set();GUARD={'forbidden_calls':0};phase_seq=0
def utc():return datetime.now(timezone.utc).isoformat()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(path,v):
 with open(path,'x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def phase(name,detail=None):
 global phase_seq
 phase_seq+=1;r={'event':'phase','sequence':phase_seq,'utc':utc(),'seconds':time.monotonic()-START,'name':name,'detail':detail}
 with open(OUT/'phases.jsonl','a') as f:f.write(json.dumps(r,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(r,sort_keys=True),flush=True)
def record(name,layer,status,start,detail=None):
 r={'batch':BATCH,'sequence':len(ROWS)+1,'utc':utc(),'seconds':time.monotonic()-start,'name':name,'layer':layer,'status':status,'detail':detail};ROWS.append(r);write(OUT/('%04d.json'%len(ROWS)),r)
 with open(OUT/'progress.jsonl','a') as f:f.write(json.dumps(r,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps({'event':'CONTROL','row':r},sort_keys=True),flush=True)
def check(name,fn,layer='pure source/model oracle; no authentication'):
 start=time.monotonic()
 try:
  if fn() is False:raise AssertionError(name)
 except BaseException as e:record(name,layer,'FAIL',start,type(e).__name__+': '+str(e));raise
 record(name,layer,'PASS',start)
def reject(name,fn,layer='pure model constraints; no authenticated basis'):
 start=time.monotonic()
 try:fn()
 except ValueError as e:record(name,layer,'REJECTED',start,str(e));return
 record(name,layer,'FAIL',start,'expected ValueError');raise AssertionError(name)
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
 if event=='exec' and str(args[0].co_filename).startswith(str(ROOT/'source-evidence')):raise RuntimeError('APPLICATION-SOURCE-EXECUTION-FORBIDDEN')
sys.addaudithook(audit)
class S(str):pass
class I(int):pass
class L(list):pass
class Q(dict):pass
FAST={
 'immortal':[{'stage':'decref-fast:'+a,'outcome':b} for a,b in [('continuation','normal'),('operand','bound'),('immortal-test','true'),('break','taken'),('macro-end','completed')]],
 'non-immortal-positive-gt-one':[{'stage':'decref-fast:'+a,'outcome':b} for a,b in [('continuation','normal'),('operand','bound'),('immortal-test','false'),('statistics','no-op'),('decrement-zero-test','nonzero'),('macro-end','completed')]]}
NORMAL=[{'stage':'exit-decref:continuation','outcome':'normal'},{'stage':'exit-decref:attempt','outcome':'attempted'}]
def setup():
 phase('fixed source identity')
 m=json.loads((ROOT/'MANIFEST.json').read_bytes());found={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
 if found!=set(m)|{'MANIFEST.json'} or not all(identity((ROOT/n).read_bytes())==v for n,v in m.items()):raise RuntimeError('SOURCE-MANIFEST-MISMATCH')
 c=load(ROOT/'code/managed_coverage.py','exit_decref_producer');a=load(ROOT/'code/correspondence.py','exit_decref_adapter')
 FORBIDDEN.update(getattr(a,n).__code__ for n in ('_basis','_construct_checked','constructed_projection','derive','validate','inputs','parent_root','_assemble','_rows'))
 sys.setprofile(profile)
 phase('compile conditional source catalogues; setup only')
 files={n:(ROOT/'reference/resolution/source'/n).read_bytes() for n in json.loads((ROOT/'reference/resolution/source-index.json').read_bytes())}
 cats=[json.loads((ROOT/'fixtures'/n).read_bytes()) for n in ['r1-catalogue.json','lookup-catalogue.json','enter-catalogue.json','return-catalogue.json','decref-catalogue.json']]
 args=((ROOT/'source-evidence/lab_bootstrap.py').read_bytes(),files['Python/bytecodes.c'],(ROOT/'reference/cpython-3.12.14/typeobject.c').read_bytes(),*cats)
 fast=c.compile_decref_fast(*args,files);res=c.compile_res_null(*args,fast,files);cat=c.compile_exit_decref(*args,fast,res,files)
 phase('catalogue setup completed');return c,a,files,args,fast,res,cat,m
def parent(c,files,fast,res,fixture,branch):
 p=fixture['output'];pb=c.decref_fast_binding(fast,p,p['instance_anchor'],'explicit conditional premise',branch,c.decref_fast_envelope(),files)
 pv={'scope':D(p['scope']),'anchor':D(p['instance_anchor']),'parent_result':D(p),'binding':pb,'outcomes':D(FAST[branch])};fp=c.decref_fast_projection(fast,pv,pv,files)
 b=c.res_null_binding(res,fp,fp['instance_anchor'],'explicit conditional premise','explicit conditional premise',files)
 v={'scope':D(fp['scope']),'anchor':D(fp['instance_anchor']),'parent_result':fp,'binding':b,'outcomes':[{'stage':'res-null:continuation','outcome':'normal'},{'stage':'res-null:comparison','outcome':'true' if p['res_value_role']['C_NULL'] else 'false'}]}
 return c.res_null_projection(res,v,v,files)
def case(c,files,cat,p):
 b=c.exit_decref_binding(cat,p,p['instance_anchor'],'explicit conditional premise','explicit conditional premise',files)
 return {'scope':D(p['scope']),'anchor':D(p['instance_anchor']),'parent_result':p,'binding':b,'outcomes':D(NORMAL)}
def source_rows(c,a,files,args,fast,res,cat):
 old=(ROOT/'reference/res-null/code/managed_coverage.py').read_bytes();new=(ROOT/'code/managed_coverage.py').read_bytes()
 check('519785-byte parent prefix preserved',lambda:len(old)==519785 and new.startswith(old),'exact source preservation')
 check('seven functions appended',lambda:[x.name for x in ast.parse(new[len(old):]).body if isinstance(x,ast.FunctionDef)]==['exit_decref_sources','exit_decref_catalogue','compile_exit_decref','validate_exit_decref','exit_decref_binding','exit_decref_projection','validate_exit_decref_projection'],'source preservation')
 bc=files['Python/bytecodes.c'].decode().splitlines();gc=files['Python/generated_cases.c.h'].decode().splitlines()
 check('independent true-guard/exit-operand/excluded-routing source order',lambda:[x.strip() for x in bc[2516:2519]]==['if (res == NULL) {','Py_DECREF(exit);','ERROR_IF(true, error);'] and [x.strip() for x in gc[3530:3533]]==['if (res == NULL) {','Py_DECREF(exit);','if (true) goto pop_1_error;'],'defining-source oracle independent of submitted catalogue')
 check('independent exit origin/storage source',lambda:bc[2501].strip()=='exit = _PyObject_LookupSpecial(mgr, &_Py_ID(__exit__));' and gc[3497].strip()=='PyObject *exit;','defining-source oracle')
 check('catalogue positive',lambda:c.validate_exit_decref(*args,fast,res,files,cat),'independent source-derived catalogue comparison')
 for path,val in [(('source','operation','line'),2516),(('source','operation','expression'),'Py_DECREF(enter);'),(('source','generated_operation','line'),3530),(('source','exit_lookup','line'),2492),(('guard_branches','comparison_required'),False),(('required_predecessor_facts',),[]),(('steps',),cat['steps'][:1]),(('order',),cat['order'][::-1]),(('declarations',),cat['declarations'][:1]),(('guard_branches','prefixes'),[]),(('guard_branches','origins'),[]),(('guard_branches','fast_branches'),['immortal'])]:
  reject('catalogue '+repr(path),lambda path=path,val=val:c.validate_exit_decref(*args,fast,res,files,change(cat,path,val)),'independent source-derived catalogue comparison')
 for name in ('Python/bytecodes.c','Python/generated_cases.c.h'):
  fs=dict(files);fs[name]=fs[name].replace(b'Py_DECREF(exit);',b'Py_DECREF(enter);');reject('wrong defining operand '+name,lambda fs=fs:c.exit_decref_sources(fs),'defining-source byte/line gate')
 defs={n.name:ast.unparse(n) for n in ast.parse((ROOT/'code/correspondence.py').read_bytes()).body if isinstance(n,ast.FunctionDef)}
 check('actual parent authentication and receipt equality wired',lambda:'p._basis(pd)' in defs['_basis'] and "fresh['saved'] == p.enc(p._assemble(pb))" in defs['_basis'] and 'compile_exit_decref' in defs['_basis'],'static integration only; authentication UNEXECUTED')
 check('actual predecessor constructed validation precedes new binding',lambda:defs['_construct_checked'].index('._construct_checked(')<defs['_construct_checked'].index('c.exit_decref_binding(') and 'validate_exit_decref_projection' in defs['_construct_checked'],'static integration only; authenticated constructed path UNEXECUTED')
 check('new format and inherited component history preserved',lambda:"I164-EXIT-DECREF-ATTEMPT-1" in defs['_assemble'] and "out['prior_res_null_components']" in defs['_assemble'] and "out['prior_decref_fast_components']" not in defs['_assemble'] and 'ctx[RELATION]' in defs['_assemble'] and 'saved == enc(result)' in defs['validate'],'static integration; no receipt derivation')
 check('constructed shape matches producer kind',lambda:"CONSTRUCTED-EXIT-DECREF-ATTEMPT" in defs['_construct_checked'],'static shape audit')
 shape={'format':'I164-EXIT-DECREF-ATTEMPT-1','contexts':[{'context':ctx,a.RELATION:{},'res_null_test_correspondence':{}} for ctx in a.CONTEXTS]}
 check('receipt shape accepted',lambda:a._receipt_shape(a.enc(shape))==shape,'pre-derivation shape gate only; not public validation')
 for i in range(2):
  for key in (a.RELATION,'res_null_test_correspondence'):
   q=D(shape);del q['contexts'][i][key];reject('missing relation '+str(i)+'/'+key,lambda q=q:a._receipt_shape(a.enc(q)),'pre-derivation shape gate only')
 prior=json.loads((ROOT/'reference/res-null/actual-receipt.json').read_bytes());marker={'meaning':'offline row construction from retained receipt, not an authenticated basis'};rows=a.declaration_rows(prior,cat,marker)
 check('both mandatory rows accepted',lambda:a.validate_declaration_rows(prior,cat,marker,rows),'pure mandatory-row comparison; no authenticated basis')
 for i in range(2):
  for path,val in [((i,'context'),'wrong'),((i,'instance_anchor','context'),'wrong'),((i,'conditional_links'),[]),((i,'classification'),'KNOWN'),((i,'multiplicity'),0),((i,'comparison_outcome'),True),((i,'exit_decref_attempt'),True),((i,'decrement_completion'),True),((i,'declaration','order'),[]),((i,'runtime_arrival'),True)]:
   reject('row '+repr(path),lambda path=path,val=val:a.validate_declaration_rows(prior,cat,marker,change(rows,path,val)),'pure mandatory-row comparison')
 reject('missing second row',lambda:a.validate_declaration_rows(prior,cat,marker,rows[:1]),'pure mandatory-row comparison')
 r=a.declaration_rows(prior,cat,marker);r[0]['declaration']['steps'].clear();r[1]['instance_anchor'].clear()
 reject('direct rows nested mutation',lambda:a.validate_declaration_rows(prior,cat,marker,r),'pure mandatory-row comparison after direct returned mutation')
 check('row expectations isolated',lambda:a.declaration_rows(prior,cat,marker)==rows)
 r=c.exit_decref_catalogue(res,files);r['source']['definition_identities'].clear();r['guard_branches']['comparison_required']=False
 check('catalogue expectations isolated',lambda:c.exit_decref_catalogue(res,files)==cat)
def matrix(c,a,files,fast,res,cat,ctx):
 fixtures=json.loads((ROOT/'fixtures/retained-decref-cases.json').read_bytes());coverage=[];selected=[]
 for num,f in enumerate(fixtures):
  if f['output']['scope']['context']!=ctx:continue
  for branch in FAST:
   label=str(num)+'/'+branch;phase('parent model setup',label);p=parent(c,files,fast,res,f,branch);phase('parent model setup completed',label)
   if not f['output']['res_value_role']['C_NULL']:
    reject(label+'/false comparison cannot supply exit attempt',lambda p=p:c.exit_decref_binding(cat,p,p['instance_anchor'],'explicit conditional premise','explicit conditional premise',files),'pure true-predecessor gate; legitimate opaque/Python-None comparison')
    continue
   v=case(c,files,cat,p);out=c.exit_decref_projection(cat,v,v,files)
   check(label+'/normal attempt accepted',lambda:c.validate_exit_decref_projection(cat,v,v,out,files),'pure output correspondence; conditional model only')
   check(label+'/independent operand/lineage/stop oracle',lambda:out['exit_decref_attempt_in_model'] is True and out['exit_decref_attempt']['operand_role']==p['binding']['exit_role'] and out['binding']['operand_role']['method']=='__exit__' and out['exit_decref_attempt']['source']['line']==2518 and out['exit_decref_attempt']['generated_source']['line']==3532 and out['res_null_test_outcome'] is True and out['last_pending_error_in_model']==p['last_pending_error_in_model'] and out['original_error_pending_in_outer_handler']==p['original_error_pending_in_outer_handler'] and out['helper_error_indicator']=='UNKNOWN' and out['terminal_python_exception_in_model'] is True and out['current_partial_effects'].startswith('UNKNOWN') and all(out[k] is False for k in ('exit_decref_completion_established','exit_macro_expansion_established','exit_refcount_effects_established','exit_destructor_invocation_established','result_error_routing_established','stack_operations_established','dispatch_established','physical_release_established','actual_admission')))
   reject(label+'/completion cannot follow attempt',lambda:c.validate_exit_decref_projection(cat,v,v,change(out,('exit_decref_completion_established',),True),files),'pure submitted-output comparison')
   coverage.append((ctx,p['earlier_control_completed_in_model'],p['failure_origin_region'],branch));selected.append({'fixture':num,'branch':branch,'output':identity(c.enc(out)),'occurrence':out['exit_decref_attempt']['id']})
 write(OUT/'matrix-identities.json',selected)
 check(ctx+'/eight true combinations and distinct selected occurrences',lambda:len(coverage)==8 and len(set(coverage))==8 and len({x['occurrence'] for x in selected})==4,'constructed alternative coverage; fast branches are alternatives, not duplicate runtime occurrences')
def mutations(c,a,files,fast,res,cat,ctx):
 fixtures=json.loads((ROOT/'fixtures/retained-decref-cases.json').read_bytes());f=next(f for f in fixtures if f['output']['scope']['context']==ctx and f['output']['res_value_role']['C_NULL'])
 phase('representative parent setup',ctx);p=parent(c,files,fast,res,f,'immortal');v=case(c,files,cat,p);out=c.exit_decref_projection(cat,v,v,files);phase('representative setup completed')
 for key in ('continuation','exit_role_continuity'):
  q=D(v);q['binding'][key]='UNESTABLISHED';q['outcomes']=[{'stage':'exit-decref:continuation','outcome':'unobserved'}];z=c.exit_decref_projection(cat,q,q,files)
  check(key+'/unobserved only',lambda:z['exit_decref_attempt_in_model'] is False and z['exit_decref_attempt'] is None and z['terminal_python_exception_in_model'] is None)
  q['outcomes']=D(NORMAL);reject(key+'/unestablished cannot attempt',lambda q=q:c.exit_decref_projection(cat,q,q,files),'pure continuation/continuity gate')
  q=D(v);del q['binding'][key];reject(key+'/missing',lambda q=q:c.exit_decref_projection(cat,q,q,files),'pure required-premise gate')
 for key in cat['required_predecessor_facts']:
  q=D(p);q.pop(key);reject('missing predecessor '+key,lambda q=q:c.exit_decref_binding(cat,q,v['anchor'],'explicit conditional premise','explicit conditional premise',files),'pure predecessor gate')
 for index,fronts in [(0,('raise','catchable-interruption','process-termination','unobserved')),(1,('interruption','process-termination','unobserved'))]:
  for front in fronts:
   q=D(v);q['outcomes']=q['outcomes'][:index+1];q['outcomes'][-1]['outcome']=front;z=c.exit_decref_projection(cat,q,q,files);uncertain=front in ('interruption','process-termination','unobserved')
   check(str(index)+'/'+front+'/lineage preserved',lambda z=z,uncertain=uncertain:z['exit_decref_attempt'] is None and z['exit_decref_attempt_in_model'] is False and z['res_null_test_completed_in_model'] is True and z['res_null_test_outcome'] is True and z['original_error_pending_in_outer_handler']==p['original_error_pending_in_outer_handler'] and z['terminal_python_exception_in_model'] is (None if uncertain else True) and z['C_primitive_python_exception_established'] is False and z['Python_unwind_established'] is False)
   reject(str(index)+'/'+front+'/invented attempt',lambda q=q,z=z:c.validate_exit_decref_projection(cat,q,q,change(z,('exit_decref_attempt_in_model',),True),files),'pure submitted-output comparison at nonnormal frontier')
   qq=D(q);qq['outcomes'].append(D(NORMAL[-1]));reject(str(index)+'/'+front+'/continued after frontier',lambda qq=qq:c.exit_decref_projection(cat,qq,qq,files),'pure first-nonnormal/order gate')
 for path,val in [(('scope','invocation'),'wrong'),(('scope','acquisition'),'wrong'),(('scope','instance','binding'),'wrong'),(('anchor','context'),'wrong'),(('binding','operand_role'),v['binding']['enter_role']),(('binding','operand_role'),v['binding']['res_value_role']),(('binding','exit_storage_role','symbol'),'stale'),(('binding','selected_lookup','id'),'wrong'),(('binding','comparison','id'),'wrong'),(('binding','comparison_result'),False),(('binding','references','owner','symbol'),'wrong'),(('binding','references','token','symbol'),'wrong'),(('binding','original_constructor_error','symbol'),'wrong'),(('outcomes',),NORMAL[::-1]),(('outcomes',),NORMAL[:1]),(('outcomes',),NORMAL+[NORMAL[-1]]),(('outcomes',1,'outcome'),'completed'),(('outcomes',1,'outcome'),'raise')]:
  q=change(v,path,val);reject('input '+repr(path),lambda q=q:c.exit_decref_projection(cat,q,q,files),'pure new-layer lineage/operand/order comparison')
 q=D(v);q['scope']['invocation']='coordinated';q['binding']['scope']['invocation']='coordinated';q['binding']['operand_role']['scope']['invocation']='coordinated'
 reject('coordinated new-layer lineage versus selected parent',lambda:c.exit_decref_projection(cat,q,q,files),'pure selected-parent comparison; no authentication')
 q=D(v);q['binding']['operand_role']=D(q['binding']['enter_role']);q['binding']['selected_lookup']['method']='__enter__'
 reject('coordinated role and lookup substitution',lambda:c.exit_decref_projection(cat,q,q,files),'pure selected-parent binding comparison')
 for path,val in [(('exit_decref_attempt_in_model',),1),(('terminal_python_exception_in_model',),False),(('exit_refcount_effects_established',),True),(('exit_destructor_invocation_established',),True),(('result_error_routing_established',),True),(('runtime_exit_decref_arrival',),True),(('helper_error_indicator',),'CLEAR'),(('new_model_claims','decrement_completion'),True),(('exit_decref_attempt','operand_role'),v['binding']['enter_role'])]:
  reject('output '+repr(path),lambda path=path,val=val:c.validate_exit_decref_projection(cat,v,v,change(out,path,val),files),'pure submitted-output comparison')
 for path,val in [(('outcomes',),L(NORMAL)),(('outcomes',0,'outcome'),S('normal')),(('binding','references',),Q(v['binding']['references'])),(('binding','comparison_result'),1)]:
  q=change(v,path,val);reject('input exact '+repr(path),lambda q=q:c.exit_decref_projection(cat,q,v,files),'exact type/selected-input gate before serialization')
 for path,val in [(('completion',),S(out['completion'])),(('events',),L(out['events'])),(('new_model_claims',),Q(out['new_model_claims']))]:
  reject('output exact '+repr(path),lambda path=path,val=val:c.validate_exit_decref_projection(cat,v,v,change(out,path,val),files),'exact output types before normalization')
 q=D(out);q['new_model_claims'][S('selected_exit_decref_attempt')]=q['new_model_claims'].pop('selected_exit_decref_attempt')
 reject('subclass literal key',lambda:c.validate_exit_decref_projection(cat,v,v,q,files),'exact dictionary-key type before normalization')
 before=D(v);beforecat=D(cat);r=c.exit_decref_projection(cat,v,v,files);r['binding']['operand_role'].clear();r['events'].clear();r['predecessor_projection']['binding']['exit_role'].clear()
 reject('direct returned projection nested mutation',lambda:c.validate_exit_decref_projection(cat,v,v,r,files),'pure output comparison after direct returned mutation')
 check('projection expectations isolated',lambda:v==before and cat==beforecat and c.exit_decref_projection(cat,v,v,files)==out)
 r=c.exit_decref_binding(cat,p,v['anchor'],'explicit conditional premise','explicit conditional premise',files);r['references'].clear();r['operand_role']['scope'].clear()
 check('binding expectations isolated',lambda:c.exit_decref_binding(cat,p,v['anchor'],'explicit conditional premise','explicit conditional premise',files)==v['binding'] and v==before)
def main():
 c,a,files,args,fast,res,cat,m=setup()
 if BATCH=='source-rows':source_rows(c,a,files,args,fast,res,cat)
 elif BATCH.startswith('matrix-'):matrix(c,a,files,fast,res,cat,'SYMBOLIC-U-'+('ONE' if BATCH.endswith('one') else 'TWO'))
 elif BATCH.startswith('mutations-'):mutations(c,a,files,fast,res,cat,'SYMBOLIC-U-'+('ONE' if BATCH.endswith('one') else 'TWO'))
 else:raise RuntimeError('UNKNOWN-BATCH')
 check('deferred paths not executed',lambda:GUARD['forbidden_calls']==0,'execution guard; not acceptance of deferred paths')
 check('source identities unchanged',lambda:all(identity((ROOT/n).read_bytes())==pin for n,pin in m.items()),'fixed source preservation')
 sys.setprofile(None);return {'result':'PASS','batch':BATCH,'rows':len(ROWS),'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')},'finished_utc':utc(),'seconds':time.monotonic()-START,'python':sys.version,'public_authentication':'UNEXECUTED','authenticated_constructed_path':'UNEXECUTED','full_public_negative_derivations':0,'guard':GUARD,'independent_acceptance':'PENDING'}
try:
 result=main();write(OUT/'RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
except BaseException as e:
 sys.setprofile(None);traceback.print_exc();write(OUT/'FAILURE.json',{'utc':utc(),'exception':type(e).__name__,'message':str(e),'completed_rows':len(ROWS)});raise
