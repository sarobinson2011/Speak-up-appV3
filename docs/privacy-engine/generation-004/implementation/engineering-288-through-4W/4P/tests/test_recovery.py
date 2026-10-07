"""Small independent exhaustive oracle and destructive LOCAL recovery tests."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from link_recovery import cli as c


def independent_oracle():
    # Literal six-node model; no production predicate/serializer/generator used.
    names = ['Z', 'A', 'B', 'A-0', 'C', 'S.$record']
    fixed = {0: 'x', 1: 'y', 3: 'x'}
    edges = [(0, 1, 1, 'SOURCE'), (0, 1, 2, 'SOURCE'), (4, 2, 1, 'EQUALS'),
             (4, 2, 1, 'EQUALS')]
    structural = {(names[i], names[j], str(r).zfill(6), k) for i, j, r, k in edges}
    potential = set()
    for i in range(6):
        for j in range(i+1, 6):
            if i not in fixed or j not in fixed or fixed[i] == fixed[j]:
                potential.add((names[i], names[j], '000000', 'EQUALS'))
    def encode(rows):
        header = b'link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n'
        return header+b''.join(('\t'.join([str(n).zfill(6), *r])+'\n').encode('ascii')
                               for n, r in enumerate(rows, 1))
    rows = sorted(structural | potential)
    desc = ('LINKS 6 4 3\n'+'\n'.join(names)+'\n0 0\n1 1\n3 0\n'+
            ''.join(f'{i} {j} {r} {k}\n' for i,j,r,k in edges)).encode()
    return encode(rows), desc, rows, encode, len(structural), len(potential)


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.raw, desc, self.rows, self.encode, self.ns, self.np = independent_oracle()
        self.file = self.root/'input.tsv'; self.file.write_bytes(self.raw)
        self.model = self.root/'model.txt'; self.model.write_bytes(desc)
        self.contract = self.root/'contract.json'; self.contract.write_bytes(b'{"test_contract":"independent CP4C oracle only"}\n')
        self.key = self.root/'key'; c.create_key(self.key)
        self.ck = self.root/'checkpoint.json'
        self.a = argparse.Namespace(operation='start', key=self.key, checkpoint=self.ck,
            input=self.file, input_sha256=hashlib.sha256(self.raw).hexdigest(),
            model=self.model, model_sha256=c.sha(self.model), contract=self.contract,
            contract_sha256=c.sha(self.contract), chunk_bytes=71, new_bytes=1000000, seconds=10)
    def tearDown(self): self.tmp.cleanup()
    def start(self, cut=None):
        self.a.operation='start'
        if cut is not None: self.a.new_bytes=cut
        return c.execute(self.a)
    def resume(self, budget=1000000, chunk=71):
        a=argparse.Namespace(**vars(self.a));a.operation='resume';a.new_bytes=budget;a.chunk_bytes=chunk
        for k in ('input','input_sha256','model','model_sha256','contract','contract_sha256'):setattr(a,k,None)
        return c.execute(a)
    def state(self): return c.load(self.ck,c.read_key(self.key))
    def assert_good(self,r):
        self.assertTrue(r['complete'],r);self.assertEqual(r['complete_stream_sha256'],hashlib.sha256(self.raw).hexdigest())
        self.assertEqual((r['structural_rows'],r['potential_rows']),(self.ns,self.np))
        self.assertFalse(r['profile_admitted']);self.assertFalse(r['actual_qualification_established'])
    def test_independent_uninterrupted_oracle(self): self.assert_good(self.start())
    def test_every_byte_pause_position_and_hash_block_boundary(self):
        for cut in range(1,len(self.raw)+1):
            self.ck.unlink(missing_ok=True)
            with self.subTest(cut=cut):
                r=self.start(cut);self.assertEqual(r['result'],'PAUSED');self.assertIsNone(r['complete_stream_sha256'])
                s=self.state()['state'];self.assertEqual(s['offset'],cut)
                self.assertEqual(s['prefix_sha256'],hashlib.sha256(self.raw[:cut]).hexdigest())
                self.assertEqual(bytes.fromhex(s['pending']),self.raw[:cut].rsplit(b'\n',1)[-1])
                self.assertEqual(len(bytes.fromhex(s['sha_block'])),cut%64)
                self.assert_good(self.resume(chunk=1+(cut%97)))
    def test_repeated_single_byte_resume(self):
        self.start(1)
        for offset in range(2,len(self.raw)+1):
            r=self.resume(1,1);self.assertEqual(r['bytes_consumed'],offset);self.assertIsNone(r['complete_stream_sha256'])
        self.assert_good(self.resume(1,1))
    def test_repeated_random_resume_sizes(self):
        rnd=random.Random(288);r=self.start(2)
        while not r['complete']:r=self.resume(rnd.randint(1,93),rnd.randint(1,127))
        self.assert_good(r)
    def test_4b_fixture_matches_exact_4b_hash(self):
        self.file.write_bytes((c.ROOT/'fixtures/link-oracle.tsv').read_bytes())
        self.raw=self.file.read_bytes();self.model.write_bytes((c.ROOT/'fixtures/link-oracle.model').read_bytes())
        self.a.input_sha256=c.sha(self.file);self.a.model_sha256=c.sha(self.model);self.ns=4;self.np=24
        self.start(123);self.assert_good(self.resume(10000,17))
    def test_changed_prefix_same_size_and_restored_mtime(self):
        self.start(100);before=self.file.stat();raw=bytearray(self.raw);raw[10]^=1;self.file.write_bytes(raw)
        os.utime(self.file,ns=(before.st_atime_ns,before.st_mtime_ns))
        old=self.ck.read_bytes()
        with self.assertRaisesRegex(c.RecoveryError,'prefix changed'):self.resume()
        self.assertEqual(self.ck.read_bytes(),old)
    def test_changed_unread_suffix_is_rejected(self):
        self.start(100);raw=bytearray(self.raw);raw[-2]=ord('X');self.file.write_bytes(raw)
        r=self.resume();self.assertEqual(r['result'],'REJECTED');self.assertIsNone(r['complete_stream_sha256'])
    def test_changed_input_size_and_missing_file(self):
        self.start(100);self.file.write_bytes(self.raw[:-1])
        with self.assertRaises(c.RecoveryError):self.resume()
        self.file.unlink()
        with self.assertRaises(FileNotFoundError):self.resume()
    def test_whole_expected_hash_mismatch_has_no_complete_digest(self):
        self.a.input_sha256='0'*64;self.start(100);r=self.resume()
        self.assertEqual(r['failure']['code'],'INVALID-EVIDENCE-DIGEST');self.assertIsNone(r['complete_stream_sha256'])
    def test_changed_model_and_contract(self):
        self.start(100);original=self.model.read_bytes();self.model.write_bytes(original+b'\n')
        with self.assertRaises(c.RecoveryError):self.resume()
        self.model.write_bytes(original);self.contract.write_bytes(b'{}')
        with self.assertRaisesRegex(c.RecoveryError,'contract changed'):self.resume()
    def test_corrupt_truncated_and_forged_journals(self):
        self.start(100);original=self.ck.read_bytes()
        for raw in (original[:-1-7],b'',b'not json',original.replace(b'"offset":100',b'"offset":101'),original+b'x'):
            self.ck.write_bytes(raw)
            with self.assertRaises(c.RecoveryError):self.resume()
        self.ck.write_bytes(original);p=json.loads(original);p['payload']['state']['potential']+=1
        self.ck.write_bytes(json.dumps(p).encode())
        with self.assertRaisesRegex(c.RecoveryError,'authentication failed'):self.resume()
    def test_wrong_key_and_wrong_validator(self):
        self.start(100);key=self.key.read_bytes();self.key.write_bytes(b'Z'*32)
        with self.assertRaisesRegex(c.RecoveryError,'authentication failed'):self.resume()
        self.key.write_bytes(key)
        with patch.object(c,'validator_identity',return_value={'version':'OTHER'}):
            with self.assertRaisesRegex(c.RecoveryError,'incompatible'):self.resume()
    def test_incompatible_format_even_with_valid_local_mac(self):
        self.start(100);p=self.state();p['format']='OTHER';c.atomic_save(self.ck,p,c.read_key(self.key))
        with self.assertRaisesRegex(c.RecoveryError,'incompatible'):self.resume()
    def test_native_rejects_internally_inconsistent_sha_state(self):
        self.start(100);p=self.state();p['state']['sha_h'][0]^=1;c.atomic_save(self.ck,p,c.read_key(self.key))
        with self.assertRaises(c.RecoveryError):self.resume()
    def test_malformed_and_missing_rows_retain_4b_failures(self):
        candidates=[self.raw[:-1],self.encode(self.rows[:-1]),self.raw+b'\n',
                    self.raw.replace(b'000001\t',b'000002\t',1),
                    self.encode(self.rows[:2]+[self.rows[1]]+self.rows[3:]),
                    self.raw.replace(b'000000\tEQUALS',b'000000\tSOURCE',1),
                    self.raw.replace(b'\n',b'\r\n'),b'\xef\xbb\xbf'+self.raw,b'']
        for raw in candidates:
            self.ck.unlink(missing_ok=True);self.file.write_bytes(raw);self.a.input_sha256=c.sha(self.file)
            r=self.start(1)
            if r['result']=='PAUSED':r=self.resume(chunk=3)
            self.assertEqual(r['result'],'REJECTED',r);self.assertIsNone(r['complete_stream_sha256'])
            with self.assertRaisesRegex(c.RecoveryError,'terminal rejected'):self.resume()
    def test_separate_structural_potential_completeness(self):
        for remove in ('000000','000001'):
            rows=[r for r in self.rows if r[2]!=remove];self.file.write_bytes(self.encode(rows));self.a.input_sha256=c.sha(self.file)
            self.ck.unlink(missing_ok=True);self.start(67);r=self.resume()
            self.assertEqual(r['failure']['code'],'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_read_ahead_on_rejection_is_not_resumable(self):
        raw=b'BAD\n'+self.raw;self.file.write_bytes(raw);self.a.input_sha256=c.sha(self.file);self.a.chunk_bytes=17
        r=self.start();self.assertEqual(r['bytes_consumed'],17)
        self.assertEqual(r['consumed_sha256'],hashlib.sha256(raw[:17]).hexdigest());self.assertIsNone(self.state()['state'])
    def test_interrupted_atomic_writes_previous_or_next_valid(self):
        self.start(99);old=self.ck.read_bytes()
        # Abrupt child process death: no Python finally cleanup, real fsync/rename calls.
        for stage in ('after_write','after_file_fsync','after_replace','after_dir_fsync'):
            self.ck.write_bytes(old)
            program='''from pathlib import Path
import os,sys
from link_recovery import cli as c
p=Path(sys.argv[1]);key=c.read_key(sys.argv[2]);state=c.load(p,key);state['sequence']+=1
def crash(stage):
 if stage==sys.argv[3]:os._exit(87)
c.atomic_save(p,state,key,fault=crash)
'''
            run=subprocess.run([sys.executable,'-c',program,str(self.ck),str(self.key),stage],cwd=c.ROOT,timeout=10)
            self.assertEqual(run.returncode,87);self.assertIn(self.state()['sequence'],(1,2))
            self.assert_good(self.resume())
    def test_abandoned_part_not_promoted(self):
        self.start(50);(self.root/'.checkpoint.json.fake.part').write_bytes(b'forged incomplete next checkpoint')
        self.assert_good(self.resume())
    def test_initial_committed_zero_state_recovers(self):
        self.start(50);p=self.state();p.update(sequence=0,state=c.initial_state(),result=None)
        c.atomic_save(self.ck,p,c.read_key(self.key));self.assert_good(self.resume())
    def test_completed_journal_rechecks_entire_input(self):
        self.assert_good(self.start());self.assert_good(self.resume());self.file.write_bytes(b'X'+self.raw[1:])
        with self.assertRaisesRegex(c.RecoveryError,'prefix changed'):self.resume()
    def test_prefix_deadline_leaves_journal(self):
        self.start(100);before=self.ck.read_bytes()
        with self.file.open('rb') as f:
            with self.assertRaisesRegex(c.RecoveryError,'deadline'):c.verify_prefix(f.fileno(),100,'0'*64,0)
        self.assertEqual(self.ck.read_bytes(),before);self.assert_good(self.resume())
    def test_resume_binding_override_and_concurrent_writer_rejected(self):
        import fcntl
        self.start(100);self.a.operation='resume'
        with self.assertRaisesRegex(c.RecoveryError,'overrides forbidden'):c.execute(self.a)
        with open(str(self.ck)+'.lock','a+b') as f:
            fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
            with self.assertRaisesRegex(c.RecoveryError,'already in use'):self.resume()
    def test_owner_only_key_permissions(self):
        os.chmod(self.key,0o644)
        with self.assertRaisesRegex(c.RecoveryError,'owner-only'):self.start()
    def test_original_4b_failure_precedence_matches_resumed(self):
        from link_stream.cli import native
        cases=[self.raw[:-1],self.encode(self.rows[:-1]),self.raw+b'\n',
               self.raw.replace(b'000001\t',b'000002\t',1),
               self.encode(self.rows[:2]+[self.rows[1]]+self.rows[3:]),
               self.raw.replace(b'000000\tEQUALS',b'000000\tSOURCE',1),
               self.raw.replace(b'\n',b'\r\n'),b'\xef\xbb\xbf'+self.raw,b'']
        for raw in cases:
            self.ck.unlink(missing_ok=True);self.file.write_bytes(raw);self.a.input_sha256=c.sha(self.file)
            original=native(self.file,self.model,self.a.model_sha256,self.a.input_sha256,3,len(raw)+1,10)
            r=self.start(1)
            if r['result']=='PAUSED':r=self.resume(chunk=3)
            self.assertEqual(r['failure']['code'],original['failure']['code'])
            self.assertEqual(r['rows_validated'],original['rows_validated'])
    def test_process_kill_after_initial_commit_is_recoverable(self):
        import signal
        self.start(50);p=self.state();p.update(sequence=0,state=c.initial_state(),result=None)
        # Persist via child, SIGKILL immediately after the durable commit.
        payload=self.root/'zero.json';payload.write_text(json.dumps(p))
        program='''import json,os,signal,sys
from pathlib import Path
from link_recovery import cli as c
c.atomic_save(Path(sys.argv[1]),json.loads(Path(sys.argv[3]).read_text()),c.read_key(sys.argv[2]))
os.kill(os.getpid(),signal.SIGKILL)
'''
        run=subprocess.run([sys.executable,'-c',program,str(self.ck),str(self.key),str(payload)],cwd=c.ROOT,timeout=10)
        self.assertEqual(run.returncode,-signal.SIGKILL);self.assert_good(self.resume())


if __name__=='__main__':unittest.main()
