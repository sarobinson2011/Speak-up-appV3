"""Versioned local PyEVM call observer; no contract instrumentation or authorization."""
import json,hashlib,os,tempfile
from pathlib import Path
from eth_utils import keccak
from eth_abi import encode,decode
from eth.vm.forks.prague import PragueVM
from eth.vm.forks.prague.state import PragueState
from eth.vm.forks.prague.computation import PragueComputation
SHA=lambda b:hashlib.sha256(b).hexdigest()
W=lambda v:(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()
SEL=keccak(text='compare(bytes32,bytes32,bytes)')[:4]
class Observer:
 def __init__(self,binding,checkpoint=None):self.binding=json.loads(W(binding));self.records=[];self.error=None;self.checkpoint=checkpoint
 def persist(self,status):
  if self.checkpoint is None:return
  p=Path(self.checkpoint);raw=W({"status":status,"binding":self.binding,"records":self.records,"error":self.error,"actual_admission":False});fd,tmp=tempfile.mkstemp(dir=p.parent,prefix=p.name+".pending-")
  with os.fdopen(fd,"wb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
  os.replace(tmp,p);d=os.open(p.parent,os.O_RDONLY);os.fsync(d);os.close(d)
 def capture(self,parent,msg):
  b=self.binding
  if msg.to.hex()!=b['gate'] or bytes(msg.data)[:4]!=SEL:return
  try:
   pc=parent.code.program_counter
   assert parent.msg.storage_address.hex()==b['registry'] and msg.is_static,'wrong frame/call'
   assert SHA(bytes(parent.msg.data))==b['calldata_sha256'],'changed calldata'
   assert SHA(parent.code._raw_code_bytes)==b['implementation_runtime_sha256'],'changed implementation'
   assert SHA(parent.state.get_code(msg.to))==b['gate_runtime_sha256'],'changed gate code'
   assert len(self.records)==0,'multiple cut callbacks'
   raw=bytes(msg.data);decision,cut,evidence=decode(['bytes32','bytes32','bytes'],raw[4:])
   assert encode(['bytes32','bytes32','bytes'],[decision,cut,evidence])==raw[4:],'noncanonical call'
   assert decision.hex()==b['decision_abi_hash'] and keccak(evidence).hex()==b['evidence_keccak'],'decision/evidence mismatch'
   a=parent.msg.storage_address;s=parent.state;words={}
   def get(n):
    n%=2**256;v=s.get_storage(a,n);words[str(n)]=f'{v:064x}';return v
   def address(n):return get(n).to_bytes(32,'big')[-20:]
   chain=s.execution_context.chain_id
   implslot=int.from_bytes(keccak(text='eip1967.proxy.implementation'),'big')-1
   impl=address(implslot)
   assert SHA(s.get_code(impl))==b['implementation_runtime_sha256'],'proxy implementation'
   config=encode(['uint256','address','address','address','address','address','address','address','address','bytes32','bytes32','uint256'],[chain,a,impl,*[address(n) for n in [1,2,6,7,8,9]],get(10).to_bytes(32,'big'),get(11).to_bytes(32,'big'),get(12)])
   petition=b['petition'];null=bytes.fromhex(b['nullifier']);base=int.from_bytes(keccak(encode(['uint256','uint256'],[petition,3])),'big')
   creator=address(base);created=get(base+1);v=get(base+2)
   if v&1:
    length=(v-1)//2;assert length<=4096,'metadata bound';q=int.from_bytes(keccak((base+2).to_bytes(32,'big')),'big');metadata=b''.join(get(q+i).to_bytes(32,'big') for i in range((length+31)//32))[:length]
   else:
    length=(v&255)//2;assert length<=31;metadata=v.to_bytes(32,'big')[:length]
   exists=bool(get(base+3)&255);slot=int.from_bytes(keccak(encode(['uint256','uint256'],[petition,4])),'big');used=bool(get(int.from_bytes(keccak(encode(['bytes32','uint256'],[null,slot])),'big'))&255)
   pre=encode(['bytes32','uint256','uint256','bytes32','address','uint256','bytes32','bool','bool'],[keccak(config),get(13),petition,null,creator,created,keccak(metadata),exists,used])
   assert keccak(pre)==cut and cut.hex()==b['cut'],'same-call cut'
   assert keccak(config).hex()==b['configuration'],'same-call configuration'
   self.records.append({'format':'I164-SAME-CALL-OBSERVER-1','binding_sha256':SHA(W(b)),'phase':'PRE-COMMITMENT','frame_depth':parent.msg.depth,'parent_code_sha256':SHA(parent.code._raw_code_bytes),'parent_input_hex':bytes(parent.msg.data).hex(),'gate_input_hex':raw.hex(),'configuration_preimage_hex':config.hex(),'cut_preimage_hex':pre.hex(),'cut':cut.hex(),'storage_words':words,'metadata_hex':metadata.hex(),'u':b['u'],'qualification_established':False})
   assert parent.code.program_counter==pc,'observer advanced execution'
   self.persist('INTERRUPTED-OR-IN-FLIGHT')
  except Exception as e:self.error=str(e);self.persist('INVALID');raise RuntimeError('OBSERVER-INVALID: '+str(e))
 def finish(self,completed=False):
  status='INVALID' if self.error else 'INTERRUPTED-OR-IN-FLIGHT' if not completed else 'CUT-OBSERVED' if self.records else 'CUT-NOT-REACHED'
  self.persist(status)
  return {'status':status,'records':self.records,'error':self.error,'binding':self.binding,'actual_admission':False}
 def vm(self):
  observer=self
  class Computation(PragueComputation):
   def apply_child_computation(self,msg):
    observer.capture(self,msg)
    child=super().apply_child_computation(msg)
    if msg.to.hex()==observer.binding['gate'] and bytes(msg.data)[:4]==SEL and observer.records:
     observer.records[-1]['gate_output_hex']=bytes(child.output).hex();observer.records[-1]['gate_error']=child.is_error
    return child
  state=PragueState.configure(__name__='I164ObservedState',computation_class=Computation)
  return PragueVM.configure(__name__='I164ObservedVM',_state_class=state)
