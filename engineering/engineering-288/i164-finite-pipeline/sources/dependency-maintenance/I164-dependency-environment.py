"""Prepared proposal: separate inventory, setup, and dependency compatibility modes."""
import argparse, hashlib, importlib.metadata, json, os, platform, shutil, stat, subprocess, sys, time, traceback, zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
OLD=Path('/home/steve/dev/Engineering-288-execution/I164-python31214-01qgue5t')
BASE=Path('/home/steve/dev/Engineering-288-execution')
PY=OLD/'venv/bin/python'
PYHASH='5ebcd7993f0e40cb4b16e15d2c4c3c343ecad419966299b8e8f6f9e6a36bf779'
RECORDS={'ENVIRONMENT-RESULT.json':(1720,'d8314be91461a8307d0ff474865ac5b1dd86712a65d44141f6fc6dc8e12b4508'),
'requirements.lock':(11173,'93c41e8b77049d05a764127cad3b3d42832810e7742a14f3537c3f0e5ac4fa50')}
WHEELS={
'cryptography-50.0.2-cp311-abi3-manylinux_2_34_x86_64.whl':'9dab55f57c74c3cad24c323bacbbd04be4705ba6eb0d92e920b1fc4837ed5079',
'cffi-2.1.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl':'c1453022f490d2459a11819d83ad1d586e9ff65a12ac3e705ffebd46d3685dcf',
'pycparser-3.11-py3-none-any.whl':'51d5a8ba2be0bbe440b99d2112604c95bbbc3c2748a64260186c541e1729cd80'}

def need(ok,label):
    if not ok: raise RuntimeError(label)
def ident(p):
    b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p): return json.loads(Path(p).read_text())
def write(p,x):
    with Path(p).open('x') as f: json.dump(x,f,indent=2);f.write('\n')
def check_originals():
    result={}
    for n,(size,digest) in RECORDS.items():
        v=ident(OLD/n);need(v=={'bytes':size,'sha256':digest},'ORIGINAL-RECORD:'+n);result[n]=v
    need(ident(PY.resolve())=={'bytes':30976376,'sha256':PYHASH},'PINNED-INTERPRETER')
    return result

def verify_tools():
    m=read(HERE/'MANIFEST.json')
    for n in ['I164-dependency-environment.py','dependency_probe.py','requirements-50.0.2.lock']:
        need(ident(HERE/n)==m[n],'DELIVERABLE-IDENTITY:'+n)

def run(args,out,name,env):
    print('RUN:',name,flush=True)
    with (out/(name+'.log')).open('x') as f:
        p=subprocess.Popen([str(x) for x in args],stdout=f,stderr=subprocess.STDOUT,env=env)
        start=time.monotonic()
        while True:
            try: rc=p.wait(timeout=30); break
            except subprocess.TimeoutExpired: print(name,round(time.monotonic()-start),'seconds; no retry',flush=True)
            except BaseException:
                p.terminate();p.wait();raise
    need(rc==0,'FAILED:'+name+'; inspect preserved log')
    return out/(name+'.log')

