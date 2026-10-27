from pathlib import Path,PurePosixPath
import hashlib,io,json,stat,sys,zipfile
p=Path(sys.argv[1]);raw=p.read_bytes()
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 infos=z.infolist();assert len(infos)==len(set(i.filename for i in infos)) and z.testzip() is None
 for i in infos:
  n=PurePosixPath(i.filename);assert not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and str(n)==i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG
 members=json.loads(z.read('MANIFEST.json'))['members'];assert set(members)==set(z.namelist())-{'MANIFEST.json'}
 for n,pin in members.items():
  b=z.read(n);assert pin=={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},n
 target=z.read('input/I164-recovery-field-correspondence-1.zip');assert len(target)==39038102 and hashlib.sha256(target).hexdigest()=='c92840a853097a9fe5fd1cd80134649fdd25a7463422cce81361a46bec70f8cf'
 with zipfile.ZipFile(io.BytesIO(target)) as t:assert len(t.infolist())==617 and t.testzip() is None
 cp=json.loads(z.read('CHECKPOINT.json'));assert cp['finding']['status']=='OPEN' and cp['finding']['public_validation_bypass'] is False and cp['boundaries']['admission'] is False
print(json.dumps({'archive':p.name,'bytes':len(raw),'entries':len(infos),'sha256':hashlib.sha256(raw).hexdigest(),'CRC':'PASS','safe_exact_membership':'PASS','manifest_hashes':'PASS','exact_embedded_target':'PASS','finding':'HF-01 OPEN; public gate rejects witness'},sort_keys=True))
