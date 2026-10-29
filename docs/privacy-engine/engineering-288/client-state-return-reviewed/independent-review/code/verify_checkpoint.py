from pathlib import Path,PurePosixPath
import hashlib,io,json,stat,sys,zipfile
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify(raw):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  ns=z.namelist();assert len(ns)==len(set(ns)) and z.testzip() is None
  for i in z.infolist():
   p=PurePosixPath(i.filename);assert str(p)==i.filename and not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
  m=json.loads(z.read('MANIFEST.json'));assert set(m)|{'MANIFEST.json'}==set(ns)
  for n,v in m.items():assert ident(z.read(n))==v,n
  return z,{**ident(raw),'entries':len(ns),'manifested_hashes':len(m),'CRC':'PASS','safe_exact_membership':'PASS'}
p=Path(sys.argv[1]);raw=p.read_bytes();z,result=verify(raw);embedded=z.read('input/I164-client-state-return-correspondence-1.zip');assert ident(embedded)=={'bytes':61624841,'sha256':'0ae24141a77f42eb96ed0f8d144f612d7a8045e04f7aa47dcaa8d1750f886907'}
_,inp=verify(embedded);assert inp['entries']==1688 and inp['manifested_hashes']==1687
cp=json.loads(z.read('CHECKPOINT.json'));assert cp['independent_results']['primary_checks']==273 and cp['independent_results']['recovered_checks']==196 and cp['boundaries']['admission'] is False
for field in ['REPORT.md','RECOVERY.md','results/composition.json','results/final-audit.json','failures/reviewer-handler-shape-attempt-1/results/RESULT.json']:assert field in z.namelist()
result.update(result='PASS',exact_input=inp,independent_checks=cp['independent_results']);print(json.dumps(result,indent=2))
