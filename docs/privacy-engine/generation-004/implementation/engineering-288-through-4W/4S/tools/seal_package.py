#!/usr/bin/env python3
"""Seal an already constructed checkpoint; omit caches and preserve all history."""
import argparse,zipfile
from common import *
p=argparse.ArgumentParser();p.add_argument('--zip',type=Path,required=True);a=p.parse_args()
files=[]
for f in sorted(R.rglob('*')):
 if f.is_file() and '__pycache__' not in f.parts and f!=R/'PACKAGE-MANIFEST.json':files.append({'path':str(f.relative_to(R)),**info(f)})
save(R/'PACKAGE-MANIFEST.json',{'format':'ENGINEERING-288-CHECKPOINT-4S-MANIFEST-1','files':files,'kernel_changed':False,'actual_admission':False,'qualification_established':False,'full_pair_or_link_stream_processed':False})
with zipfile.ZipFile(a.zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for e in files+[{'path':'PACKAGE-MANIFEST.json'}]:
  f=R/e['path'];z.write(f,R.name+'/'+e['path'],compress_type=zipfile.ZIP_STORED if f.suffix=='.zip' else zipfile.ZIP_DEFLATED)
print(json.dumps({'zip':str(a.zip),**info(a.zip),'manifested_files':len(files),'extracted_bytes':sum(e['bytes'] for e in files)+(R/'PACKAGE-MANIFEST.json').stat().st_size}))
