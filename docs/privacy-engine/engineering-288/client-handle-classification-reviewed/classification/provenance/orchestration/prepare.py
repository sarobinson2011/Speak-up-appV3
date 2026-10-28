import hashlib,io,json,stat,zipfile
from pathlib import Path,PurePosixPath
B=Path(__file__).resolve().parents[1];R=B/'outside-catch-correction';R.mkdir(exist_ok=False)
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def verify(raw,pin,entries):
 assert ident(raw)==pin
 z=zipfile.ZipFile(io.BytesIO(raw));ns=z.namelist();assert len(ns)==len(set(ns))==entries and z.testzip() is None
 m=json.loads(z.read('MANIFEST.json'));m=m.get('members',m);assert set(ns)==set(m)|{'MANIFEST.json'}
 for n in ns:
  p=PurePosixPath(n);i=z.getinfo(n);assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==n and stat.S_ISREG(i.external_attr>>16)
  if n!='MANIFEST.json':assert ident(z.read(n))==m[n]
 return z
reviewpin={'bytes':59157073,'sha256':'18cbb930e1b0db4d42b9e4b7f2af32f521d9f2c50c268216d8c02793c124df9f'}
statepin={'bytes':43439616,'sha256':'1f7b1c7dc58949e76f73cac68afb00ea0373490ac0c07bdada86d954772b4431'}
v=verify((B/'upload/Formal-Lab6-I164-client-handle-return-correspondence-independent-review(1).zip').read_bytes(),reviewpin,172)
s=verify(v.read('input/I164-client-handle-return-correspondence-1.zip'),statepin,1282)
for prefix,z in [('original',s),('review',v)]:
 for n in z.namelist():
  if n.startswith('input/'):continue
  p=R/prefix/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
for n in ['code','tests','results','provenance','failures','tools']:(R/n).mkdir()
(R/'code/managed_coverage.py').write_bytes(s.read('code/managed_coverage.py'))
(R/'tools/checkpoint.py').write_bytes(s.read('tools/checkpoint.py'))
report={'original':statepin,'original_entries':1282,'review':reviewpin,'review_entries':172,'all_manifest_hashes_CRC_safe_regular_membership':'PASS','review_copy_members':171,'review_omits_only_redundant_input_zip':True,'large_review_failure_bytes_included':True,'completed_campaigns_rerun':False}
(R/'provenance/input-verification.json').write_bytes(enc(report));print(json.dumps(report))
