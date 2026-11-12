"""Read-only reconciliation and durable byte packaging; never runs assertions."""
from pathlib import Path
import collections,hashlib,json,sys,zipfile
H=Path(__file__).resolve().parent;P=H.parent;bid=sys.argv[1];B=P/'batches'/bid
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
plan=json.loads((H/'FULL-PLAN.json').read_bytes());spec=next(x for x in json.loads((H/'BATCH-PLAN.json').read_bytes())['batches'] if x['id']==bid)
ex=json.loads((B/'exit.json').read_bytes());parse_errors=[]
def parse(b,n):
 try:return json.loads(b)
 except Exception as e:parse_errors.append({'path':n,'error':str(e),'identity':ident(b)});return None
rows=[r for f in sorted((B/'raw').glob('[0-9][0-9][0-9][0-9].json')) if (r:=parse(f.read_bytes(),str(f.relative_to(B)))) is not None]
progress=[r for i,b in enumerate((B/'raw/progress.jsonl').read_bytes().splitlines()) if (r:=parse(b,'progress:'+str(i))) is not None] if (B/'raw/progress.jsonl').exists() else []
stdout=[r for i,b in enumerate((B/'stdout.log').read_bytes().splitlines()) if (r:=parse(b,'stdout:'+str(i))) is not None]
stdout_rows=[r for r in stdout if 'original_sequence' in r];final=[r['result'] for r in stdout if r.get('event')=='RESULT']
result=parse((B/'raw/RESULT.json').read_bytes(),'RESULT') if (B/'raw/RESULT.json').exists() else None
same=rows==progress==stdout_rows
counts=dict(collections.Counter(r['status'] for r in rows));original=[r['original_sequence'] for r in rows]
for r in rows:
 expected=plan[r['original_sequence']-1]
 for k in ('name','layer','case','callsite','assertion_AST_sha256'):assert r[k]==expected[k],k
assert original==spec['sequences'][:len(original)] and all(x>145 for x in original)
streams={'stdout':bytearray(),'stderr':bytearray()}
for f in sorted((B/'chunks').glob('*.json')):
 m=json.loads(f.read_bytes());b=(B/m['path']).read_bytes();assert ident(b)=={k:m[k] for k in ['bytes','sha256']};streams[m['stream']].extend(b)
for n,b in streams.items():assert bytes(b)==(B/(n+'.log')).read_bytes()
complete=bool(same and not parse_errors and result and final==[result] and result['result']=='PASS' and original==spec['sequences'] and result['rows']==len(rows) and ex['returncode']==0 and not ex['timed_out'] and counts.get('FAIL',0)==0)
for n,pin in json.loads((P/'source/MANIFEST.json').read_bytes()).items():assert ident((P/'source'/n).read_bytes())==pin,n
rec={'batch':bid,'status':'COMPLETE' if complete else 'PARTIAL_OR_FAILED','counts':counts,'individual_rows':len(rows),'progress_rows':len(progress),'stdout_rows':len(stdout_rows),'rows_agree':same,'original_sequences':original,'planned_sequences':spec['sequences'],'explicit_exit':ex,'parse_errors':parse_errors,'result':result,'candidate_bytes_unchanged':True,'no_completed_assertions_replayed':True,'public_authentication':'UNEXECUTED','authenticated_constructed_path':'UNEXECUTED','full_public_negative_derivations':0}
(B/'RECONCILIATION.json').write_bytes(enc(rec))
members={f.relative_to(B).as_posix():ident(f.read_bytes()) for f in sorted(B.rglob('*')) if f.is_file() and f.name!='MANIFEST.json'};(B/'MANIFEST.json').write_bytes(enc(members))
zpath=P/('I164-res-null-test-1-continuation-'+bid+'.zip')
with zipfile.ZipFile(zpath,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(B.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(B).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(members)+1
 for n,pin in members.items():assert ident(z.read(n))==pin,n
summary={'filename':zpath.name,**ident(zpath.read_bytes()),'entries':len(members)+1,'batch_status':rec['status'],'counts':counts,'rows':len(rows),'exit':ex['returncode']}
(P/(bid+'-identity.json')).write_bytes(enc(summary));print(json.dumps(summary,indent=2));sys.exit(0 if complete else 2)
