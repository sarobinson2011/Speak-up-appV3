"""Count every attempt; regenerate fixture after implementation identity change."""
import json,subprocess,sys,time,resource,os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'results/4N-benchmark-summary.json').read_bytes())
for mode in ('construct','validate'):
 code="import run_4n_bench as b;from pathlib import Path;b.WORK=Path('work/4N-rebound').resolve();b.child("+repr(mode)+")"
 start=time.monotonic()
 with (ROOT/('results/4N-benchmark-rebound-'+mode+'.log')).open('w') as log:
  p=subprocess.Popen([sys.executable,'-c',code],cwd=ROOT,stdout=log,stderr=log)
  while True:
   pid,status,usage=os.wait4(p.pid,os.WNOHANG)
   if pid:break
   if time.monotonic()-start>=min(59.5,179.5-r['total_seconds']):p.kill();pid,status,usage=os.wait4(p.pid,0);break
   time.sleep(.05)
  p.returncode=os.waitstatus_to_exitcode(status)
 row={'stage':'rebound-'+mode,'seconds':time.monotonic()-start,'exit':p.returncode,'child_maxrss_kib':usage.ru_maxrss,'cpu_seconds':usage.ru_utime+usage.ru_stime};r['runs'].append(row);r['total_seconds']+=row['seconds'];print(json.dumps(row),flush=True)
 r['result']='PASS-WITH-RECORDED-STALE-FIXTURE-REJECTION' if p.returncode==0 else 'REBOUND-FAILED'
 (ROOT/'results/4N-benchmark-summary.json').write_text(json.dumps(r,indent=2)+'\n')
 if p.returncode:sys.exit(p.returncode)
