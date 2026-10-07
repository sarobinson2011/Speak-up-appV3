#!/usr/bin/env python3
"""Optional bounded local throughput measurement; never a full-stream receipt."""
import json,resource,subprocess,time
from run_task import ROOT,PLAN,verify_package,prefix,read,wire
verify_package();resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
records=[];began=time.monotonic()
for width in (16,64):
 starts=range(0,PLAN['candidate_total'],width)
 start=max(starts,key=lambda a:prefix(ROOT,min(a+width,PLAN['candidate_total']))[1]-prefix(ROOT,a)[1]);end=min(start+width,PLAN['candidate_total'])
 t=time.monotonic()
 try:
  p=subprocess.run([str(ROOT/'runner/links'),str(ROOT/PLAN['descriptor']),str(start),str(end),'INIT','complement','55'],capture_output=True,text=True,timeout=58)
  if p.returncode:raise RuntimeError(p.stderr.strip())
  x=json.loads(p.stdout);expected_rows=prefix(ROOT,end)[0]-prefix(ROOT,start)[0];expected_bytes=prefix(ROOT,end)[1]-prefix(ROOT,start)[1]
  if x['rows']!=expected_rows or x['bytes']!=expected_bytes:raise ValueError('analytical metadata mismatch; stop before any full run')
  elapsed=time.monotonic()-t;records.append({'segment_ranks':width,'start':start,'end':end,'rows':x['rows'],'bytes':x['bytes'],'wall_seconds':elapsed,'worker_seconds':x['seconds'],'effective_MB_s':x['bytes']/elapsed/1e6,'safe_45_second_segment_with_margin':elapsed<=35,'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'measurement_only':True})
 except (RuntimeError,ValueError,subprocess.TimeoutExpired) as e:records.append({'segment_ranks':width,'result':'UNSAFE-OR-FAILED-PROBE','error':str(e),'wall_seconds':time.monotonic()-t,'measurement_only':True})
 if time.monotonic()-began>=120:break
print(json.dumps({'result':'BOUNDED-LOCAL-PERFORMANCE-PROBE','records':records,'aggregate_seconds':time.monotonic()-began,'maximum_individual_seconds':58,'maximum_aggregate_seconds':116,'estimated_full_pass_hours_from_effective_rates':[{ 'segment_ranks':x['segment_ranks'],'hours':PLAN['serialized_bytes']/(x['effective_MB_s']*1e6)/3600} for x in records if 'effective_MB_s' in x],'limitations':'Size-weighted local extrapolation only; startup, late journal audit overhead and content-dependent throughput vary. No complete-stream SHA or independent supplied-file validation. Choose 64 only if safely under 35s; otherwise 16 if it passes. If neither passes, preserve results and do not launch.','parent_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'full_enumeration_started':False,'actual_admission':False},indent=2))
