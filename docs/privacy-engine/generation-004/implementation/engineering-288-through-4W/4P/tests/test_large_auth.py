import copy,hashlib,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from fixtures.auth_jobs import make
from fixtures.construct import wire,sha,l64
from large_auth.core import execute,load,Outer
from large_auth.integration import run
from link_recovery.cli import create_key,read_key,RecoveryError,atomic_save

class LargeAuthTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.job=make(self.root/'input');self.m=json.loads(self.job.read_bytes());self.key=self.root/'key';create_key(self.key);self.ck=self.root/'journal'
    def tearDown(self):self.tmp.cleanup()
    def go(self,n=10**7,resume=False,chunk=71):return execute(self.job,self.ck,self.key,new_bytes=n,seconds=30,chunk_bytes=chunk,resume=resume)
    def test_exact_independent_preimage_oracle(self):
        r=self.go();self.assertTrue(r['complete']);self.assertEqual(r['complete_object_sha256'],self.m['object_sha256']);self.assertEqual(r['complete_outer_profile_sha256'],self.m['profile_sha256']);self.assertFalse(r['incremental_signature_verified'])
    def test_pause_at_outer_parser_and_file_boundaries(self):
        size=self.m['files']['outer']['bytes'];cuts={1,7,8,24,25,26,32,33,40,55,64,65,size-1,size,size+1,size+8}
        cumulative=0
        for name in ('outer','evidence.tsv','tokens.tsv','links.tsv','signature.txt'):
            cumulative+=self.m['files'][name]['bytes'];cuts.update((cumulative-1,cumulative,cumulative+1))
        for cut in sorted(cuts):
            self.ck.unlink(missing_ok=True)
            with self.subTest(cut=cut):
                self.go(cut);r=self.go(resume=True,chunk=17);self.assertTrue(r['complete']);self.assertEqual(r['complete_object_sha256'],self.m['object_sha256'])
    def test_repeated_resume_exact_result(self):
        r=self.go(7301)
        for _ in range(80):
            if r['complete']:break
            r=self.go(7301,True,97)
        self.assertTrue(r['complete']);self.assertEqual(r['complete_object_sha256'],self.m['object_sha256'])
        again=self.go(resume=True);self.assertEqual(again['complete_object_sha256'],r['complete_object_sha256']);self.assertGreater(again['prefix_bytes_rechecked'],0)
    def test_changed_prefix_same_size_restored_timestamp(self):
        self.go(100);p=self.job.parent/'outer.bin';st=p.stat();b=bytearray(p.read_bytes());b[80]^=1;p.write_bytes(b);os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns));saved=self.ck.read_bytes()
        with self.assertRaises((RecoveryError,ValueError)):self.go(resume=True)
        self.assertEqual(saved,self.ck.read_bytes())
    def test_changed_unread_suffix_no_complete_digest(self):
        self.go(2);p=self.job.parent/'signature.txt';b=bytearray(p.read_bytes());b[-3]^=1;p.write_bytes(b)
        with self.assertRaisesRegex(RecoveryError,'digest mismatch'):self.go(resume=True)
        self.assertIsNone(load(self.ck,read_key(self.key))['result']['complete_object_sha256'])
    def test_corrupt_and_wrong_key_journals(self):
        self.go(4);raw=self.ck.read_bytes();self.ck.write_bytes(raw.replace(b'PAUSED',b'BROKEN'))
        with self.assertRaises(RecoveryError):self.go(resume=True)
        self.ck.write_bytes(raw);self.key.write_bytes(b'X'*32)
        with self.assertRaises(RecoveryError):self.go(resume=True)
    def test_manifest_binding_change_rejected(self):
        self.go(3);self.m['canonical_model_sha256']='0'*64;self.job.write_bytes(wire(self.m))
        with self.assertRaisesRegex(RecoveryError,'incompatible'):self.go(resume=True)
    def test_input_truncated_extended_or_missing(self):
        for change in ('truncate','append','missing'):
            with tempfile.TemporaryDirectory() as d:
                job=make(Path(d)/'input');p=job.parent/'links.tsv'
                if change=='truncate':p.write_bytes(p.read_bytes()[:-1])
                elif change=='append':p.write_bytes(p.read_bytes()+b'x')
                else:p.unlink()
                with self.assertRaises((RecoveryError,OSError)):execute(job,Path(d)/'j',self.key,new_bytes=1000000,seconds=10)
    def test_atomic_checkpoint_interrupt_keeps_prior_commit(self):
        self.go(3);previous=self.ck.read_bytes()
        def fault(stage):
            if stage=='after_file_fsync':raise OSError('simulated interrupted checkpoint write')
        with self.assertRaises(OSError):execute(self.job,self.ck,self.key,resume=True,new_bytes=100,seconds=10,fault=fault)
        self.assertEqual(self.ck.read_bytes(),previous);self.assertTrue(self.go(resume=True)['complete'])
    def test_interruption_during_acquisition_recoverable(self):
        from link_recovery.cli import PauseRequested
        self.go(7);original=os.read;counter=0
        def interrupted(fd,n):
            nonlocal counter
            counter+=1
            if counter==30:raise PauseRequested()
            return original(fd,n)
        with patch('large_auth.core.os.read',interrupted):
            try:self.go(resume=True)
            except PauseRequested:pass
        self.assertTrue(self.go(resume=True)['complete'])
    def test_outer_malformed_lengths_order_trailing_and_truncation(self):
        from v4_ingest.wire import PROFILE_DOMAIN
        outer=PROFILE_DOMAIN+b''.join(l64(n.encode())+l64(b'x') for n in ('SOURCE-OWNED-BODY','EXPRESSION-PROGRAM','PRIVACY'))
        for b in (outer[:-1],outer+b'x',outer.replace(b'SOURCE-OWNED-BODY',b'XOURCE-OWNED-BODY'),outer.replace(len(b'PRIVACY').to_bytes(8,'big'),(999).to_bytes(8,'big'))):
            with self.assertRaises(RecoveryError):
                parser=Outer()
                for x in b:parser.feed(bytes([x]))
                parser.finish()
    def test_integration_retains_semantics_and_crypto_unavailable(self):
        r=run(self.job,self.ck,self.key,new_bytes=10**7,seconds=30,appointment_value=json.loads((self.job.parent/'external-appointment.json').read_bytes()))
        self.assertEqual(r['result'],'REJECTED');self.assertEqual(r['earliest_failure'],'INCOMPLETE-EVIDENCE-UNIVERSE');self.assertTrue(r['bindings']['link_stage']['complete']);self.assertFalse(r['bindings']['complete_authentication'])
    def test_integration_resume_and_cross_journal_substitution(self):
        n=sum(x['bytes'] for x in self.m['files'].values());self.go(n)
        # Explicitly pause inherited supplied-link parser inside a row.
        from link_recovery import cli as c
        import argparse
        args=argparse.Namespace(operation='start',key=self.key,checkpoint=Path(str(self.ck)+'.links.json'),input=self.job.parent/'links.tsv',input_sha256=self.m['files']['links.tsv']['sha256'],model=self.job.parent/'model.txt',model_sha256=self.m['model']['sha256'],contract=self.job.parent/'contract.json',contract_sha256=self.m['contract']['sha256'],chunk_bytes=7,new_bytes=83,seconds=10)
        self.assertEqual(c.execute(args)['result'],'PAUSED')
        r=run(self.job,self.ck,self.key,resume=True,new_bytes=n,seconds=30);self.assertTrue(r['bindings']['link_stage']['complete']);self.assertIn('INVALID-EVIDENCE-AUTHORITY',r['failures'])
    def test_signal_mid_parser_preserves_previous_journal(self):
        from link_recovery.cli import PauseRequested
        self.go(3);previous=self.ck.read_bytes();original=Outer.feed
        def interrupt(parser,data):
            original(parser,data)
            if len(data)>3:raise PauseRequested()
        with patch.object(Outer,'feed',interrupt):
            with self.assertRaises(PauseRequested):self.go(resume=True)
        self.assertEqual(previous,self.ck.read_bytes());self.assertTrue(self.go(resume=True)['complete'])
    def test_all_three_small_scope_jobs(self):
        for scope in ('ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE'):
            job=make(self.root/scope,scope);r=run(job,self.root/(scope+'.j'),self.key,new_bytes=10**7,seconds=30,appointment_value=json.loads((job.parent/'external-appointment.json').read_bytes()))
            self.assertTrue(r['bindings']['link_stage']['complete']);self.assertFalse(r['profile_admitted']);self.assertFalse(r['bindings']['complete_authentication'])
    def test_collector_retains_precedence_multiple_failures(self):
        p=self.job.parent/'signature.txt';b=p.read_bytes();p.write_bytes(b[:-3]+b'x'+b[-2:])
        r=run(self.job,self.ck,self.key,new_bytes=10**7,seconds=30)
        self.assertIn('INVALID-EVIDENCE-DIGEST',r['failures']);self.assertIn('INVALID-EVIDENCE-AUTHORITY',r['failures']);self.assertEqual(r['earliest_failure'],'INVALID-EVIDENCE-AUTHORITY');self.assertTrue(r['bindings']['link_stage']['complete'])
    def test_cross_job_link_journal_rejected(self):
        r=run(self.job,self.ck,self.key,new_bytes=10**7,seconds=30)
        other=make(self.root/'other');otherck=self.root/'other.j'
        import shutil
        shutil.copyfile(str(self.ck)+'.links.json',str(otherck)+'.links.json')
        r=run(other,otherck,self.key,new_bytes=10**7,seconds=30)
        self.assertIn('cross-job link journal substitution',str(r));self.assertFalse(r['bindings']['link_stage']['complete'])
    def test_empty_four_file_lengths_match_independent_object_oracle(self):
        files=[]
        for name in ('evidence.tsv','tokens.tsv','links.tsv','signature.txt'):
            (self.job.parent/name).write_bytes(b'');self.m['files'][name].update(bytes=0,sha256=sha(b''));files.append(l64(b''))
        self.m['object_sha256']=sha(b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n'+b''.join(files));self.job.write_bytes(wire(self.m))
        self.go(25);self.assertEqual(self.go(resume=True)['complete_object_sha256'],self.m['object_sha256'])
    def test_outer_digest_failure_precedes_missing_authority(self):
        p=self.job.parent/'outer.bin';b=bytearray(p.read_bytes());b[-1]^=1;p.write_bytes(b)
        r=run(self.job,self.ck,self.key,new_bytes=10**7,seconds=30)
        self.assertEqual(r['earliest_failure'],'PROFILE-DIGEST-MISMATCH');self.assertIn('INVALID-EVIDENCE-AUTHORITY',r['failures']);self.assertTrue(r['bindings']['link_stage']['complete'])
    def test_unknown_large_backend_never_claims_verification(self):
        from large_auth.backend import capabilities
        self.assertEqual(capabilities()['incremental_pure_ed25519'],'NOT-IMPLEMENTED')

if __name__=='__main__':unittest.main()
