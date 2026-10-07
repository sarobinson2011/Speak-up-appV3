import hashlib,io,json,pathlib,random,subprocess,tempfile,types,unittest
from link_stream.validator import ModelIndex,validate_reader,validate_chunks,HEADER
from link_stream.cli import native,sha,ROOT,DESC

def oracle():
 # Independent explicit model, tuple-set enumeration, and byte serializer.
 # No production generator, membership routine, formatter or classifier is used.
 names=['Z','A','AA','A-0','A0','B','M','C']
 fixed={0:0,1:1,3:0,6:1}
 raw_edges=[(0,1,1,'REFERENCES'),(0,1,2,'REFERENCES'),(2,0,3,'SOURCE'),(5,4,1,'EQUALS'),(0,1,1,'REFERENCES')]
 structural={(names[a],names[b],str(r).rjust(6,'0'),k) for a,b,r,k in raw_edges}
 potential={(names[i],names[j],'000000','EQUALS') for i in range(len(names)) for j in range(i+1,len(names)) if i not in fixed or j not in fixed or fixed[i]==fixed[j]}
 rows=sorted(structural|potential)
 def encode(rows):return b'link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n'+b''.join(('\t'.join([str(k).rjust(6,'0'),*r])+'\n').encode() for k,r in enumerate(rows,1))
 model=types.SimpleNamespace(ids={n:i for i,n in enumerate(names)},structural=structural,pair_count=len(potential))
 model.potential=lambda i,j:0<=i<j<len(names) and (i not in fixed or j not in fixed or fixed[i]==fixed[j])
 descriptor=(f'LINKS {len(names)} {len(raw_edges)} {len(fixed)}\n'+'\n'.join(names)+'\n'+''.join(f'{i} {g}\n' for i,g in fixed.items())+''.join(f'{i} {j} {r} {k}\n' for i,j,r,k in raw_edges)).encode()
 return model,rows,encode,descriptor,potential,structural

