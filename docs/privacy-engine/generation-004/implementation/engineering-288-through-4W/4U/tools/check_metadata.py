#!/usr/bin/env python3
"""Focused 4U metadata adversarial checks; no kernel regression or stream work."""
import copy,json,tempfile,time,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode=True
import bind_text as b
from verify import check_preserved
class Cases(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=b.make_envelope();cls.executed=[]
 def setUp(self):self.e=copy.deepcopy(self.__class__.e);self.__class__.executed.append(self._testMethodName)
 def reject(self):
  with self.assertRaises(ValueError):b.validate_envelope(self.e)
 def test_valid_complete_binding(self):self.assertTrue(b.validate_envelope(self.e))
 def test_binary_digest_in_text_slot(self):self.e['identity']['sha256']=b.BINARY;self.reject()
 def test_text_digest_in_binary_slot(self):self.e['binary_identity']['sha256']=b.TEXT;self.reject()
 def test_descriptor_digest_substitution(self):self.e['identity']['sha256']=self.e['exact_inputs']['descriptor']['sha256'];self.reject()
 def test_digest_type(self):self.e['identity']['digest_type']='SHA256-CONCATENATED-SEGMENT-HASHES';self.reject()
 def test_header(self):self.e['serialization']['header_utf8']=b.HEADER.replace('\n','\r\n');self.reject()
 def test_ordering(self):self.e['serialization']['ordering']='original index order';self.reject()
 def test_orientation(self):self.e['serialization']['potential_orientation']='lexically swap endpoints';self.reject()
 def test_ordinals(self):self.e['serialization']['link_order']='exactly six digits';self.reject()
 def test_duplicate_law(self):self.e['serialization']['merge']='preserve identical duplicate tuples';self.reject()
 def test_stale_model(self):self.e['binding']['model_sha256']='08d6e7fb1e0cf37cc7effa76b50eaff0459abc158d9c6f0da52c6c58372b14f1';self.reject()
 def test_stale_contract(self):self.e['binding']['selected_contract_sha256']='0'*64;self.reject()
 def test_invented_final_profile(self):self.e['binding']['final_profile_sha256']='1'*64;self.reject()
 def test_wrong_counts(self):self.e['identity']['rows']-=1;self.reject()
 def test_compensating_set_counts(self):self.e['identity']['structural_rows']+=1;self.e['identity']['potential_rows']-=1;self.reject()
 def test_size(self):self.e['identity']['serialized_bytes']=729259627770;self.reject()
 def test_incomplete_replay(self):self.e['identity']['replay_segments']=6671;self.reject()
 def test_numeric_type(self):self.e['identity']['generation_segments']=6672.0;self.reject()
 def test_descriptor(self):self.e['exact_inputs']['descriptor']['sha256']='0'*64;self.reject()
 def test_completion_substitution(self):self.e['evidence']['completion']['sha256']='0'*64;self.reject()
 def test_snapshot_substitution(self):self.e['evidence']['snapshot']['sha256']='0'*64;self.reject()
 def test_job_substitution(self):self.e['exact_inputs']['generation_job_identity_sha256']='0'*64;self.reject()
 def test_false_independence(self):self.e['independent_generator']=True;self.reject()
 def test_false_supplied_validation(self):self.e['independent_supplied_row_validation']=True;self.reject()
 def test_false_acquisition(self):self.e['physical_supplied_file_acquired']=True;self.reject()
 def test_false_scope(self):self.e['scoped_bundle_correspondence_established']=True;self.reject()
 def test_false_authentication(self):self.e['authentication_established']=True;self.reject()
 def test_false_qualification(self):self.e['qualification_established']=True;self.reject()
 def test_false_admission(self):self.e['actual_admission']=True;self.reject()
 def test_fabricated_evidence_row(self):self.e['applicable_schema_fields']['future_evidence_field_populated']=True;self.reject()
 def test_missing_field(self):del self.e['evidence'];self.reject()
 def test_unsealed_receipt_corruption(self):
  obj={'payload':{'complete':False},'sha256':'0'*64}
  with self.assertRaises(ValueError):b.unseal(obj)
 def test_completion_report_disagrees_with_snapshot(self):
  real=b.read
  def changed(p):
   x=real(p)
   if Path(p).name=='Engineering-288-4T-return-verification.json':x['completion']['rows']-=1
   return x
  with patch.object(b,'read',changed):
   with self.assertRaises(ValueError):b.basis()
 def test_historical_bytes_preserved_and_mutation_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);p=root/'historical.json';original=b'original signed fixture bytes\n';p.write_bytes(original)
   b.save(root/'inputs/PRESERVED-FILES.json',[{'path':'historical.json',**b.info(p)}]);self.assertEqual(len(check_preserved(root)),1)
   p.write_bytes(b'relabelled signed fixture bytes\n')
   with self.assertRaises(ValueError):check_preserved(root)
 def test_cycle_rejected(self):
  g={'nodes':[{'id':'profile','depends_on':['signature']},{'id':'signature','depends_on':['profile']}]}
  with self.assertRaises(ValueError):b.graph_check(g)
 def test_dependency_missing(self):
  with self.assertRaises(ValueError):b.graph_check({'nodes':[{'id':'signature','depends_on':['missing']} ]})
 def test_broad_duty_still_open(self):
  rs=b.read(b.ROOT/'derived/REQUIREMENTS.json');r=next(r for r in rs if r['id']=='text-stream')
  self.assertEqual(r['status'],'BLOCKED');self.assertIsNone(r['full_model_input']);self.assertEqual(r['mechanical_identity']['sha256'],b.info(b.ROOT/'derived/TEXTUAL-IDENTITY.json')['sha256'])
if __name__=='__main__':
 began=time.monotonic();suite=unittest.defaultTestLoader.loadTestsFromTestCase(Cases);result=unittest.TextTestRunner(verbosity=2).run(suite)
 report={'result':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'seconds':time.monotonic()-began,'cases':Cases.executed,'full_stream_processed':False,'kernel_regression_suite_rerun':False,'actual_admission':False}
 if len(sys.argv)>1:b.save(Path(sys.argv[1]),report)
 print(json.dumps(report));sys.exit(0 if result.wasSuccessful() else 1)
