"""Fresh bounded CLI recovery/integration smoke; no retained stream processing."""
import json,subprocess,sys,tempfile
from pathlib import Path
from fixtures.auth_jobs import make
ROOT=Path(__file__).resolve().parent

def main():
    rows=[]
    with tempfile.TemporaryDirectory(prefix='cp4f-cli-') as d:
        root=Path(d);job=make(root/'input');key=root/'key';ck=root/'journal'
        cases=[(['keygen','--key',str(key)],0),(['start','--job',str(job),'--key',str(key),'--checkpoint',str(ck),'--new-bytes','25','--seconds','15'],3),(['resume','--job',str(job),'--key',str(key),'--checkpoint',str(ck),'--new-bytes','1000000','--seconds','15'],0),(['continue','--job',str(job),'--key',str(key),'--checkpoint',str(ck),'--new-bytes','1000000','--seconds','15','--appointment',str(job.parent/'external-appointment.json')],2)]
        for args,expected in cases:
            p=subprocess.run([sys.executable,'-m','large_auth',*args],cwd=ROOT,capture_output=True,text=True,timeout=30)
            result=json.loads(p.stdout) if p.stdout else None
            rows.append({'operation':args[0],'exit_code':p.returncode,'expected':expected,'pass':p.returncode==expected,'result':result,'progress':p.stderr})
        f=job.parent/'tokens.tsv';b=f.read_bytes();f.write_bytes(b[:-1]+b'x')
        p=subprocess.run([sys.executable,'-m','large_auth','resume','--job',str(job),'--key',str(key),'--checkpoint',str(ck),'--seconds','15'],cwd=ROOT,capture_output=True,text=True,timeout=30)
        rows.append({'operation':'mutated-completed-input','exit_code':p.returncode,'expected':2,'pass':p.returncode==2,'result':json.loads(p.stdout)})
    r={'result':'PASS' if all(x['pass'] for x in rows) else 'FAIL','cases':rows,'profile_admitted':False}
    (ROOT/'results/4F-cli.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':r['result'],'cases':len(rows)}));return 0 if r['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
