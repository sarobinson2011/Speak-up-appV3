import json,zipfile,hashlib,stat,sys
from pathlib import Path,PurePosixPath
ARCHIVE=Path('/workspace/scratch/ace5c9b2f18b/upload/I164-owner-lock-finalization-correspondence-1(1).zip')
EXPECTED=(74161617,2495,'09f8b6d8c527f4032977f4e2862ba9a23e0e678a6f8294a5050603a26fb43a9b')
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(dest):
 raw=ARCHIVE.read_bytes(); assert len(raw)==EXPECTED[0] and sha(raw)==EXPECTED[2]
 with zipfile.ZipFile(ARCHIVE) as z:
  infos=z.infolist(); names=[i.filename for i in infos]
  assert len(names)==EXPECTED[1] and len(set(names))==len(names)
  for i in infos:
   p=PurePosixPath(i.filename); mode=i.external_attr>>16
   assert not p.is_absolute() and '..' not in p.parts and str(p)==i.filename and '\\' not in i.filename
   assert not i.is_dir() and stat.S_IFMT(mode) in (0,stat.S_IFREG)
   assert not i.flag_bits&1
  assert z.testzip() is None
  manifest=json.loads(z.read('MANIFEST.json'))
  assert set(manifest)==set(names)-{'MANIFEST.json'}
  for n,v in manifest.items():
   b=z.read(n);assert len(b)==v['bytes'] and sha(b)==v['sha256'],n
  dest=Path(dest); assert not dest.exists();dest.mkdir()
  for n in names:
   p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
  assert set(p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_file())==set(names)
  dirs={str(PurePosixPath(n).parent) for n in names}
  dirs=set(str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.')
  assert {p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_dir()}==dirs
  return {'archive':ARCHIVE.name,'bytes':len(raw),'entries':len(names),'sha256':sha(raw),'crc':'PASS','safe_exact_regular_membership':'PASS','manifest_hashes':len(manifest),'recovered_root':str(dest.resolve()),'directories':len(dirs),'uncompressed_bytes':sum(i.file_size for i in infos)}
if __name__=='__main__':
 if len(sys.argv)>2:ARCHIVE=Path(sys.argv[2])
 result=verify(sys.argv[1]);print(json.dumps(result,indent=2))
