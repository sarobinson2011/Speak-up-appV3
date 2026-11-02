
# Bounded exceptional cleanup selection, close and normal append. No runtime calls.
def cleanup_append_source(launcher,entry,manager,details,reference):
 for raw in (launcher,entry,manager):need(type(raw) is bytes,'CLEANUP-SOURCE-BYTES')
 for v in (details,reference):status_exact_tree(v,'CLEANUP-PARENT-CATALOGUE')
 pins={n:{'bytes':len(raw),'sha256':digest(raw)} for n,raw in [('launcher',launcher),('entry',entry),('manager',manager)]}
 status_typed_same(details['source']['sources'],{n:pins[n] for n in ('launcher','entry')},'CLEANUP-DETAILS-SOURCES')
 status_typed_same(pins['manager'],{k:reference['source']['source'][k] for k in ('bytes','sha256')},'CLEANUP-MANAGER-SOURCE')
 tree,loc=_client_locate(launcher);mt,ml=_client_locate(manager)
 fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session');outer=fn.body[-1];tr=outer.body[-1];handler=tr.handlers[0];loop=handler.body[1]
 need(isinstance(tr,ast.Try) and handler.name=='e' and ast.unparse(handler.type)=='BaseException','CLEANUP-OUTER-HANDLER')
 status_typed_same({**loc(loop),'source':pins['launcher']},details['source']['stop_before'],'CLEANUP-PARENT-FRONTIER')
 need(isinstance(loop,ast.For) and not loop.orelse and len(loop.body)==1 and ast.unparse(loop.target)=='(name, obj)','CLEANUP-LOOP-SHAPE')
 need(isinstance(loop.iter,ast.List) and len(loop.iter.elts)==2,'CLEANUP-INPUT-SHAPE')
 inputs=[]
 for pair in loop.iter.elts:
  need(isinstance(pair,ast.Tuple) and len(pair.elts)==2 and isinstance(pair.elts[0],ast.Constant) and type(pair.elts[0].value) is str and isinstance(pair.elts[1],ast.Name),'CLEANUP-INPUT-PAIR')
  inputs.append({'name':pair.elts[0].value,'slot':pair.elts[1].id,'name_origin':loc(pair.elts[0]),'object_origin':loc(pair.elts[1]),'pair_origin':loc(pair)})
 status_typed_same([[v['name'],v['slot']] for v in inputs],[['raw','raw'],['managed','managed']],'CLEANUP-ORDERED-INPUTS')
 guard=loop.body[0];need(isinstance(guard,ast.If) and not guard.orelse and len(guard.body)==1,'CLEANUP-GUARD-SHAPE')
 test=guard.test;need(isinstance(test,ast.Compare) and isinstance(test.left,ast.Name) and test.left.id=='obj' and len(test.ops)==len(test.comparators)==1 and isinstance(test.ops[0],ast.IsNot) and isinstance(test.comparators[0],ast.Constant) and test.comparators[0].value is None,'CLEANUP-EXACT-NONNONE')
 protected=guard.body[0];need(isinstance(protected,ast.Try) and len(protected.body)==2 and len(protected.handlers)==1 and not protected.orelse and not protected.finalbody,'CLEANUP-SHARED-TRY')
 close,append=protected.body;error_handler=protected.handlers[0]
 need(ast.unparse(close)=='obj.close()' and isinstance(close,ast.Expr) and isinstance(close.value,ast.Call) and not close.value.args and not close.value.keywords,'CLEANUP-CLOSE-EXPRESSION')
 need(ast.unparse(append)=="details['cleanup'].append([name, 'close returned'])" and isinstance(append,ast.Expr) and isinstance(append.value,ast.Call) and len(append.value.args)==1 and not append.value.keywords,'CLEANUP-APPEND-EXPRESSION')
 need(error_handler.name=='close_error' and ast.unparse(error_handler.type)=='BaseException','CLEANUP-INNER-HANDLER')
 # Local slot origins and the successful handoff frontier are read from source.
 raw_init=[n for n in outer.body if isinstance(n,ast.Assign) and ast.unparse(n)=='raw = None'];managed_init=[n for n in outer.body if isinstance(n,ast.Assign) and ast.unparse(n)=='managed = None']
 need(len(raw_init)==len(managed_init)==1,'CLEANUP-LOCAL-INITIALIZATION')
 create=tr.body[0];need(isinstance(create,ast.If) and ast.unparse(create.test)=='create' and not create.orelse,'CLEANUP-CREATE-PREFIX')
 status_typed_same([ast.unparse(n) for n in create.body[:4]],['raw = authority.Authority.__new__(authority.Authority)',"authority.Authority.__init__(raw, db, cfg['config'], True, ownership_path=owners)",'raw.close()','raw = None'],'CLEANUP-RAW-CLEAR-PREFIX')
 managed=tr.body[1];need(ast.unparse(managed)=="managed, _ = open_session(c, db, cfg['config'], ownership_path=owners)",'CLEANUP-MANAGED-BINDING')
 yielded=tr.body[-4];need(ast.unparse(yielded)=='yield ManagedSession(managed)','CLEANUP-HANDOFF')
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedSession');init=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
 need(ast.unparse(init)=='def __init__(self, managed):\n    self.__managed = managed','CLEANUP-SESSION-REFERENCE')
 # No local raw/managed rebind in the selected handler before loop selection.
 need(not any(isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store) and n.id in ('raw','managed') for n in ast.walk(handler.body[0])),'CLEANUP-DETAILS-LOCAL-REBIND')
 mcls=next(n for n in mt.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');mc=next(n for n in mcls.body if isinstance(n,ast.FunctionDef) and n.name=='close')
 rp=[p for p in reference['source']['programs'] if p['function']=='close'];need(len(rp)==1,'CLEANUP-REFERENCE-CLOSE-PROGRAM')
 need(rp[0]['ast']==ast.dump(mc,include_attributes=False),'CLEANUP-REFERENCE-CLOSE-AST')
 points=[]
 def point(name,node,region='loop-selection'):points.append((name,node,region))
 point('loop-input-evaluation',loop.iter)
 for pair,record in zip(loop.iter.elts,inputs):
  label=record['name'];point('input-'+label+'-name',pair.elts[0]);point('input-'+label+'-object',pair.elts[1]);point('input-'+label+'-pair',pair)
 point('loop-inputs-complete',loop.iter);point('loop-iterator-attempt',loop)
 for record in inputs:
  label=record['name'];point(label+'-item-next',loop)
  for target in loop.target.elts:point(label+'-bind-'+target.id,target)
  point(label+'-guard-object',test.left);point(label+'-guard-none',test.comparators[0]);point(label+'-guard-result',test)
 # Expression traversal follows Python's callable-first, arguments-next order.
 point('selected-try-entry',protected,'try-entry')
 point('close-object-evaluation',close.value.func.value,'protected-close');point('close-method-evaluation',close.value.func,'protected-close');point('close-call-attempt',close.value,'protected-close');point('close-normal-return',close,'protected-close')
 call=append.value;sub=call.func.value;item=call.args[0]
 need(isinstance(sub,ast.Subscript) and isinstance(item,ast.List) and len(item.elts)==2,'CLEANUP-APPEND-PARTS')
 point('append-details-evaluation',sub.value,'protected-append');point('append-key-evaluation',sub.slice,'protected-append');point('append-list-resolution',sub,'protected-append');point('append-method-evaluation',call.func,'protected-append')
 for expression in item.elts:
  point('append-item-'+('name' if isinstance(expression,ast.Name) else 'message'),expression,'protected-append')
 point('append-item-complete',item,'protected-append');point('append-call-attempt',call,'protected-append');point('append-complete',append,'protected-append')
 return {'sources':pins,'ordered_inputs':inputs,'selected_name':inputs[1]['name'],'selected_slot':inputs[1]['slot'],'guard_expression':ast.unparse(test),'guard_semantics':'identity is not None; no truthiness substitution','guard_results':{'raw':False,'managed':True},
  'raw_origins':{'initial':loc(raw_init[0]),'create_close':loc(create.body[2]),'create_clear':loc(create.body[3])},'managed_initial':loc(managed_init[0]),'managed_assignment':loc(managed),'handoff':loc(yielded),'wrapper_reference':loc(init),
  'manager_close':{**ml(mc),'source':pins['manager']},'reference_close_program':copy.deepcopy(rp[0]),'close_method':close.value.func.attr,'close_arguments':[],'close_keywords':[],'close_return_use':'discarded expression result; no concrete return value asserted',
  'append_target_expression':ast.unparse(sub),'append_item_expressions':[ast.unparse(n) for n in item.elts],'append_message':item.elts[1].value,'inner_handler':{**loc(error_handler),'source':pins['launcher']},'inner_handler_name':error_handler.name,'same_try':loc(protected),
  'order':[n for n,_,_ in points],'stages':{n:{**loc(node),'source':copy.deepcopy(pins['launcher']),'semantic_region':region} for n,node,region in points},
  'continuity_premise':'Explicit conditional continuity of launcher locals, selected manager/method and details cleanup-list roles from validated handoff and completed details assignment. Not runtime identity, exclusivity, absence of mutation or qualification.',
  'raw_admissibility':'At the selected post-yield constructor-error route raw is None: initialized None on reopening, or cleared only after raw close returned on creation. A surviving partially constructed raw belongs to a different earlier route.',
  'stop':'Selected normal append only; no line172 error-report append, later iteration/loop completion, failure write, rethrow or owner-lock finalization'}

def compile_cleanup_append(launcher,entry,manager,details,reference):
 source=cleanup_append_source(launcher,entry,manager,details,reference)
 return {'format':'I164-EXCEPTIONAL-CLEANUP-APPEND-STATIC-1','source':source,'parent_catalogue_identity':{'sha256':digest((json.dumps(details,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode())},
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'parent':'Completed initial details assignment; original selected constructor error pending; no replacement','prefixes':['control absent','earlier control construction and callback completed normally'],'locals':'Same validated handoff under explicit continuity; raw None skipped, managed non-None selected','guard':'obj is not None by identity','normal':'Source-ordered progress; managed close return independently checked by reference-path interpreter before append','close_or_append_raise':'Distinct origins within same try; close_error handler is eligible but not entered/expanded by this slice','earlier_raise':'Loop input/iteration/binding/guard failures are outside the inner close_error try','termination':'No inferred Python exception or unwind','unobserved':'No further completion; absence of partial effects not established','continuity_unknown':'No loop-selection progress established'},
  'preserved_relations':['launcher_initial_details_correspondence',*details['preserved_relations']], 'runtime_cleanup_append_chain':None,'actual_admission':False}

def validate_cleanup_append(launcher,entry,manager,details,reference,submitted):
 status_exact_tree(submitted,'CLEANUP-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_cleanup_append(launcher,entry,manager,details,reference),'CLEANUP-SOURCE-CORRESPONDENCE');return True

def cleanup_append_binding(catalogue,parent,anchor,continuity):
 for v in (catalogue,parent,anchor,continuity):status_exact_tree(v,'CLEANUP-BINDING-TYPES')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'CLEANUP-CONTINUITY')
 scope=parent['scope'];refs=parent['delivery_binding']['references'];details=parent['details_in_model'];need(type(details) is dict,'CLEANUP-DETAILS-REQUIRED')
 return {'scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'selected_error':copy.deepcopy(parent['earlier_constructor_exception']),'references':copy.deepcopy(refs),'ordered_values':[{'name':'raw','value':None,'exact_type':'NoneType'},{'name':'managed','value':copy.deepcopy(refs['manager']),'meaning':'source-qualified manager reference, not an observed Python object'}],
  'selected_index':1,'name':catalogue['source']['selected_name'],'object':copy.deepcopy(refs['manager']),'guard':{'expression':catalogue['source']['guard_expression'],'left':copy.deepcopy(refs['manager']),'right':None,'right_exact_type':'NoneType','result':True},
  'close_receiver':copy.deepcopy(refs['manager']),'method':catalogue['source']['close_method'],'method_origin':copy.deepcopy(catalogue['source']['manager_close']),'cleanup_list':copy.deepcopy(details['cleanup_reference']),'append_item':[catalogue['source']['selected_name'],catalogue['source']['append_message']],
  'continuity':continuity,'premise':catalogue['source']['continuity_premise'],'runtime_object_identity':None}

def cleanup_append_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'CLEANUP-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','close_result','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'CLEANUP-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'CLEANUP-VALIDATED:'+k)
 parent=case['parent_result'];source=catalogue['source'];scope=case['scope'];anchor=case['anchor'];binding=case['binding'];error=parent['earlier_constructor_exception']
 need(parent['kind']=='CONSTRUCTED-LAUNCHER-INITIAL-DETAILS' and parent['details_assignment_completed_in_model'] is True and parent['replacement_error_in_model'] is None,'CLEANUP-COMPLETED-DETAILS')
 status_typed_same(parent['last_pending_error_in_model'],error,'CLEANUP-PENDING-ORIGINAL');status_typed_same(parent['active_caught_error_in_model'],error,'CLEANUP-ACTIVE-ORIGINAL');status_typed_same(scope,parent['scope'],'CLEANUP-PARENT-SCOPE');status_typed_same(anchor,parent['instance_anchor'],'CLEANUP-INSTANCE')
 status_typed_same(binding,cleanup_append_binding(catalogue,parent,anchor,binding['continuity']),'CLEANUP-SELECTED-BINDING')
 need(parent['cleanup_loop_entered'] is False,'CLEANUP-PARENT-FRONTIER');outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'CLEANUP-OUTCOMES')
 if binding['continuity']=='UNESTABLISHED':status_typed_same(outcomes,[{'stage':source['order'][0],'outcome':'unobserved'}],'CLEANUP-UNKNOWN-CONTINUITY')
 events=[];done=set();replacement=None;terminal=None;close_reached=False;cr=case['close_result']
 for i,stage in enumerate(source['order']):
  need(i<len(outcomes),'CLEANUP-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==stage,'CLEANUP-STEP-ORDER');kind=row['outcome'];need(type(kind) is str and kind in ('normal','raise','process-termination','unobserved'),'CLEANUP-OUTCOME');terminal=kind
  if stage=='close-normal-return':
   close_reached=True
   if cr is None:need(kind in ('process-termination','unobserved'),'CLEANUP-MISSING-CLOSE-RELATION')
   elif cr['completion']=='normal':need(kind=='normal' and cr['final']=={'_live':None,'_retired':None,'_phase':'CLOSED'},'CLEANUP-CLOSE-NORMAL-CORRESPONDENCE')
   elif cr['completion']=='abrupt':need(kind=='raise','CLEANUP-CLOSE-RAISE-CORRESPONDENCE')
   else:need(cr['completion']=='partial-prefix' and kind in ('process-termination','unobserved'),'CLEANUP-CLOSE-PARTIAL-CORRESPONDENCE')
  origin=source['stages'][stage];events.append({'id':scope['invocation']+'/cleanup/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(origin),'outcome':kind,'selected_object':copy.deepcopy(binding['object']),'selected_error':copy.deepcopy(error),'runtime_frame':None})
  if kind!='normal':
   if kind=='raise':replacement={'role':'conditional-cleanup-error','reference':scope['invocation']+'/cleanup/'+stage+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(origin),'failure_region':origin['semantic_region'],'eligible_inner_handler':source['inner_handler_name'] if origin['semantic_region'] in ('protected-close','protected-append') else None,'handler_entry_established':False,'exact_type':None,'exact_value_bytes':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  done.add(stage)
 need(len(outcomes)==len(events),'CLEANUP-UNREACHED-STEPS')
 if not close_reached:need(cr is None,'CLEANUP-UNREACHED-CLOSE-RELATION')
 closed='close-normal-return' in done;appended='append-complete' in done;details=copy.deepcopy(parent['details_in_model'])
 if appended:details['known_literal_fields']['cleanup'].append(copy.deepcopy(binding['append_item']))
 return {'kind':'CONSTRUCTED-EXCEPTIONAL-CLEANUP-APPEND','scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'validated_parent':copy.deepcopy(parent),'binding':copy.deepcopy(binding),'events':events,'completion':'selected-normal-append' if appended else {'raise':'exception-frontier','process-termination':'process-termination','unobserved':'unobserved-continuation'}[terminal],
  'earlier_constructor_exception':copy.deepcopy(error),'earlier_control_completed_in_model':parent['earlier_control_completed_in_model'],'selected_owner_continuity':copy.deepcopy(parent['selected_owner_continuity']),
  'raw_guard_false_completed_in_model':'raw-guard-result' in done,'selected_name_bound_in_model':'managed-bind-name' in done,'selected_object_bound_in_model':'managed-bind-obj' in done,'selected_non_none_guard_completed_in_model':'managed-guard-result' in done,
  'close_method_evaluation_completed_in_model':'close-method-evaluation' in done,'close_attempt_entered_in_model':any(e['stage']=='close-call-attempt' for e in events),'close_normal_return_completed_in_model':closed,'managed_close_relation':copy.deepcopy(cr),'close_return_value_observed':None,'close_return_use':source['close_return_use'],
  'append_evaluation_entered_in_model':any(e['stage']=='append-details-evaluation' for e in events),'append_attempt_entered_in_model':any(e['stage']=='append-call-attempt' for e in events),'append_completed_in_model':appended,'details_after_acknowledged_steps':details,'cleanup_list_after_frontier':'exact constructed appended item' if appended else 'UNKNOWN partial effects' if terminal!='normal' and any(e['stage']=='append-call-attempt' for e in events) else 'no append call reached in this modeled prefix',
  'replacement_error_in_model':replacement,'last_pending_error_in_model':copy.deepcopy(replacement or error),'close_itself_failed_established_in_model':close_reached and cr is not None and cr['completion']=='abrupt','terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True if terminal=='raise' else False,
  'inner_handler_entry_established':False,'error_report_append_expanded':False,'later_iteration_established':False,'loop_completion_established':False,'failure_file_established':False,'final_rethrow_established':False,'owner_finalization_established':False,'managed_local_clear_established':False,'ACTIVE_unlink_established':False,
  'completion_flags_mean':'Acknowledged conditional modeled progress; false does not prove absence of partial effects','existing_cause_context_suppression':'UNKNOWN; selected original remains represented; no new exception chain evidence','runtime_cleanup_append_chain':None,'runtime_observation':False,'physical_reference_identity':None,'physical_closure_established':False,'durability_established':False,'released_ownership_established':False,'complete_cleanup_established':False,'observer_join':None,'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_cleanup_append_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'CLEANUP-SUBMITTED-OUTPUT');status_typed_same(submitted,cleanup_append_projection(catalogue,case,validated),'CLEANUP-OUTPUT-CORRESPONDENCE');return True
