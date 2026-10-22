"""Entirely synthetic, never a project-authorized occurrence or production key."""
from bridge import *
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

def config():
 p={k:t.sha(('LAB-UNQUALIFIED-'+k).encode()) for k in ['model','profile','configuration','collector','executor','accounting','authorization','engine_code']}
 job='LAB-TRANSPORT-CONNECTION-001';root=ROOT/'retained/executor-basis/retained/kernel/candidate'
 b={'version':e.VERSION,'code':{n:e.sha((root/n).read_bytes()) for n in ['executor/session.py','executor/abi.py','contract/PetitionRegistryPilot.sol','contract/ABI.json','contract/method-identifiers.json']},'job':job}
 p['executor']=t.sha(e.enc(b));p['accounting']=t.sha((ROOT/'code/bridge.py').read_bytes())
 return {'pilot':job,'attempt_limit':2070,'query_limit':3110,'snapshot_limit':130,'staging_query_limit':2086,'staging_snapshot_limit':85,'prerequisites':p}
def intent(c,u='LAB-U-1',method='signPetition',nonce=1):
 d={k:'00'*32 for k in ['u','operationHash','actorBinding','governing','prerequisiteBinding','expectedCut','evidenceHash']};d.update(epoch=0,revision=0,deadline=0);d['u']=e.u_wire(u)
 capsule={'format':'I164-COMPUTED-COMPARISON-CAPSULE-1','permit_for_conditional_test':True,'synthetic_assumption':True}
 # Build exact declared ABI fields mechanically, including both signing paths.
 abi=json.loads((ROOT/'retained/executor-basis/retained/kernel/candidate/contract/ABI.json').read_text());f=next(x for x in abi if x.get('name')==method)
 def val(x):
  typ=x['type']
  if x['name']=='d':return d
  if typ=='bytes':return e.enc(capsule).hex() if x['name']=='evidence' else 'ab'
  if typ=='bytes32':return '00'*32
  if typ=='uint256':return 1
  if typ.endswith(']'):
   base,n=typ.rsplit('[',1);return [val({'type':base,'name':''}) for _ in range(int(n[:-1]))]
  raise ValueError(typ)
 a={x['name']:val(x) for x in f['inputs']};i={k:'0'*64 for k in ['config','source','model','contract','profile','scope']}
 i.update(config=c['prerequisites']['configuration'],model=c['prerequisites']['model'],profile=c['prerequisites']['profile'],chain='1313161555',registry='1'*40,executor='2'*40,nonce=str(nonce),calldata_hex=e.abi_encode(method,a).hex(),value='0',gas_limit='10000000',decision=e.sha(e.enc(d)),key_epoch='0',method=method,arguments=a)
 return i
def envelope(bridge,u='LAB-U-1',nonce=1):
 key=Ed25519PrivateKey.from_private_bytes(bytes(range(32)));pub=key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw).hex()
 raw=bytes.fromhex(bridge.executor.states[u]['synthetic_transaction_hex']);s={'network':'near-testnet','engine':'aurora','method':'submit','signer':'lab.testnet','public_key':pub,'nonce':nonce,'block_hash':t.sha(b'LAB-BLOCK'),'gas':10**15,'deposit':0}
 msg=t.unsigned(s,raw);return s,msg+b'\0'+key.sign(bytes.fromhex(t.sha(msg)))
def outcome(b,u='LAB-U-1',near='SUCCESS',evm='SUCCESS'):
 rec,raw=b.transport.hydrate(b.transport.states[u]);return {'kind':'LAB-SIMULATED-OUTCOME','network':rec['near_spec']['network'],'signer':rec['near_spec']['signer'],'txid':rec['txid'],'raw_sha256':t.sha(raw),'finality':'FINAL','near_outcome':near,'evm_outcome':evm}
