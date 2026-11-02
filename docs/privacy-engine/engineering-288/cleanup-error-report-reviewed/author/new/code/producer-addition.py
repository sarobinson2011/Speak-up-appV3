
# Bounded line172 selected failure -> caught error -> error-item append.
def error_report_source(launcher,entry,manager,parent):
 for raw in (launcher,entry,manager):need(type(raw) is bytes,'REPORT-SOURCE-BYTES')
 status_exact_tree(parent,'REPORT-PARENT-CATALOGUE')
 pins={n:{'bytes':len(raw),'sha256':digest(raw)} for n,raw in [('launcher',launcher),('entry',entry),('manager',manager)]}
 status_typed_same(parent['source']['sources'],pins,'REPORT-PARENT-SOURCES')
 tree,loc=_client_locate(launcher)
 fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session')
 outer=fn.body[-1].body[-1].handlers[0];loop=outer.body[1];protected=loop.body[0].body[0]
 need(outer.name=='e' and ast.unparse(outer.type)=='BaseException' and isinstance(protected,ast.Try) and len(protected.body)==2 and len(protected.handlers)==1 and not protected.orelse and not protected.finalbody,'REPORT-SHARED-TRY')
 h=protected.handlers[0];need(h.name=='close_error' and isinstance(h.type,ast.Name) and h.type.id=='BaseException' and len(h.body)==1,'REPORT-HANDLER')
 status_typed_same({**loc(h),'source':pins['launcher']},parent['source']['inner_handler'],'REPORT-HANDLER-ORIGIN')
 need([ast.unparse(n) for n in protected.body]==['obj.close()',"details['cleanup'].append([name, 'close returned'])"],'REPORT-PROTECTED-OPERATIONS')
 stmt=h.body[0];need(isinstance(stmt,ast.Expr) and isinstance(stmt.value,ast.Call),'REPORT-APPEND-STATEMENT')
 call=stmt.value
 need(ast.unparse(call)=="details['cleanup'].append([name, type(close_error).__name__, str(close_error)])" and not call.keywords and len(call.args)==1,'REPORT-ITEM-EXPRESSION')
 sub=call.func.value;item=call.args[0];name,ename,message=item.elts
 need(isinstance(call.func,ast.Attribute) and call.func.attr=='append' and isinstance(sub,ast.Subscript) and isinstance(item,ast.List) and isinstance(ename,ast.Attribute) and ename.attr=='__name__','REPORT-EXPRESSION-SHAPE')
 points=[]
 def point(label,node,region):points.append((label,node,region))
 # Semantic boundaries, not claims about Python allocation or opcode history.
 point('handler-type-evaluation',h.type,'handler-matching')
 point('handler-match',h.type,'handler-matching')
 point('handler-selection',h,'handler-selection')
 point('handler-entry',h,'handler-entry')
 point('caught-error-binding-attempt',h,'caught-binding')
 point('caught-error-binding-complete',h,'caught-binding')
 # Callable first; then list elements left-to-right, including inner callables.
 point('report-details-evaluation',sub.value,'report-target')
 point('report-key-evaluation',sub.slice,'report-target')
 point('report-list-resolution',sub,'report-target')
 point('report-method-evaluation',call.func,'report-target')
 point('report-item-name',name,'report-item')
 point('error-type-callable',ename.value.func,'report-item')
 point('error-type-argument',ename.value.args[0],'report-item')
 point('error-type-call-attempt',ename.value,'report-item')
 point('error-type-call-return',ename.value,'report-item')
 point('error-name-attribute',ename,'report-item')
 point('error-str-callable',message.func,'report-item')
 point('error-str-argument',message.args[0],'report-item')
 point('error-str-call-attempt',message,'report-item')
 point('error-str-call-return',message,'report-item')
 point('report-item-complete',item,'report-item')
 point('report-append-attempt',call,'report-append')
 point('report-append-complete',stmt,'report-append')
 protected_stages={n:copy.deepcopy(v) for n,v in parent['source']['stages'].items() if v['semantic_region'] in ('protected-close','protected-append')}
 need(bool(protected_stages),'REPORT-PROTECTED-DOMAIN')
 return {'sources':pins,'handler':{**loc(h),'source':pins['launcher']},'catch_family':h.type.id,'catch_name':h.name,'shared_try':loc(protected),
  'eligible_parent_stages':protected_stages,'name_expression':ast.unparse(name),'target_expression':ast.unparse(sub),'item_expressions':[ast.unparse(x) for x in item.elts],
  'dynamic_origins':{'error_name':{**loc(ename),'source':pins['launcher']},'message':{**loc(message),'source':pins['launcher']}},
  'order':[n for n,_,_ in points],'stages':{n:{**loc(node),'source':copy.deepcopy(pins['launcher']),'semantic_region':region} for n,node,region in points},
  'continuity':'Explicit conditional selected-error delivery and owner/local/name/details/list/method continuity; not runtime identity or exclusivity',
  'stop':'Selected error-item append completion or first nonnormal frontier; handler exit and all later cleanup remain unestablished'}

