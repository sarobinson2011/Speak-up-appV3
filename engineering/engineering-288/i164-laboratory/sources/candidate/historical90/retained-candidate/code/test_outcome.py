"""Independently constructed OFFLINE RPC-shaped fixtures, never network observations."""
import unittest,tempfile,struct,base64,copy,json,threading
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import runtime,backend,sole_service,connected,wire,outcome
from anchor import *
from test_connected import config,intent
from test_wire import KEY,EXEC_KEY,SERVER,PUBLIC
LAB=bytes.fromhex(sha(b'C4-public-laboratory-seed-not-operational'))
PUB=wire.public(LAB)
def result_bytes(tag=0,data=b'',logs=()):
 # Independent explicit Borsh layout from pinned engine.rs, not production decoder.
 b=bytes([7,tag])
 if tag in (0,1,18):b+=struct.pack('<I',len(data))+data
 elif tag==13:b+=data
 b+=struct.pack('<QI',123,len(logs))
 for a,ts,d in logs:b+=a+struct.pack('<I',len(ts))+b''.join(ts)+struct.pack('<I',len(d))+d
 return b
def vector(b):return struct.pack('<I',len(b))+b
def sign(p):p['signature']=Ed25519PrivateKey.from_private_bytes(LAB).sign(outcome.DOMAIN+enc(p['claim'])).hex();return p
class Fixture:
 def __init__(self,path,create=True):
  self.p=Path(path);self.p.mkdir(parents=True,exist_ok=True);self.c=config();self.pre={k:self.c['prerequisites'][v] for k,v in [('model','model'),('profile','profile'),('config','configuration')]}
  principals={'executor':(EXEC_KEY,['executor']),'fixture':(KEY,['executor','lab-result-provider'])}
  self.pre.update(ingress_policy=wire.policy_binding(principals,PUBLIC),outcome_lab_public_key=PUB.hex())
  self.desc={'kind':'SIMULATED','service_identity':'LAB-C4-SERVICE','table_id':'LAB-C4-TABLE'}
  self.cfg={'pilot':'LAB-C4','session':'ONE','implementation':connected.implementation(runtime.Guard(),self.pre),'backend':self.desc,'origin':'0'*64,'limits':{'attempt':2,'query':1,'snapshot':2,'staging_query':1,'staging_snapshot':2}}
  self.b=backend.SimulatedBackend(self.p/'service.db',self.desc);self.s=sole_service.Service(self.b,self.cfg,self.pre)
  if create:self.s.genesis({'executor_head':'0'*64,'transport_head':'0'*64,'transport_seq':0})
  self.ing=wire.Ingress(self.s,self.pre,principals,SERVER);self.ch=wire.OfflineChannel(self.ing);self.client=wire.Client(self.ch,self.cfg,'fixture',KEY,PUBLIC,self.p/'wire.db',create,policy=self.ing.policy);self.x=connected.Connected(self.p/'local',self.client,self.pre,create);self.u='LAB-U-1';self.sink=connected.OfflineSink()
 def sent(self):
  self.x.retire(self.u,intent(self.c),'retire');self.x.seal_conditional(self.u,'seal');spec,near,_=self.near();self.x.bind_near_conditional(self.u,'near',spec,near);self.x.submit_conditional(self.u,'attempt',self.sink)
 def close(self):self.x.close();self.client.close();self.b.close()
 def near(self):
  st=self.s.fresh();v=st['u'][self.u];evm=self.s.blob(v['record']['tx_ref'],MAX_TRANSACTION)
  spec={'network':'near-testnet','engine':'aurora','method':'submit','signer':'lab.testnet','public_key':PUB.hex(),'nonce':1,'block_hash':'21'*32,'gas':10**15,'deposit':0}
  unsigned=vector(b'lab.testnet')+b'\0'+PUB+struct.pack('<Q',1)+vector(b'aurora')+bytes.fromhex(spec['block_hash'])+struct.pack('<I',1)+b'\x02'+vector(b'submit')+vector(evm)+struct.pack('<Q',10**15)+bytes(16)
  signature=Ed25519PrivateKey.from_private_bytes(LAB).sign(bytes.fromhex(sha(unsigned)));near=unsigned+b'\0'+signature;return spec,near,evm
 def packet(self,tag=0,near_failure=False):
  st=self.s.fresh();v=st['u'][self.u];spec,near,evm=self.near();signature=near[-64:];txid=outcome.b58(bytes.fromhex(sha(near[:-65])));rid=outcome.b58(b'R'*32);block=outcome.b58(b'B'*32)
  sv={'Failure':{'ActionError':{'index':0,'kind':{'FunctionCallError':{'ExecutionError':'LAB-Engine failure; EVM unavailable'}}}}} if near_failure else {'SuccessValue':base64.b64encode(result_bytes(tag)).decode()}
  def o(identity,executor,status,receipts):return {'id':identity,'block_hash':block,'proof':[],'outcome':{'executor_id':executor,'status':status,'receipt_ids':receipts,'logs':[],'gas_burnt':100,'tokens_burnt':'0','metadata':{'version':1}}}
  tx={'hash':txid,'signer_id':'lab.testnet','public_key':'ed25519:'+outcome.b58(PUB),'nonce':1,'receiver_id':'aurora','actions':[{'FunctionCall':{'method_name':'submit','args':base64.b64encode(evm).decode(),'gas':10**15,'deposit':'0'}}],'signature':'ed25519:'+outcome.b58(signature),'priority_fee':0}
  request={'jsonrpc':'2.0','id':'query-1','method':'tx','params':{'tx_hash':txid,'sender_account_id':'lab.testnet','wait_until':'FINAL'}}
  response={'jsonrpc':'2.0','id':'query-1','result':{'final_execution_status':'FINAL','status':sv,'transaction':tx,'transaction_outcome':o(txid,'lab.testnet',{'SuccessReceiptId':rid},[rid]),'receipts_outcome':[o(rid,'aurora',sv,[])]}}
  claim={'format':'C4-LAB-NEAR-SUBMIT-1','context':outcome.context(self.cfg,self.s.binding,v,self.u,'observe',1),'near_spec':spec,'near_hex':near.hex(),'rpc_request_hex':enc(request).hex(),'rpc_response_hex':enc(response).hex(),'provenance':{'kind':'INDEPENDENTLY-CONSTRUCTED-LAB-FIXTURE','source_authenticated':False,'qualification_established':False}}
  return sign({'claim':claim,'signature':''})
 def decode(self,p):
  s=self.s.fresh();v=s['u'][self.u];return outcome.validate(p,outcome.context(self.cfg,self.s.binding,v,self.u,'observe',1),self.s.blob(v['record']['tx_ref'],MAX_TRANSACTION),PUB)
 def edit(self,p,fn):
  q=copy.deepcopy(p);z=outcome.obj(bytes.fromhex(q['claim']['rpc_response_hex']));fn(z['result']);q['claim']['rpc_response_hex']=enc(z).hex();return sign(q)
