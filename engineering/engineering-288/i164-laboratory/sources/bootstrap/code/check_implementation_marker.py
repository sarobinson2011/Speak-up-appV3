"""Focused marker repair only. Constructed metadata is explicitly not host execution."""
import importlib.util,json,sys,subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=load('old_checker',P/'failures/dependency_check-before-marker-fix.py')
new=load('new_checker',P/'code/dependency_check.py');rows=[]
def test(name,fn,reject=False):
 try:r=fn()
 except Exception as e:
  if not reject:raise
  rows.append({'name':name,'pass':True,'error':str(e)})
 else:
  assert not reject,name;rows.append({'name':name,'pass':True,'value':r})
def equals(a,b):assert a==b;return a
condition='implementation_name != "PyPy"'
test('old-exact-host-marker-reproduced',lambda:old.marker(condition),True)
test('exact-host-marker-current-interpreter',lambda:equals(new.marker(condition),sys.implementation.name!='PyPy'))
test('actual-implementation-name-equality',lambda:equals(new.marker('implementation_name == '+json.dumps(sys.implementation.name)),True))
test('false-branch-preserved',lambda:equals(new.marker('implementation_name != '+json.dumps(sys.implementation.name)),False))
test('case-preserved-not-display-name',lambda:equals(new.marker('implementation_name == "CPython"'),False))
test('existing-display-name-marker',lambda:equals(new.marker('platform_python_implementation == "CPython"'),True))
test('unknown-name-still-rejects',lambda:new.marker('unrecognized_name == "x"'),True)
test('call-still-rejects',lambda:new.marker('__import__("os")'),True)
class D:
 def __init__(self,name,version,requires):self.metadata={'Name':name};self.version=version;self.requires=requires
original=new.importlib.metadata.distributions
try:
 new.importlib.metadata.distributions=lambda:[D('cffi','2.1.1',['pycparser; '+condition]),D('pycparser','3.11',[])]
 test('exact-requirement-checked-not-skipped',lambda:equals(new.check(),[{'owner':'cffi','requirement':'pycparser; '+condition,'applicable':True,'installed':'3.11'}]))
 new.importlib.metadata.distributions=lambda:[D('cffi','2.1.1',['pycparser; '+condition])]
 test('missing-pycparser-still-rejects',new.check,True)
finally:new.importlib.metadata.distributions=original
p=subprocess.run([sys.executable,'-B','-c',"import sys;sys.path.insert(0,sys.argv[1]);import dependency_check as d;assert d.marker('implementation_name != \"PyPy\"') == (sys.implementation.name!='PyPy');print('PASS')",str(P/'code')],capture_output=True,text=True)
assert p.returncode==0,p.stderr;rows.append({'name':'fresh-process-exact-marker','pass':True})
(P/'results/marker-repair.json').write_text(json.dumps({'checks':rows,'count':len(rows),'scope':'11 fresh checker controls; original44 reused; no host or bootstrap rerun','python':sys.version,'implementation_name':sys.implementation.name},indent=2)+'\n')
print('PASS',len(rows))
