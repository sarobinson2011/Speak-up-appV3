from pathlib import Path, PurePosixPath
import hashlib, json, tarfile, zipfile, gzip, stat
B=Path(__file__).resolve().parent
def ident(p):
    return {'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()}
def safe(n):
    p=PurePosixPath(n)
    assert n and str(p)==n and not p.is_absolute() and '..' not in p.parts and '\\' not in n,n
def check(raw, pin):
    assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256'],pin
def zip_verify(p,d=None):
    with zipfile.ZipFile(p) as z:
        ns=z.namelist();assert len(set(ns))==len(ns)
        for x in z.infolist():
            safe(x.filename);assert not x.is_dir();assert stat.S_IFMT(x.external_attr>>16) in (0,stat.S_IFREG)
        assert z.testzip() is None
        m=json.loads(z.read('MANIFEST.json'));assert set(ns)==set(m)|{'MANIFEST.json'}
        for n,pin in m.items():check(z.read(n),pin)
        if d:
            assert not d.exists();d.mkdir(parents=True)
            for n in ns:
                f=d/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(z.read(n))
    return {**ident(p),'entries':len(ns),'manifested':len(m),'safe_exact_membership':True,'CRC':True}
def main():
    p=B/'inputs/I164-exit-decref-attempt-public-1-host-evidence.tar.gz'
    assert ident(p)=={'bytes':29287711,'sha256':'e23b29131ddaf0d184718b111e6510ff8ec06c000919b55beef70375c01638b2'}
    with gzip.open(p,'rb') as g:
        while g.read(1024*1024):pass
    with tarfile.open(p,'r:gz') as z:
        ms=z.getmembers();ns=[x.name for x in ms];assert len(ns)==676 and len(set(ns))==676
        for x in ms:safe(x.name);assert x.isfile() and not x.issparse(),x.name
        em=json.load(z.extractfile('EXPORT-MANIFEST.json'));pm=json.load(z.extractfile('MANIFEST.json'))
        extra=set(ns)-set(em);assert len(em)==674 and extra=={'EXPORT-MANIFEST.json','EXPORT.json'},extra
        for n,pin in em.items():check(z.extractfile(n).read(),pin)
        for n,pin in pm.items():check(z.extractfile(n).read(),pin)
        d=B/'host';assert not d.exists();d.mkdir()
        for x in ms:
            f=d/x.name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(z.extractfile(x).read())
    out={'host':{**ident(p),'entries':len(ns),'export_hashes':len(em),'preparation_hashes':len(pm),'gzip_integrity':True,'safe_exact_membership':True,'nonmanifested_export_records':sorted(extra)}}
    p=B/'inputs/I164-res-null-test-1-independent-review.zip'
    assert ident(p)=={'bytes':7465629,'sha256':'aec7858850cab8b679502de3eaf4a3c8fbd7d4a26648ee8bfb17e090a269563b'}
    out['parent_review']=zip_verify(p,B/'parent-review')
    inp=json.loads((B/'host/INPUTS.json').read_text())
    for role,dest in [('source','source'),('focused_results','author-results')]:
        pin=inp[role];hits=list((B/'host').rglob(pin['filename']));assert len(hits)==1,hits
        assert ident(hits[0])=={k:pin[k] for k in ('bytes','sha256')}
        out[role]=zip_verify(hits[0],B/dest)
    (B/'input-verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
