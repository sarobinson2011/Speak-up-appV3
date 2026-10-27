"""Separate fresh-process verification of the sealed independent review."""
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
 target=z.read('input/I164-HF01-correction.zip');assert len(target)==39924668 and hashlib.sha256(target).hexdigest()=='0e2cce5d4519ccaaab35e34af0f89ef01b8a773569fba66008ee7affb1a9529c'
 with zipfile.ZipFile(io.BytesIO(target)) as t:
  assert len(t.infolist())==732 and t.testzip() is None
  m=json.loads(t.read('MANIFEST.json'));assert set(m)==set(t.namelist())-{'MANIFEST.json'} and len(m)==731
  for n,pin in m.items():
   b=t.read(n);assert pin=={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 cp=json.loads(z.read('CHECKPOINT.json'));assert cp['verdict']=='HF-01 CLOSED within the retained saved-evidence correspondence contract' and cp['boundaries']['admission'] is False
 assert b'{{INDEPENDENT_COUNTS}}' not in z.read('REPORT.md')
print(json.dumps({'archive':p.name,'bytes':len(raw),'entries':len(infos),'sha256':hashlib.sha256(raw).hexdigest(),'CRC':'PASS','safe_exact_membership':'PASS','manifest_hashes':'PASS','exact_embedded_target':'PASS','verdict':'HF-01 CLOSED, scoped'},sort_keys=True))
