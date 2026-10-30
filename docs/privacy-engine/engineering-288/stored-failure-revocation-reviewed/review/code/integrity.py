import sys,json,hashlib,stat,zipfile,os
from pathlib import Path,PurePosixPath
EXPECTED=(76307999,2661,'cd36a49cf2366c95aa96d8407e182eec716e6e77d261a1b0908ec250266230bf')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def archive(p,dest=None):
 b=Path(p).read_bytes(); assert len(b)==EXPECTED[0] and ident(b)['sha256']==EXPECTED[2]
 with zipfile.ZipFile(p) as z:
  ns=z.namelist(); assert len(ns)==EXPECTED[1] and len(set(ns))==len(ns)
  for i in z.infolist():
   n=i.filename; q=PurePosixPath(n); mode=i.external_attr>>16
   assert n and not q.is_absolute() and str(q)==n and '..' not in q.parts and '\\' not in n
   assert not i.is_dir() and stat.S_IFMT(mode) in (0,stat.S_IFREG) and not i.flag_bits&1
  assert z.testzip() is None
  manifest_raw=z.read('MANIFEST.json');m=json.loads(manifest_raw);assert set(ns)==set(m)|{'MANIFEST.json'}
  for n,v in m.items():assert ident(z.read(n))==v,(n,v)
  if dest:
   d=Path(dest);assert not d.exists();d.mkdir()
   for n in ns:
    p=d/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
 return {'identity':ident(b),'entries':len(ns),'manifested_hashes':len(m),'CRC':'PASS','safe_exact_membership':'PASS','manifest':ident(manifest_raw)}
def root(p):
 p=Path(p);m=json.loads((p/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={str(a) for n in expected for a in PurePosixPath(n).parents if str(a)!='.'};found=set();fd=set()
 for base,ds,fs in os.walk(p,followlinks=False):
  for n in ds+fs:
   x=Path(base)/n;r=x.relative_to(p).as_posix();s=x.lstat()
   if stat.S_ISDIR(s.st_mode):fd.add(r)
   else:assert stat.S_ISREG(s.st_mode),r;found.add(r)
 assert found==expected,(sorted(found-expected),sorted(expected-found));assert fd==dirs
 for n,v in m.items():assert ident((p/n).read_bytes())==v,n
 return {'files':len(found),'directories':len(fd),'hashes':'PASS','exact_membership':'PASS'}
if __name__=='__main__':
 z,d,o=sys.argv[1:];a=archive(z,d);a['manifest']=ident((Path(d)/'MANIFEST.json').read_bytes());a['root']=root(d);Path(o).write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a))
