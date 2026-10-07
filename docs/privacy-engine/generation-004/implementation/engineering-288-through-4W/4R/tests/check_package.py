"""Only new portable-package glue checks. No retained full-universe worker run."""
import contextlib,hashlib,importlib.util,io,json,shutil,struct,tempfile,time,zipfile,types
from unittest.mock import patch
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('task',R/'run_task.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
began=time.monotonic();checks=[]
def ok(name,test):
 test();checks.append({'case':name,'result':'PASS'})
def rejects(fn):
 try:fn()
 except (ValueError,AssertionError,FileNotFoundError):return
 raise AssertionError('did not reject')
plan={**t.PLAN,'descriptor':'inputs/probe.txt','candidate_total':6,'rows':5,'serialized_bytes':74,'segment_candidates':2,'segments':3,'scope':'INDEPENDENT-FOUR-TOKEN-PACKAGE-ORACLE'}
expected=b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n'+b''.join(struct.pack('>II',i,j) for i in range(4) for j in range(i+1,4) if (i,j)!=(0,1));want=hashlib.sha256(expected).hexdigest()
with tempfile.TemporaryDirectory(prefix='cp4r-bounded-') as td,contextlib.redirect_stdout(io.StringIO()):
 base=Path(td);job=base/'normal';runtime={'test-native':'same-pinned-native'}
 assert t.drive(job,R,plan,runtime,max_actions=1)==3
 first=(job/'binary/segment-00000000.json').read_bytes()
 ok('pause after first committed segment',lambda:None)
 (job/'binary/segment-00000001.part').write_text('interrupted atomic write')
 assert t.drive(job,R,plan,runtime,max_actions=2)==3
 assert (job/'binary/segment-00000000.json').read_bytes()==first
 ok('repeated generation resume preserves exact prior segment; torn part ignored',lambda:None)
 assert t.drive(job,R,plan,runtime,max_actions=1)==3
 ok('independent replay paused after first segment',lambda:None)
 assert t.drive(job,R,plan,runtime)==0
 a=t.audit(R,job/'binary',plan);assert a['verified_whole_stream_sha256']==want and a['rows']==5 and a['serialized_bytes']==74
 ok('generation plus predicate replay equals independent Python serialized oracle',lambda:None)
 old=(job/'COMPLETION.json').read_bytes();assert t.drive(job,R,plan,runtime)==0 and (job/'COMPLETION.json').read_bytes()==old
 ok('terminal reuse identical result without worker replay',lambda:None)
 rejected=base/'corrupt';shutil.copytree(job,rejected)
 p=rejected/'binary/segment-00000001.json';x=t.read(p);x['prefix_sha256']='0'*64;t.atomic(p,x)
 ok('altered generation receipt rejected',lambda:rejects(lambda:t.audit(R,rejected/'binary',plan)))
 rejected2=base/'missing';shutil.copytree(job,rejected2);(rejected2/'binary/segment-00000001.json').unlink()
 ok('missing committed segment rejected',lambda:rejects(lambda:t.audit(R,rejected2/'binary',plan)))
 rejected3=base/'replay';shutil.copytree(job,rejected3);p=rejected3/'binary/verification/verified-00000001.json';x=t.read(p);x['engine']='complement';t.atomic(p,x)
 ok('wrong replay engine rejected',lambda:rejects(lambda:t.audit(R,rejected3/'binary',plan)))
 rejected4=base/'budget';shutil.copytree(job,rejected4);p=rejected4/'supervisor/attempt-00000.json';x=t.read(p);x['payload']['charged_seconds']=0;t.atomic(p,x)
 ok('corrupt elapsed budget journal rejected',lambda:rejects(lambda:t.budget_records(rejected4/'supervisor')))
 missing_head=base/'missing-budget-head';shutil.copytree(job,missing_head);(missing_head/'supervisor/HEAD.json').unlink()
 ok('lost budget HEAD rejected',lambda:rejects(lambda:t.budget_records(missing_head/'supervisor')))
 reset=base/'reset-budget';shutil.copytree(job,reset)
 for x in (reset/'supervisor').glob('attempt-*.json'):x.unlink()
 (reset/'supervisor/HEAD.json').unlink()
 ok('budget deletion cannot reset completed computation charge',lambda:rejects(lambda:t.drive(reset,R,plan,runtime)))
 ok('substituted runtime binding rejected',lambda:rejects(lambda:t.drive(job,R,plan,{'wrong':'library'})))
 ok('substituted plan/descriptor rejected',lambda:rejects(lambda:t.drive(job,R,{**plan,'descriptor':'inputs/pairs.txt'},runtime)))
 # Kill-equivalent interruption after actual native segment commit but before
 # accounting finalization: resume must adopt commit and conservatively charge.
 interrupted=base/'interrupted';original=t.execute_step
 def crash(*args,**kwargs):
  original(*args,**kwargs);raise RuntimeError('injected power-loss boundary')
 t.execute_step=crash
 try:t.drive(interrupted,R,plan,runtime)
 except RuntimeError:pass
 finally:t.execute_step=original
 assert t.drive(interrupted,R,plan,runtime)==0
 hist,_=t.budget_records(interrupted/'supervisor');assert hist[0]['status']=='INTERRUPTED' and hist[0]['charged_seconds']==60
 assert t.audit(R,interrupted/'binary',plan)['verified_whole_stream_sha256']==want
 ok('interruption after commit/before accounting resumes with full reservation charged',lambda:None)
 stopped=base/'stopped';limited={**plan,'aggregate_seconds':60};assert t.drive(stopped,R,limited,runtime)==4
 assert t.drive(stopped,R,limited,runtime)==4
 ok('aggregate review stop persists across repeated resume',lambda:None)
 marked=base/'marked';assert t.drive(marked,R,plan,runtime,max_actions=1)==3;(marked/'binary/PAUSE').touch();before=len(list((marked/'binary').glob('segment-*.json')));assert t.drive(marked,R,plan,runtime)==3 and len(list((marked/'binary').glob('segment-*.json')))==before
 ok('PAUSE prevents next segment',lambda:None)
 # Snapshot save/restore exercises the same public helpers with the small
 # independent plan only; the production CLI remains fixed to the full universe.
 ss=importlib.util.spec_from_file_location('snap',R/'snapshot.py');snap=importlib.util.module_from_spec(ss)
 import sys
 sys.path.insert(0,str(R));ss.loader.exec_module(snap);snap.PLAN=plan
 backup=snap.save(job);restored=base/'restored';snap.restore(Path(backup['snapshot']),restored,backup['sha256'])
 assert t.audit(R,restored/'binary',plan)['verified_whole_stream_sha256']==want
 ok('snapshot restore preserves complete independent small oracle',lambda:None)
 ok('wrong snapshot digest rejected',lambda:rejects(lambda:snap.restore(Path(backup['snapshot']),base/'wrong','0'*64)))
 ok('restore never overwrites existing job',lambda:rejects(lambda:snap.restore(Path(backup['snapshot']),restored,backup['sha256'])))
 # ZIP preflight is exercised without a filesystem extraction. Capacity tests
 # use explicit synthetic host observations; they are not user-host PASS claims.
 bs=importlib.util.spec_from_file_location('boot',R/'bootstrap.py');boot=importlib.util.module_from_spec(bs);bs.loader.exec_module(boot)
 pkg=base/'probe-kit.zip';mf=t.read(R/'PACKAGE-MANIFEST.json')
 with zipfile.ZipFile(pkg,'w') as z:
  for e in mf['files']:z.write(R/e['path'],boot.PREFIX+e['path'])
  z.write(R/'PACKAGE-MANIFEST.json',boot.PREFIX+'PACKAGE-MANIFEST.json')
 before=set(base.rglob('*'));cwd=Path.cwd()
 with zipfile.ZipFile(pkg) as z:
  with patch.object(boot,'memory_available',return_value={'effective_available_bytes':1}):
   result=boot.preflight(z,base/'readonly-target');assert any('8 GiB' in e for e in result['errors'])
  with patch.object(boot.os,'statvfs',return_value=types.SimpleNamespace(f_bavail=0,f_frsize=4096,f_flag=0,f_favail=100000)):
   result=boot.preflight(z,base/'readonly-target');assert any('insufficient disk' in e for e in result['errors'])
  with patch.object(boot,'native_probe',side_effect=ValueError('incompatible native fixture')):
   result=boot.preflight(z,base/'readonly-target');assert 'incompatible native fixture' in result['errors']
 assert set(base.rglob('*'))==before and Path.cwd()==cwd
 ok('read-only ZIP preflight rejects insufficient memory/disk and native incompatibility; no paths/cwd changed',lambda:None)
 # Independent oracle for descriptor classification, without full pair iteration.
 lines=(R/'inputs/pairs.txt').read_text().splitlines();n,m=map(int,lines[0].split());fixed=[tuple(map(int,l.split())) for l in lines[1:]];excluded=sum(1 for i,(a,g) in enumerate(fixed) for b,h in fixed[i+1:] if g!=h)
 assert n==426984 and m==len(fixed)==50 and excluded==1169 and n*(n-1)//2-excluded==91157453467
 ok('small descriptor exact complement/count recheck; no full pairs enumerated',lambda:None)
print(json.dumps({'result':'PASS','kind':'necessary bounded 4R package/recovery checks only','checks':checks,'elapsed_seconds':time.monotonic()-began,'full_universe_processed':False,'regression_suites_rerun':False,'benchmarks_run':False,'oracle_sha256':want},indent=2))
