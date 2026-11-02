"""Fresh reviewer controls. Called once with the actual public-returned basis.
No predecessor replacement, cached authentication, receipt repair or campaign replay.
"""
from common import *
from cases import build,oracle,ORDER,refresh_projection
class S(str):pass
class L(list):pass
class M(dict):pass
def replace_exact(v,old,new):
 if type(v) is type(old) and v==old:return D(new)
 if type(v) is dict:return {k:replace_exact(x,old,new) for k,x in v.items()}
 if type(v) is list:return [replace_exact(x,old,new) for x in v]
 return v
def run(m,b,public,saved,r):
 r.save('validation-layers.json',{'full_current_public_positive':1,'actual_unchanged_predecessor_public_positive':1,'full_public_negative_derivations':0,'public_negatives':'receipt required-relation gates before inputs/derivation','other_negatives':'actual-authenticated-basis constructed, semantic, candidate and receipt-comparison cores','constructed_observations_are_runtime':False})
 actual_monitoring={};sm=sys.monitoring
 for slot,p in ((3,b['prior_module']),(2,b['prior_basis']['prior_module'])):
  state={'owner':sm.get_tool(slot),'global':sm.get_events(slot),'local':sm.get_local_events(slot,p._basis.__code__)};old=sm.register_callback(slot,sm.events.PY_RETURN,None)
  if old is not None:sm.register_callback(slot,sm.events.PY_RETURN,old)
  state['callback_present']=old is not None;actual_monitoring[str(slot)]=state
  r.yes('actual authenticated public normal completion cleaned slot '+str(slot),lambda state=state:state=={'owner':None,'global':0,'local':0,'callback_present':False})
 r.save('actual-normal-monitoring-state.json',actual_monitoring)
 r.yes('independently source-ordered 35 stages',lambda:b['catalogue']['source']['order']==ORDER)
 normals={}
 for idx in range(2):
  for control in (False,True):
   label=f'context{idx}/control{int(control)}';q=build(m,b,idx,control);normals[idx,control]=q
   result=m._construct_checked(b,q)
   r.yes(label+' normal mapping except EC-01 independently corroborated',lambda q=q,result=result:oracle(q,result,known_terminal_defect=True))
   o=result['projection'];assert o['terminal_python_exception_in_model'] is False and o['last_pending_error_in_model']==o['earlier_constructor_exception']==o['validated_parent']['active_caught_error_in_model']
   r.row(label+' EC-01 accepted inconsistent terminal exception flag','DEFECT-OBSERVED',layer='authenticated-basis constructed core and producer output comparison',flag=False,pending_original_retained=True)
   fixed=change(q,['output','terminal_python_exception_in_model'],True)
   r.no(label+' source-consistent single-field replacement rejected',lambda fixed=fixed:m._construct_checked(b,fixed),'CLEANUP-OUTPUT-CORRESPONDENCE')
   if idx==0 and control is False:
    r.save('EC01-smallest-case.json',q);r.save('EC01-accepted-result.json',result);r.save('EC01-source-consistent-one-field-output.json',fixed['output'])
    r.save('EC01-witness.json',{'scope':'conditional constructed projection, not runtime loss or admission escalation','accepted_flag':False,'required_by_retained_pending_exception_semantics':True,'mutation_from_accepted_case':'/output/terminal_python_exception_in_model only: false -> true','rejection_layer':'CLEANUP-OUTPUT-CORRESPONDENCE in _construct_checked; no full public negative derivation','pending_error_equal_original':True,'parent_active_error_equal_original':True,'parent_terminal_flag':True,'source':'lab_bootstrap.py:167-171 inside except BaseException as e; no rethrow or normal overall completion in this bounded slice'})
 # Focused distinct frontiers across both contexts and control prefixes.
 frontiers=[('input-managed-object','raise'),('raw-guard-result','unobserved'),('managed-bind-obj','process-termination'),('selected-try-entry','raise'),('close-method-evaluation','raise'),('close-call-attempt','unobserved'),('close-normal-return','raise'),('close-normal-return','unobserved'),('append-details-evaluation','raise'),('append-method-evaluation','process-termination'),('append-call-attempt','raise'),('append-complete','unobserved')]
 for idx in range(2):
  for n,term in enumerate(frontiers):
   ck='abrupt' if term==('close-normal-return','raise') else 'partial-prefix' if term==('close-normal-return','unobserved') else 'normal'
   q=build(m,b,idx,bool(n%2),terminal=term,close_kind=ck)
   r.yes(f'context{idx} frontier {term[0]}/{term[1]}',lambda q=q:oracle(q,m._construct_checked(b,q)))
  q=build(m,b,idx,continuity='UNESTABLISHED');r.yes(f'context{idx} unknown continuity establishes no selection',lambda q=q:oracle(q,m._construct_checked(b,q)))
  q=build(m,b,idx,initial={'_live':None,'_retired':None,'_phase':'CLOSED'})
  r.yes(f'context{idx} empty retired reference conditionally normal; EC01 retained',lambda q=q:oracle(q,m._construct_checked(b,q),True))
  # Wrong-input tests retain all unrelated correct bytes and validated parent.
  q=normals[idx,False]
  mutations=[(['binding','selected_index'],0),(['binding','name'],'raw'),(['binding','ordered_values',0,'value'],'invented-raw'),(['binding','object'],None),(['binding','close_receiver'],None),(['binding','guard','result'],False),(['binding','guard','right'],False),(['binding','guard','expression'],'bool(obj)'),(['binding','method'],'state'),(['binding','cleanup_list'],{}),(['binding','append_item',0],'raw'),(['binding','append_item',1],'close returned '),(['binding','runtime_object_identity'],'invented'),(['invocation'],'wrong-invocation'),(['anchor','context'],m.CONTEXTS[1-idx]),(['context'],m.CONTEXTS[1-idx])]
  for path,v in mutations:
   bad=change(q,path,v);r.no(f'context{idx} reject input '+ '/'.join(map(str,path)),lambda bad=bad:m._construct_checked(b,bad))
  for key,v in [('method','state'),('context',m.CONTEXTS[1-idx]),('scope',{**q['close_case']['scope'],'invocation':'wrong-invocation'}),('scope',{**q['close_case']['scope'],'acquisition':'wrong-acquisition'}),('scope',{**q['close_case']['scope'],'instance':'wrong-instance'})]:
   bad=change(q,['close_case',key],v);r.no(f'context{idx} reject close {key}/{str(v)[:35]}',lambda bad=bad:m._construct_checked(b,bad))
  # Source outcome and inherited interpreter disagree, without changing pins.
  bad=change(q,['close_case'],None);r.no(f'context{idx} missing inherited close relation',lambda bad=bad:m._construct_checked(b,bad),'CLEANUP-VALIDATED:close_result')
  for k in (0,24,33):
   bad=D(q);bad['outcomes'].pop(k);bad['projection']['outcomes']=D(bad['outcomes']);r.no(f'context{idx} omitted ordered stage {k}',lambda bad=bad:m._construct_checked(b,bad))
  bad=D(q);bad['outcomes'][24:26]=reversed(bad['outcomes'][24:26]);bad['projection']['outcomes']=D(bad['outcomes']);r.no(f'context{idx} reordered close stages',lambda bad=bad:m._construct_checked(b,bad))
  bad=D(q);bad['outcomes'].insert(25,D(bad['outcomes'][24]));bad['projection']['outcomes']=D(bad['outcomes']);r.no(f'context{idx} duplicated close attempt',lambda bad=bad:m._construct_checked(b,bad))
  for path,v in [(['close_normal_return_completed_in_model'],False),(['append_completed_in_model'],False),(['close_itself_failed_established_in_model'],True),(['inner_handler_entry_established'],True),(['complete_cleanup_established'],True),(['final_rethrow_established'],True),(['actual_admission'],True),(['details_after_acknowledged_steps','known_literal_fields','cleanup'],[]),(['details_after_acknowledged_steps','known_literal_fields','nonexecution_established'],0),(['details_after_acknowledged_steps','dynamic_fields',0,'exact_value'],'InventedError')]:
   bad=change(q,['output',*path],v);r.no(f'context{idx} reject output '+ '/'.join(map(str,path)),lambda bad=bad:m._construct_checked(b,bad),'CLEANUP-OUTPUT-CORRESPONDENCE')
  late=build(m,b,idx,terminal=('append-call-attempt','raise'))
  for f,v in [('close_itself_failed_established_in_model',True),('close_normal_return_completed_in_model',False),('inner_handler_entry_established',True),('last_pending_error_in_model',late['parent_output']['earlier_constructor_exception'])]:
   bad=change(late,['output',f],v);r.no(f'context{idx} append failure cannot rewrite '+f,lambda bad=bad:m._construct_checked(b,bad),'CLEANUP-OUTPUT-CORRESPONDENCE')
  # Agreement among submitted layers cannot authenticate a changed manager role.
  manager=q['binding']['object'];wrong=change(manager,[next(iter(manager))],'wrong-role') if type(manager) is dict else 'wrong-manager'
  bad=replace_exact(q,manager,wrong);assert bad!=q;r.no(f'context{idx} coordinated wrong manager role',lambda bad=bad:m._construct_checked(b,bad))
  bad=D(q);bad['binding']['append_item']=['raw','close returned'];bad['projection']['binding']=D(bad['binding']);bad['output']['binding']=D(bad['binding']);bad['output']['details_after_acknowledged_steps']['known_literal_fields']['cleanup']=[['raw','close returned']]
  r.no(f'context{idx} coordinated append-item substitution',lambda bad=bad:m._construct_checked(b,bad),'CLEANUP-EXPECTED-BINDING')
  bad=D(q);bad['parent_output']['last_pending_error_in_model']=None;bad['projection']['parent_result']=D(bad['parent_output']);bad['output']['validated_parent']=D(bad['parent_output']);bad['output']['last_pending_error_in_model']=None
  r.no(f'context{idx} coordinated disappearance of constructor error',lambda bad=bad:m._construct_checked(b,bad),'CLEANUP-VALIDATED-PARENT-OUTPUT')
  result=m._construct_checked(b,q);result['projection']['binding']['append_item'][0]='raw';result['projection']['validated_parent']['details_in_model']['known_literal_fields']['cleanup'].append('bad')
  r.yes(f'context{idx} nested returned mutation leaves pristine expectations',lambda q=q:oracle(q,m._construct_checked(b,q),True))
 # Exact types are checked before comparison, including keys and containers.
 q=normals[0,False]
 for name,path,v in [('string-subclass',['binding','name'],S('managed')),('bool-as-int',['binding','guard','result'],1),('index-bool',['binding','selected_index'],True),('list-subclass',['outcomes'],L(q['outcomes'])),('dict-subclass',['binding'],M(q['binding'])),('nested-output-subclass',['output','binding','append_item',1],S('close returned'))]:
  bad=change(q,path,v);r.no('exact type '+name,lambda bad=bad:m._construct_checked(b,bad))
 bad=D(q);value=bad['output'].pop('completion');bad['output'][S('completion')]=value;r.no('literal key subclass',lambda:m._construct_checked(b,bad))
 # Semantic and candidate cores are explicitly based on this actual validation.
 rows=m._rows(b);data=b['fresh'];cat=b['catalogue'];r.yes('authenticated semantic rows accepted',lambda:m._check_candidate(b,data,cat,rows,b['evidence'])==rows)
 for idx in range(2):
  for path,v in [(['classification'],'PASS'),(['multiplicity'],0),(['actual_invocation_count'],1),(['runtime_cleanup_append_chain'],[]),(['outer_cleanup_complete'],True),(['conditional_links'],[])]:
   bad=change(rows,[idx,*path],v);r.no(f'semantic context{idx}/'+path[0],lambda bad=bad:m._check_rows(b,bad),'CLEANUP-SEMANTIC-CORRESPONDENCE')
  bad=D(cat);bad['declarations'].pop();claims=D(rows);claims[idx]['declaration']=D(bad)
  r.no(f'context{idx} coordinated omitted declaration',lambda bad=bad,claims=claims:m._check_candidate(b,data,bad,claims),'CLEANUP-CATALOGUE-SOURCE')
  submitted=json.loads(saved);del submitted['contexts'][idx][m.RELATION]
  r.no(f'public context{idx} missing mandatory relation BEFORE derivation',lambda submitted=submitted:m.validate(data['root'],m.enc(submitted)),'CLEANUP-MANDATORY-RELATIONS')
 r.no('candidate missing evidence',lambda:m._check_candidate(b,data,cat,rows,{}),'CLEANUP-VALIDATED-EVIDENCE')
 bad=dict(data);bad['sources']=(data['sources'][0]+b'\n',*data['sources'][1:]);r.no('candidate stale source',lambda:m._check_candidate(b,bad,cat,rows),'CLEANUP-CANDIDATE-SOURCE')
 bad=dict(data);bad['prior']=D(data['prior']);bad['prior']['contexts'].reverse();r.no('candidate mixed predecessor contexts',lambda:m._check_candidate(b,bad,cat,rows),'CLEANUP-CANDIDATE-PREDECESSOR')
 bad=dict(data);bad['prior_saved']=data['prior_saved']+b' ';r.no('candidate altered predecessor receipt',lambda:m._check_candidate(b,bad,cat,rows),'CLEANUP-CANDIDATE-RECEIPT')
 for label,mutator in [('reverse contexts',lambda v:v['contexts'].reverse()),('UNKNOWN to zero',lambda v:v['contexts'][0][m.RELATION].update(multiplicity=0)),('admission escalation',lambda v:v['new_cleanup_append_limits'].update(actual_admission=True)),('changed receipt code pin',lambda v:v['extension_components']['correspondence.py'].update(sha256='0'*64))]:
  v=json.loads(saved);mutator(v);r.no('receipt comparison core '+label,lambda v=v:m._receipt_checked(b,m.enc(v)),'CLEANUP-STALE-OR-ALTERED-RECEIPT')
 out=m._check_candidate(b,data,cat,rows);out[0]['declaration']['source']['order'].reverse();out.reverse();r.yes('semantic returned nested aliases isolated',lambda:m._rows(b)==rows)
 public['contexts'].reverse();public['receipt']['bytes']=0;r.yes('public returned aliases isolated in receipt comparison core',lambda:m._receipt_checked(b,saved)['contexts']==list(m.CONTEXTS))
 r.save('final-focused-summary.json',{'kind':'Independent bounded source and authenticated-basis checks','EC01':'confirmed in both contexts and control prefixes','normal_source_terminal_exception_expected':True,'candidate_false_flag_accepted':True,'runtime_failure_claimed':False,'all_other_tested_rejections_at_documented_layers':True,'prior_reviews_replayed':False})
