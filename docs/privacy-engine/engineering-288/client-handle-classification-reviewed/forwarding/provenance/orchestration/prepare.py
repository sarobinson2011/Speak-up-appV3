import hashlib,io,json,stat,zipfile
from pathlib import Path,PurePosixPath
B=Path(__file__).resolve().parents[1];R=B/'client-handle-return';R.mkdir(exist_ok=False)
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
reviewpin={'bytes':42069714,'sha256':'d69cd5939e0fc051adee4f270dd0148d4aecf5cfef2ecae65b3ec33cedf4f31c'}
statepin={'bytes':42330497,'sha256':'6b486b1ca0c49da010face18132507020a07f3db84602d62a7c75af0305caa8e'}
v=verify((B/'upload/Formal-Lab6-I164-handle-return-correspondence-independent-review(1).zip').read_bytes(),reviewpin,142)
s=verify(v.read('input/I164-handle-return-correspondence-1.zip'),statepin,1088)
for prefix,z in [('retained/handle',s),('retained/handle-review',v)]:
 for n in z.namelist():
  if n.startswith('input/'):continue
  p=R/prefix/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
for n in ['code','tests','results','provenance','failures','tools']:(R/n).mkdir()
(R/'code/managed_coverage.py').write_bytes(s.read('code/managed_coverage.py'))
(R/'tools/checkpoint.py').write_bytes(s.read('tools/checkpoint.py'))
report={'handle':statepin,'handle_entries':1088,'handle_manifest_hashes':1087,'review':reviewpin,'review_entries':142,'review_manifest_hashes':141,'CRC_membership_hashes':'PASS','review_compact_members':141,'review_copy_omits_only_embedded_handle_zip':True,'decoded_handle_complete':True,'completed_checks_rerun':False,'Git_save_repeated':False}
(R/'provenance/input-verification.json').write_bytes(enc(report));print(json.dumps(report))
