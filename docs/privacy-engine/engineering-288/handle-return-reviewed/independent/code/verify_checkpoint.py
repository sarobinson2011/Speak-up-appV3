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
 target=z.read('input/I164-handle-return-correspondence-1.zip');assert len(target)==42330497 and hashlib.sha256(target).hexdigest()=='6b486b1ca0c49da010face18132507020a07f3db84602d62a7c75af0305caa8e'
 with zipfile.ZipFile(io.BytesIO(target)) as t:
  assert len(t.infolist())==1088 and t.testzip() is None;m=json.loads(t.read('MANIFEST.json'));assert len(m)==1087 and set(m)==set(t.namelist())-{'MANIFEST.json'}
  for n,pin in m.items():
   b=t.read(n);assert pin=={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 cp=json.loads(z.read('CHECKPOINT.json'));assert cp['verdict'].startswith('SUPPORTED within bounded') and cp['boundaries']['admission'] is False and cp['observation_limits']['actual_handle_call_count'] is None
 assert b'{{COUNTS}}' not in z.read('REPORT.md') and b'{{VERDICT}}' not in z.read('REPORT.md')
print(json.dumps({'archive':p.name,'bytes':len(raw),'entries':len(infos),'sha256':hashlib.sha256(raw).hexdigest(),'CRC':'PASS','safe_exact_membership':'PASS','manifest_hashes':'PASS','exact_embedded_input':'PASS','verdict':'SUPPORTED, scoped'},sort_keys=True))
