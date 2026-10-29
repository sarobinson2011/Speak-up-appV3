from pathlib import Path,PurePosixPath
import hashlib,io,json,stat,zipfile
B=Path(__file__).resolve().parents[1];R=B/'status-forwarding';R.mkdir()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify(raw,pin,count):
 assert ident(raw)==pin;z=zipfile.ZipFile(io.BytesIO(raw));names=z.namelist()
 assert len(names)==len(set(names))==count and z.testzip() is None
 for i in z.infolist():
  p=PurePosixPath(i.filename);assert p.as_posix()==i.filename and not p.is_absolute() and '..' not in p.parts and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
 m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
 for n,pin in m.items():assert ident(z.read(n))==pin,n
 return z
raw=(B/'upload/Formal-Lab6-I164-client-state-return-correspondence-independent-review(1).zip').read_bytes()
review=verify(raw,{'bytes':60792892,'sha256':'a8762d3b81d5f5cbedfb95e5afd8d2c083143ed759f88f2b550cfebfb6de4bf6'},91)
targetraw=review.read('input/I164-client-state-return-correspondence-1.zip');target=verify(targetraw,{'bytes':61624841,'sha256':'0ae24141a77f42eb96ed0f8d144f612d7a8045e04f7aa47dcaa8d1750f886907'},1688)
for dest,z in [('retained/state',target),('retained/review',review)]:
 for n in z.namelist():
  if dest=='retained/review' and n.startswith('input/'):continue
  p=R/dest/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
for n in ['code','tests','fixtures','results','provenance','failures']: (R/n).mkdir()
(R/'code/managed_coverage.py').write_bytes(target.read('code/managed_coverage.py'))
(R/'tests/guard.py').write_bytes(target.read('tests/guard.py'))
(R/'provenance/input-verification.json').write_text(json.dumps({'review':ident(raw),'review_entries':91,'target':ident(targetraw),'target_entries':1688,'target_manifest':ident(target.read('MANIFEST.json')),'verification':'CRC safe unique regular membership exact manifest hashes; no candidate execution','review_non_input_records':90,'prior_independent_results':{'primary':273,'recovered':196,'CLI':1,'failed_attempt_checks':17,'packaging_failure_separate':True},'prior_supplied_results':{'primary':171,'recovered':173,'fresh_assertions':5},'prior_suites_rerun':False},indent=2)+'\n')
review.close();target.close();print('Exact reviewed predecessors retained; new isolated construction root ready')
