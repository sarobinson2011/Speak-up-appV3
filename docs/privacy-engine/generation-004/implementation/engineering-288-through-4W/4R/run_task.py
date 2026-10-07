#!/usr/bin/env python3
"""Binary-only supervisor around exact retained 4A machinery. No table output."""
import argparse,contextlib,fcntl,hashlib,importlib.util,json,math,os,resource,signal,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
HEADER=b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n'
PLAN={'descriptor':'inputs/pairs.txt','candidate_total':91157454636,'rows':91157453467,'serialized_bytes':729259627770,'segment_candidates':67108864,'segments':1359,'aggregate_seconds':7200,'reservation_seconds':60,'child_seconds':45,'max_attempts':4096,'scope':'CONDITIONAL-MECHANICAL-BINARY-IDENTITY-ONLY'}
PAUSED=False

def wire(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def filehash(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def read(p):
 def unique(pairs):
  d={}
  for k,v in pairs:
   if k in d:raise ValueError('duplicate JSON key')
   d[k]=v
  return d
 return json.loads(Path(p).read_bytes(),object_pairs_hook=unique)
def atomic(p,obj):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix('.part');b=wire(obj)
 with tmp.open('wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 os.replace(tmp,p);fd=os.open(p.parent,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
def sealed(p,payload):atomic(p,{'payload':payload,'sha256':sha(wire(payload))})
def unseal(p):
 x=read(p)
 if set(x)!= {'payload','sha256'} or x['sha256']!=sha(wire(x['payload'])):raise ValueError('corrupted supervisor receipt: '+str(p))
 return x['payload']
def retained(root=ROOT):
 s=importlib.util.spec_from_file_location('retained_4a',root/'runner/run.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def verify_package(root=ROOT):
 m=read(root/'PACKAGE-MANIFEST.json')
 for e in m['files']:
  p=root/e['path']
  if p.is_symlink() or p.stat().st_size!=e['bytes'] or filehash(p)!=e['sha256']:raise ValueError('package identity: '+e['path'])
 return m

def audit(root,job,plan):
 """Read-only chain/terminal check. Does not reconstruct full pair bytes."""
 r=retained(root);desc=root/plan['descriptor'];ident=r.identity(desc);gens=[];prev=sha(wire(ident));end=0;state='6a09e667bb67ae853c6ef372a54ff53a510e527f9b05688c1f83d9ab5be0cd19:34:'+HEADER.hex();count=0
 paths=sorted(job.glob('segment-*.json'))
 if not (job/'IDENTITY.json').exists():
  if paths:raise ValueError('missing generator identity')
 else:
  if read(job/'IDENTITY.json')!=ident:raise ValueError('substituted generator inputs/code')
 for k,p in enumerate(paths):
  x=read(p)
  if p.name!=f'segment-{k:08d}.json' or x['index']!=k or x['previous']!=prev or x['start']!=end or x['end']!=min(end+plan['segment_candidates'],plan['candidate_total']):raise ValueError('segment chain/interval')
  if x['engine']!='complement' or x['state_in']!=state or type(x['rows']) is not int or not 0<=x['rows']<=x['end']-x['start'] or x['bytes']!=8*x['rows']:raise ValueError('segment laws')
  count+=x['rows'];parts=x['state_out'].split(':');n=34+count*8
  if len(parts)!=3 or len(parts[0])!=64 or int(parts[1])!=n or len(bytes.fromhex(parts[2]))!=n%64:raise ValueError('SHA state size')
  for key in ('segment_sha256','prefix_sha256'):
   if len(x[key])!=64 or any(c not in '0123456789abcdef' for c in x[key]):raise ValueError('digest encoding')
  prev=sha(wire(x));end=x['end'];state=x['state_out'];gens.append(x)
 if (job/'HEAD.json').exists():
  h=read(job/'HEAD.json');k=h['segments']
  if not 0<=k<=len(gens) or h['record_sha256']!=(sha(wire(gens[k-1])) if k else sha(wire(ident))):raise ValueError('generation HEAD corruption/truncation')
 ver=[];vp=sha(wire(ident))
 for k,p in enumerate(sorted((job/'verification').glob('verified-*.json'))):
  x=read(p)
  if k>=len(gens) or p.name!=f'verified-{k:08d}.json' or x!={'index':k,'record_sha256':sha(wire(gens[k])),'previous':vp,'engine':'independent-predicate','result':'PASS'}:raise ValueError('predicate replay receipt mismatch')
  vp=sha(wire(x));ver.append(x)
 complete=end==plan['candidate_total'] and len(gens)==plan['segments'] and len(ver)==len(gens)
 if end==plan['candidate_total'] and (count!=plan['rows'] or 34+8*count!=plan['serialized_bytes']):raise ValueError('final exact cardinality/bytes')
 return {'generation_segments':len(gens),'verified_segments':len(ver),'candidate_frontier':end,'candidate_total':plan['candidate_total'],'rows':count,'serialized_bytes':34+count*8,'generation_chain_sha256':prev,'verification_chain_sha256':vp,'generated_whole_stream_sha256':gens[-1]['prefix_sha256'] if end==plan['candidate_total'] else None,'verified_whole_stream_sha256':gens[-1]['prefix_sha256'] if complete else None,'complete':complete,'actual_admission':False,'qualification_established':False,'scope':plan['scope']}

def budget_records(state):
 records=[];prev=sha(wire(unseal(state/'IDENTITY.json')))
 for k,p in enumerate(sorted(state.glob('attempt-*.json'))):
  x=unseal(p)
  if p.name!=f'attempt-{k:05d}.json' or x['index']!=k or x['previous']!=prev or x['status'] not in ('RESERVED','FINISHED','INTERRUPTED','FAILED'):raise ValueError('budget chain')
  if not 0<=x['charged_seconds']<=x['reserved_seconds'] or (x['status']=='RESERVED' and x['charged_seconds']!=x['reserved_seconds']):raise ValueError('budget accounting')
  if records and records[-1]['status']=='RESERVED':raise ValueError('unresolved prior reservation')
  records.append(x);prev=sha(wire(x))
 if (state/'HEAD.json').exists():
  h=unseal(state/'HEAD.json');k=h['attempts']
  # HEAD may lag one atomic reservation/finish write. Same-index updated receipt
  # is recognized via the stored previous reservation hash only.
  if k>len(records) or k<max(0,len(records)-1):raise ValueError('budget HEAD loss')
  expected=sha(wire(records[k-1])) if k else sha(wire(unseal(state/'IDENTITY.json')))
  if h['record_sha256']!=expected:
   if not (k==len(records) and k and records[-1].get('reservation_sha256')==h['record_sha256']):raise ValueError('budget HEAD corruption')
 elif records and not (len(records)==1 and records[0]['status']=='RESERVED'):
  raise ValueError('missing durable budget HEAD')
 return records,prev

def budget_head(state,records):
 sealed(state/'HEAD.json',{'attempts':len(records),'record_sha256':sha(wire(records[-1])) if records else sha(wire(unseal(state/'IDENTITY.json')))})

def execute_step(root,job,plan,operation,seconds):
 cmd=[sys.executable,'-B',str(root/'step.py'),operation,'--descriptor',str(root/plan['descriptor']),'--job',str(job),'--candidates',str(plan['segment_candidates']),'--seconds',str(min(seconds,plan['child_seconds']))]
 proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 try:
  out,err=proc.communicate(timeout=min(50,seconds+5))
 except BaseException:
  try:os.killpg(proc.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  try:out,err=proc.communicate(timeout=2)
  except subprocess.TimeoutExpired:
   os.killpg(proc.pid,signal.SIGKILL);out,err=proc.communicate()
  raise
 if len(out.encode())+len(err.encode())>8192:raise ValueError('step log bound exceeded')
 return proc.returncode,out,err

def drive(task,root,plan,runtime,max_actions=None):
 global PAUSED
 task=Path(task);state=task/'supervisor';job=task/'binary';state.mkdir(parents=True,exist_ok=True);job.mkdir(exist_ok=True)
 identity={'format':'CP4R-BINARY-JOB-1','package_manifest_sha256':filehash(root/'PACKAGE-MANIFEST.json'),'active':read(root/'bindings/ACTIVE-IDENTITIES.json'),'plan':plan,'native_runtime':runtime,'retained_code':retained(root).identity(root/plan['descriptor'])}
 with (state/'LOCK').open('a+b') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  if (state/'IDENTITY.json').exists():
   if unseal(state/'IDENTITY.json')!=identity:raise ValueError('incompatible package/active contract/native runtime/plan')
  else:
   if list(state.glob('attempt-*')) or list(job.glob('segment-*')):raise ValueError('unbound existing job')
   sealed(state/'IDENTITY.json',identity)
  records,_=budget_records(state)
  if records and records[-1]['status']=='RESERVED':
   x=records[-1];old=sha(wire(x));x.update(status='INTERRUPTED',reservation_sha256=old,reason='previous invocation interrupted; full reserved time charged');sealed(state/f"attempt-{x['index']:05d}.json",x);budget_head(state,records)
  actions=0;last_charged_boundary=time.monotonic()
  while True:
   began=last_charged_boundary;a=audit(root,job,plan)
   if len(records)<a['generation_segments']+a['verified_segments']:raise ValueError('missing computation budget records for completed work')
   if a['complete']:
    completion={**a,'result':'VERIFIED-CONDITIONAL-BINARY-STREAM-IDENTITY','package_manifest_sha256':identity['package_manifest_sha256'],'job_identity_sha256':sha(wire(identity)),'budget_charged_seconds':sum(x['charged_seconds'] for x in records),'receipt_trust':'Local trusted execution/checksum integrity only; not source authentication or qualification.'}
    sealed(task/'COMPLETION.json',completion);print(json.dumps(completion),flush=True);return 0
   if PAUSED or (job/'PAUSE').exists() or (max_actions is not None and actions>=max_actions):print(json.dumps({**a,'result':'PAUSED'}),flush=True);return 3
   used=sum(x['charged_seconds'] for x in records)
   if len(records)>=plan['max_attempts']:
    print(json.dumps({**a,'result':'REVIEW-STOP','reason':'4096-attempt storage/retry ceiling reached'}),flush=True);return 4
   if used+plan['reservation_seconds']>plan['aggregate_seconds']:
    print(json.dumps({**a,'result':'REVIEW-STOP','charged_seconds':used,'remaining_seconds':plan['aggregate_seconds']-used,'reason':'two-hour aggregate review stop; no automatic reset/extension'}),flush=True);return 4
   op='generate' if a['candidate_frontier']<plan['candidate_total'] else 'replay'
   i=len(records);previous=sha(wire(records[-1])) if records else sha(wire(identity))
   x={'index':i,'previous':previous,'operation':op,'status':'RESERVED','reserved_seconds':plan['reservation_seconds'],'charged_seconds':plan['reservation_seconds'],'frontier_before':a['candidate_frontier'],'verified_before':a['verified_segments']}
   sealed(state/f'attempt-{i:05d}.json',x);records.append(x);budget_head(state,records);reservation_sha=sha(wire(x))
   try:
    rc,out,err=execute_step(root,job,plan,op,plan['child_seconds'])
    atomic(state/f'log-{i:05d}.json',{'operation':op,'returncode':rc,'stdout':out,'stderr':err})
    after=audit(root,job,plan)
    elapsed=time.monotonic()-began
    if elapsed>plan['reservation_seconds']:raise RuntimeError('reserved review-budget interval exceeded; stop for review')
    x.update(status='FINISHED' if rc==0 else 'FAILED',charged_seconds=elapsed,reservation_sha256=reservation_sha)
    last_charged_boundary=began+elapsed
    sealed(state/f'attempt-{i:05d}.json',x);budget_head(state,records)
    progress={**after,'operation':op,'charged_seconds':sum(x['charged_seconds'] for x in records),'remaining_budget_seconds':plan['aggregate_seconds']-sum(x['charged_seconds'] for x in records)}
    sealed(task/'PROGRESS.json',progress);print(json.dumps(progress),flush=True);actions+=1
    if rc:print('STOP: child rejected/timeout; preserve log and checkpoint',file=sys.stderr);return 2
   except BaseException:
    # Reservation remains durable and is fully charged on resume.
    raise

def current_runtime(root):
 spec=importlib.util.spec_from_file_location('cp4r_bootstrap',root/'bootstrap.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 return m.native_probe((root/'runner/pairs').read_bytes(),(root/'inputs/probe.txt').read_bytes())['library_sha256']
def main():
 p=argparse.ArgumentParser();p.add_argument('operation',choices=['run','status','verify-completion','pause','resume']);p.add_argument('--task',type=Path,default=Path('/home/steve/dev/Engineering-288-execution'));args=p.parse_args();task=args.task.resolve()
 if 'Speak-up-appV3' in task.parts:raise ValueError('isolated task storage only')
 verify_package();plan=PLAN
 if args.operation in ('status','verify-completion'):
  a=audit(ROOT,task/'binary',plan)
  if (task/'supervisor/IDENTITY.json').exists():
   identity=unseal(task/'supervisor/IDENTITY.json')
   if identity['package_manifest_sha256']!=filehash(ROOT/'PACKAGE-MANIFEST.json') or identity['plan']!=plan or identity['active']!=read(ROOT/'bindings/ACTIVE-IDENTITIES.json'):raise ValueError('job binding mismatch')
   records,_=budget_records(task/'supervisor');a['charged_seconds']=sum(x['charged_seconds'] for x in records)
  if args.operation=='verify-completion':
   if not a['complete']:raise ValueError('generation and full predicate replay not both complete')
   c=unseal(task/'COMPLETION.json')
   for k,v in a.items():
    if k!='charged_seconds' and c[k]!=v:raise ValueError('completion substitution: '+k)
   if c['job_identity_sha256']!=sha(wire(identity)):raise ValueError('completion job substitution')
  print(json.dumps(a,indent=2));return 0
 if args.operation=='pause':
  (task/'binary').mkdir(parents=True,exist_ok=True);(task/'binary/PAUSE').touch();print('Pause requested; current segment may finish.');return 0
 if args.operation=='resume':
  try:(task/'binary/PAUSE').unlink()
  except FileNotFoundError:pass
 # Fail before starting if host capacity or exact library identity no longer fits.
 import importlib.util as util
 s=util.spec_from_file_location('bp',ROOT/'bootstrap.py');b=util.module_from_spec(s);s.loader.exec_module(b)
 mem=b.memory_available()
 if mem['effective_available_bytes']<8*1024**3:raise ValueError('less than initial 8 GiB available RAM')
 st=os.statvfs(task if task.exists() else task.parent)
 if st.f_bavail*st.f_frsize<read(ROOT/'PACKAGE-MANIFEST.json')['storage']['required_free_bytes']:raise ValueError('insufficient free disk for conservative complete task reserve')
 # At most supervisor + one Python step + one native child: <=6 GiB aggregate
 # process address-space ceilings, within the initial 8 GiB planning ceiling.
 resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
 def stop(*unused):
  global PAUSED;PAUSED=True
 signal.signal(signal.SIGINT,stop);signal.signal(signal.SIGTERM,stop)
 return drive(task,ROOT,plan,current_runtime(ROOT))
if __name__=='__main__':
 try:raise SystemExit(main())
 except Exception as e:print('REJECTED:',str(e),file=sys.stderr);raise SystemExit(2)
