"""Offline fixture and private bookkeeping diagnostic only; not a public observation API."""
import argparse,json
from pathlib import Path
from test_outcome import Fixture
from anchor import enc,sha
p=argparse.ArgumentParser();p.add_argument('mode',choices=['fixture','recover']);p.add_argument('directory');a=p.parse_args();d=Path(a.directory)
if a.mode=='fixture':
 if d.exists():raise SystemExit('Refuse existing directory; never reset a session')
 f=Fixture(d);f.sent();packet=f.packet(1);result=f.decode(packet)
 (d/'evidence.json').write_bytes(enc(packet));(d/'decoded.json').write_bytes(enc(result))
 for k in ['near_hex','rpc_request_hex','rpc_response_hex']:(d/(k.removesuffix('_hex')+'.bin')).write_bytes(bytes.fromhex(packet['claim'][k]))
 f.x.save_outcome_evidence(f.u,'observe',packet);print(json.dumps({'result':'SAVED-CONDITIONAL-EVIDENCE-REPAIR-PENDING','evidence_sha256':sha(enc(packet)),'actual_admission':False}));f.close()
else:
 f=Fixture(d,False);before=f.s.fresh();f.x.internal_terminal_repair();f.x.internal_terminal_repair();s=f.s.fresh()
 assert before['counts']==s['counts'] and before['partitions']==s['partitions']
 print(json.dumps({'result':'PASS-PRIVATE-CONDITIONAL-REPAIR','executor_status':f.x.executor.states[f.u]['status'],'counts':s['counts'],'partitions':s['partitions'],'new_observation':False,'new_send':False,'authoritative_terminal':False,'actual_admission':False}));f.close()
