"""Bounded meaningful owning-value fixture; independent signing vs validation RSS."""
import argparse,json,time,resource
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('operation',choices=('construct','validate'));a=p.parse_args();began=time.monotonic();out=ROOT/'fixtures/4L-LARGE'
 if a.operation=='construct':
  from fixtures.occurrence import export
  export(out,phase='PRE-COMMITMENT',value_bytes=8*1024*1024)
  r={'operation':'independent-owning-fixture-construction-and-signing','value_body_bytes':8*1024*1024,'required_token_occurrences':4,'input_bytes':sum(p.stat().st_size for p in out.rglob('*') if p.is_file()),'opaque_padding':False}
 else:
  from recovery_schedule.runner import run
  from link_recovery.cli import create_key
  from unittest.mock import patch
  from recovery_schedule.state import Scheduler
  from link_recovery.cli import PauseRequested
  p=ROOT/'work/4L-large';p.mkdir(parents=True,exist_ok=True);create_key(p/'key');args=(out/'manifest.json',out/'trusted.json',p/'journal',p/'key')
  original=Scheduler.save
  def stop(self,label,*a,**kw):
   if label=='ordered-ledger':raise PauseRequested()
   return original(self,label,*a,**kw)
  with patch.object(Scheduler,'save',stop):
   try:run(*args,new_bytes=268435456,seconds=55)
   except PauseRequested:pass
   else:raise AssertionError('interruption did not occur')
  result=run(*args,resume=True,new_bytes=268435456,seconds=max(.1,55-(time.monotonic()-began)))
  assert result['processing_complete'] and not result['failures'],result
  oracle=json.loads((out/'oracle.json').read_text())
  for scope,e in oracle.items():
   s=result['bindings']['scope_validation']['scopes'][scope];v=s['link_validation'];assert s['node_indices']==e['indices'] and v['complete_stream_sha256']==e['links_sha256'] and v['structural_rows']==e['structural'] and v['potential_rows']==e['potential']
  r={'operation':'bounded-owning-validation-and-recovery','result':'PASS','independent_oracle_match':True,'resumed_after_preledger_interrupt':True,'validation':result,'durable_bytes':sum(f.stat().st_size for f in p.rglob('*') if f.is_file())}
 r.update(seconds=time.monotonic()-began,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,full_retained_stream_processed=False,profile_admitted=False,performance_only_not_full_conformance=True)
 (ROOT/('results/4L-large-'+a.operation+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='validation'}))
if __name__=='__main__':main()
