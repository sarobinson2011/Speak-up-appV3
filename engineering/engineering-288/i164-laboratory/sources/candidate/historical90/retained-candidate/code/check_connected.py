"""Read-only evidence checking. Does not execute Engine or reopen live stores."""
import json,sys,hashlib
from pathlib import Path
from lab_evm import keccak
from outcome import engine_result
from anchor import enc,parse
import signed_eth
P=Path(__file__).resolve().parents[1]
checks=[]
for idx,count in [(5,15),(3,19)]:
 q=P/'runs'/str(idx);r=json.loads((q/'results/connected.json').read_bytes());full=json.loads((q/'records/full.json').read_bytes());c=full['cases'][0];rows=c['transactions'];assert r['complete'] and r['normal_authenticated_ingress'] and not r['genuine_C4']
 assert r['counts']['attempt']==len(rows)-14==r['counts']['query'];out={}
 for entry in r['rows']:
  end=entry['end'];saved=[json.loads(l) for l in (q/'results'/f'execution-{end}.jsonl').read_bytes().splitlines()]
  assert saved[-1]==entry['execution'];t=rows[end-1];e=entry['execution'];assert e['stage']==t['stage'] and e['abort'] is None
  z=engine_result(bytes.fromhex(e['return_bytes']));assert z==entry['decoded'] and z['status']=='SUCCESS';out[t['stage']]=z
  if entry['release']:
   release=entry['release'];raw=bytes.fromhex(t['signed_transaction']);assert hashlib.sha256(raw).hexdigest()==release['evm_sha256']
   tx=signed_eth.decode(raw);assert tx['target']==t['to'] and tx['calldata']==t['data'] and tx['nonce']==str(end-1)
   submission=json.loads((q/'results'/f'submission-{end-1}.json').read_bytes());near=(q/'results'/f'submission-{end-1}.near').read_bytes();assert submission['release']==release and submission['signed_evm_hex']==t['signed_transaction'] and hashlib.sha256(near).hexdigest()==release['near_sha256']
 assert out['registry-signing']['logs']==[{'address':c['registry'],'topics':[keccak(b'PetitionSigned(uint256,bytes32,bytes32)').hex(),f'{1:064x}',f'{42:064x}'],'data':'00'*32}]
 assert out['cleanup']['output_hex']==f'{1:064x}' and out['cleanup']['logs']==[{'address':c['manager'],'topics':[keccak(b'Cleaned(bytes32,bytes32,uint8,bytes32,bytes32)').hex(),c['sid'],c['u']],'data':f'{2:064x}'+c['invocation_sha256']+c['message_sha256']}]
 assert next(z for k,z in out.items() if k.startswith('finalize'))['output_hex']==f'{1:064x}'
 before=json.loads((q/'results/state-after-registry-signing.json').read_bytes());after=json.loads((q/'results/state-after-cleanup.json').read_bytes())
 def slots(s):
  trie=dict(s['trie']);prefix='0704'+c['manager']+'01000000'
  return lambda n:int(trie.get(prefix+f'{n:064x}','00'*32),16)
 a,b=slots(before),slots(after);assert a(17)==count and b(17)==0 and b(16)==0 and a(14)==b(14)
 for n in [3,8,15]:assert a(n)==b(n) and a(n)!=0
 assert b(3)==int(c['sid'],16) and b(8)==int(c['u'],16) and b(15)==int(c['invocation_sha256'],16)
 base=int.from_bytes(keccak((17).to_bytes(32,'big')),'big');erased=0
 for j in range(count):
  pos=base+j;v=a(pos);positions=[pos]
  if v&1:
   start=int.from_bytes(keccak(pos.to_bytes(32,'big')),'big');positions+=list(range(start,start+(((v-1)//2)+31)//32))
  for n in positions:assert b(n)==0;erased+=1
 for n in range(23,30):assert b(n)==0
 checks.append({'method':c['name'],'connected_governed_attempts':r['counts']['attempt'],'charged_queries':r['counts']['query'],'verifiers':r['counts']['verifier'],'snapshot_charges':r['counts']['snapshot'],'values_erased_words':erased,'actual_signing_and_cleanup':True,'post_sign_recovery_no_second_release':r['recovery_no_second_release'],'genuine_C4':False})
result={'result':'PASS-CONDITIONAL-CONNECTED-SIGNED-BYTE-PATHS','paths':checks,'actual_admission':False}
if '--check-only' not in sys.argv:(P/'results/checked-paths.json').write_bytes(enc(result))
print(json.dumps(result))
