"""Preparation-only byte assembly, no candidate/application imports."""
from pathlib import Path
import json,hashlib,zipfile,importlib.util,traceback,datetime,time
B=Path(__file__).resolve().parent;H=B/'parent-host';C=B/'candidate';start=time.monotonic()
def load(n):
 s=importlib.util.spec_from_file_location('_prepare_'+n,H/'code'/(n+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def save(n,v):
 p=B/n
 with p.open('x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n')
try:
 common=load('common_r1');recovery=load('recovery');plan=json.loads((H/'PLAN.json').read_bytes())
 archive=B/'intake/I164-helper-open-persistent-host-launcher-review-2.zip'
 assert common.identity(archive)==plan['launcher_archive']
 with zipfile.ZipFile(archive) as z:
  m=json.loads(z.read('MANIFEST.json'));assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(m)|{'MANIFEST.json'}
  for n in z.namelist():
   if n=='MANIFEST.json':continue
   raw=z.read(n);assert recovery.identity(raw)==m[n],n
   if n in ('inputs/prerun.zip','inputs/progress.zip'):
    p=B/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 r=recovery.recover(B/'inputs/prerun.zip',B/'inputs/progress.zip',B/'recovered-helper')
 (C/'retained').mkdir();res=C/'retained/res-null'
 common.unzip(H/'inputs/I164-res-null-test-1-source.zip',res,plan['source_archive'])
 (res/'retained').mkdir();fast=res/'retained/fast';common.unzip(H/'inputs/I164-decref-fast-completion-1-source.zip',fast,plan['fast_source_archive'])
 (fast/'retained').mkdir();decref=fast/'retained/decref';common.unzip(H/'inputs/I164-enter-decref-attempt-1-source.zip',decref,plan['decref_source_archive'])
 (decref/'retained').mkdir();ret=decref/'retained/return';common.unzip(H/'inputs/I164-enter-return-res-1-source.zip',ret,plan['return_source_archive'])
 (ret/'retained').mkdir();enter=ret/'retained/enter';common.unzip(H/'inputs/I164-enter-call-attempt-1-source.zip',enter,plan['enter_source_archive'])
 (enter/'retained').mkdir();lookup=enter/'retained/lookup';common.unzip(enter/'reference/lookup/I164-context-special-lookup-1-source.zip',lookup,plan['lookup_source_archive'])
 (lookup/'retained').mkdir();r1=lookup/'retained/r1';common.unzip(lookup/'reference/r1/I164-open-return-reconstruction-1-source.zip',r1,plan['r1_source_archive'])
 (r1/'retained').mkdir();(B/'recovered-helper/candidate').rename(r1/'retained/helper-open')
 checks={}
 for name,path,count,dirs in [('R1',r1,4090,1142),('LOOKUP',lookup,4124,1155),('ENTER',enter,4169,1169),('RETURN',ret,4222,1183),('DECREF',decref,4271,1197),('FAST',fast,4500,1216),('RES-NULL',res,4729,1238)]:
  manifest=(C/'reference/res-null/ASSEMBLED-ROOT-MANIFEST.json') if name=='RES-NULL' else H/'expected'/(name+'-ROOT-MANIFEST.json')
  checks[name]=common.exact_tree(path,json.loads(manifest.read_bytes()));assert checks[name]['files']==count and checks[name]['directories']==dirs
  print(json.dumps({'event':'assembled-exact-root','root':name,**checks[name]}),flush=True)
 assert common.identity(C/'reference/res-null/actual-receipt.json')=={'bytes':19046155,'sha256':'1fbbea61a963361dd0369aefa97f6b2954bc9a5099dd891fbc02e9f239620e6e'}
 assert (C/'reference/res-null/actual-receipt.json').read_bytes()==(H/'validation/results/actual-derived-receipt.json').read_bytes()
 m={p.relative_to(C).as_posix():common.identity(p) for p in sorted(C.rglob('*')) if p.is_file()}
 save('ASSEMBLED-ROOT-MANIFEST.json',m);checks['NEW']=common.exact_tree(C,m)
 recovery.verify_harness(H/'observer-reference');save('byte-recovery-result.json',{'result':'PASS','roots':checks,'parent_manifest':common.identity(C/'reference/res-null/ASSEMBLED-ROOT-MANIFEST.json'),'parent_receipt':common.identity(C/'reference/res-null/actual-receipt.json'),'actual_saved_parent_receipt_equal':True,'application_imports':0,'candidate_authentication_calls':0})
 save('byte-recovery-exit.json',{'exit':0,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-start})
except BaseException as e:
 save('byte-recovery-failure.json',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()});save('byte-recovery-exit.json',{'exit':1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-start});raise
