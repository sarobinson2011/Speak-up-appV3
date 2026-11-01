"""New adapter-bound controls. Saved inputs only; prior campaigns are not replayed."""
from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]);rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
class S(str):pass
class L(list):pass
class D(dict):pass
def coordinated(v,old,new):
 if type(v) is dict:return {k:coordinated(x,old,new) for k,x in v.items()}
 if type(v) is list:return [coordinated(x,old,new) for x in v]
 return new if type(v) is str and v==old else v
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m)
 print('PHASE actual mandatory predecessor public validation; saved inputs only',flush=True)
 if mode=='primary':
  data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);saved=m.enc(m._assemble(data,rows,basis));rec.save('launcher-details.json',json.loads(saved))
  rec.check('new mandatory derivation accepts both contexts after actual predecessor public validation',lambda:[x['context'] for x in json.loads(saved)['contexts']]==list(m.CONTEXTS))
 else:
  saved=(root/'results/primary/launcher-details.json').read_bytes();captures=[];sm=sys.monitoring;assert sm.get_tool(3) is None;sm.use_tool_id(3,'launcher-details-current-basis-observer')
  def capture(code,offset,value):
   if code is m._basis.__code__:captures.append(value)
  sm.register_callback(3,sm.events.PY_RETURN,capture);sm.set_local_events(3,m._basis.__code__,sm.events.PY_RETURN)
  rec.check('fresh recovered actual public validator accepts pristine receipt',lambda:m.validate(root,saved)['result']=='PASS')
  assert len(captures)==1;basis=captures.pop();sm.set_local_events(3,m._basis.__code__,0);sm.register_callback(3,sm.events.PY_RETURN,None);sm.free_tool_id(3);data=basis['fresh'];cat=basis['catalogue'];rows=m._rows(basis)
  rec.check('recovered authenticated derivation is exact saved bytes',lambda:m.enc(m._assemble(data,rows,basis))==saved)
 c=basis['fresh']['coverage'];source=cat['source'];rec.save('predecessor-public-result.json',basis['public_predecessor']);print('PHASE focused controls using authenticated returned basis; no function replacement',flush=True);fixtures=[]
 for idx in (0,1):
  for control in (False,True):
   tag=str((idx,control));fx=normal(m,basis,idx,control=control);fixtures.append(fx)
   rec.check('legitimate complete initial details '+tag,lambda fx=fx,control=control:oracle(m._construct_checked(basis,fx)['projection'],source,control))
   alternative=normal(m,basis,idx,control=control,invocation='distinct-launcher-details-B')
   rec.check('distinct invocation remains distinct '+tag,lambda alternative=alternative:m._construct_checked(basis,alternative)['projection']==alternative['output'])
   q=normal(m,basis,idx,control=control,owner_continuity=False)
   rec.check('selected owner continuity remains conditional '+tag,lambda q=q:m._construct_checked(basis,q)['projection']['validated_parent']['selected_owner_removed_in_model'] is None)
   q=normal(m,basis,idx,control=control,continuity='UNESTABLISHED')
   rec.check('unestablished delivery does not reach handler '+tag,lambda q=q:m._construct_checked(basis,q)['projection']['launcher_e_in_model'] is None)
   bad=change(q,('outcomes',),fx['outcomes']);bad['projection']['outcomes']=copy.deepcopy(fx['outcomes'])
   rec.reject('false continuation without delivery premise '+tag,lambda bad=bad:m._construct_checked(basis,bad))
   paths=[(('context',),'SYMBOLIC-U-OTHER'),(('invocation',),'wrong'),(('anchor','instance','binding'),'wrong'),(('parent_output','last_pending_error_in_model','reference'),'other-error'),(('parent_output','removal_completed_in_model'),False),(('parent_output','construction_outward_after_finally_established_in_model'),False),
    (('delivery_binding','selected_error','reference'),'wrong'),(('delivery_binding','selected_error','construction_attempt','source','site'),'wrong'),(('delivery_binding','references','owner','symbol'),'wrong'),(('delivery_binding','references','token','symbol'),'wrong'),(('delivery_binding','references','session','symbol'),'wrong'),(('delivery_binding','instance_anchor','instance','binding'),'wrong'),(('delivery_binding','launcher_name'),'client_error'),(('delivery_binding','route',2,'source','site'),'wrong'),
    (('output','details_in_model','dynamic_fields',0,'exact_value'),'RuntimeError'),(('output','details_in_model','dynamic_fields',1,'exact_value'),'invented message'),(('output','details_in_model','dynamic_fields',2,'formatted_bytes'),'invented traceback'),(('output','details_in_model','known_literal_fields','new_authorization'),True),(('output','details_in_model','known_literal_fields','nonexecution_established'),0),(('output','details_in_model','known_literal_fields','cleanup'),[['managed','close returned']]),
    (('output','cleanup_loop_entered'),True),(('output','normal_managed_close_spliced'),True),(('output','managed_clear_spliced'),True),(('output','ACTIVE_unlink_spliced'),True),(('output','failure_file_established'),True),(('output','outward_propagation_established'),True),(('output','runtime_handler_arrival'),True),(('output','authorization_renewed'),True),(('output','launcher_e_in_model','reference'),'wrong')]
   if mode!='primary':paths=paths[::3]
   for path,value in paths:
    bad=change(fx,path,value);rec.reject('wrong binding or invented claim '+tag+str(path),lambda bad=bad:m._construct_checked(basis,bad))
   for stage in source['order']:
    for kind in ('raise','process-termination','unobserved') if mode=='primary' else ('raise',):
     terminal=(stage,kind);q=normal(m,basis,idx,control=control,terminal=terminal)
     rec.check('conditional frontier '+tag+str(terminal),lambda q=q,control=control,terminal=terminal:oracle(m._construct_checked(basis,q)['projection'],source,control,terminal))
     bad=change(q,('output','details_assignment_completed_in_model'),True);bad['output']['details_in_model']=copy.deepcopy(fx['output']['details_in_model'])
     rec.reject('no false completed details '+tag+str(terminal),lambda bad=bad:m._construct_checked(basis,bad))
   # The old validator accepts these genuine modeled replacement frontiers.
   # This new slice must reject them even though removal completed normally.
   factory=m.module(basis['prior_basis']['fresh']['root']/'tests/cases.py','_parent_variants');p=basis['prior_module'];pb=basis['prior_basis']
   for stage in ('callback-handler-enter','callback-none-guard','callback-bare-rethrow'):
    pc=factory.normal(p,pb,idx,control=control,invocation=fx['invocation'],terminal=(stage,'raise'));po=p._construct_checked(pb,pc)['projection']
    rec.check('predecessor supports handler replacement with completed removal '+tag+stage,lambda po=po:po['removal_completed_in_model'] is True and po['handler_evaluation_error_in_model'] is not None and po['outward_error_after_finally_in_model']==po['handler_evaluation_error_in_model'])
    bad=copy.deepcopy(fx);bad['parent_case']=pc;bad['parent_output']=po;bad['delivery_binding']=c.launcher_delivery_binding(cat,po,bad['anchor'],'explicit conditional premise');bad['projection']=m._premises(basis,bad)
    rec.reject('completed pop is insufficient for selected constructor '+tag+stage,lambda bad=bad:m._construct_checked(basis,bad),reason='DETAILS-PARENT-COMPLETION')
    if idx==0 and not control and stage=='callback-none-guard':rec.save('preserved-parent-replacement-case.json',bad)
   for n in range(len(source['order'])) if mode=='primary' else (0,3,4,5,19,20):
    bad=copy.deepcopy(fx);del bad['outcomes'][n];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);rec.reject('missing stage '+tag+str(n),lambda bad=bad:m._construct_checked(basis,bad))
   for a,b in ((1,2),(6,7),(8,10),(19,20)):
    bad=copy.deepcopy(fx);bad['outcomes'][a],bad['outcomes'][b]=bad['outcomes'][b],bad['outcomes'][a];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);rec.reject('reordered bridge/evaluation/assignment '+tag+str((a,b)),lambda bad=bad:m._construct_checked(basis,bad))
   for stage in ('close-attempt','managed-clear','unlink-complete'):
    bad=copy.deepcopy(fx);bad['outcomes'].append({'stage':stage,'outcome':'normal'});bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);rec.reject('no normal-exit splice '+tag+stage,lambda bad=bad:m._construct_checked(basis,bad))
   for role in ('owner','token'):
    old=fx['delivery_binding']['references'][role]['symbol'];bad=coordinated(fx,old,'coordinated-'+role);rec.reject('coordinated owner/token '+tag+role,lambda bad=bad:m._construct_checked(basis,bad))
   old=fx['delivery_binding']['selected_error']['reference'];bad=coordinated(fx,old,'coordinated-error');rec.reject('coordinated constructor error '+tag,lambda bad=bad:m._construct_checked(basis,bad))
   for path,value in [(('delivery_binding','existing_cause'),S('UNKNOWN')),(('delivery_binding',),D(fx['delivery_binding'])),(('outcomes',),L(fx['outcomes'])),(('output','details_in_model','known_literal_fields'),{S(k):v for k,v in fx['output']['details_in_model']['known_literal_fields'].items()}),(('output','details_in_model','known_literal_fields','cleanup'),L([]))]:
    bad=change(fx,path,value);rec.reject('exact-type boundary '+tag+str(path),lambda bad=bad:m._construct_checked(basis,bad))
   got=m._construct_checked(basis,fx);got['projection']['details_in_model']['known_literal_fields']['cleanup'].append('mutated');got['projection']['validated_parent']['construction_error'].clear();got['anchor'].clear()
   rec.check('returned nested mutation does not change expectations '+tag,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
   v=m._premises(basis,fx);bad=change(fx['output'],('details_in_model','dynamic_fields',0,'name'),S('error'))
   rec.reject('direct submitted-output exact type '+tag,lambda bad=bad,v=v:c.validate_launcher_details_projection(cat,fx['projection'],v,bad))
   bad=change(fx,('output',),alternative['output']);rec.reject('cross invocation result '+tag,lambda bad=bad:m._construct_checked(basis,bad))
 rec.save('fixtures.json',fixtures)
 for idx in (0,1):
  for path,value in [(('declaration','source','catch_binding'),'wrong'),(('declaration','source','order'),source['order'][:-1]),(('runtime_handler_details_chain',),[]),(('declaration','guard_branches','parent'),'pop alone'),(('instance_anchor','instance','binding'),'wrong'),(('exact_generated_message',),'fabricated'),(('declaration','source','fields',0,'name'),S('error'))]:
   q=copy.deepcopy(rows);q[idx]=change(q[idx],path,value);rec.reject('semantic claim '+str((idx,path)),lambda q=q:m._check_rows(basis,q))
 q=copy.deepcopy(rows)
 for row in q:row['declaration']['source']['order'].pop();row['declaration']['declarations'].pop()
 rec.reject('both-context coordinated semantic omission',lambda:m._check_rows(basis,q))
 got=m._rows(basis);got[0]['declaration']['source'].clear();got.clear();rec.check('semantic expectation isolation',lambda:m._rows(basis)==rows)
 got=m._assemble(data,rows,basis);got['contexts'][0][m.RELATION].clear();got['contexts'].clear();rec.check('assembled receipt expectation isolation',lambda:m.enc(m._assemble(data,rows,basis))==saved)
 rec.check('checked receipt positive',lambda:m._receipt_checked(basis,saved)['result']=='PASS')
 bad=json.loads(saved)
 for row in bad['contexts']:row[m.RELATION]['runtime_handler_details_chain']=[]
 rec.reject('coordinated receipt at checked comparison only',lambda:m._receipt_checked(basis,m.enc(bad)),reason='DETAILS-STALE-OR-ALTERED-RECEIPT')
 q=dict(basis['evidence']);k=next(iter(q));q[k]+=b'changed';rec.reject('stale underlying evidence',lambda:m._compare_evidence(basis,q));del q[k];rec.reject('missing underlying evidence',lambda:m._compare_evidence(basis,q))
 candidate=dict(data);candidate['prior']=copy.deepcopy(data['prior']);candidate['prior']['contexts'][0]['client_construction_none_correspondence']['instance_anchor']['instance']['binding']='wrong'
 rec.reject('coordinated stale predecessor report',lambda:m._check_candidate(basis,candidate,cat))
 candidate=dict(data);candidate['sources']=(data['sources'][0]+b'\n',data['sources'][1]);rec.reject('mixed source input',lambda:m._check_candidate(basis,candidate,cat))
 for idx in (0,1):
  for rel in sorted(m.REQUIRED):
   q=json.loads(saved);del q['contexts'][idx][rel];rec.reject('public missing mandatory relation '+str((idx,rel)),lambda q=q:m.validate(root,m.enc(q)),reason='DETAILS-MANDATORY-RELATIONS')
 rec.reject('public exact bytes input',lambda:m.validate(root,saved.decode()),reason='DETAILS-RECEIPT-BYTES')
 rec.check('all prior context fields remain byte-exact',lambda:all(all(m.enc(new[k])==m.enc(v) for k,v in old.items()) and set(new)==set(old)|{m.RELATION} for new,old in zip(json.loads(saved)['contexts'],basis['prior']['contexts'])))
 rec.save('semantic-rows.json',rows);rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,scope='New launcher initial-details adapter controls; no prior campaign replay',CLI_execution_claimed=False,public_negative_scope='Missing relations/type at pre-derivation gate; other receipt mutants use actual checked comparison with authenticated basis, not separate full public derivations',predecessor_validation='Actual unmodified public validator; passive basis return, no function replacement')
