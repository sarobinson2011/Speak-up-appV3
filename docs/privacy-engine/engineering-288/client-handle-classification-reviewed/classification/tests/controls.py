"""New handle controls only. Constructed auth fixtures never reach a session."""
import argparse,ast,copy,hashlib,json,os,sys,time,types
from pathlib import Path
def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
 if event=='exec' and args[0].co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
sys.addaudithook(audit)
_kinds={}
def guard(frame,event,arg):
 if event!='call':return None
 f=frame.f_code.co_filename;k=_kinds.get(f)
 if k is None:
  n=f.rsplit('/',1)[-1];k=1 if n in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') else 2 if n=='prospective_entry.py' else 0;_kinds[f]=k
 if k==1 or k==2 and frame.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status'):raise AssertionError('APPLICATION-EXECUTION')
 return None
sys.settrace(guard)
def module(p):
 m=types.ModuleType('_classification_controls');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--write',action='store_true');p.add_argument('--recovered',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 rows=[];cases=[];error=None;start=time.monotonic()
 def check(name,fn):
  value=fn();assert value is not False,name;row={'check':name,'result':'PASS'};rows.append(row)
  with (a.output/'progress.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  print(len(rows),name,flush=True);return value
 def rejects(fn):
  try:fn()
  except ValueError:return True
  raise AssertionError('Contradictory claim accepted')
 try:
  m=module(a.root/'code/correspondence.py');d=m.inputs(a.root);c=d['coverage'];cat=m.catalogue(d);_,authority,anchor,obs=d['prior_module'].sources(d['prior_data']);v=c.handle_authentication(authority,anchor,obs)
  launcher,entry=m.sources(d);tree=ast.parse(entry);dispatch=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_dispatch');tr=next(n for n in dispatch.body if isinstance(n,ast.Try));fail=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_fail')
  check('source catch is BaseException around try body only',lambda:ast.unparse(tr.handlers[0].type)=='BaseException' and ast.unparse(tr.handlers[0].body[0])=='owner.failure = error')
  check('source owner lookup and guard precede try',lambda:dispatch.body.index(tr)==2 and isinstance(dispatch.body[0],ast.Assign) and isinstance(dispatch.body[1],ast.If))
  check('ordinary fixed helper is an intentional raise from None',lambda:isinstance(fail.body[0],ast.Raise) and fail.body[0].exc.func.id=='ClientFailure' and isinstance(fail.body[0].cause,ast.Constant) and fail.body[0].cause.value is None)
  caveat=json.loads((a.root/'review/results/classification-caveat.json').read_bytes());check('all six original prefix caveats preserved',lambda:len(caveat['cases'])==6 and all(x['result']['outside_catch_failure'] is True and x['result']['completion']=='process-termination' for x in caveat['cases']))
  def project(case):return c.client_handle_projection(cat,v,case,copy.deepcopy(case))
  def valid(case,expected_kind,location,flag):
   out=project(case);cl=out['outcome_classification'];assert cl['modeled_kind']==expected_kind and cl['location_relative_to_dispatch_catch']==location and out['outside_catch_failure'] is flag
   assert cl['runtime_python_exception_evidence']==cl['runtime_python_unwind_evidence']=='UNAVAILABLE' and not cl['retention_cleanup_or_authority_established_by_classification']
   assert c.validate_client_handle_projection(cat,v,case,copy.deepcopy(case),out)
   cases.append({'input':copy.deepcopy(case),'output':copy.deepcopy(out)});return out
  stages=['client-call','owner-lookup','owner-guard'];locations={'client-call':'caller-outside-dispatch','owner-lookup':'dispatch-before-try','owner-guard':'dispatch-before-try'}
  for old in caveat['cases']:
   case=copy.deepcopy(old['case']);stage=list(case['outcomes'])[-1];context=case['scope']['context'];label=context+':'+stage
   out=check('prefix termination classified without Python raise '+label,lambda:valid(case,'process-termination',locations[stage],False))
   check('termination alone establishes no error, cleanup or authorization '+label,lambda:out['outcome_classification']['terminal_python_exception_in_model'] is None and out['original_exception'] is None and out['fixed_client_failure'] is None and not out['retained_original'] and out['evidence_route']['original_reraised_to_launcher'] is None and out['destinations']==[] and not out['authorization_renewed'])
   for title,mut in [('old true flag',lambda x:x.update(outside_catch_failure=True)),('exception evidence',lambda x:x['outcome_classification'].update(runtime_python_exception_evidence='ESTABLISHED')),('unwind evidence',lambda x:x['outcome_classification'].update(runtime_python_unwind_evidence='ESTABLISHED')),('outside location as exception',lambda x:x['outcome_classification'].update(modeled_kind='unexpected-raise',terminal_python_exception_in_model=True)),('retained error',lambda x:x.update(retained_original=True)),('cleanup completion',lambda x:x['evidence_route'].update(retention='complete')),('renewed authorization',lambda x:x.update(authorization_renewed=True))]:
    bad=copy.deepcopy(out);mut(bad);check('contradiction rejects '+title+' '+label,lambda bad=bad:rejects(lambda:c.validate_client_handle_projection(cat,v,case,case,bad)))
   badcase=copy.deepcopy(case);badcase['callback']='returns'
   check('invented post-termination callback rejects '+label,lambda:rejects(lambda:project(badcase)))
   raised=copy.deepcopy(case);raised['outcomes'][stage]='raise';out=check('source-supported prefix raise remains outside '+label,lambda:valid(raised,'unexpected-raise',locations[stage],True))
   check('conditional raise does not supply observed unwind '+label,lambda:out['outcome_classification']['terminal_python_exception_in_model'] is True and out['outcome_classification']['runtime_python_unwind_evidence']=='UNAVAILABLE')
  oldw=json.loads((a.root/'original/results/focused-correction/cases.json').read_bytes())
  for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
   helper=copy.deepcopy(next(x['input'] for x in oldw if x['input']['scope']['context']==context and 'fixed-failure' in x['input']['outcomes']))
   out=check('original corrected helper-raise witness preserved '+context,lambda:valid(helper,'unexpected-raise','fixed-helper-outside-protected-region',True))
   bad=copy.deepcopy(out);bad['outside_catch_failure']=False;check('earliest original false classification rejects '+context,lambda:rejects(lambda:c.validate_client_handle_projection(cat,v,helper,helper,bad)))
   helper['outcomes']['fixed-failure']='normal';out=check('intentional fixed raise is distinct from unexpected failure '+context,lambda:valid(helper,'intentional-fixed-raise','fixed-helper-outside-protected-region',False))
   check('false flag does not mean no modeled Python exception '+context,lambda:out['outcome_classification']['terminal_python_exception_in_model'] is True and out['fixed_client_failure'] is not None)
   helper['outcomes']['fixed-failure']='process-termination';out=check('refusal helper termination remains no exception evidence '+context,lambda:valid(helper,'process-termination','fixed-helper-outside-protected-region',False))
   # The prior focused correction saved helper cases only. Construct storage
   # premises from the saved context-specific prefix; do not relabel observations.
   storage=copy.deepcopy(next(x['case'] for x in caveat['cases'] if x['case']['scope']['context']==context))
   storage['references']['owners[token]']=copy.deepcopy(storage['references']['owner']);storage['references']['owner_failed']=False
   storage['packet']={'type':'str','value':'invalid packet'};storage['manager_case']=None
   storage['outcomes']=dict.fromkeys(('client-call','owner-lookup','owner-guard','packet-check','retain-error'),'normal')
   storage['outcomes']['retain-error']='raise';out=check('handler-storage raise preserves original correction '+context,lambda:valid(storage,'unexpected-raise','dispatch-handler-body',True));check('failed storage stays unknown '+context,lambda:out['retained_original'] is None)
   storage['outcomes']['retain-error']='process-termination';out=check('storage termination is not a Python raise '+context,lambda:valid(storage,'process-termination','dispatch-handler-body',False));check('prior modeled error remains separate from termination '+context,lambda:out['original_exception']['kind']=='source-TypeError' and out['retained_original'] is None and out['outcome_classification']['terminal_python_exception_in_model'] is None)
   storage['outcomes']['retain-error']='normal';storage['outcomes']['fixed-failure']='process-termination';out=check('termination after confirmed conditional storage '+context,lambda:valid(storage,'process-termination','fixed-helper-outside-protected-region',False))
   check('prior storage retained without inventing cleanup or unwind '+context,lambda:out['retained_original'] is True and out['evidence_route']['original_reraised_to_launcher'] is None and [x['to'] for x in out['destinations']]==['owner.failure'] and out['fixed_client_failure'] is None)
   bad=copy.deepcopy(out);bad['retained_original']=False;check('blanket erasure of preceding storage rejects '+context,lambda:rejects(lambda:c.validate_client_handle_projection(cat,v,storage,storage,bad)))
   badcase=copy.deepcopy(storage);badcase['callback']='returns';badcase['cleanup']=dict.fromkeys(badcase['cleanup'],'normal');check('invented cleanup after process termination rejects '+context,lambda:rejects(lambda:project(badcase)))
  normals=json.loads((a.root/'original/results/recovered/constructed-cases.json').read_bytes())[:4]
  for savedcase in normals:
   case=copy.deepcopy(savedcase['input']);label=case['scope']['context']+':'+str(case['manager_case']['backend_outcomes'].get('action'))
   out=check('normal byte return remains distinct '+label,lambda:valid(case,'normal-return','caller-outside-dispatch',False))
   # Historical saved results include a deliberately mutated returned hop.
   # Exact response expectations come from the saved authenticated input.
   check('normal exact response bytes at every forwarding hop '+label,lambda:len(out['hops'])==5 and all(h['value']==case['manager_case']['wrapper_return']['value'] for h in out['hops']) and out['destinations'][0]['value']==case['manager_case']['wrapper_return']['value'])
   for stage,location in [('packet-check','dispatch-protected-try'),('client-return','caller-outside-dispatch')]:
    cut=copy.deepcopy(case);ordered=list(cut['outcomes']);index=ordered.index(stage);cut['outcomes']={n:('process-termination' if n==stage else 'normal') for n in ordered[:index+1]}
    if stage=='packet-check':cut['manager_case']=None
    out=check('location remains separate for '+stage+' '+label,lambda cut=cut,location=location:valid(cut,'process-termination',location,False))
    check('termination cannot infer missing return '+stage+' '+label,lambda out=out:not any(h['declaration']=='client-return' for h in out['hops']) and out['outcome_classification']['terminal_python_exception_in_model'] is None)
  # Regeneration, not caller-supplied classification, owns validation expectations.
  case=copy.deepcopy(caveat['cases'][0]['case']);out=project(case);out['outcome_classification']['source']['guards'].clear();out['outside_catch_failure']=True
  check('nested result mutation leaves expectations isolated',lambda:project(case)['outside_catch_failure'] is False)
  badcat=copy.deepcopy(cat);badcat['outside_catch_failure_contract']['true_iff']='termination outside catch'
  manager=d['prior_module'].catalogue(d['prior_data']);boundary=m.inner(d)['ctx']['binding']
  check('stale semantic contract rejects source regeneration',lambda:rejects(lambda:c.validate_client_handle(*m.sources(d),manager,boundary,badcat)))
  receipt=a.root/'results/client-handle-correspondence.json'
  if a.write:
   result=check('current mandatory derivation carries versioned contract in both contexts',lambda:m.derive_client(d,cat));raw=m.enc(result)
   with receipt.open('xb') as f:f.write(raw)
   check('receipt does not manufacture runtime classifications',lambda:all(x['client_handle_return_correspondence']['runtime_forwarding_links'] is None and x['client_handle_return_correspondence']['declaration']['outside_catch_failure_contract']['runtime_evidence_supplied'] is False for x in result['contexts']))
   old=(a.root/'original/results/client-handle-correspondence.json').read_bytes();check('old-semantics public receipt rejects',lambda:rejects(lambda:m.validate(a.root,old)))
  else:check('recovered public validation accepts exact current receipt',lambda:m.validate(a.root,receipt.read_bytes()))
 except BaseException as ex:error=repr(ex);raise
 finally:
  report={'result':'PASS' if error is None else 'FAIL','checks':len(rows),'rows':rows,'error':error,'seconds':time.monotonic()-start,'mode':'recovered' if a.recovered else 'primary','source':{n:identity((a.root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'only_new_classification_controls':True,'old_suites_rerun':False,'requests':0,'database_connections':0,'session_operations':0,'new_signatures':0,'constructed_not_runtime':True}
  (a.output/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');(a.output/'cases.json').write_text(json.dumps(cases,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('result','checks','seconds','error')}),flush=True)
if __name__=='__main__':main()
