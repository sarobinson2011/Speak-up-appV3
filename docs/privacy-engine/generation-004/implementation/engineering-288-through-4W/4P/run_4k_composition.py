"""Bounded signed semantic fixture, native partial rows, and completed stage reuse."""
import argparse,json,time,resource,sys,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('operation',choices=['construct','validate']);a=p.parse_args();start=time.monotonic();out=ROOT/'fixtures/4K-COMPLETE'
 if a.operation=='construct':
  from fixtures.integrated import make
  m,t=make(out,'GAMMA',semantic_outcomes=64,observation_bytes=256,profile_serial=801)
  c=json.loads(m.read_bytes());r={'operation':'independent-fixture-construction-and-signing','outcomes_per_world':64,'observation_bytes':256,'files':{n:e['bytes'] for n,e in c['records'].items()},'bytes_on_disk':sum(p.stat().st_size for p in out.rglob('*') if p.is_file())}
 else:
  from recovery_schedule.runner import run
  from link_recovery.cli import create_key
  from link_recovery import cli
  from unittest.mock import patch
  from tests.test_schedule import SchedulingTests
  work=ROOT/'work/4K-composition';work.mkdir(parents=True,exist_ok=True);key=work/'key';ck=work/'journal';create_key(key)
  calls=[];original=cli.execute
  def cut(a):a.new_bytes=23;return original(a)
  def execute(**kw):
   began=time.monotonic();v=run(out/'manifest.json',out/'trusted.json',ck,key,new_bytes=256*1024*1024,seconds=55-(time.monotonic()-start),progress=lambda x:print(json.dumps(x),file=sys.stderr),**kw)
   calls.append({'result':v['result'],'seconds':time.monotonic()-began,'reread_bytes':v['stage_schedule']['identity_bytes_reread'],'terminal_reused':v['stage_schedule']['terminal_reused']});return v
  with patch.object(cli,'execute',cut):paused=execute()
  assert paused['result']=='PAUSED' and not paused['profile_admitted']
  final=execute(resume=True);again=execute(resume=True)
  assert not final['failures'] and again['stage_schedule']['terminal_reused']
  # A separate scheduled uninterrupted job must have the same semantic verdict,
  # exact digests and counts as the interrupted/resumed execution.
  baseline=run(out/'manifest.json',out/'trusted.json',work/'uninterrupted',key,seconds=55-(time.monotonic()-start))
  normalize=SchedulingTests().semantic
  assert normalize(final)==normalize(baseline)==normalize(again)
  r={'operation':'bounded-composition-validation','result':'PASS','calls':calls,'semantic_equality_with_uninterrupted':True,'native_initial_byte_offset':23,'uninterrupted':baseline,'resumed':final,'durable_bytes':sum(p.stat().st_size for p in work.rglob('*') if p.is_file())}
 from integrated_auth.collector import implementation
 r.update(implementation=implementation(),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,profile_admitted=False,full_retained_stream_processed=False,performance_only_not_full_conformance=True)
 (ROOT/('results/4K-composition-'+a.operation+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in r if k not in ('implementation','uninterrupted','resumed')}))
if __name__=='__main__':main()
