"""Byte-only nested recovery; no candidate or application execution, no database connection."""
from pathlib import Path,PurePosixPath
import io,zipfile,json,hashlib,stat,sys,os
B=Path(__file__).resolve().parents[1]
LINE172_REVIEW={'bytes':160663290,'sha256':'156f5a7cca4b3966ac348d3bf6a0636a69ebd1c66375bb0c1277d929e4e37251'}
LINE172_AUTHOR={'bytes':159370715,'sha256':'2b6d61b3f9dc756740a0c66f4bdf70a729cfb77d43beb495424965331aa72bd1'}
CLOSURE={'bytes':154107404,'sha256':'7971a5cd95ef8775ff05e2db0ef5c3521903586c0d530b9e590b4bb54029fcef'}
AUTHOR={'bytes':153799952,'sha256':'ae83c5eeb7bf4ab09943f66f239bea3c7802777899f4fe6417e10e39dc9b1f71'}
REVIEW={'bytes':156078207,'sha256':'212d2f0886cb09cddb119470ba908e2142bb141a6eb6bdca83a3e5f83b82cbcb'}
ORIGINAL={'bytes':155659416,'sha256':'14bfe3fcc3da3f5f8e2ab6cfb3c820229f1520b439b9ebaf5f6bad83daf25c50'}
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def unique(pairs):
 d={}
 for k,v in pairs:assert k not in d,k;d[k]=v
 return d
def js(b):return json.loads(b,object_pairs_hook=unique)
def safe(n):
 p=PurePosixPath(n);assert n and str(p)==n and not p.is_absolute() and '\\' not in n and '\x00' not in n and all(x not in ('','.','..') for x in n.split('/'));return n
def contents(raw,pin,count):
 assert ident(raw)==pin
 z=zipfile.ZipFile(io.BytesIO(raw));names=[safe(i.filename) for i in z.infolist()]
 assert len(names)==len(set(names))==count
 for i in z.infolist():assert i.orig_filename==i.filename and stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1
 m=js(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
 for n,p in m.items():assert ident(z.read(n))==p,n
 return z
def write(root,n,b):
 p=root/safe(n);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
def verify(root):
 m=js((root/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs,n;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in expected,n;files.add(n)
 walk(root);assert files==expected and seen==dirs
 for n,p in m.items():assert ident((root/n).read_bytes())==p,n
 return {'files':len(files),'directories':len(dirs),'manifest':ident((root/'MANIFEST.json').read_bytes())}
def add_files(root,z):
 for n,pin in js(z.read('ADDITIONS-MANIFEST.json')).items():
  assert not n.startswith('retained/');raw=z.read('root-additions/'+safe(n));assert ident(raw)==pin;write(root,n,raw)
 write(root,'MANIFEST.json',z.read('ROOT-MANIFEST.json'));return verify(root)
def main():
 root=Path(sys.argv[1]).absolute();assert not root.exists() and not root.is_symlink();root.mkdir(parents=True)
 print('1/4 Verify exact retained line172 review and author checkpoint',flush=True)
 review=contents((B/'retained/Formal-Lab6-I164-cleanup-error-report-independent-review.zip').read_bytes(),LINE172_REVIEW,83)
 line=contents(review.read('input/I164-cleanup-error-report-correspondence-1.zip'),LINE172_AUTHOR,83);review.close()
 print('2/4 Recover exact nested EC01/cleanup root as bytes only',flush=True)
 closure=contents(line.read('retained/Formal-Lab6-I164-EC01-independent-closure.zip'),CLOSURE,52)
 author=contents(closure.read('input/I164-EC01-terminal-exception-correction-1.zip'),AUTHOR,57);closure.close()
 review=contents(author.read('retained/Formal-Lab6-I164-exceptional-cleanup-append-independent-review.zip'),REVIEW,85)
 original=contents(review.read('input/I164-exceptional-cleanup-append-correspondence-1.zip'),ORIGINAL,3982);review.close()
 report=root/'retained/report';prior=report/'retained/cleanup'
 for n in original.namelist():write(prior,n,original.read(n))
 original.close()
 for n,pin in js(author.read('OVERLAY-MANIFEST.json')).items():
  safe(n);raw=author.read('overlay/'+n);assert ident(raw)==pin;q=prior/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
 (prior/'MANIFEST.json').write_bytes(author.read('ROOT-MANIFEST.json'));author.close();verify(prior)
 print('3/4 Reconstruct unchanged line172 root and add declared loop extension',flush=True)
 add_files(report,line);line.close()
 for n,pin in js((B/'ADDITIONS-MANIFEST.json').read_bytes()).items():
  assert not n.startswith('retained/');raw=(B/'root-additions'/safe(n)).read_bytes();assert ident(raw)==pin;write(root,n,raw)
 write(root,'MANIFEST.json',(B/'ROOT-MANIFEST.json').read_bytes())
 print('4/4 Exact filesystem membership, types and hash verification',flush=True)
 print(json.dumps({'status':'PASS',**verify(root),'candidate_executed':False,'database_connections':0,'session_operations':0}),flush=True)
if __name__=='__main__':main()
