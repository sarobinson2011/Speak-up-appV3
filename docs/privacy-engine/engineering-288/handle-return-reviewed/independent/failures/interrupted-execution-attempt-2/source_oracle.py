"""Reviewer-owned AST audit. Does not call either supplied guard extractor."""
import ast,copy,hashlib
def key(n):return ':'.join(map(str,(n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__)))
def index(raw,class_name,selected):
 text=raw.decode();tree=ast.parse(raw);owner=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==class_name);methods={n.name:n for n in owner.body if isinstance(n,ast.FunctionDef)};info={};nodes={}
 def ref(n):return {'site':key(n),'expression':ast.get_source_segment(text,n)}
 def block(owner,region,seq,fn,guards,blocks,handlers):
  for i,n in enumerate(seq):walk(n,fn,guards,blocks+[{'owner':key(owner),'region':region,'normal_continuation_of':[ref(p) for p in seq[:i] if isinstance(p,ast.stmt)]}],handlers)
 def walk(n,fn,g,b,h):
  if hasattr(n,'lineno'):info[key(n)]={'function':fn,'guards':g,'continuation':b,'handlers':h};nodes[key(n)]=n
  if isinstance(n,ast.ClassDef):
   for child in n.body:
    if isinstance(child,ast.FunctionDef) and child.name in selected:walk(child,fn,g+[('class',key(n))],[],h)
  elif isinstance(n,ast.FunctionDef):block(n,'body',n.body,n.name,g+[('invoke',key(n))],[],[])
  elif isinstance(n,ast.With):
   for item in n.items:walk(item.context_expr,fn,g,b,h)
   block(n,'body',n.body,fn,g+[('enter',key(n),tuple(ast.unparse(i.context_expr) for i in n.items))],b,h)
  elif isinstance(n,ast.Try):
   block(n,'body',n.body,fn,g+[('try',key(n))],b,h)
   for i,handler in enumerate(n.handlers):walk(handler,fn,g+[('dispatch',key(n),i)],b,h)
   assert not n.orelse and not n.finalbody,'new source form needs review'
  elif isinstance(n,ast.ExceptHandler):
   block(n,'body',n.body,fn,g+[('handler',key(n),ast.unparse(n.type))],b,h+[n])
  elif isinstance(n,(ast.If,ast.IfExp)):
   walk(n.test,fn,g,b,h)
   for region,truth in [('body','truthy'),('orelse','falsy')]:
    sub=getattr(n,region);gg=g+[('predicate',key(n),ast.unparse(n.test),truth)]
    if isinstance(sub,list):block(n,region,sub,fn,gg,b,h)
    else:walk(sub,fn,gg,b,h)
  elif isinstance(n,ast.BoolOp):
   for i,operand in enumerate(n.values):
    prefix=[] if i==0 else [('bool-prefix',key(n),type(n.op).__name__,i,tuple((key(v),ast.unparse(v),'truthy' if isinstance(n.op,ast.And) else 'falsy') for v in n.values[:i]))]
    walk(operand,fn,g+prefix,b,h)
  else:
   for child in ast.iter_child_nodes(n):walk(child,fn,g,b,h)
 walk(owner,None,[],[],[])
 def guards(row):
  out=[]
  for g in row:
   kind,site,region,req=g['kind'],g['site'],g['region'],g['requires']
   if kind=='ClassDef':assert region=='class-body' and req==[{'event':'class-definition-executed'}];out.append(('class',site))
   elif kind=='FunctionDef':
    assert region=='invocation-boundary' and req==[{'event':'invocation-or-generator-resumption-required'}] and 'definition-time only' in g['outer_conditions'];out.append(('invoke',site))
   elif kind=='With':
    assert region=='body' and all(r['event']=='context-enter-completed' and r['item']==i for i,r in enumerate(req));out.append(('enter',site,tuple(r['expression'] for r in req)))
   elif kind=='Try' and region=='try-body':assert req==[{'event':'try-entered'}];out.append(('try',site))
   elif kind=='Try' and region=='handler-dispatch':
    assert req[0]=={'event':'exception-from-try-body'} and req[1]['event']=='earlier-handlers-not-selected' and len(req)==2;out.append(('dispatch',site,req[1]['count']))
   elif kind=='ExceptHandler':
    assert region=='handler-body' and len(req)==1 and req[0]['event']=='handler-selected';out.append(('handler',site,req[0]['exception_type']))
   elif kind in ('If','IfExp'):
    assert len(req)==1 and req[0]['predicate']==('truthy' if region=='body' else 'falsy') and req[0]['expression']==g['test'];out.append(('predicate',site,g['test'],req[0]['predicate']))
   elif kind=='BoolOp':
    i=int(region.removeprefix('operand-'));assert i>0 and len(req)==i and g['operator'] in ('And','Or')
    out.append(('bool-prefix',site,g['operator'],i,tuple((r['site'],r['expression'],r['predicate']) for r in req)))
   else:raise AssertionError(('unexpected guard',g))
  return out
 def check(row,n):
  q=info[key(n)];assert row["site"]==key(n) and row["expression"]==ast.get_source_segment(text,n)
  assert row["function"]==(n.name if isinstance(n,ast.FunctionDef) else q["function"])
  assert guards(row["guards"])==q["guards"],("guards",key(n))
  assert row["continuation"]==q["continuation"],("continuation",key(n))
  return True
 return methods,info,nodes,check

