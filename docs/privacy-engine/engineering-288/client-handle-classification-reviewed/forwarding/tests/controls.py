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
 m=types.ModuleType('_client_controls');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--write',action='store_true');p.add_argument('--recovered',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 start=time.monotonic();rows=[];cases=[];error=None
 def check(label,fn):
  value=fn();assert value is not False,label;row={'check':label,'result':'PASS'};rows.append(row)
  with (a.output/'progress.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  print(len(rows),label,flush=True);return value
 def rejects(fn,reason=None):
  try:fn()
  except Exception as e:
   if reason is not None:assert str(e)==reason,(str(e),reason)
   return True
  raise AssertionError('Unexpected acceptance')
 try:
  m=module(a.root/'code/correspondence.py');data=m.inputs(a.root);c=data['coverage'];cat=check('new source catalogue',lambda:m.catalogue(data));launcher,entry=m.sources(data)
  # Control-owned AST traversal of defining bodies; it does not select expected
  # coverage by reading generated declarations, stage lists or origin lists.
  lt=ast.parse(launcher);et=ast.parse(entry)
  cls=next(n for n in lt.body if isinstance(n,ast.ClassDef) and n.name=='ManagedSession');sh=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='handle')
  cl=next(n for n in et.body if isinstance(n,ast.ClassDef) and n.name=='Client');ch=next(n for n in cl.body if isinstance(n,ast.FunctionDef) and n.name=='handle')
  dispatch=next(n for n in et.body if isinstance(n,ast.FunctionDef) and n.name=='_dispatch');tr=next(n for n in dispatch.body if isinstance(n,ast.Try));branch=tr.body[0];handler=tr.handlers[0]
  check('independent direct session argument and return',lambda:ast.unparse(sh.body[0])=='return self.__managed.handle(authenticated_packet)')
  check('independent client literal selector and arguments',lambda:ast.unparse(ch.body[0])=="return _dispatch(self.__token, 'handle', authenticated_packet)")
  check('independent handler boundary and original storage',lambda:ast.unparse(handler.type)=='BaseException' and ast.unparse(handler.body[0])=='owner.failure = error' and isinstance(dispatch.body[-1],ast.Expr) and dispatch.body[-1] not in handler.body)
  check('independent exact packet/result byte guards',lambda:[ast.unparse(n.test) for n in branch.body if isinstance(n,ast.If)]==['type(packet) is not bytes','type(result) is not bytes'])
  check('independent no ok-false conversion in client branch',lambda:not any(isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and n.slice.value=='ok' for n in ast.walk(branch)))
  _,auth,anchor,obs=data['prior_module'].sources(data['prior_data']);v=c.handle_authentication(auth,anchor,obs)
  bundle=check('full mandatory predecessor and client derivation',lambda:m.derive_client(data,cat));saved=m.enc(bundle);receipt=a.root/'results/client-handle-correspondence.json'
  if a.write:
   with receipt.open('xb') as out:out.write(saved)
  else:assert receipt.read_bytes()==saved
  claims=[copy.deepcopy(x['client_handle_return_correspondence']) for x in bundle['contexts']]
  prior=json.loads((a.root/'retained/handle/results/handle-correspondence.json').read_bytes())
  check('all preceding context fields unchanged',lambda:all(all(m.enc(value)==m.enc(bundle['contexts'][i][key]) for key,value in row.items()) for i,row in enumerate(prior['contexts'])))
  check('two contexts; no fabricated runtime chain',lambda:[x['context'] for x in claims]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and all(x['runtime_forwarding_links'] is None and x['actual_client_handle_call_count'] is None and x['captured_forwarding_calls']==[] and x['reference_identity_observations'] is None for x in claims))
  fixture=json.loads((a.root/'retained/handle/results/primary/constructed-cases.json').read_bytes())
  normal=['client-call','owner-lookup','owner-guard','packet-check','session-call','manager-call','session-return','response-check','dispatch-return','client-return'];cleanup={k:'unobserved' for k in ('revoke','format','cleanup','write','outer_fail')}
  def make(old,suffix):
   mc=copy.deepcopy(old);occ='constructed-client:'+old['scope']['context']+':'+suffix;mc['occurrence']=occ+'/managed-handle'
   for n in ('underlying','run_result','wrapper_return'):
    if mc[n] is not None:mc[n]['reference']['symbol']=mc['occurrence']+':response'
   scope=copy.deepcopy(mc['scope']);refs={n:{'scope':copy.deepcopy(scope),'symbol':occ+':'+n} for n in ('client','token','owner','session','manager')}
   refs.update({a:copy.deepcopy(refs[b]) for a,b in cat['reference_edges']});refs['owner_failed']=False
   return {'occurrence':occ,'scope':scope,'references':refs,'packet':{'type':'bytes','value':copy.deepcopy(mc['arguments']['packet'])},'outcomes':dict.fromkeys(normal,'normal'),'manager_case':mc,'callback':'unobserved','cleanup':cleanup.copy()}
  def project(case,expected=None):return c.client_handle_projection(cat,v,case,copy.deepcopy(case) if expected is None else expected)
  for k,f in enumerate(fixture):
   case=make(f['input'],'ok-'+str(k));expected=copy.deepcopy(case);label=case['scope']['context']+':'+str(k%2==0)
   out=check('legitimate exact-byte forwarding '+label,lambda:project(case,expected));cases.append({'input':case,'result':out})
   check('five distinct value occurrences and three argument hops '+label,lambda:len(out['hops'])==len({h['id'] for h in out['hops']})==5 and len(out['argument_hops'])==3 and [h['declaration'] for h in out['hops']]==cat['ordered_hops'])
   check('exact bytes preserved to permitted client destination '+label,lambda:all(h['value']==case['manager_case']['wrapper_return']['value'] for h in out['hops']) and out['destinations']==[{'kind':'exact-response-bytes','to':'general-client','value':case['manager_case']['wrapper_return']['value']}] and out['original_exception'] is None)
   check('source-defined inject default, not an observation '+label,lambda:out['argument_hops'][-1]['inject'] is None and not out['runtime_observation'])
   for label2,mut in [('missing value hop',lambda x:x['hops'].pop()),('reordered value hops',lambda x:x['hops'].reverse()),('omitted argument hop',lambda x:x['argument_hops'].pop()),('wrong dispatch method',lambda x:x['argument_hops'][0].update(operation='state')),('raw error to client',lambda x:x['destinations'].append({'kind':'original-exception','to':'general-client'})),('stdout response',lambda x:x['destinations'][0].update(to='stdout')),('status capability',lambda x:x['destinations'].append({'kind':'manager-status','to':'general-client'})),('wrong recorded return type',lambda x:x['hops'][-1].update(value=None)),('altered bytes',lambda x:x['hops'][-1]['value'].update(bytes_hex='00')),('misclassified error return',lambda x:x.update(completion='fixed-client-failure'))]:
    bad=copy.deepcopy(out);mut(bad);check(label2+' rejects '+label,lambda bad=bad:rejects(lambda:c.validate_client_handle_projection(cat,v,case,expected,bad)))
   for label2,mut in [('wrong instance',lambda x:x['scope']['instance'].update(binding='f'*64)),('wrong acquisition',lambda x:x['scope'].update(acquisition='stale')),('wrong owner manager reference',lambda x:x['references']['session.managed'].update(symbol='wrong-manager')),('wrong request',lambda x:x['packet']['value'].update(bytes_hex='00')),('wrong inject',lambda x:x['manager_case']['arguments'].update(inject='changed')),('wrong method',lambda x:x['manager_case']['run_arguments'].update(method='state')),('wrong manager occurrence',lambda x:x['manager_case'].update(occurrence='other'))]:
    bad=copy.deepcopy(case);mut(bad);check(label2+' premise rejects '+label,lambda bad=bad:rejects(lambda:project(bad,expected)))
   bad=copy.deepcopy(case)
   for name in ('underlying','run_result','wrapper_return'):bad['manager_case'][name]['value']['bytes_hex']='00'
   check('coordinated manager-return substitution rejects '+label,lambda:rejects(lambda:project(bad,expected)))
   out['hops'][0]['value']['bytes_hex']='00';out['reference_bindings']['manager']['scope'].clear()
   check('nested result mutation cannot alter expectations '+label,lambda:project(case,expected)['hops'][0]['value']==expected['manager_case']['underlying']['value'])
  base=make(fixture[0]['input'],'base')
  # Different source occurrence remains different even with the same bytes.
  other=make(fixture[0]['input'],'another');aa=project(base);bb=project(other)
  check('equal bytes do not merge distinct conditional occurrences',lambda:aa['hops'][-1]['value']==bb['hops'][-1]['value'] and not ({h['id'] for h in aa['hops']}&{h['id'] for h in bb['hops']}))
  for field in ('owners[token]','owner_failed'):
   case=copy.deepcopy(base);case['references'][field]=None if field=='owners[token]' else True;case['manager_case']=None;case['outcomes']={n:'normal' for n in ['client-call','owner-lookup','owner-guard','fixed-failure']}
   out=check('source-defined fixed refusal '+field,lambda:project(case));cases.append({'input':case,'result':out});check('refusal does not invent a manager invocation '+field,lambda:out['completion']=='fixed-client-failure' and out['hops']==[] and out['manager'] is None and not out['retained_original'])
  # Wrong input types are legitimate rejection routes, not authenticated calls.
  for typ,val in [('str','invalid packet'),('int',4),('NoneType',None)]:
   case=copy.deepcopy(base);case['packet']={'type':typ,'value':val};case['manager_case']=None;case['outcomes']={n:'normal' for n in ['client-call','owner-lookup','owner-guard','packet-check','retain-error','fixed-failure']};case['callback']='returns';case['cleanup']=dict.fromkeys(cleanup,'normal')
   out=check('wrong input type becomes retained TypeError and fixed failure '+typ,lambda:project(case));cases.append({'input':case,'result':out})
   check('fixed/general and original/evidence destinations separate '+typ,lambda:out['original_exception']['message']=='PACKET-BYTES' and out['retained_original'] and out['evidence_route']['original_reraised_to_launcher'] and {d['to'] for d in out['destinations']}=={'general-client','owner.failure','launcher-existing-error-cleanup','existing-launcher-evidence/failure-*.json','general-entry-caller'})
  for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
   case=make(next(f['input'] for f in fixture if f['input']['scope']['context']==context),'escaping');mc=case['manager_case'];mc['backend_outcomes']={'authenticate':'Exception'};mc['run_outcomes']={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'raise','handler_reason':'normal','quarantine':'normal','lock_exit':'normal'}
   for n in ('underlying','run_result','wrapper_return'):mc[n]=None
   case['outcomes']={n:'normal' for n in ['client-call','owner-lookup','owner-guard','packet-check','session-call','manager-call','retain-error','fixed-failure']};case['callback']='raises';case['cleanup']=dict.fromkeys(cleanup,'normal')
   out=check('escaping manager exception retained '+context,lambda:project(case));cases.append({'input':case,'result':out})
   check('escaping exception is no normal byte return '+context,lambda:out['hops']==[] and out['original_exception']['kind']=='manager-escaping-exception' and out['evidence_route']['explicit_cause']=='client_error' and not out['external_nonexecution_established'] and not out['authorization_renewed'])
   for label,mut in [('manager-to-client raw exception',lambda x:x['destinations'].append({'kind':'original-exception-reference','to':'general-client'})),('exception-as-response',lambda x:x.update(completion='normal')),('fixed message substitution',lambda x:x['fixed_client_failure'].update(message='raw secret')),('renewal from refusal',lambda x:x.update(authorization_renewed=True)),('guaranteed record bytes',lambda x:x['evidence_route'].update(bytes='invented'))]:
    bad=copy.deepcopy(out);mut(bad);check(label+' rejects '+context,lambda bad=bad:rejects(lambda:c.validate_client_handle_projection(cat,v,case,case,bad)))
   for stage in ('revoke','format','cleanup','write'):
    branch=copy.deepcopy(case);branch['cleanup'][stage]='raise';following=False
    for n in cleanup:
     if following:branch['cleanup'][n]='unobserved'
     if n==stage:following=True
    if stage!='revoke':branch['cleanup']['outer_fail']='normal'
    result=check('failed/interrupted retention '+stage+' '+context,lambda branch=branch:project(branch));cases.append({'input':branch,'result':result});check('no evidence-write success inferred '+stage+' '+context,lambda result=result:not any(d['to']=='existing-launcher-evidence/failure-*.json' for d in result['destinations']) and result['evidence_route']['bytes'] is None)
  for stage in ('client-call','owner-lookup','owner-guard','session-call','response-check','client-return'):
   case=copy.deepcopy(base);stop=normal.index(stage);case['outcomes']={n:('raise' if n==stage else 'normal') for n in normal[:stop+1]}
   caught=stage in ('session-call','response-check')
   if caught:case['outcomes'].update({'retain-error':'normal','fixed-failure':'normal'})
   if stop<normal.index('manager-call'):case['manager_case']=None
   out=check('source catch boundary '+stage,lambda:project(case));cases.append({'input':case,'result':out})
   check('outside failures not silently fixed '+stage,lambda:out['completion']==('fixed-client-failure' if caught else 'unqualified-escape'))
  case=copy.deepcopy(base);case['manager_case']=None;case['outcomes']={'client-call':'normal','owner-lookup':'normal','owner-guard':'normal','packet-check':'process-termination'};out=project(case)
  check('process termination supplies no retention or unwind',lambda:out['completion']=='process-termination' and not out['retained_original'] and out['fixed_client_failure'] is None)
  # Independently regenerate expected source/declaration coverage for mutation checks.
  boundary=m.inner(data)['ctx']['binding'];manager=data['prior_module'].catalogue(data['prior_data'])
  for label,mut in [('declaration omitted',lambda x:x['declarations'].pop()),('guard omitted',lambda x:x['source']['stages']['response-check']['guards'].clear()),('hop order',lambda x:x['ordered_hops'].reverse()),('wrong origin',lambda x:x['source']['anchors']['session-handle'].update(expression='return other')),('raw status capability',lambda x:x['source']['public_methods'].append('status')),('false error routing',lambda x:x['required_destinations'].update(original_error='general-client')),('wrong type',lambda x:x['declarations'][0].update(logical_type='dict')),('stale manager',lambda x:x['manager_relation']['source'].update(method='state'))]:
   bad=copy.deepcopy(cat);mut(bad);check('catalogue mutation rejects '+label,lambda bad=bad:rejects(lambda:c.validate_client_handle(*m.sources(data),manager,boundary,bad)))
  altered=entry.replace(b'return result  # Preserve exact authenticated response; no re-encoding.',b'return bytes(result)  # mutation')
  check('coordinated source/boundary change rejects semantic shape',lambda:rejects(lambda:c.client_handle_source(launcher,altered,manager)))
  # Full public/internal paths rebuild the predecessor evidence; no submitted
  # report, returned nested tree or forged empty-journal row becomes authority.
  wrong=copy.deepcopy(claims);wrong[1]['validated_scope']['instance']['binding']='f'*64
  check('full semantic wrong-instance context rejects',lambda:rejects(lambda:m.semantic(data,cat,wrong),'CLIENT-CONTEXT-CORRESPONDENCE'))
  bad=copy.deepcopy(bundle);bad['contexts'][0].pop('client_handle_return_correspondence')
  check('public missing mandatory extension rejects',lambda:rejects(lambda:m.validate(a.root,m.enc(bad))))
  if not a.recovered:
   e=dict(m.inner(data)['ctx']['e']);x=json.loads(e['evidence/recovery-export-0.json']);old=fixture[0]['input'];x['journal']=[['a'*64,old['arguments']['packet']['bytes_hex'],old['wrapper_return']['value']['bytes_hex']]];e['evidence/recovery-export-0.json']=m.enc(x)
   check('coordinated fabricated journal rejected by full derivation',lambda:rejects(lambda:m.derive_client(data,cat,evidence=e),'HANDLE-VALIDATED-JOURNAL'))
   badcat=copy.deepcopy(cat);badcat['source']['operation']='state';badrows=copy.deepcopy(claims)
   for row in badrows:row['declaration']=copy.deepcopy(badcat)
   check('coordinated source and reports rejected by semantic entry',lambda:rejects(lambda:m.semantic(data,badcat,badrows),'CLIENT-SOURCE-CATALOGUE'))
  baseline=m.enc(claims);claims[0]['declaration']['ordered_hops'].clear();claims.clear();bundle['contexts'][1]['client_handle_return_correspondence']['declaration']['source']['public_methods'].append('status')
  check('returned nested mutation leaves full expectations pristine',lambda:m.enc(m.semantic(data,cat))==baseline)
  check('pristine saved public receipt passes',lambda:m.validate(a.root,saved))
 except BaseException as ex:error=repr(ex);raise
 finally:
  report={'result':'PASS' if error is None else 'FAIL','checks':len(rows),'rows':rows,'error':error,'seconds':time.monotonic()-start,'mode':'recovered' if a.recovered else 'primary','source':{n:identity((a.root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'runtime_client_handle_chain':'UNAVAILABLE','new_signatures':0,'requests_issued':0,'database_connections':0,'session_operations':0,'completed_suites_rerun':False,'constructed_not_runtime':True}
  (a.output/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');(a.output/'constructed-cases.json').write_text(json.dumps(cases,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('result','checks','seconds','error')}),flush=True)
if __name__=='__main__':main()
