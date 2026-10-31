"""New bounded static controls; no application execution or prior campaign replay."""
from pathlib import Path
import sys,copy,json,ast,traceback,gc
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
class S(str):pass
class L(list):pass
class D(dict):pass
def coordinated(v,old,new):
 if type(v) is dict:return {k:coordinated(x,old,new) for k,x in v.items()}
 if type(v) is list:return [coordinated(x,old,new) for x in v]
 return new if type(v) is str and v==old else v
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m)
 print('PHASE authenticated mandatory chain; saved evidence only',flush=True)
 if mode=='primary':
  data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);saved=m.enc(m._assemble(data,rows,basis));rec.save('client-construction-none.json',json.loads(saved));rec.check('actual mandatory derivation creates both contexts',lambda:[c['context'] for c in json.loads(saved)['contexts']]==list(m.CONTEXTS))
 else:
  saved=(root/'results/primary/client-construction-none.json').read_bytes();captures=[];sm=sys.monitoring;assert sm.get_tool(3) is None;sm.use_tool_id(3,'client-construction-basis-observer')
  def capture(code,offset,value):
   if code is m._basis.__code__:captures.append(value)
  sm.register_callback(3,sm.events.PY_RETURN,capture);sm.set_local_events(3,m._basis.__code__,sm.events.PY_RETURN)
  rec.check('fresh recovered actual public validator accepts pristine receipt',lambda:m.validate(root,saved)['result']=='PASS')
  assert len(captures)==1;basis=captures.pop();sm.set_local_events(3,m._basis.__code__,0);sm.register_callback(3,sm.events.PY_RETURN,None);sm.free_tool_id(3);data=basis['fresh'];cat=basis['catalogue'];rows=m._rows(basis)
  rec.check('recovered authenticated derivation equals saved exact bytes',lambda:m.enc(m._assemble(data,rows,basis))==saved)
 print('PHASE focused constructed controls; using the returned authenticated basis, no checker replacement',flush=True)
 c=basis['fresh']['coverage'];fixtures=[]
 for idx in (0,1):
  for control in (False,True):
   tag=str((idx,control));fx=normal(m,basis,idx,control=control);fixtures.append(fx)
   rec.check('legitimate prefix '+tag,lambda fx=fx,control=control:oracle(m._construct_checked(basis,fx)['projection'],control))
   alternate=normal(m,basis,idx,control=control,invocation='another-client-construction');rec.check('distinct occurrence '+tag,lambda alternate=alternate:m._construct_checked(basis,alternate)['projection']==alternate['output'])
   paths=[(('construction_error','reference'),'other'),(('construction_error','construction_attempt','occurrence'),'other'),(('construction_error','construction_attempt','source','site'),'other'),(('construction_error','construction_attempt','argument_token','symbol'),'other'),(('construction_error','construction_attempt','registered_owner','symbol'),'other'),(('construction_error','scope','invocation'),'other'),(('construction_error','failure_mechanism'),'MemoryError'),(('construction_error','initializer_progress'),'entered'),(('construction_error','handler_binding_established_by_this_role'),True),
    (('invocation',),'other'),(('context',),'SYMBOLIC-U-OTHER'),(('anchor',),{}),(('token_case','invocation'),'other'),(('token_case','owner_failure_none'),False),(('none_guard_binding','owner','symbol'),'other'),(('none_guard_binding','slot_value'),False),(('none_guard_binding','guard_result'),True),(('none_guard_binding','source','sha256'),'0'*64),(('projection','references','token','symbol'),'other'),
    (('output','construction_completed_in_model'),True),(('output','client_callback_executed_in_model'),True),(('output','completed_client_object_reference'),fx['projection']['references']['client']),(('output','allocation_progress'),'allocated'),(('output','initializer_progress'),'assigned'),(('output','earlier_control_callback_completed_in_model'),False),(('output','caught_error_in_model','reference'),'other'),(('output','new_explicit_cause_assignment_established_in_model'),True),(('output','exception_chain_observation','existing_cause'),None),(('output','exception_chain_observation','existing_context'),None),(('output','exception_chain_observation','existing_suppression'),False),(('output','construction_reaches_launcher_established'),True),(('output','prior_failure_storage_history'),'ABSENT'),(('output','authorization_renewed'),True)]
   if mode!='primary':paths=paths[::4]
   for path,value in paths:
    q=change(fx,path,value);rec.reject('binding/type/unsupported claim '+tag+str(path),lambda q=q:m._construct_checked(basis,q))
   for stage in ORDER:
    for outcome in ('raise','process-termination','unobserved') if mode=='primary' else ('raise',):
     terminal=(stage,outcome);q=normal(m,basis,idx,control=control,terminal=terminal)
     rec.check('source-admitted frontier '+tag+str(terminal),lambda q=q,control=control,terminal=terminal:oracle(m._construct_checked(basis,q)['projection'],control,terminal))
     bad=change(q,('output','construction_outward_after_finally_established_in_model'),True)
     if q['output']['construction_outward_after_finally_established_in_model'] is not True:rec.reject('no guaranteed construction propagation '+tag+str(terminal),lambda bad=bad:m._construct_checked(basis,bad))
     if not q['output']['removal_completed_in_model']:
      bad=change(q,('output','removal_completed_in_model'),True);rec.reject('no fabricated completed removal '+tag+str(terminal),lambda bad=bad:m._construct_checked(basis,bad))
   if mode=='primary':
    for stage in ORDER[:3]:
     for later in ('raise','process-termination','unobserved'):
      terminal=(stage,'raise');cleanup=('removal-attempt',later);q=normal(m,basis,idx,control=control,terminal=terminal,cleanup_terminal=cleanup)
      rec.check('evaluation then cleanup replacement/uncertainty '+tag+str((stage,later)),lambda q=q,control=control,terminal=terminal,cleanup=cleanup:oracle(m._construct_checked(basis,q)['projection'],control,terminal,cleanup))
   for n in range(len(ORDER)) if mode=='primary' else (0,2,5):
    q=copy.deepcopy(fx);del q['outcomes'][n];q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('coordinated omitted stage '+tag+str(n),lambda q=q:m._construct_checked(basis,q))
   q=copy.deepcopy(fx);q['outcomes'][:2]=reversed(q['outcomes'][:2]);q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('reordered handler/guard '+tag,lambda q=q:m._construct_checked(basis,q))
   q=copy.deepcopy(fx);q['outcomes'].append(copy.deepcopy(q['outcomes'][-1]));q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('duplicate cleanup completion '+tag,lambda q=q:m._construct_checked(basis,q))
   q=change(fx,('output',),alternate['output']);rec.reject('cross invocation output '+tag,lambda q=q:m._construct_checked(basis,q))
   for which in ('owner','token'):
    old=fx['projection']['references'][which]['symbol'];q=coordinated(fx,old,'substituted-'+which);rec.reject('coordinated reference substitution '+tag+which,lambda q=q:m._construct_checked(basis,q))
   q=coordinated(fx,fx['construction_error']['reference'],'substituted-error');rec.reject('coordinated error substitution '+tag,lambda q=q:m._construct_checked(basis,q))
   q=normal(m,basis,idx,control=control,continuity=False);rec.check('continuity remains conditional '+tag,lambda q=q:m._construct_checked(basis,q)['projection']['selected_owner_removed_in_model'] is None)
   for path,value in [(('construction_error','existing_cause'),S('UNKNOWN')),(('construction_error',),D(fx['construction_error'])),(('outcomes',),L(fx['outcomes'])),(('none_guard_binding',),{S(k):v for k,v in fx['none_guard_binding'].items()}),(('output','events'),L(fx['output']['events']))]:
    q=change(fx,path,value);rec.reject('exact-type boundary '+tag+str(path),lambda q=q:m._construct_checked(basis,q))
   got=m._construct_checked(basis,fx);got['projection']['construction_error'].clear();got['projection']['events'].clear();got['anchor'].clear();rec.check('nested returned mutation isolation '+tag,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
   q=change(fx,('projection','none_guard_binding','slot_value'),0);v=m._premises(basis,fx);rec.reject('projector exact None binding '+tag,lambda q=q,v=v:c.client_construction_projection(cat,q['projection'],v))
   q=change(fx,('output','construction_error','existing_context'),S('UNKNOWN'));rec.reject('submitted-output exact type '+tag,lambda q=q,v=v:c.validate_client_construction_projection(cat,fx['projection'],v,q['output']))
 rec.save('fixtures.json',fixtures)
 for idx in (0,1):
  for path,value in [(('construction_completed',),True),(('client_callback_execution',),True),(('declaration','source','selected_slot_value'),False),(('declaration','source','construction_expression','site'),'other'),(('declaration','guard_branches','prefix_control_absent'),'omitted'),(('scope',),{}),(('declaration','source','selected_slot_exact_type'),S('NoneType'))]:
   q=copy.deepcopy(rows);q[idx]=change(q[idx],path,value);rec.reject('semantic claim independent expectation '+str((idx,path)),lambda q=q:m._check_rows(basis,q))
 q=copy.deepcopy(rows)
 for row in q:row['construction_completed']=True;row['declaration']['source']['completed_client_object_established']=True
 rec.reject('both-context coordinated semantic substitution',lambda:m._check_rows(basis,q))
 got=m._rows(basis);got[0]['declaration']['source'].clear();got.clear();rec.check('semantic returned expectations isolated',lambda:m._rows(basis)==rows)
 got=m._assemble(data,rows,basis);got['contexts'][0]['client_construction_none_correspondence'].clear();got['contexts'].clear();rec.check('receipt expectations isolated',lambda:m.enc(m._assemble(data,rows,basis))==saved)
 q=dict(basis['evidence']);key=next(iter(q));q[key]=q[key]+b'changed';rec.reject('stale predecessor evidence',lambda:m._compare_evidence(basis,q));del q[key];rec.reject('missing predecessor evidence',lambda:m._compare_evidence(basis,q))
 for idx in (0,1):
  for relation in ('client_construction_none_correspondence','control_construction_revocation_correspondence','callback_bare_rethrow_correspondence'):
   q=json.loads(saved);del q['contexts'][idx][relation];rec.reject('public mandatory relation '+str((idx,relation)),lambda q=q:m.validate(root,m.enc(q)),reason='CLIENT-CONSTRUCTION-MANDATORY-RELATIONS')
 rec.reject('public exact bytes input',lambda:m.validate(root,saved.decode()),reason='CLIENT-CONSTRUCTION-RECEIPT-BYTES')
 # Source-derived independent coordinates and guards; no candidate application imports.
 raw=m.sources(data)[1];tree=ast.parse(raw);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run');attempts=[n for n in ast.walk(run) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Client'];assert len(attempts)==1;attempt=attempts[0]
 rec.check('independent constructor source identity',lambda:cat['source']['construction_expression']['site']==f'{attempt.lineno}:{attempt.col_offset}:{attempt.end_lineno}:{attempt.end_col_offset}:Call' and ast.get_source_segment(raw.decode(),attempt)=='Client(token)')
 handler=next(n for n in ast.walk(run) if isinstance(n,ast.ExceptHandler) and n.name=='client_error');guard_=handler.body[0].test;bare_=handler.body[1]
 rec.check('independent exact None and bare raise source',lambda:isinstance(guard_.ops[0],ast.IsNot) and guard_.comparators[0].value is None and bare_.exc is None and bare_.cause is None and cat['source']['selected_slot_value'] is None and cat['source']['exception_binding']==handler.name)
 rec.check('both prefix branches source covered',lambda:cat['source']['prefix_order_control_absent']==['owner-create','token-create','registry-insert','control-guard','client-create'] and cat['source']['prefix_order_control_present']==['owner-create','token-create','registry-insert','control-guard','control-create','control-callback','client-create'])
 rec.check('old context fields byte-preserved',lambda:all(all(m.enc(ctx[k])==m.enc(v) for k,v in old.items()) and set(ctx)==set(old)|{'client_construction_none_correspondence'} for ctx,old in zip(json.loads(saved)['contexts'],basis['prior']['contexts'])))
 # New integration controls for preserved branches, not their historical campaigns.
 priorfx=json.loads((root/'retained/control-construction/results/primary/fixtures.json').read_bytes())
 for idx,fx in enumerate(priorfx):rec.check('retained control construction route remains connected '+str(idx),lambda fx=fx:m._construct_prior(basis,'control-construction',fx)['projection']==fx['output'])
 if mode=='primary':
  print('PHASE one coordinated source-catalogue omission check against defining sources',flush=True)
  deps=m.dependencies(data);bad=copy.deepcopy(cat);del bad['source']['prefix_order_control_absent'];del bad['guard_branches']['prefix_control_absent'];rec.reject('coordinated source prefix omission',lambda:c.validate_client_construction(*m.sources(data)[:2],*deps,bad),reason='CLIENT-CONSTRUCTION-SOURCE-CORRESPONDENCE')
 rec.save('final-verification.json',verify_root(root));rec.save('semantic-rows.json',rows)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,scope='New constructed client-construction exact-None slice; prior counts separate',CLI_execution_claimed=False,authenticated_basis_use='Actual mandatory chain return; no validation-function replacement')
