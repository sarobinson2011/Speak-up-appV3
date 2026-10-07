#!/usr/bin/env python3
"""Deterministic member set; atomic checkpoint ZIP publication."""
import os,zipfile,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
from bind_text import ROOT,save,info
out=ROOT.parent/'Engineering-288-checkpoint-4U.zip'
files=[]
for p in sorted(ROOT.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p!=ROOT/'PACKAGE-MANIFEST.json':files.append({'path':str(p.relative_to(ROOT)),**info(p)})
save(ROOT/'PACKAGE-MANIFEST.json',{'format':'ENGINEERING-288-CHECKPOINT-4U-MANIFEST-1','files':files,'model_changed':False,'full_stream_processed':False,'actual_admission':False,'qualification_established':False})
tmp=out.with_suffix('.zip.part')
with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(ROOT.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:z.write(p,ROOT.name+'/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(tmp) as z:
 if z.testzip() is not None:raise ValueError('ZIP CRC')
with tmp.open('rb') as f:os.fsync(f.fileno())
os.replace(tmp,out);fd=os.open(out.parent,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
print(json.dumps({'filename':out.name,**info(out),'manifested_files':len(files)}))
