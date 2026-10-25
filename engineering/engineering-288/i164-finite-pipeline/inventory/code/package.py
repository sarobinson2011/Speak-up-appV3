"""Exact checkpoint packaging/recovery; no candidate imports."""
import argparse,hashlib,json,pathlib,stat,zipfile

def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(v,msg):
 if not v:raise ValueError(msg)
def verify(p,dest=None):
 with zipfile.ZipFile(p) as z:
  names=z.namelist();need(len(names)==len(set(names)) and z.testzip() is None,'CRC/UNIQUE')
  for i in z.infolist():
   n=pathlib.PurePosixPath(i.filename);need(not n.is_absolute() and '..' not in n.parts and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG),'ENTRY')
  m=json.loads(z.read('MANIFEST.json'));need(set(names)==set(m)|{'MANIFEST.json'},'MEMBERS')
  for n,v in m.items():need(ident(z.read(n))==v,'HASH:'+n)
  if dest:
   dest=pathlib.Path(dest);need(not dest.exists() and '/tmp' not in str(dest.absolute()),'NEW-PERSISTENT');dest.mkdir(parents=True)
   for n in names:
    p=dest/n;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(z.read(n))
   need({p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_file()}==set(names),'EXTRACTED-MEMBERS')
   for n,v in m.items():need(ident((dest/n).read_bytes())==v,'EXTRACTED-HASH:'+n)
 return {'crc':'PASS','exact_membership':'PASS','manifest_hashes':'PASS','fresh_extraction':'PASS' if dest else 'NOT REQUESTED','entries':len(names)}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('archive');a.add_argument('--extract');args=a.parse_args();print(json.dumps(verify(args.archive,args.extract),indent=2))
