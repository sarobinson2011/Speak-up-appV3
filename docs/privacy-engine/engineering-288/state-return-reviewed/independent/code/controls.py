"""Independent bounded state correspondence checks; saved inputs only."""
from pathlib import Path
import argparse,copy,hashlib,importlib.metadata,json,os,runpy,sys,traceback,types
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def module(p):
 m=types.ModuleType('independent_state');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('output',type=Path);p.add_argument('--recovered',action='store_true');a=p.parse_args();root=a.root.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
 rows=[];error=None;constructed=[];calls=[];kinds={}
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+event)
  if event=='exec' and args[0].co_filename.rsplit('/',1)[-1].lower() in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('PRODUCER-EXECUTION')
  if event=='open' and isinstance(args[0],(str,bytes)):
   name=os.fsdecode(args[0]);flags=args[2] or 0
   if name.startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
   if name.startswith(str(root)+'/') and flags&(os.O_WRONLY|os.O_RDWR|os.O_TRUNC|os.O_CREAT):raise AssertionError('INPUT-WRITE')
 sys.addaudithook(audit)
 def trace(frame,event,arg):
  if event!='call':return
  f=frame.f_code.co_filename;kind=kinds.get(f)
  if kind is None:
   n=f.rsplit('/',1)[-1].lower();kind=1 if n in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') else 2 if n=='prospective_entry.py' else 0;kinds[f]=kind
  name=frame.f_code.co_name
  if kind==1 or kind==2 and name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status'):raise AssertionError('APPLICATION-EXECUTION')
  parent=frame.f_back.f_code.co_name if frame.f_back else None
  if name=='derive_config' and parent=='_basis':calls.append({'function':'mandatory config derive_config','file':f,'source':identity(Path(f).read_bytes())})
  if name=='_compare_evidence' and parent=='_checked' and f==str(root/'code/correspondence.py'):
   l=frame.f_locals;path='evidence/recovery-export-0.json';expected=json.loads(bytes.fromhex(json.loads(l['basis']['evidence'][path])['head']));candidate=l['candidate'];value=None
   try:value=json.loads(bytes.fromhex(json.loads(candidate[path])['head']))
   except (ValueError,TypeError,KeyError):pass
   calls.append({'function':'state comparison','expected':expected,'candidate':value})
 sys.settrace(trace)
 def record(label,category,result,**kw):
  r={'check':label,'category':category,'result':result,**kw};rows.append(r)
  with (out/'progress.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 def check(label,fn,category='independent'):
  v=fn();assert v is not False,label;record(label,category,'PASS');return v
 def reject(label,fn,reason=None,category='negative'):
  try:fn()
  except (ValueError,TypeError,KeyError) as ex:
   if reason is not None:assert str(ex)==reason,(label,str(ex),reason)
   record(label,category,'REJECTED',error={'type':type(ex).__name__,'message':str(ex)});return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+label)
 try:
  assert sys.version_info[:3]==(3,12,14) and not sys.flags.optimize
  m=module(root/'code/correspondence.py');data=m.inputs(root);cat=m.catalogue(data);c=data['coverage'];d=m.inner(data);e=dict(d['ctx']['e']);source={n:identity((root/'code'/n).read_bytes()) for n in ('correspondence.py','managed_coverage.py')}
  oracle=runpy.run_path(str(Path(__file__).with_name('source_oracle.py')));obs=d['ctx']['c']['retained/candidate/compiler/managed_observations.py'];model=d['values']['candidate/managed-route/model.json'];producer=d['values']['candidate/managed-route/producers.json'];refs=d['reference_module'].reference_catalogue(d)
  audit_result=check('independent AST types guards forwarding backend and exception audit',lambda:oracle['audit'](d['manager'],d['authority'],obs,cat,model,producer,refs));(out/'source-audit.json').write_text(json.dumps(audit_result,indent=2)+'\n')
  claims=check('legitimate semantic correspondence',lambda:m.semantic(data,cat));bundle=check('legitimate derivation',lambda:m.derive_state(data,cat));saved=(root/'results/state-correspondence.json').read_bytes();check('derived receipt exact saved bytes',lambda:enc(bundle)==saved)
  public=check('legitimate public validation',lambda:m.validate(root,saved));prior=json.loads((root/'retained/config/results/config-correspondence.json').read_bytes())
  export=json.loads(e['evidence/recovery-export-0.json']);raw=bytes.fromhex(export['head']);state=json.loads(raw);events=json.loads(e['evidence/execution-trace.json'])['events'];hands=json.loads(e['evidence/client-handoff.json'])
  normal={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'normal','post_transaction':False,'return_expression':'normal','lock_exit':'normal'}
  check('exact two ordered contexts',lambda:[x['context'] for x in claims]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
  basis=m._basis(data);cases=[]
  for i,row in enumerate(claims):
   name=row['context'];anchor=row['validated_state_anchor'];old=prior['contexts'][i];now=bundle['contexts'][i]
   check('preserved predecessor fields '+name,lambda old=old,now=now:all(enc(now[k])==enc(v) for k,v in old.items()))
   check('exact saved HEAD and instance value '+name,lambda anchor=anchor,old=old:anchor['validated_state']==state and anchor['decoded_state_identity']==identity(raw) and anchor['record']==old['hf01_evidence_binding']['head_record'] and anchor['instance']==old['hf01_evidence_binding']['instance'] and state['binding']==anchor['instance']['binding'])
   check('source declaration and lineage joins '+name,lambda anchor=anchor,old=old:cat['inherited_head']==old['hf01_evidence_binding']['head_declaration'] and anchor['configuration_record']==old['config_return_correspondence']['validated_configuration_anchor']['record'] and anchor['recovery_occurrence']==old['hf01_evidence_binding']['occurrence']['id'] and anchor['recovery_call']==old['hf01_evidence_binding']['occurrence']['call'])
   check('observer is exact separate saved record '+name,lambda row=row,anchor=anchor:row['separate_observer']['value']==hands[0]['state'] and row['separate_observer']['caller']==hands[0]['observer_call_site'] and {k:row['separate_observer']['record'][k] for k in ('bytes','sha256')}==identity(e['evidence/client-handoff.json']) and row['separate_observer']['id']==anchor['record']['acquisition'].removeprefix('sha256:')+':'+name+':observer-state:0' and all(row['separate_observer'][k] is None for k in ('frame','parent_frame','joins_to_three_return_links')))
   check('no invented three-link execution '+name,lambda row=row:row['runtime_links'] is row['actual_call_count'] is None and row['unjoined_trace_calls']==[] and len(row['conditional_links'])==3 and all(x['observed_value'] is x['frame'] is x['object_reference_observed'] is None for x in row['conditional_links']))
   scope={'context':name,'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence']};live={'kind':'authority-reference','scope':copy.deepcopy(scope),'symbol':'review-live-A'};ref={'kind':'state-result-reference','scope':copy.deepcopy(scope),'symbol':'review-value-A'}
   projection={'method':'state','args':[],'phase':'READY','live_reference':live,'retired_reference':None,'outcomes':dict(normal),'underlying':{'receiver':copy.deepcopy(live),'value':copy.deepcopy(state),'reference':copy.deepcopy(ref)},'run_result':{'value':copy.deepcopy(state),'reference':copy.deepcopy(ref)},'wrapper_return':{'value':copy.deepcopy(state),'reference':copy.deepcopy(ref)}}
   case={'kind':'CONSTRUCTED-CONDITIONAL-STATE','context':name,'anchor':copy.deepcopy(anchor),'projection':projection};cases.append(case)
   result=check('anchored normal constructed forwarding '+name,lambda case=case:m.constructed_projection(data,cat,case),'constructed_only');constructed.append(result)
   mutations=[('method handle',lambda x:x.update(method='handle')),('extra argument',lambda x:x.update(args=[None])),('missing underlying link',lambda x:x.pop('underlying')),('wrong receiver',lambda x:x['underlying']['receiver'].update(symbol='other-live')),('copied run reference',lambda x:x['run_result']['reference'].update(symbol='copy')),('copied wrapper reference',lambda x:x['wrapper_return']['reference'].update(symbol='copy')),('cross acquisition result',lambda x:x['underlying']['reference']['scope'].update(acquisition='other')),('nested bool instead of int',lambda x:x['wrapper_return']['value']['resources'].update(holds=True)),('wrong nested count',lambda x:x['run_result']['value']['counts'].update(attempt=1)),('null state',lambda x:x['underlying'].update(value=None)),('absent live',lambda x:x.update(live_reference=None)),('retired reference',lambda x:x.update(retired_reference=copy.deepcopy(live)))]
   for label,edit in mutations:
    if a.recovered and label in ('extra argument','missing underlying link','wrong receiver','null state','absent live','retired reference'):continue
    bad=copy.deepcopy(projection);edit(bad);reject('constructed '+label+' '+name,lambda bad=bad:c.state_value_projection(cat,bad,state),category='constructed_negative')
   other=copy.deepcopy(projection)
   for k in ('underlying','run_result','wrapper_return'):other[k]['reference']['symbol']='review-value-B'
   check('alternative consistent symbols are not physical identity '+name,lambda other=other:c.state_value_projection(cat,other,state)['actual_object_identity_established'] is False,'constructed_only')
   bad=copy.deepcopy(claims);bad[i]['conditional_links'].pop(1);reject('semantic missing middle link '+name,lambda bad=bad:m.semantic(data,cat,bad),'STATE-LINK-COVERAGE')
   bad=copy.deepcopy(claims);bad[i]['validated_state_anchor']['instance']['managed_constructor_frame']+=1;reject('derivation wrong instance '+name,lambda bad=bad:m.derive_state(data,cat,bad),'STATE-ANCHOR-LINEAGE')
  # Generate stage failures from the independently audited Python region order.
  path_cases=[]
  prefix={}
  caught={'pre_transaction','dispatch','post_transaction','return_expression'}
  for stage,v in normal.items():
   q=dict(prefix);q[stage]='raise'
   if stage in caught:q.update(handler_reason='normal',quarantine='normal')
   if stage!='lock_enter':q['lock_exit']='normal' if stage!='lock_exit' else 'raise'
   path_cases.append((stage,q,stage,stage in caught,True if stage in caught else None,stage in ('post_transaction','return_expression','lock_exit')))
   prefix[stage]=v
  for stage in ('pre_transaction','post_transaction'):
   q=dict(next(x[1] for x in path_cases if x[0]==stage));q[stage]=True;path_cases.append((stage+' active',q,stage,True,True,stage=='post_transaction'))
  q={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'raise','handler_reason':'raise','lock_exit':'normal'};path_cases.append(('reason evaluation fails',q,'handler_reason',False,None,False))
  q=dict(q,handler_reason='normal',quarantine='raise');path_cases.append(('quarantine interrupted',q,'quarantine',True,False,False))
  q=dict(q,quarantine='normal',lock_exit='raise');path_cases.append(('exit supersedes rethrow',q,'lock_exit',True,True,False))
  check('normal path no quarantine or copy',lambda:c.state_path_projection(cat,normal)['completion']=='normal' and c.state_path_projection(cat,normal)['quarantine_called'] is False,'constructed_only')
  path_results=[]
  for label,outcomes,failure,called,completed,dispatch in path_cases:
   path=c.state_path_projection(cat,outcomes);path_results.append({'case':label,'premise':outcomes,'result':path})
   check('source exception region '+label,lambda path=path,failure=failure,called=called,completed=completed,dispatch=dispatch:path['completion']=='abrupt' and path['failure_site']==failure and path['quarantine_called'] is called and path['quarantine_completed'] is completed and path['dispatch_completed'] is dispatch and path['return_links_admissible'] is False,'constructed_only')
   bad=copy.deepcopy(cases[0]['projection']);bad['outcomes']=outcomes;reject('abrupt cannot claim return '+label,lambda bad=bad:c.state_value_projection(cat,bad,state),'STATE-NO-NORMAL-RETURN','constructed_negative')
  (out/'constructed-paths.json').write_text(json.dumps(path_results,indent=2)+'\n')
  reject('integer not transaction outcome',lambda:c.state_path_projection(cat,dict(normal,pre_transaction=0)),'STATE-PATH-OUTCOME:pre_transaction','constructed_negative')
  reject('unreached outcomes cannot imply dispatch',lambda:c.state_path_projection(cat,{'lock_enter':'raise','dispatch':'normal'}),'STATE-PATH-UNREACHED-OUTCOMES','constructed_negative')
  missing=dict(normal);missing.pop('lock_exit');reject('missing normal lock exit',lambda:c.state_path_projection(cat,missing),'STATE-PATH-MISSING:lock_exit','constructed_negative')
  # Independently checked source catalogue is mandatory, not optional annotation.
  badcat=copy.deepcopy(cat);badcat['source']['method']='handle';badcat['source']['wrapper_call']['expression']="self._run('handle')";badcat['delegation']['to']='Authority.handle'
  reject('semantic coordinated method catalogue substitution',lambda:m.semantic(data,badcat),'STATE-SOURCE-CATALOGUE')
  if not a.recovered:
   g=d['guards']
   for label,edit in [('omitted bridge',lambda x:x['links'].pop(0)),('changed HEAD type',lambda x:x['inherited_head']['native_template']['type']['object'].update(seq='BOOLEAN')),('exit placed in catch',lambda x:x['source']['caught_stages'].append('lock_exit')),('missing return guard',lambda x:x['source']['run_return'].update(guards=[])),('result copy claimed',lambda x:x['links'][1].update(kind='deepcopy'))]:
    bad=copy.deepcopy(cat);edit(bad);reject('source catalogue '+label,lambda bad=bad:c.validate_state_return(d['manager'],d['authority'],obs,model,producer,g['guard_relationships'],g['guard_oracle'],refs,bad),'STATE-RETURN-CORRESPONDENCE','source_negative')
   bad=copy.deepcopy(cases[0]);bad['projection']['live_reference']['scope']['instance']['ownership_incarnation']='foreign';bad['projection']['underlying']['receiver']=copy.deepcopy(bad['projection']['live_reference']);reject('full wrong-instance constructed reference',lambda:m.constructed_projection(data,cat,bad),'STATE-CASE-REFERENCE-SCOPE')
  old=state['head'];replacement=('a' if old[0]!='a' else 'b')+old[1:]
  def substitute(v):
   if type(v) is str:
    if v==old:return replacement
    try:nested=json.loads(bytes.fromhex(v))
    except (ValueError,UnicodeError):return v
    changed=substitute(nested);return enc(changed).rstrip(b'\n').hex() if changed!=nested else v
   if type(v) is list:return [substitute(x) for x in v]
   if type(v) is dict:return {k:substitute(x) for k,x in v.items()}
   return v
  altered=dict(e);changes={}
  for n,b in e.items():
   if n.endswith('.json'):
    v=json.loads(b);changed=substitute(v)
    if changed!=v:altered[n]=enc(changed);changes[n]={'before':identity(b),'after':identity(altered[n])}
  assert len(changes)>1 and json.loads(bytes.fromhex(json.loads(altered['evidence/recovery-export-0.json'])['head']))['head']==replacement
  (out/'coordinated-substitution.json').write_text(json.dumps({'original_head':old,'substituted_head':replacement,'changed_members':changes},indent=2)+'\n')
  reject('coordinated HEAD semantic comparison',lambda:m.semantic(data,cat,evidence=altered),'STATE-VALUE-ORIGIN:/head')
  reject('coordinated HEAD derivation comparison',lambda:m.derive_state(data,cat,evidence=altered),'STATE-VALUE-ORIGIN:/head')
  bad=copy.deepcopy(claims)
  for row in bad:
   row['validated_state_anchor']['validated_state']['head']=replacement
   for link in row['conditional_links']:link['conditional_value_at_validated_frontier']['head']=replacement
  reject('coordinated three-value reports both contexts',lambda:m.derive_state(data,cat,bad),'STATE-VALUE-ORIGIN:/head')
  if not a.recovered:
   candidate=dict(data);candidate['prior_data']=dict(data['prior_data']);candidate['prior_data']['prior_data']=dict(data['prior_data']['prior_data']);candidate['prior_data']['prior_data']['prior_data']=dict(d);candidate['prior_data']['prior_data']['prior_data']['ctx']=dict(d['ctx']);candidate['prior_data']['prior_data']['prior_data']['ctx']['e']=altered
   reject('candidate baseline cannot redefine validated state',lambda:m.semantic(candidate,cat),'STATE-VALUE-ORIGIN:/head')
  for label,edit in [('wrong binding',lambda x:x.update(binding='e'*64)),('nested bool',lambda x:x['counts'].update(query=True)),('missing seq',lambda x:x.pop('seq')),('list for dictionary',lambda x:x.update(u=[]))]:
   if a.recovered and label in ('wrong binding','list for dictionary'):continue
   st=copy.deepcopy(state);edit(st);ex=copy.deepcopy(export);ex['head']=enc(st).hex();ev=dict(e);ev['evidence/recovery-export-0.json']=enc(ex);reject('exact evidence '+label,lambda ev=ev:m._compare_evidence(basis,ev),category='internal_relation')
  if not a.recovered:
   ev=dict(e);del ev['evidence/recovery-export-0.json'];reject('full missing recovery evidence',lambda:m.semantic(data,cat,evidence=ev),'STATE-MISSING-EXPORT')
   for label,edit in [('stale frontier',lambda x:x['validated_state_anchor'].update(recovery_occurrence='stale')),('foreign acquisition',lambda x:x['validated_state_anchor']['record'].update(acquisition='foreign')),('link order',lambda x:x['conditional_links'].reverse()),('observer joined to missing frame',lambda x:x['separate_observer'].update(joins_to_three_return_links=[])),('observed wrapper promoted',lambda x:x['conditional_links'][2].update(observed_value=state))]:
    bad=copy.deepcopy(claims);edit(bad[1]);reject('anchor and links '+label,lambda bad=bad:m._check_rows(basis,bad,claims),category='internal_relation')
  for label,edit in [('omitted mapping',lambda b:b['contexts'][1].pop('state_return_correspondence')),('status escalation',lambda b:b['new_state_slice_limits'].update(actual_state_call_count=1,saved_three_link_execution_chain='COMPLETE',actual_admission=True)),('missing context',lambda b:b['contexts'].pop())]:
   if a.recovered and label=='missing context':continue
   bad=copy.deepcopy(bundle);edit(bad);reject('public '+label,lambda bad=bad:m.validate(root,enc(bad)),'STALE-OR-ALTERED-STATE-CORRESPONDENCE','public_negative')
  pristine=enc(claims);second=enc(claims[1]);claims[0]['conditional_links'][0]['conditional_value_at_validated_frontier']['counts']['query']=99;claims[0]['declaration']['links'].clear()
  check('nested returned contexts isolated',lambda:enc(claims[1])==second)
  public['contexts'].reverse();public['receipt'].clear();bundle['contexts'].clear();cat_before=enc(cat);cat['source']['normal_path'].clear()
  check('catalogue returned mutation cannot change expectation',lambda:enc(m.catalogue(data))==cat_before);cat=m.catalogue(data)
  check('pristine semantic after nested mutations',lambda:enc(m.semantic(data,cat))==pristine)
  check('pristine derivation after nested mutations',lambda:enc(m.derive_state(data,cat))==saved)
  check('pristine public after nested mutations',lambda:m.validate(root,saved))
  check('mandatory config predecessor actually invoked',lambda:any(x['function']=='mandatory config derive_config' for x in calls))
  check('HEAD comparison used validated original expectation',lambda:any(x['function']=='state comparison' and x['expected']==state and x['candidate'] is not None and x['candidate'].get('head')==replacement for x in calls))
  check('sources and candidate evidence unchanged',lambda:source=={n:identity((root/'code'/n).read_bytes()) for n in source} and e==d['ctx']['e'])
 except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};(out/'failure.txt').write_text(traceback.format_exc());raise
 finally:
  sys.settrace(None);r={'result':'PASS' if error is None else 'FAIL','assertions':len(rows),'categories':{c:sum(x['category']==c for x in rows) for c in sorted({x['category'] for x in rows})},'checks':rows,'error':error,'recovered':a.recovered,'environment':{'python':sys.version,'optimization':sys.flags.optimize,'cryptography_installed':importlib.metadata.version('cryptography')},'source':locals().get('source'),'database_connections':0,'session_operations':0,'completed_review_reruns':False,'constructed_cases_are_execution_evidence':False}
  (out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');(out/'call-observations.json').write_text(json.dumps(calls,indent=2)+'\n');(out/'constructed-cases.json').write_text(json.dumps(constructed,indent=2)+'\n')
 print('PASS',len(rows),'independent state checks')
if __name__=='__main__':main()