class Streams(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.model,cls.rows,cls.encode,cls.desc,cls.potential,cls.structural=oracle();cls.raw=cls.encode(cls.rows);cls.encode=staticmethod(cls.encode);cls.index=ModelIndex(cls.model)
 def call(self,b,chunk=31,expected=None):return validate_reader(io.BytesIO(b),self.index,expected,chunk)
 def assertbad(self,b):
  r=self.call(b);self.assertFalse(r['complete'],r);self.assertIsNone(r['complete_stream_sha256']);self.assertEqual(r['consumed_sha256'],hashlib.sha256(b[:r['bytes_consumed']]).hexdigest());return r
 def test_independent_exhaustive_oracle_complete(self):
  r=self.call(self.raw,1);self.assertTrue(r['complete'],r);self.assertEqual(r['complete_stream_sha256'],hashlib.sha256(self.raw).hexdigest());self.assertEqual(r['potential_rows'],len(self.potential));self.assertEqual(r['structural_rows'],len(self.structural))
 def test_every_two_chunk_boundary_and_random_partitions(self):
  for k in range(len(self.raw)+1):
   r=validate_chunks([self.raw[:k],b'',self.raw[k:]],self.index);self.assertTrue(r['complete'],(k,r))
  for seed in range(50):
   rnd=random.Random(seed);chunks=[];i=0
   while i<len(self.raw):j=i+rnd.randint(1,103);chunks.append(self.raw[i:j]);i=j
   self.assertTrue(validate_chunks(chunks,self.index)['complete'])
 def test_missing_each_structural_and_potential_row(self):
  for k in range(len(self.rows)):
   r=self.assertbad(self.encode(self.rows[:k]+self.rows[k+1:]));self.assertEqual(r['failure']['code'],'INCOMPLETE-EVIDENCE-UNIVERSE')
 def test_duplicate_every_row_even_when_count_kept_constant(self):
  for k in range(len(self.rows)-1):self.assertbad(self.encode(self.rows[:k+1]+[self.rows[k]]+self.rows[k+2:]))
 def test_cardinality_alone_counterexamples_illegal_replacement(self):
  bads=[('A','Z','000000','EQUALS'),('Z','A','000000','EQUALS'),('Z','A','000003','REFERENCES'),('ORPHAN','A','000001','SOURCE'),('Z','A','000001','WRONG'),('Z','A','000000','SOURCE')]
  for bad in bads:
   candidate=sorted(self.rows[1:]+[bad]);self.assertEqual(len(candidate),len(self.rows));self.assertbad(self.encode(candidate))
 def test_reverse_numeric_orientation_while_lexically_sorted(self):
  r=next(x for x in self.rows if x[2]=='000000');bad=(r[1],r[0],*r[2:]);self.assertbad(self.encode(sorted([bad if x==r else x for x in self.rows])))
 def test_structural_reverse_not_symmetric(self):
  r=('Z','A','000001','REFERENCES');self.assertbad(self.encode(sorted([('A','Z',r[2],r[3]) if x==r else x for x in self.rows])))
 def test_wrong_order_and_ordinals(self):
  rows=self.rows[:];rows[0],rows[1]=rows[1],rows[0];self.assertbad(self.encode(rows))
  for ordinal in (b'1',b'000000',b'000002',b'0000001',b'+00001',b'\xff00001'):
   self.assertbad(self.raw.replace(b'000001\t',ordinal+b'\t',1))
 def test_minimum_width_spelling_above_six_digits(self):
  from v4_ingest.wire import row_order
  self.assertEqual(row_order(999999),'999999');self.assertEqual(row_order(1000000),'1000000')
 def test_malformed_framing(self):
  for b in (b'',b'\xef\xbb\xbf'+self.raw,self.raw.replace(b'\n',b'\r\n'),self.raw+b'\n',self.raw.replace(b'\t',b' ',1),self.raw.replace(b'Z\t',b'Z \t'),self.raw.replace(b'Z\t',b'\xc3\xa9\t'),self.raw.replace(b'EQUALS',b'EQUALS\tEXTRA',1),self.raw.replace(b'EQUALS',b'\x00',1),HEADER+b'x'*10000):self.assertbad(b)
 def test_every_byte_truncation_no_complete_digest(self):
  for k in range(len(self.raw)):self.assertbad(self.raw[:k])
 def test_changed_bytes_and_expected_digest(self):
  self.assertTrue(self.call(self.raw,13,hashlib.sha256(self.raw).hexdigest())['complete'])
  r=self.call(self.raw,13,'0'*64);self.assertFalse(r['complete']);self.assertTrue(r['eof_observed']);self.assertIsNone(r['complete_stream_sha256']);self.assertEqual(r['failure']['code'],'INVALID-EVIDENCE-DIGEST')
 def test_never_read_unbounded_and_read_ahead_is_accounted(self):
  class R(io.BytesIO):
   def read(self,n=-1):assert 0<n<=17;return super().read(n)
  self.assertTrue(validate_reader(R(self.raw),self.index,chunk_bytes=17)['complete'])
  bad=b'BAD\n'+self.raw;r=validate_reader(io.BytesIO(bad),self.index,chunk_bytes=17);self.assertEqual(r['bytes_consumed'],17);self.assertEqual(r['consumed_sha256'],hashlib.sha256(bad[:17]).hexdigest());self.assertFalse(r['eof_observed'])
 def test_reader_io_error_does_not_make_prefix_complete(self):
  def chunks():
   yield HEADER
   raise OSError('interrupted acquisition')
  r=validate_chunks(chunks(),self.index);self.assertFalse(r['eof_observed']);self.assertIsNone(r['complete_stream_sha256']);self.assertEqual(r['consumed_sha256'],hashlib.sha256(HEADER).hexdigest())
 def test_occurrence_values_have_separate_complete_equality_set(self):
  values={n:(b'X' if i<3 else str(i).encode()) for n,i in self.model.ids.items()}
  rows=set(self.structural)
  for a,i in self.model.ids.items():
   for b,j in self.model.ids.items():
    if i<j and values[a]==values[b]:rows.add((a,b,'000000','EQUALS'))
  r=validate_reader(io.BytesIO(self.encode(sorted(rows))),ModelIndex(self.model,'E',values));self.assertTrue(r['complete']);self.assertEqual(r['potential_rows'],3)

class NativeStreams(Streams):
 @classmethod
 def setUpClass(cls):
  super().setUpClass();cls.tmp=tempfile.TemporaryDirectory();cls.base=pathlib.Path(cls.tmp.name);cls.dp=cls.base/'model.txt';cls.dp.write_bytes(cls.desc)
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def call(self,b,chunk=31,expected=None):
  p=self.base/'input.tsv';p.write_bytes(b);return native(p,self.dp,hashlib.sha256(self.desc).hexdigest(),expected,chunk,max(len(b)+1,1))
 # Python tests inherited above exercise its API where they call that API directly;
 # native-specific exhaustive chunk/truncation cases below have explicit receipts.
 def test_native_chunk_sizes(self):
  for chunk in list(range(1,100))+[127,256,65536]:self.assertTrue(self.call(self.raw,chunk)['complete'])
 def test_descriptor_changed_bytes_rejected(self):
  p=self.base/'input.tsv';p.write_bytes(self.raw);r=native(p,self.dp,'0'*64);self.assertFalse(r['complete']);self.assertEqual(r['bytes_consumed'],0)
 def test_byte_budget_no_digest_for_unobserved_eof(self):
  p=self.base/'input.tsv';p.write_bytes(self.raw);r=native(p,self.dp,hashlib.sha256(self.desc).hexdigest(),max_bytes=len(self.raw));self.assertFalse(r['complete']);self.assertFalse(r['eof_observed']);self.assertEqual(r['consumed_sha256'],hashlib.sha256(self.raw).hexdigest())
 def test_complete_retained_model_index_with_header_only(self):
  # Reads complete saved descriptor; supplies no pair rows and generates none.
  p=self.base/'header.tsv';p.write_bytes(HEADER);r=native(p,seconds=50)
  self.assertFalse(r['complete']);self.assertEqual(r['model_tokens'],426984);self.assertEqual(r['expected_potential_rows'],91157453467);self.assertEqual(r['descriptor_sha256'],DESC);self.assertIsNone(r['complete_stream_sha256'])
  (ROOT/'results/full-model-index-test.json').write_text(json.dumps(r,indent=2)+'\n')

class ModelIdentityTests(unittest.TestCase):
 def test_exact_source_defined_dollar_record_identity_is_not_primitive_id(self):
  model,rows,encode,desc,_,_=oracle()
  old='M';new='SECURITY:ALGORITHM.$record'
  model.ids[new]=model.ids.pop(old)
  rows=[tuple(new if v==old else v for v in r) for r in rows]
  model.structural={tuple(new if v==old else v for v in r) for r in model.structural}
  raw=encode(sorted(rows));index=ModelIndex(model)
  r=validate_reader(io.BytesIO(raw),index,chunk_bytes=1);self.assertTrue(r['complete'],r)
  with tempfile.TemporaryDirectory() as td:
   d=pathlib.Path(td)/'descriptor';d.write_bytes(desc.replace(b'\nM\n',b'\n'+new.encode()+b'\n'));p=d.with_suffix('.tsv');p.write_bytes(raw)
   self.assertTrue(native(p,d,sha(d),chunk_bytes=1)['complete'])
  # Only exact model membership admits that spelling; arbitrary extra syntax fails.
  r=validate_reader(io.BytesIO(raw.replace(new.encode(),b'SECURITY:ALGORITHM.$other')),index)
  self.assertFalse(r['complete'])
