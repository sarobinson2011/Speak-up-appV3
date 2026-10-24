import argparse,copy,json,subprocess,sys,shutil,traceback
from pathlib import Path
import ledger as l
v=l.v
p=argparse.ArgumentParser()
for n in ['component','consumer','model','ledger','output']:p.add_argument('--'+n,required=True)
a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=False);rows=[]
def public(submitted=None,model=None):return l.run(a.component,a.consumer,model or a.model,submitted)
def reject(name,change):
 value=copy.deepcopy(original);before=v.enc(value);change(value);raw=v.enc(value);v.need(before!=raw,'INEFFECTIVE-MUTATION:'+name)
 path=out/'current-mutant.json';path.write_bytes(raw)
 try:public(path)
 except v.Rejected as e:
  v.need(str(e)=='LEDGER-SUBSTITUTION','WRONG-REJECTION:'+str(e));rows.append({'case':name,'status':'REJECTED','reason':str(e),'bytes':len(raw),'sha256':v.sha(raw)})
 else:raise AssertionError('ACCEPTED:'+name)
 print(name,flush=True)
try:
 original=v.parse(v.regular(a.ledger));public(a.ledger);rows.append({'case':'actual saved ledger public validation','status':'PASS'})
 # Independent arithmetic/coverage from actual model, not ledger totals.
 model=v.parse(v.regular(a.model))
 for c,m in zip(original['contexts'],model['contexts']):
  v.same([k for d in c['node_duties'] for k in d['occurrence_keys']],[t['key'] for t in m['occurrences']],'INDEPENDENT-NODE-PARTITION')
  v.same([e for d in c['relation_duties'] for e in d['ordered_edges']],m['ordered_edges'],'INDEPENDENT-EDGE-PARTITION')
  v.need(len(c['fold_duties'])==len(m['duties']['fold']),'FOLD-COVERAGE')
  rows.append({'case':'independent node/edge/fold coverage '+c['context'],'status':'PASS'})
 for ci in range(2):
  reject(f'{ci}:missing-node',lambda x,ci=ci:x['contexts'][ci]['node_duties'].pop())
  reject(f'{ci}:duplicate-relation',lambda x,ci=ci:x['contexts'][ci]['relation_duties'].append(copy.deepcopy(x['contexts'][ci]['relation_duties'][0])))
  reject(f'{ci}:token-range',lambda x,ci=ci:x['contexts'][ci]['node_duties'][0].__setitem__('token_range',[0,1]))
  reject(f'{ci}:edge-range',lambda x,ci=ci:x['contexts'][ci]['relation_duties'][0].__setitem__('edge_range',[0,1]))
  reject(f'{ci}:fold-missing',lambda x,ci=ci:x['contexts'][ci]['fold_duties'].pop())
  reject(f'{ci}:context-mixing',lambda x,ci=ci:x['contexts'][ci]['node_duties'][0]['binding'].__setitem__('context','SYMBOLIC-U-TWO' if ci==0 else 'SYMBOLIC-U-ONE'))
 reject('stale-model',lambda x:x['binding']['finite_model'].__setitem__('sha256','0'*64))
 reject('missing-eight-duty',lambda x:x['contexts'][0]['node_duties'][0]['exact_duties'].pop())
 reject('qualified-duty',lambda x:x['contexts'][0]['relation_duties'][0].__setitem__('qualification','ESTABLISHED'))
 reject('remove-obligation',lambda x:x['obligations']['source_only'].pop())
 reject('admission-escalation',lambda x:x.__setitem__('actual_admission',True))
 reject('ledger-rebinding-claim',lambda x:x.__setitem__('canonical_ledger_rebound',True))
 returned=public();returned['contexts'].reverse();returned['obligations']['source_only'].clear();returned['contexts'][0]['node_duties'][0]['exact_duties'].clear()
 pristine=public(a.ledger);v.same(pristine,original,'MUTABLE-ALIAS');rows.append({'case':'returned nested aliases and pristine repeated call','status':'PASS'})
 # Same valid representation with different serialization must have a NEW binding.
 alternate=out/'alternate-model.json';alternate.write_bytes(b' \n'+v.regular(a.model));alternate_ledger=public(model=alternate)
 v.need(alternate_ledger['binding']['finite_model']['sha256']!=original['binding']['finite_model']['sha256'],'EXACT-BYTE-BINDING')
 rows.append({'case':'legitimate model reserialization has distinct exact binding','status':'PASS'})
 recovered=out/'recovered';recovered.mkdir()
 for name in ['ledger.py','verify_finite.py']:shutil.copyfile(Path(__file__).with_name(name),recovered/name)
 for label,submitted in [('fresh-positive',Path(a.ledger)),('fresh-negative',out/'current-mutant.json')]:
  cmd=[sys.executable,'-I','-B',str(recovered/'ledger.py'),'--component',a.component,'--consumer',a.consumer,'--model',a.model,'--submitted',str(submitted),'--output',str(out/label)]
  done=subprocess.run(cmd,capture_output=True,text=True);(out/(label+'.log')).write_text(done.stdout+done.stderr)
  v.need((done.returncode==0)==(label=='fresh-positive'),'PROCESS:'+label)
  if label=='fresh-negative':v.need('LEDGER-SUBSTITUTION' in done.stderr,'PROCESS-REASON')
  rows.append({'case':label,'status':'PASS','exit_code':done.returncode})
except BaseException:
 (out/'unexpected-failure.txt').write_text(traceback.format_exc());raise
finally:(out/'checks.json').write_text(json.dumps({'fresh_controls':len(rows),'checks':rows},indent=2)+'\n')
print('PASS',len(rows),'fresh controls',flush=True)
