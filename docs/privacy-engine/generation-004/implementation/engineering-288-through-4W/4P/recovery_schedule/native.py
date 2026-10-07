"""Native descriptor construction from the collector's independently checked scope.

No descriptor is accepted from caller metadata. Original token order is retained;
local contiguous indexes are an order-preserving projection, not a new universe.
"""
import argparse,os,tempfile
from pathlib import Path
from link_recovery import cli as native
from v4_ingest.records import require,digest,canonical,ValidationError

def descriptor(scoped,path,phase,values=None):
 from occurrence_values.index import ExactValues
 require(phase=='STATIC-ADMISSION' or isinstance(values,ExactValues),'complete acquired owning values; no symbolic fallback',category='INCOMPLETE-EVIDENCE-UNIVERSE')
 require(2<=len(scoped.tokens)<=1000000 and len(scoped.structural)<=10000000,'native scoped index capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
 ids={t['id']:i for i,t in enumerate(scoped.tokens)};fixed=[];groups={}
 for i,t in enumerate(scoped.tokens):
  require(len(t['id'].encode('ascii'))<=1024,'native token identifier capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  if phase!='STATIC-ADMISSION':fixed.append((i,groups.setdefault(values.group(t['id']),len(groups))))
  elif not t['arbitrary']:fixed.append((i,groups.setdefault(t['symbolic_digest'],len(groups))))
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(prefix='descriptor-',dir=path.parent)
 try:
  with os.fdopen(fd,'wb') as f:
   f.write(f'LINKS {len(ids)} {len(scoped.structural)} {len(fixed)}\n'.encode())
   for t in scoped.tokens:f.write((t['id']+'\n').encode('ascii'))
   for i,g in fixed:f.write(f'{i} {g}\n'.encode())
   for a,b,r,k in sorted(scoped.structural):
    require(len(k)<=1024 and 1<=int(r)<=999999,'native relation capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
    f.write(f'{ids[a]} {ids[b]} {int(r)} {k}\n'.encode('ascii'))
   f.flush();os.fsync(f.fileno())
  h=native.sha(tmp)
  if path.exists():require(native.sha(path)==h,'substituted source-grounded descriptor',category='INVALID-EVIDENCE-DIGEST')
  else:os.replace(tmp,path);native.fsync_dir(path.parent)
  return {'sha256':h,'tokens':len(ids),'structural':len(scoped.structural),'potential':scoped.pair_count if phase=='STATIC-ADMISSION' else values.count(scoped.tokens),'model_sha256':scoped.model.digest,'phase':phase,'original_indices_sha256':digest(canonical([t['index'] for t in scoped.tokens])),'caller_descriptor_used':False,'owning_values':None if phase=='STATIC-ADMISSION' else values.binding}
 finally:Path(tmp).unlink(missing_ok=True)

def validate(adapter,scope,scoped,request,values=None):
 scheduler=adapter.scheduler;root=scheduler.root;desc=root/(scope+'.descriptor');proof=descriptor(scoped,desc,request['phase'],values)
 contract=root/(scope+'.contract');raw=canonical({'format':'CP4K-SOURCE-GROUNDED-SCOPE-1','scope':scope,'profile_digest':request['profile_digest'],'contract':adapter.m['contract'],'proof':proof})
 if contract.exists():require(contract.read_bytes()==raw,'substituted native scope contract',category='INVALID-EVIDENCE-DIGEST')
 else:
  fd,tmp=tempfile.mkstemp(prefix='scope-contract-',dir=root)
  try:
   with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
   os.replace(tmp,contract);native.fsync_dir(root)
  finally:Path(tmp).unlink(missing_ok=True)
 entry=adapter.m['bundles'][scope]['files']['links.tsv'];path=(adapter.base/entry['path']).resolve();ck=root/(scope+'.native')
 files={str(path):entry['sha256'],str(desc):proof['sha256'],str(contract):digest(raw)}
 inputs={'files':files,'scope_proof':proof,'native':native.validator_identity(),'source_closure_recomputed':True}
 def work():
  a=argparse.Namespace(operation='resume' if ck.exists() else 'start',checkpoint=ck,key=adapter.key_path,input=None if ck.exists() else path,input_sha256=None if ck.exists() else entry['sha256'],model=None if ck.exists() else desc,model_sha256=None if ck.exists() else proof['sha256'],contract=None if ck.exists() else contract,contract_sha256=None if ck.exists() else digest(raw),chunk_bytes=adapter.chunk,new_bytes=adapter.new_bytes,seconds=adapter.remaining())
  # Validate retained native binding independently before resume. A valid MAC
  # on a different scope's journal is not correspondence to this scope.
  if ck.exists():
   p=native.load(ck,adapter.key)
   require(all(p['binding'][n]['sha256']==files[str(q)] and p['binding'][n]['path']==str(q) for n,q in [('input',path),('model',desc),('contract',contract)]),'substituted native scope journal',category='INVALID-ACTION-CONTEXT')
  try:return native.execute(a)
  except native.RecoveryError as e:raise ValidationError(str(e),category='INVALID-EVIDENCE-DIGEST') from e
 r=scheduler.cached('native-links:'+scope,inputs,work,lambda r:r['complete'] or r['result']=='REJECTED',outputs=lambda:{str(ck):native.sha(ck)})
 if not r['complete']:
  if r['result']=='PAUSED':adapter.paused=True
  else:
   failure=r.get('failure') or {};raise ValidationError(failure.get('detail','native link validation unavailable'),category=failure.get('code','INCOMPLETE-EVIDENCE-UNIVERSE'))
 else:
  require(r['structural_rows']==proof['structural'] and r['potential_rows']==proof['potential'],'separate source-grounded native counts',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  require(r['complete_stream_sha256']==entry['sha256'],'native exact whole-file digest',category='INVALID-EVIDENCE-DIGEST')
 return r
