from pathlib import Path
import json,datetime,os
base=Path('/workspace/scratch/ace5c9b2f18b/ld01-review');proc=base/'processes/public-recovered';rows=[]
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:
  argv=(p/'cmdline').read_bytes().split(b'\x00')
  if b'/workspace/scratch/ace5c9b2f18b/ld01-review/code/public_reuse.py' not in argv:continue
  stat=(p/'stat').read_text().split();rows.append({'host_pid':int(p.name),'state':stat[2],'start_ticks':stat[21],'cpu_ticks':int(stat[13])+int(stat[14]),'rss_pages':int(stat[23])})
 except (FileNotFoundError,PermissionError,ProcessLookupError):pass
v={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'processes':rows,'stdout_bytes':(proc/'stdout.log').stat().st_size,'stderr_bytes':(proc/'stderr.log').stat().st_size,'exit_status_present':(proc/'exit-status.json').exists()}
with (proc/'read-only-inspections.jsonl').open('a') as f:f.write(json.dumps(v)+'\n')
print(json.dumps(v))
print((proc/'progress.jsonl').read_text().splitlines()[-1])
if v['exit_status_present']:print((proc/'exit-status.json').read_text())
