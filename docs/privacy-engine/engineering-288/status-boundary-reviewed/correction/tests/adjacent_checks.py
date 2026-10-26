"""Adjacent value/capability and caught-error controls; disposable backend only."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]


def main():
    out=Path(sys.argv[1]).absolute();out.mkdir(parents=True,exist_ok=False)
    spec=importlib.util.spec_from_file_location('boundary_controls',ROOT/'tests/checks.py')
    t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
    m=t.load(ROOT/'code/prospective_entry.py');checks=[]
    def need(ok,label):
        if not ok:raise AssertionError(label)
        checks.append(label)
    class Unsafe:
        def __repr__(self):raise AssertionError('UNEXPECTED-REPR')
        def __deepcopy__(self,memo):raise AssertionError('UNEXPECTED-COPY')
    for kind in ('state-extra-status','state-nested-object','response-subclass','packet-object','caught-then-client-error'):
        l,a,c,r,objects,secret=t.fixture(m,out/kind,'handle' if kind=='caught-then-client-error' else None)
        def control(cap):
            obj=objects[0]
            if kind=='state-extra-status':obj.saved['status']=obj.status()
            if kind=='state-nested-object':obj.saved['u']['x']=Unsafe()
            if kind=='response-subclass':obj.handle=lambda packet:type('B',(bytes,),{})(b'x')
        def client(cap):
            call=cap.state if kind.startswith('state-') else lambda:cap.handle(Unsafe() if kind=='packet-object' else b'x')
            e=t.failure(call,m.ClientFailure)
            need(e.args==('MANAGED-OPERATION-UNAVAILABLE; outcome uncertain; no renewed authorization',),'fixed error args '+kind)
            need(e.__context__ is None and e.__cause__ is None and not e.__dict__,'no diagnostic exception fields '+kind)
            if kind=='caught-then-client-error':raise KeyError('SECOND-CLIENT-ERROR')
        stdout,stderr=io.StringIO(),io.StringIO()
        with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
            e=t.failure(lambda:m._run(l,*a,client,True,control),m.ClientFailure)
        need(stdout.getvalue()==stderr.getvalue()=='' and not m._OWNERS,'no publication and revoked '+kind)
        record=json.loads(next((Path(a[3])/'evidence').glob('failure-*')).read_bytes())
        need(record['nonexecution_established'] is False and record['new_authorization'] is False,'uncertainty preserved '+kind)
        if kind=='caught-then-client-error':
            need(secret in record['message'] and 'SECOND-CLIENT-ERROR' in record['traceback'],'original and later client error retained')
    l,a,c,r,objects,secret=t.fixture(m,out/'nonready-diagnostic')
    def control(cap):
        objects[0].phase='QUARANTINED'
        need(cap.status()['phase']=='QUARANTINED','nonREADY internal status remains available')
    m._run(l,*a,lambda cap:None,True,control)
    l,a,c,r,objects,secret=t.fixture(m,out/'public-controlled')
    original=m._load_launcher;m._load_launcher=lambda:l
    evidence=[]
    try:
        need(m.run_controlled(*a,lambda cap:None,create=True,control=lambda cap:evidence.append(cap.status())) is None,'designated controlled entry returns no diagnostic')
    finally:m._load_launcher=original
    need(evidence[0]['reason']==secret,'designated controlled entry preserves exact reason')
    (out/'RESULT.json').write_text(json.dumps({'result':'PASS','checks':checks,'count':len(checks),'real_backend_execution':False},indent=2)+'\n')
    print(json.dumps({'result':'PASS','checks':len(checks)}))


if __name__=='__main__':main()
