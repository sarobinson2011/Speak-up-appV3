import sys
import json
from pathlib import Path
from outcome import engine_result
from lab_evm import keccak
P=Path(__file__).resolve().parents[1]/'actual-begin';spec=json.loads((P/'records/probes.json').read_text());checks=[]
for i,c in enumerate(spec['cases']):
 rows=[json.loads(x) for x in (P/'results'/f'engine-{i}.jsonl').read_text().splitlines()];assert len(rows)==len(c['transactions'])
 outputs={}
 for t,r in zip(c['transactions'],rows):
  assert r['abort'] is None
  z=engine_result(bytes.fromhex(r['return_bytes']));assert z['status']==('SUCCESS' if t['expected']=='success' else 'REVERTED'),(c['name'],t['stage'],z)
  if t['expected_result'] is not None:assert int(z['output_hex'],16)==t['expected_result']
  if t['stage']=='cleanup':
   want={'address':c['manager'],'topics':[keccak(b'Cleaned(bytes32,bytes32,uint8,bytes32,bytes32)').hex(),c['sid'],c['u']],'data':(4).to_bytes(32,'big').hex()+c['invocation']+c['message']}
   assert z['logs']==[want]
  outputs[t['stage']]=z['output_hex'];checks.append({'case':c['name'],'stage':t['stage'],'evm_gas':z['gas_used'],'near_burnt_gas':r['near_burnt_gas'],'status':z['status']})
 assert outputs['hashes-before']==outputs['hashes-after']
if '--check-only' not in sys.argv:(P/'results/checks.json').write_text(json.dumps({'result':'PASS-ACTUAL-MANAGER-BEGIN-PREFIX-ABANDON-CLEANUP','transactions':len(checks),'checks':checks,'registry_signing_executed':False,'actual_admission':False},indent=2));print('PASS',len(checks))
