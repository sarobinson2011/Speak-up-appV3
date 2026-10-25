"""New integration controls; saved stage outputs, not completed component suites."""
import argparse,copy,importlib.util,pathlib,shutil

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--code',required=True);ap.add_argument('--config',required=True);ap.add_argument('--run',required=True);ap.add_argument('--output',required=True);ap.add_argument('--case',default='all');a=ap.parse_args()
 spec=importlib.util.spec_from_file_location('integration',a.code);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 c=m.load(a.config);basis=m.preflight(c);src=pathlib.Path(a.run);out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=False);fixture=out/'fixture';fixture.mkdir()
 for role in ('05-copies','06-expressions'):shutil.copytree(src/role,fixture/role)
 copy_links=m.copy_bindings(c,fixture,basis);rp=fixture/'06-expressions/receipt.json';sp=fixture/'06-expressions/result.json';original=m.load(rp);summary=m.load(sp);rows=[]
 def put(p,v):p.write_bytes(m.enc(v)+b'\n')
 def check(name,mutate=None,missing=None):
  r=copy.deepcopy(original);s=copy.deepcopy(summary)
  if mutate:mutate(r,s)
  put(rp,r);put(sp,s)
  if missing:(fixture/'06-expressions'/missing).unlink()
  try:result=m.expression_bindings(c,fixture,basis,copy_links)
  except (ValueError,KeyError,TypeError,FileNotFoundError) as e:
   if not(mutate or missing):raise
   rows.append({'case':name,'status':'PASS rejection','reason':str(e)});return
  if mutate or missing:raise AssertionError('ACCEPTED '+name)
  rows.append({'case':name,'status':'PASS acceptance'});return result
 cases={
 'stale-acquisition':lambda r,s:r.update(acquisition_id='stale'),
 'stale-copy':lambda r,s:r['bindings']['copy_receipt'].update(sha256='0'*64),
 'stale-code':lambda r,s:r['bindings']['code'].update(sha256='0'*64),
 'mixed-count-binding':lambda r,s:r['bindings']['count_and_procedure']['count_component'].update(sha256='0'*64),
 'duplicate-context':lambda r,s:r['contexts'].append(r['contexts'][0]),
 'summary-boolean':lambda r,s:s.update(selected_known=True),
 'mixed-context':lambda r,s:r['contexts'].reverse(),
 'missing-context':lambda r,s:r['contexts'].pop(),
 'duplicate-expression':lambda r,s:r['expressions'].append(copy.deepcopy(r['expressions'][0])),
 'missing-expression':lambda r,s:r['expressions'].pop(),
 'wrong-unit':lambda r,s:r['expressions'][0]['selected'].update(unit='physical_bytes'),
 'wrong-scope':lambda r,s:r['expressions'][0]['selected'].update(scope='lifetime'),
 'duplicate-occurrence':lambda r,s:r['expressions'][0]['selected']['occurrence_keys'].append(r['expressions'][0]['selected']['occurrence_keys'][0]),
 'inventory-zero':lambda r,s:r['expressions'][10]['selected'].update(value=0),
 'lifetime-zero':lambda r,s:r['expressions'][0]['lifetime'].update(value=0),
 'global-bound':lambda r,s:r.update(global_lifetime_bound=384000),
 'closure':lambda r,s:r.update(global_O06_closed=True),
 'missing-obligation':lambda r,s:r['obligations']['source_only'].pop(),
 'readiness':lambda r,s:r.update(full_expansion_ready=True),
 'summary-count':lambda r,s:s.update(expressions=0),
 'summary-known':lambda r,s:s.update(selected_known=0),
 'summary-lifetime':lambda r,s:s.update(lifetime_unknown=0),
 'summary-obligations':lambda r,s:s.update(obligations=0),
 'summary-binding':lambda r,s:s['receipt'].update(sha256='0'*64),
 'coordinated-count':lambda r,s:(r['expressions'][0]['selected'].update(value=2),s.update(receipt=m.ident(m.enc(r)+b'\n'))),
 }
 if a.case=='all':
  first=check('positive');first['expressions'].clear();first['contexts'].reverse();first['bindings'].clear()
  check('pristine-after-return-mutation');check('missing-receipt',missing='receipt.json');check('missing-summary',missing='result.json')
  for name,mut in cases.items():check(name,mut)
 elif a.case=='positive':check('positive')
 elif a.case in cases:check(a.case,cases[a.case])
 else:raise ValueError('CASE')
 m.same(m.preflight(c),basis,'PRESERVATION');m.write(out/'result.json',{'checks':rows,'scope':'new current-input stage linkage controls; full public chain separately executed','contexts':basis['contexts'],'obligations':11})
 print('PASS',len(rows),'expression linkage controls',flush=True)
if __name__=='__main__':main()
