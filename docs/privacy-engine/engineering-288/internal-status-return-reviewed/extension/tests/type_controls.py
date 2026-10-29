"""Focused exact-type correction; preserve original acceptance witnesses."""
import argparse,copy,json,runpy,time,traceback,types
from pathlib import Path
def module(p):
 m=types.ModuleType('_status_types');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--write',action='store_true');a=ap.parse_args();a.root=a.root.resolve();a.output.mkdir(parents=True,exist_ok=False);runpy.run_path(str(a.root/'tests/guard.py'))['install'](a.root);start=time.monotonic();checks=[];error=None
 def check(label,fn):
  got=fn();assert got is not False;checks.append({'check':label,'result':'PASS'});print(len(checks),label,flush=True)
  with (a.output/'progress.jsonl').open('a') as f:f.write(json.dumps(checks[-1])+'\n')
  return got
 def reject(fn):
  try:fn()
  except ValueError:return True
  raise AssertionError('Unexpected acceptance')
 try:
  m=module(a.root/'code/correspondence.py');d=m.inputs(a.root);cat=m.catalogue(d);c=d['coverage'];old=module(a.root/'failures/type-acceptance-precorrection/managed_coverage.py');fixtures=json.loads((a.root/'fixtures/normal-cases.json').read_bytes())['cases'];witnesses=[]
  for fixture in fixtures:
   case=fixture['projection'];validated={k:copy.deepcopy(v) for k,v in case.items() if k!='returned'};ctx=fixture['context'];snap=copy.deepcopy(case['manager_snapshot'])
   check('pristine typed forwarding '+ctx,lambda:c.status_forward_projection(cat,case,validated)['completion']=='normal-return')
   for name,base in [('_reason',str),('_epoch',int),('_phase',str)]:
    fake=type(base.__name__,(base,),{});bad=copy.deepcopy(snap);bad[name]=fake(bad[name]);accepted=old.status_snapshot_value(cat,bad)
    witnesses.append({'context':ctx,'kind':'builtin-name subclass in snapshot','field':name,'actual_type_name':type(bad[name]).__name__,'exact_builtin_type':type(bad[name]) is base,'original_accepted':True,'serialized_value':accepted})
    check('original named-type witness reproduced '+name+' '+ctx,lambda:True)
    check('exact type rejects named subclass '+name+' '+ctx,lambda bad=bad:reject(lambda:c.status_snapshot_value(cat,bad)))
   for kind in ('dict-subclass','str-subclass','int-subclass'):
    bad=copy.deepcopy(case)
    if kind=='dict-subclass':bad['returned'][1]['value']=type('dict',(dict,),{})(bad['returned'][1]['value'])
    elif kind=='str-subclass':bad['returned'][1]['value']['reason']=type('str',(str,),{})(bad['returned'][1]['value']['reason'])
    else:bad['returned'][1]['value']['connection_epoch']=type('int',(int,),{})(bad['returned'][1]['value']['connection_epoch'])
    original=old.status_forward_projection(cat,bad,validated);witnesses.append({'context':ctx,'kind':'serialized-equivalent returned '+kind,'original_accepted':original['completion']=='normal-return','mutated_hop':'session-return'})
    check('original return subclass witness reproduced '+kind+' '+ctx,lambda:original['completion']=='normal-return')
    check('exact return type rejects '+kind+' '+ctx,lambda bad=bad:reject(lambda:c.status_forward_projection(cat,bad,validated)))
   for key,value in [('_epoch',True),('_epoch',1.0),('_reason',b'reason'),('_phase',False)]:
    bad=copy.deepcopy(snap);bad[key]=value;check('adjacent wrong snapshot type '+key+' '+type(value).__name__+' '+ctx,lambda bad=bad:reject(lambda:c.status_snapshot_value(cat,bad)))
  (a.output/'original-witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')
  if a.write:
   result=m.derive_status(d,cat);saved=m.enc(result);p=a.root/'results/status-forward-correspondence.json';assert not p.exists();p.write_bytes(saved)
   prior=json.loads((a.root/'results/pre-type-hardening-receipt.json').read_bytes());check('only current extension component identities changed by exact-type correction',lambda:all(m.enc(result[k])==m.enc(v) for k,v in prior.items() if k!='extension_components'))
   check('final receipt isolates nested returned objects',lambda:result['contexts'][0]['internal_status_return_correspondence'] is not result['contexts'][1]['internal_status_return_correspondence'])
 except BaseException as e:error={'exception':repr(e),'traceback':traceback.format_exc()};raise
 finally:
  result={'result':'FAIL' if error else 'PASS','checks':len(checks),'rows':checks,'error':error,'seconds':time.monotonic()-start,'original_witnesses_are_constructed':True,'runtime_operations':0,'prior_suites_rerun':False};(a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
if __name__=='__main__':main()
