"""Disk exact equality. Hash buckets accelerate candidates, never prove equality."""
import sqlite3,os,shutil
from pathlib import Path
from semantic_stream.storage import Blob
from v4_ingest.records import require
from .codec import compare

def bucket(blob):return blob.sha()

class ExactValues:
 def __init__(self,path,store,binding):
  self.path=Path(path);self.store=store;self.binding=binding
  self.db=sqlite3.connect('file:'+str(path)+'?mode=ro',uri=True);self.db.execute('pragma cache_size=-256');store.docs.append(self)
 def close(self):self.db.close()
 def group(self,token):
  row=self.db.execute('select g from assignments where token=?',(token,)).fetchone();require(row is not None,'missing owning occurrence',category='INCOMPLETE-EVIDENCE-UNIVERSE');return row[0]
 def sha(self,token):return self.db.execute('select sha from groups join assignments using(g) where token=?',(token,)).fetchone()[0]
 def count(self,tokens):
  # Model-sized count map, never value-sized or pair-sized memory.
  counts={}
  for t in tokens:
   g=self.group(t['id']);counts[g]=counts.get(g,0)+1
  return sum(n*(n-1)//2 for n in counts.values())

def build(path,rows,store,binding,tick=None):
 path=Path(path);tmp=path.with_suffix('.part');tmp.unlink(missing_ok=True)
 db=sqlite3.connect(tmp);db.execute('pragma cache_size=-256');db.execute('pragma temp_store=file')
 db.executescript('create table groups(g integer primary key,bucket text,n integer,file text,sha text); create index buckets on groups(bucket,n); create table assignments(token text primary key,g integer);')
 artifacts={};nextgroup=0
 try:
  for token,blob in rows:
   if tick:tick()
   h=bucket(blob);n=len(blob);group=None
   for g,name in db.execute('select g,file from groups where bucket=? and n=? order by g',(h,n)):
    if compare(blob,Blob(store,path.parent/name))==0:group=g;break
   if group is None:
    group=nextgroup;nextgroup+=1;dest=path.with_name(path.stem+'-value-'+str(group)+'.bin');part=dest.with_suffix('.part')
    with part.open('wb') as f:
     for b in blob.chunks():f.write(b)
     f.flush();os.fsync(f.fileno())
    os.replace(part,dest);actual=blob.sha();artifacts[str(dest)]=actual
    db.execute('insert into groups values(?,?,?,?,?)',(group,h,n,dest.name,actual))
   try:db.execute('insert into assignments values(?,?)',(token,group))
   except sqlite3.IntegrityError:require(False,'duplicate/conflicting occurrence assignment',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  db.commit();db.close()
  with tmp.open('rb') as f:os.fsync(f.fileno())
  os.replace(tmp,path)
  from link_recovery.cli import fsync_dir
  from recovery_schedule.state import sha
  fsync_dir(path.parent);artifacts[str(path)]=sha(path)
  return artifacts
 finally:
  try:db.close()
  finally:tmp.unlink(missing_ok=True)
