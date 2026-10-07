"""Durable staged collector. Strict exact input rechecks on every new invocation.

Large crypto retains prefix replay. Stage reuse saves computation, not the I/O
needed to establish immutable byte identity in ordinary filesystem storage.
"""
import json,time,fcntl,os,tempfile,math
from pathlib import Path
from .state import ACTIVE,Scheduler,sha
from integrated_auth.collector import run as collect,implementation
from v4_ingest.records import parse,require,ValidationError
from admission_kernel.failures import Failures,ORDER

def identities(manifest,trusted,root,key,handles,tick=None):
 from metadata_catalog.core import temporary
 from metadata_catalog.adapters import resolve,binding,MARK
 from semantic_stream.storage import ACTIVE
 from integrated_auth.adapters import checked_path
 with manifest.open('rb') as f:raw=f.read(16*1024*1024+1)
 require(len(raw)<=16*1024*1024,'carrier capability',category='INCOMPLETE-EVIDENCE-UNIVERSE');m=parse(raw)
 catalog_errors=[]
 root.mkdir(parents=True,exist_ok=True);files=temporary(root,'inputs-');handles.append(files)
 def parts():
  with trusted.open('rb') as f:
   while b:=f.read(65536):yield b
 external=any(set(m[n])=={MARK} for n in ('materials','source_objects')) or set(m['request']['occurrence_bindings'])=={MARK}
 t=parse(ACTIVE.get().write(parts())) if external else {'occurrence_bindings':{}}
 bound=binding(m,t) if external else {};job={'manifest':sha(manifest),'trusted':sha(trusted),'implementation':implementation()}
 def add(e):
  path=str(checked_path(manifest.parent,e))
  require(path not in files or files[path]==e['sha256'],'conflicting input identity',category='INVALID-EVIDENCE-DIGEST');files[path]=e['sha256']
 for name in ('materials','source_objects'):
  value=m[name]
  if set(value)=={MARK}:add(value[MARK])
  try:entries=resolve(value,name,bound,manifest.parent,root,key,job,handles,tick)
  except __import__('integrated_auth.collector',fromlist=['Paused']).Paused:raise
  except (ValueError,OSError) as error:catalog_errors.append(error);entries={}
  for e in entries.values():add(e)
 for value in (m['request']['occurrence_bindings'],t['occurrence_bindings']):
  if set(value)=={MARK}:add(value[MARK])
 for e in m['records'].values():add(e)
 for e in (m['model'],m['contract']):add(e)
 for item in m['bundles'].values():
  for e in item['files'].values():add(e)
 files[str(trusted)]=sha(trusted);files[str(manifest)]=sha(manifest);files.commit()
 return m,files,catalog_errors

