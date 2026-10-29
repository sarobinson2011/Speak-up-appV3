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
 target=z.read('input/I164-IS01-correction.zip');assert ident(target)=={'bytes':68317556,'sha256':'5915d8d409d043e9dd95535e91880263e26c776220b8c6d48bf75690e3fc60a9'};t=verify(target);assert t['entries']==2053 and t['manifested_hashes']==2052
 cp=json.loads(z.read('CHECKPOINT.json'));assert cp['corrected_checks']==207 and cp['original_witness_checks']==14 and cp['total_completed_checks']==221 and cp['boundaries']['admission'] is False and cp['residual_witness'] is None
 audit=json.loads(z.read('results/final-audit.json'));assert audit['result']=='PASS' and len(audit['roots_verified_unchanged'])==7
 failure=json.loads(z.read('failures/reviewer-obligation-pin-shape/focused-results/RESULT.json'));assert failure['result']=='FAIL' and failure['checks']==153
 for group,count in [('original-reproductions',14),('independent-recovered',154),('fresh-full-entries',20),('adjacent',27),('public-entries',6)]:
  rr=json.loads(z.read(group+'/RESULT.json'));assert rr['result']=='PASS' and rr['checks']==count
 for n in ['REPORT.md','RECOVERY.md','START-HERE.md','results/composition.json','original-reproductions/witnesses.json','independent-recovered/source-oracle.json','public-entries/public-result.json']:assert n in z.namelist()
res.update(result='PASS',target=t,verdict=cp['verdict'],corrected_checks=207,original_witness_checks=14,failed_attempt_excluded=153);print(json.dumps(res,indent=2))
