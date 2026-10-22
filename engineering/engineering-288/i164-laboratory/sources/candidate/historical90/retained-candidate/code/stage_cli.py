"""Offline fixture recovery only. No operational provider or network sender."""
import argparse,json
from pathlib import Path
from test_stages import Fixture
from anchor import enc,parse,Uncertain
p=argparse.ArgumentParser();p.add_argument('action',choices=['demo','recover']);p.add_argument('--directory',required=True);p.add_argument('--method',choices=['signPetition','signPetitionWithZKProof'],default='signPetition');a=p.parse_args();d=Path(a.directory)
if a.action=='demo':d.mkdir(parents=True,exist_ok=False)
else:
 saved=parse((d/'fixture.json').read_bytes());a.method=saved['method']
f=None
try:
 f=Fixture(d,a.method,create=a.action=='demo')
 if a.action=='demo':
  (d/'fixture.json').write_bytes(enc({'method':a.method,'config':f.cfg,'prerequisites':f.pre,'label':'ISOLATED-LAB-NOT-PILOT001'}))
  f.start();f.step();f.prepare()
  try:f.sch.send(f.u,f.sink,crash=True)
  except Uncertain:pass
 else:
  assert saved['config']==f.cfg and saved['prerequisites']==f.pre
 st=f.sch.recover(f.u);head=f.s.fresh()
 print(json.dumps({'result':'PASS-SAME-STAGED-SESSION-RECOVERY','state':st['status'],'session':st['sid'],'next_stage':st['index'],'counts':head['counts'],'partitions':head['partitions'],'release':False,'simulated_backend':True,'qualification_established':False,'actual_admission':False}))
finally:
 if f:f.close()
