import unittest,tempfile,json,copy,shutil
from pathlib import Path
from unittest.mock import patch
from metadata_catalog.core import acquire,write_directory,wire,sha,DiskMap,FORMAT
from metadata_catalog.adapters import MARK
from integrated_auth.collector import Paused
from link_recovery.cli import create_key
from recovery_schedule.state import Scheduler
from recovery_schedule.runner import run
from fixtures.catalogs import export

class CatalogTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.p=Path(self.tmp.name);self.key=b'x'*32;self.binding={'source':'independent-fixture','phase':'E'};self.rows=[('A',{'v':1}),('B',{'v':2}),('C',{'v':3})]
  self.e=write_directory(self.p/'rows','test',self.binding,self.rows,3)
 def get(self,**kw):return acquire(self.p/'rows',self.e,'test',self.binding,self.p/'index',self.key,{'job':'one'},**kw)
 def test_exact_small_oracle_repeated_resume(self):
  for _ in range(2):
   with self.assertRaises(Paused):self.get(stop_after=1)
  x=self.get();self.assertEqual(dict(x.items()),dict(self.rows));x.close();self.assertEqual(dict(self.get().items()),dict(self.rows))
 def test_malformed_duplicate_missing_extra_conflict_order(self):
  header={'format':FORMAT,'kind':'test','binding':self.binding,'count':3}
  for rows in (self.rows[:2],self.rows+[('D',{})],[self.rows[0]]*3,[self.rows[1],self.rows[0],self.rows[2]],[self.rows[0],('A',{'v':2}),self.rows[2]]):
   with self.subTest(rows=rows):
    raw=wire(header)+b''.join(wire(list(r)) for r in rows);(self.p/'rows').write_bytes(raw);self.e.update(bytes=len(raw),sha256=sha(self.p/'rows'))
    with self.assertRaises(ValueError):self.get()
 def test_canonical_and_truncation(self):
  original=(self.p/'rows').read_bytes()
  for raw in (original[:-1],original.replace(b'"count":3',b'"count": 3'),original+b'\n',original.replace(b'"v":1',b'"v":1,"v":1')):
   (self.p/'rows').write_bytes(raw);self.e.update(bytes=len(raw),sha256=sha(self.p/'rows'))
   with self.assertRaises(ValueError):self.get()
 def test_input_mutation_checkpoint_and_database_corruption(self):
  with self.assertRaises(Paused):self.get(stop_after=1)
  original=(self.p/'rows').read_bytes();(self.p/'rows').write_bytes(original.replace(b'"v":1',b'"v":9'))
  with self.assertRaises(ValueError):self.get()
  (self.p/'rows').write_bytes(original);ck=next((self.p/'index').glob('*.json'));data=ck.read_bytes();ck.write_bytes(data[:-1]+b'x')
  with self.assertRaises(ValueError):self.get()
  ck.write_bytes(data);obj=json.loads(data)['payload'];db=self.p/'index'/obj['database'];db.write_bytes(b'bad')
  with self.assertRaises(ValueError):self.get()
 def test_atomic_checkpoint_interruption(self):
  import link_recovery.cli as c
  original=c.atomic_save
  def fail(path,p,key,*a,**kw):
   if p.get('count')==2:raise OSError('before pointer publication')
   return original(path,p,key,*a,**kw)
  with self.assertRaises(Paused):self.get(stop_after=1)
  with patch.object(c,'atomic_save',fail),self.assertRaises(OSError):self.get(stop_after=1)
  x=self.get();self.assertEqual(dict(x.items()),dict(self.rows))
 def test_bound_job_substitution(self):
  self.get();old=next((self.p/'index').glob('*.json'));raw=old.read_bytes()
  # Copy the old signed state under another job's derived filename.
  ident={'file':self.e,'kind':'test','binding':self.binding,'job':{'job':'two'}}
  import hashlib
  target=self.p/'index'/(hashlib.sha256(wire(ident)).hexdigest()+'.json');target.write_bytes(raw)
  with self.assertRaises(ValueError):acquire(self.p/'rows',self.e,'test',self.binding,self.p/'index',self.key,{'job':'two'})
 def case(self,phase='E'):
  m,t=export(self.p/'fixture',phase=phase);create_key(self.p/'key');return m,t
 def test_integrated_all_phases_and_terminal_reuse(self):
  for phase in ('E','PRE-EXECUTION','PRE-COMMITMENT'):
   with self.subTest(phase=phase):
    p=self.p/phase;m,t=export(p,phase=phase);create_key(p/'key');r=run(m,t,p/'journal',p/'key');self.assertFalse(r['failures'],r['reasons']);self.assertFalse(r['profile_admitted'])
    oracle=json.loads((p/'oracle.json').read_bytes())
    for scope,e in oracle.items():self.assertEqual(r['bindings']['scope_validation']['scopes'][scope]['link_validation']['complete_stream_sha256'],e['links_sha256'])
    q=run(m,t,p/'journal',p/'key',resume=True);self.assertTrue(q['stage_schedule']['terminal_reused']);self.assertEqual(q['result'],r['result'])
 def test_integrated_repeated_interruption(self):
  m,t=self.case()
  for i,n in enumerate((1,37,67108864)):
   r=run(m,t,self.p/'j',self.p/'key',resume=i>0,new_bytes=n)
   self.assertEqual(r['processing_complete'],i==2)
  self.assertFalse(r['failures'],r['reasons'])
 def test_missing_extra_wrong_occurrence_refs(self):
  for kind in ('missing','extra','owner','ref','phase'):
   p=self.p/kind;m,t=export(p);create_key(p/'key');mm=json.loads(m.read_bytes());tt=json.loads(t.read_bytes());e=mm['request']['occurrence_bindings'][MARK];lines=[json.loads(b) for b in (p/e['path']).read_bytes().splitlines()];header=lines[0];rows=lines[1:]
   if kind=='missing':rows.pop()
   if kind=='extra':rows.append(['ZZ-ABSENT',rows[0][1]])
   if kind=='owner':rows[0][1]['owner_source_id']='WRONG'
   if kind=='ref':rows[0][1]['material_sha256']='0'*64
   if kind=='phase':header['binding']['phase']='WRONG'
   header['count']=len(rows);raw=wire(header)+b''.join(wire(r) for r in rows);(p/e['path']).write_bytes(raw);e.update(bytes=len(raw),sha256=sha(p/e['path']));tt['occurrence_bindings']=mm['request']['occurrence_bindings'];m.write_bytes(wire(mm));t.write_bytes(wire(tt))
   try:r=run(m,t,p/'j',p/'key');self.assertTrue(r['failures'],kind)
   except ValueError:pass
 def test_directory_mutation_and_source_substitution(self):
  m,t=self.case();r=run(m,t,self.p/'j',self.p/'key');self.assertFalse(r['failures'])
  p=m.parent/'materials.jsonl';p.write_bytes(p.read_bytes()+b'\n')
  r=run(m,t,self.p/'j',self.p/'key',resume=True);self.assertTrue(r['failures']);self.assertFalse(r['profile_admitted'])
 def test_external_receipt_maps_and_prerequisite_substitution(self):
  create_key(self.p/'key');s=Scheduler(self.p/'j',self.p/'key',{'job':'one'});self.addCleanup(s.close)
  a=DiskMap(self.p/'many.sqlite');self.addCleanup(a.close)
  for i in range(20000):a[str(i)]='a'*64
  s.save('first',{}, {'ok':True},True)
  s.save('terminal',{'files':a},{'ok':True},True,{'first':s.receipts['first']},a)
  receipt=s.root/(s.name('terminal')+'.json');self.assertLess(receipt.stat().st_size,4096)
  old=s.read('terminal');self.assertEqual(len(old['inputs']['files']),20000)
  raw=json.loads(receipt.read_bytes());e=raw['payload']['prerequisites']['$cp4m_execution_catalog'];db=s.root/e['path'];db.write_bytes(b'changed')
  # A new invocation must not reuse the per-invocation trusted quiescence cache.
  s2=Scheduler(self.p/'j',self.p/'key',{'job':'one'});self.addCleanup(s2.close)
  with self.assertRaises(ValueError):s2.read('terminal')

 def test_controlled_tick_pause_keeps_committed_rows(self):
  n=0
  def tick():
   nonlocal n
   n+=1
   if n==2:raise Paused()
  with self.assertRaises(Paused):self.get(tick=tick)
  ck=json.loads(next((self.p/'index').glob('*.json')).read_bytes())['payload'];self.assertEqual(ck['count'],1)
  self.assertEqual(dict(self.get().items()),dict(self.rows))
 def test_header_all_binding_dimensions(self):
  for field in ('source','phase','model','profile','contract'):
   bad={**self.binding,field:'wrong'}
   with self.assertRaises(ValueError):acquire(self.p/'rows',self.e,'test',bad,self.p/('bad-'+field),self.key,{'job':'one'})
 def test_oversized_and_non_ascii_or_duplicate_json_keys(self):
  raw=(self.p/'rows').read_bytes();header=raw.splitlines(keepends=True)[0]
  for bad in (header+b'["A","'+b'x'*65536+b'"]\n',header+b'["A",{"v":1,"v":2}]\n',header+b'["A","\xc3\xa9"]\n'):
   (self.p/'rows').write_bytes(bad);self.e.update(bytes=len(bad),sha256=sha(self.p/'rows'))
   with self.assertRaises(ValueError):self.get()
 def test_caller_source_directory_cannot_override_trusted(self):
  m,t=self.case();mm=json.loads(m.read_bytes());e=mm['materials'][MARK];p=m.parent/e['path'];lines=p.read_bytes().splitlines(keepends=True);header=json.loads(lines[0]);header['count']-=1;raw=wire(header)+b''.join(lines[2:]);p.write_bytes(raw);e.update(bytes=len(raw),sha256=sha(p));m.write_bytes(wire(mm))
  try:r=run(m,t,self.p/'j',self.p/'key');self.assertTrue(r['failures'])
  except ValueError:pass
 def test_real_terminal_prerequisite_substitution(self):
  m,t=self.case();r=run(m,t,self.p/'j',self.p/'key');self.assertFalse(r['failures']);root=Path(str(self.p/'j')+'.stages')
  receipts=[p for p in root.glob('*.json') if json.loads(p.read_bytes()).get('payload',{}).get('label','').startswith('acquisition:')];self.assertGreater(len(receipts),1);receipts[0].write_bytes(receipts[1].read_bytes())
  with self.assertRaises(ValueError):run(m,t,self.p/'j',self.p/'key',resume=True)
 def test_receipt_snapshot_exact_both_maps(self):
  from metadata_catalog.receipts import freeze,MARK as RM
  a=DiskMap(self.p/'a');b=DiskMap(self.p/'b');self.addCleanup(a.close);self.addCleanup(b.close)
  for i in range(4097):a[str(i)]={'left':i};b[str(i)]={'right':i}
  for src in (a,b,a):
   e=freeze(src,self.p)[RM];x=DiskMap(self.p/e['path'],True);self.assertEqual(list(x.items()),list(src.items()));self.assertEqual(len(src),4097)
