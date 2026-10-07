"""External immutable scheduler maps. Small receipts bind exact database bytes."""
from pathlib import Path
import os
from .core import DiskMap,temporary,sha,sync
from v4_ingest.records import require
MARK='$cp4m_execution_catalog'

def freeze(mapping,root):
 db=temporary(root,'freeze-')
 try:
  expected=len(mapping)
  if isinstance(mapping,DiskMap):
   # Use SQLite's reviewed snapshot API for a disk source, not a live row
   # cursor interleaved with publication of other immutable generations.
   if not mapping.readonly:mapping.commit()
   source=mapping.connect()
   try:source.backup(db.db)
   finally:source.close()
  else:
   for k,v in mapping.items():db.add(k,v)
  require(len(db)==expected,'execution catalog snapshot completeness')
  db.commit();count=len(db);db.close();h=sha(db.path);dest=Path(root)/(h+'.catalog.sqlite');os.replace(db.path,dest);sync(dest)
  return {MARK:{'path':dest.name,'sha256':h,'count':count}}
 finally:
  db.close();db.path.unlink(missing_ok=True)

def thaw(value,scheduler):
 if not isinstance(value,dict) or set(value)!={MARK}:return value
 e=value[MARK];p=scheduler.root/e['path'];require(p.parent==scheduler.root,'receipt catalog containment');scheduler.verify(p,e['sha256'])
 db=DiskMap(p,True);require(len(db)==e['count'],'receipt catalog count');return db

def pack(p,root):
 q=dict(p)
 for k in ('prerequisites','artifacts'):q[k]=freeze(p[k],root)
 q['inputs']=dict(p['inputs'])
 if 'files' in q['inputs']:q['inputs']['files']=freeze(q['inputs']['files'],root)
 return q

def unpack(p,scheduler):
 for k in ('prerequisites','artifacts'):p[k]=thaw(p[k],scheduler)
 if 'files' in p['inputs']:p['inputs']['files']=thaw(p['inputs']['files'],scheduler)
 return p
