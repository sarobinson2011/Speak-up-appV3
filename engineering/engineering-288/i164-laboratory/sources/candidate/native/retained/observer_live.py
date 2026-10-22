"""Versioned observer extension: same-call guards and registry-direct external result.
No prospective execution is performed by importing this module.
"""
from observer import Observer,PragueComputation,PragueState,PragueVM,SHA,W,SEL
from eth_utils import keccak
from eth_abi import encode
from selected import params

def supplement(parent,record,external):
 a=parent.msg.storage_address;state=parent.state
 _,args=params({'records':[record]});d=args['d']
 def get(slot):return state.get_storage(a,slot)
 def consumed(key,slot):return bool(get(int.from_bytes(keccak(encode(['bytes32','uint256'],[key,slot])),'big'))&255)
 gate=get(9).to_bytes(32,'big')[-20:]
 return {'format':'I164-SAME-CALL-SUPPLEMENT-1','caller':parent.msg.sender.hex(),'call_value':parent.msg.value,'timestamp':state.execution_context.timestamp,'entered':bool(get(14)&255),'consumed_u':consumed(d[0],15),'consumed_evidence':consumed(d[6],16),'gate_codehash':keccak(state.get_code(gate)).hex(),'proxy_runtime_sha256':SHA(state.get_code(a)),'external':external}

class LiveObserver(Observer):
 def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.external=[]
 def capture(self,parent,msg):
  count=len(self.records);super().capture(parent,msg)
  if len(self.records)>count:
   try:
    if len(self.external)!=1:raise ValueError('required registry-direct external call unavailable/ambiguous')
    self.records[-1]['supplement']=supplement(parent,self.records[-1],self.external[0]);self.persist('INTERRUPTED-OR-IN-FLIGHT')
   except Exception as e:self.error=str(e);self.persist('INVALID');raise
 def vm(self):
  observer=self
  class Computation(PragueComputation):
   def apply_child_computation(self,msg):
    observer.capture(self,msg)
    direct=(self.msg.storage_address.hex()==observer.binding.get('registry') and SHA(self.code._raw_code_bytes)==observer.binding['implementation_runtime_sha256'])
    is_gate=msg.to.hex()==observer.binding['gate'] and bytes(msg.data)[:4]==SEL
    codehash=keccak(self.state.get_code(msg.to)).hex()
    child=super().apply_child_computation(msg)
    if direct and not is_gate:
     if not msg.is_static or len(bytes(msg.data))>65536 or len(bytes(child.output))>65536:raise ValueError('unsupported external call/capture bounds')
     observer.external.append({'target':msg.to.hex(),'input':bytes(msg.data).hex(),'output':bytes(child.output).hex(),'reverted':bool(child.is_error),'codehash':codehash});observer.persist('INTERRUPTED-OR-IN-FLIGHT')
    if is_gate and observer.records:
     observer.records[-1]['gate_output_hex']=bytes(child.output).hex();observer.records[-1]['gate_error']=child.is_error
    return child
  state=PragueState.configure(__name__='I164LiveFactsState',computation_class=Computation)
  return PragueVM.configure(__name__='I164LiveFactsVM',_state_class=state)

# Persist direct call outcomes even when rejection prevents reaching the cut.
def _persist_live(self,status):
 if self.checkpoint is None:return
 import os,tempfile
 from pathlib import Path
 p=Path(self.checkpoint);payload={'format':'I164-LIVE-OBSERVER-2','status':status,'binding':self.binding,'records':self.records,'registry_direct_calls':self.external,'error':self.error,'actual_admission':False}
 fd,tmp=tempfile.mkstemp(dir=p.parent,prefix=p.name+'.pending-')
 with os.fdopen(fd,'wb') as f:f.write(W(payload));f.flush();os.fsync(f.fileno())
 os.replace(tmp,p);fd=os.open(p.parent,os.O_RDONLY);os.fsync(fd);os.close(fd)
def _finish_live(self,completed=False):
 result=Observer.finish(self,completed);result['format']='I164-LIVE-OBSERVER-2';result['registry_direct_calls']=self.external;return result
LiveObserver.persist=_persist_live
LiveObserver.finish=_finish_live
