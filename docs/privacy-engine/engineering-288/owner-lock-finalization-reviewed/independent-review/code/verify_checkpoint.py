"""Verify final deliverable, including the unchanged embedded target; no candidate execution."""
from pathlib import Path,PurePosixPath
import hashlib,io,json,stat,zipfile
w=Path(__file__).resolve().parents[2];target=w/'Formal-Lab6-I164-owner-lock-finalization-independent-review.zip'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
with zipfile.ZipFile(target) as z:
 names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
 for i in z.infolist():
  p=PurePosixPath(i.filename);assert str(p)==i.filename and not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG
 manifest=json.loads(z.read('MANIFEST.json'));assert set(manifest)==set(names)-{'MANIFEST.json'}
 for n,pin in manifest.items():assert ident(z.read(n))==pin,n
 raw=z.read('input/I164-owner-lock-finalization-correspondence-1.zip');assert ident(raw)=={'bytes':74161617,'sha256':'09f8b6d8c527f4032977f4e2862ba9a23e0e678a6f8294a5050603a26fb43a9b'}
 with zipfile.ZipFile(io.BytesIO(raw)) as zi:
  assert len(zi.infolist())==2495 and zi.testzip() is None;mi=json.loads(zi.read('MANIFEST.json'));assert set(mi)==set(zi.namelist())-{'MANIFEST.json'}
  for n,pin in mi.items():assert ident(zi.read(n))==pin,n
 check=json.loads(z.read('CHECKPOINT.json'));assert check['independent_completed_controls']==323 and check['implementation_changed'] is False and check['smallest_residual_witness'] is None
 for name,v in check['independent'].items():assert ident(z.read(name+'/RESULT.json'))==v['result_identity']
print(json.dumps({'result':'PASS','file':str(target),'entries':len(names),'manifested_hashes':len(manifest),'CRC':'PASS','safe_exact_membership':'PASS','all_hashes':'PASS','embedded_target':'EXACT; CRC and all manifested hashes PASS',**ident(target.read_bytes())},indent=2))
