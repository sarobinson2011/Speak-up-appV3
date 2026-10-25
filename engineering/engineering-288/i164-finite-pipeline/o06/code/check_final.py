"""Focused final-link and CF-01 regression using actual outputs from a completed chain."""
import argparse,copy,importlib.util,pathlib,shutil

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--code',required=True);ap.add_argument('--config',required=True);ap.add_argument('--run',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 s=importlib.util.spec_from_file_location('checked_connector',a.code);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 c=m.load(a.config);o=pathlib.Path(a.output);o.mkdir(parents=True,exist_ok=False);src=pathlib.Path(a.run);basis=m.preflight(c);final=m.load(src/'receipt.json');links=m.output_bindings(c,src,basis);links['carrier_copy']=m.copy_bindings(c,src,basis);links['carrier_expressions']=m.expression_bindings(c,src,basis,links['carrier_copy'])
 expected={'format':m.FORMAT,'basis':basis,'stages':list(m.STAGES),'outputs':links};m.same(final,expected,'FINAL-RECEIPT');rows=[{'case':'actual-six-stage-final','status':'PASS'}]
 # Exercise the identical exact final-comparison used by run, with independently
 # checked links. This is not a second public five-stage execution.
 for name,f in [
 ('missing-expressions',lambda x:x['outputs'].pop('carrier_expressions')),
 ('altered-expression-summary',lambda x:x['outputs']['carrier_expressions'].update(selected_known=0)),
 ('false-lifetime-closure',lambda x:x['outputs']['carrier_expressions'].update(global_lifetime_bound=0)),
 ('missing-copy',lambda x:x['outputs'].pop('carrier_copy')),
 ('stale-copy',lambda x:x['outputs']['carrier_copy']['receipt'].update(sha256='0'*64)),
 ('copy-summary',lambda x:x['outputs']['carrier_copy'].update(selected_database_payload_bytes=0)),
 ('global-O09-closure',lambda x:x['outputs']['carrier_copy'].update(global_O09_closed=True)),
 ('missing-stage',lambda x:x['stages'].pop()),
 ('mixed-context',lambda x:x['outputs']['carrier_copy']['contexts'].reverse()),
 ('omitted-obligation',lambda x:x['basis']['obligations']['source_only'].pop()),
 ('unknown-to-zero',lambda x:x['outputs']['carrier_copy'].update(physical_storage_bytes=0))]:
  mutant=copy.deepcopy(final);f(mutant)
  try:m.validate_final(mutant,expected)
  except m.Rejected:rows.append({'case':name,'status':'PASS rejection'})
  else:raise AssertionError(name)
 fixture=o/'cf01';fixture.mkdir()
 for n in ('01-inputs','02-consumer','03-verification','04-ledger'):
  (fixture/n).mkdir()
 for n in ('01-inputs/bundle.json','01-inputs/validation.json','02-consumer/native.json','03-verification/result.json','04-ledger/ledger.json','04-ledger/result.json'):shutil.copyfile(src/n,fixture/n)
 p=fixture/'04-ledger/result.json';original=p.read_bytes();v=m.parse(original);v['contexts'][0]['node_duties']=0;p.write_bytes(m.enc(v)+b'\n')
 try:m.output_bindings(c,fixture,basis)
 except m.Rejected as e:rows.append({'case':'CF01-node-duties-zero','status':'PASS rejection','reason':str(e)})
 else:raise AssertionError('CF01')
 p.write_bytes(original);m.output_bindings(c,fixture,basis);rows.append({'case':'CF01-legitimate-restored','status':'PASS'})
 m.write(o/'result.json',{'checks':rows,'scope':'actual output linkage and final exact-comparison; no producer or component-review rerun'})
 print('PASS',len(rows),'final-link controls')
if __name__=='__main__':main()
