import pathlib,hashlib,json,zipfile,stat,sys
p=pathlib.Path(sys.argv[1]);dest=pathlib.Path(sys.argv[2]);out=pathlib.Path(sys.argv[3]);raw=p.read_bytes()
assert len(raw)==18817005 and hashlib.sha256(raw).hexdigest()=='31f3c7827ccad8e4d1a846bfee0a7e3dae25c560749bd0927e85ea81ce7839b3'
z=zipfile.ZipFile(p);names=z.namelist();assert len(names)==439 and len(set(names))==439 and z.testzip() is None
for i in z.infolist():
 n=pathlib.PurePosixPath(i.filename);assert not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and not stat.S_ISLNK(i.external_attr>>16) and not i.is_dir()
m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
for n,v in m.items():
 b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],n
z.extractall(dest)
r={'bytes':len(raw),'entries':len(names),'sha256':hashlib.sha256(raw).hexdigest(),'crc':'PASS','safe_unique_paths':'PASS','exact_membership':'PASS','manifest_files_verified':len(m)}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
