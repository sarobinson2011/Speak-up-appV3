"""Exact checkpoint extraction only; does not import or execute candidate code."""
import argparse,hashlib,json,os,stat,zipfile
from pathlib import Path,PurePosixPath
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    a=argparse.ArgumentParser();a.add_argument('archive',type=Path);a.add_argument('destination',type=Path);a.add_argument('--bytes',required=True,type=int);a.add_argument('--sha256',required=True);x=a.parse_args()
    assert str(x.destination.resolve())!='/tmp' and not str(x.destination.resolve()).startswith('/tmp/')
    assert not os.path.lexists(x.destination)
    raw=x.archive.read_bytes();assert identity(raw)=={'bytes':x.bytes,'sha256':x.sha256}
    with zipfile.ZipFile(x.archive) as z:
        names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
        for i in z.infolist():
            p=PurePosixPath(i.filename);assert not p.is_absolute() and '..' not in p.parts and not i.is_dir()
            assert stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
        m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
        for n,v in m.items():assert identity(z.read(n))==v,n
        x.destination.mkdir(parents=True);z.extractall(x.destination)
    assert {str(p.relative_to(x.destination)) for p in x.destination.rglob('*') if p.is_file()}==set(names)
    for n,v in m.items():assert identity((x.destination/n).read_bytes())==v,n
    print('PASS CRC, exact membership, manifests and fresh extraction',len(names))
if __name__=='__main__':main()
