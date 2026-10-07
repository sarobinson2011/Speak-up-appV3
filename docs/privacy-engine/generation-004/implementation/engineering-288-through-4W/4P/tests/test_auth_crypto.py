"""Established independent one-shot backends; no production streaming crypto."""
import ctypes,ctypes.util,hashlib,json,tempfile,unittest
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey,Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
from large_auth.backend import sodium_verify
from large_auth.message import signed_message
from fixtures.auth_jobs import make
VECTORS=[
 ('9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60','d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a','','e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b'),
 ('4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb','3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c','72','92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00')]
def openssl_verify(pk,sig,msg):
    try:Ed25519PublicKey.from_public_bytes(pk).verify(sig,msg);return True
    except (ValueError,InvalidSignature):return False

def cases():
    seed,pk,msg,sig=map(bytes.fromhex,VECTORS[1]);sk=Ed25519PrivateKey.from_private_bytes(seed)
    L=2**252+27742317777372353535851937790883648493
    rows=[('valid',pk,sig,msg),('changed-message',pk,sig,msg+b'x'),('wrong-key',bytes.fromhex(VECTORS[0][1]),sig,msg),('wrong-signature',pk,bytes.fromhex(VECTORS[0][3]),msg),('short-signature',pk,sig[:-1],msg),('long-signature',pk,sig+b'x',msg),('short-key',pk[:-1],sig,msg),('scalar-L',pk,sig[:32]+L.to_bytes(32,'little'),msg),('R-y-equals-p',pk,(2**255-19).to_bytes(32,'little')+sig[32:],msg),('key-y-equals-p',(2**255-19).to_bytes(32,'little'),sig,msg),('R-negative-zero',pk,b'\x01'+b'\0'*30+b'\x80'+sig[32:],msg),('digest-sha256',pk,sk.sign(hashlib.sha256(msg).digest()),msg),('digest-sha512',pk,sk.sign(hashlib.sha512(msg).digest()),msg)]
    # Genuine libsodium Ed25519ph fixture; verification must reject it as pure.
    lib=ctypes.CDLL(ctypes.util.find_library('sodium'));lib.sodium_init();lib.crypto_sign_statebytes.restype=ctypes.c_size_t
    state=ctypes.create_string_buffer(lib.crypto_sign_statebytes());pub=ctypes.create_string_buffer(32);secret=ctypes.create_string_buffer(64);out=ctypes.create_string_buffer(64);n=ctypes.c_ulonglong()
    lib.crypto_sign_seed_keypair(pub,secret,seed);lib.crypto_sign_init(state)
    lib.crypto_sign_update.argtypes=(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_ulonglong);lib.crypto_sign_update(state,msg,len(msg));lib.crypto_sign_final_create(state,out,ctypes.byref(n),secret)
    rows.append(('Ed25519ph',pk,out.raw,msg))
    identity=b'\x01'+b'\0'*31
    rows.append(('canonical-identity-small-order',identity,identity+b'\0'*32,msg))
    rows.append(('noncanonical-negative-zero-key',b'\x01'+b'\0'*30+b'\x80',identity+b'\0'*32,b'test'))
    rows.append(('noncanonical-y-identity-key',(2**255-18).to_bytes(32,'little'),identity+b'\0'*32,b'test'))
    return rows

def probe():
    return [{'case':n,'public_key':p.hex(),'signature':s.hex(),'message_hex':m.hex(),'openssl':openssl_verify(p,s,m),'libsodium':sodium_verify(p,s,m)} for n,p,s,m in cases()]

class CryptoTests(unittest.TestCase):
    def test_rfc8032_known_answers_two_independent_backends(self):
        for values in VECTORS:
            seed,pk,msg,sig=map(bytes.fromhex,values)
            self.assertEqual(Ed25519PrivateKey.from_private_bytes(seed).sign(msg),sig)
            self.assertTrue(openssl_verify(pk,sig,msg));self.assertTrue(sodium_verify(pk,sig,msg))
    def test_adversarial_encodings_bytes_signatures_and_variants(self):
        for row in probe():
            if row['case'] in ('canonical-identity-small-order','noncanonical-negative-zero-key','noncanonical-y-identity-key'):continue
            with self.subTest(case=row['case']):self.assertEqual(row['openssl'],row['case']=='valid');self.assertEqual(row['libsodium'],row['case']=='valid')
    def test_record_backend_acceptance_difference_no_equivalence_claim(self):
        for row in probe()[-3:]:
            with self.subTest(case=row['case']):self.assertTrue(row['openssl']);self.assertFalse(row['libsodium'])
    def test_original_message_iterator_independent_small_signed_fixture(self):
        with tempfile.TemporaryDirectory() as d:
            job=make(Path(d)/'fixture');m=json.loads(job.read_bytes());b=job.parent
            exact=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+b''.join((b/n).read_bytes() for n in ('evidence.tsv','tokens.tsv','links.tsv'))
            for n in (1,2,7,65536):self.assertEqual(b''.join(signed_message(m,b,n)),exact)
            authority=json.loads((b/'external-appointment.json').read_bytes());sig=bytes.fromhex((b/'signature.txt').read_text().split()[1]);pk=bytes.fromhex(authority['public_key'])
            self.assertTrue(openssl_verify(pk,sig,exact));self.assertTrue(sodium_verify(pk,sig,exact))
    def test_changed_message_iterator_rejects(self):
        from link_recovery.cli import RecoveryError
        with tempfile.TemporaryDirectory() as d:
            job=make(Path(d)/'fixture');m=json.loads(job.read_bytes());p=job.parent/'tokens.tsv';b=p.read_bytes();p.write_bytes(b[:-1]+b'x')
            with self.assertRaises(RecoveryError):list(signed_message(m,job.parent,17))
if __name__=='__main__':unittest.main()
