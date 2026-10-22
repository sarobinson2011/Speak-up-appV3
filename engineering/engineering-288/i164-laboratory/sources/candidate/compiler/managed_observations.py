"""Additive, bounded managed-route observation consumer. Trusted offline tracer,
not deployment attestation. No mutation of runtime or inherited integration."""
import ast,copy,dis,hashlib,json,sys,types
from pathlib import Path
import managed_coverage as mc

def enc(x):return mc.enc(x)
def same(a,b,msg):mc.same(a,b,msg)
def need(v,msg):mc.need(v,msg)
SOURCES={'manager':'compiler/live_connection.py','authority':'support/reference/runtime/authority.py','ingest':'support/code/ingest.py'}
TRACK={'manager':None,'authority':{'__init__','close','handle','sign'},'ingest':{'validate_export'}}
def codes(root):
 out={}
 for tag,path in SOURCES.items():
  raw=(Path(root)/path).read_bytes();c=compile(raw,str(Path(root)/path),'exec',optimize=0)
  def walk(c):
   if c.co_name!='<module>' and (TRACK[tag] is None or c.co_name in TRACK[tag]):
    out[(tag,c.co_qualname)]={'code':c,'ops':{i.offset:i for i in dis.get_instructions(c,show_caches=True)},'source':mc.identity(root,path)}
   for v in c.co_consts:
    if isinstance(v,types.CodeType):walk(v)
  walk(c)
 return out

def value(x):
 if type(x) is bytes:return {'bytes_hex':x.hex()}
 if type(x) in (str,int,bool,float,type(None)):return x
 if type(x) is dict:return {str(k):value(v) for k,v in x.items()}
 if type(x) in (tuple,list):return [value(v) for v in x]
 return {'opaque_type':type(x).__name__}
def snap(frame):
 o=frame.f_locals.get('self');d=getattr(o,'__dict__',{})
 return {'phase':d.get('_phase'),'live':d.get('_live') is not None,'retired':d.get('_retired') is not None,'epoch':d.get('_epoch')}
class Recorder:
 """Read-only trace callback; no writes to observed frames or runtime objects."""
 def __init__(self,root):self.spec=codes(root);self.events=[];self.ids={};self.next=1
 def __call__(self,f,event,arg):
  if event not in ('call','line','return','exception'):return self
  keys=[k for k,v in self.spec.items() if k[1]==f.f_code.co_qualname and v['code'].co_code==f.f_code.co_code and v['code'].co_firstlineno==f.f_code.co_firstlineno]
  if len(keys)!=1:return self
  key=keys[0]
  if event=='call':self.ids[id(f)]=self.next;self.next+=1
  if id(f) not in self.ids:return self
  p=f.f_back
  while p is not None and id(p) not in self.ids:p=p.f_back
  row={'seq':len(self.events),'frame':self.ids[id(f)],'parent':None if p is None else self.ids[id(p)],'source':key[0],'function':key[1],'event':event,'offset':f.f_lasti,'line':f.f_lineno,'state':snap(f)}
  if event=='call':row['arguments']={k:value(v) for k,v in f.f_locals.items() if k not in ('self','root','path','ownership_path','a')}
  if event=='return':row['value']=value(arg)
  if event=='exception':row['exception']={'type':arg[0].__name__,'message':str(arg[1])}
  self.events.append(row)
  if event=='return':del self.ids[id(f)]
  return self