def compile_error_report(launcher,entry,manager,parent):
 source=error_report_source(launcher,entry,manager,parent)
 return {'format':'I164-CLEANUP-ERROR-REPORT-STATIC-1','source':source,'parent_catalogue_identity':{'sha256':digest((json.dumps(parent,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode())},
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'parent':'Selected actual modeled raise within the same protected close/normal-append try; not an outside failure, normal return, process termination or unobserved frontier',
   'continuity':'Explicit conditional premise or UNESTABLISHED; unknown establishes no handler progress','prefixes':['control absent','earlier control construction and callback completed normally'],
   'close_vs_append':'Preserve selected origin and any acknowledged normal close; caught name does not imply close failed',
   'normal':'Successful suboperations retain original constructor and active selected caught error; no normal overall return or handler exit',
   'raise':'Later matching/binding/reporting error distinct from selected cleanup error and constructor error',
   'termination':'None terminal-exception classification; no inferred unwind or completed reporting',
   'unobserved':'None terminal-exception classification; earlier acknowledged facts retained, continuation unknown',
   'partial_effects':'Earlier uncertain append effects survive successful error reporting; no exact complete list inferred'},
  'preserved_relations':['exceptional_cleanup_append_correspondence',*parent['preserved_relations']],
  'runtime_error_report_chain':None,'actual_admission':False}

def validate_error_report(launcher,entry,manager,parent,submitted):
 status_exact_tree(submitted,'REPORT-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_error_report(launcher,entry,manager,parent),'REPORT-SOURCE-CORRESPONDENCE');return True

def error_report_binding(catalogue,parent,anchor,continuity):
 for v in (catalogue,parent,anchor,continuity):status_exact_tree(v,'REPORT-BINDING-TYPES')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'REPORT-CONTINUITY-DOMAIN')
 need(parent['kind']=='CONSTRUCTED-EXCEPTIONAL-CLEANUP-APPEND' and parent['completion']=='exception-frontier' and parent['terminal_python_exception_in_model'] is True,'REPORT-PARENT-FAILURE')
 err=parent['replacement_error_in_model'];need(type(err) is dict and bool(parent['events']),'REPORT-SELECTED-ERROR')
 event=parent['events'][-1];source=catalogue['source'];stage=event['stage']
 need(event['outcome']=='raise' and stage in source['eligible_parent_stages'],'REPORT-PROTECTED-FAILURE')
 origin=source['eligible_parent_stages'][stage]
 status_typed_same(event['source'],origin,'REPORT-FAILURE-OCCURRENCE-SOURCE');status_typed_same(err['origin'],origin,'REPORT-ERROR-ORIGIN')
 need(err['eligible_inner_handler']==source['catch_name'] and err['handler_entry_established'] is False and parent['inner_handler_entry_established'] is False,'REPORT-HANDLER-FRONTIER')
 scope=parent['scope'];status_typed_same(err['scope'],scope,'REPORT-ERROR-SCOPE');status_typed_same(event['scope'],scope,'REPORT-EVENT-SCOPE');status_typed_same(parent['instance_anchor'],anchor,'REPORT-INSTANCE')
 status_typed_same(parent['last_pending_error_in_model'],err,'REPORT-PENDING-SELECTED')
 need(err['reference']==scope['invocation']+'/cleanup/'+stage+'/error' and event['id']==scope['invocation']+'/cleanup/'+stage,'REPORT-FAILURE-OCCURRENCE')
 details=parent['details_after_acknowledged_steps'];b=parent['binding']
 return {'scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'selected_failure':copy.deepcopy(err),'failure_occurrence':copy.deepcopy(event),'constructor_error':copy.deepcopy(parent['earlier_constructor_exception']),
  'references':copy.deepcopy(b['references']),'selected_name':b['name'],'selected_object':copy.deepcopy(b['object']),
  'details_role':{'role':details['role'],'reference':details['reference'],'scope':copy.deepcopy(details['scope'])},'cleanup_list':copy.deepcopy(details['cleanup_reference']),
  'caught_name':source['catch_name'],'handler_origin':copy.deepcopy(source['handler']),'continuity':continuity,'premise':source['continuity'],
  'physical_identity_observed':None,'runtime_delivery_observed':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN'}

def error_report_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'REPORT-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'REPORT-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'REPORT-VALIDATED:'+k)
 source=catalogue['source'];parent=case['parent_result'];scope=case['scope'];anchor=case['anchor'];binding=case['binding']
 status_typed_same(scope,parent['scope'],'REPORT-PARENT-SCOPE');status_typed_same(anchor,parent['instance_anchor'],'REPORT-PARENT-INSTANCE')
 status_typed_same(binding,error_report_binding(catalogue,parent,anchor,binding['continuity']),'REPORT-EXPECTED-BINDING')
 selected=binding['selected_failure'];original=binding['constructor_error'];outcomes=case['outcomes']
 need(type(outcomes) is list and bool(outcomes),'REPORT-OUTCOMES')
 if binding['continuity']=='UNESTABLISHED':status_typed_same(outcomes,[{'stage':source['order'][0],'outcome':'unobserved'}],'REPORT-UNKNOWN-CONTINUITY')
 events=[];done=set();replacement=None;terminal=None
 for i,stage in enumerate(source['order']):
  need(i<len(outcomes),'REPORT-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==stage,'REPORT-STEP-ORDER')
  terminal=row['outcome'];need(type(terminal) is str and terminal in ('normal','raise','process-termination','unobserved'),'REPORT-OUTCOME')
  origin=source['stages'][stage];events.append({'id':scope['invocation']+'/error-report/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(origin),'outcome':terminal,'selected_failure_occurrence':copy.deepcopy(binding['failure_occurrence']),'selected_error':copy.deepcopy(selected),'owner':copy.deepcopy(binding['references']['owner']),'token':copy.deepcopy(binding['references']['token']),'runtime_frame':None})
  if terminal!='normal':
   if terminal=='raise':replacement={'role':'conditional-error-report-replacement','reference':scope['invocation']+'/error-report/'+stage+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(origin),'exact_type':None,'exact_value_bytes':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  done.add(stage)
 need(len(outcomes)==len(events),'REPORT-UNREACHED-STEPS')
 entered='handler-entry' in done;bound='caught-error-binding-complete' in done;appended='report-append-complete' in done
 def symbolic(which):
  idx=1 if which=='error_name' else 2
  return {'role':'unobserved-error-report-'+which,'expression':source['item_expressions'][idx],'origin':copy.deepcopy(source['dynamic_origins'][which]),'argument':copy.deepcopy(selected),'caught_name':source['catch_name'],'exact_type':None,'exact_value':None,'formatted_bytes':None,'runtime_observation':False}
 item=[binding['selected_name'],symbolic('error_name'),symbolic('message')] if 'report-item-complete' in done else None
 attempt=any(e['stage']=='report-append-attempt' for e in events)
 prior_unknown=parent['cleanup_list_after_frontier']=='UNKNOWN partial effects'
 current_unknown=attempt and not appended
 details=copy.deepcopy(parent['details_after_acknowledged_steps'])
 return {'kind':'CONSTRUCTED-CLEANUP-ERROR-REPORT','scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'validated_parent':copy.deepcopy(parent),'binding':copy.deepcopy(binding),'events':events,
  'completion':'selected-error-item-append' if appended else {'raise':'replacement-exception-frontier','process-termination':'process-termination','unobserved':'unobserved-continuation'}[terminal],
  'earlier_constructor_exception':copy.deepcopy(original),'selected_cleanup_error':copy.deepcopy(selected),'selected_failure_occurrence':copy.deepcopy(binding['failure_occurrence']),
  'failure_origin_region':selected['failure_region'],'earlier_control_completed_in_model':parent['earlier_control_completed_in_model'],'selected_owner_continuity':copy.deepcopy(parent['selected_owner_continuity']),
  'handler_eligible_in_model':True,'handler_match_completed_in_model':'handler-match' in done,'handler_selected_in_model':'handler-selection' in done,'handler_entry_completed_in_model':entered,
  'caught_binding_attempted_in_model':any(e['stage']=='caught-error-binding-attempt' for e in events),'caught_binding_completed_in_model':bound,'caught_name_in_model':source['catch_name'] if bound else None,'caught_error_in_model':copy.deepcopy(selected) if bound else None,
  'last_acknowledged_active_caught_error_in_model':copy.deepcopy(selected if entered else original),'active_at_terminal_observed':None,
  'original_error_pending_in_outer_handler':copy.deepcopy(original),'last_pending_error_in_model':copy.deepcopy(replacement or selected),'replacement_error_in_model':replacement,
  'pending_disposition':'Selected cleanup error remains represented inside its handler until handler exit, which is not modeled; no eventual propagation asserted',
  'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,'normal_overall_return_established':False,
  'close_normal_return_completed_in_model':parent['close_normal_return_completed_in_model'],'close_itself_failed_established_in_model':parent['close_itself_failed_established_in_model'],'managed_close_relation':copy.deepcopy(parent['managed_close_relation']),
  'error_item_completed_in_model':item is not None,'error_item_in_model':item,'report_append_attempted_in_model':attempt,'report_append_completed_in_model':appended,
  'details_after_predecessor_acknowledged_steps':details,
  'cleanup_list_state':{'target':copy.deepcopy(binding['cleanup_list']),'last_predecessor_acknowledged_literals':copy.deepcopy(details['known_literal_fields']['cleanup']),
   'prior_partial_effects':'UNKNOWN' if prior_unknown else 'No earlier append call reached in validated prefix','current_partial_effects':'UNKNOWN' if current_unknown else 'Acknowledged selected error-item append' if appended else 'No error-item append call reached',
   'any_unresolved_partial_effects':prior_unknown or current_unknown,'acknowledged_append':{'item':copy.deepcopy(item),'target':copy.deepcopy(binding['cleanup_list']),'occurrence':scope['invocation']+'/error-report/report-append-complete'} if appended else None,
   'complete_contents_established':False,'exact_runtime_contents':None},
  'known_false_flags_preserved':{k:details['known_literal_fields'][k] for k in ('nonexecution_established','new_authorization')},
  'dynamic_details_origins_preserved':copy.deepcopy(details['dynamic_fields']),
  'handler_exit_established':False,'later_iteration_established':False,'loop_completion_established':False,'failure_file_established':False,'final_rethrow_established':False,'owner_finalization_established':False,'complete_cleanup_established':False,
  'existing_cause_context_suppression':'UNKNOWN; no new explicit-cause or suppression assignment; original, selected and replacement errors remain distinct',
  'runtime_error_report_chain':None,'runtime_observation':False,'observer_join':None,'physical_reference_identity':None,'physical_closure_established':False,'durability_established':False,'released_ownership_established':False,
  'completion_flags_mean':'Acknowledged conditional progress, not observed objects/opcodes; false does not prove absence of partial effects','obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_error_report_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'REPORT-SUBMITTED-OUTPUT');status_typed_same(submitted,error_report_projection(catalogue,case,validated),'REPORT-OUTPUT-CORRESPONDENCE');return True
