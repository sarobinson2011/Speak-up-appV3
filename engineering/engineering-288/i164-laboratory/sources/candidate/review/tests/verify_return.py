import hashlib,json,pathlib,stat,sys,tempfile,zipfile
p=pathlib.Path(sys.argv[1]);raw=p.read_bytes();z=zipfile.ZipFile(p);names=z.namelist()
assert len(names)==len(set(names)) and z.testzip() is None
for i in z.infolist():
 n=pathlib.PurePosixPath(i.filename);assert not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and not stat.S_ISLNK(i.external_attr>>16) and not i.is_dir()
m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
for n,v in m.items():
 b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],n
with tempfile.TemporaryDirectory() as td:
 z.extractall(td);d=pathlib.Path(td)
 assert {str(f.relative_to(d)) for f in d.rglob('*') if f.is_file()}==set(names)
 for n,v in m.items():
  b=(d/n).read_bytes();assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],n
r={'filename':p.name,'bytes':len(raw),'entries':len(names),'sha256':hashlib.sha256(raw).hexdigest(),'crc':'PASS','exact_membership':'PASS','manifest':'PASS','fresh_extraction':'PASS'}
print(json.dumps(r,indent=2))