class Tests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.f=Fixture(self.tmp.name);self.f.sent();self.p=self.f.packet()
 def tearDown(self):self.f.close();self.tmp.cleanup()
 def test_success_revert_connected(self):
  for tag in (0,1):
   with self.subTest(tag=tag),tempfile.TemporaryDirectory() as d:
    f=Fixture(d);f.sent();p=f.packet(tag);r=f.decode(p);self.assertFalse(r['authoritative_terminal']);self.assertEqual(r['conditional_terminal'],['SUCCESS','REVERTED'][tag])
    f.x.save_outcome_evidence(f.u,'observe',p);before=connected.copy_counts(f.s.fresh());self.assertIsNone(f.x.internal_terminal_repair());self.assertIsNone(f.x.internal_terminal_repair());self.assertEqual(before,connected.copy_counts(f.s.fresh()));self.assertEqual(f.x.executor.states[f.u]['status'],['SUCCESS','FAILED'][tag]);self.assertEqual(len(f.sink.sent),1)
    with self.assertRaises(ValueError):f.x.submit_conditional(f.u,'again',f.sink)
    with self.assertRaises(ValueError):outcome.require_authoritative(r)
    f.close()
 def test_all_engine_variants(self):
  for tag in range(20):
   d=b'X' if tag==13 else b'error' if tag==18 else b''
   r=outcome.engine_result(result_bytes(tag,d));self.assertEqual(r['evm_outcome'],['SUCCESS','REVERTED'][tag] if tag<2 else 'OTHER-EVM-FAILURE')
 def test_exact_log_bytes(self):
  r=outcome.engine_result(result_bytes(0,b'\0\xff',[(b'A'*20,[b'T'*32],b'\r\n')]))
  self.assertEqual(r['output_hex'],'00ff');self.assertEqual(r['logs'][0]['data'],'0d0a')
 def test_malformed_borsh_boundaries(self):
  b=result_bytes(0,b'text')
  for n in range(len(b)):
   with self.assertRaises(ValueError):outcome.engine_result(b[:n])
  for x in [b+b'X',b'\x08'+b[1:],b'\x07\xff'+b[2:],b'\x07\x00\xff\xff\xff\xff',result_bytes(18,b'\xff'),b'X'*(outcome.MAX_RESULT+1)]:
   with self.assertRaises(ValueError):outcome.engine_result(x)
 def test_substituted_transaction_and_evm(self):
  for fn in [lambda z:z['transaction'].update(hash=outcome.b58(b'Z'*32)),lambda z:z['transaction'].update(nonce=2),lambda z:z['transaction']['actions'][0]['FunctionCall'].update(args='AA=='),lambda z:z['transaction'].update(receiver_id='other')]:
   with self.assertRaises(ValueError):self.f.decode(self.f.edit(self.p,fn))
  p=copy.deepcopy(self.p);p['claim']['near_hex']=p['claim']['near_hex'][:-2]+'00';sign(p)
  with self.assertRaises(ValueError):self.f.decode(p)
 def test_wrong_context_network_engine(self):
  for field in self.p['claim']['context']:
   p=copy.deepcopy(self.p);p['claim']['context'][field]='wrong';sign(p)
   with self.assertRaises(ValueError):self.f.decode(p)
  for field in ['network','engine','method']:
   p=copy.deepcopy(self.p);p['claim']['near_spec'][field]='wrong';sign(p)
   with self.assertRaises(ValueError):self.f.decode(p)
 def test_receipt_substitution_and_closure(self):
  edits=[lambda z:z['receipts_outcome'][0].update(id=outcome.b58(b'Z'*32)),lambda z:z['receipts_outcome'][0]['outcome'].update(executor_id='wrong'),lambda z:z['receipts_outcome'].append(copy.deepcopy(z['receipts_outcome'][0])),lambda z:z.update(receipts_outcome=[]),lambda z:z['receipts_outcome'][0]['outcome'].update(receipt_ids=[z['receipts_outcome'][0]['id']])]
  for fn in edits:
   with self.assertRaises(ValueError):self.f.decode(self.f.edit(self.p,fn))
 def test_altered_result_signature_and_conflict(self):
  p=self.f.edit(self.p,lambda z:z.update(status={'SuccessValue':base64.b64encode(result_bytes(1)).decode()}))
  with self.assertRaises(ValueError):self.f.decode(p)
  p=copy.deepcopy(self.p);p['signature']='00'*64
  with self.assertRaises(ValueError):self.f.decode(p)
  p=copy.deepcopy(self.p);del p['signature']
  with self.assertRaises(ValueError):self.f.decode(p)
 def test_missing_finality_and_ack_not_execution(self):
  for status in ['NONE','INCLUDED','EXECUTED_OPTIMISTIC','EXECUTED','UNKNOWN']:
   with self.assertRaises(ValueError):self.f.decode(self.f.edit(self.p,lambda z:z.update(final_execution_status=status)))
  p=copy.deepcopy(self.p);p['claim']['rpc_response_hex']=enc({'jsonrpc':'2.0','id':'query-1','result':'ackhash'}).hex();sign(p)
  with self.assertRaises(ValueError):self.f.decode(p)
 def test_near_failure_not_reverted(self):
  p=self.f.packet(near_failure=True);r=self.f.decode(p);self.assertEqual(r['evm_outcome'],'UNAVAILABLE');self.assertIsNone(r['conditional_terminal']);self.f.x.save_outcome_evidence(self.f.u,'observe',p);before=connected.copy_counts(self.f.s.fresh());self.f.x.internal_terminal_repair();self.assertEqual(self.f.x.executor.states[self.f.u]['status'],'UNCERTAIN');self.assertEqual(before,connected.copy_counts(self.f.s.fresh()))
 def test_other_evm_failure_not_reverted(self):
  p=self.f.packet(2);self.f.x.save_outcome_evidence(self.f.u,'observe',p);self.f.x.internal_terminal_repair();self.assertEqual(self.f.x.executor.states[self.f.u]['status'],'UNCERTAIN')
 def test_lab_claims_cannot_qualify(self):
  p=copy.deepcopy(self.p);p['claim']['provenance']['qualification_established']=True;sign(p)
  with self.assertRaises(ValueError):self.f.decode(p)
  r=self.f.decode(self.p)
  with self.assertRaises(ValueError):outcome.require_authoritative(dict(r,authenticated_finality=True,qualification_established=True))
 def test_no_label_only_bypass(self):
  with self.assertRaises(ValueError):self.f.x.save_conditional_observation(self.f.u,'label','SUCCESS')
  self.assertIsNone(self.f.s.fresh()['u'][self.f.u]['saved']);self.assertEqual(self.f.s.fresh()['counts']['query'],0)
 def test_reopen_after_observation_and_repair_interrupt(self):
  f=self.f
  with self.assertRaises(Uncertain):f.x.save_outcome_evidence(f.u,'observe',self.p,crash='after_service')
  f.close();self.f=f=Fixture(self.tmp.name,False);self.assertEqual(f.s.fresh()['counts']['query'],1)
  with self.assertRaises(Uncertain):f.x.internal_terminal_repair(crash='after_service')
  f.close();self.f=f=Fixture(self.tmp.name,False);f.x.internal_terminal_repair();f.x.internal_terminal_repair();self.assertEqual(f.x.executor.states[f.u]['status'],'SUCCESS');self.assertEqual(f.s.fresh()['counts']['query'],1);self.assertEqual(f.s.fresh()['counts']['attempt'],1)
 def test_before_commit_uncertain_pending(self):
  with self.assertRaises(Uncertain):self.f.x.save_outcome_evidence(self.f.u,'observe',self.p,crash='before_service')
  self.assertEqual(self.f.s.fresh()['counts']['query'],0);self.assertIsNone(self.f.s.fresh()['u'][self.f.u]['saved'])
  with self.assertRaises(ValueError):self.f.x.save_outcome_evidence(self.f.u,'another',self.p)
  self.assertEqual(self.f.x.executor.states[self.f.u]['status'],'UNCERTAIN')
 def test_duplicate_and_conflicting_evidence(self):
  self.f.x.save_outcome_evidence(self.f.u,'observe',self.p);receipt=self.f.client.resolve('observe')['receipt'];req=receipt['request']
  d=self.f.client.commit(req['expected'],'observe','OBSERVE_EVIDENCE',self.f.u,{'evidence':self.p});self.assertFalse(d['release']);self.assertTrue(d['duplicate'])
  with self.assertRaises(ValueError):self.f.client.commit(req['expected'],'observe','OBSERVE_EVIDENCE',self.f.u,{'evidence':self.f.packet(1)})
  self.assertEqual(self.f.s.fresh()['counts']['query'],1)
 def test_corrupt_saved_evidence(self):
  self.f.x.save_outcome_evidence(self.f.u,'observe',self.p);v=self.f.s.fresh()['u'][self.f.u];self.f.b.db.execute('UPDATE objects SET v=? WHERE k=?',(b'broken','BLOB/'+v['saved']['ref']))
  with self.assertRaises(ValueError):self.f.x.internal_terminal_repair()
 def test_noncanonical_json_duplicates(self):
  p=copy.deepcopy(self.p);p['claim']['rpc_response_hex']=b'{"result":1,"result":2}'.hex();sign(p)
  with self.assertRaises(ValueError):self.f.decode(p)
 def test_exhaustion_preserves_u(self):
  self.f.x.save_outcome_evidence(self.f.u,'observe',self.p)
  with self.assertRaises(ValueError):self.f.x.save_outcome_evidence(self.f.u,'extra',self.p)
  self.assertEqual(self.f.s.fresh()['counts']['query'],1);self.assertEqual(self.f.s.fresh()['counts']['attempt'],1);self.assertIn(self.f.u,self.f.s.fresh()['u'])
 def test_concurrent_observations_one_charge(self):
  barrier=threading.Barrier(2);answers=[];head=self.f.s.fresh()['head']
  def run(n):
   b=backend.SimulatedBackend(self.f.p/'service.db',self.f.desc);sv=sole_service.Service(b,self.f.cfg,self.f.pre)
   principals={'executor':(EXEC_KEY,['executor']),'fixture':(KEY,['executor','lab-result-provider'])}
   ing=wire.Ingress(sv,self.f.pre,principals,SERVER);cl=wire.Client(wire.OfflineChannel(ing),self.f.cfg,'fixture',KEY,PUBLIC,self.f.p/('parallel'+str(n)+'.db'),True,policy=ing.policy)
   p=copy.deepcopy(self.p);op='concurrent-'+str(n);p['claim']['context']['observation_request']=op;sign(p)
   try:
    barrier.wait();cl.commit(head,op,'OBSERVE_EVIDENCE',self.f.u,{'evidence':p});answers.append('commit')
   except (ValueError,Uncertain):answers.append('blocked')
   finally:cl.close();b.close()
  ts=[threading.Thread(target=run,args=(n,)) for n in range(2)]
  for t in ts:t.start()
  for t in ts:t.join(10)
  self.assertEqual(sorted(answers),['blocked','commit']);self.f.x.recover();self.assertEqual(self.f.s.fresh()['counts']['query'],1)
 def test_unavailable_service_no_repair(self):
  self.f.x.save_outcome_evidence(self.f.u,'observe',self.p);self.f.ch.available=False
  with self.assertRaises(Uncertain):self.f.x.internal_terminal_repair()
  self.f.ch.available=True;self.f.x.internal_terminal_repair();self.assertEqual(self.f.s.fresh()['counts']['query'],1)
 def test_mutated_prepared_near_and_no_second_binding(self):
  spec,near,_=self.f.near()
  with self.assertRaises(ValueError):self.f.x.bind_near_conditional(self.f.u,'near-again',spec,near)
  self.assertEqual(self.f.s.fresh()['counts']['attempt'],1)
  self.assertEqual(self.f.sink.sent,[near])
 def test_interrupted_input_validation_no_charge(self):
  p=copy.deepcopy(self.p);p['claim']['rpc_response_hex']=p['claim']['rpc_response_hex'][:-10];sign(p)
  with self.assertRaises(ValueError):self.f.x.save_outcome_evidence(self.f.u,'observe',p)
  self.assertEqual(self.f.s.fresh()['counts']['query'],0);self.assertIsNone(self.f.s.fresh()['u'][self.f.u]['saved'])
  self.f.x.save_outcome_evidence(self.f.u,'observe',self.p);self.f.x.internal_terminal_repair()
 def test_executor_only_rollback_keeps_reservation(self):
  with tempfile.TemporaryDirectory() as d:
   f=Fixture(d);old=(Path(d)/'local/executor.db').read_bytes();f.sent();p=f.packet();f.x.save_outcome_evidence(f.u,'observe',p);f.close()
   (Path(d)/'local/executor.db').write_bytes(old);f=Fixture(d,False)
   self.assertEqual(f.x.executor.states[f.u]['status'],'UNCERTAIN')
   other=intent(f.c,nonce=2)
   with self.assertRaises(ValueError):f.x.retire(f.u,other,'different-intent')
   self.assertEqual(f.s.fresh()['counts']['attempt'],1);self.assertEqual(f.s.fresh()['counts']['query'],1)
   f.close()
 def test_wrong_authorization_key(self):
  with self.assertRaises(ValueError):outcome.validate(self.p,self.p['claim']['context'],self.f.near()[2],wire.public(b'X'*32))
if __name__=='__main__':unittest.main()

