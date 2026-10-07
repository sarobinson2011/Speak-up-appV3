"""CP4F acquisition/recovery and CP4E scope/authentication plus retained recovery, streaming and ordered-admission checks."""
import argparse
import datetime
import hashlib
import json
import platform
import subprocess
import sys
import time
import unittest
from pathlib import Path
from admission_kernel.admission import collect
from admission_kernel.reuse import checkpoint2
from fixtures.construct import dataset, wire

ROOT = Path(__file__).resolve().parent


def hashes():
    result = {}
    for directory in ('accepted', 'retained', 'v4_ingest', 'amendments', 'rebinding'):
        for p in sorted((ROOT/directory).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                h=hashlib.sha256()
                with p.open('rb') as f:
                    while b:=f.read(1024*1024):h.update(b)
                result[p.relative_to(ROOT).as_posix()]=h.hexdigest()
    return result


class Results(unittest.TextTestResult):
    def startTest(self, test):
        self.start = time.monotonic();super().startTest(test)
    def addSuccess(self,test):
        self.rows.append({'test':test.id(),'result':'PASS','seconds':round(time.monotonic()-self.start,6)});super().addSuccess(test)
    def addFailure(self,test,err):
        self.rows.append({'test':test.id(),'result':'FAIL','detail':self._exc_info_to_string(err,test)});super().addFailure(test,err)
    def addError(self,test,err):
        self.rows.append({'test':test.id(),'result':'ERROR','detail':self._exc_info_to_string(err,test)});super().addError(test,err)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);a=ap.parse_args()
    out=a.output or ROOT/'results'/('checks-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    out=out.resolve()
    out.mkdir(parents=True,exist_ok=False);before=hashes();start=time.monotonic();Results.rows=[]
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),top_level_dir=str(ROOT))
    with (out/'tests.log').open('w') as log:
        result=unittest.TextTestRunner(stream=log,verbosity=2,resultclass=Results).run(suite)
    cli=[]
    for name in ('GAMMA','DELTA'):
        request,trusted=dataset(name)
        qpath,tpath=out/(name.lower()+'-request.json'),out/(name.lower()+'-lab-contract.json')
        qpath.write_bytes(wire(request));tpath.write_bytes(wire(trusted))
        for mode in ('CONDITIONAL-LAB','ACTUAL'):
            qpath_mode=out/(name.lower()+'-'+mode.lower()+'-request.json');request['mode']=mode;qpath_mode.write_bytes(wire(request))
            output=out/(name.lower()+'-'+mode.lower()+'-result.json')
            run=subprocess.run([sys.executable,'-m','admission_kernel',str(qpath_mode),'--lab-contract',str(tpath),'--output',str(output)],cwd=ROOT,capture_output=True,text=True,timeout=30)
            (out/(name.lower()+'-'+mode.lower()+'.stdout.txt')).write_text(run.stdout)
            (out/(name.lower()+'-'+mode.lower()+'.stderr.txt')).write_text(run.stderr)
            expected=0 if mode=='CONDITIONAL-LAB' else 2
            cli.append({'dataset':name,'mode':mode,'exit_code':run.returncode,'expected_exit':expected,'pass':run.returncode==expected and output.exists() and json.loads(output.read_bytes())['profile_admitted'] is False,
                        'profile_admitted':json.loads(output.read_bytes())['profile_admitted'] if output.exists() else None})
    reused=json.loads((ROOT/'inputs/universe.json').read_bytes())
    (out/'reused-checkpoint-2-admission-barriers.json').write_text(json.dumps(reused,indent=2)+'\n')
    unchanged=before==hashes()
    report={'result':'PASS' if result.wasSuccessful() and all(c['pass'] for c in cli) and unchanged else 'FAIL',
            'checkpoint':'4N','tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
            'tests':result.rows,'cli':cli,'accepted_and_retained_inputs_unchanged':unchanged,'expansion_rerun':False,
            'full_pair_stream_executed':False,'profile_admitted':False,'seconds':round(time.monotonic()-start,6),
            'python':sys.version,'platform':platform.platform()}
    (out/'check-results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='tests'},indent=2))
    if report['result']!='PASS':print((out/'tests.log').read_text()[-12000:])
    return 0 if report['result']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
