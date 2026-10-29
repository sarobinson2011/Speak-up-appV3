from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,stat,sys
PIN={'bytes':68317556,'sha256':'5915d8d409d043e9dd95535e91880263e26c776220b8c6d48bf75690e3fc60a9'}
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify_archive(p,dest):
 b=p.read_bytes();assert ident(b)==PIN
 with zipfile.ZipFile(p) as z:
  infos=z.infolist();assert len(infos)==2053;assert z.testzip() is None
  names=[i.filename for i in infos];assert len(names)==len(set(names))
  for i in infos:
   n=i.filename;q=PurePosixPath(n);mode=i.external_attr>>16
   assert n and not n.startswith('/') and '\\' not in n and not any(c in ('','.','..') for c in n.split('/'))
   assert str(q)==n and not i.is_dir() and not(i.flag_bits&1)
   assert stat.S_IFMT(mode) in (0,stat.S_IFREG),(n,oct(mode))
  m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'};assert len(m)==2052
  for n,v in m.items():assert ident(z.read(n))==v,n
  parents=set()
  for n in names:
   parents.update(str(x) for x in PurePosixPath(n).parents if str(x)!='.')
  assert not set(names)&parents
  if dest.exists():raise AssertionError('destination exists')
  dest.mkdir()
  for i in infos:
   t=dest/i.filename;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(z.read(i.filename))
  result={'archive':ident(b),'entries':len(names),'manifested_hashes':len(m),'CRC':'PASS','safe_unique_regular_membership':'PASS','implied_directories':len(parents),'manifest':ident(z.read('MANIFEST.json'))}
  check_tree(dest,names,parents,m,ident(z.read('MANIFEST.json')))
  return result
def check_tree(root,names,parents,m,mident):
 files=set();dirs=set()
 for p in root.rglob('*'):
  md=p.lstat().st_mode;n=p.relative_to(root).as_posix()
  if stat.S_ISREG(md):files.add(n)
  elif stat.S_ISDIR(md):dirs.add(n)
  else:raise AssertionError(('special',n))
 assert files==set(names) and dirs==parents
 for n in names:assert ident((root/n).read_bytes())==(mident if n=='MANIFEST.json' else m[n]),n
if __name__=='__main__':
 p=Path(sys.argv[1]);out=Path(sys.argv[2]);r=verify_archive(p,out);print(json.dumps(r,indent=2))
