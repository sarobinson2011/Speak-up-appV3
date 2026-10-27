"""Formal-Lab[6] independent reference-correspondence controls, offline only."""
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.metadata,json,os,shutil,sys,traceback,types
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def module(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--recovered',action='store_true');a=p.parse_args();root=a.root.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('PROHIBITED:'+event)
  if event=='open' and isinstance(args[0],(str,bytes)):
   name=os.fsdecode(args[0])
   if name.startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
   if name.startswith(str(root)+'/') and len(args)>2 and type(args[2]) is int and args[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC):raise AssertionError('INPUT-WRITE')
 sys.addaudithook(audit)
 def profile(frame,event,arg):
  name=frame.f_code.co_filename.rsplit('/',1)[-1]
  if event=='call' and (name in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') or name=='prospective_entry.py' and frame.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status')):raise AssertionError('APPLICATION-EXECUTION')
 sys.setprofile(profile);checks=[];paths={};failure=None;pins={n:ident((root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 def record(label,result='PASS',category='independent',error=None):
  row={'check':label,'result':result,'category':category}
  if error is not None:row['error']=error
  checks.append(row)
  with (out/'progress.jsonl').open('ab') as f:f.write((json.dumps(row,sort_keys=True)+'\n').encode())
 def good(label,value=True,category='independent'):assert value,label;record(label,category=category)
 def reject(label,fn,category='negative'):
  try:fn()
  except (ValueError,TypeError,KeyError,IndexError,FileNotFoundError) as ex:record(label,'REJECTED',category,{'type':type(ex).__name__,'message':str(ex)});return
  raise AssertionError('UNEXPECTED ACCEPTANCE: '+label)
 try:
  m=module(root/'code/correspondence.py','review_reference');data=m.reference_inputs(root);cat=m.reference_catalogue(data);raw=(root/'results/reference-correspondence.json').read_bytes();saved=json.loads(raw)
  good('legitimate internal catalogue',m.check_reference_catalogue(data,cat))
  good('legitimate public receipt',m.validate(root,raw)['result']=='PASS')
  good('derived exact saved output',m.enc(m.derive_reference(data,cat))==raw)
  oracle=module(Path(__file__).with_name('source_oracle.py'),'source_oracle');model=data['values']['candidate/managed-route/model.json'];source=oracle.audit(data['manager'],cat,data['authority'],model)
  (out/'source-audit.json').write_text(json.dumps(source,indent=2)+'\n');good('independent defining-source membership guards order and bindings')
  prior=json.loads((root/'retained/fields/results/status-field-correspondence.json').read_bytes())
  good('prior field component identities retained',saved['prior_field_components']==prior['extension_components'])
  for ctx,old in zip(saved['contexts'],prior['contexts']):
   good('source audit '+ctx['context'],oracle.audit(data['manager'],ctx['reference_declarations'],data['authority'],model)['counts']==source['counts'])
   good('all prior context fields unchanged '+ctx['context'],all(old[k]==ctx[k] for k in old))
  observed=data['occurrence'].derive(data['ctx']);evidence=data['ctx']['e'];trace=json.loads(evidence['evidence/execution-trace.json']);calls={e['frame']:e for e in trace['events'] if e['event']=='call' and not e['resumed_generator']}
  requirements={}
  for w in source['writes']:requirements.setdefault('ManagedAuthority.'+w['function'],[]).append('managed-reference-write:'+w['site'])
  for c in source['calls']:requirements.setdefault('ManagedAuthority.'+c['function'],[]).append('managed-reference-call:'+c['site'])
  for ctx in saved['contexts']:
   view=next(v for v in observed['contexts'] if v['context']==ctx['context']);expected_frames={fid for fid,c in calls.items() if c['function'] in requirements}
   rows=ctx['saved_reference_scope'];assert {v['frame'] for v in rows}==expected_frames and len(rows)==len(expected_frames)
   for r in rows:
    call=calls[r['frame']];occ=next(v for v in view['occurrences'] if v.get('frame')==r['frame'])
    assert r['occurrence']==occ['id'] and r['instance']==view['instance'] and r['parent']==call['parent']
    assert r['call_pointer']=='/events/'+str(call['seq']) and r['trace_identity']==ident(evidence['evidence/execution-trace.json'])
    assert r['source_relation_ids']==requirements[call['function']]
    assert r['observed_reference_transfers'] is None and r['object_identity'] is None and r['underlying_connection_identity'] is None
   good('exact saved invocation/conditional-source joins '+ctx['context'])
   observer=[v for v in view['occurrences'] if v['kind']=='explicit-observer-call']
   good('no invented observer or reference observations '+ctx['context'],len(observer)==1 and observer[0]['frame'] is None and len(calls)==18 and ctx['reference_observation_limits']['new_executions']==0)
  def catneg(label,edit,d=None):
   c=copy.deepcopy(cat);edit(c);reject(label,lambda:m.check_reference_catalogue(data if d is None else d,c),'catalogue_negative')
  if not a.recovered:
   for i,row in enumerate(source['writes']):
    site=row['site'];d=dict(data);d['values']=copy.deepcopy(data['values']);inventory=d['values']['candidate/managed-route/producers.json']['source_inventory']['sites'];inventory[:]=[r for r in inventory if r['site']!=site]
    def omit(c,site=site):
     c['source']['writes'][:]=[r for r in c['source']['writes'] if r['site']!=site]
     for r in c['declarations']:r['write_ids'][:]=[s for s in r['write_ids'] if s!='managed-reference-write:'+site]
    catneg('coordinated omitted writer and cached inventory '+site,omit,d)
    catneg('wrong reference origin '+site,lambda c,i=i:c['source']['writes'][i]['value'].update(kind='equal-recorded-value'))
    catneg('missing writer guard '+site,lambda c,i=i:c['source']['writes'][i].update(guards=[]))
    catneg('missing normal-continuation dependency '+site,lambda c,i=i:c['source']['writes'][i].update(continuation=[]))
   for field in ('calls','reference_reads','local_producers','programs'):
    for i,row in enumerate(cat['source'][field]):catneg('omit '+field+' '+row['site'],lambda c,i=i,field=field:c['source'][field].pop(i))
   catneg('reverse source transfer order',lambda c:c['source']['writes'].reverse())
   catneg('reverse normal prefix before publication',lambda c:next(w for w in c['source']['writes'] if w['expression']=='self._live=a')['continuation'][-1]['normal_continuation_of'].reverse())
   catneg('no-db clear claims close confirmation',lambda c:c.update(cleanup='Every retired clear confirms closure and discharges duties'))
   catneg('underlying connection from record equality',lambda c:c['connection_relation'].update(actual_object_and_connection_identity='verified equal dictionaries'))
   catneg('global allocation token',lambda c:c['identity'].update(allocation_rule='one global object'))
   catneg('classification escalation',lambda c:c['declarations'][0].update(classification='QUALIFIED',multiplicity=1))
   catneg('full model and admission escalation',lambda c:c.update(full_model_binding=True,actual_admission=True,complete_symbolic_coverage=True))
   cguard=data['guards']['guard_relationships'];site=source['writes'][2]['site']
   def changed_guard(raw):
    rows,bad=cguard.derive(raw);rows[site]=[];return rows,bad
   d=dict(data);d['guards']=dict(data['guards'],guard_relationships=types.SimpleNamespace(key=cguard.key,derive=changed_guard));d['values']=copy.deepcopy(data['values'])
   next(r for r in d['values']['candidate/managed-route/producers.json']['source_inventory']['sites'] if r['site']==site)['guards']=[]
   reject('coordinated generated/cached guard omission',lambda:m.reference_catalogue(d),'catalogue_negative')
   for name,old,new in [('manager',b'self._retired=self._live',b'self._retired=None'),('authority',b'self.db.close()',b'None')]:
    d=dict(data);assert old in data[name];d[name]=data[name].replace(old,new,1);reject('stale defining '+name+' source',lambda d=d:m.reference_catalogue(d),'catalogue_negative')
  else:
   catneg('recovered omitted transfer',lambda c:c['source']['writes'].pop())
   catneg('recovered wrong source order',lambda c:c['source']['writes'].reverse())
   catneg('recovered false closure',lambda c:c['connection_relation'].update(actual_object_and_connection_identity='ESTABLISHED'))
  matrix=module(Path(__file__).with_name('case_matrix.py'),'case_matrix')
  selected_recovered={'quarantine interrupted between copy and clear','recover successful publication','failed validation then failed cleanup retains partial object','return evaluation failure after READY cleans then quarantines'}
  for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
   cases,helpers=matrix.cases(data['manager'],context)
   for item in cases:
    if a.recovered and item['name'] not in selected_recovered:continue
    case=item['case'];answer=m.reference_path(data,case);matrix.compare(case,item['expected'],answer)
    label=context+' '+item['name'];paths[label]={'expected':item['expected'],'result':answer};good(label,category='constructed_not_execution')
    good('constructed result validates '+label,m.reference_path(data,case,answer),'constructed_not_execution')
   sample=next(v['result'] for k,v in paths.items() if k==context+' recover successful publication')
   if not a.recovered:
    for i,event in enumerate(sample['events']):
     if event['event']!='reference-write':continue
     bad=copy.deepcopy(sample);bad['events'].pop(i);reject('constructed omitted transfer '+context+' '+event['site'],lambda bad=bad:m.reference_path(data,sample['case'],bad),'constructed_negative')
    for label,change in [('changed order',lambda x:x['events'].reverse()),('stale live token',lambda x:x['final']['_live'].update(origin='initial:unrelated')),('false physical closure',lambda x:x.update(physical_close_established=True)),('discharged uncertainty',lambda x:x.update(outstanding_obligations_discharged=True)),('actual execution claim',lambda x:x.update(actual_observation=True)),('changed context',lambda x:x['scope'].update(context='MIXED'))]:
     bad=copy.deepcopy(sample);change(bad);reject('constructed '+label+' '+context,lambda bad=bad:m.reference_path(data,sample['case'],bad),'constructed_negative')
    case=copy.deepcopy(next(i['case'] for i in cases if i['name']=='failed OPEN_FAILED db=False'));next(v for v in case['facts'].values() if v['subject'] is not None)['subject']['origin']='initial:other-object'
    reject('no-db clear cannot use stale reference fact '+context,lambda:m.reference_path(data,case),'constructed_negative')
    case=copy.deepcopy(sample['case']);case['initial']['_live']=False;reject('bool is not reference '+context,lambda:m.reference_path(data,case),'constructed_negative')
   else:
    bad=copy.deepcopy(sample);bad['final']['_retired']=bad['final']['_live'];reject('recovered substituted final reference '+context,lambda:m.reference_path(data,sample['case'],bad),'constructed_negative')
  for field in ('context','acquisition','instance','invocation') if not a.recovered else ():
   sample=paths['SYMBOLIC-U-ONE recover successful publication']['result'];case=copy.deepcopy(sample['case'])
   if field=='context':case['context']='SYMBOLIC-U-TWO'
   else:case['scope'][field]+='-different'
   other=m.reference_path(data,case);good('distinct constructed '+field+' namespace',other['final']['_live']!=sample['final']['_live'],'constructed_not_execution')
   reject('stale constructed '+field+' result',lambda:m.reference_path(data,case,sample),'constructed_negative')
  # Only selected integration negatives through the new seam, not old suites.
  altered=dict(evidence);trace2=copy.deepcopy(trace);event=next(v for v in trace2['events'] if v['event']=='return' and v['function']=='ManagedAuthority.close');event['state']['_phase']='READY';altered['evidence/execution-trace.json']=m.enc(trace2)
  reject('new derivation rejects inconsistent saved close state',lambda:m.derive_reference(data,cat,altered),'saved_evidence_negative')
  if not a.recovered:
   altered=dict(evidence);trace2=copy.deepcopy(trace);event=next(v for v in trace2['events'] if v['event']=='call' and v['function']=='ManagedAuthority.recover');event['parent']=None;altered['evidence/execution-trace.json']=m.enc(trace2)
   reject('new derivation rejects altered recovery ancestry',lambda:m.derive_reference(data,cat,altered),'saved_evidence_negative')
  def public(label,edit):
   value=copy.deepcopy(saved);edit(value);reject(label,lambda:m.validate(root,m.enc(value)),'public_negative')
  for i in (0,1):
   public('public missing transfer context '+str(i),lambda b,i=i:b['contexts'][i]['reference_declarations']['source']['writes'].pop())
   public('public omitted observed function join '+str(i),lambda b,i=i:b['contexts'][i]['saved_reference_scope'].pop())
   if not a.recovered:
    public('public fabricated transfer observation '+str(i),lambda b,i=i:b['contexts'][i]['saved_reference_scope'][0].update(observed_reference_transfers=[]))
    public('public wrong occurrence identity '+str(i),lambda b,i=i:b['contexts'][i]['saved_reference_scope'][0].update(occurrence='other-acquisition'))
    public('public false cleanup discharge '+str(i),lambda b,i=i:b['contexts'][i]['reference_observation_limits'].update(outstanding_cleanup_obligations='DISCHARGED'))
  if not a.recovered:
   public('public missing context',lambda b:b['contexts'].pop())
   public('public duplicate context',lambda b:b['contexts'].__setitem__(1,copy.deepcopy(b['contexts'][0])))
   public('public reversed context order',lambda b:b['contexts'].reverse())
   public('public stale field receipt',lambda b:b['prior_field_receipt'].update(sha256='0'*64))
   public('public stale extension source',lambda b:b['extension_components']['managed_coverage.py'].update(sha256='0'*64))
   public('public false finite or readiness claims',lambda b:b['new_reference_slice_limits'].update(lifetime_bound=0,multiplicity=1,readiness='READY',actual_admission=True))
   public('public UNKNOWN totals cannot become zero',lambda b:b.update(inventory_unknown_totals=0,lifetime_unknown_totals=0))
  # Returned mutable values cannot revise validation's current expectations.
  answer=m.validate(root,raw);answer['contexts'].reverse();answer['receipt'].clear();cat['declarations'][0]['write_ids'].clear();saved['contexts'][0]['reference_declarations']['source']['writes'].clear()
  good('returned/nested aliases do not change pristine validation',m.validate(root,raw)['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
  good('new implementation source bytes unchanged',pins=={n:ident((root/'code'/n).read_bytes()) for n in pins})
 except BaseException as ex:
  failure={'type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc()}
  (out/'failure.txt').write_text(failure['traceback']);raise
 finally:
  (out/'constructed-results.json').write_text(json.dumps(paths,sort_keys=True,indent=2)+'\n')
  categories={c:sum(r['category']==c for r in checks) for c in sorted({r['category'] for r in checks})}
  result={'result':'PASS bounded reference correspondence' if failure is None else 'FAIL','assertions':len(checks),'categories':categories,'checks':checks,'failure':failure,'source':pins,'recovered':a.recovered,'environment':{'python':sys.version,'optimization':sys.flags.optimize,'cryptography_installed':importlib.metadata.version('cryptography')},'constructed_cases_not_runtime':len(paths),'no_new_observations':True,'supplied_suites_executed':False,'completed_review_reruns':False,'host_session_execution':False,'database_connections':0}
  (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS',len(checks),'independent assertions',categories)
if __name__=='__main__':main()
