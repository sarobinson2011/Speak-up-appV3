"""Reconstruct the exact corrected input tree from the retained review and minimal overlay.
This script verifies/copies bytes only. It runs no candidate or application code.
"""
from pathlib import Path,PurePosixPath
import io,json,hashlib,stat,zipfile,sys,os
B=Path(__file__).resolve().parents[1]
REVIEW={'bytes':156078207,'sha256':'212d2f0886cb09cddb119470ba908e2142bb141a6eb6bdca83a3e5f83b82cbcb'}
BASE={'bytes':155659416,'sha256':'14bfe3fcc3da3f5f8e2ab6cfb3c820229f1520b439b9ebaf5f6bad83daf25c50'}
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def unique(pairs):
 d={}
 for k,v in pairs:assert k not in d,k;d[k]=v
 return d
def js(b):return json.loads(b,object_pairs_hook=unique)
def safe(n):
 p=PurePosixPath(n);assert n and str(p)==n and not p.is_absolute() and '\\' not in n and '\x00' not in n and all(x not in ('','.','..') for x in n.split('/'));return n
def names(z,count):
 ns=[safe(i.filename) for i in z.infolist()];assert len(ns)==len(set(ns))==count
 for i in z.infolist():assert i.orig_filename==i.filename and stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1
 m=js(z.read('MANIFEST.json'));assert set(ns)==set(m)|{'MANIFEST.json'}
 return ns,m
def main():
 root=Path(sys.argv[1]).resolve();assert not root.exists();root.mkdir(parents=True)
 print('1/3 Verify exact retained independent review and original candidate bytes',flush=True)
 raw=(B/'retained/Formal-Lab6-I164-exceptional-cleanup-append-independent-review.zip').read_bytes();assert ident(raw)==REVIEW
 base=None
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  ns,m=names(z,85)
  for n in ns:
   b=z.read(n)
   if n in m:assert ident(b)==m[n],n
   if n=='input/I164-exceptional-cleanup-append-correspondence-1.zip':base=b
 assert ident(base)==BASE
 print('2/3 Recover original files and apply only declared EC01 overlay',flush=True)
 with zipfile.ZipFile(io.BytesIO(base)) as z:
  ns,m=names(z,3982)
  for n in ns:
   b=z.read(n)
   if n in m:assert ident(b)==m[n],n
   p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 om=js((B/'OVERLAY-MANIFEST.json').read_bytes());changed=js((B/'overlay/ec01/provenance/changed-files.json').read_bytes())['intentional_existing_file_changes']
 assert set(changed)=={'code/managed_coverage.py','code/correspondence.py','tests/cases.py'}
 for n,pin in om.items():
  safe(n);p=B/'overlay'/n;assert stat.S_ISREG(p.lstat().st_mode);b=p.read_bytes();assert ident(b)==pin
  q=root/n
  if n in m:assert n in changed and ident(q.read_bytes())==changed[n]['before'] and pin==changed[n]['after']
  else:assert n.startswith('ec01/') and not q.exists()
  q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 (root/'MANIFEST.json').write_bytes((B/'ROOT-MANIFEST.json').read_bytes())
 print('3/3 Verify corrected exact membership, entry types and all file identities',flush=True)
 expected=js((root/'MANIFEST.json').read_bytes());files=set(expected)|{'MANIFEST.json'};dirs={p.as_posix() for n in files for p in Path(n).parents if p.as_posix()!='.'};found=set();seen=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in files;found.add(n)
 walk(root);assert found==files and seen==dirs
 for n,pin in expected.items():assert ident((root/n).read_bytes())==pin,n
 print(json.dumps({'status':'PASS','root':str(root),'files':len(found),'directories':len(seen),'manifest':ident((root/'MANIFEST.json').read_bytes()),'code_executed':False}),flush=True)
if __name__=='__main__':main()
