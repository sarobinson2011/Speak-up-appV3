from pathlib import Path,PurePosixPath
import sys,hashlib,json,io,zipfile,stat
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify(raw):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  ns=z.namelist();assert len(ns)==len(set(ns)) and z.testzip() is None
  for i in z.infolist():
   p=PurePosixPath(i.filename);assert str(p)==i.filename and not p.is_absolute() and all(x not in ('','.','..') for x in i.filename.split('/')) and '\\' not in i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
  m=json.loads(z.read('MANIFEST.json'));assert set(m)|{'MANIFEST.json'}==set(ns)
  for n,v in m.items():assert ident(z.read(n))==v,n
  return {**ident(raw),'entries':len(ns),'manifested_hashes':len(m),'CRC':'PASS','safe_exact_membership':'PASS'}
raw=Path(sys.argv[1]).read_bytes();res=verify(raw)
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 embedded=z.read('input/I164-internal-status-return-correspondence-1.zip');assert ident(embedded)=={'bytes':62835317,'sha256':'06d3b32fdf83757b40d9963a45a21ca5a5a80d2ca5c4af813655b4ad465f3864'};target=verify(embedded);assert target['entries']==1845 and target['manifested_hashes']==1844
 cp=json.loads(z.read('CHECKPOINT.json'));assert cp['finding']['id']=='IS-01' and cp['independent_results']['primary']['checks']==206 and cp['independent_results']['recovered']['checks']==165 and cp['residual_acceptance_confirmations']==17 and cp['boundaries']['admission'] is False
 fr=json.loads(z.read('failures/initial-root-membership/RECORD.json'))
 for p in fr['undeclared_regular_files']:assert ident(z.read('failures/initial-root-membership/'+p['preserved_copy']))=={'bytes':p['bytes'],'sha256':p['sha256']}
 required=['REPORT.md','RECOVERY.md','results/composition.json','results/final-audit.json','independent-primary/full-type-witness/full-type-witnesses.json','independent-recovered/residual/residual-witnesses.json','independent-primary/key-types/key-type-witnesses.json','independent-recovered/key-full/key-type-full-witness.json','cli-recovered/RESULT.json'];assert all(p in z.namelist() for p in required)
res.update(result='PASS',target=target,verdict=cp['verdict'],independent_results=cp['independent_results']);print(json.dumps(res,indent=2))