def trace_check(root,events):
 need(sys.version_info[:3]==(3,12,14) and sys.flags.optimize==0,'INTERPRETER')
 spec=codes(root);stack=[];frames={}
 for n,e in enumerate(events):
  need(type(e['seq']) is int and e['seq']==n,'EVENT-ORDER')
  expected={'seq','frame','parent','source','function','event','offset','line','state'}|({'arguments'} if e['event']=='call' else {'value'} if e['event']=='return' else {'exception'} if e['event']=='exception' else set())
  need(set(e)==expected,'EVENT-FIELDS');st=e['state'];need(set(st)=={'phase','live','retired','epoch'} and type(st['live']) is bool and type(st['retired']) is bool and (st['epoch'] is None or type(st['epoch']) is int),'STATE-TYPES')
  need(st['phase'] in (None,'CLOSED','READY','QUARANTINED','CLEANUP_UNCERTAIN','OPEN_FAILED','VALIDATION_FAILED'),'PHASE-TYPE')
  key=(e['source'],e['function']);need(key in spec,'EVENT-SOURCE')
  c=spec[key];need(type(e['offset']) is int and e['offset'] in c['ops'],'EVENT-OFFSET');i=c['ops'][e['offset']]
  need(i.positions.lineno==e['line'] or e['event']=='call' and e['line']==c['code'].co_firstlineno,'EVENT-LINE')
  if e['event']=='call':
   need(e['frame'] not in frames and e['parent']==(stack[-1] if stack else None),'FRAME-ANCESTRY');stack.append(e['frame']);frames[e['frame']]={'call':e,'events':[e]}
  else:
   need(stack and e['frame']==stack[-1] and e['parent']==(stack[-2] if len(stack)>1 else None),'FRAME-ORDER');frames[e['frame']]['events'].append(e)
   same((e['source'],e['function']),(frames[e['frame']]['call']['source'],frames[e['frame']]['call']['function']),'FRAME-SOURCE-IDENTITY')
   need(e['event'] in ('line','exception','return'),'EVENT-KIND')
   if e['event']=='return':
    frames[e['frame']]['return']=e;frames[e['frame']]['normal']=i.opname in ('RETURN_VALUE','RETURN_CONST');stack.pop()
 need(not stack and bool(frames),'INCOMPLETE-TRACE')
 # Source guard is independently derived, not supplied by observation labels.
 raw=(Path(root)/SOURCES['manager']).read_bytes();tree=ast.parse(raw)
 req=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='_require')
 same(ast.unparse(req.body[0].test),"self._phase != 'READY' or self._live is None or self._retired is not None",'UNSUPPORTED-GUARD-SOURCE')
 for f in frames.values():
  e=f['call'];s=e['state'];name=e['function'].split('.')[-1]
  errors=[v['exception'] for v in f['events'] if v['event']=='exception']
  for error in errors:need(set(error)=={'type','message'} and type(error['type']) is str and type(error['message']) is str,'EXCEPTION-TYPE')
  if not f['normal']:need(bool(errors) and f['return']['value'] is None,'UNWIND-WITHOUT-EXCEPTION')
  if e['source']=='manager' and name=='_quarantine' and e['parent'] is not None:
   parent=frames[e['parent']];prior=[v['exception'] for v in parent['events'] if v['event']=='exception' and v['seq']<e['seq']]
   if parent['call']['function']=='ManagedAuthority._run':
    need(bool(prior),'QUARANTINE-WITHOUT-ERROR');same(e['arguments']['reason'],prior[-1]['type']+':'+prior[-1]['message'],'QUARANTINE-ERROR-BINDING')
  if e['source']=='manager' and name=='_require':
   allowed=s['phase']=='READY' and s['live'] and not s['retired'];need(f['normal']==allowed,'REQUIRE-GUARD')
  if e['source']=='manager' and name=='_quarantine' and f['normal']:
   out=f['return']['state'];need(out['phase']=='QUARANTINED' and not out['live'] and (not s['live'] or out['retired']),'QUARANTINE-TRANSFER')
  if e['source']=='manager' and name=='_run':
   children=[v for v in frames.values() if v['call']['parent']==e['frame']]
   guards=[v for v in children if v['call']['function']=='ManagedAuthority._require'];need(len(guards)==1,'MISSING-ENTRY-GUARD')
   backend=[v for v in children if v['call']['source']=='authority']
   if not guards[0]['normal']:need(not backend,'DISPATCH-WHILE-BLOCKED')
   if f['normal']:
    need(guards[0]['normal'],'RUN-BYPASS');need(f['return']['state']['phase']=='READY','NORMAL-PHASE')
   elif guards[0]['normal']:
    need(any(v['call']['function']=='ManagedAuthority._quarantine' for v in children),'MISSING-QUARANTINE');need(f['return']['state']['phase']=='QUARANTINED','FAILED-RUN-PHASE')
  if e['source']=='manager' and name=='recover' and f['normal']:
   children=[v for v in frames.values() if v['call']['parent']==e['frame']]
   validators=[v for v in children if v['call']['function']=='ManagedAuthority._validate']
   need(len(validators)==1 and validators[0]['normal'],'RECOVERY-VALIDATION')
   ingest=[v for v in frames.values() if v['call']['parent']==validators[0]['call']['frame'] and v['call']['function']=='validate_export']
   need(len(ingest)==1 and ingest[0]['normal'],'RECOVERY-INGEST')
   s2=f['return']['state'];need(s2=={'phase':'READY','live':True,'retired':False,'epoch':s['epoch']+1},'RECOVERY-PUBLISH')
   ret=f['return']['value'];need(ret['recovery_only'] is True and ret['new_attempt_authorized'] is False,'RECOVERY-AUTHORIZATION')
  if e['source']=='manager' and name=='_dispose':
   closes=[v for v in frames.values() if v['call']['parent']==e['frame'] and v['call']['function']=='Authority.close']
   if s['retired']:
    need(len(closes)==1,'MISSING-CLOSE-CALL')
    if f['normal']:need(closes[0]['normal'] and f['return']['state']['retired'] is False,'UNCONFIRMED-CLOSE')
    else:need(f['return']['state']['phase']=='CLEANUP_UNCERTAIN' and f['return']['state']['retired'],'UNCERTAIN-CLOSE-LOST')
 completion_check(frames,spec)
 source_edges(root,frames,spec)
 fixed_status(root,frames)
 return frames

