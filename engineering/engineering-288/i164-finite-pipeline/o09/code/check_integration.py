"""Focused integration checks; reuses component evidence, not review suites."""
import argparse,copy,importlib.util,json,pathlib,shutil,sys,traceback

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--code',required=True);ap.add_argument('--config',required=True);ap.add_argument('--run',required=True);ap.add_argument('--output',required=True);ap.add_argument('--case',default='all');a=ap.parse_args()
 s=importlib.util.spec_from_file_location('integration_under_test',a.code);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=False);c=m.load(a.config);basis=m.preflight(c);source=pathlib.Path(a.run);fixture=out/'fixture';(fixture/'05-copies').mkdir(parents=True)
 original=m.load(source/'05-copies/receipt.json');summary=m.load(source/'05-copies/result.json');rows=[]
 def put(p,v):p.write_bytes(m.enc(v)+b'\n')
 def check(name,mutate=None,missing=None):
  r=copy.deepcopy(original);v=copy.deepcopy(summary)
  if mutate:mutate(r,v)
  rp=fixture/'05-copies/receipt.json';sp=fixture/'05-copies/result.json';put(rp,r);put(sp,v)
  if missing:(fixture/'05-copies'/missing).unlink()
  try:result=m.copy_bindings(c,fixture,basis)
  except (ValueError,KeyError,TypeError,FileNotFoundError) as e:
   if not (mutate or missing):raise
   rows.append({'case':name,'status':'PASS rejection','reason':str(e)});return
  if mutate or missing:raise AssertionError('ACCEPTED '+name)
  rows.append({'case':name,'status':'PASS acceptance','receipt':result['receipt']});return result
 cases={
 'stale-acquisition':lambda r,s:r.update(acquisition_id='stale'),
 'mixed-context':lambda r,s:r['contexts'][0].update(context='SYMBOLIC-U-TWO'),
 'altered-evidence':lambda r,s:r['archives'][0]['identity'].update(sha256='0'*64),
 'altered-code-binding':lambda r,s:r['bindings']['count_component'].update(sha256='0'*64),
 'missing-obligation':lambda r,s:r['obligations']['source_only'].pop(),
 'unknown-to-zero':lambda r,s:r.update(physical_storage_bytes=0),
 'closure-escalation':lambda r,s:r.update(global_O09_closed=True),
 'summary-payload-zero':lambda r,s:s.update(selected_database_payload_bytes=0),
 'summary-double-context':lambda r,s:s.update(selected_database_payload_bytes=90112),
 'summary-receipt':lambda r,s:s['receipt'].update(sha256='0'*64),
 'summary-context-order':lambda r,s:s['contexts'].reverse(),
 'summary-obligations':lambda r,s:s.update(obligations=0),
 'summary-readiness':lambda r,s:s.update(full_expansion_ready=True),
 'coordinated-payload':lambda r,s:(r.update(selected_database_payload_bytes=0),s.update(selected_database_payload_bytes=0,receipt=m.ident(m.enc(r)+b'\n'))),
 }
 if a.case=='positive':check('positive')
 elif a.case in cases:check(a.case,cases[a.case])
 elif a.case=='all':
  first=check('positive');first['contexts'].reverse();first['source_bindings'].clear();first['global_O09_closed']=True
  check('pristine-after-return-mutation')
  check('missing-receipt',missing='receipt.json');check('missing-summary',missing='result.json')
  for n,f in cases.items():check(n,f)
 else:raise ValueError('CASE')
 m.same(m.preflight(c),basis,'PRESERVATION');m.write(out/'result.json',{'checks':rows,'scope':'fresh post-stage integration linkage checks; public full chain separately executed','contexts':basis['contexts'],'obligations':11})
 print('PASS',len(rows),'focused linkage checks',flush=True)
if __name__=='__main__':main()
