"""Formal-Lab[6] fresh source/model checks for res==NULL only.
No public authentication, actual interpreter operation or author campaign.
Saved decref fixtures supply conditional premises, never authenticated bases.
"""
import sys,os,time,json,ast,copy,types,hashlib,traceback,datetime,importlib.metadata
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from bytes_only import B,read,save,fid,ident
R=B/'candidate';O=B/'independent';O.mkdir(exist_ok=False);rows=[];start=time.monotonic()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def check(name,layer,fn,reject=None):
 try:
  try:detail=fn()
  except ValueError as e:
   if reject and str(e).startswith(reject):status='REJECTED';detail={'exception':'ValueError','code':str(e)}
   else:raise
  else:
   if reject:raise AssertionError('UNEXPECTED ACCEPTANCE: '+name)
   status='PASS'
 except BaseException as e:status='FAIL';detail={'type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()}
 row={'sequence':len(rows)+1,'name':name,'layer':layer,'status':status,'detail':detail,'utc':now()};rows.append(row);save(O/(f"{len(rows):04d}.json"),row)
 with (O/'progress.jsonl').open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(row,sort_keys=True),flush=True)
 if status=='FAIL':raise AssertionError('FAILED CONTROL '+name)
def eq(a,b):assert a==b,(a,b)
def module(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 def audit(event,args):
  if event.startswith(('socket.','sqlite3.','subprocess.','os.system','os.exec','os.spawn')):raise RuntimeError('REVIEW-PROHIBITED:'+event)
 sys.addaudithook(audit)
 c=module(R/'code/managed_coverage.py','_resnull_pure');a=module(R/'code/correspondence.py','_resnull_rows_only')
 src={n:(R/'reference/resolution/source'/n).read_bytes() for n in read(R/'reference/resolution/source-index.json')}
 save(O/'environment.json',{'python':sys.version,'executable':sys.executable,'cryptography_distribution':importlib.metadata.version('cryptography'),'scope':'pure-source/model, no public authentication or application/helper execution','producer':fid(R/'code/managed_coverage.py'),'adapter':fid(R/'code/correspondence.py')})
 bc=src['Python/bytecodes.c'].decode().splitlines();gen=src['Python/generated_cases.c.h'].decode().splitlines()
 def defining():
  assert [x.strip() for x in bc[2514:2519]]==['res = _PyObject_CallNoArgs(enter);','Py_DECREF(enter);','if (res == NULL) {','Py_DECREF(exit);','ERROR_IF(true, error);']
  assert gen[3498].strip()=='PyObject *res;' and gen[3527].strip()=='#line 2515 "Python/bytecodes.c"'
  assert [x.strip() for x in gen[3528:3533]]==['res = _PyObject_CallNoArgs(enter);','Py_DECREF(enter);','if (res == NULL) {','Py_DECREF(exit);','if (true) goto pop_1_error;']
  assert [x.strip() for x in gen[3535:3539]]==['STACK_GROW(1);','stack_pointer[-1] = res;','stack_pointer[-2] = exit;','DISPATCH();']
  return {'operator':'C pointer equality','selected_test':2517,'generated':3531,'true_boundary_before':3532,'false_boundary_before':3536,'Python_None':'non-NULL pointer premise, comparison false','no_branch_body_execution':True}
 check('independent defining comparison and excluded true/false successors','read-only defining source',defining)
 cats=[read(R/'fixtures'/n) for n in ('r1-catalogue.json','lookup-catalogue.json','enter-catalogue.json','return-catalogue.json','decref-catalogue.json')]
 args=[(R/'source-evidence/lab_bootstrap.py').read_bytes(),src['Python/bytecodes.c'],(R/'reference/cpython-3.12.14/typeobject.c').read_bytes(),*cats]
 fast=c.compile_decref_fast(*args,src);cat=c.compile_res_null(*args,fast,src)
 check('source-derived class mapping and two stages','source-derived catalogue comparison',lambda:eq((cat['result_by_completed_C_class'],cat['order']),({'C-NULL':True,'non-NULL/opaque':False,'non-NULL/Python-None':False},['res-null:continuation','res-null:comparison'])))
 for name,change in [('Python-None-false-to-true',lambda x:x['result_by_completed_C_class'].update({'non-NULL/Python-None':True})),('wrong-generated-occurrence',lambda x:x['source']['generated_test'].update(line=3532)),('interchange-boundaries',lambda x:x['source'].update(true_stop_before=x['source']['false_stop_before']))]:
  v=copy.deepcopy(cat);change(v);check(name,'source-derived catalogue submitted comparison',lambda v=v:c.validate_res_null(*args,fast,src,v),'RES-NULL')
 def wiring():
  text=(R/'code/correspondence.py').read_text();t=ast.parse(text);f={n.name:ast.get_source_segment(text,n) for n in t.body if isinstance(n,ast.FunctionDef)}
  for s in ['fresh=inputs(', 'pb=p._basis(pd)', 'p.enc(p._assemble(pb))', 'compile_res_null(']:assert s in f['_basis']
  assert f['_basis'].index('p._basis(pd)')<f['_basis'].index('compile_res_null(')
  assert "parent=basis['parent_module']._construct_checked" in f['_construct_checked']
  assert f['_construct_checked'].index('parent=')<f['_construct_checked'].index('res_null_binding(')<f['_construct_checked'].index('validate_res_null_projection(')
  assert 'saved==enc(result)' in f['validate'] and 'derive(root)' in f['validate']
  assert "ctx[RELATION]" in f['_assemble'] and 'declaration_rows(' in f['_rows']
  return {'static_wiring':'mandatory actual parent and full receipt comparison','authenticated_constructed_execution':'UNEXECUTED','public_authentication':'saved run reused'}
 check('mandatory actual-parent/public/constructed wiring','static source inspection only',wiring)
 fixtures=read(R/'fixtures/retained-decref-cases.json');bases={};normals={};coverage=set();setup=[]
 order={'immortal':[('continuation','normal'),('operand','bound'),('immortal-test','true'),('break','taken'),('macro-end','completed')],'non-immortal-positive-gt-one':[('continuation','normal'),('operand','bound'),('immortal-test','false'),('statistics','no-op'),('decrement-zero-test','nonzero'),('macro-end','completed')]}
 def newcase(parent,anchor,continuation='explicit conditional premise',storage='explicit conditional premise'):
  binding=c.res_null_binding(cat,parent,anchor,continuation,storage,src)
  return {'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':copy.deepcopy(parent),'binding':binding,'outcomes':[]}
 def project(v):return c.res_null_projection(cat,v,v,src)
 # Construct only the parent premises needed for this new comparison; no old assertions/campaigns.
 for i,f in enumerate(fixtures):
  for branch,steps in order.items():
   p=f['output'];pb=c.decref_fast_binding(fast,p,f['input']['anchor'],'explicit conditional premise',branch,c.decref_fast_envelope(),src)
   pc={'scope':copy.deepcopy(p['scope']),'anchor':copy.deepcopy(f['input']['anchor']),'parent_result':copy.deepcopy(p),'binding':pb,'outcomes':[{'stage':'decref-fast:'+s,'outcome':v} for s,v in steps]}
   parent=c.decref_fast_projection(fast,pc,pc,src);v=newcase(parent,f['input']['anchor'])
   expected=f['name'].endswith('/NULL');v['outcomes']=[{'stage':'res-null:continuation','outcome':'normal'},{'stage':'res-null:comparison','outcome':'true' if expected else 'false'}]
   bases[i,branch]=v
   def normal(v=v,expected=expected,i=i,branch=branch):
    o=project(v);normals[i,branch]=o;p=v['parent_result']
    assert o['res_null_test_completed_in_model'] is True and o['res_null_test_outcome'] is expected and type(o['res_null_test_outcome']) is bool
    assert o['completion']==('res-null-true' if expected else 'res-null-false') and [e['stage'] for e in o['events']]==['res-null:continuation','res-null:comparison']
    assert o['new_model_claims']=={'pointer_comparison_completed':True,'res_equals_C_NULL':expected,'Python_truthiness_used':False,'branch_body_entered':False}
    assert o['predecessor_projection']==p and o['conditional_fast_completion_in_model'] is True
    assert o['last_pending_error_in_model']==p['last_pending_error_in_model'] and o['terminal_python_exception_in_model'] is True
    assert o['original_error_pending_in_outer_handler']==p['original_error_pending_in_outer_handler'] and o['prior_acknowledged_partial_effects']==p['current_partial_effects']
    for k in ('result_test_established','result_error_routing_established','exit_decref_attempt_established','stack_operations_established','dispatch_established','context_manager_entry_established','f_binding_established','qualified_binary_correspondence'):assert o[k] is False,k
    assert o['runtime_test_arrival'] is None and o['runtime_test_outcome'] is None
    assert o['binding']['assignment']['value']==p['res_value_role'] and o['binding']['res_storage_role']['assignment_occurrence']==p['res_assignment']['occurrence']
    assert o['binding']['res_storage_role']['runtime_address'] is None and o['binding']['enter_role']!=o['binding']['exit_role']
    for e in o['events']:assert e['source']['line']==2517 and e['generated_test']['line']==3531 and e['assignment_occurrence']==p['res_assignment']['occurrence'] and e['scope']==p['scope']
    return {'fixture':fixtures[i]['name'],'branch':branch,'expected_C_NULL':expected,'input_identity':ident(c.enc(v)),'output_identity':ident(c.enc(o)),'layer_qualification':'conditional model; not actual returned authenticated basis'}
   check(f['name']+'/'+branch,'pure-model comparison derivation with independent source oracle',normal)
   coverage.add((p['scope']['context'],p['scope']['invocation'].split('/')[-2],p['failure_origin_region'],branch,f['name'].split('/')[-1]))
   setup.append({'fixture':i,'branch':branch,'parent_identity':ident(c.enc(parent)),'credit':0})
 save(O/'parent-premise-setup-identities.json',setup)
 check('48 distinct conditional combinations across both contexts/prefixes/origins/branches/classes','fresh matrix coverage, not runtime occurrence coverage',lambda:eq(len(coverage),48))
 for i,branch in [(2,'immortal'),(22,'non-immortal-positive-gt-one')]:
  base=bases[i,branch];pristine=normals[i,branch];label=base['scope']['context'];parent=base['parent_result']
  check(label+'/legitimate output validator','pure-model output comparison; fixed conditional premises',lambda:c.validate_res_null_projection(cat,base,base,pristine,src))
  for key in ('continuation','res_storage_continuity'):
   v=newcase(parent,base['anchor'],'UNESTABLISHED' if key=='continuation' else 'explicit conditional premise','UNESTABLISHED' if key=='res_storage_continuity' else 'explicit conditional premise');v['outcomes']=[{'stage':'res-null:continuation','outcome':'unobserved'}]
   check(label+'/'+key+' unknown','pure-model uncertainty derivation',lambda v=v:eq((project(v)['res_null_test_completed_in_model'],project(v)['res_null_test_outcome'],project(v)['terminal_python_exception_in_model']),(False,None,None)))
   bad=copy.deepcopy(v);bad['outcomes']=copy.deepcopy(base['outcomes']);check(label+'/'+key+' unknown cannot compare','pure-model premise gate',lambda bad=bad:project(bad),'RES-NULL')
   bad=copy.deepcopy(base);bad['binding'].pop(key);check(label+'/'+key+' missing','pure-model premise gate',lambda bad=bad:project(bad),'RES-NULL')
  for key in ('conditional_fast_completion_in_model','helper_c_return_completed_in_model','res_assignment_established','res_assignment','res_value_role'):
   p=copy.deepcopy(parent);p.pop(key)
   check(label+'/missing parent '+key,'pure predecessor-completion/assignment gate',lambda p=p:c.res_null_binding(cat,p,base['anchor'],'explicit conditional premise','explicit conditional premise',src),'RES-NULL')
  for at,frontiers in [(0,('raise','catchable-interruption','process-termination','unobserved')),(1,('interruption','process-termination','unobserved'))]:
   for frontier in frontiers:
    v=copy.deepcopy(base);v['outcomes']=v['outcomes'][:at+1];v['outcomes'][-1]['outcome']=frontier
    def frontier_check(v=v,at=at,frontier=frontier):
     o=project(v);p=v['parent_result'];assert o['res_null_test_completed_in_model'] is False and o['res_null_test_outcome'] is None and len(o['events'])==at+1
     assert o['conditional_fast_completion_in_model'] is True and o['predecessor_projection']==p and o['original_error_pending_in_outer_handler']==p['original_error_pending_in_outer_handler']
     if frontier in ('raise','catchable-interruption'):
      assert o['terminal_python_exception_in_model'] is True and o['last_pending_error_in_model']==o['replacement_error_in_model'] and o['replacement_error_in_model']['kind']==frontier
      assert o['last_pending_error_in_model']!=p['last_pending_error_in_model']
     else:assert o['terminal_python_exception_in_model'] is None and o['pending_error_at_frontier']=='UNESTABLISHED' and o['last_pending_error_in_model']==p['last_pending_error_in_model']
     assert o['prior_acknowledged_partial_effects']==p['current_partial_effects'] and o['Python_unwind_established'] is False
     return {'stage':at,'frontier':frontier,'comparison_outcome':None,'earlier_completion_preserved':True}
    check(label+f'/frontier {at} {frontier}','pure-model first-nonnormal/error lineage',frontier_check)
  muts={
   'opposite-result':lambda v:v['outcomes'][1].update(outcome='false' if i==2 else 'true'),
   'skip-continuation':lambda v:v['outcomes'].pop(0),
   'reorder-stages':lambda v:v['outcomes'].reverse(),
   'continue-after-termination':lambda v:v['outcomes'][0].update(outcome='process-termination'),
   'Python-raise-inside-C-test':lambda v:v['outcomes'][1].update(outcome='raise'),
   'wrong-storage':lambda v:v['binding']['res_storage_role'].update(symbol='other-res-storage'),
   'wrong-assignment':lambda v:v['binding']['assignment'].update(from_return_occurrence='other-return'),
   'substitute-enter-value':lambda v:v['binding'].update(res_value_role=v['binding']['enter_role']),
   'wrong-owner-token':lambda v:v['binding']['references'].update(owner='other-owner',token='other-token'),
   'wrong-selected-completion':lambda v:v['binding']['selected_fast_completion'].update(id='other-completion'),
   'mixed-context':lambda v:v['scope'].update(context='SYMBOLIC-U-TWO' if i==2 else 'SYMBOLIC-U-ONE'),
   'wrong-instance':lambda v:v['anchor']['instance'].update(binding='other-instance'),
  }
  for name,mut in muts.items():
   v=copy.deepcopy(base);mut(v);check(label+'/'+name,'pure-model order/binding/comparison constraints; changed case and selected input',lambda v=v:project(v),'RES-NULL')
  # Coordinated new-layer substitutions cannot validate each other against a fixed parent.
  v=copy.deepcopy(base);v['binding']['res_value_role']['C_NULL']=not v['binding']['res_value_role']['C_NULL'];v['binding']['assignment']['value']=copy.deepcopy(v['binding']['res_value_role']);v['outcomes'][1]['outcome']='false' if i==2 else 'true'
  check(label+'/coordinated assigned value and comparison substitution','pure-model binding correspondence to unchanged parent fixture',lambda v=v:project(v),'RES-NULL')
  p=copy.deepcopy(parent);p['res_assignment']['from_return_occurrence']='other-return';p['res_value_role']['return_occurrence']='other-return';p['res_assignment']['value']=copy.deepcopy(p['res_value_role'])
  check(label+'/coordinated parent assignment/return substitution','retained pure fast-projection output comparison, not authentication',lambda p=p:c.res_null_binding(cat,p,base['anchor'],'explicit conditional premise','explicit conditional premise',src),'DECREF-FAST')
  edits={
   'opposite-output':lambda o:o.update(res_null_test_outcome=not o['res_null_test_outcome']),
   'erase-original-error':lambda o:o.update(last_pending_error_in_model=None),
   'terminal-False':lambda o:o.update(terminal_python_exception_in_model=False),
   'true-branch-decrement':lambda o:o.update(exit_decref_attempt_established=True),
   'false-branch-stack-dispatch':lambda o:o.update(stack_operations_established=True,dispatch_established=True),
   'physical-address':lambda o:o['binding']['res_storage_role'].update(runtime_address=1),
   'erase-partial-effects':lambda o:o.update(prior_acknowledged_partial_effects='NONE'),
   'boolean-as-int':lambda o:o.update(res_null_test_outcome=int(o['res_null_test_outcome'])),
  }
  for name,edit in edits.items():
   o=copy.deepcopy(pristine);edit(o);check(label+'/'+name,'pure submitted-output comparison; fixed conditional premises',lambda o=o:c.validate_res_null_projection(cat,base,base,o,src),'RES-NULL')
  class S(str):pass
  class L(list):pass
  class D(dict):pass
  for name,edit in [('subclass-outcome',lambda v:v['outcomes'][1].update(outcome=S(v['outcomes'][1]['outcome']))),('subclass-binding',lambda v:v.update(binding=D(v['binding']))),('subclass-key',lambda v:v.update({S('scope'):v.pop('scope')})),('subclass-list',lambda v:v.update(outcomes=L(v['outcomes'])))]:
   v=copy.deepcopy(base);edit(v);check(label+'/'+name,'exact input type before normalization',lambda v=v:project(v),'RES-NULL')
  original=c.enc(base);original_cat=c.enc(cat);o=project(base)
  o['binding']['assignment']['from_return_occurrence']='MUTATED';o['events'][0]['res_storage_role']['symbol']='MUTATED';o['predecessor_projection']['scope']['instance']['binding']='MUTATED'
  check(label+'/mutated actual return rejected','pure output comparison after direct returned-object mutation',lambda:c.validate_res_null_projection(cat,base,base,o,src),'RES-NULL')
  check(label+'/pristine remains accepted after mutation','direct-return expectation isolation and repeat derivation',lambda:eq((c.enc(base),c.enc(cat),c.enc(project(base))),(original,original_cat,c.enc(pristine))))
  rb=c.res_null_binding(cat,parent,base['anchor'],'explicit conditional premise','explicit conditional premise',src);rb['references']['owner']='MUTATED';rb['res_value_role']['C_NULL']=None
  check(label+'/returned binding isolated','direct binding-return isolation',lambda:eq(c.res_null_binding(cat,parent,base['anchor'],'explicit conditional premise','explicit conditional premise',src),base['binding']))
 prior=read(R/'reference/fast/actual-receipt.json');marker={'meaning':'OFFLINE REVIEW DATA; NOT AUTHENTICATED BASIS','actual_admission':False}
 rr=a.declaration_rows(prior,cat,marker);good=copy.deepcopy(rr)
 check('both mandatory declaration rows legitimate','pure mandatory-row comparison; no authentication',lambda:a.validate_declaration_rows(prior,cat,marker,rr))
 for name,edit in [('missing-context',lambda r:r.pop()),('reversed-contexts',lambda r:r.reverse()),('invented-runtime-outcomes',lambda r:[x.update(test_outcome=True,runtime_arrival=True) for x in r]),('UNKNOWN-to-zero',lambda r:[x.update(multiplicity=0,classification='QUALIFIED') for x in r])]:
  v=copy.deepcopy(good);edit(v);check(name,'pure mandatory-row output comparison',lambda v=v:a.validate_declaration_rows(prior,cat,marker,v),'RES-NULL')
 rr[0]['declaration']['result_by_completed_C_class']['non-NULL/Python-None']=True;rr[0]['scope']['context']='MUTATED';rr.reverse()
 check('actual declaration-return nested mutation rejected','pure mandatory-row comparison after direct return mutation',lambda:a.validate_declaration_rows(prior,cat,marker,rr),'RES-NULL')
 check('declaration expectations remain isolated','direct declaration-return isolation',lambda:eq(a.declaration_rows(prior,cat,marker),good))
 returned=c.res_null_catalogue(fast,src);returned['result_by_completed_C_class']['C-NULL']=False;returned['source']['generated_test']['line']=1
 check('source catalogue returned object isolated','direct catalogue-return isolation',lambda:eq(c.res_null_catalogue(fast,src),cat))
 for n,pin in read(R/'MANIFEST.json').items():assert fid(R/n)==pin,n
 result={'result':'PASS','rows':len(rows),'counts':{s:sum(x['status']==s for x in rows) for s in ('PASS','REJECTED','FAIL')},'seconds':time.monotonic()-start,'source':fid(B/'host/inputs/I164-res-null-test-1-source.zip'),'public_calls':0,'authenticated_constructed_calls':0,'runtime_observations_added':0,'parent_setup_credit':0,'scope':'independent source/model only; saved conditional parent fixtures are not authenticated basis'}
 save(O/'RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
if __name__=='__main__':
 try:main()
 except BaseException as e:save(O/'FAILURE.json',{'error':repr(e),'traceback':traceback.format_exc(),'rows_recorded':len(rows),'seconds':time.monotonic()-start});raise
