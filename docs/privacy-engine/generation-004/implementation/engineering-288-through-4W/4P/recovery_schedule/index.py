"""Reuse canonical JSON index only after exact input and database byte checks."""
import sqlite3,os,tempfile,shutil
from pathlib import Path
from semantic_stream.storage import Document
from v4_ingest.records import digest,require
from .state import ACTIVE,sha

def parse(store,blob,original):
 scheduler=ACTIVE.get()
 if scheduler is None:return original(store,blob)
 identity={'sha256':blob.sha(),'bytes':len(blob)};label='semantic-index:'+identity['sha256']
 old=scheduler.read(label)
 if old is not None:
  require(old['inputs']==identity and old['complete'],'incompatible/incomplete semantic index receipt')
  name=old['result']['database'];path=scheduler.root/name
  require(path.parent==scheduler.root and set(old['artifacts'])=={str(path)},'semantic database containment')
  scheduler.verify(path,old['artifacts'][str(path)])
  info={'index':str(path),'index_sha256':old['artifacts'][str(path)],'input_sha256':identity['sha256'],'input_path':str(blob.path),'start':blob.start,'size':len(blob),'binding':store.binding,'receipt':label,'owner_instance':store.instance}
  d=Document.reopen(store,blob,info);store.pool.connection(d);store.documents_reused+=1
  scheduler.event(label,'REUSED-CANONICAL-INDEX-EXACT-BYTES');return d.value(0)
 result=original(store,blob)
 doc=store.last_document;dest=scheduler.root/(scheduler.name(label)+'.sqlite')
 # DB is complete/committed only after canonical EOF validation.
 source=doc.index_path;tmp=dest.with_suffix('.part');shutil.copyfile(source,tmp)
 with tmp.open('rb') as f:os.fsync(f.fileno())
 os.replace(tmp,dest)
 from link_recovery.cli import fsync_dir
 fsync_dir(dest.parent)
 scheduler.save(label,identity,{'database':dest.name},True,artifacts={str(dest):sha(dest)})
 doc.index_path=dest;doc.index_sha=sha(dest);doc.receipt=label
 import hashlib,json
 doc.identity=hashlib.sha256(json.dumps(doc.descriptor(),sort_keys=True).encode()).hexdigest()
 return result
