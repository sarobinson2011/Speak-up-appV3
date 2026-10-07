#!/usr/bin/env python3
import contextlib,copy,hashlib,io,json,os,random,shutil,struct,subprocess,sys,tempfile,time,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'tests'))
import run_task as rt
from oracle import descriptor,rows,serialize,HEADER,parse
from check_descriptor import analytical

class Checks(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def invoke(self,raw,a,b,state='INIT',engine='complement'):
  names,_,_=parse(raw);assert len(names)<=1500,'test guard: no retained universe'
  d=self.d/'input.txt';d.write_bytes(raw)
  p=subprocess.run([str(ROOT/'runner/links'),str(d),str(a),str(b),state,engine,'5'],capture_output=True,text=True,timeout=6);self.assertEqual(p.returncode,0,p.stderr);return json.loads(p.stdout)
 def raw(self,n=12):
  names=['Z','A','M','B','K.$record','K::001','K:0','K_0','K-0','K.0','L','Y'][:n]
  return descriptor(names,{0:0,2:1,4:0},[(0,1,2,'SOURCE'),(0,1,2,'SOURCE'),(0,1,1,'EQUALS'),(3,2,999999,'Z'),(1,1,10,'SELF'),(1,0,3,'BACK')])
 def test_oracle_whole_and_replay(self):
  raw=self.raw();expected=serialize(raw)
  for eng in ('complement','predicate'):
   x=self.invoke(raw,0,12,engine=eng);self.assertEqual(x['prefix_sha256'],hashlib.sha256(expected).hexdigest());self.assertEqual(x['rows'],len(rows(raw)));self.assertEqual(x['bytes'],len(expected)-67);self.assertEqual(x['engine'],'lexical-tsv')
 def test_every_split_and_empty_from_groups(self):
  raw=self.raw();names,_,_=parse(raw);expected=serialize(raw)
  for split in range(1,12):
   a=self.invoke(raw,0,split);b=self.invoke(raw,split,12,a['state_out']);self.assertEqual(b['prefix_sha256'],hashlib.sha256(expected).hexdigest());self.assertEqual(a['bytes']+b['bytes']+67,len(expected))
 def test_analytical_prefix_equals_exhaustive_oracle(self):
  raw=self.raw();names,fixed,edges=parse(raw);p,total,size,unique,potential=analytical(names,list(fixed.items()),edges);allrows=rows(raw);self.assertEqual(total,len(allrows));self.assertEqual(size,len(serialize(raw)));self.assertEqual(unique,5)
  for k in range(13):
   selected=set(sorted(names)[:k]);chosen=[(i,r) for i,r in enumerate(allrows,1) if r[0] in selected];b=HEADER+b''.join((str(i).zfill(6)+'\t'+'\t'.join(r)+'\n').encode() for i,r in chosen)
   self.assertEqual(struct.unpack_from('>QQ',p,k*16),(len(chosen),len(b)))
 def test_ordinal_crosses_six_digits(self):
  raw=descriptor([f'T{1500-i:04}' for i in range(1500)],{},[]);allrows=rows(raw);name=sorted(parse(raw)[0])[1450];selected=[(i,r) for i,r in enumerate(allrows,1) if r[0]==name];body=b''.join((str(i).zfill(6)+'\t'+'\t'.join(r)+'\n').encode() for i,r in selected);x=self.invoke(raw,1450,1451)
  self.assertGreater(x['first_row_ordinal'],999999);self.assertEqual(x['segment_sha256'],hashlib.sha256(body).hexdigest());self.assertEqual(x['rows'],len(selected))
 def tiny(self):
  root=self.d/'kit';root.mkdir();(root/'runner').mkdir();(root/'inputs').mkdir();(root/'bindings').mkdir()
  for f in ('links','links.cpp','pairs.cpp','run.py'):shutil.copyfile(ROOT/'runner'/f,root/'runner'/f)
  (root/'runner/links').chmod(0o755);shutil.copyfile(ROOT/'step.py',root/'step.py')
  raw=descriptor([f'T{32-i:02}' for i in range(32)],{0:0,3:1},[(0,1,1,'SOURCE'),(0,1,1,'SOURCE')]);(root/'inputs/links.txt').write_bytes(raw)
  names,fixed,edges=parse(raw);pref,n,b,_,_=analytical(names,list(fixed.items()),edges);(root/'inputs/prefix.bin').write_bytes(pref)
  rt.atomic(root/'PACKAGE-MANIFEST.json',{'files':[]});rt.atomic(root/'bindings/ACTIVE-IDENTITIES.json',{'conditional_test_only':True})
  plan=dict(rt.PLAN,candidate_total=32,rows=n,serialized_bytes=b,segment_candidates=16,min_segment_candidates=16,segments_max=2,aggregate_seconds=600,max_attempts=20)
  return root,plan,raw
 def drive(self,root,plan,job,actions=None):
  rt.PAUSED=False
  with contextlib.redirect_stdout(io.StringIO()):return rt.drive(job,root,plan,{},max_actions=actions,segment_ranks=16)
 def test_pause_resume_repeated_completion(self):
  root,plan,raw=self.tiny();job=self.d/'job';self.assertEqual(self.drive(root,plan,job,1),3);first=(job/'textual/segment-00000000.json').read_bytes();a=rt.audit(root,job/'textual',plan);self.assertIsNone(a['generated_whole_stream_sha256']);self.assertIsNone(a['verified_whole_stream_sha256'])
  self.assertEqual(self.drive(root,plan,job),0);self.assertEqual(first,(job/'textual/segment-00000000.json').read_bytes());self.assertEqual(self.drive(root,plan,job),0);a=rt.audit(root,job/'textual',plan);self.assertEqual(a['replayed_whole_stream_sha256'],hashlib.sha256(serialize(raw)).hexdigest());self.assertFalse(a['independent_supplied_row_validation'])
 def test_interrupted_reservation_and_unpublished_part(self):
  root,plan,raw=self.tiny();job=self.d/'job';original=rt.execute_step
  try:
   def interrupt(*a):raise KeyboardInterrupt()
   rt.execute_step=interrupt
   with self.assertRaises(KeyboardInterrupt):self.drive(root,plan,job)
  finally:rt.execute_step=original
  (job/'textual/segment-00000000.part').write_bytes(b'{incomplete')
  self.assertEqual(self.drive(root,plan,job),0);recs,_=rt.budget_records(job/'supervisor');self.assertEqual(recs[0]['status'],'INTERRUPTED');self.assertEqual(recs[0]['charged_seconds'],60)
 def test_commit_then_supervisor_interruption_keeps_segment(self):
  root,plan,raw=self.tiny();job=self.d/'job';original=rt.execute_step
  try:
   def interrupt(*a):original(*a);raise KeyboardInterrupt()
   rt.execute_step=interrupt
   with self.assertRaises(KeyboardInterrupt):self.drive(root,plan,job)
  finally:rt.execute_step=original
  first=(job/'textual/segment-00000000.json').read_bytes();self.assertEqual(self.drive(root,plan,job),0);self.assertEqual(first,(job/'textual/segment-00000000.json').read_bytes())
 def test_corrupt_and_changed_descriptor_rejected(self):
  root,plan,raw=self.tiny();job=self.d/'job';self.drive(root,plan,job,1);p=job/'textual/segment-00000000.json';old=p.read_bytes();x=rt.read(p);x['prefix_sha256']='f'*64;rt.atomic(p,x)
  with self.assertRaises(ValueError):rt.audit(root,job/'textual',plan)
  p.write_bytes(old);(root/'inputs/links.txt').write_bytes(raw+b'\n')
  with self.assertRaises(ValueError):rt.audit(root,job/'textual',plan)
 def test_budget_stop_and_explicit_grant(self):
  root,plan,raw=self.tiny();plan['aggregate_seconds']=60;job=self.d/'job';original=rt.execute_step
  try:
   rt.execute_step=lambda *a:(_ for _ in ()).throw(KeyboardInterrupt())
   with self.assertRaises(KeyboardInterrupt):self.drive(root,plan,job)
  finally:rt.execute_step=original
  self.assertEqual(self.drive(root,plan,job),4);state=job/'supervisor';ident=rt.unseal(state/'IDENTITY.json');rt.sealed(state/'grant-00000.json',{'previous':rt.sha(rt.wire(ident)),'job_identity_sha256':rt.sha(rt.wire(ident)),'seconds':600});self.assertEqual(self.drive(root,plan,job),0)
 def test_substituted_grant_rejected(self):
  root,plan,raw=self.tiny();job=self.d/'job';self.drive(root,plan,job,1);state=job/'supervisor';rt.sealed(state/'grant-00000.json',{'previous':'a'*64,'job_identity_sha256':'b'*64,'seconds':600})
  with self.assertRaises(ValueError):self.drive(root,plan,job)
 def test_wrong_runtime_or_active_model_rejected(self):
  root,plan,raw=self.tiny();job=self.d/'job';self.drive(root,plan,job,1)
  with self.assertRaises(ValueError):rt.drive(job,root,plan,{'different':'runtime'})
  rt.atomic(root/'bindings/ACTIVE-IDENTITIES.json',{'conditional_test_only':False})
  with self.assertRaises(ValueError):self.drive(root,plan,job)
 def test_same_engine_replay_tamper_rejected(self):
  root,plan,raw=self.tiny();job=self.d/'job';self.drive(root,plan,job);p=job/'textual/verification/verified-00000000.json';x=rt.read(p);x['engine']='independent-predicate';rt.atomic(p,x)
  with self.assertRaises(ValueError):rt.audit(root,job/'textual',plan)
 def test_read_only_native_host_probe(self):
  import bootstrap
  x=bootstrap.native_probe((ROOT/'runner/links').read_bytes(),(ROOT/'inputs/probe.txt').read_bytes(),rt.read(ROOT/'inputs/probe-expected.json'));self.assertEqual(x['result'],'PASS');self.assertTrue(x['library_sha256'])
 def test_snapshot_restore_corruption_and_preserved_segments(self):
  import snapshot as sn
  root,plan,raw=self.tiny();job=self.d/'job';self.drive(root,plan,job,1)
  old=(sn.ROOT,sn.PLAN,sn.verify_package)
  try:
   sn.ROOT=root;sn.PLAN=plan;sn.verify_package=lambda:rt.verify_package(root)
   snap=sn.save(job);target=self.d/'restored';sn.restore(Path(snap['snapshot']),target,snap['sha256'])
   self.assertEqual((job/'textual/segment-00000000.json').read_bytes(),(target/'textual/segment-00000000.json').read_bytes());(target/'textual/PAUSE').unlink();self.assertEqual(self.drive(root,plan,target),0)
   with self.assertRaises(ValueError):sn.restore(Path(snap['snapshot']),self.d/'corrupt','0'*64)
  finally:sn.ROOT,sn.PLAN,sn.verify_package=old
 def test_incomplete_snapshot_restore_cannot_run(self):
  root,plan,raw=self.tiny();job=self.d/'job';job.mkdir();(job/'RESTORE-INCOMPLETE').touch()
  with self.assertRaises(ValueError):self.drive(root,plan,job)
 def test_metadata_corruption_prefix_rejected_at_package_boundary(self):
  root,plan,raw=self.tiny();p=root/'inputs/prefix.bin';rt.atomic(root/'PACKAGE-MANIFEST.json',{'files':[{'path':'inputs/prefix.bin','bytes':p.stat().st_size,'sha256':rt.filehash(p)}]});p.write_bytes(p.read_bytes()[:-1]+b'X')
  with self.assertRaises(ValueError):rt.verify_package(root)
 def test_original_namespace_rejected(self):
  root,plan,raw=self.tiny();job=self.d/'job';self.drive(root,plan,job,1);p=job/'supervisor/IDENTITY.json';i=rt.unseal(p);i['format']='CP4R-BINARY-JOB-1';rt.sealed(p,i)
  with self.assertRaises(ValueError):self.drive(root,plan,job)
if __name__=='__main__':
 start=time.monotonic();suite=unittest.defaultTestLoader.loadTestsFromTestCase(Checks);result=unittest.TextTestRunner(verbosity=2).run(suite)
 (ROOT/'results/PACKAGE-CHECKS.json').write_bytes(rt.wire({'result':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'seconds':time.monotonic()-start,'full_retained_stream_processed':False,'independent_small_serialization_oracle':True}));sys.exit(not result.wasSuccessful())
