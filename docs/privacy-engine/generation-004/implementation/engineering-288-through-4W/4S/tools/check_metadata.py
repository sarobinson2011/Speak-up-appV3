#!/usr/bin/env python3
import copy,json,tempfile,unittest
from common import *
from verify_checkpoint import graph_check,comparison_check
class Checks(unittest.TestCase):
 def test_model_exact_single_edit(self):comparison_check(R/'historical/model/model.json',R/'candidate/model.json',load(R/'results/MODEL-COMPARISON.json'))
 def test_bad_edit_or_digest_rejected(self):
  x=load(R/'results/MODEL-COMPARISON.json');x['new']['sha256']='0'*64
  with self.assertRaises(AssertionError):comparison_check(R/'historical/model/model.json',R/'candidate/model.json',x)
 def test_dependency_dag(self):self.assertEqual(graph_check(load(R/'dependencies/DEPENDENCY-GRAPH.json')['nodes']),18)
 def test_cycle_rejected(self):
  with self.assertRaises(AssertionError):graph_check([dict(id='a',depends_on=['b']),dict(id='b',depends_on=['a'])])
 def test_missing_dependency_rejected(self):
  with self.assertRaises(AssertionError):graph_check([dict(id='a',depends_on=['missing'])])
 def test_duplicate_dependency_rejected(self):
  with self.assertRaises(AssertionError):graph_check([dict(id='a',depends_on=[]),dict(id='a',depends_on=[])])
 def test_stale_model_binding(self):
  new={'model_sha256':load(R/'candidate/ACTIVE-IDENTITIES.json')['model_sha256'],'profile_sha256':'1'*64};old=dict(new,model_sha256=OLD)
  with self.assertRaises(ValueError):exact_binding(old,new)
 def test_stale_profile_binding(self):
  with self.assertRaises(ValueError):exact_binding({'model_sha256':'a','profile_sha256':'old'},{'model_sha256':'a','profile_sha256':'new'})
 def test_missing_profile_cannot_be_current(self):
  b={'model_sha256':'a','profile_sha256':None}
  with self.assertRaises(ValueError):exact_binding(b,b)
 def test_small_complete_binding_gate(self):
  b={'model_sha256':'a','profile_sha256':'b'};exact_binding(b,b)
 def test_no_duty_discharge(self):
  d=load(R/'candidate/ledger/potential-domain.json');self.assertEqual(d['disposition'],'NOT-ESTABLISHED');self.assertIsNone(d['privacy_classification'])
 def test_no_profile_or_text_fabrication(self):
  d=load(R/'inventory/GAP-REPORT.json');self.assertIsNone(d['final_profile_sha256']);self.assertIsNone(d['text_stream_sha256']);self.assertFalse(d['actual_admission'])
if __name__=='__main__':unittest.main(verbosity=2)
