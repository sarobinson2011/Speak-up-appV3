"""New client-state correspondence controls only; constructed objects are not observations."""
import argparse,ast,copy,hashlib,json,runpy,sys,time,types
from pathlib import Path
def module(path):
 m=types.ModuleType('_client_state_control');m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def identity(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--write',action='store_true');p.add_argument('--recovered',action='store_true');a=p.parse_args();a.root=a.root.resolve();a.output.mkdir(parents=True,exist_ok=False)
 runpy.run_path(str(a.root/'tests/guard.py'))['install'](a.root)
 start=time.monotonic();checks=[];cases=[];error=None
 def check(label,fn):
  result=fn();assert result is not False,label;row={'check':label,'result':'PASS'};checks.append(row)
  with (a.output/'progress.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  print(len(checks),label,flush=True);return result
 def reject(fn):
  try:fn()
  except ValueError:return True
  raise AssertionError('Unexpected acceptance')
 try:
  m=module(a.root/'code/correspondence.py');d=m.inputs(a.root);cat=m.catalogue(d);c=d['coverage'];launch,entry=m.sources(d)
  lt=ast.parse(launch);et=ast.parse(entry);session=next(n for n in lt.body if isinstance(n,ast.ClassDef) and n.name=='ManagedSession');client=next(n for n in et.body if isinstance(n,ast.ClassDef) and n.name=='Client');ds=next(n for n in et.body if isinstance(n,ast.FunctionDef) and n.name=='_data');dispatch=next(n for n in et.body if isinstance(n,ast.FunctionDef) and n.name=='_dispatch')
  ss=next(n for n in session.body if isinstance(n,ast.FunctionDef) and n.name=='state');cs=next(n for n in client.body if isinstance(n,ast.FunctionDef) and n.name=='state');tr=next(n for n in dispatch.body if isinstance(n,ast.Try))
  check('independent source: session direct no-argument state forwarding',lambda:ast.unparse(ss.body[0])=='return self.__managed.state()')
  check('independent source: client state literal and None packet',lambda:ast.unparse(cs.body[0])=="return _dispatch(self.__token, 'state', None)")
  check('independent source: state result shape and conversion inside catch',lambda:ast.unparse(tr.body[2])=='result = owner.wrapper.state()' and ast.unparse(tr.body[3].test)=='type(result) is not dict or set(result) != _STATE_KEYS' and ast.unparse(tr.body[4])=='return _data(result)' and ast.unparse(tr.handlers[0].type)=='BaseException')
  body=ds.body[1:];check('independent source: exact primitive/list/dict branches and unsupported raise',lambda:ast.unparse(body[0].test)=='type(value) in (str, int, bool, type(None))' and isinstance(body[1].body[0].value,ast.ListComp) and isinstance(body[2].body[0].value,ast.DictComp) and ast.unparse(body[3])=="raise RuntimeError('UNSUPPORTED-CLIENT-VALUE')")
  check('independent source: no deepcopy or memo and no extra forwarding args',lambda:not any(isinstance(n,ast.Name) and n.id in ('copy','deepcopy','memo') for n in ast.walk(ds)) and not ss.body[0].value.args)
  check('source-regenerated catalogue accepts',lambda:c.validate_client_state(launch,entry,m.manager_state(d),d['prior_module'].catalogue(d['prior_data']),m.inner(d)['ctx']['binding'],cat))
  for label,mut in [('missing branch',lambda x:x['source']['data_branches'].pop('dict')),('wrong primitive type',lambda x:x['source']['data_primitives'].append('float')),('deepcopy alias claim',lambda x:x['copy_semantics'].update(algorithm='deepcopy with memo')),('omitted hop',lambda x:x['ordered_hops'].pop()),('stale source origin',lambda x:x['source']['stages']['conversion'].update(site='wrong'))]:
   bad=copy.deepcopy(cat);mut(bad);check('source contract rejects '+label,lambda bad=bad:reject(lambda:c.validate_client_state(launch,entry,m.manager_state(d),d['prior_module'].catalogue(d['prior_data']),m.inner(d)['ctx']['binding'],bad)))
  # Domain and graph tests use hand-built independent expected objects.
  ordinary=[None,True,False,0,-11,'arbitrary reason/content '*120,[],{},[1,False,None,'x'],{'z':1,'a':[None,True]}]
  for i,value in enumerate(ordinary):
   output=copy.deepcopy(value);check('legitimate exact data domain '+str(i),lambda value=value:c.data_source_domain(cat,value)['normal_return_domain']);check('legitimate detachment graph '+str(i),lambda value=value,output=output:c.validate_data_detachment(c.copy_graph(value,output))['result']=='PASS')
  hooks=[]
  class Trap(str):
   def __repr__(self):hooks.append('repr');raise AssertionError('hook')
   def __deepcopy__(self,memo):hooks.append('copy');raise AssertionError('hook')
  for label,value in [('float',1.0),('bytes',b'x'),('tuple',(1,)),('int-key',{1:'x'}),('subclass',Trap('x'))]:
   dom=c.data_source_domain(cat,value);check('source rejection domain '+label,lambda dom=dom:dom['normal_return_domain'] is False and dom['source_defined_raise_if_reached']=={'type':'RuntimeError','message':'UNSUPPORTED-CLIENT-VALUE'})
  check('unsupported objects invoke no copy or repr hooks',lambda:not hooks)
  shared=[1,{'k':True}];inp={'left':shared,'right':shared};out={'left':[1,{'k':True}],'right':[1,{'k':True}]};graph=c.copy_graph(inp,out);relation=check('repeated input alias is unfolded by path',lambda:c.validate_data_detachment(graph));check('output occurrences exceed distinct aliased input containers',lambda:relation['output_container_occurrences']>relation['input_distinct_containers'])
  for label,output in [('deepcopy memo alias',copy.deepcopy(inp)),('shallow copy',dict(inp)),('unchanged input',inp)]:check('reject '+label,lambda output=output:reject(lambda:c.validate_data_detachment(c.copy_graph(inp,output))))
  distinct={'left':[1],'right':[1]};merged=[1];check('reject merging distinct output copies',lambda:reject(lambda:c.validate_data_detachment(c.copy_graph(distinct,{'left':merged,'right':merged}))))
  for label,output in [('bool/int type',{'z':True}),('changed value',{'z':2}),('key order',{'a':2,'z':1})]:
   input_value={'z':1,'a':2} if label=='key order' else {'z':1};check('reject detachment '+label,lambda input_value=input_value,output=output:reject(lambda:c.validate_data_detachment(c.copy_graph(input_value,output))))
  cyclic=[];cyclic.append(cyclic);other=[];other.append(other);dom=c.data_source_domain(cat,cyclic)
  check('cycle has no finite normal traversal but no invented exception',lambda:not dom['normal_return_domain'] and dom['source_defined_raise_if_reached'] is None)
  check('cycle normal-copy claim rejects',lambda:reject(lambda:c.validate_data_detachment(c.copy_graph(cyclic,other))))
  # One full predecessor-bound semantic derivation for this new campaign.
  rows,basis=check('mandatory predecessor-bound semantic rows',lambda:m._checked(d,cat));bundle=check('current derivation assembly',lambda:m._assemble(d,rows,basis));raw=m.enc(bundle);receipt=a.root/'results/client-state-correspondence.json'
  if a.write:
   with receipt.open('xb') as f:f.write(raw)
  else:check('recovered exact saved derivation',lambda:raw==receipt.read_bytes())
  check('both contexts independent and predecessor preserved',lambda:[x['context'] for x in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and all(all(m.enc(x[k])==m.enc(v) for k,v in old.items()) for x,old in zip(bundle['contexts'],basis['prior']['contexts'])))
  check('no fabricated runtime or observer joins',lambda:all(r['runtime_forwarding_links'] is None and r['observer_to_forwarding_links'] is None and r['separate_observer']['frame'] is None and r['actual_client_state_call_count'] is None for r in rows))
  normal={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'normal','post_transaction':False,'return_expression':'normal','lock_exit':'normal'}
  order=['client-call','owner-lookup','owner-guard','operation-check','session-call','manager-call','session-return','state-shape','conversion','dispatch-return','client-return']
  for index,row in enumerate(rows):
   context=row['context'];anchor=row['validated_state_anchor'];state=anchor['validated_state'];occ='constructed-client-state:'+context+':normal';scope=m.invocation_scope(anchor,occ)
   refs={n:{'kind':'state-result-reference' if n.endswith('result') else n+'-reference','scope':copy.deepcopy(scope),'symbol':n+'-symbol'} for n in ['client','token','owner','session','manager','manager-result','data-result']}
   for akey,bkey in cat['reference_edges']:refs[akey]=copy.deepcopy(refs[bkey])
   refs['owner_failed']=False;live={'kind':'authority-reference','scope':copy.deepcopy(scope),'symbol':'live-authority'};ref=refs['manager-result']
   mr={'method':'state','args':[],'phase':'READY','live_reference':live,'retired_reference':None,'outcomes':dict(normal),'underlying':{'receiver':copy.deepcopy(live),'value':copy.deepcopy(state),'reference':copy.deepcopy(ref)},'run_result':{'value':copy.deepcopy(state),'reference':copy.deepcopy(ref)},'wrapper_return':{'value':copy.deepcopy(state),'reference':copy.deepcopy(ref)}}
   projection={'occurrence':occ,'scope':scope,'references':refs,'outcomes':dict.fromkeys(order,'normal'),'manager_case':{'outcomes':dict(normal),'returned':mr},'detachment':{'input_reference':copy.deepcopy(ref),'output_reference':copy.deepcopy(refs['data-result']),'graph':c.copy_graph(state,copy.deepcopy(state))},'callback':'unobserved','cleanup':dict.fromkeys(['revoke','format','cleanup','write','outer_fail'],'unobserved')}
   case={'kind':'CONSTRUCTED-CONDITIONAL-CLIENT-STATE','context':context,'anchor':copy.deepcopy(anchor),'projection':projection};validated={'scope':scope,'state':state}
   def project(p):return c.client_state_projection(cat,p,validated)
   value=check('legitimate source-bound forwarding '+context,lambda:m._construct_checked(basis,rows,case));out=value['projection'];cases.append({'input':copy.deepcopy(case),'result':copy.deepcopy(value)})
   check('six ordered hops and exact validated state '+context,lambda:[h['declaration'] for h in out['hops']]==cat['ordered_hops'] and all(h['value']==state for h in out['hops']))
   check('reference/copy split and request-independent invocation '+context,lambda:all(h['reference']==ref for h in out['hops'][:3]) and all(h['reference']==refs['data-result'] for h in out['hops'][3:]) and out['request_or_journal_row_required'] is False and 'request' not in scope)
   mutations=[('missing hop',lambda x:x['hops'].pop()),('reordered hops',lambda x:x['hops'].reverse()),('wrong method',lambda x:x['arguments'][0].update(operation='handle')),('extra packet',lambda x:x['arguments'][0].update(packet='request')),('copy reference substitution',lambda x:x['hops'][-1].update(reference=copy.deepcopy(ref))),('invented observation',lambda x:x.update(runtime_observation=True)),('wrong destination',lambda x:x['destinations'][0].update(to='stdout')),('false exception evidence',lambda x:x['outcome_classification'].update(runtime_python_unwind_evidence='ESTABLISHED'))]
   for label,mut in mutations:
    bad=copy.deepcopy(out);mut(bad);check('output rejects '+label+' '+context,lambda bad=bad:reject(lambda:c.validate_client_state_projection(cat,projection,validated,bad)))
   for label,mut in [('missing copy',lambda x:x.update(detachment=None)),('missing manager',lambda x:x.update(manager_case=None)),('wrong method delegation',lambda x:x['manager_case']['returned'].update(method='handle')),('wrong nested type',lambda x:x['manager_case']['returned']['run_result']['value']['counts'].update(query=True)),('wrong instance scope',lambda x:x['scope']['instance'].update(binding='f'*64)),('missing stage',lambda x:x['outcomes'].pop('state-shape')),('extra stage',lambda x:x['outcomes'].update(handle='normal')),('shallow copy',lambda x:x['detachment'].update(graph=c.copy_graph(state,state))),('same copy reference',lambda x:x['references']['data-result'].update(symbol=ref['symbol']))]:
    bad=copy.deepcopy(projection);mut(bad);check('input rejects '+label+' '+context,lambda bad=bad:reject(lambda:project(bad)))
   bad=copy.deepcopy(projection)
   for k in ('underlying','run_result','wrapper_return'):bad['manager_case']['returned'][k]['value']['head']='f'*64
   stale=copy.deepcopy(state);stale['head']='f'*64;bad['detachment']['graph']=c.copy_graph(stale,copy.deepcopy(stale));check('coordinated substituted state graph and manager reject '+context,lambda:reject(lambda:project(bad)))
   badcase=copy.deepcopy(case);badcase['anchor']['instance']['binding']='f'*64;check('wrong-instance independent anchor rejects '+context,lambda:reject(lambda:m._construct_checked(basis,rows,badcase)))
   # Conditional failures are sourced from the state branch, not handle guards.
   for stage in order:
    for disposition in ('raise','process-termination'):
     cut=copy.deepcopy(projection);pos=order.index(stage);cut['outcomes']={n:('normal' if n!=stage else disposition) for n in order[:pos+1]}
     if pos<=order.index('manager-call'):cut['manager_case']=None
     if pos<=order.index('conversion'):cut['detachment']=None
     caught=stage not in ('client-call','owner-lookup','owner-guard','client-return') and disposition=='raise'
     if caught:cut['outcomes'].update({'retain-error':'normal','fixed-failure':'normal'})
     result=check('state path '+stage+' '+disposition+' '+context,lambda cut=cut:project(cut));cl=result['outcome_classification']
     if disposition=='process-termination':assert result['completion']=='process-termination' and not result['outside_catch_failure'] and cl['terminal_python_exception_in_model'] is None and result['evidence_route']['original_reraised_to_launcher'] is None
     elif caught:assert result['completion']=='fixed-client-failure' and result['retained_original'] is True and result['original_exception']['origin']==stage and result['outside_catch_failure'] is False
     else:assert result['outside_catch_failure'] is True and result['completion']=='unqualified-escape'
     assert cl['runtime_python_exception_evidence']==cl['runtime_python_unwind_evidence']=='UNAVAILABLE' and not result['authorization_renewed']
     cases.append({'input':{'projection':copy.deepcopy(cut),'context':context},'result':copy.deepcopy(result)})
   converted_fail=copy.deepcopy(projection);converted_fail['outcomes']={n:('raise' if n=='conversion' else 'normal') for n in order[:order.index('conversion')+1]};converted_fail['detachment']=None
   for stage in ('retain-error','fixed-failure'):
    for disposition in ('raise','process-termination'):
     cut=copy.deepcopy(converted_fail);cut['outcomes']['retain-error']=disposition if stage=='retain-error' else 'normal'
     if stage=='fixed-failure':cut['outcomes']['fixed-failure']=disposition
     result=check('storage/helper '+stage+' '+disposition+' '+context,lambda cut=cut:project(cut));assert result['outside_catch_failure'] is (disposition=='raise') and result['retained_original'] is (None if stage=='retain-error' else True)
   cleanup=copy.deepcopy(converted_fail);cleanup['outcomes'].update({'retain-error':'normal','fixed-failure':'normal'});cleanup['callback']='returns';cleanup['cleanup']=dict.fromkeys(cleanup['cleanup'],'normal');result=check('conditional existing evidence route after conversion failure '+context,lambda:project(cleanup));assert result['evidence_route']['original_reraised_to_launcher'] is True and result['evidence_route']['bytes'] is None
   escaping=copy.deepcopy(converted_fail);escaping['outcomes']=dict.fromkeys(order[:order.index('manager-call')+1],'normal');escaping['outcomes'].update({'retain-error':'normal','fixed-failure':'normal'});escaping['manager_case']={'outcomes':{'lock_enter':'normal','readiness':'raise','lock_exit':'normal'},'returned':None};result=check('existing manager exception guard is reused '+context,lambda:project(escaping));assert result['original_exception']['kind']=='manager-escaping-exception'
   terminated=copy.deepcopy(projection);terminated['outcomes']={'client-call':'process-termination'};terminated['manager_case']=terminated['detachment']=None;terminated['callback']='returns';check('no callback after termination '+context,lambda:reject(lambda:project(terminated)))
   changed=copy.deepcopy(out);changed['hops'][0]['value']['counts'].clear();changed['copy_relation']['container_path_pairs'].clear();check('nested returned mutations leave projection expectations isolated '+context,lambda:project(projection)['hops'][0]['value']==state and bool(project(projection)['copy_relation']['container_path_pairs']))
   for label,mut in [('missing link',lambda x:x['conditional_links'].pop()),('reordered links',lambda x:x['conditional_links'].reverse()),('wrong instance',lambda x:x['validated_state_anchor']['instance'].update(binding='f'*64)),('stale head',lambda x:x['validated_state_anchor']['validated_state'].update(head='f'*64)),('fabricated observer join',lambda x:x.update(observer_to_forwarding_links=['invented']))]:
    bad=copy.deepcopy(rows);mut(bad[index]);check('semantic row rejects '+label+' '+context,lambda bad=bad:reject(lambda:m._check_rows(basis,bad,m._rows(basis))))
  # Same validated predecessor, not seven mutually agreeing substituted reports.
  evidence=dict(basis['evidence']);path='evidence/recovery-export-0.json';export=json.loads(evidence[path]);head=json.loads(bytes.fromhex(export['head']));head['head']='f'*64;export['head']=m.enc(head).hex();evidence[path]=m.enc(export)
  check('coordinated evidence substitution rejects before broad archive equality',lambda:reject(lambda:m._compare_evidence(basis,evidence)))
  missing=dict(basis['evidence']);missing.pop(path);check('missing HEAD evidence rejects',lambda:reject(lambda:m._compare_evidence(basis,missing)))
  baseline=m.enc(m._rows(basis));returned=m._rows(basis);returned[0]['conditional_links'][0]['conditional_value_at_validated_frontier'].clear();returned.reverse();check('nested semantic output mutation preserves independent contexts',lambda:m.enc(m._rows(basis))==baseline)
  bad=copy.deepcopy(bundle);bad['contexts'][0].pop('client_state_return_correspondence');check('public omitted mandatory relation rejects',lambda:reject(lambda:m.validate(a.root,m.enc(bad))))
  check('old predecessor public receipt rejects as current',lambda:reject(lambda:m.validate(a.root,basis['saved'])))
  if a.recovered:check('recovered public validator accepts current saved receipt',lambda:m.validate(a.root,receipt.read_bytes()))
 except BaseException as ex:error=repr(ex);raise
 finally:
  result={'result':'PASS' if error is None else 'FAIL','checks':len(checks),'rows':checks,'error':error,'seconds':time.monotonic()-start,'mode':'recovered' if a.recovered else 'primary','source':{n:identity((a.root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'constructed_not_runtime':True,'requests':0,'database_connections':0,'session_operations':0,'completed_suites_rerun':False}
  (a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(a.output/'cases.json').write_text(json.dumps(cases,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('result','checks','seconds','error')}),flush=True)
if __name__=='__main__':main()
