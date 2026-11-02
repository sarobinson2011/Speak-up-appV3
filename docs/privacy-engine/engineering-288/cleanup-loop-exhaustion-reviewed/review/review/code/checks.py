"""Focused fresh review of the loop slice with the actual returned public basis."""
from common import *
from loop_expectations import derive,ORDER,NORMAL
from loop_cases import make,refresh,frontier,oracle
class Text(str):pass
class Seq(list):pass
class Obj(dict):pass
def run(m,b,public,saved,r):
 core='actual-authenticated-basis constructed core; selected parent revalidated by unchanged predecessor'
 output='actual-authenticated-basis output comparison after selected parent revalidation'
 semantic='actual-authenticated-basis catalogue/claims comparison'
 c=b['fresh']['coverage'];cat=b['catalogue'];expect=derive(b['fresh']['sources'][0]);r.save('source-expectations.json',expect)
 def keep(n,fn,layer,actual=None):
  vals=list(fn.__defaults__ or ())
  for cell in fn.__closure__ or ():
   try:vals.append(cell.cell_contents)
   except ValueError:pass
  cases=[v for v in vals if type(v) is dict and v.get('kind')=='CONSTRUCTED-CLEANUP-LOOP']
  if cases:r.save('smallest-pending-case.json',cases[0])
  r.save('failing-check.json',{'check':n,'layer':layer})
  if actual is not None:r.save('unexpected-accepted-result.json',actual)
 def y(n,fn,layer=core):
  try:return r.yes(n,fn,layer)
  except BaseException:keep(n,fn,layer);raise
 def no(n,fn,code=None,layer=core):
  returned=[]
  def probe():v=fn();returned.append(v);return v
  try:return r.no(n,probe,code,layer)
  except BaseException:keep(n,fn,layer,returned[0] if returned else None);raise
 def source_check():
  s=cat['source']
  for k in ('order','normal_outcomes','entry_count','selected_index','next_index','target_names','caught_name','outer_caught_name'):assert s[k]==expect[k],k
  assert [[p['name'],p['slot']] for p in s['ordered_inputs']]==expect['ordered_inputs']
  assert s['required_guard_results']=={'raw':False,'managed':True} and s['guard_expression']=='obj is not None'
  for k in ('handler','loop','stop_before'):assert all(s[k][a]==v for a,v in expect[k].items()),k
  for stage in ORDER:assert all(s['stages'][stage][a]==v for a,v in expect['stages'][stage].items()),stage
  assert [d['id'] for d in cat['declarations']]==ORDER and all(d['classification']=='UNKNOWN' and d['multiplicity'] is d['ordinal'] is None for d in cat['declarations'])
  assert s['language_contract']['sections']==['8.3 for','8.4.1 except']
  return True
 y('independent defining AST and Python language boundary correspond',source_check,'source-derived AST/coordinates plus separately consulted Python3.12 reference; no application execution')
 normals={}
 for idx in range(2):
  for control in (False,True):
   for origin in ('close','append'):
    key=(idx,control,origin);q=make(m,b,idx,control,origin);normals[key]=q;label=f'{idx}-{control}-{origin}'
    o=y(label+' explicit normal departure and exact exhaustion',lambda q=q:(lambda o:(oracle(q,o,expect),o)[1])(m._construct_checked(b,q)))
    r.save('fixture-'+label+'.json',q)
    bad=change(q,['output','terminal_python_exception_in_model'],False)
    no(label+' normal suboperations cannot erase pending exception',lambda bad=bad:m._construct_checked(b,bad),'LOOP-OUTPUT-CORRESPONDENCE',output)
    bad=change(q,['output','last_pending_error_in_model'],q['parent_output']['selected_cleanup_error'])
    no(label+' exited handler restores original pending role',lambda bad=bad:m._construct_checked(b,bad),'LOOP-OUTPUT-CORRESPONDENCE',output)
 # Every new semantic frontier, four nonnormal classes, alternated contexts/prefixes/origins.
 summary=[]
 for i,stage in enumerate(ORDER):
  for j,kind in enumerate(('raise','catchable-interruption','process-termination','unobserved')):
   base=normals[(i+j)%2,bool((i+j)//2%2),'append' if j%2 else 'close'];q=frontier(b,base,stage,kind)
   o=y(stage+'/'+kind+' stops and preserves acknowledged facts',lambda q=q:(lambda o:(oracle(q,o,expect),o)[1])(m._construct_checked(b,q)))['projection']
   summary.append({'stage':stage,'outcome':kind,'context':q['context'],'control':o['earlier_control_completed_in_model'],'origin':o['failure_origin_region'],'completed':o['loop_completion_established'],'caught':o['caught_name_lifetime'],'pending':o['last_pending_error_in_model'],'terminal':o['terminal_python_exception_in_model']})
   bad=change(q,['output','loop_completion_established'],True)
   no(stage+'/'+kind+' cannot invent completed loop',lambda bad=bad:m._construct_checked(b,bad),'LOOP-OUTPUT-CORRESPONDENCE',output)
   bad=change(q,['output','terminal_python_exception_in_model'],None if kind in ('raise','catchable-interruption') else True)
   no(stage+'/'+kind+' preserves exception-versus-uncertainty class',lambda bad=bad:m._construct_checked(b,bad),'LOOP-OUTPUT-CORRESPONDENCE',output)
 r.save('frontier-summary.json',summary)
 for idx in range(2):
  q=frontier(b,normals[idx,bool(idx),'append'],ORDER[0],'unobserved','UNESTABLISHED')
  y(str(idx)+' absent continuity establishes no departure',lambda q=q:oracle(q,m._construct_checked(b,q),expect))
  bad=D(q);bad['outcomes'][0]['outcome']='normal';bad['projection']['outcomes']=D(bad['outcomes'])
  no(str(idx)+' cannot assert progress with missing continuity',lambda bad=bad:m._construct_checked(b,bad),'LOOP-UNKNOWN-CONTINUITY')
 q=normals[0,False,'append']
 # Each mutation changes all submitted binding copies; the unchanged parent is authoritative.
 changes=[('order',['loop','ordered_values'],list(reversed(q['binding']['loop']['ordered_values']))),('count',['loop','entry_count'],3),('selected index',['loop','selected_index'],0),('next index',['loop','next_index'],1),('raw skip',['loop','raw_body_skipped'],False),('last item',['loop','selected_is_last'],False),('iterator',['loop','iterator_role'],'another-iterator'),('owner',['references','owner'],'another-owner'),('token',['references','token'],'another-token'),('append occurrence',['append_occurrence','id'],'another-invocation/append'),('error reference',['selected_cleanup_error','reference'],'another-error'),('constructor reference',['original_constructor_error','reference'],'another-constructor'),('handler site',['handler_origin','site'],'171:0:171:1:Name'),('list',['cleanup_list','symbol'],'another-list'),('name',['selected_name'],'raw'),('instance',['instance_anchor'],normals[1,False,'append']['anchor'])]
 for name,path,v in changes:
  bad=change(q,['binding',*path],v);bad['projection']['binding']=D(bad['binding'])
  no('coordinated wrong '+name,lambda bad=bad:m._construct_checked(b,bad),'LOOP-EXPECTED-BINDING')
 for name,mut in [('missing departure',lambda a:a.pop(0)),('duplicate exit',lambda a:a.insert(2,D(a[1]))),('premature exhaustion',lambda a:a.insert(0,a.pop(4))),('omitted completion',lambda a:a.pop()),('additional body',lambda a:a.append({'stage':'selected-loop-body-complete','outcome':'normal'})),('exhaustion labelled normal',lambda a:a[4].update(outcome='normal'))]:
  bad=D(q);mut(bad['outcomes']);bad['projection']['outcomes']=D(bad['outcomes'])
  no(name,lambda bad=bad:m._construct_checked(b,bad),layer='source step/order/continuation gate after authenticated parent revalidation')
 stopped=frontier(b,q,ORDER[1],'raise');bad=D(stopped);bad['outcomes'].append({'stage':ORDER[2],'outcome':'normal'});bad['projection']['outcomes']=D(bad['outcomes'])
 no('no continuation after replacement error',lambda:m._construct_checked(b,bad),'LOOP-UNREACHED-STEPS')
 for name,path,v in [('unvalidated selected parent',['parent_output','events',-1,'id'],'substituted-append'),('parent never completed',['parent_output','report_append_completed_in_model'],False)]:
  bad=change(q,path,v);bad['projection']['parent_result']=D(bad['parent_output'])
  no(name,lambda bad=bad:m._construct_checked(b,bad),'LOOP-VALIDATED-PARENT-OUTPUT')
 for key,value in [('context','SYMBOLIC-U-TWO'),('invocation','other-invocation')]:
  bad=change(q,[key],value);no('wrong '+key+' does not inherit parent',lambda bad=bad:m._construct_checked(b,bad),layer='constructed context/anchor/invocation gate')
 # Do not merely change a report: a noncompleted selected parent itself is revalidated.
 bad=D(q);pc=bad['parent_case'];pc['outcomes'][-1]['outcome']='unobserved';pc['projection']['outcomes']=D(pc['outcomes'])
 pc['output']=b['prior_basis']['fresh']['coverage'].error_report_projection(b['prior_basis']['catalogue'],pc['projection'],D(pc['projection']))
 po=b['prior_module']._construct_checked(b['prior_basis'],pc)['projection'];bad['parent_output']=po;bad['projection']['parent_result']=D(po)
 no('genuinely unobserved parent append does not establish departure',lambda:m._construct_checked(b,bad),'LOOP-COMPLETED-PREDECESSOR')
 outs=[('deleted selected evidence',['retained_cleanup_error_evidence'],None),('erased original',['original_error_pending_in_outer_handler'],None),('last caught conflated',['last_acknowledged_inner_caught_error'],q['output']['original_error_pending_in_outer_handler']),('physical destruction',['caught_name_lifetime','physical_destruction_established'],True),('hidden observation',['active_error_at_terminal_observed'],q['output']['original_error_pending_in_outer_handler']),('deleted loop target',['loop_target_bindings_retained','obj'],None),('extra body',['additional_body_execution_established'],True),('exhaustion propagates',['ordinary_exhaustion_is_new_propagating_error'],True),('close acknowledgement erased',['close_normal_return_completed_in_model'],False),('close failed invented',['close_itself_failed_established_in_model'],True),('partial effects erased',['cleanup_list_state','prior_partial_effects'],'NONE'),('partial flag erased',['cleanup_list_state','any_unresolved_partial_effects'],False),('complete contents',['cleanup_list_state','complete_contents_established'],True),('contents fabricated',['cleanup_list_state','exact_runtime_contents'],[]),('False bool to int',['known_false_flags_preserved','new_authorization'],0),('terminal bool to int',['terminal_python_exception_in_model'],1),('normal overall return',['normal_overall_return_established'],True),('line174 write evaluation',['line174_evaluation_established'],True),('suppression',['line175_suppression_established'],True),('rethrow',['final_rethrow_established'],True),('owner finalization',['owner_finalization_established'],True),('managed clear',['managed_local_clear_established'],True),('ACTIVE removal',['active_removal_established'],True),('admission',['actual_admission'],True)]
 for name,path,v in outs:
  bad=change(q,['output',*path],v);no('unsupported '+name,lambda bad=bad:m._construct_checked(b,bad),'LOOP-OUTPUT-CORRESPONDENCE',output)
 for name,path,v in [('text subclass',['binding','continuity'],Text('explicit conditional premise')),('list subclass',['output','events'],Seq(q['output']['events'])),('mapping subclass',['output','binding'],Obj(q['output']['binding']))]:
  bad=change(q,path,v);no(name,lambda bad=bad:m._construct_checked(b,bad),'LOOP-CONSTRUCTED-INPUT','exact-type constructed-input gate')
 bad=D(q);v=bad['output'].pop('terminal_python_exception_in_model');bad['output'][Text('terminal_python_exception_in_model')]=v
 no('subclassed literal key',lambda:m._construct_checked(b,bad),'LOOP-CONSTRUCTED-INPUT','exact-type constructed-input gate')
 returned=m._construct_checked(b,q);returned['projection']['binding']['loop']['ordered_values'].reverse();returned['projection']['cleanup_list_state']['prior_partial_effects']='NONE'
 y('nested returned changes do not alter pristine constructed expectations',lambda:oracle(q,m._construct_checked(b,q),expect))
 claims=m._rows(b)
 for name,mut in [('reverse source entries',lambda a:a['source']['ordered_inputs'].reverse()),('source count',lambda a:a['source'].update(entry_count=3)),('delete departure',lambda a:a['source']['order'].pop(0))]:
  badcat=D(cat);mut(badcat)
  no(name+' cannot redefine source',lambda badcat=badcat:c.validate_cleanup_loop(*b['fresh']['sources'],b['prior_basis']['catalogue'],b['prior_basis']['prior_basis']['catalogue'],badcat),'LOOP-SOURCE-CORRESPONDENCE','producer source rederivation from authenticated parent catalogues')
  coordinated=D(claims)
  for row in coordinated:row['declaration']=D(badcat)
  no(name+' coordinated semantic claims',lambda badcat=badcat,coordinated=coordinated:m._check_candidate(b,b['fresh'],badcat,coordinated),'LOOP-CATALOGUE-SOURCE',semantic)
 mixed=dict(b['fresh']);mixed['sources']=(mixed['sources'][0]+b'\n',*mixed['sources'][1:])
 no('changed current source bytes',lambda:m._check_candidate(b,mixed,cat,claims),'LOOP-CANDIDATE-SOURCE',semantic)
 mixed=dict(b['fresh']);mixed['prior_saved']=mixed['prior_saved']+b'\n'
 no('stale predecessor receipt exact bytes',lambda:m._check_candidate(b,mixed,cat,claims),'LOOP-CANDIDATE-RECEIPT',semantic)
 mixed=dict(b['fresh']);mixed['prior']=D(mixed['prior']);mixed['prior']['contexts'].reverse()
 no('mixed predecessor contexts',lambda:m._check_candidate(b,mixed,cat,claims),'LOOP-CANDIDATE-PREDECESSOR',semantic)
 for idx in range(2):
  bad=D(claims);bad[idx]['handler_exit_established']=True;no(str(idx)+' runtime claim from static source unsupported',lambda bad=bad:m._check_rows(b,bad),'LOOP-SEMANTIC-CORRESPONDENCE',semantic)
 for name,mut in [('omitted context',lambda a:a.pop()),('reversed contexts',lambda a:a.reverse()),('UNKNOWN to zero',lambda a:a[0].update(multiplicity=0,classification='COMPLETE'))]:
  bad=D(claims);mut(bad);no(name,lambda bad=bad:m._check_rows(b,bad),'LOOP-SEMANTIC-CORRESPONDENCE',semantic)
 evidence=D(b['evidence']);first=next(iter(evidence));evidence[first]+=b'changed'
 no('altered retained evidence',lambda:m._compare_evidence(b,evidence),'LOOP-VALIDATED-EVIDENCE','authenticated evidence-byte comparison')
 for idx in range(2):
  receipt=json.loads(saved);del receipt['contexts'][idx][m.RELATION]
  no('public missing loop relation context'+str(idx),lambda receipt=receipt:m.validate('/no-input-consumption',m.enc(receipt)),'LOOP-MANDATORY-RELATIONS','public required-relation gate before inputs/derivation; not full public negative')
 no('legacy partial receipt cannot substitute',lambda:m._receipt_checked(b,b['fresh']['prior_saved']),'LOOP-MANDATORY-RELATIONS','receipt shape gate')
 receipt=json.loads(saved);receipt['contexts'][0][m.RELATION]['handler_exit_established']=True
 no('receipt status escalation',lambda:m._receipt_checked(b,m.enc(receipt)),'LOOP-STALE-OR-ALTERED-RECEIPT','actual-authenticated-basis exact receipt comparison')
 receipt=json.loads(saved);receipt['new_cleanup_loop_limits'].update(inventory_unknown_totals=0,lifetime_unknown_totals=0,actual_admission=True)
 no('receipt cannot erase unknown totals or enable admission',lambda:m._receipt_checked(b,m.enc(receipt)),'LOOP-STALE-OR-ALTERED-RECEIPT','actual-authenticated-basis exact receipt comparison')
 claims[0]['declaration']['source']['order'].reverse();claims[1]['reference_basis'].clear();public['contexts'].reverse();public['actual_admission']=True
 y('returned semantic rows remain detached from validation expectations',lambda:m._check_candidate(b,b['fresh'],cat,m._rows(b)) is not None,semantic)
 y('pristine exact receipt survives nested result changes',lambda:m._receipt_checked(b,saved)['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'actual-authenticated-basis exact receipt comparison')
 states={};cur=b
 for slot in (5,4,3,2):
  p=cur['prior_module'];sm=sys.monitoring
  st={'owner':sm.get_tool(slot),'global_events':sm.get_events(slot),'local_events':sm.get_local_events(slot,p._basis.__code__)};cb=sm.register_callback(slot,sm.events.PY_RETURN,None)
  if cb is not None:sm.register_callback(slot,sm.events.PY_RETURN,cb)
  st['callback_present']=cb is not None;states[str(slot)]=st
  y('actual normal public cleanup slot'+str(slot),lambda st=st:st=={'owner':None,'global_events':0,'local_events':0,'callback_present':False},'post-public normal monitoring inspection; no interrupted-reuse claim')
  cur=cur['prior_basis']
 r.save('normal-monitoring-state.json',states)
 r.save('scope-result.json',{'actual_public_positive':1,'actual_unchanged_predecessor_public_positive':1,'full_public_negative_derivations':0,'source_language_reference_checked':True,'both_contexts_prefixes_failure_origins':True,'runtime_loop_observations':0,'Engineering_factory_oracle_used':False,'predecessor_reviews_replayed':False,'stop_before_line174_evaluation':True,'admission':False})
