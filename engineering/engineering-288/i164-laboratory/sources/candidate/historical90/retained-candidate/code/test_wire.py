import unittest,tempfile,threading,copy,json
from pathlib import Path
import backend,sole_service,connected,runtime,wire
from test_connected import config,intent
from anchor import *
from connected import Connected,OfflineSink,implementation,copy_counts
from backend import SimulatedBackend
from sole_service import Service
from wire import Ingress,Client,OfflineChannel,tag
KEY=bytes.fromhex(sha(b'LAB-CALLER-NOT-SECRET'));SERVER=bytes.fromhex(sha(b'LAB-SERVICE-NOT-SECRET'));EXEC_KEY=bytes.fromhex(sha(b'LAB-EXECUTOR-NOT-SECRET'));PUBLIC=wire.public(SERVER)
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name);self.c=config();self.pre={k:self.c['prerequisites'][v] for k,v in [('model','model'),('profile','profile'),('config','configuration')]}
  self.pre['ingress_policy']=wire.policy_binding({'executor':(EXEC_KEY,['executor']),'fixture':(KEY,['executor','lab-result-provider'])},PUBLIC)
  self.desc={'kind':'SIMULATED','service_identity':'LAB-SERVICE','table_id':'LAB-TABLE'}
  self.cfg={'pilot':'LAB-WIRE','session':'ONE','implementation':implementation(runtime.Guard(),self.pre),'backend':self.desc,'origin':'0'*64,'limits':{'attempt':2,'query':1,'snapshot':2,'staging_query':1,'staging_snapshot':2}}
  self.b=SimulatedBackend(self.p/'service.db',self.desc);self.s=Service(self.b,self.cfg);self.s.genesis({'executor_head':'0'*64,'transport_head':'0'*64,'transport_seq':0})
  self.ingress=Ingress(self.s,self.pre,{'executor':(EXEC_KEY,['executor']),'fixture':(KEY,['executor','lab-result-provider'])},SERVER)
  self.channel=OfflineChannel(self.ingress);self.client=Client(self.channel,self.cfg,'fixture',KEY,PUBLIC,self.p/'wire.db',True,policy=self.ingress.policy)
  self.x=Connected(self.p/'local',self.client,self.pre,True);self.u='LAB-U-1';self.i=intent(self.c);self.sink=OfflineSink();self.old=(self.p/'local/executor.db').read_bytes()
 def tearDown(self):self.x.close();self.client.close();self.b.close();self.tmp.cleanup()
 def retire(self):return self.x.retire(self.u,self.i,'r')
 def sent(self):self.retire();self.x.seal_conditional(self.u,'seal');self.x.submit_conditional(self.u,'attempt',self.sink)
 def resign(self,q):return enc({'request':q,'mac':tag(EXEC_KEY if q['principal']=='executor' else KEY,enc(q))})
 def request(self,method,args,principal='fixture'):
  return {'policy_sha256':sha(enc(self.ingress.policy)),'format':wire.FORMAT,'service':'LAB-SERVICE','binding':self.s.binding,'pilot':'LAB-WIRE','session':'ONE','principal':principal,'challenge':'a'*64,'method':method,'args':args}
 def test_connected_positive_c1(self):
  self.sent();self.x.save_conditional_observation(self.u,'obs','REVERTED');before=copy_counts(self.s.fresh())
  self.assertIsNone(self.x.internal_terminal_repair());self.assertIsNone(self.x.internal_terminal_repair())
  self.assertEqual(copy_counts(self.s.fresh()),before);self.assertEqual(len(self.sink.sent),1);self.assertEqual(self.x.executor.states[self.u]['status'],'FAILED')
  with self.assertRaises(ValueError):self.x.submit_conditional(self.u,'again',self.sink)
 def test_unauthorized_and_trusted_assertion(self):
  for principal in ['intruder','fixture']:
   q=self.request('head',{},principal)
   if principal=='fixture':q['trusted']=True
   with self.assertRaises(ValueError):self.ingress.handle(self.resign(q))
  q=self.request('head',{});p=json.loads(self.resign(q));p['mac']='0'*64
  with self.assertRaises(ValueError):self.ingress.handle(enc(p))
  self.assertEqual(self.s.fresh()['seq'],0)
 def test_ingress_chain_and_prerequisites(self):
  for field in ['chain','model','profile','config']:
   i=dict(self.i);i[field]='1' if field=='chain' else 'f'*64
   q=self.request('commit',{'expected':self.s.fresh()['head'],'op':field,'kind':'RETIRE','u':self.u,'body':{'intent_hex':runtime.executor.enc(i).hex()}})
   result=parse(self.ingress.handle(self.resign(q)),wire.RESPONSE_LIMIT)['response'];self.assertEqual(result['status'],'REJECTED')
  self.assertEqual(self.s.fresh()['seq'],0)
 def test_no_admin_or_public_observation(self):
  for method in ['genesis','restore','apply','status','backup','raw-write']:
   with self.assertRaises(ValueError):self.ingress.handle(self.resign(self.request(method,{})))
 def test_result_role(self):
  self.sent();q=self.request('commit',{'expected':self.s.fresh()['head'],'op':'obs','kind':'OBSERVE','u':self.u,'body':{}},'executor')
  with self.assertRaises(ValueError):self.ingress.handle(self.resign(q))
  self.assertEqual(self.s.fresh()['counts']['query'],0)
 def test_request_context_and_alteration(self):
  for field in ['service','binding','pilot','session']:
   q=self.request('head',{});q[field]='wrong'
   with self.assertRaises(ValueError):self.ingress.handle(self.resign(q))
  q=self.request('head',{});packet=json.loads(self.resign(q));packet['request']['method']='resolve'
  with self.assertRaises(ValueError):self.ingress.handle(enc(packet))
 def test_response_substitution_and_replay(self):
  saved=[]
  def capture(req,res):saved.append(res);return res
  self.channel.filter=capture;self.client.fresh()
  self.channel.filter=lambda req,res:saved[0]
  with self.assertRaises(ValueError):self.client.fresh()
  self.channel.filter=lambda req,res:res[:-3]+b'XXX'
  with self.assertRaises(ValueError):self.client.fresh()
 def test_authenticated_wrong_receipt(self):
  # Lab service-key possession is a harness fault, not an attacker capability.
  def wrong(req,res):
   p=parse(res,wire.RESPONSE_LIMIT);r=p['response']
   if r['status']=='OK' and 'result' in r['data']:
    r['data']['result']['receipt']['request']['u']='OTHER'
    p['signature']=wire.signature(SERVER,r)
   return enc(p)
  self.channel.filter=wrong
  with self.assertRaises(ValueError):self.retire()
  self.channel.filter=None;self.x.recover();self.assertIn(self.u,self.s.fresh()['u'])
 def test_wrong_head_and_duplicate_delivery(self):
  head=self.s.fresh()['head'];body={'intent_hex':runtime.executor.enc(self.i).hex()}
  one=self.client.commit(head,'r','RETIRE',self.u,body)
  two=self.client.commit(head,'r','RETIRE',self.u,body)
  self.assertEqual(one['receipt'],two['receipt']);self.assertFalse(two['release'])
  with self.assertRaises(ValueError):self.client.commit(head,'different','RETIRE','other',body)
  self.assertEqual(len(self.s.fresh()['u']),1)
 def test_ack_loss_restart_and_rollback(self):
  self.retire();self.x.seal_conditional(self.u,'seal')
  def drop_commit(req,res):
   if parse(req,wire.REQUEST_LIMIT)['request']['method']=='commit':raise OSError('ack lost')
   return res
  self.channel.filter=drop_commit
  with self.assertRaises(Uncertain):self.x.submit_conditional(self.u,'attempt',self.sink)
  self.channel.filter=None;self.x.close();self.client.close();(self.p/'local/executor.db').write_bytes(self.old)
  self.client=Client(self.channel,self.cfg,'fixture',KEY,PUBLIC,self.p/'wire.db',policy=self.ingress.policy);self.x=Connected(self.p/'local',self.client,self.pre)
  self.x.recover();self.x.recover()
  with self.assertRaises(ValueError):self.x.submit_conditional(self.u,'again',self.sink)
  self.assertEqual(self.sink.sent,[]);self.assertEqual(self.s.fresh()['counts']['attempt'],1)
 def test_unavailable_ingress(self):
  self.retire();self.channel.available=False
  with self.assertRaises(Uncertain):self.x.recover()
  self.channel.available=True;self.x.recover();self.assertEqual(len(self.s.fresh()['u']),1)
 def test_canonical_and_bounds(self):
  raw=self.resign(self.request('head',{}))
  for b in [raw+b' ',raw[:-1],b'{"request":{},"request":{},"mac":""}\n',b' '*600001]:
   with self.assertRaises(ValueError):self.ingress.handle(b)
 def test_concurrent_wire_clients(self):
  head=self.s.fresh()['head'];barrier=threading.Barrier(2);results=[]
  def run(n):
   b=SimulatedBackend(self.p/'service.db',self.desc);s=Service(b,self.cfg);ing=Ingress(s,self.pre,{'executor':(EXEC_KEY,['executor']),'fixture':(KEY,['executor','lab-result-provider'])},SERVER)
   c=Client(OfflineChannel(ing),self.cfg,'fixture',KEY,PUBLIC,self.p/('wire'+str(n)+'.db'),True,policy=ing.policy)
   try:
    barrier.wait();c.commit(head,'r'+str(n),'RETIRE',self.u,{'intent_hex':runtime.executor.enc(dict(self.i,nonce=str(n+1))).hex()});results.append('commit')
   except (ValueError,Uncertain):results.append('blocked')
   finally:c.close();b.close()
  ts=[threading.Thread(target=run,args=(n,)) for n in range(2)]
  for t in ts:t.start()
  for t in ts:t.join(15)
  self.assertEqual(sorted(results),['blocked','commit']);self.x.recover()
 def test_cross_session_wire_journal(self):
  self.client.close()
  with self.assertRaises(ValueError):Client(self.channel,dict(self.cfg,session='OTHER'),'fixture',KEY,PUBLIC,self.p/'wire.db',policy=self.ingress.policy)
 def test_replayed_resolve_cannot_release(self):
  self.sent();d=self.client.resolve('attempt');self.assertFalse(d['release']);self.assertEqual(d['receipt']['request']['u'],self.u)
  for _ in range(2):self.assertFalse(self.client.resolve('attempt')['release'])
  self.assertEqual(self.s.fresh()['counts']['attempt'],1)
 def test_duplicate_attempt_never_releases(self):
  self.sent();r=self.client.resolve('attempt')['receipt'];q=r['request']
  for _ in range(3):
   v=self.client.commit(q['expected'],q['op'],q['kind'],q['u'],{})
   self.assertFalse(v['release']);self.assertTrue(v['duplicate'])
  self.assertEqual(len(self.sink.sent),1);self.assertEqual(self.s.fresh()['counts']['attempt'],1)
 def test_exhausted_observation_and_internal_repair(self):
  self.sent();self.x.save_conditional_observation(self.u,'obs','SUCCESS')
  u='U2';self.x.retire(u,intent(self.c,u,nonce=2),'r2');self.x.seal_conditional(u,'s2');self.x.submit_conditional(u,'a2',self.sink)
  with self.assertRaises(ValueError):self.x.save_conditional_observation(u,'obs2','SUCCESS')
  self.assertIsNone(self.s.fresh()['u'][u]['saved'])
  # Rejected dispatch freezes later advances; repair may not bypass that condition.
  self.assertEqual(self.s.fresh()['counts']['query'],1)
 def test_signed_cross_session_response(self):
  def wrong(req,res):
   p=parse(res,wire.RESPONSE_LIMIT);p['response']['session']='OTHER';p['signature']=wire.signature(SERVER,p['response']);return enc(p)
  self.channel.filter=wrong
  with self.assertRaises(ValueError):self.client.fresh()
 def test_executor_cannot_impersonate_provider(self):
  q=self.request('head',{});p={'request':q,'mac':tag(EXEC_KEY,enc(q))}
  with self.assertRaises(ValueError):self.ingress.handle(enc(p))
 def test_policy_replacement_blocks_open_session(self):
  self.ingress.principals['fixture']=(KEY,frozenset(['executor']))
  with self.assertRaises(Uncertain):self.client.fresh()
  self.assertEqual(self.s.fresh()['seq'],0)
 def test_caller_policy_claim_rejected(self):
  q=self.request('head',{});q['policy_sha256']='f'*64
  with self.assertRaises(ValueError):self.ingress.handle(self.resign(q))
 def test_changed_role_policy_cannot_reopen_service(self):
  with self.assertRaises(ValueError):Ingress(self.s,self.pre,{'fixture':(KEY,['executor'])},SERVER)
if __name__=='__main__':unittest.main()