def source_edges(root,frames,spec):
 """Current trace edges, derived from pinned producer AST and executable spans.
 No submitted expectation list, capture whitelist or previously validated object.
 Structural observations remain trusted-tracer evidence, not attestation.
 """
 for path in (SOURCES['manager'],SOURCES['authority']):
  same(mc.identity(root,path),mc.PINS[path],'EDGE-SOURCE-PIN')
 tree=ast.parse((Path(root)/SOURCES['manager']).read_bytes())
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority')
 methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
 opening=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='open_session')
 auth=ast.parse((Path(root)/SOURCES['authority']).read_bytes())
 ac=next(n for n in auth.body if isinstance(n,ast.ClassDef) and n.name=='Authority')
 am={n.name:n for n in ac.body if isinstance(n,ast.FunctionDef)}
 def children(f,fn=None):
  a=[v for v in frames.values() if v['call']['parent']==f['call']['frame']]
  return a if fn is None else [v for v in a if v['call']['function']==fn]
 def one(f,fn):
  a=children(f,fn);need(len(a)==1,'REQUIRED-CALL:'+fn);return a[0]
 def argument_names(node):
  a=node.args
  return {v.arg for v in a.posonlyargs+a.args+a.kwonlyargs}|({a.vararg.arg} if a.vararg else set())|({a.kwarg.arg} if a.kwarg else set())
 def errors(f):return [e for e in f['events'] if e['event']=='exception']
 def propagate(parent,child):
  need(parent['normal']==child['normal'],'WRAPPER-COMPLETION')
  if parent['normal']:same(parent['return']['value'],child['return']['value'],'RETURN-EDGE')
  else:
   need(errors(parent) and errors(child),'MISSING-EDGE-EXCEPTION')
   same(errors(parent)[-1]['exception'],errors(child)[-1]['exception'],'EXCEPTION-EDGE')
 def before(a,b):need(a['return']['seq']<b['call']['seq'],'CALL-EDGE-ORDER')
 def ast_call(node,text):
  a=[n for n in ast.walk(node) if isinstance(n,ast.Call) and ast.unparse(n.func)==text]
  need(len(a)==1,'UNSUPPORTED-CALL-SOURCE:'+text);return a[0]
 def at_call(event,node,code):
  # CPython 3.12.14 reports caller exceptions at CALL or at one of that
  # instruction's inline caches. Attribute only its contiguous cache run;
  # CACHE belonging to any other instruction is not a call-site observation.
  ops=code['ops'];offset=event['offset'];i=ops[offset]
  if i.opname=='CACHE':
   ordered=list(ops);k=ordered.index(offset)
   while k>=0 and ops[ordered[k]].opname=='CACHE':k-=1
   if k<0:return False
   i=ops[ordered[k]]
  p=i.positions
  return i.opname.startswith('CALL') and (p.lineno,p.end_lineno,p.col_offset,p.end_col_offset)==(node.lineno,node.end_lineno,node.col_offset,node.end_col_offset)
 # Formal argument sets come from defining functions and the unchanged recorder
 # exclusion contract. Excluded filesystem/object arguments are NOT observed.
 excluded={'self','root','path','ownership_path','a'}
 for f in frames.values():
  e=f['call'];node=None
  if e['source']=='manager':node=opening if e['function']=='open_session' else methods.get(e['function'].split('.')[-1])
  elif e['source']=='authority' and e['function'].startswith('Authority.'):node=am.get(e['function'].split('.')[-1])
  if node is not None:
   need(type(e['arguments']) is dict and set(e['arguments'])==argument_names(node)-excluded,'CALL-ARGUMENT-FIELDS')
  if f['normal']:
   i=spec[(e['source'],e['function'])]['ops'][f['return']['offset']]
   if i.opname=='RETURN_CONST':same(f['return']['value'],value(i.argval),'CONSTANT-RETURN')
 # Derive wrapper methods, constant dispatch selection and forwarded parameters.
 wrappers={}
 for name,node in methods.items():
  if len(node.body)==1 and isinstance(node.body[0],ast.Return) and isinstance(node.body[0].value,ast.Call):
   call=node.body[0].value
   if ast.unparse(call.func)=='self._run':
    need(not call.keywords and isinstance(call.args[0],ast.Constant) and type(call.args[0].value) is str and all(isinstance(a,ast.Name) for a in call.args[1:]),'UNSUPPORTED-WRAPPER-SOURCE')
    wrappers[name]=(call.args[0].value,[a.id for a in call.args[1:]])
 dispatch=ast_call(methods['_run'],'getattr(self._live, method)')
 same(ast.unparse(dispatch),'getattr(self._live, method)(*args)','UNSUPPORTED-DISPATCH-SOURCE')
 for f in frames.values():
  e=f['call'];name=e['function']
  if e['source']=='manager' and name.split('.')[-1] in wrappers:
   selected,params=wrappers[name.split('.')[-1]];run=one(f,'ManagedAuthority._run')
   same(run['call']['arguments'],{'method':selected,'args':[e['arguments'][p] for p in params]},'DISPATCH-WRAPPER-ARGUMENTS')
   propagate(f,run)
  if name=='ManagedAuthority._run':
   parent=frames.get(e['parent']);need(parent is not None and parent['call']['function'].split('.')[-1] in wrappers and parent['call']['source']=='manager','UNSUPPORTED-DISPATCH-CALLER')
   args=e['arguments'];method=args['method'];need(type(args['args']) is list and method in am,'DISPATCH-TYPE')
   guard=one(f,'ManagedAuthority._require')
   back=[v for v in children(f) if v['call']['source']=='authority']
   # state is not tracked by the retained recorder; only wrapper/run return
   # equality can be claimed there. handle is tracked and cannot disappear.
   if method in TRACK['authority']:
    need(len(back)<=1,'DUPLICATE-DISPATCH')
    if guard['normal'] and (f['normal'] or any(at_call(v,dispatch,spec[('manager',name)]) for v in errors(f))):need(len(back)==1,'MISSING-DISPATCH')
    if back:
     b=back[0];need(b['call']['function']=='Authority.'+method and guard['normal'],'DISPATCH-FUNCTION');before(guard,b)
     prior=[v for v in f['events'] if v['event']=='line' and v['seq']<b['call']['seq']]
     need(prior and prior[-1]['line']==dispatch.lineno,'DISPATCH-CALL-SITE')
     params=[p.arg for p in am[method].args.args if p.arg!='self'];need(len(params)==len(args['args']),'DISPATCH-ARITY')
     same(b['call']['arguments'],dict(zip(params,args['args'])),'DISPATCH-ARGUMENTS')
     if f['normal']:
      need(b['normal'],'DISPATCH-UNWIND-AS-RETURN');same(f['return']['value'],b['return']['value'],'BACKEND-RETURN-EDGE')
     if not b['normal']:
      need(not f['normal'] and errors(f) and errors(b),'DISPATCH-EXCEPTION-MISSING')
      same(errors(f)[0]['exception'],errors(b)[-1]['exception'],'DISPATCH-EXCEPTION-EDGE')
   else:need(not back,'UNTRACKED-METHOD-WITH-TRACKED-BACKEND')
 # A normal Authority.handle result is source-produced canonical signed bytes,
 # never None. Verify its request/challenge association independently of jointly
 # editable wrapper/run return fields. Authentication is laboratory scoped.
 handle=am['handle'];returns=[n for n in ast.walk(handle) if isinstance(n,ast.Return)]
 same([ast.unparse(n.value) for n in returns],['raw'],'UNSUPPORTED-HANDLE-RETURN')
 assigned=[n for n in ast.walk(handle) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='raw' for t in n.targets)]
 same([ast.unparse(n.value) for n in assigned],["enc({'response': response, 'signature': sig('server', response)})"],'UNSUPPORTED-RESPONSE-PRODUCER')
 version=next(ast.literal_eval(n.value) for n in auth.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='VERSION' for t in n.targets))
 keypath='support/reference/public-keys.json'
 keybytes=(Path(root)/keypath).read_bytes()
 keypin=json.loads((Path(root)/'provenance/layout-runtime-members.json').read_bytes())[keypath]
 same({'bytes':len(keybytes),'sha256':mc.digest(keybytes)},keypin,'RESPONSE-KEY-SOURCE')
 pub=json.loads(keybytes)
 def exact_bytes(v):
  need(type(v) is dict and set(v)=={'bytes_hex'} and type(v['bytes_hex']) is str,'RETURN-BYTES-TYPE')
  b=bytes.fromhex(v['bytes_hex']);need(b.hex()==v['bytes_hex'],'RETURN-HEX');return b
 def decode(b):
  v=json.loads(b);need(enc(v)==b,'ENVELOPE-CANONICAL');return v
 def signature(role,obj,sig):
  from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
  need(type(sig) is str and len(sig)==128,'ENVELOPE-SIGNATURE-TYPE')
  Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub[role])).verify(bytes.fromhex(sig),version.encode()+b'\0'+enc(obj))
 for f in frames.values():
  if f['call']['function']=='Authority.handle' and f['normal']:
   packet=exact_bytes(f['call']['arguments']['packet']);q=decode(packet)
   need(type(q) is dict and set(q)=={'request','signature'},'REQUEST-ENVELOPE')
   request=q['request'];signature(request['principal'],request,q['signature'])
   response=decode(exact_bytes(f['return']['value']))
   need(type(response) is dict and set(response)=={'response','signature'},'RETURN-ENVELOPE')
   r=response['response'];need(type(r) is dict and type(r.get('ok')) is bool,'RETURN-ENVELOPE-TYPE')
   need(set(r)=={'request','challenge','ok',('data' if r['ok'] else 'error')},'RETURN-ENVELOPE-FIELDS')
   same(r['request'],mc.digest(packet),'RETURN-REQUEST');same(r['challenge'],request['challenge'],'RETURN-CHALLENGE')
   signature('server',r,response['signature'])
 # recover's constructor call and ordering are derived independently of events.
 ctor=ast_call(methods['recover'],'self._runtime.Authority.__init__')
 same(ast.unparse(ctor),'self._runtime.Authority.__init__(a, self._path, copy.deepcopy(self._config), ownership_path=self._owners)','UNSUPPORTED-CONSTRUCTOR-SOURCE')
 validate_call=ast_call(methods['recover'],'self._validate')
 need(ctor.lineno<validate_call.lineno,'UNSUPPORTED-CONSTRUCTION-ORDER')
 defaults=dict(zip([a.arg for a in am['__init__'].args.args][-len(am['__init__'].args.defaults):],am['__init__'].args.defaults))
 create=ast.literal_eval(defaults['create'])
 configs=[f['call']['arguments']['config'] for f in frames.values() if f['call']['function']=='ManagedAuthority.__init__']
 need(bool(configs),'MISSING-MANAGED-CONFIG')
 for config in configs[1:]:same(config,configs[0],'MIXED-CONSTRUCTION-CONFIG')
 for f in frames.values():
  e=f['call'];name=e['function']
  if name=='open_session':
   init=one(f,'ManagedAuthority.__init__');same(init['call']['arguments'],e['arguments'],'ENTRY-CONFIG')
   rec=children(f,'ManagedAuthority.recover')
   if f['normal']:need(init['normal'] and len(rec)==1 and rec[0]['normal'],'ENTRY-CONSTRUCTION')
   if rec:need(init['normal'] and len(rec)==1,'ENTRY-FAILED-INITIALIZATION');before(init,rec[0])
  if name=='Authority.__init__':
   need(e['parent'] in frames and frames[e['parent']]['call']['function']=='ManagedAuthority.recover','CONSTRUCTOR-CALLER')
   same(e['arguments'],{'config':configs[0],'create':create},'CONSTRUCTOR-ARGUMENTS')
   if f['normal']:same(f['return']['value'],None,'CONSTRUCTOR-RETURN')
  if name=='ManagedAuthority.recover':
   ct=children(f,'Authority.__init__');va=children(f,'ManagedAuthority._validate');di=children(f,'ManagedAuthority._dispose')
   need(len(ct)<=1 and len(va)<=1,'DUPLICATE-RECOVERY-CALL')
   invoked=f['normal'] or bool(va) or any(at_call(v,ctor,spec[('manager',name)]) for v in errors(f))
   if invoked:need(len(ct)==1,'MISSING-CONSTRUCTOR')
   if ct:
    following=[v for v in f['events'] if v['seq']>ct[0]['return']['seq']]
    if following and following[0]['event']=='exception':
     need(at_call(following[0],ctor,spec[('manager',name)]),'CONSTRUCTOR-PARENT-EXCEPTION-SITE')
    parent_errors=[v for v in errors(f) if at_call(v,ctor,spec[('manager',name)])]
    if not ct[0]['normal']:need(bool(parent_errors),'CONSTRUCTOR-PROPAGATION-MISSING')
    for error in parent_errors:
     child=ct[0]
     need(child['return']['seq']<error['seq'],'CONSTRUCTOR-EXCEPTION-ORDER')
     need(not child['normal'],'CONSTRUCTOR-CALL-EXCEPTION-AS-SUCCESS')
     child_errors=errors(child);need(bool(child_errors),'CONSTRUCTOR-EXCEPTION-EVIDENCE-MISSING')
     same(error['exception'],child_errors[-1]['exception'],'CONSTRUCTOR-EXCEPTION-EDGE')
    need(di and di[0]['normal'],'MISSING-PREOPEN-DISPOSAL');before(di[0],ct[0])
    # A constructor invocation must occur on its source line, after disposal.
    prior=[v for v in f['events'] if v['seq']<ct[0]['call']['seq'] and v['event']=='line']
    need(prior and prior[-1]['line']==ctor.lineno,'CONSTRUCTOR-CALL-SITE')
    if not ct[0]['normal']:
     need(not va and not f['normal'],'FAILED-CONSTRUCTION-PUBLISHED')
     need(errors(f) and errors(ct[0]),'CONSTRUCTOR-EXCEPTION-MISSING')
     same(errors(f)[0]['exception'],errors(ct[0])[-1]['exception'],'CONSTRUCTOR-EXCEPTION-EDGE')
   if ct and ct[0]['normal'] and any(at_call(v,validate_call,spec[('manager',name)]) for v in errors(f)):
    need(len(va)==1,'MISSING-RECOVERY-VALIDATOR')
   if va:
    need(ct and ct[0]['normal'],'VALIDATE-BEFORE-CONSTRUCT');before(ct[0],va[0])
   if f['normal']:
    need(ct and ct[0]['normal'] and va and va[0]['normal'],'RECOVERY-CONSTRUCTION-COMPLETION')
    same(f['return']['value']['head'],va[0]['return']['value'],'RECOVERY-HEAD-RETURN')
   else:
    need(f['return']['state']['phase']!='READY','FAILED-RECOVERY-PUBLISHED')
    same(f['return']['state']['epoch'],e['state']['epoch'],'FAILED-RECOVERY-EPOCH')
    # With no constructor evidence, only source-established pre-call failures
    # are supported, not successful or unknown/ambiguous construction.
    if not ct:
     early=[v for v in errors(f) if v['line']<ctor.lineno]
     need(early,'UNOBSERVED-CONSTRUCTION-UNRESOLVED')
  if name=='ManagedAuthority._validate' and f['normal']:
   ing=one(f,'validate_export');need(ing['normal'],'VALIDATION-UNWIND')
   same(f['return']['value'],ing['call']['arguments']['x']['expected_head'],'VALIDATION-HEAD')

