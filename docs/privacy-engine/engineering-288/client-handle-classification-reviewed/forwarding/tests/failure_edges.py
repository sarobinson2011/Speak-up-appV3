"""New focused correction controls; no earlier completed campaign rerun."""
import argparse,copy,json,runpy,time
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 g=runpy.run_path(str(a.root/'tests/controls.py'),run_name='_guards');m=g['module'](a.root/'code/correspondence.py');d=m.inputs(a.root);cat=m.catalogue(d);c=d['coverage'];_,auth,anchor,obs=d['prior_module'].sources(d['prior_data']);v=c.handle_authentication(auth,anchor,obs)
 rows=[];cases=[];error=None;start=time.monotonic()
 def check(label,fn):
  out=fn();assert out is not False,label;row={'check':label,'result':'PASS'};rows.append(row)
  with (a.output/'progress.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  print(len(rows),label,flush=True);return out
 def rejects(fn):
  try:fn()
  except ValueError:return True
  raise AssertionError('Unexpected acceptance')
 try:
  old=json.loads((a.root/'failures/pre-correction/edge-witness.json').read_bytes());check('original inconsistent classification preserved',lambda:old['classification_inconsistent'] is True and old['output']['outside_catch_failure'] is False)
  for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
   case=copy.deepcopy(old['case']);case['scope']['context']=context
   for ref in case['references'].values():
    if type(ref) is dict:ref['scope']['context']=context
   out=check('fixed helper failure outside dispatcher catch '+context,lambda:c.client_handle_projection(cat,v,case,copy.deepcopy(case)));cases.append({'input':case,'output':out})
   check('helper failure cannot claim fixed publication '+context,lambda:out['completion']=='unqualified-escape' and out['outside_catch_failure'] and out['fixed_client_failure'] is None and out['destinations']==[])
   bad=copy.deepcopy(out);bad['outside_catch_failure']=False
   check('original witness result rejects '+context,lambda:rejects(lambda:c.validate_client_handle_projection(cat,v,case,case,bad)))
   case=copy.deepcopy(case);case['outcomes']['fixed-failure']='normal';out=c.client_handle_projection(cat,v,case,copy.deepcopy(case))
   check('normal helper still yields fixed source failure '+context,lambda:out['completion']=='fixed-client-failure' and not out['outside_catch_failure'] and out['fixed_client_failure']['suppress_context'])
   case['references']['owners[token]']=copy.deepcopy(case['references']['owner']);case['packet']={'type':'str','value':'constructed invalid input'};case['outcomes'].pop('fixed-failure');case['outcomes'].update({'packet-check':'normal','retain-error':'raise'})
   out=c.client_handle_projection(cat,v,case,copy.deepcopy(case));cases.append({'input':case,'output':out})
   check('storage failure outside handler, retention unknown '+context,lambda:out['completion']=='unqualified-escape' and out['outside_catch_failure'] and out['retained_original'] is None and out['fixed_client_failure'] is None)
   case['outcomes']['retain-error']='process-termination';out=c.client_handle_projection(cat,v,case,copy.deepcopy(case))
   check('termination is not a Python outside-catch exception '+context,lambda:out['completion']=='process-termination' and not out['outside_catch_failure'] and out['retained_original'] is None)
   case['references']['owner_failed']=True;case['packet']=copy.deepcopy(old['case']['packet']);case['outcomes']={n:'normal' for n in ('client-call','owner-lookup','owner-guard','fixed-failure')};out=c.client_handle_projection(cat,v,case,copy.deepcopy(case))
   check('earlier pending owner failure remains unresolved '+context,lambda:out['prior_owner_failure']['present'] and not out['prior_owner_failure']['resolution_established'] and out['evidence_route']['original_reraised_to_launcher'] is None)
  result=check('corrected mandatory offline derivation',lambda:m.derive_client(d,cat));raw=m.enc(result)
  with (a.root/'results/client-handle-correspondence.json').open('xb') as out:out.write(raw)
  check('corrected pristine public receipt',lambda:m.validate(a.root,raw))
 except BaseException as ex:error=repr(ex);raise
 finally:
  report={'result':'PASS' if error is None else 'FAIL','checks':len(rows),'rows':rows,'error':error,'seconds':time.monotonic()-start,'source':{n:m.identity((a.root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'new_focused_correction_only':True,'completed_primary_campaign_rerun':False,'runtime_observation':False,'database_connections':0,'requests_issued':0,'new_signatures':0,'session_operations':0}
  (a.output/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');(a.output/'cases.json').write_text(json.dumps(cases,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('result','checks','error')}),flush=True)
if __name__=='__main__':main()
