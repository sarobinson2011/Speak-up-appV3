from pathlib import Path,PurePosixPath
import json,hashlib,stat,zipfile
BASE=Path('/workspace/scratch/ace5c9b2f18b');record=json.loads((BASE/'cc-package.json').read_bytes());p=Path(record['archive'])
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert pin(p.read_bytes())==record['identity']
with zipfile.ZipFile(p) as z:
 names=z.namelist();assert len(names)==record['entries']==len(set(names));assert z.testzip() is None
 m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'} and len(m)==record['manifested_hashes']
 for i in z.infolist():
  n=i.filename;q=PurePosixPath(n);assert not q.is_absolute() and '..' not in q.parts and '\\' not in n and ':' not in n and q.as_posix()==n and not i.is_dir() and stat.S_ISREG(i.external_attr>>16)
  if n!='MANIFEST.json':assert pin(z.read(n))==m[n],n
 checkpoint=json.loads(z.read('CHECKPOINT.json'));assert pin(z.read('input/I164-control-callback-exception-correspondence-1.zip'))==checkpoint['input']
 record.update(CRC='PASS',safe_exact_membership='PASS',all_manifested_hashes='PASS',embedded_exact_input='PASS',independent_control_total=checkpoint['independent_controls'])
(BASE/'cc-verified-checkpoint.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n');print(json.dumps(record,indent=2))
