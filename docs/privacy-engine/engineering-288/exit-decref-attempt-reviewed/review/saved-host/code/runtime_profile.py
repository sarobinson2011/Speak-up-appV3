"""Read-only development-runtime profile. No candidate/application imports."""
from pathlib import Path
import sys,sysconfig,platform,struct,json,hashlib,importlib.metadata,importlib.util
def identity(p):
 h=hashlib.sha256();size=0
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);size+=len(b)
 return {'bytes':size,'sha256':h.hexdigest()}
def capture(harness):
 harness=Path(harness);headers={}
 for n in ('Python.h','pystate.h','cpython/pystate.h','ceval.h','cpython/ceval.h','frameobject.h','pyframe.h','pyconfig.h'):
  p=Path(sysconfig.get_path('include'))/n;headers[n]=identity(p) if p.is_file() else None
 deps={};dependency_roots=[]
 for name in ('cryptography','cffi','pycparser'):
  try:
   d=importlib.metadata.distribution(name);files={};dependency_roots.append(str(Path(d.locate_file('')).resolve()))
   for f in d.files or []:
    s=str(f)
    if s.endswith(('.pyc','/RECORD','/INSTALLER','/REQUESTED','/direct_url.json')) or '__pycache__' in s or s.startswith('../'):continue
    p=Path(d.locate_file(f))
    if p.is_file():files[s]=identity(p)
   deps[name]={'version':d.version,'files':files}
  except importlib.metadata.PackageNotFoundError:deps[name]=None
 lib=Path(sysconfig.get_config_var('LIBDIR') or '')/(sysconfig.get_config_var('LDLIBRARY') or '')
 native=harness/'_event_filter.cpython-312-x86_64-linux-gnu.so'
 return {'python':sys.version,'implementation':sys.implementation.name,'version':list(sys.version_info[:3]),'sys_platform':sys.platform,'machine':platform.machine(),'bits':struct.calcsize('P')*8,'byteorder':sys.byteorder,'SOABI':sysconfig.get_config_var('SOABI'),'EXT_SUFFIX':sysconfig.get_config_var('EXT_SUFFIX'),'Py_DEBUG':sysconfig.get_config_var('Py_DEBUG'),'Py_TRACE_REFS':sysconfig.get_config_var('Py_TRACE_REFS'),'isolated':sys.flags.isolated,'dont_write_bytecode':sys.dont_write_bytecode,'optimization':sys.flags.optimize,'executable_identity':identity(Path(sys.executable).resolve()),'libpython_identity':identity(lib) if lib.is_file() else None,'headers':headers,'dependencies':deps,'native':identity(native),'observation_only':{'executable':sys.executable,'libpython':str(lib),'libc':platform.libc_ver(),'kernel':platform.release(),'dependency_roots':dependency_roots}}
def comparable(v):return {k:x for k,x in v.items() if k!='observation_only'}
def differences(expected,actual,path=''):
 out=[]
 if type(expected) is dict and type(actual) is dict:
  for k in sorted(set(expected)|set(actual)):
   if k not in expected or k not in actual:out.append(path+'/'+k)
   else:out.extend(differences(expected[k],actual[k],path+'/'+k))
 elif type(expected) is not type(actual) or expected!=actual:out.append(path)
 return out
def check(harness,expected):
 actual=capture(harness);diff=differences(comparable(expected),comparable(actual));load={'attempted':False}
 paths=[sys.executable,sys.prefix,sys.base_prefix,str(harness),*sysconfig.get_paths().values(),*actual['observation_only']['dependency_roots']]
 blocked=sorted({str(Path(p).resolve()) for p in paths if str(Path(p).resolve()).startswith('/home/steve/')})
 if blocked:diff.append('UNCHANGED-HARNESS-PROHIBITED-HOST-PATH')
 if not diff:
  p=Path(harness)/'_event_filter.cpython-312-x86_64-linux-gnu.so'
  try:
   s=importlib.util.spec_from_file_location('_event_filter',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
   load={'attempted':True,'loaded':True,'install_stop_callable':callable(m.install) and callable(m.stop),'observer_installed':False}
  except BaseException as e:load={'attempted':True,'loaded':False,'error':type(e).__name__+': '+str(e)}
 return {'actual':actual,'prohibited_host_paths':blocked,'differences':diff,'native_load':load,'matches':not diff and load.get('install_stop_callable') is True,'host_qualification':'Exact captured profile only; different bytes require separate qualification, not an automatic rebuild or override'}
if __name__=='__main__':
 if len(sys.argv)==2:print(json.dumps(capture(sys.argv[1]),sort_keys=True))
 else:
  out=check(sys.argv[1],json.loads(Path(sys.argv[2]).read_bytes()));print(json.dumps(out,sort_keys=True));raise SystemExit(0 if out['matches'] else 2)