def completion_check(frames,spec):
 """CPython 3.12.14 synchronous trace exception edges, no witness offsets.
 An exception with no applicable handler exits the frame; it cannot flow to
 a normal-return opcode. A caught exception must exhibit a possible handler
 continuation. This is structural reachability, not arbitrary path coverage.
 """
 for f in frames.values():
  c=spec[(f['call']['source'],f['call']['function'])]['code']
  need(not c.co_flags & (0x20|0x80|0x200),'UNSUPPORTED-SUSPENDING-FRAME')
  ops=list(dis.get_instructions(c,show_caches=True));by={v.offset:v for v in ops};nextop={a.offset:b.offset for a,b in zip(ops,ops[1:])}
  entries=list(dis.Bytecode(c).exception_entries)
  def reachable(start,target):
   todo=[start];seen=set()
   while todo:
    off=todo.pop()
    if off==target:return True
    if off in seen or off not in by:continue
    seen.add(off);i=by[off]
    if i.opname in ('RETURN_VALUE','RETURN_CONST','RAISE_VARARGS','RERAISE'):continue
    jump=i.opcode in dis.hasjabs or i.opcode in dis.hasjrel
    if jump:todo.append(i.argval)
    if not jump or 'IF' in i.opname or i.opname in ('FOR_ITER','SEND'):
     if off in nextop:todo.append(nextop[off])
   return False
  events=f['events']
  for j,e in enumerate(events):
   if e['event']!='exception':continue
   handler=next((v for v in entries if v.start<=e['offset']<v.end),None)
   following=events[j+1:]
   need(bool(following),'EXCEPTION-COMPLETION-MISSING')
   if handler is None:
    need(not f['normal'] and len(following)==1 and following[0]['event']=='return','UNHANDLED-EXCEPTION-AS-NORMAL')
    same(following[0]['offset'],e['offset'],'UNHANDLED-EXCEPTION-RETURN-SITE')
   else:
    nxt=following[0]
    if nxt['event']!='return' or f['normal']:
     need(reachable(handler.target,nxt['offset']),'UNSUPPORTED-HANDLER-CONTINUATION')