def _run(manifest,trusted_path,checkpoint,key_path,*,resume=False,new_bytes=67108864,seconds=50,chunk_bytes=65536,progress=None,fault=None,quanta=1,auth_new_bytes=None):
 began=time.monotonic();require(0<seconds and math.isfinite(seconds) and type(quanta) is int and 1<=quanta<=1000000,'finite scheduler limits')
 require(auth_new_bytes is None or type(auth_new_bytes) is int and auth_new_bytes>0,'auth byte budget')
 manifest=Path(manifest).resolve();trusted=Path(trusted_path).resolve();ck=Path(checkpoint).resolve();ck.parent.mkdir(parents=True,exist_ok=True)
 require(resume or not ck.exists(),'existing journal requires resume');require(not resume or ck.exists(),'resume journal missing')
 from link_recovery.cli import read_key
 from metadata_catalog.core import temporary
 from semantic_stream.storage import ACTIVE as STORE
 handles=STORE.get().docs
 def remaining():
  if time.monotonic()-began>=seconds:
   from integrated_auth.collector import Paused
   raise Paused()
 # Publish the small job identity before directory construction, so an early
 # pause has a valid resume target. No completed-stage/authentication claim.
 from integrated_auth.collector import journal
 from link_recovery.cli import atomic_save
 job_binding={'manifest_path':str(manifest),'manifest_sha256':sha(manifest),'trusted_path':str(trusted),'trusted_sha256':sha(trusted),'implementation':implementation()}
 key=read_key(key_path);initial=journal(ck,key,job_binding)
 if not ck.exists():atomic_save(ck,initial,key)
 m,files,catalog_errors=identities(manifest,trusted,Path(str(ck)+'.inputs'),key,handles,remaining)
 binding={'manifest':{'path':str(manifest),'sha256':files[str(manifest)]},'trusted':{'path':str(trusted),'sha256':files[str(trusted)]},'implementation':implementation()}
 with open(str(ck)+'.schedule.lock','a+b') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  scheduler=Scheduler(ck,key_path,binding,progress,fault,began+seconds,auth_new_bytes);token=ACTIVE.set(scheduler)
  try:
   changed_input=None
   terminal=scheduler.read('ordered-ledger')
   if catalog_errors:terminal=None
   if terminal is not None:
    require(terminal['inputs']=={'files':files} and terminal['complete'],'incompatible/incomplete terminal receipt')
    # Verify receipt prerequisite graph too; a missing/corrupt prerequisite is
    # not replaced by the terminal PASS. Recursively all saved receipts are MACed.
    for path,h in terminal['artifacts'].items():scheduler.verify(path,h)
    for label,expected in terminal['prerequisites'].items():
     p=scheduler.read(label);require(p is not None and scheduler.receipts[label]==expected and p['complete'],'missing/stale prerequisite receipt')
     for path,h in p['artifacts'].items():scheduler.verify(path,h)
     for path,h in p['inputs'].get('files',{}).items():
      if path not in files:scheduler.verify(path,h)
    # Exact full hashes before any terminal result reuse. Quiescent inputs and
    # trusted executor custody during this call are explicit, not permissions.
    try:
     for path,h in files.items():scheduler.verify(path,h)
    except __import__('integrated_auth.collector',fromlist=['Paused']).Paused:raise
    except (ValueError,OSError) as e:
     changed_input=e
     # Collect independent errors afresh; cached stages also recheck their own
     # inputs, so a changed file cannot inherit a prior authentication result.
     terminal=None
    if terminal is not None:
     result_path=scheduler.root/terminal['result']['output']
     require(result_path.parent==scheduler.root and str(result_path) in terminal['artifacts'],'ledger output containment')
     with result_path.open('rb') as f:out=json.load(f)
     scheduler.event('ordered-ledger','REUSED-AFTER-EXACT-INPUT-AND-PREREQUISITE-CHECKS')
     out['stage_schedule']={'events':scheduler.events,'identity_bytes_reread':scheduler.reread,'terminal_reused':True,'source_qualification_established':False};return out
   for quantum in range(quanta):
    remaining=seconds-(time.monotonic()-began)
    if remaining<=0:
     if quantum:break
     from integrated_auth.collector import Paused
     raise Paused()
    scheduler.event('collector-quantum','START',quantum=quantum+1)
    out=collect(manifest,trusted,ck,key_path,resume=True,new_bytes=new_bytes,seconds=remaining,chunk_bytes=chunk_bytes,progress=progress)
    if out['processing_complete']:break
   if changed_input is not None or catalog_errors:
    f=Failures()
    for code,why in out['reasons'].items():
     for detail in why:f.add(code,detail)
    for error in catalog_errors+([changed_input] if changed_input is not None else []):f.add(getattr(error,'category','MISSING-EVIDENCE'),'changed bound scheduler input: '+str(error))
    verdict=f.result(out['mode']);out.update({k:verdict[k] for k in ('result','failures','reasons','earliest_failure')})
    if out.get('bindings'):
     out['bindings']['computed_dispositions']={k:'NOT-ESTABLISHED' for k in out['bindings'].get('computed_dispositions',{})};out['bindings']['computed_budgets']={}
     sv=out['bindings'].get('scope_validation',{});sv.update(conditional_checks_pass=False,ready=False,qualification='NOT-ESTABLISHED')
     for scope in sv.get('scopes',{}).values():scope.update(ready=False,qualification='NOT-ESTABLISHED')
    if not out['processing_complete']:out['result']='PAUSED'
   if out['processing_complete']:
    # Successful collection or final rejection is a derived computation only.
    # Preserve exact ordered failures, not a caller/issuer summary.
    prereqs=temporary(scheduler.root,'prerequisites-');scheduler.handles.append(prereqs)
    for label,h in scheduler.receipts.items():
     if label!='ordered-ledger' and scheduler.read(label)['complete']:prereqs[label]=h
    prereqs.commit()
    path=scheduler.root/'ledger-output.json';tmp=path.with_suffix('.part')
    with tmp.open('w') as f:json.dump(out,f,sort_keys=True,separators=(',',':'));f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
    from link_recovery.cli import fsync_dir
    fsync_dir(path.parent)
    scheduler.save('ordered-ledger',{'files':files},{'output':path.name},True,prereqs,{str(path):sha(path),str(ck):sha(ck)})
   out['stage_schedule']={'events':scheduler.events,'identity_bytes_reread':scheduler.reread,'terminal_reused':False,'source_qualification_established':False}
   return out
  finally:ACTIVE.reset(token);scheduler.close()

def run(*args,**kwargs):
 from semantic_stream.storage import Store,ACTIVE as STORE
 store=Store();token=STORE.set(store)
 try:
  ck=Path(args[2] if len(args)>2 else kwargs['checkpoint']);ck.parent.mkdir(parents=True,exist_ok=True)
  with open(str(ck)+'.catalog.lock','a+b') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
   return _run(*args,**kwargs)
 finally:STORE.reset(token);store.close()
