#!/usr/bin/env python3
import hashlib,json,math,sys,zipfile,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));import run_task as rt
files=[]
for f in sorted(ROOT.rglob('*')):
 if f.is_file() and '__pycache__' not in f.parts and f!=ROOT/'PACKAGE-MANIFEST.json':files.append({'path':f.relative_to(ROOT).as_posix(),'bytes':f.stat().st_size,'sha256':rt.filehash(f)})
allocated=sum(math.ceil(e['bytes']/4096)*4096 for e in files)+65536
segments=rt.PLAN['segments_max'];attempts=rt.PLAN['max_attempts'];grants=256
live=(2*segments+grants)*4096+attempts*(4096+8192)+16*1024**2
archive_upper=sum(e['bytes'] for e in files)+len(files)*1024+65536
storage={'exact_member_bytes_excluding_manifest':sum(e['bytes'] for e in files),'extracted_allocated_bound_4KiB_blocks':allocated,'archive_size_upper_bound':archive_upper,'max_generation_segments':segments,'max_replay_receipts':segments,'max_attempts':attempts,'max_grants':grants,'log_bytes_cap':8192,'attempt_bytes_cap':4096,'live_checkpoint_bound_bytes':live,'checkpoint_copies_at_peak':5,'copy_policy':'live plus two rotating ZIP backups plus temporary backup plus fresh restored copy; conservative uncompressed bounds','console_logs_allowance_bytes':512*1024**2,'snapshot_container_overhead_allowance_bytes':256*1024**2,'safety_headroom_bytes':256*1024**2,'task_peak_bound_bytes_4KiB_blocks':allocated+2*archive_upper+5*live+1024**3,'required_free_bytes':8*1024**3,'required_free_inodes':2*(2*segments+2*attempts+grants+len(files))+1024,'filesystem_allocation_unit_max_bytes':4096,'note':'Exact TSV is never materialized. Model/archive chain and system shared libraries are not extracted. Runtime library files are hash-bound per host.'}
assert storage['task_peak_bound_bytes_4KiB_blocks']<storage['required_free_bytes']
rt.atomic(ROOT/'PACKAGE-MANIFEST.json',{'format':'CP4T-PORTABLE-STATIC-TEXT-KIT-1','files':files,'storage':storage,'full_stream_sha256':None,'actual_admission':False})
zpath=ROOT.parent/'Engineering-288-checkpoint-4T.zip'
temporary=zpath.with_suffix('.zip.part')
with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for e in files+[{'path':'PACKAGE-MANIFEST.json'}]:z.write(ROOT/e['path'],ROOT.name+'/'+e['path'])
with zipfile.ZipFile(temporary) as z:
 assert z.testzip() is None
with temporary.open('rb') as f:os.fsync(f.fileno())
os.replace(temporary,zpath)
fd=os.open(zpath.parent,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
print(json.dumps({'zip':str(zpath),'bytes':zpath.stat().st_size,'sha256':rt.filehash(zpath),'files':len(files),'storage':storage}))