def fixed_status(root,frames):
 tree=ast.parse((Path(root)/SOURCES['manager']).read_bytes())
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority')
 methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
 node=methods['status'];returns=[n for n in ast.walk(node) if isinstance(n,ast.Return)]
 need(len(returns)==1 and isinstance(returns[0].value,ast.Dict),'UNSUPPORTED-STATUS-SOURCE')
 fields={ast.literal_eval(k):v for k,v in zip(returns[0].value.keys,returns[0].value.values)}
 dynamic={'self._phase':'phase','self._epoch':'epoch','self._reason':None}
 for f in frames.values():
  if f['call']['function']=='ManagedAuthority.status' and f['normal']:
   ret=f['return']['value'];need(type(ret) is dict and set(ret)==set(fields),'STATUS-FIELDS')
   for key,expr in fields.items():
    if isinstance(expr,ast.Constant):same(ret[key],expr.value,'STATUS-SOURCE-CONSTANT:'+key)
    else:
     selector=ast.unparse(expr);need(selector in dynamic,'UNSUPPORTED-STATUS-EXPRESSION')
     if dynamic[selector] is not None:same(ret[key],f['return']['state'][dynamic[selector]],'STATUS-STATE:'+key)
     else:need(type(ret[key]) is str,'STATUS-REASON-TYPE')
  if f['call']['function']=='ManagedAuthority.recover' and f['normal']:
   statuses=[g for g in frames.values() if g['call']['parent']==f['call']['frame'] and g['call']['function']=='ManagedAuthority.status']
   need(len(statuses)==1 and statuses[0]['normal'],'RECOVERY-STATUS-CALL')
   same(f['return']['value']['status'],statuses[0]['return']['value'],'RECOVERY-STATUS-EDGE')

