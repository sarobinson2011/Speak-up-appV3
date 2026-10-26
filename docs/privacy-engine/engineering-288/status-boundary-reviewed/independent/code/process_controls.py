"""Independent fresh-process dependency rejection and read-only CLI gate checks."""
import argparse, hashlib, json, os, shutil, subprocess, sys, traceback
from pathlib import Path

CHILD = r'''
import json,os,sys,types
from pathlib import Path
root=Path(sys.argv[1]); mode=sys.argv[2]
def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind'):raise AssertionError('DATABASE/NETWORK FORBIDDEN')
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith('/home/steve/'):raise AssertionError('HOST ACCESS FORBIDDEN')
sys.addaudithook(audit)
def load(path):
 m=types.ModuleType('fresh_target');m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
m=load(root/'code/prospective_entry.py')
reads=[];original=m._regular
def read(p):
 if 'retained' in p.relative_to(root).parts:reads.append(str(p.relative_to(root)))
 return original(p)
m._regular=read
if mode=='cli':
 unused=Path(sys.argv[3]);rc=m.main(['initialize','--candidate',str(unused/'candidate'),'--draft',str(unused/'draft'),'--runtime',str(unused/'runtime'),'--destination',str(unused/'never-created')]);raise SystemExit(rc)
if mode=='binding':
 c=load(root/'code/correspondence.py')
 try:c.validate(root,(root/'provenance/status-correspondence.json').read_bytes())
 except (ValueError,RuntimeError,FileNotFoundError) as e:print(json.dumps({'rejected':True,'error':str(e)}))
 else:print(json.dumps({'rejected':False}))
else:
 try:m.verify_inputs(root)
 except (ValueError,RuntimeError,FileNotFoundError) as e:
  verification={'rejected':True,'error':str(e),'retained_payload_reads':reads[:]}
 else:verification={'rejected':False,'retained_payload_reads':reads[:]}
 class Unexpected(Exception):pass
 # Public run should refuse at the same source gate, before any session.
 try:m.run('not-candidate','not-draft','not-runtime','not-destination',lambda c:(_ for _ in ()).throw(Unexpected()))
 except m.ClientFailure as e:verification['public_failure']={'args':e.args,'cause':e.__cause__ is not None,'context':e.__context__ is not None}
 except BaseException as e:verification['wrong_public_failure']=type(e).__name__
 else:verification['public_success']=True
 print(json.dumps(verification))
'''

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 source=Path(a.root).resolve();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
 root=out/'mutated-source-copy'
 for part in ('code','contract','retained','provenance','basis'):shutil.copytree(source/part,root/part)
 results=[]
 def run(label,mode='dependency',r=root,extra=None):
  cmd=[sys.executable,'-I','-B','-c',CHILD,str(r),mode]+([] if extra is None else [str(extra)])
  proc=subprocess.run(cmd,capture_output=True,text=True,timeout=25)
  (out/(label+'.stdout')).write_text(proc.stdout);(out/(label+'.stderr')).write_text(proc.stderr)
  record={'label':label,'mode':mode,'returncode':proc.returncode,'stdout_sha256':hashlib.sha256(proc.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(proc.stderr.encode()).hexdigest()}
  if mode!='cli':
   assert proc.returncode==0 and not proc.stderr,(label,proc.stderr)
   value=json.loads(proc.stdout);record['observation']=value;assert value['rejected'],label
   if mode=='dependency':assert value.get('public_failure')=={'args':['MANAGED-OPERATION-UNAVAILABLE; outcome uncertain; no renewed authorization'],'cause':False,'context':False},value
  else:
   assert proc.returncode==1 and proc.stdout=='' and proc.stderr=='FAILED; outcome uncertain; admission disabled\n'
   assert not (extra/'never-created').exists()
  results.append(record);return record
 try:
  for label,relative in [('unexpected-file','retained/unlisted'),('unexpected-empty-directory','retained/empty'),('unexpected-symlink','retained/link'),('unexpected-FIFO','retained/fifo')]:
   q=root/relative
   if label=='unexpected-file':q.write_bytes(b'undeclared')
   elif label=='unexpected-empty-directory':q.mkdir()
   elif label=='unexpected-symlink':q.symlink_to('launcher')
   else:os.mkfifo(q)
   record=run(label);assert record['observation']['retained_payload_reads']==[],label
   if q.is_dir() and not q.is_symlink():q.rmdir()
   else:q.unlink()
  for label,relative in [('missing-contract','contract/CONTRACT-draft-1.txt'),('missing-decision','contract/DECISION.json'),('missing-launcher','retained/launcher/code/lab_bootstrap.py')]:
   q=root/relative;raw=q.read_bytes();q.unlink();record=run(label);assert record['observation']['retained_payload_reads']==[];q.write_bytes(raw)
  q=root/'retained/candidate/compiler/live_connection.py';raw=q.read_bytes();q.unlink();os.mkfifo(q)
  record=run('declared-member-FIFO');assert record['observation']['retained_payload_reads']==[];q.unlink();q.write_bytes(raw)
  for label,relative in [('changed-contract','contract/CONTRACT-draft-1.txt'),('changed-decision','contract/DECISION.json'),('mixed-contexts','retained/candidate/candidate/contexts.json'),('changed-pins','provenance/dependency-pins.json')]:
   q=root/relative;raw=q.read_bytes();q.write_bytes(raw+b'\n');run(label);q.write_bytes(raw)
  # Substitute retained old launcher bytes only in this disposable negative tree.
  q=root/'retained/launcher/code/lab_bootstrap.py';raw=q.read_bytes();q.write_bytes((root/'retained/launcher/provenance/launcher-41.0.7.py').read_bytes());run('mixed-old-launcher');q.write_bytes(raw)
  for label,relative in [('changed-model','basis/candidate/managed-route/model.json'),('changed-procedure','basis/prospective_outputs/managed-route/procedure-duty.json'),('changed-basis-pins','provenance/basis-pins.json')]:
   q=root/relative;raw=q.read_bytes();q.write_bytes(raw+b'\n');run(label,'binding');q.write_bytes(raw)
  q=root/'basis/candidate/managed-route/producers.json';raw=q.read_bytes();q.unlink();run('missing-producers','binding');q.write_bytes(raw)
  run('unmocked-public-gate','cli',source,out/'unused')
  (out/'RESULT.json').write_text(json.dumps({'result':'PASS','process_checks':results,'count':len(results),'actual_special_files':['FIFO','symlink'],'socket_device_execution':'NOT TESTED','real_backend_positive':False,'all_mutated_files_are_disposable_inputs':True},indent=2)+'\n')
  print(json.dumps({'result':'PASS','process_checks':len(results)}))
 except BaseException:
  (out/'PARTIAL.json').write_text(json.dumps({'completed':results,'failure':traceback.format_exc()},indent=2)+'\n');raise

if __name__=='__main__':main()
