"""Projection fixture CLI recovery in every phase; actual admission disabled."""
import subprocess,sys,json,tempfile,resource
from pathlib import Path
ROOT=Path(__file__).resolve().parent;rows=[]
with tempfile.TemporaryDirectory(prefix='4p-cli-') as td:
 p=Path(td)
 def cmd(args,want):
  def limits():resource.setrlimit(resource.RLIMIT_NOFILE,(96,96))
  r=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,timeout=55,preexec_fn=limits)
  assert r.returncode==want,(args,r.returncode,r.stdout[-2500:],r.stderr[-1500:]);rows.append({'args':args,'exit':r.returncode,'expected':want})
  return json.loads(r.stdout) if r.stdout.strip().startswith('{') else None
 cmd(['-m','integrated_auth','keygen','--key',str(p/'key')],0)
 for phase in ('E','PRE-EXECUTION','PRE-COMMITMENT'):
  source=p/phase;cmd(['-m','fixtures.generated_events',str(source),'--phase',phase],0)
  common=['--key',str(p/'key'),'--manifest',str(source/'manifest.json'),'--trusted',str(source/'trusted.json'),'--checkpoint',str(source/'job')]
  r=cmd(['-m','integrated_auth','start',*common,'--new-bytes','1'],3);assert not r['profile_admitted']
  r=cmd(['-m','integrated_auth','resume',*common],0);assert not r['actual_qualification_established'] and r['occurrence_acquisition']['generated_projections']==92
  r=cmd(['-m','integrated_auth','resume',*common],0);assert r['stage_schedule']['terminal_reused']
  (source/'job').write_bytes(b'{}\n');r=cmd(['-m','integrated_auth','resume',*common],2);assert not r['profile_admitted']
r={'result':'PASS','commands':rows,'handle_limit':96,'actual_admission':False,'full_stream_processed':False};(ROOT/'results/4P-cli.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','cli_commands':len(rows)}))
