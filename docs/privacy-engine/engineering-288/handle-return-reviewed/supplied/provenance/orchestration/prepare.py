import hashlib,io,json,stat,zipfile
from pathlib import Path,PurePosixPath
B=Path(__file__).resolve().parents[1];R=B/'handle-return';R.mkdir(exist_ok=False)
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
reviewpin={'bytes':41478030,'sha256':'63c72c1b7ad2f42f05b8f005454748967bf3fac5fcbc26fb81058567a717a311'}
statepin={'bytes':41935972,'sha256':'44942004491d883af8c422f10dd38fd1e25cbc4f56e2d53e6345e264d0893fdc'}
v=verify((B/'upload/Formal-Lab6-I164-state-return-correspondence-independent-review(1).zip').read_bytes(),reviewpin,34)
s=verify(v.read('input/I164-state-return-correspondence-1.zip'),statepin,1016)
for prefix,z in [('retained/state',s),('retained/state-review',v)]:
 for n in z.namelist():
  if n.startswith('input/'):continue
  p=R/prefix/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
for n in ['code','tests','results','provenance','failures','tools']:(R/n).mkdir()
(R/'code/managed_coverage.py').write_bytes(s.read('code/managed_coverage.py'))
(R/'tools/checkpoint.py').write_bytes(s.read('tools/checkpoint.py'))
report={'state':statepin,'state_entries':1016,'state_manifest_hashes':1015,'review':reviewpin,'review_entries':34,'review_manifest_hashes':33,'CRC_membership_hashes':'PASS','review_copy_omits_only_embedded_state_zip':True,'decoded_state_complete':True,'completed_checks_rerun':False,'Git_save_repeated':False}
(R/'provenance/input-verification.json').write_bytes(enc(report));print(json.dumps(report))
