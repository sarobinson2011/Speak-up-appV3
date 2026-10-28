"""Independent bounded handle correspondence checks; saved inputs only."""
from pathlib import Path
import argparse,copy,hashlib,importlib.metadata,json,os,runpy,sys,traceback,types
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey,Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def module(p):
 m=types.ModuleType('independent_handle');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
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
  if name=='derive_handle' and parent=='_basis':calls.append({'function':'mandatory handle derive_handle','file':f,'source':identity(Path(f).read_bytes())})
  if name=='_compare_evidence' and parent=='_checked' and f==str(root/'code/correspondence.py'):
   l=frame.f_locals;path='evidence/recovery-export-0.json';expected=json.loads(l['basis']['evidence'][path]);candidate=l['candidate'];value=None
   try:value=json.loads(candidate[path])
   except (ValueError,TypeError,KeyError):pass
   calls.append({'function':'journal comparison','expected_journal':expected['journal'],'candidate_journal':None if value is None else value.get('journal'),'expected_export':identity(l['basis']['evidence'][path]),'candidate_export':None if path not in candidate else identity(candidate[path])})
 sys.settrace(trace)
 def record(label,category,result,**kw):
  r={'check':label,'category':category,'result':result,**kw};rows.append(r)
  with (out/'progress.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 def check(label,fn,category='independent'):
  v=fn();assert v is not False,label;record(label,category,'PASS');return v
 def reject(label,fn,reason=None,category='negative'):
  try:fn()
  except (ValueError,TypeError,KeyError,IndexError,InvalidSignature) as ex:
   if reason is not None:assert str(ex)==reason,(label,str(ex),reason)
   record(label,category,'REJECTED',error={'type':type(ex).__name__,'message':str(ex)});return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+label)
 try:
  assert sys.version_info[:3]==(3,12,14) and not sys.flags.optimize
  m=module(root/'code/correspondence.py');data=m.inputs(root);cat=m.catalogue(data);c=data['coverage'];d=m.inner(data);e=dict(d['ctx']['e']);source={n:identity((root/'code'/n).read_bytes()) for n in ('correspondence.py','managed_coverage.py')}
  launcher,entry=m.sources(data);manager=data['prior_module'].catalogue(data['prior_data']);manager_raw,auth,anchor,obs=data['prior_module'].sources(data['prior_data']);v=c.handle_authentication(auth,anchor,obs)
  oracle=runpy.run_path(str(Path(__file__).with_name('source_oracle.py')))
  ar=check('independent forwarding types guards and exception-destination source audit',lambda:oracle['audit'](launcher,entry,manager_raw,cat,manager,d['ctx']['binding']));(out/'source-audit.json').write_text(json.dumps(ar,indent=2)+'\n')
  basis=check('fresh mandatory predecessor basis',lambda:m._basis(data));claims=m._rows(basis);saved=(root/'results/client-handle-correspondence.json').read_bytes();bundle=json.loads(saved);prior=json.loads((root/'retained/handle/results/handle-correspondence.json').read_bytes())
  check('fresh expected rows match saved client relation',lambda:enc(claims)==enc([x['client_handle_return_correspondence'] for x in bundle['contexts']]))
  check('exact two context order',lambda:[x['context'] for x in claims]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
  for i,row in enumerate(claims):
   name=row['context'];old=prior['contexts'][i]
   check('all prior context fields unchanged '+name,lambda i=i,old=old:all(enc(bundle['contexts'][i][k])==enc(x) for k,x in old.items()))
   check('instance request source and evidence anchor '+name,lambda row=row,old=old:row['manager_relation']==old['handle_return_correspondence'] and row['validated_scope']==old['handle_return_correspondence']['validated_scope'] and row['instance_request_context']==old['handle_return_correspondence']['instance_request_context'] and row['manager_predecessor_receipt']==identity((root/'retained/handle/results/handle-correspondence.json').read_bytes()) and row['boundary_binding']==identity(enc(d['ctx']['binding'])))
   check('missing runtime links are explicitly unavailable '+name,lambda row=row:row['captured_forwarding_calls']==[] and all(row[k] is None for k in ('runtime_forwarding_links','actual_client_handle_call_count','packet_observation','reference_identity_observations','original_exception_observation','fixed_failure_observation','multiplicity','ordinal')) and row['classification']=='UNKNOWN' and row['inject_observation']=={'observed':False,'value':None})
   check('separate observer and saved output identities preserved '+name,lambda row=row,old=old:old['state_return_correspondence']['separate_observer']['frame'] is None and old['state_return_correspondence']['separate_observer']['joins_to_three_return_links'] is None and all({k:row['saved_general_output'][n][k] for k in ('bytes','sha256')}==identity(e['evidence/smoke.'+n]) for n in ('stdout','stderr')))
  normal=['client-call','owner-lookup','owner-guard','packet-check','session-call','manager-call','session-return','response-check','dispatch-return','client-return'];unseen=dict.fromkeys(('revoke','format','cleanup','write','outer_fail'),'unobserved')
  def make(old,label):
   mc=copy.deepcopy(old);occ='review:'+mc['scope']['context']+':'+label;mc['occurrence']=occ+'/managed-handle';scope=copy.deepcopy(mc['scope'])
   for n in ('underlying','run_result','wrapper_return'):
    if mc[n] is not None:mc[n]['reference']['symbol']=occ+':response'
   refs={n:{'scope':copy.deepcopy(scope),'symbol':occ+':'+n} for n in ('client','token','owner','session','manager')}
   for x,y in [('client.token','token'),('owners[token]','owner'),('owner.wrapper','session'),('session.managed','manager')]:refs[x]=copy.deepcopy(refs[y])
   refs['owner_failed']=False
   return {'occurrence':occ,'scope':scope,'references':refs,'packet':{'type':'bytes','value':copy.deepcopy(mc['arguments']['packet'])},'outcomes':dict.fromkeys(normal,'normal'),'manager_case':mc,'callback':'unobserved','cleanup':dict(unseen)}
  fixtures=json.loads((root/'retained/handle/results/primary/constructed-cases.json').read_bytes());cases=[]
  for i,f in enumerate(fixtures):
   case=make(f['input'],str(i));expected=copy.deepcopy(case);name=case['scope']['context']+':'+str(i%2);cases.append(expected)
   r=check('normal exact forwarding including ok-false '+name,lambda case=case,expected=expected:c.client_handle_projection(cat,v,case,expected),'constructed_only');constructed.append({'case':case,'result':copy.deepcopy(r)})
   check('five distinct ordered value hops and exact bytes '+name,lambda r=r,case=case:[h['declaration'] for h in r['hops']]==['manager-return','session-return','dispatch-result','dispatch-return','client-return'] and len({h['id'] for h in r['hops']})==5 and all(h['value']==case['manager_case']['wrapper_return']['value'] for h in r['hops']) and r['completion']=='normal' and r['fixed_client_failure'] is None,'constructed_only')
   check('source argument hops and only calling-client destination '+name,lambda r=r,case=case:len(r['argument_hops'])==3 and [h['to'] for h in r['argument_hops']]==['_dispatch','ManagedSession.handle','ManagedAuthority.handle'] and r['argument_hops'][0]['operation']=='handle' and r['argument_hops'][-1]['inject'] is None and r['destinations']==[{'kind':'exact-response-bytes','to':'general-client','value':case['manager_case']['wrapper_return']['value']}] and r['runtime_observation'] is False,'constructed_only')
   for label,edit in [('missing hop',lambda x:x['hops'].pop(1)),('reordered hops',lambda x:x['hops'].reverse()),('missing argument',lambda x:x['argument_hops'].pop()),('wrong selector',lambda x:x['argument_hops'][0].update(operation='state')),('substituted bytes',lambda x:x['hops'][-1]['value'].update(bytes_hex='00')),('wrong return type',lambda x:x['hops'][-1].update(value=None)),('stdout destination',lambda x:x['destinations'][0].update(to='stdout')),('status destination',lambda x:x['destinations'].append({'kind':'status','to':'general-client'})),('raw exception destination',lambda x:x['destinations'].append({'kind':'original-exception','to':'general-client'})),('error converted into fixed failure',lambda x:x.update(completion='fixed-client-failure'))]:
    if a.recovered and label in ('missing argument','status destination','raw exception destination'):continue
    bad=copy.deepcopy(r);edit(bad);reject(label+' '+name,lambda bad=bad,case=case,expected=expected:c.validate_client_handle_projection(cat,v,case,expected,bad),'CLIENT-PROJECTION-CORRESPONDENCE','constructed_negative')
   for label,edit in [('wrong owner',lambda x:x['references']['owners[token]'].update(symbol='other')),('wrong manager',lambda x:x['references']['session.managed'].update(symbol='other')),('wrong packet',lambda x:x['packet']['value'].update(bytes_hex='00')),('wrong inject',lambda x:x['manager_case']['arguments'].update(inject='other')),('wrong method',lambda x:x['manager_case']['run_arguments'].update(method='state')),('wrong acquisition',lambda x:x['scope'].update(acquisition='other'))]:
    if a.recovered and label in ('wrong owner','wrong packet','wrong method'):continue
    bad=copy.deepcopy(case);edit(bad);reject(label+' '+name,lambda bad=bad,expected=expected:c.client_handle_projection(cat,v,bad,expected),category='constructed_negative')
   bad=copy.deepcopy(case)
   for n in ('underlying','run_result','wrapper_return'):bad['manager_case'][n]['value']=copy.deepcopy(fixtures[i^1]['input']['wrapper_return']['value'])
   reject('coordinated authenticated response replacement '+name,lambda bad=bad,expected=expected:c.client_handle_projection(cat,v,bad,expected),'HANDLE-EXACT-RESPONSE:underlying','constructed_negative')
   r['hops'][0]['value']['bytes_hex']='ff';r['reference_bindings']['manager']['scope']['instance']['binding']='changed';r['argument_hops'][0]['packet']['value']['bytes_hex']='00'
   check('nested projection results isolated '+name,lambda case=case,expected=expected:case==expected and c.client_handle_projection(cat,v,case,expected)['hops'][-1]['value']==expected['manager_case']['wrapper_return']['value'],'constructed_only')
  different=make(fixtures[0]['input'],'distinct');r=c.client_handle_projection(cat,v,cases[0],copy.deepcopy(cases[0]));s=c.client_handle_projection(cat,v,different,copy.deepcopy(different));check('equal byte values retain distinct occurrences',lambda:not ({x['id'] for x in r['hops']}&{x['id'] for x in s['hops']}) and r['hops'][-1]['value']==s['hops'][-1]['value'],'constructed_only')
  # Preserved development witness: execute only old/current conditional code,
  # never the supplied campaign or any runtime function.
  old=module(root/'failures/pre-correction/code/managed_coverage.py');w=json.loads((root/'failures/pre-correction/edge-witness.json').read_bytes());witnesses=[]
  for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
   x=copy.deepcopy(w['case']);x['scope']['context']=context
   for ref in x['references'].values():
    if type(ref) is dict:ref['scope']['context']=context
   before=old.client_handle_projection(cat,v,x,copy.deepcopy(x));after=c.client_handle_projection(cat,v,x,copy.deepcopy(x));witnesses.append({'context':context,'case':x,'old':before,'corrected':after})
   check('original helper classification witness reproduced '+context,lambda before=before:before['completion']=='unqualified-escape' and before['outside_catch_failure'] is False,'old_version_witness')
   if context=='SYMBOLIC-U-ONE':check('original witness output exact',lambda:enc(before)==enc(w['output']),'old_version_witness')
   check('corrected helper classification '+context,lambda after=after:after['completion']=='unqualified-escape' and after['outside_catch_failure'] is True and after['fixed_client_failure'] is None and after['destinations']==[],'constructed_only')
   bad=copy.deepcopy(after);bad['outside_catch_failure']=False;reject('old classification rejected by corrected relation '+context,lambda x=x,bad=bad:c.validate_client_handle_projection(cat,v,x,x,bad),'CLIENT-PROJECTION-CORRESPONDENCE','constructed_negative')
   x['outcomes']['fixed-failure']='normal';r=c.client_handle_projection(cat,v,x,copy.deepcopy(x));check('normal fixed failure retains exact source message '+context,lambda r=r:r['completion']=='fixed-client-failure' and r['fixed_client_failure']==cat['source']['fixed_failure'] and r['outside_catch_failure'] is False,'constructed_only')
   x['references']['owners[token]']=copy.deepcopy(x['references']['owner']);x['packet']={'type':'str','value':'untrusted'};x['outcomes']={n:'normal' for n in ('client-call','owner-lookup','owner-guard','packet-check')};x['outcomes']['retain-error']='raise'
   before=old.client_handle_projection(cat,v,x,copy.deepcopy(x));r=c.client_handle_projection(cat,v,x,copy.deepcopy(x));witnesses.append({'context':context,'case':copy.deepcopy(x),'old':before,'corrected':r})
   check('adjacent old storage classification and corrected uncertainty '+context,lambda before=before,r=r:before['outside_catch_failure'] is before['retained_original'] is False and r['outside_catch_failure'] is True and r['retained_original'] is None and r['fixed_client_failure'] is None,'old_version_witness')
   x['outcomes']['retain-error']='process-termination';r=c.client_handle_projection(cat,v,x,copy.deepcopy(x));check('storage termination is not Python unwind '+context,lambda r=r:r['completion']=='process-termination' and r['outside_catch_failure'] is False and r['retained_original'] is None,'constructed_only')
  (out/'original-witness-reproduction.json').write_text(json.dumps(witnesses,indent=2)+'\n')
  # Source-derived failure destinations, including caught/non-caught stages.
  paths=[]
  for i in (0,2):
   base=cases[i];name=base['scope']['context']
   for typ,val in [('str','bad'),('int',4),('NoneType',None)]:
    x=copy.deepcopy(base);x['manager_case']=None;x['packet']={'type':typ,'value':val};x['outcomes']={n:'normal' for n in ('client-call','owner-lookup','owner-guard','packet-check','retain-error','fixed-failure')};x['callback']='raises';x['cleanup']=dict.fromkeys(unseen,'normal')
    r=c.client_handle_projection(cat,v,x,copy.deepcopy(x));paths.append({'case':x,'result':r})
    check('nonbyte source failure and original retention '+typ+' '+name,lambda r=r:r['original_exception']['type']=='TypeError' and r['original_exception']['message']=='PACKET-BYTES' and r['retained_original'] is True and r['hops']==[] and r['evidence_route']['original_reraised_to_launcher'] is True and r['evidence_route']['explicit_cause']=='client_error' and r['evidence_route']['bytes'] is None,'constructed_only')
    check('fixed and trusted destinations separated '+typ+' '+name,lambda r=r:{d['to'] for d in r['destinations']}=={'general-client','owner.failure','launcher-existing-error-cleanup','existing-launcher-evidence/failure-*.json','general-entry-caller'} and r['fixed_client_failure']['suppress_context'] is True,'constructed_only')
   escaped=copy.deepcopy(base);mc=escaped['manager_case'];mc['backend_outcomes']={'authenticate':'Exception'};mc['run_outcomes']={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'raise','handler_reason':'normal','quarantine':'normal','lock_exit':'normal'}
   for n in ('underlying','run_result','wrapper_return'):mc[n]=None
   escaped['outcomes']={n:'normal' for n in ('client-call','owner-lookup','owner-guard','packet-check','session-call','manager-call','retain-error','fixed-failure')};escaped['callback']='returns';escaped['cleanup']=dict.fromkeys(unseen,'normal')
   r=c.client_handle_projection(cat,v,escaped,copy.deepcopy(escaped));paths.append({'case':escaped,'result':r});check('escaping manager original reaches trusted route '+name,lambda r=r:r['original_exception']['kind']=='manager-escaping-exception' and r['hops']==[] and r['evidence_route']['explicit_cause'] is None and r['retained_original'] is True,'constructed_only')
   for stage in ('revoke','format','cleanup','write'):
    x=copy.deepcopy(escaped);x['cleanup'][stage]='raise';after=False
    for n in unseen:
     if after:x['cleanup'][n]='unobserved'
     if n==stage:after=True
    if stage!='revoke':x['cleanup']['outer_fail']='normal'
    r=c.client_handle_projection(cat,v,x,copy.deepcopy(x));paths.append({'case':x,'result':r});check('failed cleanup or evidence stage '+stage+' '+name,lambda r=r:not any(d['to']=='existing-launcher-evidence/failure-*.json' for d in r['destinations']) and r['evidence_route']['bytes'] is None,'constructed_only')
    bad=copy.deepcopy(r);bad['evidence_route']['bytes']='invented';bad['destinations'].append({'kind':'raw-original','to':'stderr'});reject('failure cannot invent evidence bytes or output '+stage+' '+name,lambda x=x,bad=bad:c.validate_client_handle_projection(cat,v,x,x,bad),'CLIENT-PROJECTION-CORRESPONDENCE','constructed_negative')
   for stage in ('client-call','owner-lookup','owner-guard','packet-check','session-call','response-check','dispatch-return','client-return'):
    if a.recovered and stage not in ('client-call','packet-check','client-return'):continue
    x=copy.deepcopy(base);stop=normal.index(stage);x['outcomes']={n:('raise' if n==stage else 'normal') for n in normal[:stop+1]};caught=stage in ('packet-check','session-call','response-check','dispatch-return')
    if stop<normal.index('manager-call'):x['manager_case']=None
    if caught:x['outcomes'].update({'retain-error':'normal','fixed-failure':'normal'})
    r=c.client_handle_projection(cat,v,x,copy.deepcopy(x));paths.append({'case':x,'result':r});check('source catch placement '+stage+' '+name,lambda r=r,caught=caught:r['completion']==('fixed-client-failure' if caught else 'unqualified-escape') and r['outside_catch_failure'] is (not caught),'constructed_only')
   # Preserve the termination classification edge explicitly for assessment.
   x=copy.deepcopy(base);x['manager_case']=None;x['outcomes']={'client-call':'process-termination'};r=c.client_handle_projection(cat,v,x,copy.deepcopy(x));paths.append({'case':x,'result':r,'assessment':'outside_catch_failure=True on process termination at outer stage; unlike False at fixed-failure/retain-error. No exception, response, retention or destination is asserted.'})
   check('outer process termination creates no Python exception or destination '+name,lambda r=r:r['completion']=='process-termination' and r['original_exception'] is r['fixed_client_failure'] is None and r['destinations']==[] and r['retained_original'] is False,'constructed_only')
  (out/'constructed-paths.json').write_text(json.dumps(paths,indent=2)+'\n')
  for label,edit in [('missing hop',lambda x:x['ordered_hops'].pop()),('reordered hop',lambda x:x['ordered_hops'].reverse()),('wrong byte type',lambda x:x['declarations'][0].update(logical_type='str')),('wrong guard',lambda x:x['source']['stages']['response-check']['guards'].clear()),('original to stdout',lambda x:x['required_destinations'].update(original_error='stdout'))]:
   bad=copy.deepcopy(cat);edit(bad);reject('source catalogue '+label,lambda bad=bad:c.validate_client_handle(launcher,entry,manager,d['ctx']['binding'],bad),'CLIENT-SOURCE-CORRESPONDENCE','source_negative')
  changed=entry.replace(b'return result  # Preserve exact authenticated response; no re-encoding.',b'return bytes(result)  # changed source')
  reject('coordinated source conversion cannot replace direct return',lambda:c.client_handle_source(launcher,changed,manager),category='source_negative')
  check('mandatory handle predecessor actually invoked',lambda:any(x['function']=='mandatory handle derive_handle' for x in calls))
  check('sources and saved evidence unchanged',lambda:source=={n:identity((root/'code'/n).read_bytes()) for n in source} and e==d['ctx']['e'] and (root/'results/client-handle-correspondence.json').read_bytes()==saved)
 except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};(out/'failure.txt').write_text(traceback.format_exc());raise
 finally:
  sys.settrace(None);r={'result':'PASS' if error is None else 'FAIL','assertions':len(rows),'categories':{cc:sum(x['category']==cc for x in rows) for cc in sorted({x['category'] for x in rows})},'checks':rows,'error':error,'recovered':a.recovered,'environment':{'python':sys.version,'optimization':sys.flags.optimize,'cryptography_installed':importlib.metadata.version('cryptography')},'source':locals().get('source'),'database_connections':0,'session_operations':0,'requests_issued':0,'new_signatures':0,'completed_review_reruns':False,'constructed_cases_are_execution_evidence':False}
  (out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');(out/'call-observations.json').write_text(json.dumps(calls,indent=2)+'\n');(out/'constructed-cases.json').write_text(json.dumps(constructed,indent=2)+'\n')
 print('PASS',len(rows),'independent client correspondence checks')
if __name__=='__main__':main()
