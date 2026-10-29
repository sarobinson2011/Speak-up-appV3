"""Fresh reviewer controls; pure AST-extracted _data oracle, no application/session calls."""
from pathlib import Path
import ast,copy,json,sys,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None

def graph(a,b):
 nodes={};memo={}
 def add(v):
  if type(v) in (list,dict):
   if id(v) in memo:return {'ref':memo[id(v)]}
   n='R'+str(len(memo));memo[id(v)]=n;nodes[n]={'kind':'dict' if type(v) is dict else 'list','items':[]}
   nodes[n]['items']=[[k,add(x)] for k,x in v.items()] if type(v) is dict else [add(x) for x in v]
   return {'ref':n}
  return {'atom':type(v).__name__,'value':v}
 return {'roots':[add(a),add(b)],'nodes':nodes}

def normal_case(anchor,ctx,invoke,source_data):
 scope={'context':ctx,'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':invoke}
 names=['client','token','owner','session','manager','manager-result','data-result'];refs={n:{'kind':'state-result-reference' if n.endswith('result') else n+'-reference','scope':copy.deepcopy(scope),'symbol':'independent/'+invoke+'/'+n} for n in names}
 for a,b in [('client.token','token'),('owners[token]','owner'),('owner.wrapper','session'),('session.managed','manager')]:refs[a]=copy.deepcopy(refs[b])
 refs['owner_failed']=False;live={'kind':'authority-reference','scope':copy.deepcopy(scope),'symbol':'independent/live'};s=anchor['validated_state'];r=refs['manager-result']
 mp={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'normal','post_transaction':False,'return_expression':'normal','lock_exit':'normal'}
 mr={'method':'state','args':[],'phase':'READY','live_reference':live,'retired_reference':None,'outcomes':dict(mp),'underlying':{'receiver':copy.deepcopy(live),'value':copy.deepcopy(s),'reference':copy.deepcopy(r)},'run_result':{'value':copy.deepcopy(s),'reference':copy.deepcopy(r)},'wrapper_return':{'value':copy.deepcopy(s),'reference':copy.deepcopy(r)}}
 return {'occurrence':invoke,'scope':scope,'references':refs,'outcomes':dict.fromkeys(ORDER,'normal'),'manager_case':{'outcomes':dict(mp),'returned':mr},'detachment':{'input_reference':copy.deepcopy(r),'output_reference':copy.deepcopy(refs['data-result']),'graph':graph(s,source_data(s))},'callback':'unobserved','cleanup':dict.fromkeys(CLEAN,'unobserved')}
ORDER=['client-call','owner-lookup','owner-guard','operation-check','session-call','manager-call','session-return','state-shape','conversion','dispatch-return','client-return']
CLEAN=['revoke','format','cleanup','write','outer_fail']
HOPS=['manager-return','session-return','dispatch-result','converted-result','dispatch-return','client-return']

def cutcase(p,stage,outcome):
 q=copy.deepcopy(p);i=ORDER.index(stage);q['outcomes']={n:outcome if n==stage else 'normal' for n in ORDER[:i+1]}
 if i<=ORDER.index('manager-call'):q['manager_case']=None
 if i<=ORDER.index('conversion'):q['detachment']=None
 if outcome=='raise' and stage not in ('client-call','owner-lookup','owner-guard','client-return'):q['outcomes'].update({'retain-error':'normal','fixed-failure':'normal'})
 return q

