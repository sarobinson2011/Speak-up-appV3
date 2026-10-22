"""Isolated fixture creation/reopen. No operational jobs, network or credentials."""
import argparse,json
from pathlib import Path
import backend,sole_service,connected,runtime
from anchor import enc,Uncertain
from test_connected import config,intent
from connected import Connected,OfflineSink,implementation
from sole_service import Service
from backend import SimulatedBackend
p=argparse.ArgumentParser();p.add_argument('action',choices=['demo','recover']);p.add_argument('--directory',required=True);a=p.parse_args();d=Path(a.directory)
b=x=None
try:
 if a.action=='demo':
  d.mkdir(parents=True,exist_ok=False);c=config();pre={k:c['prerequisites'][v] for k,v in [('model','model'),('profile','profile'),('config','configuration')]}
  desc={'kind':'OFFLINE-SIMULATION','table_id':'LAB-RECOVERY','service_identity':'LAB-SERVICE'}
  cfg={'pilot':'LAB-SOLE-ANCHOR-RECOVERY','session':'LAB-ONE','implementation':implementation(runtime.Guard(),pre),'backend':desc,'origin':'0'*64,'limits':{'attempt':2,'query':2,'snapshot':2,'staging_query':2,'staging_snapshot':2}}
  (d/'fixture.json').write_bytes(enc({'config':cfg,'prerequisites':pre}))
  b=SimulatedBackend(d/'service.db',desc);s=Service(b,cfg);s.genesis({'executor_head':'0'*64,'transport_head':'0'*64,'transport_seq':0})
  x=Connected(d/'local',s,pre,True);old=(d/'local/executor.db').read_bytes()
  try:x.retire('LAB-U-1',intent(c),'retire',crash='ack_loss')
  except Uncertain:pass
  x.close();(d/'local/executor.db').write_bytes(old)
  x=Connected(d/'local',s,pre);x.seal_conditional('LAB-U-1','seal');sink=OfflineSink()
  try:x.submit_conditional('LAB-U-1','attempt',sink,crash='ack_loss')
  except Uncertain:pass
  assert not sink.sent
 else:
  v=json.loads((d/'fixture.json').read_bytes());cfg=v['config'];pre=v['prerequisites']
  # Never create a missing service on recovery.
  if not (d/'service.db').is_file():raise ValueError('MISSING-SERVICE')
  b=SimulatedBackend(d/'service.db',cfg['backend']);s=Service(b,cfg);x=Connected(d/'local',s,pre)
 x.recover();assert x.internal_terminal_repair() is None;state=s.fresh()
 print(json.dumps({'result':'PASS-CONDITIONAL-SOLE-ANCHOR-RECOVERY','binding':s.binding,'head':state['head'],'executor_head':x.executor.head,'counts':state['counts'],'partitions':state['partitions'],'U_status':x.executor.states['LAB-U-1']['status'],'recovery_release':False,'operational_assurance':False,'actual_admission':False}))
finally:
 if x:x.close()
 if b:b.close()
