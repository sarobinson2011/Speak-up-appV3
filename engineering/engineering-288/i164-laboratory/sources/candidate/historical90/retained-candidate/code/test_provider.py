"""Independent laboratory signing path; qualifications/capability are ASSUMED.
No fixture is an appointment or observation from an actual provider/network.
"""
import unittest,tempfile,copy,json
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import runtime,backend,sole_service,connected,wire,outcome,provider
from anchor import *
from test_connected import config,intent
from test_wire import KEY,EXEC_KEY,SERVER,PUBLIC
from test_outcome import Fixture as OldFixture,PUB
SEEDS={role:bytes.fromhex(sha(('public-LAB-C4-'+role).encode())) for role in ['authority','qualifier','provider','assessor']}
def signed(role,kind,c):return {'claim':c,'signature':Ed25519PrivateKey.from_private_bytes(SEEDS[role]).sign(provider.signed_bytes(kind,c)).hex()}
BASIS_BYTES={k:('LAB-ONLY-ASSUMED-'+k).encode() for k in ['rule_sha256','trust_anchor_sha256','checkpoint_sha256']}
def policy(c,missing=None):
 d={'network':'near-testnet','genesis_sha256':sha(b'LAB-genesis'),'engine':'aurora','engine_code_sha256':sha(b'LAB-engine-code'),'protocol':87,'method':'submit'}
 g={k:c['prerequisites'][k] for k in ['model','profile','configuration']}
 p={'format':'LAB-ASSUMPTIONS-NOT-OPERATIONAL-1','domain':d,'governing':g,'authority_key':wire.public(SEEDS['authority']).hex(),'qualification_key':wire.public(SEEDS['qualifier']).hex(),'finality_basis':{k:sha(v) for k,v in BASIS_BYTES.items()}}
 for role in ['provider','assessor']:
  key=wire.public(SEEDS[role]).hex();name='LAB-'+role
  a=signed('authority','appointment',{'subject':name,'key':key,'role':role,'domain':d,'governing':g,'rule':provider.RULE,'finality_basis':p['finality_basis'],'assertion_scope':'OUTCOME-SOURCE' if role=='provider' else 'FINALITY-ASSESSMENT','laboratory_assumption':True})
  q=signed('qualifier','qualification',{'appointment_sha256':sha(enc(a)),'subject':name,'role':role,'domain':d,'governing':g,'competence_contract':provider.RULE,'finality_basis':p['finality_basis'],'status':'ASSUMED-FOR-LAB-ONLY'})
  p[role]={'id':name,'key':key,'appointment':a,'qualification':q if missing!=role else None}
 return p
class Fixture(OldFixture):
 def __init__(self,path,create=True,missing=None):
  self.p=Path(path);self.p.mkdir(parents=True,exist_ok=True);self.c=config();self.pre={k:self.c['prerequisites'][v] for k,v in [('model','model'),('profile','profile'),('config','configuration')]}
  principals={'executor':(EXEC_KEY,['executor']),'fixture':(KEY,['executor','lab-result-provider'])}
  self.policy=policy(self.c,missing)
  self.pre.update(ingress_policy=wire.policy_binding(principals,PUBLIC),outcome_lab_public_key=PUB.hex(),outcome_provider_policy=self.policy)
  self.desc={'kind':'SIMULATED','service_identity':'LAB-C4-AUTH-SERVICE','table_id':'LAB-C4-AUTH-TABLE'}
  self.cfg={'pilot':'LAB-C4-AUTH','session':'ONE','implementation':connected.implementation(runtime.Guard(),self.pre),'backend':self.desc,'origin':'0'*64,'limits':{'attempt':2,'query':1,'snapshot':2,'staging_query':1,'staging_snapshot':2}}
  self.b=backend.SimulatedBackend(self.p/'service.db',self.desc);self.s=sole_service.Service(self.b,self.cfg,self.pre)
  if create:self.s.genesis({'executor_head':'0'*64,'transport_head':'0'*64,'transport_seq':0})
  self.ing=wire.Ingress(self.s,self.pre,principals,SERVER);self.ch=wire.OfflineChannel(self.ing);self.client=wire.Client(self.ch,self.cfg,'fixture',KEY,PUBLIC,self.p/'wire.db',create,policy=self.ing.policy);self.x=connected.Connected(self.p/'local',self.client,self.pre,create);self.u='LAB-U-1';self.sink=connected.OfflineSink()
 def packet(self,tag=0,near_failure=False):
  src=super().packet(tag,near_failure)['claim'];src['format']='C4-SAVED-NEAR-SUBMIT-1'
  inv=provider.invocation(src,self.policy['domain'],self.policy['finality_basis']);artifact=b'LAB-ONLY: assumed completed qualified assessment; not a NEAR proof';ref=sha(artifact)
  trace=[{'obligation':o,'invocation_sha256':sha(enc(inv)),'evidence_refs':[ref]+list(self.policy['finality_basis'].values()),'status':'VALID'} for o in provider.OBLIGATIONS]
  a={'assessor':self.policy['assessor']['id'],'appointment':sha(enc(self.policy['assessor']['appointment'])),'qualification':sha(enc(self.policy['assessor']['qualification'])) if self.policy['assessor']['qualification'] else None,'invocation':inv,'trace':trace,'result':{'status':'VALID','invocation_sha256':sha(enc(inv)),'trace_sha256':sha(enc(trace)),'finalized_blocks':sorted(set(x['block_hash'] for x in inv['outcomes']))}}
  assessment=signed('assessor','assessment',a)
  c={'provider':self.policy['provider']['id'],'appointment':sha(enc(self.policy['provider']['appointment'])),'qualification':sha(enc(self.policy['provider']['qualification'])) if self.policy['provider']['qualification'] else None,'domain':self.policy['domain'],'governing':self.policy['governing'],'source':src,'assessment_sha256':sha(enc(assessment))}
  return {'statement':signed('provider','outcome',c),'assessment':assessment,'artifacts':{ref:artifact.hex(),**{sha(v):v.hex() for v in BASIS_BYTES.values()}}}
 def decode(self,p):
  st=self.s.fresh();v=st['u'][self.u]
  return provider.validate(p,outcome.context(self.cfg,self.s.binding,v,self.u,'observe',1),self.s.blob(v['record']['tx_ref'],MAX_TRANSACTION),self.policy)
