"""Verify exact checkpoint packaging and its unchanged embedded review target."""
from pathlib import Path,PurePosixPath
import hashlib,io,json,stat,sys,zipfile
path=Path(sys.argv[1]);raw=path.read_bytes()
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 infos=z.infolist();assert len(infos)==len(set(i.filename for i in infos)) and z.testzip() is None
 for i in infos:
  n=PurePosixPath(i.filename);assert not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and str(n)==i.filename
  assert not i.is_dir() and stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG
 members=json.loads(z.read('MANIFEST.json'))['members'];assert set(members)==set(z.namelist())-{'MANIFEST.json'}
 for n,pin in members.items():
  b=z.read(n);assert pin=={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},n
 target=z.read('input/I164-reference-transfer-correspondence-1.zip');assert len(target)==38786604 and hashlib.sha256(target).hexdigest()=='36e4dfd8199df3a9168e47416d1e2508a8868876170c3586734c5a714adadac9'
 with zipfile.ZipFile(io.BytesIO(target)) as t:assert len(t.infolist())==552 and t.testzip() is None
 cp=json.loads(z.read('CHECKPOINT.json'));assert cp['independent_checks']['primary_assertions']==276 and cp['boundaries']['admission'] is False
print(json.dumps({'archive':path.name,'bytes':len(raw),'entries':len(infos),'sha256':hashlib.sha256(raw).hexdigest(),'CRC':'PASS','safe_exact_membership':'PASS','manifest_hashes':'PASS','exact_embedded_target':'PASS'},sort_keys=True))
