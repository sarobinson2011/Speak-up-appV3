"""Bounded supplied-input benchmarks; never claims retained-stream completeness."""
import hashlib,json,pathlib,time,subprocess,platform,os
from link_stream.cli import ROOT,native,DESC,sha
from link_stream.validator import HEADER

def main():
 out=ROOT/'results/benchmark';out.mkdir(exist_ok=False);work=ROOT/'work/benchmark';work.mkdir(parents=True,exist_ok=True)
 began=time.monotonic();rows=0;paths=[];limits=[1000,10000,100000]
 # Only IDs and fixed groups are read. Construction emits at most 100,000
 # supplied potential rows total, never the retained full pair universe.
 with (ROOT/'inputs/links.txt').open() as f:
  _,n,m,fixedn=f.readline().split();n=int(n);names=[f.readline().strip() for _ in range(n)];fixed={}
  for _ in range(int(fixedn)):
   i,g=map(int,f.readline().split());fixed[i]=g
 order=sorted(range(n),key=names.__getitem__);current=work/'prefix-100000.tsv'
 with current.open('wb') as stream:
  stream.write(HEADER)
  for i in order:
   for j in order:
    if i<j and (i not in fixed or j not in fixed or fixed[i]==fixed[j]):
     rows+=1;stream.write((str(rows).rjust(6,'0')+'\t'+names[i]+'\t'+names[j]+'\t000000\tEQUALS\n').encode())
     if rows in limits:
      stream.flush();paths.append((rows,stream.tell()))
     if rows==limits[-1]:break
   if rows==limits[-1]:break
  stream.flush();os.fsync(stream.fileno())
 assert current.stat().st_size==paths[-1][1]
 for count,size in paths[:-1]:
  with current.open('rb') as src,(work/f'prefix-{count}.tsv').open('wb') as dst:
   remain=size
   while remain:
    b=src.read(min(1048576,remain));dst.write(b);remain-=len(b)
 prep=time.monotonic()-began;records=[];spent=129.67876338399583 # conservative aggregate including retained earlier attempts/diagnostics
 prior=spent
 for count,size in paths:
  limit=min(59,179-spent);p=work/f'prefix-{count}.tsv';chunk=4096 if count==1000 else 65536
  start=time.monotonic();r=native(p,ROOT/'inputs/links.txt',DESC,None,chunk,size+1,limit);wall=time.monotonic()-start;spent+=wall
  (out/f'{count}-receipt.json').write_text(json.dumps({'result':r,'wall_seconds':wall,'hard_seconds':limit,'supplied_size_before':size,'supplied_size_after':p.stat().st_size},indent=2)+'\n')
  assert r['result']=='REJECTED' and r['eof_observed'] and r['rows_validated']==count and r['complete_stream_sha256'] is None
  assert r['consumed_sha256']==sha(p)
  record={'supplied_rows':count,'supplied_bytes':size,'input_sha256':sha(p),'wall_seconds':wall,'hard_seconds':limit,'cumulative_benchmark_seconds':spent,'conformance_evidence':False,'result':r,'mb_per_second_including_model_load':size/wall/1e6,'mb_per_second_after_index_load':size/max(.000001,r['seconds']-r['index_seconds'])/1e6}
  (out/f'{count}.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record);print(json.dumps({'rows':count,'seconds':wall,'rss_kib':r['peak_rss_kib'],'total_seconds':spent}),flush=True)
 assert spent<=180 and all(r['wall_seconds']<=60 for r in records)
 report={'result':'PASS-BOUNDED-MEASUREMENTS','prior_benchmark_seconds':prior,'batch_seconds':spent-prior,'total_benchmark_seconds':spent,'preparation_seconds':prep,'maximum_supplied_rows':100000,'full_retained_universe_executed':False,'complete_retained_stream_sha256':None,'platform':platform.platform(),'records':records,'native_source_sha256':sha(ROOT/'link_stream/native.cpp'),'native_binary_sha256':sha(ROOT/'link_stream/native'),'controller_sha256':sha(ROOT/'link_stream/cli.py')}
 (ROOT/'results/benchmarks.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