def resign(p):
 if p['assessment'] is not None:p['assessment']=signed('assessor','assessment',p['assessment']['claim'])
 p['statement']['claim']['assessment_sha256']=sha(enc(p['assessment'])) if p['assessment'] else None
 p['statement']=signed('provider','outcome',p['statement']['claim']);return p
class Tests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.f=Fixture(self.tmp.name);self.f.sent();self.p=self.f.packet()
 def tearDown(self):self.f.close();self.tmp.cleanup()
 def test_original_message_native_authentication(self):
  r=self.f.decode(self.p);self.assertTrue(r['provider_signature_verified']);self.assertFalse(r['authoritative_terminal']);self.assertEqual(r['conditional_terminal'],'SUCCESS')
  q=copy.deepcopy(self.p);q['statement']['claim']['provider']='changed'
  with self.assertRaises(Blocked):self.f.decode(q)
  with self.assertRaises(Blocked):provider.require_operational(r)
 def test_success_revert_repair_and_accounting(self):
  for tag in (0,1):
   with tempfile.TemporaryDirectory() as d:
    f=Fixture(d);f.sent();p=f.packet(tag);f.x.save_outcome_evidence(f.u,'observe',p);counts=connected.copy_counts(f.s.fresh());self.assertIsNone(f.x.internal_terminal_repair());self.assertIsNone(f.x.internal_terminal_repair());self.assertEqual(counts,connected.copy_counts(f.s.fresh()));self.assertEqual(f.x.executor.states[f.u]['status'],['SUCCESS','FAILED'][tag]);self.assertEqual(len(f.sink.sent),1)
    with self.assertRaises(ValueError):f.x.submit_conditional(f.u,'another',f.sink)
    f.close()
 def test_wrong_provider_domain_governing(self):
  for field in ['provider','appointment','qualification','domain','governing']:
   p=copy.deepcopy(self.p);p['statement']['claim'][field]='wrong';resign(p)
   with self.assertRaises(ValueError):self.f.decode(p)
 def test_wrong_source_receipts_network_transaction(self):
  for field in ['rpc_response_hex','near_hex','rpc_request_hex']:
   p=copy.deepcopy(self.p);p['statement']['claim']['source'][field]='00';resign(p)
   with self.assertRaises(ValueError):self.f.decode(p)
  for field in ['network','engine','nonce']:
   p=copy.deepcopy(self.p);p['statement']['claim']['source']['near_spec'][field]='wrong';resign(p)
   with self.assertRaises((ValueError,TypeError)):self.f.decode(p)
 def test_wrong_operation_intent_u_receipt_coordinates(self):
  for field in self.p['statement']['claim']['source']['context']:
   p=copy.deepcopy(self.p);p['statement']['claim']['source']['context'][field]='wrong';resign(p)
   with self.assertRaises(ValueError):self.f.decode(p)
 def test_missing_finality_keeps_uncertainty(self):
  p=copy.deepcopy(self.p);p['assessment']=None;p['artifacts']={};resign(p)
  self.assertIsNone(self.f.decode(p)['conditional_terminal']);self.f.x.save_outcome_evidence(self.f.u,'observe',p);counts=connected.copy_counts(self.f.s.fresh());self.f.x.internal_terminal_repair();self.assertEqual(self.f.x.executor.states[self.f.u]['status'],'UNCERTAIN');self.assertEqual(counts,connected.copy_counts(self.f.s.fresh()))
 def test_missing_qualifications_do_not_complete(self):
  for role in ['provider','assessor']:
   with tempfile.TemporaryDirectory() as d:
    f=Fixture(d,missing=role);f.sent();p=f.packet();self.assertIsNone(f.decode(p)['conditional_terminal']);f.x.save_outcome_evidence(f.u,'observe',p);f.x.internal_terminal_repair();self.assertEqual(f.x.executor.states[f.u]['status'],'UNCERTAIN');f.close()
 def test_conflicting_finality_and_incomplete_trace(self):
  for edit in [lambda a:a['result'].update(finalized_blocks=[]),lambda a:a['trace'][0].update(status='INVALID'),lambda a:a['trace'].pop(),lambda a:a['invocation'].update(source_sha256='0'*64),lambda a:a.update(assessor='other')]:
   p=copy.deepcopy(self.p);edit(p['assessment']['claim']);resign(p)
   with self.assertRaises(ValueError):self.f.decode(p)
 def test_invalid_unavailable_assessment(self):
  for status in ['INVALID','UNAVAILABLE']:
   p=copy.deepcopy(self.p);a=p['assessment']['claim'];a['trace'][0]['status']=status;a['result']['status']=status;a['result']['trace_sha256']=sha(enc(a['trace']));resign(p)
   self.assertIsNone(self.f.decode(p)['conditional_terminal'])
 def test_missing_altered_finality_artifact(self):
  for artifacts in [{},{next(iter(self.p['artifacts'])):'00'}]:
   p=copy.deepcopy(self.p);p['artifacts']=artifacts
   with self.assertRaises(ValueError):self.f.decode(p)
 def test_signatures_domains_and_scalar_bounds(self):
  for which in ['statement','assessment']:
   for signature in ['00'*64,self.p[which]['signature'][:64]+'ff'*32]:
    p=copy.deepcopy(self.p);p[which]['signature']=signature
    if which=='assessment':p['statement']['claim']['assessment_sha256']=sha(enc(p['assessment']));p['statement']=signed('provider','outcome',p['statement']['claim'])
    with self.assertRaises(ValueError):self.f.decode(p)
  p=copy.deepcopy(self.p);p['statement']=signed('provider','assessment',p['statement']['claim'])
  with self.assertRaises(ValueError):self.f.decode(p)
 def test_reopen_and_interrupted_repair(self):
  with self.assertRaises(Uncertain):self.f.x.save_outcome_evidence(self.f.u,'observe',self.p,crash='after_service')
  self.f.close();self.f=Fixture(self.tmp.name,False)
  with self.assertRaises(Uncertain):self.f.x.internal_terminal_repair(crash='after_service')
  self.f.close();self.f=Fixture(self.tmp.name,False);self.f.x.internal_terminal_repair();self.f.x.internal_terminal_repair();s=self.f.s.fresh();self.assertEqual(s['counts'],{'attempt':1,'query':1,'snapshot':0});self.assertEqual(self.f.x.executor.states[self.f.u]['status'],'SUCCESS')
 def test_old_executor_restore_and_same_u(self):
  with tempfile.TemporaryDirectory() as d:
   f=Fixture(d);old=(Path(d)/'local/executor.db').read_bytes();f.sent();f.x.save_outcome_evidence(f.u,'observe',f.packet());f.close();(Path(d)/'local/executor.db').write_bytes(old);f=Fixture(d,False);f.x.internal_terminal_repair()
   with self.assertRaises(ValueError):f.x.retire(f.u,intent(f.c,nonce=2),'different')
   self.assertEqual(f.s.fresh()['counts']['attempt'],1);f.close()
 def test_replay_substitution_corruption(self):
  self.f.x.save_outcome_evidence(self.f.u,'observe',self.p)
  with self.assertRaises(ValueError):self.f.x.save_outcome_evidence(self.f.u,'new-observation',self.p)
  v=self.f.s.fresh()['u'][self.f.u];self.f.b.db.execute('UPDATE objects SET v=? WHERE k=?',(b'bad','BLOB/'+v['saved']['ref']))
  with self.assertRaises(ValueError):self.f.x.internal_terminal_repair()
 def test_near_failure_remains_not_evm_revert(self):
  p=self.f.packet(near_failure=True);r=self.f.decode(p);self.assertEqual(r['evm_outcome'],'UNAVAILABLE');self.assertIsNone(r['conditional_terminal'])
 def test_legacy_bypass_and_changed_policy(self):
  with self.assertRaises((ValueError,KeyError)):self.f.x.save_outcome_evidence(self.f.u,'observe',OldFixture.packet(self.f))
  self.f.s.provider_policy=None
  with self.assertRaises(Uncertain):self.f.x.recover()
 def test_missing_appointment(self):
  p=copy.deepcopy(self.f.policy);p['provider']['appointment']=None
  with self.assertRaisesRegex(Blocked,'APPOINTMENT-UNAVAILABLE'):provider.validate_policy(p)
 def test_no_operational_loader(self):
  p=copy.deepcopy(self.f.policy);p['format']='OPERATIONAL'
  with self.assertRaises(ValueError):provider.validate_policy(p)
 def test_same_source_different_assessment_rejected(self):
  p=copy.deepcopy(self.p);p['assessment']['claim']['invocation']['context']['u']='OTHER';resign(p)
  with self.assertRaises(ValueError):self.f.decode(p)
