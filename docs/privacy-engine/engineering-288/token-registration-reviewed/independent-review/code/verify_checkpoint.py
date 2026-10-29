from pathlib import Path,PurePosixPath
import sys,io,json,zipfile,hashlib,stat
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
 target=z.read('input/I164-token-registration-correspondence-1.zip');assert ident(target)=={'bytes':69308990,'sha256':'84c714c62aa6aa3956e5b137d03e584b055c06b26200b6768090ad33a5e4dbeb'};t=verify(target);assert t['entries']==2178 and t['manifested_hashes']==2177
 cp=json.loads(z.read('CHECKPOINT.json'));assert cp['completed_independent_controls']==238 and cp['separate_actual_fresh_recovered_CLI']==1 and cp['total_completed_including_CLI']==239 and cp['boundaries']['admission'] is False and cp['residual_witness'] is None
 for group,count in [('independent-primary-v2',170),('independent-recovered',51),('fresh-semantic',7),('fresh-constructed',10)]:
  r=json.loads(z.read(group+'/RESULT.json'));assert r['result']=='PASS' and r['checks']==count and r['error'] is None
 audit=json.loads(z.read('results/final-audit.json'));assert audit['result']=='PASS' and len(audit['roots_verified_unchanged'])==7
 cli=json.loads(z.read('fresh-cli/RESULT.json'));assert cli['result']=='PASS' and cli['checks']==1 and cli['public_result']['actual_admission'] is False
 failed=json.loads(z.read('failures/reviewer-source-fragment/results/RESULT.json'));assert failed['result']=='FAIL' and failed['checks']==11
 for name in ['REPORT.md','RECOVERY.md','START-HERE.md','results/composition.json','independent-primary-v2/source-oracle.json','independent-primary-v2/independent-cases.json','failures/reviewer-diff-section/EXPLANATION.json']:assert name in z.namelist()
res.update(result='PASS',target=t,verdict=cp['verdict'],independent_controls=238,separate_CLI=1,failed_control_attempt_excluded=11);print(json.dumps(res,indent=2))
