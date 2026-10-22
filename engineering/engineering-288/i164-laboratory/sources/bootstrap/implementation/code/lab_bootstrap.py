"""One-shot offline laboratory bootstrap. Trusted process/cooperative ownership only.
No socket, raw serving interface, scheduler commands or transaction signing CLI.
"""
import argparse, contextlib, copy, fcntl, hashlib, importlib.metadata, json, os
import platform, shutil, sqlite3, stat, sys, traceback
from pathlib import Path
P = Path(__file__).resolve().parents[1]
class Blocked(RuntimeError): pass
def require(ok, why):
    if not ok: raise Blocked(why)
def enc(x): return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def identity(p):
    b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p): return json.loads(Path(p).read_bytes())
def write_new(p,x):
    with open(p,'xb') as f:
        f.write(enc(x));f.flush();os.fsync(f.fileno())
def tree(root,pins):
    root=Path(root).absolute()
    require(not root.is_symlink(),'SYMLINK')
    require(root.is_dir(),'MISSING-TREE')
    allowed={str(a) for n in pins for a in Path(n).parents if str(a)!='.'}
    files=set();dirs=set()
    def inspect(directory):
        # Classify without following links or opening special files. Inspect the
        # entire layout before hashing any payload; only declared directories recurse.
        with os.scandir(directory) as entries:
            for entry in entries:
                q=Path(entry.path);name=str(q.relative_to(root))
                mode=entry.stat(follow_symlinks=False).st_mode
                require(not stat.S_ISLNK(mode),'SYMLINK')
                if stat.S_ISDIR(mode):
                    require(name in allowed,'TREE-DIRECTORIES')
                    dirs.add(name);inspect(q)
                else:
                    require(stat.S_ISREG(mode),'TREE-NONREGULAR:'+name)
                    require(name in pins,'TREE-MEMBERSHIP')
                    files.add(name)
    inspect(root)
    require(files==set(pins),'TREE-MEMBERSHIP')
    require(dirs==allowed,'TREE-DIRECTORIES')
    for n,v in pins.items():require(identity(root/n)==v,'FILE-IDENTITY:'+n)
    return root

def inputs(candidate,draft):
    c=tree(candidate,read(P/'provenance/candidate-members.json'))
    d=tree(draft,read(P/'provenance/draft-members.json'))
    return c,d

def runtime_pins():
    pins=read(P/'provenance/candidate-members.json')
    return {n:pins[src] for n,src in read(P/'provenance/runtime-layout.json').items()}
NATIVE_HELPER = 'retained-candidate/native/bin/pe-rfc8032-stream'
def validate_runtime(root):
    root=tree(root,runtime_pins())
    helper=root/NATIVE_HELPER
    require(stat.S_IMODE(helper.stat().st_mode)==0o755 and os.access(helper,os.X_OK),'NATIVE-EXECUTABLE-MODE')
    return root

def recover_runtime(candidate,draft,destination):
    c,d=inputs(candidate,draft);dest=Path(destination)
    require(not os.path.lexists(dest),'DESTINATION-EXISTS');dest.mkdir(mode=0o700)
    # Failure leaves exact copied prefix for inspection; never resume by overwrite.
    for n,src in read(P/'provenance/runtime-layout.json').items():
        q=dest/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((c/src).read_bytes())
    # Only the exact source-required native helper receives executable mode.
    # Byte identity is verified before mode establishment; never chmod candidate sources.
    tree(dest,runtime_pins())
    (dest/NATIVE_HELPER).chmod(0o755)
    validate_runtime(dest);return {'runtime':str(dest.resolve()),'files':len(runtime_pins())}

def environment():
    return {'implementation':platform.python_implementation(),'python':platform.python_version(),
      'optimize':sys.flags.optimize,'cryptography':importlib.metadata.version('cryptography'),
      'sqlite':sqlite3.sqlite_version,'executable':str(Path(sys.executable).resolve()),
      'executable_identity':identity(Path(sys.executable).resolve()),
      'distributions':{x.metadata['Name']:x.version for x in importlib.metadata.distributions()}}
def enforce_environment():
    e=environment();require(e['implementation']=='CPython' and e['python']=='3.12.14' and e['optimize']==0,'INTERPRETER')
    require(e['cryptography']=='41.0.7','CRYPTOGRAPHY-41.0.7-REQUIRED');return e

def binding(c,d,r,config):
    return {'format':'I164-LAB-BOOTSTRAP-BINDING-1','candidate_manifest':identity(P/'provenance/candidate-members.json'),
      'draft_manifest':identity(P/'provenance/draft-members.json'),'runtime_map':identity(P/'provenance/runtime-layout.json'),
      'launcher':identity(__file__),'candidate':str(c),'draft':str(d),'runtime':str(r),
      'configuration':copy.deepcopy(config),'environment':environment(),
      'assessment':'SOURCE-ONLY','actual_admission':False,'final_binding':'BLOCKED','streams':'UNCOMPUTED',
      'custody':'PUBLIC TEST KEYS; cooperative lock and trusted process only; no exclusive-custody assurance'}

def load_runtime(c,r):
    require(not any(n in sys.modules for n in ['authority','runtime','live_connection','compiler','ingest']), 'FRESH-PROCESS-REQUIRED')
    sys.path[:0]=[str(c/'compiler'),str(r/'prospective')]
    import authority
    # Verify actual runtime modules against the recovered source graph, not filenames.
    pinned=runtime_pins();allowed={(r/n).resolve():v for n,v in pinned.items()}
    for n,m in list(sys.modules.items()):
        f=getattr(m,'__file__',None)
        if f and Path(f).resolve().is_relative_to(r):
            q=Path(f).resolve();require(q in allowed and identity(q)==allowed[q],'IMPORTED-RUNTIME:'+n)
    require(identity(authority.__file__)==pinned['prospective/authority.py'],'AUTHORITY-BINDING')
    from live_connection import open_session
    return authority,open_session

