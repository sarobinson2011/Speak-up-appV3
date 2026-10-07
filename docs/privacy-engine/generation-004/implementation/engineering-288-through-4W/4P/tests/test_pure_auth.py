import copy,hashlib,json,os,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from fixtures.auth_jobs import make
from fixtures.construct import wire
from tests.test_auth_crypto import VECTORS,cases,openssl_verify
from large_auth.backend import sodium_verify
from pure_auth.controller import verify_job,BINARY,load,identity
from pure_auth.preflight import run
from link_recovery.cli import create_key,read_key,RecoveryError,PauseRequested

def native(pk,sig,msg,total=None,limit=None):
    total=len(msg) if total is None else total;limit=len(msg) if limit is None else limit
    return subprocess.run([str(BINARY),'verify',pk.hex(),sig.hex(),str(total),str(limit)],input=msg,capture_output=True,timeout=10)

class NativePureTests(unittest.TestCase):
    def test_standard_rfc_vectors(self):
        for seed,pk,msg,sig in VECTORS:
            p=native(bytes.fromhex(pk),bytes.fromhex(sig),bytes.fromhex(msg));self.assertEqual(p.returncode,0,p.stderr);self.assertTrue(json.loads(p.stdout)['verified'])
    def test_recorded_4f_discrepancies_and_wrong_variants(self):
        for n,pk,sig,msg in cases():
            with self.subTest(case=n):
                p=native(pk,sig,msg);self.assertEqual(p.returncode==0,n in ('valid','canonical-identity-small-order'),p.stderr)
    def test_rfc8032ctx_fixture_is_not_pure(self):
        pk=bytes.fromhex('dfc9425e4f968f7f0c29f0259cf5f9aed6851c2bb4ad8bfb860cfee0ab248292')
        msg=bytes.fromhex('f726936d19c800494e3fdaff20b276a8')
        sig=bytes.fromhex('55a4cc2f70a54e04288c5f4cd1e45a7bb520b36292911876cada7323198dd87a8b36950b95130022907a7fb7c4e9b2d5f6cca685a587b4b21f4b888e4e7edb0d')
        self.assertEqual(native(pk,sig,msg).returncode,2);self.assertFalse(openssl_verify(pk,sig,msg));self.assertFalse(sodium_verify(pk,sig,msg))
    def test_full_point_encoding_boundaries_both_signs(self):
        prime=2**255-19
        for value in (prime,prime+1,2**255-1):
            for sign in (0,1):
                point=(value+(sign<<255)).to_bytes(32,'little');p=subprocess.run([str(BINARY),'encoding',point.hex()],capture_output=True)
                self.assertEqual(p.returncode,2)
        for value in (1,prime-1):
            good=value.to_bytes(32,'little');bad=(value+(1<<255)).to_bytes(32,'little')
            self.assertEqual(subprocess.run([str(BINARY),'encoding',good.hex()],capture_output=True).returncode,0)
            self.assertEqual(subprocess.run([str(BINARY),'encoding',bad.hex()],capture_output=True).returncode,2)
        for point in (bytes(32),bytes(31)+b'\x80'):
            self.assertEqual(subprocess.run([str(BINARY),'encoding',point.hex()],capture_output=True).returncode,0)
        self.assertEqual(subprocess.run([str(BINARY),'encoding',(2).to_bytes(32,'little').hex()],capture_output=True).returncode,2)
    def test_noncanonical_R_both_recorded_forms(self):
        one=b'\x01'+b'\0'*31
        for r in (b'\x01'+b'\0'*30+b'\x80',(2**255-18).to_bytes(32,'little')):
            self.assertEqual(native(one,r+b'\0'*32,b'test').returncode,2)
    def test_scalar_bounds_not_reduced(self):
        L=2**252+27742317777372353535851937790883648493;one=b'\x01'+b'\0'*31
        for s in (L,L+1,2**253,2**256-1):
            p=native(one,one+s.to_bytes(32,'little'),b'test');self.assertEqual(p.returncode,2);self.assertIn(b'scalar',p.stderr)
        # L-1 is valid encoding but cannot satisfy the identity signature equation.
        p=native(one,one+(L-1).to_bytes(32,'little'),b'test');self.assertEqual(p.returncode,2);self.assertIn(b'equation',p.stderr)
        self.assertEqual(native(one,one+bytes(32),b'test').returncode,0)
    def test_exact_EOF_truncation_trailing_and_partial_cannot_verify(self):
        _,pk,msg,sig=VECTORS[1];pk,sig,msg=bytes.fromhex(pk),bytes.fromhex(sig),bytes.fromhex(msg)
        for data,total,limit,expected in ((b'',1,1,2),(msg+b'x',1,1,2),(b'',1,0,3)):
            p=native(pk,sig,data,total,limit);self.assertEqual(p.returncode,expected);self.assertFalse(json.loads(p.stdout)['verified'])
        proc=subprocess.Popen([str(BINARY),'verify',pk.hex(),sig.hex(),'2','2'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        proc.stdin.write(msg);proc.stdin.flush();proc.terminate();out,err=proc.communicate(timeout=5)
        self.assertNotIn(b'\"verified\":true',out)

class PureRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.job=make(self.root/'input');self.ck=self.root/'crypto.json';self.key=self.root/'key';create_key(self.key)
        self.pk=bytes.fromhex(json.loads((self.job.parent/'external-appointment.json').read_bytes())['public_key']);self.m=json.loads(self.job.read_bytes())
    def tearDown(self):self.temp.cleanup()
    def go(self,n=1000000,resume=False,chunk=17,**kw):return verify_job(self.job,self.ck,self.key,self.pk,new_bytes=n,resume=resume,seconds=10,chunk_bytes=chunk,**kw)
    def test_independent_signature_and_digest(self):
        r=self.go();raw=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+b''.join((self.job.parent/n).read_bytes() for n in ('evidence.tsv','tokens.tsv','links.tsv'))
        sig=bytes.fromhex((self.job.parent/'signature.txt').read_text().split()[1]);self.assertTrue(openssl_verify(self.pk,sig,raw));self.assertTrue(sodium_verify(self.pk,sig,raw));self.assertTrue(r['cryptographic_signature_verified']);self.assertEqual(r['complete_message_sha256'],hashlib.sha256(raw).hexdigest());self.assertFalse(r['profile_admitted'])
    def test_boundaries_and_repeated_resume(self):
        total=25+sum(self.m['files'][n]['bytes'] for n in ('evidence.tsv','tokens.tsv','links.tsv'))
        for cut in (1,24,25,26,799,800,801,total-1,total):
            self.ck.unlink(missing_ok=True);first=self.go(cut);last=self.go(resume=True,chunk=1)
            self.assertTrue(last['cryptographic_signature_verified']);self.assertEqual(last['replayed_bytes'],first['offset'])
        self.ck.unlink();r=self.go(13)
        while not r['cryptographic_signature_verified']:r=self.go(71,True,73)
        again=self.go(resume=True);self.assertEqual(r['complete_message_sha256'],again['complete_message_sha256']);self.assertEqual(again['new_bytes'],0)
    def test_changed_prefix_same_metadata_and_changed_suffix(self):
        for prefix in (True,False):
            self.ck.unlink(missing_ok=True);p=self.job.parent/'evidence.tsv';original=p.read_bytes();st=p.stat();self.go(100)
            b=bytearray(original);b[1 if prefix else -1]^=1;p.write_bytes(b);os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns));previous=self.ck.read_bytes()
            with self.assertRaises((RecoveryError,OSError,ValueError)):self.go(resume=True)
            self.assertEqual(previous,self.ck.read_bytes());p.write_bytes(original)
    def test_corrupt_journal_and_wrong_key(self):
        self.go(9);b=self.ck.read_bytes();self.ck.write_bytes(b.replace(b'PAUSED',b'BROKEN'))
        with self.assertRaises(RecoveryError):self.go(resume=True)
        self.ck.write_bytes(b);self.key.write_bytes(b'Z'*32)
        with self.assertRaises(RecoveryError):self.go(resume=True)
    def test_key_signature_manifest_backend_binding(self):
        self.go(30)
        with self.assertRaises(RecoveryError):verify_job(self.job,self.ck,self.key,b'X'*32,resume=True,seconds=10)
        with patch('pure_auth.controller.identity',return_value={'changed':True}):
            with self.assertRaises(RecoveryError):self.go(resume=True)
        raw=self.job.read_bytes();m=json.loads(raw);m['canonical_model_sha256']='0'*64;self.job.write_bytes(wire(m))
        with self.assertRaises(RecoveryError):self.go(resume=True)
        self.job.write_bytes(raw);sig=self.job.parent/'signature.txt';original=sig.read_bytes();sig.write_bytes(original[:-3]+(b'1' if original[-3:-2]==b'0' else b'0')+original[-2:])
        with self.assertRaises(RecoveryError):self.go(resume=True)
    def test_interrupted_write_previous_checkpoint_recovers(self):
        self.go(7);before=self.ck.read_bytes()
        def fault(stage):
            if stage=='after_file_fsync':raise OSError('injected interrupted checkpoint write')
        with self.assertRaises(OSError):self.go(19,True,fault=fault)
        self.assertEqual(before,self.ck.read_bytes());self.assertTrue(self.go(resume=True)['cryptographic_signature_verified'])
        self.ck.unlink();self.go(7)
        def after_replace(stage):
            if stage=='after_replace':raise OSError('crash after atomic replace')
        with self.assertRaises(OSError):self.go(19,True,fault=after_replace)
        self.assertEqual(load(self.ck,read_key(self.key))['offset'],26);self.assertTrue(self.go(resume=True)['cryptographic_signature_verified'])
    def test_interruption_midstream_never_authenticates(self):
        self.go(7);before=self.ck.read_bytes()
        from large_auth.message import signed_message
        def interrupted(*a,**kw):
            for i,b in enumerate(signed_message(*a,**kw)):
                if i==3:raise PauseRequested()
                yield b
        with patch('pure_auth.controller.signed_message',interrupted):
            with self.assertRaises(PauseRequested):self.go(resume=True)
        self.assertEqual(before,self.ck.read_bytes());self.assertTrue(self.go(resume=True)['cryptographic_signature_verified'])
    def test_malformed_or_truncated_input_never_authenticates(self):
        p=self.job.parent/'links.tsv';p.write_bytes(p.read_bytes()[:-1])
        with self.assertRaises(RecoveryError):self.go()
    def test_byte_crypto_preflight_and_outer_tampering(self):
        ck=self.root/'preflight';r=run(self.job,ck,self.key,self.pk,new_bytes=1000000,seconds=10)
        self.assertTrue(r['cryptographic_signature_verified']);self.assertTrue(r['byte_stage']['complete']);self.assertFalse(r['profile_admitted'])
        p=self.job.parent/'outer.bin';p.write_bytes(p.read_bytes()[:-1]+b'x')
        with self.assertRaises(RecoveryError):run(self.job,ck,self.key,self.pk,resume=True,new_bytes=1000000,seconds=10)

if __name__=='__main__':unittest.main()
