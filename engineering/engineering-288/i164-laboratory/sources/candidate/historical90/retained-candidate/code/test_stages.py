import unittest,tempfile,json,copy,struct
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import stages,stage_carrier,backend,sole_service,connected,wire,runtime
from anchor import *
from test_connected import config,intent
from test_wire import KEY,EXEC_KEY,SERVER,PUBLIC
SEED=bytes.fromhex(sha(b'LAB-STAGE-NEAR-KEY'))
class Fixture:
 def __init__(self,path,method='signPetition',create=True,limits=None):
  self.p=Path(path);self.method=method;self.c=config();self.u='LAB-U-1'
  self.pre={k:self.c['prerequisites'][v] for k,v in [('model','model'),('profile','profile'),('config','configuration')]};self.pre['staging_required']=True
  principals={'executor':(EXEC_KEY,['executor']),'fixture':(KEY,['executor','lab-result-provider'])}
  self.pre['ingress_policy']=wire.policy_binding(principals,PUBLIC)
  self.cfg={'pilot':'LAB-C5','session':'ONE','implementation':connected.implementation(runtime.Guard(),self.pre),'backend':{'kind':'SIMULATED','table_id':'C5-LAB','service_identity':'C5-LAB'},'origin':'0'*64,'limits':limits or {'attempt':2070,'query':3110,'snapshot':130,'staging_query':2086,'staging_snapshot':85}}
  self.b=backend.SimulatedBackend(self.p/'service.db',self.cfg['backend']);self.s=sole_service.Service(self.b,self.cfg,self.pre)
  if create:self.s.genesis({'executor_head':'0'*64,'transport_head':'0'*64,'transport_seq':0})
  self.ing=wire.Ingress(self.s,self.pre,principals,SERVER);self.ch=wire.OfflineChannel(self.ing);self.client=wire.Client(self.ch,self.cfg,'fixture',KEY,PUBLIC,self.p/'wire.db',create,policy=self.ing.policy)
  self.x=connected.Connected(self.p/'local',self.client,self.pre,create);self.sch=stages.Scheduler(self.x);self.sink=connected.OfflineSink();self.nonce=1
 def close(self):self.x.close();self.client.close();self.b.close()
 def start(self,auth_len=None):
  self.i=intent(self.c,method=self.method)
  if auth_len is not None:
   self.i['arguments']['authData']='ab'*auth_len;self.i['calldata_hex']=runtime.executor.abi_encode(self.method,self.i['arguments']).hex()
  self.x.retire(self.u,self.i,'retire')
  s=self.s.fresh();c={k:'a'*64 for k in stage_carrier.HASH_FIELDS};c.update({k:'b'*40 for k in stage_carrier.ADDRESS_FIELDS})
  c.update(pilot=self.cfg['pilot'],engine='aurora',issuer='LAB',decoder='LAB',network=self.i['chain'],epoch='0',expiry='9999999999',method=self.method,phase='PRE-COMMITMENT',registry=self.i['registry'],executor=self.i['executor'],configuration=self.i['config'],model=self.i['model'],profile=self.i['profile'],contract=self.i['contract'],u=runtime.executor.u_wire(self.u),inputs=sha(bytes.fromhex(self.i['calldata_hex'])),history_prefix=s['head'],public_key_hash=sha(b'K'*32))
  self.msg=stage_carrier.DOMAIN+enc({'format':'I164-A-STAGED-AUTHORIZED-INPUTS-2','bindings':c,'authorized_values':['']*(15 if self.method=='signPetition' else 19)})
  self.sch.open(self.u,self.msg,b'K'*32,b'S'*64)
 def prepare(self):
  s,st=self.sch.state(self.u);msg=self.client.blob(st['message'],MAX_INTENT);meta=parse(self.client.blob(st['meta'],MAX_INTENT),MAX_INTENT);cmd=stages.command(meta,msg,st['index']);raw=stages.envelope(st,dict(cmd,calldata_hex=stages.calldata(meta,st['sid'],cmd).hex()))
  spec={'network':'near-testnet','engine':'aurora','method':'submit','signer':'lab.testnet','public_key':wire.public(SEED).hex(),'nonce':self.nonce,'block_hash':'b'*64,'gas':10**15,'deposit':0};self.nonce+=1
  unsigned=runtime.retained.t.unsigned(spec,raw);near=unsigned+b'\0'+Ed25519PrivateKey.from_private_bytes(SEED).sign(bytes.fromhex(sha(unsigned)))
  self.sch.prepare(self.u,spec,near)
 def evidence(self,s,st,out='SUCCESS'):
  p=st['pending'];msg=self.s.blob(st['message'],MAX_INTENT);meta=parse(self.s.blob(st['meta'],MAX_INTENT),MAX_INTENT)
  body={'format':'LAB-STAGE-OUTCOME-1','pilot':st['pilot'],'session':st['session'],'sid':st['sid'],'u':st['u'],'intent':st['intent'],'message':st['message'],'command':stages.command(meta,msg,st['index']),'prepared_head':p['prepared_head'],'near_sha256':p['near'],'transaction_id':p['txid'],'query':p['query'],'outcome':out,'authenticity':'SIMULATED-NOT-GENUINE-C4'}
  if body['command']['kind']=='cleanup' and out=='SUCCESS':
   from lab_evm import keccak
   # Explicit synthetic execution bytes for transport-only tests, not actual EVM evidence.
   topics=[keccak(b'Cleaned(bytes32,bytes32,uint8,bytes32,bytes32)'),bytes.fromhex(st['sid']),bytes.fromhex(meta['bindings']['u'])]
   data=(2).to_bytes(32,'big')+bytes.fromhex(meta['bindings']['inputs']+meta['message_sha256'])
   raw=b'\x07\x00'+(32).to_bytes(4,'little')+(1).to_bytes(32,'big')+(100000).to_bytes(8,'little')+(1).to_bytes(4,'little')+bytes.fromhex(meta['bindings']['auth_manager'])+(3).to_bytes(4,'little')+b''.join(topics)+len(data).to_bytes(4,'little')+data
   body['cleanup_result']=raw.hex()
  return body
 def step(self):self.prepare();self.sch.send(self.u,self.sink);self.sch.observe_lab(self.u,self.evidence)
