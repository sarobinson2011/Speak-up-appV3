#!/usr/bin/env python3
"""Restore only exact unchanged 4S model bytes. No model/stream construction."""
import argparse,hashlib,os,zipfile,tempfile,sys
from pathlib import Path
sys.dont_write_bytecode=True
from bind_text import ROOT,read,info,require
p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
r=read(ROOT/'inputs/EXTERNAL-REFERENCES.json');expected=next(x for x in r['archives'] if x['filename']=='Engineering-288-checkpoint-4S.zip');m=r['model']
require(info(a.archive)=={k:expected[k] for k in ('bytes','sha256')},'exact retained 4S archive required');require(not a.output.exists(),'preserve existing output; choose a new path')
a.output.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(prefix='model-4U-',dir=a.output.parent)
try:
 h=hashlib.sha256();n=0
 with os.fdopen(fd,'wb') as out,zipfile.ZipFile(a.archive) as z,z.open(m['member']) as src:
  for b in iter(lambda:src.read(1048576),b''):h.update(b);n+=len(b);out.write(b)
  out.flush();os.fsync(out.fileno())
 require(n==m['bytes'] and h.hexdigest()==m['sha256'],'exact model bytes');os.link(tmp,a.output);os.unlink(tmp);d=os.open(a.output.parent,os.O_DIRECTORY);os.fsync(d);os.close(d)
 print('PASS — exact unchanged 4S model restored: '+str(a.output))
finally:
 if os.path.exists(tmp):os.unlink(tmp)
