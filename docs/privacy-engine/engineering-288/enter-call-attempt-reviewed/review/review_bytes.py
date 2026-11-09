"""Independent archive and byte auditing only; no candidate import."""
import gzip,hashlib,json,os,stat,tarfile,zipfile
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def fid(p):
    h=hashlib.sha256();n=0
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b);n+=len(b)
    return {'bytes':n,'sha256':h.hexdigest()}
def read(p):return json.loads(Path(p).read_bytes())
def save(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(v,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
def safe(n):
    assert type(n) is str and n and '\\' not in n and '\x00' not in n and not n.startswith('/'),repr(n)
    assert ':' not in n.split('/')[0] and all(x not in ('','.','..') for x in n.split('/')),repr(n)
    return n
def unzip(src,dest,pin=None):
    if pin:assert fid(src)==pin,(src,fid(src),pin)
    files={}
    with zipfile.ZipFile(src) as z:
        assert z.testzip() is None
        for x in z.infolist():
            n=safe(x.filename);assert n not in files and not x.is_dir() and not x.flag_bits&1 and stat.S_IFMT(x.external_attr>>16) in (0,stat.S_IFREG),n
            files[n]=z.read(x)
    manifest=json.loads(files['MANIFEST.json']);assert set(files)==set(manifest)|{'MANIFEST.json'}
    for n,pin_ in manifest.items():assert ident(files[n])==pin_,n
    dest.mkdir(parents=True,exist_ok=False)
    for n,b in files.items():
        p=dest/n;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(b)
    return {'identity':fid(src),'entries':len(files),'manifested_hashes':len(manifest),'CRC':'PASS','safe_exact_membership':'PASS','files':{n:ident(b) for n,b in files.items()}}
def untar_host(src,dest):
    assert fid(src)=={'bytes':7692623,'sha256':'fb367b2210875601b83c2629abae36ce7ee3fb8a54b34f40a89af0f58d5a6c51'}
    nbytes=0
    with gzip.open(src,'rb') as g:
        for b in iter(lambda:g.read(1024*1024),b''):nbytes+=len(b)
    files={}
    with tarfile.open(src,'r:gz') as t:
        for m in t.getmembers():
            n=safe(m.name);assert n not in files and m.isfile(),(n,m.type)
            files[n]=t.extractfile(m).read()
    assert len(files)==621
    exported=json.loads(files['EXPORT-MANIFEST.json']);assert len(exported)==619 and set(files)==set(exported)|{'EXPORT-MANIFEST.json','EXPORT-STATUS.json'}
    for n,pin in exported.items():assert ident(files[n])==pin,n
    prepared=json.loads(files['MANIFEST.json'])
    for n,pin in prepared.items():assert n in files and ident(files[n])==pin,n
    dest.mkdir(exist_ok=False)
    for n,b in files.items():
        p=dest/n;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(b)
    return {'identity':fid(src),'gzip_integrity':'PASS','gzip_uncompressed_bytes':nbytes,'tar_headers':'PASS','safe_exact_membership':'PASS','entries':621,'regular_files':621,'manifested_hashes':619,'preparation_manifest_members':len(prepared),'all_preparation_pins':'PASS','files':{n:ident(b) for n,b in files.items()},'export_status':json.loads(files['EXPORT-STATUS.json'])}
def verify_tree(root,manifest):
    found={};dirs=set()
    def walk(path):
        for e in os.scandir(path):
            q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):dirs.add(n);walk(q)
            else:assert stat.S_ISREG(mode),n;found[n]=fid(q)
    walk(root);assert found==manifest,(set(found)^set(manifest))
    assert dirs=={str(p) for n in found for p in PurePosixPath(n).parents if str(p)!='.'}
    return {'files':len(found),'directories':len(dirs),'exact_types_membership_hashes':'PASS'}
if __name__=='__main__':
    audited={}
    try:
        audited['host']=untar_host(HERE/'inputs/I164-enter-call-attempt-public-1-host-evidence.tar.gz',HERE/'host')
        deps=read(HERE/'host/DEPENDENCIES.json')
        for k,dest in [('source','source'),('results','focused')]:
            v=deps[k];audited[k]=unzip(HERE/'host'/v['included'],HERE/dest,{x:v[x] for x in ('bytes','sha256')})
        d=deps['external_recovery_archive'];audited['launcher']=unzip(HERE/'inputs'/d['filename'],HERE/'launcher',{x:d[x] for x in ('bytes','sha256')});assert audited['launcher']['entries']==60
        d=deps['lookup_independent_review'];audited['prior_review']=unzip(HERE/'inputs/I164-context-special-lookup-1-independent-review.zip',HERE/'prior-review',{x:d[x] for x in ('bytes','sha256')});assert audited['prior_review']['entries']==307
        save(HERE/'archive-audit.json',audited);save(HERE/'archive-audit.exit.json',{'exit':0,'failure':None})
        print(json.dumps({k:{x:v[x] for x in ('identity','entries','manifested_hashes')} for k,v in audited.items()},indent=2),flush=True)
    except BaseException as e:save(HERE/'archive-audit.partial.json',audited);save(HERE/'archive-audit.exit.json',{'exit':1,'failure':repr(e)});raise
