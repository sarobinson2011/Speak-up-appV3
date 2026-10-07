"""Bounded exact-byte enumeration, durable segment journal, independent replay.
No argument triggers full work implicitly. Every child has a 60-second ceiling.
"""
import argparse,hashlib,json,os,pathlib,subprocess,time,fcntl,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
HEADER=b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n'
LINK_HEADER=b'link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n'
def is_links(desc):
 with pathlib.Path(desc).open('rb') as f:return f.read(5)==b'LINKS'
def wire(v):return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(pathlib.Path(p).read_bytes())
def atomic(p,obj):
 p=pathlib.Path(p);tmp=p.with_suffix('.part')
 with tmp.open('wb') as f:f.write(wire(obj));f.flush();os.fsync(f.fileno())
 os.replace(tmp,p);fd=os.open(p.parent,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
def build():
 for name in ('pairs','links'):
  out=ROOT/'runner'/name;subprocess.run(['g++','-O3','-std=c++17','-Wno-deprecated-declarations',str(ROOT/'runner'/(name+'.cpp')),'-lcrypto','-o',str(out)],check=True,timeout=60)
 return out

def invoke(desc,start,end,state='INIT',engine='complement',seconds=50):
 if not 0<seconds<=60:raise ValueError('per-segment ceiling 60 seconds')
 cp=subprocess.run([str(ROOT/'runner'/('links' if is_links(desc) else 'pairs')),str(desc),str(start),str(end),state,engine,str(max(.001,seconds-.2))],capture_output=True,text=True,timeout=seconds)
 if cp.stderr:print(cp.stderr,file=sys.stderr,end='')
 if cp.returncode:raise RuntimeError('No commit: '+cp.stderr)
 return json.loads(cp.stdout)

def identity(desc):return {'descriptor_sha256':sha(pathlib.Path(desc).read_bytes()),'engine_source_sha256':sha((ROOT/'runner/pairs.cpp').read_bytes()),'runner_sha256':sha(pathlib.Path(__file__).read_bytes()),'links_source_sha256':sha((ROOT/'runner/links.cpp').read_bytes()),'binary_sha256':sha((ROOT/'runner'/('links' if is_links(desc) else 'pairs')).read_bytes()),'format':'CP4A-EXACT-PAIR-JOURNAL-V1'}
def total(desc):
 with pathlib.Path(desc).open() as f:line=f.readline().split()
 if line[0]=='LINKS':return int(line[1])
 n=int(line[0]);return n*(n-1)//2

def journal(desc,directory):
 directory=pathlib.Path(directory);directory.mkdir(parents=True,exist_ok=True)
 ip=directory/'IDENTITY.json';ident=identity(desc)
 if ip.exists():
  if read(ip)!=ident:raise ValueError('input/code/binary identity changed; use a new journal')
 else:
  if list(directory.glob('segment-*.json')):raise ValueError('missing identity')
  atomic(ip,ident)
 previous=sha(wire(ident));end=0;state='INIT';records=[]
 for k,p in enumerate(sorted(directory.glob('segment-*.json'))):
  r=read(p)
  if p.name!=f'segment-{k:08d}.json' or r['index']!=k or r['previous']!=previous or r['start']!=end or not end<r['end']<=total(desc):raise ValueError('journal gap/reorder/identity chain')
  if k and r['state_in']!=state:raise ValueError('hash state discontinuity')
  if not is_links(desc) and r['bytes']!=r['rows']*8:raise ValueError('row/byte mismatch')
  previous=sha(wire(r));end=r['end'];state=r['state_out'];records.append(r)
 if (directory/'HEAD.json').exists():
  h=read(directory/'HEAD.json'); idx=h['segments']
  if not 0<=idx<=len(records) or h['record_sha256']!=(sha(wire(records[idx-1])) if idx else sha(wire(ident))):raise ValueError('damaged/truncated committed journal')
 return records,previous,end,state

def run(desc,directory,max_segments=1,segment_candidates=67108864,budget=50,execute_full=False):
 if max_segments<1 or segment_candidates<1 or not 0<budget<=60:raise ValueError('positive bounded limits required')
 d=pathlib.Path(directory);d.mkdir(parents=True,exist_ok=True)
 with (d/'LOCK').open('w') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  records,previous,end,state=journal(desc,d); t=total(desc);began=time.monotonic()
  if t>1000 and end+max_segments*segment_candidates>=t and not execute_full:raise ValueError('completion of large universe requires --execute-full; no full run authorized in 4A')
  for _ in range(max_segments):
   remain=budget-(time.monotonic()-began)
   if end==t or remain<1 or (d/'PAUSE').exists():break
   r=invoke(desc,end,min(end+segment_candidates,t),state,seconds=remain)
   r.update(index=len(records),previous=previous)
   atomic(d/f'segment-{len(records):08d}.json',r)
   previous=sha(wire(r));end=r['end'];state=r['state_out'];records.append(r)
   atomic(d/'HEAD.json',{'segments':len(records),'record_sha256':previous,'candidate_frontier':end,'candidate_total':t})
   print(json.dumps({'segments':len(records),'candidate_frontier':end,'candidate_total':t,'percent':100*end/t,'elapsed_seconds':time.monotonic()-began}),flush=True)
  status={'complete':end==t,'segments':len(records),'candidate_frontier':end,'candidate_total':t,'rows':sum(r['rows'] for r in records),'serialized_bytes':len(LINK_HEADER if is_links(desc) else HEADER)+sum(r['bytes'] for r in records),'full_stream_sha256':records[-1]['prefix_sha256'] if end==t else None,'qualification_established':False}
  atomic(d/'STATUS.json',status);return status

def verify(desc,directory,budget=50,max_segments=1):
 if not 0<budget<=60 or max_segments<1:raise ValueError('bounded replay limits')
 d=pathlib.Path(directory)
 with (d/'LOCK').open('w') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  records,_,_,_=journal(desc,directory)
  vd=d/'verification';vd.mkdir(exist_ok=True)
  state='INIT';began=time.monotonic();checked=0;previous=sha(wire(identity(desc)))
  # Validated completion records persist across bounded verification calls.
  # Their hashes detect alteration/loss; they are not authentication against a
  # hostile party able to rewrite the whole journal. Replay from scratch then.
  for k,p in enumerate(sorted(vd.glob('verified-*.json'))):
   v=read(p)
   if k>=len(records) or p.name!=f'verified-{k:08d}.json' or v['index']!=k or v['previous']!=previous or v['record_sha256']!=sha(wire(records[k])):
    raise ValueError('verification chain changed or incomplete')
   previous=sha(wire(v));state=records[k]['state_out'];checked+=1
  resumed=checked
  for r in records[checked:]:
   if checked-resumed>=max_segments or time.monotonic()-began>=budget-1:break
   v=invoke(desc,r['start'],r['end'],state,'predicate',budget-(time.monotonic()-began))
   for key in ('start','end','rows','bytes','state_in','state_out','segment_sha256','prefix_sha256'):
    if r[key]!=v[key]:raise ValueError('independent replay mismatch: '+key)
   entry={'index':checked,'record_sha256':sha(wire(r)),'previous':previous,'engine':'lexical-tsv-replay' if is_links(desc) else 'independent-predicate','result':'PASS'}
   atomic(vd/f'verified-{checked:08d}.json',entry);previous=sha(wire(entry));state=v['state_out'];checked+=1
  return {'previously_verified':resumed,'verified_segments':checked,'saved_segments':len(records),'all_saved_segments_replayed':checked==len(records),'independent_generator':not is_links(desc),'full_stream_verified':checked==len(records) and bool(records) and records[-1]['end']==total(desc)}

def main():
 p=argparse.ArgumentParser();p.add_argument('operation',choices=['build','run','verify']);p.add_argument('--descriptor',type=pathlib.Path,default=ROOT/'inputs/pairs.txt');p.add_argument('--directory',type=pathlib.Path,default=ROOT/'work/pairs');p.add_argument('--max-segments',type=int,default=1);p.add_argument('--segment-candidates',type=int,default=67108864);p.add_argument('--seconds',type=float,default=50);p.add_argument('--execute-full',action='store_true');a=p.parse_args()
 if a.operation=='build':print(build())
 elif a.operation=='run':print(json.dumps(run(a.descriptor,a.directory,a.max_segments,a.segment_candidates,a.seconds,a.execute_full)))
 else:print(json.dumps(verify(a.descriptor,a.directory,a.seconds,a.max_segments)))
if __name__=='__main__':main()
