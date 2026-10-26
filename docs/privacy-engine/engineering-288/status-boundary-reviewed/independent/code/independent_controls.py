"""Formal-Lab[6] independent boundary controls. No real backend or session.

Runs unchanged entry/launcher mechanics with reviewer-written in-memory backend
fixtures. No Engineering test module is imported. All test state is create-only
under the caller-selected persistent evidence directory.
"""
import argparse, ast, contextlib, copy, hashlib, importlib.metadata, io, json
import os, pickle, platform, sys, traceback, types
from pathlib import Path

CHECKS=[]
def need(v,label):
    if not v: raise AssertionError(label)
    CHECKS.append(label)

def load(path):
    m=types.ModuleType('independent_target');m.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__)
    return m

def failure(fn):
    try: fn()
    except BaseException as e: return e
    raise AssertionError('Expected failure was accepted')

def state():
    return {'binding':'1'*64,'seq':0,'head':'0'*64,'counts':{'attempt':0,'query':0,'snapshot':0,'verifier':0},
      'partitions':{'query':0,'snapshot':0,'verifier':0},'u':{},'active':None,
      'resources':{'slots':0,'holds':0,'query_holds':0,'extra_queries':0}}

def fixture(m, work, label, fault=None):
    root=work/label; root.mkdir()
    for n in ('candidate','draft','runtime'): (root/n).mkdir()
    l=m._load_launcher(); events=[]; instances=[]
    secret='REVIEW-DIAGNOSTIC-\u03bb-\x00-'+label
    status={'phase':'READY','reason':secret,'connection_epoch':23,'actual_admission':False,
      'external_nonexecution_established':False,'authorization_renewed':False}
    class Raw:
        def __init__(self,path,config,create=False,*,ownership_path):
            events.append('raw-initialize');Path(path).touch(exist_ok=False);Path(ownership_path).touch(exist_ok=False)
            if fault=='raw-init': raise ValueError(secret)
        def close(self):
            events.append('raw-close')
            if fault=='raw-close': raise OSError(secret)
    class Managed:
        def __init__(self): self.saved=state(); self.diagnostic=copy.deepcopy(status);instances.append(self)
        def state(self):
            events.append('state')
            if fault=='preflight-state': raise ValueError(secret)
            return self.saved
        def status(self):
            events.append('status')
            if fault=='preflight-status': raise ValueError(secret)
            return copy.deepcopy(self.diagnostic)
        def handle(self,packet):
            events.append(['handle',packet.hex()])
            if fault in ('backend-error','interrupt','system-exit'):
                raise {'backend-error':ValueError,'interrupt':KeyboardInterrupt,'system-exit':SystemExit}[fault](secret)
            return b'EXACT-SIGNED-APPLICATION-ERROR\x00\xff'
        def close(self):
            events.append('managed-close')
            if fault in ('managed-close','backend-and-close'): raise OSError(secret)
            self.diagnostic['phase']='CLOSED'
    def opening(*args,**kwargs):
        events.append('managed-open')
        if fault=='managed-open':raise RuntimeError(secret)
        obj=Managed()
        if fault=='backend-and-close':
            def bad(packet):raise ValueError(secret)
            obj.handle=bad
        return obj,types.SimpleNamespace(a=obj)
    # Only backend/environment seams are mocked. session/_session/ManagedSession,
    # lock, evidence writing, ACTIVE marker and cleanup are unchanged source.
    l.inputs=lambda c,d:(Path(c),Path(d));l.validate_runtime=lambda r:Path(r)
    l.environment=lambda:{'review_fixture':True};l.enforce_environment=lambda:None
    l._profile.session_frontier=lambda *a:None
    l.load_runtime=lambda c,r:(types.SimpleNamespace(Authority=Raw),opening)
    args=[str(root/n) for n in ('candidate','draft','runtime','session')]
    return types.SimpleNamespace(launcher=l,args=args,root=root,events=events,instances=instances,secret=secret,status=status)

def public(m,f,client,control=None):
    old=m._load_launcher;m._load_launcher=lambda:f.launcher
    try:
        if control is None:return m.run(*f.args,client,create=True)
        return m.run_controlled(*f.args,client,control=control,create=True)
    finally:m._load_launcher=old

def generic(m,e,label):
    need(type(e) is m.ClientFailure and e.args==('MANAGED-OPERATION-UNAVAILABLE; outcome uncertain; no renewed authorization',),label+' fixed failure')
    need(e.__cause__ is None and e.__context__ is None and not e.__dict__,label+' no diagnostic exception fields')

def record(f):
    files=list((f.root/'session/evidence').glob('failure-*'))
    need(len(files)==1,'one existing-launcher failure record '+f.root.name)
    r=json.loads(files[0].read_bytes())
    need(r['nonexecution_established'] is False and r['new_authorization'] is False,'uncertainty retained '+f.root.name)
    need((f.root/'session/ACTIVE.json').exists(),'failure ACTIVE retained '+f.root.name)
    return r

