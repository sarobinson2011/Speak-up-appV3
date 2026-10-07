"""Reproducible bounded CP4E CLI evidence; all signing keys are public LAB keys."""
import argparse,json,subprocess,sys,time
from pathlib import Path
from fixtures.construct import dataset,wire
from fixtures.scope_cases import disconnected,export
from tests.test_admission import bad_signature
ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    cases=[]
    for name in ('connected','disconnected','actual','wrong-authority','missing-source-and-bad-signature','changed-file'):
        q,t=disconnected() if name=='disconnected' else dataset()
        if name=='actual':q['mode']='ACTUAL'
        if name=='wrong-authority':del t['appointment']
        if name=='missing-source-and-bad-signature':bad_signature(q)
        manifest=export(q,t,a.output/name)
        data=json.loads(manifest.read_bytes())
        if name=='missing-source-and-bad-signature':
            entry=next(x for x in data['objects'] if x['digest']==t['scope_source_ref']['material_sha256']);(manifest.parent/entry['blob']['path']).unlink()
        if name=='changed-file':
            entry=data['bundles']['ROOT-ELIGIBLE']['files']['links.tsv'];f=manifest.parent/entry['path'];b=f.read_bytes();f.write_bytes(b[:-1]+b'!')
        out=manifest.parent/'result.json';cmd=[sys.executable,'-m','scope_auth',str(manifest.resolve()),'--lab-contract',str((manifest.parent/'lab-contract.json').resolve()),'--output',str(out.resolve())]
        start=time.monotonic();r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=30);elapsed=time.monotonic()-start
        result=json.loads(out.read_bytes());expected=0 if name in ('connected','disconnected') else 2
        required={'actual':['INVALID-EVIDENCE-AUTHORITY'],'wrong-authority':['INVALID-EVIDENCE-AUTHORITY'],
          'missing-source-and-bad-signature':['MISSING-EVIDENCE','INVALID-EVIDENCE-AUTHENTICATION'], 'changed-file':['INVALID-EVIDENCE-DIGEST']}.get(name,[])
        ok=r.returncode==expected and not result['profile_admitted'] and all(x in result['failures'] for x in required)
        cases.append({'case':name,'pass':ok,'exit_code':r.returncode,'expected_exit':expected,'seconds':elapsed,'failures':result['failures'],'stdout':r.stdout,'stderr':r.stderr})
    report={'result':'PASS' if all(x['pass'] for x in cases) else 'FAIL','cases':cases,'full_stream_executed':False,'benchmark_seconds':0,'profile_admitted':False}
    (a.output/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0 if report['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
