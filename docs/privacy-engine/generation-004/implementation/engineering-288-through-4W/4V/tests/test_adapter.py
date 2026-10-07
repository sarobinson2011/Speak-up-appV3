import copy,hashlib,json,os,resource,shutil,sys,tempfile,time,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from adapter.core import *
from oracle import make,manifest,rows_wire,digest
class AdapterTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name);self.f=make(self.d/'inputs');self.key=self.d/'key';keygen(self.key);self.n=0
 def tearDown(self):self.tmp.cleanup()
 def new(self,kind='deterministic-laboratory-emitter',data=None,cap=257,expected=None):
  self.n+=1;p=self.d/f'job{self.n}';initialize(p,self.key,manifest(self.f,kind,data,expected),cap);return p
 def runjob(self,p,chunk=23,budget=None):
  with Job(p,self.key) as j:
   for _ in range(10000):
    r=j.step(budget,chunk);self.assertLessEqual(j.disk_bytes(),j.disk_bound())
    if r['result']!='PAUSED':return r,copy.deepcopy(j.state)
  self.fail('no termination')
 def good(self,r):
  self.assertTrue(r['complete']);self.assertEqual(r['whole_stream_sha256'],digest(self.f['text']));self.assertEqual((r['rows'],r['structural'],r['potential']),(self.f['rows'],self.f['structural'],self.f['potential']));self.assertFalse(r['actual_admission']);self.assertFalse(r['source_authenticated'])
 def test_independent_oracle_exact_emission_and_validation(self):
  p=self.new(cap=71);collected=[]
  with Job(p,self.key) as j:
   old=j.produce
   def capture(c,o):
    v=old(c,o);collected.append((p/'spool.bin').read_bytes());return v
   j.produce=capture
   while True:
    r=j.step(chunk_bytes=7)
    if r['complete']:break
  self.assertEqual(b''.join(collected),self.f['text']);self.good(r)
 def test_fixture_bytes_and_arbitrary_boundaries(self):
  for chunk in [1,2,7,67,4096]:
   with self.subTest(chunk=chunk):self.good(self.runjob(self.new('immutable-laboratory-file',cap=127),chunk)[0])
 def test_partial_header_rows_repeated_resume_and_eviction(self):
  p=self.new(cap=151)
  for b in [1,2,63,1,1,7,29]:
   with Job(p,self.key) as j:
    r=j.step(new_bytes=b,chunk_bytes=3);self.assertIsNone(r['whole_stream_sha256']);self.assertEqual(r['consumed_sha256'],digest(self.f['text'][:r['offset']]))
  r,s=self.runjob(p,chunk=1);self.good(r);self.assertGreater(s['metrics']['spools_evicted'],1);self.assertEqual(s['metrics']['evicted_prefix_bytes_reread'],0)
  with Job(p,self.key) as j:
   self.good(j.step());self.assertIsNone(j.emitter);self.assertIsNone(j.validator)
 def test_missing_current_spool_regenerated_from_bounded_cursor(self):
  p=self.new(cap=119)
  with Job(p,self.key) as j:j.step(3,2)
  (p/'spool.bin').unlink()
  with Job(p,self.key) as j:j.step(4,3)
  (p/'spool.bin').unlink()
  r,s=self.runjob(p);self.good(r);self.assertEqual(s['metrics']['spool_regenerations'],2);self.assertEqual(s['metrics']['regenerated_bytes'],238)
 def test_atomic_interruptions(self):
  for point in ['spool_fsynced','spool_published','after_write','after_fsync','after_replace','after_dir_fsync','validation_returned','eviction_committed']:
   with self.subTest(point=point):
    p=self.new(cap=121);hit=[]
    def crash(where):
     if where==point and not hit:hit.append(where);raise Interrupted(where)
    with self.assertRaises(Interrupted):
     with Job(p,self.key,crash) as j:j.step()
    self.assertEqual(hit,[point]);self.good(self.runjob(p)[0])
 def test_interrupted_validation_commit_preserves_partial_parser(self):
  p=self.new(cap=251)
  with Job(p,self.key) as j:j.step(83,5)
  for point in ['after_write','after_fsync','after_replace','after_dir_fsync']:
   def crash(where):
    if where==point:raise Interrupted(where)
   with self.assertRaises(Interrupted):
    with Job(p,self.key,crash) as j:j.step(7,2)
  self.good(self.runjob(p)[0])
 def test_malformed_streams_even_with_matching_byte_digest(self):
  r=self.f['required'];potential=next(x for x in r if x[2]=='000000');struct=next(x for x in r if x[2]!='000000')
  cases={
   'missing_potential':rows_wire([x for x in r if x!=potential]),
   'missing_structural':rows_wire([x for x in r if x!=struct]),
   'duplicate':rows_wire(sorted(r+[r[0]])),
   'wrong_orientation':rows_wire(sorted([x for x in r if x!=potential]+[(potential[1],potential[0],*potential[2:])])),
   'illegal_fixed_pair':rows_wire(sorted(r+[('z.last','a.first','000000','EQUALS')])),
   'unknown_endpoint':rows_wire(sorted(r+[('zz.unknown','z.last','000001','USES')])),
   'bad_relation':rows_wire(sorted(r+[('z.last','z.last','000099','BOGUS')])),
   'wrong_order':rows_wire(list(reversed(r))),
   'ordinal':self.f['text'].replace(b'000001\t',b'000002\t',1),
   'ordinal_padding':self.f['text'].replace(b'000001\t',b'1\t',1),
   'relation_padding':self.f['text'].replace(b'\t000000\t',b'\t0\t',1),
   'CRLF':self.f['text'].replace(b'\n',b'\r\n'),
   'BOM':b'\xef\xbb\xbf'+self.f['text'],
   'truncation':self.f['text'][:-1],
   'extra_tab':self.f['text'].replace(b'\t',b'\t\t',1),
   'extra_lf':self.f['text']+b'\n',
   'empty':b'',
   'same_cardinality_wrong_membership':rows_wire(sorted([x for x in r if x!=potential]+[('z.last','b.fixed','000000','EQUALS')]))}
  for name,data in cases.items():
   with self.subTest(case=name):
    out,_=self.runjob(self.new('immutable-laboratory-file',data,cap=91),chunk=11)
    self.assertEqual(out['result'],'REJECTED');self.assertIsNone(out['whole_stream_sha256'])
 def test_wrong_whole_digest_never_success(self):
  p=self.new(expected={'bytes':len(self.f['text']),'sha256':'0'*64});r,_=self.runjob(p);self.assertEqual(r['failure']['code'],'INVALID-EVIDENCE-DIGEST');self.assertIsNone(r['whole_stream_sha256'])
 def test_spool_mutation_rejected(self):
  p=self.new()
  with Job(p,self.key) as j:j.step(7)
  b=bytearray((p/'spool.bin').read_bytes());b[0]^=1;(p/'spool.bin').write_bytes(b)
  with self.assertRaises(Error):
   with Job(p,self.key) as j:j.step()
 def test_input_mutation_rejected_even_terminal(self):
  p=self.new('immutable-laboratory-file');self.good(self.runjob(p)[0]);(self.f['root']/'supplied.tsv').write_bytes(b'changed')
  with self.assertRaises(Error):Job(p,self.key)
 def test_descriptor_mutation(self):
  p=self.new();(self.f['root']/'descriptor.txt').write_text('changed')
  with self.assertRaises(Error):Job(p,self.key)
 def test_corrupt_and_cross_job_state(self):
  p=self.new();q=self.new();old=(p/'STATE.json').read_bytes();(p/'STATE.json').write_bytes((q/'STATE.json').read_bytes())
  with self.assertRaises(Error):Job(p,self.key)
  (p/'STATE.json').write_bytes(old.replace(b'PAUSED',b'FAILED'))
  with self.assertRaises(Error):Job(p,self.key)
  (p/'IDENTITY.json').write_bytes((q/'IDENTITY.json').read_bytes());(p/'STATE.json').write_bytes((q/'STATE.json').read_bytes())
  with self.assertRaises(Error):Job(p,self.key)
 def test_wrong_key_and_runtime_binding(self):
  p=self.new();key2=self.d/'key2';keygen(key2)
  with self.assertRaises(Error):Job(p,key2)
  identity=unseal(p/'IDENTITY.json',keyread(self.key));identity['code']['format']='other';atom(p/'IDENTITY.json',seal(identity,keyread(self.key)))
  with self.assertRaises(Error):Job(p,self.key)
 def test_worker_death_keeps_committed_prefix(self):
  p=self.new(cap=179)
  with Job(p,self.key) as j:
   j.step(80,13);j.validator.p.kill();j.validator.p.wait()
   with self.assertRaises((Error,BrokenPipeError)):j.step(13,3)
  self.good(self.runjob(p)[0])
 def test_binding_mutations_and_stale_code(self):
  for member in ['model.json','contract.json']:
   p=self.new();path=self.f['root']/member;old=path.read_bytes();path.write_bytes(old+b' ')
   with self.assertRaises(Error):Job(p,self.key)
   path.write_bytes(old)
  m=manifest(self.f);m['serialization']='binary-pairs'
  with self.assertRaises(Error):initialize(self.d/'invalid',self.key,m)
  p=self.new();identity=unseal(p/'IDENTITY.json',keyread(self.key));state=unseal(p/'STATE.json',keyread(self.key));identity['code']['files']['native/validator_service']='0'*64
  state['identity_sha256']=hashlib.sha256(wire(identity)).hexdigest();atom(p/'IDENTITY.json',seal(identity,keyread(self.key)));atom(p/'STATE.json',seal(state,keyread(self.key)))
  with self.assertRaisesRegex(Error,'incompatible code'):Job(p,self.key)
 def test_wrong_descriptor_semantics_rejects_matching_source_digest(self):
  # Exact same row bytes/hash; different legal model membership cannot pass.
  p=self.f['root']/'descriptor.txt';text=p.read_text();p.write_text(text.replace('0 0\n','0 1\n',1))
  job=self.new('immutable-laboratory-file');r,_=self.runjob(job);self.assertEqual(r['result'],'REJECTED')
 def test_caps_and_cleanup(self):
  with self.assertRaises(Error):self.new(cap=LIMIT+1)
  p=self.new(cap=101)
  with Job(p,self.key) as j:
   with self.assertRaises(Error):j.step(chunk_bytes=1048577)
   j.step(17,3);children=[j.emitter.p,j.validator.p]
   for service in [j.emitter,j.validator]:
    self.assertEqual(service.ready['address_space_limit'],1610612736);self.assertEqual(service.ready['file_size_limit'],268435456);self.assertEqual(service.ready['handle_limit'],64)
   self.assertLessEqual(resource.getrlimit(resource.RLIMIT_AS)[0],536870912)
  for child in children:self.assertIsNotNone(child.poll())
  self.good(self.runjob(p)[0])
if __name__=='__main__':unittest.main(verbosity=2)
