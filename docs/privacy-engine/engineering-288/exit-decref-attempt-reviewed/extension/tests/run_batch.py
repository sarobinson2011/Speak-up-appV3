"""One bounded offline batch; durable chunks and explicit exit. No retry."""
import hashlib,json,os,selectors,subprocess,sys,time,zipfile
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];bid=sys.argv[1];OUT=Path(sys.argv[2]);OUT.mkdir(parents=True,exist_ok=False)
plan=json.loads((ROOT/'tests/BATCH-PLAN.json').read_bytes());spec=next(x for x in plan['batches'] if x['id']==bid)
def utc():return datetime.now(timezone.utc).isoformat()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,v):
 with open(OUT/n,'x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
deadline=spec['deadline_seconds'];started=time.monotonic();cmd=[sys.executable,'-I','-B','-u',str(ROOT/'tests/focused_batch.py'),bid,str(OUT/'raw')]
save('launch.json',{'utc':utc(),'batch':bid,'command':cmd,'deadline_seconds':deadline,'deadline_basis':spec['basis'],'python':sys.version,'source_manifest':identity((ROOT/'MANIFEST.json').read_bytes()),'automatic_retries':0})
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);save('child.json',{'pid':p.pid,'utc':utc()});sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,'stdout');sel.register(p.stderr,selectors.EVENT_READ,'stderr');(OUT/'chunks').mkdir();seq=0;timedout=False
streams={k:open(OUT/(k+'.log'),'xb') for k in ('stdout','stderr')}
try:
 while sel.get_map():
  if time.monotonic()-started>deadline and p.poll() is None:timedout=True;p.kill()
  for key,_ in sel.select(0.25):
   chunk=os.read(key.fileobj.fileno(),65536)
   if not chunk:sel.unregister(key.fileobj);continue
   seq+=1;name='chunks/%05d-%s.bin'%(seq,key.data)
   with open(OUT/name,'xb') as f:f.write(chunk);f.flush();os.fsync(f.fileno())
   streams[key.data].write(chunk);streams[key.data].flush();os.fsync(streams[key.data].fileno())
   save('chunks/%05d.json'%seq,{'utc':utc(),'stream':key.data,'path':name,**identity(chunk)})
 rc=p.wait()
finally:
 for f in streams.values():f.close()
save('exit.json',{'utc':utc(),'returncode':rc,'timed_out':timedout,'seconds':time.monotonic()-started,'captured_chunks':seq,'automatic_retry':False})
rows=[json.loads(x.read_bytes()) for x in sorted((OUT/'raw').glob('[0-9][0-9][0-9][0-9].json'))]
progress=[json.loads(x) for x in (OUT/'raw/progress.jsonl').read_text().splitlines()] if (OUT/'raw/progress.jsonl').exists() else []
stdout=[json.loads(x)['row'] for x in (OUT/'stdout.log').read_text().splitlines() if json.loads(x).get('event')=='CONTROL']
result=json.loads((OUT/'raw/RESULT.json').read_bytes()) if (OUT/'raw/RESULT.json').exists() else None
agree=rows==progress==stdout and [r['sequence'] for r in rows]==list(range(1,len(rows)+1))
counts={s:sum(r['status']==s for r in rows) for s in ('PASS','REJECTED','FAIL')}
chunks_ok=all(b''.join((OUT/json.loads(x.read_bytes())['path']).read_bytes() for x in sorted((OUT/'chunks').glob('*.json')) if json.loads(x.read_bytes())['stream']==s)==(OUT/(s+'.log')).read_bytes() for s in ('stdout','stderr'))
complete=rc==0 and not timedout and agree and chunks_ok and result is not None and result['rows']==len(rows) and result['counts']==counts and result['result']=='PASS'
save('RECONCILIATION.json',{'status':'COMPLETED' if complete else 'INCOMPLETE_OR_FAILED','rows':len(rows),'counts':counts,'raw_progress_stdout_exact_agreement':agree,'stream_chunks_match':chunks_ok,'explicit_child_exit':rc,'result_present':result is not None,'source_manifest':identity((ROOT/'MANIFEST.json').read_bytes()),'public_authentication':'UNEXECUTED','authenticated_constructed_path':'UNEXECUTED'})
m={p.relative_to(OUT).as_posix():identity(p.read_bytes()) for p in sorted(OUT.rglob('*')) if p.is_file()};save('MANIFEST.json',m)
archive=OUT.parent/('I164-exit-decref-attempt-1-'+bid+'-records.zip')
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(OUT.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(OUT).as_posix())
print(json.dumps({'batch':bid,'status':'COMPLETED' if complete else 'INCOMPLETE_OR_FAILED','rows':len(rows),'counts':counts,'exit':rc,'timed_out':timedout,'records':str(OUT),'archive':str(archive),'identity':identity(archive.read_bytes())}),flush=True)
sys.exit(0 if complete else 1)
