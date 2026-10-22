"""Public deterministic laboratory material ONLY; never use for real signing."""
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from transport import enc,sha,unsigned
SEED=bytes(range(32))
def config(attempts=2070,queries=3110,snapshots=130):
 return {'pilot':'LAB-TRANSPORT-ISOLATED-001','attempt_limit':attempts,'query_limit':queries,'snapshot_limit':snapshots,'staging_query_limit':2086,'staging_snapshot_limit':85,'prerequisites':{k:sha(('LAB-UNQUALIFIED-'+k).encode()) for k in ['model','profile','configuration','collector','executor','accounting','authorization','engine_code']}}
def make(c,u='LAB-U-1',nonce=1,size=17):
 key=Ed25519PrivateKey.from_private_bytes(SEED);pub=key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw).hex()
 evm=bytes([17])*size # opaque laboratory bytes; not claimed to be an executable EVM transaction
 intent=enc({'format':'LAB-INTENT','u':u,'evm_sha256':sha(evm),'prerequisites':c['prerequisites'],'comparison_qualified':False})
 s={'network':'near-testnet','engine':'aurora','method':'submit','signer':'lab.testnet','public_key':pub,'nonce':nonce,'block_hash':sha(b'LAB-BLOCK'),'gas':10**15,'deposit':0}
 msg=unsigned(s,evm);raw=msg+b'\0'+key.sign(bytes.fromhex(sha(msg)))
 h={'kind':'LAB-RETIRED-EXECUTOR-HANDOFF','u':u,'intent_sha256':sha(intent),'evm_sha256':sha(evm),'retired':True,'executor_head':sha(b'LAB-RETIRED-HEAD'),'prerequisites':c['prerequisites']}
 return [u,intent,evm,s,raw,h]
def outcome(session,u='LAB-U-1',near='SUCCESS',evm='SUCCESS'):
 rec,raw=session.hydrate(session.states[u]);return {'kind':'LAB-SIMULATED-OUTCOME','network':rec['near_spec']['network'],'signer':rec['near_spec']['signer'],'txid':rec['txid'],'raw_sha256':sha(raw),'finality':'FINAL','near_outcome':near,'evm_outcome':evm}
