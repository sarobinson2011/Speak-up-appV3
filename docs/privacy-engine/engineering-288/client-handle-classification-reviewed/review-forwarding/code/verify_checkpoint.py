"""Verify this review's sealed bytes, without running candidate validators."""
from pathlib import Path,PurePosixPath
import hashlib,io,json,stat,sys,zipfile
p=Path(sys.argv[1]);raw=p.read_bytes()
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 infos=z.infolist();assert len(infos)==len({i.filename for i in infos}) and z.testzip() is None
 for i in infos:
  n=PurePosixPath(i.filename);assert not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and str(n)==i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG
 members=json.loads(z.read('MANIFEST.json'))['members'];assert set(members)==set(z.namelist())-{'MANIFEST.json'}
 for n,pin in members.items():
  b=z.read(n);assert pin=={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},n
 target=z.read('input/I164-client-handle-return-correspondence-1.zip');assert len(target)==43439616 and hashlib.sha256(target).hexdigest()=='1f7b1c7dc58949e76f73cac68afb00ea0373490ac0c07bdada86d954772b4431'
 with zipfile.ZipFile(io.BytesIO(target)) as t:
  assert len(t.infolist())==1282 and t.testzip() is None;m=json.loads(t.read('MANIFEST.json'));assert len(m)==1281 and set(m)==set(t.namelist())-{'MANIFEST.json'}
  for n,pin in m.items():
   b=t.read(n);assert pin=={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 cp=json.loads(z.read('CHECKPOINT.json'));assert cp['verdict'].startswith('SCOPED SUPPORT') and cp['boundaries']['admission'] is False and cp['observation_limits']['actual_client_handle_call_count'] is None
 f=z.read('failures/recovered-root-membership/unexpected-0.bin');assert len(f)==15990784 and hashlib.sha256(f).hexdigest()=='2e32d7c9c898a01c82b97f8a0c0639730f4548c6703c24b5e323e0a587b9d682'
 assert b'{{COUNTS}}' not in z.read('REPORT.md') and b'{{VERDICT}}' not in z.read('REPORT.md')
print(json.dumps({'archive':p.name,'bytes':len(raw),'entries':len(infos),'sha256':hashlib.sha256(raw).hexdigest(),'CRC':'PASS','safe_exact_membership':'PASS','manifest_hashes':'PASS','exact_embedded_input':'PASS','preserved_refusal_bytes':'PASS','verdict':'SCOPED SUPPORT; interruption flag interpretation caveat'},sort_keys=True))