def authenticated_recovery(frames,record,ingest):
 """Re-ingest actual recorded arguments, independently of claimed outcomes.
 Bind each recovery export to the authenticated enclosing history interval.
 No failure label or mutually edited expected_head can supply an anchor.
 """
 before=record['before'];after=record['after']
 for f in frames.values():
  if f['call']['function']!='validate_export':continue
  parent=frames.get(f['call']['parent']);need(parent is not None and parent['call']['function']=='ManagedAuthority._validate','RECOVERY-INGEST-CALLER')
  x=f['call']['arguments']['x']
  try:actual=ingest.validate_export(x)
  except Exception as error:
   need(not f['normal'],'INVALID-RECOVERY-EXPORT-AS-SUCCESS')
   observed=[e['exception'] for e in f['events'] if e['event']=='exception']
   need(observed,'RECOVERY-INGEST-EXCEPTION-MISSING')
   same(observed[-1],{'type':type(error).__name__,'message':str(error)},'RECOVERY-INGEST-EXCEPTION')
   need(not parent['normal'],'FAILED-INGEST-AS-VALIDATED')
   # Failed evidence has no validated-head claim or authority to publish READY.
   continue
  need(f['normal'],'VALID-RECOVERY-EXPORT-MISLABELED')
  same(f['return']['value'],actual,'RECOVERY-INGEST-RETURN')
  same(x['config'],before['config'],'RECOVERY-CONFIG-ANCHOR')
  same(x['ownership_meta'],before['ownership_meta'],'RECOVERY-OWNER-ANCHOR')
  same(x['owners'],before['owners'],'RECOVERY-OWNERS-ANCHOR');same(x['blobs'],before['blobs'],'RECOVERY-BLOBS-ANCHOR')
  need(len(before['events'])<=len(x['events'])<=len(after['events']),'RECOVERY-HISTORY-INTERVAL')
  same(x['events'],after['events'][:len(x['events'])],'RECOVERY-HISTORY-ANCHOR')
  # In this retained head/sign-claim domain, the exact HEAD at each sequence is
  # determined by the authenticated before image or the corresponding EVENT.
  if len(x['events'])==len(before['events']):expected_head=before['head']
  else:
   raw=bytes.fromhex(x['events'][-1][1]);event=json.loads(raw)
   expected_head=enc(dict(event['after'],head=mc.digest(raw))).hex()
  same(x['head'],expected_head,'RECOVERY-EXACT-HEAD-ANCHOR')
  same(x['expected_head'],json.loads(bytes.fromhex(expected_head))['head'],'RECOVERY-HEAD-ANCHOR')
  # A snapshot cannot include requests that have not reached the backend yet.
  completed=[g for g in frames.values() if g['call']['function']=='Authority.handle' and g['return']['seq']<f['call']['seq']]
  rows={r[0]:r for r in before['journal']}
  afterrows={r[0]:r for r in after['journal']}
  for g in completed:
   packet=bytes.fromhex(g['call']['arguments']['packet']['bytes_hex']);challenge=json.loads(packet)['request']['challenge']
   need(challenge in afterrows,'RECOVERY-REQUEST-ANCHOR');rows[challenge]=afterrows[challenge]
  same(x['journal'],[rows[k] for k in sorted(rows)],'RECOVERY-JOURNAL-FRONTIER')
  if parent['normal']:same(parent['return']['value'],x['expected_head'],'VALIDATED-HEAD-RETURN')

