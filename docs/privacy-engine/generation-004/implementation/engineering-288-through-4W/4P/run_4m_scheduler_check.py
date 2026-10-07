import subprocess,time,os,resource,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent;report=root/'results/4M-benchmarks.json';r=json.loads(report.read_bytes());start=time.monotonic()
with (root/'results/4M-benchmark-scheduler-final.log').open('w') as log:
 p=subprocess.Popen([sys.executable,'run_4m_metadata.py','scheduler'],stdout=log,stderr=log,cwd=root)
 while True:
  pid,status,usage=os.wait4(p.pid,os.WNOHANG)
  if pid:break
  if time.monotonic()-start>=min(59.5,179.5-r['total_seconds']):p.kill();pid,status,usage=os.wait4(p.pid,0);break
  time.sleep(.05)
 p.returncode=os.waitstatus_to_exitcode(status)
row={'stage':'scheduler-snapshot-api','seconds':time.monotonic()-start,'exit':p.returncode,'child_maxrss_kib':usage.ru_maxrss,'child_cpu_seconds':usage.ru_utime+usage.ru_stime,'corrective':True};r['processes'].append(row);r['total_seconds']+=row['seconds'];r['result']='PASS-AFTER-SNAPSHOT-CORRECTION' if p.returncode==0 else 'SCHEDULER-CAPACITY-NOT-VERIFIED';report.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(row))
