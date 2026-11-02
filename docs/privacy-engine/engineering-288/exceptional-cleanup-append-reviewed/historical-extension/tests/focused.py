"""Focused controls for new cleanup relation; authenticated basis cores are explicitly distinguished."""
from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]);rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
class S(str):pass
class L(list):pass
class D(dict):pass
class I(int):pass
def coordinated(v,old,new):
 if type(v) is dict:return {k:coordinated(x,old,new) for k,x in v.items()}
 if type(v) is list:return [coordinated(x,old,new) for x in v]
 return new if type(v) is str and v==old else v
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m);saved=(root/'receipts/prepared-cleanup-append.json').read_bytes()
 # Capture only the basis returned by this actual current public call. No replacements.
 captures=[];sm=sys.monitoring;assert sm.get_tool(5) is None;lease='cleanup-focused-observer:'+str(id(captures))
 try:
  sm.use_tool_id(5,lease)
  def capture(code,offset,value):
   if code is m._basis.__code__:captures.append(value)
  sm.register_callback(5,sm.events.PY_RETURN,capture);sm.set_local_events(5,m._basis.__code__,sm.events.PY_RETURN)
  print('PHASE actual current public validation through unchanged mandatory LD01 predecessor',flush=True)
  result=rec.check('actual full current public positive',lambda:m.validate(root,saved));rec.save('actual-public-result.json',result)
 finally:
  if sm.get_tool(5) is lease:
   try:sm.set_local_events(5,m._basis.__code__,0)
   finally:
    try:sm.register_callback(5,sm.events.PY_RETURN,None)
    finally:sm.free_tool_id(5)
 assert len(captures)==1;basis=captures[0];data=basis['fresh'];cat=basis['catalogue'];c=data['coverage'];source=cat['source'];rows=m._rows(basis)
 rec.save('predecessor-public-result.json',basis['public_predecessor']);rec.check('actual unchanged predecessor public receipt identity',lambda:basis['public_predecessor']['result']=='PASS' and basis['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT)
 actual=m.enc(m._assemble(data,rows,basis));rec.check('fresh authenticated derivation matches prepared bytes',lambda:actual==saved);(rec.path/'cleanup-append.json').write_bytes(actual)
 print('PHASE new focused controls against authenticated returned basis; no full negative derivation',flush=True)
 fixtures=[]
 for idx in (0,1):
  for control in (False,True):
   tag=str((idx,control));fx=normal(m,basis,idx,control=control);fixtures.append(fx)
   rec.check('legitimate selected managed normal append '+tag,lambda fx=fx,control=control:oracle(m._construct_checked(basis,fx)['projection'],source,control))
   alt=normal(m,basis,idx,control=control,invocation='distinct-cleanup-B');rec.check('distinct occurrence preserved '+tag,lambda alt=alt:m._construct_checked(basis,alt)['projection']['scope']['invocation']!=fx['output']['scope']['invocation'])
   q=normal(m,basis,idx,control=control,continuity='UNESTABLISHED');rec.check('unknown local continuity stops before selection '+tag,lambda q=q:len(m._construct_checked(basis,q)['projection']['events'])==1)
   bad=copy.deepcopy(q);bad['outcomes']=copy.deepcopy(fx['outcomes']);bad['projection']['outcomes']=copy.deepcopy(fx['outcomes']);bad['close_case']=copy.deepcopy(fx['close_case']);bad['projection']['close_result']=copy.deepcopy(fx['projection']['close_result'])
   rec.reject('no false continuation from missing continuity '+tag,lambda bad=bad:m._construct_checked(basis,bad))
   paths=[(('context',),'SYMBOLIC-U-OTHER'),(('invocation',),'wrong'),(('anchor','instance','binding'),'wrong'),(('parent_output','last_pending_error_in_model','reference'),'wrong'),(('parent_output','details_assignment_completed_in_model'),False),
    (('binding','name'),'raw'),(('binding','selected_index'),0),(('binding','ordered_values',0,'value'),{'surviving':'raw'}),(('binding','object','symbol'),'arbitrary-object'),(('binding','references','owner','symbol'),'wrong'),(('binding','references','token','symbol'),'wrong'),(('binding','guard','result'),False),(('binding','guard','right'),False),(('binding','guard','expression'),'bool(obj)'),
    (('binding','close_receiver','symbol'),'wrong'),(('binding','method'),'state'),(('binding','method_origin','site'),'wrong'),(('binding','cleanup_list','symbol'),'other-list'),(('binding','append_item'),['raw','close returned']),(('binding','selected_error','reference'),'wrong'),
    (('close_case','method'),'state'),(('close_case','scope','instance'),'wrong'),(('close_case','scope','invocation'),'wrong'),
    (('output','details_after_acknowledged_steps','known_literal_fields','new_authorization'),True),(('output','details_after_acknowledged_steps','known_literal_fields','nonexecution_established'),0),(('output','details_after_acknowledged_steps','dynamic_fields',0,'exact_value'),'RuntimeError'),(('output','close_return_value_observed'),'invented'),(('output','physical_closure_established'),True),(('output','loop_completion_established'),True),(('output','error_report_append_expanded'),True),(('output','failure_file_established'),True),(('output','final_rethrow_established'),True),(('output','owner_finalization_established'),True)]
   if mode=='recovered':paths=paths[::2]
   for path,value in paths:
    bad=change(fx,path,value);rec.reject('wrong binding/claim '+tag+str(path),lambda bad=bad:m._construct_checked(basis,bad))
   stages=source['order'] if mode=='primary' else ['loop-input-evaluation','input-managed-object','raw-guard-result','managed-bind-obj','managed-guard-result','close-method-evaluation','close-call-attempt','append-list-resolution','append-call-attempt','append-complete']
   for stage in stages:
    for kind in (('raise','process-termination','unobserved') if mode=='primary' else ('raise',)):
     if stage=='close-normal-return' and kind=='raise':continue # Dedicated reference-interpreter abrupt case below.
     terminal=(stage,kind);q=normal(m,basis,idx,control=control,terminal=terminal)
     rec.check('source frontier '+tag+str(terminal),lambda q=q,control=control,terminal=terminal:oracle(m._construct_checked(basis,q)['projection'],source,control,terminal))
     bad=change(q,('output','append_completed_in_model'),True);bad['output']['details_after_acknowledged_steps']=copy.deepcopy(fx['output']['details_after_acknowledged_steps'])
     rec.reject('no false append completion '+tag+str(terminal),lambda bad=bad:m._construct_checked(basis,bad))
     if source['stages'][stage]['semantic_region']=='protected-append' and kind=='raise':
      bad=change(q,('output','close_normal_return_completed_in_model'),False);bad['output']['close_itself_failed_established_in_model']=True
      rec.reject('append failure cannot erase close return or become close failure '+tag+stage,lambda bad=bad:m._construct_checked(basis,bad))
   for i in range(len(source['order'])) if mode=='primary' else (0,5,13,21,len(source['order'])-1):
    bad=copy.deepcopy(fx);del bad['outcomes'][i];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);rec.reject('missing stage '+tag+str(i),lambda bad=bad:m._construct_checked(basis,bad))
   for a,b in [(1,4),(-1,-2),(-9,-10),(21,22)]:
    bad=copy.deepcopy(fx);bad['outcomes'][a],bad['outcomes'][b]=bad['outcomes'][b],bad['outcomes'][a];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);rec.reject('reordered stages '+tag+str((a,b)),lambda bad=bad:m._construct_checked(basis,bad))
   for role in ('owner','token','manager','session'):
    old=fx['binding']['references'][role]['symbol'];bad=coordinated(fx,old,'coordinated-'+role);rec.reject('coordinated role '+tag+role,lambda bad=bad:m._construct_checked(basis,bad))
   for name,old in [('error',fx['binding']['selected_error']['reference']),('cleanup-list',fx['binding']['cleanup_list']['symbol']),('instance',fx['anchor']['instance']['binding'])]:
    bad=coordinated(fx,old,'coordinated-'+name);rec.reject('coordinated '+tag+name,lambda bad=bad:m._construct_checked(basis,bad))
   for path,value in [(('binding','name'),S('managed')),(('binding','selected_index'),I(1)),(('binding',),D(fx['binding'])),(('outcomes',),L(fx['outcomes'])),(('output','details_after_acknowledged_steps','known_literal_fields'),{S(k):v for k,v in fx['output']['details_after_acknowledged_steps']['known_literal_fields'].items()}),(('output','binding','append_item'),L(['managed','close returned']))]:
    bad=change(fx,path,value);rec.reject('exact types before comparison '+tag+str(path),lambda bad=bad:m._construct_checked(basis,bad))
   bad=change(fx,('output',),alt['output']);rec.reject('cross-invocation output '+tag,lambda bad=bad:m._construct_checked(basis,bad))
   got=m._construct_checked(basis,fx);got['projection']['binding']['object'].clear();got['projection']['details_after_acknowledged_steps']['known_literal_fields']['cleanup'][0].clear();got['anchor'].clear()
   rec.check('nested returned mutation cannot change expectations '+tag,lambda:m._construct_checked(basis,fx)['projection']==fx['output'])
   v=m._premises(basis,fx);bad=change(fx['output'],('binding','name'),S('managed'));rec.reject('direct submitted-output exact types '+tag,lambda:c.validate_cleanup_append_projection(cat,fx['projection'],v,bad))
   # Legitimate predecessor interruption/replacement never selects this relation.
   factory=m.module(basis['prior_basis']['fresh']['root']/'tests/cases.py','_details_cases');p=basis['prior_module'];pb=basis['prior_basis']
   for term in [('details-value-message','raise'),('details-assignment-complete','unobserved')]:
    pc=factory.normal(p,pb,idx,control=control,invocation=fx['invocation'],terminal=term);po=p._construct_checked(pb,pc)['projection'];bad=copy.deepcopy(fx);bad['parent_case']=pc;bad['parent_output']=po
    rec.reject('incomplete/replaced predecessor '+tag+str(term),lambda bad=bad:m._construct_checked(basis,bad))
 # Source-admitted close variants use existing reference-path interpreter.
 for phase,live,retired in [('CLOSED',None,None),('QUARANTINED',None,'retired-A'),('CLEANUP_UNCERTAIN','live-A','retired-A')]:
  q=normal(m,basis,phase=phase,live=live,retired=retired);rec.check('legitimate managed close starting references '+phase,lambda q=q:m._construct_checked(basis,q)['projection']['append_completed_in_model'])
 # Derive the opaque underlying-close gate from the existing interpreter trace.
 fx=fixtures[0];trace=fx['projection']['close_result'];rec.save('managed-close-reference-example.json',trace)
 gate=next(e['address'] for e in trace['events'] if e['event']=='premise' and e['kind']=='call:self._retired.close')
 for idx in (0,1):
  for control in (False,True):
   q=normal(m,basis,idx,control=control,terminal=('close-normal-return','raise'),close_outcomes={gate:'raise'})
   rec.check('source-derived close exception distinct '+str((idx,control)),lambda q=q,control=control:oracle(m._construct_checked(basis,q)['projection'],source,control,('close-normal-return','raise')) and q['output']['close_itself_failed_established_in_model'])
   bad=change(q,('output','close_normal_return_completed_in_model'),True);rec.reject('close failure cannot become return '+str((idx,control)),lambda bad=bad:m._construct_checked(basis,bad))
 # A stale or missing validated close return cannot be supplied as a new success.
 for path,value in [(('close_case',),None),(('projection','close_result','completion'),'abrupt'),(('projection','close_result','final','_phase'),'READY')]:
  bad=change(fx,path,value);rec.reject('close result binding '+str(path),lambda bad=bad:m._construct_checked(basis,bad))
 for idx in (0,1):
  for path,value in [(('declaration','source','selected_name'),'raw'),(('declaration','source','guard_results','managed'),False),(('declaration','source','order'),source['order'][:-1]),(('runtime_cleanup_append_chain',),[]),(('instance_anchor','instance','binding'),'wrong'),(('declaration','source','append_message'),S('close returned'))]:
   q=copy.deepcopy(rows);q[idx]=change(q[idx],path,value);rec.reject('semantic core claim '+str((idx,path)),lambda q=q:m._check_rows(basis,q))
 q=copy.deepcopy(rows)
 for row in q:row['declaration']['source']['order'].pop();row['declaration']['declarations'].pop()
 rec.reject('coordinated both-context catalogue/claims',lambda:m._check_rows(basis,q))
 badcat=copy.deepcopy(cat);badcat['source']['order'].pop();badcat['declarations'].pop();rec.reject('source-derived catalogue independently required',lambda:m._check_candidate(basis,data,badcat,q))
 got=m._rows(basis);got[0]['declaration']['source'].clear();got.clear();rec.check('semantic output expectation isolation',lambda:m._rows(basis)==rows)
 got=m._assemble(data,rows,basis);got['contexts'][0][m.RELATION].clear();got['contexts'].clear();rec.check('receipt construction expectation isolation',lambda:m.enc(m._assemble(data,rows,basis))==saved)
 bad=json.loads(saved)
 for row in bad['contexts']:row[m.RELATION]['runtime_cleanup_append_chain']=[]
 rec.reject('coordinated receipt comparison core',lambda:m._receipt_checked(basis,m.enc(bad)),'CLEANUP-STALE-OR-ALTERED-RECEIPT')
 candidate=dict(data);candidate['prior']=copy.deepcopy(data['prior']);candidate['prior']['contexts'][0]['launcher_initial_details_correspondence']['instance_anchor']['instance']['binding']='wrong';rec.reject('stale predecessor summary core',lambda:m._check_candidate(basis,candidate,cat))
 ev=dict(basis['evidence']);k=next(iter(ev));ev[k]+=b'changed';rec.reject('altered authenticated evidence core',lambda:m._compare_evidence(basis,ev));del ev[k];rec.reject('missing evidence core',lambda:m._compare_evidence(basis,ev))
 for idx in (0,1):
  for rel in sorted(m.REQUIRED):
   q=json.loads(saved);del q['contexts'][idx][rel];rec.reject('public missing required relation '+str((idx,rel)),lambda q=q:m.validate(root,m.enc(q)),'CLEANUP-MANDATORY-RELATIONS')
 rec.reject('public exact receipt bytes',lambda:m.validate(root,saved.decode()),'CLEANUP-RECEIPT-BYTES')
 rec.check('all inherited context relations preserved',lambda:all(all(m.enc(new[k])==m.enc(v) for k,v in old.items()) and set(new)==set(old)|{m.RELATION} for new,old in zip(json.loads(saved)['contexts'],basis['prior']['contexts'])))
 rec.save('fixtures.json',fixtures);rec.save('validation-layers.json',{'full_current_public_positive':1,'full_predecessor_public_positive':1,'full_public_negative_derivations':0,'public_negatives':'required-relation/type gates before derivation','other_negatives':'authenticated-basis constructed/semantic/receipt-comparison cores','runtime_observations':False});rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,scope='New selected exceptional cleanup/normal append controls; no completed campaigns replayed',full_public_negative_derivations_claimed=0,independent_review='PENDING')
