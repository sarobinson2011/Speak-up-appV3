import sys,json,subprocess,shutil,stat,os,tempfile
from pathlib import Path
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'implementation/code'));import lab_bootstrap as b
from dependency_check import marker,compare,check
from lock_contract import parse_lock
from derive_draft import derive
out=P/'results/harness';out.mkdir();rows=[]
def case(name,fn,reject=False):
 try:fn()
 except Exception as e:
  if not reject:raise
  rows.append({'name':name,'pass':True,'rejected':type(e).__name__+':'+str(e)})
 else:
  assert not reject,name;rows.append({'name':name,'pass':True})
def require(x):assert x
case('numeric-version-order',lambda:require(compare('3.12','3.9','>') and compare('41.0.7','41.0.7','==')))
case('runtime-marker',lambda:require(marker('platform_python_implementation != "PyPy"')))
case('no-unrequested-extra',lambda:require(not marker('extra == "docs"')))
case('marker-unknown-fails',lambda:marker('unknown == "x"'),True)
case('marker-call-fails',lambda:marker('__import__("os")'),True)
case('unsupported-version-fails',lambda:compare('1.dev0','1','=='),True)
# Isolate installed-metadata checker with source-shaped fixture distributions, never fake host success.
import dependency_check as dep
class D:
 def __init__(self,n,v,req):self.metadata={'Name':n};self.version=v;self.requires=req
orig=dep.importlib.metadata.distributions
for label,fixtures,reject in [('valid',[D('cryptography','41.0.7',['cffi>=1.12; platform_python_implementation != "PyPy"','sphinx>=5.3.0; extra == "docs"']),D('cffi','2.1.1',['pycparser']),D('pycparser','3.11',[])],False),('missing',[D('cryptography','41.0.7',['cffi>=1.12'])],True),('wrong-version',[D('cryptography','41.0.7',['cffi>=1.12']),D('cffi','1.0',[])],True),('unsupported',[D('cryptography','41.0.7',['cffi~=1.12']),D('cffi','2.1.1',[])],True)]:
 dep.importlib.metadata.distributions=lambda:fixtures
 case('metadata-'+label,check,reject)
dep.importlib.metadata.distributions=orig
# Exact lock pin is verified before this parser is used by Ubuntu probe.
raw=(P/'provenance/host-addendum/requirements.lock').read_bytes()
case('exact-host-lock-identity',lambda:require(b.identity(P/'provenance/host-addendum/requirements.lock')=={'bytes':11173,'sha256':'93c41e8b77049d05a764127cad3b3d42832810e7742a14f3537c3f0e5ac4fa50'}))
case('repeated-hash-rejects',lambda:parse_lock('a==1 --hash=sha256:'+'0'*64+' --hash=sha256:'+'0'*64),True)
x=b.read(P/'provenance/local-inputs.json');r=Path(b.read(P/'results/fresh/results.json')['temporary_root'])/'runtime';t=Path(tempfile.mkdtemp(prefix='i164-BR-adjacent-'))
shutil.copytree(r,t/'runtime');rr=t/'runtime';helper=rr/b.NATIVE_HELPER
helper.chmod(0o4755);case('special-mode-refused',lambda:b.validate_runtime(rr),True)
helper.chmod(0o755);original=helper.read_bytes();helper.write_bytes(original+b'x')
case('changed-helper-content-refused',lambda:b.validate_runtime(rr),True)
p=subprocess.run([sys.executable,'-B',str(P/'code/native_probe.py'),str(rr),str(P/'provenance/review/results/BR-02.json')],capture_output=True,text=True)
(out/'changed-helper-primitive.log').write_text(p.stdout+p.stderr);case('unchanged-provider-hash-gate',lambda:require(p.returncode!=0 and 'BACKEND-IDENTITY' in p.stderr))
helper.write_bytes(original);helper.unlink();helper.symlink_to(r/b.NATIVE_HELPER);case('helper-symlink-refused',lambda:b.validate_runtime(rr),True)
# Public host probe in this environment must stop before runtime/DBs; no dependency gate mocking.
cmd=[sys.executable,'-B',str(P/'code/ubuntu_verify.py'),'--package',str(P/'implementation'),'--candidate',x['candidate'],'--draft',x['draft'],'--environment-record',str(t/'missing-env'),'--lock',str(P/'provenance/host-addendum/requirements.lock'),'--compatibility-record',str(t/'missing-compat')]
p=subprocess.run(cmd,capture_output=True,text=True);(out/'missing-host-record.log').write_text(p.stdout+p.stderr)
case('missing-original-host-record-refused',lambda:require(p.returncode!=0 and 'MISSING-ORIGINAL-RECORD' in p.stderr))
# Full public environment gate also still rejects the available crypto version.
case('public-environment-still-enforced',b.enforce_environment,True)
(out/'results.json').write_bytes(b.enc({'checks':rows,'count':len(rows),'metadata_fixtures':'constructed controls only; not installed-host metadata claims'}));print('PASS',len(rows))
