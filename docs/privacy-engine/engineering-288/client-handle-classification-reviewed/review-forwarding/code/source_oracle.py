"""Reviewer-owned source/guard oracle. No candidate locator is used."""
import ast,copy,hashlib
def ident(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def basic(text,node):return {'site':f'{node.lineno}:{node.col_offset}:{node.end_lineno}:{node.end_col_offset}:{type(node).__name__}','expression':ast.get_source_segment(text,node)}
def source_index(raw):
 text=raw.decode();tree=ast.parse(raw);locations={}
 def walk(node,guards,prefix):
  if hasattr(node,'lineno'):locations[id(node)]={**basic(text,node),'guards':copy.deepcopy(guards),'continuation':copy.deepcopy(prefix)}
  for field,value in ast.iter_fields(node):
   seq=value if isinstance(value,list) else [value]
   for i,child in enumerate(seq):
    if not isinstance(child,ast.AST):continue
    g=copy.deepcopy(guards);p=copy.deepcopy(prefix)
    if isinstance(node,ast.If):g.append({'kind':'if','test':basic(text,node.test),'arm':field})
    elif isinstance(node,ast.Try):g.append({'kind':'try','region':field,'handlers':[ast.unparse(x.type) for x in node.handlers]})
    elif isinstance(node,ast.ExceptHandler):g.append({'kind':'handler','type':ast.unparse(node.type),'binding':node.name})
    elif isinstance(node,ast.With):g.append({'kind':'with','contexts':[ast.unparse(x.context_expr) for x in node.items]})
    elif isinstance(node,(ast.For,ast.While)):g.append({'kind':type(node).__name__,'source':basic(text,node),'region':field})
    if isinstance(value,list) and isinstance(child,ast.stmt):p.append({'owner':basic(text,node),'region':field,'normal_prefix':[basic(text,x) for x in seq[:i] if isinstance(x,ast.stmt)]})
    if isinstance(child,ast.FunctionDef):walk(child,[],[])
    else:walk(child,g,p)
 for n in tree.body:
  if isinstance(n,ast.FunctionDef):walk(n,[],[])
  elif isinstance(n,ast.ClassDef):
   for f in n.body:
    if isinstance(f,ast.FunctionDef):walk(f,[],[])
 def method(cls,name):
  owner=tree if cls is None else next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls)
  return next(n for n in owner.body if isinstance(n,ast.FunctionDef) and n.name==name)
 return tree,method,lambda n:locations[id(n)]
def clean(node):
 node=copy.deepcopy(node)
 if isinstance(node,ast.FunctionDef) and node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and type(node.body[0].value.value) is str:node.body.pop(0)
 return ast.dump(node,include_attributes=False)