class InteractionTests(unittest.TestCase):
 def test_ack_loss_recovery_and_no_second_submission(self):
  with tempfile.TemporaryDirectory() as d:
   f=Fixture(d);f.sent();p=f.packet()
   def lose_ack(packet,response):
    q=parse(packet,wire.REQUEST_LIMIT)['request']
    if q['method']=='commit' and q['args']['kind']=='OBSERVE_EVIDENCE':raise OSError('SIMULATED-ACK-LOSS-AFTER-COMMIT')
    return response
   f.ch.filter=lose_ack
   with self.assertRaises(Uncertain):f.x.save_outcome_evidence(f.u,'observe',p)
   f.close();f=Fixture(d,False);f.x.internal_terminal_repair();self.assertEqual(f.s.fresh()['counts']['query'],1)
   with self.assertRaises(ValueError):f.x.submit_conditional(f.u,'retry',f.sink)
   self.assertEqual(len(f.sink.sent),0);f.close()
 def test_concurrent_exact_response_same_request(self):
  import threading
  with tempfile.TemporaryDirectory() as d:
   f=Fixture(d);f.sent();p=f.packet();head=f.s.fresh()['head'];barrier=threading.Barrier(2);answers=[]
   def run():
    b=backend.SimulatedBackend(Path(d)/'service.db',f.desc);sv=sole_service.Service(b,f.cfg,f.pre)
    try:
     barrier.wait();x=sv.commit(head,'observe','OBSERVE_EVIDENCE',f.u,{'evidence':p});answers.append('duplicate' if x['duplicate'] else 'commit')
    except (Blocked,Uncertain):answers.append('retry-read-only')
    finally:b.close()
   ts=[threading.Thread(target=run) for _ in range(2)]
   for t in ts:t.start()
   for t in ts:t.join(10);self.assertFalse(t.is_alive())
   self.assertEqual(answers.count('commit'),1);self.assertEqual(len(answers),2);f.x.recover();f.x.internal_terminal_repair();self.assertEqual(f.s.fresh()['counts']['query'],1);f.close()
 def test_interrupted_verification_no_publication(self):
  with tempfile.TemporaryDirectory() as d:
   f=Fixture(d);f.sent();p=f.packet();bad=copy.deepcopy(p);bad['assessment']['signature']=bad['assessment']['signature'][:-2];resign(bad)
   # A truncated finality artifact stands for incomplete acquisition; signature
   # re-signing above is not allowed to fabricate a completed artifact.
   bad['artifacts'][next(iter(bad['artifacts']))]='00'
   with self.assertRaises(Blocked):f.x.save_outcome_evidence(f.u,'observe',bad)
   self.assertIsNone(f.s.fresh()['u'][f.u]['saved']);self.assertEqual(f.s.fresh()['counts']['query'],0)
   f.close();f=Fixture(d,False);f.x.save_outcome_evidence(f.u,'observe',p);f.x.internal_terminal_repair();self.assertEqual(f.s.fresh()['counts']['query'],1);f.close()
if __name__=='__main__':unittest.main()