def boundary(root,work):
    m=load(root/'code/prospective_entry.py')
    need(len(m.verify_inputs(root))==37,'exact dependency verification')
    need({k for k in vars(m.Client) if not k.startswith('_')}=={'state','handle'},'only two declared client methods')
    f=fixture(m,work,'normal'); held=[];ctrl=[];captures=[]
    def control(c):
        ctrl.append(c);captures.append(c.status())
    def client(c):
        held.append(c);need(c.state()==state(),'legitimate exact state')
        result=c.state();result['counts']['attempt']=999;result['u']['nested']=[{}]
        need(c.state()==state(),'nested client mutations do not change backend state')
        need(c.handle(b'PACKET\x00\xff')==b'EXACT-SIGNED-APPLICATION-ERROR\x00\xff','exact packet and application response bytes')
        need(all(not hasattr(c,n) for n in ('status','recover','close','wrapper','managed','manager','scheduler','a','control','__dict__')),'no exposed status-capable objects')
        need(c.handle.__self__ is c and repr(c)=='<I164 general client>','bound method and repr reveal no backend')
        for fn in (lambda:copy.copy(c),lambda:copy.deepcopy(c),lambda:pickle.dumps(c)):
            need(type(failure(fn)) is TypeError,'capability cannot be copied or serialized')
        return f.instances[0]
    out,err=io.StringIO(),io.StringIO()
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err): res=public(m,f,client,control)
    need(res is None and out.getvalue()==err.getvalue()=='','no callback return/status output')
    need(captures==[f.status],'trusted evidence sink receives exact status')
    complete=json.loads((f.root/'session/BOOTSTRAP-COMPLETE.json').read_bytes())
    need(complete['status']==f.status and not (f.root/'session/ACTIVE.json').exists(),'exact launcher completion evidence and confirmed close')
    need(f.events.index('raw-initialize')<f.events.index('raw-close')<f.events.index('managed-open')<f.events.index('managed-close'),'raw-close and managed-handoff ordering')
    need(not m._OWNERS,'owner table empty after success')
    generic(m,failure(held[0].state),'expired general client');generic(m,failure(ctrl[0].status),'expired diagnostic control')
    # Retained aliases from a previous invocation cannot act on a fresh owner.
    g=fixture(m,work,'second-owner')
    def second(c):
        generic(m,failure(lambda:held[0].handle(b'old')),'old alias with new owner')
        need(c.state()==state(),'new owner unaffected by old alias')
    public(m,g,second)
    # Internal status can still be read when non-READY; this adds no evidence sink.
    g=fixture(m,work,'internal-nonready');saved=[]
    def nonready(c):
        g.instances[0].diagnostic['phase']='QUARANTINED';saved.append(c.status())
    public(m,g,lambda c:None,nonready)
    need(saved[0]['phase']=='QUARANTINED' and saved[0]['reason']==g.secret,'nonREADY exact internal diagnostics')
    # Caught client failures still poison capability and reach original evidence.
    for fault in ('backend-error','interrupt','system-exit','backend-and-close'):
        g=fixture(m,work,fault,fault);aliases=[]
        def caught(c):
            aliases.append(c);generic(m,failure(lambda:c.handle(b'x')),'dispatch '+fault)
            generic(m,failure(c.state),'postfailure dispatch '+fault)
        e=failure(lambda:public(m,g,caught));generic(m,e,'outer '+fault)
        r=record(g);need(r['message']==g.secret,'original exception message retained '+fault)
        need('managed-close' in g.events and not m._OWNERS,'cleanup and revocation '+fault)
        generic(m,failure(aliases[0].state),'postclose alias '+fault)
        if fault=='backend-and-close':need(r['cleanup']==[['managed','OSError',g.secret]],'cleanup uncertainty preserved')
    for fault in ('raw-init','raw-close','managed-open','preflight-state','preflight-status','managed-close'):
        g=fixture(m,work,fault,fault)
        e=failure(lambda:public(m,g,lambda c:None));generic(m,e,'early/close '+fault)
        r=record(g);need(r['message']==g.secret and not m._OWNERS,'original failure retained '+fault)
        need('raw-close' in g.events,'raw cleanup attempted '+fault)
    # Client and diagnostic callback failures retain original private evidence.
    for label in ('callback','diagnostic-callback','caught-then-callback'):
        g=fixture(m,work,label,'backend-error' if label=='caught-then-callback' else None)
        def bad(c):
            if label=='caught-then-callback':failure(lambda:c.handle(b'x'))
            raise LookupError('SECOND-CLIENT-DETAIL')
        e=failure(lambda:public(m,g,lambda c:None,bad) if label=='diagnostic-callback' else public(m,g,bad))
        generic(m,e,label);r=record(g)
        need('SECOND-CLIENT-DETAIL' in r['traceback'],'callback failure retained '+label)
        if label=='caught-then-callback':need(r['message']==g.secret,'original backend dominates caught then callback failure')
    # Return/input shape attacks: no object hooks, no status capability transfer.
    hooks=[]
    class Object:
        def __repr__(self):hooks.append('repr');return 'bad'
        def __deepcopy__(self,memo):hooks.append('copy');return self
    for label in ('extra-status','nested-object','dict-subclass','bytes-subclass','packet-object','null-response','cyclic-state'):
        g=fixture(m,work,label)
        def mutate(c):
            o=g.instances[0]
            if label=='extra-status':o.saved['status']=o.status()
            elif label=='nested-object':o.saved['u']['x']=Object()
            elif label=='dict-subclass':o.saved=type('DerivedDict',(dict,),{})(o.saved)
            elif label=='bytes-subclass':o.handle=lambda packet:type('DerivedBytes',(bytes,),{})(b'x')
            elif label=='null-response':o.handle=lambda packet:None
            elif label=='cyclic-state':o.saved['u']['cycle']=o.saved
        def challenge(c):
            fn=c.state if label in ('extra-status','nested-object','dict-subclass','cyclic-state') else lambda:c.handle(Object() if label=='packet-object' else b'x')
            generic(m,failure(fn),'shape '+label)
        generic(m,failure(lambda:public(m,g,challenge,mutate)),'shape outer '+label)
        record(g);need(not hooks and not m._OWNERS,'no unsafe hooks and capability revoked '+label)
    # Evidence-writing failure cannot be converted to success or imaginary evidence.
    g=fixture(m,work,'failed-evidence-write','backend-error');original=g.launcher.write_new
    def write(p,x):
        if Path(p).name.startswith('failure-'):raise OSError('EVIDENCE-SINK-FAILURE')
        return original(p,x)
    g.launcher.write_new=write
    generic(m,failure(lambda:public(m,g,lambda c:c.handle(b'x'))),'failed evidence write')
    need(not list((g.root/'session/evidence').iterdir()) and (g.root/'session/ACTIVE.json').exists(),'missing evidence remains missing and uncertainty retained')
    need('managed-close' in g.events and not m._OWNERS,'cleanup still attempted despite evidence sink failure')
    # Default CLI success/failure branch, exact retained mechanics behind stub.
    for label,fault in [('cli-success',None),('cli-failure','managed-close')]:
        g=fixture(m,work,label,fault);old=m._load_launcher;m._load_launcher=lambda:g.launcher
        argv=['initialize']+sum(([f'--{n}',v] for n,v in zip(('candidate','draft','runtime','destination'),g.args)),[])
        out,err=io.StringIO(),io.StringIO()
        try:
            with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):rc=m.main(argv)
        finally:m._load_launcher=old
        need((rc,out.getvalue(),err.getvalue())==((0,'PASS initialization and confirmed close; admission disabled\n','') if fault is None else (1,'','FAILED; outcome uncertain; admission disabled\n')),'fixed CLI text and exit '+label)
        need(g.events.count('status')==1,'CLI adds no extra status read '+label)
    out,err=io.StringIO(),io.StringIO()
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):rc=m.main(['BAD-ARG-DIAGNOSTIC'])
    need((rc,out.getvalue(),err.getvalue())==(1,'','FAILED; outcome uncertain; admission disabled\n'),'argument error is fixed non-success output')
    # Original exposure, AST-extracted old main with a no-storage stub only.
    path=root/'retained/launcher/code/lab_bootstrap.py'
    node=next(n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='main')
    @contextlib.contextmanager
    def session(*a,**kw):yield types.SimpleNamespace(status=lambda:{'reason':'OLD-STDOUT-EXPOSURE'},state=lambda:{})
    ns={'argparse':argparse,'json':json,'session':session};exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),'exec'),ns)
    prev=sys.argv;sys.argv=['old','initialize'];out=io.StringIO()
    try:
        with contextlib.redirect_stdout(out):ns['main']()
    finally:sys.argv=prev
    (work/'original-output-witness.txt').write_text(out.getvalue())
    need('OLD-STDOUT-EXPOSURE' in out.getvalue(),'original stdout exposure reproduced without backend')

