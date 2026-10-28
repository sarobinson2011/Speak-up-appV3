"""Fresh current semantic/derivation/public checks; no historical campaign."""
from pathlib import Path
import argparse,copy,json,runpy,traceback
C=runpy.run_path(str(Path(__file__).with_name('common.py')));globals().update({n:C[n] for n in ('enc','identity','module','guards','monitor','Record')})
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('output',type=Path);p.add_argument('case');a=p.parse_args();root=a.root.resolve();r=Record(a.output.resolve());guards(root);error=None;calls=[];stop=lambda:None
try:
 m=module(root/'code/correspondence.py');calls,stop=monitor(m);d=m.inputs(root);cat=m.catalogue(d);saved=(root/'results/client-handle-correspondence.json').read_bytes();bundle=json.loads(saved);claims=[x['client_handle_return_correspondence'] for x in bundle['contexts']]
 if a.case=='legitimate':
  result=r.check('current source-derived receipt byte exact',lambda:m.derive_client(d,cat));r.check('both versioned contracts and all gaps preserved',lambda:enc(result)==saved and [x['context'] for x in result['contexts']]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and all(x['client_handle_return_correspondence']['runtime_forwarding_links'] is None and x['client_handle_return_correspondence']['declaration']['outside_catch_failure_contract']['runtime_evidence_supplied'] is False for x in result['contexts']))
 elif a.case in ('semantic-contract','derive-contract'):
  changed=copy.deepcopy(cat);changed['outside_catch_failure_contract']['true_iff']='any nonnormal outcome outside dispatch';bad=copy.deepcopy(claims)
  for x in bad:x['declaration']=copy.deepcopy(changed);x['classification']='QUALIFIED'
  fn=m.semantic if a.case=='semantic-contract' else m.derive_client
  r.reject('coordinated catalogue and both claims cannot change meaning',lambda:fn(d,changed,bad),'CLIENT-SOURCE-CATALOGUE')
 elif a.case=='semantic-alias':
  first=r.check('pristine semantic accepts',lambda:m.semantic(d,cat));pristine=enc(first);other=enc(first[1]);first[0]['declaration']['outside_catch_failure_contract'].clear();first[0]['validated_scope']['instance']['binding']='changed';first.reverse();r.check('separate context remains unchanged before reversal',lambda:enc(first[0])==other)
  r.check('fresh semantic expectations isolated from nested returned mutation',lambda:enc(m.semantic(d,cat))==pristine)
 elif a.case=='claims':
  bad=copy.deepcopy(claims);bad[0]['runtime_forwarding_links']=[{'completion':'process-termination','outside_catch_failure':True,'runtime_python_unwind_evidence':'ESTABLISHED'}];bad[1]['context']=bad[0]['context']
  r.reject('invented runtime classification and context substitution reject',lambda:m.semantic(d,cat,bad),'CLIENT-CONTEXT-CORRESPONDENCE')
 elif a.case in ('public-old','public-coordinated','public-missing'):
  if a.case=='public-old':bad=(root/'original/results/client-handle-correspondence.json').read_bytes()
  else:
   b=copy.deepcopy(bundle)
   for x in b['contexts']:
    if a.case=='public-missing':del x['client_handle_return_correspondence']['declaration']['outside_catch_failure_contract']
    else:x['client_handle_return_correspondence']['declaration']['outside_catch_failure_contract'].update(true_iff='termination outside catch',runtime_evidence_supplied=True)
   if a.case=='public-coordinated':b['new_client_slice_limits'].update(actual_admission=True,readiness='READY',runtime_chain='COMPLETE')
   bad=enc(b)
  r.reject(a.case,lambda:m.validate(root,bad),'STALE-OR-ALTERED-CLIENT-CORRESPONDENCE')
 elif a.case=='public-alias':
  out=r.check('public pristine before mutation',lambda:m.validate(root,saved));pristine=enc(out);out['contexts'].reverse();out['receipt'].clear();r.check('public pristine after returned nested mutation',lambda:enc(m.validate(root,saved))==pristine)
 else:raise AssertionError('unknown check')
 r.check('mandatory predecessor derivation observed',lambda:any(x['function']=='derive_handle' and '/original/retained/handle/code/correspondence.py' in x['file'] for x in calls))
 r.check('current receipt and sources unchanged',lambda:(root/'results/client-handle-correspondence.json').read_bytes()==saved and identity((root/'code/managed_coverage.py').read_bytes())==m.PRODUCER_PIN)
except BaseException as e:error={'type':type(e).__name__,'message':str(e)};(r.path/'failure.txt').write_text(traceback.format_exc());raise
finally:
 stop();r.finish(error,case=a.case,root=root.name);(r.path/'calls.json').write_text(json.dumps(calls,indent=2)+'\n')
print('PASS',a.case,len(r.rows))
