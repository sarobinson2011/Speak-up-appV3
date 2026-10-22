"""New isolated LAB fixture or recovery of that fixture only; no network."""
import argparse,json,shutil
from pathlib import Path
import wire,backend,sole_service,connected,runtime
from test_wire import Tests,KEY,EXEC_KEY,SERVER,PUBLIC
from anchor import enc,parse,Uncertain
p=argparse.ArgumentParser();p.add_argument('action',choices=['demo','recover']);p.add_argument('--directory',required=True);a=p.parse_args();d=Path(a.directory)
b=c=x=None
try:
 if a.action=='demo':
  d.mkdir(parents=True,exist_ok=False);t=Tests();t.setUp()
  try:
   t.retire();t.x.seal_conditional(t.u,'seal')
   def drop(req,res):
    q=parse(req,wire.REQUEST_LIMIT)['request']
    if q['method']=='commit' and q['args']['kind']=='ATTEMPT':
     (d/'lost-ack-request.json').write_bytes(req);(d/'lost-ack-response.json').write_bytes(res);raise OSError('LAB ACK LOSS')
    return res
   t.channel.filter=drop
   try:t.x.submit_conditional(t.u,'attempt',t.sink)
   except Uncertain:pass
   assert not t.sink.sent;t.channel.filter=None;t.x.recover()
   (d/'fixture.json').write_bytes(enc({'config':t.cfg,'prerequisites':t.pre}))
   t.x.close();t.client.close();t.b.close()
   shutil.copytree(t.p,d/'state')
  finally:t.tearDown()
 v=json.loads((d/'fixture.json').read_bytes());cfg=v['config'];pre=v['prerequisites'];state=d/'state'
 if not (state/'service.db').is_file():raise ValueError('MISSING-SERVICE')
 b=backend.SimulatedBackend(state/'service.db',cfg['backend']);s=sole_service.Service(b,cfg)
 ing=wire.Ingress(s,pre,{'executor':(EXEC_KEY,['executor']),'fixture':(KEY,['executor','lab-result-provider'])},SERVER)
 c=wire.Client(wire.OfflineChannel(ing),cfg,'fixture',KEY,PUBLIC,state/'wire.db',policy=ing.policy);x=connected.Connected(state/'local',c,pre)
 x.recover();assert x.internal_terminal_repair() is None;head=c.fresh()
 print(json.dumps({'result':'PASS-OFFLINE-WIRE-RECOVERY','binding':c.binding,'service_head':head['head'],'counts':head['counts'],'partitions':head['partitions'],'status':x.executor.states['LAB-U-1']['status'],'release':False,'authentication':'LAB-CREDENTIALS-ONLY','actual_admission':False}))
finally:
 if x:x.close()
 if c:c.close()
 if b:b.close()
