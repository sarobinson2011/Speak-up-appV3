"""Catalog transport adapters; source ownership is still checked by the collector."""
from pathlib import Path
from v4_ingest.records import require,primitive
from integrated_auth.adapters import checked_path
from .core import acquire,DiskMap
MARK='$cp4m_directory'

def binding(m,t):
 return {'source_id':t['source_id'],'source_sha256':t['source_sha256'],'model_sha256':m['canonical_model_sha256'],'profile_sha256':m['request']['profile_digest'],'contract_sha256':m['contract']['sha256'],'phase':m['request']['phase'],'attempt':m['request']['attempt'],'mapping_digest':m['request']['mapping_digest']}

def resolve(value,kind,bound,base,root,key,job,handles,tick=None):
 if not isinstance(value,dict) or set(value)!={MARK}:return value
 e=value[MARK];path=checked_path(base,e)
 def check(k,v):
  if kind in ('materials','source_objects'):
   primitive('DIGEST',k);checked_path(base,v);require(k==v['sha256'],'catalog source digest key',category='INVALID-EVIDENCE-DIGEST');primitive('DIGEST',v['sha256']);require(type(v['bytes']) is int and v['bytes']>=0,'catalog file length')
  elif kind=='occurrence_bindings':
   require(set(v)=={'owner_source_id','source_sha256','source_anchor','material_sha256'},'exact source reference');require(v['owner_source_id']==bound['source_id'] and v['source_sha256']==bound['source_sha256'],'catalog owning source join',category='INVALID-ACTION-CONTEXT')
   primitive('ID',v['source_anchor']);primitive('DIGEST',v['material_sha256'])
 db=acquire(path,e,kind,bound,root,key,job,tick=tick,validate=check);return db

def hydrate(m,t,base,root,key,job,handles,tick=None):
 # Independent failures remain collectible; no failed map yields evidence.
 from integrated_auth.collector import Paused
 b=binding(m,t);errors=[];t=dict(t.items())
 def one(value,kind):
  try:return resolve(value,kind,b,base,root,key,job,handles,tick)
  except Paused:raise
  except (ValueError,OSError) as e:errors.append(e);return {}
 for name in ('materials','source_objects'):
  try:
   if set(m[name])=={MARK}:require(t.get('file_directories',{}).get(name)==m[name],'independent source-file directory binding',category='INVALID-ACTION-CONTEXT')
  except ValueError as e:errors.append(e);m[name]={};continue
  m[name]=one(m[name],name)
 m['request']['occurrence_bindings']=one(m['request']['occurrence_bindings'],'occurrence_bindings')
 t['occurrence_bindings']=one(t['occurrence_bindings'],'occurrence_bindings')
 return m,t,errors
