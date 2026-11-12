"""Export stable saved evidence only after this one service/child has stopped.
No validation, database connections, retry, deletion or success inference.
"""
from pathlib import Path
import sys,json,hashlib,tarfile,io,os,stat,importlib.util,datetime
WORK=Path('/srv/Engineering-288-execution/steve/I164-exit-decref-attempt-public-1-20261112')
DEST=Path('/home/steve/Downloads/I164-exit-decref-attempt-public-1-host-evidence.tar.gz')
def identity(p):
 h=hashlib.sha256();size=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);size+=len(b)
 return {'bytes':size,'sha256':h.hexdigest()}
def main():
 s=importlib.util.spec_from_file_location('_export_status',WORK/'code/status.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);state=m.inspect()
 if state['service'].get('ActiveState') not in ('inactive','failed') or state['original_child_alive'] is not False:raise SystemExit('STOP: stopped service and original child required for consistent export; no process altered')
 partial=DEST.with_name(DEST.name+'.partial')
 if DEST.exists() or DEST.is_symlink() or partial.exists() or partial.is_symlink():raise SystemExit('STOP: export already exists or partial; preserve it, no overwrite or retry')
 names=[]
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(WORK).as_posix()
   if n in ('candidate','recovered-helper','inputs/prerun.zip','inputs/progress.zip'):continue
   mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):walk(q)
   elif stat.S_ISREG(mode):names.append(n)
   else:raise RuntimeError('Unsupported evidence entry: '+n)
 walk(WORK);names.sort();before={n:identity(WORK/n) for n in names}
 if any(n in before for n in ('EXPORT-MANIFEST.json','EXPORT-STATUS.json')):raise RuntimeError('Export metadata name conflict')
 def add_bytes(t,name,data):
  i=tarfile.TarInfo(name);i.size=len(data);i.mode=0o600;t.addfile(i,io.BytesIO(data))
 with partial.open('xb') as f:
  with tarfile.open(fileobj=f,mode='w:gz') as t:
   for n in names:t.add(WORK/n,arcname=n,recursive=False)
   add_bytes(t,'EXPORT-MANIFEST.json',(json.dumps(before,sort_keys=True,indent=2)+'\n').encode())
   add_bytes(t,'EXPORT-STATUS.json',(json.dumps({'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':state,'meaning':'Export of stable saved records only; result/exit qualifications preserved','omitted_recoverable_roots':['candidate','recovered-helper','inputs/prerun.zip','inputs/progress.zip']},sort_keys=True,indent=2)+'\n').encode())
  f.flush();os.fsync(f.fileno())
 if before!={n:identity(WORK/n) for n in names}:raise RuntimeError('Evidence changed during export; partial preserved')
 with tarfile.open(partial,'r:gz') as t:
  if len(t.getmembers())!=len(names)+2:raise RuntimeError('Export membership mismatch')
  for n,pin in before.items():
   h=hashlib.sha256();size=0
   with t.extractfile(n) as src:
    for data in iter(lambda:src.read(1024*1024),b''):h.update(data);size+=len(data)
   if {'bytes':size,'sha256':h.hexdigest()}!=pin:raise RuntimeError('Export bytes mismatch: '+n)
 os.link(partial,DEST);partial.unlink()
 print(json.dumps({'file':str(DEST),**identity(DEST),'entries':len(names)+2,'public_status':state['status'],'meaning':'Saved evidence exported; no validation rerun'},indent=2))
if __name__=='__main__':main()