def shape(node,program):assert clean(node)==clean(ast.parse(program).body[0]),ast.unparse(node)
def audit(launcher,entry,manager_raw,cat,manager,boundary):
 lt,lm,ll=source_index(launcher);et,em,el=source_index(entry)
 si,sh=lm('ManagedSession','__init__'),lm('ManagedSession','handle');ci,ch=em('Client','__init__'),em('Client','handle');oi=em('_Owner','__init__');dispatch=em(None,'_dispatch');failure=em(None,'_fail');run=em(None,'_run');general=em(None,'run');launch=lm(None,'_session')
 shape(si,'def __init__(self,managed):self.__managed=managed');shape(sh,'def handle(self,authenticated_packet):return self.__managed.handle(authenticated_packet)')
 shape(ci,'def __init__(self,token):self.__token=token');shape(ch,"def handle(self,authenticated_packet):return _dispatch(self.__token,'handle',authenticated_packet)")
 shape(oi,'def __init__(self,wrapper):\n self.wrapper=wrapper\n self.failure=None')
 shape(dispatch,"""def _dispatch(token,operation,packet):
 owner=_OWNERS.get(token)
 if owner is None or owner.failure is not None:_fail()
 try:
  if operation=='handle':
   if type(packet) is not bytes:raise TypeError('PACKET-BYTES')
   result=owner.wrapper.handle(packet)
   if type(result) is not bytes:raise TypeError('RESPONSE-BYTES')
   return result
  if operation!='state':raise RuntimeError('CLIENT-OPERATION')
  result=owner.wrapper.state()
  if type(result) is not dict or set(result)!=_STATE_KEYS:raise RuntimeError('STATE-SHAPE')
  return _data(result)
 except BaseException as error:owner.failure=error
 _fail()
""")
 shape(failure,"def _fail():raise ClientFailure('MANAGED-OPERATION-UNAVAILABLE; outcome uncertain; no renewed authorization') from None")
 shape(run,"""def _run(launcher,candidate,draft,runtime,destination,client,create,control):
 failed=False
 try:
  with launcher.session(candidate,draft,runtime,destination,create=create) as wrapper:
   owner=_Owner(wrapper);token=object();_OWNERS[token]=owner
   try:
    if control is not None:control(_Control(token))
    try:client(Client(token))
    except BaseException as client_error:
     if owner.failure is not None:raise owner.failure from client_error
     raise
    if owner.failure is not None:raise owner.failure
   finally:_OWNERS.pop(token,None)
 except BaseException:failed=True
 if failed:_fail()
""")
 shape(general,"""def run(candidate,draft,runtime,destination,client,*,create=False):
 failed=False
 try:launcher=_load_launcher()
 except BaseException:failed=True
 if failed:_fail()
 return _run(launcher,candidate,draft,runtime,destination,client,create,None)
""")
 tr=launch.body[-1].body[-1];assert isinstance(tr,ast.Try);handler=tr.handlers[0]
 expected=ast.parse("""try:pass
except BaseException as e:
 details={'error':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'nonexecution_established':False,'new_authorization':False,'cleanup':[]}
 for name,obj in [('raw',raw),('managed',managed)]:
  if obj is not None:
   try:obj.close();details['cleanup'].append([name,'close returned'])
   except BaseException as close_error:details['cleanup'].append([name,type(close_error).__name__,str(close_error)])
 try:write_new(dest/'evidence'/('failure-'+str(os.getpid())+'-'+str(len(list((dest/'evidence').iterdir())))+'.json'),details)
 except BaseException:pass
 raise
""").body[0].handlers[0]
 assert clean(handler)==clean(expected)
 assert [ast.unparse(n) for n in tr.body[-4:]]==['yield ManagedSession(managed)','managed.close()','managed = None',"(dest / 'ACTIVE.json').unlink()"]
 mt=ast.parse(manager_raw);mc=next(n for n in mt.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');mh=next(n for n in mc.body if isinstance(n,ast.FunctionDef) and n.name=='handle');shape(mh,"def handle(self,packet,inject=None):return self._run('handle',packet,inject)")
 dtr=dispatch.body[2];branch=dtr.body[0];dh=dtr.handlers[0];src=cat['source']
 anchors={'session-init':(si,ll,launcher),'session-handle':(sh,ll,launcher),'client-init':(ci,el,entry),'client-handle':(ch,el,entry),'owner-init':(oi,el,entry),'dispatch':(dispatch,el,entry),'fixed-failure':(failure,el,entry),'owner-route':(run,el,entry),'general-entry':(general,el,entry),'launcher-error':(handler,ll,launcher)}
 assert set(src['anchors'])==set(anchors)
 for name,(node,loc,raw) in anchors.items():assert src['anchors'][name]=={**loc(node),'source':ident(raw),'ast':ast.dump(node,include_attributes=False)},name
 stages={'client-call':(ch.body[0],el),'owner-lookup':(dispatch.body[0],el),'owner-guard':(dispatch.body[1],el),'packet-check':(branch.body[0],el),'session-call':(branch.body[1],el),'manager-call':(sh.body[0],ll),'session-return':(sh.body[0],ll),'response-check':(branch.body[2],el),'dispatch-return':(branch.body[3],el),'client-return':(ch.body[0],el),'retain-error':(dh.body[0],el),'fixed-failure':(failure.body[0],el),'owner-route':(run,el),'launcher-error':(handler,ll)}
 assert set(src['stages'])==set(stages)
 for name,(node,loc) in stages.items():assert src['stages'][name]==loc(node),name
 assert src['sources']=={'launcher':ident(launcher),'entry':ident(entry)} and src['operation']=='handle' and src['default_inject'] is None and src['caught_class']=='BaseException'
 assert src['packet_guard']=='type(packet) is not bytes' and src['response_guard']=='type(result) is not bytes'
 assert src['fixed_failure']=={'type':'ClientFailure','message':failure.body[0].exc.args[0].value,'explicit_cause':None,'suppress_context':True}
 assert src['public_methods']==['state','handle']
 assert not any(isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and n.slice.value=='ok' for n in ast.walk(branch))
 assert cat['manager_relation']==manager and cat['boundary_contract']==boundary['contract']
 ds=[x for x in manager['declarations'] if x['id']=='wrapper-return'];assert len(ds)==1
 assert cat['ordered_hops']==['manager-return','session-return','dispatch-result','dispatch-return','client-return']
 assert [x['id'] for x in cat['declarations']]==cat['ordered_hops'][1:]
 for x in cat['declarations']:assert x['type']==ds[0]['type']=='STRING' and x['logical_type']=='exact Python bytes' and x['classification']=='UNKNOWN' and x['ordinal'] is x['multiplicity'] is None
 assert cat['reference_edges']==[['client.token','token'],['owners[token]','owner'],['owner.wrapper','session'],['session.managed','manager']]
 assert cat['arguments']==[{'from':'Client.handle','to':'_dispatch','method':'handle','args':['client token','authenticated_packet']},{'from':'_dispatch','to':'ManagedSession.handle','args':['packet']},{'from':'ManagedSession.handle','to':'ManagedAuthority.handle','args':['authenticated_packet'],'inject':'source default None, not an observed value'}]
 assert cat['runtime_links'] is cat['runtime_call_count'] is None and cat['actual_admission'] is cat['complete_repetition_coverage'] is False
 return {'result':'PASS','source_identities':src['sources'],'programs':{k:ast.get_source_segment(r.decode(),n) for k,(n,_,r) in anchors.items()},'manager_handle':ast.get_source_segment(manager_raw.decode(),mh),'source_guards_and_normal_prefixes_checked':True,'outside_dispatch_catch':['client-call','owner-lookup','owner-guard','client-return','retain-error','fixed-failure'],'caught_calling_region':['packet-check','session-call','manager-call','session-return','response-check','dispatch-return'],'source_types':'Exact bytes on successful client handle; TypeError on every non-exact-byte packet; inject supplied by manager default','no_runtime_execution':True,'normal_error_response_preserved':True,'original_error_route':'owner.failure; _run re-raise on callback return or raise; token revocation before launcher context exit; best-effort original cleanup/evidence; fixed general-entry failure','return_and_destination_limits':'No automatic stdout/stderr/status publication; no introspection or callback-print protection; no observed return chain or failure-file bytes'}
