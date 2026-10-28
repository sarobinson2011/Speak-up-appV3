"""Fresh classification truth-table controls from source, not supplied results."""
from pathlib import Path
import argparse,copy,json,runpy,traceback
C=runpy.run_path(str(Path(__file__).with_name('common.py')));globals().update({n:C[n] for n in ('enc','identity','module','guards','monitor','Record')})
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('output',type=Path);p.add_argument('--recovered',action='store_true');a=p.parse_args();root=a.root.resolve();r=Record(a.output.resolve());guards(root);error=None;stop=lambda:None;cases=[];witnesses=[]
try:
 m=module(root/'code/correspondence.py');calls,stop=monitor(m);d=m.inputs(root);c=d['coverage'];cat=m.catalogue(d);launcher,entry=m.sources(d);_,authority,anchor,observations=d['prior_module'].sources(d['prior_data']);v=c.handle_authentication(authority,anchor,observations)
 oracle=runpy.run_path(str(Path(__file__).with_name('source_oracle.py')))
 source=r.check('independent defining-source dynamic catch and consumer audit',lambda:oracle['audit'](launcher,entry,cat,(root/'code/managed_coverage.py').read_bytes()));(r.path/'source-audit.json').write_text(json.dumps(source,indent=2)+'\n')
 normal=source['normal_order'];info=source['stages'];fixture=json.loads((root/'review/independent-primary/core/constructed-cases.json').read_bytes());base={ctx:copy.deepcopy(next(x['case'] for x in fixture if x['case']['scope']['context']==ctx)) for ctx in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')};unseen=dict.fromkeys(('revoke','format','cleanup','write','outer_fail'),'unobserved')
 def project(x):return c.client_handle_projection(cat,v,x,copy.deepcopy(x))
 def expected(x,kind,terminal,retained,flag):
  out=project(x);cl=out['outcome_classification'];loc=info[terminal]
  assert out['outside_catch_failure'] is flag and cl['unexpected_raise_outside_dispatch_catch'] is flag
  assert type(out['outside_catch_failure']) is bool and cl['modeled_kind']==kind and cl['stage']==terminal and cl['location_relative_to_dispatch_catch']==loc['location'] and cl['python_raise_protected_by_dispatch_catch'] is loc['protected']
  assert cl['stage_outcome']==x['outcomes'][terminal] and all(cl['source'][k]==val for k,val in loc['anchor'].items())
  model=None if kind=='process-termination' else kind!='normal-return';assert cl['terminal_python_exception_in_model'] is model
  assert cl['runtime_python_exception_evidence']==cl['runtime_python_unwind_evidence']=='UNAVAILABLE' and cl['retention_cleanup_or_authority_established_by_classification'] is False
  assert out['retained_original'] is retained and out['authorization_renewed'] is out['actual_admission'] is out['runtime_observation'] is False
  assert c.validate_client_handle_projection(cat,v,x,copy.deepcopy(x),copy.deepcopy(out)) is True
  cases.append({'case':copy.deepcopy(x),'result':copy.deepcopy(out),'source_oracle':{'terminal':terminal,'kind':kind,'flag':flag,'protected':loc['protected'],'retained_original':retained}});return out
 # Four legitimate saved input variants, including normally returned error bytes.
 for saved in fixture:
  x=copy.deepcopy(saved['case']);out=r.check('normal exact byte return '+x['occurrence'],lambda x=x:expected(x,'normal-return','client-return',False,False),'constructed')
  r.check('classification adds no normalization or occurrence merge '+x['occurrence'],lambda out=out,x=x:len(out['hops'])==5 and len({h['id'] for h in out['hops']})==5 and all(h['value']==x['manager_case']['wrapper_return']['value'] for h in out['hops']),'constructed')
 for ctx,baseline in base.items():
  for stage in normal:
   if a.recovered and stage not in ('client-call','owner-guard','packet-check','manager-call','session-return','client-return'):continue
   for abrupt in ('raise','process-termination'):
    x=copy.deepcopy(baseline);idx=normal.index(stage);x['outcomes']={n:abrupt if n==stage else 'normal' for n in normal[:idx+1]}
    if idx<=normal.index('manager-call'):x['manager_case']=None
    inside=info[stage]['protected']
    if abrupt=='raise' and inside:x['outcomes'].update({'retain-error':'normal','fixed-failure':'normal'});kind='intentional-fixed-raise';terminal='fixed-failure';retained=True;flag=False
    else:kind='unexpected-raise' if abrupt=='raise' else 'process-termination';terminal=stage;retained=False;flag=abrupt=='raise'
    out=r.check('source path '+ctx+':'+stage+':'+abrupt,lambda x=x,kind=kind,terminal=terminal,retained=retained,flag=flag:expected(x,kind,terminal,retained,flag),'constructed')
    assert [e['stage'] for e in out['events']]==list(x['outcomes'])
    if abrupt=='process-termination':
     assert out['original_exception'] is None and out['fixed_client_failure'] is None and out['evidence_route']['original_reraised_to_launcher'] is None and out['destinations']==[]
    elif inside:assert out['original_exception']['origin']==stage and out['fixed_client_failure']['type']=='ClientFailure'
  # Separate source TypeError, error storage and helper interruption premises.
  invalid=copy.deepcopy(baseline);invalid['manager_case']=None;invalid['packet']={'type':'str','value':'review-invalid-byte-packet'};invalid['outcomes']=dict.fromkeys(normal[:4]+['retain-error'],'normal')
  for abrupt in ('raise','process-termination'):
   x=copy.deepcopy(invalid);x['outcomes']['retain-error']=abrupt;out=r.check('storage '+ctx+':'+abrupt,lambda x=x,abrupt=abrupt:expected(x,'unexpected-raise' if abrupt=='raise' else 'process-termination','retain-error',None,abrupt=='raise'),'constructed');assert out['original_exception']['kind']=='source-TypeError'
  for outcome in ('normal','raise','process-termination'):
   x=copy.deepcopy(invalid);x['outcomes']['fixed-failure']=outcome;kind={'normal':'intentional-fixed-raise','raise':'unexpected-raise','process-termination':'process-termination'}[outcome]
   out=r.check('stored original then helper '+ctx+':'+outcome,lambda x=x,kind=kind,outcome=outcome:expected(x,kind,'fixed-failure',True,outcome=='raise'),'constructed');assert any(z['to']=='owner.failure' for z in out['destinations'])
   if outcome=='process-termination':
    assert out['evidence_route']['original_reraised_to_launcher'] is None and [z['to'] for z in out['destinations']]==['owner.failure']
    bad=copy.deepcopy(out);bad['retained_original']=False;r.reject('termination does not erase earlier stored original '+ctx,lambda x=x,bad=bad:c.validate_client_handle_projection(cat,v,x,x,bad),'CLIENT-PROJECTION-CORRESPONDENCE')
  for prior_failed in (False,True):
   x=copy.deepcopy(baseline);x['manager_case']=None;x['outcomes']=dict.fromkeys(normal[:3]+['fixed-failure'],'normal');x['references']['owner_failed']=prior_failed
   if not prior_failed:x['references']['owners[token]']=None
   out=r.check('intentional owner refusal '+ctx+':'+str(prior_failed),lambda x=x:expected(x,'intentional-fixed-raise','fixed-failure',False,False),'constructed');assert out['prior_owner_failure']['present'] is prior_failed and out['prior_owner_failure']['resolution_established'] is False
 # Reproduce the six retained caveats against old producer, then current repair.
 old=module(root/'original/code/managed_coverage.py');caveat=json.loads((root/'review/results/classification-caveat.json').read_bytes())
 for row in caveat['cases']:
  x=copy.deepcopy(row['case']);before=old.client_handle_projection(cat,v,x,copy.deepcopy(x));out=project(x)
  r.check('preserved prefix witness reproduced '+x['scope']['context']+':'+next(k for k,z in x['outcomes'].items() if z=='process-termination'),lambda before=before,row=row:enc(before)==enc(row['result']) and before['outside_catch_failure'] is True,'old-witness')
  assert out['outside_catch_failure'] is False and out['outcome_classification']['terminal_python_exception_in_model'] is None
  bad=copy.deepcopy(out);bad['outside_catch_failure']=True;bad['completion']='unqualified-escape';bad['events'][-1]['outcome']='raise';bad['outcome_classification'].update(modeled_kind='unexpected-raise',stage_outcome='raise',unexpected_raise_outside_dispatch_catch=True,terminal_python_exception_in_model=True)
  r.reject('coordinated termination-to-exception result rejects '+x['scope']['context']+':'+out['outcome_classification']['stage'],lambda x=x,bad=bad:c.validate_client_handle_projection(cat,v,x,x,bad),'CLIENT-PROJECTION-CORRESPONDENCE')
  changed=copy.deepcopy(x);changed['outcomes'][out['outcome_classification']['stage']]='raise';r.reject('changed outcome cannot replace fixed validated premise '+x['scope']['context']+':'+out['outcome_classification']['stage'],lambda x=x,changed=changed:c.client_handle_projection(cat,v,changed,x),'CLIENT-PREMISE:outcomes')
  for field in ('callback','cleanup'):
   changed=copy.deepcopy(x)
   if field=='callback':changed[field]='returns'
   else:changed[field]=dict.fromkeys(unseen,'normal')
   r.reject('coordinated post-termination '+field+' premise rejects '+x['scope']['context']+':'+out['outcome_classification']['stage'],lambda changed=changed:project(changed))
  witnesses.append({'case':x,'previous':before,'current':out})
 # Original helper/storage false-flag defects remain repaired.
 earliest=module(root/'original/failures/pre-correction/code/managed_coverage.py');original=json.loads((root/'original/failures/pre-correction/edge-witness.json').read_bytes())
 for ctx in base:
  x=copy.deepcopy(original['case']);x['scope']['context']=ctx
  for ref in x['references'].values():
   if type(ref) is dict:ref['scope']['context']=ctx
  before=earliest.client_handle_projection(cat,v,x,copy.deepcopy(x));out=project(x)
  r.check('earliest helper false flag reproduced and repair retained '+ctx,lambda before=before,out=out:before['outside_catch_failure'] is False and out['outside_catch_failure'] is True and out['outcome_classification']['modeled_kind']=='unexpected-raise','old-witness')
  if ctx=='SYMBOLIC-U-ONE':assert enc(before)==enc(original['output'])
  x['references']['owners[token]']=copy.deepcopy(x['references']['owner']);x['packet']={'type':'str','value':'bad'};x['outcomes']=dict.fromkeys(normal[:4]+['retain-error'],'normal');x['outcomes']['retain-error']='raise'
  before=earliest.client_handle_projection(cat,v,x,copy.deepcopy(x));out=project(x);r.check('earliest storage false flag and known-false retention repaired '+ctx,lambda before=before,out=out:before['outside_catch_failure'] is before['retained_original'] is False and out['outside_catch_failure'] is True and out['retained_original'] is None,'old-witness');witnesses.append({'case':x,'earliest':before,'current':out})
 # Exact types, missing classification, false evidence and source-location claims.
 for ctx,x in base.items():
  cut=copy.deepcopy(x);cut['manager_case']=None;cut['outcomes']={'client-call':'process-termination'};out=project(cut)
  mutations=[('missing classification',lambda q:q.pop('outcome_classification')),('integer flag',lambda q:q.update(outside_catch_failure=0)),('integer protection',lambda q:q['outcome_classification'].update(python_raise_protected_by_dispatch_catch=0)),('false means no exception',lambda q:q['outcome_classification'].update(terminal_python_exception_in_model=False)),('wrong source location',lambda q:q['outcome_classification'].update(location_relative_to_dispatch_catch='dispatch-protected-try')),('observed exception',lambda q:q['outcome_classification'].update(runtime_python_exception_evidence='ESTABLISHED')),('observed unwind',lambda q:q['outcome_classification'].update(runtime_python_unwind_evidence='ESTABLISHED')),('invented retained error',lambda q:q.update(retained_original=True)),('cleanup authority',lambda q:q['outcome_classification'].update(retention_cleanup_or_authority_established_by_classification=True)),('renewal',lambda q:q.update(authorization_renewed=True)),('admission',lambda q:q.update(actual_admission=True))]
  for name,change in mutations:
   if a.recovered and name in ('integer protection','observed exception','cleanup authority','admission'):continue
   bad=copy.deepcopy(out);change(bad);r.reject(name+' '+ctx,lambda bad=bad,cut=cut:c.validate_client_handle_projection(cat,v,cut,cut,bad),'CLIENT-PROJECTION-CORRESPONDENCE')
  pristine=enc(project(cut));out['outcome_classification']['source']['guards'].clear();out['outcome_classification']['unexpected_raise_outside_dispatch_catch']=True;r.check('returned nested mutations cannot redefine classification '+ctx,lambda cut=cut,pristine=pristine:enc(project(cut))==pristine)
 # Source validation cannot accept mutually edited location/contract annotations.
 manager=d['prior_module'].catalogue(d['prior_data']);boundary=m.inner(d)['ctx']['binding'];badcat=copy.deepcopy(cat);badcat['outside_catch_failure_contract']['true_iff']='termination outside catch';badcat['source']['stages']['retain-error']['guards'].clear()
 r.reject('coordinated contract and guard substitution rejects defining sources',lambda:c.validate_client_handle(launcher,entry,manager,boundary,badcat),'CLIENT-SOURCE-CORRESPONDENCE')
 r.check('current source pin unchanged',lambda:identity((root/'code/managed_coverage.py').read_bytes())==m.PRODUCER_PIN)
except BaseException as e:error={'type':type(e).__name__,'message':str(e)};(r.path/'failure.txt').write_text(traceback.format_exc());raise
finally:
 stop();r.finish(error,root=root.name,recovered=a.recovered);(r.path/'cases.json').write_text(json.dumps(cases,indent=2)+'\n');(r.path/'witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')
print('PASS',len(r.rows),'new source-classification controls')
