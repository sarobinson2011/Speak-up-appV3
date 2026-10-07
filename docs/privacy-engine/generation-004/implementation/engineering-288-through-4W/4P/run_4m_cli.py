"""Actual CLI recovery commands against independently signed catalog fixtures."""
import subprocess,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
P=ROOT/'work/4M-cli';P.mkdir(parents=True,exist_ok=True)
rows=[]
def cmd(args,want,out):
 r=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,timeout=55)
 (P/(out+'.stdout')).write_text(r.stdout);(P/(out+'.stderr')).write_text(r.stderr)
 assert r.returncode==want,(args,r.returncode,r.stdout[-2000:],r.stderr[-2000:]);rows.append({'args':args,'exit':r.returncode,'expected':want})
 return json.loads(r.stdout) if r.stdout.strip().startswith('{') else None
cmd(['-m','integrated_auth','keygen','--key',str(P/'key')],0,'key')
for phase in ('E','PRE-EXECUTION','PRE-COMMITMENT'):
 p=P/phase;cmd(['-m','fixtures.catalogs',str(p),'--phase',phase],0,phase+'-fixture')
 common=['--key',str(P/'key'),'--manifest',str(p/'manifest.json'),'--trusted',str(p/'trusted.json'),'--checkpoint',str(p/'job')]
 a=cmd(['-m','integrated_auth','start',*common,'--new-bytes','1'],3,phase+'-paused');assert not a['profile_admitted']
 a=cmd(['-m','integrated_auth','resume',*common],0,phase+'-resumed');assert not a['profile_admitted'] and not a['actual_qualification_established']
 a=cmd(['-m','integrated_auth','resume',*common],0,phase+'-terminal');assert a['stage_schedule']['terminal_reused']
 # Standalone transport parser: no semantic completion inference.
 e=json.loads((p/'manifest.json').read_bytes())['request']['occurrence_bindings']['$cp4m_directory'];header=json.loads((p/e['path']).read_bytes().splitlines()[0]);expect=p/'expect.json';expect.write_text(json.dumps({'file':e,'kind':'occurrence_bindings','binding':header['binding'],'job':phase}))
 args=['-m','metadata_catalog',str(p/e['path']),'--expectation',str(expect),'--state',str(p/'transport'),'--key',str(P/'key')]
 cmd([*args,'--rows','1'],3,phase+'-transport-pause');a=cmd(args,0,phase+'-transport-resume');assert not a['authentication_success'] and not a['model_membership_established']
(P/'key').chmod(0o600)
r={'result':'PASS','commands':rows,'actual_admission':False,'full_stream_processed':False};(ROOT/'results/4M-cli.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','cli_commands':len(rows)}))
