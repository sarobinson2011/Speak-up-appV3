"""Legacy small admission CLI checks; ACTUAL must reject."""
import tempfile,json,subprocess,sys
from pathlib import Path
from fixtures.construct import dataset,wire
rows=[]
with tempfile.TemporaryDirectory(prefix='4n-legacy-cli-') as td:
 p=Path(td)
 for family in ('GAMMA','DELTA'):
  q,t=dataset(family);(p/'trusted').write_bytes(wire(t))
  for mode in ('CONDITIONAL-LAB','ACTUAL'):
   q['mode']=mode;(p/'request').write_bytes(wire(q))
   r=subprocess.run([sys.executable,'-m','admission_kernel',str(p/'request'),'--lab-contract',str(p/'trusted'),'--output',str(p/'out')],capture_output=True,text=True,timeout=30)
   got=json.loads((p/'out').read_bytes());expected=0 if mode=='CONDITIONAL-LAB' else 2
   assert r.returncode==expected and not got['profile_admitted'],(r.stderr,got)
   rows.append({'family':family,'mode':mode,'exit':r.returncode,'profile_admitted':False})
result={'result':'PASS','commands':rows,'full_stream_processed':False};Path('results/4N-legacy-cli.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