def validate(root,bundle,record,context,runtime_root):
 mc.validate_bundle(root,bundle)
 need(Path(root).resolve()==Path(runtime_root).resolve(),'LAYOUT-COMBINED-ROOT-REQUIRED')
 need(record.get('format')=='I164-MANAGED-OCCURRENCE-LAYOUT-2','LAYOUT-OBSERVATION-VERSION')
 need(context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'),'CONTEXT');same(record['context'],context,'MIXED-CONTEXT')
 same(record['sources'],{k:mc.identity(root,v) for k,v in SOURCES.items()},'STALE-SOURCES')
 same(record['inputs'],{k:mc.identity(root,v) for k,v in mc.FILES.items()},'STALE-INTEGRATION')
 need(record['interpreter']=={'version':sys.version,'optimize':sys.flags.optimize} and sys.version_info[:3]==(3,12,14) and sys.flags.optimize==0,'INTERPRETER')
 same(record['boundary'],mc.BOUNDARY,'BOUNDARY');same(record['limits'],mc.LIMITS,'ESCALATION');same(record['obligations'],mc.OBLIGATIONS,'OBLIGATION-DISCHARGE')
 need(record['evidence_class']=='ACTUAL-OFFLINE-MANAGED-EXECUTION','EVIDENCE-CLASS')
 frames=trace_check(root,record['events'])
 # Current combined-layout member identities; prior two-root records must use
 # their exact predecessor consumer, not this version.
 for path,ident in json.loads((Path(__file__).resolve().parents[1]/'provenance/layout-runtime-members.json').read_bytes()).items():
  raw=(Path(runtime_root)/path).read_bytes();same({'bytes':len(raw),'sha256':mc.digest(raw)},ident,'RUNTIME-MEMBER:'+path)
 import value_flow as vf;vf.s.setup(Path(runtime_root));import ingest
 ingest.validate_export(record['before']);ingest.validate_export(record['after'])
 before=json.loads(bytes.fromhex(record['before']['head']));after=json.loads(bytes.fromhex(record['after']['head']))
 for key in ('counts','resources','partitions','active'):same(before[key],after[key],'ACCOUNTING-OR-INTENT-CHANGED:'+key)
 same(record['before']['config'],record['after']['config'],'CONFIG-CHANGED')
 authenticated_recovery(frames,record,ingest)
 same(record['before']['blobs'],record['after']['blobs'],'BLOB-CHANGED')
 same(record['before']['ownership_meta'],record['after']['ownership_meta'],'OWNER-META-CHANGED')
 same(record['before']['owners'],record['after']['owners'],'OWNER-CHANGED')
 need(record['after']['events'][:len(record['before']['events'])]==record['before']['events'],'HISTORY-LOSS')
 for f in frames.values():
  if f['call']['function'] in ('open_session','ManagedAuthority.__init__','Authority.__init__'):
   same(f['call']['arguments']['config'],record['before']['config'],'CONSTRUCTION-AUTHENTICATED-CONFIG')
  if f['call']['function']=='validate_export':
   same(f['call']['arguments']['x']['config'],record['before']['config'],'RECOVERY-AUTHENTICATED-CONFIG')
 calls=[f for f in frames.values() if f['call']['source']=='authority' and f['call']['function']=='Authority.handle']
 observed_requests=[];expected_u=copy.deepcopy(before['u']);claims=0
 for f in calls:
  raw=bytes.fromhex(f['call']['arguments']['packet']['bytes_hex']);env=json.loads(raw);q=env['request'];ingest.verify_signature(q['principal'],q,env['signature']);observed_requests.append(raw.hex())
  if q['method']=='sign':
   # Supported slice: source-admitted claim persists; injected signature commit
   # rolls back. No other U field or charged resource may change.
   sign_source=(Path(root)/SOURCES['authority']).read_text();need("p['phase']='SIGNING';self.save(s,r,'sign-claim')" in sign_source,'UNSUPPORTED-SIGN-CLAIM-SOURCE')
   pending=expected_u[q['u']]['stage']['pending'];need(pending['phase']=='DECIDED' and q['body']=={'action':pending['action']},'SIGN-ATTEMPT-ANCESTRY');pending['phase']='SIGNING';claims+=1
  else:need(q['method']=='head','OUTSIDE-EXECUTED-METHOD-DOMAIN')
  managers=[v for v in frames.values() if v['call']['frame']==f['call']['parent']];need(len(managers)==1 and managers[0]['call']['function']=='ManagedAuthority._run','RAW-ENTRY')
  same(managers[0]['call']['arguments']['args'][0],{'bytes_hex':raw.hex()},'REQUEST-ANCESTRY')
  rows=[r for r in record['after']['journal'] if r[0]==q['challenge']];need(len(rows)==1 and rows[0][1]==raw.hex(),'REQUEST-JOURNAL')
  if f['normal']:
   same(f['return']['value'],{'bytes_hex':rows[0][2]},'RESPONSE-PERSISTENCE');need(rows[0][2] is not None,'MISSING-RESPONSE')
 same(record['requests'],observed_requests,'REQUEST-COVERAGE')
 old_challenges={row[0] for row in record['before']['journal']}
 new_rows=[row for row in record['after']['journal'] if row[0] not in old_challenges]
 same(sorted(row[1] for row in new_rows),sorted(observed_requests),'UNOBSERVED-JOURNAL-REQUEST')
 same(after['u'],expected_u,'ATTEMPT-OR-OBLIGATION-CHANGE')
 need(len(record['after']['events'])==len(record['before']['events'])+claims,'EVENT-MULTIPLICITY')
 for old in record['before']['journal']:need(old in record['after']['journal'],'PRIOR-JOURNAL-CHANGE')
 # Every attempted dispatch, including requests blocked before Authority.handle.
 managed_calls=[f for f in frames.values() if f['call']['function']=='ManagedAuthority.handle']
 same(record['attempted_packets'],[f['call']['arguments']['packet']['bytes_hex'] for f in managed_calls],'MANAGED-REQUEST-COVERAGE')
 # Exact requirement/procedure joins; occurrence contribution is additive, never
 # upgrades the inherited constructed adapter or qualified duty disposition.
 seen=set()
 names={f['call']['function'] for f in frames.values()}
 for key,functions,_ in mc.REQUIREMENTS:
  if key=='response-correspondence':continue
  if any('ManagedAuthority.'+fn in names or fn in names for fn in functions):seen.add('managed:'+key)
 duties={x['requirement']:x for x in bundle['procedure']['duties']};maps={x['requirement']:x for x in bundle['producers']['mappings']};dirs={x['requirement']:x for x in bundle['directories']['managed_directories']}
 need(seen<=set(duties)&set(maps)&set(dirs),'MISSING-DOWNSTREAM-JOIN')
 return {'consumer':mc.identity(root,'compiler/managed_observations.py'),'correspondence_version':'MR-OBS-CORRESPONDENCE-2','observation_gaps':['filesystem root/path/ownership_path and object a excluded by retained recorder','Authority.state backend not tracked; wrapper/run equality only','implicit faults before observable call and complete forged trusted-tracer evidence not established'],'requirements_with_observed_function_calls':sorted(seen),'procedure_duties':[duties[k] for k in sorted(seen)],'producer_mappings':[k for k in sorted(seen)],'guarded_directories':[dirs[k]['id'] for k in sorted(seen)],'observed_events':len(record['events']),'obligations':mc.OBLIGATIONS,'limits':mc.LIMITS,'complete_runtime_coverage':False,'trusted_observer_not_attestation':True,'operational_boundary_established':False,'diagnostic_only_not_consumed_as_proof':['case','steps','fault_operations','fault_scope','status_before_final_close','runtime_layout'],'layout_limitation':'corrected combined tree; bounded laboratory evidence only' }


def validate_receipt(root,bundle,record,receipt,context,runtime_root):
 """A receipt is accepted only by recomputing current evidence validation."""
 expected=validate(root,bundle,record,context,runtime_root)
 same(receipt,expected,'OCCURRENCE-RECEIPT-MISMATCH')
 return expected
