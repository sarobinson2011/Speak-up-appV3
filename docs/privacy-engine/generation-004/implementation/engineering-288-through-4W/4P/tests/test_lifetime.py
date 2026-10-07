import unittest,tempfile,json,os,resource,subprocess,sys,copy
from pathlib import Path
from unittest.mock import patch
from semantic_stream.storage import Store,ACTIVE,Document
from semantic_stream.lifetime import ByteLRU,BoundedLog
from fixtures.construct import wire,sha,dataset
from fixtures.lifetime import export
from recovery_schedule.runner import run
from recovery_schedule.state import Scheduler
from link_recovery.cli import create_key,PauseRequested

class LifetimeTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.p=Path(self.tmp.name)
 def store(self):
  s=Store(self.p);self.addCleanup(s.close);return s
 def test_small_oracle_many_documents_and_repeated_eviction(self):
  s=self.store();blobs=[]
  for i in range(128):
   raw=wire({'i':i,'values':[None,True,str(i)]});b=s.write([raw]);blobs.append(b);self.assertEqual(s.parse(b),json.loads(raw))
  for cycle in range(3):
   for i in reversed(range(len(blobs))):self.assertEqual(s.parse(blobs[i])['i'],i)
   self.assertLessEqual(len(s.pool.data),4)
  self.assertEqual(s.documents_built,128);self.assertGreater(s.pool.evictions,100);self.assertEqual(len(s.docs),0)
 def test_live_lazy_nodes_after_eviction_and_nested_iteration(self):
  s=self.store();nodes=[];expected=[]
  for i in range(10):
   v=[{'ordinal':j,'value':str(i)} for j in range(3500)];expected.append(v);nodes.append(s.parse(s.write([wire(v)])))
  for i in (0,9,2,7,4,6):
   self.assertEqual(nodes[i],expected[i]);self.assertEqual(nodes[i][3456],expected[i][3456])
  self.assertLessEqual(s.pool.peak,4)
 def test_mutated_snapshot_after_eviction_rejects(self):
  s=self.store();b=s.write([wire({'n':1})]);s.parse(b)
  for i in range(8):s.parse(s.write([wire({'next':i})]))
  b.path.write_bytes(wire({'n':9}))
  with self.assertRaises(ValueError):s.parse(b)
 def test_mutated_index_after_eviction_rejects(self):
  s=self.store();b=s.write([wire({'n':1})]);s.parse(b);info=s.last_document.descriptor()
  for i in range(8):s.parse(s.write([wire({'next':i})]))
  Path(info['index']).write_bytes(b'corrupt')
  with self.assertRaises(ValueError):s.parse(b)
 def test_wrong_containing_object_and_cross_store_binding(self):
  s=self.store();b=s.write([wire({'n':1})]);s.parse(b);info=s.last_document.descriptor();other=self.store()
  with self.assertRaises(ValueError):Document.reopen(other,b,info)
  with self.assertRaises(ValueError):Document.reopen(s,s.write([wire({'n':1})]),info)
  bad=dict(info,binding='wrong')
  with self.assertRaises(ValueError):Document.reopen(s,b,bad)
 def test_malformed_missing_and_interrupted_cleanup(self):
  for raw in (b'{',b'{"a":1,"a":2}\n',b'[01]\n'):
   s=self.store();b=s.write([raw]);before=len(os.listdir('/proc/self/fd'))
   with self.assertRaises(ValueError):s.parse(b)
   self.assertEqual(len(os.listdir('/proc/self/fd')),before)
   self.assertFalse(list(s.root.glob('index-*')));s.close();self.assertFalse(s.root.exists())
  s=self.store();b=s.write([b'{}\n']);b.path.unlink()
  with self.assertRaises(OSError):s.parse(b)
  s.close();self.assertFalse(s.root.exists())
 def test_exception_during_parse_and_spool_closes_resources(self):
  s=self.store();b=s.write([b'{}\n'])
  with patch.object(Document,'node',side_effect=PauseRequested()),self.assertRaises(PauseRequested):s.parse(b)
  self.assertFalse(list(s.root.glob('index-*')))
  def parts():yield b'abc';raise OSError('read interrupted')
  before=set(s.root.iterdir())
  with self.assertRaises(OSError):s.write(parts())
  self.assertEqual(set(s.root.iterdir()),before);self.assertEqual(s.parse(b),{})
 def test_repeated_store_cycles_no_fd_accumulation(self):
  before=len(os.listdir('/proc/self/fd'));peaks=[]
  for cycle in range(4):
   s=Store(self.p)
   for i in range(64):s.parse(s.write([wire({'i':i})]))
   peaks.append(s.metrics()['peak_open_indexes']);s.close();s.close()
   self.assertEqual(len(os.listdir('/proc/self/fd')),before);self.assertFalse(s.root.exists())
  self.assertEqual(peaks,[4]*4)
 def test_byte_caches_and_diagnostic_tail_are_bounded(self):
  c=ByteLRU(8192,8);log=BoundedLog()
  for i in range(500):c[str(i)]='x'*100;log.append({'argument_id':str(i),'sha256':'a'*64});self.assertLessEqual(c.bytes,8192)
  self.assertLessEqual(len(c),8);self.assertLessEqual(log.cache.bytes,65536);self.assertLessEqual(len(log),32);self.assertEqual(log.total,500);self.assertEqual(log[-1]['argument_id'],'499');c.clear();self.assertEqual(c.bytes,0)
 def case(self,documents=24,family='GAMMA'):
  m,t=export(self.p/'input',documents,family);create_key(self.p/'key');return m,t
 def oracle(self,r,p):
  o=json.loads((p/'oracle.json').read_bytes());self.assertFalse(r['failures'],r['reasons']);self.assertFalse(r['profile_admitted']);self.assertFalse(r['actual_qualification_established'])
  for scope,v in o['scopes'].items():
   got=r['bindings']['scope_validation']['scopes'][scope]['link_validation'];self.assertEqual(got['complete_stream_sha256'],v['links_sha256']);self.assertEqual(got['structural_rows'],v['structural']);self.assertEqual(got['potential_rows'],v['potential'])
  inv=r['semantic_acquisition']['invocations'];self.assertEqual({x['sha256'] for x in inv},set(o['calls'].values()));self.assertTrue(all(x['dependency_count']>=o['required_shared_fragments']+2 for x in inv))
 def test_integrated_shared_dependencies_both_independent_invocation_codecs(self):
  for family in ('GAMMA','DELTA'):
   p=self.p/family;m,t=export(p,20,family);create_key(p/'key');r=run(m,t,p/'j',p/'key');self.oracle(r,p);self.assertEqual(r['semantic_acquisition']['cleanup']['open_index_connections'],0)
 def test_more_documents_than_handle_limit_through_collector(self):
  # Independent subprocess prevents changing this test runner's resource limits.
  m,t=self.case(128);script='''import resource,json
from recovery_schedule.runner import run
resource.setrlimit(resource.RLIMIT_NOFILE,(96,96))
r=run(*__import__('sys').argv[1:]);print(json.dumps(r))
'''
  p=subprocess.run([sys.executable,'-c',script,str(m),str(t),str(self.p/'j'),str(self.p/'key')],capture_output=True,text=True,timeout=55);self.assertEqual(p.returncode,0,p.stderr);r=json.loads(p.stdout);self.oracle(r,m.parent);self.assertGreater(r['semantic_acquisition']['lifetime']['documents_built'],96);self.assertLess(r['semantic_acquisition']['lifetime']['observed_peak_process_fds'],96)
 def test_repeated_pause_resume_and_terminal_reuse(self):
  m,t=self.case();r=run(m,t,self.p/'j',self.p/'key',new_bytes=1);self.assertEqual(r['result'],'PAUSED')
  r=run(m,t,self.p/'j',self.p/'key',resume=True,new_bytes=31);self.assertEqual(r['result'],'PAUSED')
  r=run(m,t,self.p/'j',self.p/'key',resume=True);self.oracle(r,m.parent)
  final=run(m,t,self.p/'j',self.p/'key',resume=True);self.assertTrue(final['stage_schedule']['terminal_reused']);self.oracle(final,m.parent)
 def test_stage_interruption_reuses_exact_semantic_indexes(self):
  m,t=self.case();save=Scheduler.save
  def stop(s,label,*a,**kw):
   if label=='ordered-ledger':raise PauseRequested()
   return save(s,label,*a,**kw)
  with patch.object(Scheduler,'save',stop),self.assertRaises(PauseRequested):run(m,t,self.p/'j',self.p/'key')
  r=run(m,t,self.p/'j',self.p/'key',resume=True);self.oracle(r,m.parent);self.assertTrue(any(e['status']=='REUSED-CANONICAL-INDEX-EXACT-BYTES' for e in r['stage_schedule']['events']))
 def test_missing_shared_dependency_does_not_pass(self):
  m,t=self.case();o=json.loads((m.parent/'oracle.json').read_bytes());(m.parent/'materials'/next(iter(o['fragment_materials'].values()))).unlink()
  r=run(m,t,self.p/'j',self.p/'key');self.assertTrue(r['failures']);self.assertFalse(r['profile_admitted']);self.assertTrue(r['semantic_acquisition']['cleanup']['temporary_root_removed'])
 def test_completed_input_mutation_and_stale_index_rejected(self):
  m,t=self.case();run(m,t,self.p/'j',self.p/'key');o=json.loads((m.parent/'oracle.json').read_bytes());p=m.parent/'materials'/next(iter(o['fragment_materials'].values()));raw=p.read_bytes();p.write_bytes(raw[:-1]+b' ')
  r=run(m,t,self.p/'j',self.p/'key',resume=True);self.assertTrue(r['failures']);self.assertFalse(r['profile_admitted'])
 def test_cross_job_receipt_substitution_rejected(self):
  m,t=self.case();run(m,t,self.p/'one',self.p/'key');run(m,t,self.p/'two',self.p/'key')
  # Same input can legitimately have equivalent computations; the absolute
  # saved snapshot/receipt graph still prevents replacing another job's files.
  roots=[Path(str(self.p/x)+'.stages') for x in ('one','two')]
  a=next(p for p in roots[0].glob('*.json') if json.loads(p.read_bytes()).get('payload',{}).get('label','').startswith('semantic-index:'))
  b=roots[1]/a.name;b.write_bytes(a.read_bytes())
  with self.assertRaises((ValueError,OSError)):run(m,t,self.p/'two',self.p/'key',resume=True)

 def test_lazy_raw_and_hex_recheck_containing_object_after_eviction(self):
  from semantic_stream.storage import canonical
  for mode in ('raw','hex'):
   s=self.store();token=ACTIVE.set(s)
   try:
    raw=wire({'bytes':'ab'*600000});b=s.write([raw]);node=s.parse(b);hexvalue=node['bytes']
    for i in range(8):s.parse(s.write([wire({'n':i})]))
    b.path.write_bytes(raw.replace(b'ab',b'ac',1))
    with self.assertRaises(ValueError):
     if mode=='raw':canonical(node)
     else:list(hexvalue.chunks())
   finally:ACTIVE.reset(token)
