"""Formal-Lab[6] focused pure-source/model review; not an authentication run.
No application, C helper, protocol method, prior suite or public validator is called.
The retained small fixture builds modeled predecessor premises only. Expectations here
come from independently inspected BEFORE_WITH, write_new and adapter source, not
Engineering's focused.py oracle. Every mutation uses a distinct copy of expectations.
"""
import ast,copy,hashlib,importlib.metadata,json,os,platform,sys,time,traceback,types
from datetime import datetime,timezone
from pathlib import Path
D=copy.deepcopy
HERE=Path(__file__).resolve().parent;ROOT=HERE/'candidate';OUT=HERE/'independent'
OUT.mkdir(exist_ok=False);ROWS=[];START=time.monotonic()
def utc():return datetime.now(timezone.utc).isoformat()
def save(n,v):
 p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def record(name,layer,status,detail=None):
 r={'sequence':len(ROWS)+1,'utc':utc(),'name':name,'layer':layer,'status':status,'detail':detail};ROWS.append(r)
 save('rows/%04d.json'%len(ROWS),r)
 with (OUT/'progress.jsonl').open('a') as f:f.write(json.dumps(r,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(r,sort_keys=True),flush=True)
def yes(name,fn,layer='independent constructed model oracle'):
 try:assert fn() is not False
 except BaseException as e:record(name,layer,'FAIL',repr(e));raise
 record(name,layer,'PASS')
def no(name,fn,layer='source-model input comparison; unauthenticated constructed premises'):
 try:fn()
 except ValueError as e:record(name,layer,'REJECTED',str(e));return
 except BaseException as e:record(name,layer,'HARNESS-FAIL',repr(e));raise
 record(name,layer,'DEFECT-OBSERVED','intended rejection absent');raise AssertionError(name)
def module(p,n):
 m=types.ModuleType(n);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def read(p):return json.loads(p.read_bytes())
def change(v,path,x):
 v=D(v);p=v
 for k in path[:-1]:p=p[k]
 p[path[-1]]=x;return v
class Text(str):pass
class Number(int):pass
class Array(list):pass
class Map(dict):pass
def main():
 versions={}
 for n in ('cryptography','cffi','pycparser'):
  try:versions[n]=importlib.metadata.version(n)
  except importlib.metadata.PackageNotFoundError:versions[n]='not installed'
 save('environment.json',{'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'installed_metadata_only':versions,'candidate_python_protocol_execution':False,'cryptography_execution':False,'host_equivalence_claim':False})
 c=module(ROOT/'code/managed_coverage.py','reviewed_enter_model');a=module(ROOT/'code/correspondence.py','reviewed_enter_adapter')
 f=module(ROOT/'reference/r1/tests/fixtures.py','retained_premise_scaffold')
 launcher=(ROOT/'source-evidence/lab_bootstrap.py').read_bytes();bc=(ROOT/'reference/cpython-3.12.14/bytecodes.c').read_bytes();tt=(ROOT/'reference/cpython-3.12.14/typeobject.c').read_bytes()
 b=bc.decode();start=b.index('        inst(BEFORE_WITH,');end=b.index('        inst(WITH_EXCEPT_START,',start);region=b[start:end]
 positions=[region.index(x) for x in ('_Py_ID(__enter__)','if (enter == NULL)','_Py_ID(__exit__)','if (exit == NULL)','DECREF_INPUTS();','res = _PyObject_CallNoArgs(enter);')]
 yes('BEFORE_WITH lookup guards precede DECREF and selected enter helper attempt',lambda:positions==sorted(positions),'independent defining-source inspection')
 yes('call-result assignment/outcome and enter release lie beyond selected call attempt',lambda:region.index('Py_DECREF(enter);',positions[-1])>positions[-1] and region.index('if (res == NULL)')>positions[-1],'independent defining-source inspection')
 tree=ast.parse(launcher);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='write_new');w=fn.body[0]
 yes('write_new operand is open(p, xb); with f binding follows protocol execution',lambda:isinstance(w,ast.With) and w.lineno==24 and ast.unparse(w.items[0].context_expr)=="open(p, 'xb')" and ast.unparse(w.items[0].optional_vars)=='f','independent defining-source inspection')
 r1=read(ROOT/'fixtures/r1-catalogue.json');lp=read(ROOT/'fixtures/lookup-catalogue.json');hc=read(ROOT/'fixtures/helper-catalogue.json');anchors=read(ROOT/'fixtures/anchors.json')
 cat=c.compile_enter_call(launcher,bc,tt,r1,lp)
 # Oracle stage values below are stated from the source slice, not read from catalogue.
 normals=[{'stage':'enter-call:continuation','outcome':'normal'},{'stage':'enter-call:attempt','outcome':'attempted'}]
 lookups=[{'stage':'lookup:continuation','outcome':'normal'},{'stage':'lookup:__enter__','outcome':'found'},{'stage':'lookup:__exit__','outcome':'found'}]
 yes('declarations match two independently selected source operations and exact zero explicit arity',lambda:cat['source']['order']==[v['stage'] for v in normals] and cat['source']['C_helper']=='_PyObject_CallNoArgs' and cat['source']['C_argument_expression']=='enter' and type(cat['source']['python_explicit_argument_count']) is int and cat['source']['python_explicit_argument_count']==0 and cat['source']['call_site']['line']==b[:b.index('_PyObject_CallNoArgs(enter)',start)].count('\n')+1,'source-derived catalogue check')
 q=D(cat);q['source']['C_argument_expression']='exit';q['source']['call_site']['expression']='_PyObject_CallNoArgs(exit)';q['source']['steps'][1]['source']=D(q['source']['call_site']);q['declarations'][1]['source']=D(q['source']['call_site'])
 no('coordinated call-site and declaration substitution',lambda:c.validate_enter_call(launcher,bc,tt,r1,lp,q),'source-derived catalogue recomputation')
 q=D(cat);q['source']['python_explicit_argument_count']=False
 no('False cannot replace exact integer zero arity',lambda:c.validate_enter_call(launcher,bc,tt,r1,lp,q),'source-derived catalogue exact-type comparison')
 defs={n.name:ast.unparse(n) for n in ast.parse((ROOT/'code/correspondence.py').read_bytes()).body if isinstance(n,ast.FunctionDef)}
 yes('public comparison follows actual predecessor operations and refreshed inputs',lambda:all(s in defs['_basis'] for s in ("fresh = inputs(data['root'])","p._basis(pd)","fresh['saved'] == p.enc(p._assemble(pb))")) and 'saved == enc(result)' in defs['validate'],'static public wiring; saved execution reconciled separately')
 yes('constructed mandatory path invokes actual predecessor checked construction before new output check',lambda:defs['_construct_checked'].index("basis['parent_module']._construct_checked")<defs['_construct_checked'].index('validate_enter_call_projection') and "case['parent_output'], parent" in defs['_construct_checked'],'static constructed wiring; authenticated execution UNEXECUTED')
 save('catalogue.json',cat)
 cases=[]
 for ri,row in enumerate(anchors):
  for prefix in ('control-absent','control-normal'):
   for origin in ('protected-close','protected-append'):
    tag='%d/%s/%s'%(ri,prefix,origin)
    hp=f.parent(c,hc,row,prefix,origin)
    # Fresh fixture uses correct missing-control premise, retained scaffold unchanged.
    if prefix=='control-absent':hp['earlier_control_completed_in_model']=None
    rv=f.projection_case(c,r1,hp);rp=c.open_return_projection(r1,rv,rv)
    lb=c.context_lookup_binding(lp,rp,rp['instance_anchor'],'explicit conditional premise')
    lv={'scope':D(rp['scope']),'anchor':D(rp['instance_anchor']),'parent_result':D(rp),'binding':lb,'outcomes':D(lookups)}
    parent=c.context_lookup_projection(lp,lv,lv)
    binding=c.enter_call_binding(cat,parent,parent['instance_anchor'],'explicit conditional premise')
    v={'scope':D(parent['scope']),'anchor':D(parent['instance_anchor']),'parent_result':D(parent),'binding':binding,'outcomes':D(normals)}
    output=c.enter_call_projection(cat,D(v),D(v));cases.append((tag,v,output))
    save('fixtures/'+tag.replace('/','-')+'.json',{'qualification':'constructed source-model premises, not authenticated or observed execution','input':v,'output':output})
    def normal_oracle():
     assert output['call']['target_role']==parent['method_roles']['__enter__']!=parent['method_roles']['__exit__']==output['call']['retained_exit_role']
     assert output['call']['python_explicit_arguments']==[] and output['call']['callability']=='UNKNOWN' and output['call']['runtime_identity'] is None
     assert [e['stage'] for e in output['events']]==[x['stage'] for x in normals]
     assert all(e['scope']==v['scope'] and e['owner']==binding['references']['owner'] and e['token']==binding['references']['token'] and e['runtime_frame'] is None for e in output['events'])
     assert output['terminal_python_exception_in_model'] is True and output['last_pending_error_in_model']==parent['original_error_pending_in_outer_handler'] and output['replacement_error_in_model'] is None
     assert all(output[k] is False for k in ('helper_dispatch_entry_established','method_body_entry_established','res_assignment_established','enter_invocation_established','exit_invocation_established','context_manager_entry_established','f_binding_established','actual_admission'))
     assert output['call_outcome'] is None and output['call_result_role'] is None and output['runtime_call_attempt_chain'] is None
     assert output['retained_cleanup_error_evidence']==parent['retained_cleanup_error_evidence'] and output['cleanup_list_state']==parent['cleanup_list_state'] and output['predecessor_projection']==parent
     assert output['continuation_past_source_operation_in_model'] is True and output['source_operation_effects'].startswith('UNKNOWN') and output['current_partial_effects'].startswith('UNKNOWN')
     return c.validate_enter_call_projection(cat,D(v),D(v),D(output))
    yes(tag+'/normal call-attempt oracle',normal_oracle)
    for frontier in ('raise','catchable-interruption','process-termination','unobserved'):
     q=D(v);q['outcomes']=[{'stage':'enter-call:continuation','outcome':frontier}]
     out=c.enter_call_projection(cat,q,D(q));unknown=frontier in ('process-termination','unobserved')
     yes(tag+'/'+frontier,lambda out=out,q=q,unknown=unknown:len(out['events'])==1 and out['call'] is None and out['continuation_past_source_operation_in_model'] is False and out['enter_call_attempt_established_in_model'] is False and out['terminal_python_exception_in_model'] is (None if unknown else True) and (out['replacement_error_in_model'] is None)==unknown and out['last_pending_error_in_model']==(parent['last_pending_error_in_model'] if unknown else out['replacement_error_in_model']) and out['retained_cleanup_error_evidence']==parent['retained_cleanup_error_evidence'] and c.validate_enter_call_projection(cat,D(q),D(q),D(out)))
    q=D(v);q['binding']['continuity']='UNESTABLISHED';q['outcomes']=[{'stage':'enter-call:continuation','outcome':'unobserved'}]
    yes(tag+'/unestablished has no fabricated progress',lambda:q['binding']['continuity']=='UNESTABLISHED' and c.enter_call_projection(cat,q,D(q))['call'] is None)
    q['outcomes']=D(normals)
    no(tag+'/unestablished cannot reach call',lambda:c.enter_call_projection(cat,q,D(q)))
    before=D(v);beforecat=D(cat);m=D(output);m['call']['target_role']['scope']['context']='MUTATED';m['binding']['references']['token']['symbol']='MUTATED';m['events'].reverse();m['predecessor_projection']['method_roles'].clear()
    no(tag+'/nested mutated output',lambda:c.validate_enter_call_projection(cat,D(v),D(v),m),'source-model submitted-output comparison')
    yes(tag+'/pristine repeat unaffected by returned aliases',lambda:v==before and cat==beforecat and c.enter_call_projection(cat,D(v),D(v))==output)
 # Adjacent/coordinated checks once per context; all eight normal/frontier combinations above.
 for i in (0,4):
  tag,v,o=cases[i];p=v['parent_result']
  negatives=[('only attempt',[normals[1]]),('missing attempt',normals[:1]),('reversed stages',normals[::-1]),('duplicate attempt',normals+[normals[1]]),('post-exception continuation',[{'stage':'enter-call:continuation','outcome':'raise'},normals[1]]),('call-return outside slice',[normals[0],{'stage':'enter-call:attempt','outcome':'normal-return'}])]
  for name,oo in negatives:
   q=change(v,('outcomes',),oo);no(tag+'/'+name,lambda q=q:c.enter_call_projection(cat,q,D(q)))
  for path,val in [(('scope','invocation'),'other-invocation'),(('binding','lookup_occurrences',0,'id'),'other-occurrence'),(('binding','references','owner','symbol'),'other-owner'),(('binding','references','token','symbol'),'other-token'),(('binding','method_results','__enter__'),D(p['method_roles']['__exit__'])),(('binding','method_results','__exit__'),D(p['method_roles']['__enter__'])),(('anchor','context'),'SYMBOLIC-U-TWO' if i==0 else 'SYMBOLIC-U-ONE')]:
   q=change(v,path,val);no(tag+'/binding '+repr(path),lambda q=q:c.enter_call_projection(cat,q,D(q)))
  for key in ('__enter__','__exit__'):
   q=change(p,('lookup_completed_in_model',key),1)
   no(tag+'/integer substitute parent '+key,lambda q=q:c.enter_call_binding(cat,q,q['instance_anchor'],'explicit conditional premise'),'supplemental parent exact-type output comparison')
  for path,val in [(('call','python_explicit_arguments'),[D(v['binding']['operand_role'])]),(('call','target_role'),D(p['method_roles']['__exit__'])),(('call','callability'),'callable'),(('terminal_python_exception_in_model',),False),(('terminal_python_exception_in_model',),1),(('call_outcome',),'normal-return'),(('helper_dispatch_entry_established',),True),(('current_partial_effects',),'NONE'),(('cleanup_list_state','complete_contents'),[])]:
   q=change(o,path,val);no(tag+'/output '+repr(path),lambda q=q:c.validate_enter_call_projection(cat,D(v),D(v),q),'source-model submitted-output comparison')
  q=D(o);q['call']['target_role']=D(q['call']['retained_exit_role']);q['binding']['method_results']['__enter__']=D(q['binding']['method_results']['__exit__']);q['events'][-1]['method_results']['__enter__']=D(q['binding']['method_results']['__exit__'])
  no(tag+'/coordinated enter-to-exit output substitution',lambda:c.validate_enter_call_projection(cat,D(v),D(v),q),'source-model submitted-output comparison')
  q=D(v);q['scope']['invocation']='coordinated';q['binding']['scope']['invocation']='coordinated';q['parent_result']['scope']['invocation']='coordinated'
  no(tag+'/coordinated candidate versus fixed validated input',lambda:c.enter_call_projection(cat,q,D(v)),'exact comparison to separately retained model premise; not public authentication')
  for path,val in [(('call','python_explicit_arguments'),Array()),(('call',),Map(o['call'])),(('completion',),Text(o['completion'])),(('source_operation_acknowledged','line'),Number(2514))]:
   q=change(o,path,val);no(tag+'/pre-normalization type '+repr(path),lambda q=q:c.validate_enter_call_projection(cat,D(v),D(v),q),'exact submitted-output type gate')
  q=D(o);x=q['call'].pop('target_role');q['call'][Text('target_role')]=x
  no(tag+'/subclassed nested key',lambda:c.validate_enter_call_projection(cat,D(v),D(v),q),'exact submitted-output key gate')
 yes('all eight source occurrences remain distinct',lambda:len({o['events'][-1]['id'] for _,_,o in cases})==8)
 # Shape gates do not invoke derive and cannot establish semantic/public negative validation.
 saved=(HERE/'host/expected/expected-enter-receipt.json').read_bytes();receipt=read(HERE/'host/expected/expected-enter-receipt.json')
 yes('exact saved receipt passes shape only',lambda:a._receipt_shape(saved)==receipt,'pre-derivation receipt-shape gate')
 for idx in range(2):
  q=D(receipt);del q['contexts'][idx]['enter_call_attempt_correspondence']
  no('context %d missing new mandatory relation'%idx,lambda q=q:a._receipt_shape(a.enc(q)),'pre-derivation receipt-shape gate')
 q=D(receipt);q['contexts'].reverse()
 no('reversed receipt context order',lambda:a._receipt_shape(a.enc(q)),'pre-derivation receipt-shape gate')
 return {'public_calls':0,'authenticated_basis_core_calls':0,'full_public_negative_derivations':0,'application_protocol_calls':0,'fresh_model_fixtures':8,'retained_scaffold':'source/reference/r1/tests/fixtures.py; source-constructed only; new absent-control premise None','no_engineering_or_historical_suites_replayed':True}
try:
 details=main();result={'status':'PASS','rows':len(ROWS),'counts':dict((s,sum(r['status']==s for r in ROWS)) for s in ('PASS','REJECTED','FAIL','HARNESS-FAIL','DEFECT-OBSERVED')),'seconds':time.monotonic()-START,'finished_utc':utc(),'qualifications':details};save('RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
except BaseException as e:
 save('FAILURE.json',{'utc':utc(),'exception':repr(e),'completed_rows':len(ROWS)});traceback.print_exc();raise
