"""Additional focused byte/authentication/path controls; no signing or sessions."""
import argparse,copy,json,runpy,time
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False);rows=[];error=None;start=time.monotonic()
 ns=runpy.run_path(str(a.root/'tests/controls.py'),run_name='_guards_only');m=ns['module'](a.root/'code/correspondence.py')
 def check(n,f):
  x=f();assert x is not False,n;rows.append({'check':n,'result':'PASS'});print(len(rows),n,flush=True);return x
 def reject(f):
  try:f()
  except Exception:return True
  raise AssertionError('Unexpected acceptance')
 try:
  d=m.inputs(a.root);cat=m.catalogue(d);c=d['coverage'];raw,auth,anchor,obs=m.sources(d);v=c.handle_authentication(auth,anchor,obs);fx=json.loads((a.root/'tests/constructed-envelopes.json').read_bytes());receipt=json.loads((a.root/'results/handle-correspondence.json').read_bytes());expected=[x['handle_return_correspondence'] for x in receipt['contexts']]
  old=json.loads(m.inner(d)['ctx']['c']['retained/launcher/results/signature-fixture.json'])
  check('retained signature primitive fixture verifies without new signing',lambda:v['signature']('observer',old['fixture'],old['signature_hex']))
  check('public key matches independently retained fixture',lambda:v['public_keys']['observer']==old['public_key_hex'])
  f=fx['cases'][0];packet=f['packet'];response=f['responses'][0]['response'];request=json.loads(bytes.fromhex(packet['bytes_hex']));rr=json.loads(bytes.fromhex(response['bytes_hex']))
  for label,mut in [('truncated signature',lambda x:x.update(signature=x['signature'][:-2])),('changed data with old signature',lambda x:x['response']['data'].update(seq=17)),('wrong challenge',lambda x:x['response'].update(challenge='b'*64))]:
   bad=copy.deepcopy(rr);mut(bad);record={'bytes_hex':m.enc(bad).hex()};check(label+' rejects authenticated-pair checker',lambda record=record:reject(lambda:c.handle_pair(cat,v,packet,record,f['instance'])))
  for k in ('expected','binding','challenge'):
   bad=copy.deepcopy(request);bad['request'][k]='b'*64;record={'bytes_hex':m.enc(bad).hex()};check('stale or substituted packet '+k,lambda record=record:reject(lambda:c.handle_pair(cat,v,record,response,f['instance'])))
  bad=copy.deepcopy(request);bad['request']['challenge']='b'*64;pp={'bytes_hex':m.enc(bad).hex()};rb=copy.deepcopy(rr);rb['response'].update(challenge='b'*64,request=ns['hashlib'].sha256(bytes.fromhex(pp['bytes_hex'])).hexdigest());rb={'bytes_hex':m.enc(rb).hex()}
  check('coordinated packet/response substitutions do not replace signatures',lambda:reject(lambda:c.handle_pair(cat,v,pp,rb,f['instance'])))
  bad=dict(f['instance'],binding='b'*64);check('valid signed pair wrong instance rejects semantically',lambda:reject(lambda:c.handle_pair(cat,v,packet,response,bad)))
  body={'authenticate':'normal','reserve':'normal','action':'normal','success_response':'normal','encode_sign':'normal','response_bound':'normal','persist':'normal','return_raw':'normal'}
  run={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'normal','post_transaction':False,'return_expression':'normal','lock_exit':'normal'}
  scope=dict(f['scope'],instance=copy.deepcopy(f['instance']));args={'packet':copy.deepcopy(packet),'inject':'after_decision_commit'};ref={'scope':copy.deepcopy(scope),'symbol':'constructed-reference'}
  case={'occurrence':'constructed:additional:0','scope':scope,'arguments':args,'run_arguments':{'method':'handle','args':[copy.deepcopy(packet),args['inject']]},'backend_arguments':copy.deepcopy(args),'backend_outcomes':body,'run_outcomes':run,**{n:{'value':copy.deepcopy(response),'reference':copy.deepcopy(ref)} for n in ('underlying','run_result','wrapper_return')}}
  out=check('known non-None inject forwards without inferring its effects',lambda:c.handle_value_projection(cat,v,case,copy.deepcopy(case)))
  check('inject value preserved as constructed argument only',lambda:out['arguments']['inject']==args['inject'] and out['runtime_observation'] is False)
  second=copy.deepcopy(case);second['occurrence']='constructed:additional:1';out2=c.handle_value_projection(cat,v,second,copy.deepcopy(second));check('equal bytes in distinct conditional occurrences remain distinct',lambda:out2['links'][0]['value']==out['links'][0]['value'] and set(x['id'] for x in out['links']).isdisjoint(x['id'] for x in out2['links']))
  bad=copy.deepcopy(case);bad['run_outcomes']={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'normal','post_transaction':True,'handler_reason':'normal','quarantine':'normal','lock_exit':'normal'};bad['wrapper_return']=None
  out=c.handle_value_projection(cat,v,bad,copy.deepcopy(bad));check('backend normal return followed by post-transaction failure has only two value links',lambda:len(out['links'])==2 and out['run']['quarantine_called'] and out['run']['completion']=='abrupt')
  bad['run_outcomes']['quarantine']='raise';out=c.handle_value_projection(cat,v,bad,copy.deepcopy(bad));check('failed quarantine preserves unknown partial effects',lambda:out['run']['quarantine_completed'] is False and out['run']['failed_or_interrupted_quarantine_effects'].startswith('UNKNOWN'))
  out=c.handle_backend_path(cat,{'authenticate':'normal','reserve':'normal','action':'Exception','error_response':'Exception'});check('error-expression failure escapes without normal response',lambda:out['completion']=='escaping-exception' and out['response_ok'] is None)
  check('internal row checker requires both contexts',lambda:reject(lambda:m._check_rows({},[],expected)))
  for i in (0,1):
   bad=copy.deepcopy(expected);bad[i]['declaration']['links'].pop();check('internal omitted link rejects context '+str(i),lambda bad=bad:reject(lambda:m._check_rows({},bad,expected)))
   bad=copy.deepcopy(expected);bad[i]['runtime_links']=[{'invented':True}];check('internal invented runtime link rejects context '+str(i),lambda bad=bad:reject(lambda:m._check_rows({},bad,expected)))
 except BaseException as e:error=repr(e);raise
 finally:
  r={'result':'PASS' if error is None else 'FAIL','checks':len(rows),'rows':rows,'error':error,'seconds':time.monotonic()-start,'scope':'additional new internal byte/authentication/path controls, not full evidence admission','new_signatures':0,'runtime_or_session_operations':0,'constructed_only':True};(a.output/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('result','checks','error')}),flush=True)
if __name__=='__main__':main()
