import ast,copy,hashlib,json,runpy,subprocess,sys,tempfile,unittest
from pathlib import Path
from fixtures.construct import dataset,wire,sha
from fixtures.field_class import literal
from fixtures.integrated import export
from integrated_auth.collector import run
from link_recovery.cli import create_key
from v4_ingest.definition import ACTIVE,SOURCE_ID,SOURCE_SHA256,definition_hashes
from v4_ingest.records import primitive,ingest_record,ingest_security,ingest_evidence,validate_record,canonical,SPEC,ValidationError
from v4_ingest.wire import decode_container
from admission_kernel.admission import collect
ROOT=Path(__file__).resolve().parents[1]

class AmendmentTests(unittest.TestCase):
    def setUp(self):
        self.q,self.t=literal();self.register={s['node_id'] for s in self.t['model']['surfaces']}
        self.profile=json.loads(decode_container(bytes.fromhex(self.q['outer_hex']))['PRIVACY']);self.security=self.profile['security_contract'];self.label=next(x for x in self.security['policy']['field_labels'] if x['surface_id'].endswith('.$record'))
        self.grammar=runpy.run_path(str(ACTIVE/'v4_record_grammar.py'));self.old=runpy.run_path(str(ROOT/'accepted/definition-completion/v4_record_grammar.py'))
    def test_only_one_schema_cell_changed(self):
        import csv
        def rows(p):return list(csv.DictReader(p.read_text().splitlines(),delimiter='\t'))
        old=rows(ROOT/'accepted/definition-completion/security-fields.tsv');new=rows(ACTIVE/'security-fields.tsv')
        changes=[(a,b) for a,b in zip(old,new) if a!=b];self.assertEqual(len(old),len(new));self.assertEqual(len(changes),1)
        a,b=changes[0];self.assertEqual((a['schema'],a['field'],a['type']),('FIELD-LABEL','surface_id','ID'));self.assertEqual(b,dict(a,type='FIELD-CLASS-REF'))
        self.assertEqual(SPEC['OBLIGATION'],self.old['SPEC']['OBLIGATION']);self.assertEqual(self.grammar['SPEC']['OBLIGATION'],self.old['SPEC']['OBLIGATION'])
    def test_general_ID_unchanged(self):
        for value in ('ABC','ABC._:#-09','a::b','SECURITY:ALGORITHM.algorithm_id'):
            for fn in (primitive,self.old['primitive'],self.grammar['primitive']):fn('ID',value)
        for value in ('SECURITY:ALGORITHM.$record','X.$other','$record','x%24record','x y','x\n','＄record'):
            for fn in (primitive,self.old['primitive'],self.grammar['primitive']):
                with self.assertRaises(ValueError):fn('ID',value)
    def test_ordinary_reference_exact_byte_compatibility(self):
        q,t=dataset();p=json.loads(decode_container(bytes.fromhex(q['outer_hex']))['PRIVACY']);reg={s['node_id'] for s in t['model']['surfaces']}
        for label in p['security_contract']['policy']['field_labels']:
            self.old['record_shape']('FIELD-LABEL',label);new=self.grammar['record_shape']('FIELD-LABEL',label,field_register=reg)
            self.assertEqual(canonical(new),canonical(label));self.assertEqual(ingest_record(canonical(label),'FIELD-LABEL',field_register=reg),label)
    def test_literal_record_reference_both_implementations(self):
        with self.assertRaises(ValueError):self.old['record_shape']('FIELD-LABEL',self.label)
        self.grammar['record_shape']('FIELD-LABEL',self.label,field_register=self.register)
        self.assertEqual(ingest_record(canonical(self.label),'FIELD-LABEL',field_register=self.register),self.label)
        self.assertIn(b'SECURITY:ALGORITHM.$record',canonical(self.label))
    def test_absent_wrong_case_alias_occurrence_other_dollar(self):
        cases=['SECURITY:UNKNOWN.$record','security:ALGORITHM.$record','SECURITY:ALGORITHM.record','SECURITY:ALGORITHM.%24record','SECURITY:ALGORITHM.$other','SECURITY:ALGORITHM.$record.extra','SYMBOLIC-U-ONE::SECURITY:ALGORITHM.$record::R','SYMBOLIC-U-ONE::LAB:metadata::R','SECURITY:ALGORITHM.＄record']
        for value in cases:
            label=dict(self.label,surface_id=value)
            with self.subTest(value=value):
                with self.assertRaises(ValueError):self.grammar['record_shape']('FIELD-LABEL',label,field_register=self.register)
                with self.assertRaises(ValidationError):ingest_record(canonical(label),'FIELD-LABEL',field_register=self.register)
    def test_missing_register_and_string_substring_context_fail(self):
        for reg in (None,'SECURITY:ALGORITHM.$record',{'wrong':'SECURITY:ALGORITHM.$record'}):
            with self.assertRaises(ValueError):ingest_record(canonical(self.label),'FIELD-LABEL',field_register=reg)
            with self.assertRaises(ValueError):self.grammar['record_shape']('FIELD-LABEL',self.label,field_register=reg)
    def test_security_and_evidence_ingestion_and_documentary_grammar(self):
        self.grammar['security_shape'](self.security,field_register=self.register)
        e=json.loads(bytes.fromhex(self.q['security_records_hex']));self.grammar['evidence_shape'](e,field_register=self.register)
        for raw,fn in ((canonical(self.security),ingest_security),(bytes.fromhex(self.q['security_records_hex']),ingest_evidence)):
            v,r=fn(raw,field_register=self.register);self.assertFalse(r['profile_admitted']);self.assertFalse(r['source_qualification_established'])
            with self.assertRaises(ValueError):fn(raw)
    def test_complete_retained_register(self):
        register=json.loads((ROOT/'rebinding/field-class-register.json').read_bytes());self.assertEqual(len(register),4119)
        record_names=[s for s in register if '$' in s];self.assertTrue(record_names)
        for name in register:
            primitive('FIELD-CLASS-REF',name,field_register=register);self.grammar['primitive']('FIELD-CLASS-REF',name,register)
        for name in record_names:
            with self.assertRaises(ValueError):primitive('ID',name)
        self.assertEqual(len(record_names),16)
    def test_unchanged_obligation_rejects_literal_node_accepts_edge(self):
        o={'obligation_id':'O','kind':'EXACT','target_ids':['T'],'coalition_id':'C','node_ids':['SYMBOLIC-U-ONE::SECURITY:ALGORITHM.$record::R'],'edge_ids':[],'experiment_id':None}
        for fn in (lambda:self.grammar['record_shape']('OBLIGATION',o,True),lambda:validate_record('OBLIGATION',o,True)):
            with self.assertRaises(ValueError):fn()
        o['node_ids']=[];o['edge_ids']=['G4-STRUCTURAL-EDGE-198061'];self.grammar['record_shape']('OBLIGATION',o,True);validate_record('OBLIGATION',o,True)
    def test_source_consolidation_and_active_identity(self):
        source=(ACTIVE/(SOURCE_ID+'.md')).read_bytes();self.assertEqual(sha(source),SOURCE_SHA256)
        for n in ('security-fields.tsv','v4_record_grammar.py','ACCEPTANCE-CONTRACT.txt'):self.assertEqual(source.count((ACTIVE/n).read_bytes()),1)
        self.assertEqual(self.profile['format_source'],SOURCE_ID)
        for k,h in definition_hashes().items():self.assertEqual(self.security[k],h)
    def test_conditional_collectors_and_recovery_for_literal_families(self):
        for name in ('GAMMA','DELTA'):
            q,t=literal(name);r=collect(q,t);self.assertEqual(r['failures'],[],r);self.assertFalse(r['actual_qualification_established'])
            with tempfile.TemporaryDirectory() as d:
                d=Path(d);m,tr=export(d/'input',q,t);key=d/'key';create_key(key)
                r=run(m,tr,d/'journal',key,new_bytes=83,seconds=30);self.assertEqual(r['result'],'PAUSED')
                r=run(m,tr,d/'journal',key,resume=True,new_bytes=10**7,seconds=30);self.assertEqual(r['failures'],[],r);self.assertFalse(r['profile_admitted'])
    def test_missing_qualification_not_established_by_amendment(self):
        self.t['laboratory_assumptions'].pop('observer-completeness');r=collect(self.q,self.t)
        self.assertIn('INVALID-EVIDENCE-AUTHORITY',r['failures']);self.assertFalse(r['profile_admitted']);self.assertFalse(r['bindings']['scope_validation']['ready'])
    def test_caller_label_cannot_define_its_own_register(self):
        e=json.loads(bytes.fromhex(self.q['security_records_hex']));e['records']['FIELD-LABEL']['instances'][0]['surface_id']='SECURITY:ABSENT.$record';self.q['security_records_hex']=canonical(e).hex()
        r=collect(self.q,self.t);self.assertIn('INCOMPLETE-EVIDENCE-UNIVERSE',r['failures']);self.assertFalse(r['profile_admitted'])
    def test_stale_old_profile_not_silently_migrated(self):
        path=ROOT/'fixtures/4H-GAMMA';m=json.loads((path/'manifest.json').read_bytes());q=copy.deepcopy(m['request']);q['outer_hex']=(path/m['records']['outer_hex']['path']).read_bytes().hex()
        self.q['outer_hex']=q['outer_hex'];r=collect(self.q,self.t);self.assertIn('INVALID-PROFILE-SCHEMA',r['failures'])
    def test_cli_exact_register(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'record').write_bytes(canonical(self.label));(p/'register').write_bytes(canonical(sorted(self.register)))
            cmd=[sys.executable,'-m','v4_ingest','record',str(p/'record'),'--schema','FIELD-LABEL']
            a=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);self.assertEqual(a.returncode,2)
            b=subprocess.run(cmd+['--field-register',str(p/'register')],cwd=ROOT,capture_output=True,text=True);self.assertEqual(b.returncode,0,b.stderr)
    def test_actual_admission_remains_disabled(self):
        self.q['mode']='ACTUAL';r=collect(self.q,self.t);self.assertIn('INVALID-EVIDENCE-AUTHORITY',r['failures']);self.assertFalse(r['profile_admitted'])
    def test_noncanonical_escape_not_an_alias(self):
        raw=canonical(self.label).replace(b'.$record',b'.\\u0024record')
        with self.assertRaises(ValueError):ingest_record(raw,'FIELD-LABEL',field_register=self.register)
    def test_historical_receipt_binding_rejected(self):
        from integrated_auth.collector import journal,implementation
        from link_recovery.cli import atomic_save,read_key
        with tempfile.TemporaryDirectory() as d:
            d=Path(d);key=d/'key';create_key(key);k=read_key(key);binding={'implementation':implementation()}
            old=copy.deepcopy(binding);old['implementation']['files']['v4_ingest/records.py']='0'*64
            atomic_save(d/'receipt',{'format':'CP4H-FILE-COLLECTOR-1','binding':old,'sequence':0,'stages':{},'last_result':None},k)
            with self.assertRaisesRegex(ValueError,'incompatible'):journal(d/'receipt',k,binding)
    def test_active_definition_not_caller_selected(self):
        from tests.test_admission import mutate_profile
        old_schema=sha((ROOT/'accepted/definition-completion/security-fields.tsv').read_bytes())
        self.t['definition_hashes']['schema_sha256']=old_schema
        mutate_profile(self.q,lambda p:p['security_contract'].__setitem__('schema_sha256',old_schema))
        r=collect(self.q,self.t);self.assertIn('INVALID-PROFILE-SCHEMA',r['failures']);self.assertIn('active amendment exact definition identity schema_sha256',str(r))
