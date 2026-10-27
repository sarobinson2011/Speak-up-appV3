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
 target=z.read('input/I164-binding-return-correspondence-1.zip');assert len(target)==40870457 and hashlib.sha256(target).hexdigest()=='269e5e439de97fe77fcacba484c544b276457db7643cc5863875ef227331dc4f'
 with zipfile.ZipFile(io.BytesIO(target)) as t:
  assert len(t.infolist())==844 and t.testzip() is None;m=json.loads(t.read('MANIFEST.json'));assert len(m)==843 and set(m)==set(t.namelist())-{'MANIFEST.json'}
  for n,pin in m.items():
   b=t.read(n);assert pin=={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 cp=json.loads(z.read('CHECKPOINT.json'));assert cp['verdict'].startswith('SUPPORTED for bounded') and cp['boundaries']['admission'] is False and cp['observation_limits']['actual_getter_count'] is None
 assert b'{{COUNTS}}' not in z.read('REPORT.md')
print(json.dumps({'archive':p.name,'bytes':len(raw),'entries':len(infos),'sha256':hashlib.sha256(raw).hexdigest(),'CRC':'PASS','safe_exact_membership':'PASS','manifest_hashes':'PASS','exact_embedded_input':'PASS','verdict':'SUPPORTED, scoped'},sort_keys=True))