def bindings(root):
    c=load(root/'code/correspondence.py');raw=(root/'provenance/status-correspondence.json').read_bytes();base=json.loads(raw)
    need(c.validate(root,raw)=={'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'actual_admission':False,'full_model_binding':False},'legitimate two-context source binding')
    # Check anchors independently of the candidate derivation helper.
    for s in base['sites']:
        a=s['anchor'];b=(root/a['path']).read_bytes()
        need(hashlib.sha256(b).hexdigest()==a['sha256'] and len(b)==a['bytes'],'independent source identity '+s['id'])
        nodes=ast.parse(b).body
        for name in a['qualified'].split('.'):
            node=next(n for n in nodes if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name);nodes=node.body
        need(ast.get_source_segment(b.decode(),node)==a['exact_source'] and [node.lineno,node.end_lineno]==[a['line'],a['end_line']],'independent anchor span '+s['id'])
    need(len(base['sites'])==19 and all(x['site_ids']==[s['id'] for s in base['sites']] for x in base['contexts']),'all 19 affected sites in both contexts')
    need([x['context'] for x in base['contexts']]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'declared context order')
    mutations=[
      ('contract',lambda x:x['contract'].update(sha256='0'*64)),
      ('coordinated-contract',lambda x:(x['contract'].update(sha256='0'*64),x['source_bindings']['contract/CONTRACT-draft-1.txt'].update(sha256='0'*64))),
      ('duplicate-context',lambda x:x['contexts'].__setitem__(1,copy.deepcopy(x['contexts'][0]))),
      ('reversed-contexts',lambda x:x['contexts'].reverse()),
      ('missing-context',lambda x:x['contexts'].pop()),
      ('site-and-both-contexts',lambda x:(x['sites'].pop(),[y['site_ids'].pop() for y in x['contexts']])),
      ('missing-relation',lambda x:x['contexts'][1]['relationships'].pop()),
      ('missing-duty',lambda x:x['contexts'][0]['inherited_requirements'].pop()),
      ('invented-ordinal',lambda x:x['contexts'][0].update(ordinal=0)),
      ('false-finite-domain',lambda x:x['contexts'][0].update(multiplicity=1,complete_symbolic_coverage=True)),
      ('false-classification',lambda x:x['contexts'][1].update(classification='PUBLIC')),
      ('missing-frames-erased',lambda x:x['occurrence_contract'].update(historical_launcher_frames='VERIFIED')),
      ('inventory-zero',lambda x:x.update(inventory_unknown_totals=0)),
      ('lifetime-zero',lambda x:x.update(lifetime_unknown_totals=0)),
      ('admission',lambda x:x['limits'].update(actual_admission=True)),
      ('final-binding',lambda x:x.update(full_model_binding=True)),
      ('policy-adoption',lambda x:x.update(profile_policy_adoption=True)),
    ]
    for name,fn in mutations:
        v=copy.deepcopy(base);fn(v);need(type(failure(lambda:c.validate(root,c.enc(v)))) is ValueError,'reject '+name)
    for raw2 in (raw[:-1],raw+b'\n',json.dumps(base,indent=2).encode(),bytearray(raw)):
        need(type(failure(lambda:c.validate(root,raw2))) is ValueError,'reject noncontract serialization/type')
    derived=c.derive(root);derived['contexts'][0]['site_ids'].reverse();derived['source_bindings'].clear();derived['limits']['actual_admission']=True
    receipt=c.validate(root,raw);receipt['contexts'].reverse();receipt['actual_admission']=True
    need(c.enc(c.derive(root))==raw and c.validate(root,raw)['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'returned nested mutations cannot change fresh expectations')

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    root=Path(a.root).resolve();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
    denied=[]
    def audit(event,args):
        if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind'):
            denied.append(event);raise AssertionError('NO DB/NETWORK OPERATIONS ALLOWED')
        if event=='open' and isinstance(args[0],(str,bytes)):
            name=os.fsdecode(args[0])
            if name.startswith('/home/steve/'):raise AssertionError('NO HOST SESSION PATHS')
            if Path(name).absolute().is_relative_to(root) and len(args)>2 and isinstance(args[2],int) and args[2] & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC):
                raise AssertionError('INPUT IS READ ONLY')
    sys.addaudithook(audit)
    env={'python':sys.version,'platform':platform.platform(),'cryptography_installed':importlib.metadata.version('cryptography'),'dont_write_bytecode':sys.dont_write_bytecode}
    try:
        boundary(root,out);n_boundary=len(CHECKS);bindings(root)
        need(not denied,'no database or network operation attempted')
        result={'result':'PASS','checks':CHECKS,'boundary_assertions':n_boundary,'binding_assertions':len(CHECKS)-n_boundary-1,'environment':env,
          'backend':'Reviewer-written stubs; unchanged retained launcher mechanics','real_session_evidence':False,'sqlite_connections':0,'host_sessions_accessed':False,'candidate_modified':False}
        (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','assertions':len(CHECKS),'boundary':n_boundary,'binding':len(CHECKS)-n_boundary-1}))
    except BaseException:
        (out/'PARTIAL.json').write_text(json.dumps({'passed':CHECKS,'environment':env,'failure':traceback.format_exc()},indent=2)+'\n');raise

if __name__=='__main__':main()
