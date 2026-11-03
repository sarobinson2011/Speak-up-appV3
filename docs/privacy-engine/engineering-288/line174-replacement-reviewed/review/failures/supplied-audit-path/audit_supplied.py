"""Read-only supplied-record reconciliation; no control/candidate execution."""
from pathlib import Path
import sys,json,collections
sys.path.insert(0,str(Path(__file__).parent))
from integrity import AREA,BASE,enc,ident,file_ident
root=AREA/'final-records';report={}
for group,label,total,expected in [('replacement-source-corrected','replacement-source',29,{'PASS':13,'REJECTED':16}),('replacement-public','replacement-public',314,{'PASS':142,'REJECTED':172})]:
 d=root/'results'/group;p=root/'processes'/label
 result=json.loads((d/'RESULT.json').read_bytes());rows=result['rows'];progress=[json.loads(x) for x in (d/'progress.jsonl').read_text().splitlines()];individual=[json.loads(q.read_bytes()) for q in sorted((d/'rows').glob('*.json'))]
 stdout=(p/'stdout.log').read_bytes();sr=[json.loads(s[6:]) for s in stdout.decode().splitlines() if s.startswith('CHECK ')]
 assert len(rows)==total and rows==progress==individual==sr and [x['ordinal'] for x in rows]==list(range(1,total+1))
 kinds=dict(collections.Counter(x['result'] for x in rows));assert kinds==expected
 exit=json.loads((p/'exit.json').read_bytes());assert exit['exit']==0 and not exit['timed_out'] and result['error'] is None
 capture=json.loads((p/'capture.json').read_bytes());stream_facts={}
 for stream in ('stdout','stderr'):
  original=(p/(stream+'.log')).read_bytes();saved=(p/(stream+'-captured.bin')).read_bytes();assert original==saved and ident(saved)==capture['streams'][stream]==exit['streams'][stream]
  chunks=capture['chunks'][stream];combined=[]
  for x in chunks:
   chunk=(p/x['path']).read_bytes();assert ident(chunk)==x['identity'];combined.append(chunk)
  assert b''.join(combined)==saved
  stream_facts[stream]={'identity':ident(original),'chunk_count':len(chunks),'log_captured_chunks_exact':True}
 report[label]={'RESULT_progress_individual_stdout_rows':total,'kinds':kinds,'all_rows_agree':True,'exit':exit,'streams':stream_facts,'actual_layers':dict(collections.Counter(x['layer'] for x in rows)),'result_identity':file_ident(d/'RESULT.json'),'campaign_replayed':False}
# The source records were already embedded before the public run: compare retained copies.
 sourcecopy=AREA/'construction/new/results'/group
 if sourcecopy.exists():
  for q in sourcecopy.rglob('*'):
   if q.is_file():assert q.read_bytes()==(d/q.relative_to(sourcecopy)).read_bytes()
  report[label]['unchanged_pre_run_source_records']=True
failure=AREA/'construction/new/failures/receipt-format'
report['preparation_failure']={'path':'construction/new/failures/receipt-format','files':{q.relative_to(failure).as_posix():file_ident(q) for q in failure.rglob('*') if q.is_file()},'controls':0,'reason':'WC-MANDATORY-RELATIONS','exit':1,'not_successful_public_validation':True}
report['history']={'earlier_missing_attempt':'UNKNOWN; reported36 checks give no verification credit for new bytes','pre_run_public_not_started':'historical, not overwritten by final records','retained_host_50_0_2':'separate from current50.0.0','no_full_public_negative_derivation':True,'all_historical_qualifications':'retained unchanged inside input/dependencies; no aggregate'}
(BASE/'results/supplied-audit.json').write_bytes(enc(report));print(enc(report).decode(),flush=True)