def audit(manager,authority,anchor,observations,cat,model,producer,refs):
 def same_ast(node,text,mode='eval'):
  want=ast.parse(text,mode=mode);want=want.body if mode=='eval' else want.body[0]
  assert ast.dump(node,include_attributes=False)==ast.dump(want,include_attributes=False),(ast.unparse(node),text)
 def one(seq):
  seq=list(seq);assert len(seq)==1;return seq[0]
 mm,_,_,mc=index(manager,'ManagedAuthority',{'handle','_run','_require'});am,_,_,ac=index(authority,'Authority',{'handle'})
 wrapper=mm['handle'];same_ast(wrapper,"def handle(self,packet,inject=None):return self._run('handle',packet,inject)",'exec')
 run=mm['_run'];same_ast(run,"""def _run(self,method,*args):
 with self._lock:
  self._require()
  try:
   if self._live.db.in_transaction:raise RecoveryBlocked('UNEXPECTED-ACTIVE-TRANSACTION')
   result=getattr(self._live,method)(*args)
   if self._live.db.in_transaction:raise RecoveryBlocked('UNCOMMITTED-STATE')
   return result
  except BaseException as e:
   self._quarantine(type(e).__name__+':'+str(e));raise
""",'exec')
 same_ast(mm['_require'],"def _require(self):\n if self._phase!='READY' or self._live is None or self._retired is not None:raise RecoveryBlocked('CONNECTION-'+self._phase)",'exec')
 backend=am['handle'];same_ast(backend,"""def handle(self,packet,inject=None):
 q=parse(packet,REQUEST_LIMIT);exact(q,['request','signature']);r=q['request'];exact(r,['version','binding','pilot','session','principal','challenge','expected','method','u','body'])
 need(r['version']==VERSION and r['binding']==self.binding and r['pilot']==self.config['pilot'] and r['session']==self.config['session'],'REQUEST-CONTEXT')
 need(r['principal'] in ['executor','observer'],'PRINCIPAL');verify(r['principal'],r,q['signature']);digest(r['challenge']);digest(r['expected']);label(r['u']);need(type(r['body']) is dict,'BODY')
 need((r['method']=='observe' and r['principal']=='observer') or (r['method']!='observe' and r['principal']=='executor'),'ROLE')
 with self.transaction():
  need(not self.db.execute('SELECT 1 FROM journal WHERE challenge=?',(r['challenge'],)).fetchone(),'REPLAY')
  need(self.db.execute('SELECT count(*) FROM journal').fetchone()[0]<MAX_ROWS,'JOURNAL-CAP')
  self.db.execute('INSERT INTO journal VALUES(?,?,NULL)',(r['challenge'],packet))
 try:
  if r['method']=='sign':data=self.sign(r,inject)
  else:
   with self.transaction():
    s=self.state();need(r['expected']==s['head'],'STALE');data=self.apply(s,r,inject)
   if r['method'] in ['retire','open']:fault('after_ownership_commit',inject)
   if r['method']=='decide':fault('after_decision_commit',inject)
   if r['method']=='release':fault('after_release_commit',inject)
   if r['method']=='retry_release':fault('after_retry_commit',inject)
   if r['method']=='observe':fault('after_observe_commit',inject)
  response={'request':sha(packet),'challenge':r['challenge'],'ok':True,'data':data}
 except Exception as e:
  response={'request':sha(packet),'challenge':r['challenge'],'ok':False,'error':type(e).__name__+':'+str(e)}
 raw=enc({'response':response,'signature':sig('server',response)});need(len(raw)<=RESPONSE_LIMIT,'RESPONSE-BOUND')
 with self.transaction():self.db.execute('UPDATE journal SET response=? WHERE challenge=?',(raw,r['challenge']))
 return raw
""",'exec')
 src=cat['source'];wr=wrapper.body[0];lock=run.body[0];ready,tr=lock.body;pre,assign,post,ret=tr.body;handler=tr.handlers[0];quarantine=handler.body[0].value
 for k,n in {'wrapper':wrapper,'wrapper_return':wr,'wrapper_call':wr.value}.items():mc(src[k],n)
 rs=src['run_source']
 for k,n in {'run':run,'readiness_program':mm['_require'],'readiness_call':ready.value,'try_region':tr,'handler':handler,'result_assignment':assign,'run_return':ret,'dispatch':assign.value,'dispatch_receiver':assign.value.func.args[0]}.items():mc(rs[k],n)
 stages={'lock_enter':lock.items[0].context_expr,'readiness':ready,'pre_transaction':pre,'dispatch':assign.value,'post_transaction':post,'return_expression':ret,'handler_reason':quarantine.args[0],'quarantine':quarantine,'reraise':handler.body[1],'lock_exit':lock}
 for k,n in stages.items():mc(rs['stages'][k],n)
 assert rs['normal_path']==['lock_enter','readiness','pre_transaction','dispatch','post_transaction','return_expression','lock_exit'] and rs['caught_stages']==['pre_transaction','dispatch','post_transaction','return_expression'] and rs['outside_handler']==['lock_enter','readiness','lock_exit']
 assert rs['result_local']=='result' and rs['ready_phase']=='READY'
 bt=one(n for n in backend.body if isinstance(n,ast.Try));bi=backend.body.index(bt);reserve=backend.body[bi-1];raw,bound,persist,br=backend.body[bi+1:];success=bt.body[-1];error=bt.handlers[0].body[0]
 for k,n in {'backend':backend,'backend_return':br,'raw_assignment':raw}.items():ac(src[k],n)
 for k,n in {'success':success,'error':error}.items():ac(src['response_assignments'][k],n)
 backstages={'authenticate':backend.body[:bi-1],'reserve':reserve,'action':bt.body[:-1],'success_response':success,'error_response':error,'encode_sign':raw,'response_bound':bound,'persist':persist,'return_raw':br}
 assert set(src['backend_stages'])==set(backstages)
 for k,n in backstages.items():
  if isinstance(n,list):
   assert len(n)==len(src['backend_stages'][k])
   for nn,rr in zip(n,src['backend_stages'][k]):ac(rr,nn)
  else:ac(src['backend_stages'][k],n)
 assert src['backend_program']==ast.dump(backend,include_attributes=False)
 const={t.id:ast.literal_eval(n.value) for n in ast.parse(authority).body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name) and t.id in ('VERSION','REQUEST_LIMIT','RESPONSE_LIMIT')}
 assert src['constants']==const and src['method']=='handle' and src['parameter_names']==['packet','inject'] and src['default_inject'] is None
 at=ast.parse(authority)
 seed=one(n for n in at.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SEEDS' for t in n.targets))
 same_ast(seed,"SEEDS={x:hashlib.sha256(('PUBLIC-LAB-ONLY-'+x).encode()).digest() for x in ['executor','observer','server']}",'exec')
 for name,program in [('public','def public(seed):return Ed25519PrivateKey.from_private_bytes(seed).public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)'),('sig',"def sig(who,x):return Ed25519PrivateKey.from_private_bytes(SEEDS[who]).sign(VERSION.encode()+b'\\0'+enc(x)).hex()")]:same_ast(one(n for n in at.body if isinstance(n,ast.FunctionDef) and n.name==name),program,'exec')
 an=ast.parse(anchor);encoder=one(n for n in an.body if isinstance(n,ast.FunctionDef) and n.name=='enc');parser=one(n for n in an.body if isinstance(n,ast.FunctionDef) and n.name=='parse')
 same_ast(encoder,"def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\\n').encode()",'exec');assert src['encoder']==ast.get_source_segment(anchor.decode(),encoder)
 parser_text=ast.unparse(parser);assert 'type(b) is bytes' in parser_text and 'enc(x) == b' in parser_text and "need(k not in d, 'DUPLICATE')" in parser_text
 ot=ast.parse(observations);edge=one(n for n in ot.body if isinstance(n,ast.FunctionDef) and n.name=='source_edges');helpers={n.name:n for n in edge.body if isinstance(n,ast.FunctionDef) and n.name in ('exact_bytes','decode','signature')}
 assert set(src['auth_helper_programs'])==set(helpers)
 for n,node in helpers.items():assert src['auth_helper_programs'][n]==ast.get_source_segment(observations.decode(),node)
 loop=one(n for n in edge.body if isinstance(n,ast.For) and "'RETURN-REQUEST'" in ast.unparse(n));assert src['auth_check_program']==ast.get_source_segment(observations.decode(),loop)
 assert "b.hex() == v['bytes_hex']" in ast.unparse(helpers['exact_bytes']) and 'enc(v) == b' in ast.unparse(helpers['decode'])
 assert "type(r.get('ok')) is bool" in ast.unparse(loop) and "same(r['request'], mc.digest(packet), 'RETURN-REQUEST')" in ast.unparse(loop) and "same(r['challenge'], request['challenge'], 'RETURN-CHALLENGE')" in ast.unparse(loop)
 inherited={x['template_id']:x for x in model['existing_declarations'] if x['template_id'] in ('PACKET:','PACKET:#exact_bytes','REQUEST:','RESPONSE:','RESPONSE:#exact_bytes','SUCCESS-RESPONSE:','ERROR-RESPONSE:')};assert cat['inherited_declarations']==inherited and len(inherited)==7
 assert inherited['RESPONSE:#exact_bytes']['native_template']['type']=='STRING'
 origins=[src['backend_return'],rs['result_assignment'],src['wrapper_return']]
 assert len(cat['declarations'])==3
 for row,n,o in zip(cat['declarations'],('underlying-response','run-result','wrapper-return'),origins):
  assert row['id']==n and row['origin']==o and row['type']=='STRING' and row['logical_type']=='exact Python bytes' and row['classification']=='UNKNOWN' and row['ordinal'] is row['multiplicity'] is None
 assert [(x['from'],x['to']) for x in cat['links']]==[('underlying-response','run-result'),('run-result','wrapper-return')]
 delegation=one(x for x in producer['delegations'] if x['from']=='ManagedAuthority.handle -> _run');assert cat['delegation']==delegation and delegation['to']=='Authority.handle -> apply/sign and response persistence'
 assert cat['reference_links']['ready']==one(x for x in refs['source']['calls'] if x['site']==key(ready.value)) and cat['reference_links']['live_read']==one(x for x in refs['source']['reference_reads'] if x['site']==key(assign.value.func.args[0]))
 assert cat['arguments']['run_to_backend']==['packet','inject'] and cat['runtime_links'] is None and cat['actual_admission'] is cat['complete_repetition_coverage'] is False
 return {'result':'PASS','wrapper':ast.get_source_segment(manager.decode(),wrapper),'run':ast.get_source_segment(manager.decode(),run),'backend':ast.get_source_segment(authority.decode(),backend),'source_constants':const,'packet_parser':ast.get_source_segment(anchor.decode(),parser),'encoder':ast.get_source_segment(anchor.decode(),encoder),'backend_source_guards_and_continuations_independently_checked':True,'source_derivation_not_runtime_execution':True,'origins':[x['site'] for x in origins],'reference_links':copy.deepcopy(cat['reference_links']),'inherited_declarations':copy.deepcopy(inherited),'type_scope':'Exact source-produced bytes; existing declaration records bytes as lowercase hex STRING; packet canonical parse; inject has no source type check at wrapper/backend entry; method/action semantics remain predecessor scope','guard_scope':'Inner Exception becomes error response only when handler and encode/persist/return complete; outside failures and BaseException escape; lock exit is required; no guarantee of cleanup/nonexecution'}

