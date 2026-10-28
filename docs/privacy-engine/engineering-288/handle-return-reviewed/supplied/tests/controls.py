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
 m=types.ModuleType('_handle_controls');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--write',action='store_true');p.add_argument('--recovered',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 start=time.monotonic();rows=[];cases=[];paths=[];error=None
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
  m=module(a.root/'code/correspondence.py');data=m.inputs(a.root);cat=check('derive exact handle source catalogue',lambda:m.catalogue(data));c=data['coverage'];raw,auth,anchor,obs=m.sources(data);v=c.handle_authentication(auth,anchor,obs)
  # Independent oracle inspects exact source, not the catalogue's branch list.
  t=ast.parse(auth);cl=next(n for n in t.body if isinstance(n,ast.ClassDef) and n.name=='Authority');h=next(n for n in cl.body if isinstance(n,ast.FunctionDef) and n.name=='handle');tr=next(n for n in h.body if isinstance(n,ast.Try));assigns=[n for n in ast.walk(h) if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='response' for x in n.targets)]
  check('independent success/error origins and handler class',lambda:len(assigns)==2 and {ast.literal_eval(n.value.values[2]) for n in assigns}=={True,False} and ast.unparse(tr.handlers[0].type)=='Exception')
  check('independent backend raw return and post-handler persistence',lambda:isinstance(h.body[-1],ast.Return) and ast.unparse(h.body[-1].value)=='raw' and isinstance(h.body[-2],ast.With) and ast.unparse(h.body[-2].items[0].context_expr)=='self.transaction()')
  claims=check('pristine full semantic correspondence',lambda:m.semantic(data,cat));bundle=check('pristine mandatory derivation',lambda:m.derive_handle(data,cat));saved=m.enc(bundle);receipt=a.root/'results/handle-correspondence.json'
  if a.write:receipt.write_bytes(saved)
  else:assert receipt.read_bytes()==saved
  check('saved smoke remains empty without fabricated handle records',lambda:all(r['saved_journal_rows']==0 and r['saved_journal_records']==[] and r['captured_handle_call_records']==[] and r['runtime_links'] is None and r['actual_handle_call_count'] is None and not r['inject_observation']['observed'] for r in claims))
  prior=json.loads((a.root/'retained/state/results/state-correspondence.json').read_bytes());check('all prior context members unchanged',lambda:all(all(m.enc(v)==m.enc(bundle['contexts'][i][k]) for k,v in p.items()) for i,p in enumerate(prior['contexts'])))
  fixture_path=a.root/'tests/constructed-envelopes.json'
  if a.write:
   # Exact retained source sig() and public laboratory seeds, extracted only.
   # Authentication test data; no runtime/app import, request issue or transaction.
   from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
   ns={'hashlib':hashlib,'Ed25519PrivateKey':Ed25519PrivateKey,'enc':m.enc}
   nodes=[n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id in ('VERSION','SEEDS') for x in n.targets)]
   nodes+=[next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='sig')]
   exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),'<constructed-authentication-fixture-only>','exec'),ns)
   fixture={'kind':'CONSTRUCTED-AUTHENTICATION-CONTROL','runtime_observation':False,'request_issued':False,'transaction_signed':False,'source':identity(auth),'cases':[]}
   for row in claims:
    instance=row['instance_request_context'];state=row['validated_state_anchor']['validated_state'];req=dict(version=cat['source']['constants']['VERSION'],**instance,principal='executor',challenge='a'*64,expected=state['head'],method='head',u='constructed-control',body={})
    packet=m.enc({'request':req,'signature':ns['sig']('executor',req)})
    values=[]
    for ok in (True,False):
     rr={'request':hashlib.sha256(packet).hexdigest(),'challenge':req['challenge'],'ok':ok};rr.update({'data':copy.deepcopy(state)} if ok else {'error':'ValueError:constructed control'})
     response=m.enc({'response':rr,'signature':ns['sig']('server',rr)})
     values.append({'ok':ok,'response':{'bytes_hex':response.hex()}})
    fixture['cases'].append({'context':row['context'],'instance':instance,'scope':row['validated_scope'],'packet':{'bytes_hex':packet.hex()},'responses':values})
   with fixture_path.open('xb') as f:f.write(m.enc(fixture))
  fixture=json.loads(fixture_path.read_bytes());assert fixture['runtime_observation'] is False and fixture['request_issued'] is False
  normal_run={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'normal','post_transaction':False,'return_expression':'normal','lock_exit':'normal'}
  normal_backend={k:'normal' for k in ('authenticate','reserve','action','success_response','encode_sign','response_bound','persist','return_raw')}
  for i,f in enumerate(fixture['cases']):
   check('fixture context bound to validated instance '+f['context'],lambda f=f,i=i:f['instance']==claims[i]['instance_request_context'] and f['scope']==claims[i]['validated_scope'])
   for r in f['responses']:
    backend=dict(normal_backend)
    if not r['ok']:backend.pop('success_response');backend.update(action='Exception',error_response='normal')
    scope=dict(f['scope'],instance=copy.deepcopy(f['instance']));occ='constructed:'+f['context']+':'+str(r['ok']);reference={'scope':copy.deepcopy(scope),'symbol':occ+':bytes-object'};args={'packet':copy.deepcopy(f['packet']),'inject':None}
    case={'occurrence':occ,'scope':scope,'arguments':args,'run_arguments':{'method':'handle','args':[copy.deepcopy(f['packet']),None]},'backend_arguments':copy.deepcopy(args),'backend_outcomes':backend,'run_outcomes':normal_run.copy(),**{n:{'value':copy.deepcopy(r['response']),'reference':copy.deepcopy(reference)} for n in ('underlying','run_result','wrapper_return')}}
    expected=copy.deepcopy(case);label=f['context']+(' success' if r['ok'] else ' error')
    projected=check('legitimate authenticated constructed '+label,lambda case=case,expected=expected:c.handle_value_projection(cat,v,case,expected));cases.append({'input':case,'result':projected})
    check('exact bytes and distinct three link occurrences '+label,lambda projected=projected,r=r:len({x['id'] for x in projected['links']})==3 and all(x['value']==r['response'] for x in projected['links']) and projected['run']['completion']=='normal' and not projected['run']['quarantine_called'])
    check('normal ok flag is not nonexecution or renewal '+label,lambda projected=projected:not projected['external_nonexecution_established'] and not projected['authorization_renewed'] and not projected['runtime_observation'])
    for label2,mut in [
     ('wrong method',lambda x:x['run_arguments'].update(method='state')),('wrong inject',lambda x:x['backend_arguments'].update(inject='changed')),('missing result',lambda x:x.pop('run_result')),('wrong return type',lambda x:x['run_result'].update(value=None)),('decoded value',lambda x:x['wrapper_return'].update(value=json.loads(bytes.fromhex(r['response']['bytes_hex'])))),('missing wrapper',lambda x:x.update(wrapper_return=None)),('copied reference',lambda x:x['wrapper_return']['reference'].update(symbol='copy')),
     ('wrong request',lambda x:x['arguments']['packet'].update(bytes_hex='00')),('wrong instance',lambda x:x['scope']['instance'].update(binding='f'*64)),('wrong occurrence',lambda x:x.update(occurrence='different'))]:
     bad=copy.deepcopy(case);mut(bad);check(label2+' rejects '+label,lambda bad=bad,expected=expected:rejects(lambda:c.handle_value_projection(cat,v,bad,expected)))
    bad=copy.deepcopy(case)
    for n in ('underlying','run_result','wrapper_return'):bad[n]['value']=copy.deepcopy(f['responses'][0 if not r['ok'] else 1]['response'])
    check('coordinated response substitution rejects '+label,lambda bad=bad,expected=expected:rejects(lambda:c.handle_value_projection(cat,v,bad,expected),'HANDLE-EXACT-RESPONSE:underlying'))
    noncanonical={'bytes_hex':(bytes.fromhex(r['response']['bytes_hex'])+b' ').hex()}
    check('equivalent decoded re-encoding is not exact response '+label,lambda f=f,noncanonical=noncanonical:rejects(lambda:c.handle_pair(cat,v,f['packet'],noncanonical,f['instance'])))
    projected['links'][0]['value']['bytes_hex']='00';check('returned nested mutation leaves premise intact '+label,lambda case=case,expected=expected:r['response']==expected['underlying']['value'] and c.handle_value_projection(cat,v,case,expected)['links'][0]['value']==r['response'])
  # Source semantics of escaping exceptions, with no returned byte edges.
  basecase=copy.deepcopy(cases[0]['input'])
  for stage,kind in [('authenticate','Exception'),('reserve','Exception'),('action','BaseException'),('encode_sign','Exception'),('persist','Exception')]:
   bo={};order=['authenticate','reserve','action','success_response','encode_sign','response_bound','persist','return_raw']
   for k in order:
    bo[k]=kind if k==stage else 'normal'
    if k==stage:break
   case=copy.deepcopy(basecase);case['backend_outcomes']=bo;case['run_outcomes']={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'raise','handler_reason':'normal','quarantine':'normal','lock_exit':'normal'}
   for n in ('underlying','run_result','wrapper_return'):case[n]=None
   out=check('escaping '+stage+' '+kind,lambda case=case:c.handle_value_projection(cat,v,case,copy.deepcopy(case)));paths.append(out)
   check('escaping path has no byte return or nonexecution claim '+stage,lambda out=out:out['links']==[] and out['run']['quarantine_called'] and not out['external_nonexecution_established'])
   bad=copy.deepcopy(case);bad['wrapper_return']=copy.deepcopy(basecase['wrapper_return']);check('fabricated return after escape rejects '+stage,lambda bad=bad,case=case:rejects(lambda:c.handle_value_projection(cat,v,bad,case),'HANDLE-NO-RETURN:wrapper_return'))
  bo={'authenticate':'normal','reserve':'normal','action':'process-termination'};out=c.handle_backend_path(cat,bo);check('process termination does not invent Python quarantine',lambda:out['completion']=='process-termination' and out['response_ok'] is None)
  # Expected source coverage independently regenerated, not submitted inventory.
  d=m.inner(data);g=d['guards']
  def validate_cat(value):return c.validate_handle_return(*m.sources(data),d['values']['candidate/managed-route/model.json'],d['values']['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],d['reference_module'].reference_catalogue(d),value)
  for label,mut in [('omitted field',lambda x:x['declarations'].pop()),('omitted link',lambda x:x['links'].pop()),('wrong method source',lambda x:x['source'].update(method='state')),('omitted error branch',lambda x:x['source']['response_assignments'].pop('error')),('false exception class',lambda x:x['source'].update(backend_program='BaseException catches all')),('wrong type origin',lambda x:x['declarations'][0].update(type='BOOLEAN'))]:
   bad=copy.deepcopy(cat);mut(bad);check('source coverage rejects '+label,lambda bad=bad:rejects(lambda:validate_cat(bad)))
  # Public and full semantic entries freshly revalidate the saved predecessor.
  bad=copy.deepcopy(claims);bad[0]['validated_scope']['instance']['binding']='f'*64;check('full semantic wrong instance rejects',lambda:rejects(lambda:m.semantic(data,cat,bad),'HANDLE-INSTANCE-LINEAGE'))
  e=dict(m.inner(data)['ctx']['e']);x=json.loads(e['evidence/recovery-export-0.json']);f=fixture['cases'][0];x['journal']=[['a'*64,f['packet']['bytes_hex'],f['responses'][0]['response']['bytes_hex']]];e['evidence/recovery-export-0.json']=m.enc(x)
  check('full derivation rejects constructed journal promotion',lambda:rejects(lambda:m.derive_handle(data,cat,evidence=e),'HANDLE-VALIDATED-JOURNAL'))
  bad=copy.deepcopy(cat);bad['source']['method']='state';check('full semantic coordinated catalogue rejects',lambda:rejects(lambda:m.semantic(data,bad),'HANDLE-SOURCE-CATALOGUE'))
  pristine=m.enc(claims);claims[0]['declaration']['links'].clear();claims[0]['saved_journal_records'].append({'fabricated':True})
  check('nested mutation cannot change fresh semantic expectations',lambda:m.enc(m.semantic(data,cat))==pristine)
  bad=copy.deepcopy(bundle);bad['contexts'][0].pop('handle_return_correspondence');check('public omitted mandatory relation rejects',lambda:rejects(lambda:m.validate(a.root,m.enc(bad))))
  check('pristine public receipt remains valid',lambda:m.validate(a.root,saved))
 except BaseException as ex:error=repr(ex);raise
 finally:
  report={'result':'PASS' if error is None else 'FAIL','checks':len(rows),'rows':rows,'error':error,'seconds':time.monotonic()-start,'mode':'recovered' if a.recovered else 'primary','source':{n:identity((a.root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'runtime_handle_chain':'UNAVAILABLE','constructed_cases_are_runtime_observations':False,'authentication_signatures_generated':bool(a.write),'request_issued':False,'transaction_signed':False,'database_connections':0,'session_operations':0,'completed_suites_rerun':False}
  (a.output/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');(a.output/'constructed-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(a.output/'escaping-paths.json').write_text(json.dumps(paths,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('result','checks','seconds','error')}),flush=True)
if __name__=='__main__':main()
