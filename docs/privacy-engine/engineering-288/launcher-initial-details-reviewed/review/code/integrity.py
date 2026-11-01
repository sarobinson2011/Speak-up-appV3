from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,stat,os,ast,difflib
BASE=Path('/workspace/scratch/ace5c9b2f18b');INPUT=BASE/'upload/I164-LD01-monitoring-lease-correction-1(1).zip';EVIDENCE=Path('/workspace/review-evidence/FL6-LD01-20261101')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(x):return (json.dumps(x,sort_keys=True,indent=2)+'\n').encode()
def unique(pairs):
 d={}
 for k,v in pairs:
  assert k not in d,('duplicate JSON key',k);d[k]=v
 return d
def js(b):return json.loads(b,object_pairs_hook=unique)
def safe(n):
 p=PurePosixPath(n);assert n and '\\' not in n and '\x00' not in n and not p.is_absolute() and all(x not in ('','.','..') for x in n.split('/')) and str(p)==n,n
 return n
def verify_root(root):
 root=Path(root);manifest=js((root/'MANIFEST.json').read_bytes());expected=set(manifest)|{'MANIFEST.json'};dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'};found=set();seen=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs,n;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in expected,n;found.add(n)
 walk(root);assert found==expected and seen==dirs
 for n,pin in manifest.items():assert ident((root/n).read_bytes())==pin,n
 return {'root':str(root),'files':len(found),'directories':len(seen),'hashes':'PASS','exact_membership':'PASS'}
def main():
 pin=ident(INPUT.read_bytes());assert pin=={'bytes':139583348,'sha256':'e4accc10b74390d08266853a0da649c8e4c235ce839bbf2b9bb9548926f7c97c'}
 EVIDENCE.mkdir(parents=True,exist_ok=False)
 with zipfile.ZipFile(INPUT) as z:
  infos=z.infolist();names=[safe(i.filename) for i in infos];assert len(names)==len(set(names))==3771
  for i in infos:assert i.orig_filename==i.filename and stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1,i.filename
  manifest=js(z.read('MANIFEST.json'));assert len(manifest)==3770 and set(names)==set(manifest)|{'MANIFEST.json'}
  for n,p in manifest.items():safe(n);assert ident(z.read(n))==p,n
  primary=EVIDENCE/'primary';recovered=EVIDENCE/'recovered'
  for root in (primary,recovered):
   root.mkdir()
   for n in names:
    p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
 old=js((primary/'retained/ld01-original/MANIFEST.json').read_bytes());assert len(old)==3555
 oldroot=EVIDENCE/'original';oldroot.mkdir()
 for n in [*old,'MANIFEST.json']:
  source=primary/('retained/ld01-original/'+n if n in ('MANIFEST.json','code/correspondence.py') else n)
  raw=source.read_bytes()
  if n!='MANIFEST.json':assert ident(raw)==old[n],n
  p=oldroot/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 changed=[n for n,p in old.items() if ident((primary/n).read_bytes())!=p];assert changed==['code/correspondence.py'],changed
 a=(oldroot/'code/correspondence.py').read_bytes();b=(primary/'code/correspondence.py').read_bytes();ta=ast.parse(a);tb=ast.parse(b)
 fa=next(n for n in ta.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor');fb=next(n for n in tb.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor')
 assert a.splitlines(True)[:fa.lineno-1]==b.splitlines(True)[:fb.lineno-1] and a.splitlines(True)[fa.end_lineno:]==b.splitlines(True)[fb.end_lineno:]
 assert [ast.dump(n) for n in ta.body if n is not fa]==[ast.dump(n) for n in tb.body if n is not fb]
 declared=js((primary/'ld01/provenance/changed-files.json').read_bytes());assert declared['before']==ident(a) and declared['after']==ident(b)
 diff=''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile='original/code/correspondence.py',tofile='corrected/code/correspondence.py'));assert diff==(primary/'ld01/provenance/implementation.diff').read_text()
 # The prior review manifest authenticates retained review files and the exact input's declared recovery identity; no recompression claim.
 review=primary/'retained/ld01-review';rm=js((review/'MANIFEST.json').read_bytes());kept=0
 for n,p in rm.items():
  if n=='input/I164-launcher-initial-details-correspondence-1.zip':assert p=={'bytes':137529057,'sha256':'aad7b718ce6c6b8f4827d68622447ec3872cf3b6bbfd7d41effaf5db7667bdb1'}
  else:assert ident((review/n).read_bytes())==p,n;kept+=1
 frozen={}
 for n in ('ld01/preparation/frozen-manifest.json','ld01/provenance/recovery-cut-manifest.json'):
  m=js((primary/n).read_bytes())
  for k,p in m.items():assert ident((primary/k).read_bytes())==p,k
  frozen[n]=len(m)
 oldreceipt=(primary/'results/primary/launcher-details.json').read_bytes();newreceipt=(primary/'ld01/receipts/corrected-launcher-details.json').read_bytes();ov=js(oldreceipt);nv=js(newreceipt);np=nv['extension_components']['correspondence.py'];assert np==ident(b)
 undo=js(newreceipt);undo['extension_components']['correspondence.py']=ident(a);canonical=lambda v:(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode();assert canonical(undo)==oldreceipt and canonical(nv)==newreceipt
 result={'input':pin,'entries':3771,'manifested_hashes':3770,'CRC':'PASS','safe_exact_membership':'PASS','manifest':ident((primary/'MANIFEST.json').read_bytes()),'roots':{k:verify_root(v) for k,v in [('primary',primary),('recovered',recovered),('original',oldroot)]},'original_declared_members_preserved':3556,'sole_changed_existing_member':changed,'only_changed_function':'_public_predecessor','implementation':declared,'prior_review_noninput_files_verified':kept,'frozen_members':frozen,'intermediate_compressed_archives_freshly_verified':False,'receipt':{'original':ident(oldreceipt),'corrected':ident(newreceipt),'sole_path':'/extension_components/correspondence.py','preparation_not_validation':True}}
 (BASE/'ld01-review/results/integrity.json').write_bytes(enc(result));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
