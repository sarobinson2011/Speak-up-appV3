"""CF-01 linkage controls on original validated saved outputs, not a review rerun."""
import argparse,copy,importlib.util,json,pathlib,shutil,subprocess,sys,traceback

def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--review',required=True);ap.add_argument('--connect',required=True);ap.add_argument('--output',required=True);ap.add_argument('--case');a=ap.parse_args()
 m=module(a.connect,'cf_corrected');review=pathlib.Path(a.review).absolute();out=pathlib.Path(a.output).absolute();out.mkdir(parents=True,exist_ok=False)
 source=review/'results/fault-chain-2';fixture=out/'stages';shutil.copytree(source,fixture)
 original=m.read(review/'results/original-ledger-result.json');summary_path=fixture/'04-ledger/result.json';summary_path.write_bytes(original)
 basis=m.load(source/'receipt.json')['basis'];config={k:str(source/p) for k,p in [('bundle','01-inputs/bundle.json'),('model','02-consumer/native.json'),('saved_ledger','04-ledger/ledger.json')]}
 ledger_before=m.ident(m.read(config['saved_ledger']));ledger=m.load(config['saved_ledger']);model=m.load(config['model']);rows=[]
 def positive(name):
  result=m.output_bindings(config,fixture,basis)
  expected=m.parse(original)['contexts'];m.same(result['ledger_contexts'],expected,'SAVED-VALID-RESULT')
  # Cross-check independently against actual model membership and ordered edges.
  for c,n in zip(result['ledger_contexts'],model['contexts']):
   assert c['context']==n['context'] and c['node_duties']==len(n['groups'])
   assert c['token_members']==len(n['occurrences']) and c['edge_members']==len(n['ordered_edges'])
  rows.append({'name':name,'result':'PASS acceptance'});return result
 def negative(name,change):
  v=m.parse(original);change(v);assert m.enc(v)!=m.enc(m.parse(original)),'INEFFECTIVE MUTATION'
  raw=m.enc(v)+b'\n';summary_path.write_bytes(raw)
  try:m.output_bindings(config,fixture,basis)
  except m.Rejected as e:
   assert str(e)=='LEDGER-RESULT-CORRESPONDENCE',str(e)
   rows.append({'name':name,'result':'PASS rejection','reason':str(e),'summary':m.ident(raw)})
  else:raise AssertionError('ACCEPTED '+name)
  finally:summary_path.write_bytes(original)
 try:
  if a.case:
   if a.case=='witness':negative('fresh-original-witness',lambda v:v['contexts'][0].update(node_duties=0))
   elif a.case=='coordinated':negative('fresh-coordinated',lambda v:[c.update(node_duties=0,relation_duties=0,fold_duties=0,token_members=0,edge_members=0) for c in v['contexts']])
   elif a.case=='positive':positive('fresh-legitimate')
   else:raise AssertionError('CASE')
  else:
   r=positive('legitimate-original-summary')
   negative('original-witness',lambda v:v['contexts'][0].update(node_duties=0))
   for ctx in range(2):
    for field in ['node_duties','relation_duties','fold_duties','token_members','edge_members']:
     negative(f'{ctx}-{field}-altered',lambda v,c=ctx,f=field:v['contexts'][c].update({f:v['contexts'][c][f]+1}))
     negative(f'{ctx}-{field}-float',lambda v,c=ctx,f=field:v['contexts'][c].update({f:float(v['contexts'][c][f])}))
     negative(f'{ctx}-{field}-missing',lambda v,c=ctx,f=field:v['contexts'][c].pop(f))
   negative('coordinated-all-counts',lambda v:[c.update(node_duties=0,relation_duties=0,fold_duties=0,token_members=0,edge_members=0) for c in v['contexts']])
   negative('contexts-reversed',lambda v:v['contexts'].reverse())
   negative('missing-context',lambda v:v['contexts'].pop())
   negative('duplicate-context',lambda v:v['contexts'].append(copy.deepcopy(v['contexts'][0])))
   negative('same-length-duplicate-context',lambda v:v['contexts'].__setitem__(1,copy.deepcopy(v['contexts'][0])))
   negative('wrong-context-name',lambda v:v['contexts'][0].update(context='OTHER'))
   negative('mixed-model-binding',lambda v:v['binding']['finite_model'].update(sha256='0'*64))
   negative('mixed-acquisition-binding',lambda v:v['binding'].update(acquisition='OTHER'))
   negative('missing-binding',lambda v:v.pop('binding'))
   negative('wrong-ledger-hash',lambda v:v['ledger'].update(sha256='f'*64))
   negative('wrong-ledger-byte-count',lambda v:v['ledger'].update(bytes=v['ledger']['bytes']+1))
   negative('wrong-obligation-count',lambda v:v.update(source_only_obligations=0))
   for key,value in [('qualification_established',True),('canonical_ledger_rebound',True),('actual_admission',True),('final_binding','COMPLETE'),('status','QUALIFIED')]:
    negative(key,lambda v,k=key,x=value:v.update({k:x}))
   negative('missing-status',lambda v:v.pop('status'))
   negative('extra-readiness-field',lambda v:v.update(full_expansion_ready=True))
   negative('boolean-count',lambda v:v['contexts'][1].update(token_members=True))
   negative('coordinated-binding-and-count',lambda v:(v['binding']['finite_model'].update(sha256='a'*64),v['ledger'].update(sha256='a'*64),v['contexts'][1].update(node_duties=0)))
   r['ledger_contexts'][0]['node_duties']=0;r['ledger_contexts'].reverse();r['artifacts'].clear();positive('unchanged-after-returned-result-mutation')
   # A semantically equivalent summary serialization is valid but binds its own bytes.
   summary_path.write_bytes(json.dumps(m.parse(original),indent=3).encode()+b'\n');x=positive('equivalent-summary-serialization');assert x['artifacts']['ledger_result']==m.ident(m.read(summary_path));summary_path.write_bytes(original)
   # Final receipt fields changed with summary cannot supply their own expectations.
   false_receipt=m.load(source/'receipt.json');assert false_receipt['outputs']['ledger_contexts'][0]['node_duties']==0
   negative('coordinated-saved-false-receipt-summary',lambda v:v['contexts'].__setitem__(0,copy.deepcopy(false_receipt['outputs']['ledger_contexts'][0])))
   positive('final-pristine')
  assert m.ident(m.read(config['saved_ledger']))==ledger_before
  m.write(out/'checks.json',{'status':'PASS','scope':'Fresh CF-01 internal linkage controls on exact reviewed full-run artifacts; no component review rerun','controls':rows,'actual_ledger_unchanged':ledger_before,'review_witness_reused':m.ident(m.read(source/'receipt.json'))})
  print('PASS',len(rows),'CF-01 controls',flush=True)
 except BaseException:
  (out/'failure.txt').write_text(traceback.format_exc());m.write(out/'partial-checks.json',rows);raise
if __name__=='__main__':main()
