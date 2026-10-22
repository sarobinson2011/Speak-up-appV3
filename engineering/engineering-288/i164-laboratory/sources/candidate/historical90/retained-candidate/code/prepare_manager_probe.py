import json,hashlib
from pathlib import Path
from lab_evm import *
ROOT=Path(__file__).resolve().parents[1]
o=json.loads((ROOT/'results/compiler-output.json').read_text())['contracts'];old=json.loads((ROOT/'retained/compiled-libraries.json').read_text())
old.update(json.loads((ROOT/'retained/unchanged-libraries.json').read_text()))
for k,v in old.items():o.setdefault(k,v)
images=[];known={};nextaddr=0x164010
def image(f,n):
 global nextaddr
 if (f,n) in known:return known[f,n]
 a=f'{nextaddr:040x}';nextaddr+=1;known[f,n]=a
 v=o[f][n]['evm']['deployedBytecode'];b=v['object']
 for ff,ns in v['linkReferences'].items():
  for nn,rr in ns.items():
   z=image(ff,nn)
   for r in rr:b=b[:2*r['start']]+z+b[2*(r['start']+r['length']):]
 if b.startswith('73'+'00'*20):b='73'+a+b[42:]
 images.append({'name':f+':'+n,'address':a,'code':b,'sha256':hashlib.sha256(bytes.fromhex(b)).hexdigest()});return a
manager=image('CleanupFixture.sol','CleanupSeed');reg=image('CleanupFixture.sol','CleanupRegistryFixture');cases=[]
for mode,st,zk in [('failed',3,False),('abandoned',1,False),('authenticated-ordinary',2,False),('authenticated-zk',2,True),('unavailable-registry',2,False),('unauthorized',3,False),('cleanup-revert-recovery',3,False)]:
 rows=[];nonces={1:0,2:0}
 def emit(stage,data,expected='success',to=manager,key=1,gas=30000000,result=None):
  raw=tx(nonces[key],to,data,gas,key);nonces[key]+=1
  rows.append({'stage':stage,'signed_transaction':raw,'expected':expected,'expected_result':result,'calldata':data.hex()})
 emit('seed-NOT-authentication',call('seed(uint256,address,bool)',st,int(reg,16) if mode!='unavailable-registry' else 0,int(zk)))
 emit('wrong-session',call('cleanup(bytes32)',99),'revert')
 if mode=='unauthorized':emit('unauthorized',call('cleanup(bytes32)',2),'revert',key=2)
 if st in [1,2]:emit('premature',call('cleanup(bytes32)',2),'revert')
 if mode=='unavailable-registry':
  emit('still-authenticated',call('status()'),result=2)
 else:
  if st==1:emit('explicit-abandon',call('abandon()'))
  if st==2:emit('LAB-consumption-oracle-NOT-registry-signing',call('consume(bytes32)',3),to=reg)
  if mode=='cleanup-revert-recovery':
   emit('insufficient-gas-rollback',call('cleanup(bytes32)',2),'failure',gas=28000)
   emit('terminal-state-retained',call('status()'),result=3)
  emit('cleanup',call('cleanup(bytes32)',2),result=1)
  emit('assert-tombstone',call('assertTombstone()'),result=1)
  emit('repeat-idempotent',call('cleanup(bytes32)',2),result=0)
  emit('no-values',call('authorizedValue(uint256)',0),'revert')
  emit('no-finalize',call('finalize()'),'revert')
  emit('no-config-resurrection',call('invalidate(bytes32)',9),'revert')
  emit('no-abandon-resurrection',call('abandon()'),'revert')
  emit('no-reseed',call('seed(uint256,address,bool)',1,int(reg,16),int(zk)),'revert')
  emit('no-append',call('append(bytes32,uint256,bytes)',2,64,96,0),'revert')
 cases.append({'name':mode,'implementation':'ACTUAL-CLEANUP-INHERITED;LAB-seeded-poststate;NO-authentication-or-live-comparison-claim','transactions':rows})
spec={'sender':'7e5f4552091a69125d5dfcb7b8c2659029395bdf','images':images,'cases':cases,'actual_admission':False};spec['binding']=hashlib.sha256(json.dumps(spec,sort_keys=True,separators=(',',':')).encode()).hexdigest()
(ROOT/'records/probes.json').write_text(json.dumps(spec,indent=2));print({'cases':len(cases),'transactions':sum(len(x['transactions']) for x in cases),'images':len(images)})
