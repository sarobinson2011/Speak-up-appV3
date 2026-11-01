
# Bounded constructor-error delivery and initial launcher details; no runtime execution.
def launcher_details_source(launcher,entry,client_construction):
 for raw in (launcher,entry):need(type(raw) is bytes,'DETAILS-SOURCE-BYTES')
 status_exact_tree(client_construction,'DETAILS-PARENT-CATALOGUE')
 pins={'launcher':{'bytes':len(launcher),'sha256':digest(launcher)},'entry':{'bytes':len(entry),'sha256':digest(entry)}}
 status_typed_same(client_construction['source']['sources'],pins,'DETAILS-PARENT-SOURCES')
 lt,ll=_client_locate(launcher);et,el=_client_locate(entry)
 def function(tree,name):
  found=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name];need(len(found)==1,'DETAILS-FUNCTION:'+name);return found[0]
 run=function(et,'_run');session=function(lt,'session');private=function(lt,'_session')
 rw=[n for n in ast.walk(run) if isinstance(n,ast.With) and ast.unparse(n.items[0].context_expr).startswith('launcher.session(')]
 need(len(rw)==1 and len(rw[0].items)==1,'DETAILS-RUN-WITH');rw=rw[0]
 need(ast.unparse(rw.items[0].context_expr)=='launcher.session(candidate, draft, runtime, destination, create=create)' and ast.unparse(rw.items[0].optional_vars)=='wrapper','DETAILS-RUN-ROUTE')
 for fn in (session,private):need([ast.unparse(d) for d in fn.decorator_list]==['contextlib.contextmanager'],'DETAILS-GENERATOR-DECORATOR')
 sw=session.body[-1];need(isinstance(sw,ast.With) and len(sw.items)==1 and ast.unparse(sw.items[0].context_expr)=='_session(*args, **kwargs)' and ast.unparse(sw.items[0].optional_vars)=='managed','DETAILS-PUBLIC-PRIVATE-BRIDGE')
 need(len(sw.body)==1 and isinstance(sw.body[0],ast.Expr) and isinstance(sw.body[0].value,ast.Yield) and ast.unparse(sw.body[0].value.value)=='managed','DETAILS-PUBLIC-YIELD');sy=sw.body[0]
 protected=[n for n in ast.walk(private) if isinstance(n,ast.Try) and any(h.name=='e' and ast.unparse(h.type)=='BaseException' for h in n.handlers)]
 need(len(protected)==1,'DETAILS-PRIVATE-CATCH');tr=protected[0];need(len(tr.handlers)==1,'DETAILS-PRIVATE-HANDLERS');handler=tr.handlers[0]
 py=[n for n in tr.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Yield)]
 need(len(py)==1 and ast.unparse(py[0].value.value)=='ManagedSession(managed)','DETAILS-PRIVATE-YIELD');py=py[0]
 need([ast.unparse(n) for n in tr.body[tr.body.index(py)+1:]]==['managed.close()','managed = None',"(dest / 'ACTIVE.json').unlink()"],'DETAILS-NORMAL-ROUTE-IDENTITY')
 assignment=handler.body[0];need(isinstance(assignment,ast.Assign) and len(assignment.targets)==1 and ast.unparse(assignment.targets[0])=='details' and isinstance(assignment.value,ast.Dict),'DETAILS-ASSIGNMENT')
 d=assignment.value;need(all(isinstance(k,ast.Constant) and type(k.value) is str for k in d.keys),'DETAILS-LITERAL-KEYS')
 names=[k.value for k in d.keys];expressions=[ast.unparse(v) for v in d.values]
 need(names==['error','message','traceback','nonexecution_established','new_authorization','cleanup'],'DETAILS-FIELD-DOMAIN')
 need(expressions==['type(e).__name__','str(e)','traceback.format_exc()','False','False','[]'],'DETAILS-FIELD-ORIGINS')
 need(isinstance(handler.body[1],ast.For),'DETAILS-STOP-BEFORE-LOOP')
 status_typed_same(client_construction['source']['run'],el(run),'DETAILS-PARENT-RUN')
 points=[('run-with-exception-exit',el(rw),pins['entry'],'conditional-context-exit'),('session-yield-delivery',ll(sy),pins['launcher'],'conditional-generator-delivery'),('session-inner-with-exception-exit',ll(sw),pins['launcher'],'conditional-context-exit'),('private-yield-delivery',ll(py),pins['launcher'],'conditional-generator-delivery'),('launcher-handler-entry',ll(handler),pins['launcher'],'handler-entry'),('details-evaluation-attempt',ll(assignment),pins['launcher'],'statement-evaluation-entry')]
 fields=[]
 for key,value in zip(d.keys,d.values):
  name=key.value;points.extend([('details-key-'+name,ll(key),pins['launcher'],'key-evaluation'),('details-value-'+name,ll(value),pins['launcher'],'value-evaluation')])
  fields.append({'name':name,'key_source':{**ll(key),'source':copy.deepcopy(pins['launcher'])},'value_source':{**ll(value),'source':copy.deepcopy(pins['launcher'])},'expression':ast.unparse(value),'error_relation':'delivered e argument' if name in ('error','message') else 'selected active caught exception, conditional continuity' if name=='traceback' else 'source literal'})
 points.extend([('details-dict-completion',ll(d),pins['launcher'],'dictionary-construction-completion'),('details-assignment-attempt',ll(assignment.targets[0]),pins['launcher'],'local-binding-attempt'),('details-assignment-complete',ll(assignment),pins['launcher'],'local-binding-completion')])
 return {'sources':pins,'run':el(run),'public_session':ll(session),'private_session':ll(private),'catch_binding':handler.name,'catch_family':ast.unparse(handler.type),'fields':fields,'order':[n for n,_,_,_ in points],
  'stages':{n:{**loc,'source':copy.deepcopy(pin),'semantic_region':region} for n,loc,pin,region in points},'stop_before':{**ll(handler.body[1]),'source':copy.deepcopy(pins['launcher'])},
  'excluded_normal_stages':[ll(n) for n in tr.body[tr.body.index(py)+1:]],
  'propagation':'Explicit conditional ordinary context-manager exception delivery through both decorated generators; no runtime arrival follows from source anchors or completed pop',
  'evaluation_order':'Dictionary key then value pairs in defining-source order, then dictionary completion and local details binding; boundaries do not assert allocation or Python opcode history',
  'dynamic_values':'No concrete error name, message, traceback, formatted bytes or dynamic result type supplied by source correspondence',
  'scope':'Stop at initial details assignment; no cleanup-loop entry, write, outer propagation, lock release or authority change'}