def wheel_check(root,python,out,env):
    wh=root/'wheelhouse';need({p.name for p in wh.iterdir()}==set(WHEELS),'WHEEL-MEMBERSHIP')
    site=Path(subprocess.check_output([str(python),'-I','-B','-c','import sysconfig; print(sysconfig.get_paths()["purelib"])'],env=env,text=True).strip())
    rows=[]
    for n,h in WHEELS.items():
        need(ident(wh/n)['sha256']==h,'WHEEL-HASH:'+n)
        with zipfile.ZipFile(wh/n) as z:
            need(z.testzip() is None,'WHEEL-CRC');count=0
            for info in z.infolist():
                path=Path(info.filename)
                need(not path.is_absolute() and '..' not in path.parts,'WHEEL-PATH')
                if info.is_dir():continue
                need('.data' not in path.parts and not any(x.endswith('.data') for x in path.parts),'UNSUPPORTED-WHEEL-LAYOUT')
                if info.filename.endswith('.dist-info/RECORD'):continue # pip regenerates this index
                target=site/path
                need(target.is_file() and not target.is_symlink(),'INSTALLED-MEMBER:'+info.filename)
                need(target.read_bytes()==z.read(info),'INSTALLED-PAYLOAD:'+info.filename);count+=1
        rows.append({'wheel':n,'sha256':h,'exact_installed_payload_files':count,'record_exception':'installer-generated RECORD; inventoried separately'})
    return rows

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('mode',choices=['inventory','setup','check']);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--environment',type=Path);a=ap.parse_args()
    out=a.output.absolute();need(out.parent.resolve()==BASE.resolve(),'OUTPUT-MUST-BE-DIRECT-CHILD-OF-PERSISTENT-WORKSPACE')
    need(not os.path.lexists(out),'OUTPUT-EXISTS');verify_tools();before=check_originals()
    out.mkdir(mode=0o700);print('PERSISTENT OUTPUT:',out,flush=True)
    env=os.environ.copy()
    for k in list(env):
        if k.startswith(('PYTHON','PIP_','UV_')):env.pop(k)
    (out/'scratch').mkdir();env.update({'TMPDIR':str(out/'scratch'),'TEMP':str(out/'scratch'),'TMP':str(out/'scratch'),'PIP_CONFIG_FILE':os.devnull,'PIP_DISABLE_PIP_VERSION_CHECK':'1'})
    result={'mode':a.mode,'scope':'PROPOSED SEPARATE DEPENDENCY BASELINE','original_records':before,'admission':False,'readiness':'BLOCKED','final_binding':'BLOCKED','streams':'UNCOMPUTED','application_compatibility':'NOT ESTABLISHED','bootstrap_gate':'UNCHANGED; 41.0.7 ONLY'}
    try:
        if a.mode=='inventory':
            need(a.environment is None,'UNEXPECTED-ENVIRONMENT')
            log=run([PY,'-I','-B',HERE/'dependency_probe.py'],out,'existing-build-inventory',env)
            result['inventory']=read(log)
        elif a.mode=='setup':
            need(a.environment is None,'UNEXPECTED-ENVIRONMENT')
            need(platform.machine()=='x86_64' and platform.system()=='Linux','HOST-PLATFORM')
            lib,ver=platform.libc_ver();need(lib=='glibc' and tuple(map(int,ver.split('.')[:2]))>=(2,34),'HOST-GLIBC')
            run([PY,'-I','-B','-m','venv','--without-pip',out/'venv'],out,'create-separate-venv',env)
            py=out/'venv/bin/python'
            run([py,'-I','-B','-m','ensurepip','--default-pip'],out,'bundled-installer',env)
            (out/'wheelhouse').mkdir()
            pip=[py,'-I','-B','-m','pip','--isolated','--disable-pip-version-check','--no-cache-dir']
            run(pip+['download','--index-url','https://pypi.org/simple','--only-binary=:all:','--no-deps','--require-hashes','-r',HERE/'requirements-50.0.2.lock','-d',out/'wheelhouse'],out,'download-three-pinned-wheels',env)
            need({p.name for p in (out/'wheelhouse').iterdir()}==set(WHEELS),'DOWNLOADED-WHEEL-MEMBERSHIP')
            for n,h in WHEELS.items():need(ident(out/'wheelhouse'/n)['sha256']==h,'DOWNLOADED-WHEEL-HASH:'+n)
            run(pip+['install','--no-index','--find-links',out/'wheelhouse','--only-binary=:all:','--no-deps','--require-hashes','-r',HERE/'requirements-50.0.2.lock'],out,'install-into-new-venv',env)
            result['wheel_payload_checks']=wheel_check(out,py,out,env)
            result['environment']=str(out)
            result['status']='SETUP COMPLETE; compatibility check not yet run'
        else:
            need(a.environment is not None,'ENVIRONMENT-REQUIRED');root=a.environment.resolve()
            need(root.parent==BASE.resolve() and root!=OLD.resolve() and root!=out,'SEPARATE-ENVIRONMENT-REQUIRED')
            setup=read(root/'RESULT.json');need(setup.get('mode')=='setup' and setup.get('status')=='SETUP COMPLETE; compatibility check not yet run','SETUP-RESULT')
            py=root/'venv/bin/python';need(ident(py.resolve())=={'bytes':30976376,'sha256':PYHASH},'ENVIRONMENT-INTERPRETER')
            result['wheel_payload_checks']=wheel_check(root,py,out,env)
            run([py,'-I','-B','-m','pip','--isolated','--disable-pip-version-check','check'],out,'dependency-compatibility',env)
            inv=read(run([py,'-I','-B',HERE/'dependency_probe.py','--probe'],out,'public-api-compatibility',env))
            need(inv['python']=='3.12.14' and inv['implementation']=='CPython' and inv['optimize']==0,'RUNTIME-VERSION')
            need({k:v['version'] for k,v in inv['packages'].items()}=={'cryptography':'50.0.2','cffi':'2.1.1','pycparser':'3.11'},'DEPENDENCY-VERSIONS')
            need(inv['cryptography_openssl']=='OpenSSL 4.0.3 29 Sep 2026','BUNDLED-OPENSSL')
            result['inventory']=inv;result['status']='PASS dependency-only compatibility; I164 compatibility remains unestablished'
        need(check_originals()==before,'ORIGINAL-IDENTITIES-CHANGED')
        if a.mode=='inventory':result['status']='PASS read-only existing-build inventory; wheel origin not authenticated'
    except BaseException as e:
        result['status']='STOP';result['failure']=repr(e)
        (out/'failure.txt').write_text(traceback.format_exc());raise
    finally:
        write(out/'RESULT.json',result)
        downloads=Path('/home/steve/Downloads');dest=downloads/(out.name+'-result.json')
        if downloads.is_dir():
            with dest.open('xb') as f:f.write((out/'RESULT.json').read_bytes())
        print('REPORT:',out/'RESULT.json',flush=True)
if __name__=='__main__':main()
