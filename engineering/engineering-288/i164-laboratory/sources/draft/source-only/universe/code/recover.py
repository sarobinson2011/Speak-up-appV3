"""Recover unchanged current candidate using two exact retained review archives."""
import argparse,hashlib,json,zipfile,stat,subprocess,sys
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parents[1]
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify_zip(path,expected,dest=None):
 b=path.read_bytes();assert identity(b)=={k:expected[k] for k in ('bytes','sha256')}
 with zipfile.ZipFile(path) as z:
  names=z.namelist();assert len(names)==len(set(names))==expected['entries'] and z.testzip() is None
  m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
  for i in z.infolist():
   n=PurePosixPath(i.filename);assert not i.is_dir() and not n.is_absolute() and '..' not in n.parts and not stat.S_ISLNK(i.external_attr>>16)
  for n,v in m.items():assert identity(z.read(n))==v,n
  if dest is not None:assert not dest.exists();z.extractall(dest)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--closure',required=True,type=Path);ap.add_argument('--unknown',required=True,type=Path);ap.add_argument('--destination',required=True,type=Path);ap.add_argument('--dependencies',required=True,type=Path);a=ap.parse_args()
 m=json.loads((P/'MANIFEST.json').read_bytes());actual={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file()};assert actual==set(m)|{'MANIFEST.json'}
 for n,v in m.items():assert identity((P/n).read_bytes())==v,n
 deps=a.dependencies.resolve();d=json.loads((P/'provenance/recovery-archives.json').read_bytes())
 verify_zip(a.closure,d['closure'],deps);verify_zip(a.unknown,d['unchanged_dependency'])
 submission=deps/'submission';verify_zip(deps/'inputs/Engineering-288C-I164-discriminator-type-correction.zip',{'bytes':9148223,'entries':86,'sha256':'910e80c30369ce8d63dca14f4f77f8193bdc646e9e58ad42a92bb34f397da358'},submission)
 subprocess.run([sys.executable,'-B',str(submission/'code/recover.py'),'--destination',str(a.destination.resolve()),'--dependencies',str(deps/'predecessors'),'--review',str(a.unknown.resolve())],check=True)
 sys.path.insert(0,str(P/'code'));import cardinality
 cardinality.verify_root(a.destination)
 print('PASS unchanged exact current 666-file candidate; companion construction is separate')
if __name__=='__main__':main()
