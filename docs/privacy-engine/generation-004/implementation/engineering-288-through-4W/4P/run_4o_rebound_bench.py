"""Final required-containing-object enforcement: fresh signed fixture and job."""
import json,subprocess,sys,time,resource,os,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent;r=json.loads((ROOT/'results/4O-benchmark-summary.json').read_bytes())
for mode in ('construct','validate'):
 shutil.copyfile(ROOT/('results/4O-benchmark-'+mode+'.json'),ROOT/('results/4O-benchmark-'+mode+'-pre-hardening.json'))
 code="import run_4o_bench as b;from pathlib import Path;b.WORK=Path('work/4O-rebound').resolve();b.child("+repr(mode)+")"
 start=time.monotonic()
 with (ROOT/('results/4O-benchmark-rebound-'+mode+'.log')).open('w') as log:
  p=subprocess.Popen([sys.executable,'-c',code],cwd=ROOT,stdout=log,stderr=log)
  while True:
   pid,status,usage=os.wait4(p.pid,os.WNOHANG)
   if pid:break
   if time.monotonic()-start>=min(59.5,179.5-r['total_seconds']):p.kill();pid,status,usage=os.wait4(p.pid,0);break
   time.sleep(.05)
  p.returncode=os.waitstatus_to_exitcode(status)
 row={'stage':'final-enforcement-'+mode,'seconds':time.monotonic()-start,'exit':p.returncode,'child_maxrss_kib':usage.ru_maxrss,'cpu_seconds':usage.ru_utime+usage.ru_stime};r['runs'].append(row);r['total_seconds']+=row['seconds'];print(json.dumps(row),flush=True)
 r['result']='PASS' if p.returncode==0 else 'FAIL';(ROOT/'results/4O-benchmark-summary.json').write_text(json.dumps(r,indent=2)+'\n')
 if p.returncode:sys.exit(p.returncode)
