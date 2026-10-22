"""Acquires saved reviewed evidence; no candidate lifecycle or signing call."""
import sys,json,sqlite3
from pathlib import Path
from common import *
from ingest import acquire
base=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(exist_ok=True,parents=True)
names=['feasible-ord-success','feasible-ord-reverted','feasible-zk-success','feasible-zk-reverted','ord-early','zk-early','ord-finalized','zk-finalized','unknown','no-resigning']
names += ['exit-'+k for k in ['before_decision_commit','after_decision_commit','after_sign_claim','before_signature_commit','after_signature_commit','before_release_commit','after_release_commit','before_retry_commit','after_retry_commit','before_observe_commit','after_observe_commit']]
names += ['failed-'+m+'-'+k for m in ['ord','zk'] for k in ['begin','append','finalize','proceed','abandon','cleanup']]
names += ['ord-abandon','zk-abandon','ord-cleanup','zk-cleanup']
receipts=[]
for n in names:
 p=base/(n+'.db');o=base/(n+'.owners.db')
 c=sqlite3.connect(p.resolve().as_uri()+'?mode=ro&immutable=1',uri=True)
 head=json.loads(c.execute('select raw from head').fetchone()[0]);packets=[json.loads(b)['request'] for b, in c.execute('select request from journal')];c.close()
 retire=next(r for r in packets if r['method']=='retire');i=json.loads(bytes.fromhex(retire['body']['intent_hex']));op=next(r for r in packets if r['method']=='open');msg=bytes.fromhex(op['body']['message_hex']);context=json.loads(msg[41:])['bindings'];config={'version':VERSION,'pilot':retire['pilot'],'session':retire['session'],'start_nonce':int(i['nonce'])-(len(msg)+511)//512-2,'manager':context['auth_manager'],'model':i['model'],'profile':i['profile'],'config':i['config']}
 x=acquire(p,o,config,head['head']);raw=enc(x);(out/(n+'.json')).write_bytes(raw);receipts.append({'name':n,'source_db_sha256':sha(p.read_bytes()),'source_ownership_sha256':sha(o.read_bytes()),'export_sha256':sha(raw),'expected_head':head['head'],'expected_head_authority':'saved fixture only, not operational protected anchor','source_execution':'PRIOR SAVED ENGINEERING RESULT; not rerun'})
(out/'INDEX.json').write_bytes(enc(receipts));print(len(receipts))
