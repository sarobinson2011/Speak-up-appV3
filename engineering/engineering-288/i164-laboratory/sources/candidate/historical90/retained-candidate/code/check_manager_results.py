import sys
import json
from pathlib import Path
from outcome import engine_result
from lab_evm import keccak
P=Path(__file__).resolve().parents[1];spec=json.loads((P/'records/probes.json').read_text());checks=[]
for idx,c in enumerate(spec['cases']):
 logs=[json.loads(x) for x in (P/'results'/f'engine-{idx}.jsonl').read_text().splitlines()];assert len(logs)==len(c['transactions']),(idx,len(logs),len(c['transactions']))
 for i,(t,r) in enumerate(zip(c['transactions'],logs)):
  assert r['abort'] is None and r['stage']==t['stage'] and r['step']==i
  z=engine_result(bytes.fromhex(r['return_bytes']));exp=t['expected'];assert (z['status']=='SUCCESS' if exp=='success' else z['status']=='REVERTED' if exp=='revert' else z['status']!='SUCCESS'),(idx,i,t,z)
  if t.get('expected_result') is not None:assert int(z['output_hex'],16)==t['expected_result'],(idx,i,z)
  if t['stage']=='cleanup':
   topic=keccak(b'Cleaned(bytes32,bytes32,uint8,bytes32,bytes32)').hex()
   assert len(z['logs'])==1 and z['logs'][0]['topics']==[topic,f'{2:064x}',f'{3:064x}'],z
   assert len(bytes.fromhex(z['logs'][0]['data']))==96
  if t['stage']=='repeat-idempotent':assert not z['logs']
  checks.append({'case':c['name'],'stage':t['stage'],'status':z['status'],'evm_gas':z['gas_used'],'near_burnt_gas':r['near_burnt_gas'],'output':z['output_hex'],'logs':z['logs']})
if '--check-only' not in sys.argv:(P/'results/manager-execution-checks.json').write_text(json.dumps({'result':'PASS-ACTUAL-INHERITED-CLEANUP-SEEDED-STATE','transactions':len(checks),'checks':checks,'actual_admission':False,'registry_signing_executed':False,'authentication_executed':False},indent=2));print('PASS',len(checks))
