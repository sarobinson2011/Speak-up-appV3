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
  if name=='derive_state' and parent=='_basis':calls.append({'function':'mandatory state derive_state','file':f,'source':identity(Path(f).read_bytes())})
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
  raw,auth,anchor,obs=m.sources(data);oracle=runpy.run_path(str(Path(__file__).with_name('source_oracle.py')));model=d['values']['candidate/managed-route/model.json'];producer=d['values']['candidate/managed-route/producers.json'];refs=d['reference_module'].reference_catalogue(d)
  ar=check('independent complete handle source and guard audit',lambda:oracle['audit'](raw,auth,anchor,obs,cat,model,producer,refs));(out/'source-audit.json').write_text(json.dumps(ar,indent=2)+'\n')
  claims=check('legitimate full semantic relation',lambda:m.semantic(data,cat));bundle=check('legitimate mandatory derivation',lambda:m.derive_handle(data,cat));saved=(root/'results/handle-correspondence.json').read_bytes();check('exact saved receipt',lambda:enc(bundle)==saved)
  public=check('legitimate public validation',lambda:m.validate(root,saved));prior=json.loads((root/'retained/state/results/state-correspondence.json').read_bytes());basis=m._basis(data);v=c.handle_authentication(auth,anchor,obs)
  check('exact ordered context domain',lambda:[x['context'] for x in claims]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
  export=json.loads(e['evidence/recovery-export-0.json']);events=json.loads(e['evidence/execution-trace.json'])['events'];state=json.loads(bytes.fromhex(export['head']));fixtures=json.loads((root/'tests/constructed-envelopes.json').read_bytes())
  check('fixture provenance remains constructed only',lambda:fixtures['kind']=='CONSTRUCTED-AUTHENTICATION-CONTROL' and fixtures['runtime_observation'] is fixtures['request_issued'] is fixtures['transaction_signed'] is False and fixtures['source']==identity(auth))
  keys={role:Ed25519PrivateKey.from_private_bytes(hashlib.sha256(('PUBLIC-LAB-ONLY-'+role).encode()).digest()).public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw).hex() for role in ('executor','observer','server')}
  keyfixture=json.loads(d['ctx']['c']['retained/launcher/results/signature-fixture.json'])
  check('independent source public keys and retained observer key match',lambda:keys==v['public_keys'] and keys['observer']==keyfixture['public_key_hex'])
  normal_run={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'normal','post_transaction':False,'return_expression':'normal','lock_exit':'normal'}
  normal_backend={k:'normal' for k in ('authenticate','reserve','action','success_response','encode_sign','response_bound','persist','return_raw')}
  cases=[]
  for i,row in enumerate(claims):
   name=row['context'];old=prior['contexts'][i];fixture=fixtures['cases'][i];scope=row['validated_scope'];instance=row['instance_request_context']
   check('all predecessor context members unchanged '+name,lambda i=i,old=old:all(enc(bundle['contexts'][i][k])==enc(x) for k,x in old.items()))
   check('validated HEAD instance and configuration join '+name,lambda row=row,old=old:row['validated_state_anchor']==old['state_return_correspondence']['validated_state_anchor'] and row['validated_scope']['instance']==old['hf01_evidence_binding']['instance'] and row['instance_request_context']=={'binding':state['binding'],'pilot':export['config']['pilot'],'session':export['config']['session']} and row['predecessor_receipt']==identity((root/'retained/state/results/state-correspondence.json').read_bytes()))
   check('saved empty journal and absent handle calls derived '+name,lambda row=row:export['journal']==row['saved_journal_records']==[] and row['saved_journal_rows']==0 and row['captured_handle_call_records']==[] and not any(x['event']=='call' and (x['function'] in ('ManagedAuthority.handle','Authority.handle') or x['function']=='ManagedAuthority._run' and x.get('arguments',{}).get('method')=='handle') for x in events))
   check('missing observations do not become None returns or lifetime zero '+name,lambda row=row:all(row[k] is None for k in ('runtime_links','packet_observation','underlying_response_observation','run_result_observation','wrapper_return_observation','actual_handle_call_count','multiplicity')) and row['inject_observation']=={'observed':False,'value':None} and row['classification']=='UNKNOWN')
   check('separate observer and original trace retained '+name,lambda old=old:old['state_return_correspondence']['separate_observer']['joins_to_three_return_links'] is None and old['state_return_correspondence']['separate_observer']['frame'] is None and len({x['frame'] for x in events if x['event']=='call'})==18)
   check('fixture scope anchored independently '+name,lambda fixture=fixture,row=row:fixture['scope']==row['validated_scope'] and fixture['instance']==row['instance_request_context'])
   packet=bytes.fromhex(fixture['packet']['bytes_hex']);q=json.loads(packet);request=q['request']
   def authenticate_fixture():
    assert enc(q)==packet
    Ed25519PublicKey.from_public_bytes(bytes.fromhex(keys[request['principal']])).verify(bytes.fromhex(q['signature']),cat['source']['constants']['VERSION'].encode()+b'\0'+enc(request))
    assert {k:request[k] for k in ('binding','pilot','session')}==instance and request['method']=='head' and request['body']=={} and request['expected']==state['head']
    for rr in fixture['responses']:
     b=bytes.fromhex(rr['response']['bytes_hex']);obj=json.loads(b);r=obj['response'];assert enc(obj)==b and type(r['ok']) is bool and r['ok'] is rr['ok'] and r['request']==hashlib.sha256(packet).hexdigest() and r['challenge']==request['challenge']
     Ed25519PublicKey.from_public_bytes(bytes.fromhex(keys['server'])).verify(bytes.fromhex(obj['signature']),cat['source']['constants']['VERSION'].encode()+b'\0'+enc(r))
     if r['ok']:assert r['data']==state
     else:assert type(r['error']) is str and r['error']=='ValueError:constructed control'
    return True
   check('independent exact envelope and Ed25519 verification '+name,authenticate_fixture,'constructed_only')
   for rr in fixture['responses']:
    label=name+(' success' if rr['ok'] else ' handled error');bo=dict(normal_backend)
    if not rr['ok']:bo.pop('success_response');bo.update(action='Exception',error_response='normal')
    scoped=dict(copy.deepcopy(scope),instance=copy.deepcopy(instance));occ='review:handle:'+name+':'+str(rr['ok']);reference={'scope':copy.deepcopy(scoped),'symbol':occ+':response'};args={'packet':copy.deepcopy(fixture['packet']),'inject':None}
    case={'occurrence':occ,'scope':scoped,'arguments':args,'run_arguments':{'method':'handle','args':[copy.deepcopy(fixture['packet']),None]},'backend_arguments':copy.deepcopy(args),'backend_outcomes':bo,'run_outcomes':dict(normal_run),**{n:{'value':copy.deepcopy(rr['response']),'reference':copy.deepcopy(reference)} for n in ('underlying','run_result','wrapper_return')}}
    expected=copy.deepcopy(case);cases.append(expected)
    projected=check('normal conditional forwarding '+label,lambda case=case,expected=expected:c.handle_value_projection(cat,v,case,expected),'constructed_only');constructed.append({'premise':expected,'result':copy.deepcopy(projected)})
    check('three distinct links exact unnormalized bytes '+label,lambda projected=projected,rr=rr:len({x['id'] for x in projected['links']})==3 and all(x['value']==rr['response'] for x in projected['links']) and projected['runtime_observation'] is projected['physical_object_identity_established'] is projected['external_nonexecution_established'] is projected['authorization_renewed'] is projected['admission'] is False,'constructed_only')
    edits=[('wrong selector',lambda x:x['run_arguments'].update(method='state')),('missing backend value',lambda x:x.update(underlying=None)),('missing local result',lambda x:x.pop('run_result')),('missing wrapper value',lambda x:x.update(wrapper_return=None)),('null bytes',lambda x:x['run_result'].update(value=None)),('decoded bytes substitute',lambda x:x['wrapper_return'].update(value=json.loads(bytes.fromhex(rr['response']['bytes_hex'])))),('uppercase hex',lambda x:x['underlying']['value'].update(bytes_hex=x['underlying']['value']['bytes_hex'].upper())),('integer hex',lambda x:x['run_result'].update(value={'bytes_hex':0})),('altered reference',lambda x:x['wrapper_return']['reference'].update(symbol='different')),('wrong instance',lambda x:x['scope']['instance'].update(binding='f'*64)),('wrong acquisition',lambda x:x['scope'].update(acquisition='other')),('incorrect inject forwarding',lambda x:x['backend_arguments'].update(inject=0)),('wrong order of arguments',lambda x:x['run_arguments']['args'].reverse()),('changed occurrence',lambda x:x.update(occurrence='other'))]
    if a.recovered:edits=[x for x in edits if x[0] in ('wrong selector','missing local result','null bytes','wrong instance','incorrect inject forwarding','altered reference')]
    for label2,edit in edits:
     bad=copy.deepcopy(case);edit(bad);reject('conditional '+label2+' '+label,lambda bad=bad,expected=expected:c.handle_value_projection(cat,v,bad,expected),category='constructed_negative')
    bad=copy.deepcopy(case)
    for n in ('underlying','run_result','wrapper_return'):bad[n]['value']=copy.deepcopy(fixture['responses'][0 if not rr['ok'] else 1]['response'])
    reject('coordinated signed response substitution '+label,lambda bad=bad,expected=expected:c.handle_value_projection(cat,v,bad,expected),'HANDLE-EXACT-RESPONSE:underlying','constructed_negative')
    reject('independent instance binding '+label,lambda fixture=fixture,rr=rr:c.handle_pair(cat,v,fixture['packet'],rr['response'],dict(fixture['instance'],session='foreign')),'HANDLE-INSTANCE:session','constructed_negative')
    payload=bytes.fromhex(rr['response']['bytes_hex']);changed={'bytes_hex':(payload+b' ').hex()}
    reject('normalization cannot replace exact envelope '+label,lambda changed=changed,fixture=fixture:c.handle_pair(cat,v,fixture['packet'],changed,fixture['instance']),'ENVELOPE-CANONICAL','constructed_negative')
    projected['links'][0]['value']['bytes_hex']='00';projected['arguments']['packet']['bytes_hex']='ff';projected['scope']['instance']['binding']='bad';projected['verified_pair']['request']['body']['changed']=True
    check('nested result does not mutate premises '+label,lambda case=case,expected=expected:case==expected and c.handle_value_projection(cat,v,case,expected)['links'][0]['value']==expected['underlying']['value'],'constructed_only')
   # Equal bytes are separate conditional occurrences, not a replay entitlement.
   first=copy.deepcopy(cases[-2]);second=copy.deepcopy(first);second['occurrence']+=':second'
   one=c.handle_value_projection(cat,v,first,copy.deepcopy(first));two=c.handle_value_projection(cat,v,second,copy.deepcopy(second))
   check('equal bytes distinct occurrence identifiers '+name,lambda one=one,two=two:one['links'][0]['value']==two['links'][0]['value'] and set(x['id'] for x in one['links']).isdisjoint(x['id'] for x in two['links']),'constructed_only')
  # Source imposes no inject type rule at this forwarding boundary. These
  # head-method premises do not claim fault-trigger feasibility or execution.
  for inject in (None,'after_decision_commit',0,True,[],{'opaque':'parameter'}):
   if a.recovered and inject not in (None,'after_decision_commit'):continue
   x=copy.deepcopy(cases[0]);x['arguments']['inject']=copy.deepcopy(inject);x['run_arguments']['args'][1]=copy.deepcopy(inject);x['backend_arguments']['inject']=copy.deepcopy(inject)
   check('source supported opaque inject '+repr(inject),lambda x=x:c.handle_value_projection(cat,v,x,copy.deepcopy(x))['arguments']==x['arguments'],'constructed_only')
  x=copy.deepcopy(cases[0]);x['arguments']['inject']=True;x['run_arguments']['args'][1]=True;x['backend_arguments']['inject']=1
  reject('bool int inject distinction',lambda:c.handle_value_projection(cat,v,x,copy.deepcopy(x)),'HANDLE-BACKEND-ARGUMENTS','constructed_negative')
  # Independent stage outcomes from the audited source order and handler region.
  paths=[];stages=['authenticate','reserve','action','success_response','encode_sign','response_bound','persist','return_raw']
  for stage in stages:
   for failure in ('Exception','BaseException','process-termination'):
    if a.recovered and stage not in ('authenticate','action','encode_sign','persist'):continue
    bo={k:'normal' for k in stages[:stages.index(stage)]};bo[stage]=failure;caught=failure=='Exception' and stage in ('action','success_response')
    if caught:bo['error_response']='normal';bo.update({k:'normal' for k in stages[4:]})
    result=c.handle_backend_path(cat,bo);paths.append({'stage':stage,'outcomes':bo,'result':result})
    expected_completion='normal' if caught else 'process-termination' if failure=='process-termination' else 'escaping-exception'
    check('source backend '+stage+' '+failure,lambda result=result,expected_completion=expected_completion,caught=caught:result['completion']==expected_completion and result['response_ok'] is (False if caught else None) and result['runtime_observation'] is False,'constructed_only')
  for fail in ('Exception','BaseException','process-termination'):
   bo={'authenticate':'normal','reserve':'normal','action':'Exception','error_response':fail};r=c.handle_backend_path(cat,bo)
   check('failed error expression '+fail,lambda r=r,fail=fail:r['completion']==('process-termination' if fail=='process-termination' else 'escaping-exception') and r['response_ok'] is None,'constructed_only')
  escape=copy.deepcopy(cases[0]);escape['backend_outcomes']={'authenticate':'normal','reserve':'Exception'};escape['run_outcomes']={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'raise','handler_reason':'normal','quarantine':'normal','lock_exit':'normal'}
  for n in ('underlying','run_result','wrapper_return'):escape[n]=None
  er=check('escaping backend gives no byte links',lambda:c.handle_value_projection(cat,v,escape,copy.deepcopy(escape)),'constructed_only');check('escape quarantine conditional only',lambda:er['links']==[] and er['run']['quarantine_called'] and er['run']['completion']=='abrupt','constructed_only')
  for n in ('underlying','run_result','wrapper_return'):
   bad=copy.deepcopy(escape);bad[n]=copy.deepcopy(cases[0][n]);reject('invented return after escape '+n,lambda bad=bad:c.handle_value_projection(cat,v,bad,escape),'HANDLE-NO-RETURN:'+n,'constructed_negative')
  term=copy.deepcopy(escape);term['backend_outcomes']={'authenticate':'process-termination'}
  reject('process termination supplies no Python unwind',lambda:c.handle_value_projection(cat,v,term,copy.deepcopy(term)),'HANDLE-NO-PYTHON-UNWIND-FOR-PROCESS-TERMINATION','constructed_negative')
  for stage in ('post_transaction','return_expression','lock_exit'):
   x=copy.deepcopy(cases[0]);x['wrapper_return']=None;x['run_outcomes']={k:vv for k,vv in normal_run.items() if list(normal_run).index(k)<=list(normal_run).index(stage)};x['run_outcomes'][stage]=True if stage=='post_transaction' else 'raise'
   if stage!='lock_exit':x['run_outcomes'].update(handler_reason='normal',quarantine='normal',lock_exit='normal')
   r=check('backend returned but wrapper failed at '+stage,lambda x=x:c.handle_value_projection(cat,v,x,copy.deepcopy(x)),'constructed_only');check('only backend and assigned result survive '+stage,lambda r=r:len(r['links'])==2 and r['run']['completion']=='abrupt','constructed_only')
  x=copy.deepcopy(escape);x['run_outcomes']['quarantine']='raise';r=c.handle_value_projection(cat,v,x,copy.deepcopy(x));check('failed quarantine effects remain unknown',lambda:r['run']['quarantine_completed'] is False and r['run']['failed_or_interrupted_quarantine_effects'].startswith('UNKNOWN'),'constructed_only')
  x=copy.deepcopy(escape);x['run_outcomes'].pop('quarantine');x['run_outcomes']['handler_reason']='raise';r=c.handle_value_projection(cat,v,x,copy.deepcopy(x));check('reason failure precedes quarantine',lambda:r['run']['quarantine_called'] is False,'constructed_only')
  (out/'constructed-paths.json').write_text(json.dumps(paths,indent=2)+'\n')
  # Authenticate altered bytes without using any capture/archive hash as oracle.
  fixture=fixtures['cases'][0];response=fixture['responses'][0]['response'];rr=json.loads(bytes.fromhex(response['bytes_hex']));q=json.loads(bytes.fromhex(fixture['packet']['bytes_hex']))
  for label,edit in [('response data',lambda x:x['response']['data'].update(seq=1)),('response signature',lambda x:x.update(signature='0'*128)),('wrong request digest',lambda x:x['response'].update(request='f'*64)),('wrong challenge',lambda x:x['response'].update(challenge='e'*64)),('integer ok',lambda x:x['response'].update(ok=1)),('extra field',lambda x:x['response'].update(extra=None))]:
   if a.recovered and label not in ('response data','integer ok'):continue
   bad=copy.deepcopy(rr);edit(bad);recorded={'bytes_hex':enc(bad).hex()};reject('authenticated pair '+label,lambda recorded=recorded:c.handle_pair(cat,v,fixture['packet'],recorded,fixture['instance']),category='authentication_negative')
  badq=copy.deepcopy(q);badq['request']['challenge']='f'*64;pb=enc(badq);badr=copy.deepcopy(rr);badr['response'].update(request=hashlib.sha256(pb).hexdigest(),challenge='f'*64)
  reject('coordinated packet response hashes cannot replace authentication',lambda:c.handle_pair(cat,v,{'bytes_hex':pb.hex()},{'bytes_hex':enc(badr).hex()},fixture['instance']),category='authentication_negative')
  # Full entries rebuild their own predecessor expectations, unlike a
  # conditional projection whose separately validated premise is a caller duty.
  for i in (0,1):
   edits=[('missing declaration link',lambda x:x['declaration']['links'].pop()),('observed result invented',lambda x:x.update(runtime_links=[{}])),('inject unknown promoted to None',lambda x:x['inject_observation'].update(observed=True)),('wrong context',lambda x:x.update(context='OTHER')),('stale recovery frontier',lambda x:x['validated_scope'].update(recovery_frontier='old')),('wrong constructor instance',lambda x:x['validated_scope']['instance'].update(managed_constructor_frame=99)),('wrong predecessor receipt',lambda x:x['predecessor_receipt'].update(sha256='f'*64)),('finite zero promoted to lifetime zero',lambda x:x.update(actual_handle_call_count=0))]
   if a.recovered:edits=[x for x in edits if x[0] in ('missing declaration link','wrong constructor instance','inject unknown promoted to None')]
   for label,edit in edits:
    bad=copy.deepcopy(claims);edit(bad[i]);reject('current internal row '+label+' '+str(i),lambda bad=bad:m._check_rows(basis,bad,claims),category='internal_relation')
  for label,bad in [('missing context',claims[:1]),('duplicate context',[claims[0],claims[0]]),('reversed contexts',claims[::-1])]:reject('current internal '+label,lambda bad=bad:m._check_rows(basis,bad,claims),category='internal_relation')
  bad=copy.deepcopy(claims);bad[0]['validated_scope']['instance']['binding']='e'*64
  reject('full semantic wrong instance',lambda:m.semantic(data,cat,bad),'HANDLE-INSTANCE-LINEAGE')
  if not a.recovered:
   badcat=copy.deepcopy(cat);badcat['source']['method']='state';badcat['source']['wrapper_call']['expression']="self._run('state', packet, inject)";badcat['delegation']['to']='Authority.state'
   reject('full coordinated delegation substitution',lambda:m.semantic(data,badcat),'HANDLE-SOURCE-CATALOGUE')
  promoted=dict(e);ex=copy.deepcopy(export);ex['journal']=[[q['request']['challenge'],fixture['packet']['bytes_hex'],response['bytes_hex']]];promoted['evidence/recovery-export-0.json']=enc(ex)
  badclaims=copy.deepcopy(claims)
  for x in badclaims:x['saved_journal_rows']=1;x['saved_journal_records']=[{'constructed_promoted':True}]
  reject('coordinated journal and claims derivation',lambda:m.derive_handle(data,cat,badclaims,promoted),'HANDLE-VALIDATED-JOURNAL')
  reject('coordinated journal semantic comparison',lambda:m.semantic(data,cat,evidence=promoted),'HANDLE-VALIDATED-JOURNAL')
  if not a.recovered:
   # Shallow-copy the data spine only; original evidence remains immutable bytes.
   candidate=dict(data);cur=candidate;orig=data
   for _ in range(4):cur['prior_data']=dict(orig['prior_data']);cur=cur['prior_data'];orig=orig['prior_data']
   cur['ctx']=dict(orig['ctx']);cur['ctx']['e']=promoted
   reject('mutable candidate baseline cannot redefine empty journal',lambda:m.semantic(candidate,cat),'HANDLE-VALIDATED-JOURNAL')
   missing=dict(e);del missing['evidence/recovery-export-0.json'];reject('full missing export',lambda:m.semantic(data,cat,evidence=missing),'HANDLE-MISSING-EXPORT')
  for label,edit in [('wrong HEAD',lambda x:x.update(head=enc(dict(state,head='e'*64)).rstrip(b'\n').hex())),('wrong configuration',lambda x:x['config'].update(session='other'))]:
   mixed=dict(e);ex=copy.deepcopy(export);edit(ex);mixed['evidence/recovery-export-0.json']=enc(ex);reject('validated evidence '+label,lambda mixed=mixed:m._compare_evidence(basis,mixed),category='internal_relation')
  for label,edit in [('missing handle mapping',lambda x:x['contexts'][1].pop('handle_return_correspondence')),('readiness escalation',lambda x:x['new_handle_slice_limits'].update(readiness='READY',actual_admission=True)),('context duplication',lambda x:x['contexts'].__setitem__(1,copy.deepcopy(x['contexts'][0])))]:
   if a.recovered and label=='context duplication':continue
   bad=copy.deepcopy(bundle);edit(bad);reject('public '+label,lambda bad=bad:m.validate(root,enc(bad)),'STALE-OR-ALTERED-HANDLE-CORRESPONDENCE','public_negative')
  # Mutating any returned nested report must not be an expectation update.
  pristine=enc(claims);other=enc(claims[1]);claims[0]['declaration']['links'].clear();claims[0]['validated_scope']['instance']['binding']='bad';claims[0]['saved_journal_records'].append({'forged':True})
  check('context nested trees isolated',lambda:enc(claims[1])==other)
  public['contexts'].reverse();public['receipt'].clear();bundle['contexts'][0]['handle_return_correspondence']['declaration']['links'].clear();bundle['contexts'].clear();catbytes=enc(cat);cat['source']['backend_stages']['authenticate'].clear()
  check('catalogue mutation cannot update expected source',lambda:enc(m.catalogue(data))==catbytes);cat=m.catalogue(data)
  check('pristine semantic after nested mutations',lambda:enc(m.semantic(data,cat))==pristine)
  check('pristine public after nested mutations',lambda:m.validate(root,saved))
  check('mandatory state derivation actually invoked',lambda:any(x['function']=='mandatory state derive_state' for x in calls))
  check('journal expectation is fresh validated empty evidence',lambda:any(x['function']=='journal comparison' and x['expected_journal']==[] and len(x['candidate_journal'] or [])==1 for x in calls))
  check('candidate source evidence and saved receipt unchanged',lambda:source=={n:identity((root/'code'/n).read_bytes()) for n in source} and e==d['ctx']['e'] and (root/'results/handle-correspondence.json').read_bytes()==saved)
 except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};(out/'failure.txt').write_text(traceback.format_exc());raise
 finally:
  sys.settrace(None);r={'result':'PASS' if error is None else 'FAIL','assertions':len(rows),'categories':{cc:sum(x['category']==cc for x in rows) for cc in sorted({x['category'] for x in rows})},'checks':rows,'error':error,'recovered':a.recovered,'environment':{'python':sys.version,'optimization':sys.flags.optimize,'cryptography_installed':importlib.metadata.version('cryptography')},'source':locals().get('source'),'database_connections':0,'session_operations':0,'requests_issued':0,'new_signatures':0,'completed_review_reruns':False,'constructed_cases_are_execution_evidence':False}
  (out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');(out/'call-observations.json').write_text(json.dumps(calls,indent=2)+'\n');(out/'constructed-cases.json').write_text(json.dumps(constructed,indent=2)+'\n')
 print('PASS',len(rows),'independent handle checks')
if __name__=='__main__':main()
