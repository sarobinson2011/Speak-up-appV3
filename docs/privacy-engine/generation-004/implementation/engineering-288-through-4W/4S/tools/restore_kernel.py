#!/usr/bin/env python3
import argparse,zipfile,shutil,tempfile
from common import *
p=argparse.ArgumentParser();p.add_argument('--destination',type=Path,required=True);a=p.parse_args();dest=a.destination.resolve()
if dest.exists():raise ValueError('fresh destination required')
zpath=R/'retained/Engineering-288-checkpoint-4Q.zip';assert sha(zpath)=='353d158a0a7cbbd8f0a33619f4123eb7fc3e95921f3c92aed3b3312aebc7cd32'
with tempfile.TemporaryDirectory(prefix='4s-restore-') as td:
 archive=Path(td)/'4P.zip'
 with zipfile.ZipFile(zpath) as z,z.open('Engineering-288-checkpoint-4Q/retained/Engineering-288-checkpoint-4P.zip') as src,archive.open('wb') as out:shutil.copyfileobj(src,out,1048576)
 assert sha(archive)=='d3205e211382b30a52f6aced75a32187f02c5032833925fde97f118e33c7e7a9'
 with zipfile.ZipFile(archive) as z:
  names=set()
  for e in z.infolist():
   assert e.filename not in names and (dest/e.filename).resolve().is_relative_to(dest);names.add(e.filename)
  z.extractall(dest)
  for e in z.infolist():
   if not e.is_dir() and (e.external_attr >> 16) & 0o111:(dest/e.filename).chmod(0o755)
print(dest/'Engineering-288-checkpoint-4P')