@contextlib.contextmanager
def owner_lock(destination):
    dest=Path(destination).absolute();require(dest.name not in ('','.','..'),'DESTINATION')
    parent=dest.parent.resolve();require(parent.is_dir(),'MISSING-PARENT')
    dest=parent/dest.name
    fd=os.open(parent/('.'+dest.name+'.owner.lock'),os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
    try:
        try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise Blocked('OWNER-LOCK-CONTENDED')
        yield dest
    finally:os.close(fd)

class ManagedSession:
    """Deliberately no raw Authority, DB or scheduler capability in public API."""
    def __init__(self,managed):self.__managed=managed
    def status(self):return self.__managed.status()
    def state(self):return self.__managed.state()
    def handle(self,authenticated_packet):return self.__managed.handle(authenticated_packet)

@contextlib.contextmanager
def _session(candidate,draft,runtime,destination,*,create=False):
    """Private mechanics, public session() enforces the environment.
    Separate tests exercise mechanics under their explicitly recorded environment.
    Lock spans raw creation, confirmed close, managed reopening, caller handoff,
    and final managed close. Unconfirmed cleanup blocks later opening.
    """
    c,d=inputs(candidate,draft);r=validate_runtime(runtime)
    cfg=read(P/'laboratory-configuration.json');b=binding(c,d,r,cfg)
    authority,open_session=load_runtime(c,r)
    with owner_lock(destination) as dest:
        if create:
            require(not os.path.lexists(dest),'DESTINATION-EXISTS')
            dest.mkdir(mode=0o700);(dest/'state').mkdir();(dest/'evidence').mkdir()
            write_new(dest/'binding.json',b);write_new(dest/'BOOTSTRAP-STARTED.json',{'stage':'before database creation'})
        else:
            require(dest.is_dir() and not dest.is_symlink(),'MISSING-SESSION')
            require(read(dest/'binding.json')==b,'SESSION-BINDING')
            require((dest/'BOOTSTRAP-COMPLETE.json').is_file(),'PARTIAL-BOOTSTRAP')
            require(not (dest/'ACTIVE.json').exists() and not list((dest/'evidence').glob('failure-*')),'UNCERTAIN-PRIOR-OWNER')
            require(all((dest/'state'/n).is_file() and not (dest/'state'/n).is_symlink() for n in ['session.sqlite','ownership.sqlite']),'MISSING-STATE')
        db=dest/'state/session.sqlite';owners=dest/'state/ownership.sqlite';raw=None;managed=None
        write_new(dest/'ACTIVE.json',{'pid':os.getpid(),'operation':'bootstrap' if create else 'managed reopening'})
        try:
            if create:
                # Retain partially initialized raw object for cleanup. Never return it.
                raw=authority.Authority.__new__(authority.Authority)
                authority.Authority.__init__(raw,db,cfg['config'],True,ownership_path=owners)
                raw.close();raw=None
                write_new(dest/'RAW-CREATION-CLOSED.json',{'close_returned':True})
            managed,_=open_session(c,db,cfg['config'],ownership_path=owners)
            state=managed.state();status=managed.status()
            require(status['actual_admission'] is False,'ADMISSION')
            if create:
                require(state['seq']==0 and state['head']=='0'*64 and state['u']=={} and state['active'] is None,'GENESIS')
                require(all(type(v) is int and v==0 for k in ['counts','partitions','resources'] for v in state[k].values()),'GENESIS-ACCOUNTING')
                write_new(dest/'BOOTSTRAP-COMPLETE.json',{'state':state,'status':status,'raw_serving_exposed':False})
            yield ManagedSession(managed)
            managed.close();managed=None
            (dest/'ACTIVE.json').unlink()
        except BaseException as e:
            details={'error':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'nonexecution_established':False,'new_authorization':False,'cleanup':[]}
            for name,obj in [('raw',raw),('managed',managed)]:
                if obj is not None:
                    try:obj.close();details['cleanup'].append([name,'close returned'])
                    except BaseException as close_error:details['cleanup'].append([name,type(close_error).__name__,str(close_error)])
            # Preserve ACTIVE even if cleanup succeeds: interrupted ownership requires explicit recovery decision.
            try:write_new(dest/'evidence'/('failure-'+str(os.getpid())+'-'+str(len(list((dest/'evidence').iterdir())))+'.json'),details)
            except BaseException:pass
            raise

@contextlib.contextmanager
def session(*args,**kwargs):
    enforce_environment()
    with _session(*args,**kwargs) as managed:
        yield managed

def main():
    a=argparse.ArgumentParser();a.add_argument('operation',choices=['recover-runtime','initialize','check-environment']);a.add_argument('--candidate');a.add_argument('--draft');a.add_argument('--runtime');a.add_argument('--destination');args=a.parse_args()
    if args.operation=='check-environment':print(json.dumps(enforce_environment(),indent=2));return
    if args.operation=='recover-runtime':print(json.dumps(recover_runtime(args.candidate,args.draft,args.destination),indent=2));return
    enforce_environment()
    with session(args.candidate,args.draft,args.runtime,args.destination,create=True) as managed:
        print(json.dumps({'status':managed.status(),'state':managed.state(),'serving':False},indent=2))
    print('PASS bootstrap, managed validation and confirmed close; no serving process; admission disabled')
if __name__=='__main__':main()
