"""Fresh focused line172 checks, all authenticated cores use the live public basis."""
from common import *
from source_expectations import derive,ORDER
from report_cases import make,parent,binding,oracle
import cleanup_cases
class S(str):pass
class L(list):pass
class M(dict):pass
def run(m,b,public,saved,r):
 core='actual-authenticated-basis _construct_checked; selected parent revalidated'
 output='actual-authenticated-basis output comparison after selected parent revalidation'
 semantic='actual-authenticated-basis semantic catalogue/claims comparison'
 c=b['fresh']['coverage'];cat=b['catalogue'];raw=b['fresh']['sources'][0];expected=derive(raw);r.save('independent-source-expectations.json',expected)
 def preserve_failure(n,fn,layer,actual=None):
  values=list(fn.__defaults__ or ())
  for cell in fn.__closure__ or ():
   try:values.append(cell.cell_contents)
   except ValueError:pass
  candidates=[v for v in values if type(v) is dict and v.get('kind')=='CONSTRUCTED-CLEANUP-ERROR-REPORT']
  if candidates:r.save('failing-independent-case.json',candidates[0])
  r.save('failing-check.json',{'check':n,'layer':layer,'actual_return_available':actual is not None})
  if actual is not None:r.save('unexpected-accepted-result.json',actual)
 def y(n,fn,layer=core):
  try:return r.yes(n,fn,layer)
  except BaseException:preserve_failure(n,fn,layer);raise
 def no(n,fn,code=None,layer=core):
  captured=[]
  def probe():
   v=fn();captured.append(v);return v
  try:return r.no(n,probe,code,layer)
  except BaseException:preserve_failure(n,fn,layer,captured[0] if captured else None);raise
 def source_check():
  assert cat['source']['order']==ORDER and [d['id'] for d in cat['declarations']]==ORDER
  for name,p in expected['stages'].items():
   assert all(cat['source']['stages'][name][k]==v for k,v in p.items()),name
   guards=cat['source']['stages'][name]['guards'];assert any(g.get('kind')=='if' and g.get('test',{}).get('expression')=='obj is not None' for g in guards)
  eligible=cat['source']['eligible_parent_stages'];assert set(eligible)=={s for s in cleanup_cases.ORDER if s.startswith(('close-','append-'))}
  assert all(x['site'].startswith('171:') and x['semantic_region'] in ('protected-close','protected-append') for x in eligible.values())
  assert all(d['classification']=='UNKNOWN' and d['multiplicity'] is d['ordinal'] is None for d in cat['declarations'])
  return True
 y('independent source order positions guards and protected failure domain',source_check,'defining-source AST versus authenticated catalogue; not runtime execution')
 normals={}
 for idx in range(2):
  for control in (False,True):
   for origin in ('close','append'):
    label=f'context{idx}/control{int(control)}/{origin}';q=make(m,b,idx,control,origin);normals[idx,control,origin]=q
    o=y(label+' legitimate error reporting',lambda q=q:(lambda o:(oracle(q,o,expected),o)[1])(m._construct_checked(b,q)))
    if idx==0 and not control:r.save(origin+'-independent-case.json',q);r.save(origin+'-independent-result.json',o)
    if origin=='append':y(label+' reporting preserves prior UNKNOWN append effects',lambda o=o:o['projection']['cleanup_list_state']['prior_partial_effects']=='UNKNOWN' and o['projection']['cleanup_list_state']['any_unresolved_partial_effects'] is True and o['projection']['close_normal_return_completed_in_model'] is True,'independent outcome oracle over authenticated result')
    bad=change(q,['output','terminal_python_exception_in_model'],False);no(label+' cannot turn reporting into normal overall return',lambda bad=bad:m._construct_checked(b,bad),'REPORT-OUTPUT-CORRESPONDENCE',output)
    bad=change(q,['output','last_pending_error_in_model'],None);no(label+' selected error cannot disappear',lambda bad=bad:m._construct_checked(b,bad),'REPORT-OUTPUT-CORRESPONDENCE',output)
 for idx,origin in enumerate(('lookup','append-lookup')):
  q=make(m,b,idx,bool(idx),origin);y(origin+' legitimate protected evaluation failure',lambda q=q:oracle(q,m._construct_checked(b,q),expected))
 frontiers=[('handler-type-evaluation','raise'),('handler-match','raise'),('handler-selection','unobserved'),('handler-entry','raise'),('caught-error-binding-attempt','raise'),('caught-error-binding-complete','process-termination'),('report-method-evaluation','raise'),('error-type-call-return','raise'),('error-name-attribute','unobserved'),('error-str-call-return','raise'),('report-item-complete','process-termination'),('report-append-attempt','raise'),('report-append-complete','unobserved')]
 summary=[]
 for j,t in enumerate(frontiers):
  q=make(m,b,j%2,bool((j//2)%2),'append' if j%3 else 'close',terminal=t,invocation='fl6-line172-frontier-'+str(j))
  o=y('/'.join(t)+' respects acknowledgements and distinct errors',lambda q=q:(lambda o:(oracle(q,o,expected),o)[1])(m._construct_checked(b,q)))['projection']
  summary.append({'stage':t[0],'outcome':t[1],'context':q['context'],'prefix':q['parent_output']['earlier_control_completed_in_model'],'caught':o['caught_name_in_model'],'last_acknowledged_active_role':o['last_acknowledged_active_caught_error_in_model']['role'],'pending_role':o['last_pending_error_in_model']['role'],'terminal':o['terminal_python_exception_in_model'],'prior_unknown':o['cleanup_list_state']['prior_partial_effects'],'current_unknown':o['cleanup_list_state']['current_partial_effects']})
  bad=change(q,['output','report_append_completed_in_model'],True);no('/'.join(t)+' cannot invent append completion',lambda bad=bad:m._construct_checked(b,bad),'REPORT-OUTPUT-CORRESPONDENCE',output)
  bad=change(q,['output','last_pending_error_in_model'],q['parent_output']['earlier_constructor_exception']);no('/'.join(t)+' cannot replace pending role by constructor role',lambda bad=bad:m._construct_checked(b,bad),'REPORT-OUTPUT-CORRESPONDENCE',output)
  bad=change(q,['output','terminal_python_exception_in_model'],None if t[1]=='raise' else True);no('/'.join(t)+' rejects wrong terminal exception classification',lambda bad=bad:m._construct_checked(b,bad),'REPORT-OUTPUT-CORRESPONDENCE',output)
 r.save('frontier-summary.json',summary)
 for idx in range(2):
  q=make(m,b,idx,bool(idx),'append',continuity='UNESTABLISHED');y('context'+str(idx)+' unknown continuity makes no handler progress',lambda q=q:oracle(q,m._construct_checked(b,q),expected))
 # Outside-try parent is genuinely revalidated; no hash-only witness rejection.
 for idx,stage in enumerate(('managed-guard-result','selected-try-entry')):
  q=D(normals[idx,False,'append']);pc,po=parent(b['prior_module'],b['prior_basis'],idx,False,stage,q['invocation']);q['parent_case']=pc;q['parent_output']=po;q['projection']['parent_result']=D(po)
  no(stage+' failure cannot acquire line172 handler',lambda q=q:m._construct_checked(b,q),'REPORT-PROTECTED-FAILURE','actual-authenticated parent + source-protected-failure gate')
 q=normals[0,False,'append']
 for name,path,v in [('name',['selected_name'],'raw'),('owner',['references','owner'],'other-owner'),('token',['references','token'],'other-token'),('selected error',['selected_failure','reference'],'other-error'),('occurrence',['failure_occurrence','id'],'other-occurrence'),('list role',['cleanup_list','symbol'],'other-list'),('instance',['instance_anchor'],normals[1,False,'append']['anchor'])]:
  bad=D(q);p=bad['binding']
  for k in path[:-1]:p=p[k]
  p[path[-1]]=v;bad['projection']['binding']=D(bad['binding'])
  if bad==q:continue
  no('coordinated wrong '+name+' binding',lambda bad=bad:m._construct_checked(b,bad),'REPORT-EXPECTED-BINDING')
 bad=change(q,['parent_output','last_pending_error_in_model','reference'],'unvalidated-error');bad['projection']['parent_result']=D(bad['parent_output'])
 no('coordinated substituted parent report is revalidated',lambda:m._construct_checked(b,bad),'REPORT-VALIDATED-PARENT-OUTPUT')
 for name,key,value in [('context','context','SYMBOLIC-U-TWO'),('invocation','invocation','different-invocation')]:
  bad=D(q);bad[key]=value;no('wrong '+name+' cannot inherit selected parent',lambda bad=bad:m._construct_checked(b,bad),layer='context/anchor/parent invocation gate before selected-parent validation')
 bad=D(q);bad['binding']['instance_anchor']['instance']='wrong-instance';bad['projection']['binding']=D(bad['binding'])
 no('wrong underlying instance binding',lambda:m._construct_checked(b,bad),'REPORT-EXPECTED-BINDING')
 for name,mutate in [('omitted first stage',lambda a:a.pop(0)),('callable after argument',lambda a:a.__setitem__(slice(11,13),list(reversed(a[11:13])))),('omitted final completion',lambda a:a.pop()),('duplicate stage',lambda a:a.insert(8,D(a[8])))]:
  bad=D(q);mutate(bad['outcomes']);bad['projection']['outcomes']=D(bad['outcomes']);no(name,lambda bad=bad:m._construct_checked(b,bad),layer='source step/order gate after actual parent validation')
 qstop=make(m,b,1,True,'append',terminal=('error-str-call-return','raise'),invocation='fl6-line172-stopping');bad=D(qstop);bad['outcomes'].append({'stage':'report-item-complete','outcome':'normal'});bad['projection']['outcomes']=D(bad['outcomes'])
 no('continuation after first nonnormal frontier',lambda:m._construct_checked(b,bad),'REPORT-UNREACHED-STEPS')
 alterations=[('prior partial effects',['cleanup_list_state','prior_partial_effects'],'none'),('partial flag',['cleanup_list_state','any_unresolved_partial_effects'],False),('complete list',['cleanup_list_state','complete_contents_established'],True),('list contents',['cleanup_list_state','exact_runtime_contents'],[]),('close erased',['close_normal_return_completed_in_model'],False),('close failure invented',['close_itself_failed_established_in_model'],True),('generated name',['error_item_in_model',1,'exact_value'],'RuntimeError'),('generated message bytes',['error_item_in_model',2,'formatted_bytes'],'message'),('False int alias',['known_false_flags_preserved','new_authorization'],0),('terminal int alias',['terminal_python_exception_in_model'],1),('handler exit',['handler_exit_established'],True),('later iteration',['later_iteration_established'],True),('failure-file writing',['failure_file_established'],True),('final rethrow',['final_rethrow_established'],True),('owner finalization',['owner_finalization_established'],True),('admission',['actual_admission'],True)]
 for name,path,v in alterations:
  bad=change(q,['output',*path],v);no('unsupported output '+name,lambda bad=bad:m._construct_checked(b,bad),'REPORT-OUTPUT-CORRESPONDENCE',output)
 for name,path,v in [('str subclass',['output','caught_name_in_model'],S('close_error')),('list subclass',['output','error_item_in_model'],L(q['output']['error_item_in_model'])),('dict subclass',['binding'],M(q['binding']))]:
  bad=change(q,path,v);no(name,lambda bad=bad:m._construct_checked(b,bad),'REPORT-CONSTRUCTED-INPUT','exact-type input gate before selected-parent construction')
 bad=D(q);v=bad['output'].pop('terminal_python_exception_in_model');bad['output'][S('terminal_python_exception_in_model')]=v
 no('literal key subclass',lambda:m._construct_checked(b,bad),'REPORT-CONSTRUCTED-INPUT','exact-type input gate before selected-parent construction')
 mutated=m._construct_checked(b,q);mutated['projection']['binding']['references']['owner']='altered-return';mutated['projection']['cleanup_list_state']['prior_partial_effects']='none'
 y('nested returned mutations leave pristine constructed expectations',lambda:oracle(q,m._construct_checked(b,q),expected))
 claims=m._rows(b);badcat=D(cat);s='handler-match';badcat['source']['order'].remove(s);del badcat['source']['stages'][s];badcat['declarations']=[d for d in badcat['declarations'] if d['id']!=s]
 no('coordinated catalogue omission rejects from defining source',lambda:c.validate_error_report(*b['fresh']['sources'],b['prior_basis']['catalogue'],badcat),'REPORT-SOURCE-CORRESPONDENCE','producer source rederivation, current authenticated parent catalogue')
 no('coordinated catalogue omission rejects authenticated semantic core',lambda:m._check_candidate(b,b['fresh'],badcat,claims),'REPORT-CATALOGUE-SOURCE',semantic)
 mixed=dict(b['fresh']);mixed['sources']=(mixed['sources'][0]+b'\n',*mixed['sources'][1:])
 no('mixed defining-source bytes reject',lambda:m._check_candidate(b,mixed,cat,claims),'REPORT-CANDIDATE-SOURCE','actual-authenticated-basis source-byte comparison')
 mixed=dict(b['fresh']);mixed['prior_saved']=mixed['prior_saved']+b'\n'
 no('stale predecessor receipt bytes reject',lambda:m._check_candidate(b,mixed,cat,claims),'REPORT-CANDIDATE-RECEIPT','actual-authenticated-basis predecessor receipt-byte comparison')
 mixed=dict(b['fresh']);mixed['prior']=D(mixed['prior']);mixed['prior']['contexts'].reverse()
 no('mixed predecessor context report rejects',lambda:m._check_candidate(b,mixed,cat,claims),'REPORT-CANDIDATE-PREDECESSOR','actual-authenticated-basis predecessor report comparison')
 for idx in range(2):
  bad=D(claims);bad[idx]['handler_exit_established']=True;no('context'+str(idx)+' claim escalation',lambda bad=bad:m._check_rows(b,bad),'REPORT-SEMANTIC-CORRESPONDENCE',semantic)
 bad=D(claims);bad.pop();no('omitted required context',lambda:m._check_rows(b,bad),'REPORT-SEMANTIC-CORRESPONDENCE',semantic)
 bad=D(claims);bad.reverse();no('reordered context claims',lambda:m._check_rows(b,bad),'REPORT-SEMANTIC-CORRESPONDENCE',semantic)
 bad=D(claims);bad[1]['multiplicity']=0;bad[1]['classification']='COMPLETE';no('coordinated UNKNOWN-to-zero qualification claim',lambda:m._check_rows(b,bad),'REPORT-SEMANTIC-CORRESPONDENCE',semantic)
 bad=D(b['evidence']);first=next(iter(bad));bad[first]=bad[first]+b'altered';no('altered authenticated evidence',lambda:m._compare_evidence(b,bad),'REPORT-VALIDATED-EVIDENCE','authenticated evidence byte comparison')
 oldsaved=b['fresh']['prior_saved'];no('partial legacy receipt substitute',lambda:m._receipt_checked(b,oldsaved),'REPORT-MANDATORY-RELATIONS','receipt shape/mandatory relation gate; no public derivation')
 receipt=json.loads(saved);receipt['contexts'][0][m.RELATION]['handler_exit_established']=True
 no('coordinated receipt escalation',lambda:m._receipt_checked(b,m.enc(receipt)),'REPORT-STALE-OR-ALTERED-RECEIPT','actual-authenticated-basis receipt comparison')
 receipt=json.loads(saved);receipt['new_error_report_limits'].update(inventory_unknown_totals=0,lifetime_unknown_totals=0,actual_admission=True)
 no('receipt cannot erase unknown totals and enable admission',lambda:m._receipt_checked(b,m.enc(receipt)),'REPORT-STALE-OR-ALTERED-RECEIPT','actual-authenticated-basis receipt comparison')
 claims[0]['declaration']['source']['order'].reverse();public['contexts'].reverse();public['actual_admission']=True
 y('returned nested contexts cannot mutate expected mandatory rows',lambda:m._check_candidate(b,b['fresh'],cat,m._rows(b)) is not None,semantic)
 y('pristine receipt still accepted after result mutations',lambda:m._receipt_checked(b,saved)['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'actual-authenticated-basis receipt comparison')
 sm=sys.monitoring;states={}
 for slot,p in ((4,b['prior_module']),(3,b['prior_basis']['prior_module']),(2,b['prior_basis']['prior_basis']['prior_module'])):
  st={'owner':sm.get_tool(slot),'global_events':sm.get_events(slot),'local_events':sm.get_local_events(slot,p._basis.__code__)};cb=sm.register_callback(slot,sm.events.PY_RETURN,None)
  if cb is not None:sm.register_callback(slot,sm.events.PY_RETURN,cb)
  st['callback_present']=cb is not None;states[str(slot)]=st;y('normal actual-public monitoring cleanup slot'+str(slot),lambda st=st:st=={'owner':None,'global_events':0,'local_events':0,'callback_present':False},'actual post-public normal monitoring inspection; not interruption campaign')
 r.save('normal-monitoring-state.json',states)
 r.save('scope-result.json',{'focused_checks_completed':True,'actual_public_positive':1,'actual_unchanged_predecessor_public_positive':1,'full_public_negative_derivations':0,'actual_runtime_line172_observations':0,'author_oracle_used':False,'old_reviews_replayed':False,'both_contexts_and_prefixes':True,'stop_before_handler_exit':True,'admission':False})
