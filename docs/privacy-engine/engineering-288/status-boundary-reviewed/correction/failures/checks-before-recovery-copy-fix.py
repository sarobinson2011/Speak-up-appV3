"""New boundary controls only. No SQLite, network or existing host session access.
Positive flow uses exact retained launcher mechanics with disposable stub backend;
it is not a lifecycle, backend qualification or exact-host positive environment run.
"""
import argparse
import ast
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import pickle
import shutil
import subprocess
import sys
import tempfile
import types

ROOT = Path(__file__).resolve().parents[1]
CHECKS = []


def audit(event, args):
    if event.startswith('sqlite3.connect') or event in ('socket.connect', 'socket.bind'):
        raise AssertionError('DATABASE/NETWORK FORBIDDEN')
    if event == 'open' and isinstance(args[0], (str, bytes)):
        if os.fsdecode(args[0]).startswith('/home/steve/'):
            raise AssertionError('EXISTING HOST PATH FORBIDDEN')
sys.addaudithook(audit)


def need(ok, label):
    if not ok:
        raise AssertionError(label)
    CHECKS.append(label)


def load(path):
    spec = importlib.util.spec_from_file_location('boundary_under_test', path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def failure(fn, cls=BaseException):
    try:
        fn()
    except cls as e:
        return e
    raise AssertionError('expected rejection')


def state():
    return {'binding':'1'*64, 'seq':0, 'head':'0'*64, 'counts':{'attempt':0,'query':0,'snapshot':0,'verifier':0},
            'partitions':{'query':0,'snapshot':0,'verifier':0}, 'u':{}, 'active':None,
            'resources':{'slots':0,'holds':0,'query_holds':0,'extra_queries':0}}


def fixture(module, base, fault=None):
    launcher = module._load_launcher()  # Exact dependency verification/import.
    root = Path(base); root.mkdir()
    for n in ('candidate','draft','runtime'):
        (root/n).mkdir()
    calls = []; retained = []; managed_objects = []
    secret = 'PRIVATE-REASON-\u03bb-epoch-17'
    class Managed:
        def __init__(self):
            self.phase = 'READY'; self.saved = state(); managed_objects.append(self)
        def status(self):
            calls.append('status')
            return {'phase':self.phase,'reason':secret,'connection_epoch':17,
                    'actual_admission':False,'external_nonexecution_established':False,'authorization_renewed':False}
        def state(self):
            calls.append('state')
            if fault == 'state':
                raise ValueError(secret)
            return self.saved
        def handle(self, packet):
            calls.append(('handle', packet))
            if fault in ('handle','interrupt'):
                raise (KeyboardInterrupt(secret) if fault=='interrupt' else ValueError(secret))
            if fault == 'capability-result':
                return self
            return b'EXACT-AUTHENTICATED-RESPONSE\x00'
        def close(self):
            calls.append('managed-close')
            if fault == 'close':
                raise OSError(secret)
            self.phase='CLOSED'
    class Raw:
        def __init__(self, path, cfg, create=False, *, ownership_path):
            calls.append('raw-create')
            Path(path).touch(exist_ok=False); Path(ownership_path).touch(exist_ok=False)
        def close(self):
            calls.append('raw-close')
    def opening(*args, **kwargs):
        calls.append('open-session')
        if fault == 'open':
            raise RuntimeError(secret)
        m = Managed()
        return m, types.SimpleNamespace(a=m)
    launcher.inputs = lambda c,d:(Path(c),Path(d))
    launcher.validate_runtime = lambda r:Path(r)
    launcher.environment = lambda:{'fixture':'NO REAL ENVIRONMENT CLAIM'}
    launcher.enforce_environment = lambda:None
    launcher._profile.session_frontier = lambda *args:None
    launcher.load_runtime = lambda c,r:(types.SimpleNamespace(Authority=Raw),opening)
    original_write = launcher.write_new
    def write(p,x):
        original_write(p,x)
        retained.append((str(Path(p).relative_to(root)),Path(p).read_bytes()))
    launcher.write_new = write
    args = tuple(str(root/n) for n in ('candidate','draft','runtime','session'))
    return launcher,args,calls,retained,managed_objects,secret


def exercise(module, work):
    need(len(module.verify_inputs())==37,'exact dependencies verified')
    need(set(n for n in vars(module.Client) if not n.startswith('_'))=={'state','handle'},'client API only state/handle')
    l,a,c,r,objects,secret=fixture(module,work/'normal')
    held=[];control_held=[];capture=[]
    def control(cap):
        control_held.append(cap)
        value=cap.status()
        # Explicit test-only evidence sink, not installed by production entry.
        capture.append(json.dumps(value,ensure_ascii=False).encode())
    def client(cap):
        held.append(cap)
        need(cap.state()==state(),'state preserved')
        result=cap.state();result['counts']['attempt']=999
        need(objects[0].saved['counts']['attempt']==0,'state output detached')
        need(cap.handle(b'EXACT-PACKET')==b'EXACT-AUTHENTICATED-RESPONSE\x00','exact packet/response bytes preserved')
        for attr in ('status','recover','close','manager','managed','wrapper','scheduler','a','control','__dict__'):
            need(not hasattr(cap,attr),'no client capability attribute '+attr)
        need(cap.handle.__self__ is cap,'bound method receiver is only client')
        for name,fn in [('pickle',lambda:pickle.dumps(cap)),('copy',lambda:copy.copy(cap)),('deepcopy',lambda:copy.deepcopy(cap))]:
            need(type(failure(fn)) is TypeError,'no capability '+name)
        return objects[0]  # A hostile test callback result is not forwarded.
    stdout,stderr=io.StringIO(),io.StringIO()
    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
        result=module._run(l,*a,client,True,control)
    need(result is None and stdout.getvalue()==stderr.getvalue()=='','no automatic callback/status output')
    need(secret.encode() in capture[0] and 'λ'.encode() in capture[0],'explicit internal capture keeps full reason')
    need(c.index('raw-create')<c.index('raw-close')<c.index('open-session')<c.index('managed-close'),'initialization and close order preserved')
    complete=json.loads((Path(a[3])/'BOOTSTRAP-COMPLETE.json').read_bytes())
    need(complete['status']['reason']==secret and not (Path(a[3])/'ACTIVE.json').exists(),'original completion retention/active cleanup preserved')
    need(not module._OWNERS,'registry revoked after success')
    for cap in (held[0],control_held[0]):
        fn=cap.state if isinstance(cap,module.Client) else cap.status
        e=failure(fn,module.ClientFailure)
        need(e.__context__ is None and e.__cause__ is None,'expired capability has no original error chain')
    # Reopen metadata route with same synthetic state, not a real database.
    before=len([x for x in r if x[0].endswith('BOOTSTRAP-COMPLETE.json')])
    module._run(l,*a,lambda cap:cap.state(),False,None)
    need(before==len([x for x in r if x[0].endswith('BOOTSTRAP-COMPLETE.json')]),'reopen adds no automatic status receipt')
    original_binding=(Path(a[3])/'binding.json').read_bytes()
    (Path(a[3])/'binding.json').write_bytes(b'{}')
    previous=len(c)
    e=failure(lambda:module._run(l,*a,lambda cap:None,False,None),module.ClientFailure)
    need(len(c)==previous and secret not in str(e),'stale session binding refuses before managed open')
    (Path(a[3])/'binding.json').write_bytes(original_binding)
    # Output return channels cannot carry a manager through nested data/types.
    for label,value in [('direct',objects[0]),('nested',{'x':[objects[0]]}),('subclass',type('D',(dict,),{})())]:
        need(type(failure(lambda v=value:module._data(v))) is RuntimeError,'reject non-data capability '+label)
    for fault in ('handle','interrupt','close','open','state','capability-result'):
        l,a,c,r,objects,secret=fixture(module,work/fault,fault)
        held=[]
        def client(cap):
            held.append(cap)
            e=failure(lambda:cap.handle(b'FAULT'),module.ClientFailure)
            need(secret not in str(e) and e.__context__ is None and e.__cause__ is None,'sanitized dispatch '+fault)
            need(type(failure(cap.state)) is module.ClientFailure,'pending failure blocks later dispatch '+fault)
        fn=client if fault in ('handle','interrupt','capability-result') else lambda cap:held.append(cap)
        out,err=io.StringIO(),io.StringIO()
        with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
            e=failure(lambda:module._run(l,*a,fn,True,None),module.ClientFailure)
        need(not out.getvalue() and not err.getvalue() and secret not in str(e),'no automatic error output '+fault)
        need(e.__context__ is None and e.__cause__ is None,'outer error detached '+fault)
        records=list((Path(a[3])/'evidence').glob('failure-*'))
        need(len(records)==1 and (Path(a[3])/'ACTIVE.json').exists(),'existing failure record and uncertainty marker '+fault)
        failure_bytes=records[0].read_bytes()
        expected='RESPONSE-BYTES' if fault=='capability-result' else secret
        need(expected in json.loads(failure_bytes)['message'],'original error retained '+fault)
        need(not module._OWNERS,'capabilities revoked after failure '+fault)
    # General callback errors reach original evidence retention, not stdout.
    l,a,c,r,o,secret=fixture(module,work/'client-error')
    def bad(cap):raise RuntimeError(secret)
    e=failure(lambda:module._run(l,*a,bad,True,None),module.ClientFailure)
    need(secret not in str(e) and secret in json.loads(next((Path(a[3])/'evidence').glob('failure-*')).read_bytes())['message'],'client error retained privately')
    # Control failures are also retained; callback returns are never publication.
    l,a,c,r,o,secret=fixture(module,work/'control-error')
    def bad_control(cap):raise RuntimeError(secret)
    e=failure(lambda:module._run(l,*a,lambda cap:None,True,bad_control),module.ClientFailure)
    need(secret not in str(e) and next((Path(a[3])/'evidence').glob('failure-*')).is_file(),'control error uses existing failure path')
    # Public wiring delegates to same tested orchestration; no public backend arg.
    real_load=module._load_launcher
    try:
        l,a,c,r,o,secret=fixture(module,work/'public-run')
        module._load_launcher=lambda:l
        held=[]
        need(module.run(*a,lambda cap:held.append(cap),create=True) is None,'public run delegates without control')
        need(len(held)==1 and c.count('status')==1,'general run has only launcher diagnostic call')
    finally:module._load_launcher=real_load
    # Prospective CLI normal and error sinks, exercising its actual main body.
    for fault in (None,'close'):
        l,a,c,r,o,secret=fixture(module,work/('cli-'+str(fault)),fault)
        module._load_launcher=lambda:l
        out,err=io.StringIO(),io.StringIO()
        try:
            argv=['initialize']+sum(([f'--{n}',v] for n,v in zip(('candidate','draft','runtime','destination'),a)),[])
            with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):code=module.main(argv)
        finally:module._load_launcher=real_load
        need(code==(1 if fault else 0),'CLI disposition '+str(fault))
        need(secret not in out.getvalue()+err.getvalue() and 'Traceback' not in err.getvalue(),'CLI no diagnostic/error serialization '+str(fault))
        need(c.count('status')==1,'CLI no extra status call '+str(fault))
    out,err=io.StringIO(),io.StringIO()
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):code=module.main(['PRIVATE-ARG'])
    need(code==1 and out.getvalue()=='' and err.getvalue()=='FAILED; outcome uncertain; admission disabled\n','CLI parse failure fixed output')
    # Original stdout witness, AST-selected main only with disposable stub.
    old=ROOT/'retained/launcher/code/lab_bootstrap.py'
    node=next(n for n in ast.parse(old.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='main')
    @contextlib.contextmanager
    def fake_session(*args,**kwargs):
        yield types.SimpleNamespace(status=lambda:{'reason':'ORIGINAL-STDOUT-WITNESS'},state=lambda:{})
    ns={'argparse':argparse,'json':json,'session':fake_session}
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(old),'exec'),ns)
    oldargv=sys.argv;sys.argv=['old','initialize'];out=io.StringIO()
    try:
        with contextlib.redirect_stdout(out):ns['main']()
    finally:sys.argv=oldargv
    (work/'original-stdout-witness.txt').write_text(out.getvalue())
    need('ORIGINAL-STDOUT-WITNESS' in out.getvalue(),'retained historical stdout witness reproduced with stub')


