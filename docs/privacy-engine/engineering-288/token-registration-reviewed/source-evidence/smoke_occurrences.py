"""Offline adapter for the exact retained status smoke. No runtime/session calls.

Public acceptance is archive-qualified. semantic() is a negative-control seam,
not an unpinned evidence admission API. Sparse trace limits remain explicit.
"""
import ast, copy, datetime, dis, hashlib, io, json, os, stat, sys, types, zipfile
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[1]
PINS={'correction.zip':(4269431,'983e8aa849be387c4f92a54953fd24e2271bb090a01a0fb589230f0edad53185'),
      'smoke.zip':(77696,'bbea8f904a91b5c13b4b79653b702154352c68471f0ed8e51035cdf27becc6e8')}
WORK='/home/steve/dev/Engineering-288-execution/I164-status-smoke-20261026T140935Z-55023eb7'
CONTEXTS=('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(v,s):
 if not v:raise ValueError(s)
def same(a,b,s):need(enc(a)==enc(b),s)
def regular(p):
 need(stat.S_ISREG(p.lstat().st_mode),'NONREGULAR:'+str(p));return p.read_bytes()
def archive(path,pin):
 raw=regular(path);same(identity(raw),dict(zip(('bytes','sha256'),pin)),'ARCHIVE-IDENTITY')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  names=z.namelist();need(len(names)==len(set(names)),'DUPLICATE-MEMBER')
  for i in z.infolist():
   p=PurePosixPath(i.filename)
   need(not p.is_absolute() and '..' not in p.parts and p.as_posix()==i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG),'ARCHIVE-MEMBER')
  return {n:z.read(n) for n in names}
def exact_tree(root,expected):
 dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'};seen=set();found=set()
 need(stat.S_ISDIR(root.lstat().st_mode),'ROOT-TYPE')
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):
    need(n in dirs,'UNDECLARED-DIRECTORY');found.add(n);walk(q)
   else:need(stat.S_ISREG(mode) and n in expected,'UNDECLARED-OR-NONREGULAR');seen.add(n)
 walk(root);need(seen==set(expected) and found==dirs,'ROOT-MEMBERSHIP')
 for n,b in expected.items():need(regular(root/n)==b,'ROOT-BYTES:'+n)
def module(raw,name,path):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(raw,str(path),'exec'),m.__dict__);return m
def load(root=ROOT):
 root=Path(root);c=archive(root/'inputs/correction.zip',PINS['correction.zip']);e=archive(root/'inputs/smoke.zip',PINS['smoke.zip'])
 r=root/'retained/correction';exact_tree(r,c)
 b=module(c['code/correspondence.py'],'_status_correspondence',r/'code/correspondence.py')
 b.validate(r,c['provenance/status-correspondence.json'])
 binding=json.loads(c['provenance/status-correspondence.json'])
 # Reuse existing status-value validator without loading Authority or a backend.
 mc=module(c['retained/candidate/compiler/managed_coverage.py'],'managed_coverage',r/'retained/candidate/compiler/managed_coverage.py')
 prior=sys.modules.get('managed_coverage');sys.modules['managed_coverage']=mc
 try:mo=module(c['retained/candidate/compiler/managed_observations.py'],'_managed_observations',r/'retained/candidate/compiler/managed_observations.py')
 finally:
  if prior is None:del sys.modules['managed_coverage']
  else:sys.modules['managed_coverage']=prior
 return {'root':r,'c':c,'e':e,'binding':binding,'mo':mo,'mc':mc}
def codes(raw,path):
 result={}
 def walk(c):
  if c.co_name!='<module>':result[c.co_qualname]=c
  for child in c.co_consts:
   if isinstance(child,types.CodeType):walk(child)
 walk(compile(raw,path,'exec',optimize=0));return result
