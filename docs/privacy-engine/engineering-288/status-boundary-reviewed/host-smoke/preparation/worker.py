"""Host-only, one disposable real-backend smoke; never execute during preparation."""
import datetime, dis, fcntl, hashlib, importlib.util, json, os
from pathlib import Path
import stat, sys, time, traceback

WORK=Path(sys.argv[2]).resolve()
ROOT=WORK/'reviewed-boundary'
EVIDENCE=WORK/'evidence'
SESSION=WORK/'disposable-session'
MODE=sys.argv[1]
DB_CALLS=[]
TRACE=[]
FRAMES={}
NEXT=1
HANDOFF=[]
FORBIDDEN=[]
EXPORTS=[]
OPCODES={}

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def need(ok,why):
    if not ok:raise RuntimeError(why)
def ident(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def write(name,value):
    raw=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    with (EVIDENCE/name).open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
def stable(path):
    s=path.lstat();need(stat.S_ISREG(s.st_mode),'NONREGULAR:'+str(path))
    with path.open('rb') as f:
        a=os.fstat(f.fileno());raw=f.read();b=os.fstat(f.fileno())
    t=path.lstat()
    key=lambda v:(v.st_dev,v.st_ino,v.st_size,v.st_mtime_ns,v.st_ctime_ns)
    need(key(s)==key(a)==key(b)==key(t),'CHANGING-FILE:'+str(path))
    return raw
def audit(event,args):
    if event in ('socket.connect','socket.bind','socket.getaddrinfo'):
        raise RuntimeError('NETWORK-FORBIDDEN')
    if event=='sqlite3.connect':
        p=Path(str(args[0])).absolute()
        need(MODE=='smoke' and p==SESSION/'state/session.sqlite','DATABASE-OUTSIDE-NEW-SMOKE')
        DB_CALLS.append({'path':str(p),'observed_at':utc()})
    if event=='open' and isinstance(args[0],(str,bytes)):
        p=Path(os.fsdecode(args[0])).absolute()
        if p.name in ('session.sqlite','ownership.sqlite'):
            need(WORK in p.parents,'EXISTING-SESSION-FILE-FORBIDDEN')
sys.addaudithook(audit)

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def snapshot(f):
    o=f.f_locals.get('self')
    if o is None:return None
    d=getattr(o,'__dict__',{})
    return {k:d[k] for k in ('_phase','_reason','_epoch','binding','ownership_binding') if k in d}

def check_handoff(cap,entry):
    # Additional explicit, read-only client invocation by the smoke observer.
    # Tracing callbacks are not recursively traced; this call has its own record.
    need(type(cap) is entry.Client,'HANDOFF-CLIENT-TYPE')
    public=sorted(n for n in vars(type(cap)) if not n.startswith('_'))
    need(public==['handle','state'],'CLIENT-PUBLIC-SURFACE')
    absent=['status','recover','close','manager','managed','wrapper','scheduler','a','control','__dict__']
    need(all(not hasattr(cap,n) for n in absent),'CLIENT-CAPABILITY-EXPOSURE')
    need(cap.handle.__self__ is cap and cap.state.__self__ is cap,'BOUND-METHOD-RECEIVER')
    before=utc();state=cap.state();after=utc()
    need(type(state) is dict and state['seq']==0 and state['head']=='0'*64 and state['u']=={} and state['active'] is None,'FRESH-STATE')
    need(all(type(v) is int and v==0 for k in ('counts','partitions','resources') for v in state[k].values()),'FRESH-ACCOUNTING')
    HANDOFF.append({'observed_before':before,'observed_after':after,'public_methods':public,'absent_attributes':absent,
                    'state':state,'request_issued':False,'observer_call_site':'worker.py:check_handoff -> Client.state',
                    'trace_limitation':'State call made inside observer; not represented as recursively traced frames'})
    need(len(HANDOFF)==1,'MULTIPLE-HANDOFFS')

def smoke(entry,launcher):
    watched={
      str(ROOT/'code/prospective_entry.py'):{'main','run','_run','Client.__init__','<lambda>'},
      str(ROOT/'retained/launcher/code/lab_bootstrap.py'):{'_session','session','ManagedSession.status'},
      str(WORK/'candidate/compiler/live_connection.py'):{'open_session','ManagedAuthority.__init__','ManagedAuthority.recover','ManagedAuthority.status','ManagedAuthority._validate','ManagedAuthority.close'},
      str(WORK/'runtime/prospective/authority.py'):{'Authority.__init__','Authority.close'},
    }
    manager=str(WORK/'candidate/compiler/live_connection.py')
    authority=str(WORK/'runtime/prospective/authority.py')
    def observer(f,event,arg):
        global NEXT
        path=f.f_code.co_filename;name=f.f_code.co_qualname
        if event=='call':
            if ((path==manager and name=='ManagedAuthority.handle') or
                (path==authority and name in ('Authority.handle','Authority.sign','Scheduler.packet','Scheduler.call')) or
                (Path(path).name=='lab_evm.py' and f.f_code.co_name=='tx')):
                FORBIDDEN.append({'path':path,'function':name});raise RuntimeError('REQUEST-OR-TX-FORBIDDEN')
            if path==authority and name=='Authority.__init__':
                need(Path(f.f_locals['path']).resolve()==SESSION/'state/session.sqlite','AUTHORITY-PATH')
                need(Path(f.f_locals['ownership_path']).resolve()==SESSION/'state/ownership.sqlite','OWNERSHIP-PATH')
        matched=path in watched and (name in watched[path] or (path==str(ROOT/'code/prospective_entry.py') and f.f_code.co_name=='<lambda>'))
        if not matched:return observer
        if event not in ('call','return','exception'):return observer
        resumed=event=='call' and id(f) in FRAMES
        if event=='call' and not resumed:FRAMES[id(f)]=NEXT;NEXT+=1
        parent=f.f_back
        while parent is not None and id(parent) not in FRAMES:parent=parent.f_back
        row={'seq':len(TRACE),'observed_at':utc(),'monotonic_ns':time.monotonic_ns(),'frame':FRAMES.get(id(f)),
             'parent':None if parent is None else FRAMES[id(parent)],'path':path,'function':name,'line':f.f_lineno,'event':event,'resumed_generator':resumed,'state':snapshot(f)}
        if event=='return':
            ops=OPCODES.setdefault(f.f_code,{i.offset:i.opname for i in dis.get_instructions(f.f_code,show_caches=True)})
            row['opcode']=ops.get(f.f_lasti);row['normal_return']=row['opcode'] in ('RETURN_VALUE','RETURN_CONST')
            if name in ('ManagedAuthority.status','ManagedAuthority.recover','main'):row['value']=arg
            if name=='ManagedAuthority._validate' and row['normal_return']:
                EXPORTS.append(f.f_locals['x'])
        if event=='exception':row['exception']={'type':arg[0].__name__,'message':str(arg[1])}
        TRACE.append(row)
        if event=='call' and path==str(ROOT/'code/prospective_entry.py') and f.f_code.co_name=='<lambda>':
            check_handoff(f.f_locals['client'],entry)
        if event=='return' and row.get('normal_return'):FRAMES.pop(id(f),None)
        return observer
    need(not SESSION.exists(),'DESTINATION-EXISTS')
    write('SMOKE-ABOUT-TO-START.json',{'observed_at':utc(),'destination':str(SESSION),'entry':ident(stable(ROOT/'code/prospective_entry.py')),
           'requests_authorized':False,'transactions_authorized':False,'one_initialization_only':True,
           'instrumentation':'Read-only trace plus one explicit Client.state call at actual CLI lambda handoff; no monkeypatching/stubs'})
    sys.settrace(observer)
    try:
        code=entry.main(['initialize','--candidate',str(WORK/'candidate'),'--draft',str(WORK/'draft'),'--runtime',str(WORK/'runtime'),'--destination',str(SESSION)])
    finally:
        sys.settrace(None)
        write('execution-trace.json',{'format':'I164-STATUS-SMOKE-OBSERVATION-1','events':TRACE,'history_claim':'This execution only; no historical launcher-frame reconstruction'})
        write('client-handoff.json',HANDOFF)
        write('database-open-observations.json',DB_CALLS)
        write('forbidden-call-observations.json',FORBIDDEN)
        for i,x in enumerate(EXPORTS):write('recovery-export-'+str(i)+'.json',x)
    need(code==0 and len(HANDOFF)==1 and not FORBIDDEN,'SMOKE-DISPOSITION')
    need(len(EXPORTS)==1,'RECOVERY-EXPORT-COUNT')
    closes=[x for x in TRACE if x['function']=='ManagedAuthority.close' and x['event']=='return' and x.get('normal_return')]
    need(len(closes)==1 and closes[0]['state']['_phase']=='CLOSED','CONFIRMED-MANAGED-CLOSE')
    need(not any(x['event']=='exception' for x in TRACE),'OBSERVED-EXCEPTION')
    need(not entry._OWNERS,'UNREVOKED-CLIENT-CAPABILITY')
    lock=WORK/('.'+SESSION.name+'.owner.lock')
    need(stat.S_ISREG(lock.lstat().st_mode),'MISSING-OWNER-LOCK')
    fd=os.open(lock,os.O_RDWR|os.O_NOFOLLOW)
    try:
        fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not (SESSION/'ACTIVE.json').exists() and not list((SESSION/'evidence').iterdir()),'UNCERTAIN-CLOSE-MARKERS')
        need({p.name for p in (SESSION/'state').iterdir()}=={'session.sqlite','ownership.sqlite'},'UNEXPECTED-DATABASE-SIDECAR')
        before={}
        for n in ('binding.json','BOOTSTRAP-COMPLETE.json','BOOTSTRAP-STARTED.json','RAW-CREATION-CLOSED.json','state/session.sqlite','state/ownership.sqlite'):
            raw=stable(SESSION/n);before[n]=ident(raw)
            target=EVIDENCE/'session-records'/n;target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        after={n:ident(stable(SESSION/n)) for n in before}
        need(before==after,'CHANGING-CLOSED-FILES')
        binding=json.loads(stable(SESSION/'binding.json'))
        complete=json.loads(stable(SESSION/'BOOTSTRAP-COMPLETE.json'))
        cfg=json.loads(stable(ROOT/'retained/launcher/laboratory-configuration.json'))
        need(binding['configuration']==cfg and binding['launcher']==ident(stable(ROOT/'retained/launcher/code/lab_bootstrap.py')),'SAVED-BINDING')
        need(complete['state']==HANDOFF[0]['state'] and complete['status']['phase']=='READY','COMPLETION-HANDOFF')
        write('confirmed-close.json',{'observed_at':utc(),'normal_close_event':closes[0],'active_marker_absent':True,'failure_records_absent':True,
             'cooperative_lock_reacquired':True,'before':before,'after':after,'real_storage_durability':'UNESTABLISHED'})
    finally:os.close(fd)
    x=EXPORTS[0]
    rows={k:len(x[k]) for k in ('events','blobs','journal','owners')}
    need(all(v==0 for v in rows.values()),'UNEXPECTED-FRESH-ROWS')
    write('smoke-result.json',{'result':'PASS','observed_at':utc(),'rows_from_actual_recovery_export':rows,'config':x['config'],
         'head':x['head'],'ownership_meta':x['ownership_meta'],'state':HANDOFF[0]['state'],'actual_sqlite_opens':len(DB_CALLS),
         'requests_issued':0,'transactions_signed_or_submitted':0,'service_started':False,'actual_admission':False,
         'scope':'One instrumented fresh disposable bootstrap/handoff/clean-close; not request/signing/lifecycle qualification'})

