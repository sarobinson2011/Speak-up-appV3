import copy,json,tempfile,unittest
from pathlib import Path
from fixtures.construct import dataset,wire
from tests.test_admission import profile
from admission_kernel.model import Model
from admission_kernel.sources import FiniteLabProvider
from ledger_kernel.construct import acquire
from ledger_kernel.audit import partition
from ledger_kernel.retained import ROOT
from v4_ingest.records import ValidationError,validate_record

class ConstructionTests(unittest.TestCase):
    def test_constructed_static_templates_equal_independent_fixtures(self):
        for name in ('GAMMA','DELTA'):
            q,t=dataset(name);p=profile(q);provider=FiniteLabProvider(t,{k:bytes.fromhex(v) for k,v in q['materials'].items()},{k:bytes.fromhex(v) for k,v in q['source_objects'].items()})
            r=acquire(provider,t['ledger_source_ref'],Model(p['model']),p['security_contract']['policy']['record'])
            self.assertEqual(r['templates'],{k:p['security_contract'][k] for k in ('obligations','composition_rules')})
            self.assertFalse(r['qualification_established']);self.assertFalse(r['profile_admitted'])
            for row in r['templates']['obligations']:
                self.assertNotIn('profile_digest',row);self.assertNotIn('disposition',row)
    def test_constructor_requires_external_classification_role(self):
        q,t=dataset();del t['laboratory_assumptions']['model-ledger-classification'];p=profile(q)
        provider=FiniteLabProvider(t,{k:bytes.fromhex(v) for k,v in q['materials'].items()},{k:bytes.fromhex(v) for k,v in q['source_objects'].items()})
        with self.assertRaises(ValidationError):acquire(provider,t['ledger_source_ref'],Model(p['model']),p['security_contract']['policy']['record'])
    def test_interval_partition_rejects_missing_duplicate_illegal_counts(self):
        partition([[[0,2]],[[2,4]]],0,4)
        for groups in ([[[0,2]],[[3,4]]],[[[0,2]],[[1,4]]],[[[-1,4]]],[[[0,5]]],[[[0,3]]]):
            with self.assertRaises(ValidationError):partition(groups,0,4)
    def test_inherited_record_ordinals_are_not_primitive_ids(self):
        q,t=dataset();m=copy.deepcopy(t['model'])
        for token in m['tokens']:token['record']=1
        self.assertEqual(len(Model(m).tokens),4)
        for value in (0,-1,True):
            m['tokens'][0]['record']=value
            with self.assertRaises(ValidationError):Model(m)
    def test_literal_record_node_reference_blocker_preserved(self):
        # Exact known obstacle; do not widen accepted grammar or rename nodes.
        row={'obligation_id':'TEST','kind':'EXACT','target_ids':['TARGET'],'coalition_id':'COALITION',
             'node_ids':['SYMBOLIC-U-ONE::SECURITY:ALGORITHM.$record::CP2-ALGORITHM-000001'],
             'edge_ids':[],'experiment_id':None}
        with self.assertRaises(ValidationError):validate_record('OBLIGATION',row,True)

if __name__=='__main__':unittest.main()