def capture_contract(c,e,paths):
 """Read the pinned capture declarations as AST data, never run the worker.

 This implements only its existing watched-map and snapshot projection forms.
 Unsupported syntax rejects instead of supplying a guessed observation rule.
 """
 worker=ast.parse(e['preparation/worker.py']);smoke=next(n for n in worker.body if isinstance(n,ast.FunctionDef) and n.name=='smoke')
 watched=next(n.value for n in smoke.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='watched' for t in n.targets))
 def path_expr(n):
  if isinstance(n,ast.Name):
   need(n.id in ('ROOT','WORK'),'WATCH-PATH-ROOT');return WORK+'/reviewed-boundary' if n.id=='ROOT' else WORK
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div):return path_expr(n.left)+'/'+ast.literal_eval(n.right)
  need(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='str' and len(n.args)==1 and not n.keywords,'WATCH-PATH-FORM')
  return path_expr(n.args[0])
 need(isinstance(watched,ast.Dict),'WATCH-MAP-FORM')
 watch={path_expr(k):frozenset(ast.literal_eval(v)) for k,v in zip(watched.keys,watched.values)}
 same(sorted(watch),sorted(paths),'WATCH-SOURCE-PATHS')
 snap=next(n for n in worker.body if isinstance(n,ast.FunctionDef) and n.name=='snapshot')
 projection=next(n.value for n in snap.body if isinstance(n,ast.Return))
 need(isinstance(projection,ast.DictComp) and len(projection.generators)==1,'SNAPSHOT-FORM')
 keys=ast.literal_eval(projection.generators[0].iter)
 # Anchor the other projection semantics, including absent self and dictionary
 # membership. These are syntax support requirements for this finite adapter.
 same([ast.unparse(n) for n in snap.body[:3]], ["o = f.f_locals.get('self')",'if o is None:\n    return None',"d = getattr(o, '__dict__', {})"],'SNAPSHOT-CONTRACT')
 same(ast.unparse(projection.key),'k','SNAPSHOT-KEY');same(ast.unparse(projection.value),'d[k]','SNAPSHOT-VALUE')
 same([ast.unparse(n) for n in projection.generators[0].ifs],['k in d'],'SNAPSHOT-PRESENCE')
 observer=next(n for n in smoke.body if isinstance(n,ast.FunctionDef) and n.name=='observer')
 matched=next(n.value for n in observer.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='matched' for t in n.targets))
 expected="path in watched and (name in watched[path] or (path == str(ROOT / 'code/prospective_entry.py') and f.f_code.co_name == '<lambda>'))"
 same(ast.dump(matched,include_attributes=False),ast.dump(ast.parse(expected,mode='eval').body,include_attributes=False),'WATCH-PREDICATE')
 start=next(n.value for n in worker.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NEXT' for t in n.targets))
 increments=[n for n in ast.walk(observer) if isinstance(n,ast.AugAssign) and isinstance(n.target,ast.Name) and n.target.id=='NEXT']
 need(len(increments)==1 and isinstance(increments[0].op,ast.Add),'FRAME-ALLOCATION-SOURCE')
 first=ast.literal_eval(start);step=ast.literal_eval(increments[0].value)
 need(type(first) is int and type(step) is int and step>0,'FRAME-ALLOCATION-TYPE')
 return watch,keys,first,step

def source_snapshot_check(c,e,paths,specs,frames):
 """Source-supported successful constructor/recovery/close snapshot slice.
 No synthetic offsets, arguments, missing frames or exception-path claims.
 """
 watch,keys,next_frame,frame_step=capture_contract(c,e,paths)
 manager=WORK+'/candidate/compiler/live_connection.py';entry=WORK+'/reviewed-boundary/code/prospective_entry.py'
 tree=ast.parse(c[paths[manager]]);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
 def field(t):return t.attr if isinstance(t,ast.Attribute) and isinstance(t.value,ast.Name) and t.value.id=='self' else None
 def constants(body):
  values={}
  for n in body:
   if isinstance(n,ast.Assign):
    for t in n.targets:
     k=field(t)
     if k in keys:
      need(k not in values,'DUPLICATE-CONSTRUCTOR-ASSIGNMENT');values[k]=ast.literal_eval(n.value)
  return values
 initial=constants(methods['__init__'].body)
 # Every projected constructor write must be the direct literal assignments
 # above; no hidden branch or augmentation may be silently ignored.
 writes=[field(t) for n in ast.walk(methods['__init__']) if isinstance(n,ast.Assign) for t in n.targets if field(t) in keys]
 same(sorted(writes),sorted(initial),'CONSTRUCTOR-WRITE-COVERAGE')
 need(not any(isinstance(n,(ast.AugAssign,ast.AnnAssign)) and field(n.target) in keys for n in ast.walk(methods['__init__'])),'CONSTRUCTOR-UNSUPPORTED-WRITE')
 recover=methods['recover'];withbody=recover.body[0].body;tr=next(n for n in withbody if isinstance(n,ast.Try))
 state=copy.deepcopy(initial)
 def assign(n):
  if isinstance(n,ast.Assign):
   for t in n.targets:
    k=field(t)
    if k in initial:state[k]=ast.literal_eval(n.value)
  elif isinstance(n,ast.AugAssign) and field(n.target) in initial:
   k=field(n.target);need(isinstance(n.op,ast.Add) and type(state[k]) is int,'RECOVERY-AUGMENT');v=ast.literal_eval(n.value);need(type(v) is int,'RECOVERY-AUGMENT-TYPE');state[k]+=v
 for n in withbody:
  if n is tr:break
  assign(n)
 validation=None
 for n in tr.body:
  if any(isinstance(a,ast.Call) and isinstance(a.func,ast.Attribute) and isinstance(a.func.value,ast.Name) and a.func.value.id=='self' and a.func.attr=='_validate' for a in ast.walk(n)):
   validation=copy.deepcopy(state)
  assign(n)
 ready=copy.deepcopy(state);need(validation is not None,'VALIDATE-SOURCE-CALL')
 closebody=methods['close'].body[0].body;closed=copy.deepcopy(ready)
 closed.update(constants(closebody))
 for f in frames.values():
  call=f['call'];path=call['path'];name=call['function'];code=specs[path][name]
  same(call['frame'],next_frame,'FRAME-ALLOCATION');next_frame+=frame_step
  need(name in watch[path] or path==entry and code.co_name=='<lambda>','UNWATCHED-PRODUCER')
  # The capture returns None when the frame has no local self. The code object
  # supplies that local-variable fact independently of the submitted snapshot.
  has_self='self' in code.co_varnames
  for v in f['events']:
   if not has_self:same(v['state'],None,'SNAPSHOT-NO-SELF')
   else:
    need(type(v['state']) is dict and set(v['state'])<=set(keys),'SNAPSHOT-PROJECTION')
    for k,value in v['state'].items():
     need(type(value) is (int if k=='_epoch' else str),'SNAPSHOT-EXACT-TYPE')
  if path==manager and name.startswith('ManagedAuthority.'):
   if name=='ManagedAuthority.__init__':
    same(call['state'],{},'CONSTRUCTOR-ENTRY');same(f['return_event']['state'],initial,'CONSTRUCTOR-STATE')
   else:
    states={'ManagedAuthority.recover':(initial,ready),'ManagedAuthority._validate':(validation,validation),'ManagedAuthority.status':(ready,ready),'ManagedAuthority.close':(ready,closed)}
    need(name in states,'UNSUPPORTED-MANAGED-SNAPSHOT');a,b=states[name]
    same(call['state'],a,'MANAGED-CALL-STATE');same(f['return_event']['state'],b,'MANAGED-RETURN-STATE')
  elif has_self:
   # The other watched objects expose only source-assigned projected fields.
   source=ast.parse(c[paths[path]]);classname=name.split('.')[0];owner=next(n for n in source.body if isinstance(n,ast.ClassDef) and n.name==classname)
   assigned={field(t) for n in ast.walk(owner) if isinstance(n,ast.Assign) for t in n.targets}&set(keys)
   for v in f['events']:
    expected=set() if name.endswith('.__init__') and v['event']=='call' else assigned
    same(sorted(v['state']),sorted(expected),'OBJECT-SNAPSHOT-FIELDS')
   if name=='Authority.close':
    # Supported source body closes the db member only. There is no write to
    # the containing Authority's projected identity fields on this route.
    close_method=next(n for n in owner.body if isinstance(n,ast.FunctionDef) and n.name=='close')
    same([ast.dump(n,include_attributes=False) for n in close_method.body],
         [ast.dump(n,include_attributes=False) for n in ast.parse('self.db.close()').body],
         'UNSUPPORTED-AUTHORITY-CLOSE-EFFECT')
    # Derive the exact projection from this class's assignments and the saved
    # observer projection. Check each invocation, including raw and managed
    # close; equal-valued copies never substitute for invocation identity.
    same({k:call['state'][k] for k in assigned},
         {k:f['return_event']['state'][k] for k in assigned},
         'AUTHORITY-CLOSE-IDENTITY-TRANSITION')
  if path==entry and name=='main':
   main=next(n for n in ast.parse(c[paths[entry]]).body if isinstance(n,ast.FunctionDef) and n.name=='main')
   need(isinstance(main.body[-1],ast.Return),'MAIN-SUCCESS-RETURN-SOURCE')
   same(f['return_event']['value'],ast.literal_eval(main.body[-1].value),'MAIN-SUCCESS-EXACT-TYPE')
def semantic(ctx,e):
 """Check native sparse evidence, without inventing old-format trace fields."""
 c=ctx['c'];j=lambda n:json.loads(e[n]);events=j('evidence/execution-trace.json')['events']
 need(sys.version_info[:3]==(3,12,14) and sys.flags.optimize==0,'CHECKER-INTERPRETER')
 trace=j('evidence/execution-trace.json');need(trace['format']=='I164-STATUS-SMOKE-OBSERVATION-1','TRACE-FORMAT')
 paths={WORK+'/reviewed-boundary/code/prospective_entry.py':'code/prospective_entry.py',
  WORK+'/reviewed-boundary/retained/launcher/code/lab_bootstrap.py':'retained/launcher/code/lab_bootstrap.py',
  WORK+'/candidate/compiler/live_connection.py':'retained/candidate/compiler/live_connection.py',
  WORK+'/runtime/prospective/authority.py':'retained/candidate/support/reference/runtime/authority.py'}
 specs={p:codes(c[n],p) for p,n in paths.items()}
 frames={};stack=[];suspended=set();last=-1
 for seq,v in enumerate(events):
  need(type(v['seq']) is int and v['seq']==seq and type(v['frame']) is int,'TRACE-ORDER')
  need(v['frame']>0 and (v['parent'] is None or type(v['parent']) is int and v['parent']>0),'FRAME-EXACT-TYPE')
  need(type(v['resumed_generator']) is bool and type(v['line']) is int,'CAPTURE-EXACT-TYPES')
  if v['event']=='return':need(type(v['normal_return']) is bool,'COMPLETION-EXACT-TYPE')
  fields={'seq','observed_at','monotonic_ns','frame','parent','path','function','line','event','resumed_generator','state'}
  if v['event']=='return':
   fields|={'opcode','normal_return'}
   if v['function'] in ('ManagedAuthority.status','ManagedAuthority.recover','main'):fields.add('value')
  same(sorted(v),sorted(fields),'TRACE-FIELDS')
  need(v['path'] in specs and v['function'] in specs[v['path']],'TRACE-SOURCE')
  code=specs[v['path']][v['function']];ops=list(dis.get_instructions(code,show_caches=True))
  need(type(v['monotonic_ns']) is int and v['monotonic_ns']>last,'MONOTONIC-ORDER');last=v['monotonic_ns']
  datetime.datetime.fromisoformat(v['observed_at'])
  f=v['frame'];need(v['event'] in ('call','return'),'OUTSIDE-SUCCESS-SMOKE')
  if v['event']=='call':
   need(v['parent']==(stack[-1] if stack else None),'CALLER-PARENT')
   if v['resumed_generator']:
    need(f in suspended,'INVENTED-RESUME');suspended.remove(f)
    old=frames[f]['call'];same([v[k] for k in ('path','function','parent')],[old[k] for k in ('path','function','parent')],'RESUME-IDENTITY')
    need(v['line']==frames[f]['yield']['line'],'RESUME-LINE')
   else:
    need(f not in frames and v['line']==code.co_firstlineno,'FRAME-IDENTITY');frames[f]={'call':v,'events':[]}
   stack.append(f)
  else:
   need(stack and stack[-1]==f,'RETURN-STACK');old=frames[f]['call']
   same([v[k] for k in ('path','function','parent')],[old[k] for k in ('path','function','parent')],'RETURN-IDENTITY')
   need(not v['resumed_generator'],'RETURN-RESUME-FLAG')
   need(any(i.opname==v['opcode'] and i.positions.lineno==v['line'] for i in ops),'SOURCE-RETURN-SITE')
   normal=v['opcode'] in ('RETURN_VALUE','RETURN_CONST');same(v['normal_return'],normal,'COMPLETION-CLASS')
   stack.pop()
   if normal:frames[f].update(normal=True,return_event=v)
   else:
    need(code.co_flags & 0x20 and v['opcode']=='YIELD_VALUE','UNSUPPORTED-COMPLETION');suspended.add(f);frames[f]['yield']=v
  frames[f]['events'].append(v)
 need(not stack and not suspended and all(f.get('normal') for f in frames.values()),'INCOMPLETE-TRACE')
 source_snapshot_check(c,e,paths,specs,frames)
 def one(name,parent=None):
  fs=[f for f in frames.values() if f['call']['function']==name and (parent is None or f['call']['parent']==parent['call']['frame'])]
  need(len(fs)==1,'CALL-FAMILY:'+name);return fs[0]
 main=one('main');run=one('run',main);route=one('_run',run);session=one('session',route);launch=one('_session',session)
 opened=one('open_session',launch);init=one('ManagedAuthority.__init__',opened);recover=one('ManagedAuthority.recover',opened)
 ctor=one('Authority.__init__',recover);validate=one('ManagedAuthority._validate',recover);status=one('ManagedAuthority.status',recover)
 diagnostic=one('ManagedAuthority.status',launch);client=one('Client.__init__',route);handoff=one('main.<locals>.<lambda>',route)
 closed=one('ManagedAuthority.close',launch);close_backend=one('Authority.close',closed)
 raw_ctor=one('Authority.__init__',launch);raw_close=one('Authority.close',launch)
 need(len(frames)==18,'UNEXPECTED-CALL-MULTIPLICITY')
 def before(a,b):need(a['return_event']['seq']<b['call']['seq'],'CALL-ORDER')
 for a,b in [(raw_ctor,raw_close),(raw_close,opened),(init,recover),(ctor,validate),(validate,status),(opened,diagnostic),(diagnostic,client),(client,handoff),(handoff,closed)]:before(a,b)
 need(main['call']['parent'] is None and main['return_event'].get('value')==0,'ENTRY-COMPLETION')
 same(closed['return_event']['state'],{'_phase':'CLOSED','_reason':'close confirmed; no serving connection','_epoch':1},'CLOSE-STATE')
 same(recover['call']['state']['_epoch'],0,'INITIAL-EPOCH');same(recover['return_event']['state']['_epoch'],1,'RECOVERY-EPOCH')
 # Existing fixed_status consumes only these recorded state selectors. No live,
 # retired, argument, offset or ingest frame is manufactured for it.
 adapted={}
 for k,f in frames.items():
  ret=copy.deepcopy(f['return_event']);s=ret['state'] or {};ret['state']={'phase':s.get('_phase'),'epoch':s.get('_epoch')}
  adapted[k]={'call':f['call'],'normal':f['normal'],'return':ret}
 ctx['mo'].fixed_status(ctx['root']/'retained/candidate',adapted)
 for f in (status,diagnostic):same(f['return_event']['value']['reason'],f['return_event']['state']['_reason'],'REASON-SNAPSHOT')
 rec=recover['return_event']['value'];same(rec['recovery_only'],True,'RECOVERY-ONLY');same(rec['new_attempt_authorized'],False,'NO-RENEWAL')
 x=j('evidence/recovery-export-0.json');head=json.loads(bytes.fromhex(x['head']));own=json.loads(bytes.fromhex(x['ownership_meta']))
 bind=j('evidence/session-records/binding.json');complete=j('evidence/session-records/BOOTSTRAP-COMPLETE.json');hands=j('evidence/client-handoff.json');need(len(hands)==1,'HANDOFF-COUNT');hand=hands[0]
 cfg=json.loads(c['retained/launcher/laboratory-configuration.json']);same(bind['configuration'],cfg,'CONFIGURATION');same(x['config'],cfg['config'],'EXPORT-CONFIG')
 need(bind['candidate']==WORK+'/candidate' and bind['draft']==WORK+'/draft' and bind['runtime']==WORK+'/runtime','WORKSPACE-LINEAGE')
 same(bind['launcher'],identity(c['retained/launcher/code/lab_bootstrap.py']),'LAUNCHER-BINDING')
 for key,n in [('environment_guard','code/environment5002.py'),('environment_profile','environment-profile.json'),('runtime_map','provenance/runtime-layout.json'),('candidate_manifest','provenance/candidate-members.json'),('draft_manifest','provenance/draft-members.json')]:same(bind[key],identity(c['retained/launcher/'+n]),'BINDING:'+key)
 env=j('evidence/environment-preflight.json')['environment'];same(bind['environment'],env,'ENVIRONMENT-BINDING');need(env['python']=='3.12.14' and env['packages']['cryptography']['version']=='50.0.2','HOST-PROFILE')
 copies=j('evidence/source-copy-identities.json')
 for k in ('candidate','draft'):same(copies[k],json.loads(c['retained/launcher/provenance/'+k+'-members.json']),'SOURCE-COPY:'+k)
 same(copies['before_after_match'],True,'SOURCE-COPY-STABILITY')
 layout=json.loads(c['retained/launcher/provenance/runtime-layout.json']);same(layout['prospective/authority.py'],'support/reference/runtime/authority.py','RUNTIME-SOURCE-MAP')
 for n in ('compiler/live_connection.py','support/reference/runtime/authority.py'):same(copies['candidate'][n],identity(c['retained/candidate/'+n]),'EXECUTED-SOURCE:'+n)
 prep=j('preparation/preparation-identity.json');same(prep['correction'],dict(zip(('bytes','sha256'),PINS['correction.zip'])),'PREPARATION-CORRECTION');same(prep['worker'],identity(e['preparation/worker.py']),'OBSERVER-SOURCE')
 started=j('evidence/SMOKE-ABOUT-TO-START.json');same(started['entry'],identity(c['code/prospective_entry.py']),'EXECUTED-ENTRY');same(started['destination'],WORK+'/disposable-session','SESSION-LINEAGE')
 same(hand['state'],head,'HANDOFF-HEAD');same(complete['state'],head,'BOOTSTRAP-STATE');same(complete['status'],diagnostic['return_event']['value'],'BOOTSTRAP-DIAGNOSTIC')
 same(rec['head'],x['expected_head'],'RECOVERY-HEAD');same(head['head'],x['expected_head'],'EXPORT-HEAD')
 for f in (ctor,raw_ctor,raw_close,close_backend):
  same(f['return_event']['state']['binding'],head['binding'],'INSTANCE-BINDING')
  same(f['return_event']['state']['ownership_binding'],hashlib.sha256(bytes.fromhex(x['ownership_meta'])).hexdigest(),'OWNERSHIP-INCARNATION')
  if f['call']['function']=='Authority.close':
   same(f['call']['state']['binding'],head['binding'],'CLOSE-ENTRY-INSTANCE-BINDING')
   same(f['call']['state']['ownership_binding'],hashlib.sha256(bytes.fromhex(x['ownership_meta'])).hexdigest(),'CLOSE-ENTRY-OWNERSHIP-INCARNATION')
 need(all(x[k]==[] for k in ('events','blobs','journal','owners')) and head['seq']==0 and head['u']=={} and head['active'] is None,'FRESH-EMPTY-EXPORT')
 need(all(type(v) is int and v==0 for k in ('counts','partitions','resources') for v in head[k].values()),'FRESH-COUNTS')
 same(hand['public_methods'],['handle','state'],'CLIENT-SURFACE');same(hand['absent_attributes'],['status','recover','close','manager','managed','wrapper','scheduler','a','control','__dict__'],'CLIENT-ABSENCES')
 same(hand['request_issued'],False,'NO-REQUEST');same(hand['observer_call_site'],'worker.py:check_handoff -> Client.state','OBSERVER-CALLER')
 need(set(hand)=={'observed_before','observed_after','public_methods','absent_attributes','state','request_issued','observer_call_site','trace_limitation'},'HANDOFF-FIELDS')
 need(handoff['call']['observed_at']<=hand['observed_before']<=hand['observed_after']<=handoff['return_event']['observed_at'],'HANDOFF-INTERVAL')
 need(not any(f['call']['function']=='Client.state' for f in frames.values()),'INVENTED-STATE-FRAME')
 close=j('evidence/confirmed-close.json');same(close['normal_close_event'],closed['return_event'],'CLOSE-EVENT')
 for k in ('active_marker_absent','failure_records_absent','cooperative_lock_reacquired'):same(close[k],True,'CLOSE-GUARD:'+k)
 same(close['before'],close['after'],'CLOSED-FILE-CHANGE')
 same(sorted(close['before']),sorted(['binding.json','BOOTSTRAP-COMPLETE.json','BOOTSTRAP-STARTED.json','RAW-CREATION-CLOSED.json','state/session.sqlite','state/ownership.sqlite']),'RETAINED-SET')
 for n,pin in close['before'].items():same(identity(e['evidence/session-records/'+n]),pin,'RETAINED-IDENTITY:'+n)
 for n in ('binding.json','BOOTSTRAP-COMPLETE.json','BOOTSTRAP-STARTED.json','RAW-CREATION-CLOSED.json'):need(e['new-session-records/'+n]==e['evidence/session-records/'+n],'COPY-LINEAGE')
 main_ast=next(n for n in ast.parse(c['code/prospective_entry.py']).body if isinstance(n,ast.FunctionDef) and n.name=='main')
 prints=[n for n in ast.walk(main_ast) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='print' and not n.keywords]
 need(len(prints)==1,'OUTPUT-SOURCE');stdout=(ast.literal_eval(prints[0].args[0])+'\n').encode()
 need(e['evidence/smoke.stdout']==stdout and e['evidence/smoke.stderr']==b'','DEFAULT-OUTPUT')
 process=j('evidence/smoke-process-result.json');same(process['returncode'],0,'PROCESS-EXIT')
 for k in ('stdout','stderr'):same(process[k],identity(e['evidence/smoke.'+k]),'PROCESS-OUTPUT-HASH')
 output=j('evidence/output-check.json')
 for k,v in [('exact_fixed_stdout',True),('empty_stderr',True),('status_serialized_to_default_output',False),('raw_traceback_to_default_output',False)]:same(output[k],v,'OUTPUT-ASSERTION')
 same(j('evidence/forbidden-call-observations.json'),[],'FORBIDDEN-CALLS')
 result=j('evidence/smoke-result.json');same(result['result'],'PASS','RESULT');same(result['state'],head,'RESULT-STATE')
 for k in ('head','config','ownership_meta'):same(result[k],x[k],'RESULT-EXPORT:'+k)
 same(result['rows_from_actual_recovery_export'],{k:len(x[k]) for k in ('events','blobs','journal','owners')},'RESULT-ROW-COUNTS')
 for k in ('requests_issued','transactions_signed_or_submitted'):same(result[k],0,'RESULT-NO-ACTIONS')
 for k in ('service_started','actual_admission'):same(result[k],False,'RESULT-BOUNDARY')
 return {'frames':frames,'paths':paths,'head':head,'ownership':own,'handoff_frame':handoff['call']['frame'],'close_frame':closed['call']['frame']}

def derive(ctx):
 e=ctx['e'];s=semantic(ctx,e);c=ctx['c'];binding=ctx['binding'];aid=PINS['smoke.zip'][1]
 def ref(n,pointer):return {'acquisition':'sha256:'+aid,'artifact':n,**identity(e[n]),'pointer':pointer}
 instance={'workspace':WORK,'session_label':json.loads(e['evidence/recovery-export-0.json'])['config']['session'],'binding':s['head']['binding'],'ownership_incarnation':s['ownership']['incarnation'],'managed_constructor_frame':next(k for k,f in s['frames'].items() if f['call']['function']=='ManagedAuthority.__init__')}
 # Site joins are existing additive declarations; close is joined directly to
 # the source-owned managed requirement absent from the status-only site list.
 site_map={'main':'prospective-output','run':'general-entry','_run':'owner-routing','session':'launcher-entry','_session':'launcher-diagnostic-and-evidence','open_session':'managed-entry','ManagedAuthority.recover':'recover-embedding','ManagedAuthority.status':'manager-status','Client.__init__':'owner-routing','main.<locals>.<lambda>':'general-entry'}
 req_map={'main':'normal','run':'entry','_run':'entry','session':'entry','_session':'entry','open_session':'entry','ManagedAuthority.__init__':'entry','ManagedAuthority.recover':'restored','ManagedAuthority._validate':'obligation-preservation','ManagedAuthority.status':'restored','ManagedAuthority.close':'close-confirmed','Authority.__init__':'entry','Authority.close':'close-confirmed','Client.__init__':'normal','main.<locals>.<lambda>':'normal'}
 model=json.loads(c['basis/candidate/managed-route/model.json']);duties=json.loads(c['basis/prospective_outputs/managed-route/procedure-duty.json'])['duties'];producers=json.loads(c['basis/candidate/managed-route/producers.json'])['mappings'];dirs=json.loads(c['basis/candidate/managed-route/directory-relations.json'])['managed_directories']
 contexts=[]
 for context in CONTEXTS:
  occurrences=[]
  for fid,f in sorted(s['frames'].items()):
   v=f['call'];name=v['function'];req='managed:'+req_map[name]
   site=next((a for a in binding['sites'] if a['id']==site_map.get(name)),None)
   row={'id':f'{aid}:{context}:frame:{fid}','kind':'traced-invocation','frame':fid,'parent_frame':v['parent'],'source':{'path':s['paths'][v['path']],**identity(c[s['paths'][v['path']]]),'qualified':name},'site':None if site is None else site['id'],'requirement':req,'call':ref('evidence/execution-trace.json',f"/events/{v['seq']}"),'completion':ref('evidence/execution-trace.json',f"/events/{f['return_event']['seq']}"),'suspension_events':[ref('evidence/execution-trace.json',f"/events/{a['seq']}") for a in f['events'] if a.get('opcode')=='YIELD_VALUE'],'observed_local_values':{k:f['return_event']['state'][field] for k,field in [('managed-local:phase','_phase'),('managed-local:epoch','_epoch')] if f['return_event']['state'] and field in f['return_event']['state']},'classification':'UNKNOWN','canonical_ordinal':None}
   if name=='ManagedAuthority.recover':row['observed_local_values']['managed-local:recovery-result']=f['return_event']['value']
   occurrences.append(row)
  occurrences.append({'id':f'{aid}:{context}:observer-state:0','kind':'explicit-observer-call','frame':None,'parent_frame':None,'site':'client-state','requirement':'managed:normal','record':ref('evidence/client-handoff.json','/0'),'source':{'path':'code/prospective_entry.py',**identity(c['code/prospective_entry.py']),'qualified':'Client.state'},'observer_source':ref('preparation/worker.py','check_handoff'),'associated_handoff_frame':s['handoff_frame'],'classification':'UNKNOWN','canonical_ordinal':None})
  used=sorted({r['requirement'] for r in occurrences});joined={}
  for req in used:
   d=[v for v in duties if v['requirement']==req];p=[v for v in producers if v['requirement']==req];g=[v for v in dirs if v['requirement']==req];need(len(d)==len(p)==len(g)==1,'DOWNSTREAM-JOIN')
   joined[req]={'duty':d[0],'producer':p[0],'directory_id':g[0]['id']}
  contexts.append({'context':context,'instance':copy.deepcopy(instance),'occurrences':occurrences,'joins':joined,'declarations':model['local_declarations'],'output_observation':{'stdout':ref('evidence/smoke.stdout','whole-bytes'),'stderr':ref('evidence/smoke.stderr','whole-bytes'),'site':'prospective-output','requirement':'managed:normal'},'close_observation':{'record':ref('evidence/confirmed-close.json',''),'frame':s['close_frame'],'requirement':'managed:close-confirmed'},'retained_copies':[{'copy':ref('new-session-records/'+n,''),'of':ref('evidence/session-records/'+n,''),'new_invocation':False} for n in ('binding.json','BOOTSTRAP-COMPLETE.json','BOOTSTRAP-STARTED.json','RAW-CREATION-CLOSED.json')]})
  contexts[-1]['record_declaration_joins']=[{'declaration':next(v for v in model['existing_declarations'] if v['template_id']==template),'record':ref('evidence/recovery-export-0.json',pointer),'additional_invocation':False} for template,pointer in [('HEAD:','/head'),('CONFIG:','/config'),('OWNERSHIP-META:','/ownership_meta')]]
 return {'format':'I164-STATUS-SMOKE-OCCURRENCE-CONNECTION-1','input_archives':{k:dict(zip(('bytes','sha256'),v)) for k,v in PINS.items()},'status_binding':identity(c['provenance/status-correspondence.json']),'contexts':contexts,'obligation_source':identity(c['retained/remaining-obligations.json']),'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'limits':copy.deepcopy(binding['limits']),'gaps':['Sparse trace has no bytecode offsets, line events, call arguments or live/retired snapshots; old full trace validator is not invoked','Status value checker reused on recorded fields; no synthetic ingest/state frames','Counts describe this capture only; two context views are not two executions','Source state/handle surface is observed; handle was not invoked','Historical launcher-frame provenance remains unavailable','Export bytes are correlated with saved records; no fresh ingest or database validation, durability or exclusivity proof','Trusted observer and stable trusted filesystem; no forged-observer resistance or arbitrary Python isolation','Canonical allocation, full-model binding, complete lifetime scope and qualification remain unestablished'],'SOURCE_ONLY':'UNCHANGED','Decision_B':'UNCHANGED','cumulative_envelope':'UNADOPTED','actual_admission':False}
def validate(root,saved):
 expected=enc(derive(load(root)));need(type(saved) is bytes and saved==expected,'OCCURRENCE-RECEIPT-MISMATCH');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(expected),'actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('operation',choices=['write','check']);p.add_argument('output');p.add_argument('--root',type=Path,default=ROOT);a=p.parse_args()
 if a.operation=='write':
  raw=enc(derive(load(a.root)))
  with Path(a.output).open('xb') as f:f.write(raw)
 else:print(json.dumps(validate(a.root,Path(a.output).read_bytes()),sort_keys=True))
