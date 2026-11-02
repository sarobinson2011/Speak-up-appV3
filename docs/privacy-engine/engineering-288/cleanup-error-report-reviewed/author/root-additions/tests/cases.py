import copy,ast
D=copy.deepcopy
def outcomes(cat,terminal=None,continuity='explicit conditional premise'):
 rows=[]
 if continuity=='UNESTABLISHED':return [{'stage':cat['source']['order'][0],'outcome':'unobserved'}]
 for stage in cat['source']['order']:
  kind=terminal[1] if terminal and terminal[0]==stage else 'normal';rows.append({'stage':stage,'outcome':kind})
  if kind!='normal':break
 return rows
def from_parent(m,basis,pc,terminal=None,continuity='explicit conditional premise'):
 p=basis['prior_module'];pb=basis['prior_basis'];po=p._construct_checked(pb,pc)['projection'];c=basis['fresh']['coverage'];cat=basis['catalogue']
 b=c.error_report_binding(cat,po,pc['anchor'],continuity);o=outcomes(cat,terminal,continuity)
 case={'kind':'CONSTRUCTED-CLEANUP-ERROR-REPORT','context':pc['context'],'anchor':D(pc['anchor']),'invocation':pc['invocation'],'parent_case':D(pc),'parent_output':po,'binding':b,'outcomes':o,'projection':{},'output':{}}
 v=m._premises(basis,case);case['projection']=D(v);case['output']=c.error_report_projection(cat,v,v);return case
def parent_case(m,basis,idx,control,origin='append',invocation='report-example'):
 p=basis['prior_module'];pb=basis['prior_basis'];factory=m.module(pb['fresh']['root']/'tests/cases.py','_cleanup_factory')
 if origin=='append':return factory.normal(p,pb,idx,control=control,invocation=invocation,terminal=('append-call-attempt','raise'))
 if origin=='close-method':return factory.normal(p,pb,idx,control=control,invocation=invocation,terminal=('close-method-evaluation','raise'))
 if origin=='outside':return factory.normal(p,pb,idx,control=control,invocation=invocation,terminal=('loop-input-evaluation','raise'))
 if origin=='normal':return factory.normal(p,pb,idx,control=control,invocation=invocation)
 if origin in ('process-termination','unobserved'):return factory.normal(p,pb,idx,control=control,invocation=invocation,terminal=('append-call-attempt',origin))
 normal=factory.normal(p,pb,idx,control=control,invocation=invocation)
 address=next(e['address'] for e in normal['projection']['close_result']['events'] if e['event']=='premise' and e['kind']=='call:self._retired.close')
 return factory.normal(p,pb,idx,control=control,invocation=invocation,terminal=('close-normal-return','raise'),close_outcomes={address:'raise'})
def source_oracle(raw):
 # Defining-source traversal independent of the generated catalogue.
 tree=ast.parse(raw);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session')
 h=next(n for n in ast.walk(fn) if isinstance(n,ast.ExceptHandler) and n.name=='close_error')
 assert ast.unparse(h.type)=='BaseException' and h.lineno==172 and len(h.body)==1
 call=h.body[0].value;assert ast.unparse(call)=="details['cleanup'].append([name, type(close_error).__name__, str(close_error)])"
 sub=call.func.value;name,typ,msg=call.args[0].elts
 nodes=[h.type,h.type,h,h,h,h,sub.value,sub.slice,sub,call.func,name,typ.value.func,typ.value.args[0],typ.value,typ.value,typ,msg.func,msg.args[0],msg,msg,call.args[0],call,h.body[0]]
 order=['handler-type-evaluation','handler-match','handler-selection','handler-entry','caught-error-binding-attempt','caught-error-binding-complete','report-details-evaluation','report-key-evaluation','report-list-resolution','report-method-evaluation','report-item-name','error-type-callable','error-type-argument','error-type-call-attempt','error-type-call-return','error-name-attribute','error-str-callable','error-str-argument','error-str-call-attempt','error-str-call-return','report-item-complete','report-append-attempt','report-append-complete']
 return order,{label:{'site':f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}','expression':ast.get_source_segment(raw.decode(),n)} for label,n in zip(order,nodes)}
def oracle(out,control,origin,terminal=None):
 p=out['validated_parent'];selected=p['replacement_error_in_model'];original=p['earlier_constructor_exception'];done={x['stage'] for x in out['events'] if x['outcome']=='normal'}
 assert out['selected_cleanup_error']==selected and out['earlier_constructor_exception']==original and selected!=original
 assert out['selected_failure_occurrence']==p['events'][-1]
 assert out['earlier_control_completed_in_model'] is (True if control else None)
 assert out['handler_selected_in_model']==('handler-selection' in done)
 assert out['handler_entry_completed_in_model']==('handler-entry' in done)
 assert out['caught_binding_completed_in_model']==('caught-error-binding-complete' in done)
 assert out['caught_error_in_model']==(selected if 'caught-error-binding-complete' in done else None)
 assert out['close_normal_return_completed_in_model'] is (origin=='append')
 assert out['close_itself_failed_established_in_model'] is (origin=='close')
 assert out['terminal_python_exception_in_model'] is (None if terminal and terminal[1] in ('process-termination','unobserved') else True)
 assert out['last_pending_error_in_model']==(out['replacement_error_in_model'] or selected)
 if terminal and terminal[1]=='raise':assert out['replacement_error_in_model'] not in (None,selected,original)
 else:assert out['replacement_error_in_model'] is None
 state=out['cleanup_list_state'];assert state['prior_partial_effects']==('UNKNOWN' if origin=='append' else 'No earlier append call reached in validated prefix')
 if origin=='append':assert state['any_unresolved_partial_effects'] is True
 assert out['known_false_flags_preserved']=={'nonexecution_established':False,'new_authorization':False}
 assert out['dynamic_details_origins_preserved']==p['details_after_acknowledged_steps']['dynamic_fields']
 if out['report_append_completed_in_model']:
  item=state['acknowledged_append']['item'];assert item[0]=='managed'
  assert [x['expression'] for x in item[1:]]==['type(close_error).__name__','str(close_error)']
  assert all(x['argument']==selected and x['exact_value'] is None and x['formatted_bytes'] is None for x in item[1:])
 assert all(out[k] is False for k in ('normal_overall_return_established','handler_exit_established','later_iteration_established','loop_completion_established','failure_file_established','final_rethrow_established','owner_finalization_established','complete_cleanup_established','runtime_observation','physical_closure_established','durability_established','released_ownership_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission'))
 assert out['observer_join'] is None and state['complete_contents_established'] is False
 return True
