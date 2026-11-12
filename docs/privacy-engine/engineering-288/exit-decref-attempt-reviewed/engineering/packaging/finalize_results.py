"""Reconcile already saved records only; no candidate imports or checks."""
from pathlib import Path
import hashlib,json,zipfile,shutil,datetime
B=Path(__file__).resolve().parent;R=B/'results'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def write(n,v):
 p=R/n
 with p.open('xb') as f:f.write(enc(v) if type(v) is dict or type(v) is list else v.encode())
source=json.loads((B/'SOURCE-SAVE.json').read_bytes());assert ident((B/source['filename']).read_bytes())=={k:source[k] for k in ('bytes','sha256')}
groups=[];combined=[];layers={};all_complete=True
plan=json.loads((B/'candidate/tests/BATCH-PLAN.json').read_bytes())
for spec in plan['batches']:
 bid=spec['id'];p=R/bid
 if not (p/'RECONCILIATION.json').exists():groups.append({'batch':bid,'status':'NO_FINAL_RECONCILIATION'});all_complete=False;continue
 rec=json.loads((p/'RECONCILIATION.json').read_bytes());ex=json.loads((p/'exit.json').read_bytes());m=json.loads((p/'MANIFEST.json').read_bytes())
 assert {x.relative_to(p).as_posix() for x in p.rglob('*') if x.is_file()}==set(m)|{'MANIFEST.json'}
 for n,pin in m.items():assert ident((p/n).read_bytes())==pin,n
 rows=[json.loads(x.read_bytes()) for x in sorted((p/'raw').glob('[0-9][0-9][0-9][0-9].json'))]
 progress=[json.loads(x) for x in (p/'raw/progress.jsonl').read_text().splitlines()] if (p/'raw/progress.jsonl').exists() else []
 stdout=[json.loads(x)['row'] for x in (p/'stdout.log').read_text().splitlines() if json.loads(x).get('event')=='CONTROL']
 assert rows==progress==stdout and len(rows)==rec['rows'];assert rec['source_manifest']==ident((B/'candidate/MANIFEST.json').read_bytes())
 all_complete &= rec['status']=='COMPLETED' and ex['returncode']==0 and not ex['timed_out']
 group={'batch':bid,**rec,'exit':ex,'raw_root':str(p/'raw'),'recovered_root':bid.startswith('mutations-')};groups.append(group)
 for row in rows:
  combined.append({'batch':bid,'sequence':row['sequence'],'name':row['name'],'status':row['status'],'layer':row['layer'],'raw':bid+'/raw/%04d.json'%row['sequence']})
  layer=layers.setdefault(row['layer'],{});layer[row['status']]=layer.get(row['status'],0)+1
 assert len({(x['batch'],x['sequence']) for x in combined})==len(combined)
for root in [B/'candidate',B/'recovered']:
 m=json.loads((root/'MANIFEST.json').read_bytes())
 assert {x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file()}==set(m)|{'MANIFEST.json'}
 for n,pin in m.items():assert ident((root/n).read_bytes())==pin
counts={s:sum(x['status']==s for x in combined) for s in ('PASS','REJECTED','FAIL')}
write('SOURCE.json',source);write('GROUPS.json',groups);write('COMBINED-INDEX.json',combined)
write('RECONCILIATION.json',{'status':'COMPLETED' if all_complete else 'INCOMPLETE_OR_FAILED','rows':len(combined),'counts':counts,'groups':[{k:g[k] for k in ('batch','status','rows','counts') if k in g} for g in groups],'raw_progress_stdout_RESULT_exit':'agree for each completed group','layers':layers,'candidate_and_recovered_root':'all exact membership/hash identities unchanged','prior_campaigns_replayed':0,'public_authentication':'UNEXECUTED','authenticated_constructed_path':'UNEXECUTED','full_public_negative_derivations':0,'runtime_application_execution':0,'independent_acceptance':'PENDING','source':source})
write('FAILURES.json',{'new_batch_failures':[g for g in groups if g['status']!='COMPLETED'],'static_draft_and_inspection_qualifications':json.loads((B/'candidate/FAILURES.json').read_bytes()),'historical':'159 independent;145 timeout rows with missing final RESULT/FAILURE;171 continuation rows;one saved Ubuntu public positive remain separate. All older qualifications retained unchanged.','missing_records':'No missing historical or current records reconstructed.'})
write('CHANGES.json',json.loads((B/'candidate/CHANGES.json').read_bytes()))
write('RECOVERY.txt','''Retrieve exact source using SOURCE.json Library ID/link and verify size/SHA256/manifest. This results checkpoint contains only new source/model records and preserves their separate bounded batch exits. Verify flat MANIFEST.json and batch manifests. COMBINED-INDEX.json points to each raw row; GROUPS.json and RECONCILIATION.json record actual layers and reconciliation. Saved intermediate batch checkpoint IDs/identities are in SAVED-BATCH-CHECKPOINTS.json.\n\nReuse these completed checks. Do not rerun any source campaign, parent campaign or public run on handoff. New producer and mandatory adapter are fixed; both public authentication and authenticated constructed-path execution remain UNEXECUTED for these bytes. Actual returned predecessor basis cannot be substituted with these model fixtures or saved receipts. Any future public preparation/execution needs separate authorization.\n\nScope ends at conditional selected Py_DECREF(exit) attempt, before decrement completion/effects, error routing and false-branch operations. Runtime arrival, exit object state and qualified binary correspondence remain unestablished. Zero-count destructor completion unresolved. Parent producer prefix and runtime sources unchanged. Both acquisitions, eleven obligations,4/14UNKNOWN totals, DecisionB, retention and allowances persist. SOURCE-ONLY; cumulative envelope unadopted; backup kernel-only; streams UNCOMPUTED; readiness/final binding blocked; admission disabled. Independent review pending.\n''')
write('REPORT.txt',f"I164-EXIT-DECREF-ATTEMPT-1 new focused pass\nStatus: {'COMPLETED' if all_complete else 'INCOMPLETE_OR_FAILED'}\n{len(combined)} new controls: {counts}.\nFive separately bounded fresh processes; last two run from exact ZIP-recovered source. Raw rows/progress/stdout/RESULT/chunks/explicit exits reconcile. No historical assertion credit. No public or authenticated constructed-path execution. Source/model results do not establish runtime effects or independent acceptance.\n")
write('finalization-exit.json',{'exit':0,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Read-only reconciliation and result packaging; no candidate execution'})
# Intermediate compressed archives remain separately saved; include raw records once.
members={p.relative_to(R).as_posix():ident(p.read_bytes()) for p in sorted(R.rglob('*')) if p.is_file() and p.suffix!='.zip'}
write('MANIFEST.json',members)
archive=B/'I164-exit-decref-attempt-1-results.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in sorted(set(members)|{'MANIFEST.json'}):z.write(R/n,n)
with zipfile.ZipFile(archive) as z:
 assert not z.testzip() and set(z.namelist())==set(members)|{'MANIFEST.json'}
 for n,pin in members.items():assert ident(z.read(n))==pin
print(json.dumps({'file':str(archive),'identity':ident(archive.read_bytes()),'entries':len(members)+1,'rows':len(combined),'counts':counts,'status':'COMPLETED' if all_complete else 'INCOMPLETE_OR_FAILED'},indent=2))
