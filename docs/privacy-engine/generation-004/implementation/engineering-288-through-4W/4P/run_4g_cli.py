"""Fresh small-fixture CLI/recovery smoke; original source/authority stays conditional."""
import json,subprocess,sys,tempfile
from pathlib import Path
from fixtures.auth_jobs import make
ROOT=Path(__file__).resolve().parent

def main():
    rows=[]
    with tempfile.TemporaryDirectory(prefix='cp4g-cli-') as d:
        root=Path(d);job=make(root/'input');key=root/'key';ck=root/'signature';pk=json.loads((job.parent/'external-appointment.json').read_bytes())['public_key']
        base=['--job',str(job),'--key',str(key),'--checkpoint',str(ck),'--public-key',pk,'--seconds','10']
        cases=[(['keygen','--key',str(key)],0),(['start',*base,'--new-bytes','1'],3),(['resume',*base,'--new-bytes','31'],3),(['resume',*base,'--new-bytes','1000000'],0),(['resume',*base,'--new-bytes','1000000'],0)]
        for args,expected in cases:
            p=subprocess.run([sys.executable,'-m','pure_auth',*args],cwd=ROOT,capture_output=True,text=True,timeout=15);r=json.loads(p.stdout) if p.stdout else None
            rows.append({'operation':args[0],'expected_exit':expected,'actual_exit':p.returncode,'pass':p.returncode==expected,'result':r,'progress':p.stderr})
        for op,n,expected in [('preflight','25',3),('continue','1000000',0)]:
            args=[op,'--job',str(job),'--key',str(key),'--checkpoint',str(root/'preflight'),'--public-key',pk,'--new-bytes',n,'--seconds','10']
            p=subprocess.run([sys.executable,'-m','pure_auth',*args],cwd=ROOT,capture_output=True,text=True,timeout=15);r=json.loads(p.stdout)
            rows.append({'operation':op,'expected_exit':expected,'actual_exit':p.returncode,'pass':p.returncode==expected,'result':r,'progress':p.stderr})
        f=job.parent/'links.tsv';b=f.read_bytes();f.write_bytes(b[:-1]+b'x')
        p=subprocess.run([sys.executable,'-m','pure_auth','resume',*base,'--new-bytes','1000000'],cwd=ROOT,capture_output=True,text=True,timeout=15);r=json.loads(p.stdout);rows.append({'operation':'mutated-completed-input','actual_exit':p.returncode,'pass':p.returncode==2 and not r['cryptographic_signature_verified'],'result':r})
    r={'result':'PASS' if all(x['pass'] for x in rows) else 'FAIL','cases':rows,'profile_admitted':False};(ROOT/'results/4G-cli.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':r['result'],'cases':len(rows)}));return 0 if r['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
