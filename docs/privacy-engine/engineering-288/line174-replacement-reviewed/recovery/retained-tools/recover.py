"""Byte-only recovery of NEW replacement checkpoint; no candidate validation."""
from pathlib import Path,PurePosixPath
import sys,zipfile,hashlib,json,stat,subprocess,os
B=Path(__file__).resolve().parents[1]
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def unpack(raw,path,pin,count):
 import io
 assert ident(raw)==pin and not path.exists();path.mkdir(parents=True)
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  ns=z.namelist();m=json.loads(z.read('MANIFEST.json'));assert len(ns)==len(set(ns))==count and set(ns)==set(m)|{'MANIFEST.json'}
  for i in z.infolist():
   n=i.filename;assert str(PurePosixPath(n))==n and not n.startswith('/') and '..' not in PurePosixPath(n).parts and stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1
   b=z.read(n)
   if n in m:assert ident(b)==m[n]
   q=path/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
def main():
 target=Path(sys.argv[1]).absolute();assert not target.exists();deps=target.with_name(target.name+'-byte-recovery');assert not deps.exists()
 review={'bytes':176585667,'sha256':'da62fa43eaf66a37d86830bdbb3aa93a3f9f91aa3258237713cde69a196e53c7'}
 author={'bytes':169181718,'sha256':'a48cb3be9002e8dbdcf3ac8c6e2d0ed45ea1eced14126af3d9d1862ec1963dd5'}
 unpack((B/'retained/cleanup-loop-review.zip').read_bytes(),deps/'review',review,275)
 unpack((deps/'review/input/I164-cleanup-loop-exhaustion-correspondence-1.zip').read_bytes(),deps/'baseline',author,81)
 subprocess.run([sys.executable,'-I','-B',str(deps/'baseline/tools/recover.py'),str(target/'retained/loop')],check=True,timeout=180)
 for n,pin in json.loads((B/'ADDITIONS-MANIFEST.json').read_bytes()).items():
  assert not n.startswith('retained/') and '..' not in PurePosixPath(n).parts;b=(B/'root-additions'/n).read_bytes();assert ident(b)==pin
  q=target/n;q.parent.mkdir(parents=True,exist_ok=True)
  with q.open('xb') as f:f.write(b)
 (target/'MANIFEST.json').write_bytes((B/'ROOT-MANIFEST.json').read_bytes())
 m=json.loads((target/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(target).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs,n;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in expected,n;files.add(n)
 walk(target);assert files==expected and seen==dirs
 for n,pin in m.items():assert ident((target/n).read_bytes())==pin,n
 print(json.dumps({'byte_recovery':'PASS','files':len(files),'directories':len(dirs),'manifest':ident((target/'MANIFEST.json').read_bytes()),'candidate_validation_executed':False}),flush=True)
if __name__=='__main__':main()