try:
 monitor=guard(root);m=module(root/'code/correspondence.py');monitor(m);d=m.inputs(root);c=d['coverage'];cat=m.catalogue(d);launcher,entry=m.sources(d)
 et=ast.parse(entry);lt=ast.parse(launcher)
 def fn(tree,name,cls=None):return next(n for n in (next(x.body for x in tree.body if isinstance(x,ast.ClassDef) and x.name==cls) if cls else tree.body) if isinstance(n,ast.FunctionDef) and n.name==name)
 cs=fn(et,'state','Client');ss=fn(lt,'state','ManagedSession');dispatch=fn(et,'_dispatch');data=fn(et,'_data');tr=next(x for x in dispatch.body if isinstance(x,ast.Try));keynode=next(n for n in et.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_STATE_KEYS' for t in n.targets));keys=ast.literal_eval(keynode.value.args[0]);statebranch=tr.body[1:]
 rec.check('source client state passes token, state, None exactly',lambda:ast.unparse(cs.body[0])=="return _dispatch(self.__token, 'state', None)")
 rec.check('source session forwards same manager result without conversion',lambda:ast.unparse(ss.body[0])=='return self.__managed.state()')
 rec.check('source state selection, exact shape and conversion occur inside BaseException catch',lambda:[ast.unparse(x) for x in statebranch]==["if operation != 'state':\n    raise RuntimeError('CLIENT-OPERATION')",'result = owner.wrapper.state()',"if type(result) is not dict or set(result) != _STATE_KEYS:\n    raise RuntimeError('STATE-SHAPE')",'return _data(result)'] and ast.unparse(tr.handlers[0].type)=='BaseException')
 rec.check('source owner lookup and guard precede protected branch',lambda:ast.unparse(dispatch.body[0])=='owner = _OWNERS.get(token)' and ast.unparse(dispatch.body[1].test)=='owner is None or owner.failure is not None')
 rec.check('source handler retains original and only then intentional fixed helper',lambda:ast.unparse(tr.handlers[0].body[0])=='owner.failure = error' and ast.unparse(dispatch.body[-1])=='_fail()' and isinstance(fn(et,'_fail').body[0],ast.Raise))
 # Exact pure function extracted by AST: no import or operational body runs.
 pure=ast.Module(body=[copy.deepcopy(data)],type_ignores=[]);ns={};exec(compile(ast.fix_missing_locations(pure),'independent-extracted-data-oracle','exec'),ns);source_data=ns['_data']
 rec.check('catalogue keys/types/hops match independently parsed source chain',lambda:set(cat['source']['state_keys'])==set(keys) and cat['ordered_hops']==HOPS and all(x['type']==cat['manager_relation']['inherited_head']['native_template']['type'] for x in cat['declarations']))
 rec.check('generated source declaration validates against defining bytes',lambda:c.validate_client_state(launcher,entry,m.manager_state(d),d['prior_module'].catalogue(d['prior_data']),m.inner(d)['ctx']['binding'],cat))
 expected={'client-call':cs.body[0],'client-return':cs.body[0],'owner-lookup':dispatch.body[0],'owner-guard':dispatch.body[1],'operation-check':statebranch[0],'session-call':statebranch[1],'manager-call':ss.body[0],'session-return':ss.body[0],'state-shape':statebranch[2],'conversion':statebranch[3].value,'dispatch-return':statebranch[3],'retain-error':tr.handlers[0].body[0]}
 for stage,node in expected.items():rec.check('source anchor and order '+stage,lambda stage=stage,node=node:cat['source']['stages'][stage]['site']==f'{node.lineno}:{node.col_offset}:{node.end_lineno}:{node.end_col_offset}:{type(node).__name__}')
 rec.save('source-oracle.json',{'entry':identity(entry),'launcher':identity(launcher),'data_ast':ast.dump(data,include_attributes=False),'source_hops':HOPS,'state_keys':keys,'independent_stage_sites':{k:f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}' for k,n in expected.items()},'pure_source_extraction_is_constructed_not_runtime':True})
 shared=[{'inner':[]},False];values=[None,False,True,0,-7,2**160,'', 'x\u0000\nΩ',[],{},[1,None,False],{'z':[],'a':{'n':1}}, {'left':shared,'right':shared},[[],[]]]
 for i,v in enumerate(values):
  out=source_data(v);g=graph(v,out);res=c.validate_data_detachment(g);dom=c.data_source_domain(cat,v)
  rec.check('pure source and graph exact detachment '+str(i),lambda res=res,dom=dom:res['result']=='PASS' and dom['normal_return_domain'] and not dom['resource_completion_established'] and not res['runtime_observation'])
  if type(v) in (list,dict):rec.check('mutable root copied '+str(i),lambda v=v,out=out:out is not v)
 rec.check('repeated nested alias splits at every visited path',lambda:source_data(values[12])['left'] is not source_data(values[12])['right'])
 actual=source_data(values[12]);rec.check('single output repeated aliases split including nested empty containers',lambda:actual['left'] is not actual['right'] and actual['left'][0] is not actual['right'][0] and actual['left'][0]['inner'] is not actual['right'][0]['inner'])
 for label,v,o in [('deepcopy memo',values[12],copy.deepcopy(values[12])),('shallow copy',values[12],dict(values[12])),('same object',values[12],values[12])]:rec.reject('detachment rejects '+label,lambda v=v,o=o:c.validate_data_detachment(graph(v,o)))
 inp={'x':[],'y':[]};z=[];rec.reject('distinct equal input containers cannot merge',lambda:c.validate_data_detachment(graph(inp,{'x':z,'y':z})))
 for label,a,b in [('key-order',{'z':1,'a':2},{'a':2,'z':1}),('bool-int',[True],[1]),('container-kind',[],{}),('changed-value',{'x':'é'},{'x':'e\u0301'})]:rec.reject('exact graph '+label,lambda a=a,b=b:c.validate_data_detachment(graph(a,b)))
 hooks=[]
 class StringSubclass(str):
  def __deepcopy__(self,m):hooks.append('copy');raise AssertionError('hook')
  def __repr__(self):hooks.append('repr');raise AssertionError('hook')
 class ListSubclass(list):pass
 class DictSubclass(dict):pass
 class IntSubclass(int):pass
 badvalues=[1.5,b'x',bytearray(b'x'),(1,),{1},StringSubclass('x'),ListSubclass([1]),DictSubclass(x=1),IntSubclass(1),{1:'x'},{True:'x'},{None:'x'},{StringSubclass('k'):1}, {'first':[None,1.5],'last':0}]
 for i,v in enumerate(badvalues):
  try:source_data(v)
  except RuntimeError as e:assert str(e)=='UNSUPPORTED-CLIENT-VALUE'
  else:raise AssertionError('oracle expected unsupported')
  dom=c.data_source_domain(cat,v);rec.check('source exact-type unsupported '+str(i),lambda dom=dom:not dom['normal_return_domain'] and dom['source_defined_raise_if_reached']=={'type':'RuntimeError','message':'UNSUPPORTED-CLIENT-VALUE'})
 rec.check('unsupported subclasses invoke no repr or copy hooks',lambda:not hooks)
 cyc=[];cyc.append(cyc);cycd={};cycd['self']=cycd
 for i,v in enumerate([cyc,cycd]):
  dom=c.data_source_domain(cat,v);rec.check('cycle analysis asserts no exact terminal exception '+str(i),lambda dom=dom:not dom['normal_return_domain'] and dom['source_defined_raise_if_reached'] is None)
  rec.reject('cycle cannot claim finite normal output '+str(i),lambda v=v:c.validate_data_detachment(graph(v,[])))
 g=graph({'x':[False]}, {'x':[False]})
 for label,mut in [('extra-node',lambda x:x['nodes'].update(extra={'kind':'list','items':[]})),('missing-node',lambda x:x['nodes'].pop(x['roots'][1]['ref'])),('wrong-atom-type',lambda x:x['nodes']['R3']['items'][0].update(atom='int')),('duplicate-key',lambda x:x['nodes']['R2']['items'].append(copy.deepcopy(x['nodes']['R2']['items'][0])) )]:
  bad=copy.deepcopy(g);mut(bad);rec.reject('graph structural rejection '+label,lambda bad=bad:c.validate_data_detachment(bad))
 # One mandatory checked basis for these focused helper tests. Never patched/cached by replacing candidate functions.
 rows,basis=rec.check('full current predecessor validation before independent cases',lambda:m._checked(d,cat));bundle=m._assemble(d,rows,basis);raw=(root/'results/client-state-correspondence.json').read_bytes()
 rec.check('derived receipt equals exact saved current bytes',lambda:enc(bundle)==raw)
 rec.check('predecessor context contents preserved without edits',lambda:all(all(enc(new[k])==enc(v) for k,v in old.items()) for new,old in zip(bundle['contexts'],basis['prior']['contexts'])))
 rec.check('both ordered contexts and observer remains unjoined',lambda:[r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and all(r['runtime_forwarding_links'] is None and r['observer_to_forwarding_links'] is None and r['separate_observer']['frame'] is None and r['actual_client_state_call_count'] is None for r in rows))
 cases=[]
 for idx,row in enumerate(rows):
  ctx=row['context'];anchor=row['validated_state_anchor'];state=anchor['validated_state'];p=normal_case(anchor,ctx,'independent-state-'+str(idx),source_data);validated={'scope':copy.deepcopy(p['scope']),'state':copy.deepcopy(state)}
  case={'kind':'CONSTRUCTED-CONDITIONAL-CLIENT-STATE','context':ctx,'anchor':copy.deepcopy(anchor),'projection':copy.deepcopy(p)}
  def project(q):return c.client_state_projection(cat,q,validated)
  out=rec.check('legitimate bound constructed state '+ctx,lambda:m._construct_checked(basis,rows,case))['projection'];cases.append({'input':case,'result':out})
  rec.check('six ordered hops exact HEAD and reference-copy split '+ctx,lambda:[h['declaration'] for h in out['hops']]==HOPS and all(h['value']==state for h in out['hops']) and all(h['reference']==p['references']['manager-result'] for h in out['hops'][:3]) and all(h['reference']==p['references']['data-result'] for h in out['hops'][3:]))
  rec.check('normal is not runtime/authorization proof '+ctx,lambda:out['completion']=='normal' and out['outcome_classification']['terminal_python_exception_in_model'] is False and out['runtime_observation'] is False and out['authorization_renewed'] is False and out['actual_admission'] is False)
  p2=normal_case(anchor,ctx,'independent-state-second-'+str(idx),source_data);out2=c.client_state_projection(cat,p2,{'scope':p2['scope'],'state':state})
  rec.check('equal HEAD values retain distinct invocation occurrence identities '+ctx,lambda:out['hops'][0]['id']!=out2['hops'][0]['id'] and out['hops'][0]['value']==out2['hops'][0]['value'])
  changes=[('missing-copy',lambda x:x.update(detachment=None)),('missing-manager',lambda x:x.update(manager_case=None)),('wrong-method',lambda x:x['manager_case']['returned'].update(method='handle')),('wrong-args',lambda x:x['manager_case']['returned'].update(args=[None])),('wrong-phase',lambda x:x['manager_case']['returned'].update(phase='CLOSED')),('int-bool',lambda x:x['manager_case']['returned']['underlying']['value']['counts'].update(query=True)),('missing-shape',lambda x:x['outcomes'].pop('state-shape')),('wrong-instance',lambda x:x['scope']['instance'].update(binding='f'*64)),('wrong-frontier',lambda x:x['scope'].update(frontier='stale')),('wrong-context',lambda x:x['scope'].update(context=rows[1-idx]['context'])),('wrong-invocation',lambda x:x['scope'].update(invocation='other')),('result-ref-same',lambda x:x['references']['data-result'].update(symbol=x['references']['manager-result']['symbol'])),('shallow-graph',lambda x:x['detachment'].update(graph=graph(state,state))),('stale-owner',lambda x:x['references']['owner.wrapper'].update(symbol='other'))]
  for label,mut in changes:
   q=copy.deepcopy(p);mut(q);rec.reject('path input '+label+' '+ctx,lambda q=q:project(q))
  q=copy.deepcopy(p);stale=copy.deepcopy(state);stale['head']='f'*64
  for name in ['underlying','run_result','wrapper_return']:q['manager_case']['returned'][name]['value']=copy.deepcopy(stale)
  q['detachment']['graph']=graph(stale,source_data(stale));rec.reject('coordinated values and graph cannot replace validated HEAD '+ctx,lambda:project(q),'STATE-VALUE-ORIGIN:/head')
  for label,mut in [('missing-hop',lambda x:x['hops'].pop()),('reordered-hop',lambda x:x['hops'].reverse()),('wrong-argument',lambda x:x['arguments'][0].update(operation='handle')),('wrong-destination',lambda x:x['destinations'][0].update(to='stdout')),('false-observation',lambda x:x.update(runtime_observation=True)),('false-readiness',lambda x:x.update(actual_admission=True)),('copy-memo-claim',lambda x:x['copy_relation'].update(internal_input_aliases_preserved=True))]:
   q=copy.deepcopy(out);mut(q);rec.reject('output contradiction '+label+' '+ctx,lambda q=q:c.validate_client_state_projection(cat,p,validated,q),'PROJECTION-CORRESPONDENCE')
  selected=ORDER if mode=='primary' else ['owner-lookup','session-call','conversion','client-return']
  for stage in selected:
   for outcome in ['raise','process-termination']:
    q=cutcase(p,stage,outcome);r=project(q);cl=r['outcome_classification'];caught=outcome=='raise' and stage not in ('client-call','owner-lookup','owner-guard','client-return')
    rec.check('path classification '+stage+' '+outcome+' '+ctx,lambda r=r,cl=cl,caught=caught,outcome=outcome:r['completion']==('process-termination' if outcome=='process-termination' else 'fixed-client-failure' if caught else 'unqualified-escape') and r['outside_catch_failure']==(outcome=='raise' and not caught) and cl['terminal_python_exception_in_model'] is (None if outcome=='process-termination' else True) and cl['runtime_python_unwind_evidence']=='UNAVAILABLE' and not r['authorization_renewed'])
    if outcome=='process-termination':
     q['callback']='returns';rec.reject('termination cannot establish callback '+stage+' '+ctx,lambda q=q:project(q),'TERMINATION-CONTINUATION')
  for outcome in ('raise','process-termination'):
   for stage in ('retain-error','fixed-failure'):
    q=cutcase(p,'conversion','raise');q['outcomes']['retain-error']=outcome if stage=='retain-error' else 'normal'
    if stage=='retain-error':q['outcomes'].pop('fixed-failure')
    else:q['outcomes']['fixed-failure']=outcome
    r=project(q);rec.check('storage/helper distinction '+stage+' '+outcome+' '+ctx,lambda r=r,stage=stage,outcome=outcome:r['retained_original'] is (None if stage=='retain-error' else True) and r['outside_catch_failure'] is (outcome=='raise') and r['evidence_route']['bytes'] is None)
  q=cutcase(p,'conversion','raise');q['callback']='raises';q['cleanup']=dict.fromkeys(CLEAN,'normal');r=project(q);rec.check('conversion failure preserves conditional original cleanup route '+ctx,lambda:r['original_exception']['origin']=='conversion' and r['evidence_route']['original_reraised_to_launcher'] is True and r['evidence_route']['bytes'] is None and r['evidence_route']['active_marker_removal']=='UNESTABLISHED')
  q=cutcase(p,'manager-call','raise');q['outcomes']['manager-call']='normal';q['manager_case']={'outcomes':{'lock_enter':'normal','readiness':'raise','lock_exit':'normal'},'returned':None};r=project(q);rec.check('manager exceptional result supplies no successful return '+ctx,lambda:r['original_exception']['kind']=='manager-escaping-exception' and not r['hops'])
  q=copy.deepcopy(p);q['outcomes']={n:'normal' for n in ORDER[:3]};q['outcomes']['fixed-failure']='normal';q['references']['owner_failed']=True;q['manager_case']=q['detachment']=None;r=project(q);rec.check('intentional prior-failure refusal is not unexpected raise '+ctx,lambda:r['completion']=='fixed-client-failure' and not r['outside_catch_failure'] and r['original_exception'] is None)
  q=copy.deepcopy(out);q['hops'][0]['value']['counts'].clear();q['copy_relation']['container_path_pairs'].clear();q['scope']['instance']['binding']='stale';rec.check('projection nested mutations isolated '+ctx,lambda:enc(project(p))==enc(out))
  for label,mut in [('omitted-link',lambda x:x['conditional_links'].pop()),('reordered-link',lambda x:x['conditional_links'].reverse()),('wrong-anchor',lambda x:x['validated_state_anchor']['instance'].update(binding='f'*64)),('observer-join',lambda x:x.update(observer_to_forwarding_links=['unobserved'])),('runtime-claim',lambda x:x.update(actual_client_state_call_count=1))]:
   rr=copy.deepcopy(rows);mut(rr[idx]);rec.reject('checked semantic rows '+label+' '+ctx,lambda rr=rr:m._check_rows(basis,rr,m._rows(basis)))
 for label,mut in [('omit-context',lambda x:x.pop()),('duplicate-context',lambda x:x.__setitem__(1,copy.deepcopy(x[0]))),('reverse-context',lambda x:x.reverse())]:
  rr=copy.deepcopy(rows);mut(rr);rec.reject('semantic context domain '+label,lambda rr=rr:m._check_rows(basis,rr,m._rows(basis)))
 for label,mut in [('missing',lambda e:e.pop('evidence/recovery-export-0.json')),('stale',lambda e:e.__setitem__('evidence/recovery-export-0.json',b'{}')),('wrong-type',lambda e:e.__setitem__('evidence/recovery-export-0.json','{}'))]:
  e=dict(basis['evidence']);mut(e);rec.reject('validated evidence '+label,lambda e=e:m._compare_evidence(basis,e))
 rec.save('constructed-cases.json',cases)
 rec.check('actual mandatory predecessor invocation observed',lambda:any(x['function']=='derive_client' for x in CALLS))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,pure_data_oracle_calls_are_constructed_source_tests=True)
