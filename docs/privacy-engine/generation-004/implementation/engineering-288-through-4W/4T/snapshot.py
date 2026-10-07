"""Explicit paused-job snapshots; two rotating slots. Never copies table output."""
import argparse,fcntl,hashlib,json,os,sys,zipfile
from pathlib import Path
sys.dont_write_bytecode=True
from run_task import ROOT,PLAN,verify_package,audit,budget_records,filehash,wire,sha,read,atomic,unseal,budget_limit

def save(task):
 verify_package();state=task/'supervisor'
 with (state/'LOCK').open('a+b') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  a=audit(ROOT,task/'textual',PLAN);budget_records(state);budget_limit(state,unseal(state/'IDENTITY.json'),PLAN)
  dest=task/'backups';dest.mkdir(exist_ok=True);head=dest/'HEAD.json';slot=(read(head)['slot']+1)%2 if head.exists() else 0
  output=dest/f'checkpoint-{slot}.zip';tmp=output.with_suffix('.part')
  files=sorted([p for folder in ('supervisor','textual') for p in (task/folder).rglob('*.json')]+[p for p in [task/'PROGRESS.json',task/'COMPLETION.json'] if p.exists()])
  entries=[]
  for p in files:
   if p.is_symlink():raise ValueError('snapshot symlink')
   entries.append({'path':str(p.relative_to(task)),'bytes':p.stat().st_size,'sha256':filehash(p)})
  info={'format':'CP4T-DURABLE-SNAPSHOT-1','package_manifest_sha256':filehash(ROOT/'PACKAGE-MANIFEST.json'),'files':entries,'progress':a}
  with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED) as z:
   for e in entries:z.write(task/e['path'],e['path'])
   z.writestr('SNAPSHOT-MANIFEST.json',wire(info))
  with zipfile.ZipFile(tmp) as z:
   if z.testzip() is not None:raise ValueError('snapshot CRC')
  with tmp.open('rb') as f:os.fsync(f.fileno())
  os.replace(tmp,output);atomic(head,{'slot':slot,'sha256':filehash(output),'bytes':output.stat().st_size})
  return {'snapshot':str(output),'sha256':filehash(output),'qualification_established':False}

def restore(snapshot,target,expected_sha256):
 verify_package()
 if filehash(snapshot)!=expected_sha256:raise ValueError('snapshot SHA mismatch')
 if target.exists():raise ValueError('restore requires a fresh destination; historical job never overwritten')
 with zipfile.ZipFile(snapshot) as z:
  m=json.loads(z.read('SNAPSHOT-MANIFEST.json'))
  if m['package_manifest_sha256']!=filehash(ROOT/'PACKAGE-MANIFEST.json'):raise ValueError('snapshot code binding')
  expected={e['path'] for e in m['files']}|{'SNAPSHOT-MANIFEST.json'}
  if len(z.namelist())!=len(expected) or set(z.namelist())!=expected:raise ValueError('snapshot membership')
  for e in m['files']:
   p=Path(e['path']);b=z.read(e['path'])
   if p.is_absolute() or '..' in p.parts or '.env' in p.parts or p.parts[0] not in ('supervisor','textual','PROGRESS.json','COMPLETION.json'):raise ValueError('snapshot path')
   if (len(b),sha(b))!=(e['bytes'],e['sha256']):raise ValueError('snapshot bytes')
  target.mkdir(parents=True)
  (target/'RESTORE-INCOMPLETE').write_text('Do not resume; incomplete restore\n')
  for e in m['files']:
   p=target/e['path'];p.parent.mkdir(parents=True,exist_ok=True);
   with p.open('wb') as out:out.write(z.read(e['path']));out.flush();os.fsync(out.fileno())
  # Restore paused; user explicitly resumes after exact code/runtime checks.
  (target/'textual/PAUSE').touch()
 audit(ROOT,target/'textual',PLAN);budget_records(target/'supervisor');budget_limit(target/'supervisor',unseal(target/'supervisor/IDENTITY.json'),PLAN)
 for directory in [p for p in target.rglob('*') if p.is_dir()]+[target]:
  fd=os.open(directory,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
 (target/'RESTORE-INCOMPLETE').unlink();fd=os.open(target,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
 return {'restored':str(target),'paused':True,'actual_admission':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('operation',choices=('save','restore'));p.add_argument('--task',type=Path,required=True);p.add_argument('--snapshot',type=Path);p.add_argument('--sha256');a=p.parse_args()
 try:
  if 'Speak-up-appV3' in a.task.resolve().parts:raise ValueError('isolated task path required')
  print(json.dumps(save(a.task) if a.operation=='save' else restore(a.snapshot,a.task,a.sha256),indent=2))
 except Exception as e:print('REJECTED:',e,file=sys.stderr);raise SystemExit(2)
