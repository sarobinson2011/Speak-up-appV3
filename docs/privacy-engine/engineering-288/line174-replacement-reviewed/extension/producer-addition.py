
# NEW replacement construction, 2026-11-03. No unavailable earlier bytes recovered.
def write_call_source(launcher,entry,manager,loop,report,cleanup):
 for b in (launcher,entry,manager):need(type(b) is bytes,'WC-SOURCE-TYPE')
 validate_cleanup_loop(launcher,entry,manager,report,cleanup,loop)
 tree,oldloc=_client_locate(launcher);functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 fn=functions['_session'];owner=fn.body[-1];outer=owner.body[-1].handlers[0];region=outer.body[2]
 need(isinstance(region,ast.Try) and region.lineno==174 and len(region.body)==1 and not region.orelse and not region.finalbody,'WC-PROTECTED-SOURCE')
 call=region.body[0].value
 syntax="write_new(dest/'evidence'/('failure-'+str(os.getpid())+'-'+str(len(list((dest/'evidence').iterdir())))+'.json'),details)"
 need(ast.dump(call,include_attributes=False)==ast.dump(ast.parse(syntax,mode='eval').body,include_attributes=False),'WC-EXACT-EXPRESSION')
 pin=loop['source']['sources']['launcher'];status_typed_same(loop['source']['stop_before'],{**oldloc(call),'source':pin},'WC-PREDECESSOR-FRONTIER')
 lock=functions['owner_lock'];callee=functions['write_new']
 need(ast.unparse(owner.items[0].context_expr)=='owner_lock(destination)' and ast.unparse(owner.items[0].optional_vars)=='dest','WC-OWNER-BRIDGE')
 need(ast.unparse(lock.body[0])=='dest = Path(destination).absolute()' and ast.unparse(lock.body[2])=='parent = dest.parent.resolve()' and ast.unparse(lock.body[4])=='dest = parent / dest.name','WC-DESTINATION-ORIGIN')
 ys=[n for n in ast.walk(lock) if isinstance(n,ast.Yield)];need(len(ys)==1 and ast.unparse(ys[0].value)=='dest','WC-DESTINATION-YIELD')
 need([a.arg for a in callee.args.args]==['p','x'] and not callee.args.defaults and not callee.args.vararg and not callee.args.kwarg,'WC-CALLEE-ARGS')
 def loc(n):return {'source':copy.deepcopy(pin),'site':[n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__],'expression':ast.get_source_segment(launcher.decode(),n)}
 steps=[]
 def add(path,node,op,inputs,normal='normal',**kw):
  ident='write:'+path;need(ident not in {s['id'] for s in steps},'WC-UNIQUE-DECLARATION')
  steps.append({'id':ident,'source':loc(node),'operation':op,'inputs':inputs,'normal_outcome':normal,**kw});return ident
 add('continuation',region,'explicit continuation into selected protecting try',[])
 def visit(n,path):
  if isinstance(n,ast.Name):
   need(isinstance(n.ctx,ast.Load),'WC-NAME-LOAD');return add(path,n,'name lookup',[],name=n.id)
  if isinstance(n,ast.Constant):
   need(type(n.value) is str,'WC-LITERAL-TYPE');return add(path,n,'literal',[],literal=n.value)
  if isinstance(n,ast.Attribute):return add(path,n,'attribute lookup',[visit(n.value,path+'.base')],attribute=n.attr)
  if isinstance(n,ast.BinOp):
   need(type(n.op) in (ast.Add,ast.Div),'WC-OPERATOR');a=visit(n.left,path+'.left');b=visit(n.right,path+'.right');return add(path,n,'binary operation',[a,b],operator=type(n.op).__name__)
  if isinstance(n,ast.Call):
   need(not n.keywords and not any(isinstance(a,ast.Starred) for a in n.args),'WC-CALL-SHAPE')
   f=visit(n.func,path+'.callable');args=[visit(a,path+'.arg'+str(i)) for i,a in enumerate(n.args)]
   attempt=add(path+'.attempt',n,'nested call attempt',[f,*args],normal='attempted')
   return add(path+'.return',n,'nested normal return',[attempt])
  need(False,'WC-UNSUPPORTED-EXPRESSION')
 f=visit(call.func,'callable');args=[visit(a,'arg'+str(i)) for i,a in enumerate(call.args)]
 add('call-attempt',call,'write_new call attempt; body excluded',[f,*args],normal='attempted')
 return {'sources':copy.deepcopy(loop['source']['sources']),'call':loc(call),'outer_handler':loc(outer),'callee':loc(callee),'callee_parameters':['p','x'],'owner_lock':oldloc(lock),'destination_bridge':loc(owner.items[0].context_expr),'destination_yield':loc(ys[0]),'stop_before':loc(callee.body[0]),'steps':steps,'order':[s['id'] for s in steps],'normal_outcomes':{s['id']:s['normal_outcome'] for s in steps},'callable_step':f,'arguments':args,
  'language_contract':{'version':'Python3.12 under retained CPython3.12.14 cooperative contract','reference':'https://docs.python.org/3.12/reference/expressions.html','sections':['6.3.4 calls','6.16 evaluation order'],'rules':['Callable then positional arguments, left to right','Binary operands left to right; nested calls evaluate callable and arguments before attempted call and acknowledged normal return'],'limits':'Semantic regions; not observed opcode order, hidden library iteration, hostile-replacement resistance or alternate-interpreter qualification'},
  'continuity':'Explicit continuation and selected invocation/owner/token/error/destination/details/list and source-defined callable/builtin binding continuity; not runtime exclusivity',
  'excluded':['write_new body','open/write/flush/fsync','line175 suppression','line176 rethrow','owner finalization']}

