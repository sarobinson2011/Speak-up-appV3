from pathlib import Path,PurePosixPath
import hashlib,io,json,stat,sys,zipfile
p=Path(sys.argv[1]);raw=p.read_bytes();z=zipfile.ZipFile(io.BytesIO(raw));infos=z.infolist()
assert len(infos)==len(set(i.filename for i in infos)) and z.testzip() is None
for i in infos:
 n=PurePosixPath(i.filename)
 assert not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and str(n)==i.filename
 assert not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
m=json.loads(z.read('MANIFEST.json'))['members'];assert set(m)==set(z.namelist())-{'MANIFEST.json'}
for n,v in m.items():
 b=z.read(n);assert v=={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},n
target=z.read('input/I164-SOC02-R1-correction.zip')
assert len(target)==30156228 and hashlib.sha256(target).hexdigest()=='eb8f0c74f1431a00cfe67e7b756a7e3416385a34bebaa0e2b3981c063898092f'
with zipfile.ZipFile(io.BytesIO(target)) as t:assert len(t.namelist())==520 and t.testzip() is None
print(json.dumps({'archive':p.name,'bytes':len(raw),'entries':len(infos),'sha256':hashlib.sha256(raw).hexdigest(),'CRC':'PASS','safe_exact_membership':'PASS','manifest_hashes':'PASS','embedded_target':'PASS'},sort_keys=True))
