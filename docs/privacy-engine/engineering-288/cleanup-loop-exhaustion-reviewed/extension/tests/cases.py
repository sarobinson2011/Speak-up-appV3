import ast,copy
D=copy.deepcopy
def outcomes(cat,terminal=None,continuity='explicit conditional premise'):
 if continuity=='UNESTABLISHED':return [{'stage':cat['source']['order'][0],'outcome':'unobserved'}]
 rows=[]
 for n in cat['source']['order']:
  kind=terminal[1] if terminal and terminal[0]==n else cat['source']['normal_outcomes'][n];rows.append({'stage':n,'outcome':kind})
  if kind!=cat['source']['normal_outcomes'][n]:break
 return rows
def from_parent(m,basis,pc,terminal=None,continuity='explicit conditional premise'):
 po=basis['prior_module']._construct_checked(basis['prior_basis'],pc)['projection'];c=basis['fresh']['coverage'];cat=basis['catalogue'];b=c.cleanup_loop_binding(cat,po,pc['anchor'],continuity);o=outcomes(cat,terminal,continuity)
 case={'kind':'CONSTRUCTED-CLEANUP-LOOP','context':pc['context'],'anchor':D(pc['anchor']),'invocation':pc['invocation'],'parent_case':D(pc),'parent_output':po,'binding':b,'outcomes':o,'projection':{},'output':{}}
 v=m._premises(basis,case);case['projection']=D(v);case['output']=c.cleanup_loop_projection(cat,v,v);return case
def normal(m,basis,idx,control,origin,invocation):
 p=basis['prior_module'];pb=basis['prior_basis'];f=m.module(pb['fresh']['root']/'tests/cases.py','_reviewed_report_factory')
 pc=f.parent_case(p,pb,idx,control,origin,invocation);report=f.from_parent(p,pb,pc);return from_parent(m,basis,report)
def source_oracle(raw):
 tree=ast.parse(raw);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session')
 hs=[n for n in ast.walk(fn) if isinstance(n,ast.ExceptHandler) and n.name=='e'];assert len(hs)==1;outer=hs[0]
 loops=[n for n in outer.body if isinstance(n,ast.For)];assert len(loops)==1;loop=loops[0];guard=loop.body[0];tr=guard.body[0];h=tr.handlers[0]
 assert loop.lineno==169 and loop.end_lineno==172 and not loop.orelse and len(loop.body)==1
 assert ast.literal_eval(ast.List(elts=[p.elts[0] for p in loop.iter.elts],ctx=ast.Load()))==['raw','managed']
 assert [p.elts[1].id for p in loop.iter.elts]==['raw','managed'] and [t.id for t in loop.target.elts]==['name','obj']
 assert ast.unparse(guard.test)=='obj is not None' and not guard.orelse and len(guard.body)==1
 assert h.name=='close_error' and ast.unparse(h.type)=='BaseException' and len(h.body)==1 and not tr.orelse and not tr.finalbody
 assert ast.unparse(h.body[0])=="details['cleanup'].append([name, type(close_error).__name__, str(close_error)])"
 assert outer.body[2].lineno==174 and isinstance(outer.body[2],ast.Try)
 labels=['inner-handler-departure-attempt','inner-handler-exit-complete','selected-loop-body-complete','final-iterator-advance-attempt','ordinary-iterator-exhaustion','cleanup-loop-complete']
 nodes=[h,h,guard,loop,loop.iter,loop]
 return labels,{n:{'site':f'{v.lineno}:{v.col_offset}:{v.end_lineno}:{v.end_col_offset}:{type(v).__name__}','expression':ast.get_source_segment(raw.decode(),v)} for n,v in zip(labels,nodes)}
def oracle(o,control,origin,terminal=None):
 p=o['validated_parent'];original=p['earlier_constructor_exception'];selected=p['selected_cleanup_error'];done={e['stage'] for e in o['events'] if e['outcome'] in ('normal','exhausted')};exited='inner-handler-exit-complete' in done
 assert o['handler_exit_established'] is exited and o['loop_completion_established'] is ('cleanup-loop-complete' in done)
 assert o['ordinary_exhaustion_established'] is ('ordinary-iterator-exhaustion' in done)
 assert o['original_error_pending_in_outer_handler']==original and o['retained_cleanup_error_evidence']==selected and o['last_acknowledged_inner_caught_error']==selected
 assert o['last_acknowledged_active_caught_error_in_model']==(original if exited else selected)
 assert o['caught_name_lifetime']['last_acknowledged_binding']==('CLEARED' if exited else 'BOUND selected cleanup error')
 assert o['last_pending_error_in_model']==(o['replacement_error_in_model'] or (original if exited else selected))
 assert o['terminal_python_exception_in_model'] is (None if terminal and terminal[1] in ('process-termination','unobserved') else True)
 if terminal and terminal[1] in ('raise','catchable-interruption'):assert o['replacement_error_in_model'] not in (None,original,selected)
 else:assert o['replacement_error_in_model'] is None
 assert o['cleanup_list_state']==p['cleanup_list_state'] and o['cleanup_list_state']['complete_contents_established'] is False
 assert o['close_normal_return_completed_in_model'] is (origin=='append') and o['close_itself_failed_established_in_model'] is (origin=='close')
 assert o['earlier_control_completed_in_model'] is (True if control else None)
 assert o['known_false_flags_preserved']=={'nonexecution_established':False,'new_authorization':False} and o['dynamic_details_origins_preserved']==p['dynamic_details_origins_preserved']
 if origin=='append':assert o['cleanup_list_state']['prior_partial_effects']=='UNKNOWN' and o['cleanup_list_state']['any_unresolved_partial_effects'] is True
 assert all(o[k] is False for k in ('ordinary_exhaustion_is_new_propagating_error','normal_overall_return_established','additional_body_execution_established','line174_evaluation_established','failure_file_established','line175_suppression_established','final_rethrow_established','owner_finalization_established','managed_local_clear_established','active_removal_established','complete_cleanup_established','runtime_observation','physical_closure_established','durability_established','released_ownership_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission'))
 assert o['observer_join'] is None and o['active_error_at_terminal_observed'] is None and o['caught_name_lifetime']['physical_destruction_established'] is False
 return True
