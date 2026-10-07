import copy,json,os,tempfile,unittest
from pathlib import Path
from fixtures.construct import dataset,wire,sha
from fixtures.integrated import make,export
from integrated_auth.collector import run
from integrated_auth.adapters import TokenMatcher,token_lines
from link_recovery.cli import create_key
from admission_kernel.model import Model
from scope_auth.closure import ScopedModel
from v4_ingest.records import ValidationError

class IntegratedTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.key=self.root/'key';create_key(self.key);self.ck=self.root/'journal'
        self.q,self.t=dataset();self.m,self.tr=export(self.root/'input',self.q,self.t)
    def tearDown(self):self.tmp.cleanup()
    def go(self,resume=False,n=10**7,chunk=71):return run(self.m,self.tr,self.ck,self.key,resume=resume,new_bytes=n,seconds=30,chunk_bytes=chunk)
    def fresh(self,q=None,t=None):self.m,self.tr=export(self.root/'input',q or self.q,t or self.t)
    def assert_reject(self,r,code):self.assertIn(code,r['failures']);self.assertFalse(r['profile_admitted'])
    def test_end_to_end_independent_families(self):
        for name in ('GAMMA','DELTA'):
            with self.subTest(name=name):
                self.m,self.tr=make(self.root/name,name);self.ck=self.root/(name+'.j');r=self.go();self.assertEqual(r['failures'],[]);self.assertTrue(r['bindings']['scope_validation']['conditional_checks_pass']);self.assertFalse(r['actual_qualification_established'])
                for a in r['bindings']['bundle_authentication'].values():self.assertTrue(a['signature_valid']);self.assertTrue(a['four_file_identity'])
    def test_repeated_resume_exact_results_and_terminal_recheck(self):
        r=self.go(n=83,chunk=7);self.assertEqual(r['result'],'PAUSED');self.assertFalse(r['complete_authentication'])
        for n in (107,257,10**7):r=self.go(True,n,17)
        self.assertEqual(r['failures'],[]);r2=self.go(True);self.assertEqual(r2['failures'],[])
        for scope in r['bindings']['bundle_authentication']:
            a=r['bindings']['bundle_authentication'][scope];b=r2['bindings']['bundle_authentication'][scope]
            self.assertEqual(a['crypto_stage']['complete_message_sha256'],b['crypto_stage']['complete_message_sha256'])
    def test_parser_boundary_resumes(self):
        for n in (1,8,76,77,78,83,314,315,316,583,584):
            self.ck=self.root/('j'+str(n));self.go(n=n,chunk=1);r=self.go(True,chunk=13);self.assertEqual(r['failures'],[])
    def test_missing_appointment_and_missing_qualification(self):
        t=copy.deepcopy(self.t);t.pop('appointment');t['laboratory_assumptions'].pop('proof-soundness');self.fresh(t=t)
        r=self.go();self.assert_reject(r,'INVALID-EVIDENCE-AUTHORITY');self.assertEqual(r['earliest_failure'],'INVALID-EVIDENCE-AUTHORITY')
    def test_wrong_appointment(self):
        t=copy.deepcopy(self.t);t['appointment']['public_key']='01'*32;t['appointment']['key_fingerprint_sha256']=sha(bytes.fromhex('01'*32));self.fresh(t=t)
        r=self.go();self.assert_reject(r,'INVALID-EVIDENCE-AUTHORITY');self.assert_reject(r,'INVALID-EVIDENCE-AUTHENTICATION')
    def test_substituted_scope_bundle(self):
        q=copy.deepcopy(self.q);q['bundles']['ROOT-ELIGIBLE']=q['bundles']['NOT-APPLICABLE'];self.fresh(q=q)
        r=self.go();self.assert_reject(r,'INVALID-ACTION-CONTEXT');self.assert_reject(r,'INVALID-EVIDENCE-DIGEST')
    def test_altered_file_and_independent_qualification_failure(self):
        t=copy.deepcopy(self.t);t['laboratory_assumptions'].pop('proof-soundness');self.fresh(t=t)
        p=self.m.parent/'ROOT-ELIGIBLE/links.tsv';b=p.read_bytes();p.write_bytes(b.replace(b'EQUALS',b'SOURCE'))
        r=self.go();self.assert_reject(r,'INVALID-EVIDENCE-AUTHENTICATION');self.assert_reject(r,'INVALID-EVIDENCE-DIGEST');self.assert_reject(r,'INVALID-EVIDENCE-AUTHORITY');self.assertEqual(r['earliest_failure'],'INVALID-PROFILE-SCHEMA')
    def test_wrong_model_contract_and_profile(self):
        m=json.loads(self.m.read_bytes());m['canonical_model_sha256']='0'*64;m['request']['profile_digest']='1'*64;self.m.write_bytes(wire(m))
        r=self.go();self.assert_reject(r,'PROFILE-DIGEST-MISMATCH');self.assert_reject(r,'INVALID-ACTION-CONTEXT')
    def test_source_bytes_changed(self):
        m=json.loads(self.m.read_bytes());e=next(iter(m['materials'].values()));p=self.m.parent/e['path'];p.write_bytes(b'X'*e['bytes'])
        self.assert_reject(self.go(),'INVALID-EVIDENCE-DIGEST')
    def test_dishonest_signed_pass_assertion(self):
        self.q,self.t=dataset(maximum=[0,1],observation={'nodes':[{'id':'a','type':'PRIVATE-ACTOR','actor_id':'alice'}],'edges':[],'visibility':{}})
        # DELTA independent exact bound is 1/4, while signed cells are authored PASS.
        self.q,self.t=dataset('DELTA',maximum=[0,1]);self.fresh();r=self.go();self.assert_reject(r,'CORRELATION-FAILURE');self.assert_reject(r,'INCOMPLETE-EVIDENCE-UNIVERSE');self.assertFalse(r['bindings']['scope_validation']['signed_results_consistent'])
    def test_changed_prefix_same_size_timestamp_terminal(self):
        self.go();p=self.m.parent/'SCOPED-USED/tokens.tsv';st=p.stat();b=p.read_bytes();p.write_bytes(b.replace(b'G-N0',b'G-N9'));os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns))
        r=self.go(True);self.assert_reject(r,'INVALID-EVIDENCE-DIGEST');self.assert_reject(r,'INVALID-EVIDENCE-AUTHENTICATION')
    def test_corrupt_journal(self):
        self.go(n=5);self.ck.write_bytes(self.ck.read_bytes().replace(b'PAUSED',b'BROKEN'))
        with self.assertRaises(ValueError):self.go(True)
    def test_stale_manifest_or_trusted_receipt(self):
        self.go(n=5);t=json.loads(self.tr.read_bytes());t['scope']='SUBSTITUTED';self.tr.write_bytes(wire(t))
        with self.assertRaisesRegex(ValueError,'stale'):self.go(True)
    def test_cross_scope_crypto_receipt_substitution(self):
        self.go(n=100);a=Path(str(self.ck)+'.ROOT-ELIGIBLE.crypto');b=Path(str(self.ck)+'.SCOPED-USED.crypto');b.write_bytes(a.read_bytes())
        r=self.go(True);self.assert_reject(r,'INVALID-EVIDENCE-AUTHENTICATION')
    def test_missing_link_and_duplicate_are_not_completeness(self):
        for name,mut in [('missing',lambda b:b[:b.rfind(b'\n',0,-1)+1]),('duplicate',lambda b:b+b.splitlines(keepends=True)[-1])]:
            self.ck=self.root/(name+'.j');p=self.m.parent/'ROOT-ELIGIBLE/links.tsv';original=bytes.fromhex(self.q['bundles']['ROOT-ELIGIBLE']['files']['links.tsv']);p.write_bytes(mut(original));r=self.go();self.assertTrue(r['failures']);self.assertFalse(r['bindings'].get('scope_validation',{}).get('conditional_checks_pass',False));p.write_bytes(original)
    def test_token_adapter_arbitrary_chunks_and_truncation(self):
        model=Model(self.t['model']);s=ScopedModel(model,list(range(len(model.tokens))));raw=b''.join(token_lines(s,'STATIC-ADMISSION',None))
        self.assertEqual(raw,bytes.fromhex(self.q['bundles']['NOT-APPLICABLE']['files']['tokens.tsv']))
        for n in (1,2,7,64,65536):
            p=TokenMatcher(s,'STATIC-ADMISSION',None)
            for off in range(0,len(raw),n):p.feed(raw[off:off+n])
            p.finish()
        for b in (raw[:-1],raw+b'\n',raw.replace(b'000001',b'000002'),raw.replace(b'\n',b'\r\n')):
            with self.assertRaises(ValidationError):p=TokenMatcher(s,'STATIC-ADMISSION',None);p.feed(b);p.finish()
    def test_actual_always_disabled(self):
        q=copy.deepcopy(self.q);q['mode']='ACTUAL';self.fresh(q=q);r=self.go();self.assert_reject(r,'INVALID-EVIDENCE-AUTHORITY');self.assertFalse(r['profile_admitted'])
    def test_interrupted_collector_commit_recovers_prior_state(self):
        from unittest.mock import patch
        from link_recovery.cli import atomic_save
        self.go(n=13);prior=self.ck.read_bytes()
        def interrupted(path,payload,key):
            def fault(stage):
                if stage=='after_file_fsync':raise OSError('injected checkpoint interruption')
            return atomic_save(path,payload,key,fault)
        with patch('integrated_auth.collector.atomic_save',interrupted):
            with self.assertRaises(OSError):self.go(True,n=23)
        self.assertEqual(self.ck.read_bytes(),prior);self.assertEqual(self.go(True)['failures'],[])
    def test_missing_supplied_file_is_missing_evidence(self):
        (self.m.parent/'ROOT-ELIGIBLE/links.tsv').unlink();self.assert_reject(self.go(),'MISSING-EVIDENCE')
    def test_source_owned_seed_closure_not_caller_metadata(self):
        t=copy.deepcopy(self.t);t['scope_source_ref']=t['ledger_source_ref'];self.fresh(t=t);r=self.go();self.assertTrue(r['failures']);self.assertFalse(r['bindings']['scope_validation']['ready'])
    def test_receipt_cannot_grant_source_qualification(self):
        self.go();t=copy.deepcopy(self.t);t['laboratory_assumptions'].pop('source-producer-correspondence');self.tr.write_bytes(wire(t))
        with self.assertRaisesRegex(ValueError,'stale'):self.go(True)
        self.ck=self.root/'new-receipt';r=self.go();self.assert_reject(r,'INVALID-EVIDENCE-AUTHORITY');self.assertFalse(r['bindings']['scope_validation']['ready'])
    def test_malformed_token_framing_precedes_missing_authority(self):
        t=copy.deepcopy(self.t);t.pop('appointment');self.fresh(t=t)
        p=self.m.parent/'ROOT-ELIGIBLE/tokens.tsv';p.write_bytes(p.read_bytes().replace(b'\n',b'\r\n'))
        r=self.go();self.assert_reject(r,'INVALID-PROFILE-SCHEMA');self.assert_reject(r,'INVALID-EVIDENCE-AUTHORITY');self.assertEqual(r['earliest_failure'],'INVALID-PROFILE-SCHEMA')
