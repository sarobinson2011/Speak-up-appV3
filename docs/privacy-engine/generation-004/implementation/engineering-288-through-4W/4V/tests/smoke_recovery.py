"""Fresh-extraction smoke check; bounded small oracle, no old regression suite."""
import json,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'tests')]
from adapter.core import *
from oracle import make,manifest,digest
with tempfile.TemporaryDirectory() as tmp:
 d=Path(tmp);f=make(d/'inputs');keygen(d/'key');initialize(d/'job',d/'key',manifest(f),113)
 with Job(d/'job',d/'key') as j:
  r=j.step(17,3);assert not r['complete'] and r['offset']==17
 (d/'job'/'spool.bin').unlink() # force exact bounded regeneration after extraction
 with Job(d/'job',d/'key') as j:
  for i in range(30):
   r=j.step(chunk_bytes=7)
   if r['complete']:break
  assert r['complete'] and r['whole_stream_sha256']==digest(f['text'])
  assert (r['structural'],r['potential'])==(f['structural'],f['potential'])
  assert j.state['metrics']['spool_regenerations']==1
  print(json.dumps({'result':'PASS-FRESH-SMALL-RECOVERY','rows':r['rows'],'structural':r['structural'],'potential':r['potential'],'bytes':r['offset'],'whole_stream_sha256':r['whole_stream_sha256'],'spool_regenerations':1,'actual_admission':False}))