def main():
    need(MODE in ('preflight','smoke'),'MODE')
    entry=load(ROOT/'code/prospective_entry.py','i164_smoke_entry')
    launcher=entry._load_launcher()
    if MODE=='preflight':
        environment=launcher.enforce_environment()
        write('environment-preflight.json',{'observed_at':utc(),'environment':environment,'guard':'Exact reviewed guard, including installed RECORD checks','db_calls':DB_CALLS})
    else:
        # Source recovery only, before any runtime/database import. Never reuse an old runtime.
        need(not (WORK/'runtime').exists(),'RUNTIME-EXISTS')
        launcher.enforce_environment()
        result=launcher.recover_runtime(WORK/'candidate',WORK/'draft',WORK/'runtime')
        write('source-preflight.json',{'observed_at':utc(),'candidate':str(WORK/'candidate'),'draft':str(WORK/'draft'),'runtime':result,
              'counts':{'candidate':666,'draft':163,'runtime':93},'complete_tests_or_reviews_rerun':False})
        smoke(entry,launcher)

if __name__=='__main__':
    try:main()
    except BaseException as e:
        write('worker-failure-'+MODE+'.json',{'observed_at':utc(),'error':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),
              'nonexecution_established':False,'retry_authorized':False,'workspace_preserved':str(WORK)})
        raise SystemExit(1)
