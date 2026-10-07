import unittest,runpy
from pathlib import Path
from proposal.field_class import field_class_ref
from v4_ingest.records import primitive
ROOT=Path(__file__).resolve().parents[1]
class ProposalTests(unittest.TestCase):
    def test_current_accepted_rejection_preserved(self):
        g=runpy.run_path(str(ROOT/'accepted/definition-completion/v4_record_grammar.py'))
        for fn in (primitive,g['primitive']):
            with self.assertRaises(ValueError):fn('ID','SECURITY:ALGORITHM.$record')
        self.assertEqual(g['SPEC']['FIELD-LABEL']['surface_id'],'ID')
    def test_proposed_field_only_literal_and_existing_spelling(self):
        register={'SECURITY:ALGORITHM.$record','SECURITY:ALGORITHM.algorithm_id'}
        for value in register:self.assertTrue(field_class_ref(value,register))
        for value in ('SECURITY:UNKNOWN.$record','SECURITY:ALGORITHM.%24record','SECURITY:ALGORITHM.$other','SECURITY:ALGORITHM.$record\n','SECURITY:ALGORITHM.＄record','SYMBOLIC-U-ONE::SECURITY:ALGORITHM.$record::x'):
            self.assertFalse(field_class_ref(value,register))
    def test_no_general_id_relaxation(self):
        self.assertTrue(field_class_ref('X.$record',{'X.$record'}))
        with self.assertRaises(ValueError):primitive('ID','X.$record')
