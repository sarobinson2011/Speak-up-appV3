"""Read-only reconciliation of this review's already completed processes."""
from pathlib import Path
import json,sys,collections
sys.path.insert(0,str(Path(__file__).parent))
from integrity import BASE,enc,ident,file_ident
out={}
for label in ('preparation','slot1-monitor','public-recovered'):
 p=BASE/'processes'/label;d=BASE/'results'/label;r=json.loads((d/'RESULT.json').read_bytes());ex=json.loads((p/'exit-status.json').read_bytes());assert ex['returncode']==0 and not ex['timed_out'] and r['error'] is None
 rows=r['rows'];progress=[json.loads(x) for x in (d/'progress.jsonl').read_text().splitlines()] if (d/'progress.jsonl').exists() else [];individual=[json.loads(x.read_bytes()) for x in sorted((d/'rows').glob('*.json'))]
 stdout=(p/'stdout.log').read_bytes();parsed=[json.loads(x[4:]) for x in stdout.decode().splitlines() if x.startswith('ROW ')]
 assert rows==progress==individual==parsed and len(rows)==r['checks'] and [x['ordinal'] for x in rows]==list(range(1,len(rows)+1))
 capture=json.loads((p/'capture.json').read_bytes());streams={}
 for stream in ('stdout','stderr'):
  chunks=[x for x in capture if x['stream']==stream];pieces=[]
  for x in chunks:
   data=(p/x['file']).read_bytes();assert ident(data)=={k:x[k] for k in ('bytes','sha256')};pieces.append(data)
  whole=(p/(stream+'.log')).read_bytes();assert whole==b''.join(pieces);streams[stream]={'identity':ident(whole),'chunks':len(chunks),'exact':True}
 out[label]={'rows':len(rows),'kinds':dict(collections.Counter(x['result'] for x in rows)),'layers':dict(collections.Counter(x['layer'] for x in rows)),'all_RESULT_progress_individual_stdout_rows_agree':True,'streams':streams,'exit':ex,'RESULT_identity':file_ident(d/'RESULT.json')}
 if label=='public-recovered':
  codes={};precise=[]
  for row in rows:
   if row['result']!='REJECTED':continue
   code=row['error'];layer=row['layer']
   if code=='WC-MANDATORY-RELATIONS':detail='Public receipt shape gate before inputs or predecessor derivation.'
   elif code=='WC-STALE-OR-ALTERED-RECEIPT':detail='Exact-byte receipt comparison with assembly from actual authenticated basis; no new public derivation.'
   elif code.startswith('WC-OUTPUT-TYPE'):detail='Producer exact-type output gate before normalizing/comparing submitted output.'
   elif code.startswith('WC-OUTPUT-CORRESPONDENCE'):detail='Producer exact typed output comparison against recomputation using actual authenticated parent premises.'
   elif code.startswith(('WC-ORDER','WC-UNREACHED-STEPS','WC-UNKNOWN-CONTINUITY')):detail='Producer ordered conditional projection gate with actual authenticated parent premises and constructed outcomes.'
   elif code.startswith('WC-PARENT-INVOCATION'):detail='Mandatory constructed input binding gate before the selected parent mutant would be revalidated.'
   elif code.startswith(('WC-VALIDATED-PARENT','WC-VALIDATED-DESTINATION')):detail='Mandatory constructed premises compare after actual unchanged predecessor validates the selected parent case.'
   elif code.startswith('WC-VALIDATED:'):detail='Producer submitted premises compared with the previously authenticated selected parent premises.'
   elif code.startswith('WC-CLAIMS:'):detail='Adapter exact-type semantic-claim gate before comparison.'
   else:detail='Adapter actual-authenticated-basis semantic/source/evidence comparison; exact error code retained.'
   precise.append({'ordinal':row['ordinal'],'check':row['check'],'error':code,'recorded_layer':layer,'precise_layer':detail,'full_public_negative_derivation':False})
  (BASE/'results/rejection-layers.json').write_bytes(enc(precise))
  assert json.loads((d/'input-root.json').read_bytes())==json.loads((d/'final-root.json').read_bytes())
  out[label]['input_final_root_equal']=True
out['accounting_policy']='Separate groups; QUALIFIED is not PASS. Preparation carries no authentication credit. No Engineering or historical controls are included.'
(BASE/'results/independent-reconciliation.json').write_bytes(enc(out));print(enc(out).decode(),flush=True)
