"""Formal-Lab[6]: new bounded pure-source/model controls, never public authentication.
Expected order and completion facts are derived here from the inspected C body;
saved predecessor cases are conditional fixtures, not an authenticated basis.
"""
import sys,copy,json,hashlib,ast,re,types,os,time,datetime,traceback,importlib.metadata
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from bytes_only import B,read,save,fid,ident
R=B/'candidate';OUT=B/'independent';OUT.mkdir(exist_ok=False);start=time.monotonic();rows=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def check(name,layer,fn,reject=None):
 try:
  try:detail=fn()
  except ValueError as e:
   if reject and str(e).startswith(reject):status='REJECTED';detail={'exception':type(e).__name__,'code':str(e)}
   else:raise
  else:
   if reject:raise AssertionError('UNEXPECTED ACCEPTANCE: '+name)
   status='PASS'
 except BaseException as e:
  status='FAIL';detail={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
 row={'sequence':len(rows)+1,'name':name,'layer':layer,'status':status,'detail':detail,'utc':now()};rows.append(row)
 save(OUT/(str(row['sequence']).zfill(4)+'.json'),row)
 with (OUT/'progress.jsonl').open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(row,sort_keys=True),flush=True)
 if status=='FAIL':raise AssertionError('FAILED CONTROL '+name)
