"""Check this review archive without extracting or executing application code."""
import argparse, hashlib, json, stat, zipfile
from pathlib import Path, PurePosixPath

def main():
    p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('--sha256');p.add_argument('--bytes',type=int);p.add_argument('--entries',type=int);a=p.parse_args()
    raw=Path(a.archive).read_bytes();digest=hashlib.sha256(raw).hexdigest()
    if a.sha256 is not None:assert digest==a.sha256
    if a.bytes is not None:assert len(raw)==a.bytes
    with zipfile.ZipFile(a.archive) as z:
        names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
        if a.entries is not None:assert len(names)==a.entries
        manifest=json.loads(z.read('MANIFEST.json'))['members']
        assert set(names)==set(manifest)|{'MANIFEST.json'}
        for i in z.infolist():
            n=i.filename;q=PurePosixPath(n)
            assert not q.is_absolute() and '..' not in q.parts and str(q)==n and '\\' not in n
            assert not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
            if n!='MANIFEST.json':
                b=z.read(n);assert {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}==manifest[n],n
        cp=json.loads(z.read('CHECKPOINT.json'));b=z.read('input/I164-status-boundary-correction-1.zip')
        assert {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}==cp['input']
    print(json.dumps({'result':'PASS','bytes':len(raw),'entries':len(names),'sha256':digest,'crc':'PASS','safe_exact_membership':'PASS','manifest_hashes':'PASS','unchanged_input':'PASS'}))

if __name__=='__main__':main()
