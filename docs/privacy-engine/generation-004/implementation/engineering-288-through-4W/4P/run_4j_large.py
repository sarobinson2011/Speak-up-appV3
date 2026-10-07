"""Bounded complete semantic fixture: construction and validation in separate processes."""
import argparse,json,time,resource,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('operation',choices=['construct','validate']);p.add_argument('--outcomes',type=int,default=512);a=p.parse_args();start=time.monotonic();out=ROOT/'fixtures/4J-LARGE'
 if a.operation=='construct':
  from fixtures.integrated import make
  m,t=make(out,'GAMMA',semantic_outcomes=a.outcomes,observation_bytes=256,profile_serial=601)
  carrier=json.loads(m.read_bytes());r={'operation':'independent-fixture-construction-and-signing','outcomes_per_world':a.outcomes,'observation_bytes':256,'semantics':'complete finite supports, independently computed normalized equal worlds and zero exact distance; no opaque padding','files':{n:e['bytes'] for n,e in carrier['records'].items()},'material_max_bytes':max(e['bytes'] for e in carrier['materials'].values()),'bytes_on_disk':sum(p.stat().st_size for p in out.rglob('*') if p.is_file()),'profile_admitted':False}
 else:
  from integrated_auth.collector import run
  from link_recovery.cli import create_key
  work=ROOT/'work/4J-large';work.mkdir(parents=True,exist_ok=True);key=work/'key';ck=work/'journal'
  if not key.exists():create_key(key)
  r=run(out/'manifest.json',out/'trusted.json',ck,key,resume=ck.exists(),new_bytes=256*1024*1024,seconds=55,progress=lambda v:print(json.dumps(v),file=sys.stderr))
  r['operation']='bounded-complete-semantic-collector';r['benchmark_only_for_performance_estimates']=True
 from integrated_auth.collector import implementation
 r['implementation']=implementation()
 r['seconds']=time.monotonic()-start;r['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 (ROOT/('results/4J-large-'+a.operation+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k in ('operation','result','seconds','peak_rss_kib','files','material_max_bytes','bytes_on_disk','reasons')}))
 if a.operation=='validate' and r['failures']:return 2
 return 0
if __name__=='__main__':raise SystemExit(main())