def compile_launcher_details(launcher,entry,client_construction):
 source=launcher_details_source(launcher,entry,client_construction)
 return {'format':'I164-LAUNCHER-INITIAL-DETAILS-STATIC-1','source':source,
  'parent_catalogue':{'format':client_construction['format'],'identity':{'sha256':digest((json.dumps(client_construction,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode())}},
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'parent':'Reviewed exact-None bare rethrow, normal pop and original constructor error still pending; completed pop alone is insufficient','prefixes':['control absent','earlier control construction/callback completed normally'],'delivery':'Selected exception continuity is explicit conditional premise; unknown continuity establishes no handler arrival','evaluation':'Normal acknowledges only selected source-expression evaluation; exact generated values remain unknown','raise':'Replacement exception frontier; preserve earlier established constructor error and handler binding','termination':'No inferred Python exception or unwind','unobserved':'No further established progress','completion':'Known literal fields and initially empty cleanup list represented only after complete details assignment','excluded':'No normal managed close/clear/unlink, cleanup-loop, write, outward propagation or authority claim'},
  'preserved_relations':['client_construction_none_correspondence',*client_construction['preserved_relations']],
  'runtime_handler_details_observations':None,'non_none_construction_complete':False,'outer_cleanup_complete':False,'actual_admission':False}

def validate_launcher_details(launcher,entry,client_construction,submitted):
 status_exact_tree(submitted,'DETAILS-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_launcher_details(launcher,entry,client_construction),'DETAILS-SOURCE-CORRESPONDENCE');return True

def launcher_delivery_binding(catalogue,parent,anchor,continuity):
 for v in (catalogue,parent,anchor,continuity):status_exact_tree(v,'DETAILS-DELIVERY-TYPES')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'DETAILS-CONTINUITY-DOMAIN')
 source=catalogue['source'];scope=parent['scope'];refs=parent['reference_bindings']
 return {'scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'selected_error':copy.deepcopy(parent['construction_error']),
  'references':{n:copy.deepcopy(refs[n]) for n in ('owner','token','session','manager')},
  'route':[{'stage':n,'source':copy.deepcopy(source['stages'][n])} for n in source['order'][:5]],
  'launcher_name':source['catch_binding'],'continuity':continuity,'active_exception_continuity':'Conditional same selected error across ordinary delivery and normal evaluation; no observation',
  'runtime_delivery':None,'physical_object_identity':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN'}

def launcher_details_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'DETAILS-EXACT-TYPE')
 keys={'scope','anchor','parent_result','delivery_binding','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'DETAILS-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'DETAILS-VALIDATED:'+k)
 parent=case['parent_result'];scope=case['scope'];anchor=case['anchor'];source=catalogue['source'];delivery=case['delivery_binding'];error=parent['construction_error']
 status_typed_same(scope,parent['scope'],'DETAILS-PARENT-SCOPE');status_typed_same(anchor['instance'],scope['instance'],'DETAILS-INSTANCE');need(anchor['context']==scope['context'],'DETAILS-CONTEXT')
 need(parent['kind']=='CONSTRUCTED-CLIENT-CONSTRUCTION-NONE' and parent['completion']=='normal-removal-pending-construction-error','DETAILS-PARENT-COMPLETION')
 need(parent['handler_entry_completed_in_model'] is True and parent['none_guard_completed_in_model'] is True and parent['bare_rethrow_effect_established_in_model'] is True and parent['removal_completed_in_model'] is True,'DETAILS-PARENT-REQUIRED-STEPS')
 need(parent['handler_evaluation_error_in_model'] is None and parent['cleanup_error_in_model'] is None and parent['construction_outward_after_finally_established_in_model'] is True,'DETAILS-PENDING-ORIGINAL-ERROR')
 for k in ('caught_error_in_model','reraised_error_in_model','last_pending_error_in_model','outward_error_after_finally_in_model'):status_typed_same(parent[k],error,'DETAILS-PARENT-ERROR:'+k)
 need(parent['construction_completed_in_model'] is False and parent['client_callback_executed_in_model'] is False,'DETAILS-PARENT-NO-CLIENT')
 status_typed_same(delivery,launcher_delivery_binding(catalogue,parent,anchor,delivery['continuity']),'DETAILS-DELIVERY-BINDING')
 outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'DETAILS-OUTCOMES')
 if delivery['continuity']=='UNESTABLISHED':status_typed_same(outcomes,[{'stage':source['order'][0],'outcome':'unobserved'}],'DETAILS-UNESTABLISHED-DELIVERY')
 events=[];done=set();replacement=None;terminal=None;completion=None
 for i,stage in enumerate(source['order']):
  need(i<len(outcomes),'DETAILS-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==stage,'DETAILS-STEP-ORDER')
  kind=row['outcome'];need(type(kind) is str and kind in ('normal','raise','process-termination','unobserved'),'DETAILS-OUTCOME');terminal=kind
  events.append({'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(source['stages'][stage]),'outcome':kind,'selected_error':copy.deepcopy(error),'owner':copy.deepcopy(delivery['references']['owner']),'token':copy.deepcopy(delivery['references']['token']),'runtime_frame':None})
  if kind!='normal':
   if kind=='raise':replacement={'role':'conditional-launcher-delivery-or-evaluation-error','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(source['stages'][stage]),'exact_type':None,'exact_value_bytes':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','physical_identity':None}
   completion={'raise':'replacement-exception-frontier','process-termination':'process-termination','unobserved':'unobserved-continuation'}[kind];break
  done.add(stage)
  if stage==source['order'][-1]:completion='initial-details-assignment-complete'
 need(len(events)==len(outcomes),'DETAILS-UNREACHED-STEPS')
 assigned='details-assignment-complete' in done;entered='launcher-handler-entry' in done;details=None
 if assigned:
  details={'role':'conditional-initial-launcher-details','reference':scope['invocation']+'/launcher/details','scope':copy.deepcopy(scope),'assignment_source':copy.deepcopy(source['stages']['details-assignment-complete']),
   'dynamic_fields':[{'name':f['name'],'expression':f['expression'],'source':copy.deepcopy(f['value_source']),'selected_error':copy.deepcopy(error),'binding':f['error_relation'],'exact_value':None,'exact_type':None,'formatted_bytes':None,'observation':'UNAVAILABLE'} for f in source['fields'][:3]],
   'known_literal_fields':{'nonexecution_established':False,'new_authorization':False,'cleanup':[]},'cleanup_reference':{'scope':copy.deepcopy(scope),'symbol':scope['invocation']+'/launcher/details/initial-cleanup-list','meaning':'source-created empty list at this assignment; no observed physical identity'},
   'complete_runtime_dictionary_observed':False,'exact_serialized_bytes':None}
 return {'kind':'CONSTRUCTED-LAUNCHER-INITIAL-DETAILS','scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'validated_parent':copy.deepcopy(parent),'delivery_binding':copy.deepcopy(delivery),'events':events,'completion':completion,
  'earlier_constructor_exception':copy.deepcopy(error),'earlier_control_completed_in_model':parent['earlier_control_callback_completed_in_model'],'selected_owner_continuity':copy.deepcopy(parent['selected_slot_before_removal']),
  'handler_entry_completed_in_model':entered,'launcher_e_in_model':copy.deepcopy(error) if entered else None,'active_caught_error_in_model':copy.deepcopy(error) if entered else None,
  'details_evaluation_attempt_in_model':'details-evaluation-attempt' in done,'details_dictionary_completed_in_model':'details-dict-completion' in done,'details_assignment_attempt_in_model':'details-assignment-attempt' in done,'details_assignment_completed_in_model':assigned,'details_in_model':details,
  'replacement_error_in_model':replacement,'last_pending_error_in_model':copy.deepcopy(replacement or error),'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,
  'existing_cause_context_suppression':'UNKNOWN; no new chain observation','new_explicit_cause_assignment_established':False,'runtime_handler_arrival':None,'runtime_handler_details_chain':None,'runtime_unwind_evidence':'UNAVAILABLE','physical_reference_identity':None,
  'cleanup_loop_entered':False,'normal_managed_close_spliced':False,'managed_clear_spliced':False,'ACTIVE_unlink_spliced':False,'retained_failure_record_bytes':None,'failure_file_established':False,'outward_propagation_established':False,'physical_closure_established':False,'physical_lock_release_established':False,'durability_established':False,'outer_cleanup_complete':False,
  'completion_flags_mean':'Acknowledged conditional modeled progress only; false means not established, not absence of partial effects','runtime_observation':False,'observer_join':None,'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_launcher_details_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'DETAILS-SUBMITTED-OUTPUT');status_typed_same(submitted,launcher_details_projection(catalogue,case,validated),'DETAILS-OUTPUT-CORRESPONDENCE');return True