class Tests(unittest.TestCase):
 def setUp(self):self.t=tempfile.TemporaryDirectory();self.f=Fixture(self.t.name)
 def tearDown(self):self.f.close();self.t.cleanup()
 def test_complete_both_paths(self):
  for method in ['signPetition','signPetitionWithZKProof']:
   with tempfile.TemporaryDirectory() as d:
    f=Fixture(d,method);f.start()
    with self.assertRaises(ValueError):f.x.seal_conditional(f.u,'early')
    while f.s.fresh()['u'][f.u]['stage']['status']=='READY':f.step()
    self.assertEqual(f.s.fresh()['u'][f.u]['stage']['status'],'AUTHENTICATED-CONDITIONAL')
    # Existing conditional comparison capsule is still required by SEAL.
    f.x.seal_conditional(f.u,'seal');f.x.submit_conditional(f.u,'signing',f.sink)
    f.x.save_conditional_observation(f.u,'sign-result','SUCCESS');before=connected.copy_counts(f.s.fresh());f.x.internal_terminal_repair();f.x.internal_terminal_repair();self.assertEqual(before,connected.copy_counts(f.s.fresh()))
    f.sch.advance(f.u,'STAGE_CLEANUP_READY');f.step();self.assertEqual(f.s.fresh()['u'][f.u]['stage']['status'],'COMPLETE')
    with self.assertRaises(ValueError):f.sch.operational()
    with self.assertRaises(ValueError):f.x.submit_conditional(f.u,'second',f.sink)
    f.close()
 def test_ack_loss_and_identical_retry(self):
  f=self.f;f.start();f.prepare();before=f.s.fresh()['counts']['attempt']
  def drop(q,r):
   if parse(q,wire.REQUEST_LIMIT)['request']['args'].get('kind')=='STAGE_ATTEMPT':raise OSError('lost')
   return r
  f.ch.filter=drop
  with self.assertRaises(Uncertain):f.sch.send(f.u,f.sink)
  f.ch.filter=None;self.assertEqual(len(f.sink.sent),0);self.assertEqual(f.s.fresh()['counts']['attempt'],before+1)
  f.sch.recover(f.u)
  with self.assertRaises(ValueError):f.sch.send(f.u,f.sink)
  f.sch.send(f.u,f.sink,retry=True);self.assertEqual(f.s.fresh()['counts']['attempt'],before+2)
  f.sch.observe_lab(f.u,f.evidence)
 def test_crash_reopen_no_release(self):
  f=self.f;f.start();f.prepare()
  with self.assertRaises(Uncertain):f.sch.send(f.u,f.sink,crash=True)
  st=f.s.fresh();f.close();self.f=Fixture(self.t.name,create=False);g=self.f;self.assertEqual(g.sch.recover(g.u),st['u'][g.u]['stage'])
  g.sch.recover(g.u);self.assertEqual(g.s.fresh()['counts'],st['counts']);self.assertEqual(len(g.sink.sent),0)
 def test_result_substitutions(self):
  f=self.f;f.start();f.prepare();f.sch.send(f.u,f.sink);f.sch.advance(f.u,'STAGE_QUERY');s,st=f.sch.state(f.u);good=f.evidence(s,st)
  for k in ['pilot','session','sid','u','intent','message','command','prepared_head','near_sha256','transaction_id','query']:
   bad=copy.deepcopy(good);bad[k]='wrong'
   with self.assertRaises(ValueError):f.sch.advance(f.u,'STAGE_RESULT',bad)
  f.sch.advance(f.u,'STAGE_RESULT',good)
  with self.assertRaises(ValueError):f.sch.advance(f.u,'STAGE_RESULT',good)
 def test_wrong_command_predecessor_nonce(self):
  f=self.f;f.start();f.prepare();s=f.s.fresh();p=s['u'][f.u]['stage']['pending'];body=parse(f.s.blob(p['ref'],MAX_INTENT),MAX_INTENT)
  with self.assertRaises(ValueError):f.sch.advance(f.u,'STAGE_PREPARE',body)
  f.sch.send(f.u,f.sink);f.sch.observe_lab(f.u,f.evidence)
  for key in ['command','previous']:
   bad=copy.deepcopy(body);bad[key]='wrong'
   with self.assertRaises(ValueError):f.sch.advance(f.u,'STAGE_PREPARE',bad)
  f.nonce=1
  with self.assertRaises(ValueError):f.prepare()
 def test_unavailable_and_revert(self):
  f=self.f;f.start();f.prepare();f.sch.send(f.u,f.sink);f.sch.observe_lab(f.u,lambda s,st:f.evidence(s,st,'UNAVAILABLE'))
  self.assertEqual(f.sch.recover(f.u)['status'],'UNCERTAIN')
  with self.assertRaises(ValueError):f.prepare()
  with self.assertRaises(ValueError):f.x.seal_conditional(f.u,'bad')
 def test_capacity(self):
  a=stages.capacity(41972,'signPetition');self.assertEqual(a['appends'],82);self.assertEqual(a['attempts_with_shared_retries'],102);self.assertLess(a['events_reserved'],12000)
  self.assertEqual(stages.capacity(21376,'signPetitionWithZKProof')['appends'],42)
  for n in [True,41973,0]:
   with self.assertRaises(ValueError):stages.capacity(n,'signPetition')
 def test_backup_precharge_failure(self):
  f=self.f;f.start();b=f.s.fresh()['counts']['snapshot']
  with self.assertRaises(RuntimeError):f.sch.backup(f.u,lambda:(_ for _ in ()).throw(RuntimeError('interruption')))
  self.assertEqual(f.s.fresh()['counts']['snapshot'],b+1)
 def test_no_new_session_and_identity(self):
  f=self.f;f.start()
  with self.assertRaises(ValueError):f.sch.open(f.u,f.msg,b'K'*32,b'S'*64)
  self.assertEqual(len(f.s.fresh()['u']),1)
  f.pre['config']='f'*64
  # Connected owns a canonical copy; caller mutation does not change bindings.
  self.assertNotEqual(f.x.prerequisites['config'],f.pre['config'])
 def test_exhaustion_before_send(self):
  f=self.f;f.start();f.prepare();f.sch.send(f.u,f.sink)
  for _ in range(16):f.sch.send(f.u,f.sink,retry=True)
  before=f.s.fresh()['counts']
  with self.assertRaises(ValueError):f.sch.send(f.u,f.sink,retry=True)
  self.assertEqual(f.s.fresh()['counts'],before);self.assertEqual(len(f.sink.sent),17)
 def test_query_and_backup_partition_exhaustion(self):
  for which in ['query','snapshot']:
   with tempfile.TemporaryDirectory() as d:
    lim={'attempt':2070,'query':3110,'snapshot':130,'staging_query':2086,'staging_snapshot':1}
    f=Fixture(d,limits=lim);f.start()
    if which=='snapshot':
     calls=[];f.sch.backup(f.u,lambda:calls.append(1))
     with self.assertRaises(ValueError):f.sch.backup(f.u,lambda:calls.append(2))
     self.assertEqual(calls,[1])
    else:
     # Capacity refusal is before opening, with insufficient adopted partition.
     f.close()
     with tempfile.TemporaryDirectory() as dd:
      lim['staging_query']=1;g=Fixture(dd,limits=lim)
      with self.assertRaises(ValueError):g.start()
      self.assertIsNone(g.s.fresh()['u'][g.u].get('stage'));self.assertEqual(g.s.fresh()['counts']['attempt'],0);g.close()
     continue
    f.close()
 def test_concurrent_service_head(self):
  import threading
  f=self.f;f.start();f.prepare();f.sch.send(f.u,f.sink);head=f.s.fresh()['head'];barrier=threading.Barrier(2);results=[]
  def run(n):
   b=backend.SimulatedBackend(f.p/'service.db',f.cfg['backend']);sv=sole_service.Service(b,f.cfg,f.pre)
   try:
    barrier.wait();sv.commit(head,'race-'+str(n),'STAGE_QUERY',f.u,{});results.append('committed')
   except (ValueError,Uncertain):results.append('blocked')
   finally:b.close()
  ts=[threading.Thread(target=run,args=(i,)) for i in range(2)]
  for t in ts:t.start()
  for t in ts:t.join()
  self.assertEqual(sorted(results),['blocked','committed']);self.assertEqual(f.s.fresh()['counts']['query'],1)
 def test_unavailable_then_bound_result_and_revert(self):
  f=self.f;f.start();f.prepare();f.sch.send(f.u,f.sink);f.sch.observe_lab(f.u,lambda s,st:f.evidence(s,st,'UNAVAILABLE'))
  f.sch.observe_lab(f.u,lambda s,st:f.evidence(s,st,'REVERTED'));self.assertEqual(f.sch.recover(f.u)['status'],'FAILED')
  with self.assertRaises(ValueError):f.sch.send(f.u,f.sink,retry=True)
 def test_wrong_open_bindings_and_changed_message(self):
  f=self.f;f.start();m=stage_carrier.decode(f.msg[len(stage_carrier.DOMAIN):])
  for key in ['pilot','method','configuration','model','u','inputs','history_prefix']:
   x=copy.deepcopy(m);x['bindings'][key]='wrong';raw=stage_carrier.DOMAIN+enc(x)
   with self.assertRaises(ValueError):f.sch.open(f.u,raw,b'K'*32,b'S'*64)
 def test_actual_cleanup_abi(self):
  self.assertEqual(stages.calldata({},'a'*64,{'kind':'cleanup'}),bytes.fromhex('f474fb90'+'a'*64))
 def test_changed_config_reopen(self):
  f=self.f;f.start();old=f.s.fresh();f.x.prerequisites['config']='f'*64
  with self.assertRaises(ValueError):f.sch.recover(f.u)
  self.assertEqual(f.s.fresh(),old)

 def test_duplicate_attempt_receipt_no_second_release(self):
  f=self.f;f.start();f.prepare();state=f.s.fresh();head=state['head'];body={'release':stages.release_binding(state,state['u'][f.u]['stage'],'STAGE_ATTEMPT')};r=f.client.commit(head,'fixed-attempt','STAGE_ATTEMPT',f.u,body)
  self.assertTrue(r['release']);r2=f.client.commit(head,'fixed-attempt','STAGE_ATTEMPT',f.u,body)
  self.assertFalse(r2['release']);self.assertTrue(r2['duplicate']);self.assertEqual(f.s.fresh()['counts']['attempt'],1)
 def test_unavailable_ingress_no_fallback(self):
  f=self.f;f.start();f.prepare();f.ch.available=False
  with self.assertRaises(Uncertain):f.sch.send(f.u,f.sink)
  self.assertEqual(f.s.fresh()['counts']['attempt'],0);self.assertFalse(f.sink.sent)

 def test_authdata_restriction_before_staging(self):
  for n in [4096,4097]:
   with tempfile.TemporaryDirectory() as d:
    f=Fixture(d)
    if n==4096:f.start(auth_len=n);self.assertIsNotNone(f.s.fresh()['u'][f.u].get('stage'))
    else:
     with self.assertRaises(ValueError):f.start(auth_len=n)
     self.assertEqual(f.s.fresh()['u'][f.u]['record']['status'],'RETIRED');self.assertIsNone(f.s.fresh()['u'][f.u].get('stage'));self.assertEqual(f.s.fresh()['counts']['attempt'],0)
    f.close()

if __name__=='__main__':unittest.main(verbosity=2)