def process(command, label, output):
    p=subprocess.run(command,capture_output=True,text=True,timeout=45)
    (output/(label+'.stdout')).write_text(p.stdout);(output/(label+'.stderr')).write_text(p.stderr)
    return {'label':label,'command':command,'returncode':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--child',action='store_true');args=parser.parse_args()
    out=Path(args.output).absolute();out.mkdir(parents=True,exist_ok=False)
    m=load(ROOT/'code/prospective_entry.py')
    try:
        exercise(m,out)
        processes=[]
        if not args.child:
            for label in ('fresh','recovered'):
                root=ROOT
                if label=='recovered':
                    root=out/'recovered-root'
                    shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('results','__pycache__'))
                r=process([sys.executable,'-I','-B',str(root/'tests/checks.py'),'--child','--output',str(out/(label+'-evidence'))],label,out)
                processes.append(r);need(r['returncode']==0,label+' process positive boundary checks')
            # Actual public environment guard: this assessment host must refuse.
            r=process([sys.executable,'-I','-B',str(ROOT/'code/prospective_entry.py'),'initialize','--candidate',str(out/'NO-CANDIDATE'),'--draft',str(out/'NO-DRAFT'),'--runtime',str(out/'NO-RUNTIME'),'--destination',str(out/'NEVER-CREATED')],'actual-public-refusal',out)
            processes.append(r);need(r['returncode']==1 and not (out/'NEVER-CREATED').exists(),'actual public guard refuses before session creation')
            # Stale binding and unsupported filesystem entries, no app import.
            mutation_root=out/'mutations';mutation_root.mkdir()
            for name in ('contract','decision','launcher','manager','pins','fifo','empty-dir','symlink'):
                root=mutation_root/name
                for part in ('code','contract','retained','provenance'):
                    shutil.copytree(ROOT/part,root/part)
                target={'contract':'contract/CONTRACT-draft-1.txt','decision':'contract/DECISION.json','launcher':'retained/launcher/code/lab_bootstrap.py','manager':'retained/candidate/compiler/live_connection.py','pins':'provenance/dependency-pins.json'}.get(name)
                if target:
                    p=root/target;p.write_bytes(p.read_bytes()+b'\n')
                elif name=='fifo':os.mkfifo(root/'retained/unlisted')
                elif name=='empty-dir':(root/'retained/empty').mkdir()
                else:(root/'retained/link').symlink_to('launcher')
                code="import runpy; m=runpy.run_path("+repr(str(root/'code/prospective_entry.py'))+"); m['verify_inputs']()"
                r=process([sys.executable,'-I','-B','-c',code],'reject-'+name,out)
                processes.append(r);need(r['returncode']!=0,'reject stale/unsupported '+name)
        result={'result':'PASS','checks':CHECKS,'count':len(CHECKS),'processes':processes,'positive_backend':'DISPOSABLE STUB; exact retained launcher mechanics','real_database_connections':0,'real_managed_lifecycle_executions':0,'completed_reviews_rerun':0,'host_sessions_accessed':False,'actual_admission':False}
        (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'result':'PASS','checks':len(CHECKS),'processes':len(processes)}))
    except BaseException:
        (out/'PARTIAL.json').write_text(json.dumps({'passed':CHECKS},indent=2)+'\n')
        raise


if __name__=='__main__':main()
