# Client state forwarding and source-specific detachment. No runtime calls.
def client_state_source(launcher,entry,state,handle,boundary):
 validate_client_handle(launcher,entry,handle['manager_relation'],boundary,handle)
 common=client_handle_source(launcher,entry,handle['manager_relation'])
 lt,ll=_client_locate(launcher);et,el=_client_locate(entry)
 def method(tree,cls,name):
  body=next(n.body for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls) if cls else tree.body
  return next(n for n in body if isinstance(n,ast.FunctionDef) and n.name==name)
 def shape(node,text):
  def norm(n):
   n=copy.deepcopy(n)
   if isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant) and type(n.body[0].value.value) is str:n.body.pop(0)
   return ast.dump(n,include_attributes=False)
  same(norm(node),norm(ast.parse(text).body[0]),'CLIENT-STATE-DEFINING-SHAPE:'+node.name)
 session=method(lt,'ManagedSession','state');client=method(et,'Client','state');data=method(et,None,'_data');dispatch=method(et,None,'_dispatch')
 shape(session,'def state(self): return self.__managed.state()')
 shape(client,"def state(self): return _dispatch(self.__token, 'state', None)")
 shape(data,"""def _data(value):
 if type(value) in (str,int,bool,type(None)): return value
 if type(value) is list: return [_data(v) for v in value]
 if type(value) is dict and all(type(k) is str for k in value): return {k:_data(v) for k,v in value.items()}
 raise RuntimeError('UNSUPPORTED-CLIENT-VALUE')
""")
 key_nodes=[n for n in et.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_STATE_KEYS' for t in n.targets)]
 need(len(key_nodes)==1,'CLIENT-STATE-KEY-SOURCE');kn=key_nodes[0]
 need(isinstance(kn.value,ast.Call) and ast.unparse(kn.value.func)=='frozenset' and len(kn.value.args)==1 and not kn.value.keywords,'CLIENT-STATE-KEY-EXPRESSION')
 keys=ast.literal_eval(kn.value.args[0]);need(type(keys) is tuple and all(type(k) is str for k in keys) and len(keys)==len(set(keys)),'CLIENT-STATE-KEYS')
 same(sorted(keys),sorted(state['inherited_head']['native_template']['type']['object']),'CLIENT-STATE-HEAD-SHAPE')
 same(state['source']['method'],'state','CLIENT-STATE-MANAGER-METHOD');same(state['source']['args'],[],'CLIENT-STATE-MANAGER-ARGS')
 tr=dispatch.body[2];body=tr.body;db=[n for n in data.body if not (isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and type(n.value.value) is str)]
 primitives=[ast.unparse(n) for n in db[0].test.comparators[0].elts]
 same(primitives,['str','int','bool','type(None)'],'CLIENT-STATE-DATA-PRIMITIVES')
 stages={'client-call':el(client.body[0]),'owner-lookup':el(dispatch.body[0]),'owner-guard':el(dispatch.body[1]),'operation-check':el(body[1]),'session-call':el(body[2]),'manager-call':ll(session.body[0]),'session-return':ll(session.body[0]),'state-shape':el(body[3]),'conversion':el(body[4].value),'dispatch-return':el(body[4]),'client-return':el(client.body[0]),'retain-error':el(tr.handlers[0].body[0]),'fixed-failure':copy.deepcopy(common['stages']['fixed-failure'])}
 anchors={n:{**loc(node),'source':{'bytes':len(raw),'sha256':digest(raw)},'ast':ast.dump(node,include_attributes=False)} for n,raw,loc,node in [('session-state',launcher,ll,session),('client-state',entry,el,client),('data',entry,el,data),('state-keys',entry,lambda n:{'site':f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}','expression':ast.get_source_segment(entry.decode(),n),'guards':[],'continuation':[]},kn)]}
 return {'sources':copy.deepcopy(common['sources']),'anchors':anchors,'stages':stages,'common_anchors':{n:copy.deepcopy(common['anchors'][n]) for n in ('session-init','client-init','owner-init','dispatch','fixed-failure','owner-route','general-entry','launcher-error')},
  'operation':client.body[0].value.args[1].value,'packet':ast.literal_eval(client.body[0].value.args[2]),'state_keys':list(keys),'state_shape_guard':ast.unparse(body[3].test),'operation_guard':ast.unparse(body[1].test),
  'state_shape_failure':{'type':body[3].body[0].exc.func.id,'message':body[3].body[0].exc.args[0].value},'operation_failure':{'type':body[1].body[0].exc.func.id,'message':body[1].body[0].exc.args[0].value},
  'data_primitives':['NoneType' if n=='type(None)' else n for n in primitives],
  'data_branches':{'primitive':el(db[0]),'list':el(db[1]),'dict':el(db[2]),'unsupported':el(db[3])},'data_failure':{'type':db[3].exc.func.id,'message':db[3].exc.args[0].value},
  'fixed_failure':copy.deepcopy(common['fixed_failure']),'caught_class':ast.unparse(tr.handlers[0].type),'limits':copy.deepcopy(common['limits'])}

def compile_client_state(launcher,entry,state,handle,boundary):
 source=client_state_source(launcher,entry,state,handle,boundary)
 wanted=['client-state','data-detachment','dispatch-and-failure','owner-routing','launcher-diagnostic-and-evidence'];sites={s['id']:s for s in boundary['sites']}
 for n in wanted:
  need(n in sites,'CLIENT-STATE-BOUNDARY-SITE');pin=source['sources']['launcher' if n.startswith('launcher') else 'entry'];same({k:sites[n]['anchor'][k] for k in pin},pin,'CLIENT-STATE-BOUNDARY-PIN')
 values=['manager-return','session-return','dispatch-result','converted-result','dispatch-return','client-return']
 origins=[state['source']['wrapper_return'],source['stages']['session-return'],source['stages']['session-call'],source['anchors']['data'],source['stages']['dispatch-return'],source['stages']['client-return']]
 return {'format':'I164-CLIENT-STATE-STATIC-1','source':source,'manager_relation':copy.deepcopy(state),'boundary_contract':copy.deepcopy(boundary['contract']),'boundary_sites':[copy.deepcopy(sites[n]) for n in wanted],
  'declarations':[{'id':n,'type':copy.deepcopy(state['inherited_head']['native_template']['type']),'source_origin':copy.deepcopy(o),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n,o in zip(values,origins)],'ordered_hops':values,
  'arguments':[{'from':'Client.state','to':'_dispatch','operation':'state','packet':None,'token':'client.token'},{'from':'_dispatch','to':'ManagedSession.state','args':[]},{'from':'ManagedSession.state','to':'ManagedAuthority.state','args':[]}],
  'reference_edges':copy.deepcopy(handle['reference_edges']),
  'copy_semantics':{'algorithm':'source-recursive exact-type detachment; no memo','containers':'fresh list/dict for EACH visited input path; repeated mutable aliases split, no output mutable alias sharing','keys':'exact str keys in insertion order','primitives':'same exact primitive values/types; no immutable physical-identity observation','cycles':'no finite normal unfolding; no inferred terminal exception class or resource bound','normal_guard':'supported acyclic finite input AND every source continuation returns normally','unsupported_guard':'unsupported exact type or non-str dict key when reached -> source RuntimeError; no user copy/repr hook'},
  'outside_catch_failure_contract':copy.deepcopy(handle['outside_catch_failure_contract']),
  'scope':'request-independent acquisition/context/instance/frontier plus distinct invocation; frontier is not an unobserved call time',
  'runtime_links':None,'physical_alias_observations':None,'complete_repetition_coverage':False,'actual_admission':False}

def validate_client_state(launcher,entry,state,handle,boundary,submitted):
 same(submitted,compile_client_state(launcher,entry,state,handle,boundary),'CLIENT-STATE-SOURCE-CORRESPONDENCE');return True

def data_source_domain(catalogue,value):
 """Source-domain analysis of constructed objects; never calls application _data.
 Domain feasibility is separate from resource/exception/termination outcomes.
 """
 src=catalogue['source'];allowed={'str':str,'int':int,'bool':bool,'NoneType':type(None)};types=tuple(allowed[n] for n in src['data_primitives']);pending=[(value,(),frozenset())];containers=0
 while pending:
  v,path,parents=pending.pop();t=type(v)
  if t in types:continue
  if t not in (list,dict) or t is dict and not all(type(k) is str for k in v):
   return {'normal_return_domain':False,'reason':'unsupported-type-or-dict-key','path':list(path),'source_defined_raise_if_reached':copy.deepcopy(src['data_failure']),'runtime_observation':False}
  if id(v) in parents:return {'normal_return_domain':False,'reason':'cycle-no-finite-normal-unfolding','path':list(path),'source_defined_raise_if_reached':None,'runtime_observation':False}
  containers+=1;anc=parents|{id(v)};children=list(v.items()) if t is dict else list(enumerate(v));pending.extend((x,path+(k,),anc) for k,x in reversed(children))
 return {'normal_return_domain':True,'container_path_occurrences':containers,'resource_completion_established':False,'runtime_observation':False}

def validate_data_detachment(graph):
 """Finite normal-return graph relation. Unlike deepcopy, no input-node memo.
 Symbols are constructed occurrence-local premises, never physical addresses.
 """
 need(type(graph) is dict and set(graph)=={'roots','nodes'},'DATA-GRAPH-FIELDS');roots=graph['roots'];nodes=graph['nodes']
 need(type(roots) is list and len(roots)==2 and type(nodes) is dict and all(type(k) is str and k for k in nodes),'DATA-GRAPH-DOMAIN')
 def edge(e):
  need(type(e) is dict,'DATA-EDGE')
  if set(e)=={'ref'}:need(type(e['ref']) is str and e['ref'] in nodes,'DATA-REFERENCE');return
  need(set(e)=={'atom','value'} and type(e['atom']) is str,'DATA-ATOM');types={'NoneType':type(None),'bool':bool,'int':int,'str':str}
  need(e['atom'] in types and type(e['value']) is types[e['atom']],'DATA-EXACT-PRIMITIVE')
 for n in nodes.values():
  need(type(n) is dict and set(n)=={'kind','items'} and n['kind'] in ('dict','list') and type(n['items']) is list,'DATA-NODE')
  if n['kind']=='dict':
   keys=[]
   for pair in n['items']:need(type(pair) is list and len(pair)==2 and type(pair[0]) is str,'DATA-DICT-ITEM');keys.append(pair[0]);edge(pair[1])
   need(len(keys)==len(set(keys)),'DATA-DUPLICATE-KEY')
  else:
   for e in n['items']:edge(e)
 for e in roots:edge(e)
 input_nodes=set();output_nodes=set();pairs=[];pending=[(roots[0],roots[1],(),frozenset())]
 while pending:
  a,b,path,anc=pending.pop();need(set(a)==set(b),'DATA-EDGE-KIND')
  if 'atom' in a:same(a,b,'DATA-EXACT-ATOM-VALUE');continue
  x,y=a['ref'],b['ref'];need(x not in anc,'DATA-CYCLE-NO-NORMAL-RETURN');need(y not in output_nodes,'DATA-OUTPUT-ALIAS-MEMO-OR-MERGE');input_nodes.add(x);output_nodes.add(y)
  an,bn=nodes[x],nodes[y];need(an['kind']==bn['kind'] and len(an['items'])==len(bn['items']),'DATA-CONTAINER-SHAPE');pairs.append({'path':list(path),'input':x,'output':y,'kind':an['kind']})
  children=[]
  for i,(av,bv) in enumerate(zip(an['items'],bn['items'])):
   if an['kind']=='dict':need(av[0]==bv[0],'DATA-KEY-ORDER');children.append((av[1],bv[1],path+(av[0],),anc|{x}))
   else:children.append((av,bv,path+(i,),anc|{x}))
  pending.extend(reversed(children))
 need(not input_nodes&output_nodes,'DATA-INPUT-OUTPUT-MUTABLE-SHARING');need(input_nodes|output_nodes==set(nodes),'DATA-UNREACHABLE-NODE')
 return {'result':'PASS','container_path_pairs':pairs,'input_distinct_containers':len(input_nodes),'output_container_occurrences':len(output_nodes),'internal_input_aliases_preserved':False,'immutable_identity_established':False,'runtime_observation':False}

def _data_graph_value(graph,root):
 """Decode only after the normal detachment relation has rejected cycles."""
 values={n:({} if v['kind']=='dict' else []) for n,v in graph['nodes'].items()}
 def val(e):return values[e['ref']] if 'ref' in e else e['value']
 for n,v in graph['nodes'].items():
  if v['kind']=='dict':values[n].update((k,val(e)) for k,e in v['items'])
  else:values[n].extend(val(e) for e in v['items'])
 return val(root)

def client_state_projection(catalogue,case,validated):
 """Conditional, source-grounded state path under independent validated premises.
 Neither this pure projector nor a caller-supplied graph admits actual evidence.
 """
 need(type(case) is dict and set(case)=={'occurrence','scope','references','outcomes','manager_case','detachment','callback','cleanup'},'CLIENT-STATE-CASE')
 need(type(validated) is dict and set(validated)=={'scope','state'},'CLIENT-STATE-VALIDATED');same(case['scope'],validated['scope'],'CLIENT-STATE-SCOPE')
 scope=case['scope'];need(type(scope) is dict and set(scope)=={'context','acquisition','instance','frontier','invocation'} and scope['context'] in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'),'CLIENT-STATE-INVOCATION-SCOPE')
 need(type(case['occurrence']) is str and bool(case['occurrence']) and case['occurrence']==scope['invocation'],'CLIENT-STATE-OCCURRENCE')
 refs=case['references'];base={'client','token','owner','session','manager','manager-result','data-result'};required=base|{'client.token','owners[token]','owner.wrapper','session.managed','owner_failed'}
 need(type(refs) is dict and set(refs)==required and type(refs['owner_failed']) is bool,'CLIENT-STATE-REFERENCES')
 for k in base:
  r=refs[k];need(type(r) is dict and set(r)=={'kind','scope','symbol'} and r['kind']==('state-result-reference' if k.endswith('result') else k+'-reference') and type(r['symbol']) is str and bool(r['symbol']),'CLIENT-STATE-REFERENCE-TYPE');same(r['scope'],scope,'CLIENT-STATE-REFERENCE-SCOPE')
 need(refs['manager-result']['symbol']!=refs['data-result']['symbol'],'CLIENT-STATE-DETACHED-REFERENCE')
 for a,b in catalogue['reference_edges']:
  if a=='owners[token]' and refs[a] is None:continue
  same(refs[a],refs[b],'CLIENT-STATE-REFERENCE-EDGE:'+a)
 outcomes=case['outcomes'];need(type(outcomes) is dict,'CLIENT-STATE-OUTCOMES');used=set();events=[];hops=[];args=[];dest=[];original=None;fixed=None;retained=False;completion='pending';manager=None;copy_relation=None;converted=None
 def step(n):
  need(n in outcomes and type(outcomes[n]) is str and outcomes[n] in ('normal','raise','process-termination'),'CLIENT-STATE-STAGE:'+n);used.add(n);v=outcomes[n];events.append({'stage':n,'source':copy.deepcopy(catalogue['source']['stages'][n]),'outcome':v});return v
 def link(n,value,reference):hops.append({'id':case['occurrence']+'/'+n,'declaration':n,'scope':copy.deepcopy(scope),'value':copy.deepcopy(value),'reference':copy.deepcopy(reference),'source':copy.deepcopy(next(d['source_origin'] for d in catalogue['declarations'] if d['id']==n))})
 def fail_fixed():
  nonlocal fixed,completion
  v=step('fixed-failure')
  if v=='normal':fixed=copy.deepcopy(catalogue['source']['fixed_failure']);completion='fixed-client-failure';dest.append({'kind':'fixed-failure','to':'general-client','value':copy.deepcopy(fixed)})
  else:completion='unqualified-escape' if v=='raise' else v
 def prefix(n):
  nonlocal completion
  v=step(n)
  if v!='normal':completion='unqualified-escape' if v=='raise' else v;return False
  return True
 entered=prefix('client-call')
 if entered:args.append({'id':case['occurrence']+'/client-to-dispatch','to':'_dispatch','token':copy.deepcopy(refs['token']),'operation':catalogue['source']['operation'],'packet':catalogue['source']['packet']})
 entered=entered and prefix('owner-lookup') and prefix('owner-guard')
 if entered and (refs['owners[token]'] is None or refs['owner_failed']):fail_fixed()
 elif entered:
  for stage in ('operation-check','session-call','manager-call','session-return','state-shape','conversion','dispatch-return','client-return'):
   v=step(stage)
   if v!='normal':
    if v=='process-termination':completion=v;break
    if stage=='client-return':completion='unqualified-escape';break
    original={'kind':'conditional-exception','origin':stage,'catch_family':catalogue['source']['caught_class'],'exact_type':None,'reference':case['occurrence']+'/error'};break
   if stage=='session-call':args.append({'id':case['occurrence']+'/dispatch-to-session','to':'ManagedSession.state','receiver':copy.deepcopy(refs['session']),'args':[]})
   elif stage=='manager-call':
    mc=case['manager_case'];need(type(mc) is dict and set(mc)=={'outcomes','returned'},'CLIENT-STATE-MANAGER-PREMISE')
    path=state_path_projection(catalogue['manager_relation'],mc['outcomes']);args.append({'id':case['occurrence']+'/session-to-manager','to':'ManagedAuthority.state','receiver':copy.deepcopy(refs['manager']),'args':[]})
    if path['completion']!='normal':
     need(mc['returned'] is None,'CLIENT-STATE-NO-ABRUPT-RETURN');manager={'path':path,'return':None};original={'kind':'manager-escaping-exception','origin':stage,'catch_family':'BaseException','exact_type':None,'reference':case['occurrence']+'/error'};break
    ret=mc['returned'];need(type(ret) is dict,'CLIENT-STATE-MANAGER-RETURN');same(ret['outcomes'],mc['outcomes'],'CLIENT-STATE-MANAGER-OUTCOMES')
    same(ret['live_reference']['scope'],scope,'CLIENT-STATE-LIVE-SCOPE');same(ret['wrapper_return']['reference'],refs['manager-result'],'CLIENT-STATE-MANAGER-REFERENCE')
    manager=state_value_projection(catalogue['manager_relation'],ret,validated['state']);link('manager-return',ret['wrapper_return']['value'],refs['manager-result'])
   elif stage=='session-return':
    need(manager is not None and manager.get('kind')=='CONSTRUCTED-STATE-RETURN','CLIENT-STATE-NORMAL-MANAGER');value=case['manager_case']['returned']['wrapper_return']['value'];link('session-return',value,refs['manager-result']);link('dispatch-result',value,refs['manager-result'])
   elif stage=='state-shape':
    value=case['manager_case']['returned']['wrapper_return']['value'];need(type(value) is dict and set(value)==set(catalogue['source']['state_keys']),'CLIENT-STATE-REQUIRED-SHAPE')
   elif stage=='conversion':
    d=case['detachment'];need(type(d) is dict and set(d)=={'input_reference','output_reference','graph'},'CLIENT-STATE-COPY-PREMISE')
    same(d['input_reference'],refs['manager-result'],'CLIENT-STATE-COPY-INPUT-REFERENCE');same(d['output_reference'],refs['data-result'],'CLIENT-STATE-COPY-OUTPUT-REFERENCE')
    copy_relation=validate_data_detachment(d['graph']);value=_data_graph_value(d['graph'],d['graph']['roots'][0]);converted=_data_graph_value(d['graph'],d['graph']['roots'][1]);state_value_compare(catalogue['manager_relation'],value,validated['state']);state_value_compare(catalogue['manager_relation'],converted,validated['state'])
    need(data_source_domain(catalogue,value)['normal_return_domain'],'CLIENT-STATE-COPY-DOMAIN');link('converted-result',converted,refs['data-result'])
   elif stage=='dispatch-return':need(copy_relation is not None,'CLIENT-STATE-CONVERSION-COMPLETION');link('dispatch-return',converted,refs['data-result'])
   elif stage=='client-return':link('client-return',converted,refs['data-result']);completion='normal';dest.append({'kind':'detached-state-data','to':'general-client','value':copy.deepcopy(converted)})
  if original is not None:
   v=step('retain-error')
   if v=='normal':retained=True;dest.append({'kind':'original-exception-reference','to':'owner.failure','reference':original['reference']});fail_fixed()
   else:retained=None;completion='unqualified-escape' if v=='raise' else v
 if manager is None:need(case['manager_case'] is None,'CLIENT-STATE-UNREACHED-MANAGER')
 if copy_relation is None:need(case['detachment'] is None,'CLIENT-STATE-UNREACHED-COPY')
 need(used==set(outcomes),'CLIENT-STATE-UNREACHED-STAGE')
 callback=case['callback'];cleanup=case['cleanup'];need(callback in ('returns','raises','unobserved'),'CLIENT-STATE-CALLBACK');need(type(cleanup) is dict and set(cleanup)=={'revoke','format','cleanup','write','outer_fail'} and all(v in ('normal','raise','unobserved') for v in cleanup.values()),'CLIENT-STATE-CLEANUP')
 evidence={'original_reraised_to_launcher':None,'reference':None,'explicit_cause':'unobserved','retention':'UNESTABLISHED','bytes':None,'cleanup_obligations':'UNCHANGED','cleanup_premise':'normal means iteration/error-detail handling completed, not every connection closed','active_marker_removal':'UNESTABLISHED'}
 if retained and completion=='fixed-client-failure' and callback!='unobserved':
  if cleanup['revoke']=='normal':
   evidence.update(original_reraised_to_launcher=True,reference=original['reference'],explicit_cause='client_error' if callback=='raises' else None);dest.append({'kind':'original-exception-reference','to':'launcher-existing-error-cleanup','reference':original['reference']})
   if cleanup['format']=='normal' and cleanup['cleanup']=='normal':
    evidence['retention']='existing write returned; durability unestablished' if cleanup['write']=='normal' else 'write failed and suppressed; no record established' if cleanup['write']=='raise' else 'write unobserved'
    if cleanup['write']=='normal':dest.append({'kind':'source-defined-original-error-details','to':'existing-launcher-evidence/failure-*.json','reference':original['reference'],'exact_bytes':None,'observed':False})
   elif cleanup['format']=='raise' or cleanup['cleanup']=='raise':evidence['retention']='formatting/cleanup interrupted; no record established'
   if cleanup['format']!='normal':need(cleanup['cleanup']==cleanup['write']=='unobserved','CLIENT-STATE-UNREACHED-RETENTION')
   elif cleanup['cleanup']!='normal':need(cleanup['write']=='unobserved','CLIENT-STATE-UNREACHED-WRITE')
  else:need(all(cleanup[k]=='unobserved' for k in ('format','cleanup','write','outer_fail')),'CLIENT-STATE-UNREACHED-LAUNCHER')
  completed=cleanup['revoke']=='normal' and (cleanup['format']=='raise' or cleanup['format']=='normal' and (cleanup['cleanup']=='raise' or cleanup['cleanup']=='normal' and cleanup['write']!='unobserved'))
  if not completed:need(cleanup['outer_fail']=='unobserved','CLIENT-STATE-UNREACHED-OUTER')
  elif cleanup['outer_fail']=='normal':dest.append({'kind':'fixed-failure','to':'general-entry-caller','value':copy.deepcopy(catalogue['source']['fixed_failure'])})
 else:need(all(v=='unobserved' for v in cleanup.values()),'CLIENT-STATE-UNSUPPORTED-CLEANUP')
 if completion=='process-termination':need(callback=='unobserved' and all(v=='unobserved' for v in cleanup.values()),'CLIENT-STATE-TERMINATION-CONTINUATION')
 classification=_client_outcome_classification(catalogue,events,completion)
 return {'kind':'CONSTRUCTED-CLIENT-STATE','occurrence':case['occurrence'],'scope':copy.deepcopy(scope),'references':copy.deepcopy(refs),'arguments':args,'manager':copy.deepcopy(manager),'events':events,'hops':hops,'copy_relation':copy_relation,'completion':completion,'original_exception':original,'retained_original':retained,'fixed_client_failure':fixed,'destinations':dest,'evidence_route':evidence,
  'outside_catch_failure':classification['unexpected_raise_outside_dispatch_catch'],'outcome_classification':classification,'prior_owner_failure':{'present':refs['owner_failed'],'resolution_established':False},'runtime_observation':False,'physical_identity_established':False,'request_or_journal_row_required':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False,'outer_continuation':'PARTIAL; abrupt/unrepresented continuation stays unresolved'}

def validate_client_state_projection(catalogue,case,validated,submitted):
 same(submitted,client_state_projection(catalogue,case,validated),'CLIENT-STATE-PROJECTION-CORRESPONDENCE');return True

