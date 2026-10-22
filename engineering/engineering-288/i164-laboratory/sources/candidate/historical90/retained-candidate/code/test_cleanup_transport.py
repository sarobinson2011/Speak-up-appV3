"""Narrow connected transport checks. LAB provider and storage guarantees only."""
import tempfile,unittest,copy
from test_stages import Fixture
import connected,stages
class CleanupTests(unittest.TestCase):
 def ready(self,f):
  f.start()
  while f.s.fresh()['u'][f.u]['stage']['status']=='READY':f.step()
  f.x.seal_conditional(f.u,'seal');f.x.submit_conditional(f.u,'sign',f.sink)
  f.x.save_conditional_observation(f.u,'observation','SUCCESS');f.x.internal_terminal_repair()
  f.sch.advance(f.u,'STAGE_CLEANUP_READY');f.prepare()
 def test_bound_outcome_and_interruption(self):
  with tempfile.TemporaryDirectory() as p:
   f=Fixture(p);self.ready(f);before=f.s.fresh()['counts'].copy()
   with self.assertRaises(Exception):f.sch.send(f.u,f.sink,crash=True)
   state=f.s.fresh();f.close();f=Fixture(p,create=False)
   self.assertEqual(f.sch.recover(f.u),state['u'][f.u]['stage']);self.assertEqual(f.s.fresh()['counts'],state['counts'])
   with self.assertRaises(Exception):f.sch.send(f.u,f.sink)
   f.sch.advance(f.u,'STAGE_QUERY');s,st=f.sch.state(f.u);body=f.evidence(s,st)
   bad=copy.deepcopy(body);del bad['cleanup_result']
   with self.assertRaises(Exception):f.sch.advance(f.u,'STAGE_RESULT',bad)
   for at in [10,80,len(body['cleanup_result'])-5]:
    bad=copy.deepcopy(body);raw=bytearray.fromhex(bad['cleanup_result']);raw[min(at,len(raw)-1)]^=1;bad['cleanup_result']=raw.hex()
    with self.assertRaises(Exception):f.sch.advance(f.u,'STAGE_RESULT',bad)
   f.sch.advance(f.u,'STAGE_RESULT',body);c=f.s.fresh()['counts'];self.assertEqual(c['attempt'],before['attempt']+1);self.assertEqual(c['query'],before['query']+1)
   self.assertEqual(f.sch.recover(f.u)['status'],'COMPLETE');self.assertEqual(f.s.fresh()['counts'],c)
   with self.assertRaises(Exception):f.prepare()
   with self.assertRaises(Exception):f.x.submit_conditional(f.u,'another',f.sink)
   with self.assertRaises(Exception):f.sch.operational()
   f.close()
 def test_failure_does_not_report_cleanup(self):
  with tempfile.TemporaryDirectory() as p:
   f=Fixture(p);self.ready(f);f.sch.send(f.u,f.sink)
   f.sch.observe_lab(f.u,lambda s,st:f.evidence(s,st,'UNAVAILABLE'))
   self.assertEqual(f.sch.recover(f.u)['status'],'UNCERTAIN')
   f.sch.observe_lab(f.u,lambda s,st:f.evidence(s,st,'REVERTED'))
   self.assertEqual(f.sch.recover(f.u)['status'],'FAILED')
   with self.assertRaises(Exception):f.sch.send(f.u,f.sink,retry=True)
   self.assertEqual(f.s.fresh()['u'][f.u]['record']['status'],'SUCCESS');f.close()
 def test_no_fixture_marker(self):
  self.assertEqual(stages.calldata({},'ab'*32,{'kind':'cleanup'}),bytes.fromhex('f474fb90'+'ab'*32))
  with self.assertRaises(Exception):stages.envelope({},dict(target='00'*20,calldata_hex=None))
if __name__=='__main__':unittest.main(verbosity=2)