def eq(a,b):assert a==b,(a,b)
def module(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 # Fail closed if the narrow source/model run attempts any external action.
 def guard(event,args):
  if event.startswith(('socket.','sqlite3.','subprocess.','os.system','os.exec','os.spawn')):raise RuntimeError('REVIEW-PROHIBITED:'+event)
 sys.addaudithook(guard)
 c=module(R/'code/managed_coverage.py','reviewed_pure_model');a=module(R/'code/correspondence.py','reviewed_adapter_static_only')
 src={n:(R/'reference/resolution/source'/n).read_bytes() for n in read(R/'reference/resolution/source-index.json')}
 fixed=read(R/'fixtures/retained-decref-cases.json');oldcat=read(R/'fixtures/decref-catalogue.json')
 save(OUT/'environment.json',{'python':sys.version,'executable':sys.executable,'cryptography_distribution':importlib.metadata.version('cryptography'),'source':fid(B/'host/inputs/I164-decref-fast-completion-1-source.zip'),'scope':'pure source/model only; no native observer, public authentication or application execution'})
 def official():
  tree=read(B/'resolution/retrieved/official-tree.json');assert tree['truncated'] is False
  blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
  for n,b in src.items():
   if n=='Include/pyconfig.h':continue
   assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blobs[n],n
  cfg=next((B/'resolution/configuration/installed').rglob('pyconfig.h'));assert src['Include/pyconfig.h']==cfg.read_bytes()
  assert len(src)==183
  return {'upstream_tree_files':182,'installed_generated_pyconfig':1,'provenance':'retained immutable-tree response; no independent signature or binary-build verification'}
 check('183 definition-context identities, retained upstream tree and installed configuration','read-only source identity',official)
 ceval=src['Python/ceval.c'].decode().splitlines();gen=src['Python/generated_cases.c.h'].decode().splitlines();bc=src['Python/bytecodes.c'].decode().splitlines()
 def source_order():
  assert ceval[48].strip()=='#if !defined(Py_DEBUG) && !defined(Py_TRACE_REFS)'
  assert [x.strip().rstrip('\\').rstrip() for x in ceval[56:68]]==['#define Py_DECREF(arg)','do {','PyObject *op = _PyObject_CAST(arg);','if (_Py_IsImmortal(op)) {','break;','}','_Py_DECREF_STAT_INC();','if (--op->ob_refcnt == 0) {','destructor dealloc = Py_TYPE(op)->tp_dealloc;','(*dealloc)(op);','}','} while (0)']
  assert [x.strip() for x in bc[2514:2517]]==['res = _PyObject_CallNoArgs(enter);','Py_DECREF(enter);','if (res == NULL) {']
  assert gen[3527].strip()=='#line 2515 "Python/bytecodes.c"' and gen[3528:3531]==['            '+x for x in ['res = _PyObject_CallNoArgs(enter);','Py_DECREF(enter);','if (res == NULL) {']]
  assert gen[3522].strip()=='Py_DECREF(enter);' and gen[3526].strip()=='Py_DECREF(mgr);'
  return {'selected_generated_line':3530,'excluded_failed_lookup':3523,'res_test_after_selected_operation':True,'immortal_break':'exits do/while, not interpreter'}
 check('local override, generated occurrence and independently derived branch order','read-only defining source',source_order)
 def later_context():
  # Only remaining project includes after the macro and before generated use.
  includes=[(i+1,x.strip()) for i,x in enumerate(ceval) if 68<i+1<=849 and re.match(r'\s*#\s*include\s*"',x)]
  assert includes==[(603,'#include "ceval_macros.h"'),(663,'#include "opcode_targets.h"'),(849,'#include "generated_cases.c.h"')]
  for n in ['Python/ceval_macros.h','Python/opcode_targets.h']:
   assert not re.search(rb'#\s*(define|undef)\s+(Py_DECREF|_Py_IsImmortal|_PyObject_CAST|_Py_DECREF_STAT_INC)\b',src[n])
  assert not re.search(r'#\s*(define|undef)\s+Py_DECREF\b','\n'.join(ceval[68:849]))
  assert '#define _Py_DECREF_STAT_INC() ((void)0)' in src['Include/pystats.h'].decode()
  assert 'return _Py_CAST(PY_INT32_T, op->ob_refcnt) < 0;' in src['Include/object.h'].decode()
  return {'C_and_external_override_premises':'conditional, not historical preprocessing','stats':'disabled no-op','cast_result':'branch premise, unobserved'}
 check('no later project override; selected immortal predicate and statistics branch','read-only source/configuration',later_context)
 cats=[read(R/'fixtures'/n) for n in ['r1-catalogue.json','lookup-catalogue.json','enter-catalogue.json','return-catalogue.json','decref-catalogue.json']]
 args=[(R/'source-evidence/lab_bootstrap.py').read_bytes(),(R/'reference/cpython-3.12.14/bytecodes.c').read_bytes(),(R/'reference/cpython-3.12.14/typeobject.c').read_bytes(),*cats,src]
 cat=c.compile_decref_fast(*args)
 orders={'immortal':[('continuation','normal'),('operand','bound'),('immortal-test','true'),('break','taken'),('macro-end','completed')], 'non-immortal-positive-gt-one':[('continuation','normal'),('operand','bound'),('immortal-test','false'),('statistics','no-op'),('decrement-zero-test','nonzero'),('macro-end','completed')]}
 check('catalogue matches independently derived two branch orders','source-derived catalogue comparison',lambda:eq(cat['branch_orders'],{k:['decref-fast:'+n for n,_ in v] for k,v in orders.items()}))
 def wiring():
  t=ast.parse((R/'code/correspondence.py').read_bytes());f={n.name:ast.get_source_segment((R/'code/correspondence.py').read_text(),n) for n in t.body if isinstance(n,ast.FunctionDef)}
  for s in ['fresh=inputs(', 'pb=p._basis(pd)', 'p.enc(p._assemble(pb))','compile_decref_fast(']:assert s in f['_basis']
  assert f['_basis'].index('pb=p._basis(pd)')<f['_basis'].index('compile_decref_fast(')
  assert "parent=basis['parent_module']._construct_checked" in f['_construct_checked']
  assert f['_construct_checked'].index('_construct_checked(')<f['_construct_checked'].index('decref_fast_binding(')<f['_construct_checked'].index('validate_decref_fast_projection(')
  assert 'derive(root)' in f['validate'] and 'saved==enc(result)' in f['validate']
  assert "ctx[RELATION]" in f['_assemble'] and 'copy.deepcopy' in f['_rows']
  return {'public_authentication':'saved run only','authenticated_constructed_route':'statically mandatory; execution UNTESTED'}
 check('actual-parent authentication/construct wiring and mandatory both-context rows','static integration inspection, no execution',wiring)
 def setup(f,branch,continuity='explicit conditional premise'):
  p=f['output'];bind=c.decref_fast_binding(cat,p,f['input']['anchor'],continuity,branch,c.decref_fast_envelope(),src)
  return {'scope':copy.deepcopy(p['scope']),'anchor':copy.deepcopy(f['input']['anchor']),'parent_result':copy.deepcopy(p),'binding':bind,'outcomes':[{'stage':'decref-fast:'+n,'outcome':v} for n,v in orders.get(branch,[('continuation','unobserved')])]}
 def project(v):return c.decref_fast_projection(cat,v,v,src)
 bases={}
 for i,f in enumerate(fixed):
  for branch in orders:
   v=setup(f,branch);bases[i,branch]=v
   def normal(v=v,branch=branch):
    o=project(v);p=v['parent_result'];claims=o['new_model_claims'];isimm=branch=='immortal'
    assert o['conditional_fast_completion_in_model'] is True and claims['macro_completion_in_model'] is True
    assert claims['immortal_predicate_result'] is isimm and claims['break_from_do_while_in_model'] is isimm and claims['decrement_and_nonzero_test_in_model'] is (not isimm)
    if isimm:assert claims['count_relation'] is None
    else:
     rel=claims['count_relation'];assert rel['before']=='n' and rel['after']=='n - 1' and rel['nonzero'] is True and rel['concrete_values'] is None and rel['same_selected_enter_role']==v['binding']['enter_role']
    assert o['terminal_python_exception_in_model'] is True and o['last_pending_error_in_model']==p['last_pending_error_in_model'] and o['original_error_pending_in_outer_handler']==p['original_error_pending_in_outer_handler']
    assert o['predecessor_projection']==p and o['prior_acknowledged_partial_effects']==p['current_partial_effects']
    for k in ['result_test_established','physical_release_established','reference_count_change_established','finalization_established','context_manager_entry_established','f_binding_established','qualified_binary_correspondence']:assert o[k] is False,k
    assert o['res_value_role']==p['res_value_role'] and o['binding']['enter_role']!=o['binding']['exit_role']
    assert c.validate_decref_fast_projection(cat,v,v,o,src) is True
    return {'fixture':f['name'],'branch':branch,'input_identity':ident(c.enc(v)),'output_identity':ident(c.enc(o)),'runtime_observation':False}
   check(f['name']+'/'+branch,'pure-model derivation and output comparison; conditional saved parent fixture',normal)
 # Representatives in both contexts, with all prefixes/origins already exercised above.
 for i in (2,23):
  f=fixed[i]
  for branch in orders:
   base=bases[i,branch]
   frontiers=[(0,'raise'),(0,'catchable-interruption'),(1,'interruption'),(2,'process-termination'),(len(base['outcomes'])-1,'unobserved')]
   for at,outcome in frontiers:
    def frontier(at=at,outcome=outcome,base=base):
     v=copy.deepcopy(base);v['outcomes']=v['outcomes'][:at+1];v['outcomes'][-1]['outcome']=outcome;o=project(v);p=v['parent_result']
     assert len(o['events'])==at+1 and o['conditional_fast_completion_in_model'] is False
     assert o['original_error_pending_in_outer_handler']==p['original_error_pending_in_outer_handler'] and o['predecessor_projection']==p
     if outcome in ('raise','catchable-interruption'):
      assert o['terminal_python_exception_in_model'] is True and o['replacement_error_in_model']['kind']==outcome and o['last_pending_error_in_model']==o['replacement_error_in_model']
      assert o['last_pending_error_in_model']!=p['last_pending_error_in_model']
     else:
      assert o['terminal_python_exception_in_model'] is None and o['pending_error_at_frontier']=='UNESTABLISHED' and o['last_pending_error_in_model']==p['last_pending_error_in_model']
     if at==len(base['outcomes'])-1:
      assert o['new_model_claims']['break_from_do_while_in_model'] is (branch=='immortal') and o['new_model_claims']['decrement_and_nonzero_test_in_model'] is (branch!='immortal')
     return {'outcome':outcome,'stage':v['outcomes'][-1]['stage'],'prior_facts_preserved':True}
    check(f['name']+'/'+branch+f'/frontier-{at}-{outcome}','pure-model first-nonnormal derivation',frontier)
  for kw in ('continuity','branch'):
   v=setup(f,'immortal' if kw=='continuity' else 'UNESTABLISHED','UNESTABLISHED' if kw=='continuity' else 'explicit conditional premise');v['outcomes']=[{'stage':'decref-fast:continuation','outcome':'unobserved'}]
   check(f['name']+'/'+kw+' unestablished','pure-model uncertainty derivation',lambda v=v:eq((project(v)['conditional_fast_completion_in_model'],project(v)['terminal_python_exception_in_model']),(False,None)))
  base=bases[i,'non-immortal-positive-gt-one']
  mutations={
   'missing-continuation':lambda v:v['outcomes'].pop(0),
   'reordered-stages':lambda v:v['outcomes'].reverse(),
   'extra-stage-after-frontier':lambda v:v['outcomes'][1].update(outcome='unobserved'),
   'immortal-predicate-conflicts-with-nonimmortal':lambda v:v['outcomes'][2].update(outcome='true'),
   'invented-C-primitive-raise':lambda v:v['outcomes'][4].update(outcome='raise'),
   'invented-zero-destructor-completion':lambda v:v['binding'].update(branch='zero-count-destructor-complete'),
   'missing-defined-C-premise':lambda v:v['binding']['envelope'].pop('defined_C_evaluation_and_integer_semantics'),
   'stats-enabled-envelope':lambda v:v['binding']['envelope']['configuration'].update(Py_STATS=True),
   'bool-for-pointer-size':lambda v:v['binding']['envelope']['configuration'].update(SIZEOF_VOID_P=True),
   'wrong-occurrence':lambda v:v['binding']['selected_attempt'].update(id='another-decref'),
   'substitute-exit-for-enter':lambda v:v['binding'].update(enter_role=v['binding']['exit_role']),
   'wrong-owner-token':lambda v:v['binding']['references'].update(owner='other-owner',token='other-token'),
   'mixed-context':lambda v:v['scope'].update(context='SYMBOLIC-U-TWO' if i==2 else 'SYMBOLIC-U-ONE'),
   'wrong-instance':lambda v:v['anchor']['instance'].update(binding='other-instance'),
   'erase-pending':lambda v:v['binding'].update(pending_error_before_macro=None),
   'coordinated-concrete-count-claim':lambda v:v['binding']['state_premise'].update(concrete_count=2,derived_from_res=True),
   'unestablished-but-continued':lambda v:v['binding'].update(continuity='UNESTABLISHED'),
  }
  for name,mut in mutations.items():
   v=copy.deepcopy(base);mut(v)
   check(f['name']+'/'+name,'pure-model constraints; mutually changed case/selected-input, unchanged source and parent fixture',lambda v=v:project(v),'DECREF-FAST')
  pristine=project(base)
  edits={
   'no-pending-error':lambda o:o.update(last_pending_error_in_model=None),
   'False-terminal':lambda o:o.update(terminal_python_exception_in_model=False),
   'zero-count-complete':lambda o:o['new_model_claims'].update(zero_count_completion=True),
   'destructor-called':lambda o:o['new_model_claims'].update(destructor_invocation_in_model=True),
   'normal-interpreter-return':lambda o:o['new_model_claims'].update(interpreter_return_established=True),
   'concrete-count-effect':lambda o:o['new_model_claims']['count_relation'].update(concrete_values=[2,1]),
   'line2517-reached':lambda o:o.update(result_test_established=True),
   'physical-release':lambda o:o.update(physical_release_established=True),
   'erase-partial-effects':lambda o:o.update(prior_acknowledged_partial_effects='NONE'),
   'coordinated-lineage-output':lambda o:(o['binding']['references'].update(owner='other'),[e.update(owner='other') for e in o['events']]),
   'missing-event':lambda o:o['events'].pop(1),
   'bool-as-int-flag':lambda o:o.update(conditional_fast_completion_in_model=1),
  }
  for name,edit in edits.items():
   o=copy.deepcopy(pristine);edit(o)
   check(f['name']+'/'+name,'pure-model submitted-output exact comparison; fixed conditional premises',lambda o=o:c.validate_decref_fast_projection(cat,base,base,o,src),'DECREF-FAST')
  class S(str):pass
  class D(dict):pass
  class L(list):pass
  class I(int):pass
  for name,edit in [('subclass-branch',lambda v:v['binding'].update(branch=S(v['binding']['branch']))),('subclass-key',lambda v:v.update({S('scope'):v.pop('scope')})),('subclass-container',lambda v:v.update(outcomes=L(v['outcomes']))),('subclass-int',lambda v:v['binding']['envelope']['configuration'].update(SIZEOF_VOID_P=I(8)))]:
   v=copy.deepcopy(base);edit(v);check(f['name']+'/'+name,'exact input types before normalization',lambda v=v:project(v),'DECREF-FAST')
  # Mutate actual returned object, not a deepcopy of it.
  original_input=c.enc(base);original_cat=c.enc(cat);direct=project(base)
  direct['predecessor_projection']['scope']['instance']['binding']='MUTATED'
  direct['binding']['envelope']['configuration']['Py_DEBUG']=True
  direct['events'][0]['owner']='MUTATED'
  check(f['name']+'/direct-return-mutation-rejected','pure-model output comparison after actual return mutation',lambda:c.validate_decref_fast_projection(cat,base,base,direct,src),'DECREF-FAST')
  check(f['name']+'/pristine-after-direct-mutation','actual-return isolation and repeat pure-model derivation',lambda:eq((c.enc(base),c.enc(cat),c.enc(project(base))),(original_input,original_cat,c.enc(pristine))))
 # Independent catalogue/source mutations, rather than archive-only reasoning.
 for name,path,value in [('macro-op','macro_definition','ordinary-object.h-Py_DECREF'),('wrong-generated-occurrence','generated_operation',3523)]:
  mutant=copy.deepcopy(cat)
  if path=='macro_definition':mutant['source'][path]['expression']=value
  else:mutant['source'][path]['line']=value
  check(name,'source-derived catalogue comparison',lambda mutant=mutant:c.validate_decref_fast(*args,mutant),'DECREF-FAST')
 direct=c.decref_fast_catalogue(oldcat,src);direct['branch_orders']['immortal'].reverse();direct['configuration_and_C_premises']['configuration']['Py_STATS']=True
 check('catalogue-return-nested-alias-isolation','actual returned catalogue isolation',lambda:eq(c.decref_fast_catalogue(oldcat,src),cat))
 # Adapter declaration returns checked offline only; never call _basis/derive/validate.
 receipt=read(R/'reference/decref/actual-receipt.json');basis={'prior':receipt,'catalogue':cat,'parent_public':{'result':'SAVED-FIXTURE-ONLY'},'fresh':{'root':R}}
 pristine_rows=a._rows(basis);ret=a._rows(basis);ret.reverse();ret[0]['declaration']['branch_orders']['immortal'].clear();ret[0]['scope']['context']='MUTATED'
 check('adapter-row-context-and-nested-isolation','offline _rows over saved data; not authentication',lambda:eq(a._rows(basis),pristine_rows))
 # Every inspected source hash remains fixed; roots are audited separately.
 for n,pin in read(R/'MANIFEST.json').items():assert fid(R/n)==pin,n
 counts={k:sum(x['status']==k for x in rows) for k in ('PASS','REJECTED','FAIL')}
 result={'result':'PASS','rows':len(rows),'counts':counts,'seconds':time.monotonic()-start,'source':fid(B/'host/inputs/I164-decref-fast-completion-1-source.zip'),'public_calls':0,'authenticated_constructed_calls':0,'runtime_observations_added':0,'qualification':'Pure-source/model controls using saved conditional parent fixtures; no new authentication. Source checks are not binary correspondence.'}
 save(OUT/'RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
if __name__=='__main__':
 try:main()
 except BaseException as ex:
  save(OUT/'FAILED.json',{'type':type(ex).__name__,'error':str(ex),'traceback':traceback.format_exc(),'completed_rows':len(rows),'seconds':time.monotonic()-start});raise
