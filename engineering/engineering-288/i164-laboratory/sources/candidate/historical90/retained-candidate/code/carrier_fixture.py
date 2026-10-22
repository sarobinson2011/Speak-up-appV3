"""Isolated public LAB credentials and simulated service/C4 evidence. Never operational."""
import json,copy,base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import runtime,backend,sole_service,connected,wire,stages,stage_carrier,outcome,signed_eth
from anchor import *
from test_wire import KEY,EXEC_KEY,SERVER,PUBLIC
from test_outcome import LAB,PUB,sign
from lab_evm import tx
class Fixture:
 def __init__(self,path,pre,create=True):
  self.p=Path(path);self.p.mkdir(parents=True,exist_ok=True);self.pre=parse(enc(pre));self.u='SIGNED-CARRIER-LAB-U'
  principals={'executor':(EXEC_KEY,['executor']),'fixture':(KEY,['executor','lab-result-provider'])}
  self.pre.update(ingress_policy=wire.policy_binding(principals,PUBLIC),outcome_lab_public_key=PUB.hex(),staging_required=True)
  self.cfg={'pilot':'SIGNED-CARRIER-LAB','session':'ONE','implementation':connected.implementation(runtime.Guard(),self.pre),'backend':{'kind':'SIMULATED','table_id':'SIGNED-CARRIER-LAB','service_identity':'SIGNED-CARRIER-LAB'},'origin':'0'*64,'limits':{'attempt':2070,'query':3110,'snapshot':130,'staging_query':2086,'staging_snapshot':85}}
  self.b=backend.SimulatedBackend(self.p/'service.db',self.cfg['backend']);self.s=sole_service.Service(self.b,self.cfg,self.pre)
  if create:self.s.genesis({'executor_head':'0'*64,'transport_head':'0'*64,'transport_seq':0})
  self.ing=wire.Ingress(self.s,self.pre,principals,SERVER);self.ch=wire.OfflineChannel(self.ing);self.client=wire.Client(self.ch,self.cfg,'fixture',KEY,PUBLIC,self.p/'wire.db',create,policy=self.ing.policy);self.x=connected.Connected(self.p/'local',self.client,self.pre,create);self.sch=stages.Scheduler(self.x);self.sink=connected.OfflineSink()
 def close(self):self.x.close();self.client.close();self.b.close()
 def near(self,raw,nonce):
  spec={'network':'near-testnet','engine':'aurora','method':'submit','signer':'lab.testnet','public_key':PUB.hex(),'nonce':nonce,'block_hash':'21'*32,'gas':10**15,'deposit':0}
  unsigned=runtime.retained.t.unsigned(spec,raw);return spec,unsigned+b'\0'+Ed25519PrivateKey.from_private_bytes(LAB).sign(bytes.fromhex(sha(unsigned)))
 def stage_result(self,raw):
  def provide(s,st):
   p=st['pending'];meta=parse(self.s.blob(st['meta'],MAX_INTENT),MAX_INTENT);msg=self.s.blob(st['message'],MAX_INTENT);cmd=stages.command(meta,msg,st['index']);decoded=outcome.engine_result(raw)
   body={'format':'LAB-STAGE-OUTCOME-1','pilot':st['pilot'],'session':st['session'],'sid':st['sid'],'u':st['u'],'intent':st['intent'],'message':st['message'],'command':cmd,'prepared_head':p['prepared_head'],'near_sha256':p['near'],'transaction_id':p['txid'],'query':p['query'],'outcome':decoded['evm_outcome'],'authenticity':'SIMULATED-NOT-GENUINE-C4'}
   if cmd['kind']=='cleanup':body['cleanup_result']=raw.hex()
   return body
  return self.sch.observe_lab(self.u,provide)
 def packet(self,raw):
  s=self.s.fresh();v=s['u'][self.u];prep=parse(self.s.blob(v['near']['ref'],MAX_INTENT),MAX_INTENT);spec=prep['near_spec'];near=bytes.fromhex(prep['near_hex']);evm=self.s.blob(v['record']['tx_ref'],MAX_TRANSACTION)
  tid=outcome.b58(bytes.fromhex(v['near']['transaction_id']));rid=outcome.b58(b'R'*32);block=outcome.b58(b'B'*32);sv={'SuccessValue':base64.b64encode(raw).decode()}
  def o(identity,executor,status,rs):return {'id':identity,'block_hash':block,'proof':[],'outcome':{'executor_id':executor,'status':status,'receipt_ids':rs,'logs':[],'gas_burnt':100,'tokens_burnt':'0','metadata':{'version':1}}}
  transaction={'hash':tid,'signer_id':spec['signer'],'public_key':'ed25519:'+outcome.b58(PUB),'nonce':spec['nonce'],'receiver_id':'aurora','actions':[{'FunctionCall':{'method_name':'submit','args':base64.b64encode(evm).decode(),'gas':10**15,'deposit':'0'}}],'signature':'ed25519:'+outcome.b58(near[-64:]),'priority_fee':0}
  request={'jsonrpc':'2.0','id':'lab','method':'tx','params':{'tx_hash':tid,'sender_account_id':spec['signer'],'wait_until':'FINAL'}}
  response={'jsonrpc':'2.0','id':'lab','result':{'final_execution_status':'FINAL','status':sv,'transaction':transaction,'transaction_outcome':o(tid,spec['signer'],{'SuccessReceiptId':rid},[rid]),'receipts_outcome':[o(rid,'aurora',sv,[])]}}
  return sign({'claim':{'format':'C4-LAB-NEAR-SUBMIT-1','context':outcome.context(self.cfg,self.s.binding,v,self.u,'observe',s['counts']['query']+1),'near_spec':spec,'near_hex':near.hex(),'rpc_request_hex':enc(request).hex(),'rpc_response_hex':enc(response).hex(),'provenance':{'kind':'INDEPENDENTLY-CONSTRUCTED-LAB-FIXTURE','source_authenticated':False,'qualification_established':False}},'signature':''})
