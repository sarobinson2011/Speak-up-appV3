from pathlib import Path,PurePosixPath
import sys,zipfile,json,hashlib,stat,io
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
p=Path(sys.argv[1]);raw=p.read_bytes()
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 ns=z.namelist();assert len(ns)==len(set(ns)) and z.testzip() is None
 for i in z.infolist():
  n=i.filename;q=PurePosixPath(n);assert str(q)==n and not q.is_absolute() and '..' not in q.parts and '\\' not in n and not i.is_dir() and stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG
 m=json.loads(z.read('MANIFEST.json'));assert set(ns)==set(m)|{'MANIFEST.json'}
 for n,v in m.items():assert ident(z.read(n))==v,n
 c=json.loads(z.read('CHECKPOINT.json'));a=z.read('input/'+c['target']);assert ident(a)=={k:c['input'][k] for k in ('bytes','sha256')}
 with zipfile.ZipFile(io.BytesIO(a)) as inp:
  assert len(inp.infolist())==2807 and inp.testzip() is None
  im=json.loads(inp.read('MANIFEST.json'));assert len(im)==2806 and set(inp.namelist())==set(im)|{'MANIFEST.json'}
  for n,v in im.items():assert ident(inp.read(n))==v
 print(json.dumps({'identity':ident(raw),'entries':len(ns),'manifested_hashes':len(m),'CRC':'PASS','safe_exact_membership':'PASS','all_review_hashes':'PASS','exact_embedded_target_and_all_2806_hashes':'PASS','independent_completed_controls':c['independent_completed_controls']}))