def compile_write_call(launcher,entry,manager,loop,report,cleanup):
 s=write_call_source(launcher,entry,manager,loop,report,cleanup)
 return {'format':'I164-WRITE-CALL-REPLACEMENT-STATIC-1','source':s,'parent_catalogue_sha256':digest((json.dumps(loop,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()),'declarations':[{'id':x['id'],'source':copy.deepcopy(x['source']),'operation':x['operation'],'inputs':copy.deepcopy(x['inputs']),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for x in s['steps']],
  'guard_branches':{'parent':'Validated completed selected loop; original constructor pending; no replacement','continuity':['explicit conditional premise','UNESTABLISHED'],'prefixes':['control absent','control construction and callback completed normally'],'origins':['protected-close','protected-append'],'frontiers':['raise','catchable-interruption','process-termination','unobserved'],'values':'PID, directory count/contents and filename unobserved; no finite bound introduced'},'preserved_relations':['cleanup_loop_exhaustion_correspondence',*loop['preserved_relations']],'runtime_chain':None,'actual_admission':False}

def validate_write_call(launcher,entry,manager,loop,report,cleanup,submitted):
 status_exact_tree(submitted,'WC-CATALOGUE-TYPE');status_typed_same(submitted,compile_write_call(launcher,entry,manager,loop,report,cleanup),'WC-SOURCE-CORRESPONDENCE');return True

def write_call_binding(cat,parent,anchor,session,continuity):
 for v in (cat,parent,anchor,session,continuity):status_exact_tree(v,'WC-BINDING-TYPE')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'WC-CONTINUITY')
 need(parent['kind']=='CONSTRUCTED-CLEANUP-LOOP' and parent['completion']=='normal-cleanup-loop-exhaustion','WC-PARENT-COMPLETION')
 need(all(parent[k] is True for k in ('handler_exit_established','selected_body_complete','ordinary_exhaustion_established','loop_completion_established','terminal_python_exception_in_model')),'WC-PARENT-FLAGS')
 need(parent['replacement_error_in_model'] is None and parent['line174_evaluation_established'] is False,'WC-PARENT-ERROR-FRONTIER')
 error=parent['original_error_pending_in_outer_handler'];scope=parent['scope'];b=parent['binding'];event=parent['events'][-1]
 status_typed_same(parent['last_pending_error_in_model'],error,'WC-PENDING-ORIGINAL');status_typed_same(parent['last_acknowledged_active_caught_error_in_model'],error,'WC-ACTIVE-ORIGINAL');status_typed_same(parent['instance_anchor'],anchor,'WC-INSTANCE')
 status_typed_same(scope['instance'],anchor['instance'],'WC-SCOPE-INSTANCE');status_typed_same(session['instance'],anchor['instance'],'WC-DESTINATION-INSTANCE');need(session['acquisition']==scope['acquisition']==anchor['record']['acquisition'],'WC-ACQUISITION')
 status_typed_same(session['source_owner_lock'],cat['source']['owner_lock'],'WC-DESTINATION-SOURCE');need(type(session['recorded_destination']) is str and session['physical_resolved_destination'] is None,'WC-DESTINATION-ROLE')
 need(event['stage']=='cleanup-loop-complete' and event['outcome']=='normal' and event['id']==scope['invocation']+'/cleanup-loop/cleanup-loop-complete','WC-PARENT-OCCURRENCE')
 for k,v in (('scope',scope),('owner',b['references']['owner']),('token',b['references']['token'])):status_typed_same(event[k],v,'WC-PARENT-'+k)
 need(b['continuity']=='explicit conditional premise' and b['loop']['selected_is_last'] is True,'WC-PARENT-CONTINUITY')
 for k in ('details_role','cleanup_list'):status_typed_same(b[k]['scope'],scope,'WC-DETAILS-SCOPE')
 status_typed_same(parent['cleanup_list_state']['acknowledged_append']['target'],b['cleanup_list'],'WC-CLEANUP-TARGET')
 return {'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'loop_occurrence':copy.deepcopy(event),'references':copy.deepcopy(b['references']),'original_constructor_error':copy.deepcopy(error),'details_role':copy.deepcopy(b['details_role']),'cleanup_list':copy.deepcopy(b['cleanup_list']),
  'destination':{'role':'owner-lock-yielded-dest','symbol':scope['invocation']+'/launcher/dest','scope':copy.deepcopy(scope),'session_binding':copy.deepcopy(session),'bridge':copy.deepcopy(cat['source']['destination_bridge']),'yield':copy.deepcopy(cat['source']['destination_yield']),'physical_resolved_value':None},
  'callable':{'name':'write_new','scope':copy.deepcopy(scope),'source':copy.deepcopy(cat['source']['callee']),'runtime_identity':None},'call_source':copy.deepcopy(cat['source']['call']),'continuity':continuity,'premise':cat['source']['continuity'],'observed_identity':None}

def write_call_projection(cat,case,validated):
 for v in (cat,case,validated):status_exact_tree(v,'WC-EXACT-TYPE')
 keys={'scope','anchor','parent_result','session_binding','binding','outcomes'};need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'WC-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'WC-VALIDATED:'+k)
 p=case['parent_result'];scope=case['scope'];b=case['binding'];s=cat['source'];oo=case['outcomes']
 status_typed_same(scope,p['scope'],'WC-PARENT-SCOPE');status_typed_same(b,write_call_binding(cat,p,case['anchor'],case['session_binding'],b['continuity']),'WC-EXPECTED-BINDING')
 need(type(oo) is list and bool(oo),'WC-OUTCOMES')
 if b['continuity']=='UNESTABLISHED':status_typed_same(oo,[{'stage':s['order'][0],'outcome':'unobserved'}],'WC-UNKNOWN-CONTINUITY')
 events=[];values={};replacement=None;last=None;complete=False
 for i,step in enumerate(s['steps']):
  need(i<len(oo),'WC-MISSING-STEP');r=oo[i];need(type(r) is dict and set(r)=={'stage','outcome'} and type(r['stage']) is str and r['stage']==step['id'],'WC-ORDER')
  last=r['outcome'];need(type(last) is str and last in (step['normal_outcome'],'raise','catchable-interruption','process-termination','unobserved'),'WC-OUTCOME')
  ev={'id':scope['invocation']+'/line174/'+step['id'],'scope':copy.deepcopy(scope),'stage':step['id'],'source':copy.deepcopy(step['source']),'outcome':last,'owner':copy.deepcopy(b['references']['owner']),'token':copy.deepcopy(b['references']['token']),'runtime_frame':None};events.append(ev)
  if last!=step['normal_outcome']:
   if last in ('raise','catchable-interruption'):replacement={'role':'conditional-line174-replacement','reference':ev['id']+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(step['source']),'kind':last,'exact_type':None,'exact_value':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  if step['operation'] not in ('explicit continuation into selected protecting try','nested call attempt','write_new call attempt; body excluded'):
   role=copy.deepcopy(b['destination']) if step.get('name')=='dest' else copy.deepcopy(b['details_role']) if step.get('name')=='details' else copy.deepcopy(b['callable']) if step.get('name')=='write_new' else None
   values[step['id']]={'symbol':ev['id']+'/value','inputs':[{'occurrence':scope['invocation']+'/line174/'+x,'value':values[x]['symbol'] if x in values else None,'kind':'prior result' if x in values else 'prior call attempt'} for x in step['inputs']],'source':copy.deepcopy(step['source']),'literal':step.get('literal'),'value_kind':'source literal str' if 'literal' in step else 'symbolic unobserved result','bound_role':role,'concrete_value':step.get('literal') if 'literal' in step else None,'runtime_identity':None}
  if step['id']=='write:call-attempt':complete=True
 need(len(oo)==len(events),'WC-UNREACHED-STEPS')
 uncertain=last in ('process-termination','unobserved')
 out={'kind':'CONSTRUCTED-WRITE-CALL-REPLACEMENT','scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(case['anchor']),'binding':copy.deepcopy(b),'events':events,'values':values,'completion':'write_new-call-attempt' if complete else last+'-frontier','call_attempt_established':complete,
  'call_arguments':{'p':copy.deepcopy(values.get(s['arguments'][0])),'x':copy.deepcopy(b['details_role'])} if complete else None,
  'original_error_pending_in_outer_handler':copy.deepcopy(p['original_error_pending_in_outer_handler']),'last_pending_error_in_model':copy.deepcopy(replacement or p['last_pending_error_in_model']),'replacement_error_in_model':replacement,'terminal_python_exception_in_model':None if uncertain else True,
  'pid_value':None,'directory_count_value':None,'filename_value':None,'exact_path_value':None,'current_partial_effects':'UNKNOWN at nonnormal frontier; acknowledged semantic values only' if not complete else 'Evaluation acknowledged conditionally; no callee-body effects established',
  'existing_cause_context_suppression':'UNKNOWN; no new exception-chain facts','runtime_chain':None,'runtime_observation':False,'observer_join':None,'physical_reference_identity':None}
 for k in ('retained_cleanup_error_evidence','last_acknowledged_inner_caught_error','last_acknowledged_active_caught_error_in_model','earlier_control_completed_in_model','selected_owner_continuity','failure_origin_region','close_normal_return_completed_in_model','close_itself_failed_established_in_model','managed_close_relation','cleanup_list_state','details_after_predecessor_acknowledged_steps','known_false_flags_preserved','dynamic_details_origins_preserved'):out[k]=copy.deepcopy(p[k])
 for k in ('write_new_body_entry_established','write_new_return_established','file_open_established','file_write_established','file_flush_established','file_fsync_established','failure_file_established','line175_handler_entry_established','line175_suppression_established','final_rethrow_established','owner_finalization_established','managed_local_clear_established','active_removal_established','complete_cleanup_established','normal_overall_return_established','physical_closure_established','durability_established','released_ownership_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission'):out[k]=False
 return out

def validate_write_call_projection(cat,case,validated,submitted):
 status_exact_tree(submitted,'WC-OUTPUT-TYPE');status_typed_same(submitted,write_call_projection(cat,case,validated),'WC-OUTPUT-CORRESPONDENCE');return True
