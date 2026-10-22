"""Bounded fixture preparation from unchanged saved contract inputs. No EVM execution."""
import sys,json,copy,shutil
from pathlib import Path
from anchor import *
from carrier_fixture import Fixture
from lab_evm import keccak,tx
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import runtime,stages,stage_carrier,signed_eth
P=Path(__file__).resolve().parents[1]
def decode_args(method,raw):
 abi=json.loads(runtime.executor.abi_encode.__globals__['ABI_BYTES']);fields=next(x['inputs'] for x in abi if x.get('name')==method);data=raw[4:]
 def val(f,pos):
  typ=f['type']
  if typ=='tuple':
   out={}
   for c in f['components']:out[c['name']],pos=val(c,pos)
   return out,pos
  if typ.endswith(']'):
   base,n=typ.rsplit('[',1);a=[]
   for _ in range(int(n[:-1])):x,pos=val({'type':base},pos);a.append(x)
   return a,pos
  b=data[pos:pos+32];assert len(b)==32
  if typ=='uint256':return int.from_bytes(b,'big'),pos+32
  if typ=='bytes32':return b.hex(),pos+32
  if typ=='bytes':
   off=int.from_bytes(b,'big');n=int.from_bytes(data[off:off+32],'big');return data[off+32:off+32+n].hex(),pos+32
  raise ValueError(typ)
 out={};pos=0
 for f in fields:out[f['name']],pos=val(f,pos)
 assert runtime.executor.abi_encode(method,out)==raw
 return out

def prepare(old,idx,target=None):
 old=Path(old);q=P/'runs'/str(idx if target is None else target);q.mkdir(parents=True,exist_ok=False)
 prior=json.loads((old/'records/probes.json').read_bytes());case=prior['cases'][idx];meta=json.loads((old/f'records/meta-{idx}.json').read_bytes());message=(old/f'records/message-{idx}.bin').read_bytes();decoded=json.loads(message[len(stage_carrier.DOMAIN):]);c=decoded['bindings'];method=c['method'];args=decode_args(method,bytes.fromhex(meta['invocation']));old_u=c['u'];u='SIGNED-CARRIER-LAB-U';new_u=runtime.executor.u_wire(u);args['d']['u']=new_u;inv=runtime.executor.abi_encode(method,args)
 decoded['authorized_values']=[bytes.fromhex(v).replace(bytes.fromhex(old_u),bytes.fromhex(new_u)).hex() for v in decoded['authorized_values']]
 c.update(pilot='SIGNED-CARRIER-LAB',engine='aurora',u=new_u,inputs=sha(inv))
 # History hash is always exactly 64 chars, so count is known before reservation.
 n=(len(stage_carrier.DOMAIN+enc(decoded))+511)//512;start=len([t for t in case['transactions'] if t['stage'].startswith('setup-')]);nonce=start+n+2
 policy={'version':signed_eth.VERSION,'signer':c['executor'],'chain':c['network'],'gas_limit':'100000000','gas_price':'0','value':'0','stage_start_nonce':str(start)}
 pre={'model':c['model'],'profile':c['profile'],'config':c['configuration'],'ethereum_carrier':policy}
 f=Fixture(q/'stores',pre)
 i={k:'a'*64 for k in ['source','scope']};i.update(chain=c['network'],registry=c['registry'],executor=c['executor'],nonce=str(nonce),calldata_hex=inv.hex(),value='0',gas_limit='100000000',config=c['configuration'],decision=sha(enc(args['d'])),model=c['model'],contract=c['contract'],profile=c['profile'],key_epoch='0',method=method,arguments=args,carrier=signed_eth.VERSION,gas_price='0',signed_evm_hex=tx(nonce,c['registry'],inv,100000000),conditional_comparison_hex=enc({'format':'I164-COMPUTED-COMPARISON-CAPSULE-1','permit_for_conditional_test':True,'synthetic_assumption':True,'scope':'local fixture only; not operational comparison authorization'}).hex())
 f.x.retire_compact(u,i,'retire');c['history_prefix']=f.s.fresh()['head'];message=stage_carrier.DOMAIN+enc(decoded);assert (len(message)+511)//512==n
 sig=Ed25519PrivateKey.from_private_bytes(bytes([17])*32).sign(message);key=bytes.fromhex(meta['key']);f.sch.open(u,message,key,sig)
 s,st=f.sch.state(u);meta=parse(f.s.blob(st['meta'],MAX_INTENT),MAX_INTENT);rows=copy.deepcopy(case['transactions'][:start]);assert all(t['stage'].startswith('setup-') for t in rows)
 for index in range(n+2):
  cmd=stages.command(meta,message,index);data=stages.calldata(meta,st['sid'],cmd);no=start+index;rows.append({'stage':cmd['kind']+'-'+str(index),'signed_transaction':tx(no,cmd['target'],data,100000000),'timestamp':1791000001+no,'data':data.hex(),'to':cmd['target'],'expected':'success'})
 target=next(t for t in case['transactions'] if t['stage']=='registry-signing');rows.append({'stage':'registry-signing','signed_transaction':i['signed_evm_hex'],'timestamp':target['timestamp'],'data':inv.hex(),'to':c['registry'],'expected':'success'})
 cmd=stages.command(meta,message,n+2);data=stages.calldata(meta,st['sid'],cmd);rows.append({'stage':'cleanup','signed_transaction':tx(nonce+1,cmd['target'],data,100000000),'timestamp':target['timestamp']+3,'data':data.hex(),'to':cmd['target'],'expected':'success'})
 spec={'sender':prior['sender'],'images':[],'cases':[dict(case,transactions=rows,sid=st['sid'],u=new_u,invocation_sha256=sha(inv),message_sha256=sha(message))],'actual_admission':False};spec['binding']=sha(enc(spec))
 (q/'records').mkdir();(q/'results').mkdir();(q/'records/full.json').write_bytes(enc(spec));(q/'records/intent.json').write_bytes(enc(i));(q/'records/prerequisites.json').write_bytes(enc(f.pre));(q/'records/meta.json').write_bytes(enc(meta));(q/'records/message.bin').write_bytes(message)
 for name in ['retained/source/aurora-engine.wasm','retained/records/testnet-pinned-block.json']:
  (q/name).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(old/name,q/name)
 f.close();return {'case':idx,'method':method,'governed_transactions':n+4,'setup_transactions':start,'sid':st['sid'],'u':new_u,'intent_sha256':sha(enc(i)),'message_sha256':sha(message),'actual_admission':False}
if __name__=='__main__':
 print(json.dumps([prepare(sys.argv[1],i,i+2) for i in [0,1]],indent=2))
