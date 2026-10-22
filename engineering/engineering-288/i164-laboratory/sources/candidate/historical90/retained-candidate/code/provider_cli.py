"""Only isolated laboratory state. No network, credentials or operational mode."""
import argparse,json
from pathlib import Path
from anchor import enc
from test_provider import Fixture
p=argparse.ArgumentParser();p.add_argument('action',choices=['fixture','recover']);p.add_argument('directory',type=Path);a=p.parse_args()
if a.action=='fixture':
 if a.directory.exists():raise SystemExit('REFUSE-EXISTING-DIRECTORY')
 f=Fixture(a.directory);f.sent();packet=f.packet(1);result=f.decode(packet)
 f.x.save_outcome_evidence(f.u,'observe',packet)
 (a.directory/'provider-evidence.json').write_bytes(enc(packet));(a.directory/'policy-LAB-ONLY.json').write_bytes(enc(f.policy));(a.directory/'verification.json').write_bytes(enc(result))
else:
 if not a.directory.is_dir():raise SystemExit('MISSING-STATE-NO-INIT')
 f=Fixture(a.directory,False);f.x.internal_terminal_repair();f.x.internal_terminal_repair()
s=f.s.fresh();print(json.dumps({'result':'PASS-CONDITIONAL-'+a.action.upper(),'executor':f.x.executor.states[f.u]['status'],'counts':s['counts'],'partitions':s['partitions'],'laboratory_assumptions':True,'technical_finality_reexecuted':False,'qualification_established':False,'actual_admission':False}));f.close()
